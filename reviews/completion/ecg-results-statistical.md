# ECG results review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Run source: `6dc5e504690ae141dceac03b773f6d199f5774ec`.
Protocol: `fbd9a70b6b5ca5fa83f41cb86d3b2559cc5325df`.
Scope: saved predictions, training membership, source snapshot, model audit,
metrics, figures, report and story. No classifiers were refitted and no folds,
training samples or hyperparameters were changed after seeing the results.

**Results verdict: approved.** Independent scoring and source/group alignment
match the saved evidence. **Publication verdict: pending ECG-P01 below and the
planned exact-reproduction gate.** The missing plain-language result must expose
the rare-class failures rather than let high overall accuracy stand alone.

## Independent checks completed

All 402,648 prediction rows represent four methods on the identical 100,662
retained beats. Every model has exactly one row for every source beat index.
Record, person, sample, annotation symbol, grouped truth and frozen fold match
the source. Records 201/202 remain patient 201. Every patient's test fold excludes
that patient from training, including both shared-person records.

All 172,000 saved training-membership rows match the deterministic sampling rule,
source identities and the cap of 1,000 beats per training person. This reviewer
regenerated sampling indices without fitting models. The 34/34/34/35/35 training
person counts and 9/9/9/8/8 held-out person counts match the pre-run structural
review. Every actual training fold contains all four classes, so no class/model
was substituted or silently dropped.

Using saved parameters, the reviewer reconstructed every majority, nearest
template and logistic prediction. Training-only template means, PCA centering,
orthonormal components and logistic scaling reproduce the saved audit. Forest
hard predictions were independently scored but not regenerated: trees are not
serialized, and this review did not refit them. Exact deterministic reproduction
must cover that later. All five logistic fits converge in 30–32 iterations with
no recorded warnings.

Independent confusion-matrix arithmetic reproduces every pooled metric and
per-class rate, all per-person metrics and person/class support rows, and every
fold score. Fixed-four-class F1, true-supported per-person means, null precision/
recall and zero-F1 denominator conventions are consistent with the frozen design.
All output hashes in `run.json` match the inspected files. The source/snapshot
hashes match the approved implementation/intake.

## What the evidence supports

| Method | Pooled macro F1 | Accuracy | Macro class recall |
| --- | ---: | ---: | ---: |
| Majority | 0.2361 | 0.8948 | 0.2500 |
| Class template | 0.2505 | 0.4482 | 0.3513 |
| Logistic | 0.3895 | 0.6973 | 0.5086 |
| Forest | 0.4340 | 0.8961 | 0.4884 |

The forest has the largest pooled macro F1 among these frozen pipelines, but its
accuracy exceeds majority by only 0.00131, or about 0.13 percentage points. The
forest recognizes 6,434/7,007 V beats and 302/2,781 S beats, but **0/802 F beats**.
Its 111 F predictions are all incorrect. Logistic has higher S recall
(1,510/2,781) and macro recall, but far more false class assignments; it recognizes
only 27/802 F beats and makes 11,310 F predictions. A single accuracy or winner
label would conceal materially different errors.

The F support is strongly concentrated across the frozen folds:

| Fold | Capped training F beats | Held-out F beats |
| --- | ---: | ---: |
| 0 | 262 | 30 |
| 1 | 258 | 6 |
| 2 | 14 | 755 |
| 3 | 274 | 7 |
| 4 | 268 | 4 |

Thus fold two contains approximately 94.1% of all held-out F beats while retaining
only 14 F training examples after the declared per-person cap. This is observed
support imbalance in a person-disjoint benchmark, not a discovered split bug.
It materially limits broad claims about F recognition; it does not authorize
reselecting folds or changing the cap after inspection. No causal attribution of
the failure to this one factor is established.

Per-person supported macro recall also varies widely. Its median is 0.602 for
forest and 0.632 for logistic; forest spans approximately 0.275–1.000 and logistic
0.091–1.000. Those summaries use the classes present in each person, unlike the
fixed-four-class pooled F1. They are descriptive variation across 43 groups,
not beat-level confidence intervals or a population-generalization guarantee.

Both figures were visually inspected. Class bars agree with the audited recalls;
the person plot names its supported-class denominator. The second figure is
explicitly a fold-zero training-template plot, not a test example or a claim that
the class means describe every person. Expert beat locations, annotation-derived
previous RR, quarter-second lookahead, paced-record exclusions and the enriched
historical sample remain important limits. These are conditional waveform
classification results, not beat detection or evidence of clinical effectiveness.

## ECG-P01 — State the result, class failures and actual study status

Type: publication omission, not a metric or leakage defect. Priority: close
before publication. Add a brief direct answer to the report's question: these
pipelines show some recognition across held-out people, with substantial
class/person dependence and poor F recognition. Give the forest/majority accuracy
comparison, the forest's zero F true positives, and the concentrated F support.
Explain that different metrics favor different error tradeoffs; avoid a general
claim that waveform recognition transfers reliably or that forest is universally
best. No additional model search is requested.

The current study story still ends at source intake and says no classifier has
run in its last dated entry. Preserve that historical entry and append the
implementation, fixed-run results and independent review milestones; update the
current-status summary. The process story should make clear that patient grouping
was fixed before fitting and these disappointing rare-class results were retained.

Closure requires checking the regenerated report/story and unchanged numerical
evidence, followed by the separately planned exact reproduction. It does not
require refitting for this review or changing the design after outcomes are known.

## Inspected SHA-256 identities

```text
6dd098712d2e82053b1e566f533568f750c9a9230b0e77bf2c8786ef94768b25  src/tsatlas/ecg.py
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
2e99a77d11059ba65913b6f91c3f847bd3d5132e1a441592bd0c1fcb2e953562  studies/ecg/folds.json
1c728814c63da383b0440cc5d2bd25f43517e2a07e3303a8af5b5e0b3facc3e8  reports/results/ecg/predictions.csv.gz
2ec4be305773555d86dc19ccaa5051af17d3fd303700c9b84bb16905090f2776  reports/results/ecg/training-membership.csv.gz
f3d1ef9a6a2c2cd88c581a1f675a9765cea20690db4655751b647d847274f359  reports/results/ecg/metrics.json
56330dfd54803a6216d916b2b01f9a9a5365ae67ec0ce2ddec3022ca23fb916b  reports/results/ecg/model-audit.json
1b8fd4054e02943d17c2f6b94214ed6375baaeb6a33e64a38095ef0582210855  reports/results/ecg/person-class-scores.csv
b6e3d9e7503ebddf5f3dfbc72af5bb59e59e1de6d8df48d7e581e9a051f0d67c  reports/results/ecg/person-scores.csv
03dab31e3088e973981620eaa3b74dfc898d8bac309e3965655707b349ef1ecf  reports/results/ecg/fold-scores.csv
a8b75c7366b5b33dc826ef69782bdeed6a5ac094234017974d3b7bc6b757fe7d  reports/results/ecg/people-and-classes.png
22ddffc2768290e343182e6feb3cc9547bafeb6160bc16b9db6e39617f325f6d  reports/results/ecg/training-templates.png
406d566c64603e6b81e096d8edfc83c2957ac39e1309b989d0453c62efd65f65  reports/results/ecg/REPORT.md
915d3f3a207cc7114654908b9f4a6088a3290636ea4065b940d4b5126852fa46  reports/results/ecg/run.json
6f1ab6e71c7820246b5daf190e05a0fcb42c819ba3f874a44aff62af15674379  studies/ecg/STORY.md
```
