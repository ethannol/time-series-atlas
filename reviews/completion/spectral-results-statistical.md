# Spectral results review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Run source/protocol: `2c0af60037ae691aae7e13c92cb37228215e5876`.
Scope: saved generated inputs, all replicate results, sample/spectrum evidence,
metrics, figures, report and story. This reviewer recomputed spectra using the
frozen settings, did not tune methods, and did not refit any other study's models.

**Results verdict: approved.** The saved inputs, estimates, ambiguity diagnostics
and summary arithmetic agree with independent recomputation. **Publication
verdict: pending SP-P01/SP-P02 below and the planned exact-reproduction gate.**
There is no requested change to the scientific design or numerical results.

## Independent checks completed

The reviewer replayed the declared random-draw order independently of the study
functions. All 83,278 saved timestamps and signal values match numerically,
including phases, Bernoulli retention, jitter and noise drawn at the actual
sampled times. Every one of the 300 input realizations has increasing timestamps
and the declared endpoint rule. The sample-count/span ledger matches the inputs.
Regular sampling has 480 observations over 479 seconds; thinning has 160 over
477 seconds. Irregular replicates have 167–217 observations, median 193 and mean
192.78, over 479 seconds.

The independent reconstruction reproduces the 2,403-point alias-expanded grid.
From saved inputs, it recomputes all 900 condition/replicate/method spectra and
selected peaks, absolute errors, recovery indicators and tie counts. It also
matches every saved truth/known-alias power and all 8,338 replicate-zero spectrum
rows. FFT mean removal, positive-bin selection, interpolation bounds, actual-time
Lomb–Scargle arguments and lowest-frequency tie rule follow the frozen contract.
Each method receives the same realization within its replicate.

All nine metric rows reproduce from the per-replicate outcomes, each with exactly
100 replicates. Median error, recovered counts/fractions and the number of
replicates with tied maxima agree. Every output hash listed in `run.json` matches.
This verifies the retained evidence and numerical implementation; the separate
whole-command reproduction gate is still outstanding at this review point.

## Results and the alias question

| Sampling | Method | Recovered / 100 | Median absolute error, Hz | Replicates with tied maxima |
| --- | --- | ---: | ---: | ---: |
| Regular 1 second | Index FFT | 100 | 0.0008333 | 0 |
| Regular 1 second | Interpolated FFT | 100 | 0.0008333 | 0 |
| Regular 1 second | Lomb–Scargle | 100 | 0 | 0 |
| Irregular + jitter | Index FFT | 0 | 0.1067354 | 0 |
| Irregular + jitter | Interpolated FFT | 74 | 0.0008333 | 0 |
| Irregular + jitter | Lomb–Scargle | 100 | 0 | 0 |
| Regular 3 seconds | Index FFT | 0 | 0.3175000 | 0 |
| Regular 3 seconds | Interpolated FFT | 0 | 0.0068201 | 0 |
| Regular 3 seconds | Lomb–Scargle | 0 | 0.0066667 | 100 |

Recovery here means within 1/480 Hz of the declared 0.17-Hz signal. In the
irregular condition, using actual timestamps succeeds in all 100 replicates,
interpolation succeeds in 74, and pretending retained indices are seconds
succeeds in none. Lomb–Scargle's maximum irregular-condition absolute error is
approximately 0.0001667 Hz; a zero median error does not mean every estimate is
exact. These are finite simulation outcomes under one declared signal/noise/grid,
not universal success probabilities or evidence about ECG physiology.

The anticipated alias diagnostic survives the actual evaluation: **all 100
three-second Lomb–Scargle spectra have exactly two tied maximum candidates**.
The greatest absolute power difference between the selected peak and its
equivalent alias is approximately 4.7e-11. The greatest difference between the
specifically recorded true-frequency and known-alias powers is about 7.4e-11.
Both are below the frozen 1e-10 tolerance, closing the pre-run numerical question
for these realized inputs. The regular and irregular Lomb–Scargle maxima are
unique under that same rule.

