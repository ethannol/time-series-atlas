# First-release design review — statistical perspective

Reviewer: `statistical_critic`, an AI subagent that did not author the contracts.
Date: 2026-10-30.
Scope: the draft CO₂, electricity, and synthetic contracts, with source-intake evidence and population-selection documentation. No model fitting, implementation validation, or result interpretation was performed.

## Verdict

**Approve the proposed study designs for implementation; no source/target, leakage, split, or scoring defect was found that blocks the proposed comparisons.** Incorporate the small scope and denominator clarifications below when freezing the contracts. This is not approval of model code or permission to bypass the independent pre-run implementation checkpoint. No claim of statistical skill is established.

## Design strengths checked

- CO₂ calibration origins end in 2006 and their longest-horizon targets end in 2009, before the first test origin. Reusing older observed test-period measurements for later fits is legitimate under the declared rolling-origin task; interval calibration remains frozen. The small empirical interval calibration sample and overlapping multiyear errors are acknowledged.
- CO₂ uses a substantive trend-plus-seasonal baseline rather than relying only on seasonal naive. Quality-suspect records retain their calendar positions. The target column, cutoff, source-period qualification, and substitution sensitivity are explicit.
- Electricity uses training-period cohort selection and a fixed population for all comparisons. Its declaration of nominal mean power, interval-end assumption, latency assumption, and exclusion of physical-settlement claims is appropriate for the source.
- Excluding transition days and the following fourteen days covers the longest stated 336-hour lag; the previous-day mean is also covered. The code must implement this on the same shifted nominal-day axis used for target construction. Secondary transition-inclusive scoring is explicitly a separate sensitivity analysis.
- Monthly electricity fits use only earlier targets. All within-day features are available at the declared midnight origin if the previous day is completely reported as assumed. Newly observed lag inputs during the month do not constitute model refitting or leakage.
- Electricity scoring preserves customer-level performance, a fixed training-period scale, and aggregate errors calculated after summing loads. It does not misuse the name MASE or claim a random population sample.
- Synthetic thresholds are calibrated on independent no-change streams and frozen before evaluation. First-alarm accounting prevents resetting away false alarms. The AR stress test is deliberately outside the IID calibration setting, and the contract does not promise real-world false-alarm control.

## Clarifications to carry into the frozen contracts

### D-STAT-01 — CO₂ evaluation covers particular calendar targets

**Priority:** low; scope clarification.

Annual December origins at horizons 1, 12, and 36 evaluate January, December, and December targets respectively. They do not measure average performance across all target months or issuance seasons. Keep the bounded design, but call the result a December-origin forecasting comparison. Show the number of origins per horizon (18 calibration, 13 test before any scoring exclusions) and actual counts after masks.

The substitution sensitivity removes affected target months only; it does not remove their influence from all later training histories. Label it precisely rather than presenting it as a complete removal of the observing-site change.

### D-STAT-02 — Synthetic outcome denominators should be a fixed partition

**Priority:** low; reporting and implementation clarification.

For each shifted condition, partition all 200 replicates into: first alarm before index 200; first alarm at/after index 200; and no alarm. Eligible replicates equal 200 minus prechange alarms. Report detection rate and misses among those eligible, along with all three raw counts; a prechange alarm is not silently counted as a successful detection or omitted from the overall experiment. Conditional median delay uses detected eligible replicates and should be unavailable when that set is empty. For no-change conditions, any-alert rate uses all 200 replicates. Apply both detectors to the same generated streams so their comparison is paired.

The contract's existing logic supports this accounting; this clarification prevents later implementation ambiguity. Freeze the sample-standard-deviation convention, score initialization, threshold comparison, and AR initialization in the implementation configuration before the reviewed bounded trial.

### D-STAT-03 — The high-load threshold is fixed by training data

**Priority:** low; wording clarification.

The electricity contract says “top 10% actual load hours” and then correctly specifies a threshold from 2012. Call these **hours exceeding each customer's 2012 90th percentile**. Their share of 2014 need not be 10%. Preserve per-customer scored counts, including empty subsets, and do not recompute the threshold on the final year.

