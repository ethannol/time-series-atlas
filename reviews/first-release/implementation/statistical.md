# First-release implementation review — statistical perspective

Reviewer: `statistical_critic`, an AI subagent that did not author the implementation.
Date: 2026-10-30.
Scope: CO₂/electricity/synthetic algorithms, source adapters, metrics, CLI/run evidence, three test files, and the recorded two-customer January 2013 trial. No full study was run and no final evaluation scores were inspected.
Source baseline at inspection: `b374e9baa39f021481aefaefba958543534c916f`, with implementation edits identified by the hashes below.

## Initial verdict

**Hold the full-run gate until M-STAT-01 and M-STAT-02 are corrected and independently checked.** These are reproduced scoring-path defects on deliberately invalid miniature fixtures. They are not claims that the acquired source data or any fitted study predictions contained those problems. No core future-data leak or incorrect declared-model recurrence was found.

### M-STAT-01 — Electricity scoring silently omits missing predictions

**Priority:** medium; blocks scoring approval.

`electricity.summarize` uses pandas means and sums without validating its inputs. On a two-hour, one-client fixture with actual values `[10, 20]` and pooled predictions `[NaN, 20]`, it reports customer `n=2` and MAE `0.0`; the missing prediction is silently skipped. Its aggregate score treats the missing prediction as zero and reports MAE `5.0`. These disagree about the scored population and can conceal a failed prediction.

**Required correction:** reject nonfinite actuals/predictions before scoring and enforce the complete, unique hour/customer panel required by matched comparisons. Add a meaningful regression test showing the invalid fixture fails rather than producing favorable metrics.

### M-STAT-02 — Shared forecast scoring permits unpaired shapes and invalid intervals

**Priority:** medium; blocks scoring approval.

`forecast_scores([0, 10], [[1], [11]])` broadcasts a one-dimensional actual vector against a two-dimensional prediction vector and returns MAE `5.5`, rather than rejecting unpaired inputs. The intended aligned errors would each be `1`. Nonfinite interval endpoints are also accepted: one NaN lower endpoint changes reported coverage while width/interval score become NaN.

**Required correction:** enforce nonempty, equally shaped one-dimensional actual/prediction vectors; require both interval endpoints together, equally shaped and finite; reject reversed intervals. Test shape mismatch and nonfinite endpoints. Failing later JSON serialization is not sufficient, especially when broadcasting yields finite but incorrect metrics.

### M-STAT-03 — CO₂ origin timestamps needed a month-label qualification

**Priority:** low; corrected during inspection.

The model uses the complete December observation, while the former `origin` timestamp was December 1 because source rows are month-start-labelled. This did not establish a future-data leak under the declared monthly task, but could mislead readers about literal issuance. The author changed the field to `origin_month` and records the assumption that issuance follows availability of December's observation. I inspected those changes. Actual historical publication latency remains outside the study's revised-data claim.

## Algorithm and invariant checks completed

- CO₂ training filters to usable rows at or before the last observed month. The trailing window retains calendar positions. Regression time centering and seasonal indicators implement the declared comparisons. Calibration offsets use `actual - prediction` and are added to predictions, with calibration rows isolated from test rows. Sensitivity removes substituted-site targets and the report explicitly limits that interpretation.
- Electricity lag features and previous-day means use information before each target day's midnight origin. Monthly model targets end before the fitted month; scale estimates use only eligible training rows. Local and pooled penalties equal `.001 * n_training_rows`; clipping is shared and raw outputs are retained.
- An independent mask probe over every hour of 2011–2014 verified exact exclusion of each transition day plus fourteen following days. No primary-safe target had its stated 24/168/336-hour lag or previous-day-mean source day on a transition day.
- A miniature offsetting-error fixture verified that aggregate electricity error is calculated after summing predictions/actuals, and that the macro normalized score uses the fixed customer scales.
- Synthetic code generates the stream once per replicate before applying both methods. Separate seeds isolate calibration and evaluation. The AR recurrence has stationary initialization and unit marginal variance; a same-seed comparison confirmed the added shift is exactly one generating-process standard deviation after index 200.
- Independent synthetic summary probes verified all-early-alarm, all-miss, and all-detected cases. Empty eligible/detected groups return unavailable rates/delays. Counts partition the full condition, with delay conditional on eligible detections.
- The CLI bounds numerical-library threads. The revised run wrapper captures source/input evidence before execution, checks stability before publication, and requires committed source; implementation-specific provenance verification is also covered by the separate data/implementation reviewer.

