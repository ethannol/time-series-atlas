# Retail, oil, and air-quality source/design review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: three new raw manifests, the intake adapter and audit/snapshot outputs,
and the draft contracts. Baseline is `bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`,
freshly fetched by the primary agent at 21:17:43Z. No candidate model or final
evaluation was run by the reviewer. Source reconstruction below used an
independent read-only script, not a call to the authored intake functions.

**Source verdict: pass for all three inspected pinned snapshots.** The source
choices and transformations support the declared targets, with the limitations
recorded below. **Design verdict:** retail is ready from this perspective;
oil and air-quality need the bounded specification amendments C-D01 and C-D02
before their contracts are frozen. No model implementation approval is implied.

## Independent source verification

All three raw manifests' byte sizes and SHA-256 hashes match the local files;
their audit references agree. All retained snapshot sizes/hashes match their
audits. Official access/license checks are recorded in the preceding
[source implementation review](source-implementation.md).

### Retail

The reviewer independently streamed every row of both workbook sheets,
recomputed the filters, aggregated sales, applied eligibility/ranking, and
compared the resulting selected daily matrix exactly to the snapshot.

- Sheets contain 525,461 and 541,910 rows, totaling 1,067,371. Their observed
  date ranges match the audit.
- The overlap from December 1–9, 2010 is **exact multiset equality across all
  eight source columns**, including multiplicity: 22,523 rows in each sheet,
  with 22,523 common rows. Choosing the later sheet for this overlap removes
  duplicated source payload; it does not discard a different competing version.
- Recomputed exclusions match: 22,523 overlapping rows, 84,865 non-UK rows,
  16,349 cancellations, 3,802 non-merchandise-code rows, and 5,907 nonpositive
  quantity/price rows. The remaining 933,925 rows are the declared gross-sales
  population, not a count of unique orders or customers.
- Independently selected 2,072 eligible products from 2010 only, sorted by
  annual units with stock-code tie ordering, then the same 24 equally spaced
  ranks. Every value in the resulting 739-day panel equals the snapshot.

The first-half/last-quarter requirement and 10–146 active-day criterion depend
only on training data. Later disappearance remains in the target rather than
silently removing difficult products. Missing customer IDs do not prevent
product-level aggregation. Keeping unresolved repeated within-sheet lines is an
explicit limitation, distinct from the verified cross-sheet duplication above.
The code preserves case-sensitive source codes rather than claiming an audited
product-identity crosswalk.

The contract describes gross recorded units, complete weekly evaluation windows,
the origin's assumed reporting cutoff, a fixed cohort, and nonzero training
scales. Its always-zero and signed-error reporting prevents an absolute-error
winner from being presented as an adequate inventory policy. Zero-filled days
do not establish stock availability or latent demand. These distinctions make
the question answerable with the actual records.

At implementation review, verify daily Croston-SBA/TSB recurrence initialization,
elapsed-interval counting, the SBA adjustment, and updates through January 2
before the first January 3 origin. Prove future daily observations cannot change
earlier weekly forecasts. These are forthcoming implementation checks, not
defects observed in an implementation that has not yet been written.

### Oil

The reviewer independently parsed both `Data 1` sheets and reconstructed the
union-calendar snapshot with its end-2025 cutoff. Every value and missing mask
matches. The actual raw data contain the negative WTI price identified in C-I05;
the contract retains it and uses dollar changes. Own-observation calendars,
saved gap lengths, separate market scores, and the explicit revised-data
availability assumption are coherent. There is no need to impute an artificial
zero weekend change or align an unused cross-market predictor.

The squared-change variance target is a noisy proxy and the proposed
log-variance score is a declared quasi-likelihood comparison. The contract
correctly separates direction scores from variance scores and avoids a trading
or tail-calibration conclusion. Training-only optimizer selection is allowed;
failed attempts must remain in the record as stated.

### Air quality

The reviewer independently read all 12 nested station CSVs, confirmed one station
identity per file, 12 distinct identities, and the exact common hourly grid.
Every PM2.5 vector and missingness mask matches the snapshot. This independently
closes the specific payload-selection concern C-I04 for the inspected adapter.
The adapter selects the full nested files, not the outer small CSV companions.

