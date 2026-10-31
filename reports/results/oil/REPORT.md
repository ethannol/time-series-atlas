# Can uncertainty be forecast when direction is difficult?

**In this comparison, adaptive variance forecasts improve the declared QLIKE
score for both markets, while logistic direction forecasts perform worse than
the training-prevalence baseline on Brier score.** The fixed variance instead
has the lowest absolute error against squared price changes. A model ranking
depends on the quantity and loss being evaluated; these results do not establish
profitable trading or calibrated financial risk limits.

Variance and direction require separate comparisons. Negative values in the
chart mean improvement over that task's simple baseline; the two panels have
different units and must not be compared in magnitude. Every setting was fixed
before evaluating 2015–2025.

![Separate variance and direction scores](risk-and-direction.png)

| Market | Variance model | QLIKE | Squared-change MAE |
| --- | --- | --- | --- |
| brent | ewma | 1.7101 | 2.828 |
| brent | fixed | 2.0155 | 2.787 |
| brent | garch | 1.7074 | 2.855 |
| brent | rolling_60 | 1.7773 | 2.940 |
| wti | ewma | 1.8586 | 6.182 |
| wti | fixed | 2.6779 | 4.779 |
| wti | garch | 1.8533 | 6.160 |
| wti | rolling_60 | 1.9480 | 6.391 |


| Market | Direction model | Brier | Accuracy |
| --- | --- | --- | --- |
| brent | logistic | 0.2514 | 0.509 |
| brent | prevalence | 0.2498 | 0.515 |
| wti | logistic | 0.2511 | 0.514 |
| wti | prevalence | 0.2495 | 0.521 |


## What was actually forecast

The target is the next **observed** dollar price change for each market, not a
fixed calendar-day return. Weekend and source gaps are not filled with zeros.
The negative WTI observation remains in the experiment; ordinary log returns
would not be defined there. Variance forecasts update from previous changes;
GARCH parameters and the direction model were fitted on 2000–2014 only.

Squared dollar changes are a noisy volatility proxy. QLIKE scores expected
variance differently from absolute proxy error; inspect both. The [annual and
gap breakdown](variance-subgroups.csv) includes a predeclared 2020 stress-period
comparison. The [direction years](direction-years.csv) show how conclusions vary
through time. A lower score does not demonstrate profitable trading, calibrated
tail-risk limits or measured business savings. The [direction gap breakdown](direction-gaps.csv)
also separates short observation gaps from longer ones.
Historical data are revised and
reporting latency is unknown.

GARCH's QLIKE is only slightly lower than the simple EWMA in both markets. That
small difference does not, by itself, justify the additional fitting machinery.
Absolute error against squared changes rewards their conditional median; QLIKE
targets conditional variance under the stated zero-mean change model. Neither
criterion is a universal measure of usefulness.

## Source access is part of reproducibility

EIA identifies Refinitiv as the underlying spot-price source. Free access does
not establish permission to mirror the complete price history. We retain inputs
and true-change evidence locally, publish original forecasts and aggregate scores,
and pin the exact normalized historical-input hash. **This is a source-file
distribution boundary, not a guarantee that derived outcomes are unrecoverable.**
Consecutive published EWMA variance forecasts reveal nearly every test squared
change: `change[t]² = (variance[t+1] − 0.94 × variance[t]) / 0.06`.
GARCH forecasts and their published coefficients similarly expose squared
changes. This does not recover their signs or the complete signed price history.
[The fresh critique](../../../reviews/study-critiques-20261030/oil.md) documents
the reconstruction. Keeping those already-public analytical artifacts is an
explicit publication choice; this disclosure makes no claim of unrestricted
third-party reuse or a demonstrated licence violation.

`uv run atlas fetch oil`
can use a newer workbook only if normalization through 2025 reproduces that hash.
Historical revisions may make exact public reproduction unavailable; the command
fails explicitly rather than silently changing the experiment.

Reproduce locally with `uv run atlas fetch oil` then `uv run atlas oil`.
[Design](../../../studies/oil/DESIGN.md) · [Story](../../../studies/oil/STORY.md) ·
[Audit](../../intake/oil.json) · [Metrics](metrics.json) · [Parameters](parameters.json) ·
[Variance predictions](variance-predictions.csv.gz) · [Direction predictions](direction-predictions.csv.gz) · [Run evidence](run.json).
Source: EIA spot-price workbooks released October 28, 2026, underlying source
Refinitiv; figures, model forecasts and summaries are this project's analysis.
