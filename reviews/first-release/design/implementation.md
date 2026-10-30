# First-release design review: data and implementation perspective

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: the three draft study contracts, source-constraint carry-forward,
feasibility, and retained evidence. Supporting intake documentation, audit, and
adapter were read for context; this is not implementation approval and no loader
or model was executed during this review. The reviewer did not author the
contracts or adapter. HEAD remained
`d7218096c7920e30da3ad722a3d1bffbede8fa4e`; reviewed additions were uncommitted.

**Design verdict:** the proposed studies are bounded and implementable, and the
material source constraints have been carried into their designs. Settle DI01
before fitting the electricity models. DI02 and DI03 are small reproducibility
and reporting clarifications to incorporate before the protocol commit; they do
not require new datasets or a larger experiment. This review does not verify
source handling in execution, release readiness, or analytical remedies R01–R16.

## Findings

### DI01 — Freeze treatment of negative electricity predictions

Priority: medium; resolve before affected model fits. Status: `identified`.

The target is nonnegative power, but unconstrained Ridge can emit negative
predictions. The contract specifies models and metrics without saying whether
these predictions are scored directly or clipped at zero. Post-hoc selection of
that policy would change the evaluated method after seeing its errors.

Choose either policy now, apply it consistently to local and pooled fits, and
persist raw predictions plus any transformed prediction used for scoring. Record
the frequency of negative/clipped predictions. This is a benchmark definition,
not a claim that negative predictions have occurred.

### DI02 — Specify the remaining synthetic process conventions

Priority: medium; clarify before the protocol commit. Status: `identified`.

The contract specifies seeds, sample sizes, calibration quantiles, and online
information. For an exact reproducible experiment, also state the AR initial
distribution, innovation scale, the baseline standard-deviation convention, the
size of the planted shift in true versus estimated standard deviations, and the
score recurrence/initial value. The phrase stationary AR(1) should correspond to
stationary initialization, rather than silently starting every stream at zero.

Suggested explicit form: standard-normal initial AR state with innovation scale
`sqrt(1-rho**2)`; a fixed +1 shift in true marginal-standard-deviation units;
baseline mean/sample standard deviation from points 0–99; standardized score
using those frozen estimates; CUSUM starting at zero and updated as
`max(0, previous + standardized_value - 0.5)`. The author may choose another
fully stated convention. Freeze whether equality with a threshold triggers an
alarm and specify delay-zero behavior at the change index.

### DI03 — Narrow two evaluation labels to the actual target sets

Priority: low; reporting clarification before the protocol commit.
Status: `identified`.

- Annual December CO₂ origins mean horizon 1 targets January, while horizons 12
  and 36 target December. State this directly; the experiment does not evaluate
  a full monthly forecast trajectory or every seasonal phase. This does not
  invalidate the chosen comparison.
- Electricity's fixed 2012 90th-percentile cutoff defines hours above a historical
  threshold, not necessarily the top 10% of 2014 hours. Label the subgroup that
  way and report how many evaluation hours meet it.

## Source constraints successfully carried into the draft

- CO₂ uses the pinned monthly-average column, excludes the early Scripps period,
  preserves the time axis through quality exclusions, and describes the task as
  revised-data hindcasting. The negative-metadata discrepancy is reflected in
  the OR rule and cautious `quality-suspect` terminology.
- The CO₂ site-substitution sensitivity explicitly excludes affected targets.
  It does not claim to remove every potential effect on training observations.
- Electricity declares its assumed interval-end convention, mean-power target,
  nominal provider clock, and unknown real reporting delay. No UTC or settlement
  reconstruction is claimed.
- Calendar-based DST treatment replaces an all-customers-zero inference. Removing
  each transition day and the following 14 days covers the stated maximum
  336-hour lag. Implementation must apply the same validity rule to training
  targets and all required feature history.
- Eligibility and scale-ranked panel selection use only 2011/2012. Selection is
  deliberately nonrandom and the contract limits its generalization accordingly.
