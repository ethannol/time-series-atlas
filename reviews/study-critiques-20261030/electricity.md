# Electricity — fresh implementation, findings, and presentation critique

Reviewer: `/root/critique_electricity`, a non-authoring AI agent. Date: 2026-10-30.
This is an independent agent critique, not independent human validation.

## Scope and revision

Reviewed the electricity implementation, shared source adapter/run machinery,
relevant tests, frozen design, process story, intake audit, all retained electricity
results, README, methods table, and electricity claims in `portfolio.json`.
Inspected source and formed an initial assessment before reading earlier review
conclusions. Later compared the assessment with the first-release statistical and
general reviews to distinguish existing qualifications and corrected findings.

- Fresh review baseline: `71999b34ccfd7127840b173efb287ac0a66b2a26`.
- Parent's fetch verification: `2026-10-30T23:19:56.565503+00:00`, recorded in
  [baseline.json](baseline.json); independently confirmed `origin/main` matches.
- Reviewed branch: `review/study-critiques-20261030`.
- Historical results source: `b607f9f410dec080388b84163f6ca073c6630607`;
  protocol commit: `b374e9baa39f021481aefaefba958543534c916f`.
- Instrumentation patch: none. No implementation, design, result, or data edits.
  Only this review was written. No model fitting, retuning, or full run.
- All checks ran locally with numerical-library concurrency limited to one thread;
  the session-managed check process exited. No browser or unrelated process used.

The electricity algorithm and design are unchanged from the historical run.
Inspected intervening changes to the shared adapter/run machinery: they extend
input verification and provenance to the other studies, without changing the
electricity transformation or model specification.

## Three verdicts

| Dimension | Verdict | Basis |
| --- | --- | --- |
| Implementation | Accepted for the declared historical comparison | Saved predictions reconstruct from saved monthly parameters; feature timing, training cutoffs, scales, DST masking, and scoring are consistent with the contract. No new implementation defect affecting these results found. |
| Findings | Supported within the stated scope | Independent recomputation reproduces customer, aggregate, and peak scores, winner counts, and sensitivity ordering. The comparison does not identify a universal or causal effect of pooling. |
| Presentation | Publishable with optional refinements | The report states its answer and limits clearly; the figure identifies every customer and shows exact small differences. Magnitude and concentration context could strengthen the portfolio summary without changing conclusions. |

No newly identified mandatory correction or publication blocker. The suggestions
below are optional and must not be read as a requirement to alter the frozen
comparison after observing its scores.

## Checks and observed evidence

### Timing, units, selection, and model implementation

1. `src/tsatlas/electricity.py:18–26` constructs same-hour lags 24, 168, and 336
   hours plus the complete previous-day mean and calendar features. Every source
   observation precedes that target day's midnight under the explicitly assumed
   reporting availability (`studies/electricity/DESIGN.md:10–15`). Predicting later
   days with newly observed lags is valid for the daily-origin task; it is not a
   month-ahead forecast from the month's first day.
2. Independently reconstructed all 24 monthly training masks, training counts,
   last training timestamps, and all 576 customer scales. All targets precede the
   model's month; each scale exactly matches the saved value. The common mean-loss
   ridge penalty and the extra pooled customer indicators match the design
   (`src/tsatlas/electricity.py:35–68`). The architecture qualification is explicit
   at `studies/electricity/DESIGN.md:34–41`.
3. Independently generated last-Sunday transition dates and their following 14-day
   exclusion windows. The saved flags agree for every prediction. Primary 2014
   scores exclude 30 nominal days: 17,280 of 210,240 customer-hour rows, leaving
   8,040 hours per customer. The conservative continuous window is wider than the
   precise set of lag-touching dates, as the contract explicitly specifies.
4. The input is the complete 35,064-hour nominal grid for 2011–2014 with 24 selected
   columns. Every selected customer has some positive 2011 consumption and 366
   positive-total days in 2012; selected 2012 means range from 6.950642 to
   21,091.615437 kW. Reviewed `cohort` at `src/tsatlas/data.py:88–99` and the existing
   future-perturbation test; neither eligibility nor rank selection uses 2013/2014.
5. Rechecked the [UCI provider documentation](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014):
   it describes quarter-hour values in kW, nominal Portuguese labels, fixed daily
   record counts, and special DST encoding. Thus averaging four values is the
   declared hourly power transformation; summing them would change the units.
   The provider does not settle the interval-end assumption. Independently
   transformed the first 96 raw records and matched the selected first-day hourly
   snapshot within `1.82e-12` kW. All 24 selected customers have nonzero hourly
   values around the 2014 spring transition, consistent with the documented reason
   for using calendar flags rather than an all-customer-zero detector.

