# Implementation plan

Post-publication follow-up (2026-10-30): Ethan requested fresh dedicated critics
for every investigation's implementation, findings and presentation. That review
round and its corrections are tracked [separately](reviews/study-critiques-20261030/README.md)
from the historical first-completion checklist below. A fresh review is additional
scrutiny, not a promise that earlier approvals found every limitation.

Status (2026-10-30): all eight investigations executed, reviewed, reproduced and
published. All 68 outputs matched in a fresh checkout; 41 tests passed. Atlas
PR2 and profile PR3 merged, main CI passed, and the live portfolio deployment
was verified. The independent general critic audited every checklist item and
found no remaining study or publication-content omission. Its
[closure audit](reviews/completion/completion-audit-general.md) records that exact
checkpoint; the documentation follow-up is subject to the same CI/deploy rule.

## Overall completion checklist

Every study must meet the definition of done below: independently reviewed
design and implementation, executed and reproducible results, evidence and
figures, reviewed interpretation, a plain-language story, and publication.

- [x] CO₂ — initial release; retain and verify its evidence during final audit.
- [x] Electricity — initial release; retain and verify its evidence during final audit.
- [x] Synthetic change detection — initial release; retain and verify its evidence during final audit.
- [x] Promised synthetic irregular-sampling frequency-recovery control (R10).
- [x] Intermittent retail sales.
- [x] Oil prices and volatility.
- [x] River-flow warnings.
- [x] Air-quality warnings during sensor outages.
- [x] ECG recognition across people.
- [x] Final collection documentation, dataset credits, and method-coverage status.
- [x] Reproduction and CI checks for the final revision.
- [x] Portfolio and GitHub profile updated for all completed studies; deployment verified.
- [x] Independent general-critic audit of this entire checklist with linked evidence.
- [x] Reconcile R01–R16 and later findings against a per-study gate/evidence matrix.

Continue until this agreed scope is complete, unless Ethan stops or changes it,
or a concrete blocker prevents further progress. Completed milestones belong in
progress reports. They are not permission to end the overall task early.

Resumption baseline: fetched `origin/main` at 2026-10-30T21:17:43Z,
`bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`; new work uses branch
`feat/complete-atlas`. No analysis instrumentation changes at this checkpoint.

## Purpose and audience

Build a data-science hiring portfolio that demonstrates useful questions,
careful handling of measurements, fair evaluation, response to criticism, and
clear communication. Broad method coverage serves these goals; it is not a
completion criterion by itself.

The story of the critique is a main deliverable, alongside the eventual results.
Keep the [initial findings](reviews/01-design-review.md) visible and maintain the
[project story](STORY.md) and every study story throughout implementation.

## Delivery sequence

1. **Source intake and design.** Resolve official files, inspect representative
   records and provider notes, preserve provenance and flags, check redistribution
   terms, estimate resource needs, and specify the primary question. Complete
   source and design reviews before committing to a full experiment.
2. **First completed studies.** A concise CO₂ investigation and a deeper electricity
   study. Add one focused synthetic change-detection control so the initial
   release demonstrates more than forecasting. Build only the shared utilities
   these studies need.
3. **Extend one complete study at a time.** Retail, oil, river flow, air quality,
   and ECG all received the same review and story workflow.
4. **Question-driven extensions.** Bayesian, neural/pretrained, reconciliation,
   or other advanced methods only when a specific unresolved question justifies
   their dependencies and compute. Keep planned versus evaluated coverage visible.
5. **Publication and integration.** Publish reviewed work to GitHub and integrate
   completed-study evidence into Ethan's portfolio and profile. Keep unevaluated conditional
   extensions visibly separate. Follow any PR checks through the final revision.

## Study contract, frozen before fitting

Create `studies/<slug>/DESIGN.md` after source intake. It must state:

- Primary question, purpose, and what evidence could contradict the expectation.
- Data version, target definition, units, time semantics, and population/cohort.
- Forecast issue time and horizon, or the precise reconstruction/detection task.
- Allowed inputs and their availability; known gaps, flags, and exclusions.
- Baselines, two or three substantive comparisons, and a bounded tuning budget.
- Training/validation/final evaluation splits; preprocessing and calibration rules.
- Primary metrics, uncertainty summaries, and relevant subgroup/regime checks.
- Claims the data cannot support and how synthetic controls relate to the study.

Record the protocol commit before full model runs. Log changes with their reason
and whether results had already been inspected. Do not silently reuse a final
evaluation period for model selection.

## Reviews are required milestones

Use the [review protocol](docs/REVIEW_PROTOCOL.md) for source intake, study design,
implementation before full runs, first results before conclusions, and publication.
Each checkpoint produces an independent review, an author response, and evidence
for resolution. Keep disagreement and limitations visible. No new user approval
is needed to perform routine reviews or repairs within the approved scope.

## Technical shape

- Python analysis scripts as the authoritative implementation; generate notebooks
  if useful rather than maintaining two versions of the analysis.
- Share acquisition/provenance, split records, result records, plotting, and report
  generation. Keep dataset semantics in explicit adapters.
- Save prediction/detection-level evidence, metrics, warnings, source commit and
  patch hash, locked dependencies, seeds, inputs, split membership, runtime, and
  resource use. Reports cite these artifacts.
- Separate `reproduce` with pinned source bytes from an explicit data refresh.
  Preserve permitted immutable snapshots; document any public reproduction limit
  where source bytes cannot be redistributed.
- Offer an offline small example and full-study commands. The locked package installs the bounded specialized
  dependencies together; optional groups were considered but not implemented.
- Use offline CI fixtures for meaningful data/split/scoring invariants. Full model
  runs are explicit release checks; live provider access is not a unit test.
- Execute locally with bounded concurrency. Measure a representative run before
  increasing scale; do not detach jobs.

## Definition of done

A completed study has an independently reviewed design and implementation,
recorded execution, figures, a clear answer supported by evidence, explicit
limitations, a reproducible command, a results ledger, and an updated short story.
Findings are verified or explicitly accepted as bounded limitations. An author's
response alone does not close a finding.

## Repository baseline

Initialized locally on 2026-10-29 at 23:48:38 UTC on branch `main`. No local
`time-series-atlas` directory or resolvable `ethannol/time-series-atlas` GitHub
repository existed at the preflight check. There was no remote/main to fetch for
this initial documentation. Once a remote exists, fetch and verify fresh
`origin/main` before new implementation work, following Ethan's standing rules.
Existing sibling repositories have not been modified for this scaffold.
