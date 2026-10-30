# First-release results and publication review — statistical perspective

Reviewer: `statistical_critic`, an AI subagent that did not author the analyses or result narratives.
Date: 2026-10-30; initial inspected hashes recorded at 16:36 UTC.
Scope: all three saved result sets, generated reports and figures, the root README/story, and the three executed-study stories. I recomputed scores from saved predictions/outcomes without refitting any model or altering final-score-driven choices.

## Separate verdicts

**Results: approved.** Independent calculations reproduce the reported point, interval, customer, aggregate, peak, and detection metrics. Persisted actuals match the pinned source snapshots. The saved paired CO₂ differences also match independent calculation. All run-output hashes match their respective recorded manifests. No numerical-results blocker was found.

**Publication: statistical claims approved with the low-priority copy clarifications below.** The bounded origin/population scope, small overlapping CO₂ evaluation, conditional detection denominators, and lack of operational/clinical benefit claims are represented honestly. This review does not establish general scientific validity beyond the declared comparisons or constitute independent human validation. Other required publication perspectives remain separate.

## Independent checks and results

All three run records identify source commit `5953a7f6426bb44ddb2433153ce0c54038b6eb90`, protocol commit `b374e9baa39f021481aefaefba958543534c916f`, and stable source during execution. I independently checked the output-file hashes listed in each record. This verifies the saved artifacts against the recorded evidence; it is not a new execution of the model fits.

### CO₂

I recomputed every model/horizon point score, interval coverage, width, and interval score for the test population and the site-target exclusion sensitivity. I recomputed signed calibration-error quantiles and checked that saved interval endpoints equal prediction plus those offsets; each calibration target precedes the first test origin. The saved actual values match the monthly-average column in the pinned input.

The primary three-year comparison has 13 December-origin forecasts:

| Model | Recomputed MAE ppm | Interval coverage | Interval width ppm | Interval score |
| --- | ---: | ---: | ---: | ---: |
| Expanding linear | 6.963806 | 0/13 | 4.560618 | 41.359220 |
| Trailing 120-month linear | 1.118816 | 13/13 | 4.001049 | 4.001049 |
| Expanding quadratic | 1.605715 | 13/13 | 4.584443 | 4.584443 |

Both changing-growth procedures beat the substantive expanding-linear baseline in absolute error at every one of the 13 evaluated origins. Excluding the substituted-site target yields MAEs approximately 6.925901, 1.211324, and 1.662448 ppm respectively, preserving the ordering.

The 0% and 100% coverage figures are correct empirical counts, not guarantees. The report keeps the small sample, overlapping forecast errors, widths, and proper interval scores visible. The site sensitivity is correctly described as removing affected targets, not all later training influence. The January/December target limitation and revised-data status prevent an unsupported all-month or historical-live-vintage claim.

### Electricity

I independently recomputed customer MAE/bias, fixed-2012-scale normalized MAE, peak counts/errors using the fixed 2012 percentile thresholds, macro summaries, and aggregate errors after summing customers. Checks covered both 2013 development and 2014 evaluation outputs, for primary-safe dates and the all-date sensitivity. Saved hourly targets match the pinned panel; customer/hour keys are unique, every scored hour has all 24 clients, and all saved predictions/actuals are finite.

Primary 2014 macro normalized MAE is 0.0983150154 for local Ridge and 0.1021403718 for pooled Ridge. The pooled model improves 3 customers and worsens 21. Its gains in normalized MAE are small:

| Customer | Pooled minus local normalized MAE |
| --- | ---: |
| MT_302 | -0.0000004893 |
| MT_210 | -0.0001610189 |
| MT_166 | -0.0003064225 |

The maximum deterioration is approximately +0.0329907204. These are score differences, not percentage changes or established business value. The story appropriately describes this as one specified regression comparison on a deliberately selected panel rather than a general rejection of pooling.

The full-date sensitivity also favors local models on macro and aggregate measures and still has 3 customer improvements, but its improved-customer set differs: MT_198 replaces MT_302. No additional model, cohort, or parameter search was performed in this review.

### Synthetic change detection

