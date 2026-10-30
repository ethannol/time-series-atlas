# Oil results and publication — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Results source: `ed1072c56209d3b53cdfbcd80e42ea4c480529e3`.
Protocol: `715ac6c89b1948609c67626c883a4cc63ec3abde`.

Read the report, metrics, parameter/optimizer summaries, dated subgroup evidence,
run metadata, public prediction column schemas, and current oil story. Visually
inspected the figure. No model was fitted, private outcome series rescored, or
exact reproduction performed by this reviewer. Parameter summaries and public
prediction headers were inspected for context, not as a code audit.

## Results/interpretation verdict

**The proposed bounded answer is supported by the saved metrics: dynamic variance
forecasts improve the prespecified QLIKE comparison on both markets, while the
tested logistic direction model has worse Brier scores than training prevalence.**
The absolute squared-change-proxy MAE gives a different variance ranking. Do not
collapse these into a universal predictive-skill or business-benefit claim.

On Brent, GARCH QLIKE is 1.70740855 versus fixed variance 2.01548913; on WTI it is
1.85331920 versus 2.67792846. EWMA and the rolling model also improve on fixed
variance under the full-period QLIKE score. In contrast, fixed variance has the
lowest absolute proxy MAE in both markets (2.7870 Brent; 4.7791 WTI).
Logistic Brier is 0.25143190 versus prevalence 0.24977939 for Brent and 0.25112398
versus 0.24954583 for WTI. These are observed comparisons, not significance claims
or evidence that every forecasting model would behave similarly.

The figure correctly separates task scores and makes the lower-is-better
direction explicit. Subgroup files retain annual, stress-period, and gap results;
the overall result should not be described as a win in every year. In particular,
the long-gap direction subsets contain only 15 Brent and 8 WTI outcomes, so their
counts are necessary context for any later discussion.

## Publication verdict

**Two presentation/story corrections are needed. Exact reproduction and the final
publication-inventory checks are also still pending and cannot be inferred from
this general review.** Neither correction requires model or metric changes.

### ORES01 — State the answer and the contrasting score ranking directly

Priority: medium; status: identified.

The report begins by explaining how to compare panels, rather than answering its
question. Add a short opening result: the tested dynamic variance models improved
the declared QLIKE score for both markets, but the tested direction model did not
beat prevalence. Explicitly state that fixed variance nevertheless has lower
absolute squared-change-proxy error, so the variance conclusion is score-specific.

Give QLIKE and Brier a brief plain-language explanation or point to an immediately
adjacent definition so a hiring reader can interpret the result without decoding
the implementation. Preserve the current cautions about next-observed-date
horizons, noisy volatility proxies, revised data, and distinct task scales.
Do not add claims of calibrated monetary risk, profitable trading, cost savings,
or a universal GARCH advantage over EWMA from their small average difference.

### ORES02 — Add the actual execution/result step to the oil story

Priority: medium; status: identified.

The story's current metadata still describes an intended snapshot and source-intake
status. Its last dated entry explains a future fetch-only plan; there is no dated
account of the run, its measured answer, or the still-pending result/reproduction
gates. Update current metadata and append a short execution/results entry that
links the actual report and review. Retain the correctly dated planning history.

The new entry should explain what the separate variance/direction comparisons
found and why the raw proxy-error ranking differs, without assigning unperformed
numerical checks to Ethan or implying the full collection is complete.

## Source/reproduction framing

The report appropriately distinguishes free EIA access from a right to mirror the
underlying price history. The inspected public prediction tables contain forecast
values, dates, gaps, model and market identifiers; they do not have price or true-
change columns. Metrics retain paths/hashes for ignored local outcome evidence.
This schema check is not a complete repository/history inventory or legal review.

The explicit future-upstream-revision limitation is useful and should remain
visible after local reproduction succeeds. The command description is a
reproduction procedure, not evidence that another checkout has already succeeded.
Require the separate reproduction artifact before claiming that gate complete.

## Inspected SHA-256 hashes

```text
7210a4dbcc7e30c51ddaeeff211e990512b920b754273763401e6c240a97ea2b  reports/results/oil/REPORT.md
dc2dbe7350d482009aff4524d636f16a398baccd00e16d638b8e9bd7e823045a  reports/results/oil/metrics.json
3baef33eaf77a467713bf2d4c04a3b53af123f369e0ebc63b44d8378b3da7766  reports/results/oil/parameters.json
b92b59d55c9e4fba07884cdc8800017ee251583a0f4f59a772a75845ee7e2552  reports/results/oil/run.json
359f64e2917c22e74d08624e02c3313e1dd2e6226d2344d67ce842815ec86bd8  reports/results/oil/risk-and-direction.png
888ed1714e9f9018b83a92561d7cf6d86dfa8b9d06006b9f5d0f5ddb0947e053  reports/results/oil/direction-predictions.csv.gz
f58f9b28b1e7b714409e7e5b0e2e6d14b2de03cc291ce49aecd88685d3a862f3  reports/results/oil/variance-predictions.csv.gz
a29d37e52523e623d827667fd7dce5d5c2593106cf0cdfbcffa9340d95145303  reports/results/oil/direction-gaps.csv
504abe81276767a8d8eed646d16552cc6f54a3d03ba50554cb03be6129a71726  reports/results/oil/direction-years.csv
3c7f1bf10cdf3caeed7dbb521925994af9a115d24e0ab7a1027ad947928373d2  reports/results/oil/variance-subgroups.csv
ba51be078dd2749be7fa9a9f1b9e69bb7c954ee404626b43ffe800a02354030c  studies/oil/STORY.md
```
