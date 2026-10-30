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
customers, quarterly-hour power readings aggregated to hourly mean kW under the
explicit nominal end-label convention. Original source bytes remain pinned but
the large ZIP is not in Git. Source timestamps are shifted back 15 minutes before
aggregation into start-labeled hours; no UTC reconstruction is claimed. Selection
uses only 2011/2012: some positive readings in 2011 and at least 350 positive-total
days in 2012; choose 24 evenly spaced ranks of 2012 mean power. This is a deliberate
scale-spanning panel of established customers, not a random representative sample.
No test-year forecast scores entered selection. Original 2011 zero values remain.

Changed provider bytes require explicit new versioning. The derived panel can be
recreated only from the pinned archive, package lock, and transformation code.
