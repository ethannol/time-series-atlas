# River, ECG and spectral control: source/design statistical review

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: actual river/ECG manifests, intake audits, raw members, compact snapshots,
source adapters and the new river-flow, ECG and spectral draft contracts. The
reviewer did not author the adapters or designs. No forecast, classifier or
spectral comparison was fitted/run. Source extraction checks and mathematical
design inspection are distinct from model performance evidence.

## Separate verdicts

| Investigation | Source verdict | Design verdict |
|---|---|---|
| River flow | Approved for the selected daily observed-flow/Daymet panel and declared QC mask | Approved to implement, with interpretation/invariant requirements below |
| ECG | Waveform/beat population verified; correct the exclusion-reason audit in E01 before source freeze | Clarify E01–E02 before freeze; principal patient-disjoint design is sound |
| Synthetic frequency control | No downloaded source; data-generation contract is the source specification | Clarify S01 before freeze; the explicit alias limitation is sound |

These are the next gated steps within the agreed eight investigations. The
spectral control extends the synthetic investigation; it does not replace ECG
or silently add a ninth required investigation. Earlier synthetic change-detection
results remain unchanged.

## River-flow actual source evidence

The reviewer independently hashed all **114 acquired members** against the
manifest and read the supplied streamflow/forcing readmes. They distinguish
certified daily mean flow (`A`), certified **estimated** daily mean flow (`A:e`),
and missing (`M`, with -999 sentinel). Selecting exactly `A` is an explicit
analysis restriction, not evidence that all estimated measurements are invalid.

For all 17 selected gauges, independent raw parsing reproduced every snapshot
flow value, QC value and selected forcing column. There are **217,328 rows**:
17 complete calendars of 12,784 dates from 1980 through 2014. Missing source
rows remain distinct from source flags. Named precipitation/maximum/minimum
temperature columns match; no snow-water-equivalent/temperature column swap was
found. Actual forcing hours are nominal metadata, not publication timestamps.

The source adapter's cohort decision uses only geography/ID and 1980–1999
approved nonnegative flow coverage. Inspected selected gauges all meet 95%; the
manifest's ordered trial lists retain the failed candidates and the HUC09 absence.
This review verified selected raw values and the trial ledger's ordered
acceptance structure, not a fresh remote selection/download of every candidate.
The bounded member acquisition verifies local member hashes/CRCs; it explicitly
does not claim the entire remote ZIP's MD5 was checked.

The independent training-only threshold check found **no zero high-flow
thresholds** (minimum 6.6 cfs), so the declared persistence-score denominator is
valid for this frozen cohort. The training cold-precipitation proxy has seven
gauges below 0.1 and ten at/above 0.1; it is a descriptive proxy rather than a
hydrological mechanism measurement. These are source/design diagnostics, not
forecast results.

The version/access/license and attribute-origin evidence remains documented in
[preliminary source reconnaissance](source-statistical.md). No full-record
hydrological signature or retrospective future weather enters the proposed
feature set.

## River-flow design assessment and carried-forward invariants

The known-gauge temporal task, separate one-/three-day target offsets, target-date
split, training-only scaler/threshold, calibration-only alert cutoff, shared
information-valid cohort, and limited operational-availability assumption fit
these data. Comparing recall only beside false-positive rate/precision is
essential: calibration to approximately 10% false-positive days is not a promise
of the same test budget. Persistence scores are correctly excluded from Brier
scoring because they are not probabilities.

Onset eligibility may use intervening **outcomes** to define the secondary
retrospective event stratum, but never to decide whether to issue a forecast or
to filter the ordinary high-day evaluation. The three-day eligible-onset subset
differs from the one-day subset. Report both denominators; a difference in recall
is not by itself a measured change in operational warning lead time. Calendar
date offset is especially important because issuance assumes the completed
origin day's values are available only at the following day's start.

Source/QC masks define the population. For example, some selected gauges have
substantial `A:e` periods in the full record. The common seven-day approved-flow
requirement can further remove extended periods and particular regimes. Show
those exclusions by gauge and period; do not claim the remaining observations
represent all flows, seasons, catchments or unobserved flood damage. This is an
accepted scope limitation, not an identified leakage bug.

At implementation review require:

- A future-weather/target perturbation cannot change a saved earlier prediction;
  all rolling windows preserve calendar days and terminate at the origin.
- Calibration rows belong to 2000–2004 by target date; no test truth selects the
  percentile or cutoff. Record actual calibration class counts/false-positive
  rate, including tie behavior.
- The high-day cohort remains identical across methods. If fitting fails,
  preserve the failure and report matched evaluable gauges for method contrasts
  rather than silently comparing different macro populations.
- Unknown truth or absent issued forecasts cannot be compressed into adjacent
  event/alert days. Event ledgers distinguish all starts, missing-truth censoring,
  eligible onsets, alerted onsets and misses. Origin/intervening truth used for
  onset eligibility must not become a model input.

## ECG actual source evidence

