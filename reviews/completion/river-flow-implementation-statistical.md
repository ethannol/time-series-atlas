# River-flow pre-run implementation review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: `river_flow.py`, focused tests, amended contract, and the pre-2005 bounded
development trial. No final-period forecast fit or accuracy comparison was run
by the reviewer. The reviewer did not author implementation or tests.

**Initial verdict: core forecasting/split logic passes; complete RI01–RI03 before
closing the implementation gate.** These findings concern event provenance,
coverage and comparison denominators. They are not evidence of an executed
final-period leakage error. A later appended verification will record closure.

## Core logic checked

`approved_flow` accepts exactly QC `A` and nonnegative flow. The pinned source
preserves a complete daily calendar, so shifts/rolling windows refer to calendar
days rather than compressing unknown dates. Seven-day flow and weather windows
terminate at the origin; negative precipitation and nonfinite features invalidate
the common information cohort. The flow-only, weather and persistence methods
share that cohort and approved target truth within each gauge/horizon.

The reviewed transformations are log1p current/lagged flow, log1p seven-day mean
flow, annual phase, log1p current/three-/seven-day precipitation and mean
seven-day temperature. No current target or intervening future weather enters
a feature. Standardization and logistic fitting use only training targets;
the high-flow percentile uses approved training flow only.

The amended origin guards are implemented in `split_masks`. At horizon three,
the first eligible calibration target is January 3, 2000 and the first test
target January 3, 2005. This prevents later training/calibration outcomes entering
an earlier issue time. Independent date checks verified both boundaries, not
just the test boundary. Strict alert cutoffs use only calibration scores on
non-high targets; ties are not alerts. Persistence remains an uncalibrated score
and is correctly excluded from Brier scoring.

Onset eligibility is calculated only in `event_ledger`, after forecasts exist.
Its intervening non-high observations define a retrospective secondary stratum;
they do not filter the main forecast population or become fitted features.
Event calendars are restored before alert-run counting, so absent dates are not
compressed into adjacent issued alerts. The separate equal-gauge high-day and
pooled eligible-onset denominators are named in the report template.

## RI01 — Event censoring and origin provenance are incomplete

Type: observed event-ledger defect/contract omission. Priority: correct before
the full event output is produced. Status: identified.

`right_censored` initially means only the end of the test window. A high run
ending immediately before missing/estimated truth also has an unknown
continuation. The independent toy fixture has high flow January 3–4, excluded
`A:e` truth January 5, and high flow January 6. The first recorded run incorrectly
has `right_censored=False`; the second correctly has a censored start.

Mark missing-truth boundaries correctly, and distinguish alert segments touching
unknown/unissued boundaries from fully observed episode endings. Unknown truth
must not be treated as observed low flow or evidence that the entire underlying
alert episode was false. Preserve the frozen known-segment scoring interpretation
explicitly instead of inferring unobserved event duration.

The contract also promises origin/target dates in event evidence. The code
computes an onset origin but saves only event start/end and horizon. Add explicit
origin/target-date fields (with appropriate segment-start meaning for alert
episodes) so the forecast timing is directly inspectable.

Closure requires a missing-truth boundary fixture and inspection of saved event
fields. No final outcome ranking is needed to make this correction.

## RI02 — Make the split coverage counts reconcile

Type: observed incomplete audit specification. Priority: fix before publication;
prefer before full output generation. Status: identified.

`test_invalid_input_rows` and `test_invalid_target_rows` are separate masks and
may overlap. Without their intersection/union, the excluded counts cannot always
be added to explain the scheduled-to-scored denominator. Add an explicit overlap
and union, or mutually exclusive exclusion categories, and verify the identity
`scheduled_after_boundary = scored + excluded_union`.

Keep the two boundary exclusions distinct from missing-input/target exclusions.
The early development trial happens to reconcile with 29 scheduled, 17 scored,
9 input-invalid and 3 target-invalid rows; that does not prove overlap is absent
in other gauges/horizons.

## RI03 — Preserve matching gauge populations and rate denominators

Type: prospective comparison risk plus missing denominator fields.
Priority: enforce before full comparisons. Status: identified.

The implementation can retain persistence when a logistic training class is
absent, recording the logistic model as unevaluable. Without an explicit matched
gauge policy, subsequent model macros could compare different gauge populations.
Preserve all failures/unevaluable statuses and use matched gauges for method
contrasts, with the included/excluded IDs or an explicit equality assertion.
Do not silently replace a gauge or choose a threshold using test outcomes.

The primary macro already records recall/FPR contributing-gauge counts, but
not the precision denominator; grouped macros record total gauges without
rate-specific contributors. Add those counts and explicit null handling when
no gauge contributes to a rate. This follows the frozen contract's distinction
between unevaluable denominators and zero performance.

## Bounded evidence executed

`uv run pytest -q tests/test_river_flow.py`: **3 passed** on the initial inspected
implementation. Tests cover future feature mutation, estimated-flow masking,
the horizon-three test boundary, and onset/miss behavior. Existing NumPy
timedelta deprecation warnings did not fail the tests.

