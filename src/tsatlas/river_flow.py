"""Known-gauge daily high-flow forecasts with issue-safe calibration and onset audits."""
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from .data import ROOT,write_json
from .common import start_run,finish_run,save_frame,markdown_table
from .classification import binary_scores,runs,rate

FLOW=['flow_now','flow_lag1','flow_lag2','flow_mean7','annual_sin','annual_cos']
WEATHER=['precip_now','precip_sum3','precip_sum7','temperature_mean7']
MODELS=['persistence','flow_only','flow_weather']


def approved_flow(frame):return frame.flow_cfs.where((frame.qc=='A')&(frame.flow_cfs>=0))


def features(frame):
    q=approved_flow(frame);p=frame.precip_mm.where(frame.precip_mm>=0);t=(frame.tmax_c+frame.tmin_c)/2
    phase=2*np.pi*frame.index.dayofyear.to_numpy()/365.25
    x=pd.DataFrame({'flow_now':np.log1p(q),'flow_lag1':np.log1p(q.shift(1)),'flow_lag2':np.log1p(q.shift(2)),
                    'flow_mean7':np.log1p(q.rolling(7).mean()),'annual_sin':np.sin(phase),'annual_cos':np.cos(phase),
                    'precip_now':np.log1p(p),'precip_sum3':np.log1p(p.rolling(3).sum()),
                    'precip_sum7':np.log1p(p.rolling(7).sum()),'temperature_mean7':t.rolling(7).mean()},index=frame.index)
    return x.where(np.isfinite(x))


def split_masks(origin,target,train_end,cal_end,test_end):
    origin=pd.DatetimeIndex(origin);target=pd.DatetimeIndex(target)
    train_end=pd.Timestamp(train_end);cal_end=pd.Timestamp(cal_end);test_end=pd.Timestamp(test_end)
    train=target<=train_end
    cal=(target>train_end)&(target<=cal_end)&(origin>=train_end)
    test=(target>cal_end)&(target<=test_end)&(origin>=cal_end)
    return train,cal,test


def predict_gauge(frame,gauge,horizon,train_end='1999-12-31',cal_end='2004-12-31',test_end='2014-12-31'):
    q=approved_flow(frame);x=features(frame);threshold=float(q.loc[:train_end].quantile(.9,interpolation='linear'))
    if not np.isfinite(threshold) or threshold<=0:raise ValueError('Gauge needs a positive approved training threshold')
    outcome=q.shift(-horizon);target=frame.index+pd.Timedelta(days=horizon)
    train_mask,cal_mask,test_mask=split_masks(frame.index,target,train_end,cal_end,test_end)
    valid=x.notna().all(axis=1).to_numpy()&outcome.notna().to_numpy()
    train=train_mask&valid;cal=cal_mask&valid;test=test_mask&valid
    high=(outcome>threshold).to_numpy();params={'high_flow_threshold_cfs':threshold,'models':{}}
    audit={'gauge':gauge,'horizon':horizon,'train_rows':int(train.sum()),'calibration_rows':int(cal.sum()),'test_rows':int(test.sum()),
           'calibration_boundary_exclusions':int(((target>pd.Timestamp(train_end))&(target<=pd.Timestamp(cal_end))&(frame.index<pd.Timestamp(train_end))).sum()),
           'test_boundary_exclusions':int(((target>pd.Timestamp(cal_end))&(target<=pd.Timestamp(test_end))&(frame.index<pd.Timestamp(cal_end))).sum()),
           'test_invalid_input_rows':int((test_mask&~x.notna().all(axis=1).to_numpy()).sum()),
           'test_invalid_target_rows':int((test_mask&outcome.isna().to_numpy()).sum()),'test_scheduled_after_boundary':int(test_mask.sum())}
    bad_input=~x.notna().all(axis=1).to_numpy();bad_target=outcome.isna().to_numpy()
    audit['test_invalid_both_rows']=int((test_mask&bad_input&bad_target).sum())
    audit['test_invalid_union_rows']=int((test_mask&(bad_input|bad_target)).sum())
    if audit['test_rows']+audit['test_invalid_union_rows']!=audit['test_scheduled_after_boundary']:
        raise ValueError('Split coverage does not reconcile')
    rows=[]
    for name in MODELS:
        if not ((cal&~high).any()):
            params['models'][name]={'status':'unevaluable','reason':'no calibration negatives'};continue
        if name=='persistence':
            scores=q.to_numpy()/threshold;details={'status':'ok','score':'latest approved flow / training threshold'}
        else:
            if len(np.unique(high[train]))<2:
                params['models'][name]={'status':'unevaluable','reason':'training class absent'};continue
            cols=FLOW+(WEATHER if name=='flow_weather' else [])
            model=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=1000))
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always');model.fit(x.loc[train,cols],high[train].astype(int))
            scores=np.full(len(frame),np.nan)
            scores[valid]=model.predict_proba(x.loc[valid,cols])[:,list(model[-1].classes_).index(1)]
            details={'status':'ok','features':cols,'mean':model[0].mean_.tolist(),'scale':model[0].scale_.tolist(),
                     'coefficient':model[-1].coef_.tolist(),'intercept':model[-1].intercept_.tolist(),
                     'iterations':model[-1].n_iter_.tolist(),'warnings':[str(w.message) for w in caught]}
        if not np.isfinite(scores[valid]).all():raise ValueError('Nonfinite model score')
        cutoff=float(np.quantile(scores[cal&~high],.9,method='linear'));details['alert_cutoff']=cutoff
        details['calibration_negative_days']=int((cal&~high).sum());params['models'][name]=details
        for i in np.flatnonzero(test):
            rows.append({'gauge':gauge,'horizon':horizon,'model':name,'origin':frame.index[i],'target_date':target[i],
                         'flow_cfs':float(outcome.iloc[i]),'high_threshold':threshold,'high':bool(high[i]),
                         'score':float(scores[i]),'alert_cutoff':cutoff,'alert':bool(scores[i]>cutoff)})
    return pd.DataFrame(rows),params,audit