The zero recovery count after three-second thinning follows the frozen convention
of choosing the lower alias, near 0.1633333 Hz. It does not demonstrate that one
physical frequency was identifiable but the estimator failed to select it.
The sampled sine/cosine spans are equivalent, even with the same added noise.
A different deterministic tie-break could change the scored selection without
adding any identifying information. The explicit ambiguity evidence is the
substantive result in that condition.

Both figures were visually inspected against the numerical evidence. Replicate
zero was fixed in advance, including its unfavorable interpolation example in
the irregular case. The report states that spectral heights are divided by each
method's own maximum, so visual heights must not be compared as common power.
Sampling conditions differ in sample count as well as timing, and the comparison
does not isolate a causal effect of irregularity alone.

## SP-P01 — Add the empirical answer and completed story milestone

Type: publication omission. Priority: close before publication. The report
currently explains the experiment and ambiguity but leaves its direct answer
in tables. Add a short finding with the irregular 100/74/0 recovery counts,
followed by the 100/100 ambiguous thinned cases and the tie-break interpretation.
Keep the finite-simulation and non-physiological scope explicit. Do not describe
the aliased zero recovery count as evidence that timestamp-aware estimation
resolves the wrong physical frequency uniquely.

The story currently ends with results not yet interpreted. Preserve the earlier
grid-amendment chronology and append actual execution, findings and independent
review. The original omission of this promised control from the first release
should remain visible. No retuning or new model comparison is requested.

## SP-P02 — Name the method in the ambiguity panel

Type: figure labeling omission. Priority: close before publication. The right
panel of `recovery-and-ambiguity.png` uses only Lomb–Scargle tie counts, but its
title and y-axis do not name that method. Add that label so the panel cannot be
read as pooled ambiguity evidence for all three methods. The counts are correct;
this is a presentation correction, not a reason to alter spectra or outcomes.

Closure requires checking the regenerated narrative/story/figure and confirming
unchanged numerical inputs/results/metrics, plus the separate reproduction gate.

## Inspected SHA-256 identities

```text
45c1851a85db81157a0b3e40a3352ac15983602d1b394e60749ca59d385b7ef3  src/tsatlas/spectral.py (run source)
195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422  studies/spectral/DESIGN.md
7dd5b02bb7bc8afeaaf41bd0320c8d2b0b36170380bc85d9ba2e80b002ebff9f  reports/results/spectral/inputs.csv.gz
8067b80377a5af51487ac842f827c976dc66c1eb412fcc75bb433ca81db4b467  reports/results/spectral/replicates.csv.gz
3c1ab52d60ce41bb9920aa29c2a8fcf8bcff3a6b80b142bd2ac78b152250d244  reports/results/spectral/metrics.json
c7d006cfa5b4de98c37643b5e0ca190a6260d7c0ba5ce0b17ab633c9e2ec4615  reports/results/spectral/example-spectra.csv.gz
58e32d541f4c26b72c40b69ce2a8977cf1af8824eb97c82beb83c14770a41fee  reports/results/spectral/sampling.csv
37036241d69b51e948e0ce74559dc2f3083cdb8085f2b2d897325b3461c50d7a  reports/results/spectral/preselected-examples.png
b698992e81a41f5d613cc6c294a4fcd3b2dcb23fa170c843de8f784f7bd8c280  reports/results/spectral/recovery-and-ambiguity.png
ba4982ded6d607ee2624efb75b79eb807c001edbf71d8fbd37949ceb30662e96  reports/results/spectral/REPORT.md
42b2225ab875b7d5e88bbf66a3a7dbed2e9efa93072cb6e40b8c082e3aacc058  reports/results/spectral/run.json
93262c04377dccdbc39aa1d73a9f74349ce392c17a2a9ddff0c439396d72cba6  studies/spectral/STORY.md
```
