# Air quality — fresh study critique

Date: 2026-10-30. Reviewer: independent AI subagent `critique_air_quality`.
The reviewer did not author the implementation. Implementation was read before
earlier verdicts; those verdicts were subsequently checked for accepted boundaries.

Reviewed baseline: `71999b34ccfd7127840b173efb287ac0a66b2a26`, the parent's freshly
fetched `origin/main`, recorded in [baseline.json](baseline.json) at
`2026-10-30T23:19:56.565503+00:00`. No instrumentation patch. Published run source:
`2c0af60037ae691aae7e13c92cb37228215e5876`; protocol:
`715ac6c89b1948609c67626c883a4cc63ec3abde`. All line references and hashes below
describe the reviewed baseline, not the parent's subsequent presentation repair.
That repair has not been verified in this initial review.

## Three scoped verdicts

| Scope | Verdict |
| --- | --- |
| Implementation | Pass within the frozen single-station nowcast contract. No new source, leakage, split, scoring, or event-ledger defect found. |
| Findings | Supported as descriptive results for the prescribed monthly windows and complete-truth cohort. No inference of universal station/season superiority or operational performance is justified. |
| Presentation | Revise the missing promised station/quarter summary below. Existing aggregate numbers remain valid; no refit or new model selection is requested. |

## Required finding

**AQ-C01 — Medium: the report omits promised subgroup context that qualifies its headline.**
Status: identified in the baseline; parent has acknowledged a presentation repair,
which remains outside this initial verification.

`studies/air-quality/DESIGN.md:59` requires seasonal and station variation.
`src/tsatlas/air_quality.py:125` saves quarterly evidence, but the report at
`reports/results/air-quality/REPORT.md:18` presents only the overall scores and
does not summarize or link `quarter-scores.csv`. Its station-evidence link at
line 38 concerns undefined classes rather than the actual heterogeneity.

Independent aggregation of the saved station/quarter rows establishes:

| Saved subset | Peer-median macro balanced accuracy | Persistence | Support/context |
| --- | ---: | ---: | --- |
| 24-hour, quarter 1 | 0.8532 | 0.8599 | All 12 stations contribute; small reversal of the overall ranking. |
| 6-hour, quarter 3 | undefined | undefined | Zero high hours; zero BA contributors, despite 180 scored station-hours. |
| 24-hour, quarter 3 | undefined | undefined | Zero high hours; zero BA contributors, despite 696 scored station-hours. |
| 72-hour, quarter 2 | 0.9300 | 0.5909 | Only 4 stations contribute defined BA. |

At 6 hours, peer median beats persistence at 9/12 stations, losing at Changping,
Dingling and Dongsi; its BA differences there are −0.0370, −0.0370 and −0.0333.
At 24 hours it wins at 11/12, losing at Tiantan by 0.0117; at 72 hours it wins
at all 12. Evidence: `reports/results/air-quality/station-scores.csv:7`, `:11`,
`:15`, and `reports/results/air-quality/quarter-scores.csv:1` (aggregate across
the explicit duration/quarter/model keys). All these score cells were recomputed.

Impact: the aggregate headline is true, but readers do not receive the frozen
design's promised information about where the comparison fails or lacks high-class
support. Remedy: add a short descriptive paragraph/table with contributor counts,
station win counts and a direct quarter-evidence link; keep undefined BA undefined.
Explain that quarter 1 combines March 2016 with January–February 2017 and that
these are scheduled windows, not continuous seasonal coverage. Do not tune models,
claim significance, or use these subgroups to replace the frozen primary result.

## Accepted boundaries and optional improvements

- The target station is dropped from network inputs (`air_quality.py:15`), and
  fitting/scaling/thresholds stop at February 2015 (`:21`). Same-hour peers are
  permitted inputs under the declared arrival assumption, not future forecasts.
- Complete-block truth selection is explicit, not leakage into predictors.
  All 64 excluded blocks lack target truth; all 368 eligible blocks have an
  immediately preceding reading. Coverage correctly separates truth eligibility
  from peer availability. This preserves the earlier verified AQI-S01 correction.
- Every scheduled hour has at least **8** peers here. Thus the three-peer minimum
  and abstention logic are fixture-tested, not empirically challenged by this run.
  Correlated failures, reporting delay and real-gap performance remain untested.
- Macro station BA and macro station MAE are equal-station summaries; pooled rates
  use pooled confusion counts. All 12 stations contribute overall BA. The calendar
  baseline issues no high alerts, explaining BA 0.5; it is a concentration baseline,
  not evidence that all plausible local warning methods are ineffective.