def event_ledger(frame,predictions,threshold,gauge,horizon):
    q=approved_flow(frame);truth=q.loc['2005':'2014'];events=[]
    for name,g in predictions.groupby('model'):
        lookup=g.set_index('target_date');base={'gauge':gauge,'horizon':horizon,'model':name}
        for a,b in runs((truth>threshold).to_numpy()):
            start=truth.index[a];previous=q.get(start-pd.Timedelta(days=1),np.nan)
            known_onset=bool(np.isfinite(previous) and previous<=threshold)
            origin=start-pd.Timedelta(days=horizon);history=q.loc[origin:start-pd.Timedelta(days=1)]
            before_onset=bool(len(history)==horizon and history.notna().all() and (history<=threshold).all())
            covered=start in lookup.index
            eligible=known_onset and before_onset and covered
            events.append({**base,'type':'high_run','event_start':start,'target_date':start,'origin':origin,'event_end':truth.index[b-1],
                           'known_onset':known_onset,'left_censored':not known_onset,'right_censored':b==len(truth) or pd.isna(truth.iloc[b]),
                           'forecast_covered':covered,'nonhigh_through_origin_to_event':before_onset,'eligible_onset':eligible,
                           'alerted_onset':bool(lookup.loc[start,'alert']) if eligible else None})
        # Restore a complete test calendar so gaps/unknown truth split alert runs.
        issued=g.set_index('target_date').alert.reindex(truth.index)
        alert=issued.eq(True)
        known=truth.notna();alert=alert&known
        for a,b in runs(alert.to_numpy()):
            if not (truth.iloc[a:b]>threshold).any():
                left=a==0 or pd.isna(truth.iloc[a-1]) or pd.isna(issued.iloc[a-1])
                right=b==len(truth) or pd.isna(truth.iloc[b]) or pd.isna(issued.iloc[b])
                events.append({**base,'type':'unresolved_alert_segment' if left or right else 'false_alert_episode',
                               'event_start':truth.index[a],'target_date':truth.index[a],'origin':truth.index[a]-pd.Timedelta(days=horizon),'event_end':truth.index[b-1],
                               'known_onset':None,'left_censored':left,'right_censored':right,
                               'forecast_covered':True,'nonhigh_through_origin_to_event':None,'eligible_onset':False,'alerted_onset':None})
    return pd.DataFrame(events)


def site_scores(predictions):
    records=[]
    for (gauge,horizon,model),g in predictions.groupby(['gauge','horizon','model']):
        s=binary_scores(g.high,g.alert)
        records.append({'gauge':gauge,'horizon':int(horizon),'model':model,**s,
                        'brier':float(np.mean((g.score-g.high.astype(int))**2)) if model!='persistence' else None})
    return pd.DataFrame(records)


def mean_defined(values):return float(values.mean()) if values.notna().any() else None


