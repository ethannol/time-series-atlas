"""Separate volatility and direction forecasts; fetch-only price truth stays local."""
import json
import warnings
import gzip
import hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.signal import lfilter
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .data import ROOT,write_json,digest
from .common import start_run,finish_run,save_frame,markdown_table


def variance_path(changes,omega,alpha,beta,initial,floor=1e-8):
    y=np.asarray(changes,dtype=float)
    if y.ndim!=1 or not len(y) or not np.isfinite(y).all():raise ValueError('Invalid change vector')
    if initial<=0 or omega<0 or alpha<0 or beta<0 or beta>=1 or floor<=0:raise ValueError('Invalid variance recursion')
    if len(y)==1:return np.array([max(initial,floor)])
    tail,_=lfilter([1],[1,-beta],omega+alpha*y[:-1]**2,zi=[beta*initial])
    return np.maximum(np.r_[initial,tail],floor)


def fit_garch(training):
    y=np.asarray(training,dtype=float);scale=float(np.sqrt(np.mean(y*y)))
    if scale<=0:raise ValueError('Cannot fit zero-variance training series')
    z=y/scale
    def objective(theta):
        v=variance_path(z,*theta,1.,floor=1e-8/scale**2)
        return float(np.mean(np.log(v)+z*z/v))
    attempts=[];best=None
    for alpha,beta in [(.05,.9),(.1,.8),(.15,.7)]:
        result=minimize(objective,[1-alpha-beta,alpha,beta],method='SLSQP',
                        bounds=[(1e-10,None),(0,.999),(0,.999)],
                        constraints=[{'type':'ineq','fun':lambda p:.999-p[1]-p[2]}],
                        options={'maxiter':500,'ftol':1e-9})
        valid=bool(result.success and np.isfinite(result.fun) and np.isfinite(result.x).all() and result.x[0]>0 and result.x[1]>=0 and result.x[2]>=0 and result.x[1]+result.x[2]<=.999+1e-9)
        attempts.append({'start':[1-alpha-beta,alpha,beta],'success':valid,'message':str(result.message),'iterations':int(result.nit),
                         'objective':float(result.fun) if np.isfinite(result.fun) else None,'standardized_parameters':result.x.tolist()})
        if valid and (best is None or result.fun<best.fun):best=result
    if best is None:raise RuntimeError('All declared GARCH training starts failed: '+json.dumps(attempts))
    parameters=[float(best.x[0]*scale**2),float(best.x[1]),float(best.x[2])]
    return parameters,{'attempts':attempts,'training_rms':scale,'parameters_dollar_units':parameters}


def qlike(changes,variance):
    y=np.asarray(changes,dtype=float);v=np.asarray(variance,dtype=float)
    if y.ndim!=1 or y.shape!=v.shape or not len(y) or not np.isfinite(y).all() or not np.isfinite(v).all() or (v<=0).any():
        raise ValueError('QLIKE needs same-shape finite changes and positive variance')
    return float(np.mean(np.log(v)+y*y/v))


def direction_features(prices):
    change=prices.diff()
    return pd.DataFrame({'last_change':change.shift(1),'mean5':change.rolling(5).mean().shift(1),
                         'mean20':change.rolling(20).mean().shift(1),'std20':change.rolling(20).std(ddof=0).shift(1),
                         'previous_price':prices.shift(1)})


def fit_market(prices,train_end='2014-12-31',test_start='2015-01-01'):
    change=prices.diff();gap=prices.index.to_series().diff().dt.days
    analysis=change.loc['2000':'2025'].dropna();training=analysis.loc[:train_end];test=analysis.index>=test_start
    initial=float(np.mean(training.to_numpy()**2))
    params,garch=fit_garch(training)
    variances={'fixed':np.full(len(analysis),initial),
               'rolling_60':change.pow(2).rolling(60).mean().shift(1).reindex(analysis.index).to_numpy(),
               'ewma':variance_path(analysis,0,.06,.94,initial),
               'garch':variance_path(analysis,*params,initial)}
    rows=[]
    for model,variance in variances.items():
        for date,y,v in zip(analysis.index[test],analysis.to_numpy()[test],np.maximum(variance[test],1e-8)):
            rows.append({'date':date,'model':model,'variance':float(v),'change':float(y),'gap_days':int(gap.loc[date])})
    features=direction_features(prices)
    valid=features.notna().all(axis=1)&change.notna();x=features.loc[valid];target=(change.loc[valid]>0).astype(int)
    train=(x.index>='2000-01-01')&(x.index<=train_end);evaluation=(x.index>=test_start)&(x.index<='2025-12-31')
    model=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always');model.fit(x.loc[train],target.loc[train])
    p=model.predict_proba(x.loc[evaluation])[:,list(model[-1].classes_).index(1)]
    prevalence=float(target.loc[train].mean());directions=[]
    for name,prob in [('prevalence',np.full(len(p),prevalence)),('logistic',p)]:
        for date,value,truth in zip(x.index[evaluation],prob,target.loc[evaluation]):
            directions.append({'date':date,'model':name,'up_probability':float(value),'up':int(truth),'gap_days':int(gap.loc[date])})
    parameters={'garch':garch,'variance_initial':initial,'training_changes':len(training),'variance_first_test_date':str(analysis.index[test][0].date()),
                'direction':{'training_rows':int(train.sum()),'test_rows':int(evaluation.sum()),'prevalence':prevalence,
                             'features':list(x.columns),'mean':model[0].mean_.tolist(),'scale':model[0].scale_.tolist(),
                             'coefficient':model[-1].coef_.tolist(),'intercept':model[-1].intercept_.tolist(),
                             'iterations':model[-1].n_iter_.tolist(),'warnings':[str(w.message) for w in caught]}}
    return pd.DataFrame(rows),pd.DataFrame(directions),parameters


