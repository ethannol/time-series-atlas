"""Post-publication reader context derived from the unchanged original evidence."""
import numpy as np
import pandas as pd
from .common import markdown_table
from .data import write_json


def fmt(value, digits=3):
    return 'undefined' if value is None or pd.isna(value) else f'{value:.{digits}f}'


def electricity_context(out, predictions, primary, peaks):
    models=['yesterday','last_week','local_ridge','pooled_ridge']
    local=primary['local_ridge'];pooled=primary['pooled_ridge']
    macro_change=100*(pooled['macro_normalized_mae']/local['macro_normalized_mae']-1)
    aggregate_change=100*(pooled['aggregate_mae_kw']/local['aggregate_mae_kw']-1)
    frame=predictions[(predictions.split=='test')&predictions.safe]
    loads=frame.groupby('client').actual.sum();total=loads.sum()
    rows=[];peak_rows=[]
    for customer in sorted(local['customers']):
        a=local['customers'][customer];b=pooled['customers'][customer]
        rows.append({'client':customer,'local_normalized_mae':a['normalized_mae'],
            'pooled_normalized_mae':b['normalized_mae'],'delta':b['normalized_mae']-a['normalized_mae'],
            'actual_load_share':float(loads[customer]/total)})
        peak_rows.append([customer,fmt(peaks[customer],1),a['peak_n'],
            *[fmt(primary[m]['customers'][customer]['peak_mae_kw'],2) for m in models]])
    table=pd.DataFrame(rows).sort_values(['delta','client'],ascending=[False,True])
    table.to_csv(out/'followup-customer-context.csv',index=False)
    net=float(table.delta.sum());top=table[table.delta>0].head(2)
    share=float(top.delta.sum()/net) if net else None
    share_text='undefined (zero net change)' if share is None else f'{share:.2%}'
    biggest=table.sort_values(['actual_load_share','client'],ascending=[False,True]).iloc[0]
    summary={'macro_mae_relative_change_percent':float(macro_change),
        'aggregate_mae_relative_change_percent':float(aggregate_change),
        'top_two_positive_delta_customers':top.client.tolist(),'top_two_share_of_net_delta':share,
        'largest_load_customer':biggest.client,'largest_actual_load_share':float(biggest.actual_load_share)}
    write_json(out/'followup-context.json',summary)
    peak_report='# High-load results for every selected customer\n\n'
    peak_report+='Secondary endpoint from the original frozen comparison. Peaks strictly exceed each customer’s 2012 90th percentile. Every method uses the same peak hours for that customer. Counts differ across customers; these are not the top tenth of each test series. MAE is in kW, without customer normalization.\n\n'
    peak_report+=markdown_table(['Customer','Training threshold kW','Test peak hours','Yesterday MAE','Last week MAE','Local ridge MAE','Pooled ridge MAE'],peak_rows)
    peak_report+='\n[Main report](REPORT.md) · [Original metrics](metrics.json).\n'
    (out/'followup-peak-scores.md').write_text(peak_report)
    return f'''\n## Follow-up: how large is the disadvantage, and who contributes?

Added after publication on 2026-11-10, using the same saved comparisons. Relative
to separate regression, pooled regression changes macro normalized MAE by
**{macro_change:+.2f}%** and aggregate MAE by **{aggregate_change:+.2f}%**. These
are relative changes in error, not percentage errors on each observation or
measured business costs. The original count of customers harmed does not show
the magnitude by itself.

The two largest positive customer-normalized error changes,
{', '.join(top.client)}, account for {share_text} of the **signed net** increase
summed across customers. Gains elsewhere reduce that denominator. Separately,
{biggest.client} contributes {biggest.actual_load_share:.2%} of actual load on
the primary test dates. Load share alone does not prove error dominance: the
aggregate score sums signed prediction errors before taking an absolute value.
No customer was removed or reweighted after inspecting these summaries.

[All customer deltas and load shares](followup-customer-context.csv) ·
[Every customer's high-load threshold, count and method scores](followup-peak-scores.md) ·
[Summary values](followup-context.json).
'''