def run():
    out,started=start_run('river-flow')
    panel=pd.read_csv(ROOT/'data/snapshots/river-daily-panel.csv.gz',dtype={'gauge':str,'huc':str},parse_dates=['date'])
    frames=[];events=[];audits=[];parameters={};groups=[]
    for gauge,raw in panel.groupby('gauge'):
        frame=raw.set_index('date').sort_index();area=float(frame.area_km2.iloc[0]);train=frame.loc[:'1999-12-31']
        cold=float(train.loc[(train.tmax_c+train.tmin_c)/2<0,'precip_mm'].sum()/train.precip_mm.sum())
        groups.append({'gauge':gauge,'huc':str(frame.huc.iloc[0]),'area_km2':area,
                       'area_group':'lt100' if area<100 else '100to1000' if area<=1000 else 'gt1000',
                       'cold_precip_fraction':cold,'climate_group':'cold_fraction_lt0.1' if cold<.1 else 'cold_fraction_ge0.1'})
        for horizon in [1,3]:
            prediction,params,audit=predict_gauge(frame,gauge,horizon)
            frames.append(prediction);audits.append(audit);parameters[f'{gauge}_h{horizon}']=params
            if len(prediction):events.append(event_ledger(frame,prediction,params['high_flow_threshold_cfs'],gauge,horizon))
    p=pd.concat(frames,ignore_index=True);event=pd.concat(events,ignore_index=True)
    save_frame(p,out/'predictions.csv.gz');save_frame(event,out/'events.csv.gz')
    pd.DataFrame(audits).to_csv(out/'split-audit.csv',index=False);pd.DataFrame(groups).to_csv(out/'catchment-groups.csv',index=False)
    scores=site_scores(p);scores.to_csv(out/'gauge-scores.csv',index=False);write_json(out/'parameters.json',parameters)
    matched=scores.groupby(['gauge','horizon']).model.nunique()
    common_pairs=matched[matched==len(MODELS)].index
    score_index=scores.set_index(['gauge','horizon']);common=score_index[score_index.index.isin(common_pairs)].reset_index()
    unmatched=[{'gauge':a['gauge'],'horizon':a['horizon'],'available_models':int(matched.get((a['gauge'],a['horizon']),0))}
               for a in audits if matched.get((a['gauge'],a['horizon']),0)!=len(MODELS)]
    primary=[]
    for (horizon,model),g in common.groupby(['horizon','model']):
        primary.append({'horizon':int(horizon),'model':model,'gauges':len(g),'macro_recall':mean_defined(g.recall),
                        'recall_gauges':int(g.recall.notna().sum()),'macro_false_positive_rate':mean_defined(g.false_positive_rate),
                        'fpr_gauges':int(g.false_positive_rate.notna().sum()),'macro_precision':mean_defined(g.precision),
                        'precision_gauges':int(g.precision.notna().sum()),'macro_brier':mean_defined(g.brier),
                        'brier_gauges':int(g.brier.notna().sum()),
                        **{k:int(g[k].sum()) for k in ['n','tp','fp','tn','fn']}})
    onset=[]
    event_index=event.set_index(['gauge','horizon']);common_events=event_index[event_index.index.isin(common_pairs)].reset_index()
    for (horizon,model),g in common_events.groupby(['horizon','model']):
        high=g[g.type=='high_run'];eligible=high[high.eligible_onset==True]
        detected=int((eligible.alerted_onset==True).sum())
        onset.append({'horizon':int(horizon),'model':model,'high_runs':len(high),'censored_starts':int(high.left_censored.sum()),
                      'known_onsets':int(high.known_onset.sum()),'eligible_onsets':len(eligible),'alerted_onsets':detected,
                      'missed_onsets':len(eligible)-detected,'onset_recall':rate(detected,len(eligible)),
                      'false_alert_episodes':int((g.type=='false_alert_episode').sum()),
                      'unresolved_alert_segments':int((g.type=='unresolved_alert_segment').sum())})
    write_json(out/'metrics.json',{'primary':primary,'onsets':onset,'gauges':len(groups),'unmatched_gauge_horizons':unmatched})
    grouped=common.merge(pd.DataFrame(groups),on='gauge');subgroups=[]
    for field in ['area_group','climate_group']:
        for (label,horizon,model),g in grouped.groupby([field,'horizon','model']):
            subgroups.append({'group_type':field,'group':label,'horizon':int(horizon),'model':model,'gauges':len(g),
                              'macro_recall':mean_defined(g.recall),'recall_gauges':int(g.recall.notna().sum()),
                              'macro_false_positive_rate':mean_defined(g.false_positive_rate),'fpr_gauges':int(g.false_positive_rate.notna().sum())})
    pd.DataFrame(subgroups).to_csv(out/'group-scores.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5));table=pd.DataFrame(primary);onsets=pd.DataFrame(onset)
    colors=['#6b7280','#2563eb','#0f766e']
    for i,model in enumerate(MODELS):
        g=table[table.model==model].sort_values('horizon');e=onsets[onsets.model==model].sort_values('horizon')
        axes[0].bar(np.arange(2)+(i-1)*.25,g.macro_recall,width=.23,label={'flow_only':'Flow only','flow_weather':'Flow + weather','persistence':'Persistence'}[model],color=colors[i])
        axes[1].bar(np.arange(2)+(i-1)*.25,e.onset_recall,width=.23,label={'flow_only':'Flow only','flow_weather':'Flow + weather','persistence':'Persistence'}[model],color=colors[i])
    for ax in axes:ax.set_xticks(range(2),['Next daily target','Target three days later']);ax.set_ylim(0,1);ax.legend(fontsize=8)
    axes[0].set_ylabel('Macro gauge high-day recall');axes[1].set_ylabel('Pooled eligible-onset recall')
    axes[0].set_title('Recognizing high-flow days');axes[1].set_title('Warning before a new high-flow run')
    fig.suptitle('Known-gauge daily forecasts • cutoffs fixed using 2000–2004 negatives');fig.tight_layout();fig.savefig(out/'flow-and-onsets.png');plt.close(fig)
    def fmt(value):return f'{value:.3f}' if value is not None else 'undefined'
    primary_table=markdown_table(['Date offset','Method','Macro recall','Macro false-positive rate','Gauges'],[[r['horizon'],r['model'],fmt(r['macro_recall']),fmt(r['macro_false_positive_rate']),r['gauges']] for r in primary])
    event_table=markdown_table(['Date offset','Method','Alerted / eligible onsets','Misses','False-alert episodes'],[[r['horizon'],r['model'],f"{r['alerted_onsets']} / {r['eligible_onsets']}",r['missed_onsets'],r['false_alert_episodes']] for r in onset])
    report=f'''# Does high-flow prediction provide warning before a new rise?

Adding past weather improved next-day high-flow recall only slightly (0.915
versus 0.906 for flow alone). Before new rises, it alerted on 496 of 822 eligible
onsets versus 467 for flow alone, with 830 wholly false alert episodes versus
653. At a three-day date offset, weather added just one detected onset
(166 versus 165 of 696). Continued high flow is easier to recognize than a new rise.

Test false-positive rates were about 14–15%, above the roughly 10% targeted in
calibration. That target did not guarantee the later alert burden. The comparison
below separates high-day recall from new-onset indications and shows their false-alert burden.

![High days versus new onsets](flow-and-onsets.png)

{primary_table}

{event_table}

## What the warning horizon means

Inputs end on observed day d; we assume those daily aggregates have arrived at
the start of d+1. Targets are daily flow on d+1 or d+3. These are date offsets,
not measured 24- or 72-hour operational lead times. Future rainfall is excluded.
The source weather is retrospective, and its Hr12 field proves no release time.

A high-flow threshold is the training 90th percentile for that gauge. For onset
scoring, the previous day and every day since origin must be observed and non-high.
That condition is a retrospective event-scoring stratum, never an input filter.
The second panel pools eligible events; the first weights gauges equally. A
successful indication of continued high flow does not necessarily warn of onset.
Unknown truth breaks events; censored starts and forecast coverage are retained
in [the event ledger](events.csv.gz).
Alert segments touching unknown truth, absent forecasts or the study boundary
remain unresolved and are counted separately from fully observed false-alert
episodes. False-positive days remain in the primary rates. Primary method
contrasts use matched gauge/horizon sets; any unevaluable model is preserved in
the parameter/status ledger and excluded from that matched comparison explicitly.

## Which rivers and observations this represents

The fixed panel has 17 gauges, chosen by geography and 1980–1999 approved-flow
coverage. No HUC09 candidate met that rule. It is not representative of all
rivers or an ungauged-catchment test. Estimated A:e and missing flow are excluded,
and [split coverage](split-audit.csv) stays visible. [Gauge scores](gauge-scores.csv)
and [area/climate groups](group-scores.csv) expose heterogeneity. Climate groups
use training-period cold precipitation only, not full-record hydrological signatures.
At date offset +3, weather-model recall was 0.858 in the ten higher-cold-fraction
gauges and 0.528 in the seven lower-group gauges; false-positive rates were
0.165 and 0.120. These small, selected groups describe heterogeneity. They do
not establish why catchments differ or a causal effect of cold precipitation.

Training ends in 1999 and calibration in 2004. Source review and a later design
check caught a boundary hazard: early three-day forecasts could otherwise use
calibration outcomes from after their origin. Explicit origin guards remove those
first two boundary targets. All model choices preceded the final 2005–2014 run.
This study establishes no flood damage, hourly warning, or operational benefit.

[Design](../../../studies/river-flow/DESIGN.md) · [Story](../../../studies/river-flow/STORY.md) ·
[Intake audit](../../intake/river-flow.json) · [Predictions](predictions.csv.gz) ·
[Metrics](metrics.json) · [Parameters](parameters.json) · [Run evidence](run.json).
Run `uv run atlas river-flow`. Data: CAMELS-US time series v1.2, observed USGS
streamflow and Daymet basin forcings, DOI10.5065/D6MW2F4D, CC BY 4.0.
'''
    (out/'REPORT.md').write_text(report)
    finish_run('river-flow',out,started,{'horizons':[1,3],'train_end':'1999-12-31','calibration_end':'2004-12-31','test_end':'2014-12-31','calibration_negative_quantile':.9})


if __name__=='__main__':run()
