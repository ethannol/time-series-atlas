# Retail pre-run implementation and shared provenance review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: retail implementation/tests against the contract frozen at `b369cc8`,
study-scoped input checks, historical-source validation, CLI wiring, and the
acquisition/execution boundary. No full study or 2011 accuracy evaluation was
performed. The reviewer did not author implementation code.

**Pre-run verdict: pass for retail from the implementation perspective.**
Commit the reviewed source/configuration and run the frozen retail study after
the other required independent gate is satisfied. The existing clean-source
guard correctly prevents execution from the currently changing source tree.
This is not approval of the unfinished oil, river, air-quality, ECG, or spectral
model implementations, nor a claim that collection-wide evidence is complete.

## Retail behavior checked

The source snapshot and deterministic cohort were independently reconstructed
in the [source/design review](design-implementation.md). The forecasting code
uses only observations strictly before each origin. This includes January 1–2
before the first January 3 forecast. Seven-day targets end December 4; the
partial terminal week is excluded. All 24 products have the same 48 target
weeks, so the implementation's equally weighted product-week mean equals the
declared macro product mean. Training denominators use only 2010.

Croston's elapsed interval starts at the first positive observation, its size
and interval update only after positive sales, and its SBA adjustment is applied
to the daily rate before multiplying by seven. TSB's occurrence probability
updates on every subsequent day. Shared size updates are appropriate because
the design declares the same size smoothing coefficient. The always-zero,
last-week, and 28-day baselines use the specified past windows. The current
metrics save signed total error, both unit totals, and product/quarter summaries.
No rounding, model selection, or clipping changes the forecasts.

The reviewer ran the three targeted retail tests: **3 passed**. They cover
target/future perturbation, TSB decay versus unchanged Croston forecasts during
inactivity, all-zero histories, and rejection of invalid sales histories.
The run emitted 12 NumPy/pandas timedelta deprecation warnings; the locked
runtime executed correctly. These warnings are not model failures.

A separate hand-calculated recurrence probe used `[0, 0, 6, 0, 8]`: smoothed
size 6.2, interval 2.9, and probability 0.37 gave the expected SBA/TSB rates.
The reviewer also repeated the bounded development trial with the current
source hash below: two products (`90181B`, `85232b`), origin 2010-12-20, ten
prediction rows, all finite and nonnegative. No comparative accuracy statistic
was computed or inspected. The retail source hash was unchanged across this
probe. The author's earlier trial artifact names an earlier source hash; it is
not silently treated as execution evidence for the later signed-total/report
updates. The reviewer probe establishes the current bounded check separately.

## C-I01 — Historical provenance correction verified

Status: `verified` for the inspected implementation. The updated evidence
validator resolves every recorded source file at that run's `source_commit`
using Git, while checking retained outputs and available snapshots against
their current bytes. Missing historical revisions and source-hash mismatches
fail. It does not replace old hashes with new ones. CI fetches full history.

The reviewer independently ran the four evidence tests: **4 passed**. The fixture
shows that a changed current source file leaves valid historical evidence valid,
while a corrupt recorded historical hash or current output fails. The three
actual first-release records also validate with an explicit three-study scope
despite the new implementation files. This closes the original preservation
problem without refitting or rewriting their results.

The collection validator now requires the full declared set, including the
spectral companion to the synthetic work. Missing unfinished study records must
still fail its default final-release check; the scoped check above is not a
claim of final collection completion.

## Input and command boundaries

`start_run()` and `finish_run()` verify the named study's inputs with private
inputs required. Source/design/configuration must be committed before a full
run; source hashes are compared again before output promotion. New study
manifests/audits are recorded in addition to the retained first-release records.
The existing staged-output promotion and resource/time evidence remain intact.

Using an isolated temporary fixture, the reviewer confirmed that a missing
fetch-only input is reported as unavailable in permissive verification, fails
strict execution verification, and that a present corrupt input fails in both
modes. No actual source input was removed or altered for this test.

The first inspected CLI still lacked retail and printed an unqualified snapshot
success message. The updated CLI fixes both. A mocked-run dispatch check
confirmed `atlas retail` reaches the retail runner without executing it. A
mocked missing-input check confirmed `atlas verify` explicitly prints the absent
fetch-only input and says it was **NOT verified**, with its acquisition command.
No network access occurs in study execution.

The new acquisition module separates provider access from analysis. Its oil
path permits an updated workbook only when the normalized through-2025 input
matches the pinned hash; a mismatch prevents promotion. Original manifest
hashes remain recorded, and acquisition metadata distinguishes identical raw
bytes from identical normalized inputs. This code-path inspection and the
strict-input fixture do not substitute for the later actual oil acquisition/
reproduction check. River selective acquisition and ECG intake receive their
own source/implementation reviews.

## Inspected hashes

```text
d94819d04917c476abbd039a1f90ba46a6ff0ac633b09f1cd04cb636d2081c92  src/tsatlas/retail.py
bfe578cd417c166cba55ee069662773d4e135f5af55b8819a07de5006615751c  tests/test_retail.py
ccbbae99f581992fc1f9111d14d076fd316fa7db93e56dcad43fd21ae29df840  studies/retail/DESIGN.md
d71a5dcaf01e04e47a630cdeb9446e1e2b0dea608f3aabd75be37bee4aec7254  src/tsatlas/common.py
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
8ded82ddfaa1d7d1cfaae756419e614e991eb8b2bc699c59a746c8d23e3930dc  src/tsatlas/cli.py
b15b13e15064526b97e8615581521147800704caed6587ad933b85fe11517fe3  src/tsatlas/acquire.py
e931e6a747f57e53deb9aa16042f2d7f1432abb265919517bf2dfebbe5bebc18  scripts/validate_evidence.py
05f21be147e935c64eb7a0b98117c75faa766cd81830eec25b4ccdf28912c7de  tests/test_evidence.py
2ee611419ca1b2d16a55bcc12ef6eb54f75b5861a7e03b6cf056e517f5d28f2e  .github/workflows/checks.yml
2ed602cb2eaf80d275bd1c9706c5276cd142e8b0e7b6ce1e6b6f5d2a6f71f7bb  reports/verification/retail-development-trial.json
```
