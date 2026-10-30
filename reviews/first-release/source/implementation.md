# Independent source intake review: CO₂ and electricity

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: official documentation, access and reuse terms, downloaded raw bytes,
bounded numerical samples, and complete timestamp/shape scans. No project loader,
model, forecast score, or proposed remedy was verified. The reviewer did not
download or author these source files or implement their adapters.

Baseline: `d7218096c7920e30da3ad722a3d1bffbede8fa4e`, matching observed HEAD.
The acquisition manifest records the primary agent's fresh-main fetch at
`2026-10-30T16:14:39Z`. Its download completion fields are explicitly inferred
from file modification times, not represented as server-certified timestamps.

**Source-intake verdict:** both downloads are usable for the proposed studies and
their hashes match the acquisition manifest. Proceed to frozen design with the
constraints below. Do not begin affected full model runs until the time/quality
semantics are implemented and independently checked. Two discrepancies between
provider prose and actual values were observed; these are source-intake findings,
not demonstrated defects in project code.

## Independently checked evidence

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `data/raw/co2_mm_mlo.txt` | 59,678 | `0ce4e7749217b4af2cca8e0bdf263856ad59b0a2946d4e98c7b22ccfbff21cad` |
| `data/raw/electricity.zip` | 261,335,609 | `f6c4d0e0df12ecdb9ea008dd6eef3518adb52c559d04a9bac2e1b81dcfc8d4e1` |
| `data/manifest.json` | — | `6d7a297fe89d6a653e52beae413ac3f352396ae0759a60d1e9016fcdd6ba8fd8` |
| `AGENTS.md` | — | `f02fa27d7e43e6ab190467893aed717f62ce6a5918ffae0789ad768b76f78b46` |

The raw files are intentionally outside committed source. These hashes identify
the exact inspected bytes; the public reproduction path still needs a retained
snapshot or permitted versioned subset rather than reliance on a mutable URL.

### NOAA sample and full small-file audit

The local file has 823 rows, each with eight fields, from March 1958 through
September 2026. All month keys are consecutive and unique; monthly averages are
positive. There are 194 rows before May 1974 and 629 from May 1974 onward. The
header records file creation on October 9, 2026. Source publication time and
local retrieval time are different provenance fields.

Two NOAA-era rows contain negative standard-deviation metadata:

| Month | Monthly average | Number of days | Standard deviation | Uncertainty |
| --- | ---: | ---: | ---: | ---: |
| 1975-12 | 330.77 | -1 | -9.99 | 0.00 |
| 1984-04 | 347.37 | 2 | -9.99 | 0.00 |

**SI01 — High: preserve the discrepancy between flag prose and raw values.**
The file header describes negative standard deviation and uncertainty as
indicators of interpolated NOAA months, but these rows have zero uncertainty.
A parser requiring both fields to be negative would miss them. Conversely,
negative metadata in the early Scripps period indicates unavailable metadata,
not proof every early month was interpolated. Preserve the raw fields and use
an explicitly named quality/suspect flag without claiming certainty beyond the
source. Freeze whether these months are excluded from scoring and how a
sensitivity analysis handles them. Do not interpret zero uncertainty as exact
measurement certainty. Status: `identified`; adapter behavior not reviewed.

**SI02 — High: retain processing and site provenance.** The monthly-average
column is already a provider-processed quantity; do not call it an unprocessed
measurement. The header explains monthly centering, early Scripps provenance,
and Maunakea substitution from December 2022 through July 4, 2023. The July
monthly record cannot simply be labelled wholly Maunakea or wholly Mauna Loa.
Use month identifiers rather than treating the decimal-year field as an exact
observation timestamp, retain source-period/site flags, and use the monthly
average rather than the provider's deseasonalized field as the primary target.
Status: `identified`; study input policy still needs a frozen design.

