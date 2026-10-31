# Oil: fresh independent study critique

Reviewer: `/root/critique_oil`, a non-authoring AI critic. Date: 2026-10-30.
Scope: implementation, findings, and presentation; this is not human scientific validation.
Reviewed baseline: `71999b34ccfd7127840b173efb287ac0a66b2a26`, freshly fetched and
verified at `2026-10-30T23:25:29Z`, on `review/study-critiques-20261030`.
No implementation edits, model refits, test-set tuning, or instrumentation patches.
References and hashes below identify the initial baseline, before the parent's subsequent repairs.

I inspected the code, contract, story, source records, retained predictions and
figure before reading the earlier oil implementation/results review verdicts.
Local checks used the installed locked environment and one numerical thread.
No raw price series or private outcome series is included in this review.

## Separate verdicts

| Perspective | Verdict |
| --- | --- |
| Implementation | **Pass for the executed calculations.** Observed-date calendars, target timing, training-only fitting, recursions, saved predictions and scores reconcile. No result-invalidating defect found. |
| Findings | **Pass for the bounded descriptive answer.** The selected adaptive models improve full-period QLIKE, whereas the selected logistic model loses full-period Brier. This does not establish inherent direction unpredictability, operational utility, or calibrated risk. |
| Presentation | **A disclosure clarification is needed.** The numerical figure is readable and accurate; the public/local evidence explanation omits that adaptive forecasts reveal realized squared changes. Annual context and score explanations are useful optional improvements. |

The natural question is answered as a specific historical comparison of these
models and losses. The broader word “usefully” in the design is not established
as financial or operational usefulness, and the report correctly disclaims those claims.

## OIL-01 — Medium: disclose recoverable squared-change outcomes

**Classification:** newly identified underqualified disclosure; status: `identified`.
This is not a demonstrated license violation or a forecast/scoring defect.

**Locations:** baseline `src/tsatlas/oil.py:70–71,132–135`;
`data/README.md:66–69`; `reports/results/oil/REPORT.md:63–69`;
`studies/oil/DESIGN.md:75–77`.
The data README says “full realized outcome series are **fetch-only and excluded
from Git**.” The report explains that inputs and true-change evidence are retained
locally while original forecasts and aggregate scores are published. Those statements
remain literally correct about the source files and full **signed** change/label
columns. They do not adequately explain what the published forecast values reveal.

For consecutive observed targets, the public EWMA forecasts imply
`change[t]² = (variance[t+1] - 0.94 * variance[t]) / 0.06`.
The public GARCH forecasts and saved parameters independently imply
`change[t]² = (variance[t+1] - omega - beta * variance[t]) / alpha`.
These are algebraic inversions of the declared recursions, not an inferred attack
on unavailable data. Applying them to the public files recovered:

| Market | Squared outcomes recovered by each recursion | EWMA maximum absolute error | GARCH maximum absolute error |
| --- | ---: | ---: | ---: |
| WTI | 2,744 of 2,745 | 6.62e-13 | 5.62e-13 |
| Brent | 2,792 of 2,793 | 8.86e-14 | 8.53e-14 |

Errors compare the recovered values with retained private squared changes in
USD²/barrel². The last target lacks a subsequent published forecast. I did not
establish recovery of signed changes, direction labels, or complete price levels.

**Consequence:** dropping outcome columns is not a boundary that withholds the
realized volatility targets. Prior schema checks establish absence of explicit
outcome columns, not absence of recoverable outcomes. The accepted archival
limitation still holds: exact source prices may become unavailable after revisions.

**Required correction:** disclose this reconstructability beside the public/local
evidence explanation, distinguish squared magnitudes from full signed changes and
prices, and record this as a later discovery without rewriting earlier reviews.
**Optional, dependent on a separate publication decision:** reconsider public
release of sequential adaptive forecasts if the intended restriction also covers
recoverable magnitudes. Removing only EWMA would be insufficient because GARCH
is also invertible. This review does not require artifact removal, history rewriting,
or a legal conclusion. Disclosure alone can make the existing boundary honest.

## Optional presentation follow-ups

**OIL-02 — Low, optional:** `REPORT.md:3–15,45–59` names QLIKE and Brier before
giving an accessible explanation. Add one sentence that Brier measures probability
error for up/non-up outcomes, while the variance score penalizes forecasts that
are too small for large changes as well as forecasts that are unnecessarily large.
The report correctly explains the conditional-mean versus median distinction;
the improvement is accessibility, not a change to the conclusion.

**OIL-03 — Low, optional:** surface temporal context from the existing files rather
than requiring readers to interpret a CSV. Using annual counts and score differences
in `variance-subgroups.csv:22–33,82–93`, 2020 contributes 71.45% of WTI's total
EWMA-versus-fixed QLIKE gain; 2022 contributes 77.37% of Brent's. These are post hoc
descriptive decompositions, not new selection rules. GARCH beats fixed annual QLIKE
in 10 of 11 years in each market. Logistic beats prevalence annual Brier in 6 of 11
WTI years and 3 of 11 Brent years (`direction-years.csv`), despite losing pooled
Brier in both. The present headline is accurate for the pooled period; it does not
claim a win every year. No additional fitting or mandatory robustness run is requested.

