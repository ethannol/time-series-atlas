# First-release results and publication review — general critic

Reviewer: `/root/general_critic` (separate automated reviewer).
Date: 2026-10-30.
Results source commit: `5953a7f6426bb44ddb2433153ce0c54038b6eb90`.
Protocol commit: `b374e9baa39f021481aefaefba958543534c916f`.

## Scope and evidence

Read the root README, story, plan, the three executed-study stories, their reports,
saved metrics and run metadata, and the first-release checkpoint record. Visually
inspected all three generated PNG figures. Compared the reported headline numbers
and customer comparisons with saved metrics. No model was fitted or rerun, no
hyperparameters changed, and no scoring implementation was independently audited
in this general review. Only this review file was written.

This combined session has separate verdicts for results interpretation and
publication, as required by the review protocol.

## Results/interpretation verdict

**The bounded headline interpretations are supported by the inspected saved
metrics. No result-invalidating issue was found within the general-review scope.**
This is not an independent numerical reimplementation or proof of model-code
correctness; those checks belong to the technical reviews.

- CO₂: the 36-month recent-growth MAE is 1.1188158508 ppm versus 6.9638058667 ppm
  for expanding linear growth. Both changing-growth models have lower absolute
  error at all 13 recorded origins. The text correctly limits the target months,
  revised-data interpretation, and dependent evaluation origins.
- Electricity: primary macro normalized MAE is 0.0983150154 for local Ridge versus
  0.1021403718 for pooled Ridge. The saved customer comparisons give three numeric
  improvements and 21 deteriorations. Local Ridge also has lower aggregate MAE;
  the overall model ordering persists in the all-date sensitivity. Those facts
  do not establish that every shared model fails or that these customers represent
  the wider population, and the story avoids those claims.
- Synthetic detection: the recorded CUSUM no-change false-alert counts are 10/200
  under independent noise and 146/200 under persistent noise. The reports keep
  early alarms, eligible runs, detections, and misses visible rather than presenting
  conditional detection delay alone. The field-performance limitation is clear.

## Publication verdict

**Not yet ready from the general-review perspective: address GP01–GP04 below.**
The required fixes concern presentation, current status, and complete attribution.
They do not require refitting, retuning, changing endpoints, or expanding the
study. Preserve the saved analysis results and evidence while improving the
reader-facing explanation.

### GP01 — Make customer-level differences visible and answer “who?”

Priority: medium; required publication correction.
Files: `reports/results/electricity/pooling-comparison.png`, its `REPORT.md`, and
the electricity story's interpretation where appropriate.

The scatter has one normalized-error point near 1 and another near .2; most of
the 24 customers overlap near .04–.09. No customer is labelled. Consequently the
figure does not let a reader identify the three improved customers or assess the
small differences, despite the report saying it preserves those differences.
The aggregate bar chart is readable, but cannot answer the customer-level question.

Add a labelled per-customer delta plot or table computed from the saved metrics,
with the sign and normalization explicit. Preserve all customers, including the
large-error customer. An inset is an alternative if every customer can still be
identified and the larger points remain visible.

For context, the primary numerical improvements are MT_166 (-0.0003064225),
MT_210 (-0.0001610189), and MT_302 (-0.0000004893) in pooled-minus-local normalized
MAE. The last is effectively indistinguishable visually at the present scale.
Keep the exact sign count, but describe its small magnitudes. In the all-date
sensitivity the improved IDs are MT_166, MT_198, and MT_210: the count and broad
ordering persist, but the identities are not identical. This is a useful bounded
finding rather than a reason to change the scoring.

### GP02 — Give each report a standalone plain-language answer

Priority: medium; required publication correction.
Files: all three `reports/results/*/REPORT.md` files.

The README and process stories explain the lessons, but the reports themselves
mostly begin with scope cautions, a plot, and technical tables. A reader following
an executed-report link should not need to infer its main answer or decode an
implementation identifier first.

Add one or two opening sentences stating the measured answer and its scope. Map
`linear_120months` to a trend fitted on the previous ten years, `linear_expanding`
to a trend fitted on the available expanding history, and local/pooled Ridge to
separate/shared regression. Retain machine identifiers where useful for auditing.
For synthetic detection, explain independent versus persistent noise in ordinary
language and label the delay unit as **samples after the change**. State that the
false-alert percentages concern any alert during the declared monitoring window,
not a per-sample probability. The figure already supplies the 300-point window;
put that meaning beside the numerical table too.

This is a communication change. The reports already contain appropriately bounded
conclusions in linked stories; do not add unsupported mechanisms or operational
savings to make them sound more decisive.

### GP03 — Reconcile current-status prose with executed evidence

Priority: medium; required publication correction.
Files: the three executed-study `STORY.md` files, root README, and
`reviews/first-release/README.md`.

