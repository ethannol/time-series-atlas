# Data snapshots and attribution

The committed snapshots let the first studies run offline against fixed bytes.
`manifest.json` pins original downloads; `reports/intake/audit.json` pins the
analysis snapshots. `atlas fetch` refuses revised upstream bytes; `atlas intake`
rebuilds the panel from the original archive. Refresh is deliberately not an
implicit fallback: a new source version requires a new manifest and review.

## CO₂

Source: [NOAA Global Monitoring Laboratory](https://gml.noaa.gov/ccgg/trends/data.html),
monthly Mauna Loa series, downloaded 2026-10-30. Credit NOAA GML/Xin Lan and the
Scripps Institution of Oceanography/C. David Keeling for the early observations
identified in the retained file header. The full original header is preserved.
[NOAA reuse statement](https://gml.noaa.gov/about/disclaimer.html).
No NOAA endorsement is implied. The repository's eventual code licence does not
relicense provider observations. This is a revised historical series, not a
collection of historical release vintages. Analysis excludes the early Scripps
period and observations after December 2025.

## Electricity

Trindade, A. (2015). ElectricityLoadDiagrams20112014. UCI Machine Learning
Repository. [DOI](https://doi.org/10.24432/C58C86).
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
[Provider documentation](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014).

The committed file is a **modified subset**, not the original archive: 24 selected
customers, quarter-hour power readings aggregated to hourly mean kW under the
explicit nominal end-label convention. Original source bytes remain pinned but
the large ZIP is not in Git. Source timestamps are shifted back 15 minutes before
aggregation into start-labeled hours; no UTC reconstruction is claimed. Selection
uses only 2011/2012: some positive readings in 2011 and at least 350 positive-total
days in 2012; choose 24 evenly spaced ranks of 2012 mean power. This is a deliberate
scale-spanning panel of established customers, not a random representative sample.
No test-year forecast scores entered selection. Original 2011 zero values remain.

Changed provider bytes require explicit new versioning. The derived panel can be
recreated only from the pinned archive, package lock, and transformation code.

## Retail

Daqing Chen (2012), [Online Retail II, UCI](https://archive.ics.uci.edu/dataset/502/online+retail+ii),
[DOI 10.24432/C5CG6D](https://doi.org/10.24432/C5CG6D),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
The modified snapshot contains daily gross recorded UK merchandise sales for
24 products selected using 2010 only. It is not latent demand or an inventory
record. The workbook's annual sheets overlap: the complete 22,523-row multiset
for December 1–9, 2010 is duplicated. We use the first sheet before December 1
and the second thereafter. Within-sheet repeated rows remain because their
meaning is unknown. Cancellations, nonpositive quantities/prices and nonmerchandise
codes are excluded; missing customer IDs are retained. The audit records every
filter and the training-only sparse-product cohort.
[Raw manifest](manifests/retail.json) · [Intake audit](../reports/intake/retail.json).

## Oil: free access, with a public archival limitation

[EIA WTI spot prices](https://www.eia.gov/dnav/pet/hist/RWTCd.htm) and
[EIA Brent spot prices](https://www.eia.gov/dnav/pet/hist/RBRTEd.htm), daily dollars
per barrel, downloaded October 30, 2026; analysis ends December 31, 2025.
The [series definitions](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp)
identify Refinitiv as the underlying source. EIA's
[reuse policy](https://www.eia.gov/about/copyrights_reuse.php) contains third-party
exceptions. Free access does not establish unrestricted redistribution rights.

Accordingly, price workbooks, the normalized price snapshot, and full realized
outcome series are **fetch-only and excluded from Git**. Published artifacts
contain model parameters, forecasts and aggregate evaluation, with private
outcome hashes. Exact local reproduction needs `uv run atlas fetch oil` before
`uv run atlas oil` or `uv run atlas all`. The acquisition helper accepts later
workbook additions only if normalization through 2025 reproduces the originally
pinned snapshot hash. Historical revisions fail explicitly. We do not guarantee
future recovery of unchanged source bytes from the public endpoint.

Each series retains its own observed dates; no weekend filling or forced shared
calendar is used. The observed negative WTI level makes a universal log-price
transform invalid. Targets are next-observation dollar changes, with long gaps
shown separately. [Raw manifest](manifests/oil.json) ·
[Intake and private snapshot hash](../reports/intake/oil.json).

## River flow

Newman and colleagues, [CAMELS-US time series version 1.2](https://zenodo.org/records/15529996),
[DOI 10.5065/D6MW2F4D](https://doi.org/10.5065/D6MW2F4D), CC BY 4.0.
The source documentation cites Newman et al. (2015), *Development of a large-sample
watershed-scale hydrometeorological dataset for the contiguous USA*.
Credit NCAR, USGS observed streamflow, and the Daymet basin forcing product.
This is the time-series product, not the separately versioned CAMELS attributes.

The modified daily snapshot contains 17 known gauges for 1980–2014. Selection
uses geographic HUC group and approved training-period flow coverage; no HUC09
candidate met the rule. Only nonnegative flow with QC exactly `A` is approved;
`A:e`, missing sentinels and absent rows remain distinguishable. Weather column
names and units are preserved. Forcing-header area/latitude differ in meaning
from gauge metadata; the model uses the documented fields explicitly. `Hr=12`
is not proof of publication time. No outcome-derived full-period signature is
used as a predictor.

Acquisition read ZIP ranges and verified CRC plus SHA-256 for 114 selected
members, transferring 11,791,230 bytes. **The entire 3.4 GB archive was neither
downloaded nor independently checksum-verified.** Its provider MD5 is metadata,
not our verification claim. The range client rejects a full-file fallback and
checks pinned member hashes before replacing cached inputs.
[Member/version manifest](manifests/river-flow.json) ·
[Intake audit](../reports/intake/river-flow.json).

## Air quality

Chen, S. (Song Chen, 2017), [Beijing Multi-Site Air Quality, UCI](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data),
[DOI 10.24432/C5RK5G](https://doi.org/10.24432/C5RK5G), CC BY 4.0.
The modified snapshot retains hourly PM2.5 (µg/m³) at twelve stations,
March 2013–February 2017. Missing readings remain missing. The adapter uses the
full nested twelve-station archive, not the unrelated small CSV examples in
the outer ZIP. Source calendar hours are used as provided.

Synthetic contiguous local outages retain real same-hour peer measurements.
This is reconstruction during an outage under an explicit peer-arrival assumption,
not forecasting future pollution. Hidden local observations are used only for
scoring where they truly exist. The high-pollution label is a training-derived
quantile, not a health or regulatory threshold.
[Raw manifest](manifests/air-quality.json) · [Intake audit](../reports/intake/air-quality.json).

## ECG

Contains information from Moody and Mark (2005),
[MIT-BIH Arrhythmia Database v1.0.0](https://physionet.org/content/mitdb/1.0.0/),
[DOI 10.13026/C2F305](https://doi.org/10.13026/C2F305), made available under the
[Open Data Commons Attribution License v1.0](https://opendatacommons.org/licenses/by/1-0/).
The snapshot and predictions are modified extracts; the source database and
its licence are separate from this repository's code.

The provider's checksums were verified for all current signal/header/annotation
members used. The adapter selects MLII by name (record 114 reverses channel order),
excludes four paced recordings, maps the declared beat symbols to N/S/V/F groups,
and keeps records 201/202 together as one person. It extracts 0.5-second windows
around expert annotation centers, resamples 360 Hz to 120 Hz with a polyphase
filter, and records previous annotated RR. The retained 100,662 beats come from
44 records and 43 people. Missing prior RR and waveform-boundary exclusions are
separately counted. This is classification given expert locations; the N group
is not a healthy-person diagnosis. [Raw manifest](manifests/ecg.json) ·
[Intake audit](../reports/intake/ecg.json) · [Frozen person folds](../studies/ecg/folds.json).

## Generated controls and reproducibility scope

Synthetic change-detection streams and irregular-sampling frequency experiments
are generated by the committed code with declared seeds. They need no external
data licence. They reveal specific failure modes under known truth, not measured
field performance. Their protocols and run records retain all assumptions.

All source collections are free to access; only oil lacks a mirrored analysis
snapshot. `atlas verify` checks every locally present pinned snapshot and explicitly
lists absent fetch-only inputs as **not verified**. For original CO₂/electricity
archives use `atlas fetch` then `atlas intake`. For each later source use
`atlas fetch <slug>` then `atlas intake <slug>`; acquisition remains separate from
analysis. Exact intake reproduction requires the pinned original bytes, locked
software and transformation code. Revised upstream history requires an explicit
new version and review, never a silent refresh.
