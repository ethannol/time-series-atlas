# Choose the question before the method

The collection covers seven real datasets and one synthetic investigation with
two controls. Each data type makes a different analytical mistake tempting.
The linked reports show evaluated comparisons; there is no shared leaderboard
across forecasting, classification, reconstruction, detection and frequency estimation.

| Data and distinctive quality | Compelling question | Methods actually evaluated | Evaluation choice that matters | Evidence |
| --- | --- | --- | --- | --- |
| Monthly CO₂: long growth trend, annual cycle, revised/filled values and changing site provenance | Does adapting the growth estimate improve multiyear forecasts? | Seasonal naive, linear seasonal regression with expanding/recent windows, quadratic trend, calibrated residual intervals | December origins, separate selection/test periods, quality sensitivity; historical revised data | [Report](../reports/results/co2/REPORT.md) |
| Electricity: many customers with different scales and shared calendar patterns | Who benefits or suffers when coefficients are shared across customers? | Yesterday, last week, local ridge, pooled ridge | Select customers before test year; score people and summed load separately; explicit clock convention | [Report](../reports/results/electricity/REPORT.md) |
| Retail: transaction events, long zero stretches, sheet overlap and returns | What is a useful next-week sales forecast when most product-weeks have little activity? | Zero, last week, 28-day rate, Croston-SBA, TSB | Gross recorded sales, training-only cohort, macro normalized and raw unit error plus total volume | [Report](../reports/results/retail/REPORT.md) |
| Oil: irregular observed dates, negative levels and changing fluctuation size | Can volatility be predicted better even when direction cannot? | Fixed/rolling variance, EWMA, GARCH; prevalence versus logistic direction | Next-observation dollar changes; train-only fitting; QLIKE and Brier answer different questions | [Report](../reports/results/oil/REPORT.md) |
| River flow: catchment differences, quality flags and persistent events | Does predicting high water also provide warning before a new rise? | Persistence, flow-only logistic, flow-plus-past-weather logistic | Origin-safe calibration; no future weather; event onset, censoring and false-alert episodes | [Report](../reports/results/river-flow/REPORT.md) |
| Air quality: spatial peers, missing truth and contiguous station outages | Can neighboring stations preserve a useful local high-pollution indication during an outage? | Last reading, training calendar median, same-hour network median, ridge calibration | Same-hour nowcast, full-block observed truth for scoring, separate peer availability and scoring coverage | [Report](../reports/results/air-quality/REPORT.md) |
| ECG: rapid waveforms, rare beat groups, person dependence and recording artifacts | Does annotated-beat recognition transfer to people absent from training? | Majority, class-mean templates, training-only PCA with logistic regression or random forest | Person-disjoint folds, label-independent training caps, per-class/person support; expert beat centers given | [Report](../reports/results/ecg/REPORT.md) |
| Synthetic changes: known onset and controllable serial dependence | How quickly can a change be detected without too many false alerts? | Shewhart and CUSUM, frozen IID-calibrated thresholds | Separate calibration; AR(1) stress; early alarms, misses and conditional delay together | [Detection report](../reports/results/synthetic/REPORT.md) |
| Synthetic sampling: known physical frequency and timestamps | Is a clear spectral peak uniquely identifiable from this sampling schedule? | Deliberately naive index FFT, interpolation plus FFT, floating-mean Lomb–Scargle | Fixed realizations, full alias-family grid, ambiguity alongside frequency recovery | [Frequency report](../reports/results/spectral/REPORT.md) |

The retail example is especially useful for decision framing: an always-zero
forecast can win a median-oriented error score while missing every recorded sale.
That does not make the score wrong; it makes the intended decision indispensable.
The ECG and river examples similarly expose what an attractive aggregate number
leaves unanswered. Read the [process stories](../STORY.md) and
[review evidence](../reviews/README.md) for when these questions were asked and
which defects were actually found.

Bayesian, neural/pretrained, hierarchical reconciliation, ungauged-catchment
transfer, oil cointegration and an automatic ECG detector are **not evaluated**.
They were conditional extensions, not hidden accomplishments. No extra method
is needed to make an unconvincing result look successful.

[Dataset credits, transformations and public reproduction limits](../data/README.md).
