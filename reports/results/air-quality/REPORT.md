# Can other stations preserve indications during a sensor outage?

**Other-station medians outperform holding the last local reading on balanced
accuracy at all three tested durations.** Learned calibration produces almost
the same high/low warning score, while reducing concentration error. Its lower
false-positive rates can come with lower recall; those tradeoffs are shown
separately below. The near-overlapping network curves are a near tie, not a
missing method. A higher 72-hour score than 24-hour score is not evidence that
longer outages help: eligible blocks and evaluated hours differ.

This is a **same-hour nowcast under an explicit reporting assumption**. Other
stations must have delivered their readings. It is not a forecast of future
pollution. The tables separate scored performance, truth eligibility, and peer
data availability across the entire schedule. None is observed operational uptime.

![Outage performance and coverage](outage-warnings.png)

| Hours | Method | Balanced accuracy | Stations contributing | MAE (µg/m³) |
| --- | --- | --- | --- | --- |
| 6 | calendar | 0.500 | 12 | 85.3 |
| 6 | network_median | 0.938 | 12 | 13.2 |
| 6 | network_ridge | 0.938 | 12 | 12.8 |
| 6 | persistence | 0.836 | 12 | 24.7 |
| 24 | calendar | 0.500 | 12 | 73.6 |
| 24 | network_median | 0.846 | 12 | 20.4 |
| 24 | network_ridge | 0.846 | 12 | 19.0 |
| 24 | persistence | 0.754 | 12 | 46.8 |
| 72 | calendar | 0.500 | 12 | 85.2 |
| 72 | network_median | 0.887 | 12 | 27.9 |
| 72 | network_ridge | 0.886 | 12 | 25.0 |
| 72 | persistence | 0.645 | 12 | 86.1 |


The high-pollution cutoff is each station's training 90th percentile, with strict
exceedance. It is a research threshold, not a regulatory or health threshold.
Balanced accuracy gives sensitivity and specificity equal weight. A station
without both true classes contributes no balanced accuracy; its counts remain
in [station evidence](station-scores.csv). All methods use the same scoreable
hours in the primary table.

| Hours | Method | Pooled precision | Pooled recall | Pooled false-positive rate |
| --- | --- | --- | --- | --- |
| 6 | calendar | undefined | 0.000 | 0.000 |
| 6 | network_median | 0.821 | 0.911 | 0.044 |
| 6 | network_ridge | 0.831 | 0.911 | 0.041 |
| 6 | persistence | 1.000 | 0.658 | 0.000 |
| 24 | calendar | undefined | 0.000 | 0.000 |
| 24 | network_median | 0.764 | 0.746 | 0.042 |
| 24 | network_ridge | 0.797 | 0.723 | 0.034 |
| 24 | persistence | 0.774 | 0.545 | 0.029 |
| 72 | calendar | undefined | 0.000 | 0.000 |
| 72 | network_median | 0.786 | 0.834 | 0.061 |
| 72 | network_ridge | 0.811 | 0.829 | 0.052 |
| 72 | persistence | 0.691 | 0.337 | 0.041 |


## A pooled advantage is not a guarantee for each season or station

These are descriptive slices of the frozen experiment, already retained in
[quarterly evidence](quarter-scores.csv), not new tuning criteria. Entries are
macro station balanced accuracy; undefined means no station in that slice has
both true classes. High-hour counts use the same matched observations once,
not once per method. The test spans March 2016–February 2017, so calendar Q1
combines March 2016 with January–February 2017; it is not a continuous season.

| Hours | Calendar quarter | BA stations | High hours | Last reading | Calendar | Peer median | Network ridge |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6 | 1 | 12 | 72 | 1.000 | 0.500 | 1.000 | 1.000 |
| 6 | 2 | 9 | 44 | 0.722 | 0.500 | 0.946 | 0.943 |
| 6 | 3 | 0 | 0 | undefined | undefined | undefined | undefined |
| 6 | 4 | 9 | 30 | 0.500 | 0.500 | 0.811 | 0.839 |
| 24 | 1 | 12 | 271 | 0.860 | 0.500 | 0.853 | 0.868 |
| 24 | 2 | 8 | 84 | 0.643 | 0.500 | 0.949 | 0.933 |
| 24 | 3 | 0 | 0 | undefined | undefined | undefined | undefined |
| 24 | 4 | 12 | 122 | 0.500 | 0.500 | 0.729 | 0.763 |
| 72 | 1 | 12 | 989 | 0.674 | 0.500 | 0.879 | 0.880 |
| 72 | 2 | 4 | 45 | 0.591 | 0.500 | 0.930 | 0.924 |
| 72 | 3 | 10 | 32 | 0.500 | 0.500 | 0.808 | 0.759 |
| 72 | 4 | 12 | 557 | 0.500 | 0.500 | 0.834 | 0.836 |


