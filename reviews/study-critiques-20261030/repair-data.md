# Presentation repairs — data/implementation verification

Reviewer: `/root/repair_data`, non-authoring AI reviewer. Date: 2026-10-30
(Pacific). This is automated scrutiny, not independent human scientific validation.

## Pre-regeneration checkpoint

**Pass for report regeneration; no source, target, split, or scoring blocker
found. Final artifact verification is pending.** This verdict does not claim
that the revised reports or figures have already been regenerated or checked.

Baseline: `71999b34ccfd7127840b173efb287ac0a66b2a26`, parent fetch recorded in
[baseline.json](baseline.json). Reviewer fetched origin again at
`2026-10-31T00:16:10Z`; `origin/main` and HEAD both remained that commit. Branch:
`review/study-critiques-20261030`. Reviewed the author's working-tree changes
against that baseline, after reading `AGENTS.md` and the review protocol.
No instrumentation patch, source edits, fit, full study run, or browser server.
Only this review was written. One bounded saved-evidence check used the locked
environment and one numerical thread; no process remains.

Scope: CO₂, retail, oil, river-flow, air-quality and spectral report changes;
associated README, methods, data provenance, CO₂ design amendment and portfolio
claims. This is a repair review, not a repeat validation of every original model.

### Checks and evidence

- All non-`run` function ASTs in the six edited modules equal the baseline.
  Inspection of every `run` diff found unchanged loading, fitting, target/split
  rules, original predictions, scores, parameters and saved numerical evidence.
  The air-quality concatenation is assigned to a variable before the identical
  CSV save. Added calculations consume results for reports; the new CO₂
  diagnostic adds an evidence file. Actual byte invariance after regeneration
  remains a separate final check.
- CO₂'s inferred origin `(3*p12-p36)/2` is valid because these two linear
  predictions and their origin share the December seasonal effect. The same 13
  test origins have both horizons. Independently calculated origin-gap, growth
  error and total signed-error means are `4.602566, 2.361239, 6.963806` ppm for
  all-history linear and `0.294360, 0.818702, 1.113062` ppm for trailing-decade
  linear. The identity holds within `1e-12`; growth absolute-error means also
  improve (`2.361239` to `0.859580`). The narrative and dated amendment correctly
  distinguish signed-error accounting from MAE decomposition, causality, and an
  unrun anchored-model comparison. Model labels/colors are consistently assigned.
- Retail changes preserve exact case-sensitive identifiers and every numerical
  operation. Report/figure/source text identifies stock-code series and explicitly
  avoids inferring discontinuation or merging possible aliases without a crosswalk.
- River totals reconcile scored plus invalid-union rows to post-boundary
  schedules: `48,262 / 62,084` next-day and `47,877 / 62,050` three-day gauge-days.
  Gauge `09386900` has `200 / 3,652` and `195 / 3,650`; saved three-day weather
  counts are 14 true positives and zero false negatives. Denominators count each
  gauge-target once, not once per model. Equal macro weighting is disclosed.
- Air-quality quarterly high counts and BA support use persistence once, with
  identical true-class and observation counts across methods. Macro BA averages
  only defined station scores. The Q1 24-hour reversal (`0.853231` peer versus
  `0.859873` persistence), zero high hours/undefined BA in 6/24-hour Q3, and peer
  station wins/ties/losses (`9/0/3`, `11/0/1`, `12/0/0`) all match saved evidence.
  Q1's discontinuous calendar span and descriptive status are explicit.
- Spectral's unequal native FFT versus Lomb–Scargle bands/grids are explicit.
  Exactly 6 of 26 irregular interpolation failures select peaks below 0.01 Hz.
  Added sampling/support and alias-power summaries derive from retained records;
  paired power differences are calculated before their maximum is summarized.
  Regular thinning's maximum paired gap is `7.36e-11`. No matched-band experiment
  is implied. The plot limit changes only the displayed frequency range.
- Oil's EWMA inversion and GARCH inversion agree on 2,744/2,745 WTI and
  2,792/2,793 Brent squared magnitudes, with maximum cross-recursion difference
  below `1.2e-12`. The last target lacks a subsequent forecast. The disclosure
  identifies this recoverability without claiming sign/price reconstruction,
  unrestricted reuse, or a demonstrated licence violation. This reviewer makes
  no new legal determination.

### Preflight identities (SHA-256)

```text
6fc101460b493ec18b2d72cfb2f52a1afca500510d197e0b421524c59ac366d9  src/tsatlas/co2.py
ae10477f16983993c073789be6296e7cb6639d868b50cf3ceedfbc10c8bd234a  src/tsatlas/retail.py
d9f7dccf65c42e02f252b14cbe9b18d4337a36b7775dce28c7211bc3d346dc43  src/tsatlas/oil.py
a096c17dc0d95704c5778197476035f3cfe8db187423379d12cdc0832c2749a4  src/tsatlas/river_flow.py
214355e5c3fabdf3de4cf4b44f13829f6b9bb3f51899cc20308614a4a9cb8016  src/tsatlas/air_quality.py
1ee3758793e3483534d5a99fd0fbe648b6322a8de550f190baa6d6efde8bc29e  src/tsatlas/spectral.py
558887e25f0f2e7f3b330f7bfd4b2a05ee30f88485e51dd60346d096f8f3125d  portfolio.json
aff4eab6a6837006ddcded76b517380cdf91bdbb5d3b3f7bfc00034fdf45f081  data/README.md
3625250c2002f5e50bd4dc6e0b18f702dae4294cab5163c45d4aeab70e35b0a5  docs/METHODS.md
94609b45f88fc4389a1dc8ef3c6671131e4258bad32cd6e9490a6408d2eb2992  studies/co2/DESIGN.md
c24844e468b51aa59e2be69102da365dee417a318b7525992781e4cf551cfc53  README.md
```

