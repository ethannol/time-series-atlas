# Spectral grid amendment: independent statistical review

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: the pre-run amendment in `studies/spectral/DESIGN.md`. No final spectral
comparison has been run by this reviewer. The reviewer did not author the change.

**Design-amendment verdict: approved.** The amendment repairs a prospective
identifiability demonstration risk, not an observed final-result bug. Credit for
finding the incomplete original grid belongs to the lead agent. The earlier
design review's approval of including only the true frequency and its alias did
not account for noise shifting a maximum to a different candidate.

For times `t = 3n`, adding an integer multiple of `1/3` Hz leaves the sampled
sine/cosine span unchanged; changing frequency sign changes a sine-column sign,
not the fitted span. These equivalences apply to every candidate frequency,
including a noise-shifted maximum. Merely adding 0.17 and its known alias can
therefore leave a different sampled maximum artificially unique.

Expanding every base frequency to `abs(k/3 ± f)`, keeping the declared frequency
range and deduplicating after 12-place rounding, addresses that grid-selection
problem. Using the same resulting grid in all conditions avoids changing the
search according to the outcome. Fixed generation order and replicate-zero
examples also make the experiment reconstructible without favorable selection.

The amendment does not make regular three-second samples identify the physical
frequency. The lowest tied maximum is a reporting convention. Numerical ties
are not confidence intervals, and interpolation cannot recover the information
lost to exact regular aliasing. The proposed report retains these limits and
keeps this simulation separate from physiological claims about ECG recordings.

Closure evidence belongs to the paired
[pre-run implementation review](spectral-implementation-statistical.md): inspect
alias-family grid coverage and bounded noisy peak invariance. The later results
gate must confirm that the saved ambiguity diagnostics support the claims for
all evaluation replicates. There is no authorization to retune the grid after
seeing recovery rankings.

Inspected SHA-256:

```text
195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422  studies/spectral/DESIGN.md
```
