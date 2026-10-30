# Air-quality result evidence review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: the first full air-quality run, source
`89f0031ba2f232a84ba8639a53e32c2a0fea1487`, with predictions, outage schedule,
coverage, fitted parameters, classification scores and event ledgers.
The reviewer authored no implementation and refitted no model. Checks used
independent calculations from pinned inputs and saved parameters.

**Artifact and numerical verdict: pass. Publication remains pending the
final narrative/rendering updates and clean-checkout reproduction.** No new
model, split, score, or event-count defect was found.

## Provenance, schedule, and prediction reconstruction

All **33 recorded source hashes** match historical Git blobs at the source
commit; all **ten output hashes** and the pinned snapshot hash match current
bytes. The protocol commit is `715ac6c89b1948609c67626c883a4cc63ec3abde`.
The run records stable committed source, approximately 2.39 seconds elapsed,
and 267 MB process-lifetime peak RSS. These describe this execution, not a
portable performance benchmark.

The reviewer independently reconstructed the exact Cartesian schedule of
12 stations, 12 monthly starts at 09:00, and three durations: **432 blocks**.
All half-open endpoints, prior-reading checks, target-truth checks, exclusion
reasons, and peer-availability counts match. **368 blocks** are eligible;
all **64 exclusions** are due to missing target truth. No excluded block has
prediction rows. No retained block/hour/model key is duplicated.

For each station, the training-only 90th percentile, training eligibility count,
feature means and population scales agree with the pinned source. Using those
inputs, saved Ridge coefficients/intercepts, directly recomputed training
calendar medians, and each block's last preceding local reading reproduced
**all 46,104 prediction rows**, including raw predictions, clipped predictions,
targets, availability, and thresholds. This was a direct arithmetic
reconstruction, not another call to the authored forecast functions or a fit.
Twenty raw Ridge predictions were negative and are correctly retained beside
their zero-clipped values.

The earlier report phrase “different denominators” is corrected in this run
to “different subsets of the same scheduled hours.” This closes the minor
presentation observation in the [implementation review](air-quality-implementation-data.md).

## Coverage, rates, and events

At durations 6/24/72 hours, eligible blocks are **133/129/106 out of 144**;
scoreable hours are **798/3,096/7,632**. At least three peers report during every
scheduled hour, including the excluded blocks. Thus peer-input coverage is
100% on this fixed schedule, while scoreable coverage is about 92.4%/89.6%/73.6%.
No empirical network abstention occurs here. The missing-peer behavior was
tested with fixtures, but these results do not demonstrate robustness to
correlated failures or sparse peer reporting. The available-hour and common-hour
score files are consequently identical, correctly reflecting this actual cohort.

The reviewer recomputed every station, available-hour, and quarterly confusion
count, rate, balanced accuracy, and MAE, then all primary macro scores and pooled
rates. All expected group keys are present without duplicates. Counts match
exactly; numeric values match within `rtol=1e-11, atol=1e-11`; undefined rates
remain missing/null. The primary macro has all 12 contributing stations for
each model/duration in this realized dataset, which does not remove the need
for the implementation's absent-class handling elsewhere.

An independent loop over consecutive truth/alert runs reconstructed all
**1,223 event-ledger rows**, including exact times, misses, censoring, delay,
and false-episode definitions. Every event aggregate agrees. There are
31/67/187 true block-local high runs by duration, repeated for each method.
Counts must not be summed across nested scenarios or stations as unique
pollution incidents. Zero median delay concerns detected non-left-censored
events only; missed events and the delay sample are retained alongside it.

## Presentation and claims

The figure was visually inspected. Labels and coverage categories are readable;
the two network accuracy curves nearly coincide, with Ridge covering the median
curve. The numerical tables retain the distinction. Network methods outperform
the calendar/persistence baselines on the declared aggregate discrimination
measure, while Ridge adds little balanced accuracy over the simple network
median in this dataset. Ridge's lower MAE is a separate observation. The
72-hour accuracy increase over 24 hours should not be interpreted as an effect
of longer outages: eligibility changes the cohort, as the report states.

The report correctly calls this a same-hour nowcast under assumed peer-report
availability, preserves a relative research threshold, and avoids operational
uptime, advance-warning, health-benefit, natural-gap recovery, or correlated
failure claims. UCI source attribution and CC BY 4.0 are present.

Minor publication correction: the event table currently displays Python `None`
for absent delay estimates. Render a reader-facing label such as “undefined”
or “no detected non-censored events”; retain the zero sample count and JSON null.
Append the actual implementation corrections and result/coverage interpretation
to the process story rather than rewriting planning history. A concise result
sentence should distinguish the benefit of contemporaneous peers from the
small additional discrimination benefit of fitted Ridge.

## Remaining verification

This review checks the current evidence and prediction arithmetic without
refitting. It does not claim a clean-checkout rerun or final site publication.
Those remain the parent's final reproduction/publication checkpoints. Any
renderer refresh must keep the numerical artifacts unchanged or be reviewed
as a substantive change, with updated run evidence.

## Inspected hashes

```text
d5d2e37bfa3cdd3f47d8b07302f54c39fd7913473e242b0e8636eca9cb7fda4b  reports/results/air-quality/run.json
06bb7d366a2f9b6efbf94d03f292661f571c61a13ba9d709bd23ca311c387664  reports/results/air-quality/REPORT.md
21c4e8fbe9c6804cd15628fa023d2e3633f0c1eeebb9b040c1d89a5860497ffd  reports/results/air-quality/metrics.json
e04843cb83cc6e81274d05ed0c0abab7102a931b07d2f60b0c30b5920372bf01  reports/results/air-quality/predictions.csv.gz
1e90e651ffee8219cd7ec176c06bf8833dda9972da2b0f74f2e69d6d13fbac14  reports/results/air-quality/events.csv.gz
66479107f6c560c17321da6a3bad46b4dd8bd4fcb78a8c11387e0f34cf57affe  reports/results/air-quality/outages.csv
c5d5bf97101dcb31042369133f83da76f8a785a104b9d4023132f0ed942d36ad  reports/results/air-quality/parameters.json
c0fe245ef25a72d39aea2a8729fbc14139b95e3e790cbddfc2d8551ee5740ea0  reports/results/air-quality/outage-warnings.png
734e21cddbee577d55e8d6ac470b26fd6bae262144d12ae4785d3163a31a498a  studies/air-quality/STORY.md
7494522604d213a82e8d8d8bcf9a9c5c94a683067a306ff9999458f2380561ae  src/tsatlas/air_quality.py
```
