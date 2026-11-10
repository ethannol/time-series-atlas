# Optional follow-ups: independent results/data review

Date: 2026-11-10. Role: non-authoring automated data/implementation critic.
Scope: every completed follow-up's retained data, arithmetic and provenance.
Verdict: **accepted for this checkpoint; no unresolved data or numerical blocker
identified**. This does not substitute for visual, interpretation, CI or live
publication checks. No full model fits or simulation grids were rerun.

## Exact execution and preservation scope

- Eight final study records use `2446d4b1defbff7b5fd341171d9130381e279eb4`.
  Retail uses `a90ceb16236015edd92f06d67bcb7488c1436bf5` after its presentation
  clarification. The mixed revisions are intentional and independently checked.
- All nine run records' source hashes match their historical committed blobs;
  all declared input hashes match local snapshots, and every current output is
  present in its run record with the correct hash. No undeclared output or
  omitted staged output was found. Each includes the shared follow-up contract.
- Contract SHA-256:
  `e0b36080e9bdd4e61f51b76656e7eff77a46a0c01dd11010eadf68f7434de7bc`.
  Fixed original-output ledger SHA-256:
  `9644e6e9698d21d27d1d824878a11e71f55eb7746c9e16c88cdad12c9451a686`.
- **All 49 original numerical files remain byte-identical** to the fixed
  pre-follow-up ledger and baseline Git blobs. There are **59 new follow-up
  artifacts**: CO2 6, electricity 3, synthetic detection 5, retail 8, oil 1,
  river 0, air quality 1, ECG 27, spectral 8. Presentation edits are separate.
- `optional-retail-presentation.json` records only REPORT.md/run.json changed
  on the targeted rerun. I verified all **13** recorded unchanged retail
  numerical/figure files against current bytes. Earlier arithmetic checks
  remain applicable after that rerun.
- `optional-execution.json` records nine sequential units, 219.09 seconds,
  644,251,648-byte process-lifetime peak RSS, five environment thread caps at
  one and observed OpenMP at one. Accelerate's cap remains an environment
  request, not a directly observed internal thread count. Instrumentation is
  described as completion/timing/pool logging without a scoring/source patch.

## Independent arithmetic and membership reconstruction

Checks below used saved inputs/predictions and independent arithmetic, without
calling the follow-up scoring helpers. Floating comparisons used tight
round-trip tolerances; original-artifact preservation used exact byte hashes.

**CO2:** Reconstructed all 62 linear-model/origin level adjustments from the
source observations and original December predictions; verified all 372
comparison rows, six calibration offsets with 18 residuals apiece, and their
interval endpoints. All calibration outcomes precede the first test origin.
Independently reconstructed all 24 primary/site-target-sensitivity model-horizon
score rows: MAE, signed bias, coverage, width and interval score.

**Retail:** Independently reconstructed all 1,152 weekly medians from the exact
364 preceding calendar days, using the midpoint of sorted weekly totals 26/27.
Verified target totals and fixed 2010 scales. Recomputed all six primary scores,
144 leave-one-code-out scores, 24 quarterly scores, code volume shares and all
24 boundary-week telescoping bias identities. The combined ledger has 6,912
unique product/week/method rows and all 24 exclusions retain every method.

**Electricity:** From original test predictions and training snapshot, checked
all 24 normalized deltas/load shares, 96 customer/method peak MAEs and their
counts, both relative error changes, and the signed-net top-two concentration.
The readable peak table includes all 24 customers. Aggregate error sums signed
customer errors within each hour before taking its absolute value.

**Oil:** Checked all 22 annual count-weighted fixed-minus-EWMA contributions,
separate signed denominators for the two markets, and each market's shares
summing to one while retaining negative contributions. Every 2015–2025 year
is present in the annual report tables. Original outcomes/source-disclosure
boundaries remain unchanged; this review makes no new redistribution claim.

**Air quality / river:** Confirmed identical truth-event copies across methods,
then reconstructed the three duration-specific left/right/both-boundary counts
from one copy. Calendar predictions contain zero high-hour indications. River
has no new numerical artifact; its original evidence remains byte-identical.
Caption rendering and wording receive separate publication review.

**Detection:** Verified 6,400 new first-alarm rows from 3,200 paired streams,
all 32 method/cell summaries with 200 streams each, and all eight original
summary rows. Independently reconstructed every early/postchange/no-alarm count,
eligible denominator, rate, pointwise Wilson interval and conditional median
delay. New configuration thresholds equal the preserved original thresholds;
no recalibration is recorded. Zero-magnitude alarms remain false alarms.

**ECG bootstrap:** Reconstructed the 43-person confusion tensors from original
held-out predictions; checked all 86,000 sampled patient identities against the
declared seeded draws, including repeated-cluster multiplicities. Independently
summed all 8,000 pooled confusion matrices and recomputed 2,000 paired
forest-minus-logistic contrasts, per-method scores and all nine percentile rows.

**ECG assignments:** All three maps match independent seeded permutations of the
same sorted people. Verified **1,207,944** new prediction rows in total: exact
beat/truth/record/person/sample metadata, fold assignment and complete per-method
held-out coverage. Each repeat retains 172,000 capped training-membership rows;
every selected index matches an independently reconstructed fixed-seed cap draw.
Training/test people are disjoint; 201/202 remain together. Verified forest
seeds, one-job settings, audit memberships and all new fold/class support counts.
Recomputed n, accuracy and fixed-four-class macro F1 for all 96 original/new
pooled/fold score rows, 384 class support/precision/recall rows and eight
descriptive ranges, preserving undefined precision/recall.
All 15 new fits are marked complete; the retained failure list is empty.

**Spectral:** Verified 900 saved realizations, 4,500 new procedure rows, all 90
new and 15 matched-band summary rows, cell denominators, absolute errors,
recovery flags, Wilson intervals and tie/ambiguity counts. The original 2,403-point
LS grid is identical; all schedule timestamps/sample counts/spans agree with
their declared conditions. The 900 original-procedure rows are retained in the
1,500-row matched ledger. Independently recomputed all 600 added matched-band FFT
peaks. As a bounded check, recomputed all five peaks/tie counts for replicate zero
in each of the 18 new cells: all 90 procedure results matched. The other new
peaks were audited through saved outcomes/summaries, not refitted exhaustively.

No finding required an implementation change during this results review.
Automated review supplies additional evidence, not independent human scientific
validation, population uncertainty guarantees or deployment validation.
