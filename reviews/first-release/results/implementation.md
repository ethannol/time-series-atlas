# Results and publication evidence review: implementation perspective

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: the three first-release run records, recorded source/input/output hashes,
README execution path, CI workflow, validation scripts, and archived evidence.
The reviewer did not refit the studies or alter the implementation. Statistical
interpretation and figure design are covered by the other independent reviewers.

**Initial artifact verdict:** the inspected results have matching source,
snapshot, and output evidence. **Initial publication verdict: pending** correction
of RI01 and review of fresh-checkout reproduction evidence. Reproduction in a
new checkout has not yet been established by this review.

## Artifact verification performed

The three run records identify source commit
`5953a7f6426bb44ddb2433153ce0c54038b6eb90` and protocol commit
`b374e9baa39f021481aefaefba958543534c916f`. Their source-stability fields are true,
their source-patch hashes identify an empty patch, and their UTC timestamps
sequence the runs consistently.

The reviewer independently recomputed all recorded hashes rather than relying
only on the repository validator:

- **57 source-file entries:** match current file bytes and the corresponding
  Git blobs at the recorded source commit, including frozen study designs,
  dependency lock, acquisition manifest, and intake audit.
- **14 output entries:** match the prediction/replicate files, metrics,
  parameters, figures, and reports named in the three run records.
- **6 snapshot entries:** the two fixed snapshots referenced by each study match
  the recorded hashes.

These are entry counts across records, not counts of independent datasets or
tests. No model was executed to perform these checks. Later report-only commits
need not have the same SHA as the execution commit; the retained source hashes
make that distinction inspectable.

The run records report about 0.81 seconds for CO₂, 10.20 seconds for electricity,
and 0.23 seconds for the synthetic study. The largest recorded process-lifetime
peak is 740,605,952 bytes. The shared-process synthetic peak is correctly labelled
as process-lifetime usage, not its isolated incremental memory cost. These are
the author's recorded execution measurements, not an independent timing run.

## RI01 — Missing result records can produce a false successful evidence check

Priority: medium; fix before treating CI as the three-study publication gate.
Status at initial inspection: `identified`.

`scripts/validate_evidence.py` only iterates discovered `*/run.json` files. An
empty collection therefore exits successfully and prints that all recorded hashes
match. A missing individual study is also not rejected. The reviewer reproduced
the empty case by mocking `Path.glob` to return no records; the script exited
with code zero and reported zero checked records. No files were removed or edited
for this probe.

Require the expected first-release study set, agreement between directory and
recorded study name, and nonempty required source/output/snapshot mappings.
The checks should continue to validate actual hashes. This is a validation-gate
defect; it does not invalidate the existing three records, which independently
passed all hash checks above.

## RI02 — Fresh-checkout reproduction remains unverified

Priority: high before claiming fresh-checkout reproduction. Status at initial
inspection: `identified`, pending the primary agent's planned execution.

The README provides a coherent offline path: locked Python/dependency setup,
snapshot verification, bounded tests, full execution from committed source,
and artifact validation. Committed snapshots remove dependence on live NOAA/UCI
downloads during study execution. Dependency installation can still need network
access; “offline” here describes data and analysis execution after setup.

To close this finding, retain the new checkout's commit, setup and execution
commands, exit statuses, source/input hashes, and comparisons of regenerated
metrics/predictions against the committed reference outputs. Validating newly
generated outputs solely against their newly generated hashes demonstrates
self-consistency, not reproduction of the reference result. If numerical
tolerances are needed across environments, state them before comparing and report
the actual differences. Runtime/timestamp fields need not match.

## CI and command assessment

The inspected workflow pins its checkout/setup actions, requests read-only
repository permissions, sets a ten-minute timeout and thread limits, installs
locked dependencies, verifies snapshots, runs bounded tests, and validates
documentation and recorded evidence. It does not refit the full studies on every
push or require provider downloads. This is appropriate once RI01 is corrected.
Workflow execution and green checks on the final published revision remain the
primary agent's responsibility; reading the YAML is not proof that CI passed.

