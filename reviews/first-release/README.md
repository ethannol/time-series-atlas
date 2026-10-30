# First release: checkpoint record

Baseline fetched 2026-10-30T16:14:39Z: origin/main
`d7218096c7920e30da3ad722a3d1bffbede8fa4e`. Clean checkout; branch
`feat/first-studies`. Planning scaffold was published before implementation.

## Source intake

[Statistical review](source/statistical.md) and
[implementation review](source/implementation.md) inspected actual pinned files.
Both found source descriptions differed from observations. NOAA negative-standard-
deviation rows had zero uncertainty; UCI spring-DST zero handling was not uniform.
The adapter conservatively flags either negative NOAA metadata field, distinguishes
early Scripps unknown metadata, and identifies DST by calendar rather than values.
These are new observed source findings, not merely the initial prospective risks.

Source verdict: sufficient for design with explicit scope/quality conventions.
Code behavior is not yet approved. [Audit and source notes](../../reports/intake/README.md).

## Design review and freeze

[General](design/general.md), [statistical](design/statistical.md), and
[implementation](design/implementation.md) critics reviewed all three contracts
and verified their requested clarifications before any model fitting:

- CO₂ results cover December-origin January/December targets, not all months.
- Electricity peaks exceed a fixed training-year percentile; learned predictions
  share zero clipping with raw values preserved; Ridge penalties are equal per row.
- Synthetic initial condition, standard deviation, score recurrence, threshold
  comparison, shift units, and outcome denominators are explicit.

Design verdict: ready to freeze. Contracts will be committed before bounded
implementation trials and full runs. This does not verify numerical behavior.

## Implementation and results

Pending. No full model run or scientific conclusion is authorized by a design-only
review. Independent implementation review follows bounded tests/trials.
