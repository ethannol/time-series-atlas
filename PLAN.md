# Implementation plan

Status (2026-10-30): sources acquired, first three designs frozen, implementation
reviewed, and first full runs executed and reproduced. Local results/publication
reviews passed; GitHub CI and deployment are tracked during rollout.
The remaining five real-data studies are planned.

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
   and ECG remain in scope. Each receives the same review and story workflow.
4. **Question-driven extensions.** Bayesian, neural/pretrained, reconciliation,
   or other advanced methods only when a specific unresolved question justifies
   their dependencies and compute. Keep planned versus evaluated coverage visible.
5. **Publication and integration.** Publish reviewed work to GitHub and integrate
   completed-study evidence into Ethan's portfolio and profile. Keep planned
   studies visibly separate. Follow any PR checks through the final revision.

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
- Offer an offline small example and full-study commands. Use optional dependency
  groups for specialized methods.
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
