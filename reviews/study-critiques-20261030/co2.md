# Fresh CO₂ study critique — 2026-10-30

Reviewer: `/root/critique_co2`, a non-authoring AI subagent. Scope: implementation,
findings, and presentation. I inspected the implementation, contract, source
header, saved results, and figure before consulting previous review conclusions.
This is additional automated scrutiny, not independent human validation.

## Scope and revision

- Parent-verified fresh `origin/main` and reviewed HEAD:
  `71999b34ccfd7127840b173efb287ac0a66b2a26`, fetched/verified at
  `2026-10-30T23:19:56.565503+00:00`; branch
  `review/study-critiques-20261030`. See [baseline record](baseline.json).
- Original retained CO₂ run source: `b607f9f410dec080388b84163f6ca073c6630607`;
  protocol: `b374e9baa39f021481aefaefba958543534c916f`. The current CO₂ model,
  scoring module, and design match their recorded run hashes. Subsequent shared
  data/run-wrapper changes add per-study input verification and configuration
  evidence; the CO₂ parser and forecast calculations are unchanged.
- No instrumentation patch, source edits, model retuning, full model rerun, or
  detached process. The only file written by this reviewer is this review.
- Inspected `src/tsatlas/co2.py`, the relevant data, metrics, common/CLI logic,
  forecast/intake/metric tests, design/story, source manifest and retained NOAA
  header, intake audit, all six files in `reports/results/co2/`, README, methods
  guide, and CO₂ claims/source references in `portfolio.json`.

## Separate verdicts

| Area | Verdict |
| --- | --- |
| Implementation | **No result-invalidating defect found in the inspected path.** The declared data mask, rolling origins, model windows, signed-error intervals, and scoring are implemented consistently. Saved evidence passes the checks below. |
| Findings | **The exact predictive comparison is supported; qualify its explanation.** The 6.964 → 1.119 ppm MAE reduction and 13/13 origin wins are correct. C01 identifies an unreported starting-level difference that prevents interpreting that entire improvement as better prediction of future growth. |
| Presentation | **Readable and bounded, with one substantive explanatory omission (C01).** The figure and table agree with retained results. Cross-panel model colors remain an already-recorded optional improvement, not a new publication blocker. |

No new leakage, target, split, or score blocker was established. The smallest
useful correction is a narrative qualification supported by the retained-data
diagnostic below. This review does not call for replacing or rerunning the
frozen experiment.

## C01 — Medium: separate starting-level fit from forecast growth in the explanation

Status: **identified**, newly documented interpretation limitation; numerical
results remain valid. Relevant locations:

- `src/tsatlas/co2.py:19–26`: both linear models freely fit an intercept, slope,
  and month indicators, then extrapolate the fitted level. Neither is anchored
  to the last observed December value. Shortening the window changes all these
  coefficients, not just growth.
- `studies/co2/DESIGN.md:3–6` and `:23–26`: the question and model labels emphasize
  changing growth versus an expanding fixed trend.
- `reports/results/co2/REPORT.md:1–5`, generated at `src/tsatlas/co2.py:81–83`:
  the headline reports the valid improvement but does not explain the large
  baseline error already present at issuance.
- `studies/co2/STORY.md:54–58`, `README.md:28`, and `portfolio.json:70` carry the
  comparison into the reader-facing lesson.

**Evidence.** For each of the 13 test December origins (2010–2022), select saved
`linear_expanding` and `linear_120months` predictions at horizons 12 and 36. Both
targets are December, so each linear regression's implied fitted value at the
origin is exactly:

```text
fitted_origin = (3 * prediction_12months - prediction_36months) / 2
origin_gap = observed_origin - fitted_origin
36month_signed_error = observed_target_36months - prediction_36months
growth_error = 36month_signed_error - origin_gap
```

The observed origin is the pinned file's `average` for that December. This is an
algebraic decomposition of retained predictions, not refitting or selecting a
new model. Positive gaps/errors below mean underprediction. Apply it only to
the two linear models, not to the quadratic model.

