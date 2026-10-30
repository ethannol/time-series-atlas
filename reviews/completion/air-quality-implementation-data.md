# Air-quality pre-run implementation review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: air-quality implementation, binary/event utilities, frozen design,
source snapshot/audit linkage, and bounded development-period invariant checks.
No final-period predictions or comparative accuracy scores were computed by the
reviewer, who authored no implementation code.

**Pre-run verdict: pass from the implementation perspective.** The implementation
honors the declared information and scoring boundaries. Commit the reviewed
source and satisfy the separate statistical gate before the full study. This
does not approve eventual results, interpretations, or publication evidence.

## Data and outage boundaries

The previously independently verified twelve-station PM2.5 snapshot and its
preserved natural missingness remain the only input. Training stops at
2015-02-28 23:00. Threshold quantiles, calendar medians/fallback, network
calibration, and standardization use that training interval only. Network
features explicitly drop the target station and require at least three other
reporting stations during both fitting and prediction.

The fixed schedule creates 12 monthly starts for each of 12 stations and three
durations. Each scenario uses its own target station; it does not remove all
stations simultaneously. The half-open interval, complete local truth, and
strictly preceding 24-hour reading requirement match the contract. Every
scheduled block receives an eligibility/exclusion record. Persistence uses the
last preceding reading; calendar and network predictions cannot consume local
values inside the outage or its later endpoint. Negative Ridge predictions
are clipped to zero while their raw values remain in the prediction evidence.

The reviewer independently checked that changing all data after the training
cutoff leaves fitted coefficients, feature means, threshold, fallback, and
training-row count unchanged. For the development example Aotizhongxin,
2015-03-01 09:00, six hours, the current source produced 24 finite prediction
rows. Mutating all hidden local and later values left predictions unchanged.
No final-period predictions or scores were involved.

Additional temporary in-memory fixtures verified that fewer than three other
readings causes both network methods to abstain while calendar/persistence
remain available, and that missing local truth and missing preceding readings
produce their respective block exclusions. Real snapshot bytes were untouched.

## Denominators, coverage, and event evidence

Primary comparisons use the common network-available hours. Station balanced
accuracy is defined only when both actual classes occur; undefined values stay
null and the macro reports its contributing-station count. Confusion counts
remain available. The separate available-hour scores retain baseline evidence
outside that common subset. Coverage records both eligible/scheduled blocks and
network hours relative to eligible and scheduled hours, so successful estimates
cannot conceal excluded or unavailable scope. Quarterly summaries are descriptive.

Event rows are constructed on complete eligible blocks, including unavailable
network hours, rather than after filtering to common hours. Abstention breaks
alert runs and can cause a missed true event. Non-left-censored detected events
alone contribute delay, with misses and censoring retained separately. False
episodes require no overlap with a true high hour. The block-local definition
correctly permits one sustained prediction to overlap several true runs and
does not claim unique real incidents across nested durations or stations.

An independent six-hour event fixture confirmed a one-hour onset delay, a
separate missed right-censored event, an abstention break, and one false episode.
The report template explains the selection/availability assumptions and does
not present the relative training quantile as a health or regulatory cutoff.

## Executed checks and limits

The reviewer ran `pytest -q tests/test_air_quality.py`: **4 passed**. The tests
cover hidden-target independence, absent-class denominators, half-open outage
boundaries and future-endpoint independence, and event misses/censoring/delay.
Four NumPy/pandas timedelta deprecation warnings were emitted; execution in the
locked runtime succeeded. The independent probes above passed with unchanged
source SHA-256 before and after execution. No additional blocker was found.

The author's finite-only development trial names the same inspected source
revision. This bounded execution evidence does not establish forecast quality.
Full-result review must still independently reconstruct the actual schedule,
coverage, metrics, and events from retained predictions and verify run hashes;
fresh-checkout reproduction is also outstanding at this gate.

## Inspected hashes

```text
1138c840274f0e5404176336560aa4ac2efbcf405c54bbfce796405d3389c306  src/tsatlas/air_quality.py
36a342dd2c23a9826d25a478a7a85028c70e6f93395f7e7befc3571de580fd6a  src/tsatlas/classification.py
73225b68863e0b8fab496ade572744dc9b6098a04253fb264a7a30a3cce2ad2b  tests/test_air_quality.py
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
aefd807b20f4bff6ab06a5beb9e0d7c68fdb0e74d6c9e227ccd900664a642494  data/manifests/air-quality.json
6c6eb61a5d4ef68ef2a187395b803de674c34abe7149beb672bf1950a02f02bd  reports/intake/air-quality.json
1728af0edf50039ca234a58803f75bcc5e121c51b0fc9bef2c3d298f19a20fc5  data/snapshots/air-quality-hourly.csv.gz
940af75e51501e090f8df8e5e3108439b0a087b784b2e8e06a46ce2d9eb6237f  reports/verification/air-quality-development-trial.json
```

## 2026-10-30 — All-schedule peer-availability correction verified

The statistical reviewer identified that the earlier coverage implementation
counted available peer hours only inside scoreable blocks. The initial review
above accepted its scoreable/scheduled coverage but did not identify the missing
all-schedule availability measure. These are distinct questions: peer data can
exist even when missing local truth prevents scoring.

The corrected outage function computes peer availability before any eligibility
return and records `peer_available_hours` for every scheduled block. Metrics
separately retain all-schedule peer input availability and scoreable network
hours; the figure and report label both alongside truth eligibility. Predictions
and model settings are unchanged. Pooled precision, recall and false-positive
rate are also exposed directly from the already retained confusion counts.

The reviewer reran the four focused tests: **4 passed**, with six existing
timedelta deprecation warnings. An independent fixture made a six-hour block
unscoreable by deleting local truth while leaving only five peer-available
hours. The ledger retained five; restoring local truth made those same five
hours scoreable. This verifies the required distinction without final-period
evaluation or a new model fit.

**Pre-run implementation pass stands.** One presentation correction remains:
the template's phrase “different denominators” is inaccurate for the two
scheduled-hour fractions, which share a denominator but count different subsets.
The author has been asked to correct that sentence before publication. The
previous finite-only trial is for the earlier source hash; this follow-up's
tests/probe specifically cover the changed ledger behavior.

```text
f553a836e2eae2be550f72a6397a1c7ce2057b6e5f2a45a0a1ae2400c8f8c851  src/tsatlas/air_quality.py
f9be97008368484c68bed34dcb86530cbe8b1bd3e8620d03b1e0cff913add8a9  tests/test_air_quality.py
```
