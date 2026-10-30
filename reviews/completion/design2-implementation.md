# River, ECG, and spectral source/design review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: official-source acquisition records, actual retained raw members,
intake adapters/audits/snapshots, and three draft study designs. The reviewer
authored no implementation and ran no forecast/classifier/spectral comparison.
Raw-to-snapshot verification below is an independent reconstruction using the
source files and standard readers, not a call to the authored intake functions.

**Source verdict: river and ECG pinned snapshot contents pass.** River and ECG
designs are ready to implement from this perspective, with the minor ECG
exclusion-description correction C-D04 below. Spectral design needs the single
sampling-rule clarification C-D03 before freezing. Approval of source/design
does not approve forthcoming fitted models or their eventual interpretations.

## River-flow source checks

The reviewer rehashed all **114 pinned CAMELS members** and independently
recomputed all **93 training-coverage candidate checks** from the raw flow files
and gauge metadata. The resulting cohort is exactly the recorded 17 gauges,
one per qualifying HUC region; no HUC09 gauge meets the declared requirement.
The rule uses 1980–1999 approved/nonnegative flow only, with no final-period
completeness or performance selection.

For all **217,328 snapshot rows**, the reviewer reconstructed the calendar join
and verified raw flow values, preserved QC/missingness, precipitation, both
temperature columns, gauge/HUC identity, and metadata area. Temperature values
match the actual `tmax(C)` and `tmin(C)` headers exactly. They are not positional
substitutes such as snow-water equivalent. Audit QC counts agree with raw records,
including source-absent rows. The training weather fields are finite in this
pinned cohort; all training flow thresholds are positive (smallest 90th percentile
6.6 cfs), so the specified persistence score has a valid denominator.

The primary agent reported an earlier missing-QC serialization error and a
positional temperature-column defect. This review did not reproduce those
earlier versions; it independently verifies the corrected final snapshot and
header-based mapping. That distinction should remain in the process story.

The selective-acquisition guard now checks a newly read member's SHA-256 against
the previous manifest **before** replacing a local file. This corrects the
earlier read-through observation that a mismatch could overwrite pinned bytes
before raising. HTTP 206, precise ranges, bounded read sizes, member CRCs, and
the explicit “whole archive checksum not verified” distinction remain present.
No large archive was downloaded for this review.

The design uses the observed-flow product, separates approved from estimated
flow, avoids full-record hydrological attributes, and specifies an idealized
end-of-day availability assumption for retrospective weather. Calibration
thresholds use pre-test negative cases; both horizons share a coherent
information-valid evaluation cohort. Onset opportunities condition on future
truth only for scoring, not as forecast inputs. Their narrowed interpretation
and denominator must remain visible in the eventual event ledger. Geographic
spread is correctly distinguished from representative or ungauged transfer.

## ECG source checks

The reviewer compared all **146 extracted archive members** with ZIP bytes and
recorded hashes. Every selected member other than the checksum list itself is
present in, and matches, the provider's checksum list. The full ZIP matches its
acquisition manifest. All 48 headers/annotation inventories were inspected by
the reader; sampling metadata are 360 Hz and 650,000 samples.

The four paced records are excluded, leaving **44 records from 43 people**.
The group mapping keeps 201 and 202 together. MLII is selected by header name,
including its second-channel position in record 114. The reviewer independently
reconstructed every retained record/person/sample/symbol/group/previous-RR
entry and **every resampled 60-value waveform**, using the raw MLII windows and
`resample_poly` along an independently stacked window axis. All stored arrays
match exactly, including float32 representation.

The retained **100,662 beats** comprise N 90,072; S 2,781; V 7,007; F 802.
These are source class counts, not classifier outcomes. All actual annotation
symbols were inventoried; rhythm/noise markers are excluded from beat windows
and do not become prior-RR references. Paced/unclassified beat symbols do affect
the previous-beat timing where present, as declared.

The design correctly makes this annotation-centered waveform classification,
with explicit post-center lookahead, rather than a complete beat detector.
Its patient grouping, training-only transforms, per-person sampling cap, fixed
class mapping, and held-out-person evidence requirements are implementable.
PCA20/full SVD and a single-worker bounded forest are feasible at the declared
training size. Record the fold/person mapping and training membership before
the first classifier fit; the implementation gate must test those boundaries.

### C-D04 — Distinguish missing previous RR from waveform boundaries

Priority: low; clarify the audit/design before publication. Status: `identified`.
The current adapter increments `boundary_excluded` both when a window crosses
the recording edge and when no previous beat annotation exists. The reviewer
found **31 eligible records** whose first mapped beat has a complete waveform
window but no preceding RR (for example, record103/sample265). These are valid
exclusions for a model requiring previous RR, but their current reason label is
imprecise. Split that count into no-previous-beat and waveform-boundary reasons,
and state the no-prior-RR exclusion in the contract. Retained beats/waveforms
need not change. This does not invalidate the recognition cohort or require a
new comparison design.

