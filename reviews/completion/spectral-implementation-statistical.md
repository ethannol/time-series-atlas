# Spectral pre-run implementation review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: `spectral.py`, focused tests and the amended design. No final 100-replicate
comparison was run by this reviewer; checks use bounded invariants and separate
toy seeds. The reviewer did not author implementation or tests.

**Statistical implementation verdict: approved for the frozen run.** No blocking
data-generation, method, denominator or information-boundary discrepancy was
identified. The related [grid amendment](design-amendment-statistical.md) is also
approved. Results and publication remain unreviewed until outputs exist.

## Generation, method and scoring checks

Generation order matches the amended contract: condition then replicate, phase
first, irregular retention/jitter when relevant, and independent noise at the
actual observation times. The irregular interior uses independent Bernoulli 0.4
retention with jitter within ±0.4 seconds; endpoints remain 0 and 479. Jitter
cannot reverse adjacent retained integer times. Regular conditions contain 480
observations through 479 seconds or 160 observations through 477 seconds. A
single seeded generator supplies disjoint draws; every method within a replicate
receives the identical realization. There is no hidden dense-noise interpolation.

FFT implementations subtract their own input mean, discard the DC bin, retain
the positive real-FFT frequencies and apply the declared one-second spacing.
That spacing is appropriate for the regular control and intentionally incorrect
for raw irregular/thinned indices, as the revised report now states. Interpolation
uses only integer times inside the observed range, with no endpoint extrapolation.
Lomb–Scargle receives actual timestamps, angular frequencies, a floating mean and
normalized power. Its grid and tie tolerance match the amended contract.

The selected peak is the lowest frequency within the fixed maximum tolerance;
FFT uses exact ties and Lomb–Scargle uses 1e-10. Recovery uses the predeclared
inclusive 1/480-Hz tolerance around 0.17 Hz. The run loops produce 100 observations
per condition/method. Summary denominators count replicates, and the tie summary
counts replicates with more than one tied peak rather than summing frequencies.
Inputs, per-replicate errors/ties, paired known-alias powers, sample spans and
preselected replicate-zero spectra are saved. Normalizing each example spectrum
to its own maximum is explicitly a display convention, not a power comparison.

## Bounded evidence executed

`uv run pytest -q tests/test_spectral.py`: **3 passed**. The tests cover a noisy
three-second alias family, breaking the known alias with timing jitter, and an
FFT time-unit fixture. No frozen-experiment recovery summary was generated.

An independent grid check finds 2,403 sorted distinct candidates and all declared
in-range aliases within approximately 6.7e-13 Hz of a represented candidate.
A separate noisy toy sinusoid at 0.1134 Hz, rather than the experiment's 0.17-Hz
truth, yields three tied maximum candidates under the declared 1e-10 rule.
This directly checks an alias family away from the specially named true/alias
pair. Across that toy's entire grid, paired power differences can reach about
3.7e-10 away from maxima because 12-place rounding is not exact arithmetic; the
maximum aliases nevertheless meet the required peak tie rule. This is bounded
numerical evidence, not a proof of a floating-point tolerance for all signals.
The results review should check the final maximum/known-alias diagnostics rather
than infer identification from a finite-grid peak.

Independent separate-seed generation checks confirm sorted times, deterministic
repetition, endpoint/sample-count rules and jitter bounds without calculating
recovery scores. A hand-computable summary fixture verifies median error,
recovered count/fraction and ambiguous-replicate denominator; a two-near-equal-
peak fixture verifies the lowest-frequency convention. The first reviewer grid
script needed an empty-alias-family guard before its reduction; this was a
review-script correction, not a change to study code or an implementation defect.

The final inspected revision changes renderer labels and generated-only metadata
from the initially tested revision; generation, estimators and scoring functions
remain unchanged. The metadata identifies seeded observations as the analytical
inputs, separate from inherited workspace integrity checks. No external source
is needed by the simulation itself.

## Interpretation limits and later gates

Different conditions also have different sample counts, and this is a single
sinusoid/noise/window specification. The comparison establishes no universal
method ranking, effect of irregularity alone, or conclusion about physiological
ECG frequencies. Regular three-second sampling remains nonidentifying regardless
of the deterministic peak chosen. Any claimed full-run recovery rate must be
presented beside that ambiguity and its actual replicate counts. This review
requests no final-score-driven tuning.

Inspected SHA-256 identities:

```text
45c1851a85db81157a0b3e40a3352ac15983602d1b394e60749ca59d385b7ef3  src/tsatlas/spectral.py
ae87688396e11e8c75de7424cc98b40d35fc898814acead536bf23d8360ea5e2  tests/test_spectral.py
195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422  studies/spectral/DESIGN.md
```
