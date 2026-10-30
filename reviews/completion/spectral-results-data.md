# Spectral result evidence and alias audit

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: the full spectral run from source/protocol
`2c0af60037ae691aae7e13c92cb37228215e5876`, seeded observations, spectra,
replicate summaries and provenance. The reviewer independently reconstructed
the fixed calculations without authoring source, changing parameters or tuning.

**Artifact and numeric verdict: pass. Publication remains pending the final
result story/copy and clean-checkout reproduction.** No mismatch was found in
the recorded seed realization, frequency estimates, ties, examples or summaries.

## Provenance and seeded inputs

All **37 source hashes** match historical Git blobs at the recorded commit;
all **eight output hashes** match current files. The inherited snapshot checks
also pass and are explicitly labelled workspace integrity only, separate from
the seeded observations that actually enter this study. The run records stable
source, approximately 5.38 seconds elapsed and 364 MB process-lifetime peak RSS.
These are local execution measurements, not portable performance benchmarks.

An independent generator following the frozen RNG order and seed 20261032
recreated all **83,278 input rows** across 300 replicates. Serializing/compressing
that independently generated table produced the **exact saved input SHA-256**.
The same realized observations feed each replicate's three methods. All 300
sample-count/span rows agree. Irregular samples range from 167 to 217 observations
(mean 192.78) over 479 seconds; regular samples have 480 over 479 seconds, and
three-second samples have 160 over 477 seconds.

## Spectra, estimates and aliases

The reviewer independently recreated the 2,403-point rounded alias-complete
grid, index FFTs, integer-grid interpolation FFTs, and normalized floating-mean
Lomb–Scargle powers from those observations. Every one of the **900 method
result rows** matches its peak, error, recovery flag, tie count and applicable
truth/alias powers. All **8,338 preselected replicate-zero spectrum rows** also
match, as do all nine aggregate summaries. No final example was selected for
appearance. Numeric comparisons allow only floating CSV/operation tolerances;
input compressed bytes match exactly.

All 100 regular replicates recover within the declared tolerance for each method.
For irregular observations, index FFT recovers 0/100, interpolation FFT 74/100,
and Lomb–Scargle 100/100. For every-three-second observations, every method has
0/100 recovery under the fixed selection rule. **All 100 thinned Lomb–Scargle
replicates have exactly two tied maxima**. The maximum saved truth/known-alias
power difference is about `7.36e-11`, below the fixed `1e-10` equality tolerance.
The lowest-frequency tie rule picks an alias, not a physically identifiable truth.

The Lomb–Scargle zero median error in regular/irregular cases concerns this
discrete search grid, which explicitly includes the known true frequency. It
should not be described as arbitrary-precision continuous-frequency estimation.
Nor do this one sinusoid, noise level, time window and method configuration
establish a universal ranking of frequency-estimation methods.

## Figure and claim review

Both figures were visually inspected. The recovery and ambiguity panels expose
the distinction between a chosen peak and an identifiable answer. The preselected
time/spectrum examples match the saved data and show the index FFT's lost time
units. Spectra are divided by their own maximum for display; the report clearly
says their displayed heights are not comparable power estimates across methods.

The report preserves the physiological/ECG boundary, numerical tie definition,
prospective grid amendment and same-observation comparison. Its phrase
“including an occasional correct one” should be rewritten hypothetically:
no thinned replicate was recovered by the fixed rule in this run. For example,
an estimate matching truth would still not resolve the alias ambiguity. This
is a copy clarification, not a numeric defect or reason to change the tie rule.

The process story currently ends before interpretation. Append what the final
run showed, including successful irregular-time recovery in this setting and
the irreducible alias ambiguity under regular thinning. Preserve the earlier
planning/amendment chronology; do not claim the expanded grid was chosen after
these observed results. Add the discrete-grid qualification beside zero-error
claims rather than letting a perfect-looking number imply unlimited precision.

## Remaining checkpoint and inspected hashes

This review independently reconstructs the evidence but does not claim a final
clean-checkout rerun or publication. The parent is separately refreshing study
presentation artifacts; their numerical-byte comparison and final reproduction
remain outstanding. No source files were changed by this review.

```text
42b2225ab875b7d5e88bbf66a3a7dbed2e9efa93072cb6e40b8c082e3aacc058  reports/results/spectral/run.json
3c1ab52d60ce41bb9920aa29c2a8fcf8bcff3a6b80b142bd2ac78b152250d244  reports/results/spectral/metrics.json
7dd5b02bb7bc8afeaaf41bd0320c8d2b0b36170380bc85d9ba2e80b002ebff9f  reports/results/spectral/inputs.csv.gz
8067b80377a5af51487ac842f827c976dc66c1eb412fcc75bb433ca81db4b467  reports/results/spectral/replicates.csv.gz
c7d006cfa5b4de98c37643b5e0ca190a6260d7c0ba5ce0b17ab633c9e2ec4615  reports/results/spectral/example-spectra.csv.gz
ba4982ded6d607ee2624efb75b79eb807c001edbf71d8fbd37949ceb30662e96  reports/results/spectral/REPORT.md
58e32d541f4c26b72c40b69ce2a8977cf1af8824eb97c82beb83c14770a41fee  reports/results/spectral/sampling.csv
b698992e81a41f5d613cc6c294a4fcd3b2dcb23fa170c843de8f784f7bd8c280  reports/results/spectral/recovery-and-ambiguity.png
37036241d69b51e948e0ce74559dc2f3083cdb8085f2b2d897325b3461c50d7a  reports/results/spectral/preselected-examples.png
93262c04377dccdbc39aa1d73a9f74349ce392c17a2a9ddff0c439396d72cba6  studies/spectral/STORY.md
```
