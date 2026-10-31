# River flow: the process story

**Question:** How much warning of high flow can recent rainfall and flow provide across different catchment types?

**Data:** [CAMELS-US](https://ncar.github.io/hydrology/datasets/); daily streamflow and weather for US catchments, with a 17-gauge panel selected using geography and training-period approved-flow coverage.

**Current status (2026-10-30):** executed, independently reviewed and reproduced
from a fresh checkout. GitHub and live portfolio publication are verified. Earlier dated
entries preserve what was known at each stage. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected paired weather and river-flow records because rivers respond to rainfall with different delays. Comparing catchments could show when recent observations give useful advance warning.

## 2026-10-29 — Challenge the first plan

The reviewers found that some supplied catchment descriptions already summarize the river flow we might predict. They also pointed out that observed future rainfall is not information available to a forecaster today.

## 2026-10-29 — Change the design before fitting

We will trace where each input comes from and what would be known when a warning is issued. Any later experiment on ungauged rivers must exclude descriptors calculated from their flow. The study must distinguish advance warning from reconstructing an event after its weather is known.

Technical evidence and outstanding checks: [R04–R05](../../reviews/01-design-review.md#r04--some-catchment-descriptors-already-contain-the-outcome) and [R14](../../reviews/01-design-review.md#r14--resolve-actual-camels-files-and-versions).

## Next at planning time — 2026-10-29

Acquire and audit the intended source files, choose a fixed catchment subset, and define warning horizons and reporting assumptions. No high-flow performance or transfer result exists yet.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Resolve the archive and inspect real daily records

The official archive can be read in bounded pieces, so we acquired the needed
members without downloading several gigabytes of unrelated data. A fixed rule
selected 17 geographic regions using past measurement coverage. We kept failed
candidates and quality flags visible, rather than replacing gauges based on
later performance.

Actual records differed from convenient documentation assumptions: flow has a
quality column, and the weather hour field does not establish a publication
time. Intake also caught a positional-column mistake before design approval;
temperatures now use explicit column names. The proposed study separates
continuing high water from warning before a new rise. No model has run yet.

[Source review](../../reviews/completion/source-implementation.md).

## 2026-10-30 — Check when the warning rule itself becomes available

A later design check by the lead agent caught a boundary problem that the first
review pass had missed. The earliest three-day forecasts could have used a
cutoff calibrated on outcomes occurring after their forecast origin. We amended
the date rules before implementation and added a boundary test. Independent
reviewers verified the amendment and recorded that their earlier approval had
missed it. Review is repeated because one pass cannot guarantee correctness.

## 2026-10-30 — Recognizing high water is not the same as early warning

We ran the frozen comparison on the seventeen retained gauges. Past weather
added only a little to recognizing high-flow days. Before new rises, the
next-day weather model alerted on 496 of 822 eligible events, compared with
467 using flow alone, but generated more fully observed false-alert episodes.
At the three-day date offset it added just one detected onset.

The roughly ten-percent calibration false-positive target became about
fourteen to fifteen percent in the test period. We kept that loss of calibration
visible, alongside missed onsets and the daily-information assumption. Separate
reviewers reconstructed predictions, event boundaries and scores from retained
evidence. The useful answer is about a limited warning tradeoff, not a claim
that a high day-level recall establishes a flood warning system.

[Results](../../reports/results/river-flow/REPORT.md) ·
[Statistical audit](../../reviews/completion/river-flow-results-statistical.md).

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

## 2026-10-30 — Put the missing days beside the score

The new critic reconstructed the forecasts, scores and event ledger. The
calculation was sound, but our main report left important coverage counts behind
a link. About a quarter of scheduled targets cannot be scored, and one equally
weighted gauge has only about one twentieth of its scheduled days observed and
usable. Its apparently perfect three-day recall rests on fourteen high days.

We brought those denominators beside the macro scores. The original panel was
selected using training data and remains unchanged. We can describe performance
on the observed subset; we cannot turn that into continuous warning coverage.

[Dedicated critique](../../reviews/study-critiques-20261030/river-flow.md) ·
[Resolution status](../../reviews/study-critiques-20261030/RESPONSE.md).
