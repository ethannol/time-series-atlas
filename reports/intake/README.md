# Source intake — 2026-10-30

Actual downloads were inspected before model fitting. The [audit](audit.json)
records source hashes, dimensions, quality flags, selected customers, and snapshot
hashes. `transcript.json` is the captured initial intake output; no forecast scores
were calculated. See [data provenance and attribution](../../data/README.md).

Two source/documentation discrepancies changed the design:

- NOAA-era observations for December 1975 and April 1984 have negative standard
  deviation but zero uncertainty. Requiring both metadata fields to be negative
  would miss them. We conservatively mark either negative as **quality-suspect**,
  not as proof of how each observation was constructed. Early Scripps metadata
  have a separate unknown status.
- UCI's description of DST zeros is not uniform in actual customer readings.
  Independent reviewers found nonzero values within the documented spring
  transition window. We identify transition dates by calendar and do not infer
  their presence from an all-customer-zero rule. No physical UTC reconstruction
  is possible from the documentation alone.

The first/last electricity labels support an end-label convention, but the
provider does not explicitly specify interval endpoints. The convention is an
assumption, preserved in the audit and study design. Hourly targets are nominal
provider-clock mean power, not a reconstructed physical energy-settlement series.

Source intake does not validate model code. Independent reports are under
[the source checkpoint](../../reviews/first-release/source/).
