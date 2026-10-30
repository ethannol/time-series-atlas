# Spectral alias-grid amendment — general design review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Scope: the pre-run amendment in `studies/spectral/DESIGN.md`.
Inspected SHA-256:
`195486becdbe87e0c2953368c05a7935e6c4ade14297d2ff4592bf669522a422`.
The last committed design revision was `fbd9a70b6b5ca5fa83f41cb86d3b2559cc5325df`;
the hash above identifies the amended working file reviewed here. No spectral
results exist at this checkpoint and no code, fit, or numerical test was run by
this reviewer.

**General design verdict: the amendment is appropriate and ready for the required
technical implementation review and pre-run invariant checks. It is not a result
or implementation-verification verdict.**

The scientific question remains compelling: when is an attractive frequency peak
actually identified by the measurements? Including aliases of every candidate
addresses the stated risk more fully than including only the known true frequency
and its one named counterpart. Noise can move the maximum away from that known
pair; the comparison should not call a peak unique merely because its equivalent
candidate is absent from the search grid. A common fixed grid across conditions
also keeps that choice visible and reproducible.

The amendment is proportionate. It changes the grid to protect interpretation,
without adding a new method family or selecting a favorable example. The fixed
generation order, same realization per method, replicate-zero illustration,
tie count, and explicit non-identifiability limitation remain useful. The
three-second condition is a deliberate case the observations cannot resolve,
not a chance to manufacture a winner by the tie-break rule. Likewise, the naive
index FFT illustrates an incorrect time-axis assumption; it is not a fair
representation of every FFT workflow.

Preserve the chronology: this was a lead-agent-identified design risk before
implementation/results. The earlier general design pass did not identify the
noise-shifted-maximum case. Do not recast this as an observed error in a completed
spectral result or as something the initial approval already checked. Technical
review must verify the actual candidate construction, rounding/tolerance, and
alias-invariance behavior; this prose review does not establish those properties.

For the eventual report, explain the change in plain language: equivalent
frequency explanations must be present before a peak can be described as unique.
Show the ambiguity beside any recovery-rate number, and do not infer physiological
ECG frequencies from this generated signal. The design's opening statement that
the control "completes" R10 describes intended scope only; actual completion still
requires execution, reviewed evidence, reproduction, and publication.
