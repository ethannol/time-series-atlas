# General design review — optional follow-ups

Date: 2026-11-10. Role: non-authoring automated general critic.
Checkpoint: question/design. No source or contract edits, fits, simulations,
tests, browser checks, or delegation were performed in this review.

## Scope and evidence

Reviewed `AGENTS.md`, `docs/REVIEW_PROTOCOL.md`, the follow-up contract, the
previous author response, and the relevant optional/accepted-limit sections
of all eight dedicated investigation critiques. Read the standing execution
and repository-freshness guidance. Local HEAD and origin/main both resolve to
`1a0ec0180b857f7d98b092a8104a575657d53445`; the parent supplied the fresh-base
provenance. I did not independently fetch or validate future execution provenance.

Reviewed file SHA-256 identities:

- `studies/followups/DESIGN.md`:
  `9e1a93c1f7dd976bfda67a45a14b7b3f67409e626d1de3f875e9456e59b05951`
- `reviews/study-critiques-20261030/RESPONSE.md`:
  `7029d98a36b5f3a3c89a744bb49db0dd57abe4766e0ad91ff6839a11d403a8af`
- `docs/REVIEW_PROTOCOL.md`:
  `675275bf09409edec4459817e0652743b0e2b745d9723c74585062d246253f1f`

## Verdict and blockers

**General design accepted; no material blocker identified.** These questions
are useful, answerable with the declared evidence, and finite. Acceptance is
of the proposed scope and claim boundaries, not implementation correctness or
scientific validation. The independent technical gates remain prerequisites
to full new runs. Publication and resolution verification remain pending.

The opening explicitly acknowledges prior-result knowledge and calls this a
post-publication exploratory extension. Retaining original artifacts, running
all declared comparisons, and freezing the added contract are appropriate.
Freezing now constrains additional discretion; it does not make reused test
people, years, codes, origins, or sampling realizations newly held out.

## Question value and optional recommendation coverage

| Investigation | Assessment and disposition |
| --- | --- |
| CO₂ | Anchoring asks a concrete question prompted by the known starting-level diagnostic. Two fixed alternatives and the origin-gap figure adopt both relevant outstanding suggestions. Calibration stays separate from test scoring. The earlier color correction is already completed, not a new follow-up accomplishment. |
| Electricity | Relative magnitude, individual deltas, load shares, and the linked peak table adopt O1–O3. They make the existing result more useful without implying a different model or removing difficult customers. Signed net concentration and load concentration must remain different quantities. |
| Retail | The 52-week median is one reasonable, bounded absolute-error-oriented comparator. Concentration, quarter summaries, all 24 exclusions, bias telescoping, and a hand-calculated recurrence fixture cover the earlier suggestions. All-exclusion reporting avoids turning sensitivity analysis into cohort selection. |
| Oil | Plain-language loss explanations and complete annual tables adopt OIL-02/OIL-03. Weighted annual contributions answer why the pooled comparison can differ from a typical year. Retaining negative contributions is necessary and declared. |
| River | Portable caption context adopts the outstanding presentation suggestion. No new model is needed to explain the reporting assumption, false/missed alerts, or unscored support. |
| Air quality | Explicit macro-MAE labeling, censoring counts, and the calendar baseline explanation adopt all three optional presentation suggestions. Overlapping boundary counts are correctly distinguished from distinct missed events. |
| ECG | Precision/support tables, patient-composition resampling, and three fixed additional assignments adopt the proposed presentation and stability extensions. The two stability questions are distinct and worthwhile; neither requires tuning the cap or hunting for a favorable split. |
| Synthetic detection | A fixed dependence/shift grid and Monte Carlo intervals adopt the suggested condition/interval extensions. Overall detection beside conditional delay addresses the standalone interpretation concern. Fixed calibration keeps this a stress test of that threshold. |
| Synthetic sampling | Common-band selection on original realizations plus the declared frequency/noise grid adopt the suggested sensitivity extensions. Unchanged LS bins and off-grid truths make this more informative while preserving a finite budget. |

The oil critic also conditionally suggested reconsidering release of invertible
adaptive forecasts if the intended restriction covered recoverable magnitudes.
The follow-up explicitly retains those artifacts and the reconstruction
disclosure. I acknowledge that as **not adopted**: this scope makes no new
restriction covering magnitudes, licence finding, or removal decision. The
prior critic explicitly allowed disclosure without removal. This is not a
verified legal clearance or a correction of reconstructability.

Broader electricity model families, new covariates, operational availability
validation, and other listed untested scopes were accepted boundaries, not an
instruction to implement every imaginable extension. Leaving them outside
this finite round is appropriate. No outstanding optional recommendation in
the reviewed response lacks a reasonable adoption or exclusion here.

## Accepted limitations

- The new retail comparator is a historical median, not a demonstrated optimal
  conditional median. The design already makes this distinction.
- CO₂ anchoring changes an algorithmic level term. It cannot assign atmospheric
  causes or turn overlapping historical intervals into operational coverage.
- ECG bootstrap percentiles describe these saved predictions under sampled
  patient composition. Repeated folds reuse the same people and offer limited
  descriptive stability evidence, not independent replications or clinical proof.
- Synthetic intervals are conditional, pointwise Monte Carlo summaries. More
  simulated cells do not establish robustness to every process or calibration.
- Matched frequency bands still leave different bins and procedures. Aliased
  three-second sampling remains physically ambiguous even with a unique numeric
  maximum. The proposed reporting correctly preserves that limitation.
- Existing source, availability, cohort and outcome limitations remain. None of
  these presentation or exploratory additions establishes deployment readiness.

## Recommendations for execution and publication

1. Preserve the exploratory label in each added report section and any portfolio
   headline that draws on it. A standalone reader should not need this contract
   to discover prior-result reuse. This is a publication check, not a new design
   defect; the contract already requires clearly labeled additions.
2. Keep complete diagnostic tables linked, but lead the portfolio with the small
   number of consequences the results actually support. Signed contribution
   percentages can exceed 100% through cancellation; avoid calling them shares
   of total absolute error or implying they must sum as nonnegative slices.
3. Record the earlier optional deferrals as historical decisions and append this
   adoption history. Do not relabel optional additions as repairs to demonstrated
   defects. Resolve this review against the exact final design before execution;
   assess generated evidence and claims again at publication.

Status: design accepted with explicit limits; execution and publication pending.
