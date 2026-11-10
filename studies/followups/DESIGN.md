# Optional follow-ups — declared after seeing the original results

Date: 2026-11-10. Ethan authorized the optional suggestions from the dedicated
critiques. This is a finite extension of the published collection at
`1a0ec0180b857f7d98b092a8104a575657d53445`. Original results have already informed
these questions. These are **post-publication exploratory follow-ups**, not fresh
confirmatory tests or retroactive parts of the original frozen comparisons.

The original models, cohorts, splits, predictions and score artifacts remain
unchanged. Add separately named follow-up artifacts and clearly labeled report
sections. Run all declared comparisons, including failures; do not choose a
winning seed, cohort, time window, frequency grid or hyperparameter afterward.
No new external sources or refreshed input bytes are needed.

## Questions, comparisons and budgets

### CO₂: how much does anchoring at the last observed level matter?

For each existing calibration/test origin and horizon, preserve the expanding
and trailing-decade linear predictions. Reconstruct each fitted December origin
as `(3*p12-p36)/2`. Add the observed December minus fitted December to every
horizon of that model. This changes only its origin level; its slope and seasonal
coefficients stay fixed. Require usable origin observations. Score the two
anchored alternatives alongside the two original linear fits on the same targets.
Calibrate each anchored model's residual 10th/90th quantiles on the original
calibration period only. Report MAE, bias, 80% coverage/width/interval score for
1,12,36 months, with December-at-three-years primary for comparability.
Retain the original sensitivity excluding site-substitution-affected targets
for the anchored models too; this does not remove substitution effects in history.
No origin-anchored quadratic or tuning search. Add a source-series/origin-gap
figure to explain the starting-level problem. This arithmetic intervention on
the fitted procedure is not causal attribution about the atmosphere.

### Electricity: how large and concentrated is the pooling disadvantage?

Show relative changes in existing macro-normalized and aggregate MAE, with
denominators named. Report all customer deltas and actual load shares. Summarize
the largest two positive normalized deltas as a share of the signed net delta;
this is an after-the-fact concentration diagnostic, not removal of those customers.
Show the existing customer-specific peak thresholds, counts and each method's
peak MAE in a linked readable table. No new model, cohort or weighting.

### Retail: does an absolute-error-oriented forecast change the answer?

Add one **trailing median of 52 complete weekly totals** for each exact stock
code. At each existing Monday origin, use exactly the 364 preceding calendar
days, reshape into 52 seven-day totals, then take their ordinary sample median.
Require complete finite history. All existing origins have sufficient history.
This is a simple history-conditioned median baseline, not a proof of an optimal
conditional quantile. Same 48 target weeks and fixed training scales; no tuning.
Report the original five methods and this sixth method using the original scores.

Separately report volume concentration, quarterly winners, the small original
scaled-error gap, and leave-one-code-out scores for **all 24 exclusions** and all
six methods without choosing a replacement cohort. Explain the last-week summed
bias identity using the pre-test week and final target week. Add a hand-calculated
Croston/TSB recurrence regression test independent of implementation structure.

### Oil: which periods drive the pooled comparison?

Explain QLIKE and Brier in plain language. Show every existing test year's
variance and direction losses with its count. Compute each year's contribution
to the total fixed-minus-EWMA QLIKE gain within each market with target-count weighting; use
a clearly signed denominator and retain negative contributions. No new fitting,
source redistribution, artifact removal or legal conclusion. Existing source
and derived-outcome disclosure remains in place.

### River flow and air quality: make support visible when figures travel

Add the idealized daily reporting assumption, missed/false alerts and unscored
days to the river figure/portfolio captions. No new river fitting or selection.
For air quality, label MAE as macro station MAE, expose left/right censoring
counts for true events once per duration, and explain the observed calendar
baseline's absence of high alerts. Boundary censoring counts can overlap; they
are not distinct missed events. Preserve all score and event definitions.

### ECG: how stable is the finding across people and fold assignments?

Expose precision, recall, predicted count and true support for all four methods
and all four classes, preserving undefined values.

