# Air-quality results and publication review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Run source: `89f0031ba2f232a84ba8639a53e32c2a0fea1487`.

**Results verdict: approved.** Independent source-to-output checks reproduce
predictions, classification scores, coverage and event ledgers. **Publication
verdict:** existing numbers and stated limitations are supported; finish the
plain-language answer/current story and the presentation clarifications below.
Full reproduction remains pending. No model was refitted or retuned.

## Independently verified evidence

All result files match the run's output hashes. The saved evidence contains
**432 scheduled blocks** and **46,104 prediction rows**. Every eligible station/
start/duration/hour has the same four methods and one shared target, with no
duplicate model keys. Every saved target equals the actual source concentration;
natural missing values were not imputed into truth.

For every scheduled block, the reviewer independently reconstructed its half-open
hour grid, preceding-24-hour local history, truth eligibility and other-station
report count. Saved thresholds match the local training 90th percentile with
linear interpolation. Every persistence, calendar and network-median prediction
was recomputed directly from the source. Every ridge raw/clipped prediction was
recomputed from the saved coefficients/scaler and permitted same-hour peer inputs.
All match. This is evaluation of saved parameters, not fitting a new model.

All per-station, available-hour and quarterly confusion counts, precision,
recall, false-positive rates, balanced accuracies and MAEs reproduce. Primary
macro scores reproduce by explicitly averaging station scores, and pooled rates
reproduce from pooled counts. All 12 stations contribute a defined BA for each
duration in the primary comparison. Undefined rates remain missing rather than
being reported as perfect recognition.

An independent consecutive-run implementation reconstructed **all 1,223 saved
event rows**, including event boundaries, left/right censoring, detections,
conditional delays and false-alert episodes. Every event-summary count and
conditional median matches. Quarterly/episode analyses preserve the declared
dependent nature of overlapping durations; they are not independent samples.

## What the results support

| Outage duration | Peer median macro BA | Persistence macro BA | Ridge macro BA |
|---|---:|---:|---:|
| 6 hours | 0.93842 | 0.83572 | 0.93804 |
| 24 hours | 0.84596 | 0.75351 | 0.84630 |
| 72 hours | 0.88665 | 0.64513 | 0.88596 |

Other stations' same-hour median improves on carrying forward the last local
reading at all three durations in this scheduled experiment. Ridge and the
simple median have nearly identical primary balanced accuracy; ridge has lower
concentration MAE at all three durations. Those are distinct endpoints. These
averages do not establish statistical significance, health benefit, prospective
pollution forecasting or a universal network-model ranking.

The 72-hour network BA exceeding the 24-hour BA does **not** mean longer outages
make the task easier. The complete-truth restriction changes the eligible block
cohort and the added hours change the mix of pollution states. The report already
identifies that population change; retain it beside any duration comparison.

## Coverage: missing truth is the limiting factor here

Independent schedule checks reproduce:

| Duration | Eligible / scheduled blocks | Scored network / scheduled hours | Peer-available / scheduled hours |
|---|---:|---:|---:|
| 6 hours | 133 / 144 | 798 / 864 | 864 / 864 |
| 24 hours | 129 / 144 | 3,096 / 3,456 | 3,456 / 3,456 |
| 72 hours | 106 / 144 | 7,632 / 10,368 | 10,368 / 10,368 |

All exclusions are missing local target truth: 11, 15 and 38 blocks respectively.
No otherwise truth-complete block lacks the required prior local reading. Every
scheduled hour has at least three observed peers, including hours in excluded
blocks. Thus the network abstention path was tested by fixtures but **not
empirically exercised by this final schedule**. Available-hour and common-hour
score files are correctly identical for this run.

The corrected coverage display makes this distinction visible. Its 100% peer
input availability is a property of selected archived observations under the
timely-report assumption; it is not measured operational uptime or evidence
about correlated station failures. Complete-block eligibility restricts what can
be said about real sensor outages and natural gaps.

## Events: keep misses beside the zero median delays

