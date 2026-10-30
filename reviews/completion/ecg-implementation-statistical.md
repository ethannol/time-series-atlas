# ECG pre-run implementation review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: ECG classification implementation, focused tests, frozen design/fold map,
previously reviewed source extraction and bounded development evidence. The
reviewer did not author these implementations, did not run the full five-fold
classifiers and did not inspect full-run accuracy. This continues the verified
completion review suite, not a new experiment on a different repository base.

**Statistical implementation verdict: approved for the frozen full run.** No
blocking discrepancy was identified between this code and the reviewed contract.
Approval concerns separation, arithmetic and bounded execution; it does not
establish generalization or approve claims about results not yet produced.

## Patient separation and the comparison population

`fold_indices` uses the frozen person-to-fold mapping, traverses training people
in sorted order and samples at most 1,000 beats per person without replacement
using `default_rng(20261031 + fold)`. Selection reads no labels. Every held-out
beat remains in its test fold. Both records 201 and 202 carry person ID 201 in
the pinned source and consequently remain together. All four methods receive
the same capped training indices and held-out indices within each fold.

An independent structural pass over the actual 100,662-beat snapshot verified
that training and test people never overlap, training caps hold, changing every
label leaves sampled indices unchanged, and every beat belongs to exactly one
test fold. All four benchmark classes are present in each actual capped training
fold. Thus the code's explicit exception for a training fold with fewer than two
classes is not reached on these frozen inputs; no failed model was substituted.

| Fold | Training people | Training beats | Test people | Test beats |
| --- | ---: | ---: | ---: | ---: |
| 0 | 34 | 34,000 | 9 | 20,588 |
| 1 | 34 | 34,000 | 9 | 21,806 |
| 2 | 34 | 34,000 | 9 | 21,093 |
| 3 | 35 | 35,000 | 8 | 17,683 |
| 4 | 35 | 35,000 | 8 | 19,492 |

The final assembly asserts unique, complete beat-index coverage for each model.
Saved record/person/sample/symbol/truth/fold fields and training membership will
allow a second independent check after the full run. This is person transfer
within the selected historic benchmark, not prospective chronological validation.

## Fitted information and timing

Beat normalization is local to each 60-sample waveform. Computing this row-local
transformation for all rows does not estimate a test-population statistic. Class
templates and the majority class use training labels only. Sorted class order
provides the declared deterministic template tie rule.

PCA fits only normalized training rows, using 20 components, full SVD and no
whitening. Logistic scaling fits only the 22 training features; the two extra
features are floored log amplitude and log previous RR. Logistic and forest
settings match the contract, including balanced weights, fixed seeds, tree/depth/
leaf limits and one forest worker. Test data enter transforms/prediction after
fitting, not fitted means, components or class statistics.

In a bounded synthetic fixture, this reviewer fitted the declared pipelines on
120 training rows from three people and 10 test rows from a fourth person. After
changing all held-out waveforms, RR values and labels, training class counts,
templates, PCA metadata, logistic parameters/scaler and forest diagnostics were
identical. Every method still emitted exactly the same ten held-out beat indices.
No predictive accuracy was computed; this fixture tests information separation.

The source extractor still uses MLII selected by name and the declared
`[-90,+90)` waveform window at 360 Hz, then fixed 1:3 resampling. Previous RR is
computed from the preceding recognized beat annotation, including relevant
excluded-class beats, before filtering to the four output groups. It does not use
the next beat. The quarter-second post-center waveform and expert annotation
locations are stated in the report: this is classification conditional on known
beat locations, not instantaneous detection. The audited snapshot and extraction
code hashes remain unchanged from source/design review.

## Score arithmetic and interpretation

`classification_scores` checks aligned nonempty vectors and recognized labels.
Confusion rows are actual classes and columns are predicted classes in explicit
N/S/V/F order. Precision uses predicted support, recall uses actual support,
and zero-denominator rates stay null. F1 uses `2 TP / (actual + predicted)`.
The fixed four-class macro assigns zero only when the F1 denominator is zero,
recording that condition. Per-person macro F1 and macro recall instead average
classes actually present for the person and retain the contributing-class count.

Independent hand arithmetic checked a confusion matrix with an actual-absent
but predicted class, as well as a wholly absent class. It verified fixed-class
versus supported-class macro F1, undefined recall versus defined zero precision,
and the explicit zero-F1 convention. The code retains per-class supports and
per-person/fold summaries rather than presenting pooled accuracy alone.

The report template correctly says that template, logistic and forest are
different pipelines; their comparison cannot isolate algorithm family alone.
It distinguishes the N benchmark group from a healthy-person diagnosis and
avoids treating 100,662 beats as independent patient evidence. The eventual
results review must still inspect rare-class failures and between-person
variation; no clinical or population-prevalence claim follows from this gate.

## Executed evidence and remaining gates

`uv run pytest -q tests/test_ecg.py`: **3 passed**. Independent checks described
above also passed. The author's fold-zero development trial uses a deliberately
smaller structural cohort: 50 training beats per person, 10 test beats per person,
1,700 training beats and 90 test beats, yielding 360 valid-label prediction rows.
It records patient disjointness and no accuracy computation. Its source hash
matches the implementation inspected here. Those reduced caps are development
evidence only; the final implementation retains the frozen 1,000 training cap
and all held-out beats.

No request to retune models, resample folds or alter the frozen cohort follows
from this review. Full saved predictions, convergence diagnostics, metrics,
figures, conclusions and exact reproduction remain subject to their results and
publication gates. A completed bounded trial is not completion of the ECG study.

## Inspected SHA-256 identities

```text
6dd098712d2e82053b1e566f533568f750c9a9230b0e77bf2c8786ef94768b25  src/tsatlas/ecg.py
ca978264b5b51f5ddb20df572e496a553f794bb24e66f2b3461700102ce4b594  tests/test_ecg.py
3ddc1074feb94ce2f0ad08ca6196c9491035dc8f5f0f1bc5d12af3490bd92186  src/tsatlas/ecg_source.py
36a342dd2c23a9826d25a478a7a85028c70e6f93395f7e7befc3571de580fd6a  src/tsatlas/classification.py
70ea0f6bc5fe539448afc659e898eb72febb92aa777c1be86c4795dbcff34a59  studies/ecg/DESIGN.md
2e99a77d11059ba65913b6f91c3f847bd3d5132e1a441592bd0c1fcb2e953562  studies/ecg/folds.json
1a61640bf69e5cd72bf217ab66065bf618938ad2fb10caaf13053a18bc72bc75  reports/intake/ecg.json
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
8ee972ceb36c9e7aabfdbd36d3b908b7fb80c6159c655c74db3daafefa2af89d  reports/verification/ecg-development-trial.json
```
