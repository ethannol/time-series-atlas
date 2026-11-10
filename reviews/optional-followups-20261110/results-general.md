# General results and presentation review — optional follow-ups

Date: 2026-11-10. Reviewer: non-authoring automated general critic.
Checkpoint: results, interpretation and proposed publication content.

**Accepted within this scope; no unresolved material claim or presentation
blocker identified.** This is not the final completion/publication audit.
CI, final integration, deployed pages and live checks remain pending.

## Scope and evidence

Reviewed the nine study reports' findings and added sections, electricity's
peak-score table, the complete spectral robustness tables, README, portfolio
metadata, the method guide, and all nine studies' new chronological story entries.
Inspected all six new/changed PNGs: CO₂ origin anchoring, retail median, detection
grid, river caption, ECG split sensitivity, and spectral grid. The first four
were inspected during the earlier completed-unit pass; their hashes remain the
same. The final retail report includes the subsequent opening-summary repair.

Also reviewed only the Atlas section/link diff in the isolated profile worktree
`/Users/ethannol/src/side-projects/.profile-atlas-optional-20261110/README.md`.
Its base HEAD/origin/main is `81b7e664cc8b92dbca7027f7264746b403346a20`;
reviewed README SHA-256 is
`b9403b35ec3f0847d45c008d947df29c7573290d2d7d65c432b2f280ffb51a8c`.

Execution was recorded at `2446d4b1defbff7b5fd341171d9130381e279eb4`;
the retail presentation rerun used `a90ceb16236015edd92f06d67bcb7488c1436bf5`,
which was HEAD at the initial content pass. The outputs/documents were then
committed at `5a18c10221d32f051fb8176996129d2e13dc6806`. I also checked the
subsequent working-tree ECG headline-label refinement. The hash appendix
identifies the inspected content, including that final label.

I read the execution, preservation and retail-presentation records, checked ECG
bootstrap/range/status files against their prose, and compared displayed claims
with the report tables. I did not fit, simulate, rerun tests, reconstruct every
metric, rerender figures, operate a browser, or edit source/publication copy.
Numerical reconstruction and implementation audits remain separate technical
reviews. Automated review is additional scrutiny, not human validation.

## Actual findings and interpretation

| Unit | Assessment |
| --- | --- |
| CO₂ | The 6.964→2.361 and 1.119→0.860 ppm three-year MAE comparisons agree with the added table. The recent fit still leads after anchoring. Original comparisons, the earlier algebraic diagnostic and the new intervention remain distinct. Site-target and interval-coverage limitations remain visible. |
| Electricity | +3.89% macro and +2.12% aggregate changes use separate regression as denominator. The 68.57% signed-net concentration and 67.15% load share describe different quantities. The peak table exposes all customers and unequal counts without inventing a new pooled endpoint. |
| Retail | The median's 0.904224 scaled and 23.408 unit MAE beat all five original methods on the full panel. Forecasting 18,002.5 versus 33,858 recorded units supports the roughly 47% shortfall. The all-exclusion table exposes the raw-unit reversal without code 17003; no replacement cohort is selected. |
| Oil | All annual rows show that 2020 WTI and 2022 Brent account for most net EWMA gains, with negative contributions preserved. The copy does not treat annual slices as independent tests or infer trading value. Source and derived-outcome disclosure remains intact. |
| River | The figure and portfolio caption carry reporting assumptions, misses, false alerts and unscored-day context. Matched observed targets, macro high-day recall and pooled eligible-onset recall remain distinct. No new operational result is implied. |
| Air quality | The zero-alert calendar baseline and once-per-duration boundary counts are explained without treating overlapping censoring counts as extra missed events. Equal-station MAE is named. Missing truth and same-hour peer availability remain different boundaries. |
| ECG | All four assignments appear and all new repeats completed. Forest macro F1 spans 0.399527–0.449316 and leads each assignment. Its paired bootstrap 2.5th/97.5th percentiles are −0.026726/+0.114785. The report appropriately limits those percentiles to composition variation conditional on saved predictions and distinguishes whole-procedure split sensitivity. |
| Detection | Overall and eligible conditional denominators appear together. For example, rho=.9/shift=1 CUSUM detects 65/200 overall despite 65/65 conditional detection. No-change alarms remain false after index 200. Pointwise intervals are not presented as simultaneous or paired-difference inference. |
| Sampling | The matched-band table supports 74→79/100 irregular interpolation-FFT recovery. All 18 robustness conditions and five procedures are retained. Regular-thinning recoveries remain analytically ambiguous, so a successful tie-break is not promoted to identification. |

