# Final publication review: statistical claims and evidence

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: the nine current reports, study-story endpoints, root README/story,
method guide, portfolio metadata, source credits, review reconciliation and
the Atlas material in the separate GitHub-profile draft. The reviewer did not
author these materials. No models were refitted in this final pass.

**Statistical/claims content verdict: approved.** The results presentation
findings listed below are closed for the inspected files. No remaining
statistical interpretation or denominator blocker was identified in this scope.
**This is not overall completion or deployment approval:** final clean-checkout
reproduction, final-suite tests/CI, portfolio build and live publication remain
separate pending gates, as the evidence matrix currently states.

## Numerical continuity was independently checked

The reviewer compared current file bytes directly with the Git objects named in
the two presentation-comparison records, rather than relying only on their
author-written lists:

- All 34 numerical artifacts in `completion-presentation-refresh.json` equal
  their versions at `2c0af60037ae691aae7e13c92cb37228215e5876`.
- All 13 in `completion-presentation-final.json` equal their versions at
  `f14924eb7de588721a0d12021cb35521ec928a2f`.
- These lists overlap: they cover **39 distinct numerical files**, not 47
  independent files.
- Every current output hash in all nine run records matches the actual file.

Consequently, the prior independent numerical audits still apply after the
presentation revisions. This pass did not repeat those full audits or treat
byte equality as a substitute for the upcoming independent checkout execution.

Portfolio source references resolve correctly: CO₂ recent/expanding three-year
MAE is 1.11881585081595/6.963805866697118 ppm; ECG forest/majority macro F1 is
0.43401845977482834/0.23611941237534997; electricity has 21 customers worsened by
pooling. The newly added river subgroup prose also matches its retained table:
ten higher-cold-fraction gauges have three-day weather-model macro recall
0.8579368 and FPR 0.1648154, versus seven lower-group gauges at 0.5281458 and
0.1196499. Its descriptive, noncausal interpretation is appropriate.

## Prior presentation findings closed

| Prior finding | Final evidence and disposition |
| --- | --- |
| Retail current data/story wording and metric interpretation | Daily/weekly aggregation is explicit; the report and new story entry explain zero's normalized-error result, TSB's raw-unit result and the absence of stockout/cost evidence. Closed. |
| Oil OP01 | The report leads with QLIKE improvement, direction's worse Brier score, the secondary-loss reversal and the small GARCH/EWMA gap. Current story and fetch-only limitations are explicit. Closed. |
| Air AP01 | The report directly answers the nowcasting question and distinguishes concentration error from alert classification; the story describes the actual findings. Closed. |
| Air AP02 | Delay is labeled in hours, undefined values are readable, misses and conditional-delay counts remain together, near-overlapping methods have different markers/styles, and zero false episodes is distinguished from zero false-positive hours. Closed. |
| River RF-P01 | The report states modest weather gains, 496/822 versus 467/822 eligible next-day onsets, the single extra longer-offset onset, and false-alert burden. Current 17-gauge status/story and quality/coverage links are present. Closed. |
| ECG ECG-P01 | The report leads with zero correctly recognized F beats, 10.9% S recall, near-majority accuracy and the 755-test/14-training F support imbalance. Current story preserves the frozen grouping/cap and expert-location boundary. Closed. |
| Spectral SP-P01 | The report/story state irregular recovery counts 100/74/0 and the two tied peaks in every thinned replicate; zero recovery under the lowest-alias rule is correctly separated from identification. Closed. |
| Spectral SP-P02 | The updated right-panel title explicitly names Lomb–Scargle. Closed after visual inspection. |

The updated retail, air and spectral figures were visually inspected in this
pass. Earlier figure audits and the unchanged numerical evidence support the
remaining display checks. The river report now describes different high-day and
onset recall populations rather than inferring relative intrinsic difficulty
from differently weighted rates.

## Collection-level interpretation and scope

The README, method guide, portfolio and profile Atlas section accurately describe
seven real-data investigations plus synthetic controls: eight investigations,
with detection and sampling as two execution units. Conditional Bayesian/neural,
reconciliation, ungauged-transfer, cointegration and automatic beat-detection
extensions are clearly not performed. There is no invented common leaderboard.

Units and information boundaries remain tied to each question: revised
December-origin CO₂ hindcasts and ppm errors; hourly mean electricity power,
customer-normalized errors and nominal clocks; gross retail sales rather than
latent demand; next-observation dollar changes and task-specific oil losses;
river daily date offsets rather than measured hourly warning; same-hour peer
air-quality inputs and µg/m³ error; annotation-centered ECG classification with
post-center waveform information; sample-count delays and hertz in the synthetic
controls. No operational reporting-time, financial return, causal, clinical or
universal-ranking conclusion is added by the summaries.

The source credits distinguish modified extracts from source databases, preserve
attribution/licensing statements, and explain oil's fetch-only restriction and
possible historical revisions. CAMELS verification is limited to acquired ZIP
members rather than claiming a checksum of the full archive. The amended oil
instructions distinguish normalized-input acquisition from intake of original
pinned workbooks. This pass checks consistency with the earlier source reviews;
it is not a new independent legal opinion or proof that public endpoints will
retain identical data forever.

The review reconciliation preserves initial design risks, source facts, actual
implementation/copy defects and verified fixes as different categories. It credits
the lead agent with discovering the river-boundary and spectral-grid issues that
earlier reviews missed. The original premature stopping and recovered spectral
scope remain visible. AI scrutiny is explicitly distinguished from independent
human scientific validation.

