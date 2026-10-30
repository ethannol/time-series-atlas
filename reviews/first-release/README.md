# First release: checkpoint record

Baseline fetched 2026-10-30T16:14:39Z: origin/main
`d7218096c7920e30da3ad722a3d1bffbede8fa4e`. Clean checkout; branch
`feat/first-studies`. Planning scaffold was published before implementation.

## Source intake

[Statistical review](source/statistical.md) and
[implementation review](source/implementation.md) inspected actual pinned files.
Both found source descriptions differed from observations. NOAA negative-standard-
deviation rows had zero uncertainty; UCI spring-DST zero handling was not uniform.
The adapter conservatively flags either negative NOAA metadata field, distinguishes
early Scripps unknown metadata, and identifies DST by calendar rather than values.
These are new observed source findings, not merely the initial prospective risks.

Source verdict: sufficient for design with explicit scope/quality conventions.
Code behavior is not yet approved. [Audit and source notes](../../reports/intake/README.md).

## Design review and freeze

[General](design/general.md), [statistical](design/statistical.md), and
[implementation](design/implementation.md) critics reviewed all three contracts
and verified their requested clarifications before any model fitting:

- CO₂ results cover December-origin January/December targets, not all months.
- Electricity peaks exceed a fixed training-year percentile; learned predictions
  share zero clipping with raw values preserved; Ridge penalties are equal per row.
- Synthetic initial condition, standard deviation, score recurrence, threshold
  comparison, shift units, and outcome denominators are explicit.

Design verdict: ready to freeze. Contracts will be committed before bounded
implementation trials and full runs. This does not verify numerical behavior.

## Initial implementation/results status, before the gates below

At that point these stages were pending. No full model run or scientific conclusion is authorized by a design-only
review. Independent implementation review follows bounded tests/trials.

## 2026-10-30 — Pre-run implementation gate completed

[Statistical implementation review](implementation/statistical.md) reproduced two
invalid-input scoring defects: NaNs could be omitted while retaining the count,
and vector shapes could broadcast instead of pairing. Both now raise explicit
errors, with independently verified regression tests. The original finding and
resolution remain in the review.

[Implementation review](implementation/implementation.md) required start/end source
hash checks, committed-source full runs, staged result promotion, UTC timestamps,
and honest month/peak-memory labels. These were implemented and verified.
The final check artifact records 16 passing tests, including bounded future-data
perturbation checks. A two-customer January 2013 trial exercised the implementation;
no final evaluation scores were used to make model choices.

Both technical perspectives approve committing the reviewed source and running
the frozen studies. Results/interpretation and publication review remain pending.

## 2026-10-30 — First results reviewed, presentation and evidence gate revised

The critics independently recomputed the headline metrics from saved predictions.
They agreed with the bounded interpretations, but requested clearer customer-level
magnitudes, readable model names, delay units, and current-status wording.
The first scatter hid most small customer differences; a labelled difference plot
and table replace it without changing the experiment.

Publication review also found a real verification defect: the evidence validator
could pass when expected study records were missing. It now requires all declared
studies, matching names, and nonempty evidence maps, with regression tests.
A fresh checkout reproduced every original result output exactly without raw
source downloads; [comparison evidence](../../reports/verification/reproduction-initial.json)
records this separately from merely checking a generated manifest against itself.

These are presentation/verification changes after seeing results, not changes to
models, split choices, thresholds, or scoring. A committed refresh run will update
source/output evidence, followed by reproduction and final publication checks.

## Local publication gate

All three perspectives approve the first-release scope:
[general](results/general.md), [statistical](results/statistical.md), and
[implementation](results/implementation.md). Headline metrics were independently
recomputed from saved predictions. The refreshed presentation preserves the
original model predictions and metrics.

[Final fresh-checkout reproduction](../../reports/verification/reproduction-final.json)
matched all fifteen result outputs exactly on this machine;
[raw-intake regeneration](../../reports/verification/raw-intake-reproduction.json)
also reproduced both analysis snapshots and their audit. This is not a promise
of bitwise identity on every platform. Offline checks now contain eighteen tests.

RI04, the stale portfolio build, was corrected by rebuilding after the output
commit; the reviewer checked every pinned Atlas link against Git. Integration uses
isolated worktrees and leaves Ethan's dirty portfolio checkout unchanged.

Rollout order: Atlas to main first, then independent portfolio/profile PRs. All
three repositories allow merge commits; Atlas retains the design-before-fitting
commit history. At scope reconciliation there were no existing open PRs in these
repositories. Only this task's three new PRs are in scope; no drafts or unrelated
work are included. CI and deployment are followed to completion after publishing.

Integration baselines fetched 2026-10-30: portfolio
`e7235937fb91177b56712a7f8cfa52d16757d566` at 16:39:04 UTC; profile
`1434b98c8a78f2a2be5ae3dfdcb2e6d14005102b` at 16:39:05 UTC.
