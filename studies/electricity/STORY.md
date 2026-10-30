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

