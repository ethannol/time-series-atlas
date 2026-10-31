# CO₂ C01 repair verification — 2026-10-30

Reviewer: `/root/critique_co2`, the non-authoring critic who identified C01.
Scope: the proposed source/prose repair against baseline
`71999b34ccfd7127840b173efb287ac0a66b2a26`; no full rerun or new fit.
The uncommitted inspected versions are identified by the hashes below.

**Pre-run verdict: approved for this repair.** C01 is resolved in the inspected
source and prose. **Generated-output/publication verification remains pending.**
The retained report and figure still contain their original bytes; this review
does not claim that the new diagnostic file or rendered report was published.

## What was verified

- `regression_matrix` and `predict` are AST-identical to baseline. The entire
  original `run` prefix through prediction generation, calibration, main and
  site-sensitivity scoring, paired differences, and `metrics.json` writing is
  AST-identical. The declared model/horizon lists are unchanged.
- Executed the exact new diagnostic statements in memory against the retained
  predictions and pinned source, replacing `save_frame` with an in-memory
  capture. No forecast fitting or result-file writing occurred.
- The diagnostic contains 26 unique model/origin rows: the same 13 test origins
  for each linear model. Its December formula `(3*p12-p36)/2` is appropriate for
  these linear fits with identical target-month indicators. It is not applied
  to the quadratic model.
- Verified `origin_gap = observed_origin - fitted_origin`,
  `growth_error = observed_growth - predicted_growth`, and
  `signed_error_36 = origin_gap + growth_error` for every row. Independent C01
  means match to numerical precision. The intended table displays:

| Fit | Origin gap, ppm | Growth error, ppm | Total signed error, ppm |
| --- | ---: | ---: | ---: |
| All history linear | 4.603 | 2.361 | 6.964 |
| Trailing decade linear | 0.294 | 0.819 | 1.113 |

- The report source labels this a post-publication arithmetic diagnostic,
  distinguishes signed error from MAE and causal attribution, preserves the
  frozen predictive comparison, and does not claim an anchored alternative
  was evaluated. The unchanged recent-fit MAE remains 1.119 ppm.
- README, methods, story, and portfolio copy now describe recent-history
  fitting and explicitly include fitted starting level as well as growth.
  The design appends a dated amendment acknowledging that results were already
  inspected; earlier dated story entries remain intact. Portfolio JSON parses.
- The optional color refinement is implemented with a shared model/color map
  in both plot calls and readable labels. Actual PNG rendering is still pending.
- All six original CO₂ result files are byte-identical to the review baseline.

## Remaining verification

After committed-source regeneration, independently check the new diagnostic
artifact, rendered report and PNG, output manifest, and unchanged original
predictions/metrics/paired differences. This is an output gate, not a request
for model retuning or an expanded study. No additional source repair requested.

## Inspected SHA-256 hashes

```text
6fc101460b493ec18b2d72cfb2f52a1afca500510d197e0b421524c59ac366d9 src/tsatlas/co2.py
94609b45f88fc4389a1dc8ef3c6671131e4258bad32cd6e9490a6408d2eb2992 studies/co2/DESIGN.md
c24844e468b51aa59e2be69102da365dee417a318b7525992781e4cf551cfc53 README.md
3625250c2002f5e50bd4dc6e0b18f702dae4294cab5163c45d4aeab70e35b0a5 docs/METHODS.md
58e1731de7251cddedf3e6fa19d4c9bd107e8e2ccbd15b95326bc6281f3a764c studies/co2/STORY.md
558887e25f0f2e7f3b330f7bfd4b2a05ee30f88485e51dd60346d096f8f3125d portfolio.json
```

## Final statistical/output verification — 2026-10-30

Inspected regenerated artifacts from source
`2dee5c82f480637a59489c3043a881dba4c8947b`. This entry closes the CO₂ output
gate above and adds the requested statistical check of changed river,
air-quality, and spectral descriptive summaries. It does not reopen their
model reviews or cover the retail/oil disclosure repairs.

**Verdict: approved within this scope. C01: implemented → verified, including
emitted evidence and presentation.** RF-C01, AQ-C01, SYN-01 and SYN-02's changed
descriptive summaries and qualifications also pass this statistical check.
No additional repair or model run is requested.

- **CO₂:** independently reconstructed every numeric diagnostic column for all
  26 model/origin rows from retained predictions and pinned observations; all
  match within `1e-11` ppm. The emitted means are 4.603 + 2.361 = 6.964 and
  0.294 + 0.819 = 1.113 ppm. The report identifies signed-error accounting,
  distinguishes it from MAE/causal attribution, dates the diagnostic after
  publication, and retains the original 1.119 ppm MAE. Viewed the final PNG:
  both panels consistently use teal for recent linear and purple for quadratic,
  with readable labels and unchanged plotted comparisons. Deferring an extra
  origin-gap figure remains acceptable; the table and per-origin file suffice.
