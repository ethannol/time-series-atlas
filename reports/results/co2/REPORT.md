# Can changing growth improve CO₂ forecasts?

The recent-growth model reduced three-year mean absolute error from 6.964 ppm for expanding fixed growth to 1.119 ppm in this comparison. Both changing-growth specifications improved on fixed growth at every evaluated three-year origin.

These are December-origin revised-data hindcasts. The primary comparison predicts December three years later, not an entire monthly trajectory.

![Forecast comparisons](forecast-comparison.png)

| Model | MAE ppm | Bias ppm | 80% coverage | Width ppm | Interval score |
| --- | --- | --- | --- | --- | --- |
| Repeat last same month | 7.548 | -7.548 | 0.0% | 2.828 | 14.493 |
| Fixed growth, all history | 6.964 | -6.964 | 0.0% | 4.561 | 41.359 |
| Recent growth, trailing decade | 1.119 | -1.113 | 100.0% | 4.001 | 4.001 |
| Quadratic growth, all history | 1.606 | -1.606 | 100.0% | 4.584 | 4.584 |

There are 13 paired evaluation origins. Negative error differences in the right-hand plot favor the changing-growth model. The full origin-level differences are retained; overlapping three-year errors are not treated as independent samples.

Intervals use only pre-test calibration outcomes. Their nominal 80% label is a target, not a guarantee. Seasonal naive is a reference; the expanding linear model is the substantive baseline.

Source-quality exclusions, site-substitution target sensitivity, all calibration/test predictions, and metrics are retained. Site sensitivity removes affected **targets**, not all effects of changed-site observations used later in training. No causal explanation or real-time-vintage claim is made.

[Design](../../../studies/co2/DESIGN.md) · [Process story](../../../studies/co2/STORY.md) · [Metrics](metrics.json) · [Run evidence](run.json)
