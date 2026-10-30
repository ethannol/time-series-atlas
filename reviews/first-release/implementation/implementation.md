# Pre-run implementation review: data and reproducibility perspective

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: `src/tsatlas/*.py`, offline tests, check recorder, frozen designs,
intake manifest/audit, and the bounded development-trial artifact. The reviewer
did not author the implementation and made no implementation edits. Source HEAD
was `b374e9baa39f021481aefaefba958543534c916f`; reviewed model additions and fixes
were still uncommitted and are identified by hashes below.

**Gate verdict: ready to commit the reviewed source and proceed to full runs.**
No unresolved material implementation blocker was found within this review's
scope after the corrections below. The existing dirty-source guard correctly
prevents full runs until that commit. This is not a results, interpretation, or
publication review; no held-out scores were computed by this reviewer.

## Findings and corrections during review

### II01 — Capture the executed source, not only the source after execution

Priority: high for reliable run evidence. Initial state: `identified`.

The initial recorder collected source hashes only after execution and used a Git
diff hash that would omit untracked model files. A source change during execution
could therefore be misrepresented by the resulting run record.

**Correction verified:** `start_run` rejects changed or untracked source, tests,
scripts, design, lock/configuration, and intake manifests; records the starting
revision, protocol commit, hashes, input snapshots, and UTC time; and
`finish_run` compares freshly enumerated source hashes and revalidates pinned
inputs before promotion. The test recorder also re-enumerates and compares
source/test/script/configuration hashes around its execution. Actual checks
include untracked additions at this review stage, and their hashes match the
reviewed files. Status: `verified` at code-inspection and bounded-guard-test scope.

### II02 — Avoid mixed old evidence and partial new results

Priority: high for truthful publication artifacts. Initial state: `identified`.

The initial implementation wrote directly into an existing result directory,
which could leave an earlier successful run record beside partial rerun output.

**Correction verified by code inspection:** each run now writes to a unique
staging directory, creates its evidence there after final checks, and promotes
the whole directory. Replacement uses a backup with restoration if promotion
raises an exception. Model failures before promotion leave the prior published
directory intact. The reviewer exercised the source-mutation refusal before
writing/promotion; it did not inject filesystem failures or claim crash-durable
atomicity across the directory-renaming sequence. Status: `verified` within
that stated scope.

### II03 — Distinguish period labels and process-level resource measurements

Priority: medium for evidence interpretation. Initial state: `identified`.

The initial CO₂ record called a December 1 month label `origin`, despite using
the complete December monthly average. The initial resource field also did not
identify that `ru_maxrss` is a process-lifetime maximum.

**Correction verified by code inspection:** output now names the field
`origin_month`, and run configuration states that issuance is assumed after the
December observation is available. The memory field is
`process_lifetime_peak_rss_bytes`, with platform unit conversion, and UTC start
and completion timestamps are recorded. These names do not claim a historical
release-date reconstruction or per-study isolated peak measurement. Status:
`verified` at code-inspection scope.

## Bounded independent checks executed

No full evaluation function was called. The reviewer used the installed Python
environment for these read-only or mocked checks:

- Recomputed the two committed snapshot hashes and matched the intake audit.
- Parsed the pinned CO₂ snapshot and confirmed only December 1975 and April 1984
  receive the NOAA quality-suspect flag.
- Traced the pinned `MT_187` features for January 15, 2013: previous-day mean
  equals January 14's mean; same-hour lags 24, 168, and 336 match January 14,
  January 8, and January 1 respectively. These are all known by the stated
  midnight origin. No final-evaluation error was calculated.
- Checked the calendar masks: both 2013 and 2014 contain 8,760 nominal hours,
  with 8,040 primary-safe hours and 720 excluded hours. This was an index-only
  check and did not inspect 2014 forecast outcomes.
- On a deterministic toy stream, independently computed the declared CUSUM
  recurrence and matched its returned scores; checked strict threshold crossing.
  No calibration/evaluation simulation suite was run.
- Called `start_run('co2')` while model source was uncommitted and confirmed it
  refused before creating a staging directory.
- Mocked a changed source-hash set in `finish_run` and confirmed it refused
  before writing or promoting output.

All these checks passed. Their processes completed; no background jobs remain.

## Reviewed test and development evidence

The first captured test artifact inspected during review contained 12 passing
tests and one failed future-cohort fixture: the fixture attempted to mutate a
read-only `numpy.broadcast_to` view. The author changed the fixture to a writable
copy. This was a test-construction failure, not measured evidence of cohort
leakage.

