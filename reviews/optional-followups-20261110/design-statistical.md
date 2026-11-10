# Optional follow-ups: statistical design review

- Reviewer: non-authoring automated statistical critic; 2026-11-10.
- Baseline: `1a0ec0180b857f7d98b092a8104a575657d53445` (`HEAD` and `origin/main`).
- Branch: `feat/optional-study-followups-20261110`.
- Fetch evidence: `baseline.json`, verified at `2026-11-10T18:57:41.447815+00:00`;
  instrumentation patch: null. Reviewed tracked helpers were unchanged.
- Proposed contract SHA-256:
  `9e1a93c1f7dd976bfda67a45a14b7b3f67409e626d1de3f875e9456e59b05951`.
- Scope: `studies/followups/DESIGN.md`, original affected contracts and helpers,
  `AGENTS.md`, `docs/REVIEW_PROTOCOL.md`, and bounded existing-artifact inspection.

## Verdict

The finite exploratory design is statistically defensible. No concrete leakage,
invalid split, or scoring defect was identified that requires abandoning a
comparison or adding more methods. Resolve the bounded clarifications below in
the frozen contract and reports. This is design acceptance, **not authorization
to skip the separate pre-run implementation review**, and not scientific validation.
No fits, simulations, study commands, test suites, or subagents were run here.

## Required clarifications

1. **ECG repeated-fold estimand — interpretation, not a leakage finding.**
   `ecg.fold_indices` seeds its cap sampler with `SEED + fold` and consumes that
   stream while traversing the fold's training people. A new assignment changes
   both fold numbers and which people precede a person in that traversal; even
   with identical seed constants, capped training beats can change. Forest
   randomness is also fold-indexed. State that the repeats assess the complete
   fixed fitting procedure under new assignments, including assignment-induced
   training subsampling/randomness. Do not attribute their variation solely to
   the identity of held-out people. Keep the proposed unchanged helper behavior;
   a new fixed-per-person cap design is unnecessary scope expansion.

2. **Oil contribution denominator — freeze the aggregation level.**
   Existing `variance_summary` groups by market and model. Specify that yearly
   contributions remain **within each market**:
   `C_y = (n_y / sum(n_y)) * (QLIKE_EWMA,y - QLIKE_fixed,y)`.
   The signed share is `C_y / sum(C_y)`, undefined if that denominator is zero.
   Retain negative contributions and values above 100%; they are signed shares
   of a net difference, not fractions of all positive loss. Do not silently pool
   WTI and Brent or average yearly means with equal weights. This is a contract
   clarification for derived evidence, not a request for additional fitting.

3. **CO₂ inherited sensitivity — make its continuation explicit.**
   Preserve the original target-site exclusion sensitivity for both anchored
   alternatives as well as the primary common-target scores. Exclusion must
   remove affected targets only, without recalibrating intervals or removing
   training observations. Origin anchoring can itself use a substituted-site
   observation (December 2022); target exclusion does not remove that influence.
   This keeps the new comparison's scope aligned with the original contract.

## Accepted limits and bounded scope

- **CO₂:** The December reconstruction is algebraically valid for the existing
  linear trend plus fixed month indicators: p12 and p36 share the December
  seasonal term. Adding the origin residual to every horizon leaves slope and
  month contrasts fixed. Separate calibration residuals for each anchored model
  and horizon are necessary and already declared. January remains secondary;
  multiyear errors overlap, calibration is small, and no IID superiority test or
  causal decomposition of MAE is justified. Keep paired original/anchored rows.
- **Retail:** A median of 52 complete Monday–Sunday totals is a meaningful
  absolute-error-oriented baseline. It estimates a trailing empirical median,
  not the conditional median of a stationary demand process or an optimal order
  quantity. The 364-day window must end before issuance and include every day;
  no compressed-day reshaping. All 24 leave-one-code-out exclusions and all six
  methods prevent a favorable replacement cohort from being selected. These
  exclusions and quarterly winners are descriptive, dependent comparisons.
- **Electricity:** Signed normalized deltas can be added across customers because
  the macro score uses equal customer weights. Their concentration diagnostic is
  not a decomposition of aggregate-load MAE, where customer errors can cancel.
  Label the signed denominator and matched 2014 safe-hour load-share support.
  Zero net delta would make the concentration share undefined.
- **ECG bootstrap:** Resampling whole people with shared draws across methods,
  summing their confusion matrices with multiplicity, and then recomputing
  fixed-four-class F1 preserves the declared pooled score. Averaging patient F1s
  would change it. The resulting empirical percentiles condition on the saved
  cross-validation predictions; overlapping training sets and the selected
  benchmark prevent interpreting them as a general population confidence claim.
  Repeats are dependent reuse of 43 people. Missing classes and failures must be
  retained with support, undefined precision/recall, and the original F1 rule.
- **Detection:** Keep the original first-alarm/no-restart rule. Overall detection
  is postchange first alarms divided by 200; conditional detection instead uses
  200 minus early alarms. A no-alarm miss is distinct from an early false alarm.
  The zero-shift cell estimates false alerts, not meaningful change detection.
  Wilson denominators must follow these units; zero eligible trials give an
  undefined conditional rate/interval. Finite grid results cannot establish
  smoothness, universal calibration, or simultaneous uncertainty coverage.
- **Spectral:** Shared realizations and a frozen LS grid make this bounded
  sensitivity useful. Matched band limits still leave different bins, spacing
  assumptions and interpolation behavior. Off-grid truths reduce dependence on
  the original truth-grid alignment without isolating every algorithmic cause.
  Every-three-second aliases remain physical ambiguities under every noise level,
  even if a numerical tie rule happens to recover the planted frequency.
- **River/air:** Captions need their distinct scoring supports. Count true air
  events once per duration using a single model's truth ledger or validated
  model-independent event keys; do not sum model-repeated truth events. Left and
  right censoring counts can overlap and are not added to missed-event counts.
- The stated additions are sufficient. No new source, hyperparameter search,
  extra bootstrap family, expanded grid, or significance-testing quota is needed.

## Evidence checked and next gate

Read-only CSV/source inspection found all **31** declared CO₂ origins usable,
and p12/p36 predictions present for both linear fits at every origin. Retail's
24-column daily panel spans 2009-12-01 through 2011-12-09 (739 rows), sufficient
for the first 364-day history window. The ECG manifest contains 43 people.
Reviewed `co2.predict/regression_matrix`, `retail.forecast/predict/summarize`,
`ecg.fold_indices/fit_fold/classification_scores`, detection `stream/scores/
first_alarm/summarize`, spectral generation/grid/peak helpers, electricity/oil
summaries, air event grouping, and the shared source guard.

The implementation gate must check exact history boundaries, anchoring and
calibration arithmetic, person/method alignment and bootstrap multiplicities,
repeat membership/disjointness, first-alarm partitions and interval denominators,
unchanged spectral grid/tie rules, contract hashing, and original-artifact
preservation. These are prospective checks, not verified implementations.
