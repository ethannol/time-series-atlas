# Spectral design amendment and pre-run implementation review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: the prospective alias-grid amendment, generator/method implementation,
bounded structural tests, provenance/output contracts and a separate-seed
finite-only development trial. The reviewer authored no implementation and did
not execute the final seed's recovery comparison or tune any setting.

**Amended design and pre-run implementation: pass from this perspective.**
Commit the reviewed source/design and satisfy the other required review gates
before the full comparison. Final results/interpretation and clean-checkout
reproduction remain separate checkpoints.

## Why the amendment matters

The initial grid explicitly included the true 0.17 Hz frequency and its
three-second alias. That did not guarantee that a noise-shifted maximizing
candidate would have its own equivalent aliases represented. The primary
agent identified this before final comparison results and expanded every base
candidate's alias family. The amendment is prospective and records its reason;
it does not claim an earlier recovery result demonstrated this problem.

The reviewer independently rebuilt the final **2,403-point** grid from
`linspace(0.01, 0.45, 881)` plus truth and `abs(k/3 ± f)`, k=-2..2, filtered to
the declared interval, rounded to 12 decimals and sorted uniquely. Every grid
entry matches. Checking alias closure of the expanded grid gives a maximum
nearest-grid discrepancy of about `6.67e-13` Hz, consistent with that rounding.
The same grid is supplied to every sampling condition. Physical equivalence
under the three-second schedule is not a confidence interval or identification.

A separate arbitrary-noise structural fixture on three-second timestamps gave
maximum paired alias-power difference **5.36e-11**, below the fixed `1e-10`
tie tolerance. It did not use final generator observations or assess frequency
recovery. The reviewed three focused tests also passed, covering alias equality
with noise, loss of that equality after jitter, and the wrong time units from
an index FFT applied to thinned samples.

## Generator and method boundaries

The generator follows the frozen order: condition, replicate, phase, applicable
retention/jitter, then noise at actual times. Bernoulli retention precedes jitter;
endpoints are retained for irregular samples. Jitter cannot reverse the retained
integer-time ordering. Regular/thinned spans are 479/477 seconds, respectively,
and the evidence ledger preserves that distinction.

All compared methods receive the same realized time/value pair. Index FFT
mean-centers values and assumes one second per retained sample; that assumption
is correct for the regular control and intentionally incorrect for the irregular
and thinned cases. Interpolation uses only integer times between the observed
endpoints, without extrapolation. Lomb–Scargle receives angular frequencies,
actual timestamps, a floating mean and normalized power. Its lowest-frequency
tie rule and exact numerical tolerance match the contract. Every final input,
replicate result, sample count/span and preselected replicate-zero spectrum is
saved by the runner; examples are not chosen after seeing their appearance.

The implementation has no tuning path or external-data acquisition. The inherited
shared guard still checks first-release CO2/electricity snapshots for workspace
integrity. Configuration now explicitly distinguishes those checks from the
spectral study's **seeded generated observations only**, avoiding a false claim
that those external datasets are analytical inputs. Old run records are untouched.

## Independent finite-only development trial

The reviewer ran one realization per condition with separate seed **20261041**,
retaining the declared generator order. All timestamps were finite/strictly
increasing and all three methods returned aligned finite positive-frequency
power arrays. Interpolated frequencies/powers were independently reconstructed
from the no-extrapolation integer grid. **No peaks, errors or recovery rates
were computed for this trial.** Source hash remained unchanged through it.

| Condition | Samples | Span (seconds) | Index FFT bins | Interpolated FFT bins | Lomb–Scargle bins |
| --- | --- | --- | --- | --- | --- |
| Regular | 480 | 479 | 240 | 240 | 2,403 |
| Irregular | 187 | 479 | 93 | 240 | 2,403 |
| Every three seconds | 160 | 477 | 80 | 239 | 2,403 |

The scoped test command was `pytest -q tests/test_spectral.py`: **3 passed**.
This is execution/invariant evidence, not a final recovery estimate. No repeated
seed search, model fit or post-result choice occurred.

## Presentation and later verification

Two initial template ambiguities were corrected before the gate: index FFT's
one-second assumption is explicitly correct in the regular control, and the
tie column now says **replicates with tied peaks**, matching its numerator.
The report limits the study to the single sinusoid/noise/window/grid setting,
states the alias identifiability limit and avoids physiological ECG claims.
Spectrum heights are normalized to each method's own maximum for display and
are explicitly not comparable power estimates across methods.

Full-result review must independently regenerate final inputs, score summaries,
ties/paired alias powers and selected examples, and check their provenance.
That remains outstanding at this pre-run gate.

## Inspected hashes

```text
45c1851a85db81157a0b3e40a3352ac15983602d1b394e60749ca59d385b7ef3  src/tsatlas/spectral.py
ae87688396e11e8c75de7424cc98b40d35fc898814acead536bf23d8360ea5e2  tests/test_spectral.py
195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422  studies/spectral/DESIGN.md
```