`atlas fetch` intentionally rejects upstream revisions and `atlas intake` requires
the pinned archive. Their failure when historical source bytes are no longer
available is documented rather than silently replacing the baseline. Ordinary
study reproduction uses the committed derived electricity panel and retained CO₂
snapshot instead.

## RI03 — Mark superseded checkpoint prose as historical

Priority: low, presentation-only. Status at initial inspection: `identified`.

The first-release review index still has an undated “Implementation and results”
paragraph saying the work is pending, followed later by a completed implementation
gate. Label the former as an initial historical status, or update the current
status while retaining the dated history. This avoids making a reader reconcile
apparently contradictory checkpoint states. It does not affect computed results.

## Initial inspected SHA-256 hashes

```text
98d97913845ab4c0fe14197575e04891efc93c98ae50eb05faf47cd2d5e09340  README.md
0f367acfd23e7b9febfec837cb77f24876e906d72c3ba1bb52401364b68cc078  .github/workflows/checks.yml
1270ddf6a7896224627afb78447e33528032abfb2c53b096d038027e4502dd9f  scripts/validate_docs.py
bc10ccbb5bb0e031f3964c216752b427518327f4cd6444760dcdd0a5ae12b756  scripts/validate_evidence.py
25a2f9bf21be6dc1621656b0e9ee327dc3b1f6565953fe132c895ff061472c98  reports/results/co2/run.json
b8031cce8180102e2b5250c540b800872cb93c03157f989c74baec004ffbb327  reports/results/electricity/run.json
5e881497079185936e8e3df6a51e3e7d0d8bd3d778d727dc1d479158ba9878df  reports/results/synthetic/run.json
a3476893e812fbf233d767fbcbed23ad12f77a90450816a7c21877f9b5da8aa5  reports/verification/checks.json
```

Any later resolution verification must be appended with its own scope and hashes;
the initial observations above must not be silently rewritten as resolved.

## 2026-10-30 — Validator correction and original-run reproduction verified

Reviewer: `/root/implementation_critic`. This addendum preserves the initial
review above and distinguishes the original executed artifacts from the pending
updated report rendering.

**RI01: verified.** The updated validator requires exactly the first-release
study set, checks the study name against its directory, requires nonempty
source/output/snapshot mappings, and continues to verify their bytes and source
stability flag. The reviewer independently ran only `tests/test_evidence.py`:
two tests passed. They exercise missing records, empty evidence maps, and a
mismatched study name. No full studies were executed by the reviewer.

**RI02: verified for the original published-result candidate.** The primary agent
ran the studies in the temporary checkout at
`/tmp/time-series-atlas-reproduce-20261030`, commit
`4a3022c2486586eabbf9588c57e33457bca0ad99`. The reviewer independently inspected
that checkout and confirmed:

- Imported `tsatlas` resolves inside that checkout, not the main working tree.
- No `data/raw` directory is present; the studies use the committed snapshots.
- The three new run records identify that checkout commit and new execution
  timestamps, with their recorded source and snapshot hashes matching its files.
- All **14** regenerated output files match the output hashes in the original
  committed run records read directly from Git at that checkout commit. The
  regenerated run records also contain those same output hashes. No numerical
  tolerance was needed: comparison was exact SHA-256 equality, including metrics,
  saved predictions/replicates, parameters, reports, and figures.

This is independent inspection and recomparison of the primary agent's recorded
fresh-checkout execution, not a second reviewer-executed fit. Execution metadata
is expected to differ and was excluded from equality. The comparison record is
`reports/verification/reproduction-initial.json` at the hash below.

**RI03: verified.** The earlier pending paragraph now has the heading “Initial
implementation/results status, before the gates below,” and its prose explicitly
states that it describes the earlier stage.

### Gate decision for refreshed report output

The inspected diffs in the three study modules change report text, labels, the
electricity comparison plot, and an additional customer comparison output. They
do not change model fitting, feature construction, splits, thresholds, or primary
score computation. **Proceed with committing the reviewed changes and rerunning
the unchanged computations to generate evidence for the revised source.**

Final publication verification remains pending the refreshed run records and
fresh-checkout comparison of the updated rendering. The verified original
reproduction should remain archived; it is not silently relabelled as proof for
files that did not yet exist in that checkout.