The undated Data fields still say the CO₂ snapshot is “still to be frozen,”
electricity aggregation is “planned,” and synthetic rules/seeds are “to be frozen
before execution.” These conflict with the current executed status and run
metadata. Update those current metadata fields; retain the explicitly dated
planning entries as historical records.

The checkpoint record also has an undated “Implementation and results” section
marked “Pending,” and says contracts “will be committed,” followed by later
implementation approval. Date or explicitly identify those as prior states and
add the current full-run/source/protocol evidence and review status. Do not label
results/publication verified until the respective reviewers have completed them.

The root README still says redistribution conditions “will be checked separately
before publishing source snapshots,” while its reproduction instructions already
use committed analysis snapshots. Distinguish the first release's actual data
handling/attribution status from the remaining planned sources, with a link to
the data documentation. This review has not independently adjudicated licensing.

### GP04 — Extend AI attribution to the work that now exists

Priority: low; required attribution completion.
File: root README, “Ownership and AI assistance.”

The attribution currently enumerates agent planning, source research, and critique,
but not the now-existing implementation, execution, and generated reports. Add
the actual contributions of agents to those artifacts. Preserve the bounded
description of Ethan's demonstrated direction-setting and requested reviews;
do not imply he personally implemented or reviewed numerical analyses unless
that occurred. The present text does not fabricate human authorship, but it is
incomplete for this release.

## Visual assessment

- CO₂: readable axes, units, and origin-level differences make the primary result
  clear. The model colors change across panels; consistent colors would be a
  useful optional refinement, not a publication blocker.
- Electricity: aggregate comparison is useful; customer scatter needs GP01.
- Synthetic: the paired false-alert/detection views are useful and explicitly
  distinguish the eligible detection denominator. Keep that qualification when
  reusing the image elsewhere. The table supplies misses and early-alarm counts,
  which are essential context for the apparently perfect conditional detection.

The first release's three distinct lessons provide a coherent portfolio entry.
The remaining five real-data studies are visibly planned. No extra dataset,
dashboard, model family, or experimental rerun is requested by this review.

## Inspected SHA-256 hashes

```text
98d97913845ab4c0fe14197575e04891efc93c98ae50eb05faf47cd2d5e09340  README.md
7b8cd81a31341592f887ddf817ccfe8767a5da635b12018e776018647d54b99a  STORY.md
eb3a0b27a33470425cf1b1552667b56aef90c74ba6528103ac6e4a4d7a357d97  PLAN.md
c54a16b0f372f66106fb8b17e43cd68983a0f440b1c324711b017a02d32d1f7e  studies/co2/STORY.md
9cc41a6a3b77a61d245c9b118f91bcd0073446c86422dbeebe584402216e6a7c  studies/electricity/STORY.md
489359c70dab3b78b32d7f61a4b12f67d5f96ddf51cfd7510778988e74f6635e  studies/synthetic/STORY.md
8fc3d871e01d53f2a43076888c46788d23ba494f77243cd8b1e426029b4ae783  reports/results/co2/REPORT.md
5d9ba50ea685c9d1845890d18c0eb23d1106d78d496bfc125a1c3a1d778bf0a8  reports/results/electricity/REPORT.md
3cb24ba485d15fe68c1e8ab59152a5bf30b289d0e53a2939f33fc4ee110b3b8c  reports/results/synthetic/REPORT.md
36e0cef9a2e517645a44fb78de94bfddf716342a5f031ed4f897b68764c2deb9  reports/results/co2/metrics.json
eea0c9d198bbbedd09910f407b41bf74ddac16e13e32eb450c870226cd0ab0db  reports/results/electricity/metrics.json
17eb15c6a025db3dad0536ff9579e1f201392472e790d58d54b44188ea44aeec  reports/results/synthetic/metrics.json
d75ced7a440c5dfb50e4ac926ba464651169ed6f3bf1455f06b8712409ed5b68  reports/results/co2/forecast-comparison.png
7e71f1aaaf378c9007bb73fd3bdd279112c722ee06467d7c4b4ce0bc62624e6a  reports/results/electricity/pooling-comparison.png
74830249eb8de5f54433487a0470e9a5bce5a48b708ad6a905c3fea420bda997  reports/results/synthetic/detection-comparison.png
25a2f9bf21be6dc1621656b0e9ee327dc3b1f6565953fe132c895ff061472c98  reports/results/co2/run.json
b8031cce8180102e2b5250c540b800872cb93c03157f989c74baec004ffbb327  reports/results/electricity/run.json
5e881497079185936e8e3df6a51e3e7d0d8bd3d778d727dc1d479158ba9878df  reports/results/synthetic/run.json
f4273b1eca659ca7518084ed005dddf849d3d926e7eb616270f6f7d7ae5438a8  reviews/first-release/README.md
```
