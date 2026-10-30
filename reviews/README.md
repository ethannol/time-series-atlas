# Review findings and evidence status

**Review complete does not mean risks resolved.** The initial design review is
recorded. All implementation-dependent remedies remain unverified. No analyses
have run and no empirical findings are claimed.

The [initial review record](01-design-review.md) distinguishes source-confirmed
facts from prospective risks, proposed changes, and evidence still needed.
The [review protocol](../docs/REVIEW_PROTOCOL.md) governs future checkpoints.
The [status history](HISTORY.md) preserves changes instead of overwriting their
chronology. Documentation fixes have a separate [review response](project/2026-10-29-documentation/response.md);
they do not close analytical findings R01–R16.

| ID | Applies to | Finding | Current status | Evidence still needed |
| --- | --- | --- | --- | --- |
| R01 | Project | Methods preceded precise questions and the scope could sprawl | design amended | Independent review of each frozen study contract |
| R02 | CO₂ | Published values include interpolation and mixed provenance | design amended | Actual input/flag audit and sensitivity analysis |
| R03 | Electricity | Some zeros and intervals encode activation/DST conventions | design amended | Unit/time audit, quality masks, cohort construction |
| R04 | River flow | Some attributes are derived from the target | design amended | Feature provenance and leakage rejection checks |
| R05 | River flow | Observed future weather is not forecast-time information | design amended | Input availability table and timestamp trace |
| R06 | Retail | Sales are not unconstrained demand; cancellations and entry matter | design amended | Target/cohort audit and claim review |
| R07 | Retail, forecasting | Some metrics hide sparse-series failure or unhelpful intervals | design amended | Baseline/scoring verification and final comparisons |
| R08 | Air quality | Isolated hidden points do not represent station outages | design amended | Block masks and no-future-input audit |
| R09 | ECG | Record separation is not necessarily person separation | design amended | Subject-to-split manifest and disjointness checks |
| R10 | ECG, synthetic | Recording artifacts complicate physiological spectral claims | design amended | Artifact-aware processing and interpretation review |
| R11 | Oil | Transformations and presumed relationships require testing | design amended | Nonpositive-value audit and frozen evaluation design |
| R12 | All studies | Forecasting, reconstruction, detection, and selection can leak information | design amended | Implemented split/preprocessing/tuning audit |
| R13 | Reproducibility | Hashes identify bytes but cannot recover unavailable snapshots | design amended | Pinned-byte reproduction and redistribution basis |
| R14 | CAMELS acquisition | Versions, official download resolution, and bundle size need explicit handling | design amended | Exact files/version manifest and measured intake |
| R15 | Project | A large framework and expensive methods can obscure the investigation | design amended | Bounded runtime evidence and working offline entry point |
| R16 | Claims and AI | Agent agreement, scenario value, and authored conclusions are not measured proof | design amended | Evidence-linked independent interpretation/publication review |

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
- **Dataset source intake, frozen contracts, implementation, results, publication:**
  not performed. The initial source-documentation review does not replace them.

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
