# River-flow pre-run implementation review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: forecast temporal/QC boundaries, split/calibration logic, event evidence,
source metadata use, and bounded development checks. The reviewer authored no
implementation. No final 2005–2014 model predictions or accuracy scores were
computed by the reviewer.

**Initial verdict: hold the affected full river run for the event-evidence
correction below.** Temporal predictors and origin-safe calibration passed the
checks performed; this is not a forecast leakage finding. Remaining aggregation
denominator completeness should also be addressed in the reviewed implementation.

## Temporal and quality boundaries verified

Only QC exactly `A` and nonnegative flow enters the approved-flow vector.
Seven-day feature windows require all flow days to pass this rule, including
when only shorter lags are directly named by the flow-only model. Weather
eligibility is shared by all three methods, preserving the specified common
cohort. Inputs use only the origin day and preceding observations; future
target truth determines scoreability, not an input feature. The positive
training high-flow threshold uses approved training-period observations only.

Both calibration and test masks enforce target dates **and** the approved
origin boundaries. The split audit records the two excluded initial dates at
horizon three. Logistic fitting/standardization use training targets; alert
cutoffs use only information-valid calibration negative targets and strict
exceedance. Persistence remains an uncalibrated score, with no Brier score.
Convergence warnings and iterations are retained instead of silently dropping
models. The fixed cohort is not changed after source intake.

The reviewer ran the three authored focused tests: **3 passed**, with eight
existing timedelta deprecation warnings. A separate bounded development probe
explicitly truncated raw snapshot rows through **1995-01-31**, fitted gauge
01162500/horizon3 on targets through 1989 with calibration through 1994, and
produced **51 finite rows** (17 target dates, three methods). Actual eligible
origins ranged from 1995-01-06 through 1995-01-22; invalid QC/history removed
other trial dates. No accuracy statistic was computed.

Independent loops over raw seven-day windows reconstructed eligibility and
training/calibration/trial counts. Independently recomputed training feature
means/scales, negative-calibration counts, 90th-percentile cutoffs, and saved-
parameter trial scores agree. The development source hash was unchanged across
the probe. This was not a final-period execution or tuning exercise.

For all 17 gauges, snapshot metadata area/HUC match the intake audit and are
constant within gauge. Training-only cold-precipitation fractions are finite
and between zero and one. These are source/metadata checks, not model scores;
the fraction remains a climate proxy, not a snowmelt label or causal explanation.

## C-I08 — Event origin trace and missing-truth censoring

Priority: medium; status `identified`, 2026-10-30. The event ledger omits the
explicit origin field promised by the design. Event-start target dates and
horizons make it derivable, but the saved ledger should carry that origin
directly for both high runs and false-alert episodes.

More substantively, `right_censored` is set only when a run reaches the study
end. A high-flow run immediately followed by a missing/QC-rejected observation
is also right-censored: its observed end cannot establish that high flow ended.
An independent fixture with high flow January 3–4 followed by rejected January
5 truth reproduces `right_censored=False`, confirming the defect in the
inspected code. Correct that flag and check analogous alert-run boundary
metadata adjacent to unknown truth. Unknown values already split the runs;
the defect concerns honesty of retained event evidence, not forecast fitting.
Add a targeted fixture and verify before the full run.

## C-I09 — Retain each rate's contributing-gauge count

Priority: low; status `identified`, 2026-10-30. Primary aggregation retains
`recall_gauges` and `fpr_gauges`, but macro precision lacks its defined-gauge
count. Area/climate grouped rates similarly retain only total gauges. The
design promises the contributing count for each null-excluding macro rate.
Add precision and subgroup contribution counts rather than implying all gauges
contribute to every rate. Entirely undefined aggregates should remain null,
not NaN that fails strict JSON serialization. This does not change any score
definition or authorize selecting gauges by observed performance.

## Evidence and limits

The inspected author trial names the same initial source hash as the reviewer's
independent bounded check. Full output provenance and numerical results are
later gates. The report template correctly separates high-day recall from
eligible-onset recall, calendar offsets from operational lead time, and
known-gauge comparisons from geographic transfer. The two panels use different
aggregation units, disclosed in its prose. Event-scoring strata use future
truth only to describe eligibility, not to generate the forecast.

## Initial inspected hashes