The full ZIP hash matches its manifest. All extracted member hashes match the
intake member inventory. The snapshot contains **100,662 finite 60-point
waveforms**, **44 records**, and **43 patient groups**. Records 201 and 202 map
to the same person. The four declared paced records are excluded. Actual record
114's MLII is its second channel, and the adapter selects it by name.

Independent annotation parsing reproduced **every retained sample index,
original symbol, four-group label and previous-RR value**. A bounded sample of
three windows per retained record—132 windows total—was independently extracted
from the declared MLII channel, filtered/resampled and compared exactly to the
snapshot. This is not a claim to have independently regenerated all 100,662
waveform arrays. The retained groups are N=90,072; S=2,781; V=7,007; F=802.

[SciPy resample_poly documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.resample_poly.html)
confirms that the selected operation filters and downsamples the supplied window;
its default boundary extension is zero. The lookahead belongs to that declared
half-second extracted window; no neighboring record or full-record fitted
normalizer is used. The final model must still implement the declared per-beat
normalization and training-only PCA/scaling.

### E01 — Distinguish missing previous RR from waveform-boundary exclusion

**Type:** observed audit-label defect plus incomplete eligibility wording.
**Priority:** small correction before source/design freeze. **Status:** identified.

`ecg_source.py` increments `boundary_excluded` when no previous beat exists,
even when the waveform window is entirely inside the recording. Independent
inspection found **31 such first beats** with valid windows and unavailable RR.
They are legitimately excluded by the proposed RR feature requirement, but
calling all of them waveform-boundary exclusions is inaccurate.

State that absent previous RR excludes an otherwise eligible beat, and separate
the reason/count from true window-boundary exclusions. These reasons can overlap
for some first beats: use an explicit mutually exclusive precedence or clearly
label overlapping counts. The retained population need not change. Check revised
reason totals against all four-group source annotations before freezing.

### E02 — Define zero-denominator F1/precision conventions

**Type:** prospective score-definition gap. **Priority:** clarify before scoring.
**Status:** identified.

The pooled primary uses all four declared classes and is well motivated; the
contract already handles class-absent per-person recall. Specify precision when
no examples are predicted for a class and F1 when `2TP+FP+FN=0`, plus the class
set/denominator used in per-fold/per-person macro summaries. Do not let library
defaults silently turn absent support into observed failure or success. One
defensible rule is explicit null rates with supports and a named supported-class
macro, while retaining the predeclared four-class pooled primary. Another fixed
convention can be used if named clearly; no held-out score should choose it.

The frozen random patient assignment produces all four classes in every test
fold, but support is very uneven: F counts are **30, 6, 755, 7, 4** across folds
0–4, and S counts **623, 362, 67, 1,719, 10**. This is source/split evidence only.
Keep the already specified split rather than improving it after inspecting
support, and show this concentration when interpreting rare-class results.

The training-only cap, PCA and scaler are appropriate; all comparisons should
use the declared capped training membership. Expert localization and prior RR
make this conditional beat-group classification, not an end-to-end detector.
The N group correctly is not called a healthy-heart class. The benchmark's
deliberate enrichment and age prevent prevalence or clinical utility claims.

## Spectral design assessment

The known-truth signal, timestamp-aware Lomb–Scargle, interpolation comparison,
and intentionally incorrect sample-index FFT provide a useful controlled
demonstration. Describe the naive index method as ignoring the timestamp units,
not as a fair implementation of spectral analysis on the true time axis.

