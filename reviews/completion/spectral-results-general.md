# Spectral control results and publication — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Run source and protocol: `2c0af60037ae691aae7e13c92cb37228215e5876`.

Read the report, summary metrics, frozen design/amendment, current spectral and
synthetic stories, run metadata, sampling schema/examples, and replicate-zero
result rows. Visually inspected both figures. Hashed the full linked evidence
for scope; did not regenerate signals, recompute spectra, audit every prediction,
run tests, or perform exact reproduction.

## Results verdict

**The saved results support the intended lesson: preserving actual observation
times helps in this irregular-sampling experiment, but a sharp spectral peak
does not resolve an alias created by the sampling schedule.** This completes
the execution of the promised supporting comparison, not its remaining review,
reproduction or publication gates and not the overall project's completion.

Under regular one-second observations, all three methods recover within the
declared 1/480 Hz tolerance in all 100 replicates. Under irregular retention and
jitter, Lomb–Scargle recovers in 100/100, interpolation plus FFT in 74/100, and the
deliberately mis-timed index FFT in 0/100. The latter illustrates the consequence
of an incorrect time-axis assumption; it is not a fair general-purpose FFT
baseline for irregular sampling.

Under regular three-second sampling, every method's selected peak misses the
declared recovery tolerance. Lomb–Scargle retains two equal-power grid maxima in
all 100 replicates; the fixed lowest-frequency tie-break selects the lower alias.
This is non-identifiability from those observations, not evidence that changing
the tie-break would recover physical truth. Both correct and incorrect selected
answers could arise from arbitrary tie-breaking while leaving the ambiguity.

The pre-run amendment and known-alias explanation are appropriately prominent.
The report limits the result to a single-sinusoid/noise/window/grid experiment,
does not attribute a physiological result to ECG, and does not claim a universal
method ranking. The executed regular and deliberately aliased controls keep this
from being only a favorable example for the timestamp-aware estimator.

## Publication verdict

**Scoped result interpretation is supportable. The short answer, diagnostic
labels, and executed-story updates below remain necessary before publication.**
No data generation, grid, estimator, scoring or tuning change is requested.
Separate numerical review and clean-checkout reproduction remain outstanding
from this general review's perspective.

### GSP01 — Lead with recovery versus identifiability, and explain zero error

Priority: medium; status: identified.

The report opens with a method list. Give the reader the direct answer first:
using timestamps improves this irregular comparison, while three-second sampling
leaves two equivalent frequency explanations. Use 100/100 versus 74/100 and the
100 tied cases to make the result concrete, without treating that finite count
as a guarantee for other signals or sampling patterns.

The zero median error deserves one precise qualification: the Lomb–Scargle grid
explicitly contains the planted truth, while FFT frequency bins differ. Its
zero median versus the small nonzero regular-FFT error is not a general precision
ranking. All regular-control methods meet the same declared tolerance. Preserve
the fixed design; this asks for interpretation, not a post-result grid change.

### GSP02 — Identify what the ambiguity plot actually measures

Priority: medium; status: identified.

The right panel of `recovery-and-ambiguity.png` does not name the method whose
equal-power peaks it displays. Label it explicitly as the Lomb–Scargle grid
diagnostic. The three point locations overlay 100 replicates apiece; an `n=100`
annotation or caption would make the replication clear without inventing jitter.

The table records no FFT ties in the aliased condition, but that is not evidence
that FFT identifies the physical frequency. State that numerical maxima/tie
counts reflect each method's search representation; structural alias ambiguity
remains even when an implementation reports one peak. Keep this distinction
beside the table/figure so a reader cannot interpret fewer ties as better science.

The example figure is useful and legible. The time-axis warning on the FFT,
truth/alias reference lines and per-method power normalization are well stated.
Add that left panels display only the first 60 seconds, while spectra use each
full record (479-second span for regular/irregular, 477 for thinned). The
preselected irregular example happens to be an interpolation failure; the
74/100 aggregate already prevents treating it as a representative success rate.
Retain the explicit preselection rather than replacing it with a prettier case.

### GSP03 — Append the measured result to the synthetic/spectral story

Priority: medium; status: pending parent update.

The spectral story ends with "Results have not yet been interpreted"; the parent
synthetic story still calls the control outstanding and says no comparison has
run. Append the actual execution and bounded answer, link the report/reviews,
and keep reproduction/publication honestly pending. Make the spectral entry
discoverable from the main synthetic story as its supporting control. Preserve
the scope-recovery and grid-amendment chronology, including that the latter was
a lead-agent-identified pre-run design risk rather than an executed score defect.

## Inspected evidence hashes

The input/spectrum files below are scoped evidence, not a claim that this general
review independently recomputed them.

```text
ba4982ded6d607ee2624efb75b79eb807c001edbf71d8fbd37949ceb30662e96  reports/results/spectral/REPORT.md
3c1ab52d60ce41bb9920aa29c2a8fcf8bcff3a6b80b142bd2ac78b152250d244  reports/results/spectral/metrics.json
b698992e81a41f5d613cc6c294a4fcd3b2dcb23fa170c843de8f784f7bd8c280  reports/results/spectral/recovery-and-ambiguity.png
37036241d69b51e948e0ce74559dc2f3083cdb8085f2b2d897325b3461c50d7a  reports/results/spectral/preselected-examples.png
8067b80377a5af51487ac842f827c976dc66c1eb412fcc75bb433ca81db4b467  reports/results/spectral/replicates.csv.gz
58e32d541f4c26b72c40b69ce2a8977cf1af8824eb97c82beb83c14770a41fee  reports/results/spectral/sampling.csv
c7d006cfa5b4de98c37643b5e0ca190a6260d7c0ba5ce0b17ab633c9e2ec4615  reports/results/spectral/example-spectra.csv.gz
7dd5b02bb7bc8afeaaf41bd0320c8d2b0b36170380bc85d9ba2e80b002ebff9f  reports/results/spectral/inputs.csv.gz
42b2225ab875b7d5e88bbf66a3a7dbed2e9efa93072cb6e40b8c082e3aacc058  reports/results/spectral/run.json
195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422  studies/spectral/DESIGN.md
93262c04377dccdbc39aa1d73a9f74349ce392c17a2a9ddff0c439396d72cba6  studies/spectral/STORY.md
718fb2a856d39ee8df2bcd564433b70ee1056489b1f0902a8789be9d91f07f18  studies/synthetic/STORY.md
```
