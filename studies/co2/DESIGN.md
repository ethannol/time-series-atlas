# CO₂ analysis contract — frozen before fitting

Question: does allowing growth rate to change improve multiyear forecasts over
an expanding fixed linear trend plus an annual cycle? A finding of no reliable
improvement is valid. This is revised-data hindcasting, not historical real-time
forecast reconstruction or causal attribution.

## Observations and exclusions

Use pinned monthly average (ppm), May 1974–December 2025. Exclude NOAA-era rows
with negative stdev OR uncertainty from model fitting and scoring; retain their
time positions rather than compressing time. The source header and actual values
differ, so call these quality-suspect, not definitively interpolated. Early Scripps
rows are outside scope, not labelled interpolation. Mark December 2022–July 2023
as site-substitution affected, include in main measured-data evaluation, and
report sensitivity excluding affected target months. No deseasonalized column
enters any model. Retrospective plots are labelled accordingly.

## Comparisons and time splits

No hyperparameter search. Four prespecified models:

1. Seasonal naive: latest usable same-calendar-month observation, no growth.
2. Expanding linear trend plus 11 month indicators (the substantive fixed-growth baseline).
3. Trailing 120-month linear trend plus the same month indicators (adapting growth).
4. Expanding quadratic trend plus the same month indicators (changing growth).

All regression fits use only usable observations through the December origin.
Calendar time is numeric in years; center it at each origin for conditioning.
Keep month gaps in the time axis. Seasonal naive is a reference, not the sole
baseline a flexible model must beat.

Generate annual December origins 1989–2022, horizons 1, 12, 36 months.
These are December-origin forecasts only: January targets at horizon 1, December
targets at horizons 12/36. They do not evaluate all-month trajectories.
Calibration origins: 1989–2006 only, so all calibration targets end by December
2009. Test origins: 2010–2022, with targets no later than December 2025.
2007–2009 origins are unused. All choices are fixed before fitting. Predictions
may use earlier test-period observations once those are in the past, but interval
calibration remains frozen before the first test origin.

For each model/horizon, empirical 80% prediction intervals use the 10th/90th
percentiles of signed calibration forecast errors (linear quantiles). This is a
small historical calibration sample with no claimed distribution-free coverage.
No forecast interval uses the final evaluation errors for calibration.

## Evidence

Persist each origin/model/horizon/target/prediction/interval/actual/quality flag.
Report MAE and signed bias in ppm, 80% coverage, interval width and interval score
(alpha .2), plus paired absolute-error differences against expanding linear by
origin. Show their spread without IID p-values or confidence intervals over
heavily overlapping multiyear forecasts. Primary comparison: 36-month horizon;
1 and 12 months are secondary. Include sensitivity excluding substituted-site
targets. Do not label a model a universal winner from a small number of origins.

Complete source/design reviews and commit this contract before fitting. A changed
question, split, model, or metric requires a dated amendment stating whether
results were already inspected.
