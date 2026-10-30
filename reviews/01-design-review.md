# What critical review changed before implementation

Date: 2026-10-29. Scope: the proposed datasets, questions, evaluation, delivery
plan, and source documentation. No analysis code, fitted models, or measured
results existed. This record is the primary agent's synthesis of three separate
agent critiques and subsequent user steering, not a verbatim transcript or human
validation report.

Individual reviewer reports are retained separately:
[general critic and subsequent clarifications](project/2026-10-29-initial/general.md),
[statistical critic](project/2026-10-29-initial/statistical.md), and
[data/implementation critic](project/2026-10-29-initial/implementation.md).
Read them alongside the [decisions about recommendations](README.md#decisions-about-reviewer-recommendations)
to distinguish each critique from the synthesis and later user direction.

**Why this is prominent:** Ethan requested critical agents after the initial
proposal. That intervention surfaced consequential issues before implementation.
The original proposal did not adequately address them. We cannot know that every
risk would have become an error; we can show exactly how review changed the plan.

## What each perspective contributed

- **General critic:** challenged breadth without a coherent question, overlap with
  the existing statistics cheat sheet, a forecasting-heavy first release, and
  whether a reader could distinguish planned methods from completed studies.
- **Statistical critic:** challenged predictor availability, split construction,
  target-derived catchment descriptors, sparse-sales metrics, subject leakage,
  recording artifacts, and overinterpretation of uncertainty and clinical value.
- **Data/implementation critic:** checked source notes, data revisions and snapshots,
  official download/version resolution, redistribution assumptions, execution cost,
  and whether the shared framework would become larger than the investigations.

All reviewers were AI agents. Their claims require evidence; being independently
authored does not make them independent human checks or guarantee correctness.

## R01 — Ask an answerable question before choosing methods

**Type:** design/communication risk. **Priority:** high.
The original breadth of methods could produce a catalogue without a memorable
finding. CO₂ also overlaps the existing statistics reference.

**Change:** one compelling question, a simple benchmark, a few justified
comparisons, and a clear answer per study. Keep CO₂ concise, electricity deeper,
and label capabilities as planned, implemented, or evaluated.

**Verification needed:** review each frozen study contract for answerability,
evaluation, and scope. A rewritten plan alone does not establish a useful study.

## R02 — A published CO₂ series already contains processing decisions

**Type:** source-confirmed facts with prospective analysis risks. **Priority:** high.
NOAA's file documents interpolated missing months, early Scripps observations,
and a temporary Maunakea substitution during the Mauna Loa interruption. Negative
metadata values in the early Scripps portion indicate unavailable metadata, so
they must not all be treated as interpolation flags.
[Source: official file header](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt).

**Why it matters:** filled values could be mistaken for independent measurements;
a site-related change could be interpreted as a change in atmospheric behavior.
Currently published historical values are not necessarily the values available
at each historical forecast date.

**Change:** preserve provenance and quality fields, use the monthly-average
column rather than the already deseasonalized column, inspect flags by source
period, and label revised-data backtests honestly.

**Verification needed:** inspect actual inputs and flagged periods, verify
training-only transformations, and review sensitivity to affected observations.

## R03 — Electricity zeros and time labels are not self-explanatory

**Type:** source-confirmed facts with prospective analysis risks. **Priority:** high.
UCI documents zeros before some customers became active, zeros during a
daylight-saving transition, and aggregated values during the opposite transition.
The observations represent power in kW; energy aggregation requires explicit
interval handling. Ordinary timezone conversion cannot recover information the
publisher already combined.
[Source: UCI electricity documentation](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014).

**Change:** separate activation and clock-transition handling, retain quality
masks, define the power/energy target, and construct cohorts from permissible
history. Separate forecasts for known customers from transfer to new customers.

**Verification needed:** unit and interval checks, actual cohort/split records,
and sensitivity to affected periods. Do not assume every zero is inactivity.

## R04 — Some catchment descriptors already contain the outcome

**Type:** source-confirmed fact and conditional leakage risk. **Priority:** critical
for any ungauged-catchment experiment.
CAMELS attributes include hydrological signatures calculated from flow, such as
mean discharge and baseflow index.
[Source: NCAR attribute documentation](https://ncar.github.io/hydrology/datasets/CAMELS_attributes).

**Why it matters:** using these to predict an ostensibly unseen river's flow could
give a model information it would not have at an ungauged site.

**Change:** allowlist feature provenance. Exclude target-derived attributes from
ungauged experiments; compute permissible historical summaries only within
training data. Audit the time support of other derived attributes too.

**Verification needed:** inspect actual feature inputs and include a check that
rejects forbidden attributes. No leakage was observed in code because no code existed.

## R05 — Observed weather is not a weather forecast

**Type:** information-availability design risk. **Priority:** high.
CAMELS supplies retrospective meteorological inputs. Future observed rainfall
cannot be silently supplied to a model claiming an operational forecast.
[Source: NCAR dataset descriptions](https://ncar.github.io/hydrology/datasets/).

**Change:** declare input availability and lags. Use permitted history for the
primary warning question; label any future-observed-weather experiment as
retrospective conditional prediction. Note assumptions about reporting delays.

**Verification needed:** a timestamp trace from raw input through a representative
prediction and independent review of the declared forecast setting.

## R06 — Transactions tell us what sold, not everything customers wanted

**Type:** source-schema fact and interpretation/cohort risks. **Priority:** high.
Online Retail II records transactions and cancellations; its documented fields
do not establish inventory availability, unmet demand, or replenishment lead times.
The roughly two-year window also limits evidence about repeated annual patterns.
[Source: UCI retail documentation](https://archive.ics.uci.edu/dataset/502/online+retail+ii).

**Change:** forecast positive observed sales, account separately for returns and
cancellations, and define product eligibility using training history rather than
eventual last-sale dates. Do not claim optimal inventory or measured savings.

**Verification needed:** actual target/cohort construction and review of any
scenario assumptions. Inventory-cost calculations, if added, remain scenarios.

## R07 — A favorable metric can hide an unhelpful forecast

**Type:** methodological evaluation limitation. **Priority:** high.
Absolute error alone can favor always-zero forecasts for sparse series. Interval
coverage alone can reward excessively wide forecasts. MAPE is unsuitable at zero,
and scaled scores require a rule for zero denominators.

**Change:** include zero/simple-rate sales baselines, weekly totals, signed and
aggregate bias, and appropriate probabilistic scores. Pair interval coverage with
width and proper interval scoring by horizon. Compare identical origins/targets.

**Verification needed:** scoring checks and actual comparison outputs. No model
has yet been shown to win or fail under these metrics.

## R08 — A missing point is not a station outage

**Type:** source-confirmed missingness and experimental-design risk. **Priority:** high.
Beijing data have missing hourly observations. Randomly hiding isolated points is
not equivalent to losing a station for hours or days.
[Source: UCI air-quality documentation](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data).

**Change:** simulate contiguous outages on observed periods, vary duration, and
separate online warnings from retrospective reconstruction. Nearby-station inputs
must be available at the declared decision time. Natural missing values have no
known truth and cannot be scored as though they did.

**Verification needed:** mask construction, concealed held-out truth, and a trace
showing no later readings entered an earlier warning. Use event-level false
alarms, misses, and delay; synthetic missingness may still differ from real outages.

## R09 — Separate people, not just files

**Type:** source-confirmed fact and conditional split risk. **Priority:** critical
for claims about new-person generalization.
MIT-BIH records 201 and 202 belong to the same person. Random beat splitting or
even naive record splitting can therefore misrepresent person-level generalization.
[Source: PhysioNet recording notes](https://physionet.org/physiobank/database/html/mitdbdir/intro.htm).

**Change:** explicit person-group splits, including the shared subject, and
per-class/per-person evaluation. Detection tolerance must be specified in advance.

**Verification needed:** actual person-to-split manifest and disjointness checks.
This is a known risk; no inflated performance has been measured in this project.

## R10 — A spectral peak can come from the recording apparatus

**Type:** source-confirmed artifacts and sampling design. **Priority:** high.
PhysioNet documents tape-related artifacts, including a prominent 0.167 Hz
component, and cautions about heart-rate-variability analysis. The collection
also deliberately includes unusual rhythms.
[Source: PhysioNet recording notes](https://physionet.org/physiobank/database/html/mitdbdir/intro.htm).

**Change:** retain waveform recognition as the ECG question, interpret signals
with recording artifacts in mind, and use synthetic controls for clean
irregular-sampling spectral recovery. No population prevalence or clinical
effectiveness claims follow from benchmark recognition scores.

**Verification needed:** processing/figure/claim review against recording notes;
synthetic controls must include cases poorly matched to the tested models.

## R11 — Price transformations and relationships are hypotheses

**Type:** design risk to inspect against actual observations. **Priority:** high.
Log transformations require positive values. Price relationships and stable
cointegration cannot be assumed merely because two series describe crude oil.
[Sources: EIA WTI](https://www.eia.gov/dnav/pet/hist/RWTCD.htm),
[EIA Brent](https://www.eia.gov/dnav/pet/hist/RBRTED.htm).

**Change:** audit nonpositive values and trading-calendar gaps, freeze level/
difference/return rules, benchmark direction and volatility separately, and test
any relationship extension with sensitivity to changing regimes.

**Verification needed:** input audit, explicit transformation behavior, and
out-of-sample scoring. No profitable strategy or stable relationship is presumed.

## R12 — Separate tasks and protect the evaluation process

**Type:** cross-cutting methodological risks. **Priority:** high.
Centered smoothing and retrospective reconstruction can use later observations.
Forecasting and online detection cannot. Tuning, imputation, normalization,
calibration, and repeated inspection can also cross evaluation boundaries.

**Change:** declare task/issue time/horizon/input availability; fit transformations
within training windows; use rolling selection and a final evaluation period with
selection frozen. Distinguish new-series transfer from known-series forecasting.
Log protocol deviations and include failed attempts in result review.

**Verification needed:** split and transformation audits, future-perturbation
checks where applicable, tuning logs, and uncertainty summaries that respect
overlapping forecasts and related series rather than assuming independent errors.

## R13 — A checksum is not an archive or a redistribution license

**Type:** reproducibility limitation. **Priority:** high before reproduction claims.
A manifest detects changed bytes but cannot retrieve a historical file after the
provider replaces it. Free access alone does not establish every redistribution
right. EIA's reuse policy distinguishes third-party material, and its oil-price
notes identify an external source.
[EIA reuse policy](https://www.eia.gov/about/copyrights_reuse.php),
[price source notes](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp).

**Change:** retain exact source snapshots; separate reproduction from refresh;
record redistribution basis before mirroring. If public archival rights remain
unclear, document the limitation and preserve acquisition instructions/local bytes.
Unclear mirroring rights do not automatically prevent analysis.

**Verification needed:** actual pinned-byte reproduction and a recorded basis for
each published snapshot. Hash documentation alone does not close this finding.

## R14 — Resolve actual CAMELS files and versions

**Type:** source-access/packaging finding from documentation review. **Priority:** medium.
The implementation reviewer traced the official DOI to the NCAR Zenodo deposit,
identified an unrelated destination in a third-party directory, and noted that
the needed observation/forcing bundle is about 3.4 GB. A small analytical subset
does not imply a small upstream download. Time-series and attribute versions differ.
[Official deposit](https://zenodo.org/records/15529996),
[NCAR download page](https://ral.ucar.edu/dataset/camels-catchment-attributes-and-meteorology-large-sample-studies-dataset-downloads).

**Change:** resolve official identifiers, record exact archive names and versions,
download needed source bundles once, extract a fixed subset, and skip model-output
archives. Treat size as a planning estimate until actual intake.

**Verification needed:** actual download manifest, hashes, archive contents, and
measured resource use. No full download has been performed.

## R15 — Keep the infrastructure smaller than the investigation

**Type:** delivery/architecture risk. **Priority:** medium.
A universal abstraction, dozens of models, or mandatory heavy dependencies could
obscure the questions and make reproduction expensive.

**Change:** share provenance/splits/results/plotting; preserve explicit adapters
for distinct data semantics. Provide offline examples, specialized optional
dependencies, bounded tuning, and separate full-run release checks from fixture CI.

**Verification needed:** a working entry point, representative runtime/resource
measurements, and review of scope. Expensive methods need a question to justify them.

## R16 — The story must stay within the evidence

**Type:** interpretation and authorship risk. **Priority:** high before publication.
Generated metrics do not validate an interpretation. Agent agreement is not proof.
These public datasets do not by themselves establish realized business savings,
optimal inventory, avoided damage, or clinical benefit.

**Change:** distinguish measurements from scenario assumptions, source facts from
risks and observed defects, and human contributions from agent work. Show planned
versus completed work. Preserve critiques, disputes, and changes in the story.

**Verification needed:** independent review of exact headline claims and the
process narrative against source, execution, and review evidence. Do not invent
surprising outcomes or successful interventions before they occur.

## Current disposition

All sixteen findings have amended the plan. None is claimed as an independently
verified implementation remedy. Use the [register](README.md) for current status
and the [review protocol](../docs/REVIEW_PROTOCOL.md) for subsequent evidence.
