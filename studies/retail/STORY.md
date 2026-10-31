# Intermittent retail sales: the process story

**Question:** How should we forecast next week's recorded sales for stock codes that sell only occasionally?

**Data:** [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii); timestamped transactions from December 2009 to December 2011, aggregated into daily product series and complete weekly targets.

**Current status (2026-10-30):** executed, independently reviewed and reproduced
from a fresh checkout. GitHub and live portfolio publication are verified. Earlier dated
entries preserve what was known at each stage. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected transaction records to investigate products with many days without sales. The planning problem is appealing because a forecast that looks reasonable day by day might still miss the total sold over a week.

## 2026-10-29 — Challenge the first plan

Review stressed that recorded sales do not tell us how many customers wanted an unavailable item. It also challenged how cancellations, product entry, and zero-heavy scoring would be handled.

## 2026-10-29 — Change the design before fitting

The target is observed sales, with cancellations treated explicitly. Product selection will use only information available at the time. Evaluation will include weekly totals and systematic underprediction so the tradeoffs of an always-zero forecast remain visible.

Technical evidence and outstanding checks: [R06–R07](../../reviews/01-design-review.md#r06--transactions-tell-us-what-sold-not-everything-customers-wanted).

## Next at planning time — 2026-10-29

Audit transaction types and product histories, then freeze the target and comparison rules. We have not estimated unmet demand, optimized inventory, or measured forecast performance.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Discover that the source repeats sales

The workbook's two annual sheets overlap. Independent intake review compared
the complete rows and found exactly 22,523 transactions repeated in both sheets,
including their duplicate multiplicities. We used the later sheet for that
period, preventing double counting. The audit also kept cancellations distinct
from positive recorded sales and selected products using 2010 information only.

## 2026-10-30 — Check the forecast before looking at its score

We froze the weekly target and five simple comparisons. Review checked that
future sales could not enter an earlier forecast and that inactivity affected
the intermittent-sales methods as intended. A small development trial exercised
the pipeline without comparing accuracy. The signed total error was added
explicitly so underforecasting would remain visible beside the headline score.

## 2026-10-30 — A zero forecast wins one score and misses every sale

The first full run scored 24 products over 48 complete weeks. Always predicting
zero had the lowest average normalized absolute error, yet missed all 33,858
recorded units. The result makes the choice of evaluation question tangible:
low error alone does not tell a planner what to order. Other methods predict totals much closer to the recorded sales volume. This dataset still cannot reveal unmet demand or an
optimal purchasing decision. Results and publication review are pending.

[Report](../../reports/results/retail/REPORT.md) ·
[Independent source/design review](../../reviews/completion/design-implementation.md) ·
[Pre-run statistical review](../../reviews/completion/retail-implementation-statistical.md).

## 2026-10-30 — Check the decision hidden inside the score

Independent reviewers reproduced the predictions and scores, then asked us to
make the disagreement between metrics explicit. Zero won normalized absolute
error; TSB won raw-unit error and its forecast total was much closer to recorded
sales. Most product-weeks had no sales, so a median-oriented loss could reward
zero while missing all volume. Neither score establishes what stock to buy.

We revised the explanation and figure labels without changing any numerical
artifact. [Results review](../../reviews/completion/retail-results-general.md)
records that interpretation; final fresh-checkout reproduction and publication
are separate delivery checks.

## 2026-10-30 — Reproduce the complete result from a new checkout

A new locked environment reproduced every published numerical and presentation
file for this study exactly, compared against the committed reference hashes.
The full collection also passed forty-one tests. This is a reproduction check,
not new evidence of operational or scientific generalization.

[Full reproduction record](../../reports/verification/completion-reproduction.json).

## 2026-10-30 — Publish and verify the result readers receive

The reviewed collection merged after green checks. The deployed portfolio links
this report and its evidence, and the live page was checked against the published
revision. [Rollout record](../../reports/verification/completion-rollout.json).

## 2026-10-30 — Check what a “product” identifier means

The fresh retail critic reproduced the source panel and every saved score, then
asked whether our product labels implied more identity certainty than the data
supplied. Some differently capitalized stock codes share descriptions. Without
a verified crosswalk, we cannot tell whether a quiet code means a discontinued
product or activity recorded under another identifier.

We now describe the exact case-sensitive codes prominently. The original panel
and scores remain unchanged; merging identifiers after seeing the result would
require a separate, reviewed analysis. [Dedicated critique](../../reviews/study-critiques-20261030/retail.md)
and [resolution status](../../reviews/study-critiques-20261030/RESPONSE.md).