### Saved predictions and numerical results

Reconstructed every saved prediction using independently assembled lag/calendar
inputs and matrix multiplication of the saved coefficients. No `Ridge.fit`, study
`run`, or full intake was called. The 420,480 rows form a unique complete
hour/customer panel for 2013 and 2014. Actuals and both naive forecasts match the
snapshot exactly. Maximum absolute reconstruction differences are `7.28e-12` kW
for separate regression and `1.82e-11` kW for shared regression. Clipped predictions
match their raw counterparts under the specified policy; both years have zero
negative raw predictions for either learned model.

Independently calculated customer MAE, normalized MAE, bias, peak denominators and
MAE, macro averages, and aggregate-before-error MAE/bias for both years and both
date masks. Maximum difference from any recorded numeric score was `4.55e-13`.

| 2014 primary model | Macro normalized MAE | Aggregate MAE, kW | Aggregate bias, kW |
| --- | ---: | ---: | ---: |
| Yesterday | 0.111749460 | 1522.172346 | -7.247671 |
| Last week | 0.128308478 | 1792.054792 | -20.181061 |
| Separate regression | 0.098315015 | 1355.696136 | 10.342798 |
| Shared regression | 0.102140372 | 1384.389500 | 20.416882 |

The saved comparison gives three numerical gains and 21 losses. The gain IDs are
MT_166, MT_210, and MT_302 on primary dates, versus MT_166, MT_198, and MT_210 on all
dates. The report correctly distinguishes the unchanged overall ranking from the
changed identity of one nearly tied customer. The primary normalized difference
averages `0.003825356`; its median is `0.000884816`. These are descriptive outcomes,
not evidence of 21 statistically established or economically important harms.

Verified every output hash in `run.json`, every historical source-file hash against
its Git blob, the electricity snapshot hash, and the original archive hash. This
checks artifact provenance; it is not a new end-to-end reproduction of fitting.

### Tests and visual inspection

Seven existing targeted, no-fit tests passed in 1.43 seconds:

- Target-day feature future-perturbation and longest-lag DST coverage.
- End-label hourly transformation, cohort future-independence, and calendar DST
  identification independent of zeros.
- Missing-prediction/duplicate rejection and aggregate-before-absolute-error
  scoring.

Inspected `reports/results/electricity/pooling-comparison.png` visually at its
1920×1280 output resolution. Customer labels and signed differences are legible;
the sign convention and normalized-error axis are explicit. The aggregate panel
uses kW and a zero baseline. The accompanying table supplies precise aggregate
values. The current delta plot resolves the earlier unlabelled-scatter criticism;
that is not a new open finding. The report and story also already limit the tiny
gains, cohort representativeness, and all-date sensitivity interpretation.

## Optional improvements, ranked by usefulness

### O1 — Give the headline count an effect-size companion

Priority: low; optional presentation improvement.
Locations: `portfolio.json:51–55,70`, `README.md:29`, and
`reports/results/electricity/REPORT.md:16–20`.

The count of 21 worsened customers is correct, but the portfolio headline presents
the sign count without a magnitude. Shared regression raises macro normalized MAE
by **3.89% relative to separate regression** and aggregate MAE by **2.12%**. Add one
of those comparisons beside the count, preserving the fixed-panel qualification.
This helps a hiring reader assess practical scale without interpreting the count
as statistical certainty or measured business harm. The linked report already
shows the underlying table and small individual differences, so this is not an
unsupported-results finding.

### O2 — Explain the distinct concentration of customer and aggregate outcomes

Priority: low; optional interpretation context.
Locations: `reports/results/electricity/REPORT.md:3–20`,
`src/tsatlas/electricity.py:124–136`, and
`reports/results/electricity/customer-comparison.csv.gz` (MT_156/MT_187 rows).

The two largest normalized losses, MT_156 and MT_187, contribute **68.57% of the
net sum of customer normalized-error increases**. Separately, MT_196 supplies
**67.15% of actual total load** on primary dates. A short sentence can explain why
the equal-customer and total-load summaries answer differently weighted questions.
The current aggregate calculation is correct; do not replace it, remove the
largest customer, or claim the load-share statistic itself proves error dominance.

### O3 — Surface the already-computed high-load endpoint for readers

Priority: low; optional presentation improvement.
Locations: `studies/electricity/DESIGN.md:58–65`,
`reports/results/electricity/REPORT.md:22`, and
`reports/results/electricity/metrics.json` (`test.primary.*.customers.*.peak_*`).

