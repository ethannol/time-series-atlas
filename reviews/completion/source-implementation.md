# Completion source and evidence-framework review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Baseline supplied by the primary agent: freshly fetched `origin/main`
`bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`, fetched at 21:17:43Z;
working branch `feat/complete-atlas`.

Scope: official access/terms, bounded source samples, practical intake, and
preservation of earlier execution evidence while adding the remaining studies.
No model evaluation, fits, dependency installation, or implementation edits were
performed. Only this review record was authored. Remote inspection transferred
metadata, small headers, and approximately 3.3 MB of selected CAMELS ZIP ranges;
no full CAMELS or ECG archive was downloaded by this reviewer. Oil and air-quality
samples were read from the primary agent's existing downloads.

**Verdict:** the five remaining collections have free official acquisition paths.
CAMELS selective access is demonstrated, not merely proposed. This review permits
source intake to proceed; it does not approve a final cohort, study design,
adapter implementation, or full model run. Resolve the evidence-framework issue
below before claiming final collection-wide verification.

## C-I01 — Preserve historical source provenance when extending the code

Priority: high for collection-wide evidence validation. Status: `identified`;
primary agent accepted the proposed direction, implementation not yet reviewed.

The existing `source_snapshot()` hashes every source, test, and script file plus
the lock, manifest, audit, and study design. `validate_evidence.py` then compares
those historical source hashes to today's working-tree bytes. Adding a study or
changing shared infrastructure will make earlier records fail even when their
inputs and outputs remain intact. Rewriting old `source_files` to match new code
would erase the actual execution provenance.

Recommended minimal correction:

- Check each historical `source_files` map against Git blobs at that record's
  `source_commit`; fail if the revision or any recorded blob is unavailable or
  different. Independently check current retained outputs and input snapshots
  against their recorded hashes. Current tests/check evidence validates current
  implementation separately.
- Preserve original run records, acquisition manifest, and intake audit. Add a
  per-study manifest/audit and explicit input selection for new studies rather
  than mutating the first-release audit or requiring unrelated inputs for every
  command. Keep start/end source-stability checks and staged output promotion.
- Retain source revisions in reachable Git history and make CI fetch that history.
  The existing `b607f9f` execution revision is an ancestor of current main, verified
  using Git; a future squash/delete workflow must not silently lose new execution
  commits. Full history cannot retrieve an unreachable object by assumption.
- Replace the hard-coded three-study expected set with an explicit release
  registry that distinguishes planned from completed studies. Missing required
  evidence must still fail. At overall completion all eight must be required.
  Add focused tests for old valid source after an unrelated new edit, corrupt
  output, corrupt historical source hash, and missing expected study evidence.

An unchanged study need not be rerun just to update its recorded source SHA.
Material changes to its computation still require the relevant review and a new
execution record. Fresh-checkout reproduction should compare regenerated outputs
to the retained reference bytes, not only to newly generated self-hashes.

## CAMELS-US: official archive, selected access, and observed source caveats

