# Heartbeat recognition across people: study contract

Draft for independent source/design review. No classifiers have run.

## Question and source

Can waveform recognition distinguish heartbeat groups in people absent from
training? Use all eligible MIT-BIH Arrhythmia Database v1.0.0 recordings,
Moody and Mark (2005), DOI10.13026/C2F305, Open Data Commons Attribution1.0.
The48 records represent47 people;201/202 share patient201. Verify current
.hea/.dat/.atr member hashes against the provider checksum list, retain exact
download hash and label counts. Backup annotations are not current truth.

Exclude the four paced records102,104,107,217. Select MLII by header name,
including its second-channel position in114. A record without MLII is excluded
explicitly, never replaced using test performance. The retained44 records from43
people are a deliberately enriched historic benchmark, not a population sample.

Map beat symbols to four groups: N={N,L,R,e,j}, S={A,a,J,S}, V={V,E}, F={F}.
These are benchmark groups, not a healthy/ill diagnosis; the N group includes
bundle-branch and escape beats. Other labels and non-beat annotations are excluded
with counts. Expert annotation centers supply beat localization. Classification
given these centers does not evaluate beat detection, diagnostic decisions or
end-to-end clinical use.

## Waveforms, input timing and grouping

Extract MLII[-90,+90) samples around each annotated center at360Hz, then fixed
resample_poly(up1,down3) to60 samples. This needs up to0.25s post-center waveform;
it is retrospective classification with stated lookahead, not instant detection.
Reject boundary/nonfinite windows and beats lacking a previous beat for RR;
count these exclusion reasons separately. Previous RR is time since the preceding
beat annotation (including paced/unclassified beats when present); it uses no
next-beat annotation. Normalize each60-sample window by subtracting its median
and dividing by max(peak-to-peak,1e-6). Retain log amplitude and log previous RR
as additional features; RR and amplitude floors1e-6 are declared numerical rules.

Create5 patient-disjoint folds: sorted unique patient IDs, NumPy default_rng seed
20261031 permutation, assigned round-robin to folds0–4. Record the entire mapping
before fitting.201/202 must always share a fold. Each person is tested once on
all eligible beats. For a training fold only, cap each person's beats at1000 by
uniform sampling without replacement using seed20261031+fold; traverse persons
in sorted order. Cap without using labels; retain all test beats. No tuning or
feature/class selection after held-out scores are inspected.

## Fixed comparisons

Training majority-class baseline; nearest class-mean waveform template; multinomial
logistic regression; random forest. Templates use the normalized60-point shape,
Euclidean distance and sorted-label tie breaking. If a class is absent from a
fold's training data, document that and retain all its held-out examples.

For logistic/forest, fit PCA20 components on normalized training waveforms only,
full SVD, whitenFalse. Add log amplitude and log RR. Logistic standardizes these22
features on training data and uses C1,balanced class weights,max_iter1000.
Forest uses100 trees,max_depth12,min_samples_leaf10,class_weight balanced_subsample,
seed20261031+fold,n_jobs1. Both see the identical capped training cohort and all
test beats. Record convergence warnings/failures; do not silently substitute models.

## Scores and scientific limits

Primary: pooled out-of-person macroF1 over the four declared classes. Also
per-class precision/recall/support, confusion counts, total accuracy, macro recall,
per-fold and per-person scores. Per-person class-absent recall is null; show
support, and label any mean of supported-class recall with its contributing count.
For pooled/per-fold macroF1, use all four fixed classes and F1=0 when its
2TP+FP+FN denominator is zero, recording that case. Per-person macroF1 averages
only classes with actual support for that person, with that count shown; it is
not the same denominator as pooled macroF1. Per-class precision is null when no
beats are predicted in that class, and recall is null when actual support is
zero. These undefined rates are never presented as perfect recognition.
Thousands of beats are not thousands of independent people. Describe variation
across people without a naive beat-level significance claim. No random-beat-split
score may be described as evidence of unseen-person performance.

Preserve record/person/sample/symbol/label/fold and every predicted class, model
parameters or model audit, sampling membership, training-only transform metadata,
runtime, source/protocol revisions, and an inspectable waveform/score figure.
The separate synthetic spectral control addresses irregular sampling honestly;
ECG tape artifacts do not establish a clean physiological periodicity result.

## Required reviews

Source/design review includes actual headers, annotation inventory, group mapping
and extraction. Pre-run implementation review tests patient separation, within-
training transforms, exclusions and post-beat lookahead. Results/publication
reviews challenge generalization, class support and clinical overstatement.
