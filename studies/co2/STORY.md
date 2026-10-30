# Atmospheric CO₂: the process story

**Question:** Does a changing growth rate improve multiyear forecasts over a fixed trend and annual cycle?

**Data:** [NOAA Mauna Loa CO₂ monthly series](https://gml.noaa.gov/ccgg/trends/data.html); monthly records from 1958 onward, with the study snapshot still to be frozen.

**Status (2026-10-30):** first run executed; result/publication review in progress.
The dated entries distinguish earlier plans from later measurements. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected a long atmospheric record because its rise and repeating seasonal pattern make the forecasting problem easy to see. The initial plan listed decomposition and forecasting methods; it did not yet specify the most useful comparison.

## 2026-10-29 — Challenge the first plan

The critical review surfaced that the published series already contains filled-in months and a temporary change of observing site. It also challenged whether this would repeat material already in Ethan's statistics cheat sheet.

## 2026-10-29 — Change the design before fitting

The study now asks whether allowing the rate of increase to change actually improves forecasts. We will preserve the source flags and keep the introductory explanation short. A visible change in the record will not automatically be called a change in the atmosphere.

Technical evidence and outstanding checks: [R01–R02](../../reviews/01-design-review.md#r02--a-published-co₂-series-already-contains-processing-decisions).

## Next at planning time — 2026-10-29

Inspect the actual monthly records and their source notes, then freeze the forecast horizons and comparisons. No model has been fitted and no forecast improvement has been measured.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Check the actual observations

We downloaded and pinned the source file. Both source reviewers found that two
NOAA-era rows had negative variability metadata but zero uncertainty, rather than
the paired negative flags described in the header. The loader now preserves the
fields and conservatively marks either negative value as quality-suspect. It does
not confuse the older Scripps records' unknown metadata with these later flags.

## 2026-10-30 — Define what the comparison can answer

Review narrowed the claim to forecasts made after the December monthly value is
available: one month ahead means January; three years ahead means December. This
is not an evaluation of every month of a future trajectory. The design was
committed before fitting, including a calibration period that ends before the
evaluation begins.

[Source and design evidence](../../reviews/first-release/README.md).

## 2026-10-30 — Run the frozen comparison

For the three-year December targets, the recent-growth model had a mean absolute
error of 1.119 ppm, compared with 6.964 ppm for a fixed growth rate fitted over the
expanding history. Both changing-growth approaches improved on that fixed-growth
baseline at every evaluated origin. The lesson is narrower than “complex models
win”: how much history we assume still applies can matter more than model complexity.

The uncertainty bands also deserve scrutiny. Historical calibration did not
maintain its nominal coverage for the fixed-growth model. Wider or more frequently
covering bands are not automatically better; the report retains their widths and
scores. There are only 13 overlapping three-year origins, not independent trials.

[Executed report](../../reports/results/co2/REPORT.md) · [Saved metrics](../../reports/results/co2/metrics.json).
