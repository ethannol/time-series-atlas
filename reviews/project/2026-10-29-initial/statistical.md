# Initial statistical critique

Reviewer: `statistical_critic`, a separate AI subagent.
Date: 2026-10-29.
Scope: the proposed datasets, methods, evaluation, and questions, before implementation.
Record: the substantive initial review below is reproduced verbatim from the reviewer's final response to the primary agent. This is an automated design critique, not an empirical result or independent human validation.

---

The dataset selection is sound. The main weakness is that the plan names many methods before fixing the questions, information available at prediction time, and evaluation rules. Keep all seven datasets, but make each study answer one primary question; treat other methods as supporting comparisons.

**Must fix before implementation**

1. **Separate forecasting, retrospective reconstruction, and online detection.**  
   A centered smoother, STL decomposition, or Kalman smoother may legitimately use later observations when reconstructing history. It must not feed a forecasting or real-time detection model. Create an explicit task declaration for each run: target, prediction time, horizon, available variables, split unit, and metric. Label observed-future-weather CAMELS results as retrospective conditional prediction, not operational forecasting.

2. **Freeze a complete evaluation design, not just a final holdout.**  
   Use rolling-origin validation for model selection, then a final temporal evaluation period with the selection process frozen. All imputers, scalers, feature selection, seasonal estimates, tuning, and uncertainty calibration belong inside training windows. Compare models at identical origins and horizons. For pooled models, distinguish “future observations for known customers/catchments” from “new customer/catchment”; these require different splits. Report variation across origins and series rather than a universal winner. The standard forecasting reference explicitly distinguishes training residuals from forecast errors and describes rolling-origin evaluation. [Forecasting: Principles and Practice](https://otexts.com/fpp3/toolbox.html)

3. **CAMELS has a specific hidden leakage route.**  
   Its attribute tables contain discharge-derived hydrological signatures, including mean flow and baseflow index. Those cannot be treated as ordinary static predictors in a genuinely ungauged-catchment experiment. Physical geology/soil/topography descriptors are appropriate; target-derived summaries must be recomputed from allowed training history and excluded when no flow history is allowed. The provider describes how these signatures were derived. [NCAR CAMELS attributes](https://ncar.github.io/hydrology/datasets/CAMELS_attributes)

4. **Retail needs a precise target and a metric that respects sparsity.**  
   Keep cancellations/returns separate from positive observed sales. Define the active-product cohort using training information; never use the eventual last sale to decide whether a product was active earlier. Two years of observations do not support strong claims about annual seasonality. Compare weekly totals and explicitly chosen lead-time sums, alongside zero and simple-rate baselines. MAE alone can favor an always-zero forecast when zeros dominate. Add signed bias, aggregate error, and a count-distribution or quantile score. Since stockouts and inventory are absent, replenishment costs or savings can only be hypothetical scenarios.

5. **Uncertainty needs more than interval coverage.**  
   Report coverage **and** width/proper interval score by horizon and relevant regimes; extremely wide intervals can achieve high coverage without being useful. Use temporal blocks and/or series-level summaries for uncertainty in model comparisons rather than treating overlapping forecast errors as independent observations. For zero-heavy series, avoid MAPE; define what happens when a scaled-error denominator is zero. Detection evaluation needs event-level false alarms, missed events, and detection delay—not only pointwise accuracy.

6. **Revise the ECG claims to reflect the recording process.**  
   Patient separation is essential: records 201 and 202 belong to the same person. The data also deliberately enrich rare arrhythmias, so dataset performance does not establish deployment prevalence or clinical usefulness. Most concretely, PhysioNet documents tape artifacts—including a prominent 0.167 Hz component—and warns about heart-rate-variability analysis. Retain ECG for beat detection, morphology/classification, and artifact-aware signal analysis. Use the synthetic lab as the primary demonstration of irregular-sampling spectral recovery. [PhysioNet recording and selection notes](https://physionet.org/physiobank/database/html/mitdbdir/intro.htm)

**Revised questions and evidence**

| Study | Primary question | Evidence that would answer it |
|---|---|---|
| CO₂ | How far ahead does explicitly modeling trend and seasonality improve prediction over simple extrapolation? | Errors and interval scores at fixed monthly horizons, with full-history decomposition clearly separated from forecast inputs. |
| Electricity | When do calendar patterns and information shared across customers improve next-day load forecasts? | Same-origin comparisons against daily/weekly seasonal baselines; individual and aggregate accuracy; performance across customer scales. |
| CAMELS | How much does recent rainfall and flow improve high-flow prediction, and does the relationship transfer to new catchments? | Temporal evaluation plus a distinct held-out-catchment experiment; forecast availability declared; peak/threshold evaluation alongside overall error. |
| Oil | Is volatility more predictable than the direction of daily price changes? | Random-walk/constant-volatility baselines, out-of-sample variance scores and interval behavior, with breaks examined rather than presumed. |
| Retail | Which methods predict next-week sales for products with frequent zero-sales days? | Weekly product totals, aggregate bias, performance by training-defined sparsity, explicit treatment of cancellations and product entry. |
| Air quality | Can recent weather and nearby stations improve short-horizon pollution predictions when measurements are missing? | Forecast errors and threshold-event performance; missing-block experiments compared with genuine data gaps, separately labeled. |
| ECG | How reliably can beat detection and classification transfer to different people? | Patient-disjoint evaluation, event-matching tolerance fixed in advance, per-class and per-patient results, documented signal artifacts. |

These questions are naturally useful without forcing a business framing. Electricity and retail support operational decisions; CO₂ and ECG support scientific understanding. Actual savings, optimal inventory, prevented damages, and clinical benefit remain outside what these data establish.

**Dataset-specific adjustments**

- **CO₂:** Use the measured monthly series, not an already deseasonalized/smoothed product as model input. Audit provider interpolation flags. Annotate the temporary observing-site change: NOAA says observations from December 2022 through July 4, 2023 came from Maunakea. Don’t automatically interpret a detected break there as a climate change. [NOAA record notes](https://gml.noaa.gov/ccgg/trends/index.html)
- **Electricity:** Treat preactivation zeros and daylight-saving modifications according to provider documentation. A timezone conversion cannot recover information already aggregated by the publisher. Preserve a quality mask and show sensitivity to those periods.
- **Oil:** Predefine level/difference/return transformations and handling of nonpositive prices. Cointegration is a hypothesis to investigate with break sensitivity, not an expected result.
- **Air quality:** Randomly hiding isolated points is too easy and differs from station outages. Include contiguous missing blocks and station-wide missingness. Do not score naturally missing values against invented truth.

**Optional, later work**

- Add forecast reconciliation after the underlying customer forecasts are credible.
- Add neural/pretrained comparisons only with a fixed compute/tuning budget. Public historical datasets may overlap pretrained-model training data; document known or unknown contamination.
- Use multiple synthetic mechanisms, including ones poorly matched to the tested models, so recovery results are not merely demonstrations that a model recovers its own assumptions.
- Keep causal/intervention analysis out of the headline claims unless a defensible intervention design is added.

I would preserve CO₂ and electricity as the first release, but require the task declarations and evaluation machinery before adding more model families.