The recorded check artifact initially showed a test-fixture error caused by attempting to mutate a read-only NumPy broadcast array. The author corrected the fixture with a copy; the later artifact inspected here reports 13 passing tests. That correction is distinct from the scoring defects above. The development trial records 1,488 rows for two customers in January 2013 and finite predictions; it establishes bounded pipeline execution, not final-study accuracy.

## Inspected SHA-256 hashes

These identify the inspected state before the pending scoring corrections. CO₂ origin labelling and the run-wrapper changes were reread during this inspection.

```text
07ca58309b36a5dc578667397750e0721b7358f3a5e1a2bee7fa9b4c8c2b27a8  src/tsatlas/co2.py
dc1e20ba556f92c056b9bf13f63676fdac31aa6a1eddcd7ef90bf34647cb1b2c  src/tsatlas/electricity.py
717177942041ff2cd6be3ef65edb4094f69b74de1199bffd933162c6ba5bc763  src/tsatlas/synthetic.py
a4ceb2ab208ca624f40e506db060c2520ef84366b38bdc3af51a7422f9a56ae8  src/tsatlas/metrics.py
20c2b1b2b1be74dade626c8b54d18f3db5691ec3e82b94416fa4bd73d65a1fd5  src/tsatlas/data.py
c73905fb7f8662835f15f0aa065dc1519bf8b46fc58a778ead12af6e4c47174b  src/tsatlas/common.py
2fed5022d7d69fb0878b3b932620883f98aab1edf581d91b4f20979ffeb34cd3  src/tsatlas/cli.py
bfdb1be484fbbda2939cebf152711041b89030e1ba56b415756a458890c4b71d  tests/test_forecasts.py
372ba374e5b26d9baefe1955a9568b6613cd68eb9c273c47f866f1077f147d08  tests/test_intake.py
2bb2c0a3a1d23808e8f4cbd1401e251739bff5db957da50d27c59f658f32fc1b  tests/test_metrics.py
3ff67ad1111c322719d03101ff70c06fd3a8cf6e4517947a2ff9c990bad52d11  reports/verification/checks.json
e09146c71f15f97114ad8fc57c5607b941e509055078a11db8f5ba2c184a9dd4  reports/verification/development-trial.json
```

This record concerns implementation correctness within the frozen tasks. It does not establish model skill, validate scientific conclusions, or constitute independent human review.

## 2026-10-30 — Independent resolution verification

**Updated verdict: M-STAT-01 and M-STAT-02 are corrected and independently verified; the statistical implementation gate is approved for the frozen first-release studies.** M-STAT-03's month-label clarification remains verified. Full runs must still start from committed source and satisfy the other required review perspective.

I reread the revised scoring functions and independently reran the previously failing miniature fixtures. Missing electricity predictions, duplicate hour/customer observations, incomplete customer panels, mismatched vector shapes, nonfinite interval endpoints, single-ended intervals, and reversed bounds now raise `ValueError`. The valid matched forecast fixture still returns MAE `1.0`, and a complete correctly predicted electricity panel still scores zero. No model fitting or final-score inspection was needed for this verification.

The updated recorded test artifact at `2026-10-30T16:29:18.438224+00:00` reports exit code zero and 16 passing tests. An independent digest comparison found all 14 recorded source-file hashes equal to the current files. The initial failing read-only test fixture was corrected separately; the new scoring regression tests cover the reproduced defects and correct aggregate cancellation.

I also reread the final run-wrapper change labeling memory usage as a process-lifetime peak. No changes to the declared model comparisons, splits, thresholds, or final evaluation choices were involved in these repairs.

Resolved-state hashes (other initially inspected algorithm files are unchanged):

```text
07ca58309b36a5dc578667397750e0721b7358f3a5e1a2bee7fa9b4c8c2b27a8  src/tsatlas/co2.py
32f7680163364a48010193d6957915a797df709541401effed394704064ad320  src/tsatlas/electricity.py
f0029cfbcee9a19df28294b40e39627fda31d7d5f4e5fc4b52e7068083c24931  src/tsatlas/metrics.py
1bdc4e6ce523986d004678f7ed876fae57a258f6ae9eebdace225e5aa6ea3c3a  src/tsatlas/common.py
e3c7a398b72e28aa1175eaa16e45702a73828205fbe402952320070c39fb88c5  tests/test_metrics.py
c3f3dc8097078a5c56d49fa2312e069da837bd17e9ca1c16a9bdd2dc783ebbd4  reports/verification/checks.json
```

This approval concerns implemented statistical mechanics and verified safeguards. Empirical conclusions and their presentation remain subject to the subsequent results and publication reviews.
