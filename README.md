# Time Series Atlas

**Seven real datasets, eight investigations, and a visible record of the questions,
critiques and corrections behind each answer.** Built as a data-science hiring
portfolio: the methods matter, and so does knowing what their scores mean.

> **The first consequential result changed the plan.**
> Ethan asked for independent critics before implementation. They surfaced
> outcome-derived river attributes, ECG recordings from the same person, and
> interpolation and observing-site changes in the CO₂ record. Those were design
> risks, caught before models ran. Later reviews found actual source discrepancies,
> code defects and misleading summaries. We keep those categories separate.
> **Asking the right question at the right time changed what we built and what
> we could honestly conclude.**

Start with [the project story](STORY.md), [what the initial critique changed](reviews/01-design-review.md),
or the [dataset → question → method guide](docs/METHODS.md).
The [review register](reviews/README.md) and [full evidence matrix](reviews/completion/README.md)
connect the plain-language account to technical checks.

## The investigations

Every row has a frozen design, retained evidence and a chronological story.
Synthetic detection and sampling are two execution units within one investigation.

| Investigation | Question and measured lesson | Results | Process |
| --- | --- | --- | --- |
| Atmospheric CO₂ | Does changing growth improve multiyear forecasts? A trailing-decade model reduced three-year December-target MAE from 6.964 to 1.119 ppm in the revised-data comparison. | [Report](reports/results/co2/REPORT.md) | [Story](studies/co2/STORY.md) |
| Electricity | Who gains from learning across customers? Sharing coefficients worsened forecasts for 21 of 24 selected customers. | [Report](reports/results/electricity/REPORT.md) | [Story](studies/electricity/STORY.md) |
| Intermittent retail sales | What should next week's forecast optimize? Zero won normalized absolute error while missing every recorded sale; TSB won raw-unit MAE. | [Report](reports/results/retail/REPORT.md) | [Story](studies/retail/STORY.md) |
| Oil | Can volatility improve when direction does not? Adaptive variance beat fixed variance on QLIKE; direction lost to prevalence on Brier. The secondary variance loss favored the fixed baseline. | [Report](reports/results/oil/REPORT.md) | [Story](studies/oil/STORY.md) |
| River flow | Does recognizing high water mean warning before a rise? Weather added little at the longer date offset; onset misses and false alerts qualified the high-day recall. | [Report](reports/results/river-flow/REPORT.md) | [Story](studies/river-flow/STORY.md) |
| Air quality | Can peers preserve indications during a station outage? Same-hour network readings beat local persistence, but missing local truth restricted what could be scored. | [Report](reports/results/air-quality/REPORT.md) | [Story](studies/air-quality/STORY.md) |
| ECG | Does annotated-beat recognition transfer to new people? The forest led macro F1 yet missed every F-group beat; overall accuracy hid rare-class failure. | [Report](reports/results/ecg/REPORT.md) | [Story](studies/ecg/STORY.md) |
| Synthetic controls | Can an apparently good detector or spectral peak be trusted? Persistent noise broke false-alert calibration; sampling ambiguity is evaluated separately from frequency recovery. | [Detection](reports/results/synthetic/REPORT.md) · [Sampling](reports/results/spectral/REPORT.md) | [Detection story](studies/synthetic/STORY.md) · [Sampling story](studies/spectral/STORY.md) |

These are bounded comparisons, not universal method rankings. No realized savings,
causal explanation, clinical benefit or operational warning performance is claimed.
The [method guide](docs/METHODS.md) explicitly distinguishes evaluated techniques
from conditional extensions that were not performed.

## What review changed after the plan

- **The source changed the target:** duplicated retail workbook periods required
  a documented cutover; recorded sales could not become unconstrained demand.
- **The clock changed the split:** a later check found that early three-day river
  targets could use calibration outcomes from after their forecast origin. The
  initial review missed this; explicit origin guards were added before the full run.
- **The denominator changed the answer:** air-quality input availability and
  availability of hidden scoring truth were different quantities; ECG person and
  class support mattered more than a high pooled accuracy.
- **The grid could invent certainty:** the spectral design needed every candidate's
  sampling aliases, not merely an alias at the known true frequency.
- **Delivery needed review too:** the lead agent stopped after three studies and
  Ethan challenged the premature completion claim. That failure, the restored
  full scope, and the required final audit remain in the [story](STORY.md).

Separate general, statistical and data/implementation agents review sources,
designs, implementations before full runs, results and publication claims.
Findings and rechecks stay linked in the [review records](reviews/completion/README.md).
Agent agreement is additional scrutiny, not independent human validation or a
guarantee of correctness. [Recurring review protocol](docs/REVIEW_PROTOCOL.md).

## Run and inspect

```bash
uv sync --locked --python 3.12
uv run atlas verify                 # absent fetch-only oil input is disclosed
uv run python scripts/check.py      # bounded offline invariant tests
uv run atlas fetch oil              # explicit free acquisition; pinned history required
uv run atlas all                    # nine execution units, sequential, one CPU thread
uv run python scripts/validate_evidence.py
uv run python scripts/validate_docs.py
```

Individual commands are `atlas co2`, `electricity`, `retail`, `oil`, `river-flow`,
`air-quality`, `ecg`, `synthetic` and `spectral`, each prefixed with `uv run`.
All except oil can run offline from committed snapshots or generated inputs.
Full execution requires committed source/designs, stages outputs and verifies
that source and input bytes stayed fixed. Run records retain source/protocol
commits, seeds, parameters, runtime, memory and output hashes; the full Git history
is required to verify historical source blobs.

**Oil is freely accessible but its inputs are not mirrored:** the EIA tables
identify third-party material. Acquisition must reproduce the pinned historical
snapshot; changed history fails explicitly. A successful current reproduction
does not guarantee future public recovery. See [data credits and transformations](data/README.md)
for all seven sources, licences, exact acquisition commands and this limitation.
No analysis command silently downloads or refreshes data.

A fresh checkout reproduced all 68 result files exactly and passed 41 tests.
The nine sequential run units took about 66 seconds with a process peak of
730 MiB on this machine, excluding installation and acquisition. Runtime varies.
Reproduction, test and publication records are indexed in the
[completion evidence](reviews/completion/README.md). The original three-study
[release record](reviews/first-release/README.md) remains historical evidence,
not proof of completion for the rest of the collection.

## Ownership and AI assistance

Ethan set the direction, requested the critical reviews and made the process and
its corrections central to the portfolio. AI agents researched sources, drafted
contracts, implemented and executed analyses, generated reports and supplied the
recorded critiques. Stories identify substantive decisions and checks without
attributing agent work or unperformed human reviews to Ethan.
