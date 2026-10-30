# Completion source and design review: retail, oil, air quality

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: the three draft `DESIGN.md` contracts, actual pinned raw inputs and
snapshots, their manifests/intake reports, and the corresponding functions in
`src/tsatlas/extended_data.py`. No candidate models or final score comparisons
were run. The reviewer did not author these contracts or loaders.

The checked worktree reports baseline and `origin/main`
`bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`; manifests record the parent's fresh
fetch at `2026-10-30T21:17:43Z`. This is review of the active completion changes,
not an experiment on a different source revision. Earlier three-study results
are outside this review and were not retuned.

## Separate verdicts

| Study | Source intake verdict | Design verdict |
|---|---|---|
| Retail | Approved for the declared recorded-sales target, with the documented data limits below | Approved to implement; pre-run implementation review still required |
| Oil | Approved for observed-date dollar changes; acquisition/snapshot values checked | Amend D01 before contract freeze/full scoring |
| Air quality | Approved for artificial single-station outage evaluation using the acquired hourly panel | Amend D02–D03 before contract freeze/full scoring |

No observed source-value corruption or demonstrated leakage was found. D01–D03
are prospective specification risks, **not executed bugs or empirical results**.
These source verdicts do not approve future model inputs or scoring code.

## Required design clarifications

### D01 — Oil recursion and train/target boundaries are not fully frozen

**Priority:** required before freezing and full test scoring. **Status:** identified.

The contract fixes decay, GARCH constraints and three optimizer starts, but not
the EWMA starting variance, GARCH conditional-variance initialization/backcast,
or which first training change is permitted. It also describes the training
period in terms of observations without explicitly assigning supervised examples
by target date. A training feature row dated 2014-12-31 can have a 2015 target;
origin-only slicing would train on the first held-out outcome.

Freeze the starting-state formula, recursion indexing and initial likelihood
contribution; declare whether the first difference uses a pre-2000 price or
starts with two in-period observations. Bound optimizer iterations/tolerance and
retain its convergence outcomes. Define train/test membership by **target date**,
with every feature at or before the previous observed-price origin. The first
test difference may legitimately use the last training price. Specify whether
the prevalence baseline uses the same eligible training target rows as logistic
regression; identical rows are the cleanest comparison.

**Closure evidence:** amended contract, then implementation assertions that the
last training target precedes 2015, first test features contain no test outcome,
and each variance is saved before the corresponding realized change updates its
recursion. Initialization must reproduce across reruns. No test-driven choice
among initializations is needed or justified.

### D02 — Specify whether the air outages happen one station at a time

**Priority:** required information-availability definition. **Status:** identified.

Every station currently has the same monthly scheduled start. The design also
uses the other eleven stations' simultaneous reports. These are compatible if
each target-station block is an independent **single-station outage scenario**,
with the other stations retaining their original observed values/missingness.
They are incompatible if all twelve scheduled outages are imposed together.

State the independent-scenario interpretation explicitly and identify it in
saved records. A shared-sensor/network failure is outside this experiment, as the
limitations already acknowledge. This recommendation does not require adding a
second correlated-failure experiment.

**Closure evidence:** amended contract followed by a mask invariant showing the
target station cannot enter the network median and only that target station's
simulated outage is imposed in its scenario. Actual missingness at peers remains
missing and contributes to the minimum-three-reporters rule.

### D03 — Freeze threshold ties and the macro-score denominator

**Priority:** required scoring definition. **Status:** identified.

The air contract correctly says undefined rates remain null. It should also
define what happens to the **macro station balanced accuracy** when a station's
eligible common hours contain no positives or no negatives. Computing one-class
accuracy, silently discarding the station, and returning an overall null are
different summaries. The discrete PM2.5 values also make `>` versus `>=` at the
90th-percentile threshold consequential.

Choose the threshold quantile method and comparator in advance, using only
observed training local concentrations. Define station balanced accuracy only
when both class denominators are positive; if macro-averaging the defined
stations, publish the included station count/list and exclude a station equally
for every method. Retain pooled confusion counts and per-station denominators
regardless. Spell out scheduled versus eligible versus common-scored hours for
coverage; dependent duration prefixes must not inflate replication counts.

