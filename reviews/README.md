# Review findings and evidence status

**Verification is scoped to the work actually performed.** The initial design
review remains preserved. The CO₂, electricity, and synthetic studies now have
source, design, implementation, results, and reproduction evidence. The other
five studies remain planned; their remedies are not implemented or verified.

See the [first-release checkpoint record](first-release/README.md) and its original
review reports. New observed source discrepancies and actual scoring/verification
defects are distinguished from the initial prospective risks.

The [initial review record](01-design-review.md) distinguishes source-confirmed
facts from prospective risks, proposed changes, and evidence still needed.
The [review protocol](../docs/REVIEW_PROTOCOL.md) governs future checkpoints.
The [status history](HISTORY.md) preserves changes instead of overwriting their
chronology. Documentation fixes have a separate [review response](project/2026-10-29-documentation/response.md);
they did not close analytical findings R01–R16. Later first-release implementation
verification is recorded separately below.

| ID | Applies to | Finding | Current status | Verification requirement |
| --- | --- | --- | --- | --- |
| R01 | Project | Methods preceded precise questions and the scope could sprawl | verified for first-release scope; remaining work pending | Independent review of each frozen study contract |
| R02 | CO₂ | Published values include interpolation and mixed provenance | verified for first-release scope; remaining work pending | Actual input/flag audit and sensitivity analysis |
| R03 | Electricity | Some zeros and intervals encode activation/DST conventions | verified for first-release scope; remaining work pending | Unit/time audit, quality masks, cohort construction |
| R04 | River flow | Some attributes are derived from the target | design amended | Feature provenance and leakage rejection checks |
| R05 | River flow | Observed future weather is not forecast-time information | design amended | Input availability table and timestamp trace |
| R06 | Retail | Sales are not unconstrained demand; cancellations and entry matter | design amended | Target/cohort audit and claim review |
| R07 | Retail, forecasting | Some metrics hide sparse-series failure or unhelpful intervals | verified for first-release scope; remaining work pending | Baseline/scoring verification and final comparisons |
| R08 | Air quality | Isolated hidden points do not represent station outages | design amended | Block masks and no-future-input audit |
| R09 | ECG | Record separation is not necessarily person separation | design amended | Subject-to-split manifest and disjointness checks |
| R10 | ECG, synthetic | Recording artifacts complicate physiological spectral claims | design amended | Artifact-aware processing and interpretation review |
| R11 | Oil | Transformations and presumed relationships require testing | design amended | Nonpositive-value audit and frozen evaluation design |
| R12 | All studies | Forecasting, reconstruction, detection, and selection can leak information | verified for first-release scope; remaining work pending | Implemented split/preprocessing/tuning audit |
| R13 | Reproducibility | Hashes identify bytes but cannot recover unavailable snapshots | verified for first-release scope; remaining work pending | Pinned-byte reproduction and redistribution basis |
| R14 | CAMELS acquisition | Versions, official download resolution, and bundle size need explicit handling | design amended | Exact files/version manifest and measured intake |
| R15 | Project | A large framework and expensive methods can obscure the investigation | verified for first-release scope; remaining work pending | Bounded runtime evidence and working offline entry point |
| R16 | Claims and AI | Agent agreement, scenario value, and authored conclusions are not measured proof | verified for first-release publication scope; remaining work pending | Evidence-linked independent interpretation/publication review |

Implementation ownership: the primary implementation agent is responsible for
carrying these remedies into the work; a non-authoring reviewer verifies them.
This is a workflow assignment, not a claim of Ethan's personal verification.

## Checkpoint record

- **2026-10-29, initial project design review:** three separate agents (general,
  statistical, data/implementation). Source-documentation and plan review only.
  See [findings and synthesis](01-design-review.md).
- **Documentation review:** three separate agents inspected the scaffold and
  recommended specific improvements. D01–D08 were independently verified as
  documentation corrections; see the [response and evidence](project/2026-10-29-documentation/response.md).
  This does not close any analytical remedy R01–R16.
- **First-release source intake, contracts, implementation, results:** performed
  and independently reviewed for CO₂, electricity, and the synthetic control.
  Fresh-checkout reproduction matched every result output. Publication verification
  is recorded in the [checkpoint record](first-release/README.md).
- **Remaining studies:** source intake and later gates are not performed; the
  initial documentation review does not replace them.

## Decisions about reviewer recommendations

- **Adopted:** one primary question per study, small comparison sets, compact CO₂
  introduction, recurring reviews, explicit evidence status, retained source bytes,
  and separation of retrospective and online tasks.
- **Not adopted:** demoting CO₂ and ECG solely because they lack a direct commercial
  use case. Ethan clarified that a compelling question natural to the data is
  sufficient. Both remain core studies.
- **Not adopted:** replacing the first release with electricity plus retail.
  Keep the approved concise CO₂/electricity release and move retail next; this
  balances an accessible scientific example with a deeper operational study.
- **Deferred:** neural/pretrained models, Bayesian extensions, and hierarchical
  reconciliation until a core result supplies a question that justifies them.

Preserve future rejected or disputed suggestions with their rationale. Review is
not a requirement to accept every criticism.

## Observed issues found during implementation and publication

These occurred after the prospective design critique. Their records distinguish
source discrepancies, demonstrated code defects, and integration mistakes.

| Observed issue | Response and evidence | Status |
| --- | --- | --- |
| NOAA flags differ from the header; DST treatment is not uniform | Conservative quality/calendar handling, [source records](first-release/README.md#source-intake) | Handling verified; source limitations retained |
| Missing predictions and shape broadcasting could distort scores | Reproduced fixtures, explicit rejection, [statistical implementation review](first-release/implementation/statistical.md) | verified before full runs |
| Execution evidence did not guard against source mutation | Start/end hashes, clean-source guard, staged outputs, [implementation review](first-release/implementation/implementation.md) | verified |
| Missing expected study records could pass validation | Require declared studies/maps/names, [publication review](first-release/results/implementation.md) | verified |
| RI04: early portfolio build pinned links to a commit lacking the new table | Rebuild after the results commit; all pinned paths checked, [resolution](first-release/results/implementation.md) | verified locally; deployment follows |
