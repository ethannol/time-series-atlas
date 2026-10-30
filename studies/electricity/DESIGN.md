# Electricity analysis contract — frozen before fitting

Question: when does learning across customers improve tomorrow's load forecast,
and who benefits or suffers? Models must be compared on the same customers,
inputs, origins, and horizons. This is a historical benchmark, not measured
procurement savings, a production system, or new-customer transfer.

## Target, population, availability

Target: 24 hourly mean-power readings (kW) for the next nominal provider-clock
day. Assume quarter-hour timestamps label interval ends, subtract 15 minutes,
and average four values per start-labelled hour. This assumption matches file
boundaries; provider does not explicitly define endpoints. Do not convert to UTC
or claim energy-settlement accuracy. Assume the complete previous nominal day
is available at midnight; actual reporting latency is unknown.

Use the pinned 24-customer panel selected solely from 2011/2012. Eligibility and
rank selection are in data/README.md and intake audit. The panel spans scale and
contains established, mostly active customers; conclusions do not generalize to
all 370 clients, new clients, or an unknown business segment. Customers are anonymous.

DST: flag entire last-Sunday-of-March/October days. Primary evaluation excludes
these dates and the following 14 days, so target and lagged inputs do not touch
an affected day. Training also excludes these rows. Secondary scores include
these dates with the same fitted models to show sensitivity, clearly labelled.
Zeros elsewhere are retained; no use of future activation or last-positive dates.

## Fixed comparisons

Baselines: yesterday's same hour and last week's same hour.
Matched learned models: Ridge regression fitted separately to each customer,
and Ridge fitted on all customers with shared coefficients. Normalize each
customer by its mean power over the current training window; denormalize to kW.
The pooled model adds customer intercept indicators. Both use identical numeric
features: normalized same-hour lags 24, 168, 336; normalized previous-day mean;
cyclic hour-of-day, day-of-week, and month terms. These are all known at the
midnight origin. Use a fixed mean-loss ridge penalty lambda=.001, implemented as
Ridge alpha=.001 * n_training_rows for each fit, so local and pooled models
have the same penalty per observation. No tuning. Describe pooling as shared
coefficients/regularization, not a controlled isolation of every architectural
choice. Do not interpret coefficients causally. Clip learned forecasts at zero
for physical consistency, apply the same policy to local and pooled predictions,
and retain raw forecasts plus clipping counts.

Training window: preceding 365 days, excluding invalid-history rows. Refit on the
first day of each month; never use any current-month target for that month's fit.
Scale estimates use training observations only. Test predictions use newly observed
lags as days progress, without monthly model re-estimation. No intervals in this
first bounded comparison: interval methods require a separately reviewed extension.

Development year: 2013, for inspecting pipeline behavior; frozen main evaluation:
2014. No hyperparameter selection is planned. Record development results separately
and do not alter final-study choices without an explicit amendment. Fit 12 times
per year per model; bounded linear models should run on one CPU thread.

## Metrics and outputs

Save hourly predictions by customer/model/origin. Report per-customer MAE in kW,
macro mean of customer MAE divided by each customer's fixed 2012 mean kW, signed
bias, and aggregate-load MAE (sum predictions and actuals BEFORE absolute error).
Compare local/pooled paired customer errors; report winner counts and full client
scatter, not IID significance. Primary endpoint: macro normalized MAE in 2014 on
safe dates. Secondary: aggregated load and MAE during hours whose actual load exceeds
the fixed per-customer 2012 90th-percentile threshold (not necessarily 10% of
evaluation hours). Count observations excluded.

The normalized score is a scale-normalized MAE, not MASE. Zero/near-zero means
are rejected by cohort/scaling checks. No claim that this nonrandom panel estimates
a population effect. Save monthly coefficients/scales/configuration and run metadata.

Complete source/design reviews and commit before fitting. Keep any full-sample
source audit distinct from selection or tuning: no future outcome-informed choices.
