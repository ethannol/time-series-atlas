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

[Frozen design and amendment](DESIGN.md). Results have not yet been interpreted.
