# Optional follow-ups: pre-run implementation/data review

Date: 2026-11-10. Non-authoring automated data/implementation review.
Reviewed committed source `c2d318a58789fcad91356b2973d019e3e455bcac`, followed
by the narrowly scoped CLI thread-limit repair described below. No full fits,
new full simulation grids, source edits or analysis-output writes were performed.
Bounded probes used read-only inputs or temporary directories.

## Verdict and scope

The analysis implementation satisfies D1–D4 from [design review](design-data.md)
at the pre-run checkpoint. D5 exposed one actual CLI resource-control defect;
the author's repair is independently verified in the working tree. Commit that
repair and its test before full runs, and retain launch-time thread caps and
effective-library evidence. No remaining source/target/leakage/scoring blocker
was identified. Full artifact preservation, completed-repeat support and output
metric reconstruction remain results-stage checks, not claims verified here.

## Checked evidence and gate disposition

**D1 — verified.** `common.source_snapshot` and `start_run` include the shared
follow-up contract. Independent temporary-repository probes confirmed dirty edit,
dirty deletion, mid-run edit and mid-run deletion all fail before publication.
The shared contract hash is included in the run's `source_files` mapping.

**D2 — implemented; baseline verified, post-run check pending.** Independently
matched all 49 ledger numerical paths and their hashes to both the baseline Git
blobs and current disk bytes. The preservation checker derives its fixed scope
from `1a0ec0180b857f7d98b092a8104a575657d53445`, asserts 49, fails on changed or
missing originals, and enumerates additions/presentation differences. Every
integration calls its follow-up before REPORT.md and `finish_run`; the original
numeric-writing blocks are unchanged. All helper writes use `followup-*` names.
The complete staging directory is promoted and hashed only after those calls.
Do not mark preservation verified until the final regenerated outputs pass.

**D3 — verified for mappings/input isolation; fits remain pending.** Independent
read-only checks on the actual 100,662-beat snapshot reconstructed all three maps
from sorted person IDs and each seed. Every repeat covers every beat exactly once,
with test-person counts 9/9/9/8/8; every training person has at most 1,000 beats,
training/test people are disjoint, and records 201/202 remain together. Fitting
functions and model seeds are unchanged. Validation compares beat identity,
truth, record, person and held-out fold for all four methods. Code retains all
repeat maps, membership, model audits, pooled/fold/class scores and support;
failed folds keep attempt evidence and cannot acquire a partial pooled score.
Patient bootstrap uses common whole-person multiplicity counts across methods.

**D4 — verified with bounded probes and source inspection.** On saved CO2 rows,
changing every test truth by one million changed neither anchored predictions
nor the six calibration offsets, and caller rows remained unchanged. All last
calibration targets precede the first test origin. A hand-constructed retail
series matched an independent 52-by-7 weekly median; changing future and older
out-of-window values had no effect and deleting one required day failed. New
retail rows inherit original targets/scales; all 24 exclusions retain six models.
The separate hand-calculated Croston/TSB recurrence assertions are meaningful.

One realization per original sampling schedule reproduced the original generator
exactly at its original signal settings. The fixed LS grid has 2,403 entries and
neither new off-grid truth is inserted. A native-bin toy verified inclusive
0.01/0.45 band selection. The detection generator preserved the first 200 values
and added exactly the declared post-200 shift. A four-alarm toy partitioned early,
postchange, absent and eligible counts as 1/2/1/3 with overall rate 1/2 and
conditional rate 2/3. Source loops implement the declared seeds/order/budgets and
paired inputs; original RNG/calibration code is unchanged.

Context helpers retain all customer rows, same-model-support load-share ratios,
per-customer peak counts, complete per-market annual count-weighted oil tables,
and once-per-duration air-quality truth censoring counts. Original numerical
artifacts are not extended in place. These new summaries require independent
post-run reconstruction; reading their source is not that reconstruction.

**D5 — defect identified, repaired and independently verified locally.** At
`c2d318a`, `cli.main` entered `threadpool_limits(1)` before importing ECG. A fresh
process replacing only `ecg.run` with an inspection callback saw **libomp=10**
inside the actual CLI call, without fitting anything. The author moved all
requested study imports before the thread-limit context. A second fresh-process
probe through actual `cli.main(all)` visited all nine callbacks sequentially and
observed **libomp=1** at every call. The new regression test probes `ecg` and
`all` in subprocesses without inherited common thread caps. This repair must be
committed before full runs. NumPy reports Apple Accelerate BLAS/LAPACK, which is
not enumerated by this threadpool probe: preserve `VECLIB_MAXIMUM_THREADS=1`
at launch and record environment caps separately from observed OpenMP counts.

The author's retained suite evidence at `c2d318a` records 69 passed in 3.03 s,
with stable source and 221 warnings. I inspected that evidence and the relevant
tests; I did not rerun the entire suite. The CLI repair needs its own recorded
checks, which the author was running during this review.

## Exact reviewed hashes

- Shared contract: `e0b36080e9bdd4e61f51b76656e7eff77a46a0c01dd11010eadf68f7434de7bc`
- Fixed original-output ledger: `9644e6e9698d21d27d1d824878a11e71f55eb7746c9e16c88cdad12c9451a686`
- Repaired cli.py: `291c732ecf570d97a7799c1a27332bf91f3d537b85e520903580a43428d8a9e2`
- New CLI test: `fecf81268ab95fc2617acae0b77bae19164aaa89ef072e384265dfd65d33eeec`

All other reviewed analysis source is identified by the full commit above.
No scientific-validation or results/publication approval is implied.

## D5 final amendment — pre-import environment caps

2026-11-10: The author additionally sets VECLIB/OMP/OPENBLAS/MKL/BLIS thread
environment caps to `1` before `.data` imports NumPy. This closes the manual
environment requirement for the documented `atlas` CLI entry point. I reviewed
the diff and independently probed both `ecg` and `all` in fresh subprocesses
with all five inherited caps removed. An import finder observed all five values
already equal to `1` at NumPy's first import. After deliberately setting OMP to
`4` before importing real study modules, the actual CLI's 1 and 9 no-fit callbacks
each observed OpenMP at `1`; the context restored `4` after work ended, as
expected. No models or full simulations ran. Accelerate's environment setting
was verified; its internal thread count is still not directly measured here.
Final repair is independently verified; commit these bytes before execution:

- cli.py: `26ea30e8eb59282d12be90417c68b7bb7447a5ca26822a61498db922053b6826`
- test_cli_threads.py: `bc5670d84feef2af8416f309ff489ddbdb1b240a2f334b32a97c5f9da0cc82a6`

These supersede the preceding repaired-CLI/test hashes without erasing the
initial defect and repair history. Explicit execution-runner launch caps remain
useful redundant evidence, not an additional user action required by the CLI.
