# Intermittent retail sales: the process story

**Question:** How should we forecast next week's sales for products that sell only occasionally?

**Data:** [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii); timestamped transactions from December 2009 to December 2011, to be aggregated into product sales series.

**Status:** design only. This is a record of decisions already made and work still
to do, not a report of results. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected transaction records to investigate products with many days without sales. The planning problem is appealing because a forecast that looks reasonable day by day might still miss the total sold over a week.

## 2026-10-29 — Challenge the first plan

Review stressed that recorded sales do not tell us how many customers wanted an unavailable item. It also challenged how cancellations, product entry, and zero-heavy scoring would be handled.

## 2026-10-29 — Change the design before fitting

The target is observed sales, with cancellations treated explicitly. Product selection will use only information available at the time. Evaluation will include weekly totals and systematic underprediction so the tradeoffs of an always-zero forecast remain visible.

Technical evidence and outstanding checks: [R06–R07](../../reviews/01-design-review.md#r06--transactions-tell-us-what-sold-not-everything-customers-wanted).

## Next, not yet done

Audit transaction types and product histories, then freeze the target and comparison rules. We have not estimated unmet demand, optimized inventory, or measured forecast performance.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).

