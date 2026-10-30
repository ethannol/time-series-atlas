# Oil results and publication review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Run source: `ed1072c56209d3b53cdfbcd80e42ea4c480529e3`.
Frozen protocol: `715ac6c89b1948609c67626c883a4cc63ec3abde`.

**Results verdict: approved.** Saved forecasts, actual outcomes, target dates,
gap lengths and all inspected scores reconcile independently. **Publication
verdict:** the existing numerical tables, figure and limitations are supported;
complete the plain-language answer and current story/status in OP01 before
calling this study publication-ready. Exact full reproduction remains pending.
No model was refitted or retuned for this review.

## Independent recalculation and provenance

All generated-file hashes match the run's output ledger. The recorded oil source
hash matches the independently approved pre-run implementation, including the
corrected standardized variance floor. The ledger records stable source during
execution. Both immutable private outcome files exist and match the hashes in
`metrics.json`; `git check-ignore` confirms they reside in the ignored local
evidence directory.

For each market, the reviewer independently differenced the pinned observed
price series, preserved its own calendar and selected the frozen target dates.
Every saved change, strict-positive direction label and calendar gap agrees with
that input. There are **2,745 WTI** and **2,793 Brent** scored target dates per
method, with no duplicate market/date/model keys or unequal within-task cohorts.
The first target is January 2, 2015. Zero changes remain non-upward and the
negative WTI episode is retained.

The reviewer recomputed **all saved variance forecasts from fixed parameters**:
training mean-square baseline, lagged 60-change mean square, and independent
scalar EWMA/GARCH recursions initialized with the declared training statistic.
These agree with the public predictions. Logistic probabilities were recomputed
from the saved coefficients, training scaler statistics and independently
constructed lagged price/change features; they also agree. This is forward
evaluation of saved parameters, not a new fit or optimizer run.

All primary QLIKE/proxy-MAE values and Brier/accuracy/confusion counts reproduce.
Every annual variance and direction row, variance 2020/other-year row, and both
tasks' `<=4`/`>4` gap summaries reproduce from the saved dated outcomes. The long-
gap subsets contain only **8 WTI** and **15 Brent** targets, so they are small
descriptive checks, not reliable estimates for arbitrary long reporting gaps.

The three recorded GARCH starts converge for each market, and the published
parameters correspond to the lowest recorded converged training objective.
Alpha/beta are nonnegative and their sums satisfy the frozen upper bound.
Logistic fits report five iterations and no convergence warnings. No failed
attempt was silently replaced in these saved diagnostics.

## What the two tasks actually show

| Market | GARCH minus fixed QLIKE | GARCH minus EWMA QLIKE | Logistic minus prevalence Brier |
|---|---:|---:|---:|
| WTI | -0.824609 | -0.005240 | +0.001578 |
| Brent | -0.308081 | -0.002723 | +0.001653 |

Under the **predeclared expected-second-moment score**, all three adaptive
variance methods improve on fixed variance over the full evaluation period.
GARCH has the lowest average QLIKE, but its extra improvement over the simple
EWMA is small in the declared units. It has lower annual QLIKE than EWMA in
9 of 11 WTI years and 8 of 11 Brent years; this is descriptive variation, not an
independent-year significance test or evidence of a universal winner.

Logistic direction prediction is slightly **worse** than the training-prevalence
baseline on Brier and accuracy in both markets. The supported conclusion is
that these fixed lagged features and this logistic model did not improve on that
baseline. The study cannot establish that price direction is inherently
unpredictable or that all possible direction models would fail.

Fixed variance, meanwhile, has the lowest MAE against realized squared changes.
That is not an arithmetic contradiction. QLIKE targets the conditional expected
squared change (variance under the declared zero-mean convention); absolute
error against squared changes rewards their conditional median. These losses
prefer different point summaries. The observed squared change is also only a
noisy volatility proxy. Keep the frozen QLIKE primary and show both losses;
neither licenses a claim about calibrated tails, profitable trading or savings.

