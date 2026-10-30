"""Forecast recorded weekly sales using origin-safe intermittent-demand methods."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .data import ROOT,write_json
from .common import start_run,finish_run,save_frame,markdown_table

MODELS=['zero','last_week','rolling_28','croston_sba','tsb']


def intermittent_rates(history,alpha=.1):
    y=np.asarray(history,dtype=float)
    if y.ndim!=1 or not np.isfinite(y).all() or (y<0).any():
        raise ValueError('Expected finite nonnegative one-dimensional sales')
    positive=np.flatnonzero(y>0)
    if not len(positive):return 0.,0.
    first=int(positive[0]);size=y[first];interval=float(first+1);prob=1/interval;gap=0
    for value in y[first+1:]:
        gap+=1
        prob=(1-alpha)*prob+alpha*float(value>0)
        if value>0:
            size=(1-alpha)*size+alpha*value
            interval=(1-alpha)*interval+alpha*gap
            gap=0
    return float((1-alpha/2)*size/interval),float(prob*size)


def forecast(history):
    y=np.asarray(history,dtype=float)
    sba,tsb=intermittent_rates(y)
    if len(y)<28:raise ValueError('Insufficient forecast history')
    return {'zero':0.,'last_week':float(y[-7:].sum()),'rolling_28':float(7*y[-28:].mean()),'croston_sba':7*sba,'tsb':7*tsb}


def predict(panel,origins):
    rows=[];scale=panel.loc['2010'].mean()*7
    if (scale<=0).any():raise ValueError('Nonpositive training normalization')
    for origin in origins:
        for product in panel:
            history=panel.loc[panel.index<origin,product]
            target=panel.loc[origin:origin+pd.Timedelta(days=6),product]
            if len(target)!=7:raise ValueError('Incomplete target week')
            if not np.isfinite(target).all():raise ValueError('Unknown target sales')
            for model,value in forecast(history).items():
                rows.append({'origin':origin,'target_end':origin+pd.Timedelta(days=6),'product':product,'model':model,
                             'observed':float(target.sum()),'prediction':value,'training_weekly_scale':float(scale[product])})
    return pd.DataFrame(rows)


def summarize(frame):
    records=[]
    for model,g in frame.groupby('model',sort=False):
        error=g.prediction-g.observed
        records.append({'model':model,'product_weeks':len(g),'macro_scaled_mae':float((error.abs()/g.training_weekly_scale).mean()),
                        'unit_mae':float(error.abs().mean()),'mean_error_units':float(error.mean()),
                        'signed_total_error_units':float(error.sum()),
                        'observed_total_units':float(g.observed.sum()),'forecast_total_units':float(g.prediction.sum()),
                        'underforecast_product_weeks':int((error<0).sum())})
    return records


def run():
    out,started=start_run('retail')
    panel=pd.read_csv(ROOT/'data/snapshots/retail-daily-panel.csv.gz',index_col=0,parse_dates=True)
    predictions=predict(panel,pd.date_range('2011-01-03','2011-11-28',freq='W-MON'))
    save_frame(predictions,out/'predictions.csv.gz')
    metrics=summarize(predictions);write_json(out/'metrics.json',{'primary':metrics,'products':len(panel.columns),'weeks':predictions.origin.nunique()})
    product=[];quarter=[]
    for name,g in predictions.groupby('product'):
        product.extend([{'product':name,**row} for row in summarize(g)])
    for name,g in predictions.groupby(predictions.origin.dt.quarter):
        quarter.extend([{'quarter':int(name),**row} for row in summarize(g)])
    pd.DataFrame(product).to_csv(out/'per-product.csv',index=False)
    pd.DataFrame(quarter).to_csv(out/'per-quarter.csv',index=False)
    table=pd.DataFrame(metrics).set_index('model').loc[MODELS]
    fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    colors=['#6b7280','#9ca3af','#2563eb','#0f766e','#b45309']
    axes[0].barh(MODELS,table.macro_scaled_mae,color=colors)
    axes[0].set_xlabel('Weekly MAE / mean training-week sales (lower is better)')
    axes[0].set_title('Weekly error, equally weighted products')
    bias=(table.forecast_total_units/table.observed_total_units-1)*100
    axes[1].barh(MODELS,bias,color=colors);axes[1].axvline(0,color='black',lw=.8)
    axes[1].set_xlabel('Total forecast minus recorded sales (%)');axes[1].set_title('Underforecasting remains visible')
    fig.suptitle('24 established intermittent products • 48 complete test weeks')
    fig.tight_layout();fig.savefig(out/'weekly-sales.png');plt.close(fig)
    best=min(metrics,key=lambda x:x['macro_scaled_mae'])
    headers=['Model','Scaled weekly MAE','Unit MAE','Forecast total','Recorded total']
    rows=[[m['model'],f"{m['macro_scaled_mae']:.3f}",f"{m['unit_mae']:.2f}",f"{m['forecast_total_units']:.1f}",f"{m['observed_total_units']:.0f}"] for m in metrics]
    report=f'''# What should next week's sales forecast optimize?

For this fixed panel, **{best['model']} has the lowest normalized weekly absolute
error ({best['macro_scaled_mae']:.3f})**. The total-sales comparison below shows
whether a low-error forecast still systematically understates recorded sales.
Neither criterion alone establishes an inventory decision or unmet demand.

{markdown_table(headers,rows)}

![Weekly errors and systematic bias](weekly-sales.png)

## What this comparison means

The cohort contains 24 products selected using 2010 sales only, from 2,072 eligible
intermittent products. We evaluated {predictions.origin.nunique()} full weeks in 2011.
Forecasts update using prior transactions only; all smoothing settings were fixed
before test scoring. The mean training-week denominator gives small products a
voice; the second panel instead counts units across products and is dominated by
larger sellers. Those answer different questions. See [per-product](per-product.csv)
and [quarterly](per-quarter.csv) evidence before generalizing a pooled ranking.

The workbook repeats 22,523 transaction rows across its annual sheets. Independent
source review verified exact duplicate multiplicities; using the later sheet at
the overlap prevents counting those sales twice. Cancellations, non-merchandise
codes and nonpositive sale rows are excluded under the frozen gross-sales target.
Missing customer IDs remain: product-level sales do not require customer identity.

## Limits and evidence

A recorded zero is not proof of availability or zero demand. This fixed,
nonrandom established-product panel includes later inactivity, and does not
represent new products. There is no stockout, profit or purchasing-cost outcome.
Signed bias is a sales-forecast diagnostic. Repeated rows within one annual sheet
remain because their meaning cannot be inferred safely from identical fields.

[Design](../../../studies/retail/DESIGN.md) ·
[Story](../../../studies/retail/STORY.md) · [Source audit](../../intake/retail.json) ·
[Predictions](predictions.csv.gz) · [Metrics](metrics.json) · [Run evidence](run.json).
Reproduce with `uv run atlas retail` from committed source.
Data: Daqing Chen, Online Retail II, UCI (2012), CC BY 4.0;
source and transformations are credited in the repository data documentation.
'''
    (out/'REPORT.md').write_text(report)
    finish_run('retail',out,started,{'test_origins':['2011-01-03','2011-11-28'],'alpha':.1,'models':MODELS,'selection_end':'2010-12-31'})


if __name__=='__main__':run()
