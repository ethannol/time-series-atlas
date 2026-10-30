# Air quality during sensor outages: the process story

**Question:** Can nearby stations preserve useful high-pollution warnings when a local sensor goes offline?

**Data:** [UCI Beijing Multi-Site Air Quality](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data); hourly pollution and weather observations at 12 stations, March 2013–February 2017.

**Status:** design only. This is a record of decisions already made and work still
to do, not a report of results. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected pollution measurements from several stations because nearby observations may help when a local instrument is unavailable. The revised question makes missing-data handling part of an actual warning task.

## 2026-10-29 — Challenge the first plan

The critics pointed out that hiding a few isolated readings would be an easy but potentially misleading experiment. Real outages can remove long stretches, and missing observations have no known truth to score against.

## 2026-10-29 — Change the design before fitting

We will deliberately hide continuous stretches where the readings are known, vary the outage length, and allow only information available when the warning is made. Later reconstruction will be kept separate. Simulated outages will be identified as simulations, not evidence about every real equipment failure.

Technical evidence and outstanding checks: [R08](../../reviews/01-design-review.md#r08--a-missing-point-is-not-a-station-outage) and [R12](../../reviews/01-design-review.md#r12--separate-tasks-and-protect-the-evaluation-process).

## Next, not yet done

Audit coverage and station timestamps, then define warning thresholds, timing, and outage experiments. No warning improvement or missing-value recovery has been measured.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).

