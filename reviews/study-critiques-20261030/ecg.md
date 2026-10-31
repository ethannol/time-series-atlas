# ECG — fresh implementation, findings and presentation critique

Date: 2026-10-30. Reviewer: dedicated non-authoring AI subagent `critique_ecg`.
Read implementation, frozen design, outputs and figures before prior verdicts.
This is a fresh artifact audit, not independent human or clinical validation.

## Baseline and scope

- Parent fetch verified at `2026-10-30T23:19:56.565503+00:00`, recorded in
  [baseline.json](baseline.json); reviewed commit
  `71999b34ccfd7127840b173efb287ac0a66b2a26` on `review/study-critiques-20261030`.
- Verified ECG implementation/common helpers, design, folds and result artifacts
  against that commit. Read shared README/METHODS/portfolio copy with `git show`
  because other studies were being edited. No instrumentation patch or fitting.
- Historical run source is `2c0af60037ae691aae7e13c92cb37228215e5876`, protocol
  `fbd9a70b6b5ca5fa83f41cb86d3b2559cc5325df`
  (`reports/results/ecg/run.json:2–4`). Relevant source hashes still match.

## Separate verdicts

| Checkpoint | Verdict |
| --- | --- |
| Implementation/data | Supported within inspected scope; no new leakage, source, split or scoring defect found. |
| Findings/statistical interpretation | Supported as descriptive results for these frozen pipelines and 43 patient groups. |
| Presentation/publication | Supported; rare-class failures, expert localization and population limits are prominent. No blocker found. |

No new material defect or insufficiently qualified headline was established.
Existing limitations below remain limitations; this review does not mark them fixed.

## Implementation evidence

1. **Source and exclusions agree with retained data.** Rehashed all 146 extracted
   members against the intake audit. Read all 48 headers/annotations and rebuilt
   every retained sample identity, grouped label and previous RR without using
   model predictions. All 100,662 rows match; 44 initial beats and 12 boundary
   windows are excluded. The audit records zero nonfinite exclusions.
   Source: `src/tsatlas/ecg_source.py:14–19,34–61`;
   `reports/intake/ecg.json:1203–1228`.
2. **MLII and shared-person handling are correct.** Paced records 102/104/107/217
   are absent. All other records contain MLII. For first/middle/last retained beats
   of each of 114/201/202, independently extracting `[-90,+90)` and resampling
   1/3 reproduced all nine stored waveforms exactly. Record 114 uses channel 1;
   201/202 use channel 0. Both 201/202 map to patient 201 and test fold 1
   (`studies/ecg/folds.json:26,71–72`; source lines 19,37–53).
3. **Splits and caps match the contract.** Independently recreated the seeded
   person-to-fold permutation. Regenerating the implemented cap matches all
   172,000 membership rows, with identities checked against the snapshot.
   Training/test people are disjoint; training contains 34/34/34/35/35 people,
   capped at 1,000 beats each; test contains 9/9/9/8/8 people with all their beats.
   Mutating labels leaves sampled indices unchanged. Each model has exactly one
   held-out prediction per eligible beat. Source: `src/tsatlas/ecg.py:31–39,94–107`;
   contract: `studies/ecg/DESIGN.md:38–44`.
4. **Transforms respect the training boundary.** Per-beat normalization is local;
   changing one waveform/RR leaves other beat features unchanged. Recomputed
   all training template means and PCA centering from actual capped members.
   Projecting those members through saved PCA components reproduces all logistic
   scaler means and standard deviations within absolute tolerance `2e-14`.
   Saved PCA/scaler/logistic parameters reconstruct every logistic test label.
   Source explicitly fits PCA and scaler on training rows only
   (`src/tsatlas/ecg.py:21–28,42–57`); no logistic warnings are recorded.

## Independent score checks and findings

Confusion-matrix arithmetic, separate from `classification_scores`, reproduced
all pooled metrics, per-class rates and zero-denominator flags. It also matched
all 172 person rows, 688 person/class rows and 20 fold rows (`atol=2e-14`).
All 402,648 prediction rows match source record/person/sample/symbol/truth/fold.
The four-class F1 and supported-class person denominators follow
`src/tsatlas/ecg.py:76–90,111–119` and `studies/ecg/DESIGN.md:62–74`.