I reconstructed every outcome partition and conditional score from the saved replicate records. Each method/condition has 200 unique replicate IDs. Saved threshold values match the specified higher 95th-percentile calculation over the retained calibration maxima.

CUSUM raises alerts in 10/200 no-change IID streams and 146/200 no-change AR streams: 5% and 73%. In the changed AR condition, 77/200 trials alarm before the change; the remaining 123/200 are detected after it, with conditional median delay 12. Thus 100% detection among eligible streams is not 100% successful detection among all changed streams. The report, figure, and story keep this conditioning and the early-alarm counts explicit. The reported short delay does not establish a useful field warning system.

## Publication clarifications

### P-STAT-01 — Update current data summaries after execution

**Priority:** low; documentation consistency.

The undated/current Data paragraphs in the CO₂, electricity, and synthetic stories still refer to the snapshot, aggregation, or seeds as awaiting specification, despite the updated executed status. Replace those current summaries with the actual pinned/declared setup. Preserve the dated historical planning entries rather than rewriting their chronology. The README's future-tense redistribution statement can likewise distinguish the included first-release snapshots from later datasets still awaiting intake.

### P-STAT-02 — Specify what the sensitivity ordering preserves

**Priority:** low; interpretation precision.

The electricity story's statement that “the same ordering” holds on excluded dates is true for macro/aggregate model ranking. It is not true for every customer's winner identity. State the overall-ranking scope explicitly; optionally mention that one of the three small-gain identities changes. This supports the existing caution against treating a win count as decisive.

### P-STAT-03 — Make small customer differences easier to inspect

**Priority:** optional presentation improvement; not a score defect.

The electricity scatter is numerically correct, but a high normalized-error customer compresses most points near the diagonal. A compact difference table or linked per-customer comparison would make the tiny gains and larger losses easier to read. The preserved metrics and explicit story already avoid a false practical-significance claim. Any added view should be rendered from the frozen predictions, without refitting or selecting new models.

## Figure inspection

I viewed all three generated PNGs. CO₂ axes identify December origins and the direction of error differences. Electricity distinguishes individual normalized error from aggregate kW error. The synthetic figure labels the 300-point no-change window and conditions detection on no early alarm; its adjacent report supplies the excluded-trial counts. No mislabeled metric or contradictory plotted conclusion was found.

## Inspected SHA-256 hashes

```text
8fc3d871e01d53f2a43076888c46788d23ba494f77243cd8b1e426029b4ae783  reports/results/co2/REPORT.md
d75ced7a440c5dfb50e4ac926ba464651169ed6f3bf1455f06b8712409ed5b68  reports/results/co2/forecast-comparison.png
36e0cef9a2e517645a44fb78de94bfddf716342a5f031ed4f897b68764c2deb9  reports/results/co2/metrics.json
b056a41321a6a1fac51abbdf6b20f7bfc1d9b755151fa0a7bd663f1827d8016f  reports/results/co2/paired-error-differences.csv.gz
90d3993ef871868520c3ef127960fea235431ac872640224397394db9b8eadaa  reports/results/co2/predictions.csv.gz
25a2f9bf21be6dc1621656b0e9ee327dc3b1f6565953fe132c895ff061472c98  reports/results/co2/run.json
5d9ba50ea685c9d1845890d18c0eb23d1106d78d496bfc125a1c3a1d778bf0a8  reports/results/electricity/REPORT.md
eea0c9d198bbbedd09910f407b41bf74ddac16e13e32eb450c870226cd0ab0db  reports/results/electricity/metrics.json
86e69932a5f36660cf85e5b304827111cc501cf4149cf4f28935359d4b463729  reports/results/electricity/parameters.json
7e71f1aaaf378c9007bb73fd3bdd279112c722ee06467d7c4b4ce0bc62624e6a  reports/results/electricity/pooling-comparison.png
d5d006d4ab30f8971290845ece0068bbae075eda9c03c03d1d76238f672c1a09  reports/results/electricity/predictions.csv.gz
b8031cce8180102e2b5250c540b800872cb93c03157f989c74baec004ffbb327  reports/results/electricity/run.json
3cb24ba485d15fe68c1e8ab59152a5bf30b289d0e53a2939f33fc4ee110b3b8c  reports/results/synthetic/REPORT.md
74830249eb8de5f54433487a0470e9a5bce5a48b708ad6a905c3fea420bda997  reports/results/synthetic/detection-comparison.png
17eb15c6a025db3dad0536ff9579e1f201392472e790d58d54b44188ea44aeec  reports/results/synthetic/metrics.json
b7265351f8b0b730057915777b33dcc5eeb4f53aa3ba05db86f6336851b8c75a  reports/results/synthetic/replicates.csv.gz
5e881497079185936e8e3df6a51e3e7d0d8bd3d778d727dc1d479158ba9878df  reports/results/synthetic/run.json
98d97913845ab4c0fe14197575e04891efc93c98ae50eb05faf47cd2d5e09340  README.md
7b8cd81a31341592f887ddf817ccfe8767a5da635b12018e776018647d54b99a  STORY.md
c54a16b0f372f66106fb8b17e43cd68983a0f440b1c324711b017a02d32d1f7e  studies/co2/STORY.md
9cc41a6a3b77a61d245c9b118f91bcd0073446c86422dbeebe584402216e6a7c  studies/electricity/STORY.md
489359c70dab3b78b32d7f61a4b12f67d5f96ddf51cfd7510778988e74f6635e  studies/synthetic/STORY.md
```