| Quantity, mean across the same 13 origins | Expanding linear | Trailing decade |
| --- | ---: | ---: |
| Observed minus fitted origin level, ppm | 4.602566 | 0.294360 |
| Predicted three-year increase from fitted origin, ppm | 5.187222 | 6.729760 |
| Observed three-year increase, ppm | 7.548462 | 7.548462 |
| Three-year growth underprediction, ppm | 2.361239 | 0.818702 |
| Total signed three-year underprediction, ppm | 6.963806 | 1.113062 |

The difference in origin gaps is 4.308206 ppm, or 73.6% of the 5.850744 ppm
difference in **mean signed** three-year errors. This is an arithmetic
decomposition, not a causal percentage or a decomposition of MAE. The recent
model slightly overpredicts at one origin, so its MAE (1.118816) differs from its
mean signed error. The recent model also estimates the subsequent increase more
accurately on average; the diagnostic does not overturn its observed advantage.

**Consequence.** The study compares complete forecasting procedures, which is a
valid question. It does not isolate the effect of adapting the future growth
rate while holding the starting level and seasonal fit constant. Much of the
dramatic headline gap is the expanding regression's inability to track the
already-observed level. The report's explicit absence of a causal explanation
does not itself explain this model-comparison limitation. An accessible study
should show readers why the ostensibly substantive baseline is already poor at
short horizons (its saved one-month MAE is 4.801 ppm).

**Smallest correction.** Preserve the frozen scores and comparison. Add a short
report/story qualification such as: “The trailing-decade fit improves both the
level at the forecast origin and the extrapolated growth rate. The all-history
linear fit was already about 4.60 ppm below the observed December level on
average, versus 0.29 ppm for the recent fit, so this comparison does not isolate
growth adaptation alone.” Retain “in this comparison” and the revised-data,
December-target qualifications wherever the headline is reused. A brief
diagnostic table or linked calculation can substantiate the explanation.

An origin-anchored drift baseline would be an **optional new, explicitly
post-hoc study**, not a required replacement, retuning exercise, or retroactive
addition to the frozen comparison. Do not silently relabel diagnostic scores
as preregistered evidence.

### C01 per-origin audit evidence

All quantities are ppm, rounded here to six decimals; use the calculation below
for full precision. The December 2022 origin is site-substitution affected under
the original inclusion policy. That is retained rather than silently changing
the population.

| Origin | Observed December ppm | Fixed origin gap | Recent origin gap | Fixed 36m error | Recent 36m error |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2010 | 389.990000 | 2.694876 | -0.165432 | 4.800829 | 0.716280 |
| 2011 | 392.060000 | 2.827390 | -0.020614 | 4.878650 | 0.933644 |
| 2012 | 394.570000 | 3.361769 | 0.507886 | 5.846999 | 1.983811 |
| 2013 | 397.030000 | 3.779378 | 0.665727 | 6.342406 | 2.117545 |
| 2014 | 399.080000 | 3.780198 | 0.467795 | 6.612789 | 2.157659 |
| 2015 | 402.060000 | 4.673829 | 1.091045 | 6.756412 | 1.949742 |
| 2016 | 404.640000 | 5.063562 | 0.907545 | 7.215115 | 1.551909 |
| 2017 | 407.000000 | 5.214126 | 0.546545 | 7.215622 | 0.797576 |
| 2018 | 409.270000 | 5.284156 | 0.246023 | 7.410121 | 0.518705 |
| 2019 | 411.970000 | 5.722463 | 0.274432 | 7.418661 | 0.008720 |
| 2020 | 414.230000 | 5.697235 | -0.184841 | 7.953392 | -0.037402 |
| 2021 | 416.670000 | 5.849015 | -0.250886 | 9.158008 | 0.966523 |
| 2022 | 418.990000 | 5.885368 | -0.258545 | 8.920472 | 0.805091 |

Reproduce the diagnostic from the repository root without fitting:

```python
import pandas as pd

p = pd.read_csv('reports/results/co2/predictions.csv.gz',
                parse_dates=['origin_month', 'target'])
raw = pd.read_csv('data/snapshots/co2_mm_mlo.txt', sep=r'\s+', comment='#',
                  header=None, names=['year', 'month', 'decimal', 'average',
                                      'deseasonalized', 'days', 'stdev', 'uncertainty'])
raw.index = pd.to_datetime(dict(year=raw.year, month=raw.month, day=1))
audit = {}
for model in ['linear_expanding', 'linear_120months']:
    g = p.loc[(p.split == 'test') & (p.model == model)]
    z = g.pivot(index='origin_month', columns='horizon', values='prediction')
    actual36 = g.loc[g.horizon == 36].set_index('origin_month').actual
    fitted_origin = (3*z[12] - z[36])/2
    gap = raw.loc[z.index, 'average'] - fitted_origin
    audit[model] = pd.DataFrame({
        'observed_origin': raw.loc[z.index, 'average'],
        'origin_gap': gap,
        'signed_error_36': actual36 - z[36],
        'growth_error': actual36 - z[36] - gap,
    })
    print(model, audit[model].to_string(), audit[model].mean(), sep='\n')
```

## Accepted limitations and optional improvements

1. **Known optional visual refinement, not a newly discovered blocker.** In
   `src/tsatlas/co2.py:68–75`, each subplot starts a fresh Matplotlib color cycle.
   In the inspected `forecast-comparison.png`, blue means seasonal naive on the
   left but trailing-decade regression on the right; orange means expanding
   linear on the left but expanding quadratic on the right. The two compared
   models are green/red on the left and blue/orange on the right. Legends make
   the values recoverable, but a fixed model-to-color mapping and the report's
   plain-language labels would reduce misreading. This was already explicitly
   optional in `reviews/first-release/results/general.md:138–140` and `:201–202`.
   The image has readable labels, units, and no visible clipping.
2. **Historical intervals have weak calibration evidence, honestly disclosed.**
   There are only 18 calibration origins per model/horizon, signed residual
   quantiles use linear interpolation, and the errors overlap at 36 months.
   Static historical calibration is not exchangeable with a changing-growth
   test period. The observed 0/13 and 13/13 coverage counts are correct; neither
   establishes calibrated operational coverage. Design `:42–45`, report `:16–18`,
   and story `:60–63` already limit the claim. No new interval defect found.
3. **Target and issue-time limitations remain explicit.** January is the
   one-month target; December is the 12/36-month target. The left plot is not a
   same-calendar-month error curve for every horizon. December origin labels
   denote the last available monthly value, not literal December 1 issuance.
   The retrospective snapshot cannot establish historical release availability.
   These were previously reviewed and are accurately disclosed.
4. **Source/provenance limits remain accepted.** The retained header describes
   processed monthly means and mixed site provenance. The two NOAA quality-
   suspect rows are excluded without compressing time; early Scripps unknown
   metadata are separate. Site sensitivity excludes affected targets only, not
   all training effects. It leaves 12 rather than 13 observations per horizon
   and preserves the substantive ordering. The actual primary sensitivity MAEs
   are 6.925901, 1.211324, and 1.662448 ppm for expanding linear, recent linear,
   and quadratic respectively.
5. **Optional explanatory visual.** A source-series or fitted-origin-gap panel
   could make C01 intuitive and show what the annual cycle means. Such a figure
   is useful for a hiring reader, but is not required to establish the already
   checked numerical comparison. No broader method catalogue is recommended.

After independent inspection I consulted the prior source/design,
implementation, and results reviews plus the completion publication reviews.
They already address source flags, revised vintages, target-month scope,
month-label semantics, finite scoring, small/overlapping samples, site-target
sensitivity, and the optional color issue. Those are not counted as new findings.
I did not find C01's starting-level decomposition in those CO₂ discussions.

## Checks actually run

- Read the relevant source paths and used `view_image` on the committed PNG.
- Independently enumerated the exact expected 372 model/origin/horizon keys:
  216 calibration rows (18 origins × 3 horizons × 4 models) and 156 test rows
  (13 × 3 × 4); no duplicated or missing keys, unexpected split labels,
  nonfinite values, or target-offset mismatch.