1. Patient bootstrap of the original held-out predictions: 2,000 draws, seed
   20261110, sample all 43 patient groups with replacement, keeping each group's
   beats together. Use the same sampled groups for every model. Recompute pooled
   fixed-four-class macro F1, accuracy and forest-minus-logistic macro-F1
   differences from summed patient confusion matrices. Report empirical 2.5/50/
   97.5 percentiles; zero F1-denominator convention matches the original metric.
   This measures conditional patient-composition variation of the saved
   predictions, not training uncertainty, independent fold replications, a
   population confidence guarantee or clinical validation.
2. Three additional five-fold patient assignments, seeds 20261110,20261111,
   20261112: sort the 43 patient IDs, permute with NumPy default_rng(seed), assign
   `permuted_position % 5`. Shared-person records remain together. Reuse the
   original fitting functions, training cap and model random seeds unchanged;
   only the assignment mapping changes. Every person is held out once per repeat.
   Changing membership also changes the existing RNG traversal used for capped
   training draws and the fold-specific model seed assigned to a person. Interpret
   this as whole-procedure split sensitivity, not an isolated causal fold effect.
   Retain mappings, training membership, prediction rows, model audit records,
   pooled and fold/class support scores. Report every repeat beside the original,
   plus their descriptive ranges; never choose the best repeat. The repeated
   scores are dependent reuses of the same people, not independent trials or a
   p-value for superiority. No hyperparameter search or post-result cap change.

### Synthetic detection: does failure vary smoothly with dependence and shift?

Keep original calibration maxima and thresholds. New evaluation seed 20261113;
loop rho in [0,.3,.6,.9], shift magnitude in [0,.5,1,2], replicate 0..199.
Generate the original unit-marginal-variance 400-point AR stream with no shift,
then add the declared magnitude at index 200. One realization feeds both methods.
No recalibration, restart or changed standardization. Retain every alarm.
Show no-change false alarms, early alarms, overall postchange detection, eligible
conditional detection, misses and conditional median delay with explicit counts.
For binomial proportions add pointwise 95% Wilson intervals; their trial unit
is an independently generated stream, not a time point. They describe Monte Carlo
variation conditional on the fixed calibration; they are not simultaneous bands.
Also expose the original overall detection fractions beside conditional delays.

### Synthetic sampling: are differences robust to search band and signal settings?

First apply matched-band peak selection (0.01–0.45 Hz inclusive) to both FFTs
on all original saved input realizations, alongside the original full-band FFTs
and original Lomb–Scargle. Keep the original fixed 2,403-point Lomb–Scargle grid
and 1/480 Hz recovery tolerance. A common band does not align frequency bins or
otherwise isolate timestamp handling. Retain every method/replicate result.

Then run a fixed robustness grid: true frequency [.08325,.17,.28725] Hz,
noise SD [.5,1.0], the three original sampling schedules, 50 independent
replicates per cell; seed 20261114. Loop in that order. Draw phase, then schedule
retention/jitter, then noise at actual sampled times as in the original generator.
Use the **unchanged grid** even for off-grid truth. All five procedures use the
same realization. Record inputs, peaks, errors, recovery and LS tie counts.
Report every cell with denominator 50 and pointwise Wilson intervals. For
three-second sampling retain analytic ambiguity even if numerical maxima are
not tied; recovery under a tie-break never proves unique physical identification.
This is 900 new realizations, not an open-ended frequency/noise search.

## Execution, review and evidence

Run units remain the same nine commands; each writes its follow-ups alongside
its original artifacts. The shared run guard must hash this contract as well
as the study-specific contract, and reject uncommitted or mid-run changes.
Original numerical files are compared byte-for-byte against the baseline.
Any intentional presentation change and each added artifact is enumerated.

Before full new comparisons: separate statistical, data/implementation and
general design reviews; then non-authoring technical implementation review and
bounded invariants. Freeze/commit final source and contracts before execution.
All fits and simulations run sequentially with one numerical thread; at most
three reviewers work concurrently. A bounded trial may estimate runtime but
cannot select parameters. No detached jobs.

After execution: independent reconstruction of added metrics, visual inspection,
general review of every conclusion, updated plain-language stories and explicit
review dispositions. Publish through green final-head/main CI, portfolio deploy
and live checks. Preserve the earlier reviews and append status history.
