# Can changing growth improve CO₂ forecasts?

These are December-origin revised-data hindcasts. The primary comparison predicts December three years later, not an entire monthly trajectory.

![Forecast comparisons](forecast-comparison.png)

| Model | MAE ppm | Bias ppm | 80% coverage | Width ppm | Interval score |
| --- | --- | --- | --- | --- | --- |
| seasonal_naive | 7.548 | -7.548 | 0.0% | 2.828 | 14.493 |
| linear_expanding | 6.964 | -6.964 | 0.0% | 4.561 | 41.359 |
| linear_120months | 1.119 | -1.113 | 100.0% | 4.001 | 4.001 |
| quadratic_expanding | 1.606 | -1.606 | 100.0% | 4.584 | 4.584 |

There are 13 paired evaluation origins. Negative error differences in the right-hand plot favor the changing-growth model. The full origin-level differences are retained; overlapping three-year errors are not treated as independent samples.

Intervals use only pre-test calibration outcomes. Their nominal 80% label is a target, not a guarantee. Seasonal naive is a reference; the expanding linear model is the substantive baseline.

Source-quality exclusions, site-substitution target sensitivity, all calibration/test predictions, and metrics are retained. Site sensitivity removes affected **targets**, not all effects of changed-site observations used later in training. No causal explanation or real-time-vintage claim is made.

[Design](../../../studies/co2/DESIGN.md) · [Process story](../../../studies/co2/STORY.md) · [Metrics](metrics.json) · [Run evidence](run.json)
