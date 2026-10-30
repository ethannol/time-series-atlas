# Time Series Atlas

**A portfolio of time series investigations—and the questions, critiques, and
revisions that make their conclusions worth trusting.**

Each study starts with a question that matters for its data. Business questions
belong where they fit; scientific and engineering questions belong here too.
Methods serve the question. A more complicated model does not have to win.

> **The first consequential result was a change to the plan.**
> Ethan requested independent critical agents before implementation. Their review
> exposed source details and evaluation risks the initial proposal had not
> addressed: river-flow predictors derived from the outcome, ECG records from the
> same person, and CO₂ values that already include interpolation and a temporary
> observing-site substitution. These findings changed the planned analyses.
> **At that checkpoint no models had run: those were risks caught in design.
> Later source discrepancies, actual code defects, and measured results are
> recorded separately in the process stories.**

**Start here:** [How the project changed](STORY.md) ·
[What review caught and why it matters](reviews/01-design-review.md) ·
[Open findings and evidence status](reviews/README.md)

## What this portfolio demonstrates

The aim is to make analytical judgment visible: framing a useful question,
examining how measurements were produced, choosing an honest evaluation,
responding to criticism, and explaining what the evidence supports. Model
performance will be shown alongside the decisions that make it interpretable.

For a quick read, follow the project story and the individual study stories.
For technical scrutiny, follow their finding IDs into the review records and,
once implemented, the analysis designs and reproducible results.

## The investigations

| Study | Primary question | Plain-language process story | Status |
| --- | --- | --- | --- |
| Atmospheric CO₂ | Does a changing growth rate improve multiyear forecasts over a fixed trend and annual cycle? | [CO₂ story](studies/co2/STORY.md) | [Executed report](reports/results/co2/REPORT.md) |
| Electricity demand | When does learning across customers improve tomorrow's load forecast, and who benefits or suffers? | [Electricity story](studies/electricity/STORY.md) | [Executed report](reports/results/electricity/REPORT.md) |
| River flow | How much warning of high flow can recent rainfall and flow provide across different catchment types? | [River-flow story](studies/river-flow/STORY.md) | Planned |
| Oil prices | Can volatility forecasts improve on simple baselines even when price-direction forecasts cannot? | [Oil story](studies/oil/STORY.md) | Planned |
| Intermittent retail sales | How should we forecast next week's sales for products that sell only occasionally? | [Retail story](studies/retail/STORY.md) | Planned |
| Air quality | Can nearby stations preserve useful high-pollution warnings when a local sensor goes offline? | [Air-quality story](studies/air-quality/STORY.md) | Planned |
| ECG waveforms | Does a model that recognizes abnormal heartbeat shapes work on people it has never seen? | [ECG story](studies/ecg/STORY.md) | Planned |
| Synthetic controls | When the truth is known, how quickly can a sustained change be distinguished from ordinary variation? | [Synthetic-lab story](studies/synthetic/STORY.md) | [Executed report](reports/results/synthetic/REPORT.md) |

The seven real-data collections are free to access. The first-release snapshot attribution and redistribution basis are documented
in [data credits](data/README.md); the remaining datasets will be checked before
their snapshots are published. The first CO₂, electricity, and synthetic studies have executed under frozen
designs. The other five real-data studies remain planned. No financial or clinical
benefit is claimed.

## Review is part of the analysis

Separate agents review source intake, the analysis design, the implementation,
results, and publication claims. A general critic participates alongside
statistical and data/implementation critics. Findings remain visible until
evidence supports closure; changing the prose is not proof that a fix works.

See the [recurring review protocol](docs/REVIEW_PROTOCOL.md) and
[implementation plan](PLAN.md). These are required checkpoints, not optional
cleanup at the end. Automated reviews can share blind spots: they are additional
scrutiny, not independent human validation or a guarantee of correctness.

## Ownership and AI assistance

Ethan set the project direction, requested the initial independent critique, and
made the process and its corrections central to the portfolio. AI agents drafted
the plan, researched sources, implemented and executed the analyses, generated
reports, and supplied the critiques recorded here. Future
stories will identify who made each substantive decision and what was checked;
they will not attribute agent work or unperformed reviews to Ethan.

## What the first runs found

- **CO₂:** the recent-growth model reduced three-year December-target MAE from
  6.964 ppm for the expanding fixed-growth model to 1.119 ppm. This is a bounded
  revised-data comparison, not a claim about every forecast date or future climate.
- **Electricity:** the shared model was worse for 21 of 24 selected customers.
  More shared data did not automatically improve this forecasting comparison.
- **Change detection:** CUSUM's false-alert frequency rose from 5% on independent
  noise to 73% on persistent noise under the same frozen threshold. Assumptions
  mattered more than the attractive detection-delay number.

These statements refer to the linked reports and their saved predictions. Read
[the first-release review record](reviews/first-release/README.md) for checkpoints,
known limitations, and publication status. Planned capabilities remain distinct.

## Run and inspect

```bash
uv sync --locked --python 3.12
uv run atlas verify                 # checks pinned analysis snapshot hashes
uv run python scripts/check.py      # offline, bounded tests with evidence
uv run atlas all                    # three reviewed studies; one CPU thread
uv run python scripts/validate_evidence.py
```

Run from a clean, committed source checkout: full execution refuses uncommitted
source/design changes and stages output until source stability is checked.
Analysis uses the committed snapshots and does not download data. The first
recorded local full run took about eleven seconds; runtime varies by machine.
For the original archives, `uv run atlas fetch` verifies pinned hashes and
`uv run atlas intake` rebuilds the panel. Upstream revisions fail explicitly;
there is no silent refresh. See [data credits and transformations](data/README.md).

[CO₂ result and evidence](reports/results/co2/REPORT.md) ·
[Electricity result and evidence](reports/results/electricity/REPORT.md) ·
[Synthetic result and evidence](reports/results/synthetic/REPORT.md)

