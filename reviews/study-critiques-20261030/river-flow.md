# River flow: fresh dedicated study critique

Date: 2026-10-30. Reviewer: `/root/critique_river_flow`, non-authoring AI agent.
Reviewed published baseline `71999b34ccfd7127840b173efb287ac0a66b2a26`.
Independent fetch verified that `origin/main` at 2026-10-30T23:25:46Z. Source
and saved evidence were inspected before reading earlier review verdicts.
This records the completed baseline audit; later parent repairs are not reviewed here.

## Three verdicts

- **Implementation: pass for the frozen study.** No temporal leakage, source,
  target, cohort, calibration, event-scoring or numerical defect was found.
- **Findings: pass within the declared descriptive scope.** The retained evidence
  supports the small weather increment and onset/false-alert tradeoff. It does
  not establish operational warning value or general catchment effects.
- **Presentation: one medium disclosure amendment requested.** Quantify incomplete
  and highly uneven test coverage beside the headline results. No refitting,
  gauge reselection or change to the frozen metrics is requested.

## RF-C01 — Medium: numerical coverage is too easy to miss

Status: `identified`. Targets: `reports/results/river-flow/REPORT.md:57` and
`:63`; baseline generator `src/tsatlas/river_flow.py:230` and `:236`.
The report describes 17 gauges, links the split audit, and presents macro scores
and climate groups, but never states how much of the test calendar contributed.

Independent reconstruction gives the following counts **per method**:

| Date offset | Scheduled after origin guard | Scored targets | Invalid input/target union | Scored fraction |
| --- | ---: | ---: | ---: | ---: |
| +1 | 62,084 | 48,262 | 13,822 | 77.7% |
| +3 | 62,050 | 47,877 | 14,173 | 77.2% |

At +3, a further two boundary targets per gauge (34 total) are excluded before
the scheduled denominator. These counts reconcile exactly with the split audit.
They are scoreability counts, not measured operational uptime.

The extreme case is gauge `09386900`: `split-audit.csv:28` records 200/3,652
scored days at +1 (5.5%), and `split-audit.csv:29` records 195/3,650 at +3
(5.3%). It retains equal gauge weight. Its weather-model recall is 14/15 at +1
and 14/14 at +3 (`gauge-scores.csv:81`, `:84`); only six/four eligible onsets
support its respective onset results. Thus “17 gauges” does not mean seventeen
equally supported decade-long evaluations. The high-cold-fraction group also
contains this gauge. The omitted dates' performance is unknown; this audit
does not establish either the direction or size of selection bias.

**Requested change:** add the scheduled/scored counts or percentages and one
sentence about the sparse gauge and equal macro weight near the primary or
catchment summary. Keep the frozen cohort and existing scores. Closure needs
only inspection of the amended report/generator and unchanged numerical files.

Earlier RF-P01 explicitly requested incomplete-coverage context; final review
closed it on the presence of quality/coverage links
(`reviews/completion/publication-final-statistical.md:50`). This finding asks
for stronger prominence of the already measured limitation, not a claim that
the audit or accepted scoring convention was wrong.

## Actual checks and evidence

- Read `river_flow.py`, `camels_source.py`, shared classification/scoring helpers,
  relevant tests, provider readmes, source manifest/intake/credits, DESIGN/STORY,
  every river result artifact, and river claims in README, methods, collection
  story and `portfolio.json`. Inspected earlier findings only after source review.
- Verified all 114 cached raw-member SHA-256 hashes; recomputed all 93 candidate
  coverage fractions and the deterministic 17-gauge selection. HUC09's best
  candidate had 94.8665%, below the frozen 95% rule. Reconstructed all 217,328
  snapshot rows from named source columns and preserved quality flags.
- Rebuilt origin-time features, approved training quantiles, train/calibration/test
  masks, training scaler statistics, and calibration-negative cutoffs. Saved
  coefficients reproduced all **288,417 predictions** without fitting; maximum
  score difference was `3.55e-15`. All alert/truth/date keys matched exactly.
  Calibration false-positive fractions ranged from 9.11% to 10.08%, consistent
  with strict empirical quantiles and ties. No saved convergence warnings exist.
- Recomputed all **34 split rows, 102 gauge-score rows, six primary summaries,
  and 30 subgroup rows**. Matched method cohorts, denominators, confusion counts,
  Brier exclusions and training-only group definitions agree.
