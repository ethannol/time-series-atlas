# Oil result evidence and public-data boundary review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: the first full oil run from source `ed1072c56209d3b53cdfbcd80e42ea4c480529e3`,
its public artifacts and retained immutable private outcomes. The reviewer
reconstructed forecasts from saved parameters and recomputed scores; no model
was refitted or changed. This is separate from authoring and statistical review.

**Artifact and numeric verdict: pass. Publication remains pending the final
process-story update and clean-checkout reproduction checkpoint.** No raw-input
or private-outcome redistribution was found in the inspected tracked paths or
their Git history. The fetch-only reproduction limitation remains explicit.

## Provenance and private evidence

All **33 source hashes** match the Git blobs at the recorded source commit,
all **nine public output hashes** match retained files, and the normalized
fetch-only input matches its pinned hash. The recorded protocol commit is
`715ac6c89b1948609c67626c883a4cc63ec3abde`. Source stability, clean-source patch
hash, timestamps, runtime, and process-lifetime peak RSS are retained. The run
reports approximately 0.82 seconds and 225 MB RSS; these are recorded local
execution facts, not a portable performance benchmark.

Both private outcome files exist, match their content-addressed filenames and
recorded hashes, and are ignored by Git. Dropping only `change` from variance
evidence and `up` from direction evidence reproduces the public prediction
tables exactly. Public tables have no duplicated market/date/model keys and
contain no explicit price or true-change/true-direction columns. Fitted
parameters, training aggregates, predictions, gaps, and score summaries are
the declared public outputs. `git ls-files` returns no raw/processed inputs;
history queries for those paths and the formerly considered public normalized
oil path found no committed files.

This verifies the implementation's chosen publication boundary; it does not
establish a broader third-party data license. The report correctly identifies
EIA's Refinitiv attribution and does not call the source prices government-owned.

## Independent numerical checks

The retained outputs contain **22,152 variance rows** and **11,076 direction
rows**, representing 5,538 distinct market/date targets: WTI 2,745 and Brent
2,793. Each market's methods share its actual observed target dates, starting
2015-01-02. Every private target value and calendar gap matches that market's
own normalized source history. The negative WTI episode remains in the source
and corresponding first differences; no log transformation or calendar filling
appears in this reconstruction.

Using independent NumPy/Pandas calculations and the saved coefficients, the
reviewer reconstructed all four variance forecasts and both direction forecast
definitions. An explicit chronological recurrence independently checked EWMA
and GARCH; fixed and 60-observation estimates used the pinned history. Logistic
probabilities were reconstructed from the saved scaler, coefficient and intercept.
All agree with saved predictions within numerical tolerance, without optimization.

Training counts, mean-square initial variances, direction prevalence, feature
means and population standard deviations agree with the declared 2000–2014
rows. Each of the three GARCH attempts per market is recorded as successful;
the retained parameters correspond to the smallest saved training objective.
This checks the recorded selection, not an independent reoptimization.

Every primary variance/direction score, annual summary, 2020/other-year
variance summary, and both tasks' calendar-gap summary was recomputed directly
from private evidence. Counts/confusion cells match exactly; numerical scores
match within `rtol=1e-11, atol=1e-12`. Public/private alignment and source-target
alignment were checked independently before rescoring, so agreement is not
merely a second call to the author's metric functions.

## Claims and presentation

The figure was visually inspected: labels, zero references, task units and
market distinction are readable. Its plotted differences agree with the tables.
All three changing-variance methods improve aggregate QLIKE over the fixed
variance for both markets, while the logistic direction model has worse aggregate
Brier scores than prevalence for both. The variance-proxy MAE favors the fixed
baseline in both markets, demonstrating that “better risk model” is too broad
a claim for these results. The report presents both scores and their separate
meaning without claiming calibrated tail limits, trading profit, savings, or
real-time source availability.

The long-gap slices are small: only eight WTI and fifteen Brent targets exceed
four calendar days. Their retained subgroup scores should remain descriptive,
not evidence of dependable long-gap prediction. Annual and stress-period
breakdowns are linked rather than treated as independent repeated trials.

The inspected process story currently ends at source intake. Before publication,
append the actual pre-run corrections, observed results, score tradeoff and
remaining limitations with links to the reviews; do not rewrite the earlier
planning entries as though the results were known. A short plain-language result
sentence in the report would also help readers interpret its numerical tables.

## Remaining reproduction boundary

The public commands clearly separate `atlas fetch oil` from `atlas oil`, and
require the historical normalized hash before claiming exact input reproduction.
An updated provider workbook can preserve that window; historical revisions
can also make exact public acquisition unavailable. The guarded mocked
acquisition probes were recorded in the [implementation review](oil-implementation-data.md).
This result review verifies the currently retained local input and outcomes;
it does not claim a fresh public download or clean-checkout rerun occurred.
The parent plans that final reproduction checkpoint after all study artifacts
are committed. It remains outstanding here.

## Inspected hashes

```text
b92b59d55c9e4fba07884cdc8800017ee251583a0f4f59a772a75845ee7e2552  reports/results/oil/run.json
dc2dbe7350d482009aff4524d636f16a398baccd00e16d638b8e9bd7e823045a  reports/results/oil/metrics.json
7210a4dbcc7e30c51ddaeeff211e990512b920b754273763401e6c240a97ea2b  reports/results/oil/REPORT.md
3baef33eaf77a467713bf2d4c04a3b53af123f369e0ebc63b44d8378b3da7766  reports/results/oil/parameters.json
359f64e2917c22e74d08624e02c3313e1dd2e6226d2344d67ce842815ec86bd8  reports/results/oil/risk-and-direction.png
9481986d496c3bc93a281e12f2ac1c86b92d2d7f9259e31124c5e3be24883f8f  private variance outcomes (path recorded in metrics.json)
74702891ff7cb63822ea1f14ed872cb8c79ff7959a2a1198c8e2075f40e63cb6  private direction outcomes (path recorded in metrics.json)
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/processed/oil-daily.csv.gz
ba51be078dd2749be7fa9a9f1b9e69bb7c954ee404626b43ffe800a02354030c  studies/oil/STORY.md
```
