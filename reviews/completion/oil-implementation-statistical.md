# Oil pre-run implementation review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: `src/tsatlas/oil.py`, focused tests, the reviewed oil contract frozen in
`715ac6c89b1948609c67626c883a4cc63ec3abde`, and the finite-only development trial.
No 2015–2025 scores, final predictions or model comparisons were inspected.
The reviewer did not author implementation or tests.

**Final pre-run verdict: approved from the statistical perspective.** The two
findings below were corrected and verified before a full test-period run.
Committed-source requirements and the independent implementation critic's
gate still apply. This is not a results or publication-content approval.

## Findings and verified corrections

### OI-S01 — The optimizer's variance floor initially changed physical units

Type: observed implementation/contract mismatch, found before final scoring.
Priority: required before the full run.

The initial `fit_garch` standardized changes by training RMS but called a
recurrence that hardcoded variance floor `1e-8` in its input units. The fit's
effective dollar-variance floor was therefore `1e-8 * RMS²`, while the frozen
contract requires `1e-8` in dollar-squared units. Ordinary prediction used the
declared dollar floor. This could make the fitting objective and prediction
recursion disagree near the floor; no claim is made that it affected any
previously published empirical result.

A concrete arithmetic counterexample with scale 10 gives a floored standardized
path converted back to dollars of `[100, 1e-6]`, versus `[100, 1e-8]` when
evaluated directly in dollar units. The author added an explicit floor argument
and now passes `1e-8/RMS²` during standardized fitting. The corrected comparison
matches `[100, 1e-8]` on both paths. The new regression test independently covers
this unit conversion. Model settings and final-period data were not retuned.

Status: identified → implemented → verified, 2026-10-30. The production objective
call, the units check, and the focused regression test all establish this remedy.

### OI-S02 — Direction gap summaries were missing

Type: observed output omission relative to the frozen evidence contract.
Priority: include before final reporting; no predictor change required.

The original output included calendar-gap breakdowns only for variance, although
the contract promises short/long observed-gap scores and saves gaps for both
tasks. The author added `direction-gaps.csv`, grouped at gaps `<=4` and `>4`
days for both direction models, and linked it from the report template. The code
uses the existing saved target dates/probabilities and changes no prediction.
The existing variance breakdown still includes those gaps, annual scores and
the predeclared 2020 contrast.

Status: identified → implemented → verified by code inspection, 2026-10-30.
Actual output values and row counts remain a post-run results check.

## Statistical implementation checks

Each market is processed on its own observed-price dates after dropping only
its own absent prices. First differences preserve the negative WTI observation.
No log-return transformation, cross-market fill or artificial weekend zero is
introduced. Gap length is the actual number of calendar days since that market's
preceding observation.

Change targets are assigned by their observation dates. Training objectives and
initial mean-square variance use 2000–2014 targets; the first 2000 change and lag
warm-up may use preceding history as expressly allowed. The full-history
rolling-60 series is shifted once. EWMA and GARCH initialize at the training
mean square and advance chronologically: the variance saved for a target uses
the previous change, never the target change itself. Independent scalar-loop
arithmetic reproduced the vectorized `lfilter` recurrence.

GARCH uses the three fixed starts, SLSQP iteration/tolerance budget, positive
omega/nonnegative alpha/beta and stationarity constraint. Selection is by
converged finite **training** objective, with all attempts retained. Conversion
of omega back to dollar units is correct. If all starts fail, execution raises
with the attempt diagnostics; it does not silently substitute an unreported
model. Actual final convergence/parameter values remain uninspected.

Direction rows are target-indexed: previous price and shifted change summaries
are all available at the immediately preceding observation's origin. The target
is strictly positive change, so zero is non-upward. Both models use identical
complete-feature training/test rows. The scaler, prevalence and logistic model
are fitted only on training targets, and rolling standard deviation uses ddof=0.
An independent toy vector check reproduced all five feature values at a selected
target row. The future-mutation test protects this offset explicitly.

QLIKE uses aligned finite changes and strictly positive variance; its formula
matches independent arithmetic. Raw squared-change MAE is a secondary proxy
loss, not a proper conditional-variance target by itself. Direction Brier,
threshold-0.5 accuracy and confusion counts use the correct labels. The two task
scores remain distinct. The figure compares each model with its own task's
baseline on identical rows; it does not compare score magnitudes across tasks.

## Local outcomes and proposed public artifacts

The public variance file drops true changes; the public direction file drops
true up/down labels. Complete outcome evidence goes to ignored
`data/processed/oil-evidence/` under content-addressed filenames. The new private
evidence test confirms a later save cannot replace earlier bytes. Public
metrics keep private evidence paths/hashes plus aggregate scores. This is
consistent with the reviewed fetch-only source policy; the final tracked files
and generated public outputs still require publication inspection.

The report's October 28, 2026 workbook release-date attribution was independently
confirmed in both raw XLS `Contents` sheets. Its caveats about revised inputs,
observed rather than fixed-calendar horizons, uncalibrated tail risk, and lack of
trading/ROI evidence are appropriate. Final reports must answer from actual
results rather than assuming variance will be easier to predict than direction.

## Bounded execution evidence

`uv run pytest -q tests/test_oil.py`: **4 passed**, including future-input
invariance, negative prices, variance-floor unit conversion and immutable
private evidence. Independent toy checks passed scalar recurrence, lagged
direction-feature arithmetic, QLIKE and the corrected floor conversion.

The refreshed development-trial record is tied to the final inspected source
hash. It fits through 2003 and records 32 variance rows and 16 direction rows
within the January 2004 bounded trial, finite positive variances, valid
probabilities and three successful GARCH starts. It explicitly says no accuracy
scores were computed. The author repeated it because the pre-run review changed
floor units/private evidence and added the gap output, before viewing final
2015–2025 results.

## Final inspected SHA-256 identities

```text
d3ab40ec71bae9cb94ac30829ae2dece45a124899f611cc8794663efb5456bf5  src/tsatlas/oil.py
cf44f073a01162c95a42c1f130e3f6c13337311fd7a1f0fde7f66a0aa959202a  tests/test_oil.py
64e2b98cd9f2a653bd8444412be50500a4007a211560045390e8f16e7515b2ef  studies/oil/DESIGN.md
d49a8218ceb13370113505f102986e296984c77f0ecc1a0e1db75bcfc7622ec6  reports/verification/oil-development-trial.json
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
```

2026-10-30, statistical reviewer: OI-S01 and OI-S02 verified; statistical pre-run
implementation gate approved. Final performance, realized failures, file
reproduction and publication claims remain unreviewed.