```text
d8f74e00e04c2c986956f1cbc538dfb431194ccb9002b20ad6366718c553b47f  scripts/validate_evidence.py
51e6d8e1921f0b9908cbcde151a28ff8bb8a2bef3ac4f197c786d46d5653c018  tests/test_evidence.py
0d0d565c460203fe43f0f69ad77ce295065b622c215affd408219562339901d7  reports/verification/reproduction-initial.json
6a652546f1a67f658e99cfc5808c341505b83a3f04bdac1082468c99cec98c0a  src/tsatlas/co2.py
bff038460bc7cba8996c999b22a327101d9252ed123be5054071af3946a5b43f  src/tsatlas/electricity.py
7974c9d74ab57f4db295e8b6008b28acf675cc91b4e2d85fe39ea5caa61ac8fc  src/tsatlas/synthetic.py
29bddbfb2fc08c39c390b99edea3677014cc843c96c7238460f1f955e988a45a  reviews/first-release/README.md
```

## 2026-10-30 — Refreshed artifacts and final clean-checkout reproduction

Reviewer: `/root/implementation_critic`. The review covers updated execution
source `b607f9f410dec080388b84163f6ca073c6630607`, result commit
`d20c0ccf2d458986ad99afbd7b01569b6cd86fbd`, final reproduction evidence, and the
proposed portfolio/profile integration. The reviewer did not execute any model
fits or rebuild the portfolio.

**Updated artifact verdict: pass. RI02: verified for the final rendered results.**
The repository evidence validator passes. Independently recomputed hashes match
all **60 source entries**, **15 output entries**, and **6 snapshot entries**
across the three records; source entries also match Git blobs at their recorded
execution revision. These are counts of entries across records. The retained
test artifact reports **18 passed**, exit status zero; its source-file hashes
match the inspected files.

The primary agent executed the documented setup and study commands in
`/tmp/time-series-atlas-reproduce-final-20261030` at result commit `d20c0cc`.
The reviewer independently confirmed the imported package resolves inside that
checkout and that it contains no `data/raw` directory. Its new run records name
that checkout revision, carry new UTC execution times, and have matching source
and snapshot hashes. All **15 regenerated output files** match the reference
hashes read directly from the committed run records at `d20c0cc`. Comparison
uses exact SHA-256 equality, with no numerical tolerance; execution metadata is
excluded because revision, timestamps, and runtime measurements necessarily
change. This verifies the primary agent's recorded fresh-checkout execution by
independent inspection and recomparison, not a separate reviewer-executed fit.

The recorded command uses locked Python 3.12 dependencies and bounds BLAS/OpenMP
threads. Offline reproduction refers to analysis from committed snapshots after
dependency setup. Live provider files are unnecessary for that path. The final
comparison JSON and execution log are retained at the hashes below.

### Integration and CI assessment

The atlas `portfolio.json` resolves headline values from retained metrics,
distinguishes completed and planned studies, links the process/review record,
and does not claim a representative panel, causal effects, clinical benefit, or
independent human validation. The profile addition makes the same scope clear.
The portfolio manifest adds the atlas as a required sibling project, and the
Pages workflow checks out `ethannol/time-series-atlas` at `main` into the matching
directory before its strict build. **Land the atlas first-release files on main
before deploying the dependent portfolio change.**

The atlas CI workflow and README commands remain coherent. CI installs locked
dependencies, verifies the snapshots, runs bounded tests, and validates docs and
evidence without provider downloads or full fits. The inspected GitHub workflow
list was empty at this checkpoint: neither this YAML review nor local success
establishes green GitHub checks. The primary agent must follow checks on the
actual published revisions through completion.

### RI04 — Rebuild the portfolio against a results-containing revision

Priority: medium before deploying the portfolio. Status at this inspection:
`identified`.

The generated local portfolio HTML and `site/numbers.json` still identify source
revision `b607f9f`. The page embeds updated report prose but pins its links to
that earlier source commit. In particular, its customer-comparison download
targets `reports/results/electricity/customer-comparison.csv.gz` at `b607f9f`;
Git confirms that path is absent there and present at `d20c0cc`. Run-evidence
links also resolve to the earlier records. The builder correctly selects the
project's Git HEAD, so this is a stale build artifact, not evidence of a model
or builder defect. Rebuild after committing results, then verify the generated
source revision and result-link destinations. No analysis rerun is required.

