"""Matched local/pooled regression on a fixed historical customer panel."""
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from .data import ROOT,dst_days,write_json
from .common import start_run,finish_run,save_frame,markdown_table,plt

MODELS=['yesterday','last_week','local_ridge','pooled_ridge']
FEATURES=['lag24','lag168','lag336','previous_day_mean','hour_sin','hour_cos','dow_sin','dow_cos','month_sin','month_cos']


def safe_hours(index):
    days=pd.date_range(index.min().normalize()-pd.Timedelta(days=14),index.max().normalize(),freq='D')
    flags=pd.Series(dst_days(days),index=days).rolling(15,min_periods=1).max().astype(bool)
    return ~flags.reindex(index.normalize()).to_numpy()


def features(series):
    idx=series.index
    daily=series.resample('D').mean().shift(1)
    result=pd.DataFrame({'lag24':series.shift(24),'lag168':series.shift(168),'lag336':series.shift(336),
                        'previous_day_mean':daily.reindex(idx.normalize()).to_numpy()},index=idx)
    for label,value,period in [('hour',idx.hour,24),('dow',idx.dayofweek,7),('month',idx.month-1,12)]:
        result[label+'_sin']=np.sin(2*np.pi*value/period)
        result[label+'_cos']=np.cos(2*np.pi*value/period)
    return result


def normalized_x(frame,scale):
    x=frame.to_numpy(copy=True)
    x[:,:4]/=scale
    return x


def fit_month(panel,month):
    """All fit targets precede month; each forecast day's features precede its origin."""
    end=month+pd.offsets.MonthBegin(1)
    train_mask=(panel.index>=month-pd.Timedelta(days=365))&(panel.index<month)&safe_hours(panel.index)
    test_mask=(panel.index>=month)&(panel.index<end)
    xs=[];ys=[];test_x=[];records=[];params=[]
    for client_no,client in enumerate(panel.columns):
        f=features(panel[client])
        valid=f.notna().all(axis=1).to_numpy()
        train=train_mask&valid
        test=test_mask&valid
        scale=float(panel.loc[train,client].mean())
        if not np.isfinite(scale) or scale<=0: raise ValueError('Invalid training scale')
        x=normalized_x(f.loc[train],scale); y=panel.loc[train,client].to_numpy()/scale
        xt=normalized_x(f.loc[test],scale)
        local=Ridge(alpha=.001*len(y),solver='cholesky').fit(x,y)
        raw=local.predict(xt)*scale
        rec=pd.DataFrame({'hour':panel.index[test],'client':client,'actual':panel.loc[test,client].to_numpy(),
            'safe':safe_hours(panel.index)[test],'yesterday':f.loc[test,'lag24'].to_numpy(),
            'last_week':f.loc[test,'lag168'].to_numpy(),'local_raw':raw,'local_ridge':np.maximum(raw,0)})
        records.append(rec)
        indicators=np.zeros((len(x),len(panel.columns))); indicators[:,client_no]=1
        test_ind=np.zeros((len(xt),len(panel.columns))); test_ind[:,client_no]=1
        xs.append(np.column_stack([x,indicators]));ys.append(y)
        test_x.append((np.column_stack([xt,test_ind]),scale))
        params.append({'client':client,'scale_kw':scale,'n_train':int(train.sum()),'last_train':str(panel.index[train][-1]),
                       'intercept':float(local.intercept_),'coefficients':local.coef_.tolist()})
    pooled_x=np.vstack(xs); pooled_y=np.concatenate(ys)
    pooled=Ridge(alpha=.001*len(pooled_y),solver='cholesky').fit(pooled_x,pooled_y)
    for rec,(xt,scale) in zip(records,test_x):
        raw=pooled.predict(xt)*scale
        rec['pooled_raw']=raw;rec['pooled_ridge']=np.maximum(raw,0)
    metadata={'month':str(month.date()),'features':FEATURES,'local':params,'pooled':{'n_train':len(pooled_y),
              'intercept':float(pooled.intercept_),'coefficients':pooled.coef_.tolist(),'client_indicators':panel.columns.tolist()}}
    return pd.concat(records,ignore_index=True),metadata


def summarize(frame,means,peaks):
    if frame.empty or not np.isfinite(frame[['actual',*MODELS]].to_numpy()).all():
        raise ValueError('All matched target/prediction values must be finite')
    if frame.duplicated(['hour','client']).any():
        raise ValueError('Duplicate hour/customer observation')
    if set(frame.client)!=set(means.index) or not (frame.groupby('hour').client.nunique()==len(means)).all():
        raise ValueError('Incomplete matched customer panel')
    if not np.isfinite(means).all() or (means<=0).any():
        raise ValueError('Invalid normalization means')
    result={}
    for model in MODELS:
        individual={}
        for client,g in frame.groupby('client'):
            error=g[model]-g.actual
            peak=g.actual>peaks[client]
            individual[client]={'n':len(g),'mae_kw':float(abs(error).mean()),'bias_kw':float(error.mean()),
                'normalized_mae':float(abs(error).mean()/means[client]),'peak_n':int(peak.sum()),
                'peak_mae_kw':float(abs(error[peak]).mean()) if peak.any() else None}
        aggregate=frame.groupby('hour')[[model,'actual']].sum()
        result[model]={'customers':individual,'macro_normalized_mae':float(np.mean([x['normalized_mae'] for x in individual.values()])),
            'aggregate_mae_kw':float(abs(aggregate[model]-aggregate.actual).mean()),
            'aggregate_bias_kw':float((aggregate[model]-aggregate.actual).mean())}
    return result