The contract makes the experiment a contemporaneous nowcast under an explicit
availability assumption. It preserves natural gaps, scores only known truth,
hides continuous local blocks, keeps source-station counts, and reports network
abstention rather than scoring unavailable predictions as if observed. Complete
block eligibility is correctly identified as a limitation, and the nested
durations are not falsely counted as independent replications.

At implementation review, require future/end-of-block perturbation checks and
confirm that target-station values cannot enter the other-station median.
Verify unique station names explicitly; the present pinned payload is unique,
although a column-count-only check would not detect duplicates in future inputs.

## C-D01 — Freeze variance initialization, optimization budget, and target dates

Priority: medium; amend before freezing the oil design. Status: `identified`.

The draft fixes models and GARCH parameter constraints/starting points, but not
the first conditional variance, exact EWMA/GARCH recurrence state, or optimizer
method and iteration/tolerance budget. Those choices affect deterministic
execution and what constitutes a failed fit. State them before fitting, including
whether the initial scale is mean squared change or centered sample variance.

Also state split assignment by target date and the first eligible training
difference. In particular, clarify whether a price immediately before January
2000 may form the first training change, and whether pre-2000 changes are allowed
only as lag history or excluded entirely. Direction baseline and regression
training populations should be explicit so feature warm-up is auditable. These
are specification gaps, not evidence that leakage or a fit failure occurred.

## C-D02 — Freeze threshold ties and exact outage endpoints

Priority: medium; amend before freezing the air-quality design. Status:
`identified`.

PM2.5 values are often discrete, so `>` versus `>=` the training 90th percentile
can change event labels materially. Specify the quantile interpolation method
and the same strict/non-strict comparison for observations and every prediction.
Specify durations as an exact set of hourly labels, preferably the half-open
interval `[start, start + duration)`, so a six-hour outage contains six labels.
Retain the already declared null handling and denominators for undefined rates;
macro scores should expose how many stations have defined class-specific rates.

## Publication follow-through

The current `data/README.md` still documents the first two real datasets only.
Before publishing the new snapshots, add each new source/DOI, license/reuse
notice, transformations, cutoff, and pinned-source reproduction path. This is
routine unfinished publication documentation, not a reason to block source
inspection or design refinement. The new studies also remain subject to C-I01's
historical-provenance correction and their later implementation/result gates.

## Inspected SHA-256 hashes

```text
aaf1096c3a90aa3ae739c97cce26412a10361a1d3dabfff99ab1d67434a88d8f  src/tsatlas/extended_data.py
1c6c22952105781ff6a82369df958e152b18103a539b0af841dd2715ef3bf78a  studies/retail/DESIGN.md
71599f40f7a21a7acf3c09a2d35ec2d395468229b64fd5748b20d0ceb14e2987  studies/oil/DESIGN.md
6e13abab56781de90d59c0db6c456bf596139e65272ce1398e0700c9187481de  studies/air-quality/DESIGN.md
1335e7efa10e41ee7fc4a0a5cdf19294f1e77a6ba59fbec7a89f880d174324fc  reports/intake/retail.json
4120dd53e6db0c14b3a1277563fb9d934e94d3f3f56c0cc2d148a27c9e7549ca  reports/intake/oil.json
6c6eb61a5d4ef68ef2a187395b803de674c34abe7149beb672bf1950a02f02bd  reports/intake/air-quality.json
ff182cabcef9a37ea81cadc0997ea2c4dd2ba02ed2586d44d472b05038fec275  data/manifests/retail.json
0024217008da826cf749bee93fbe85200f5ce9abf8526e49616b804b911b3990  data/manifests/oil.json
aefd807b20f4bff6ab06a5beb9e0d7c68fdb0e74d6c9e227ccd900664a642494  data/manifests/air-quality.json
c99f629abc67df7eecf625f47bcdf8e294558f9a6a625747838bd48d317b7b53  data/snapshots/retail-daily-panel.csv.gz
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/snapshots/oil-daily.csv.gz
1728af0edf50039ca234a58803f75bcc5e121c51b0fc9bef2c3d298f19a20fc5  data/snapshots/air-quality-hourly.csv.gz
```