## 2026-10-30 — Copy and presentation correction verification

I inspected the changed story summaries, README, and report-rendering source diffs against the executed source revision `5953a7f6426bb44ddb2433153ce0c54038b6eb90`.

**Verdict: approve the revised wording and presentation source without reopening analytical choices.** The computation prefixes through scoring/output calculation in all three study modules are byte-for-byte unchanged. The changes add readable conclusions/labels, a customer-level difference plot and saved comparison table, and sample units for synthetic delay. No model, split, mask, calibration, threshold, scoring rule, or tuning choice changed in response to final scores.

- P-STAT-01: all three study Data summaries now describe the pinned/aggregated/generated inputs actually used. Their dated planning entries remain preserved. The README's broad future-tense redistribution sentence still needs the minor scope qualification noted above; this is a wording issue, not a change to the statistical results.
- P-STAT-02: the electricity story now explicitly limits preserved sensitivity ordering to overall model ranking and mentions the changed identity of one tiny-gain customer. This matches the recomputed evidence.
- P-STAT-03: the renderer now exposes signed customer-level differences and saves an exact comparison table. That addresses the readability concern in source; the actual new figure and artifact must still be inspected after generation.

The updated CO₂ conclusion matches the already checked origin-by-origin results. The synthetic headline remains qualified to the stress test, and delay is labelled in samples. The README also explicitly attributes implementation and execution to agents rather than inventing human authorship.

This is approval of the unchanged analytical choices and the inspected presentation changes. Final regenerated output hashes, table values, and figures remain pending the next output check. The separate evidence-validator repair is outside this narrow statistical copy/diff pass and requires its own implementation review; its existence is not treated here as verified behavior.

Inspected hashes for this pass:

```text
6a652546f1a67f658e99cfc5808c341505b83a3f04bdac1082468c99cec98c0a  src/tsatlas/co2.py
bff038460bc7cba8996c999b22a327101d9252ed123be5054071af3946a5b43f  src/tsatlas/electricity.py
7974c9d74ab57f4db295e8b6008b28acf675cc91b4e2d85fe39ea5caa61ac8fc  src/tsatlas/synthetic.py
f758bcf6402aa0b09dd6601ac0a946b5b8bcabee90b524d52a9fcdeaf1e23007  README.md
fc2a946b768c3db213375ba2dcf1820eb671d7f60afb79175d97677472f7503f  studies/co2/STORY.md
bac79f08d741a51b6f177cd4469d282fcf38fc173421e605dd25067251626b00  studies/electricity/STORY.md
c25add0a5944cbf16da3bcc19bff7d744eddc8b9aa7512868c10d5d1060872d5  studies/synthetic/STORY.md
```

## 2026-10-30 — Final regenerated-output and integration verification

