# Review findings and evidence status

**Verification is scoped to work actually performed.** All eight investigations
now have executed evidence (nine run units). The
[full gate matrix](completion/README.md) links source, design, pre-run,
results and presentation checks. Final reproduction and publication are separate
gates; their current state is explicit there. The
[original critique](01-design-review.md) and [status history](HISTORY.md) remain
unchanged historical records.

## Fresh dedicated study critiques after publication

At Ethan's request, each investigation received a new independent agent reviewing
its implementation, findings and presentation from the published baseline.
[Per-study verdicts, evidence and resolution status](study-critiques-20261030/README.md)
record this round. Later qualifications reopen the affected claims; they do not
erase the earlier checks or imply that every optional extension is a defect.

## Original findings, reconciled to actual scope

| ID | Finding | Current resolution and evidence | Boundary retained |
| --- | --- | --- | --- |
| R01 | Methods preceded questions; scope could sprawl | Every run has a frozen contract; [question/method guide](../docs/METHODS.md) and [gate matrix](completion/README.md) | Conditional advanced methods are not performed or claimed |
| R02 | CO₂ interpolation and mixed provenance | [Source audit, sensitivity and results](first-release/README.md) | Revised hindcasts; sensitivity does not erase all provenance effects |
| R03 | Electricity zeros and interval/DST conventions | [Unit/clock/cohort checks](first-release/README.md) | Nominal clock, not verified UTC reconstruction; selected established customers |
| R04 | Some river attributes summarize the target | [Known-gauge feature audit](completion/river-flow-implementation-data.md) | No full-period outcome signatures; ungauged transfer was not evaluated |
| R05 | Future observed weather is not available input | [Origin and split audit](completion/river-flow-results-statistical.md) | Past daily weather only; reporting latency assumed, not measured |
| R06 | Recorded sales are not unconstrained demand | [Target, filters and overlap verification](completion/retail-implementation-data.md) | Gross sales only; no inventory/stockout or unmet-demand inference |
| R07 | Metrics can hide sparse-series failure or bad intervals | [Retail score audit](completion/retail-results-statistical.md), [CO₂ interval evidence](../reports/results/co2/REPORT.md) | Retail is point forecasting; electricity has no intervals; no universal scoring winner |
| R08 | Isolated masks do not represent station outages | [Block, coverage and event audit](completion/air-quality-results-data.md) | One station at a time, same-hour peers; no operational uptime claim |
| R09 | Record splits can mix people | [ECG person/fold and prediction audit](completion/ecg-results-data.md) | Expert-centered classification, so automatic detection tolerance is not applicable |
| R10 | Artifacts complicate physiological spectral claims | [ECG scope](../reports/results/ecg/REPORT.md), [synthetic sampling audit](completion/spectral-results-statistical.md) | Sampling control completed; no physiological rhythm claim; aliases remain ambiguous |
| R11 | Oil transformations and relationships need scrutiny | [Negative values, calendars, separate task scores](completion/oil-results-statistical.md) | Dollar changes; direction and variance losses not compared in magnitude; cointegration not performed |
| R12 | Availability, preprocessing and selection can leak | [Per-study technical gates](completion/README.md), including river origin correction | Final outputs were not used to tune models; different tasks retain different information assumptions |
| R13 | Hashes cannot recover unavailable inputs | [Source credits and acquisition](../data/README.md); reproduction gate in [matrix](completion/README.md) | Oil is fetch-only with an accepted future archival limitation; no unrestricted third-party reuse claim |
| R14 | CAMELS versions, paths and size need explicit handling | [Version/member manifest](../data/manifests/river-flow.json) and [source recheck](completion/design2-implementation.md) | CRC/SHA for selected members; full archive checksum not independently verified |
| R15 | Framework/compute can obscure the study | Bounded sequential execution, locked package, per-run measured resources; [author response](completion/RESPONSE.md) | Specialized dependencies installed together, not optional groups; full-suite measurement remains separately recorded |
| R16 | Agent agreement and attractive claims are not proof | [Independent results and publication gates](completion/README.md) | Final-scope publication review remains required; AI review is not human validation |

## What actually went wrong later

Initial risks are not retrospectively labeled as implemented mistakes. These
observed findings arose during intake, coding, communication or delivery.

| Type and issue | Response and independent evidence |
| --- | --- |
| Source discrepancy: NOAA quality flags and electricity clock-change values differ from descriptions | [Conservative handling and limits](first-release/README.md#source-intake) |
| Code defects: missing predictions and array broadcasting could distort scores | [Pre-run scoring repairs](first-release/implementation/statistical.md) |
| Verification defects: changing source or missing expected studies could pass | [Source/output guards](first-release/implementation/implementation.md), [expected-record checks](first-release/results/implementation.md) |
| Publication defect RI04: links pinned to a commit lacking the new table | [Committed-output rebuild and recheck](first-release/results/implementation.md) |
| Execution failure: agent stopped after three studies and implied completion | [User correction and explicit full-scope safeguard](../STORY.md), [required final audit](../AGENTS.md) |
| Scope omission: synthetic frequency control missing from completion checklist | [General critic finding](completion/general.md), [executed control](../reports/results/spectral/REPORT.md) |
| Source facts: duplicated retail annual overlap, negative WTI level, third-party oil attribution | [Independent source/design checks](completion/design-implementation.md) |
| Source/audit defects: river weather columns and missing QC handling; ECG exclusion label conflated two causes | [Corrected snapshot and audit reconstruction](completion/design2-implementation.md) |
| Missed design risk: river calibration outcomes could postdate an early three-day origin | [Author discovery and independent amended-design recheck](completion/design2-statistical.md) |
| Code defects: oil variance floor in wrong units; failed-run private evidence overwrite | [Verified fixes C-I06/C-I07](completion/oil-implementation-data.md) |
| Coverage defect: air peer availability initially used only scoreable blocks | [All-schedule denominator correction](completion/air-quality-implementation-data.md) |
| Event evidence defects: river issue origins and censoring/unknown alert segments | [Event-ledger correction and recheck](completion/river-flow-implementation-data.md) |
| Design risk: a partial spectral alias grid could invent uniqueness | [Pre-run amendment and numerical verification](completion/spectral-implementation-statistical.md) |
| Communication defects: weak direct answers, obscured near ties, and stale stories | [Results reviews and author responses](completion/RESPONSE.md); numeric outputs unchanged after presentation fixes |
| Copy errors: invented electricity intervals and split creator attribution | [Publication copy corrections and independent verification](completion/publication-copy-general.md) |

Each linked review retains its initial finding and later verification, including
cases where the first review missed a problem. Reproduction and deployment are
not inferred from successful model execution.

## Decisions about reviewer recommendations

Three separate critics—general, statistical, and data/implementation—reviewed
the initial plan and recurring checkpoints. The author implemented fixes;
non-authoring reviewers verified them. See [the protocol](../docs/REVIEW_PROTOCOL.md),
[documentation-only D01–D08](project/2026-10-29-documentation/response.md),
[first release](first-release/README.md) and [completion matrix](completion/README.md).

We retained scientific and engineering questions when a business framing would
misrepresent the data, as Ethan requested. One primary question and a small,
justified comparison set replaced method accumulation. CO₂ remained the accessible
opening, with electricity and detection as the initial release; that sequencing
never reduced the agreed full scope. Neural/pretrained models, Bayesian
extensions, reconciliation and other conditional extensions remain unevaluated.
The [author response](completion/RESPONSE.md) records accepted limitations and
implementation choices instead of silently treating every recommendation as done.
