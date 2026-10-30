# Initial data and implementation critique

Date: 2026-10-29. Reviewer: AI subagent `/root/implementation_critic`.
Scope: proposed seven-dataset collection, source documentation, reproducibility,
execution cost, implementation architecture, and staged delivery.
This record preserves the substantive final critique delivered to the primary
agent. It is not a tool transcript. No implementation, full downloads, or model
runs were reviewed. This file was saved after the original critique, without
claiming that its recommendations were implemented or verified.

---

The dataset selection is feasible. I would keep all seven collections, but tighten the plan in six places before building.

1. **Add a data-admission step before committing each study’s design.** A source page is not yet proof that the exact intended subset can be acquired, interpreted, and reproduced. For each dataset, resolve actual files, read provider notes, validate a small sample, record units/time semantics/quality flags, and estimate download and run costs. Then freeze the study contract: question, target, issue time, horizon, evaluation population, allowable inputs, and metrics. The question should arise naturally from the data; commercial value need not be invented.

2. **Correct two source assumptions immediately.**
   - **CO₂:** NOAA’s file already interpolates some missing months, combines early Scripps observations with later NOAA observations, and substitutes Maunakea observations during the 2022–23 disruption. Preserve those flags and provenance. Use the monthly-average field rather than NOAA’s already deseasonalized field for forecasting, and identify the exercise as a backtest on the currently published historical record, not a reconstruction of data available at each historical date. [Official file and notes](https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt).
   - **CAMELS:** Follow the official DOIs to the [NCAR Zenodo deposit](https://zenodo.org/records/15529996). The third-party directory’s `gdex.ucar.edu/datasets/d629001/` link resolves to an unrelated tropical-convection dataset. The needed observations/forcing archive is **3.4 GB**, even if only one meteorological product is used; all products are bundled. Download that archive once, extract the fixed subset, and skip the model-output archives. Record time-series version **1.2** and attributes version **2.0** separately rather than a single vague “CAMELS version.”

3. **Preserving hashes is necessary but insufficient for public reproduction.** If NOAA or EIA revises a file, a manifest can detect the change but cannot recover the old bytes. Provide:
   - Immutable, versioned source snapshots or redistribution-permitted excerpts where possible.
   - A `reproduce` path that requires the pinned bytes and refuses silent refreshes.
   - A separate `refresh` operation that creates a new dataset version and reports changes.
   - For files whose redistribution rights are unresolved, preserve local snapshots and describe the public reproducibility limit honestly.

   The three UCI datasets have straightforward attribution licences. MIT-BIH is also openly available under its stated licence. For CAMELS, the current landing page’s rendered licence field is blank; preserve provider terms and resolve redistribution before publishing a mirror. EIA generally permits reuse, but the oil-price notes identify Refinitiv as the source and EIA’s policy separately discusses protected third-party materials. That is a reason to verify mirroring rights—not a reason to reject the free dataset. [EIA reuse policy](https://www.eia.gov/about/copyrights_reuse.php), [oil-price source notes](https://www.eia.gov/dnav/pet/TblDefs/pet_pri_spt_tbldef2.asp).

4. **Use a small shared execution framework, not a universal time-series abstraction.** Share acquisition, manifests, split definitions, evaluation records, plotting style, and report generation. Keep dataset-specific semantics in explicit adapters. Electricity intervals, retail transaction events, daily basin measurements, and ECG waveforms should not be squeezed into a schema that loses their meaning. A run record should include:
   - Source commit and patch hash, dependency lock, seed, configuration.
   - Raw and processed-data hashes, selected series/records, exact split boundaries.
   - Predictions or detections, metrics, warnings, runtime, and peak memory.
   
   Store prediction-level evidence so a metric can be recomputed without refitting. Generate notebooks from scripts; avoid two independently maintained analysis implementations. Integrate with the existing portfolio’s result ledger/card format without requiring the portfolio package to run this repository.

5. **Make the first release runnable and bounded.** Preserve CO₂ and electricity as the first completed studies, but cap their initial model families and tuning budgets. Provide:
   - A small, offline quickstart.
   - The full published-study reproduction command.
   - Separate optional extras for volatility, ECG, Bayesian, and neural methods.
   
   First measure a representative run, then set documented budgets. Electricity has about **249 MB compressed / 678 MB text**, and its time labels encode daylight-saving adjustments; hourly conversion must specify whether the target is mean power or energy and cannot reconstruct an ordinary UTC series without addressing those adjustments. [UCI documentation](https://archive.ics.uci.edu/dataset/321/electricityloaddiagrams20112014). Neural and Bayesian examples should remain later additions, with dependency and compute costs justified by the question.

6. **Separate CI validation from rerunning every analysis.** Pull-request checks should use offline fixtures and test meaningful invariants: no future inputs, preserved units, correct interval aggregation, hash enforcement, reproducible split membership, and metric calculations. Full model runs should be explicit release checks using pinned data, bounded threads, and captured evidence. A provider outage or silent dataset revision should not become an ordinary unit-test failure. Do not use exact floating-point output equality across platforms as the scientific correctness criterion.

For the revised plan, I recommend **Phase 0: source validation and study contracts; Phase 1: two polished end-to-end studies; Phase 2: remaining datasets one complete study at a time; Phase 3: expensive advanced comparisons only where they answer an unresolved question**.

Where a study does discuss decisions, distinguish measured results from scenarios: the retail data do not establish unmet demand or stockout costs, electricity lacks procurement/capacity costs, and CAMELS supplies retrospective weather rather than archived forecast weather. These limits can make the case studies more interesting without forcing commercial claims.
