# Fresh retail investigation critique

Date: 2026-10-30. Reviewer: independent AI subagent `/root/critique_retail`,
covering implementation, findings, and presentation. The reviewer did not author
this study. This is a retrospective fresh critique, not a replacement for the
historical pre-run review or independent human validation.

The reviewer fetched origin at **2026-10-30T23:20:45Z** and verified both HEAD and
origin/main as **71999b34ccfd7127840b173efb287ac0a66b2a26**, on the parent's
`review/study-critiques-20261030` branch. Implementation, contract, and saved
artifacts were read before prior critic verdicts. Subsequent reads of the prior
source, implementation, and result reviews distinguish new observations from
already disclosed limitations. No instrumentation patch, implementation edit,
full model rerun, or post-result tuning was performed.

## Verdicts

| Area | Verdict | Reason |
| --- | --- | --- |
| Implementation | **Pass for the frozen, case-sensitive stock-code panel.** | Raw aggregation, selection, recurrence probes, forecast timing, and score arithmetic agree with the contract. No source/target, leakage, split, or numerical blocker was established. |
| Findings | **Pass as descriptive results for this fixed cohort and period.** | All saved targets/scales and primary, product, and quarterly metrics recompute. Zero wins the declared scaled MAE; TSB wins raw-unit MAE. Neither conclusion establishes inventory value or general superiority. |
| Presentation | **Pass with one minor clarification requested below.** | Figure and numerical claims are accurate and readable. The main narrative should expose the existing stock-code identity limitation when describing products and inactivity. |

No high- or medium-severity defect was established. The one actionable item is
a disclosure improvement, not a request to alter the cohort or redo the study.

## Actionable finding, ranked by severity

### RET-01 — Low: surface the stock-code identity limitation in the report

Status: **identified**. Affected locations:
`src/tsatlas/extended_data.py:57`, `:63`, `:70`–`:74`;
`reports/results/retail/REPORT.md:33`–`:39`, `:53`–`:57`;
`studies/retail/DESIGN.md:33`–`:37`.

The implementation preserves case-sensitive stock-code strings. That policy is
reasonable without a verified identity crosswalk, but the public report calls
them 24 established “products” and discusses later inactivity without explaining
that a product's history may be split across differently capitalized codes.
The caveat appears in `reviews/completion/design-implementation.md:48`–`:49`,
not in the main report's limits. This is an **existing accepted source limitation
with an insufficiently prominent consequence**, not a newly discovered covert
filter or a demonstrated identity merge error.

An independent pass through the pinned workbook found the following retained
UK positive-sale records after the declared overlap cutover and filters:

| Exact source code | 2010 units | 2011 units through December 9 | Shared descriptions across the case variants |
| --- | ---: | ---: | --- |
| `85232b` — selected | 24 | 0 | `SET/3 RUSSIAN DOLL STACKING TINS`; `SET OF 3 BABUSHKA STACKING TINS` |
| `85232B` | 1,290 | 9 | Same two descriptions |
| `84660C` — selected | 195 | 499 | `PINK STITCHED WALL CLOCK` |
| `84660c` | 17 | 14 | Same description |
| `84596G` — selected | 375 | 1,680 | `SMALL CHOCOLATES PINK BOWL` |
| `84596g` | 2 | 3 | Same description |

These totals use the full available 2011 window, not only the scored weeks.
The selected `85232b` also has zero recorded units in all 48 scored weeks.
Identical descriptions are evidence of plausible aliasing, not authoritative
proof that identifiers can be merged. The issue matters because eligibility,
training normalization, apparent intermittency, and apparent disappearance all
operate on those exact strings.

**Requested correction:** add a brief limitation near the cohort/zero-sales
discussion: the study forecasts unharmonized, case-sensitive source stock codes;
some differently capitalized codes have matching descriptions, so code
inactivity is not verified product discontinuation. Preserve the existing result
and provenance. Do not silently uppercase codes, change selection, or claim an
audited identity resolution. If a later study resolves identities, that is a
versioned target/cohort amendment requiring renewed review.

## Implementation and source evidence

- **Annual-sheet overlap:** a fresh read-only workbook pass compared all eight
  columns as multisets over December 1–9, 2010. Both sheets contain exactly
  **22,523 rows** in that overlap; multiset equality is exact, including duplicate
  multiplicities, with no residual rows on either side. The cutover is supported
  by the actual records. Retaining unresolved within-sheet duplicates remains a
  separate, disclosed choice.
- **Panel and cohort:** independent aggregation after the declared UK,
  cancellation, code-format, quantity, and price filters exactly reproduced the
  **739 × 24** daily snapshot. Independently recomputing 2010 active-day counts,
  first-half and last-quarter activity, stable code tie ordering, annual-volume
  ranks, and 24 evenly spaced ranks produced **2,072 eligible codes** and the
  exact saved selection in order. Later activity never enters eligibility.
