# Author response and resolution trail

Date: 2026-10-30. Author: lead implementation agent. Independent verdicts live
in the linked reviewer records; this response alone does not establish closure.
The full scope is eight investigations, with two synthetic execution units.

## Source and design changes before full runs

- **Retail:** independent row-multiset comparison confirmed 22,523 overlapping
  transactions across annual sheets. A date cutover removes the cross-sheet
  duplication; unknown within-sheet repeats remain. The target is gross recorded
  sales, with a training-only cohort and multiple score/volume views.
  [Source/design verification](design-implementation.md).
- **Oil:** the observed negative WTI level rules out an unqualified log transform.
  Refinitiv attribution prevents treating the input as unrestricted government
  data. Inputs/outcomes remain private fetch-only files; growing source workbooks
  are accepted only when the pinned historical normalized bytes match. This is
  an accepted public archival limitation, not a claim of open redistribution.
  Initialization, physical variance floor and recursion boundaries were frozen.
  [Design amendments and verification](design-statistical.md).
- **Air quality:** specified separate single-station outages, exact half-open
  endpoints, threshold ties, class-absent metrics and event censoring. Input peer
  coverage is distinct from available hidden local truth.
  [Contract review](design-statistical.md).
- **River:** verified flags, units, named weather columns, range-member integrity
  and training-only cohort. The author found positional weather-column and
  missing-QC audit defects during intake; independent reviewers reconstructed the
  corrected snapshot. Later, the author caught an origin-boundary leakage risk
  that the first design review had missed. Explicit origin guards exclude the
  first two three-day targets at calibration/test boundaries.
  [Source/design recheck](design2-implementation.md).
- **ECG:** provider checksums, MLII channel identity, shared person 201/202 and
  every retained waveform were checked. Missing previous RR is now counted
  separately from waveform boundaries. Frozen person folds, label-independent
  caps and class-absent scoring conventions precede model execution.
  [Design recheck](design2-statistical.md).
- **Spectral:** the general critic recovered the omitted promised control. The
  author then noticed that including only the truth's alias could make another
  noisy peak look unique. Every candidate's alias family is now included.
  [Amendment](design-amendment-statistical.md) and
  [pre-run verification](spectral-implementation-data.md) preserve this chronology.

## Actual implementation defects and safeguards

| Finding | Author response | Independent verification |
| --- | --- | --- |
| Historical evidence compared old runs to today's source | Verify each recorded source file against its historical Git blob; preserve original runs | [Retail/evidence review](retail-implementation-data.md) |
| CLI did not expose the whole collection and could overstate private-input verification | Add every execution unit; explicitly disclose absent fetch-only inputs | [Command/input checks](retail-implementation-data.md) |
| Oil GARCH floor was applied in standardized rather than physical units | Transform the floor into optimizer units, restore dollar-squared output floor | [C-I06](oil-implementation-data.md) |
| A failed later oil run could overwrite earlier private outcomes | Immutable content-addressed private outcome files | [C-I07](oil-implementation-data.md) |
| Air peer coverage was initially limited to scoreable blocks | Retain peer availability across every scheduled hour, separately from local truth eligibility | [Coverage recheck](air-quality-implementation-data.md) |
| River event ledger lacked issue origins and mishandled unknown-boundary alert segments | Explicit origin/target dates, censored high runs, unresolved alert segments, matched cohorts and contributor counts | [Event recheck](river-flow-implementation-data.md) |
| Later river pandas warning cleanup might change alert semantics | Replace fill-and-cast with explicit equality; verify every restored calendar Boolean and final numerical files | [Equivalence check](river-flow-results-data.md) |

No scoring fix was selected to improve final performance. Required split/scoring
repairs preceded the affected full run. Subsequent numerical audits recomputed
scores from retained predictions and, where possible, reconstructed predictions
from saved parameters without refitting. Forest hard labels were independently
rescored; exact tree recreation belongs to the fresh-checkout reproduction.

## Results and presentation responses

The first reports sometimes described an evaluation without plainly answering
its question. General reviewers required measured answers, tradeoffs and current
stories. We added retail's mean/median and weighting distinction; oil's loss
ranking reversal and small GARCH/EWMA difference; air's separate coverage
quantities and conditional event interpretation; river's onset misses and false
alerts; ECG's rare-class failures and training support; and spectral ambiguity.

Plots now expose small retail differences, separate overlapping air curves,
name the spectral ambiguity method, and use readable river labels. Source-generated
reports retain their evidence links. [Presentation refresh verification](../../reports/verification/completion-presentation-refresh.json)
compares numerical artifacts against the prior committed results; later refreshes
are recorded separately. Re-rendering is not a new model-selection opportunity.

Publication review caught two actual copy errors in the new method/source guide:
electricity was incorrectly described as having prediction intervals, and one
creator, Song Chen, was split into two authors. Both were corrected and
independently rechecked in [the copy review](publication-copy-general.md).
The same review replaced an unsupported claim about the relative difficulty of
continued flow with the directly observed contrast between high-day and onset
recall. Those populations and weightings differ.

## Accepted boundaries and deferred work

The data do not establish operational reporting latency, population-level clinical
performance, causal effects, latent retail demand, realized economic value or
universal model rankings. Oil's public source may revise history. CAMELS verification
covers acquired members, not the entire archive. The synthetic examples have
known but narrow generating assumptions. Final publication and reproduction are
separate gates in the [evidence matrix](README.md).

Bayesian/neural methods, reconciliation, ungauged transfer, oil cointegration and
end-to-end ECG detection were conditional extensions and were not performed.
Specialized small Python dependencies were installed together in the locked
package for one reproducible entry point; optional groups were not implemented.
Bounded execution and measured resource evidence replace the original optional-
dependency suggestion. No Mac mini is required or used.
