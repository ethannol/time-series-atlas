# Full-collection evidence and review matrix

The agreed scope is eight investigations: seven real datasets and synthetic
controls. Detection and frequency recovery are separate synthetic run units.
This index preserves the difference between a reviewed analysis and a verified
publication. The original [three-study release](../first-release/README.md)
remains scoped historical evidence.

**Current checkpoint:** all nine run units executed; independent numerical and
results reviews passed with presentation amendments. Final presentation recheck,
fresh-checkout reproduction, CI and live publication are still pending.

## Per-study gates

Every report links its figures, numerical artifacts and run record. Run records
pin full source/protocol revisions, input hashes, output hashes, seeds, runtime
and process-lifetime peak memory. Source reviews cover redistribution and
transformation; the [data credits](../../data/README.md) explain the oil exception.

| Study/run unit | Source and design review | Frozen protocol | Pre-run implementation | Executed evidence/source | Independent results reviews | Plain-language story |
| --- | --- | --- | --- | --- | --- | --- |
| CO₂ | [First-release gates](../first-release/README.md) | [Design](../../studies/co2/DESIGN.md), `b374e9b` | [First-release gates](../first-release/README.md) | [Report](../../reports/results/co2/REPORT.md), [run](../../reports/results/co2/run.json), `b607f9f` | [First-release gates](../first-release/README.md) | [Story](../../studies/co2/STORY.md) |
| Electricity | [First-release gates](../first-release/README.md) | [Design](../../studies/electricity/DESIGN.md), `b374e9b` | [First-release gates](../first-release/README.md) | [Report](../../reports/results/electricity/REPORT.md), [run](../../reports/results/electricity/run.json), `b607f9f` | [First-release gates](../first-release/README.md) | [Story](../../studies/electricity/STORY.md) |
| Synthetic detection | [First-release gates](../first-release/README.md) | [Design](../../studies/synthetic/DESIGN.md), `b374e9b` | [First-release gates](../first-release/README.md) | [Report](../../reports/results/synthetic/REPORT.md), [run](../../reports/results/synthetic/run.json), `b607f9f` | [First-release gates](../first-release/README.md) | [Story](../../studies/synthetic/STORY.md) |
| Retail | [Source/design](design-implementation.md) | [Design](../../studies/retail/DESIGN.md), `b369cc8` | [Statistical](retail-implementation-statistical.md) / [data](retail-implementation-data.md) | [Report](../../reports/results/retail/REPORT.md), [run](../../reports/results/retail/run.json), `2c0af60` | [General](retail-results-general.md) / [statistical](retail-results-statistical.md) / [data](retail-results-data.md) | [Story](../../studies/retail/STORY.md) |
| Oil | [Source/design](design-implementation.md) | [Design](../../studies/oil/DESIGN.md), `715ac6c` | [Statistical](oil-implementation-statistical.md) / [data](oil-implementation-data.md) | [Report](../../reports/results/oil/REPORT.md), [run](../../reports/results/oil/run.json), `2c0af60` | [General](oil-results-general.md) / [statistical](oil-results-statistical.md) / [data](oil-results-data.md) | [Story](../../studies/oil/STORY.md) |
| River flow | [Source/design](design2-implementation.md) | [Design](../../studies/river-flow/DESIGN.md), `7e6c91d` | [Statistical](river-flow-implementation-statistical.md) / [data](river-flow-implementation-data.md) | [Report](../../reports/results/river-flow/REPORT.md), [run](../../reports/results/river-flow/run.json), `f14924e` | [General](river-flow-results-general.md) / [statistical](river-flow-results-statistical.md) / [data](river-flow-results-data.md) | [Story](../../studies/river-flow/STORY.md) |
| Air quality | [Source/design](design-implementation.md) | [Design](../../studies/air-quality/DESIGN.md), `715ac6c` | [Statistical](air-quality-implementation-statistical.md) / [data](air-quality-implementation-data.md) | [Report](../../reports/results/air-quality/REPORT.md), [run](../../reports/results/air-quality/run.json), `2c0af60` | [General](air-quality-results-general.md) / [statistical](air-quality-results-statistical.md) / [data](air-quality-results-data.md) | [Story](../../studies/air-quality/STORY.md) |
| ECG | [Source/design](design2-implementation.md) | [Design](../../studies/ecg/DESIGN.md), `fbd9a70` | [Statistical](ecg-implementation-statistical.md) / [data](ecg-implementation-data.md) | [Report](../../reports/results/ecg/REPORT.md), [run](../../reports/results/ecg/run.json), `2c0af60` | [General](ecg-results-general.md) / [statistical](ecg-results-statistical.md) / [data](ecg-results-data.md) | [Story](../../studies/ecg/STORY.md) |
| Synthetic sampling | [Alias amendment](design-amendment-statistical.md) | [Design](../../studies/spectral/DESIGN.md), `2c0af60` | [Statistical](spectral-implementation-statistical.md) / [data](spectral-implementation-data.md) | [Report](../../reports/results/spectral/REPORT.md), [run](../../reports/results/spectral/run.json), `f14924e` | [General](spectral-results-general.md) / [statistical](spectral-results-statistical.md) / [data](spectral-results-data.md) | [Story](../../studies/spectral/STORY.md) |

The [author response](RESPONSE.md) synthesizes changes and accepted limitations.
Original reviewer findings and their appended independent rechecks remain intact;
an author response or a checked box alone is not verification. Separate agents
reviewed source/design, implementation before full runs, and results. They are
AI reviewers, not independent human scientific validation.

## Collection checks and publication

- [Presentation refresh](../../reports/verification/completion-presentation-refresh.json):
  all 34 numerical artifacts for retail, oil, air, river and ECG unchanged while
  report/figure clarity changed.
- [Final spectral/river presentation comparison](../../reports/verification/completion-presentation-final.json):
  all 13 numerical artifacts unchanged. No outcome-driven model tuning.
- [Recorded offline tests](../../reports/verification/checks.json): the record
  states its exact source revision; final-suite refresh is still pending here.
- Final clean-checkout reproduction, strict portfolio build, profile review,
  GitHub checks and deployment: pending. These gates will be linked here when
  they have actually run. The general critic must audit every item before an
  overall completion claim.

The [publication preflight](publication-preflight-general.md) identified the
full-scope obligations. [Copy review](publication-copy-general.md) caught actual
method/attribution errors before publication. Source freshness began at fetched
`bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`, recorded in the
[baseline refresh](../../reports/verification/completion-baseline-refresh.json).
Each run then froze its committed source; no revision changed mid-run.

## Accepted boundaries

Oil input history is fetch-only; local reproduction does not guarantee future
public access to identical history. CAMELS acquisition verifies selected members,
not the full archive. River and air reporting latency is assumed rather than
measured. ECG classification is given expert beat centers; rare-class/person
support limits interpretation. Synthetic recovery is tied to the declared
sampling/noise process. Original CO₂ revision/provenance and electricity clock
limitations remain. No universal winner, causal benefit or human validation is
implied. Conditional advanced-method extensions remain unevaluated.
