# Retail results: artifact and numerical review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: recorded run, predictions, summary tables, report, figure, and story.
No forecasts were refitted. The reviewer independently recomputed outcomes,
normalization, and scores from the saved prediction table and pinned panel.

**Artifact/numerical verdict: pass. Publication verdict: pending final rendered
artifacts and fresh-checkout reproduction.** The primary agent plans a
presentation refresh and a subsequent exact-reference comparison. This review
does not relabel the existing checks as proof of that future execution.

The run identifies source `715ac6c89b1948609c67626c883a4cc63ec3abde` and protocol
`b369cc865d4eafaabe8e8f4d3b7ba26ae36bb0ba`. All **28 source-file entries** match
their Git blobs at the execution revision; all **six output hashes** and the
input snapshot hash match retained bytes. Source stability and an empty source
patch are recorded. Later edits to other study code do not invalidate this
historical source record.

The reviewer checked all **5,760 predictions**, covering five methods and
**1,152 unique product-weeks**: 24 products, 48 Monday origins, and seven-day
targets ending December 4. There are no duplicate model/product/origin keys,
missing declared combinations, invalid training scales, or nonfinite/negative
predictions. Every target is the corresponding sum from the pinned daily panel;
every scale is seven times its product's 2010 daily mean.

Every primary, per-product, and quarterly statistic recomputes from the saved
predictions, with a numeric comparison tolerance of `rtol=1e-12, atol=1e-10`
for CSV/JSON floating representation. These are score-audit tolerances, not a
relaxation of the future exact-byte reproduction comparison. There are 33,858
observed units and 669 zero-sales product-weeks. The always-zero model has the
lowest declared normalized MAE, 0.9860568865, while forecasting none of those
units. The report/story accurately limit that result to the fixed panel and
do not equate it with an inventory decision or unmet demand.

The figure was visually inspected: labels and both panels are readable, the
zero model's complete volume shortfall remains visible, and the plotted metric
definitions agree with the saved summaries. Per-product and quarter tables
remain available rather than concealing variation behind a single ranking.

Remaining publication checks: verify the final presentation after any renderer
change, retain the forthcoming fresh-checkout reference comparison, complete
dataset attribution documentation, and mark superseded “Next, not yet done”
story prose as historical. The latter is presentation housekeeping: later dated
entries already report the actual result. No new numeric defect was found.

```text
7170a6f0d4cef2b390d5a04f9ebb3c5fee0c86c3fbfd0049df03607622ddc96b  reports/results/retail/run.json
7cc2937018564832c656dbed080dba3b7eba36c15327a87735addf0bcfcb5f68  reports/results/retail/REPORT.md
a0cb2c69370222904b3f0798069cd63bb0df6f44de8919636c53cbe9c8f391ff  reports/results/retail/metrics.json
d2261a87326367c7def22678a8199afb4235c1254ac0f28fc8d9988feaef89ce  reports/results/retail/weekly-sales.png
fde607a4c43cbb7c6c54cc12fa0bcdf5af627a594d94b43c5b34015e1ecd99c4  studies/retail/STORY.md
```