- **River:** recomputed scored/scheduled totals from the split ledger:
  48,262/62,084 (77.7%) and 47,877/62,050 (77.2%). Checked each gauge/horizon/model
  prediction count against its audit denominator. Gauge 09386900 contributes
  200/3,652 and 195/3,650; its three-day weather recall is indeed 14/14. The
  report correctly limits these macro scores to usable targets and keeps the
  sparse gauge's equal weighting visible; it does not imply continuous coverage.
- **Air quality:** recomputed balanced accuracy directly from the saved TP/TN/
  FP/FN counts, then reproduced all 12 quarterly rows and all three station-
  comparison rows. High/low truth counts match across methods within each slice.
  Six- and 24-hour Q3 have no high hours and undefined BA. At 24 hours Q1,
  median 0.853 trails persistence 0.860. Station wins/ties/losses are 9/0/3,
  11/0/1 and 12/0/0. The report preserves the discontinuous calendar-Q1 and
  descriptive-subgroup qualifications without selecting new cohorts or models.
- **Spectral:** checked all 300 sampling-ledger counts/spans against saved input
  timestamps and reproduced both added summary tables. The maximum paired
  truth/alias power gap under thinning is `7.36e-11`; the displayed statistic is
  computed within each realization before aggregation. Exactly 6 of 26 irregular
  interpolation failures have peaks below 0.01 Hz. The fixed Lomb–Scargle range
  is 0.01–0.45 Hz; the report explicitly avoids inferring matched-band FFT
  performance from those six failures. Viewed the final example PNG: its axes
  now include zero and reveal low-frequency FFT power. No changed search or
  new comparison is presented as part of the frozen experiment.
- Independently byte-compared all **48 original numerical files** with baseline
  `71999b3`, rather than relying only on the regeneration claim: all are unchanged.
  Verified actual output hashes and source revision in the four scoped run
  manifests. The regeneration record accurately calls this an existing-checkout
  replay, not a fresh acquisition replay. No fits, full reruns, source edits or
  browser tasks were performed in this verification.

Final inspected SHA-256 hashes (the run manifests retain the remaining outputs):

```text
910388c44ebd747924722fde7c8f1ea6036d1980dd2cb33b4696ce6d1fc979dd reports/verification/dedicated-review-regeneration.json
fb5d245e771502879432a98863674ac961ef59daef7d9a2cf7c32b5a30acaa2b reports/results/co2/origin-level-diagnostic.csv.gz
95e62b5cc255cc82b8d1b88d551abd1fbf6a033852fb63d5c9581c82500a1a48 reports/results/co2/REPORT.md
62ecdf2c69175d8f60cfd6a89f85fd4034dc2f965ff9b14653d378bf3dfe2df6 reports/results/co2/forecast-comparison.png
54d1b72552f9a6f08c57e8832249fca9895aba304eb1793ee2dcda612e2d5bbf reports/results/co2/run.json
e41e5fd9686e2ca8d9407e8932f4ab175322bc30f7e728a27d0a4cd2319e3c91 reports/results/river-flow/REPORT.md
ec32436c279cce849bddd658a20141f7b15647216b07b14982ba679339d80905 reports/results/river-flow/split-audit.csv
63b44f22fadcc61a995fe13bc5b172bdb854ba665d42b1b650856931df66e7b0 reports/results/river-flow/gauge-scores.csv
9e713379e19f066dbb30c76f3be119823c675906a895155ad3575762601ca0fc reports/results/air-quality/REPORT.md
cc2f9de86546188238b7b8a9b41380c3d7af071f6e4abf28b0d84b6665f6de5e reports/results/air-quality/quarter-scores.csv
2792d1cf8e45ad6b9df123161cd06236a7fea3cb59cd061eb105d7b4d4c19a47 reports/results/air-quality/station-scores.csv
bbcff43d53ad5c321c24a2f975254f8e11d75b649267a2f367e65ef339fc89d3 reports/results/spectral/REPORT.md
58e32d541f4c26b72c40b69ce2a8977cf1af8824eb97c82beb83c14770a41fee reports/results/spectral/sampling.csv
8067b80377a5af51487ac842f827c976dc66c1eb412fcc75bb433ca81db4b467 reports/results/spectral/replicates.csv.gz
76089a638185642295277d68e859dd26d2bcc3a463c77c7f90d31503b42fc3d2 reports/results/spectral/preselected-examples.png
```