### D-STAT-04 — Shared Ridge coefficients do not isolate pooling alone

**Priority:** low; accepted comparison limitation if retained explicitly.

In the usual sum-of-squared-errors Ridge objective, holding `alpha=1` fixed while multiplying the number of training rows changes the penalty relative to mean loss. The pooled fit also has customer intercept indicators. Thus the planned comparison combines shared coefficients, different effective regularization, and intercept structure; it does not identify a causal effect of information sharing alone.

The draft already discloses this limitation and is valid as a comparison of two specified forecasting procedures. Retain that framing in conclusions. Alternatively, use a penalty defined relative to mean loss and document the changed objective before any fitting; such a change should appear in the frozen contract, not be made after inspecting scores.

## Required evidence at the separate implementation checkpoint

Inspect actual training and prediction timestamps; future-perturbation checks; all paired model targets; source-quality and DST masks including lag history; means and peak thresholds fitted to their declared periods; interval-error sign and quantile calculation; aggregate-before-error scoring; and synthetic outcome/denominator partitions. Reject nonfinite predictions and make exclusions/failures visible rather than silently dropping them.

## Inspected SHA-256 hashes

```text
355de8b3405b26f4ebfd21e2ca3a665d5b43a0b46062a3aaafe7cd25edc89fad  studies/co2/DESIGN.md
51bce01c2f693200434c8e480f5ec2d3e0cea30051dfb5dad80529d65634faa1  studies/electricity/DESIGN.md
ce8b0b9ef22f4c7f4d56f8b38487ad16e2834bf6510922a0c3f5e0a4158bfac5  studies/synthetic/DESIGN.md
a834f7e306f6ba87c6a3e4fbdfbdfb2d9cf4b6900676706b85eb0e406a9a9588  data/README.md
2b44293c453ecd008e8c7cf76e87a3f38a592afdd14870cb54b408309b020198  reports/intake/audit.json
```

The approval applies to these designs with the stated limitations. It does not close the implementation-dependent remedies in the project's earlier review register.

## 2026-10-30 — Contract-freeze verification

I inspected the revised contracts at the hashes below, before any model fitting.

**Verdict: approved for freezing and implementation.** The principal requested clarifications are incorporated:

- D-STAT-01: the CO₂ contract explicitly limits the design to December origins and January/December targets. The existing sensitivity language limits exclusion to affected target months, rather than claiming complete removal of site-change influence.
- D-STAT-02: the synthetic contract specifies the complete changed-stream partition, eligibility denominator, missed-alarm fraction, delay definition, and no-change denominator. It also fixes stationary AR initialization, sample standard deviation, the one-sided score recurrence, and strict alarm thresholds.
- D-STAT-03: the electricity high-load endpoint explicitly uses the fixed 2012 90th percentile and does not imply that exactly 10% of evaluation hours exceed it.
- D-STAT-04: electricity now specifies a common mean-loss penalty with `alpha = .001 * n_training_rows`, removing the different sample-size weighting of the prior fixed-alpha proposal. The different intercept structure remains an acknowledged comparison limitation. Identical nonnegative clipping policies for learned models, with raw predictions and clipping counts retained, are also declared before fitting.

The implementation review must still check that both detectors see the same generated evaluation streams, empty eligible/detected groups yield explicitly unavailable rates/delays, and the synthetic shift magnitude is implemented against the stated generating-process scale (unit marginal standard deviation) rather than silently changing with each estimated baseline scale. These are pre-run verification requirements, not claims of an observed bug. The design is otherwise sufficiently specified for implementation; no model result has been reviewed or approved.

Verified contract SHA-256 hashes:

```text
e3a18e9a3df89cdbb9ab48b5d89de155474d3bc7311570469aca1523afd222f8  studies/co2/DESIGN.md
7237e98c225fdc788fc84c311ca39a34adf0a006b9c495353df9590753e3e09a  studies/electricity/DESIGN.md
28ab0483542d77bc66fadcd3b87dead99c203a3181eaeb3094c4000576420964  studies/synthetic/DESIGN.md
```