For peer median, missed/high-event counts are **1/31**, **19/67**, and **43/187**
at 6, 24 and 72 hours. Conditional delay samples are only **13**, **33**, and
**133**, after excluding left-censored runs and undetected events. Their zero
median delay means same-hour recognition among those detected eligible runs;
it is not advance warning, a guarantee of instant detection, or a description
of missed events. Reporting delay without the misses would change its meaning.

Persistence records zero false-alert **episodes**, while its hourly false-positive
rate is nonzero at 24 and 72 hours. This is consistent with the frozen rule:
a long constant alert run overlapping any true high hour is not counted as a
wholly false episode, even if many of its hours are false positives. It can also
overlap several true runs. The metric is a block-local overlap summary, not a
complete accounting of alarm burden or unique operational notifications.
Keep the hourly counts/rates and this limitation; do not redefine episodes after
seeing the outcome to obtain a preferred ranking.

## Publication follow-ups

**AP01 — Complete the answer and process story.** The report currently explains
how to read valid tables but should state the bounded result directly: peer
information beats persistence in this experiment, while ridge adds little BA
over the peer median. Note the tradeoff with concentration MAE. The story still
says “design only”; update its current status and add dated intake, review and
first-results entries, preserving historical plans. Report full reproduction as
pending until verified.

**AP02 — Make conditional event/plot displays unambiguous.** Label median onset
delay in **hours**, render undefined delay as “undefined” or an em dash instead
of Python `None`, and retain misses/sample counts. The two network BA curves
visually overlap almost completely; a short explicit statement or distinct line/
marker styles should make clear that both curves are present and nearly tied.
Add the persistence episode-versus-hour distinction above when discussing event
results. These are presentation clarifications, not model changes.

The figure was visually inspected and otherwise matches the numeric evidence,
including the separate eligibility and peer-input coverage bars. No unsupported
clinical/regulatory threshold or recovered natural-gap claim appears in the
current report. Overall Atlas completion claims are outside this scoped review.

## Inspected SHA-256 identities

```text
06bb7d366a2f9b6efbf94d03f292661f571c61a13ba9d709bd23ca311c387664  reports/results/air-quality/REPORT.md
21c4e8fbe9c6804cd15628fa023d2e3633f0c1eeebb9b040c1d89a5860497ffd  reports/results/air-quality/metrics.json
d5d2e37bfa3cdd3f47d8b07302f54c39fd7913473e242b0e8636eca9cb7fda4b  reports/results/air-quality/run.json
c5d5bf97101dcb31042369133f83da76f8a785a104b9d4023132f0ed942d36ad  reports/results/air-quality/parameters.json
e04843cb83cc6e81274d05ed0c0abab7102a931b07d2f60b0c30b5920372bf01  reports/results/air-quality/predictions.csv.gz
66479107f6c560c17321da6a3bad46b4dd8bd4fcb78a8c11387e0f34cf57affe  reports/results/air-quality/outages.csv
1e90e651ffee8219cd7ec176c06bf8833dda9972da2b0f74f2e69d6d13fbac14  reports/results/air-quality/events.csv.gz
2792d1cf8e45ad6b9df123161cd06236a7fea3cb59cd061eb105d7b4d4c19a47  reports/results/air-quality/station-scores.csv
2792d1cf8e45ad6b9df123161cd06236a7fea3cb59cd061eb105d7b4d4c19a47  reports/results/air-quality/available-hour-scores.csv
cc2f9de86546188238b7b8a9b41380c3d7af071f6e4abf28b0d84b6665f6de5e  reports/results/air-quality/quarter-scores.csv
c0fe245ef25a72d39aea2a8729fbc14139b95e3e790cbddfc2d8551ee5740ea0  reports/results/air-quality/outage-warnings.png
734e21cddbee577d55e8d6ac470b26fd6bae262144d12ae4785d3163a31a498a  studies/air-quality/STORY.md
```

2026-10-30, statistical reviewer: results approved; AP01/AP02 identified for
publication completion; reproduction pending. No final-period tuning requested
or performed.
