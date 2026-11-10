# Optional follow-ups: data and implementation design review

Date: 2026-11-10. Role: non-authoring automated data/implementation critic.
Checkpoint: source availability and proposed design, before new full comparisons.
Baseline: `1a0ec0180b857f7d98b092a8104a575657d53445`; HEAD and origin/main
both match the parent's recorded fresh baseline. No fits, simulations, tests,
network acquisition or implementation edits were performed in this review.
Read AGENTS.md, docs/REVIEW_PROTOCOL.md and the standing execution/freshness notes.
Reviewed follow-up contract SHA-256:
`9e1a93c1f7dd976bfda67a45a14b7b3f67409e626d1de3f875e9456e59b05951`.

## Verdict

The proposed source, time semantics and finite comparison scope are feasible.
No new source/target or leakage defect was found in the design. Proceed with
implementation, then require the separate implementation checkpoint below before
full runs. This is design approval, not verification of code that does not yet
exist. Original publication limitations remain applicable.

## Evidence checked

- Exactly **49 existing numerical artifacts** occur under reports/results
  (CSV, CSV.GZ and JSON excluding run.json). Every current byte hash matches
  the blob in the stated baseline. Preserve this explicit original file set;
  counting all numerical files after additions would conflate new and old work.
- All seven distinct analysis snapshots exist and match intake SHA-256 hashes,
  including private `data/processed/oil-daily.csv.gz`. Both original raw files,
  the retail/air-quality/ECG archives, two oil workbooks and all 114 CAMELS
  member files exist locally and match their manifest hashes. No acquisition,
  upstream refresh or new redistribution decision is needed for this scope.
- Existing spectral inputs retain actual time/value pairs for all original
  realizations. Synthetic metrics retain both calibration maxima and thresholds.
  ECG retains predictions, people, training membership, fold assignment and
  model audit records. These support the proposed posthoc calculations.
- CO2 saved predictions contain both 12- and 36-month predictions for all
  62 linear-model/origin pairs, including calibration; every required origin
  observation passes the existing positive-value/metadata usability rule.
  The anchoring identity is supported by the shared December seasonal term.
- Retail snapshot has 24 columns and 739 daily rows from 2009-12-01 through
  2011-12-09. The earliest test origin, 2011-01-03, has a complete 364-day
  calendar window starting 2010-01-04. Monday alignment gives 52 complete
  preceding Monday–Sunday weeks without using the target week.
- `ecg.fold_indices` groups by person, uses the fixed 1,000-beat cap and
  `SEED + fold`; `fit_fold` fits PCA/scaling on training data and forest uses
  `n_jobs=1`. `studies/ecg/folds.json` already maps records 201/202 to person
  201. New assignments can reuse these functions without changing the policy.
- Existing run evidence records ECG at 35.82 seconds and spectral at 5.09
  seconds; these are historical measurements, not guarantees for this revision.
  Fifteen additional ECG fits and 900 spectral realizations are bounded and
  plausible locally. The recorded RSS is process-lifetime peak, not each
  study's isolated memory use; do not sum it as per-study consumption.

## Required implementation gates (not observed result defects)

**D1 — shared contract guard.** `common.source_snapshot` and `start_run` currently
include only the study-specific DESIGN.md. Add `studies/followups/DESIGN.md` to
both the dirty-source rejection and start/end hash snapshot for every affected
command. Verify rejection of an uncommitted global contract and a mid-run change,
including deletion. Preserve its exact hash in run evidence. The design already
requires this; existing code does not yet implement it.

**D2 — original evidence and output transaction.** Freeze a path/hash ledger of
the 49 baseline files before execution, compare every member afterward, and
reject omissions as well as changes. `finish_run` replaces the entire study
directory; each command must write its complete original and follow-up set to
the staged output before promotion. New comparisons must use separate named
files rather than adding rows/keys to original prediction/metric files. Keep
original functions' random-number consumption and file ordering stable. Do not
refresh a baseline hash to excuse changed originals. Enumerate presentation
changes separately and retain the original provenance in Git history.

**D3 — ECG assignment and support audit.** Materialize all three seeded maps
from the same sorted 43 person IDs, retain each map, and check each person has
exactly one held-out fold per repeat. Verify the 201/202 shared-person case,
training/test disjointness, unchanged cap and model seeds, and exactly one
prediction per beat/model/repeat. Retain training membership and fold/class
test and training support, including zero support and undefined precision or
recall. The design is adequate; these checks remain pre-run acceptance criteria.

**D4 — origin and simulation invariants.** Check exact complete finite retail
windows and unchanged training scales; CO2 requires calibration-only quantiles
for each new model/horizon. Match original spectral realizations by condition
and replicate; restrict FFT bins inclusively without mutating their spectrum.
Keep the original 2,403-point LS grid independent of new truth values. Assert
the declared loop orders, cell counts and shared input realization across methods.
For detection reuse original thresholds without consuming calibration RNG again
inside new cells; retain separate magnitude-zero false-alarm denominators and
changed-stream eligibility, misses and early alarms. Numerical reconstruction
of added metrics remains a later checkpoint.

**D5 — bounded execution evidence.** Apply numerical thread limits before
NumPy/scikit-learn import, retain effective limits and exact command/source
revision in execution evidence, and run the nine commands sequentially in the
managed session. `n_jobs=1` alone does not limit BLAS/OpenMP. A timing trial may
estimate resources but must not choose a seed, cap, frequency grid or cohort.

## Optional improvements and accepted limits

Optional: record per-repeat/per-grid-stage wall time to make future reproduction
cost clearer. This is not a condition for scientific scoring or publication.
Reusing existing revised CO2 data, nominal electricity clock, recorded retail
sales, oil disclosure, idealized river reporting, same-hour air-quality peers,
and annotated ECG locations retains existing scope limits. Added analysis does
not turn those inputs into real-time vintages, deployment evidence or clinical
validation. No new web/source-law review was needed or claimed here.

Status: design/source checkpoint accepted; D1–D5 are implementation gates pending
evidence, not verified remedies. Return for non-authoring implementation review
before full runs, and results/publication review after artifacts exist.