Independent toy arithmetic verified the current/lagged/seven-day flow features,
precipitation sums, temperature mean, negative-precipitation rolling mask, and
both calibration/test origin boundaries. A separate missing-truth event fixture
demonstrated RI01 as described above.

The author trial uses gauge 01162500, horizon three, training through 1989,
calibration through 1994 and January 1995 trial targets. Its 51 prediction rows
are three methods on 17 eligible targets, finite, with no accuracy computed and
no 2005+ inputs. It records two removed boundary targets in calibration and test.
This supports execution/indexing only; no final-period performance is inferred.

## Initial inspected SHA-256 identities

```text
66cac156ec5e5194a15ee2da689503aaae3e771fff8b46752448916d7b1a0308  src/tsatlas/river_flow.py
abd362a9d39d43d06675b2c621ba7a87d3839039c4d2674f8370d0b7d63d7d20  tests/test_river_flow.py
19acfb8f72b093b6ec2b4947c6a7d53f05a4c0f79f800bfda1abf959a62f5021  studies/river-flow/DESIGN.md
01592cfc8a075106b5dd52f9101ca41d1c4ec2436aec3628b4090f793fe2d878  reports/verification/river-flow-development-trial.json
```

2026-10-30, statistical reviewer: forecasting/split logic checked; RI01–RI03
identified; final pre-run approval pending the bounded corrections above.

## Pre-run correction verification — 2026-10-30

**Statistical implementation verdict: approved for the frozen full run. RI01,
RI02 and RI03 are closed for this gate.** This is approval of implementation and
bounded execution evidence, not a result or publication verdict. No final-period
model fit, score comparison or model retuning was performed by this reviewer.

RI01: high runs now end with `right_censored=True` at unknown truth as well as
the test edge. False-alert segments touching unknown truth, unissued forecasts
or study edges are separately labeled `unresolved_alert_segment`. The ledger
saves explicit origin and target dates; for an alert segment these describe its
first forecast target. Independent fixtures checked an interior fully observed
false episode, an unissued neighbor, both study edges, and two high segments
separated by excluded `A:e` truth. The first high segment is right-censored and
the second left-censored; the latter is not treated as an eligible onset. All
saved origin/target offsets in those fixtures are exactly the stated horizon.
These are repairs to pre-run ledger behavior, not discoveries about river skill.

RI02: the split audit now includes invalid-both and invalid-union counts and
raises if scored rows plus the invalid union do not equal scheduled rows after
the origin guard. The union equals the two invalid counts minus their overlap.
Boundary exclusions remain separate. Both identities passed in the bounded
trial; a separate overlapping-mask arithmetic fixture checked the inclusion–
exclusion identity rather than assuming the trial's zero overlap generalizes.

RI03: primary and event comparisons now restrict to gauge/horizon pairs with
all three methods. Per-gauge output and every model's parameter/status record
remain available, with omitted pairs recorded explicitly in metrics. Primary
macros retain recall, false-positive-rate, precision and Brier contributor counts;
subgroups retain contributor counts for both rates they report. Undefined rates
remain null; the report formatter labels them undefined. This closes the
unequal-gauge comparison risk without deleting failed attempts or selecting
replacement gauges. Precision contributors can still differ by method when a
method makes no positive predictions; the counts expose that intended convention.

The contract documents the event/matching clarification as pre-run. Thresholds,
features, model settings, target-date splits and origin guards remain unchanged.
The four focused tests pass. Independent event fixtures also pass; pandas/NumPy
deprecation warnings are not suppressed in the archived test outcome and do not
alter the observed assertions.

The author's refreshed finite-only trial records the earlier source identity
`e46cc7ef7f80f0847f858d8e5e1cd4dbb29377a6b5e4907c2180e236b96b2dc3`.
To cover the final null-formatting/presentation revision directly, this reviewer
repeated the same bounded gauge 01162500/horizon-three execution on current
source, with only rows through January 31, 1995 passed into `predict_gauge`.
Training ends in 1989 and calibration in 1994. All 51 predictions are finite;
no accuracy was computed. Audit counts are 3,286 training rows, 1,588 calibration
rows and 17 trial targets per method; 29 scheduled targets reconcile as 17
scored plus 12 invalid (9 input, 3 target, 0 both). Both later-period origin
guards exclude two boundary targets. This checks execution without inspecting
the final 2005–2014 evaluation period.

### Verified SHA-256 identities

```text
f9166af30692780c85e8e276ad6081fed4c28821d6f89cc90200b2ed34e36829  src/tsatlas/river_flow.py
5f8a5381ff03a93de82d6911c250ea16b52f6c0c4b4fa800a2d6160732f859ce  tests/test_river_flow.py
996fef9e5d69d8187ecddbe4690592badfda3b825d91c123a5b03173cf2843ee  studies/river-flow/DESIGN.md
ed89646446782b53693fc5b13e475557137544d42b8536f803e80c6f66504602  reports/verification/river-flow-development-trial.json
```

No remaining statistical blocker to the frozen full run was identified in this
scope. Results, interpretation, figures and exact reproduction still require
their subsequent gates.
