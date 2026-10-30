# River-flow results and provenance review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: full run from `7e6c91d4777beccb3abb05870e880918197ae93f` (also its
protocol commit), saved predictions/parameters, source/split provenance, event
evidence and aggregate scores. No model was refitted or tuned by the reviewer.

**Artifact and numeric verdict: pass. Publication remains pending final
narrative updates and clean-checkout reproduction.** No scoring, temporal
alignment, source-hash or event-ledger mismatch was found.

## Independent reconstruction

All **37 recorded source hashes** match their historical Git blobs, all **ten
output hashes** match retained artifacts, and the pinned river snapshot matches.
The run records stable source, 6.28 seconds elapsed and approximately 399 MB
process-lifetime peak RSS; these are local execution measurements.

The reviewer independently reconstructed every gauge's approved-flow mask,
daily feature vector, training quantile, training scaler statistics, target
alignment, origin-safe split masks and negative-calibration score cutoff. Saved
logistic parameters and the persistence definition then reproduced all
**288,417 dated predictions**, including raw target flow, high/low truth and
strict-cutoff alerts. No optimizer or classifier fit was invoked. All recorded
convergence warning lists are empty.

All **34 split-audit rows** match source-based counts, including boundary
exclusions, invalid-input/target intersections/unions and coverage reconciliation.
Horizon three excludes January 1–2 at calibration/test boundaries; no such
exclusion is needed at horizon one. Each model shares 48,262 eligible targets
at horizon one and 47,877 at horizon three across the fixed 17 gauges. All
gauge/horizon pairs have every model; the unmatched list is correctly empty.
No failed gauge was replaced or silently removed from method contrasts.

Metadata area/HUC and training-only cold-precipitation fractions match their
source values. Area/climate assignments agree with the declared cutoffs.
All **102 gauge-score rows**, **30 subgroup rows**, primary macro rates,
contributing-gauge counts, pooled confusion counts and probability Brier scores
were independently recomputed. Counts match exactly; numeric checks used
`rtol=1e-10, atol=1e-11`. Persistence has null Brier and zero Brier contributors.

## Event audit

Independent calendar/run traversal reconstructed every field of **10,158
event rows**: 5,886 high-run records, 3,915 fully observed false-alert episodes,
and 357 unresolved alert segments. Repeated high-run records across model and
horizon are intentional; they are not 5,886 independent flood incidents.
The underlying 981 runs per model/horizon include 103 censored starts and 878
known onsets. Origin/target dates, preceding/intervening non-high requirements,
forecast coverage, onset alerts, missing-truth right censoring, and uncertain
alert-segment classification all match the pinned source and prediction ledger.

Every onset aggregate agrees with this independently reconstructed ledger.
Horizon one has 822 eligible onsets; horizon three has 696, reflecting its more
restrictive prospective-origin history stratum. The eligibility rule uses future
truth for retrospective scoring only, not as an input filter or operationally
observable trigger. Unknown truth cannot establish a wholly false alert episode.

## Interpretation and presentation

The figure was visually inspected and its bars agree with the metrics. It
separates macro gauge high-day recall from pooled eligible-onset recall; the
different aggregation units are disclosed. The adjacent table pairs recall
with actual false-positive rates, roughly 14–15%, rather than presenting the
calibration target of 10% as a test guarantee.

High-day recognition is easier than warning before a new run. At horizon one,
weather raises alerted eligible onsets from 467 to 496 relative to flow-only,
while fully observed false-alert episodes increase from 653 to 830. At horizon
three, weather raises the alerted count from 165 to 166 out of 696, while false
episodes increase from 547 to 697. These descriptive comparisons do not establish
reliable incremental benefit, operational warning utility or flood-damage value.
The result narrative should state that tradeoff plainly rather than implying
that adding weather broadly solves onset prediction.

The report correctly limits the study to geographically spread known gauges,
retrospective daily weather and an idealized issue-time assumption. It avoids
ungauged transfer, representative-river, hourly lead-time and damage claims.
Calendar offsets are not measured 24/72-hour warning times. Process-story
updates should preserve the actual design-origin and event-censoring corrections
and link their reviews, followed by the observed results.

## Remaining checkpoint and hashes

No clean-checkout reproduction or final publication is claimed here. The parent
plans that checkpoint after report/story finalization; renderer refreshes must
retain or explicitly reconcile these numerical artifacts and record new source
and output identities honestly.

```text
16fb0481f248a75068f8acc55e505df1e2dea46e02b35c692fc7e81deca15ba3  reports/results/river-flow/run.json
0af39059acf633a74c818405bef3d2340957e2bb2f06028da060475f5f72b33b  reports/results/river-flow/metrics.json
530a67b01853c859d34780f0e82e1753d0ca85cc0fc798ad4fcf1fb2bb98588f  reports/results/river-flow/predictions.csv.gz
ed6454881bf8ff270d43b90a8b83aadbea1e2fcad23cbb836636929780bbf2e6  reports/results/river-flow/events.csv.gz
7be3a0a749cc3ee3f93c2e0b7e22df75e29b926319d17d2e9204136c431f0192  reports/results/river-flow/REPORT.md
f6eac62831ded8233484a88b16c7da93db2fb69bf1a3adc253a731749d109df2  reports/results/river-flow/parameters.json
ec32436c279cce849bddd658a20141f7b15647216b07b14982ba679339d80905  reports/results/river-flow/split-audit.csv
fd2b4ac1d3bc7ffacaa03a28ab356ef57be846eb07078360aec2b9a1dda5d5c8  reports/results/river-flow/flow-and-onsets.png
```

## 2026-10-30 — Boolean warning cleanup verified before report refresh

The updated source replaces `issued.fillna(False).astype(bool)` with
`issued.eq(True)` to avoid a pandas downcasting warning. The reviewer compared
both expressions on every actual gauge/horizon/model's restored daily calendar:
all **372,504 Boolean entries** match exactly, including unissued dates. This
verifies equivalent event-mask semantics for the retained run. Narrative/label
edits and this cleanup await the parent's committed refresh and numerical-byte
comparison; the earlier run evidence is not relabelled as a newer execution.

```text
7f2799251a0af2ad0c26d68c9f48ed98871abe7e770c387a4ea0249d9c74a545  src/tsatlas/river_flow.py
```