## Spectral design and runtime feasibility

The control states the known signal, noise, observation window, three sampling
conditions, method definitions, search grid, alias handling, and bounded
replicate count. The regular-three-second schedule makes 0.17 Hz and
`1/3 - 0.17` indistinguishable within the sampled sine/cosine span. Reporting
that ambiguity alongside recovery avoids crediting a grid tie-break with
identifying physical truth. The deliberately incorrect index-FFT assumption is
labelled explicitly; conclusions are limited to the simulated setting.

The installed locked SciPy 1.18.1 signature accepts `floating_mean` and
`normalize`. The [official SciPy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lombscargle.html)
confirms that its frequency argument is angular frequency and explains the
floating-mean model. The proposed `2πf` conversion and keyword choices agree.
No Lomb–Scargle or FFT experiment was run during this design review.

### C-D03 — Specify the irregular retention mechanism

Priority: low; resolve before freezing the generator. Status: `identified`.
“Retained40% of interior integer times” can mean an independent Bernoulli
selection with probability0.4 or an exact-size random subset. Specify which,
including whether selection precedes jitter. Both are feasible; the choice must
precede results because it determines sample-count variation and reproducibility.
No change to the scientific question is requested.

## Inspected hashes

```text
1cef0c1cee7dcfec1a04118752dc6b0750f5e3419b978ed4f58206d8527ba052  studies/river-flow/DESIGN.md
ed3eed51a1dd3c925e81d63c9571000ea858b16a25fa62709bc355ae28b8974e  studies/ecg/DESIGN.md
707cd450c0bd61a92409480fe2bc9b53b4fe5f1678f68326b65110221891f14c  studies/spectral/DESIGN.md
e1a84280cb4f2d7c590b9d508c654f92de8d6d023df13cca113e3a1a024faa3e  src/tsatlas/camels_source.py
9d491002430c73decadc96081b250d2bbfb221ded4718d3b79b858fc05d2cf6a  src/tsatlas/ecg_source.py
16e56c36554bd04fe9dfb24c98706d48eecb1883bfa482a4a297da7b64c76405  data/manifests/river-flow.json
1f3d8c64cc9d177b27501c3929088804b67b16d190f2dfe9d536991a5a136ec1  data/manifests/ecg.json
8426fccd9461d410d2fd76ffe700009b9fdc647eda42271cb1112a471c0ad775  reports/intake/river-flow.json
7744cb5569b699261bc2c3d18d278a6f5965b06c2f0477c89bdb842fff3e7937  reports/intake/ecg.json
392dd930c5a975488d938ae56ee722982c02feca9f32b0bb0a7d8af299295956  data/snapshots/river-daily-panel.csv.gz
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
```

## 2026-10-30 — Design amendments and ECG exclusion audit verified

**C-D03: verified at the design checkpoint.** The spectral generator now states
independent Bernoulli retention with probability0.4 for interior integer times,
followed by the declared jitter, with endpoints retained. No comparison results
were inspected to make this clarification.

**C-D04: verified.** ECG's design and adapter distinguish no-previous-beat
exclusions from waveform boundaries. The reviewer independently recounted
these from the raw annotations: 44 without a prior beat and 12 waveform-edge
exclusions, matching every per-record audit counter. The regenerated NPZ retains
its earlier SHA-256, confirming no retained beat or waveform changed.

The new `folds.json` was independently reconstructed from the declared RNG rule:
all 43 patient assignments and 44 record-to-patient mappings match, with 201/202
together. The revised F1 text explicitly distinguishes fixed-class pooled/fold
denominators from supported-class per-person summaries.

**Final source/design verdict: pass for river flow, ECG, and the supporting
spectral control from the implementation perspective.** Commit the frozen
contracts/mapping before fitting. Their pre-run model implementation reviews
remain separate required checkpoints.

```text
70ea0f6bc5fe539448afc659e898eb72febb92aa777c1be86c4795dbcff34a59  studies/ecg/DESIGN.md
eb205ebe3249cf4a9fd5051e1e2deee086ca80a4c669d45e98890ad01c5be994  studies/spectral/DESIGN.md
3ddc1074feb94ce2f0ad08ca6196c9491035dc8f5f0f1bc5d12af3490bd92186  src/tsatlas/ecg_source.py
1a61640bf69e5cd72bf217ab66065bf618938ad2fb10caaf13053a18bc72bc75  reports/intake/ecg.json
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
2e99a77d11059ba65913b6f91c3f847bd3d5132e1a441592bd0c1fcb2e953562  studies/ecg/folds.json
```