The finite optional inventory is represented in actual outputs. The durable
retail recurrence fixture was present at preflight; this general review does
not independently claim its test execution. Earlier CO₂ color repair remains
historical. Conditional oil artifact removal remains not adopted with disclosure;
no new legal finding is claimed. No broader-method checklist is added here.

## Presentation resolution and accepted limitation

**G-R1, readability recommendation — verified.** In the interim review I noted
that the new retail winner appeared only after the original report's source
footer. Its original-five-method label was already correct, so this was a
visibility improvement, not a scoring defect. The current opening identifies
the dated exploratory result, both median scores and its large volume shortfall,
and links the full section. The following raw-unit paragraph also says “within
that original five-method comparison.” Readers can find the changed answer
without mistaking zero or TSB for the current full-panel six-method winner.
The rerun record reports only REPORT/run changes; the inspected figure is unchanged.

All six images have readable axes, legends, units and primary annotations with
no observed clipping. CO₂ colors remain consistent across panels. Retail shows
error and volume bias from zero-based axes. Detection prints its denominators.
River's assumption travels with its image. Spectral retains all conditions and
prominently qualifies thinning ambiguity, including successful-recovery cells.

**Accepted minor presentation limitation:** fold-number labels overlap in the
dense upper-left ECG support cloud and near the large held-out-F counts. The
main support contrast and score panel remain visible; exact assignment/fold
counts are linked in `followup-fold-support.csv.gz`. This is a support overview,
not a substitute for that table. It does not block the bounded claim or justify
changing the analysis.

## Top-level copy and chronology

README, methods and portfolio acknowledge later exploratory scope, preserve
fixed-panel/revised-data/person-reuse qualifications, and no longer present the
original retail winner as the current complete answer. ECG's consistent split
ranking and bootstrap sign variation coexist without a significance or clinical
claim. Conditional advanced methods remain explicitly unevaluated.

Reviewed the final precision edits too: README now calls the added simulation
conditions a fixed frequency/noise robustness grid; it does not suggest changed
LS bins. The portfolio conclusion says ECG scores varied across patient fold
assignments, avoiding a suggestion that different sets of people were scored.
The ECG headline now explicitly says “original assignment,” matching its
original 0.434 source instead of implying a repeated-assignment summary.
The profile diff removes the unqualified old retail claim, reports the actual
exploratory findings and links their review trail. No unrelated profile section
changes were included in that inspected diff.

Each study story preserves its prospective entry and appends the actual finding.
Agent work is not attributed to an unperformed human review. The native-library
thread repair is described as a pre-run execution defect, not a numerical result.
README distinguishes the existing-checkout extension from the earlier clean
reproduction. Its execution/preservation counts match the linked records: nine
units, 219 seconds, about 614 MiB lifetime peak, 49 original numerical artifacts
unchanged and 59 added outputs. This reconciles records; it is not another
independent byte-level reproduction.

Status history: general interim review identified G-R1 as a recommendation;
the author implemented it at `a90ceb1`; this non-authoring review verified the
generated report. No required source or copy repair remains from this review.
The final extension/publication checklist remains pending the separate final
CI, integration and live-delivery audit.

## Exact inspected content

The canonical sorted compact JSON mapping of these paths to SHA-256 values
has SHA-256 `75a1da955f54274011bf4600e1a6adf5f5bd293febad426e19db52c99d81ac1a`.