These source facts come from the [official file header](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt).
The [change log](https://gml.noaa.gov/ccgg/trends/trends_log.html) also records
historical revisions, a file-format change, and calibration-scale changes.
Consequently, this snapshot supports revised-data backtests, not an assertion
that every historical forecast used the values available at the time.

### Electricity sample and full timestamp audit

The archive contains `LD2011_2014.txt` (710,998,915 bytes), a `__MACOSX/`
directory, and a 1,080-byte resource-fork file. Only the named text member is a
data input. The quoted semicolon-separated header has 371 fields: a timestamp
and 370 customer columns. Values use decimal commas.

A streamed scan found 140,256 data rows. Labels begin at
`2011-01-01 00:15:00` and end at `2015-01-01 00:00:00`; every adjacent label is
exactly 15 minutes apart. This checks the complete index, not numerical validity
of every customer value. Numerical inspection was limited to selected clock-change
times and the first/last rows; a full missing/nonfinite/value audit remains the
adapter's responsibility.

Selected rows around the documented spring change:

| Raw label | Customers equal to zero | Sum across customer values, kW |
| --- | ---: | ---: |
| 2011-03-27 00:45 | 211 | 75,109.578 |
| 2011-03-27 01:00 | 214 | 73,186.043 |
| 2012-03-25 00:45 | 50 | 129,262.659 |
| 2012-03-25 01:00 | 251 | 4,398.907 |
| 2013-03-31 00:45 | 36 | 133,956.382 |
| 2013-03-31 01:00 | 242 | 4,443.946 |
| 2014-03-30 00:45 | 4 | 137,727.110 |
| 2014-03-30 01:00 | 253 | 342.596 |

These sums describe raw records; they are not estimates of physical energy
during the affected intervals. October samples in 2012–2014 show aggregate values
at 01:00–01:45 roughly twice nearby values, consistent with the documented
combining of repeated hours. This visual numerical consistency does not establish
the exact treatment of every customer or year.

**SI03 — High: the documented spring convention is not uniform in the bytes.**
UCI says the affected hour is zero for all points, but the inspected rows are
not universally zero; 2011 also lacks the conspicuous aggregate collapse seen
in the later years. Do not detect clock changes solely by an all-customers-zero
predicate or claim a uniformly applied correction. Identify affected periods
from the documented calendar convention, retain quality masks, and declare
whether affected targets and lag/rolling-feature windows are excluded or treated
in a separate sensitivity analysis. Do not silently repair a particular customer
by assuming its zero or nonzero value is correct. Status: `identified`.

**SI04 — High: freeze the target and timestamp convention.**
The start/end labels are consistent with interval-end labels, but the provider
notes reviewed here do not explicitly define that convention. If adopting it,
identify it as a documented analysis convention supported by the endpoints.
For ordinary hours, mean power is the mean of four quarter-hour kW readings;
energy is their sum divided by four. Aggregation bins, midnight ownership, issue
time, and target labels must agree. The source is an adjusted 96-slots-per-day
Portuguese clock index, not a recoverable ordinary UTC sequence. Blind timezone
localization or calendar-date grouping risks changing the target or leaking an
interval across a forecast boundary. Status: `identified`.

**SI05 — High: customer activity is not established by every zero.**
Keep pre-activation zeros distinct from later observed zero demand. Freeze an
eligibility rule using training history; do not use eventual last activity or
future completeness to select the evaluation cohort. Status: `identified`;
the complete activity audit has not yet been reviewed.

Provider facts and attribution are in the [UCI dataset record](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014).

## Access, attribution, and reproducibility disposition

- **Electricity:** the official UCI record identifies CC BY 4.0. The licence
  permits sharing and adaptation with its attribution conditions. Retain the
  dataset creator/citation, DOI, licence link, and descriptions of changes such
  as aggregation, masking, and subsetting. A reproducible attributed subset can
  be published without placing the large text file in Git history.
  [Licence](https://creativecommons.org/licenses/by/4.0/).
- **CO₂:** GML's file describes public availability and requests citation. Its
  [reuse page](https://gml.noaa.gov/about/disclaimer.html) permits use subject to
  the stated attribution/representation conditions. Preserve the original
  header and both NOAA/Scripps credit, distinguish transformed project outputs
  from official provider material, and do not put third-party observations under
  the repository's code licence. The frozen source bytes should remain identifiable.
- **SI06 — Medium before publication:** record how a fresh checkout obtains the
  exact pinned bytes or a versioned derived subset. Upstream hash verification
  alone cannot recover a replaced file. Preserve download and processing hashes,
  archive-member names, record selection, and attribution. Status: `identified`;
  no public snapshot or fresh-checkout reproduction was tested here.

## Verification still required before affected full runs

The next design/implementation review must inspect actual predicates and example
rows for NOAA quality/source flags; electricity interval bins and DST masks;
training-only eligibility; schema/nonfinite-value audits; and a timestamp trace
from raw observation through one prediction's inputs and target. Source intake
does not verify these future behaviors. A record of an accepted bounded source
limitation is legitimate; claiming the raw ambiguity has been repaired is not.

## Audit method

The reviewer independently recomputed SHA-256 for both raw downloads, read the
NOAA header and every small-file row with Python's standard library, and streamed
the named electricity ZIP member using `zipfile` and `io.TextIOWrapper`. Every
electricity timestamp was checked for a 15-minute increment; only selected
clock-change rows were parsed numerically with `csv.reader` and decimal-comma
conversion. No project loader was called and no model was fitted. All audit
processes completed; no background process was left running.
