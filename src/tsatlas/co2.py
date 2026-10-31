"""December-origin CO2 hindcasts; all source quality exclusions stay on the time axis."""
import numpy as np
import pandas as pd
from .data import ROOT,co2_frame,write_json
from .metrics import forecast_scores
from .common import start_run,finish_run,save_frame,markdown_table,plt

MODELS=['seasonal_naive','linear_expanding','linear_120months','quadratic_expanding']
HORIZONS=[1,12,36]
LABELS={'seasonal_naive':'Repeat last same month','linear_expanding':'Linear fit, all history',
        'linear_120months':'Linear fit, trailing decade','quadratic_expanding':'Quadratic fit, all history'}
COLORS=dict(zip(MODELS,['#6b7280','#d97706','#0f766e','#7c3aed']))


def regression_matrix(index,origin,quadratic=False):
    t=np.asarray((index.year-origin.year)+(index.month-origin.month)/12,dtype=float)
    cols=[np.ones(len(index)),t]+[np.asarray(index.month==m,dtype=float) for m in range(2,13)]
    if quadratic: cols.append(t*t)
    return np.column_stack(cols)


def predict(frame,origin,target,model):
    train=frame.loc[(frame.index<=origin)&frame.usable]
    if model=='seasonal_naive':
        return float(train.loc[train.index.month==target.month,'average'].iloc[-1])
    if model=='linear_120months': train=train.loc[train.index>origin-pd.DateOffset(months=120)]
    x=regression_matrix(train.index,origin,model=='quadratic_expanding')
    beta=np.linalg.lstsq(x,train.average.to_numpy(),rcond=None)[0]
    return float((regression_matrix(pd.DatetimeIndex([target]),origin,model=='quadratic_expanding')@beta)[0])


