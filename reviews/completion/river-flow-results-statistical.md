# River-flow results review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Run source/protocol: `7e6c91d4777beccb3abb05870e880918197ae93f`.
Scope: saved predictions, source snapshot, fitted/calibrated parameters, split and
event ledgers, metric tables, figure, report and study story. No models were
refitted and no final-score-driven change was requested.

**Results verdict: approved.** Independent arithmetic and source alignment match
the saved outputs. **Publication verdict: pending RF-P01 below and the planned
exact-reproduction gate.** The numerical result is usable; the current narrative
has not yet explained the actual answer or brought the process story current.

## Independent checks completed

All 288,417 prediction rows have unique gauge/horizon/model/target keys, correct
source target flow and high-flow labels, exact calendar offsets, and origins on
or after December 31, 2004. The common cohorts contain 48,262 next-day and 47,877
three-day targets per method. Every comparison includes the same 17 gauges;
there are no unmatched gauge/horizon pairs or unevaluable model substitutions.

This reviewer reconstructed origin-time features directly from the pinned daily
panel, approved-flow flags and calendar. Training percentile thresholds, training
scaler means/standard deviations, saved-coefficient logistic scores, persistence
scores, calibration-negative percentiles and all alert decisions match. Maximum
absolute prediction-score difference was approximately 3.6e-15. There are no
recorded logistic convergence warnings. Computing predictions from saved
coefficients is an audit of the existing run, not a model refit.

All train/calibration/test and invalid-input/target overlap counts independently
reconcile. Scheduled test targets after boundary guards are 62,084 at offset one
and 62,050 at offset three; invalid unions exclude 13,822 and 14,173, respectively.
The latter horizon also removes two boundary targets per gauge. Consequently,
these scores apply to approximately 77.7% and 77.2% of scheduled targets, not all
calendar days. Every model uses the same information/truth mask for its comparison.

Independent confusion-count arithmetic reproduces every per-gauge score, all six
primary macros and contributor counts, and all area/climate subgroup rows.
Catchment areas and the training-only cold-precipitation calculation reproduce
the subgroup labels from the source. Persistence Brier is correctly null because
its score is not a probability. No daily independence assumption or significance
claim is needed for these descriptive comparisons.

The reviewer independently rebuilt all 10,158 event-ledger rows using the complete
calendar rather than calling the study's event function. Starts, ends, origins,
target dates, unknown-boundary censoring, forecast coverage, retrospective onset
eligibility, missed/alerted onsets, fully observed false-alert episodes and
unresolved segments all match. Every reported event count/rate follows from those
rows. Missing truth and absent forecasts are not silently treated as low flow.

All output hashes in `run.json` match the inspected artifacts. The recorded
source/snapshot identities match the approved implementation and intake. This
checks the saved run's integrity; independent full-command reproduction remains
a separate later gate.

## What the evidence supports

| Date offset | Method | Macro high-day recall | Macro false-positive rate | Alerted / eligible onsets |
| --- | --- | ---: | ---: | ---: |
| 1 | Persistence | 0.8919 | 0.1471 | 414 / 822 |
| 1 | Flow only | 0.9061 | 0.1482 | 467 / 822 |
| 1 | Flow + weather | 0.9150 | 0.1456 | 496 / 822 |
| 3 | Persistence | 0.7146 | 0.1486 | 147 / 696 |
| 3 | Flow only | 0.7196 | 0.1442 | 165 / 696 |
| 3 | Flow + weather | 0.7221 | 0.1462 | 166 / 696 |

The methods recognize continuing high-flow days much more often than they flag
an eligible new rise. Weather adds 29 alerted eligible onsets to flow-only at
offset one, but only one at offset three. The macro high-day recall difference
is similarly small: approximately +0.009 and +0.003. Gauge-level recall improves
in 6, ties in 10 and worsens in 1 gauge at offset one; the corresponding counts
at offset three are 5, 6 and 6. This is not uniform improvement across catchments.