The profile review is scoped to its new Atlas description and attribution of AI
work. The biography and unrelated older projects were not independently
revalidated here. The new wording does not invent Ethan's review of work performed
by the agents and retains the oil-input availability limit.

## Two additional copy findings, corrected during this pass

1. The synthetic story's current status still called the spectral control
   outstanding despite the completed dated entry. The author updated it to
   executed with independent numerical review; the reviewer checked the new text.
2. The electricity row in the method guide said “score people.” It now says
   “score customers,” matching the observational unit; the reviewer verified it.

These were actual documentation inconsistencies, not errors in the numerical
results. The final portfolio information-boundary wording also distinguishes
forecast/nowcast cutoffs from ECG's declared post-center classification window.
No analytical setting changed as part of these corrections.

The original results reviews remain chronological records of what was pending
when written. This final record closes their content findings; it does not
retroactively make reproduction, CI or publication complete.

## Inspected SHA-256 identities

The profile path identifies the draft inspected; it is not a claim that the
GitHub profile or portfolio site has already been updated.

```text
fe0610428be8a08f663a3ebc847b17fae46d7161e070f27a573f8dd44607b788 README.md
ab916992005846c053bf36b5bc301809253f1ae4aa59ac66853ebe2228d9090a docs/METHODS.md
9dc9066c3810b15df1cfb2750b1cce0059917c200a063dd7aab176ad31f0b0bc portfolio.json
e499446dce1b1329f668fc83c83353c326f52602e9910c0e0f5491ef13424d80 data/README.md
1d9887d0bc1aceaec3395d75dcea6ae0c42a17071cd9ed8e1f0169b06c3a8928 STORY.md
ef4deeea0578a8e38ad07958b33bd672ae49154fd935940a4bbe75f45595d60d reviews/README.md
7d67ff9a170b20647ba6d00ec964e09270c1dcf2752aade0bea8ef26003e77f0 reviews/completion/README.md
b3f19e1ed85fc41b3e04f51e56f9d6a7357dc4f871bccf6b9031ae3899776cef reviews/completion/RESPONSE.md
1a55137c58beef4b0559c4812b762abeed6404dbedab669fe85755e8c9b01ac5 reports/verification/completion-presentation-refresh.json
d20c76443bbb939f69f4e3692c6439f7c2a047df699c771f8467cb3923aa8d48 reports/verification/completion-presentation-final.json
0529ea280461ce3e002cb89abc27f6d32e1d794aaaf5302791621b4db927f682 reports/results/co2/REPORT.md
34ddc6041e119e23be8a2b31d60121e1fab1c57a11036ca4cf01d29a4fbadf1f reports/results/electricity/REPORT.md
b4a32c0f011fbeea823d95a84b15b1ed57a770e31ebae17b458dbaa46e17021d reports/results/retail/REPORT.md
51153cc1bb7fc3c69da6c185ae3572f84a6862a38b79680ebef7abf3b17030a3 reports/results/oil/REPORT.md
81bb7dbcd2df5e19504060702952a4fd26d84dab77243900fbb7f23c96ba6f50 reports/results/river-flow/REPORT.md
cd55b1d09af0edb1a4ee42f5a16f8e4498193f72ad27ac5adf2377352d4f4afd reports/results/air-quality/REPORT.md
de0e8ddfb3ab2161ea1a6e06153ca6494b3b8e042932fc7e83c63b46afeffdd6 reports/results/ecg/REPORT.md
ec3778a38a65578015cc44168de506c926b866d4e078cc4eb2c9d5e303a16476 reports/results/synthetic/REPORT.md
1cf6598a7523e65cd322ae11e300018cec2930bb275e9fa42cb7ce97ee416d4f reports/results/spectral/REPORT.md
902861f217c542630204a72d9b5a544fc7a9e7ef39824bd2c0b328e64468ba8a studies/co2/STORY.md
5b4310e708b854ce1180af3bc00524fde47a059a128ee56159e5d231ddd2413f studies/electricity/STORY.md
1095300dc930345917f79231f84d47fc9ba3b43638e4e9b9bb64b67dd63b6943 studies/retail/STORY.md
4e5c8d5c8fa28ca16987d271e670ad81c3b4b0601403de100fb2f70119c10828 studies/oil/STORY.md
dc4dcb282eb44726d551372529c14dde56fc1c1d0c432d9bcfdb2398a1d979ea studies/river-flow/STORY.md
2ba7fbbe85bd60b509c3a94f100e9489e17dc277d3ca96c239e2d096cd149cee studies/air-quality/STORY.md
5518625c5a45ea56c5d6079cf9876dc022ff67ddb96f3327236cfe84105a8f6d studies/ecg/STORY.md
02477acac228539afbf67244418e84bba6071608fe72b3ab3945eb5c9a32c800 studies/synthetic/STORY.md
4d90fdcec6679f9d1410d996bed46410b09cf66d00c7d87fe8541cd680de8bd5 studies/spectral/STORY.md
0cebc13252d809986dafa26d8f3a41d4f6a134fe88bec5152c01e90b57c8b873 reports/results/retail/weekly-sales.png
6e6aed2d530ac01158343e571e2e204e6c29f1f62eee15505fed43a41ba2866a reports/results/air-quality/outage-warnings.png
31a09b91de1ab316aaf4c17ada03a25aea63842d7e962651bc153bf783a47408 reports/results/spectral/recovery-and-ambiguity.png
166effd6de5fe67fcfb649c35731f761050d3f41c2529d3d59c32e100917b30e /Users/ethannol/src/side-projects/profile-atlas-complete-20261030/README.md
```

