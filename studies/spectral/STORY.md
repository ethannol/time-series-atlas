# The spectral control story

## 2026-10-29 — A convincing waveform needs a sampling question

The initial critique asked us to separate a waveform's appearance from the
process that sampled it. We planned a small known-truth control alongside the
ECG investigation: preserve actual observation times, then ask whether the
dominant frequency can be recovered. It is part of the synthetic study and
does not establish a physiological finding.

## 2026-10-30 — Restore a promise omitted from the first release

The general critic caught that completing change detection had not completed
the promised synthetic controls. This frequency experiment remained outstanding.
We restored it explicitly to the full-scope checklist.

## 2026-10-30 — Do not let the search grid invent certainty

Before implementing the experiment, the lead agent noticed a flaw in the proposed
frequency grid. It contained the true frequency and its sampling alias, but
noise could move a peak to a different candidate whose alias was missing.
We amended the design to include the full alias family of every candidate,
and asked independent reviewers to check it. The lesson is about identifiability:
some observation schedules cannot distinguish different physical signals,
however clear a plotted peak looks.

[Frozen design and amendment](DESIGN.md). The result step follows below.

## 2026-10-30 — Recover a frequency, then ask whether it is unique

The frozen experiment recovered the planted frequency in every irregular-sampling
Lomb–Scargle trial, versus seventy-four of one hundred interpolation-plus-FFT
trials. Ignoring the timestamps recovered none. Yet when observations were
regularly spaced three seconds apart, every Lomb–Scargle trial had two equally
strong peaks. Its declared tie rule selected the lower alias each time.

That is the distinction the control was designed to expose: a selected spectral
peak is not necessarily a uniquely identified physical frequency. Reviewers
recreated the generated observations and all spectra, checked the numerical
alias ties, and asked us to make the ambiguity and discrete search grid explicit
in the report and figures. The result does not establish an ECG rhythm finding.

[Results](../../reports/results/spectral/REPORT.md) ·
[Statistical audit](../../reviews/completion/spectral-results-statistical.md).

## 2026-10-30 — Reproduce all generated inputs and outputs

A clean checkout regenerated the same observations, spectra, metrics, figures
and report byte-for-byte. [Reproduction evidence](../../reports/verification/completion-reproduction.json)
records the separate environment and comparison against committed reference files.
Live publication verification remains a separate delivery gate.

## 2026-10-30 — Verify the public control alongside the real-data studies

The control is published within the synthetic investigation. Live verification
checked its report link and the deployed recovery/ambiguity figure against the
retained bytes. [Publication evidence](../../reports/verification/completion-rollout.json).

## 2026-10-30 — Ask whether the comparison changes more than timestamps

The dedicated critic confirmed the recovery counts and alias ambiguity, then
noticed that our main explanation did not make the unequal search ranges clear.
Lomb–Scargle excludes very low frequencies that the FFT can select. Some FFT
failures fall in that excluded range, so the comparison cannot isolate timestamp
handling alone.

We disclosed that difference, exposed the low-frequency part of the spectrum
plot, and summarized the already-saved sampling support and paired alias powers.
The methods, grids and recovery scores remain unchanged. A matched-range
comparison would be a separate study, not a correction to these frozen scores.

[Dedicated critique](../../reviews/study-critiques-20261030/synthetic.md) ·
[Resolution status](../../reviews/study-critiques-20261030/RESPONSE.md).