| Method | Macro F1 | Accuracy | Macro class recall |
| --- | ---: | ---: | ---: |
| Majority | 0.236119 | 0.894796 | 0.250000 |
| Template | 0.250466 | 0.448223 | 0.351280 |
| Logistic | 0.389501 | 0.697334 | 0.508583 |
| Forest | 0.434018 | 0.896108 | 0.488375 |

Forest recognizes 302/2,781 S, 6,434/7,007 V and 0/802 F beats; all 111 forest
F predictions are wrong (`reports/results/ecg/metrics.json:10–77`). Its accuracy
advantage over majority is only 0.131 percentage points. Logistic recognizes
27 F beats and template 21. These independently checked counts support the
report's opening conclusion (`reports/results/ecg/REPORT.md:3–15`).

The capped training/test F counts by fold are 262/30, 258/6, 14/755, 274/7,
268/4. People 208 and 213 contribute 734 of the 802 F beats. This supports the
report's concentration warning (`REPORT.md:53–57`), not a causal explanation
that the cap alone produced failure. Forest fold F1 ranges 0.3241–0.5263 and
loses to logistic in fold 3 (`fold-scores.csv:2–19`); the pooled winner is not
universally superior. Forest person supported-class recall spans 0.2754–1.0000.

## Presentation and disposition

Both PNGs were inspected with `view_image`. Class bars match the audited recall;
the person panel names its supported-class denominator, and the waveform figure
clearly says fold-0 training templates. Text and axes are legible. The report
defines N/S/V/F, distinguishes 44 recordings from 43 people, gives annotation
lookahead, and explains different model inputs (`REPORT.md:27–51,63–75`).
Baseline README line 34 and portfolio lines 74,81 preserve the same bounded claim.

- **Accepted limits, freshly checked:** expert locations and annotation RR,
  quarter-second post-center waveform, selected historical cohort, single frozen
  split, sparse F training support, differing pipeline features/weights, and
  person summaries with different class support. These are disclosed in
  `REPORT.md:37–69` and `studies/ecg/DESIGN.md:28–36,48–74`.
- **Optional ECG-O1, low priority:** add a compact precision/recall table or one
  sentence about false class assignments beside the recall plot. For example,
  forest V recall is 91.8% but precision is 49.2%, and logistic F precision is
  0.24%. Metrics already expose these tradeoffs and the text claims no reliable
  four-group recognition, so this is a presentation improvement, not a blocker.
- Patient-level uncertainty or repeated frozen splits would be a new extension;
  no significance claim currently requires them. Do not tune the existing split
  or cap to repair its observed rare-class result.

Prior completion reviews were read only after these checks. Their earlier
narrative omissions are addressed in current `REPORT.md:3–15,27–32,53–57` and
`studies/ecg/STORY.md:50–70`; earlier PASS/approval language was not evidence.

## Check boundary and identities

Two session-managed, single-threaded `.venv/bin/python` no-fit checks completed
in approximately 3.8s and 1.3s. No source/output changes, model fits, full test
suite, browser server or live deployment check were performed. Forest trees are
not serialized: their saved predictions were rescored, not regenerated. PCA
components were used for reconstruction, not refitted. Raw waveform equality was
sampled at nine beats; annotation/RR, membership and score checks covered all rows.
All ten output hashes matched `run.json:78–88`. Selected SHA-256 identities:

```text
e22c1ca033feb5ca17d2fba32c3417a108c447260105caebbe07d64f5e9a062b  src/tsatlas/ecg.py
3ddc1074feb94ce2f0ad08ca6196c9491035dc8f5f0f1bc5d12af3490bd92186  src/tsatlas/ecg_source.py
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
1c728814c63da383b0440cc5d2bd25f43517e2a07e3303a8af5b5e0b3facc3e8  reports/results/ecg/predictions.csv.gz
2ec4be305773555d86dc19ccaa5051af17d3fd303700c9b84bb16905090f2776  reports/results/ecg/training-membership.csv.gz
56330dfd54803a6216d916b2b01f9a9a5365ae67ec0ce2ddec3022ca23fb916b  reports/results/ecg/model-audit.json
f3d1ef9a6a2c2cd88c581a1f675a9765cea20690db4655751b647d847274f359  reports/results/ecg/metrics.json
de0e8ddfb3ab2161ea1a6e06153ca6494b3b8e042932fc7e83c63b46afeffdd6  reports/results/ecg/REPORT.md
```
