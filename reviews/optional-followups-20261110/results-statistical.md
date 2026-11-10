# Optional follow-ups: independent statistical results review

- Reviewer: non-authoring automated statistical critic; 2026-11-10.
- Full-run source: `2446d4b1defbff7b5fd341171d9130381e279eb4`.
- Retail presentation rerun: `a90ceb16236015edd92f06d67bcb7488c1436bf5`.
- Baseline: `1a0ec0180b857f7d98b092a8104a575657d53445`; a fresh review-time
  fetch left `origin/main` unchanged. The running suite retained its frozen source.
- Contract SHA-256:
  `e0b36080e9bdd4e61f51b76656e7eff77a46a0c01dd11010eadf68f7434de7bc`.

## Verdict

**PASS: numerical results and reviewed interpretation. Required corrections:
none remaining.** All nine completed units were reviewed. Initial retail opening
ambiguity and two small top-level wording issues were corrected and independently
rechecked below. No new fits, data generation, tuning, or full simulation replay
was performed by this reviewer. Publication/CI/deployment gates remain separate.

Reconstruction used short one-thread Python processes, streaming larger tables
in 40,000–50,000-row chunks. Computations used retained rows and direct arithmetic,
not the new score-summary helpers. All 49 original numerical files were independently
hashed against the baseline and remain byte-identical. Run output hashes matched
every reviewed artifact; the retail rerun's 13 unchanged outputs also matched.

## Independent reconstruction

- **CO₂:** Reconstructed every anchored forecast from original p12/p36 and the
  pinned observed origin. Original targets match. Recomputed all calibration
  offsets by sorted residual interpolation and all 24 model/horizon/sample score
  sets: count, MAE, bias, coverage, width and interval score. Calibration targets
  precede test origins. Target-site sensitivity preserves the calibrated intervals.
- **Retail:** Reconstructed all 1,152 weekly medians from calendar-aligned daily
  inputs, all targets and fixed 2010 scales. Recomputed six primary score rows,
  144 leave-one-code-out rows and 24 quarterly rows. Checked all 24 telescoping
  bias identities. All six methods retain the same 24 codes and 48 target weeks.
- **Electricity:** Independently reconstructed all 24 normalized deltas, safe-hour
  load shares, both relative error changes and the signed-net concentration share.
  Pooled macro error rises 3.8909%, aggregate error 2.1165%; the two largest
  positive normalized deltas contribute 68.5673% of the signed net delta.
- **Oil:** All 22 market/year contribution rows reproduce count-weighted
  fixed-minus-EWMA QLIKE differences and within-market signed shares. All years,
  including negative contributions, remain. Earlier implementation reconstruction
  verified that weighted annual means equal the original pooled QLIKE scores.
- **River/air:** Original numerical artifacts remain unchanged. Air's three
  censoring summaries match every method's copy of the same true events; counting
  one copy avoids model duplication. Calendar predictions produce zero high-hour
  indications. The 6-hour counts are 31 true runs, 17 left, 23 right and 17 both:
  overlapping censoring is retained, not added to missed events. River caption
  limitations preserve the existing daily-input assumption and scoring scope.
- **Detection:** All 6,400 method rows represent 3,200 distinct shared streams,
  exactly two methods per realization. Independently reconstructed all 32 new
  and eight original method/cell summaries, including first-alarm partitions,
  both denominators, misses, detected-delay medians and Wilson intervals (checked
  via the equivalent score-test quadratic). Original thresholds are unchanged.
- **ECG:** Streamed original plus all three repeat prediction files. Every model
  has all 100,662 held-out beats exactly once per assignment, with matching truth,
  person and fold. All repeat mappings match their declared seeded permutations;
  saved training memberships exclude the held-out people and respect the cap.
  All 15 fit audits completed. Reconstructed 16 assignment/model scores, 96
  pooled/fold scores and all 384 class rows, including undefined rates. Rebuilt
  all 172 patient confusion matrices from predictions. Verified the saved 2,000
  draw vectors against the declared seed and their patient IDs; their multiplicity
  weights reproduce all 8,000 saved confusion matrices, all bootstrap scores,
  paired differences and nine percentile summaries. No new bootstrap sample or
  model fit was substituted for the saved evidence.
- **Spectral:** All 1,500 original-plus-comparator rows and 4,500 new method rows
  reproduce their errors, recovery flags and analytic ambiguity indicators.
  Recomputed all 105 cell summaries and Wilson intervals. Original 900 procedure
  rows are preserved; all 600 added matched-band FFT peaks match direct FFTs of
  the 300 original inputs. The new input ledger contains 900 aligned, finite,
  increasing-time realizations with correct recorded sample counts/spans. As a
  bounded computational check, recomputed all five procedures for preselected
  replicate zero in each of the 18 new cells; peaks/ties matched. The 2,403-point
  LS grid equals the saved original grid. No complete new-grid replay was run.