def variance_summary(frame):
    rows=[]
    for (market,model),g in frame.groupby(['market','model']):
        rows.append({'market':market,'model':model,'n':len(g),'qlike':qlike(g.change,g.variance),
                     'variance_proxy_mae':float(np.mean(np.abs(g.variance-g.change**2)))})
    return rows


def direction_summary(frame):
    rows=[]
    for (market,model),g in frame.groupby(['market','model']):
        predicted=g.up_probability>=.5;actual=g.up.astype(bool)
        rows.append({'market':market,'model':model,'n':len(g),'brier':float(np.mean((g.up_probability-g.up)**2)),
                     'accuracy':float(np.mean(predicted==actual)),'tp':int((predicted&actual).sum()),'fp':int((predicted&~actual).sum()),
                     'tn':int((~predicted&~actual).sum()),'fn':int((~predicted&actual).sum())})
    return rows


def save_private(frame,kind):
    """Immutable content-addressed evidence cannot overwrite an earlier run's truth."""
    content=gzip.compress(frame.to_csv(index=False).encode(),mtime=0)
    sha=hashlib.sha256(content).hexdigest()
    path=ROOT/'data/processed/oil-evidence'/f'{kind}-{sha}.csv.gz'
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        if digest(path)!=sha:raise ValueError('Corrupted immutable private outcome evidence')
    else:path.write_bytes(content)
    return {'path':str(path.relative_to(ROOT)),'sha256':sha}


