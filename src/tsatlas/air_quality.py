"""Single-station outage nowcasts with explicit real missingness and event evidence."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from .data import ROOT,write_json
from .common import start_run,finish_run,save_frame,markdown_table
from .classification import binary_scores,runs,rate

MODELS=['persistence','calendar','network_median','network_ridge']


def network_features(panel,station):
    others=panel.drop(columns=station);median=others.median(axis=1);count=others.notna().sum(axis=1)
    hour=panel.index.hour.to_numpy()
    return pd.DataFrame({'median':median,'hour_sin':np.sin(2*np.pi*hour/24),'hour_cos':np.cos(2*np.pi*hour/24)},index=panel.index),count


def fit_station(panel,station):
    train=panel.loc[:'2015-02-28 23:00'];x,count=network_features(train,station)
    valid=train[station].notna()&(count>=3)
    model=make_pipeline(StandardScaler(),Ridge(alpha=1.))
    model.fit(x.loc[valid],train.loc[valid,station])
    medians=train[station].groupby([train.index.month,train.index.hour]).median()
    return {'model':model,'calendar':medians,'fallback':float(train[station].median()),
            'threshold':float(train[station].quantile(.9,interpolation='linear')),'training_rows':int(valid.sum())}


def outage(panel,station,start,length,fitted):
    times=pd.date_range(start,periods=length,freq='h')
    target=panel[station].reindex(times)
    prior=panel[station].loc[(panel.index<start)&(panel.index>=start-pd.Timedelta(hours=24))].dropna()
    x,count=network_features(panel.reindex(times),station);available=count>=3
    reason='missing_target_truth' if target.isna().any() else 'no_prior_24h_reading' if prior.empty else None
    ledger={'station':station,'start':start,'end_exclusive':start+pd.Timedelta(hours=length),'duration':length,'eligible':reason is None,'exclusion':reason,
            'peer_available_hours':int(available.sum())}
    if reason:return None,ledger
    raw=np.full(length,np.nan)
    if available.any():raw[available]=fitted['model'].predict(x.loc[available])
    calendar=np.array([fitted['calendar'].get((t.month,t.hour),fitted['fallback']) for t in times],dtype=float)
    predictions={'persistence':np.full(length,float(prior.iloc[-1])),'calendar':calendar,
                 'network_median':x['median'].where(available).to_numpy(),'network_ridge':np.maximum(raw,0)}
    records=[]
    for model,values in predictions.items():
        for i,t in enumerate(times):
            records.append({'station':station,'start':start,'duration':length,'hour':t,'model':model,'observed':float(target.iloc[i]),
                            'prediction':float(values[i]),'raw_prediction':float(raw[i]) if model=='network_ridge' else float(values[i]),
                            'other_reporting_stations':int(count.iloc[i]),'common_coverage':bool(available.iloc[i]),'threshold':fitted['threshold']})
    return pd.DataFrame(records),ledger


def event_rows(frame):
    rows=[]
    for (station,start,duration,model),g in frame.groupby(['station','start','duration','model']):
        g=g.sort_values('hour');truth=(g.observed>g.threshold).to_numpy();issued=g.prediction.notna().to_numpy()
        alert=issued&(g.prediction>g.threshold).to_numpy()
        base={'station':station,'start':start,'duration':int(duration),'model':model}
        for a,b in runs(truth):
            found=np.flatnonzero(alert[a:b]);censored=a==0
            rows.append({**base,'type':'high_event','event_start':g.hour.iloc[a],'event_end':g.hour.iloc[b-1],
                         'left_censored':censored,'right_censored':b==len(g),'detected':bool(len(found)),
                         'delay_hours':int(found[0]) if len(found) and not censored else None})
        for a,b in runs(alert):
            if not truth[a:b].any():
                rows.append({**base,'type':'false_alert','event_start':g.hour.iloc[a],'event_end':g.hour.iloc[b-1],
                             'left_censored':a==0,'right_censored':b==len(g),'detected':None,'delay_hours':None})
    return pd.DataFrame(rows)


def score(frame,common=True):
    records=[]
    if common:frame=frame[frame.common_coverage]
    for (duration,station,model),g in frame.groupby(['duration','station','model']):
        valid=g.prediction.notna();h=g[valid]
        scores=binary_scores(h.observed>h.threshold,h.prediction>h.threshold)
        records.append({'duration':int(duration),'station':station,'model':model,**scores,'hours_in_scope':len(g),
                        'mae':float(np.mean(np.abs(h.prediction-h.observed))) if len(h) else None})
    return pd.DataFrame(records)


def run():
    out,started=start_run('air-quality')
    panel=pd.read_csv(ROOT/'data/snapshots/air-quality-hourly.csv.gz',index_col=0,parse_dates=True)
    starts=pd.date_range('2016-03-01','2017-02-01',freq='MS')+pd.Timedelta(hours=9)
    frames=[];ledger=[];parameters={}
    for station in panel:
        fit=fit_station(panel,station);model=fit['model']
        parameters[station]={'threshold':fit['threshold'],'training_rows':fit['training_rows'],'ridge_coefficient':model[-1].coef_.tolist(),
                             'ridge_intercept':float(model[-1].intercept_),'feature_mean':model[0].mean_.tolist(),'feature_scale':model[0].scale_.tolist()}
        for start in starts:
            for length in [6,24,72]:
                frame,row=outage(panel,station,start,length,fit);ledger.append(row)
                if frame is not None:frames.append(frame)
    predictions=pd.concat(frames,ignore_index=True);schedule=pd.DataFrame(ledger)
    save_frame(predictions,out/'predictions.csv.gz');schedule.to_csv(out/'outages.csv',index=False)
    events=event_rows(predictions);save_frame(events,out/'events.csv.gz')
    per_station=score(predictions);per_station.to_csv(out/'station-scores.csv',index=False)
    score(predictions,common=False).to_csv(out/'available-hour-scores.csv',index=False)
    primary=[]
    for (duration,model),g in per_station.groupby(['duration','model']):
        row={'duration':int(duration),'model':model,'macro_balanced_accuracy':float(g.balanced_accuracy.mean()) if g.balanced_accuracy.notna().any() else None,
             'contributing_stations':int(g.balanced_accuracy.notna().sum()),'macro_mae':float(g.mae.mean())}
        row.update({k:int(g[k].sum()) for k in ['n','tp','tn','fp','fn']})
        row.update({'pooled_precision':rate(row['tp'],row['tp']+row['fp']),'pooled_recall':rate(row['tp'],row['tp']+row['fn']),
                    'pooled_false_positive_rate':rate(row['fp'],row['fp']+row['tn'])});primary.append(row)
    coverage=[]
    unique=predictions[predictions.model=='persistence']
    for duration,g in unique.groupby('duration'):
        sched=schedule[schedule.duration==duration]
        coverage.append({'duration':int(duration),'scheduled_blocks':len(sched),'eligible_blocks':int(sched.eligible.sum()),
                         'scheduled_hours':int(len(sched)*duration),'eligible_hours':len(g),'scoreable_network_hours':int(g.common_coverage.sum()),
                         'peer_available_hours_all_scheduled':int(sched.peer_available_hours.sum()),
                         'network_fraction_of_eligible':float(g.common_coverage.mean()),
                         'scoreable_network_fraction_of_scheduled':float(g.common_coverage.sum()/(len(sched)*duration)),
                         'peer_input_fraction_of_scheduled':float(sched.peer_available_hours.sum()/(len(sched)*duration))})
    event_summary=[]
    for (duration,model),g in events.groupby(['duration','model']):
        high=g[g.type=='high_event'];delay=high.delay_hours.dropna()
        event_summary.append({'duration':int(duration),'model':model,'high_events':len(high),'missed_events':int((high.detected==False).sum()),
                              'left_censored_high_events':int(high.left_censored.sum()),'delay_observations':len(delay),
                              'median_delay_hours':float(delay.median()) if len(delay) else None,'false_alert_episodes':int((g.type=='false_alert').sum())})
    write_json(out/'metrics.json',{'primary':primary,'coverage':coverage,'events':event_summary});write_json(out/'parameters.json',parameters)
    seasonal=[]
    for quarter,g in predictions.groupby(predictions.hour.dt.quarter):
        s=score(g);s['quarter']=int(quarter);seasonal.append(s)
    pd.concat(seasonal,ignore_index=True).to_csv(out/'quarter-scores.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4.5));table=pd.DataFrame(primary)
    for model,label in zip(MODELS,['Last local reading','Calendar median','Other-station median','Calibrated network']):
        g=table[table.model==model].sort_values('duration');axes[0].plot(g.duration,g.macro_balanced_accuracy,'o-',label=label)
    axes[0].set_xticks([6,24,72]);axes[0].set_ylim(0,1);axes[0].set_xlabel('Simulated outage duration (hours)');axes[0].set_ylabel('Macro station balanced accuracy');axes[0].legend(fontsize=8)
    c=pd.DataFrame(coverage);axes[1].bar(np.arange(3)-.24,c.eligible_hours/c.scheduled_hours,width=.22,label='Hours in scoreable blocks')
    axes[1].bar(np.arange(3),c.scoreable_network_fraction_of_scheduled,width=.22,label='Scoreable network hours')
    axes[1].bar(np.arange(3)+.24,c.peer_input_fraction_of_scheduled,width=.22,label='Peer inputs available (all hours)')
    axes[1].set_xticks(range(3),['6 h','24 h','72 h']);axes[1].set_ylim(0,1);axes[1].set_ylabel('Fraction of scheduled scope');axes[1].legend(fontsize=8)
    fig.suptitle('Outage nowcasting • one station removed at a time, March 2016–February 2017');fig.tight_layout();fig.savefig(out/'outage-warnings.png');plt.close(fig)
    score_table=markdown_table(['Hours','Method','Balanced accuracy','Stations contributing','MAE (µg/m³)'],[[r['duration'],r['model'],f"{r['macro_balanced_accuracy']:.3f}" if r['macro_balanced_accuracy'] is not None else 'undefined',r['contributing_stations'],f"{r['macro_mae']:.1f}"] for r in primary])
    def fmt(value):return f'{value:.3f}' if value is not None else 'undefined'
    rates_table=markdown_table(['Hours','Method','Pooled precision','Pooled recall','Pooled false-positive rate'],[[r['duration'],r['model'],fmt(r['pooled_precision']),fmt(r['pooled_recall']),fmt(r['pooled_false_positive_rate'])] for r in primary])
    coverage_table=markdown_table(['Hours','Eligible / scheduled blocks','Scoreable network / scheduled hours','Peer data available / scheduled hours'],[[r['duration'],f"{r['eligible_blocks']} / {r['scheduled_blocks']}",f"{r['scoreable_network_hours']} / {r['scheduled_hours']}",f"{r['peer_available_hours_all_scheduled']} / {r['scheduled_hours']}"] for r in coverage])
    event_table=markdown_table(['Hours','Method','Missed / high events','False-alert episodes','Median onset delay','Delay sample'],[[r['duration'],r['model'],f"{r['missed_events']} / {r['high_events']}",r['false_alert_episodes'],r['median_delay_hours'],r['delay_observations']] for r in event_summary])
    report=f'''# Can other stations preserve indications during a sensor outage?

This is a **same-hour nowcast under an explicit reporting assumption**. Other
stations must have delivered their readings. It is not a forecast of future
pollution. The tables separate scored performance, truth eligibility, and peer
data availability across the entire schedule. None is observed operational uptime.

![Outage performance and coverage](outage-warnings.png)

{score_table}

The high-pollution cutoff is each station's training 90th percentile, with strict
exceedance. It is a research threshold, not a regulatory or health threshold.
Balanced accuracy gives sensitivity and specificity equal weight. A station
without both true classes contributes no balanced accuracy; its counts remain
in [station evidence](station-scores.csv). All methods use the same scoreable
hours in the primary table.

{rates_table}

## Coverage changes the scope of the answer

{coverage_table}

The schedule fixes one outage at 09:00 on the first day of each month per station,
at three durations. Each scenario removes only that station. Complete local truth
and a preceding local reading are required to score an outage. Longer eligible
blocks can therefore represent a different cohort, and simulated missingness
need not resemble real failures. Natural missing observations have no known truth.
Network methods abstain when fewer than three other stations report.
Peer-input availability is counted even in blocks excluded for missing local
truth; scoreable network coverage additionally requires that truth. These are
different subsets of the same scheduled hours. Baseline
scores on all their available hours are [retained separately](available-hour-scores.csv).

## Event misses belong beside successful detection delay

{event_table}

Delay describes detected, non-left-censored high runs only; missed events remain
in the table. Episodes are defined within blocks, not deduplicated pollution
incidents across stations or overlapping-duration scenarios. One sustained
prediction may overlap multiple high runs. The [event ledger](events.csv.gz)
retains censoring and event times so these denominators can be inspected.

Fit/calibration uses March 2013–February 2015. No local value inside an outage or
future endpoint enters a prediction. No real-gap recovery, future reporting
latency, health benefit, or robustness to correlated network failures is claimed.

[Design](../../../studies/air-quality/DESIGN.md) · [Story](../../../studies/air-quality/STORY.md) ·
[Source audit](../../intake/air-quality.json) · [Schedule](outages.csv) ·
[Predictions](predictions.csv.gz) · [Metrics](metrics.json) · [Run evidence](run.json).
Run `uv run atlas air-quality`. Data: Song Chen (2017), Beijing Multi-Site Air
Quality, UCI, CC BY 4.0; input is the twelve full station files.
'''
    (out/'REPORT.md').write_text(report)
    finish_run('air-quality',out,started,{'outage_durations':[6,24,72],'minimum_other_stations':3,'test_start':'2016-03-01','test_end':'2017-02-28','threshold_quantile':.9})


if __name__=='__main__':run()