def run():
    out,started=start_run('co2')
    frame=co2_frame(ROOT/'data/snapshots/co2_mm_mlo.txt').loc['1974-05':'2025-12']
    records=[]
    for year in list(range(1989,2007))+list(range(2010,2023)):
        origin=pd.Timestamp(year,12,1)
        for horizon in HORIZONS:
            target=origin+pd.DateOffset(months=horizon)
            row=frame.loc[target]
            if not row.usable: continue
            for model in MODELS:
                records.append({'origin_month':origin,'target':target,'horizon':horizon,'model':model,
                    'split':'calibration' if year<=2006 else 'test','actual':float(row.average),
                    'prediction':predict(frame,origin,target,model),'site_substitution':bool(row.site_substitution)})
    predictions=pd.DataFrame(records)
    for model in MODELS:
        for horizon in HORIZONS:
            mask=(predictions.model==model)&(predictions.horizon==horizon)
            calibration=predictions.loc[mask&(predictions.split=='calibration')]
            offsets=np.quantile(calibration.actual-calibration.prediction,[.1,.9],method='linear')
            predictions.loc[mask,'lower']=predictions.loc[mask,'prediction']+offsets[0]
            predictions.loc[mask,'upper']=predictions.loc[mask,'prediction']+offsets[1]
    save_frame(predictions,out/'predictions.csv.gz')
    test=predictions.loc[predictions.split=='test']
    scores={}
    for (model,horizon),group in test.groupby(['model','horizon']):
        scores[f'{model}/{horizon}']=forecast_scores(group.actual,group.prediction,group.lower,group.upper)
    sensitivity={}
    for (model,horizon),group in test.loc[~test.site_substitution].groupby(['model','horizon']):
        sensitivity[f'{model}/{horizon}']=forecast_scores(group.actual,group.prediction,group.lower,group.upper)
    primary=test.loc[test.horizon==36].copy()
    primary['absolute_error']=abs(primary.prediction-primary.actual)
    paired=primary.pivot(index='origin_month',columns='model',values='absolute_error')
    deltas=paired.subtract(paired.linear_expanding,axis=0)
    paired_out=deltas.reset_index()
    save_frame(paired_out,out/'paired-error-differences.csv.gz')
    write_json(out/'metrics.json',{'test':scores,'exclude_site_targets':sensitivity,
        'paired_36month_mae_difference_vs_linear':{m:{'mean':float(deltas[m].mean()),'min':float(deltas[m].min()),'max':float(deltas[m].max()),'origins_better':int((deltas[m]<0).sum())} for m in MODELS}})
    # Post-publication interpretation diagnostic; no refitting or new comparison.
    diagnostics=[]
    for model in ['linear_expanding','linear_120months']:
        group=test.loc[test.model==model]
        forecasts=group.pivot(index='origin_month',columns='horizon',values='prediction')
        observed_origin=frame.loc[forecasts.index,'average']
        observed_target=group.loc[group.horizon==36].set_index('origin_month').actual
        fitted_origin=(3*forecasts[12]-forecasts[36])/2
        gap=observed_origin-fitted_origin
        signed_error=observed_target-forecasts[36]
        diagnostics.append(pd.DataFrame({'model':model,'observed_origin':observed_origin,
            'fitted_origin':fitted_origin,'origin_gap':gap,
            'predicted_growth':forecasts[36]-fitted_origin,
            'observed_growth':observed_target-observed_origin,
            'growth_error':signed_error-gap,'signed_error_36':signed_error}).rename_axis('origin_month').reset_index())
    diagnostic=pd.concat(diagnostics,ignore_index=True)
    save_frame(diagnostic,out/'origin-level-diagnostic.csv.gz')
    means=diagnostic.groupby('model').mean(numeric_only=True)
    diagnostic_rows=[[LABELS[m],f"{means.loc[m,'origin_gap']:.3f}",
        f"{means.loc[m,'growth_error']:.3f}",f"{means.loc[m,'signed_error_36']:.3f}"]
        for m in ['linear_expanding','linear_120months']]
    fig,axes=plt.subplots(1,2,figsize=(11,4.2))
    for m in MODELS:
        axes[0].plot(HORIZONS,[scores[f'{m}/{h}']['mae'] for h in HORIZONS],marker='o',label=LABELS[m],color=COLORS[m])
    axes[0].set(xlabel='Horizon (months)',ylabel='MAE (ppm)',title='December-origin forecasts',xticks=HORIZONS)
    axes[0].legend(fontsize=7)
    for m in MODELS[2:]: axes[1].plot(deltas.index.year,deltas[m],marker='o',label=LABELS[m],color=COLORS[m])
    axes[1].axhline(0,color='black',lw=.8)
    axes[1].set(xlabel='December origin year',ylabel='Absolute-error difference (ppm)',title='Three-year forecasts vs all-history linear fit')
    axes[1].legend(fontsize=7)
    fig.tight_layout();fig.savefig(out/'forecast-comparison.png');plt.close(fig)
    rows=[]
    for m in MODELS:
        v=scores[f'{m}/36']
        rows.append([LABELS[m],f"{v['mae']:.3f}",f"{v['bias']:+.3f}",f"{v['coverage80']:.1%}",f"{v['width80']:.3f}",f"{v['interval_score80']:.3f}"])
    report='# Does fitting recent history improve multiyear CO₂ forecasts?\n\n'
    report+=f"The trailing-decade linear fit reduced three-year mean absolute error from {scores['linear_expanding/36']['mae']:.3f} ppm for the all-history linear fit to {scores['linear_120months/36']['mae']:.3f} ppm in this comparison. Both the recent linear and all-history quadratic fits improved on the all-history linear fit at every evaluated three-year origin. **The recent fit improves both its starting level and subsequent growth estimate; this comparison does not isolate growth adaptation alone.**\n\n"
    report+='These are December-origin revised-data hindcasts. The primary comparison predicts December three years later, not an entire monthly trajectory.\n\n'
    report+='![Forecast comparisons](forecast-comparison.png)\n\n'
    report+=markdown_table(['Model','MAE ppm','Bias ppm','80% coverage','Width ppm','Interval score'],rows)
    report+=f'\nThere are {len(paired)} paired evaluation origins. Negative error differences in the right-hand plot favor the alternative to the all-history linear fit. The full origin-level differences are retained; overlapping three-year errors are not treated as independent samples.\n\n'
    report+='## What the improvement includes\n\n'
    report+='A fresh critique after publication identified an omitted qualification: neither linear regression is anchored to the last observation. Changing the training window changes the fitted level as well as the slope. This **post-publication diagnostic** decomposes the same saved linear predictions, without fitting or selecting another model. Positive values below mean underprediction; all values are means in ppm across the same origins.\n\n'
    report+=markdown_table(['Fit','Observed minus fitted origin','Growth error','Total signed error at three years'],diagnostic_rows)
    report+='\nOrigin gap plus growth error equals total signed error. This is an arithmetic identity, **not causal attribution or a decomposition of MAE**. The recent fit also estimates the subsequent increase more accurately on average. We have not evaluated an origin-anchored alternative. For December predictions p12 and p36, fitted origin = (3 × p12 − p36) / 2; growth error = actual36 − p36 − origin gap. [Per-origin diagnostic](origin-level-diagnostic.csv.gz) · [Fresh critique](../../../reviews/study-critiques-20261030/co2.md).\n\n'
    report+='Intervals use only pre-test calibration outcomes. Their nominal 80% label is a target, not a guarantee. Seasonal naive is a reference; the expanding linear model is the substantive baseline.\n\n'
    report+='Source-quality exclusions, site-substitution target sensitivity, all calibration/test predictions, and metrics are retained. Site sensitivity removes affected **targets**, not all effects of changed-site observations used later in training. No causal explanation or real-time-vintage claim is made.\n\n'
    report+='[Design](../../../studies/co2/DESIGN.md) · [Process story](../../../studies/co2/STORY.md) · [Metrics](metrics.json) · [Run evidence](run.json)\n'
    (out/'REPORT.md').write_text(report)
    finish_run('co2',out,started,{'models':MODELS,'horizons':HORIZONS,'no_tuning':True,'origin_month_semantics':'Last observed monthly value, not release date; assume issuance after December value is available'})
    return scores