def run():
    out,started=start_run('electricity')
    panel=pd.read_csv(ROOT/'data/snapshots/electricity-hourly-panel.csv.gz',index_col=0,parse_dates=True)
    records=[]; parameters=[]
    for month in pd.date_range('2013-01-01','2014-12-01',freq='MS'):
        print(f'Electricity fit {month:%Y-%m}',flush=True)
        frame,params=fit_month(panel,month); records.append(frame);parameters.append(params)
    predictions=pd.concat(records,ignore_index=True)
    predictions['split']=np.where(predictions.hour.dt.year==2013,'development','test')
    save_frame(predictions,out/'predictions.csv.gz')
    write_json(out/'parameters.json',{'monthly_fits':parameters})
    means=panel.loc['2012'].mean();peaks=panel.loc['2012'].quantile(.9)
    scores={}
    for split in ['development','test']:
        f=predictions.loc[predictions.split==split]
        scores[split]={'primary':summarize(f.loc[f.safe],means,peaks),'all_dates_sensitivity':summarize(f,means,peaks),
                      'hour_customer_rows':len(f),'excluded_hour_customer_rows':int((~f.safe).sum()),
                      'negative_raw_predictions':{m:int((f[m]<0).sum()) for m in ['local_raw','pooled_raw']}}
    primary=scores['test']['primary']
    customers=panel.columns.tolist()
    local=np.array([primary['local_ridge']['customers'][c]['normalized_mae'] for c in customers])
    pooled=np.array([primary['pooled_ridge']['customers'][c]['normalized_mae'] for c in customers])
    scores['test']['pooled_better_customers']=int((pooled<local).sum())
    scores['test']['pooled_worse_customers']=int((pooled>local).sum())
    write_json(out/'metrics.json',scores)
    delta=pooled-local
    order=np.argsort(delta)
    fig,axes=plt.subplots(1,2,figsize=(12,8),gridspec_kw={'width_ratios':[1.2,1]})
    ordered=delta[order]
    axes[0].barh(np.arange(len(order)),ordered,color=np.where(ordered<0,'#26836d','#ac563e'))
    axes[0].axvline(0,color='gray',lw=.8)
    axes[0].set_yticks(np.arange(len(order)),np.array(customers)[order])
    axes[0].invert_yaxis()
    axes[0].set(xlabel='Pooled minus local normalized MAE',title='Most differences are small; negative helps')
    for i,value in enumerate(ordered):
        axes[0].text(max(value,0)+.0005,i,f'{value:+.3g}',va='center',fontsize=7)
    axes[0].set_xlim(-.003,max(delta)*1.35)
    labels=['Yesterday','Last week','Separate regressions','Shared regression']
    axes[1].barh(labels,[primary[m]['aggregate_mae_kw'] for m in MODELS],color='#3c718e')
    axes[1].set(xlabel='Aggregate-load MAE (kW)',title='Sum customers before scoring')
    fig.tight_layout();fig.savefig(out/'pooling-comparison.png');plt.close(fig)
    detail=pd.DataFrame({'client':customers,'local_normalized_mae':local,'pooled_normalized_mae':pooled,'pooled_minus_local':delta})
    detail=detail.sort_values('pooled_minus_local')
    save_frame(detail,out/'customer-comparison.csv.gz')
    rows=[[{'yesterday':'Yesterday','last_week':'Last week','local_ridge':'Separate regressions','pooled_ridge':'Shared regression'}[m],f"{primary[m]['macro_normalized_mae']:.4f}",f"{primary[m]['aggregate_mae_kw']:.1f}",f"{primary[m]['aggregate_bias_kw']:+.1f}"] for m in MODELS]
    report='# Does sharing information help tomorrow’s electricity forecasts?\n\n'
    report+='Sharing coefficients did not improve this panel overall: the separate regressions had lower customer-normalized and aggregate-load error. That is a result for this specified comparison, not a claim that all pooled models fail.\n\n'
    report+='This is a fixed, scale-spanning panel of 24 established customers, not a random sample or new-customer test. Primary results use 2014 dates whose targets and recent history avoid the DST exclusions.\n\n'
    report+='![Customer and aggregate comparisons](pooling-comparison.png)\n\n'
    report+=markdown_table(['Model','Macro normalized MAE','Aggregate MAE kW','Aggregate bias kW'],rows)
    report+=f"\nPooling improves normalized MAE for {int((pooled<local).sum())} of {len(customers)} customers and worsens it for {int((pooled>local).sum())}. The labelled difference plot preserves those magnitudes rather than hiding them in a single average.\n\n"
    report+=f"Primary evaluation excludes {scores['test']['excluded_hour_customer_rows']} of {scores['test']['hour_customer_rows']} hourly customer observations. Full-date sensitivity and 2013 development scores are retained separately in the metrics file.\n\n"
    report+='The three gains are small; the exact customer-level differences are retained in [the comparison table](customer-comparison.csv.gz). Full-date sensitivity preserves the overall model ranking, but not the identity of every customer with a small gain.\n\n'
    report+='Normalized MAE divides each customer’s error by its fixed 2012 mean power; it is not MASE or a percentage-error metric. Peak subsets exceed fixed 2012 thresholds and need not contain 10% of test hours. No intervals, measured cost savings, or production latency claims are made. The nominal-clock interval convention is an assumption, not a UTC reconstruction.\n\n'
    report+='[Design](../../../studies/electricity/DESIGN.md) · [Process story](../../../studies/electricity/STORY.md) · [Metrics](metrics.json) · [Run evidence](run.json)\n'
    (out/'REPORT.md').write_text(report)
    finish_run('electricity',out,started,{'models':MODELS,'lambda_mean_loss':.001,'threads':1,'years':[2013,2014]})
    return scores
