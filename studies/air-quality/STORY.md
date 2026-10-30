# Air quality during sensor outages: the process story

**Question:** Can nearby stations preserve useful high-pollution warnings when a local sensor goes offline?

**Data:** [UCI Beijing Multi-Site Air Quality](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data); hourly pollution and weather observations at 12 stations, March 2013–February 2017.

**Current status (2026-10-30):** executed and independently checked; final
presentation and clean-checkout reproduction remain pending. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected pollution measurements from several stations because nearby observations may help when a local instrument is unavailable. The revised question makes missing-data handling part of an actual warning task.

## 2026-10-29 — Challenge the first plan

The critics pointed out that hiding a few isolated readings would be an easy but potentially misleading experiment. Real outages can remove long stretches, and missing observations have no known truth to score against.

## 2026-10-29 — Change the design before fitting

We will deliberately hide continuous stretches where the readings are known, vary the outage length, and allow only information available when the warning is made. Later reconstruction will be kept separate. Simulated outages will be identified as simulations, not evidence about every real equipment failure.

Technical evidence and outstanding checks: [R08](../../reviews/01-design-review.md#r08--a-missing-point-is-not-a-station-outage) and [R12](../../reviews/01-design-review.md#r12--separate-tasks-and-protect-the-evaluation-process).

## Next at planning time — 2026-10-29

Audit coverage and station timestamps, then define warning thresholds, timing, and outage experiments. No warning improvement or missing-value recovery has been measured.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Hide outages, not isolated convenient readings

We acquired and checked all twelve station histories. The experiment removes
one station at a time for 6, 24 or 72 consecutive hours, on a fixed schedule.
Review verified that concealed local values and later endpoints cannot leak
into predictions. Unknown natural gaps are excluded from scoring, not filled
and treated as known truth.

## 2026-10-30 — Separate data availability from the ability to score

Pre-run review caught an ambiguous coverage statistic. A block may have nearby
readings sufficient to make a prediction while missing local truth needed to
score it. We now count those separately across the complete scheduled scope.
This is an example of asking what a denominator actually represents before
accepting a performance chart.

## 2026-10-30 — Nearby readings help, but a more fitted model adds little to the warning score

Other-station medians outperformed holding the last local reading at all three
outage lengths. Learned calibration reduced concentration error but produced
almost the same balanced high/low warning accuracy, with recall and false-alarm
tradeoffs. We report those rates separately.

Nearby inputs were available throughout this particular schedule, yet only
73.6% of scheduled 72-hour observations belonged to scoreable blocks with known
local truth. The simulation cannot establish performance on every real outage.
A zero conditional detection delay or zero wholly false alert episodes also
cannot establish that there were no misses or false-positive hours.

Independent reviewers recalculated every saved prediction, score and event.
Final presentation and clean-checkout reproduction remain pending.

[Executed report](../../reports/results/air-quality/REPORT.md) ·
[Results review](../../reviews/completion/air-quality-results-statistical.md).