## What the results support, and what they do not

- **Anchoring materially changes the comparison's scale.** Three-year MAE falls
  from 6.964 to 2.361 ppm for the expanding linear model and 1.119 to 0.860 for the
  recent model. The recent model still leads with both anchored. This is a fixed
  procedural comparison on revised historical data, not atmospheric causal
  attribution. Improved point forecasts do not imply reliable intervals: the
  anchored expanding model covers only 1/13 three-year targets; both anchored
  one-month intervals cover fewer than 60%. The tables and story retain this limit.
- **Retail error improvements do not remove substantial volume shortfall.**
  Median scaled MAE is 0.904224 and unit MAE 23.407552, lowest among all six methods;
  its 18,002.5 forecast units are 46.8294% below 33,858 recorded units. It leads
  both scores in every scored quarter. It leads scaled error for every code
  exclusion, but removing `17003` changes the unit-error winner to `rolling_28`.
  These dependent slices establish neither an inventory policy nor population
  superiority; no replacement cohort was chosen.
- **ECG supports bounded sensitivity statements.** Forest macro F1 ranges from
  0.399527 to 0.449316 and exceeds logistic under all four assignments. The paired
  conditional bootstrap difference percentiles are -0.026726, 0.045708, 0.114785.
  Both signs occur in that conditional patient-composition distribution; neither
  a superiority test nor a population confidence interval follows. Fixed saved
  predictions omit training uncertainty, and repeats reuse the same people.
- **Detection conditioning remains consequential.** At rho .9 and shift 1,
  CUSUM detects 65/200 overall but 65/65 among eligible streams; 135 early alarms
  account for the difference. At rho .9 its no-change false-alert fraction is
  185/200. Pointwise intervals condition on the frozen calibration and do not
  establish simultaneous coverage, paired method inference or field reliability.
- **Matched bands improve one spectral result, not identification generally.**
  Original irregular interpolation recovery changes from 74/100 to 79/100.
  Regular three-second sampling at .08325 Hz can recover all 50 planted values
  while retaining aliases. At .17/.28725 Hz the same ambiguity persists despite
  different recovery rates. All settings and numerical ties remain visible;
  unchanged bins/grids and the stated signal generator limit method rankings.

## Interpretation and presentation follow-through

Reviewed README, portfolio, method guide, affected study stories, reports and
CO₂/retail/detection figures. Their numerical summaries and exploratory limits
agree with the retained evidence. The retail chart visibly preserves its large
negative volume bias; detection panels label different denominators explicitly.

The initial retail opening left the raw-unit winner insufficiently qualified.
The dated six-method opening now states the median result and forecast/recorded
totals; the TSB statement explicitly applies to the original five methods.
The rerun changed only `REPORT.md` and `run.json`, independently verified.
Two suggested top-level precision improvements were also observed: README now
says “fixed frequency/noise robustness grid,” avoiding an implication that the
LS search grid changed; portfolio now says ECG scores varied across patient fold
assignments, rather than implying a different overall held-out patient cohort.
No unsupported superiority, clinical, causal or inventory-policy claim remains
in the reviewed optional-follow-up copy. Automated review is additional scrutiny,
not independent human scientific validation.

## Exact evidence identifiers

Run metadata hashes identify the complete output hash maps used in this review:

| Unit | `run.json` SHA-256 |
| --- | --- |
| CO₂ | `5423417c375d337e1828ba07332398d532010139cc0d926c06fd2c388895a87f` |
| Electricity | `2b7715d00e1193ed3f21fd34d5297e9434168dd76de2644583a03754a1861703` |
| Retail, final | `cd609371e6148979127f7be63efda6c736630612bd711fb04d78999f8212f414` |
| Oil | `c1d1d5a4b6fde2be52f2af5631872eda3e63044a25d708f9b818c13c953bef00` |
| River | `04f48ba114c85a7d0dc9249e6c41abcc2d0c5f429479442d53caf4854e33afef` |
| Air | `6ae3b6f78622d1cafe2e8ddb9c2412b0d82526b1cb97e5b511d865e40369c6c7` |
| ECG | `a2f1b7f2cfc2125979803d6b35eb89db442d545ad3f774801801618990f2e785` |
| Detection | `db12a3f082b8a630acb7985bd0874f7d6b5b4c411bb0265b75e31afb9c82a725` |
| Spectral | `25d4a3bbe667b3543b57dd6df8c8cb53252e42e6b1063d1f6463013081c25107` |

Reviewed top-level content SHA-256: README
`0d337deb05262a0e1a315ea21578b07ff5180852f8df95ffe77baa6533b18206`;
portfolio `5aa902267babb8860427ef9b8c92d728430ecff7e74555eec7d3ca183edd4638`;
method guide `8cda4464ba2851c9a4231f71d1e4c16745857d4a044d9325990b2d0086492795`.