```text
66cac156ec5e5194a15ee2da689503aaae3e771fff8b46752448916d7b1a0308  src/tsatlas/river_flow.py
abd362a9d39d43d06675b2c621ba7a87d3839039c4d2674f8370d0b7d63d7d20  tests/test_river_flow.py
19acfb8f72b093b6ec2b4947c6a7d53f05a4c0f79f800bfda1abf959a62f5021  studies/river-flow/DESIGN.md
36a342dd2c23a9826d25a478a7a85028c70e6f93395f7e7befc3571de580fd6a  src/tsatlas/classification.py
8426fccd9461d410d2fd76ffe700009b9fdc647eda42271cb1112a471c0ad775  reports/intake/river-flow.json
392dd930c5a975488d938ae56ee722982c02feca9f32b0bb0a7d8af299295956  data/snapshots/river-daily-panel.csv.gz
```

## 2026-10-30 — Event, cohort, and denominator fixes verified

**C-I08: fixed and verified.** Both event types retain explicit origin and
target dates. High runs ending before unknown truth are right-censored. Alert
segments adjacent to unknown truth, unissued forecasts or the study boundary
are retained as `unresolved_alert_segment`, rather than being counted as proven
wholly false episodes. Fully bounded, known-false episodes remain separate.
The design records this clarification before final comparison results exist.

The reviewer reran the expanded focused suite: **4 passed**, with 12 existing
timedelta deprecation warnings. Independent fixtures verified a censored high
run, unresolved alert segments beside unknown truth and an unissued forecast,
and a fully bounded false episode. Every event origin equals its target date
minus the declared horizon. The unissued-forecast fixture also emitted a
pandas downcasting future warning; it executed successfully in the locked runtime.

**C-I09: fixed and verified for numeric aggregation.** Primary precision and
Brier estimates now retain contributing-gauge counts; grouped recall/FPR
estimates retain their counts. `mean_defined` returns null for an entirely
undefined rate. Primary method and onset contrasts use matched gauge/horizon
sets, with unevaluable statuses and excluded pair identities retained.
Independent checks confirmed the null helper's behavior.

The split audit now gives invalid-input, invalid-target, intersection and union
counts. The current trial reconciles 17 eligible plus 12 invalid dates to 29
scheduled dates after the two origin-boundary exclusions; the intersection is
zero in this trial. The refreshed finite-only author trial at
`2026-10-30T22:16:14.848910+00:00` names the exact inspected `e46cc7e…` source
and explains the repetition. It retains the same 51 rows and no accuracy scores.

One small follow-up remains in the renderer: it still applies `:.3f` to possibly
null macro values. Use a null-aware label so the corrected aggregation can be
published without a formatting exception. The daily river report/design also
mistakenly says false-positive “hours/hourly”; correct to days/daily. These
follow-ups do not alter forecasting or score definitions; final identity
verification follows below when corrected.

```text
e46cc7ef7f80f0847f858d8e5e1cd4dbb29377a6b5e4907c2180e236b96b2dc3  src/tsatlas/river_flow.py
5f8a5381ff03a93de82d6911c250ea16b52f6c0c4b4fa800a2d6160732f859ce  tests/test_river_flow.py
b1c10d8c068361126bcb19d9c3f0edc7b2e5e9cf7f329aae41b073bed2c2f16d  studies/river-flow/DESIGN.md
ed89646446782b53693fc5b13e475557137544d42b8536f803e80c6f66504602  reports/verification/river-flow-development-trial.json
```

## 2026-10-30 — Final pre-run gate

**Final implementation verdict: pass.** C-I08 and C-I09 are verified closed;
the null-aware formatter and daily wording are corrected. Commit the reviewed
source/design and satisfy the separate statistical gate before the full run.
Result interpretation and clean-checkout reproduction remain later checkpoints.

The reviewer reversed only the explicit formatting/text edits in memory and
obtained the exact earlier `e46cc7e…` source hash and `b1c10d…` design hash.
This proves the final delta contains only the reviewed null-aware formatting
and hours-to-days wording; predictive, event and numeric aggregation functions
are unchanged from the tested source. The extracted formatter was directly
checked for `None` → `undefined` and `0.25` → `0.250`. No fit was repeated for
this presentation change. The finite-only trial retains its honest earlier
source identity rather than being relabelled as a later execution.

```text
f9166af30692780c85e8e276ad6081fed4c28821d6f89cc90200b2ed34e36829  src/tsatlas/river_flow.py
996fef9e5d69d8187ecddbe4690592badfda3b825d91c123a5b03173cf2843ee  studies/river-flow/DESIGN.md
5f8a5381ff03a93de82d6911c250ea16b52f6c0c4b4fa800a2d6160732f859ce  tests/test_river_flow.py
ed89646446782b53693fc5b13e475557137544d42b8536f803e80c6f66504602  reports/verification/river-flow-development-trial.json
```