[SciPy's Lomb–Scargle documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lombscargle.html)
supports use of actual sample times, angular frequencies and a fitted floating
mean. A well-defined regular Nyquist bound does not generally extend to irregular
sampling by replacing the sampling interval with its average.

For the every-three-second grid, `f=0.17` and `f=1/3-0.17` have the same sampled
cosine span and opposite sampled sine, so their fitted sine/cosine model spaces
are identical. Including both candidates and retaining their powers prevents an
accidental frequency-grid advantage. Lowest-tied-frequency selection is a
deterministic convention, not identification. The contract appropriately refuses
to count an apparent recovery there as proof of physical truth. No spectral
comparison was executed to reach this mathematical conclusion.

### S01 — Freeze how 40% of interior timestamps are retained

**Type:** prospective generation ambiguity. **Priority:** clarify before freeze.
**Status:** identified.

“Retained 40% of interior integer times” could mean independent Bernoulli(0.4)
retention or a fixed-size subset without replacement. Either can support the
question, but they produce different sample-count distributions. Specify the
rule, rounding if fixed-size, and RNG traversal order before generating the
100-replicate conditions. Retain endpoints and apply the declared independent
jitter only to selected interior points. Confirm timestamps remain sorted and
unique and save the actual inputs. No new condition or tuning is requested.

## Inspected SHA-256 identities

```text
1cef0c1cee7dcfec1a04118752dc6b0750f5e3419b978ed4f58206d8527ba052  studies/river-flow/DESIGN.md
ed3eed51a1dd3c925e81d63c9571000ea858b16a25fa62709bc355ae28b8974e  studies/ecg/DESIGN.md
707cd450c0bd61a92409480fe2bc9b53b4fe5f1678f68326b65110221891f14c  studies/spectral/DESIGN.md
8426fccd9461d410d2fd76ffe700009b9fdc647eda42271cb1112a471c0ad775  reports/intake/river-flow.json
7744cb5569b699261bc2c3d18d278a6f5965b06c2f0477c89bdb842fff3e7937  reports/intake/ecg.json
e1a84280cb4f2d7c590b9d508c654f92de8d6d023df13cca113e3a1a024faa3e  src/tsatlas/camels_source.py
9d491002430c73decadc96081b250d2bbfb221ded4718d3b79b858fc05d2cf6a  src/tsatlas/ecg_source.py
16e56c36554bd04fe9dfb24c98706d48eecb1883bfa482a4a297da7b64c76405  data/manifests/river-flow.json
1f3d8c64cc9d177b27501c3929088804b67b16d190f2dfe9d536991a5a136ec1  data/manifests/ecg.json
392dd930c5a975488d938ae56ee722982c02feca9f32b0bb0a7d8af299295956  data/snapshots/river-daily-panel.csv.gz
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
```

2026-10-30, statistical reviewer: river source/design approved within its scope;
ECG source-value verification passed with E01 reason-audit correction pending;
ECG design pending E01–E02 and spectral design pending S01. These are pre-run
gates; no forecast, classifier, or frequency-recovery performance is established.

## 2026-10-30 — ECG and spectral amendments verified

**E01: identified → implemented → verified.** The adapter now applies explicit
nonoverlapping precedence: missing previous beat first, then waveform boundary,
then nonfinite waveform. The corrected audit records 44 no-previous-beat
exclusions, 12 boundary exclusions and zero nonfinite exclusions across the
retained records. Independently checked per-record totals reconcile to every
four-group source annotation. The 100,662-beat snapshot is **byte-identical** to
the previously verified input. The design now explicitly states the missing-RR
exclusion. This corrects provenance labels without changing the analytical
population.

**E02: identified → design amended → verified at contract level.** Pooled and
per-fold macro F1 use all four fixed classes and explicitly record a zero F1
convention for zero denominators. Per-person macro F1 uses only actually
supported classes, with a reported count, and is distinguished from the pooled
denominator. Precision/recall with no predicted/actual support remain null.
This is a clear prospective convention; it does not claim absent classes were
recognized successfully. The implementation must honor these definitions.

The new 43-person fold mapping independently reproduces the specified seeded
permutation/round-robin rule and groups records 201/202 under patient 201. It was
recorded before fitting; the previously observed rare-class concentration is
retained rather than used to optimize the partition.

**S01: identified → design amended → verified at contract level.** The irregular
condition now uses independent Bernoulli(0.4) retention of interior timestamps.
The implementation's committed generation order and saved actual inputs will
provide exact seeded reproduction; no generation or frequency estimate has
been evaluated by this reviewer.

**Updated verdict:** river and ECG source gates and all three design gates are
approved from the statistical perspective. No open blocker remains in this
review. The carried-forward mask, event, transformation and scoring checks still
belong to separate pre-run implementation gates, and no performance claim is
approved by this design review.

```text
70ea0f6bc5fe539448afc659e898eb72febb92aa777c1be86c4795dbcff34a59  studies/ecg/DESIGN.md
eb205ebe3249cf4a9fd5051e1e2deee086ca80a4c669d45e98890ad01c5be994  studies/spectral/DESIGN.md
2e99a77d11059ba65913b6f91c3f847bd3d5132e1a441592bd0c1fcb2e953562  studies/ecg/folds.json
3ddc1074feb94ce2f0ad08ca6196c9491035dc8f5f0f1bc5d12af3490bd92186  src/tsatlas/ecg_source.py
1a61640bf69e5cd72bf217ab66065bf618938ad2fb10caaf13053a18bc72bc75  reports/intake/ecg.json
228644d98e2c549638eb6c464e9fedb338f39c7a6d8f073be9646e8f010ab051  data/snapshots/ecg-beats.npz
```


## 2026-10-30 — Author-identified river boundary risk and verification

After the initial statistical design approval, the author identified a split
boundary problem before implementation: target-date assignment alone permits
the first two horizon-three calibration origins to occur before the last
training outcome, and the first two test origins before the last calibration
outcome. Thresholds/model parameters or calibrated cutoffs would then include
outcomes later than those forecast origins. The earlier statistical pass missed
this boundary risk; it was not an executed-model result or discovered final-score
effect.

The design gate was reopened for this material availability clarification. The
amended contract requires calibration origins `>=1999-12-31` and test origins
`>=2004-12-31`, in addition to target-period membership. Independent date arithmetic
confirms that this removes the first two target dates at h=3 and none at h=1.
All fitted/calibrated outcomes then precede or coincide with the last observed
origin day under the stated next-day issuance assumption.

Status: author identified → design amended → independently verified at contract
level. **River design approval is restored for the amended contract.** Require
the actual implementation to enforce and ledger these boundary exclusions;
target-date-only slicing remains insufficient. No river models were run.

```text
19acfb8f72b093b6ec2b4947c6a7d53f05a4c0f79f800bfda1abf959a62f5021  studies/river-flow/DESIGN.md
```