- Independently traversed full calendars to reconstruct **10,158 event rows**:
  5,886 high-run records, 3,915 false episodes and 357 unresolved segments.
  All dates, coverage, censoring, onset eligibility and alert counts matched.
  Per method/horizon there are 981 high runs, 103 censored starts and 878 known
  onsets. Eligible onsets are 822 at +1 and 696 at +3; eligibility differs by horizon.
- `uv run pytest tests/test_river_flow.py -q`: **4 passed**, with 12 existing
  NumPy timedelta deprecation warnings. No implementation was edited.
- All ten output hashes and all 39 source hashes in the recorded run matched
  the inspected baseline bytes. The run identifies source `f14924eb7de588721a0d12021cb35521ec928a2f`
  and protocol `7e6c91d4777beccb3abb05870e880918197ae93f`. Relevant recorded
  reproduction and rollout hashes also agree; those workflows were not repeated.
- Visually inspected the PNG: legible, unclipped, zero-based axes, correct bars
  and readable legends. It distinguishes macro high-day from pooled onset recall.
  Official [Zenodo record/API](https://zenodo.org/records/15529996) confirms
  version 1.2, the cited DOI, retrospective forcing and CC BY 4.0 metadata.

## Accepted limitations and optional follow-up

The daily availability assumption is explicit; approved flow and retrospective
weather are not demonstrated real-time vintages. +1/+3 are date offsets, not
measured 24/72-hour leads. Origin guards correctly prevent boundary calibration
outcomes from postdating issue time under that assumption. The deterministic
known-gauge panel, exclusion of estimated flow, and equal-gauge weighting remain
accepted design choices. Catchment groups are small, selected and descriptive.

Onset eligibility uses intervening truth only as a retrospective scoring stratum.
It does not filter model inputs. Different high-day/onset weights and different
horizon-specific onset populations prevent interpreting panel differences as a
paired causal effect. Unknown truth/forecasts create unresolved segments; wholly
false episodes and false-positive days measure different alert behavior.

Optional: strengthen the standalone portfolio caption (`portfolio.json:103`)
with actual false-alert burden or the idealized availability assumption. Its
current caveat and linked report prevent treating this as another numerical defect.

No full refits, tuning, new models, full archive acquisition, operational latency
validation, uncertainty analysis or live portfolio rendering were performed.
Automated review and reproduction do not constitute independent human validation.

## Baseline SHA-256 identities

```text
2c704ceec6a28eaa156716167fc637a62bd0925011b30c474e8eb3b58b4ecf80  src/tsatlas/river_flow.py
e1a84280cb4f2d7c590b9d508c654f92de8d6d023df13cca113e3a1a024faa3e  src/tsatlas/camels_source.py
36a342dd2c23a9826d25a478a7a85028c70e6f93395f7e7befc3571de580fd6a  src/tsatlas/classification.py
996fef9e5d69d8187ecddbe4690592badfda3b825d91c123a5b03173cf2843ee  studies/river-flow/DESIGN.md
16e56c36554bd04fe9dfb24c98706d48eecb1883bfa482a4a297da7b64c76405  data/manifests/river-flow.json
8426fccd9461d410d2fd76ffe700009b9fdc647eda42271cb1112a471c0ad775  reports/intake/river-flow.json
392dd930c5a975488d938ae56ee722982c02feca9f32b0bb0a7d8af299295956  data/snapshots/river-daily-panel.csv.gz
530a67b01853c859d34780f0e82e1753d0ca85cc0fc798ad4fcf1fb2bb98588f  reports/results/river-flow/predictions.csv.gz
ed6454881bf8ff270d43b90a8b83aadbea1e2fcad23cbb836636929780bbf2e6  reports/results/river-flow/events.csv.gz
0af39059acf633a74c818405bef3d2340957e2bb2f06028da060475f5f72b33b  reports/results/river-flow/metrics.json
ec32436c279cce849bddd658a20141f7b15647216b07b14982ba679339d80905  reports/results/river-flow/split-audit.csv
81bb7dbcd2df5e19504060702952a4fd26d84dab77243900fbb7f23c96ba6f50  reports/results/river-flow/REPORT.md
99fa0bf0efcec997d9034a48568d9e20c667cd2e0f61fe0a8b8b6a82b001303a  reports/results/river-flow/flow-and-onsets.png
997fdd0767f41c1c1131faec5be45b9abd8102552a7633db473c5f36465a309d  reports/results/river-flow/run.json
```
