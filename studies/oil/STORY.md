# Oil prices: the process story

**Question:** Can volatility forecasts improve on simple baselines even when price-direction forecasts cannot?

**Data:** EIA daily spot prices for [WTI](https://www.eia.gov/dnav/pet/hist/RWTCD.htm) and [Brent](https://www.eia.gov/dnav/pet/hist/RBRTED.htm); the intended common-history snapshot ends in 2025.

**Current status (2026-10-30):** source intake complete; later dated entries
record implementation and results status. Earlier entries preserve the original plan. Ethan set the direction and requested the critical
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


## 2026-10-30 — Check both mathematical and reuse assumptions

The actual WTI file contains a negative price. We retained it and chose dollar
changes, since ordinary log returns would fail on that observation. We also
verified that EIA identifies Refinitiv as the price source. Free access through
a government website does not, by itself, settle redistribution rights.

The study will fetch price inputs for local use and publish our analysis outputs,
without claiming the underlying prices are government-owned. A normalized-input
hash will detect changes to the historical data. Future source revisions may
prevent exact public reproduction; that limitation is explicit. The oil study
remains in scope, with separate direction and volatility questions and scores.

[Design](DESIGN.md) · [Review](../../reviews/completion/design-general.md).