Later resolution verification belongs in a dated addendum; do not rewrite the
initial findings as though the missing specifications were present initially.

## 2026-10-30 — Amendment verification and oil acquisition boundary

Reviewer: `/root/implementation_critic`. This is a design/documentation check,
with a narrow check of the relocated oil input. No model evaluation was run.

**C-D02: verified at the design checkpoint.** Air quality now declares pandas'
linear quantile interpolation, strict `concentration > threshold` for both truth
and predictions, and exactly L hourly labels in `[start, start + L hours)`.
The contract defines single-station scenarios, undefined balanced accuracy, and
contributing-station counts, and adds explicit block-local event evidence.
The previous implementation-scope precautions remain for the next gate; this
verification does not establish executed behavior.

**C-D01: mostly amended, narrow clarification pending at this inspection.**
The oil contract now specifies initial mean squared change, exact variance
recurrences, SLSQP/500 iterations/1e-9 tolerance, training-RMS conditioning,
convergence checks, target-date membership, identical direction training rows,
and population rolling standard deviation. The older phrase initializing omega
with “training variance” should use the exact intended definition, consistent
with the new mean-square wording. Also state explicitly whether pre-2000 changes
may supply lag features; this avoids ambiguity with the retained statement that
prior observations are not fitted. The reviewer requested these two final
wording corrections before closing C-D01.

### Oil input remains local; reproducibility requires acquisition

The revised contract correctly identifies that EIA's official
[spot-price source notes](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
name Refinitiv, an LSEG business. The generic EIA reuse policy alone is
insufficient evidence to label these particular prices government-owned or
freely redistributable. This qualifies the initial feasibility discussion's
generic EIA-policy reference; it is not a newly verified redistribution license.

The design therefore keeps raw workbooks, normalized source prices, and complete
true changes local, while publishing analysis forecasts, parameters, aggregate
scores, and hashes. The reviewer confirmed the old public snapshot path is
absent, the normalized file is now `data/processed/oil-daily.csv.gz`, Git ignores
that path, and its bytes still match the independently checked original
normalized-input hash. The audit records `availability: fetch-only` and its
explicit private path. This verifies relocation and the design decision only.

The proposed exact-reproduction rule is sound: acquire the public source,
normalize the declared historical window, and require its pinned hash before
claiming exact reproduction. A revised provider history may prevent new users
from obtaining the exact historical input. State that limitation in public
commands/CI evidence; missing private data cannot count as a successful full
oil reproduction. The acquisition/validator implementation and public-output
redaction will be reviewed later. Retail's verified overlap belongs in the
story/review evidence without silently rewriting the earlier deterministic audit.

```text
8bc0e4e5723e23beb7c729a2128f78ce62d5f2900700d558dce049fda8f8f16e  studies/oil/DESIGN.md
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
fafaf2e42d1e98f74390fed96032f216046947d245ff34c5736a1a738311129f  .gitignore
a3a388c33094c2bd00af2cddb12ed32a634b161956c7040dbf49e03c4b39aa00  reports/intake/oil.json
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/processed/oil-daily.csv.gz
```

## 2026-10-30 — Oil design clarification verified; freeze approved

**C-D01: verified at the design checkpoint.** The final wording initializes
omega using the training mean squared change and explicitly permits pre-2000
changes only for lag-feature warm-up, excluding their targets from fitting,
prevalence, scale, and initial-variance statistics. This resolves both remaining
ambiguities without a new model or inspected evaluation result.

**Design verdict: retail, oil, and air quality are ready to freeze and implement
from the data/implementation perspective.** C-D01 and C-D02 are closed for the
specification, not as claims of verified model behavior. Oil's fetch-only input
boundary and eventual acquisition/reproduction checks remain as documented above.

```text
64e2b98cd9f2a653bd8444412be50500a4007a211560045390e8f16e7515b2ef  studies/oil/DESIGN.md
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
```