## Checks and accepted limitations

- Nine focused oil/shared-metric tests passed: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --locked pytest -q tests/test_oil.py tests/test_metrics.py`.
- Raw workbook identities, normalized input, private evidence and all nine public output hashes matched their ledgers. Workbook headers identify WTI/Brent spot prices in dollars per barrel.
- Independently reconstructed all forecasts from saved parameters, without calling a fitter: maximum variance discrepancy 2.84e-14; probability discrepancy 2.34e-15. Training feature means/scales, target labels and calendar gaps agree.
- Recomputed headline scores, confusion counts and every annual/stress/gap summary; largest subgroup numerical discrepancy 7.11e-15. Each market's methods use identical targets: 2,745 WTI and 2,793 Brent.
- All six saved GARCH objectives reproduce; saved starts converge and satisfy constraints. Alpha plus beta is 0.997812 WTI and 0.998712 Brent. The standardized floor has the declared dollar units and does not bind the saved forecasts.
- First differences preserve negative WTI prices; each market retains its own calendar. Features and variance updates use prior observations. Training statistics use 2000–2014; initialization is carried through training into evaluation.
- Visually inspected `risk-and-direction.png`: signs, baselines and labels match the evidence, and separate task scales are explicit. The fixed model's contrary proxy-MAE ranking is prominent in the report.
- Accepted limitations: revised historical inputs and unknown publication latency; next-observed rather than fixed-day horizons; squared changes as a noisy second-moment proxy; zero-mean interpretation of variance; one frozen logistic specification; no uncertainty intervals or universal superiority claim. Long-gap subsets have only eight WTI and fifteen Brent targets.
- EIA's [series definitions](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp) confirm Refinitiv attribution; its [reuse page](https://www.eia.gov/about/copyrights_reuse.php) distinguishes government publications from protected contributed material. This supports the cautious attribution, not a new legal determination.

## Exact evidence identities

Published run source: `2c0af60037ae691aae7e13c92cb37228215e5876`;
protocol: `715ac6c89b1948609c67626c883a4cc63ec3abde`. Baseline oil code matches the recorded run hash.

```text
8fea9499d7504f45ae8553963cacc1981bec17158a2f32aa245bebb2ad0f0d82  src/tsatlas/oil.py
b15b13e15064526b97e8615581521147800704caed6587ad933b85fe11517fe3  src/tsatlas/acquire.py
870801c933476d2133b0a233d3e85188b376ba93b33a8c75c88fc36ba03675f5  src/tsatlas/extended_data.py
64e2b98cd9f2a653bd8444412be50500a4007a211560045390e8f16e7515b2ef  studies/oil/DESIGN.md
aea642f81d0824a6ffe9d3295618594271db6227e28691cea5473d3ae197cb99  studies/oil/STORY.md
51153cc1bb7fc3c69da6c185ae3572f84a6862a38b79680ebef7abf3b17030a3  reports/results/oil/REPORT.md
dc2dbe7350d482009aff4524d636f16a398baccd00e16d638b8e9bd7e823045a  reports/results/oil/metrics.json
3baef33eaf77a467713bf2d4c04a3b53af123f369e0ebc63b44d8378b3da7766  reports/results/oil/parameters.json
359f64e2917c22e74d08624e02c3313e1dd2e6226d2344d67ce842815ec86bd8  reports/results/oil/risk-and-direction.png
0919b370f8d9bdea5822ea753f50ece76c7cd6ea9894e24e1cd6f7629a63a07d  reports/results/oil/run.json
f58f9b28b1e7b714409e7e5b0e2e6d14b2de03cc291ce49aecd88685d3a862f3  reports/results/oil/variance-predictions.csv.gz
888ed1714e9f9018b83a92561d7cf6d86dfa8b9d06006b9f5d0f5ddb0947e053  reports/results/oil/direction-predictions.csv.gz
3c7f1bf10cdf3caeed7dbb521925994af9a115d24e0ab7a1027ad947928373d2  reports/results/oil/variance-subgroups.csv
504abe81276767a8d8eed646d16552cc6f54a3d03ba50554cb03be6129a71726  reports/results/oil/direction-years.csv
a29d37e52523e623d827667fd7dce5d5c2593106cf0cdfbcffa9340d95145303  reports/results/oil/direction-gaps.csv
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  local normalized input
9481986d496c3bc93a281e12f2ac1c86b92d2d7f9259e31124c5e3be24883f8f  local variance evidence
74702891ff7cb63822ea1f14ed872cb8c79ff7959a2a1198c8e2075f40e63cb6  local direction evidence
```