- Attribution distinguishes raw data from the modified hourly subset. The
  acquisition manifest and intake audit separately identify original bytes and
  analysis snapshots.

These are verified statements about the draft text, not execution claims.

## Feasibility and evidence expectations

The bounded regression comparisons avoid dependency and tuning expansion.
Electricity's two evaluated years imply 576 local monthly fits plus 24 pooled
fits for the declared 24-customer panel, excluding trivial baselines. This is
consistent with a modest linear-model study when thread counts are bounded;
actual runtime and peak memory still need measurement.

The implementation review should inspect one complete midnight forecast trace,
especially previous-day mean construction, monthly fit cutoffs, lag indexing,
training-only scaling, and DST validity. Retaining new daily observations as
inputs within a month is allowed by this contract; refitting on current-month
targets is not. Save row-level predictions, included/excluded counts, monthly
scale/coefficient records, split/configuration hashes, warnings, and exact score
inputs. Do not claim the source or design review has established these behaviors.

## Inspected SHA-256 hashes

```text
355de8b3405b26f4ebfd21e2ca3a665d5b43a0b46062a3aaafe7cd25edc89fad  studies/co2/DESIGN.md
51bce01c2f693200434c8e480f5ec2d3e0cea30051dfb5dad80529d65634faa1  studies/electricity/DESIGN.md
ce8b0b9ef22f4c7f4d56f8b38487ad16e2834bf6510922a0c3f5e0a4158bfac5  studies/synthetic/DESIGN.md
a834f7e306f6ba87c6a3e4fbdfbdfb2d9cf4b6900676706b85eb0e406a9a9588  data/README.md
2b44293c453ecd008e8c7cf76e87a3f38a592afdd14870cb54b408309b020198  reports/intake/audit.json
20c2b1b2b1be74dade626c8b54d18f3db5691ec3e82b94416fa4bd73d65a1fd5  src/tsatlas/data.py
```

## 2026-10-30 — Independent verification of design amendments

Reviewer: `/root/implementation_critic`, rereading the author-amended contracts.
The initial review and its inspected hashes above are preserved.

**Docs-only freeze verdict: the three contracts are ready to freeze and commit.**
DI01–DI03 are verified as documentation corrections at the hashes below. No
remaining design blocker was found in this review's scope. This is not approval
of unreviewed model implementations or evidence that any model result is correct.
The mandatory implementation review still precedes full runs.

- **DI01:** electricity explicitly clips learned forecasts at zero for both local
  and pooled fits, retaining raw forecasts and clipping counts. The previously
  unspecified scored-output transformation is now fixed before fitting.
- **DI02:** synthetic generation specifies a stationary standard-normal AR
  initial state and innovation scale; a fixed additive 1.0 shift in true marginal
  standard-deviation units; baseline `ddof=1`; CUSUM state `S[99]=0` with updates
  beginning at 100; a strict threshold comparison; and the outcome/denominator
  partition. Detection at index 200 has zero delay. These are textual conventions
  whose implementation must still be checked.
- **DI03:** CO₂ explicitly limits the evaluated targets to January/December for
  the selected December origins. The electricity peak subset is labelled using
  its fixed 2012 threshold and is no longer described as necessarily 10% of
  evaluation hours.
- The revised electricity contract also fixes a common mean-loss regularization
  penalty through `alpha = .001 * n_training_rows`, a justified clarification from
  the broader independent review. Local and pooled models retain a matched
  penalty convention despite different fit sizes. This verifies the stated
  formula only, not its future execution.

```text
e3a18e9a3df89cdbb9ab48b5d89de155474d3bc7311570469aca1523afd222f8  studies/co2/DESIGN.md
7237e98c225fdc788fc84c311ca39a34adf0a006b9c495353df9590753e3e09a  studies/electricity/DESIGN.md
4febf3974bdce85bbefbec9688480b50c89723ebd6f1c081cfbc4e8e1dfba0ec  studies/synthetic/DESIGN.md
```