def run():
    out,started=start_run('oil');panel=pd.read_csv(ROOT/'data/processed/oil-daily.csv.gz',index_col=0,parse_dates=True)
    forecasts=[];directions=[];parameters={}
    for market in panel:
        v,d,p=fit_market(panel[market].dropna());v['market']=market;d['market']=market
        forecasts.append(v);directions.append(d);parameters[market]=p
    v=pd.concat(forecasts,ignore_index=True);d=pd.concat(directions,ignore_index=True)
    # Preserve full outcome evidence locally without mirroring the provider's price series.
    private=save_private(v,'variance');direction_private=save_private(d,'direction')
    save_frame(v.drop(columns='change'),out/'variance-predictions.csv.gz')
    save_frame(d.drop(columns='up'),out/'direction-predictions.csv.gz')
    metrics={'variance':variance_summary(v),'direction':direction_summary(d),
             'private_outcomes':{'variance':private,'direction':direction_private}}
    write_json(out/'metrics.json',metrics);write_json(out/'parameters.json',parameters)
    subgroups=[]
    for market,g in v.groupby('market'):
        for year,h in g.groupby(g.date.dt.year):
            subgroups.extend([{'group':f'year_{year}',**r} for r in variance_summary(h)])
        for name,mask in [('2020',g.date.dt.year==2020),('other_years',g.date.dt.year!=2020),('gap_le4',g.gap_days<=4),('gap_gt4',g.gap_days>4)]:
            if mask.any():subgroups.extend([{'group':name,**r} for r in variance_summary(g.loc[mask])])
    pd.DataFrame(subgroups).to_csv(out/'variance-subgroups.csv',index=False)
    yearly=[]
    for year,g in d.groupby(d.date.dt.year):yearly.extend([{'year':int(year),**r} for r in direction_summary(g)])
    pd.DataFrame(yearly).to_csv(out/'direction-years.csv',index=False)
    gap_scores=[]
    for name,mask in [('gap_le4',d.gap_days<=4),('gap_gt4',d.gap_days>4)]:
        if mask.any():gap_scores.extend([{'group':name,**r} for r in direction_summary(d[mask])])
    pd.DataFrame(gap_scores).to_csv(out/'direction-gaps.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(10,4.5))
    summary=pd.DataFrame(metrics['variance']);direction=pd.DataFrame(metrics['direction'])
    for i,market in enumerate(['wti','brent']):
        s=summary[summary.market==market].set_index('model');names=['rolling_60','ewma','garch']
        axes[0].bar(np.arange(3)+(i-.5)*.32,s.loc[names,'qlike']-s.loc['fixed','qlike'],width=.3,label=market.upper())
        t=direction[direction.market==market].set_index('model')
        axes[1].bar(i,t.loc['logistic','brier']-t.loc['prevalence','brier'],color=['#2563eb','#0f766e'][i])
    axes[0].set_xticks(range(3),['60 observations','EWMA','GARCH']);axes[0].set_ylabel('QLIKE minus fixed variance (lower is better)');axes[0].legend()
    axes[1].set_xticks(range(2),['WTI','Brent']);axes[1].set_ylabel('Logistic Brier minus prevalence (lower is better)')
    for ax in axes:ax.axhline(0,color='black',lw=.8)
    axes[0].set_title('Forecasting variance');axes[1].set_title('Forecasting direction')
    fig.suptitle('Two questions, separate scores • next observed price change, 2015–2025');fig.tight_layout();fig.savefig(out/'risk-and-direction.png');plt.close(fig)
    variance_table=markdown_table(['Market','Variance model','QLIKE','Squared-change MAE'],[[r['market'],r['model'],f"{r['qlike']:.4f}",f"{r['variance_proxy_mae']:.3f}"] for r in metrics['variance']])
    direction_table=markdown_table(['Market','Direction model','Brier','Accuracy'],[[r['market'],r['model'],f"{r['brier']:.4f}",f"{r['accuracy']:.3f}"] for r in metrics['direction']])
    report=f'''# Can uncertainty be forecast when direction is difficult?

Variance and direction require separate comparisons. Negative values in the
chart mean improvement over that task's simple baseline; the two panels have
different units and must not be compared in magnitude. Every setting was fixed
before evaluating 2015–2025.

![Separate variance and direction scores](risk-and-direction.png)

{variance_table}

{direction_table}

## What was actually forecast

The target is the next **observed** dollar price change for each market, not a
fixed calendar-day return. Weekend and source gaps are not filled with zeros.
The negative WTI observation remains in the experiment; ordinary log returns
would not be defined there. Variance forecasts update from previous changes;
GARCH parameters and the direction model were fitted on 2000–2014 only.

Squared dollar changes are a noisy volatility proxy. QLIKE scores expected
variance differently from absolute proxy error; inspect both. The [annual and
gap breakdown](variance-subgroups.csv) includes a predeclared 2020 stress-period
comparison. The [direction years](direction-years.csv) show how conclusions vary
through time. A lower score does not demonstrate profitable trading, calibrated
tail-risk limits or measured business savings. The [direction gap breakdown](direction-gaps.csv)
also separates short observation gaps from longer ones.
Historical data are revised and
reporting latency is unknown.

## Source access is part of reproducibility

EIA identifies Refinitiv as the underlying spot-price source. Free access does
not establish permission to mirror the complete price history. We retain inputs
and true-change evidence locally, publish original forecasts and aggregate scores,
and pin the exact normalized historical-input hash. `uv run atlas fetch oil`
can use a newer workbook only if normalization through 2025 reproduces that hash.
Historical revisions may make exact public reproduction unavailable; the command
fails explicitly rather than silently changing the experiment.

Reproduce locally with `uv run atlas fetch oil` then `uv run atlas oil`.
[Design](../../../studies/oil/DESIGN.md) · [Story](../../../studies/oil/STORY.md) ·
[Audit](../../intake/oil.json) · [Metrics](metrics.json) · [Parameters](parameters.json) ·
[Variance predictions](variance-predictions.csv.gz) · [Direction predictions](direction-predictions.csv.gz) · [Run evidence](run.json).
Source: EIA spot-price workbooks released October 28, 2026, underlying source
Refinitiv; figures, model forecasts and summaries are this project's analysis.
'''
    (out/'REPORT.md').write_text(report)
    finish_run('oil',out,started,{'train':['2000-01-01','2014-12-31'],'test':['2015-01-01','2025-12-31'],'ewma_decay':.94,'price_inputs':'fetch-only'})


if __name__=='__main__':run()