**Publication checkpoint:** atlas results and reproduction are ready from the
implementation perspective. Portfolio deployment remains pending RI04; final
published CI and deployment status remain operational follow-through rather than
claims established by this local review.

### Final artifact and integration hashes inspected

Sibling paths below identify the primary agent's isolated integration worktrees;
they are not paths packaged inside this repository.

```text
ab27a5138fb5e9e969019f69a775f1de2b62e9b6cef19f24b0219cf83a2bb9f3  README.md
5ac08ff58dd4bc552693ecd50ad8d11226995fbf6c0a7f9d295fd9f6035635a3  portfolio.json
0f367acfd23e7b9febfec837cb77f24876e906d72c3ba1bb52401364b68cc078  .github/workflows/checks.yml
d8f74e00e04c2c986956f1cbc538dfb431194ccb9002b20ad6366718c553b47f  scripts/validate_evidence.py
1270ddf6a7896224627afb78447e33528032abfb2c53b096d038027e4502dd9f  scripts/validate_docs.py
c51c73977e13304a8106e37f5afd419ebf40bf940561e9e6cce47d2f72d63826  reports/results/co2/run.json
43a55431f786690ecd605ea71cd4d42e7a4aff821a38168b56672853405f0204  reports/results/electricity/run.json
c77320ad4f5cd842afce8991f2802a85a95fc981b6dcf0b015df4fc2594657b1  reports/results/synthetic/run.json
cc0bf4e8732ebe2bfc16f48ab0b75e7b2d475d02d0ee5db4de3f963dd9ede91c  reports/verification/reproduction-final.json
8175a2732419c0496a53e8f1ad04c171c807e2071174116a742b1051c71b5150  reports/verification/reproduction-final.log
344824debbefa56fabb688d3afc6338ac02daffe27c6dad88fac8b0b2a3e77c9  reports/verification/checks.json
78ea206f789989dd6dded86a0534f46416eaac992d16b7bf8052648f3f64f6d8  ../portfolio-tsatlas-20261030/manifest.json
244012b3f3bba5fd5ae7fce6d0fa5c8160a35a62076e605f43dfb89129a2629c  ../portfolio-tsatlas-20261030/.github/workflows/pages.yml
d9578ca794e903c3a74553446c18450f0c7930a8fe3e34653f7144f3cd934b3b  ../github-profile-tsatlas-20261030/README.md
```

## 2026-10-30 — Portfolio rebuild verified; local publication gate passed

**RI04: verified.** After the primary agent rebuilt the portfolio, the reviewer
checked all **33 unique revision-pinned atlas file links** in its generated
project page. All name `d20c0ccf2d458986ad99afbd7b01569b6cd86fbd`, and Git confirms
that every target exists at that revision, including the customer comparison
download and all three run records. This is a local revision/target check, not
an assertion that unpushed Git objects are already reachable on GitHub.

The supplemental raw-intake reproduction record reports matching before/after
hashes for the intake audit and both snapshots. The reviewer confirmed all three
recorded hashes match the files currently on disk. The primary agent performed
that regeneration; the reviewer did not rerun the full raw adapter.

**Final local publication verdict: pass from the implementation perspective.**
The three results have matching provenance, verified exact-byte reproduction
from a clean checkout, coherent execution/CI commands, and working local
portfolio/profile integration. Rebuild the portfolio again after the final
review-metadata commit so the published page includes the completed review, and
follow the actual atlas and portfolio GitHub checks/deployment to completion.
Those publication operations are outside this review's observed evidence.

```text
1dde5097d3b9ff18275e4f154574128e9282e7e4267df8484ab1b09804fd94b1  ../portfolio-tsatlas-20261030/site/projects/time-series-atlas.html
1e9ecb2855e3d192f45a74120a94e1f06c61303cfd0c003c14c7a8a5d2333936  ../portfolio-tsatlas-20261030/site/numbers.json
567e31671774f6369d1fe2d0d3b954b17771adf0cb3cfea8fed0c7a72717dddb  reports/verification/raw-intake-reproduction.json
```