- **Zero versus missing:** the snapshot is a complete, finite, nonnegative daily
  grid from December 1, 2009 through December 9, 2011. Zero-filling implements
  “no retained transaction in this source,” not known availability, true demand,
  or a demonstrated complete reporting process. The report's explicit warning
  is necessary and appropriate; no audit can recover stockouts from these data.
- **Timing:** `src/tsatlas/retail.py:35`–`:46` uses history strictly before each
  Monday, including January 1–2 before the first forecast. Targets are seven
  calendar days through Sunday. All 48 origins end by November 28, covering
  through December 4 and avoiding the terminal partial week. The 2010 scale is
  fixed and available at every scored origin. All products receive identical
  weeks, making row-average scaled error equal to the declared product macro
  average.
- **Intermittent methods:** code inspection and independent toy calculations
  agree with the frozen initialization and daily updates. For `[0,0,6,0,8]`, the
  ending size is 6.2, interval 2.9, and TSB occurrence probability 0.37; the rates
  are `0.95*6.2/2.9` and `0.37*6.2`. Consecutive positives have a gap of one;
  `[0,0,10]` uses an initial interval of three. Croston's states remain fixed
  through zeros, while TSB probability decays. Multiplication by seven produces
  an origin-time weekly rate forecast without using future within-week sales.
  Sharing the size state is valid for the declared equal smoothing constants.
- **Tests:** `uv run pytest -q tests/test_retail.py` passed **3 tests** in the
  locked environment. The 12 timedelta deprecation warnings are already known
  and did not change dates or test outcomes. Tests cover future mutation,
  inactivity decay, all-zero histories, and invalid sales. No broad test suite
  or expensive process was started by this reviewer.

## Findings checked from saved outputs

There are **5,760 rows**, five methods on **1,152 unique product-weeks**, with no
duplicate method/product/origin keys. Every target equals its seven-day sum from
the pinned panel, and every scale equals seven times its product's mean 2010
daily sales. Independent arithmetic matched every primary, per-product, and
quarterly statistic with tolerances no looser than `rtol=1e-12, atol=1e-10`.

Zero's scaled MAE is **0.9860568865**, TSB's **0.9993053092**, and the 28-day
mean's **1.0049620102**. Raw-unit MAE instead favors TSB (**25.92123536**) over
the 28-day mean (**26.13368056**) and zero (**29.390625**). The report states
these results accurately. There are **669 zero-sales product-weeks** and
**33,858 recorded units**. The zero forecast's complete volume shortfall is
visible rather than hidden behind its narrow score advantage.

The median-versus-mean explanation is reasonable as motivation, not proof of
conditional optimality: unconditional sparsity alone cannot establish that
zero is the correct conditional median at every origin. The report says it
“helps explain” the outcome and declines an inventory conclusion, which is
appropriately limited. Scores are not evidence of significance from 1,152
independent observations, and the report does not make that claim.

Saved-output heterogeneity checks reinforce why conclusions must stay bounded:

- Zero wins 15 per-product scaled-error comparisons under the saved table's
  ordering; TSB wins 4, Croston-SBA 4, and last-week 1. Zero wins quarters 1–2,
  TSB quarter 3, and the 28-day mean quarter 4.
- Product code `17003` supplies **21,484 / 33,858 = 63.45%** of test units.
  Descriptively omitting that one code from saved rows changes the raw-unit MAE
  winner to the 28-day mean (**9.07156**) versus TSB (**9.28742**). This is a
  sensitivity illustration, not a proposed new cohort or replacement endpoint.
- Zero's overall scaled advantage over TSB is only **0.0132484**. Omitting
  `90181B` descriptively reverses that order: TSB **0.96147**, zero **0.97697**.
  This is not evidence that this code should be excluded. It shows the limited
  stability of a winner statement for a 24-code nonrandom panel.

## Presentation inspection and optional improvements

The saved `weekly-sales.png` was visually inspected at its native file size.
Both panels, numeric annotations, labels, and axes are legible and consistent
with the metrics. The zero forecast's `-100.0%` label sits inside its bar and
does not overlap the axis label. The left panel starts at zero and does not
exaggerate the small zero/TSB/28-day differences. The table reports raw MAE,
and the prose explains rate methods and the difference in product weighting.
README and portfolio claims reproduce the same bounded metric-dependent result.

The following are **optional enhancements, not uncorrected blockers**:

1. Put the small primary-score gap and one concrete concentration statistic in
   the report rather than relying entirely on linked CSVs. The quarter winners
   or 63.45% volume share would make heterogeneity more accessible. The prior
   statistical review already discussed the largest product; the new
   leave-one-code calculations above quantify the consequence without fitting.
2. Clarify what total bias cannot show. For the last-week baseline over contiguous
   weeks, the summed forecast minus actual telescopes to the pre-test week minus
   the final target week. Here that is **0 − 423 = −423** units, exactly its
   reported bias. Near-matching aggregate volume can therefore coexist with poor
   week-by-week allocation. Current raw MAE and business caveats already prevent
   a strong unsupported purchasing claim, so this would deepen the explanation.
