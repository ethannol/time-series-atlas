# River-flow indications: study contract

Draft for independent source/design review. No forecast models have run.

## Question and boundary

How much warning of high flow can recent rainfall and flow provide across
different catchments? Compare a flow-only model to the same model with recent
rainfall and temperature, at target dates one and three days after the last
observed day. Separately measure newly starting high-flow events: predicting
continued high water is easier than warning before a rise. This is an idealized
daily research forecast, not an operational flood-warning or damage model.

## Sources, cohort, time and availability

CAMELS-US time series version 1.2, DOI10.5065/D6MW2F4D, official Zenodo deposit
15529996, CC BY4.0. Use observed USGS streamflow and basin-mean Daymet forcing,
not model output. Range acquisition verifies each selected ZIP member's CRC and
SHA256; it does not independently verify the provider's entire 3.4GB archive MD5.
The manifest retains member paths, trials, metadata and checksums.

Take the first gauge by ID in each HUC02 region with at least95% approved,
nonnegative flow in1980–1999. This deterministic source-only rule selected17
regions; no gauge from HUC09 qualified. Retain the failed training-coverage
candidates in the acquisition manifest. Never use final-period completeness or
forecast skill to choose replacements. This is a geographically spread,
nonrandom known-gauge panel, not an ungauged-river transfer experiment.

Retain a continuous1980–2014 calendar per gauge. Flow is cfs; only QC exactlyA
and nonnegative observations are allowed as inputs and truth. Missing sentinel
-999, M, absent rows and estimated A:e remain distinct in the audit. Precipitation
is mm/day, temperatures°C. Address columns by their header names: snow-water
equivalent is not maximum temperature. The forcing's Hr12 field is not evidence
of noon availability. Assume completed day d's approved flow and retrospective
weather are available at the start of d+1. Predict flow status on d+h, h=1 or3;
the horizons are date offsets, not guaranteed24/72-hour operational warning.
No target-day or intervening future weather, flow-derived static attributes,
full-record hydrological signatures, or outside forecasting feeds are allowed.

## Frozen split, models and calibration

Training target dates1980–1999; calibration target dates2000–2004; test target
dates2005–2014. Input history may cross a split boundary but every input must be
at or before its origin d. Define high flow as strictly greater than the training
90th percentile of approved daily flow, pandas linear quantile. Train separate
models per gauge and horizon, no test-based tuning or refitting.

Use three score models: persistence score = latest flow / training threshold;
logistic flow-only; logistic flow+weather. Flow features: log1p latest flow,
log1p flow at d-1 and d-2, log1p mean of last7 days, and annual sine/cosine at d.
Weather adds log1p precipitation on d, sum of last3 and last7 days, and mean
temperature of last7 days. All7 flow days must be approved/nonnegative; weather
must be finite with precipitation nonnegative. All models are evaluated on that
same information-valid cohort with approved target truth. Standardize using
training features only; LogisticRegression C1,max_iter1000,no class weights.
Save convergence warnings and counts, never silently exclude a failed model.

For each gauge/horizon/model, fix the alert cutoff to the90th percentile of its
calibration scores on non-high target days. Strictly exceed the cutoff to alert;
ties remain no-alert. This budgets approximately10% false-positive days in
calibration, not a guaranteed future budget. If either training class or
calibration negatives are absent, report that gauge/model as unevaluable, do
not choose a new gauge or threshold from test outcomes.

## Scores, events and variation

Primary: macro gauge high-day recall at the frozen alert cutoffs, accompanied
inseparably by test false-positive rate, precision, confusion counts and coverage.
Logistic models also receive Brier scores; persistence is an uncalibrated score
and is not scored as a probability. Provide per-gauge/horizon rows and pooled
counts. Rates with zero denominator are null and excluded from the relevant
macro with the contributing-gauge count. No naive daily significance claim.

An onset is a high target day preceded by an approved non-high calendar day.
An onset is eligible at horizon h only if origin d and all intervening approved
observed days are non-high; this separates warning before onset from high-flow
persistence. Record all high runs, event starts, censored starts after missing
truth, eligible onsets, alerted onsets and misses. Count runs of alerting target
days with no overlap with actual high days as false-alert episodes; unknown
truth splits runs and cannot prove a false alert. All event ledgers show horizon,
origin and target date; no within-day timing or damage claim.

Show results by gauge and by metadata area (<100,100–1000,>1000km²). Additionally
report a training-only cold-precipitation fraction: sum precip on days with mean
temperature<0 divided by all training precipitation. Group <0.1 versus>=0.1 as
a climate proxy, not observed snowmelt. These groups are descriptive comparisons,
not causal explanations. Do not use full-record CAMELS climate indices.

## Reproduction and gates

Source manifest `data/manifests/river-flow.json`, audit `reports/intake/river-flow.json`,
compact snapshot `river-daily-panel.csv.gz`. Preserve dated scores, targets,
thresholds, event ledgers, exclusions, coefficients, source and protocol commits.
Source/design and implementation reviews precede full runs; results/publication
reviews must challenge the warning and cross-catchment interpretations.