The [official NCAR download page](https://ral.ucar.edu/dataset/camels-catchment-attributes-and-meteorology-large-sample-studies-dataset-downloads)
routes the time-series DOI to [Zenodo record 15529996](https://zenodo.org/records/15529996).
Its [API metadata](https://zenodo.org/api/records/15529996) identifies version 1.2,
open access, and `cc-by-4.0`; attribute files retain their separate v2.0 names.
[UCAR's data-repository terms](https://www.ucar.edu/terms-of-use/data) also state
CC BY 4.0 unless otherwise specified. Retained subsets should carry source/DOI,
license, and transformation attribution. Do not use the unrelated GDEX dataset
`d629001` as a CAMELS source; direct inspection showed it is a tropical-convection
weather archive.

The required [forcing and observed-flow ZIP](https://zenodo.org/api/records/15529996/files/basin_timeseries_v1p2_metForcing_obsFlow.zip/content)
is **3,406,626,583 bytes**, with provider MD5
`8e9a466710e8270b58f01d332a87184f`. It includes all three weather products,
streamflow, metadata, and documentation. The separate model-output ZIPs and
full-resolution shapefile are unnecessary for the planned question. All numeric
sizes here are API values, not independently recomputed whole-archive hashes.

### Selective download was tested

The content URL returned HTTP 206 with correct `Content-Range`. A 131,072-byte
tail request exposed 17,728 central-directory entries; the directory occupies
2,811,679 bytes beginning at offset 3,403,814,882. Reading it plus selected member
ranges allowed CRC-checked decompression of three readmes, gauge metadata, and
one catchment's flow/Daymet records without acquiring the full archive.

A small range-aware seekable reader or `remotezip` is feasible. Require HTTP 206,
exact response range/length, total-size consistency, bounded reads, and member
CRC; abort if the server returns a full body. Record the official archive URL,
record/version, provider checksum, member paths, sizes, CRCs, and independently
computed SHA-256 for every retained member. A range subset does **not** verify
the complete archive MD5. Do not label it as a full verified download. Pin and
retain permitted member bytes for later offline use.

For a compact cohort, retrieve all small gauge metadata first, predeclare a
selection rule based on geography/physical attributes and training-period
coverage, then retrieve only the corresponding streamflow and basin-mean Daymet
members. Avoid the elevation-band/HRU products unless the question needs them.
For sample gauge `01013500`, flow is 65,370 compressed / 402,240 uncompressed
bytes; basin-mean Daymet is 232,633 / 754,189 bytes. A modest cohort is inexpensive.
Record any deterministic fallback when a proposed gauge lacks training coverage;
do not choose basins by final forecast scores.

### C-I02 — Actual file semantics override convenient assumptions

Status: `identified`; carry into source audit/design and independently verify
the final loader. These discrepancies are observed, not hypothetical:

- Streamflow has six columns: gauge ID, year, month, day, flow in cubic feet per
  second, and QC. Its README says five while listing six. Missing values are
  `-999` with `M`; `A:e` identifies estimates and must remain distinguishable from
  `A`. The inspected gauge ends 2014 with missing values. Preserve the leading
  zero in its eight-character ID.
- The basin forcing README describes hour zero, but actual Daymet rows have
  `Hr=12`. These are daily aggregates; noon is not demonstrated release time.
  Model inputs must use an explicit daily cutoff and reporting assumption.
- The sample forcing header latitude is 46.84, whereas gauge metadata lists
  47.23739. Retain both source fields without labelling them interchangeable
  gauge coordinates. Forcing-header area is in square metres; gauge metadata
  area is square kilometres. State the chosen area if converting discharge.

The [NCAR archive description](https://zenodo.org/records/15529996) calls the
weather inputs retrospective forcings. Restrict the warning experiment to past
observations under a declared availability assumption; observed target-day
rainfall is not a weather forecast. Flow-derived catchment signatures and
whole-record climate summaries must not become leakage into cohort selection or
predictors. The current story already identifies this risk; the forthcoming
contract must implement it concretely.

Inspected CAMELS member hashes (paths relative to `basin_dataset_public_v1p2/`):

```text
b8697d0f12d1ca9f7755c5b620fce940687b78f2b32c830c0150d7dc4a933b7f  readme_FIRST.txt
a2bf7ba2050bc3602064ae99c5e63da62ddcb364c7e7662c067ad5454558e5a5  readme_basin_mean_forcing.txt
2e616da566af66821d94c0ee192d681e6343f01969cbd330f75402e2af6a85a6  readme_streamflow.txt
71694637f4a6e8407d6e3a54dea04818881094d550241590a2f422ca7235a1fa  basin_metadata/gauge_information.txt
bce4b441f9bdf8b22438d9106d9b049f5bbd57f6bd455330ee9dbf3941b8e12a  usgs_streamflow/01/01013500_streamflow_qc.txt
2dd0c986e2ae6016cfbbfc907a1c32789fc4c04f5ee0a002373712f79ab6592d  basin_mean_forcing/daymet/01/01013500_lump_cida_forcing_leap.txt
```

## MIT-BIH: bounded acquisition and person/lead integrity

The [versioned PhysioNet page](https://physionet.org/content/mitdb/1.0.0/) supplies
an open [ZIP download](https://physionet.org/content/mitdb/get-zip/1.0.0/), whose
HEAD response reports **77,030,320 bytes** (the page displays 73.5 MB; total
uncompressed size is displayed as 104.3 MB). The parent is acquiring it.
Alternatively, the [official file directory](https://physionet.org/files/mitdb/1.0.0/)
serves each `{record}.dat`, `.hea`, and `.atr` directly: each waveform is
1,950,000 bytes, and headers/annotations are small. Preserve `RECORDS` and
`SHA256SUMS.txt`; verify selected files against the provider list and record
independent hashes. Do not confuse backup annotations with current `.atr` files.

The [dataset license](https://physionet.org/content/mitdb/view-license/1.0.0/) is
ODC Attribution 1.0. Keep the notice/license URI with redistributed data and
attribute the database in derived reports. This does not turn the dataset into
the repository's code license. The provider permits open access; no credentialed
clinical-data workflow is required for this collection.

### C-I03 — Keep people and lead identity explicit

Status: `identified`; already acknowledged in the project story, still requires
verification against the eventual implementation.

[PhysioNet's acquisition notes](https://physionet.org/physiobank/database/html/mitdbdir/intro.htm)
describe 48 records from 47 people, with 201 and 202 belonging to the same person;
they must remain in one split/group. The collection deliberately includes
unusual rhythms, so study prevalence is not population prevalence. Paced records
102, 104, 107, and 217 require an explicit inclusion/label policy.

Downloaded headers independently confirm 360 Hz, 650,000 samples, two channels,
and format 212. Record 114 has V5 first and MLII second; 100 has MLII first.
Select a lead by header name, not column number. The 202 header explicitly links
its source tape to 201. These four header hashes matched the provider checksum
list. The list contains 48 record names.

Use a maintained WFDB reader in a pinned optional intake dependency rather than
reimplementing packed waveform/annotation formats. Preserve record/person IDs,
annotation sample index and symbol, sampling rate, lead identity, gain/baseline,
and boundary exclusions in a compact derived input. Exclude non-beat annotations
according to a frozen mapping. A window centered on the expert beat location
defines annotated-beat classification, not end-to-end beat detection. Freeze any
post-beat lookahead and RR features accordingly. Training-only preprocessing and
person-grouped evaluation are necessary; waveform extraction may be shared
provided it uses no global label-informed fitting.

```text
60ebc904c7bf3e04d142638d3fd5c903e8dc9f10f1ea3264e07926aa089ee75e  100.hea
830ba89cebf60945db0c78332e3cc6c64acbe218f6f16594660d4f17423ee889  114.hea
dba34d6252879af28c1d10cde200989a4f6507d98df4395f5cba5f81af5b7e5a  201.hea
6822216d1bc51f7014637c53e543cdc3863fea4ee3fec3aa99fb0762aece0cba  202.hea
b61158a96d5f2ca80edfb354a9a66a6324836c390a84e1966dcee2b907d6be43  SHA256SUMS.txt
fcdca7ead9fc93f612f7e025029241cb6429ba2fcd05327b661bdc6b26fbcb57  RECORDS
```

## Air quality, oil, and retail

**C-I04 — Select the full air-quality payload explicitly.** Status: `identified`.
The [UCI source](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)
is CC BY 4.0. Its [download](https://archive.ics.uci.edu/static/public/501/beijing%2Bmulti%2Bsite%2Bair%2Bquality%2Bdata.zip)
is 8,192,212 bytes locally. It contains a nested `PRSA2017_Data_20130301-20170228.zip`
with 12 station CSVs (32,508,303 uncompressed bytes), plus small `data.csv` and
`test.csv` files. Use the full nested station files, not those small companions.
The inspected Aotizhongxin file has 35,064 unique hourly rows from March 2013 to
February 2017 and 925 missing PM2.5 values. Retain actual missingness separately
from simulated outages, station identity, and native calendar timestamps. Source
weather is matched to nearby meteorological stations; contemporaneous reporting
availability is an experiment assumption. Score hidden observations only where
truth exists, and do not allow the hidden station's PM values back through a
derived feature or an interpolation that sees later times.

**C-I05 — Preserve the negative WTI observation and observation calendar.** Status:
`identified`. Official [WTI](https://www.eia.gov/dnav/pet/hist/RWTCD.htm) and
[Brent](https://www.eia.gov/dnav/pet/hist/RBRTED.htm) pages link downloadable
[WTI XLS](https://www.eia.gov/dnav/pet/hist_xls/RWTCd.xls) and
[Brent XLS](https://www.eia.gov/dnav/pet/hist_xls/RBRTEd.xls), respectively
471,552 and 452,608 bytes. Both parse from `Data 1` after two initial rows.
The inspected WTI history contains **-36.98 USD/barrel on 2020-04-20**. Ordinary
log returns are invalid for that episode. Freeze a valid signed transformation
such as dollar changes and retain the stress episode; do not silently discard
it. Gaps are not zero returns. Define next-observation versus next-calendar-day
horizons, and intersect calendars before related-series comparisons. Both current
files end 2026-10-27; the approved study intends an end-2025 snapshot.
[EIA's reuse policy](https://www.eia.gov/about/copyrights_reuse.php) permits use and
distribution of its data with acknowledgement while distinguishing separately
protected third-party material. Preserve the source/date notice and workbook
metadata; do not imply these are tradable futures or real-time vintages.

**Retail access is straightforward; detailed intake remains a separate review.**
[UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
provides its two-year workbook under CC BY 4.0 and displays 43.5 MB. The primary
agent is handling its actual intake. Cancellation handling, duplicate records,
non-product lines, incomplete terminal weeks, and training-only item selection
must be explicit. No transactions is not demonstrated unmet demand, stockout
status, or continuous product availability. Keep realized sales as the supported
target. A compact product/day panel can omit customer identifiers without losing
the selected forecasting question.

## Inspected local hashes

These identify the files read during this review, before the proposed evidence
framework changes. Later changes require their own independent verification.

```text
e0b67ed6819d4a8eb36b844cc475697499132ce24dcf1113c1f2e8573212c18c  AGENTS.md
f0ea1313c5e9c5bc61a07209bf216e26095f495a560808e63f1d3b6d383e65fc  PLAN.md
675275bf09409edec4459817e0652743b0e2b745d9723c74585062d246253f1f  docs/REVIEW_PROTOCOL.md
1bdc4e6ce523986d004678f7ed876fae57a258f6ae9eebdace225e5aa6ea3c3a  src/tsatlas/common.py
20c2b1b2b1be74dade626c8b54d18f3db5691ec3e82b94416fa4bd73d65a1fd5  src/tsatlas/data.py
2fed5022d7d69fb0878b3b932620883f98aab1edf581d91b4f20979ffeb34cd3  src/tsatlas/cli.py
d8f74e00e04c2c986956f1cbc538dfb431194ccb9002b20ad6366718c553b47f  scripts/validate_evidence.py
d111d6606fd523638a661e5f575c6c33b450d4c4271d00d71807dbdfe318b0e8  scripts/check.py
51e6d8e1921f0b9908cbcde151a28ff8bb8a2bef3ac4f197c786d46d5653c018  tests/test_evidence.py
6d7a297fe89d6a653e52beae413ac3f352396ae0759a60d1e9016fcdd6ba8fd8  data/manifest.json
2b44293c453ecd008e8c7cf76e87a3f38a592afdd14870cb54b408309b020198  reports/intake/audit.json
b04da438b2f331ac0ffd45aebdfec0d20d2367feb5f6948c4b1f7ce1191e33c4  data/raw/air-quality.zip
1f4c7c6c80c4ef6eb9e7b6c95e87c8df6439e3fb6ecccea72e9135bb37acf048  data/raw/wti.xls
c7c1e1eeb321fa5982f74747886963b35bd2df3c2f63960271c353421d5830ca  data/raw/brent.xls
```