The false-alert tradeoff needs equal prominence. Flow+weather has 830 fully
observed false episodes versus 653 for flow-only at offset one, despite a slightly
lower false-positive-day rate. At offset three those counts are 697 versus 547,
with a slightly higher false-positive-day rate. Episode fragmentation and total
false-positive days answer different questions. Unresolved segments stay
separate (42 versus 47 at offset one; 69 versus 73 at offset three), not counted
as proven false episodes. There is no measured response cost or flood-damage
outcome from which to turn these into operational utility.

Actual later-period false-positive rates are roughly 14–15%, above the nominal
10% calibration target. No claim that calibration guarantees a future budget is
supported. The figure correctly labels the equal-gauge high-day metric and the
pooled eligible-onset metric; their difference is not a paired effect estimate
over an identical population. Daily date offsets and retrospective forcing
availability assumptions remain explicit rather than claiming hourly lead times.

## RF-P01 — Complete the empirical answer and current story

Type: publication omission, not a numerical defect. Priority: close before
publication. The present report describes how to read its tables but does not
state their empirical answer. Add a short bounded conclusion covering limited
onset performance, the modest weather increment, false-positive-day/episode
tradeoffs and incomplete scoring coverage. Preserve the different denominators
and the idealized availability assumption; do not claim operational flood benefit.

The current study story still ends at pre-implementation review. Its top Data
summary says the analytical subset remains to be fixed even though it now contains
17 fixed gauges. Update current summaries and append the actual implementation,
results and review milestones. Preserve historical entries, including the lead
agent's discovery of the origin-boundary hazard and reviewers' earlier miss.

Closure needs inspection of regenerated report/story wording and confirmation
that numerical predictions/metrics remain unchanged. It does not require model
retuning or a new scientific experiment.

## Inspected SHA-256 identities

```text
f9166af30692780c85e8e276ad6081fed4c28821d6f89cc90200b2ed34e36829  src/tsatlas/river_flow.py
392dd930c5a975488d938ae56ee722982c02feca9f32b0bb0a7d8af299295956  data/snapshots/river-daily-panel.csv.gz
530a67b01853c859d34780f0e82e1753d0ca85cc0fc798ad4fcf1fb2bb98588f  reports/results/river-flow/predictions.csv.gz
ed6454881bf8ff270d43b90a8b83aadbea1e2fcad23cbb836636929780bbf2e6  reports/results/river-flow/events.csv.gz
0af39059acf633a74c818405bef3d2340957e2bb2f06028da060475f5f72b33b  reports/results/river-flow/metrics.json
f6eac62831ded8233484a88b16c7da93db2fb69bf1a3adc253a731749d109df2  reports/results/river-flow/parameters.json
ec32436c279cce849bddd658a20141f7b15647216b07b14982ba679339d80905  reports/results/river-flow/split-audit.csv
63b44f22fadcc61a995fe13bc5b172bdb854ba665d42b1b650856931df66e7b0  reports/results/river-flow/gauge-scores.csv
f0ca5b224e9590949f1dcacaea8cf1e72bae4348acfcc9d1e855afe8597df35c  reports/results/river-flow/group-scores.csv
65018e04323a5bb5e810b0f158002b9464b4a3b6b7ce2b07cf1c57d9ef48e411  reports/results/river-flow/catchment-groups.csv
fd2b4ac1d3bc7ffacaa03a28ab356ef57be846eb07078360aec2b9a1dda5d5c8  reports/results/river-flow/flow-and-onsets.png
7be3a0a749cc3ee3f93c2e0b7e22df75e29b926319d17d2e9204136c431f0192  reports/results/river-flow/REPORT.md
16fb0481f248a75068f8acc55e505df1e2dea46e02b35c692fc7e81deca15ba3  reports/results/river-flow/run.json
b80ef263a8a86d186be77dd437960ce14f553e1397af865a28d1c8d0494e73bb  studies/river-flow/STORY.md
```
