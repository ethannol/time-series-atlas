# Synthetic change detection contract — frozen before fitting

Question: how quickly can a sustained increase be detected without frequent false
alarms? This is a known-truth control, not evidence of field performance.

Generate 200 calibration no-change Gaussian streams and a disjoint 200 evaluation
replicates per condition, each length 400. First 100 points estimate baseline
mean/std; monitoring begins at index 100. Seed 20261030 calibration; 20261031
independent evaluation. At index 200 impose a fixed additive mean shift of 1.0 (one true marginal standard deviation), or no shift. Evaluate both IID noise and stationary AR(1) noise rho=.6 with
unit marginal variance. Draw x[0] ~ N(0,1), then x[t]=.6*x[t-1]+sqrt(1-.6²)*epsilon[t]
for AR noise; add the level shift after generating the stationary noise. AR cases deliberately violate IID calibration assumptions.

Estimate baseline standard deviation with ddof=1. Standardize subsequent readings
using only the first 100 observations. Shewhart score at t is z[t]. CUSUM initializes S[99]=0 and updates from t=100: S[t]=max(0,S[t-1]+z[t]-.5). Alarm when score is
strictly greater than its threshold.
Calibrate each threshold separately using the 95th percentile (higher quantile)
of its maximum score over complete calibration monitoring windows. Freeze thresholds
before evaluation. Calibrate under IID only, then reuse in AR stress tests.

Online scores use only baseline and present/past observations. First alarm wins;
no reset or repeated trial after a false alarm. Report probability of any alert in
no-change streams; probability of prechange false alert; postchange detection rate
among streams without a prechange alert; misses; and median delay among detected
eligible streams. Always report denominators and misses alongside conditional delay.
For changed streams, partition all 200 runs into prechange alarms (<200),
postchange detections (>=200), and no alarms. Eligible count = 200 minus
prechange alarms; detection rate = postchange detections / eligible; misses =
no alarms / eligible. Delay is alarm index minus 200 conditional on detection.
No-change false-alarm rate uses all 200 no-change streams.
Persist replicate outcomes and calibrated thresholds. No universal winner or
real-world false-alarm guarantee. Pre-run review and protocol commit required.