At 24 hours in calendar Q1, peer median (0.853) slightly trails the last reading
(0.860), reversing their overall ranking. At 6 and 24 hours, Q3 has no observed
high hours in the scored blocks; balanced accuracy is undefined, not zero or
perfect. Those blocks still contribute other counts and error measurements.

The peer-median comparison also varies across stations:

| Hours | Peer median better | Tied | Worse | Comparable stations |
| --- | --- | --- | --- | --- |
| 6 | 9 | 0 | 3 | 12 |
| 24 | 11 | 0 | 1 | 12 |
| 72 | 12 | 0 | 0 | 12 |


At 6 hours it loses to persistence at 3 of 12 stations. These small scheduled
slices support neither a universal seasonal ranking nor a claim that each
station benefits. All station scores and support remain in the
[station evidence](station-scores.csv).

## Coverage changes the scope of the answer

| Hours | Eligible / scheduled blocks | Scoreable network / scheduled hours | Peer data available / scheduled hours |
| --- | --- | --- | --- |
| 6 | 133 / 144 | 798 / 864 | 864 / 864 |
| 24 | 129 / 144 | 3096 / 3456 | 3456 / 3456 |
| 72 | 106 / 144 | 7632 / 10368 | 10368 / 10368 |


The schedule fixes one outage at 09:00 on the first day of each month per station,
at three durations. Each scenario removes only that station. Complete local truth
and a preceding local reading are required to score an outage. Longer eligible
blocks can therefore represent a different cohort, and simulated missingness
need not resemble real failures. Natural missing observations have no known truth.
Network methods abstain when fewer than three other stations report.
Peer-input availability is counted even in blocks excluded for missing local
truth; scoreable network coverage additionally requires that truth. These are
different subsets of the same scheduled hours. Baseline
scores on all their available hours are [retained separately](available-hour-scores.csv).

## Event misses belong beside successful detection delay

| Hours | Method | Missed / high events | False-alert episodes | Median onset delay (hours) | Delay sample |
| --- | --- | --- | --- | --- | --- |
| 6 | calendar | 31 / 31 | 0 | undefined | 0 |
| 6 | network_median | 1 / 31 | 4 | 0.0 | 13 |
| 6 | network_ridge | 3 / 31 | 4 | 0.0 | 11 |
| 6 | persistence | 15 / 31 | 0 | undefined | 0 |
| 24 | calendar | 67 / 67 | 0 | undefined | 0 |
| 24 | network_median | 19 / 67 | 12 | 0.0 | 33 |
| 24 | network_ridge | 26 / 67 | 12 | 0.0 | 26 |
| 24 | persistence | 52 / 67 | 0 | 0.0 | 1 |
| 72 | calendar | 187 / 187 | 0 | undefined | 0 |
| 72 | network_median | 43 / 187 | 23 | 0.0 | 133 |
| 72 | network_ridge | 48 / 187 | 28 | 0.0 | 128 |
| 72 | persistence | 146 / 187 | 0 | 0.0 | 30 |


Delay describes detected, non-left-censored high runs only; missed events remain
in the table. Episodes are defined within blocks, not deduplicated pollution
incidents across stations or overlapping-duration scenarios. One sustained
prediction may overlap multiple high runs. The [event ledger](events.csv.gz)
retains censoring and event times so these denominators can be inspected.

A zero median delay means same-hour recognition among the detected, non-censored
events; it does not mean advance warning or that no events were missed. A zero
false-alert-episode count also need not mean zero false-positive hours: under
the frozen matching rule, a long alert run that overlaps any true high hour is
not a wholly false episode. The hourly false-positive rates remain essential.

Fit/calibration uses March 2013–February 2015. No local value inside an outage or
future endpoint enters a prediction. No real-gap recovery, future reporting
latency, health benefit, or robustness to correlated network failures is claimed.

[Design](../../../studies/air-quality/DESIGN.md) · [Story](../../../studies/air-quality/STORY.md) ·
[Source audit](../../intake/air-quality.json) · [Schedule](outages.csv) ·
[Predictions](predictions.csv.gz) · [Metrics](metrics.json) · [Run evidence](run.json).
Run `uv run atlas air-quality`. Data: Song Chen (2017), Beijing Multi-Site Air
Quality, UCI, CC BY 4.0; input is the twelve full station files.
