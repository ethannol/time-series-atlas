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
