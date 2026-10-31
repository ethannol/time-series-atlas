# Fresh critique: synthetic detection and spectral sampling

Reviewer: dedicated non-authoring Codex agent, 2026-10-30 PDT (2026-10-31 UTC).
This is automated critique, not independent human validation. Source/contracts
were inspected and numerical checks completed before consulting older verdicts.

## Baseline and scope

- Published baseline: `71999b34ccfd7127840b173efb287ac0a66b2a26`.
- Parent fetch record: `baseline.json`, `2026-10-30T23:19:56.565503+00:00`;
  parent reports a further fetch around 00:03 UTC October 31 with main unchanged.
- Reviewed both controls as one investigation. All 21 checked implementation,
  contract, test, run-manifest and output files equal the baseline bytes. Parent's
  unrelated study edits were excluded. No instrumentation or source patch.
- Independently recomputed saved-score arithmetic, performed bounded no-fit
  invariants, checked input/ledger consistency, and viewed all three PNGs.
  No full simulation rerun, model fitting, browser, server, or subagents.

## Separate verdicts

| Control | Implementation | Findings | Presentation |
| --- | --- | --- | --- |
| Change detection | Pass within checked scope | Supported for the declared simulation | Pass; conditional denominators remain visible |
| Spectral sampling | Pass within checked scope | Supported for the fixed methods and grids | Pass with two minor reporting improvements below |

No new result-invalidating defect, leakage, scoring error, or run blocker was
identified. The spectral qualifications do not require changing the frozen
methods, replacing saved scores, or rerunning the experiment.

## Change detection: evidence and interpretation

`src/tsatlas/synthetic.py:8–28` implements stationary AR(1) initialization,
unit marginal noise variance, an additive shift at index 200, baseline-only
standardization, a one-sided CUSUM, and strict first threshold crossing.
Separate calibration/evaluation seeds and frozen IID thresholds appear at
`src/tsatlas/synthetic.py:48–58`, matching `studies/synthetic/DESIGN.md:6–18`.
The baseline is re-estimated per stream; the alarm threshold is not.

All 1,600 saved rows have unique method/condition/replicate keys, 200 rows per
cell, and either an integer alarm index 100–399 or no alarm. Independent
aggregation reproduced every stored count, rate and conditional median:

| Method / noise | No-change alerts / 200 | Early / eligible / detected / missed | Median detected delay |
| --- | --- | --- | --- |
| Shewhart / IID | 4 | 4 / 196 / 79 / 117 | 65 |
| CUSUM / IID | 10 | 3 / 197 / 197 / 0 | 14 |
| Shewhart / AR(.6) | 20 | 3 / 197 / 97 / 100 | 65 |
| CUSUM / AR(.6) | 146 | 77 / 123 / 123 / 0 | 12 |

Each saved calibration list has 200 maxima. Its zero-based order statistic 190
exactly reproduces thresholds 3.8012186802788572 and 8.20600147986711; strict
crossing leaves 9/200 calibration exceedances for each method. Thus “5% target”
is correctly a calibration target, not an assertion of exactly 5% in every set.
See `reports/results/synthetic/metrics.json:2–69` and
`src/tsatlas/synthetic.py:50–52`.

Bounded fixtures verified the AR recurrence against independent arithmetic,
the unchanged pre-200 segment and +1 shift thereafter, manual CUSUM recursion,
strict crossing, and invariance of earlier scores to a changed future suffix.
The code uses present/past data only after the frozen baseline.

The 73% false-alert result is supported. A 12-sample conditional median is not
evidence that AR noise improved useful detection: 77/200 changed streams had
already alerted; only 123/200 produced a first postchange alert. The report
explicitly explains this selection and no-restart rule
(`reports/results/synthetic/REPORT.md:9–16`). The PNG labels both the 300-point
false-alert horizon and conditional detection. It is legible and matches the
saved rates; an optional “123/200 overall” annotation could make standalone
reuse clearer, but the adjacent table already supplies the necessary counts.

Accepted limits: one shift size, one dependence parameter, one-sided monitoring,
200 evaluation streams per condition, finite calibration uncertainty, and
conditional delay. Dependence changes both baseline estimation and monitored
excursions; this is a combined stress test, not a decomposition of those causes.
The report makes no field-performance or universal-winner claim.

## Spectral sampling: evidence and interpretation

`src/tsatlas/spectral.py:22–50` preserves actual timestamps, draws noise at those
times, supplies the same realization to all methods, interpolates only within
observed endpoints, and deliberately gives the index FFT a false one-second
spacing outside the regular control. The fixed Lomb–Scargle grid, floating
mean, normalization, tie rule and recovery criterion agree with the contract
(`studies/spectral/DESIGN.md:25–43`; `src/tsatlas/spectral.py:54–68,84–91`).