## Final artifact checkpoint

**Pass for the reviewed data/implementation publication checkpoint.** All seven
required repair findings are verified against the regenerated artifacts below.
This final verdict follows, and does not retrospectively replace, the separate
preflight verdict above. Publication/CI/deployment themselves are outside this
review's scope.

Reviewed regeneration source: `2dee5c82f480637a59489c3043a881dba4c8947b`.
The parent's [regeneration record](../../reports/verification/dedicated-review-regeneration.json)
describes a sequential nine-unit replay in the existing locked checkout, not a
fresh acquisition. A further reviewer fetch left `origin/main` at the original
baseline. This reviewer ran no fits or full replays.

Independent verification used actual Git baseline blobs and current file bytes,
not the author's `unchanged` flags alone:

- The ledger exhaustively covers all 68 original non-`run.json` result artifacts.
  All **48/48 original numerical artifacts are byte-identical**. Exactly nine
  presentation files changed: six reports and the three PNGs listed below.
- All **69 output hashes** across the nine new run manifests match current bytes.
  All **56 distinct recorded source-file identities** match both committed source
  and the current checkout. Every run records the intended source revision,
  stable source during execution, and an empty source patch. The new CO₂
  diagnostic is included in its run manifest.
- Independently rebuilt every numeric field in all **26 CO₂ diagnostic rows**
  from the original predictions and observed origins; all seven numeric columns
  agree within `1e-12`. The report means round correctly. Independently checked
  every added air-quality quarter/station, river-coverage, and spectral
  sampling/paired-power table cell against retained evidence.
- Read all six complete generated reports. Visually inspected all three changed
  PNGs at their saved resolution: CO₂ has consistent cross-panel model colors and
  explicit linear-fit labels; retail names exact stock-code series without
  obscuring scores or bias; spectral shows zero through 0.5, including the newly
  exposed low frequencies. Titles, axes and legends are readable and unclipped.

| Finding | Final disposition and verified evidence |
| --- | --- |
| C01 | **Verified.** Report, diagnostic, design amendment and portfolio distinguish fitted starting level from future growth; no causal or MAE decomposition is claimed. Original scores and predictions are unchanged. |
| RET-01 | **Verified.** Generated report and figure identify stock-code series, preserve case, and explain the unverified alias/discontinuation interpretation. No cohort or outcome change. |
| OIL-01 | **Verified disclosure.** Generated report states the recoverable squared-change recursion beside the source boundary. Reconstruction and archival limitations remain limitations; neither signs/price reconstruction nor a licence finding is asserted. |
| RF-C01 | **Verified.** Observed/scheduled coverage and sparse-gauge counts appear immediately after the macro-score table; original weighting and comparisons are unchanged. |
| AQ-C01 | **Verified.** Generated quarter/station tables expose the reversal, absent high classes and contribution denominators. No retuning or scope replacement. |
| SYN-01 | **Verified.** Unequal bands/grids and six of 26 out-of-band interpolation failures are explicit; plots expose low frequencies and no matched-band counterfactual performance is claimed. |
| SYN-02 | **Verified.** Generated report adds sample-count/span distributions and paired alias-power summaries; original realizations, frequency choices and recovery scores are unchanged. |

I acknowledge every optional **not adopted in this correction round** disposition
in [RESPONSE.md](RESPONSE.md), including the eight-row proposal table. The stated
rationales are compatible with the bounded claims and retained evidence; none
is needed to cure an established result-invalidating defect in this repair scope.
The corrected response accurately says retail concentration and leave-one-code-out
diagnostics were already calculated by its critic and remain available there;
their main-report promotion and proposed new studies are deferred. Optional
experiments and accepted limitations are not being labeled verified fixes.

### Final changed/new artifact identities (SHA-256)

```text
9e713379e19f066dbb30c76f3be119823c675906a895155ad3575762601ca0fc  reports/results/air-quality/REPORT.md
95e62b5cc255cc82b8d1b88d551abd1fbf6a033852fb63d5c9581c82500a1a48  reports/results/co2/REPORT.md
62ecdf2c69175d8f60cfd6a89f85fd4034dc2f965ff9b14653d378bf3dfe2df6  reports/results/co2/forecast-comparison.png
fb5d245e771502879432a98863674ac961ef59daef7d9a2cf7c32b5a30acaa2b  reports/results/co2/origin-level-diagnostic.csv.gz
916e0c357c718619d1c4c229b2a16f526295f7ca7c45fe2381234ab8b33a1255  reports/results/oil/REPORT.md
535a117683357460d5c82d9dce5a2221b44a47c3b9c6e78739a88ad14fc5fd50  reports/results/retail/REPORT.md
a5efea25abdd88987f5952e9141eed160bc716bf7b3dc5cc04a668c5c71100cd  reports/results/retail/weekly-sales.png
e41e5fd9686e2ca8d9407e8932f4ab175322bc30f7e728a27d0a4cd2319e3c91  reports/results/river-flow/REPORT.md
bbcff43d53ad5c321c24a2f975254f8e11d75b649267a2f367e65ef339fc89d3  reports/results/spectral/REPORT.md
76089a638185642295277d68e859dd26d2bcc3a463c77c7f90d31503b42fc3d2  reports/results/spectral/preselected-examples.png
910388c44ebd747924722fde7c8f1ea6036d1980dd2cb33b4696ce6d1fc979dd  reports/verification/dedicated-review-regeneration.json
b8c726d7ec3796e662886cb6731c46f92c94570af824085a93314d562fb3b89a  reviews/study-critiques-20261030/RESPONSE.md
```

Source-file hashes remain those recorded at preflight. No remaining blocker was
found in the scoped implementation, evidence or disclosure repairs.
