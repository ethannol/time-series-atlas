# Retail pre-run implementation review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: `src/tsatlas/retail.py`, its focused tests, the frozen retail contract,
shared run-provenance helpers, and the bounded development-trial record. The
reviewer did not author model code or tests. The contract is frozen in commit
`b369cc865d4eafaabe8e8f4d3b7ba26ae36bb0ba`, on the completion branch whose verified
baseline is `bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`.

**Verdict: statistical implementation approved for the declared pinned retail
panel and full schedule.** No source/target, recurrence, leakage or score-arithmetic
blocker was found. Two minor output corrections below should be made before
publication. The independent implementation critic's gate and committed-source
requirements still apply. No full scoring or final-result inspection was performed
by this reviewer; this is not a results/publication approval.

## What was checked

### Daily states and weekly availability

- Croston initializes its nonzero size at the first positive observation and its
  interval at the one-based elapsed day from collection start. Subsequent gaps
  count every day since the preceding positive, including the next positive day.
  Size and interval update only at a positive observation; SBA multiplies the
  ratio by `1-alpha/2` with the frozen alpha 0.1.
- TSB uses the same nonzero-size updates because both size smoothing constants
  equal 0.1. Occurrence probability initializes at the inverse first interval and
  updates every following day, including zeros. Thus its rate decays during
  inactivity while Croston's remains unchanged. Sharing the size state is valid
  for these equal frozen size-smoothing constants.
- Recomputing these deterministic states from all allowed daily history at each
  origin is equivalent to carrying them forward. History is strictly before
  Monday's origin; the target is the seven dates Monday through Sunday. January
  1–2 are correctly available for the first January 3 forecast. Multiplying each
  intermittent daily rate by seven uses no within-week observations.
- Zero, the preceding seven-day sum, and the preceding 28-day daily mean times
  seven use the declared history. The scale uses only 2010 and remains fixed.
  The actual schedule ends November 28, covering through December 4: 48 full
  weeks for all 24 fixed products, with no later activity filter.

### Scores and report logic

Every product has the same complete weekly schedule. Therefore the mean of
absolute error divided by each product's fixed scale equals the promised
equally weighted mean of per-product scaled MAEs. This equivalence depends on
the balanced panel; a future incomplete/unbalanced extension must preserve
explicit product weighting rather than silently reusing the row average.

Raw-unit MAE, mean signed error, observed/forecast unit totals and underforecast
counts have the correct signs and units. Per-product and quarterly summaries use
the same definitions. The two plot panels properly distinguish equal-product
scaled accuracy from summed-unit bias, which can be dominated by large sellers.
The generated lowest-error statement is calculated from the actual primary
metric and remains limited to this fixed panel. It does not claim that the winner
optimizes inventory, profit or unobserved demand.

Shared run helpers check pinned inputs, require committed source/configuration,
record the protocol commit and input/source hashes, and reject changed source
or inputs before publishing a run directory. This review read those controls;
the separate provenance/implementation review remains responsible for their
broader validation across studies.

## Executed bounded evidence

`uv run pytest -q tests/test_retail.py`: **3 passed**. These tests cover TSB
inactivity decay versus unchanged Croston, all-zero histories, rejection of
unknown/signed/multidimensional sales, and mutation of target/future values
without changing earlier forecasts. The run emitted NumPy timedelta deprecation
warnings under the current pinned environment; it did not fail. They do not alter
the verified target dates, and future dependency changes require rerunning checks.

An independent toy arithmetic check passed without fitting or scoring the real
test period:

- For `[0,0,10,0,20,0]`, final size is 11 and interval is 2.9, giving SBA rate
  `0.95*11/2.9`. TSB probabilities after initialization are `1/3`, `0.3`, `0.37`,
  `0.333`, giving rate `0.333*11`.
- `[10,20]` confirms a consecutive-positive gap of one day.
- A complete artificial calendar with January 1–2 values changed to 11 and 21
  produces preceding-week total 37, rolling-28 forecast 14.5, seven-day target 7,
  and unchanged 2010 scale 7 at the January 3 origin.
- A balanced two-product toy frame with tenfold scales gives macro scaled MAE
  0.5, unit MAE 27.5, zero signed mean error and equal total forecasts/outcomes.

The first reviewer-authored arithmetic attempt had an incorrect TSB reference
probability; a subsequent exact floating-point assertion also needed a numerical
tolerance. Corrected independent calculations passed without changing production
code. Those were review-check errors, not implementation defects.

The author's `reports/verification/retail-development-trial.json` records one
December 20, 2010 origin for two products, ten finite nonnegative prediction
rows, no comparative accuracy calculation, and the inspected retail source hash.
It is a bounded execution/shape check rather than held-out performance evidence.
The full-2010 scale in that pre-test trial must not be interpreted as an
origin-safe December forecast evaluation; no such accuracy claim is made.

## Minor findings

### RI-S01 — Save the promised signed total error directly

Priority: low; output/protocol clarity, not a numerical-model blocker.
Status: identified.

The contract requests signed total error, but the summary directly emits mean
signed error and the two totals. Their difference already permits exact recovery,
so information is not lost; adding `signed_total_error_units` makes compliance
and downstream reading explicit. Preserve the sign forecast minus observed.
Verify it equals forecast total minus observed total in each summary.

### RI-S02 — Repair joined number/word tokens before publication

Priority: low; readability. Status: identified.

The report template contains tokens such as `contains24`, `using2010`,
`from2072`, `evaluated{...}` and `in2011`. Add normal spaces before the report is
published. This is a presentation change and needs no model retuning.

## Inspected identities

```text
12866e44e3d63a2bb6d999444442b8a414f70085a97d209fe078d11d7d456278  src/tsatlas/retail.py
bfe578cd417c166cba55ee069662773d4e135f5af55b8819a07de5006615751c  tests/test_retail.py
ccbbae99f581992fc1f9111d14d076fd316fa7db93e56dcad43fd21ae29df840  studies/retail/DESIGN.md
d71a5dcaf01e04e47a630cdeb9446e1e2b0dea608f3aabd75be37bee4aec7254  src/tsatlas/common.py
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
2ed602cb2eaf80d275bd1c9706c5276cd142e8b0e7b6ce1e6b6f5d2a6f71f7bb  reports/verification/retail-development-trial.json
```

2026-10-30, statistical reviewer: implementation approved for this frozen scope;
RI-S01/RI-S02 identified as minor output follow-ups. Full-run results and final
claims remain unreviewed.

## 2026-10-30 — Minor output corrections verified

RI-S01 and RI-S02: identified → implemented → verified. The summary now emits
`signed_total_error_units = sum(prediction - observed)`. An independent two-row
fixture produced -1 and verified equality to forecast total minus observed total.
The report template now separates the flagged word/number combinations and uses
readable number/license spacing. No method, target, split or prediction changed.

```text
d94819d04917c476abbd039a1f90ba46a6ff0ac633b09f1cd04cb636d2081c92  src/tsatlas/retail.py
```

The statistical implementation approval remains; there are no open findings in
this retail implementation review. Final results and publication remain separate
gates. No full model run or final scoring was performed for this verification.
