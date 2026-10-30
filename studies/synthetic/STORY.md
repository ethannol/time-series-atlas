# Known-truth controls: the process story

**Question:** When the truth is known, how quickly can a sustained change be distinguished from ordinary variation?

**Data:** Purpose-built generated series, with generating rules and random seeds frozen before execution; no downloaded observational dataset.

**Status (2026-10-30):** the change-detection control is executed, independently
reviewed, and reproduced. The promised supporting spectral control is outstanding.
The dated entries distinguish earlier plans from later measurements. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We proposed generated time series because real observations rarely tell us exactly when a change began or what a missing value should have been. Known-truth examples can expose failures that attractive real-data plots cannot settle.

## 2026-10-29 — Challenge the first plan

The general critic challenged a forecasting-only first release and the risk of a miscellaneous synthetic-method gallery. The statistical critic warned that testing a method only on data generated from its own assumptions would be too easy.

## 2026-10-29 — Change the design before fitting

The first control will study change detection, measuring false alerts and delay. Later controls will attach to named real studies and include situations that violate model assumptions. Generated truth will help test methods, but will not be presented as measured real-world performance.

Technical evidence and outstanding checks: [R07](../../reviews/01-design-review.md#r07--a-favorable-metric-can-hide-an-unhelpful-forecast), [R10](../../reviews/01-design-review.md#r10--a-spectral-peak-can-come-from-the-recording-apparatus), and [R12](../../reviews/01-design-review.md#r12--separate-tasks-and-protect-the-evaluation-process).

## Next at planning time — 2026-10-29

Specify the generating processes, seeds, change conditions, and alert evaluation before running comparisons. No synthetic experiment has run.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Specify what counts as a successful warning

Review made the experiment precise before it ran: an early false alert consumes
the attempt, missed changes stay visible, and reported delay is conditional on
actually detecting a change. The thresholds are calibrated on separate simple
noise streams, then tested against both similar noise and deliberately persistent
noise. This lets us ask whether a method's apparent reliability survives a change
in assumptions.

The committed design also fixes the initial condition, the size of the change,
and the exact alert rule. No result has been selected by trying different rules.

[Reviewed contract](DESIGN.md) · [Design checkpoint](../../reviews/first-release/README.md).

## 2026-10-30 — Fast detection can conceal too many false alerts

With independent noise, CUSUM raised a false alert in 5% of the no-change streams.
With persistent noise and the same threshold, it raised one in 73%. Its detection
delay still looked attractive among eligible successful runs. Looking only at
delay would have hidden the practical failure.

The result illustrates why a method's assumptions and evaluation denominator
belong in the main story. It is evidence from declared simulated conditions, not
a measured failure rate for a deployed monitoring system.

[Executed report](../../reports/results/synthetic/REPORT.md) · [Saved outcomes](../../reports/results/synthetic/replicates.csv.gz).

## 2026-10-30 — Recover a promised control from the scope audit

The independent completion critic noticed that the project had promised a
frequency-recovery example for irregularly sampled data, but the checklist
counted the synthetic work as finished after change detection alone. We restored
that supporting control to the outstanding work. Its design includes a sampling
pattern that makes the true frequency ambiguous, so a good-looking peak cannot
be mistaken for proof that a method recovered the truth. No spectral comparison
has run yet.

## 2026-10-30 — Complete the second known-truth control

The full investigation also includes a [sampling and frequency experiment](../spectral/STORY.md).
A general review caught its omission from the first release. We restored it,
reviewed its alias-aware design before execution, and retained all generated
observations and spectra. The two controls test different assumptions: persistent
noise can break an alarm threshold, while a regular sampling schedule can make
different frequencies indistinguishable. Neither is a field-performance claim.
