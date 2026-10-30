# Electricity demand: the process story

**Question:** When does learning across customers improve tomorrow's load forecast, and who benefits or suffers?

**Data:** [UCI Electricity Load Diagrams 2011–2014](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014); 15-minute readings for 370 customers, with explicit aggregation planned.

**Status:** design only. This is a record of decisions already made and work still
to do, not a report of results. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected electricity readings from many customers to compare individual forecasting with learning shared patterns. This is a natural planning problem: forecasts should help at both customer and aggregate levels.

## 2026-10-29 — Challenge the first plan

The review emphasized that some zeros mean a customer was not yet active, while clock changes have special encoding. It also challenged a plan that tried to demonstrate too many techniques in one study.

## 2026-10-29 — Change the design before fitting

The main comparison is now whether sharing information helps different customers. We will define which customers are eligible using only earlier information, audit what zeros mean, and keep clock handling explicit. An improvement in the total must not hide customers whose forecasts become worse.

Technical evidence and outstanding checks: [R03](../../reviews/01-design-review.md#r03--electricity-zeros-and-time-labels-are-not-self-explanatory) and [R12](../../reviews/01-design-review.md#r12--separate-tasks-and-protect-the-evaluation-process).

## Next, not yet done

Inspect the files and their time/unit conventions, then freeze customer selection and evaluation. No demand model, saving, or improvement has been demonstrated.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Find a mismatch between description and readings

We downloaded the full archive. The provider says customers have zeros during a
spring clock-change window, but the reviewers found customers with nonzero
readings there. We therefore flag transition dates by calendar, not by looking
for every customer to become zero. The hourly clock convention is documented as
an assumption, rather than pretending to recover exact physical-time readings.

## 2026-10-30 — Make the comparison fair and bounded

The panel uses 24 established customers selected from earlier data across a range
of consumption levels. Review required the separate and shared models to use the
same penalty per observation and the same handling of impossible negative
forecasts. The contract was frozen before evaluation.

## 2026-10-30 — Catch a scoring defect before the full run

A critic deliberately supplied a missing prediction. The scoring code could
silently drop it from one average while still reporting the full observation
count. That was a real implementation defect, although it had not yet affected a
study result. Missing, duplicate, or mismatched prediction records now fail
explicitly, and tests preserve that behavior.

[Source/design evidence](../../reviews/first-release/README.md) ·
[Scoring review](../../reviews/first-release/implementation/statistical.md).