The prespecified high-load secondary scores are retained and numerically correct,
but the prose only defines their threshold. A compact linked human-readable table
could make that endpoint easier to inspect than nested JSON. Preserve each
customer's peak count and the fixed 2012 threshold definition; do not average
incompatible denominators into an unexplained new headline or select a favorable
subset after inspection.

## Accepted limitations and extensions

- **Availability and physical time:** complete prior-day reporting at midnight is
  assumed; actual latency is unknown. End-labelled nominal intervals and the DST
  mask do not recover UTC or energy-settlement truth. Already disclosed; not a new
  observed source defect or a reason to claim operational readiness.
- **Scope of pooling:** shared slopes plus regularized customer indicators differ
  from independently fitted slopes and intercepts. The equal mean-loss penalty
  does not isolate every architectural choice. The design explicitly says so,
  and the report's conclusion is confined to these specified procedures.
- **Population and weighting:** 24 preselected established customers spanning scale
  do not estimate a random-customer population effect or cold-start transfer.
  Training-scale normalization and fixed-2012 scoring normalization are different
  declared choices, not leakage. The latter is not MASE or percentage error.
- **Evidence strength:** one held-out year, dependent daily errors, and tiny sign
  changes do not establish uncertain future rankings. No significance or interval
  guarantee is asserted. The simple yesterday/last-week baselines are relevant to
  the stated matched regression comparison; more sophisticated baselines,
  hierarchical pooling, weather/holiday inputs, or block-based uncertainty would
  require a separately reviewed extension, not retrospective retuning.
- **Publication history:** the earlier missing-prediction score bug was corrected
  before these results; current invariants and saved completeness support that
  distinction. Earlier reviews also raised the model-structure qualification and
  small-gain readability. Those are disclosed or verified corrections, not newly
  rediscovered blockers.

## Untested areas

Did not refit any model, rerun the full study, rederive all 370 customers' ranks
from the entire raw archive, or repeat full raw intake. Raw-byte identity, a
bounded raw transformation, selected-customer eligibility, adapter logic, and the
saved 24-customer evidence were checked. Did not measure production reporting
latency, recover physical-time DST readings, estimate uncertainty, inspect an
external deployed portfolio rendering, or infer customer business segments.

## Inspected SHA-256 identifiers

```text
bff038460bc7cba8996c999b22a327101d9252ed123be5054071af3946a5b43f  src/tsatlas/electricity.py
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
95a699e75a84da2651dc70268c942232abb62c7cdbd75f6e0454dc14788d3468  src/tsatlas/common.py
d7739838ec65fd59b196385deab8f5da94767bfd1ad29255bae8222758a8c5a5  studies/electricity/DESIGN.md
5b4310e708b854ce1180af3bc00524fde47a059a128ee56159e5d231ddd2413f  studies/electricity/STORY.md
2b44293c453ecd008e8c7cf76e87a3f38a592afdd14870cb54b408309b020198  reports/intake/audit.json
f6c4d0e0df12ecdb9ea008dd6eef3518adb52c559d04a9bac2e1b81dcfc8d4e1  data/raw/electricity.zip
2283fe9e8c2fdcdf4c9544267c34dcf2671efd8ebabc754201b87fb7f414d6fc  data/snapshots/electricity-hourly-panel.csv.gz
34ddc6041e119e23be8a2b31d60121e1fab1c57a11036ca4cf01d29a4fbadf1f  reports/results/electricity/REPORT.md
114034594c046b771f5d9b3386e0ce6315332551103096b84cc4aa35023f979b  reports/results/electricity/customer-comparison.csv.gz
eea0c9d198bbbedd09910f407b41bf74ddac16e13e32eb450c870226cd0ab0db  reports/results/electricity/metrics.json
86e69932a5f36660cf85e5b304827111cc501cf4149cf4f28935359d4b463729  reports/results/electricity/parameters.json
c4369754e5402e7f18b8592b27c7b22d5d5be5eedf81bd552d4439028e4454d2  reports/results/electricity/pooling-comparison.png
d5d006d4ab30f8971290845ece0068bbae075eda9c03c03d1d76238f672c1a09  reports/results/electricity/predictions.csv.gz
43a55431f786690ecd605ea71cd4d42e7a4aff821a38168b56672853405f0204  reports/results/electricity/run.json
1dc152d9288c02ca5f99ce8d801b409391ada1ed1d0a0f86e5c3ce0da6654650  README.md
9dc9066c3810b15df1cfb2750b1cce0059917c200a063dd7aab176ad31f0b0bc  portfolio.json
```
