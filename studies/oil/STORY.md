# Oil prices: the process story

**Question:** Can volatility forecasts improve on simple baselines even when price-direction forecasts cannot?

**Data:** EIA daily spot prices for [WTI](https://www.eia.gov/dnav/pet/hist/RWTCD.htm) and [Brent](https://www.eia.gov/dnav/pet/hist/RBRTED.htm); the intended common-history snapshot ends in 2025.

**Status:** design only. This is a record of decisions already made and work still
to do, not a report of results. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected related oil-price histories to study a difficult distinction: a price may be hard to predict while the uncertainty around it still changes in useful ways.

## 2026-10-29 — Challenge the first plan

Review challenged assumptions about transformations, stable relationships between prices, and what a risk model would actually establish. A convenient mathematical transformation is not valid for every possible price.

## 2026-10-29 — Change the design before fitting

Direction and volatility will each be evaluated against their own simple benchmarks. We will ask where repeatable improvement exists, without directly comparing scores for different tasks. We will inspect price values and calendar gaps before choosing transformations. Any budget example will state its hypothetical assumptions rather than claiming measured savings or profitable trading.

Technical evidence and outstanding checks: [R11](../../reviews/01-design-review.md#r11--price-transformations-and-relationships-are-hypotheses), [R13](../../reviews/01-design-review.md#r13--a-checksum-is-not-an-archive-or-a-redistribution-license), and [R16](../../reviews/01-design-review.md#r16--the-story-must-stay-within-the-evidence).

## Next, not yet done

Inspect the actual price history, establish source-snapshot handling, and freeze comparable horizons and scoring. No price relationship or forecasting skill has been established.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).