- Block-local event matching faithfully implements the frozen rule, including
  left/right censoring, abstention breaks and conditional delay. Sustained alerts
  can match multiple true runs. Zero wholly false episodes does not mean zero
  false-positive hours. The report now makes these earlier accepted limits clear.
- Optional: explicitly label table MAE as macro station MAE, expose censoring counts
  beside event totals, and explain the calendar baseline's never-high behavior.
  These improve interpretation without changing results. No new benchmark is required.

## Checks actually performed and untested scope

1. `uv run --locked pytest -q tests/test_air_quality.py`: **4 passed**, six existing
   NumPy/pandas timedelta deprecation warnings; no test failure.
2. Verified 39 historical source hashes, all 10 published output hashes and the
   snapshot hash against `run.json`. Verified the archived raw ZIP hash and all
   twelve station grids/PM2.5 columns against the snapshot: 35,064 hours × 12 stations.
3. Independently checked all 432 scheduled blocks, half-open endpoints, exclusions,
   prior-reading eligibility and peer counts. Checked all 46,104 saved prediction
   rows for unique keys, shared truth, thresholds, peer counts and common coverage.
4. Independently recomputed every station, available-hour and quarterly score,
   primary macro/pooled aggregate, coverage aggregate, all 1,223 event rows and
   event summaries. A first probe stopped at an audit-only int32/int64 quarter-index
   comparison; accepting equivalent index types yielded matching numeric results.
5. Checked saved-parameter arithmetic without fitting for three blocks: 6-hour
   Aotizhongxin, 24-hour Dingling, 72-hour Wanliu. Training counts/scaler moments
   and all four methods agree. All raw/clipped Ridge values agree; 20 are clipped.
6. Small in-memory fixtures verified the exactly-24-hour prior boundary, absent
   prior exclusion, leap-day/month crossing, three-peer issue versus two-peer
   abstention, and negative raw clipping. No source/input files were changed.
7. Visually inspected `outage-warnings.png`: readable axes/units, distinguishable
   near-overlapping network styles, separately labeled coverage bars. Reviewed
   report prose/tables and nowcast-versus-forecast framing. Rendered-browser review
   was attempted but the browser access host was unavailable; no live-layout claim.
8. Checked the official [UCI dataset page](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data):
   twelve sites, hourly dates, NA convention, PM2.5 units, citation and CC BY 4.0
   agree with the source credits. Read the saved reproduction record; did not
   conduct another clean-checkout reproduction, full fit/replay, tuning or release audit.

## Baseline identities (SHA-256)

```text
6b40572e23e0afc788cdd6f57089bff45515b76fe079925028537fd92bac6a52  src/tsatlas/air_quality.py
36a342dd2c23a9826d25a478a7a85028c70e6f93395f7e7befc3571de580fd6a  src/tsatlas/classification.py
870801c933476d2133b0a233d3e85188b376ba93b33a8c75c88fc36ba03675f5  src/tsatlas/extended_data.py
f9be97008368484c68bed34dcb86530cbe8b1bd3e8620d03b1e0cff913add8a9  tests/test_air_quality.py
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
9ed10058371b24b9602a8d4078088d9952255c0aa5fa3231b3972d7aa1a19e19  studies/air-quality/STORY.md
1728af0edf50039ca234a58803f75bcc5e121c51b0fc9bef2c3d298f19a20fc5  data/snapshots/air-quality-hourly.csv.gz
b04da438b2f331ac0ffd45aebdfec0d20d2367feb5f6948c4b1f7ce1191e33c4  data/raw/air-quality.zip
8454955ff7dc5fd3fa5f43757ee46180ae419a087c38cb2175d8b65a6b0946e6  reports/results/air-quality/run.json
cd55b1d09af0edb1a4ee42f5a16f8e4498193f72ad27ac5adf2377352d4f4afd  reports/results/air-quality/REPORT.md
21c4e8fbe9c6804cd15628fa023d2e3633f0c1eeebb9b040c1d89a5860497ffd  reports/results/air-quality/metrics.json
cc2f9de86546188238b7b8a9b41380c3d7af071f6e4abf28b0d84b6665f6de5e  reports/results/air-quality/quarter-scores.csv
2792d1cf8e45ad6b9df123161cd06236a7fea3cb59cd061eb105d7b4d4c19a47  reports/results/air-quality/station-scores.csv
e04843cb83cc6e81274d05ed0c0abab7102a931b07d2f60b0c30b5920372bf01  reports/results/air-quality/predictions.csv.gz
1e90e651ffee8219cd7ec176c06bf8833dda9972da2b0f74f2e69d6d13fbac14  reports/results/air-quality/events.csv.gz
6e6aed2d530ac01158343e571e2e204e6c29f1f62eee15505fed43a41ba2866a  reports/results/air-quality/outage-warnings.png
```
