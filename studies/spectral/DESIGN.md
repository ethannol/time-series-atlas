# Supporting synthetic control: irregular sampling and frequency recovery

Frozen design, with the pre-run amendment below; no comparisons run. This completes the
R10 control promised alongside ECG; it is part of the synthetic investigation.

## Question and relevance

When observation times are irregular, can a dominant frequency estimate be
trusted? A periodic-looking waveform can reflect the sampling schedule or
recording machinery. Known truth lets us distinguish recovery from an attractive
spectral peak. This is not a finding about physiological ECG frequencies.

## Frozen data generation

Generate 100 replicates per sampling condition, seed 20261032, NumPy default_rng.
Signal sin(2π*0.17*t+phase) plus independent Normal(0,0.5²) measurement noise;
phase uniform[0,2π). Nominal observation window0–479seconds. Three conditions:
regular integer seconds; irregular independent Bernoulli(p=0.4) retention of
interior integer times with
independent uniform[-0.4,0.4] jitter (retain endpoints0 and479); regular thinning
to every3seconds (0,3,...477). Generate noise at the actual sampled times; do not
interpolate noise from a denser hidden process. Record all actual times and values.
Replicates are independent. Same sampled realization feeds all compared methods.

## Fixed methods

Naive index FFT assumes successive retained samples are one second apart,
subtracts their mean, uses an unwindowed real FFT and takes the strongest
positive frequency. Interpolated FFT linearly interpolates to integer seconds
from ceil(first observed time) through floor(last observed time), then applies
the same FFT with one-second spacing; no extrapolated endpoints.
Lomb–Scargle uses actual timestamps and a floating mean, without interpolation.
Start with frequencies linspace(0.01,0.45,881) plus 0.17. Include the entire
three-second alias family abs(k/3 ± f), k=-2,...,2, within [0.01,0.45]; round
to 12 decimal places and sort unique. Use this same grid in every condition. Use scipy.signal.lombscargle with angular frequencies
2πf, floating_mean=True, normalize=True. If powers are within1e-10 of the maximum,
choose the lowest tied frequency; retain tie count and both known-alias powers.
No tuning of grids, smoothing, thresholds or generation based on results.

The every-three-second condition has Nyquist frequency1/6Hz below the true0.17Hz.
Both0.17 and1/3-0.17 yield equivalent sampled sine/cosine spans. Including both
explicitly prevents grid alignment from masquerading as identification. A
method must not be credited with resolving this ambiguity from these samples.

## Evidence and interpretation

Per condition/method report median absolute frequency error and recovery fraction
within1/480Hz of0.17, with replicate count. Show sample count/span distributions,
the paired alias powers, and one preselected replicate0 time/spectrum example.
Save every replicate's input, peak, error and ambiguity diagnostics. No claim
of universal Lomb–Scargle superiority, significance, or real-world performance.
Frequency recovery rates in the aliased condition must be accompanied by the
identifiability limitation; a grid tie-break is not evidence of physical truth.

No downloaded source is required. Scientific software usage follows the official
[SciPy lombscargle documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lombscargle.html); exact runtime dependencies are locked. Separate
general/statistical/implementation design review and pre-run technical review
precede execution; results and publication review check the interpretation.

## Pre-run amendment — 2026-10-30

Before implementation or any frequency-recovery results, the lead agent noticed
that including only the true frequency and its alias was insufficient. Noise
can move the maximum to another grid point whose equivalent alias was absent,
creating an apparent unique answer caused by the grid. The expanded grid includes
each candidate's alias family. Rounding removes floating-point duplicate points;
the fixed tolerance handles numerical equality, not statistical uncertainty.
This change requires renewed review and a numerical alias-invariance test.

Generation order is regular, irregular, every-three-seconds, then replicate
0–99 within each condition. Draw phase first, then any retention/jitter, then
measurement noise. The same realization feeds all three methods. The saved
replicate-zero spectra are illustrative, not selected for their appearance.
