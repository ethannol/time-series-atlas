# Air quality during outages: frozen study contract

Draft for independent source/design review; no candidate models have run.

## Question and source

Can other stations preserve useful high-pollution indications while a local
sensor is offline? This is a contemporaneous outage nowcast, not advance warning
of future pollution or clinical/regulatory guidance. Other stations' current-hour
reports are assumed available when the indication is issued; actual reporting
latency is unknown. No future observations or post-outage endpoints are allowed.

Use all12 station files from the nested PRSA2017 ZIP inside UCI Beijing Multi-Site
Air Quality (Song Chen,2017,CC BY4.0), March2013–February2017. Ignore the unrelated
outer data.csv/test.csv samples. PM2.5 is micrograms/m³; NA is missing, not zero.
Preserve nominal provider hours without inferred timezone conversions. Audit and
hashes are in `reports/intake/air-quality.json` and `data/manifests/air-quality.json`.

## Training and outages

Fit March2013–February2015. March2015–February2016 is reserved for a bounded
implementation trial only; no tuning. Final period March2016–February2017.
For each station, simulate outages starting09:00 on the first day of every
test month, durations6,24,72hours. An outage is eligible only if its local target
is fully observed and a local reading exists during the prior24hours. Record
every scheduled block and exclusion. The three durations share a prefix and
are dependent scenarios, not independent replications. No selection by model
performance or event magnitude. Natural gaps have no known truth and are not
scored. Complete-block selection limits generalization to real outages.

Each station/duration/block is a separate single-station outage scenario; other
stations retain their real observed availability. These are not simultaneous
network-wide failures. A block starting s with duration L includes timestamps
s through s+(L-1)hours, the half-open interval [s,s+L hours).

Hide every local observation inside a block from every model. Persistence holds
the last available reading strictly before the block. A calendar baseline uses
the training station median for month/hour (global training median fallback).
A network baseline takes the current median of the other11 stations. A calibrated
network model fits Ridge(alpha1) separately for each target, using that median
and hour-of-day sine/cosine; training-only standardization, no tuning. No local
outage values, future values, or interpolated endpoints enter network features.
At least3 other stations must report for the network models to issue a value;
otherwise they abstain. Keep negative fitted concentrations clipped to0 and
save raw predictions too. Fit the same eligibility rule in training.

## Warning threshold and scores

Per-station high pollution is its training90th percentile, fixed across scenarios.
Use pandas' linear quantile interpolation and strict concentration > threshold;
ties are low for truth and prediction alike.
This is a relative research threshold, not a health or regulatory standard.
Compare high/low predictions using that same concentration cutoff for all models.
Primary: macro station balanced accuracy, by duration, on the common hours where
network models can report. Also precision, recall, false-positive rate, counts,
MAE in micrograms/m³ and network availability. Report all-scheduled-hour coverage,
eligible-outage counts, and calendar/persistence performance beyond the common
subset separately. Undefined rates remain null with their denominators shown;
no quiet zero fill. Summarize seasons and station variation, no naive hourly
significance test. Save outage start/end, scheduling/exclusion ledger, all
predictions and targets, source availability, thresholds and fitted coefficients.

Balanced accuracy is (sensitivity+specificity)/2 only when both actual classes
are present for that station/duration/common subset. Otherwise it is null and
excluded from the macro, with the contributing-station count shown. Other rates
show their own denominators; publish pooled confusion counts as secondary evidence.

Also retain the promised event summaries. Within each outage, an event is a
maximal consecutive run of truly high hours; a high run already present at the
first outage hour is left-censored and excluded from onset-delay statistics.
An event is missed if no issued high prediction overlaps it; detection delay
is the number of hours from its start to its first overlapping issued high
prediction, reported only for detected non-left-censored events, alongside
miss and censoring counts. A false-alert episode is a maximal consecutive run
of issued high predictions overlapping no true high hour. These are block-local
episodes, not unique pollution incidents or alarm notifications; a sustained
prediction can overlap multiple true runs. Abstention breaks predicted runs,
and missed events due to abstention stay visible. Natural missingness is not
filled to manufacture event truth. Save event-level evidence for each model.

## Interpretation and gates

Current nearby measurements can help only under the declared availability
assumption; correlated failures and event-dependent real missingness are outside
this simulation. Do not claim recovered natural gaps or population health benefit.
Independent source/design and pre-run implementation reviews precede full runs;
results/publication reviews challenge exactly those scoped claims.
