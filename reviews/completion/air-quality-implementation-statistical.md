# Air-quality pre-run implementation review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: `air_quality.py`, `classification.py`, the focused air tests, reviewed
contract, and finite-only development execution. The reviewer did not author
implementation or tests. No March 2016–February 2017 accuracy scores or final
model-comparison outputs were inspected.

**Final verdict: statistical pre-run implementation gate approved for the
declared single-station outage experiment.** The coverage issue below was
corrected and verified before the full run. Committed-source and other reviewer
gates remain applicable. Actual final results, reproduction and publication
remain separate reviews.

## AQI-S01 — Separate scoreability from peer-input availability

Type: observed coverage-output/interpretation mismatch, found before full scoring.
Priority: correct before reporting availability.

Initially, `network_fraction_of_scheduled` counted peer-available hours only
after discarding entire blocks without complete local truth or a prior reading.
It therefore combined truth eligibility with network-input availability. Calling
it simply hours with network estimates could imply network downtime that was
actually missing evaluation truth. The forecast predictions and primary common-
hour classification calculation were unaffected.

The author moved the peer-count calculation before truth-based block exclusion.
Every scheduled block now records `peer_available_hours`. Coverage separately
reports eligible hours, scoreable network hours, and peer-input availability over
all scheduled hours. The figure/table labels and report identify these separate
quantities and explicitly do not call them operational uptime. The extended
fixture has missing local truth but six peer-available hours, proving the
numerator is retained even for an unscoreable block.

Status: identified → implemented → verified, 2026-10-30. Final output totals
must still reconcile with the saved schedule at results review. No forecast was
retuned to address this evidence-label problem.

## Availability and fitting checks

The ridge model, scaler, calendar medians, fallback and local 90th-percentile
threshold use only the training period through February 28, 2015. Target-specific
network features drop that station entirely; no local value can enter its
peer median. Training needs known local truth and at least three observed peers.
The explicit per-station Ridge alpha is 1 and does not depend on final outcomes.

Each scenario uses its declared half-open sequence of hourly timestamps.
Persistence takes the last known local reading strictly before the block within
the preceding 24 hours. Network features use only other stations' contemporaneous
values; future endpoints and local values inside the outage do not enter any
prediction. Real peer missingness is preserved, and fewer than three peers cause
both network models to abstain. The source supports this retrospective simulation
under a timely-report assumption, not actual deployed reporting latency.

The ridge output is clipped at zero and its unclipped values remain saved.
Calendar and persistence predictions remain available beyond the common-network
subset; separate available-hour scores retain their broader population. Local
truth eligibility is used for scoring scenarios, not presented as a real-time
sensor's ability to know its future outage measurements.

## Scores, event logic and denominators

The primary cohort uses common peer-available hours for all four methods.
Strict concentration greater than the training threshold labels high pollution;
ties are low. `binary_scores` returns explicit counts, precision, recall and
false-positive rate, with undefined denominators null. Balanced accuracy requires
both actual classes. The macro drops only undefined station BAs and reports the
contributing count; counts for all scored stations remain saved. Macro MAE is a
separate equal-station concentration-error summary.

Pooled confusion counts and the newly explicit pooled rates are calculated from
the underlying counts, not by averaging station ratios. Those pooled rates and
the macro station BA have different weights and are named accordingly. Quarterly
scores remain descriptive; overlapping outage durations are not represented as
independent replications.

Event logic operates on each full eligible, time-ordered block/model. True high
runs are independent of prediction availability. A high run starting at the first
block hour is left-censored for onset delay; right censoring is also retained.
Any overlapping issued high prediction detects a run. Delay is measured from the
run's start only for detected, non-left-censored events. Misses remain in event
counts, including those caused by abstention. False-alert episodes are predicted
high runs with no true-high overlap; abstention breaks a predicted run. This
matches the frozen block-local interpretation and does not establish unique
population pollution incidents or actual alarm notifications.

## Executed bounded checks

- `uv run pytest -q tests/test_air_quality.py`: **4 passed** after the coverage
  correction. Fixtures exercise target-station removal, minimum peer counts,
  local/future-value mutation invariance, exact half-open block length, undefined
  one-class rates, event censoring/delay/misses, and retained peer availability
  when local truth is missing.
- An independent synthetic-panel check changed all post-training data and
  reproduced the fitted scaler, ridge coefficients and threshold exactly.
  Independent confusion arithmetic produced BA 0.75 from TP=2, TN=1, FP=1, FN=0.
- A separate threshold-tie fixture confirmed true values equal to the threshold
  are low, a missing prediction splits two false-alert episodes, and a one-class
  subset has null BA instead of a fabricated perfect score.
- The reviewer ran a **current-source finite-only trial**: Aotizhongxin,
  March 1, 2015 at 09:00, six hours, 24 method/hour prediction rows. All predictions
  were finite, six hours had sufficient peers, and the source hash was unchanged
  across the trial. No accuracy was computed. This verifies the amended code,
  independently of the earlier author trial record tied to the pre-fix source.

The focused tests emitted existing NumPy timedelta deprecation warnings but no
failures. Exact block timestamps and date arithmetic were independently checked;
future dependency changes must rerun these invariants.

## Inspected identities and execution scope

```text
f553a836e2eae2be550f72a6397a1c7ce2057b6e5f2a45a0a1ae2400c8f8c851  src/tsatlas/air_quality.py
36a342dd2c23a9826d25a478a7a85028c70e6f93395f7e7befc3571de580fd6a  src/tsatlas/classification.py
f9be97008368484c68bed34dcb86530cbe8b1bd3e8620d03b1e0cff913add8a9  tests/test_air_quality.py
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
940af75e51501e090f8df8e5e3108439b0a087b784b2e8e06a46ce2d9eb6237f  reports/verification/air-quality-development-trial.json
```

The last listed author trial is historical pre-coverage-fix evidence; the
independent amended-source trial described above supplies this review's current
execution evidence. No full model-comparison run was performed here.

2026-10-30, statistical reviewer: AQI-S01 verified; statistical implementation
gate approved. Final empirical rankings, observed exclusion/coverage totals,
event denominators and public artifact claims remain unreviewed.