3. Preserve a small hand-calculated Croston/TSB recurrence as a durable test.
   Existing invariants could pass some incorrect interval or smoothing updates;
   the manual probes in this and prior reviews close that gap only for the
   inspected revision. No test addition is needed to correct a demonstrated
   current recurrence defect, because none was found.
4. If expanding the investigation later, prespecify a simple conditional-median
   weekly comparator for the absolute-error objective, alongside rate forecasts.
   Its absence does not invalidate this frozen five-method comparison, and no
   post-result candidate should be inserted into the existing run.

## Accepted limitations and untested scope

The source is gross recorded sales under explicit transaction filters, not net
revenue or latent demand. Zero-filled dates do not establish stock availability.
The nonrandom training-selected cohort excludes new products and retains later
code inactivity. Case-sensitive identity and within-sheet repeated-row meaning
remain unresolved. Initialization is from the collection boundary rather than
known product birth. Prior-day reporting availability is assumed, not measured.
There are no inventory costs, service levels, profit outcomes, uncertainty
intervals, or generalization claims to other retailers. These are scope limits,
not evidence that the implemented arithmetic failed.

No full model run, alternative smoothing search, automatic code merging,
stockout reconstruction, new-source refresh, or operational validation was
performed. This reviewer did not browse the live portfolio deployment or
revalidate provider licensing; presentation inspection covered committed
README/portfolio text, report, story, and the local figure. The raw workbook
pass, output checks, and focused tests were local, bounded, session-managed,
and completed; no process was left running. One diagnostic script initially
used `groupby.observed`, which collides with pandas' `observed` option; changing
the reviewer expression to `groupby['observed']` completed that probe. This was
a review-script error, not a study failure.

## Exact inspected identities

The retained run records source commit
`2c0af60037ae691aae7e13c92cb37228215e5876` and protocol commit
`b369cc865d4eafaabe8e8f4d3b7ba26ae36bb0ba`. All **39 recorded source hashes**
match their historical Git blobs; the protocol commit matches that source
revision's design history. All **six retained output hashes** match the run
ledger. The current retail implementation, adapter, and design match the
recorded source bytes. No instrumentation patch was applied.

```text
572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb  data/raw/retail.zip
c99f629abc67df7eecf625f47bcdf8e294558f9a6a625747838bd48d317b7b53  data/snapshots/retail-daily-panel.csv.gz
ff182cabcef9a37ea81cadc0997ea2c4dd2ba02ed2586d44d472b05038fec275  data/manifests/retail.json
1335e7efa10e41ee7fc4a0a5cdf19294f1e77a6ba59fbec7a89f880d174324fc  reports/intake/retail.json
5d32c448121c5650ca38b4781b2f7ffe4ff1c0a19af059783eafd752e44c9fbb  src/tsatlas/retail.py
870801c933476d2133b0a233d3e85188b376ba93b33a8c75c88fc36ba03675f5  src/tsatlas/extended_data.py
95a699e75a84da2651dc70268c942232abb62c7cdbd75f6e0454dc14788d3468  src/tsatlas/common.py
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
bfe578cd417c166cba55ee069662773d4e135f5af55b8819a07de5006615751c  tests/test_retail.py
372ba374e5b26d9baefe1955a9568b6613cd68eb9c273c47f866f1077f147d08  tests/test_intake.py
ccbbae99f581992fc1f9111d14d076fd316fa7db93e56dcad43fd21ae29df840  studies/retail/DESIGN.md
ff169a5f6c4bcfd9d26a1ea1ed946a3944aaebcde0c51147ed9db0e5e99e67fe  studies/retail/STORY.md
b4a32c0f011fbeea823d95a84b15b1ed57a770e31ebae17b458dbaa46e17021d  reports/results/retail/REPORT.md
a0cb2c69370222904b3f0798069cd63bb0df6f44de8919636c53cbe9c8f391ff  reports/results/retail/metrics.json
ca96bcf0d9c4655635ab84e317126bb60038cbeee20112d4e61f6560211da2e6  reports/results/retail/predictions.csv.gz
0015d463a48c59bf9d30ce936c4df243a89126c847bf15195bdd6858f4d81350  reports/results/retail/per-product.csv
cd7d0e8be650b70e376c7595766414a8d0a1a621da950f047bbe41a29b1f5aa4  reports/results/retail/per-quarter.csv
0cebc13252d809986dafa26d8f3a41d4f6a134fe88bec5152c01e90b57c8b873  reports/results/retail/weekly-sales.png
e8195aafb0cd0a50494d2f5837a495424a245c7511bfdf3bfa466092931fec7b  reports/results/retail/run.json
1dc152d9288c02ca5f99ce8d801b409391ada1ed1d0a0f86e5c3ce0da6654650  README.md
9dc9066c3810b15df1cfb2750b1cce0059917c200a063dd7aab176ad31f0b0bc  portfolio.json
```

2026-10-30 status entry: RET-01 **identified** by this non-authoring reviewer at
revision `71999b34ccfd7127840b173efb287ac0a66b2a26`; no author response or
verification of a correction is claimed. The scope and optional checks above
must not be relabeled as changes to the frozen study.