def oil_context(out):
    variance=pd.read_csv(out/'variance-subgroups.csv')
    variance=variance[variance['group'].str.startswith('year_')].copy()
    variance['year']=variance['group'].str.removeprefix('year_').astype(int)
    direction=pd.read_csv(out/'direction-years.csv')
    rows=[];direction_rows=[];contributions=[]
    for market,g in variance.groupby('market'):
        q=g.pivot(index='year',columns='model',values='qlike')
        counts=g.pivot(index='year',columns='model',values='n')
        assert (counts.eq(counts.fixed,axis=0)).all().all()
        gain=counts.fixed*(q.fixed-q.ewma);net=float(gain.sum())
        d=direction[direction.market==market].pivot(index='year',columns='model',values='brier')
        dn=direction[direction.market==market].pivot(index='year',columns='model',values='n')
        assert (dn.eq(dn.prevalence,axis=0)).all().all()
        for year in q.index:
            fraction=float(gain.loc[year]/net) if net else None
            rows.append([market.upper(),int(year),int(counts.loc[year,'fixed']),
                *[fmt(q.loc[year,m],4) for m in ['fixed','rolling_60','ewma','garch']],
                'undefined' if fraction is None else f'{fraction:.1%}'])
            contributions.append({'market':market,'year':int(year),'n':int(counts.loc[year,'fixed']),
                'fixed_minus_ewma_qlike_sum':float(gain.loc[year]),'share_of_net_gain':fraction})
            direction_rows.append([market.upper(),int(year),int(dn.loc[year,'prevalence']),
                fmt(d.loc[year,'prevalence'],4),fmt(d.loc[year,'logistic'],4),
                fmt(d.loc[year,'logistic']-d.loc[year,'prevalence'],4)])
    pd.DataFrame(contributions).to_csv(out/'followup-year-contributions.csv',index=False)
    text='\n## Follow-up: does the pooled result describe every year?\n\n'
    text+='This descriptive breakdown was added after publication. Every year is shown, including reversals. Smaller QLIKE is better. The last column weights each year’s fixed-minus-EWMA QLIKE difference by its target count, then divides by the signed sum across all years. Negative contributions offset gains; these shares need not lie between zero and one. No year is excluded or selected for fitting.\n\n'
    text+=markdown_table(['Market','Year','Targets','Fixed QLIKE','Rolling QLIKE','EWMA QLIKE','GARCH QLIKE','Share of net EWMA gain'],rows)
    text+='\nDirection uses its own observed-target counts. Negative logistic-minus-prevalence Brier favors logistic. Winning the full-period average does not mean winning every year; these are descriptive slices, not independent significance tests.\n\n'
    text+=markdown_table(['Market','Year','Targets','Prevalence Brier','Logistic Brier','Difference'],direction_rows)
    text+='\n[Weighted annual contributions](followup-year-contributions.csv) · [Full annual/gap evidence](variance-subgroups.csv) · [Direction years](direction-years.csv).\n'
    return text


def air_context(out, events, predictions):
    high=events[(events.model=='persistence')&(events.type=='high_event')]
    rows=[];records=[]
    for duration,g in high.groupby('duration'):
        row={'duration':int(duration),'high_runs':len(g),'left_censored':int(g.left_censored.sum()),
            'right_censored':int(g.right_censored.sum()),
            'both_boundaries':int((g.left_censored&g.right_censored).sum())}
        records.append(row);rows.append(list(row.values()))
    write_json(out/'followup-censoring.json',{'support':records})
    calendar=predictions[predictions.model=='calendar']
    alerts=int((calendar.prediction>calendar.threshold).sum())
    text='\n## Follow-up: what the baseline and event boundaries imply\n\n'
    text+=f'The calendar-median baseline issued {alerts} high-hour indications in these scheduled, eligible blocks. Its overall balanced accuracy of 0.5 reflects recognizing non-high hours while missing high hours. This does not show that all possible local warning methods fail. MAE elsewhere in this report is averaged equally over stations.\n\n'
    text+=markdown_table(['Outage hours','True high runs','Left boundary','Right boundary','Both boundaries'],rows)
    text+='\nTruth runs are counted once per duration, using one method’s copy of the shared truth. Left-censored means already high at the block start; right-censored means still high at the block end. These counts overlap and are not additional missed events. Delay remains conditional on detected, non-left-censored runs; natural missing observations still have unknown truth. [Saved counts](followup-censoring.json).\n'
    return text