I inspected the final regenerated output recorded at commit `d20c0ccf2d458986ad99afbd7b01569b6cd86fbd`, whose run evidence identifies source `b607f9f410dec080388b84163f6ca073c6630607` and the unchanged protocol commit `b374e9baa39f021481aefaefba958543534c916f`. I also reviewed `portfolio.json` and the proposed GitHub-profile README for claims about this project. No model was fitted by this reviewer.

**Final results verdict: approved. Final statistical publication verdict: approved, including the inspected portfolio/profile integration claims. No statistical blocker remains.**

I compared the regenerated metric files and saved predictions/replicate outcomes directly with their Git bytes at `4a3022c` (the archived results from source `5953a7f`). They are byte-for-byte identical for all three studies. Electricity model parameters and the CO₂ paired-error-difference file are also identical. Every output hash in each new run manifest matches the final file. Thus the previously independently recomputed results remain unchanged after the presentation/evidence update.

The new electricity customer-comparison table has one row for each of the 24 customers. I independently checked its local error, pooled error, and signed difference against the unchanged metrics. I viewed the regenerated figure: customer IDs, signed labels, negative/positive directions, and aggregate comparison agree with that table. It makes the tiny improvements and larger deteriorations visible without changing the comparison population or scoring.

P-STAT-01 is resolved: current study summaries describe the actual setup, and the README distinguishes the first-release snapshot basis from later datasets' pending intake. P-STAT-02 is resolved: the electricity story/report distinguish preserved overall ranking from the changed identity of one small-gain customer. P-STAT-03 is addressed by the verified labelled difference view and exact comparison table.

The reports' plain-language conclusions match the unchanged results. Synthetic delay now has explicit sample units, and its conditional nature remains visible. The portfolio card and GitHub-profile text describe the selected electricity panel, bounded CO₂ comparison, and synthetic detection stress test without claiming universal rankings, realized savings, clinical benefit, completion of planned datasets, or human validation of agent work. Ledger-backed headline quantities are consistent with the reviewed metrics; portfolio-builder rendering and publication mechanics are outside this statistical check.

Relevant final artifact hashes (unchanged numerical artifacts retain the hashes recorded earlier):

```text
0529ea280461ce3e002cb89abc27f6d32e1d794aaaf5302791621b4db927f682  reports/results/co2/REPORT.md
c51c73977e13304a8106e37f5afd419ebf40bf940561e9e6cce47d2f72d63826  reports/results/co2/run.json
34ddc6041e119e23be8a2b31d60121e1fab1c57a11036ca4cf01d29a4fbadf1f  reports/results/electricity/REPORT.md
114034594c046b771f5d9b3386e0ce6315332551103096b84cc4aa35023f979b  reports/results/electricity/customer-comparison.csv.gz
c4369754e5402e7f18b8592b27c7b22d5d5be5eedf81bd552d4439028e4454d2  reports/results/electricity/pooling-comparison.png
43a55431f786690ecd605ea71cd4d42e7a4aff821a38168b56672853405f0204  reports/results/electricity/run.json
ec3778a38a65578015cc44168de506c926b866d4e078cc4eb2c9d5e303a16476  reports/results/synthetic/REPORT.md
c77320ad4f5cd842afce8991f2802a85a95fc981b6dcf0b015df4fc2594657b1  reports/results/synthetic/run.json
ab27a5138fb5e9e969019f69a775f1de2b62e9b6cef19f24b0219cf83a2bb9f3  README.md
5ac08ff58dd4bc552693ecd50ad8d11226995fbf6c0a7f9d295fd9f6035635a3  portfolio.json
d9578ca794e903c3a74553446c18450f0c7930a8fe3e34653f7144f3cd934b3b  ../github-profile-tsatlas-20261030/README.md
fc2a946b768c3db213375ba2dcf1820eb671d7f60afb79175d97677472f7503f  studies/co2/STORY.md
bac79f08d741a51b6f177cd4469d282fcf38fc173421e605dd25067251626b00  studies/electricity/STORY.md
c25add0a5944cbf16da3bcc19bff7d744eddc8b9aa7512868c10d5d1060872d5  studies/synthetic/STORY.md
```
