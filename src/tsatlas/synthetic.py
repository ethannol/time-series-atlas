"""Known-truth sequential detection, with deliberate dependence stress tests."""
import numpy as np
import pandas as pd
from .data import write_json
from .common import start_run,finish_run,save_frame,markdown_table,plt


def stream(rng,rho=0.,shift=False):
    noise=rng.normal(size=400)
    if rho:
        for t in range(1,len(noise)): noise[t]=rho*noise[t-1]+np.sqrt(1-rho*rho)*noise[t]
    if shift: noise[200:]+=1.
    return noise


def scores(x):
    scale=np.std(x[:100],ddof=1)
    if scale<=0: raise ValueError('Degenerate baseline')
    z=(x[100:]-x[:100].mean())/scale
    accum=[];state=0.
    for value in z:
        state=max(0.,state+value-.5);accum.append(state)
    return {'shewhart':z,'cusum':np.array(accum)}


def first_alarm(values,threshold):
    exceed=np.flatnonzero(values>threshold)
    return int(exceed[0]+100) if len(exceed) else None


def summarize(frame):
    output={}
    for (method,rho,shift),g in frame.groupby(['method','rho','shift']):
        alarms=g.alarm.to_numpy()
        if shift:
            pre=int((alarms<200).sum());detect=int((alarms>=200).sum());miss=int(np.isnan(alarms).sum());eligible=len(g)-pre
            delays=alarms[alarms>=200]-200
            output[f'{method}/rho={rho}/shift']={'n':len(g),'prechange_alarms':pre,'eligible':eligible,'detections':detect,'misses':miss,
                'prechange_rate':pre/len(g),'eligible_detection_rate':detect/eligible if eligible else None,
                'eligible_miss_rate':miss/eligible if eligible else None,'median_detected_delay':float(np.median(delays)) if len(delays) else None}
        else:
            output[f'{method}/rho={rho}/no_shift']={'n':len(g),'false_alarms':int(np.isfinite(alarms).sum()),'false_alarm_rate':float(np.isfinite(alarms).mean())}
    return output


def run():
    out,started=start_run('synthetic')
    rng=np.random.default_rng(20261030)
    maxima={m:[] for m in ['shewhart','cusum']}
    for _ in range(200):
        for m,values in scores(stream(rng)).items(): maxima[m].append(float(values.max()))
    thresholds={m:float(np.quantile(values,.95,method='higher')) for m,values in maxima.items()}
    rng=np.random.default_rng(20261031);rows=[]
    for rho in [0.,.6]:
        for shift in [False,True]:
            for replicate in range(200):
                for method,values in scores(stream(rng,rho,shift)).items():
                    rows.append({'rho':rho,'shift':shift,'replicate':replicate,'method':method,'alarm':first_alarm(values,thresholds[method])})
    frame=pd.DataFrame(rows);save_frame(frame,out/'replicates.csv.gz')
    result=summarize(frame)
    write_json(out/'metrics.json',{'thresholds':thresholds,'results':result,'calibration_maxima':maxima})
    fig,axes=plt.subplots(1,2,figsize=(10,4.2))
    positions=np.arange(2)
    for k,method in enumerate(['shewhart','cusum']):
        fa=[result[f'{method}/rho={rho}/no_shift']['false_alarm_rate'] for rho in [0.,.6]]
        detect=[result[f'{method}/rho={rho}/shift']['eligible_detection_rate'] for rho in [0.,.6]]
        axes[0].bar(positions+(k-.5)*.3,fa,width=.3,label=method)
        axes[1].bar(positions+(k-.5)*.3,detect,width=.3,label=method)
    axes[0].axhline(.05,color='gray',ls='--',label='calibration target')
    axes[0].set(title='Any false alarm in 300 monitored points',ylabel='Fraction of no-change streams')
    axes[1].set(title='Detection conditional on no early alarm',ylabel='Fraction of eligible changed streams')
    for ax in axes: ax.set_xticks(positions,['IID','AR(1), rho=.6']);ax.set_ylim(0,1);ax.legend(fontsize=8)
    fig.tight_layout();fig.savefig(out/'detection-comparison.png');plt.close(fig)
    rows=[]
    for rho in [0.,.6]:
        for method in ['shewhart','cusum']:
            c=result[f'{method}/rho={rho}/shift'];n=result[f'{method}/rho={rho}/no_shift']
            rows.append([method,rho,f"{n['false_alarm_rate']:.1%}",c['prechange_alarms'],c['eligible'],c['detections'],c['misses'],c['median_detected_delay']])
    report='# How quickly can a sustained change be detected?\n\n'
    report+='Thresholds were calibrated on separate IID streams, then frozen. AR(1) streams deliberately violate the independence assumption. These are known-truth simulations, not measured field performance.\n\n![Detection comparison](detection-comparison.png)\n\n'
    report+=markdown_table(['Method','rho','No-change false alerts','Early alarms /200','Eligible','Detected','Missed','Median detected delay'],rows)
    report+='\nEach changed condition contains 200 streams. Early alarms remove a stream from the eligible denominator; detected-delay summaries omit misses and must be read beside detection counts. No restart after an early alarm is allowed. Each no-change false-alert rate has denominator 200. A 5% calibration target is not a universal guarantee.\n\n'
    report+='[Design](../../../studies/synthetic/DESIGN.md) · [Process story](../../../studies/synthetic/STORY.md) · [Metrics](metrics.json) · [Run evidence](run.json)\n'
    (out/'REPORT.md').write_text(report)
    finish_run('synthetic',out,started,{'calibration_seed':20261030,'evaluation_seed':20261031,'replicates':200,'thresholds':thresholds})
    return result
