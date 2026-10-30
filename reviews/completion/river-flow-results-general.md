# River-flow results and publication — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Run source and protocol: `7e6c91d4777beccb3abb05870e880918197ae93f`.

Read the report, design, current story, complete summary metrics, descriptive
group table, and run metadata; visually inspected the figure. Linked prediction,
event, parameter, and split artifacts were hashed for scope, not independently
rebuilt by this general review. No model, test, or exact reproduction was run.

## Results verdict

**The saved evidence supports a useful, bounded answer: these methods recognize
high-flow days much more often than they warn before eligible new rises. Recent
weather adds a small high-day recall improvement, with an alert-episode tradeoff.**
This is a descriptive result on the selected known gauges, not an operational
warning or damage-reduction result.

At date offset +1, flow plus weather has macro high-day recall 0.9150 versus
0.9061 for flow only and 0.8919 for persistence. Its pooled eligible-onset recall
is much lower: 496/822 = 60.3%, versus 467/822 = 56.8% and 414/822 = 50.4%.
The weather model has 830 wholly false alert episodes, versus 653 for flow only
and 536 for persistence, even though its daily false-positive rate is slightly
lower. Episode count and false-positive days measure different features of an
alert stream; neither implies a cost without a decision model.

At +3, the weather/flow-only difference is small: macro high-day recall 0.7221
versus 0.7196, and 166 versus 165 alerted eligible onsets out of 696. The weather
model still misses 530 of those onsets. Across primary rows, test false-positive
rates are about 14.4–14.9%, above the approximate 10% calibration target. The
report correctly treats calibration as a rule, not a guaranteed future budget.

The two figure panels have different populations and weighting: macro gauge
high-day recall versus pooled eligible-onset recall. Their contrast is useful
but is not a causal estimate of changing the target or lead time. The +1 and +3
onset cohorts also differ. Current text correctly explains date offsets, input
availability assumptions, censoring, unknown truth, and the selected panel.

## Publication verdict

**Presentation and story amendments below are needed before publication.
Reproduction and final release gates remain separate.** No model, target, tuning,
or scoring change is requested by this general review.

### GRIV01 — State the measured answer and retain the tradeoff

Priority: medium; status: identified, parent has accepted a presentation update.

The report begins by describing two questions, rather than answering either.
Add a brief opening that conveys the limited additional benefit of recent
weather, the much lower eligible-onset recall, and the false-alert tradeoff.
Do not headline 91.5% as the fraction of new rises warned about. Use date-offset
language and preserve the test false-positive rates beside the recall claim.

The original question also asks about different catchment types. The linked
group data satisfy the evidence requirement, but one short descriptive summary
would help the reader: for example, +3 weather-model recall is about 0.858 in the
ten higher-cold-precipitation-fraction gauges versus 0.528 in the seven lower-group
gauges, with different false-positive rates (0.165 versus 0.120). These are small,
selected, descriptive groups, not an explanation of why rivers behave differently
or evidence that cold precipitation causes easier warning. No new analysis is
needed; a concise summary can point to the existing group table.

The figure clearly separates high days from new onsets and uses suitable axes.
Replace implementation identifiers such as `flow_weather` with readable labels.
If used alone on the portfolio, its caption must include the false-positive
tradeoff and date-offset limitation; recall-only panels should not become a
standalone claim of an effective flood warning system. The adjacent report
tables already provide those values.

### GRIV02 — Append the run/result step and update current metadata

Priority: medium; status: pending parent update.

The current data header still says the analytical subset is to be fixed, and the
status still says source intake complete. Update these to the actual selected
17-gauge panel and executed-but-pending-gates state. Append the run and measured
answer with report and review links. Keep the earlier dated "no model" statements
as history and retain the candid account of the calibration-boundary risk the
first review pass missed. Reproduction is not established by this review.

## Scope hashes

```text
7be3a0a749cc3ee3f93c2e0b7e22df75e29b926319d17d2e9204136c431f0192  reports/results/river-flow/REPORT.md
0af39059acf633a74c818405bef3d2340957e2bb2f06028da060475f5f72b33b  reports/results/river-flow/metrics.json
fd2b4ac1d3bc7ffacaa03a28ab356ef57be846eb07078360aec2b9a1dda5d5c8  reports/results/river-flow/flow-and-onsets.png
f0ca5b224e9590949f1dcacaea8cf1e72bae4348acfcc9d1e855afe8597df35c  reports/results/river-flow/group-scores.csv
63b44f22fadcc61a995fe13bc5b172bdb854ba665d42b1b650856931df66e7b0  reports/results/river-flow/gauge-scores.csv
65018e04323a5bb5e810b0f158002b9464b4a3b6b7ce2b07cf1c57d9ef48e411  reports/results/river-flow/catchment-groups.csv
ed6454881bf8ff270d43b90a8b83aadbea1e2fcad23cbb836636929780bbf2e6  reports/results/river-flow/events.csv.gz
f6eac62831ded8233484a88b16c7da93db2fb69bf1a3adc253a731749d109df2  reports/results/river-flow/parameters.json
530a67b01853c859d34780f0e82e1753d0ca85cc0fc798ad4fcf1fb2bb98588f  reports/results/river-flow/predictions.csv.gz
16fb0481f248a75068f8acc55e505df1e2dea46e02b35c692fc7e81deca15ba3  reports/results/river-flow/run.json
ec32436c279cce849bddd658a20141f7b15647216b07b14982ba679339d80905  reports/results/river-flow/split-audit.csv
996fef9e5d69d8187ecddbe4690592badfda3b825d91c123a5b03173cf2843ee  studies/river-flow/DESIGN.md
b80ef263a8a86d186be77dd437960ce14f553e1397af865a28d1c8d0494e73bb  studies/river-flow/STORY.md
```