The two plot panels have different scores and scales. Their magnitudes cannot
measure whether volatility is inherently “more predictable” than direction.
Each panel answers whether its selected method improved on its own benchmark.
Visual inspection confirmed that bar signs, labels and displayed comparisons
agree with the saved metrics.

## Public/local evidence split

The public variance predictions contain date, model, variance, gap and market;
the public direction predictions contain date, model, probability, gap and market.
They equal the private prediction columns exactly, with true change/up labels
removed. No raw price or complete true-change/label column is present in these
public tables. Aggregate scores, training parameters and evidence hashes remain
public as planned. This checks adherence to the agreed publication policy; it
is not a new legal determination about source rights.

The report correctly discloses the Refinitiv provenance, local retained truth,
normalized-input matching requirement and the possibility that historical
revisions prevent exact public re-acquisition. It does not imply that a checksum
alone retrieves old bytes. The upcoming full reproduction must verify actual
commands/artifacts before being described as completed.

## OP01 — Finish the plain-language answer and current story

Priority: publication completion, not a numerical-results blocker.
Status: identified.

The report currently opens with how to read the chart and then presents valid
tables. Add a short explicit answer: adaptive variance forecasts improve on fixed
variance by QLIKE; EWMA is close to GARCH; this logistic direction comparison does
not beat prevalence. Mention the opposite squared-change-MAE ranking and its
different target. Do not imply a statistically established or commercially useful
GARCH advantage over EWMA.

The story's current Data sentence still describes an “intended common-history
snapshot,” and its latest dated entry describes work yet to be run. Update the
current summary to the pinned, separate observed-market calendars and add an
honest dated first-results entry. Preserve earlier plans and uncertainty. Mark
reproduction/publication review pending until those final gates actually close.

No new model, threshold, split, score selection or final-data tuning is requested.

## Inspected SHA-256 identities

```text
7210a4dbcc7e30c51ddaeeff211e990512b920b754273763401e6c240a97ea2b  reports/results/oil/REPORT.md
dc2dbe7350d482009aff4524d636f16a398baccd00e16d638b8e9bd7e823045a  reports/results/oil/metrics.json
b92b59d55c9e4fba07884cdc8800017ee251583a0f4f59a772a75845ee7e2552  reports/results/oil/run.json
3baef33eaf77a467713bf2d4c04a3b53af123f369e0ebc63b44d8378b3da7766  reports/results/oil/parameters.json
f58f9b28b1e7b714409e7e5b0e2e6d14b2de03cc291ce49aecd88685d3a862f3  reports/results/oil/variance-predictions.csv.gz
888ed1714e9f9018b83a92561d7cf6d86dfa8b9d06006b9f5d0f5ddb0947e053  reports/results/oil/direction-predictions.csv.gz
3c7f1bf10cdf3caeed7dbb521925994af9a115d24e0ab7a1027ad947928373d2  reports/results/oil/variance-subgroups.csv
504abe81276767a8d8eed646d16552cc6f54a3d03ba50554cb03be6129a71726  reports/results/oil/direction-years.csv
a29d37e52523e623d827667fd7dce5d5c2593106cf0cdfbcffa9340d95145303  reports/results/oil/direction-gaps.csv
359f64e2917c22e74d08624e02c3313e1dd2e6226d2344d67ce842815ec86bd8  reports/results/oil/risk-and-direction.png
ba51be078dd2749be7fa9a9f1b9e69bb7c954ee404626b43ffe800a02354030c  studies/oil/STORY.md
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/processed/oil-daily.csv.gz
9481986d496c3bc93a281e12f2ac1c86b92d2d7f9259e31124c5e3be24883f8f  private variance evidence (path recorded in metrics.json)
74702891ff7cb63822ea1f14ed872cb8c79ff7959a2a1198c8e2075f40e63cb6  private direction evidence (path recorded in metrics.json)
```

2026-10-30, statistical reviewer: results approved; numerical publication claims
approved; OP01 identified for report/story completion; full reproduction pending.
