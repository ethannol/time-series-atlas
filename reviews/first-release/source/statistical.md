# First-release source intake — statistical review

Reviewer: `statistical_critic`, a separate AI agent that did not author the acquisition or study design.
Reviewed: 2026-10-30; inspection completed at approximately 16:17 UTC.
Baseline: `d7218096c7920e30da3ad722a3d1bffbede8fa4e`, freshly fetched by the primary agent at `2026-10-30T16:14:39Z`.
Scope: downloaded raw bytes, NOAA's embedded header, official NOAA/UCI notes, and bounded independent data inspection. No model was fitted; no forecast output or proposed implementation was reviewed.

## Verdict

**Source intake is sufficient to draft the study contracts, with the constraints below carried forward.** Two discrepancies between simplified source descriptions and actual records require explicit handling. These are observed source facts, not bugs found in project code. The verdict does not approve a loader, population selection, evaluation design, or model result.

## Evidence inspected

Independent SHA-256 calculations matched the acquisition manifest:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `data/raw/co2_mm_mlo.txt` | 59,678 | `0ce4e7749217b4af2cca8e0bdf263856ad59b0a2946d4e98c7b22ccfbff21cad` |
| `data/raw/electricity.zip` | 261,335,609 | `f6c4d0e0df12ecdb9ea008dd6eef3518adb52c559d04a9bac2e1b81dcfc8d4e1` |

`data/manifest.json` inspected SHA-256: `6d7a297fe89d6a653e52beae413ac3f352396ae0759a60d1e9016fcdd6ba8fd8`.

The NOAA header says the file was created on 2026-10-09. I parsed its eight fields with whitespace separation and inspected every monthly record. For electricity I inspected the ZIP directory and initial raw lines, then parsed the full timestamp column and six preselected customer columns (`MT_001`, `MT_010`, `MT_100`, `MT_200`, `MT_300`, `MT_370`) using semicolon delimiters and comma decimals. This is not an audit of every customer's measurements.

## Findings and constraints

### S-STAT-01 — NOAA quality flags do not follow a literal both-negative rule

**Classification:** actual source records differing from a simplistic interpretation of the header. **Priority:** high for quality-mask construction.

The file contains 823 consecutive unique months, from 1958-03 through 2026-09. The 194 months before NOAA's May 1974 portion have unavailable Scripps metadata; those negative metadata fields must not automatically be classified as interpolation. Among the later rows, two have negative standard deviation but zero uncertainty:

| Month | Monthly average | Days | Standard deviation | Uncertainty |
| --- | ---: | ---: | ---: | ---: |
| 1975-12 | 330.77 | -1 | -9.99 | 0.0 |
| 1984-04 | 347.37 | 2 | -9.99 | 0.0 |

The header discusses negative standard deviation and uncertainty as interpolation markers. Requiring **both** to be negative would miss these records. Use a period-aware, conservative quality flag that catches negative standard deviation **or** negative uncertainty in the NOAA portion. Preserve the original fields and describe this as source-quality interpretation, rather than asserting that the two rows' provenance was independently recovered. No monthly-average value was negative in this file.

**Required subsequent verification:** actual mask behavior on these rows, separation of Scripps unknown metadata, and declared treatment during fitting and scoring.

### S-STAT-02 — The electricity DST description has observed exceptions

**Classification:** actual source/documentation discrepancy. **Priority:** high for time-quality handling.

The provider describes zero readings for all customers in the spring transition hour. The downloaded sample does not always follow that uniformly:

| Nominal timestamp | MT_010 | MT_100 | MT_200 |
| --- | ---: | ---: | ---: |
| 2012-03-25 01:00 | 0.000 | 11.984 | 0.000 |
| 2012-03-25 01:15 | 0.000 | 11.984 | 0.000 |
| 2012-03-25 01:30 | 0.000 | 10.652 | 0.000 |
| 2012-03-25 01:45 | 0.000 | 9.987 | 0.000 |

Values above are rounded to three decimals for display. The same three customers were all zero at these four nominal times on 2014-03-30. Sampled autumn rows showed larger readings for some customers, consistent with—but not independently proving—the documented aggregation convention.

Identify transition quality periods from an explicit calendar policy, not an assumption that every meter will be zero. Do not automatically replace every zero or infer inactivity from one zero. Decide which target periods and lagged inputs are contaminated before fitting. A generic timezone localization cannot reconstruct observations the publisher combined.

**Required subsequent verification:** actual transition masks, treatment of lagged transition measurements, and score population with excluded periods stated explicitly.

### S-STAT-03 — The nominal grid needs an explicit target and interval convention

**Classification:** observed timestamp geometry plus an unresolved interpretation assumption. **Priority:** high for target construction.

The electricity archive contains `LD2011_2014.txt` (710,998,915 bytes) plus a macOS metadata directory/file. The data have 370 customer columns. The full timestamp vector has 140,256 unique rows, starts at `2011-01-01 00:15`, ends at `2015-01-01 00:00`, and advances in nominal 15-minute steps throughout. This supports an interval-end interpretation but does not itself prove the physical timestamp convention. State any interval assignment explicitly. In particular, careless midnight/day grouping can shift the last interval into the next day's target.

The provider labels measurements as kW and gives the quarter-hour conversion to kWh. Specify whether forecasts target average power or interval energy, keep nominal-grid DST limitations visible, and verify aggregation algebra. Hourly means and sums answer different questions.

**Required subsequent verification:** boundary examples at midnight and year end; unit tests based on the declared target; timestamps of inputs available at each issue time.

### S-STAT-04 — Customer eligibility changes the population being studied

**Classification:** observed activation patterns and prospective selection risk. **Priority:** high for cohort design.

In the six inspected columns there were no parsed missing or negative values. First positive readings occurred at 2011-01-01 00:15 for `MT_200` and `MT_300`, at 2012-01-01 00:15 for `MT_001`, `MT_010`, and `MT_100`, and at 2013-01-01 00:15 for `MT_370`. These observations agree with the warning that some leading zeros precede activation. They do not establish contractual activation dates or classify later zeros.

Freeze eligibility using permitted history. Describe known-customer forecasting separately from new-customer transfer. If a subset is selected for runtime, identify the rule and the resulting population; do not claim all 370 customers were evaluated. Avoid using later survival, future completeness, or eventual last activity to select earlier evaluation cases.

**Required subsequent verification:** selected IDs, training-period eligibility evidence, and unchanged test population across comparisons.

### S-STAT-05 — CO₂ is a revised, processed observational product

**Classification:** source-confirmed processing and provenance limitations. **Priority:** high for interpretation.

Use the monthly-average field rather than the supplied deseasonalized series. NOAA describes the latter's seasonal correction using neighboring years. The monthly average itself is already corrected to the center of the month; it is not untouched instrument output. The file also documents temporary Maunakea observations during the Mauna Loa interruption. Preserve that period in metadata and describe any exclusion/sensitivity policy before seeing forecast outcomes.

The snapshot extends beyond the intended 2025 study cutoff. Enforce the cutoff separately from acquisition. A present-day snapshot backtest does not recreate historical release vintages or real operational publication delays. Treat the series as a site-based atmospheric record, not automatically a global concentration estimate.

**Required subsequent verification:** target column/cutoff, issue-time assumptions, quality metadata, and honest revised-data wording in the report.

## Official references

- [NOAA data file and embedded notes](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt)
- [NOAA processing and interpretation notes](https://gml.noaa.gov/ccgg/trends/index.html)
- [UCI electricity documentation](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014)

These source-intake findings require later design and implementation evidence. No prior analytical finding is closed solely by this review.
