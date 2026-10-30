# River flow: the process story

**Question:** How much warning of high flow can recent rainfall and flow provide across different catchment types?

**Data:** [CAMELS-US](https://ncar.github.io/hydrology/datasets/); daily streamflow and weather for US catchments, with the analytical subset still to be fixed.

**Status:** design only. This is a record of decisions already made and work still
to do, not a report of results. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected paired weather and river-flow records because rivers respond to rainfall with different delays. Comparing catchments could show when recent observations give useful advance warning.

## 2026-10-29 — Challenge the first plan

The reviewers found that some supplied catchment descriptions already summarize the river flow we might predict. They also pointed out that observed future rainfall is not information available to a forecaster today.

## 2026-10-29 — Change the design before fitting

We will trace where each input comes from and what would be known when a warning is issued. Any later experiment on ungauged rivers must exclude descriptors calculated from their flow. The study must distinguish advance warning from reconstructing an event after its weather is known.

Technical evidence and outstanding checks: [R04–R05](../../reviews/01-design-review.md#r04--some-catchment-descriptors-already-contain-the-outcome) and [R14](../../reviews/01-design-review.md#r14--resolve-actual-camels-files-and-versions).

## Next, not yet done

Acquire and audit the intended source files, choose a fixed catchment subset, and define warning horizons and reporting assumptions. No high-flow performance or transfer result exists yet.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).

