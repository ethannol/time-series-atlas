# ECG pre-run implementation review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: patient/fold identities, capped training membership, pinned waveform use,
preprocessing/model fit boundaries, score denominators, and output provenance.
The reviewer authored no implementation and ran no full classifier fit or
held-out classification accuracy evaluation. The author's bounded structural
trial is inspected as such, not relabelled as independent reviewer execution.

**Pre-run verdict: pass from the implementation perspective.** Commit the
reviewed source/configuration and satisfy the separate statistical gate before
full out-of-person scoring. Results and reproduction remain separate checkpoints.

## Source and grouping boundaries

The NPZ still matches the previously independently reconstructed snapshot:
100,662 annotation-centered MLII waveforms, 44 records, 43 people. The current
classifier consumes this pinned snapshot rather than rereading different leads
or annotations. The earlier source review establishes the 360 Hz window,
60-value resampling, previous-RR definition, paced-record exclusions and record
114's MLII channel choice. Those raw-source checks were not repeated here.

The reviewer independently regenerated the frozen mapping from the declared
seed/permutation and checked every snapshot record/person pair against it.
Records 201 and 202 both map to person 201. All five training memberships were
independently reconstructed from the declared per-fold RNG and sorted-person
sampling rule. Indices match exactly, without replacement, capped at 1,000 per
person across both records where relevant. Shuffling labels leaves membership
unchanged. Training/test people and beat indices are disjoint in every fold.
The union of test indices covers every one of the 100,662 beats exactly once.

| Fold | Training people | Training beats | Test people | Test beats | Training F beats |
| --- | --- | --- | --- | --- | --- |
| 0 | 34 | 34,000 | 9 | 20,588 | 262 |
| 1 | 34 | 34,000 | 9 | 21,806 | 258 |
| 2 | 34 | 34,000 | 9 | 21,093 | 14 |
| 3 | 35 | 35,000 | 8 | 17,683 | 274 |
| 4 | 35 | 35,000 | 8 | 19,492 | 268 |

All four classes occur in every actual capped training fold. Fold 2's **14 F
examples** are a material source/cohort limitation to preserve when interpreting
later class results. This is a pre-run membership count, not observed classifier
performance or a reason to change the frozen cap after review.

## Preprocessing and fitted model boundaries

Median subtraction, peak-to-peak normalization, log amplitude and log previous
RR operate on each beat independently. Hand-calculated checks and perturbing
unrelated waveform rows confirm that local transform property. Processing all
rows with this stateless transform does not estimate a shared test-data statistic.
Declared amplitude/RR floors are retained.

Code inspection confirms templates average capped training shapes by class;
sorted training labels determine ties. PCA fits only capped training shapes,
then transforms test shapes. Logistic scaling fits only PCA-plus-extra training
features. The forest and logistic use the same capped rows, training PCA and
held-out rows, with their exact frozen settings. The forest is single-worker.
No test labels select features, caps, class weights, hyperparameters or folds.
Logistic warnings/iterations are retained. Absent training classes cannot be
predicted but their held-out beats remain; the actual membership checks above
found all four classes in this dataset.

The model audit contract preserves class templates, PCA mean/components,
explained-variance ratios, scaler/logistic parameters, class counts, person
identities, warnings, forest settings/node counts/importances, and floor counts.
Forest trees themselves are not serialized; saved predictions remain separately
scoreable and exact deterministic refitting is a later reproduction check.

## Scoring and output contracts

Independent manual confusion fixtures verified true-row/predicted-column class
order, accuracy, four-fixed-class macro F1, supported-class per-person F1,
and precision/recall null behavior. A class absent from truth but predicted
incorrectly has null recall and zero precision; it is not perfect recognition.
The fixed-class zero-denominator F1 convention and flags match the contract.
Per-person contributing class counts and class supports are retained, while
pooled/per-fold F1 use all four fixed groups.

The reviewer ran `pytest -q tests/test_ecg.py`: **3 passed**. These cover shared
patient records, deterministic person caps, local normalization, declared extra
features, absent-class denominators and invalid labels. Additional independent
membership and score checks above also passed. No classifier was fitted by
the reviewer during this gate.

The author's trial names the exact inspected source hash. It uses fold 0,
50 training beats/person and ten test beats/person: 1,700 training beats,
90 test beats, 360 prediction rows across four methods. It reports valid labels,
patient separation and explicitly no accuracy scores. That proves bounded
execution/structure only. It does not establish full-cap runtime or recognition
quality, and the test cap is confined to that development trial.

Full execution saves every training membership and every held-out prediction
with index, patient, record, sample, symbol, truth, fold and model. It checks
complete unique test coverage for each method. Shared run provenance includes
the study's frozen JSON mapping and input hashes, with committed/stable-source
guards. Publication language correctly limits this to expert-centered waveform
recognition with post-center lookahead, not beat detection, diagnosis, population
prevalence or clinical effectiveness. The N group is explicitly not a healthy-
person label. No new implementation blocker was found.

## Inspected hashes

```text
6dd098712d2e82053b1e566f533568f750c9a9230b0e77bf2c8786ef94768b25  src/tsatlas/ecg.py
ca978264b5b51f5ddb20df572e496a553f794bb24e66f2b3461700102ce4b594  tests/test_ecg.py
70ea0f6bc5fe539448afc659e898eb72febb92aa777c1be86c4795dbcff34a59  studies/ecg/DESIGN.md
2e99a77d11059ba65913b6f91c3f847bd3d5132e1a441592bd0c1fcb2e953562  studies/ecg/folds.json
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
1a61640bf69e5cd72bf217ab66065bf618938ad2fb10caaf13053a18bc72bc75  reports/intake/ecg.json
8ee972ceb36c9e7aabfdbd36d3b908b7fb80c6159c655c74db3daafefa2af89d  reports/verification/ecg-development-trial.json
95a699e75a84da2651dc70268c942232abb62c7cdbd75f6e0454dc14788d3468  src/tsatlas/common.py
```
