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
> **No models have run yet: these are risks caught in design, not demonstrated
> implementation failures or empirical findings.**

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
| Atmospheric CO₂ | Does a changing growth rate improve multiyear forecasts over a fixed trend and annual cycle? | [CO₂ story](studies/co2/STORY.md) | Design; not implemented |
| Electricity demand | When does learning across customers improve tomorrow's load forecast, and who benefits or suffers? | [Electricity story](studies/electricity/STORY.md) | Design; not implemented |
| River flow | How much warning of high flow can recent rainfall and flow provide across different catchment types? | [River-flow story](studies/river-flow/STORY.md) | Design; not implemented |
| Oil prices | Can volatility forecasts improve on simple baselines even when price-direction forecasts cannot? | [Oil story](studies/oil/STORY.md) | Design; not implemented |
| Intermittent retail sales | How should we forecast next week's sales for products that sell only occasionally? | [Retail story](studies/retail/STORY.md) | Design; not implemented |
| Air quality | Can nearby stations preserve useful high-pollution warnings when a local sensor goes offline? | [Air-quality story](studies/air-quality/STORY.md) | Design; not implemented |
| ECG waveforms | Does a model that recognizes abnormal heartbeat shapes work on people it has never seen? | [ECG story](studies/ecg/STORY.md) | Design; not implemented |
| Synthetic controls | When the truth is known, how quickly can a sustained change be distinguished from ordinary variation? | [Synthetic-lab story](studies/synthetic/STORY.md) | Design; not implemented |

The seven real-data collections are free to access. Redistribution conditions
will be checked separately before publishing source snapshots. No observed model
scores, conclusions, or claims of financial or clinical benefit exist yet.

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
the plan, researched sources, and supplied the critiques recorded here. Future
stories will identify who made each substantive decision and what was checked;
they will not attribute agent work or unperformed reviews to Ethan.

Implementation, measured results, and reproducible analysis commands will be
added as each study is completed. Planned capabilities are not presented as
finished work.