| File | SHA-256 |
| --- | --- |
| `README.md` | `0d337deb05262a0e1a315ea21578b07ff5180852f8df95ffe77baa6533b18206` |
| `docs/METHODS.md` | `8cda4464ba2851c9a4231f71d1e4c16745857d4a044d9325990b2d0086492795` |
| `portfolio.json` | `70c7dbdbbc3331cd77d9d7a811c1aa00f8e42c04a711b6bbd209c3e10edb53f8` |
| `reports/results/air-quality/REPORT.md` | `1ff10283dad73e73a09fdf4f5152f1aafcfe6efd6da3a7621a1ef723f51218aa` |
| `reports/results/co2/REPORT.md` | `b0ac5949d3e3aff0c29ba942dedc041b105df9a133047802e35ea4eccf46c861` |
| `reports/results/co2/followup-origin-anchoring.png` | `ebd10d62d289ad6bb1c481ea6bc56e083720660cc31cff67ab24c6def363e1d5` |
| `reports/results/ecg/REPORT.md` | `22cba434dccd26065fca8fc5379251d5a2b52223718639dedfbe66026afdf242` |
| `reports/results/ecg/followup-split-sensitivity.png` | `b7b6709957a2b180b045f96a501484c7c9767de1359cf73c2f0acf02d4429baa` |
| `reports/results/electricity/REPORT.md` | `1d529b0df58406e683f6afd95683f1726124eddcecf9a1201f027408590a7172` |
| `reports/results/electricity/followup-peak-scores.md` | `a03190594a2d40f2f8d8487669d72d72a2b8e8d9779878101c02e04a0f62d677` |
| `reports/results/oil/REPORT.md` | `9f414688cfea84d4e3d31c676dbe835bba7c0def94e86fcbf1777705bb614345` |
| `reports/results/retail/REPORT.md` | `622f49f49fa247ad5173bcbfe0748e79267fbfb840377b70dd8fadcda91f1a25` |
| `reports/results/retail/followup-median-comparison.png` | `e5fcb7ca41a62e36343129dc5d05172b67c56f27257124f40866e0f543683b82` |
| `reports/results/river-flow/REPORT.md` | `e41e5fd9686e2ca8d9407e8932f4ab175322bc30f7e728a27d0a4cd2319e3c91` |
| `reports/results/river-flow/flow-and-onsets.png` | `d6eb0b7d63bd9306fdd652506fa69fd5b44be2b6afdf7ad231540529905ea10a` |
| `reports/results/spectral/REPORT.md` | `8f8ed6aaf336a49d47fed8ec3f6f37900c40b5d2cb275e4c2253830717699b56` |
| `reports/results/spectral/followup-robustness-tables.md` | `eb98d01fe999e8ab525e8cf099a252a55581338b21b7c58df59dfe5cde1e7e2f` |
| `reports/results/spectral/followup-spectral-grid.png` | `ef11aef754c2768657e88cf9661b00ecddd7eba7204f5e2d15952efdabd24135` |
| `reports/results/synthetic/REPORT.md` | `06fea5db74148c968c7968a75f0213c061434d9f637a4f2067207856e3b702b0` |
| `reports/results/synthetic/followup-detection-grid.png` | `26cdef34ac8d17831d70515f2f1736f5adb57f4e37a0992eeff265c013babbdc` |
| `studies/air-quality/STORY.md` | `13d7bdd6d69c476535435c84a073c0768ee706d9591fdaabc0b2ac3493fa5bde` |
| `studies/co2/STORY.md` | `c4a3bac5b1e6f6f1186ecce2261d093b47c644eee42ec1ad9088c2be877d7542` |
| `studies/ecg/STORY.md` | `01ab61bb0a47ab325c1e1dd1fc5f9704243b6b4a10a09c38dc47e1274965a303` |
| `studies/electricity/STORY.md` | `e925f8687ee107b2d7dce6ac8f3afc00937ede574465445b9ca420925ce416f7` |
| `studies/oil/STORY.md` | `a6c8cbdcf0d5a29f29cbde27fe26ffd77f9ec8a7cf29d2f5be116c9636978364` |
| `studies/retail/STORY.md` | `474282efa2d403d3970eecc6ad06f5cf55fa1e2ee6f1145da5771920b669d138` |
| `studies/river-flow/STORY.md` | `7010366f4c785cc78503d373cbbc83bbf0add3dd3aca5a8d31041b0bb8bbce86` |
| `studies/spectral/STORY.md` | `0b32f98f8409d234157ff9556607f42066aade67942878a64ab8a1c28bab6f2b` |
| `studies/synthetic/STORY.md` | `dbd9f3fc495946c05352c57d49541565b22075290a6171c060cf1220219abf5a` |
