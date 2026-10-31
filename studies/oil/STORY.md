# Oil prices: the process story

**Question:** Can volatility forecasts improve on simple baselines even when price-direction forecasts cannot?

**Data:** EIA daily spot prices for [WTI](https://www.eia.gov/dnav/pet/hist/RWTCD.htm) and [Brent](https://www.eia.gov/dnav/pet/hist/RBRTED.htm); the pinned study snapshot ends in 2025.

**Current status (2026-10-30):** executed, independently reviewed and reproduced
from a fresh checkout. GitHub and live portfolio publication are verified. Earlier dated
entries preserve what was known at each stage. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected related oil-price histories to study a difficult distinction: a price may be hard to predict while the uncertainty around it still changes in useful ways.

## 2026-10-29 — Challenge the first plan

Review challenged assumptions about transformations, stable relationships between prices, and what a risk model would actually establish. A convenient mathematical transformation is not valid for every possible price.

## 2026-10-29 — Change the design before fitting

Direction and volatility will each be evaluated against their own simple benchmarks. We will ask where repeatable improvement exists, without directly comparing scores for different tasks. We will inspect price values and calendar gaps before choosing transformations. Any budget example will state its hypothetical assumptions rather than claiming measured savings or profitable trading.

Technical evidence and outstanding checks: [R11](../../reviews/01-design-review.md#r11--price-transformations-and-relationships-are-hypotheses), [R13](../../reviews/01-design-review.md#r13--a-checksum-is-not-an-archive-or-a-redistribution-license), and [R16](../../reviews/01-design-review.md#r16--the-story-must-stay-within-the-evidence).

## Next at planning time — 2026-10-29

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

## 2026-10-30 — Review units and preserve earlier evidence

Before the full run, technical review caught a variance floor expressed in the
wrong units inside the standardized optimizer. We corrected its scale and added
a regression check. Review also required private outcome files to be immutable,
so a failed later run could not overwrite the evidence supporting an earlier
report. The repaired implementation passed independent pre-run checks.

## 2026-10-30 — Uncertainty and direction give different answers

Adaptive variance forecasts beat a fixed variance on the declared QLIKE score
for both WTI and Brent. The direction model instead performed worse than a
simple historical upward-frequency baseline. GARCH's advantage over simple EWMA
was small. The fixed variance won the absolute squared-change-error comparison,
which asks a different statistical question. We kept all of those results.

Independent reviewers reconstructed the forecasts from saved parameters and
recalculated the scores without refitting. Final presentation and clean-checkout
reproduction remain pending. No settings changed after seeing the test scores.

[Executed report](../../reports/results/oil/REPORT.md) ·
[Results review](../../reviews/completion/oil-results-statistical.md).

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

## 2026-10-30 — A published forecast can reveal part of its target

The fresh oil critic reproduced the calculations, then tested what a reader
could recover from the public forecasts alone. Consecutive adaptive variance
forecasts reveal squared price changes. Keeping source workbooks and signed
outcomes out of Git does not make all derived outcomes unrecoverable.

We added that disclosure to the report and data documentation and retained the
already-public analysis and its history. The finding neither reconstructs the
complete signed price history nor establishes a licence violation. It changes
how we explain the publication boundary, not the forecast scores.

[Dedicated critique](../../reviews/study-critiques-20261030/oil.md) ·
[Resolution status](../../reviews/study-critiques-20261030/RESPONSE.md).