- Independently parsed the retained text file; all saved actuals equal its
  monthly-average field and all site flags equal the stated calendar interval.
  The quality mask excludes exactly December 1975 and April 1984 in the study
  range. All scored targets are usable. No post-2025 target is present.
- Confirmed the latest calibration target is December 2009, before the first
  test origin in December 2010. Recomputed every main and target-site-exclusion
  MAE, bias, coverage, width, and interval score using direct NumPy expressions,
  rather than the production scoring function. Maximum absolute difference
  from saved metrics: `6.616929226765933e-14`.
- Recomputed all model/horizon calibration quantiles and checked interval
  endpoints; recomputed the paired three-year differences and every associated
  mean/min/max/origin-win count. Both changing-growth procedures win all 13
  primary origins under the frozen comparison.
- Verified every output hash in the CO₂ run record, every recorded historical
  source hash against its Git blob, and the pinned CO₂ snapshot hash. Inspected
  the current-versus-run diff for the shared data/run code. No mismatch found.
- Ran `uv run pytest -q
  tests/test_forecasts.py::test_co2_recovers_linear_seasonality_and_ignores_future
  tests/test_intake.py::test_quality_flags_do_not_confuse_scripps_with_noaa
  tests/test_metrics.py`: **7 passed in 1.54 s**.
- Ran a bounded synthetic fixture for all four predictors: changing future
  values, quality-excluded values, and the unused deseasonalized column left
  predictions unchanged. Seasonal naive correctly fell back to the previous
  usable same-calendar-month observation when the latest December was masked.
- Ran the C01 algebraic diagnostic and retained its per-origin results above.
  Exploratory arithmetic also shifted saved forecasts by their implied origin
  gaps; no fitted anchored-baseline experiment, selection, or retuning was
  performed. This review makes no claim that a proposed repair would win.

Untested here: no full analysis replay, external provider refresh, historical
vintage reconstruction, larger calibration experiment, alternative-method
benchmark, browser rendering, or deployed portfolio inspection. Prior replay
records were consulted as historical evidence, not presented as a new replay by
this reviewer. All commands were bounded and session-managed; no process remains.

## Selected inspected SHA-256 hashes

```text
6a652546f1a67f658e99cfc5808c341505b83a3f04bdac1082468c99cec98c0a  src/tsatlas/co2.py
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
95a699e75a84da2651dc70268c942232abb62c7cdbd75f6e0454dc14788d3468  src/tsatlas/common.py
f0029cfbcee9a19df28294b40e39627fda31d7d5f4e5fc4b52e7068083c24931  src/tsatlas/metrics.py
d070a91da04b8fee7d4c37e20f8160e6444a649a9551d3a198da62a4d2cb3fb3  studies/co2/DESIGN.md
902861f217c542630204a72d9b5a544fc7a9e7ef39824bd2c0b328e64468ba8a  studies/co2/STORY.md
0ce4e7749217b4af2cca8e0bdf263856ad59b0a2946d4e98c7b22ccfbff21cad  data/snapshots/co2_mm_mlo.txt
0529ea280461ce3e002cb89abc27f6d32e1d794aaaf5302791621b4db927f682  reports/results/co2/REPORT.md
36e0cef9a2e517645a44fb78de94bfddf716342a5f031ed4f897b68764c2deb9  reports/results/co2/metrics.json
c51c73977e13304a8106e37f5afd419ebf40bf940561e9e6cce47d2f72d63826  reports/results/co2/run.json
b056a41321a6a1fac51abbdf6b20f7bfc1d9b755151fa0a7bd663f1827d8016f  reports/results/co2/paired-error-differences.csv.gz
90d3993ef871868520c3ef127960fea235431ac872640224397394db9b8eadaa  reports/results/co2/predictions.csv.gz
d75ced7a440c5dfb50e4ac926ba464651169ed6f3bf1455f06b8712409ed5b68  reports/results/co2/forecast-comparison.png
```