All 83,278 saved input rows are finite with strictly increasing times within
each of 300 realizations. All sample counts/spans match `sampling.csv`: regular
480/479 seconds; thinned 160/477 seconds; irregular 167–217 observations, median
193, over 479 seconds. Endpoint and jitter bounds pass. All 900 outcome rows
have unique keys, 100 per condition/method. Errors, recovery indicators,
medians, fractions and ambiguous-replicate counts reproduce independently.
Regular recovery is 100/100 for every method; irregular recovery is 0/74/100
for index/interpolated/Lomb–Scargle; thinned recovery is 0/100 for all three.

The 2,403-point saved grid matches the implementation. Every in-range alias of
every candidate is represented within 6.67e-13 Hz, including aliases of added
candidates. All nine saved replicate-zero spectra reproduce their recorded
peak and tie count without re-fitting. All 100 thinned Lomb–Scargle outcomes
record two maximum candidates; saved truth/alias powers differ by at most
7.37e-11, below the 1e-10 tie tolerance. The lowest-frequency choice explains
zero recoveries without implying that the true candidate lacked support.

All-frequency power equality is approximate: the saved thinned example has
off-maximum alias differences up to 2.26e-10. This is an already documented
rounding limitation, not a new winning-peak defect; compare
`reviews/completion/spectral-implementation-statistical.md:47–57`. The analytic
sampling ambiguity survives any numerical tie result. No guarantee for every
possible signal or floating-point tolerance is established by this review.

Both spectral PNGs are readable and consistent with the saved examples/results.
The recovery plot names the fixed rule and Lomb–Scargle ambiguity; the example
plot states the index-FFT time assumption and normalizes each method separately.
The report explains zero FFT ties, grid-aligned zero error, nonidentifiability,
preselected replicate zero, and lack of a universal ranking
(`reports/results/spectral/REPORT.md:21–27`). Those are substantive safeguards.

## Minor findings and optional extensions

**SYN-01 — Underqualified disclosure, low severity, identified.** The headline
100-versus-74 comparison is factual, but the methods also search different
frequency ranges: Lomb–Scargle uses 0.01–0.45 Hz, whereas FFT retains all positive
native bins (`src/tsatlas/spectral.py:15–19,37–50`). Six of the 26 irregular
interpolation failures peak below 0.01 Hz (replicates 22, 24, 45, 56, 59, 69).
The report discusses bin alignment but omits this range difference
(`reports/results/spectral/REPORT.md:3–5,21`). Add a short qualification that the
result compares the complete fixed procedures, including unequal search ranges;
it does not isolate timestamp handling alone. These six peaks do **not** prove
that a common search range would recover six additional cases. That sensitivity
is untested and optional; do not silently change the original comparison.

**SYN-02 — Reporting omission, low severity, identified.** The frozen contract
asks to show sample-count/span distributions and paired alias powers
(`studies/spectral/DESIGN.md:47–49`). The report links the raw sampling ledger
but does not summarize those distributions or the paired-power diagnostic
(`reports/results/spectral/REPORT.md:27`). Add the count/span summary and maximum
truth/alias power difference above. Existing saved evidence is sufficient; this
is a reader-accessibility/contract-completeness repair, not missing computation.

Optional extensions are Monte Carlo intervals, additional shift/noise/frequency
conditions, and a common-band comparison. None is required to support the
current bounded claims. The single planted frequency, truth-containing grid,
finite replicates and numerical rather than statistical tie criterion remain
accepted limitations, not newly discovered defects.

## Reproducibility boundary and hashes

All 12 output SHA-256 entries in the two run manifests match current files.
Checks used the existing local `.venv` and sequential sub-second/small Python
commands. They did not regenerate every stream, spectrum, or plot, verify the
live site, or independently establish historical pre-run chronology. Prior
reproduction claims are not substituted for those unperformed checks.

| Artifact | SHA-256 |
| --- | --- |
| `src/tsatlas/synthetic.py` | `7974c9d74ab57f4db295e8b6008b28acf675cc91b4e2d85fe39ea5caa61ac8fc` |
| `src/tsatlas/spectral.py` | `2b3fb70dbced18fb24a8cc464da9883171ec4debe3c0524b128e3a005f72dbfc` |
| `studies/synthetic/DESIGN.md` | `f3fae56511a80dbb5647915eff040ffd4cdd10e0184299dd7b39786302acc42d` |
| `studies/spectral/DESIGN.md` | `195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422` |
| `reports/results/synthetic/run.json` | `c77320ad4f5cd842afce8991f2802a85a95fc981b6dcf0b015df4fc2594657b1` |
| `reports/results/spectral/run.json` | `e283b642992f63063ba6c5d8829e76d336880c479ed4229c0bd6b859ffc3dc13` |

The hashed manifests enumerate the metrics, replicate evidence and all PNG hashes.
Historical recorded run sources are `b607f9f410dec080388b84163f6ca073c6630607`
(detection) and `f14924eb7de588721a0d12021cb35521ec928a2f` (spectral);
the review baseline is the later published commit stated above.
