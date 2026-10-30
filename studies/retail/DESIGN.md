# Intermittent retail sales: frozen study contract

Source/design reviewed before fitting; no candidate models have run at freeze.

## Question and decision

How should we forecast next week's recorded sales for established products that
sell only occasionally? A weekly purchasing planner needs both an error measure
and a warning about systematically underforecasting recorded sales. This is a forecast of
recorded gross sales, not latent demand, stockouts, inventory optimization, or ROI.

## Source and target

UCI Online Retail II, Daqing Chen (2012), CC BY 4.0. Raw ZIP hashes are in
`data/manifests/retail.json`; transformations and audit in `reports/intake/retail.json`.
Use UK transactions, merchandise stock codes matching five digits with at most
one letter suffix, positive quantity and price, and invoices not prefixed C.
Keep rows with missing customer IDs: the target is product-level sales.
Cancellations and corrections are audited separately; they are not negative
customer demand or retroactive edits to a past forecast target. Repeated rows
within one sheet remain because their meaning is unresolved. The two annual
sheets overlap: use the first before 2010-12-01 and the second thereafter.

Aggregate daily units, zero-fill within the supplied collection window. A zero
means no retained sale was recorded, not confirmed availability or zero demand.
The nominal invoice date is used without timezone inference. Restrict complete
scored weeks to Monday 2011-01-03 through Sunday 2011-12-04; exclude the final
partial week. At Monday midnight, forecast the next seven days' total, assuming
prior-day transactions have arrived. Real reporting latency is unknown.

## Cohort, splits, comparisons

Selection uses 2010 only: 10–146 positive-sales days, a sale in the first half,
and a sale in the last quarter. Sort eligible products by total 2010 units
(stable stock-code tie ordering); take 24 equally spaced ranks. Freeze this
nonrandom established-product cohort, including any later discontinuations.
It is not representative of all products or newly launched products.

Initialize methods on daily history from 2009-12-01 through 2010-12-31.
Online updates use only observations before each weekly origin. No test-based
hyperparameter selection. Fixed comparisons: always zero, previous week's total,
28-day mean times seven, Croston-SBA (alpha 0.1), and TSB (size alpha 0.1,
occurrence probability alpha 0.1). Initialize Croston at the first positive
observation with its elapsed interval from collection start; initialize TSB
probability as inverse of that interval. No forecast rounding or clipping needed.

## Scoring and limits

Primary: macro weekly MAE divided by each product's mean 2010 weekly sales
(7 times daily mean). Also save raw-unit MAE, signed total error, total observed
units, total forecast units, and quarterly/per-product scores. Always-zero's
underprediction must remain visible even if its absolute error is competitive.
No claim of statistical significance from treating product-weeks as independent.
Save every weekly target/prediction, origin, scale and product ID. Report coverage
and exclusions, no tuning after inspecting 2011. The records cannot identify
stockouts, lost sales, replacement products or a cost-optimal order quantity.

## Required gates

Separate source/design, pre-run implementation, results, and publication reviews.
Exact protocol commit is recorded by the run metadata. Source audit summaries
may be inspected before fitting; no model comparison or 2011-based cohort choice.