The latest inspected `checks.json` reports **16 passed**, exit code zero, and
`source_stable_during_checks: true`. The reviewer independently compared every
listed source hash with the current file and found no mismatch. The test set
includes training/future perturbations, interval semantics, quality flags,
declared scoring behavior, and invalid/misaligned score input rejection added
following the statistical review. There are 11 deprecation warnings from the
pinned NumPy/pandas combination; they do not invalidate the recorded test result.

The development-trial artifact describes two customers in January 2013, with
1,488 hourly customer rows and finite predictions. Its recorded training
endpoints precede January 2013. That artifact is a bounded trial, not a full
24-customer result or validation of final-evaluation performance. The reviewer
did not rerun that fit or use its predictions to choose methods.

## Implementation assessment and remaining review boundaries

Inspection found the declared feature availability and monthly training cutoff
implemented consistently: calendar-day means are shifted by a day; same-hour
lags are historical; training targets precede the monthly cutoff; scaling uses
the training mask; learned predictions retain raw values and common zero clipping.
The pooled Ridge fit uses the declared mean-loss penalty scaling. Scores reject
nonfinite or incomplete matched customer panels and aggregate customers before
taking absolute errors. These checks support running the frozen benchmark, not
an assertion that a particular model will perform well.

The actual pinned snapshots already passed independent source-index review.
This review does not claim the adapters are a general ingestion system for
arbitrary malformed future source releases. New bytes or changed time semantics
require new intake review. Final result counts, figures, interpretations, fresh-
checkout reproduction, and publication claims remain separate checkpoints.

## Inspected SHA-256 hashes

```text
89f11ba0aa45c18d94a0ca870de8484452e2fa55cfcacbadf6a9f70a34c54ca9  src/tsatlas/__init__.py
2fed5022d7d69fb0878b3b932620883f98aab1edf581d91b4f20979ffeb34cd3  src/tsatlas/cli.py
07ca58309b36a5dc578667397750e0721b7358f3a5e1a2bee7fa9b4c8c2b27a8  src/tsatlas/co2.py
1bdc4e6ce523986d004678f7ed876fae57a258f6ae9eebdace225e5aa6ea3c3a  src/tsatlas/common.py
20c2b1b2b1be74dade626c8b54d18f3db5691ec3e82b94416fa4bd73d65a1fd5  src/tsatlas/data.py
32f7680163364a48010193d6957915a797df709541401effed394704064ad320  src/tsatlas/electricity.py
f0029cfbcee9a19df28294b40e39627fda31d7d5f4e5fc4b52e7068083c24931  src/tsatlas/metrics.py
717177942041ff2cd6be3ef65edb4094f69b74de1199bffd933162c6ba5bc763  src/tsatlas/synthetic.py
bfdb1be484fbbda2939cebf152711041b89030e1ba56b415756a458890c4b71d  tests/test_forecasts.py
372ba374e5b26d9baefe1955a9568b6613cd68eb9c273c47f866f1077f147d08  tests/test_intake.py
e3c7a398b72e28aa1175eaa16e45702a73828205fbe402952320070c39fb88c5  tests/test_metrics.py
4ddebc8f09003170fc9902c9727e011b861d1776b19b8c627986d89f1b6f011c  scripts/check.py
d070a91da04b8fee7d4c37e20f8160e6444a649a9551d3a198da62a4d2cb3fb3  studies/co2/DESIGN.md
d7739838ec65fd59b196385deab8f5da94767bfd1ad29255bae8222758a8c5a5  studies/electricity/DESIGN.md
f3fae56511a80dbb5647915eff040ffd4cdd10e0184299dd7b39786302acc42d  studies/synthetic/DESIGN.md
6d7a297fe89d6a653e52beae413ac3f352396ae0759a60d1e9016fcdd6ba8fd8  data/manifest.json
2b44293c453ecd008e8c7cf76e87a3f38a592afdd14870cb54b408309b020198  reports/intake/audit.json
c3f3dc8097078a5c56d49fa2312e069da837bd17e9ca1c16a9bdd2dc783ebbd4  reports/verification/checks.json
e09146c71f15f97114ad8fc57c5607b941e509055078a11db8f5ba2c184a9dd4  reports/verification/development-trial.json
0de9017d9a999123fd7f57fdece2afc3a47ca3f2584847e89abdc453a88a0691  pyproject.toml
54c0cd902e55158735fba20145a5a4d60269ba31f020099e39aa378a0c4061ac  uv.lock
```
