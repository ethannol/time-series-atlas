# ECG results, patient membership and provenance review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: full ECG run from `6dc5e504690ae141dceac03b773f6d199f5774ec`, protocol
`fbd9a70b6b5ca5fa83f41cb86d3b2559cc5325df`, and its saved outputs. The reviewer
authored no implementation and performed no classifier or PCA refit.

**Artifact and score verdict: pass. Publication remains pending the final
result narrative and clean-checkout reproduction.** Majority, template and
logistic hard predictions were independently reconstructed. Forest labels were
independently rescored and aligned to source; tree reconstruction is not claimed.

## Provenance and complete patient coverage

All **38 source hashes** match their recorded historical Git blobs, all **ten
output hashes** match retained artifacts, and the NPZ matches its source audit.
The run records stable source, 37.10 seconds elapsed and approximately 608 MB
process-lifetime peak RSS, describing this local execution rather than a
portable performance benchmark.

All **402,648 prediction rows** align exactly with the snapshot's beat index,
person, record, sample, symbol and label. Each of four models predicts every
one of the 100,662 retained beats once, in the person's frozen held-out fold.
The reviewer independently regenerated all **172,000 training-membership rows**
from the declared RNG/cap rule, verified record/person/sample/label fields,
training/test disjointness and all per-fold class/person counts. Records 201/202
remain together. No training cap was applied to the held-out population.

## Transform and prediction reconstruction

The reviewer independently computed the per-beat median/peak-to-peak
normalization and log extras from pinned waveforms/RR. Each saved class template
matches the mean of its actual capped training beats. Majority and nearest-
template labels reconstructed from those values match every held-out prediction.

Every PCA mean equals its capped training mean, components are orthonormal,
and projected training variances reproduce the saved explained-variance ratios.
Saved scaler statistics match the projected training rows plus the two extras.
Applying saved PCA/scaler/logistic coefficients to held-out waveforms reproduces
every saved logistic label. This verifies training-transform metadata and
inference arithmetic without re-estimating PCA or logistic parameters. All
logistic warning lists are empty and iteration counts are below the cap.

The forest audit retains the declared seed, 100 trees, depth/leaf limits,
single-worker setting, 22 feature importances and per-tree node counts. Saved
settings and diagnostics are consistent. Trees are not serialized, so exact
forest inference cannot be reconstructed from this audit alone. Full forest
reproduction remains the later deterministic refit checkpoint; this review
verifies its retained hard predictions, correct held-out identities and scores.
There are no degenerate-amplitude or previous-RR floor cases in this snapshot.

## Score and figure audit

Independent confusion-matrix arithmetic exactly reproduces pooled counts for
all four models, all four fixed-class F1 averages, accuracy, class support,
precision/recall and zero-denominator flags. Every per-fold, per-person and
person/class row is present and agrees: **20 fold**, **172 person** and **688
person/class** rows. Per-person F1/recall use only actually supported classes;
pooled/per-fold F1 retain all four declared classes. Numeric comparisons used
`rtol=1e-11, atol=1e-12`; null rates retain their actual undefined meaning.

Both figures were visually inspected. The class-recall plot exposes the rare-
class failures instead of hiding them behind total accuracy, and its person
boxplot labels the supported-class denominator. The waveform figure contains
fold-zero training templates only, with the expert-centered time coordinate.
The report preserves the benchmark's enriched historical cohort, annotation
lookahead and selected-group definition; N is not a healthy-person diagnosis.

## Required emphasis in the final narrative

The forest's **89.6% accuracy** is close to the majority baseline's **89.5%**;
its higher fixed-class macro F1, 0.434 versus 0.236, is a distinct result. The
forest correctly identifies **zero of 802 F beats** and only **302 of 2,781 S
beats** (10.9% recall), despite strong N/V recall. Those failures should be
prominent in plain language. Logistic has higher S recall but many more false
class assignments; none of these pipelines demonstrates clinical readiness.

Fold 2 had only 14 capped training F examples, as recorded before results.
That sparse class support and across-person variation constrain interpretation;
they should not motivate an unrecorded post-result cap or model change. The
pipelines differ in features/weighting as well as classifier family, so this
is not an isolated causal claim that one model family is superior.

The inspected report is careful about these boundaries but needs an explicit
result takeaway and the process story's actual implementation/results entry.
Preserve the original plan and append what was learned. Fresh-checkout
reproduction and final publication checks remain outstanding in this record.

## Inspected hashes

```text
915d3f3a207cc7114654908b9f4a6088a3290636ea4065b940d4b5126852fa46  reports/results/ecg/run.json
f3d1ef9a6a2c2cd88c581a1f675a9765cea20690db4655751b647d847274f359  reports/results/ecg/metrics.json
56330dfd54803a6216d916b2b01f9a9a5365ae67ec0ce2ddec3022ca23fb916b  reports/results/ecg/model-audit.json
1c728814c63da383b0440cc5d2bd25f43517e2a07e3303a8af5b5e0b3facc3e8  reports/results/ecg/predictions.csv.gz
2ec4be305773555d86dc19ccaa5051af17d3fd303700c9b84bb16905090f2776  reports/results/ecg/training-membership.csv.gz
406d566c64603e6b81e096d8edfc83c2957ac39e1309b989d0453c62efd65f65  reports/results/ecg/REPORT.md
a8b75c7366b5b33dc826ef69782bdeed6a5ac094234017974d3b7bc6b757fe7d  reports/results/ecg/people-and-classes.png
22ddffc2768290e343182e6feb3cc9547bafeb6160bc16b9db6e39617f325f6d  reports/results/ecg/training-templates.png
```