**Closure evidence:** amended contract and small metric fixtures with absent
positive/negative classes and a value exactly on the threshold. Saved scenario
ledgers must reconcile scheduled, excluded, eligible and common-scored totals.

## Source facts and independent checks

### Retail

[UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
confirms the two-year transaction source, creator/citation, cancellation invoice
prefix, missing values, and CC BY 4.0 license. Its stock-code prose is simpler
than the actual workbook: inspected rows include numeric codes and letter
suffixes, supporting an explicit eligibility regex rather than an integer cast.
The study's 2012 citation year matches UCI's dataset citation even though the
page's donation date differs.

Independent read-only inspection verified the raw ZIP SHA-256/size against its
manifest, workbook member and both sheet headers/initial rows. The sheet starts
support the stated December 2010 cutover. The selected snapshot has 739 unique,
complete daily dates and 24 unique product columns, nonnegative integer units,
and no missing values. Each selected product's 2010 total and positive-day count
matches the intake report. The proposed scored schedule contains **48 complete
weeks, or 1,152 product-weeks**.

Loader inspection confirms the cohort eligibility/ranking uses only 2010; no
2011 sales or future discontinuation filter selects products. The raw filtering
categories are sequential and their reported counts reconcile to all 1,067,371
rows. This review sampled the workbook rather than independently re-aggregating
every transaction, so it does not claim a second full retail loader reproduction.

The target is appropriately bounded: retained gross recorded sales, not demand
or availability. Within-sheet duplicates remain a disclosed source ambiguity;
cancellations and nonpositive/correction-like rows are excluded explicitly.
The rank-spaced cohort is intentionally nonrandom, and its very different sales
scales justify both macro scaled errors and raw/per-product evidence. Signed
total error makes always-zero underprediction visible. Mean-based forecasts
are not guaranteed MAE-optimal for sparse sales, so a zero baseline winning MAE
would not establish a desirable purchasing policy. The current contract does
not claim that it would.

### Oil

The [EIA WTI page](https://www.eia.gov/dnav/pet/hist/RWTCd.htm) identifies the
series as Cushing spot price in dollars per barrel. The actual Brent XLS header
identifies Europe Brent spot price in the same units. [EIA reuse guidance](https://www.eia.gov/about/copyrights_reuse.php)
permits reuse of its government data with acknowledgment; retain source/date
attribution and do not generalize that statement to unrelated protected site
assets.

Both raw XLS SHA-256 hashes and sizes match the manifests. Independently parsed
raw market series, restricted to the snapshot dates, equal **every corresponding
nonmissing snapshot value**. The union has 9,697 dates, 8,222 common observed
dates and 1,475 missing market/date cells. Preserving those differing calendars
is correct. The raw WTI file contains the declared negative spot price, so dollar
differences avoid a log-transform failure without deleting that episode.

Next-observation horizon, calendar gaps, separate market scores, zero-inclusive
direction labels, no post-training refit, and the revised-data/reporting-latency
limit are appropriate. The variance score evaluates a conditional second-moment
forecast under the stated zero-mean convention; squared changes are noisy
proxies. It does not establish tail calibration or profitability. Direction and
variance scores remain separate; comparisons to their own baselines answer the
question without comparing incompatible score magnitudes.

### Air quality

[UCI Beijing Multi-Site Air Quality](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)
confirms 12 monitoring sites, hourly March 2013–February 2017 coverage,
PM2.5 units of micrograms per cubic metre, NA missingness, and CC BY 4.0.
The outer ZIP includes the unrelated small sample files; the loader selects the
specified full nested archive.

The raw ZIP SHA-256/size matches the manifest. Independent comparison of **all
12 raw station PM2.5 arrays and timestamps** to the snapshot passed. Each raw
file has one station identity, and the snapshot has 35,064 unique hourly dates,
12 unique columns and 8,739 genuinely missing concentrations. These were
preserved, not zero-filled. The source does not verify real-time publication
latency; treating nominal hours without an invented timezone conversion is
appropriately explicit.

The shift from prospective forecasting to contemporaneous outage nowcasting is
scientifically coherent when named plainly. All eligible targets are observed
before masking; naturally missing values are never scored as truth. Complete
blocks and fixed first-day/09:00 starts define a narrow, nonrandom simulation,
not the frequency or severity distribution of real outages. Network availability
must accompany conditional common-hour accuracy. The declared limitations cover
selection on observability and correlated failures; they remain accepted limits,
not problems that the simulation has solved.

## Implementation-review requirements carried forward

- Retail: verify nonoverlapping seven-day target totals, no double updating of
  daily state, and inclusion of January 1–2 history before the first Monday
  origin. Confirm SBA/TSB initial states and updates, scales and cohort IDs.
- Oil: verify D01 plus own-market observed-date differencing, lag windows, no
  leakage from cross-market forward fill, valid variance floors and explicit
  optimizer failures.
- Air: verify D02–D03 plus target exclusion from network features, training-only
  scaling/coefficients/thresholds, no local outage values or right endpoints,
  minimum peer count, raw and clipped fitted values, identical scoring masks.

No new method or additional final-data sensitivity is requested to pass this
review. Freeze these definitions, verify their implementation, then run the
declared comparisons and report whatever they show.

## Inspected file identities (SHA-256)

```text
1c6c22952105781ff6a82369df958e152b18103a539b0af841dd2715ef3bf78a  studies/retail/DESIGN.md
71599f40f7a21a7acf3c09a2d35ec2d395468229b64fd5748b20d0ceb14e2987  studies/oil/DESIGN.md
6e13abab56781de90d59c0db6c456bf596139e65272ce1398e0700c9187481de  studies/air-quality/DESIGN.md
1335e7efa10e41ee7fc4a0a5cdf19294f1e77a6ba59fbec7a89f880d174324fc  reports/intake/retail.json
4120dd53e6db0c14b3a1277563fb9d934e94d3f3f56c0cc2d148a27c9e7549ca  reports/intake/oil.json
6c6eb61a5d4ef68ef2a187395b803de674c34abe7149beb672bf1950a02f02bd  reports/intake/air-quality.json
aaf1096c3a90aa3ae739c97cce26412a10361a1d3dabfff99ab1d67434a88d8f  src/tsatlas/extended_data.py
ff182cabcef9a37ea81cadc0997ea2c4dd2ba02ed2586d44d472b05038fec275  data/manifests/retail.json
0024217008da826cf749bee93fbe85200f5ce9abf8526e49616b804b911b3990  data/manifests/oil.json
aefd807b20f4bff6ab06a5beb9e0d7c68fdb0e74d6c9e227ccd900664a642494  data/manifests/air-quality.json
c99f629abc67df7eecf625f47bcdf8e294558f9a6a625747838bd48d317b7b53  data/snapshots/retail-daily-panel.csv.gz
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/snapshots/oil-daily.csv.gz
1728af0edf50039ca234a58803f75bcc5e121c51b0fc9bef2c3d298f19a20fc5  data/snapshots/air-quality-hourly.csv.gz
572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb  data/raw/retail.zip
1f4c7c6c80c4ef6eb9e7b6c95e87c8df6439e3fb6ecccea72e9135bb37acf048  data/raw/wti.xls
c7c1e1eeb321fa5982f74747886963b35bd2df3c2f63960271c353421d5830ca  data/raw/brent.xls
b04da438b2f331ac0ffd45aebdfec0d20d2367feb5f6948c4b1f7ce1191e33c4  data/raw/air-quality.zip
```

## Status history

2026-10-30, statistical reviewer: source gates approved within the stated scope;
retail design approved to implement; D01–D03 identified and oil/air design freeze
pending. A later appended review must verify the author's amendments. No full
model run or result validation has occurred in this review.

## 2026-10-30 — Verification of oil and air contract amendments

The statistical reviewer reread the amended contracts and independently checked
the EIA source notes. No model was run and no final scores were inspected.

**D01: identified → design amended → verified at the contract level.** Oil now
assigns membership by target observation date, explicitly permits the first 2000
change to use the last 1999 price, and uses identical complete-feature rows for
the direction models. The EWMA and GARCH recursions, training-mean-square initial
variance, chronological training-state updates, GARCH fixed initial likelihood
variance, training-RMS numerical scaling, SLSQP budget/tolerance, convergence
criteria, and three predeclared starts are specified. This closes the design
ambiguity. Code review must still prove actual indexing, original-unit
conversion, constraint checks, and no test-outcome-dependent fitting.

**D02: identified → design amended → verified at the contract level.** Air
outages are explicitly separate single-station scenarios. Other stations retain
their real missingness. The half-open block `[s, s+L hours)` removes endpoint
ambiguity. Model-feature masking remains an implementation gate.

**D03: identified → design amended → verified at the contract level.** The
threshold uses linear quantile interpolation and a strict `>` comparison; ties
are low for predictions and truth. Station balanced accuracy requires both
actual classes. Undefined stations are excluded from its macro with the
contributing count reported, while other rates retain their denominators and
pooled confusion counts remain available. Because all methods use the same
common subset, this class-support exclusion is identical across methods.
Saved ledgers/per-station evidence must still establish every actual denominator.

**Added event summaries: approved at design level.** The amended air contract
defines consecutive high-hour events, left censoring at block starts, overlap
detection, conditional delay with misses/censoring, and false-alert episodes.
Abstentions break issued-alert runs and remain visible in misses. These are
explicitly block-local summaries; overlapping duration scenarios and a sustained
prediction touching several true runs are not counted as independent incidents
or distinct notification events. This is a bounded secondary description, not a
clinical, regulatory, or operational alarm-effectiveness claim. Implementation
fixtures must cover these exact censoring, overlap and abstention rules.

### Correction/clarification to the earlier oil source discussion

The earlier source section described EIA's **general** government-data reuse
policy but did not independently close the price data's third-party ownership
question. It must not be read as approval to republish these raw prices. The
[specific EIA spot-price source notes](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
identify **Refinitiv, an LSEG business**. The generic public-domain language does
not by itself establish that these underlying third-party prices are openly
licensed. This source fact was independently verified in this follow-up.

The amended oil contract adopts the acceptable fetch-only/local-input path:
raw workbooks, normalized price input and full true-change outcomes remain
outside Git; original forecasts, aggregate scores, parameters and hashes are
public. Local rescoring reconstructs truth from pinned inputs. A later source
refresh may differ, and the normalized analysis-input hash must match before
claiming exact reproduction. This is an explicit acquisition limitation, not a
new source license determination.

**Packaging remains unverified:** at this inspection, the raw directory is
ignored, but `data/snapshots/oil-daily.csv.gz` is untracked and is **not yet
ignored** by `.gitignore`. The contract therefore states the intended policy;
it does not prove publication exclusion has been implemented. Before staging or
publishing, move/ignore that input and verify tracked files and generated public
results exclude the complete underlying price/change series. This packaging
follow-up does not prevent local modeling after implementation review.

### Updated verdict and inspected identities

**Oil and air-quality design gates are approved to implement from the statistical
perspective.** Retail's earlier design approval remains. The source-value checks
remain valid; oil source approval is expressly for local analysis, with its
fetch-only public reproduction limitation. Full runs still require the separate
pre-run implementation gate, and publication still requires concrete artifact
and claim review. No finding is represented as an executed bug or verified
analytical result.

```text
8bc0e4e5723e23beb7c729a2128f78ce62d5f2900700d558dce049fda8f8f16e  studies/oil/DESIGN.md
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
aaf1096c3a90aa3ae739c97cce26412a10361a1d3dabfff99ab1d67434a88d8f  src/tsatlas/extended_data.py
```

**Subsequent packaging verification, same date:** the author moved the oil
snapshot into `data/processed/oil-daily.csv.gz`. The reviewer confirmed that
`git check-ignore` identifies that path, the old public snapshot path no longer
exists, and the input SHA-256 is unchanged. The intake record now identifies the
private path and `fetch-only` availability. This verifies the current snapshot
exclusion, closing that narrow packaging follow-up. Generated result files do
not yet exist and still need the planned publication-content check.

```text
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/processed/oil-daily.csv.gz
a3a388c33094c2bd00af2cddb12ed32a634b161956c7040dbf49e03c4b39aa00  reports/intake/oil.json
fafaf2e42d1e98f74390fed96032f216046947d245ff34c5736a1a738311129f  .gitignore
```
