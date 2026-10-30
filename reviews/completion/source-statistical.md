# Completion source reconnaissance: river flow and ECG

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
Scope: primary-source reconnaissance and small source-header inspection, before
the completion study contracts or model runs. Parent reports freshly fetched
baseline `bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e` at
`2026-10-30T21:17:43Z`, working branch `feat/complete-atlas`.

This is preliminary source evidence, **not approval of downloaded analytical
inputs, a frozen design, an implementation, or results**. No models were fitted.
The reviewer read repository instructions, the plan, both study stories, and the
initial statistical critique. Suggestions below are review recommendations;
the author must choose and document the actual contracts for separate review.

## CAMELS-US: verified source facts

The [official NCAR deposit on Zenodo](https://zenodo.org/records/15529996)
identifies time series version 1.2, DOI `10.5065/D6MW2F4D`. It covers 671
catchments. Daymet and NLDAS retrospective meteorological forcing spans
1980–2014; Maurer ends in 2008. The single
`basin_timeseries_v1p2_metForcing_obsFlow.zip` contains the meteorological
products, observed streamflow, metadata, readmes, and simplified boundaries.
Separate model-output archives are not necessary to acquire these observations.
The provider describes daily resolution; this is not an hourly flood-warning
dataset. Individual streamflow availability still needs inspection.

The [record API](https://zenodo.org/api/records/15529996), retrieved successfully
with system `curl`, reports `access_right: open`, `license.id: cc-by-4.0`,
version `1.2`, and the following artifact metadata:

| Item | Verified provider metadata |
|---|---|
| File | `basin_timeseries_v1p2_metForcing_obsFlow.zip` |
| Size | 3,406,626,583 bytes |
| Provider checksum | MD5 `8e9a466710e8270b58f01d332a87184f` |
| Direct endpoint | [Zenodo file content](https://zenodo.org/api/records/15529996/files/basin_timeseries_v1p2_metForcing_obsFlow.zip/content) |

The API license resolves the earlier uncertainty about this identified deposit's
published license metadata. Preserve provider citation and attribution in the
data documentation; code licensing does not replace data licensing. Record our
own acquired-byte SHA-256 and retrieval time. A published checksum is not proof
that our download matches until it is checked.

The [NCAR attribute documentation](https://ncar.github.io/hydrology/datasets/CAMELS_attributes)
separately identifies **attribute version 2.0**, DOI `10.5065/D6G73C3Q`.
Hydrological signatures and climatic indices were calculated from time series;
mean discharge and baseflow index are examples of outcome-derived attributes.
Topography, soil, geology, and vegetation have other documented sources.
Consequently, an undifferentiated “CAMELS version 2” label is inadequate for
pinning both products. The small
[deposit readme](https://zenodo.org/records/15529996/files/readme.txt?download=1)
was retrieved; it describes the attribute version changes and citation needs.

## CAMELS-US: design risks and proposed constraints

These are prospective risks, not observed implementation defects.

1. **Operational availability is unverified.** Retrospective forcing is not a
   historical archive of information actually published by each forecast issue
   time. Use only days through the last fully observed day, and declare an
   idealized timely-observation assumption. Do not feed the realized future
   rainfall to a forecast or imply that an input labelled day *t* was available
   at the start of day *t*. The source alone cannot substantiate live reporting
   latency or first-release weather quality.
2. **Daily high flow is not observed flood damage.** A defensible target is flow
   exceeding a training-defined threshold at a declared future daily horizon.
   Claims of hourly warning lead time, avoided damages, or infrastructure risk
   would need additional outcomes. Threshold exceedance persistence can look
   useful without warning of onset: report event starts, false alerts, misses,
   and timing if the headline retains “warning.” Define contiguous event and
   matching rules before running; also retain ordinary day-level forecast error.
3. **Descriptors can contain target history.** For genuinely ungauged transfer,
   exclude discharge-derived signatures entirely. For known-gauge forecasts,
   any flow summary must be calculated only from allowed past training data.
   Audit climatic-summary temporal support as well. A temporal test on familiar
   gauges does not demonstrate transfer to unseen catchments.
4. **Cohort selection needs a reproducible rule.** A manageable proposal is
   approximately 12–24 gauges, one forcing product initially, selected by fixed
   geographic/static criteria and training-period eligibility. Report exact IDs
   and diversity criteria. Never pick gauges by held-out predictive skill or
   future completeness. Retain missing calendar days; score only real available
   outcomes and publish the exclusion counts.
5. **Different basins need interpretable comparisons.** Freeze any unit conversion
   and normalization, training thresholds, and site weighting. Show per-site
   skill beside aggregate scores so a large river cannot silently determine the
   result. Distinguish any held-out-gauge evaluation from the known-gauge task.

**Required intake verification before source approval:** inspect the actual ZIP
readmes, member paths and tables; verify units, dates, missing sentinels, quality
flags, duplicates and daily continuity; distinguish observed streamflow from
model output; inspect all chosen gauges' training and scoring masks. No exact
internal path, missing-value encoding, or complete 1980–2014 discharge coverage
is asserted here. Missing or estimated measurements must not silently become
observed high-flow labels.

## MIT-BIH: verified source facts and access

The [official dataset page](https://physionet.org/content/mitdb/1.0.0/) identifies
version 1.0.0, DOI `10.13026/C2F305`, open access under the **Open Data Commons
Attribution License v1.0**. It lists 48 roughly half-hour, two-channel records
from 47 people at 360 Hz. Its whole-download size is 73.5 MB compressed
(104.3 MB uncompressed), making acquisition of all records practical. The
principal files are `.dat` signals, `.hea` headers and current `.atr`
annotations. These annotations include beat and non-beat events. Earlier
annotation copies are retained for some records, so a suffix wildcard is not
a safe annotation selection rule. The page describes a 2018 correction to
`102.atr` despite the unchanged dataset version label: byte-level pinning matters.

File access is through the [versioned file directory](https://physionet.org/files/mitdb/1.0.0/),
with [RECORDS](https://physionet.org/files/mitdb/1.0.0/RECORDS) as the explicit
48-record inventory. The [license page](https://physionet.org/content/mitdb/view-license/1.0.0/)
was retrieved. Preserve dataset citation and license information alongside
manifests; acquire only the intended current annotation files.

The [official recording notes](https://physionet.org/physiobank/database/html/mitdbdir/intro.htm)
establish these relevant constraints:

- Records **201 and 202 belong to one person**; they must share a partition.
- Twenty-three records were randomly chosen and 25 deliberately enriched unusual
  phenomena. Pooled prevalence does not represent general clinical practice.
- Lead placement varies. Record 114 reverses the usual lead order; 102 and 104
  lack MLII. Records 102, 104, 107 and 217 include paced beats.
- Tape artifacts include a prominent 0.167 Hz component, and the provider warns
  about heart-rate-variability interpretation. Two channels can also have tape
  timing skew.
- Beat classes, rhythm changes, signal quality and comments are distinct kinds
  of annotations.

Actual small-file inspection independently confirmed lead variation:
[100.hea](https://physionet.org/files/mitdb/1.0.0/100.hea) lists MLII first and V5
second; [114.hea](https://physionet.org/files/mitdb/1.0.0/114.hea) lists V5 first and
MLII second. Both headers declare 360 Hz and 650,000 samples. This is evidence
against assuming channel zero always denotes MLII; it is not an audit of all
waveforms or annotation files.

## MIT-BIH: design risks and proposed constraints

1. **Separate people, then beats.** Define a stable patient-group mapping with
   201/202 grouped before train/validation/test allocation. Validate any adopted
   published record split against that rule. No random beat split can answer the
   study's unseen-person question.
2. **State what recognition conditions on.** Expert annotation centers can
   legitimately define waveform windows for conditional beat classification.
   That evaluates classification given beat localization, not an end-to-end beat
   detector. Windows extending beyond the annotated center imply declared
   processing latency/offline recognition. Do not report clinical diagnostic
   performance or instantaneous detection from such a design.
3. **Freeze the label taxonomy and eligibility.** Enumerate beat symbols,
   exclusions and the intended scientific interpretation. Normal-versus-PVC is
   a narrower question than all abnormal-heartbeat recognition. Rhythm markers,
   artifact markers, paced/fusion beats and unclassifiable beats need explicit
   handling; a generic “everything except N is abnormal” rule is not adequate.
4. **Handle leads by metadata.** Select the declared lead by name, or define an
   explicit alternate-lead analysis. A consistent MLII-only study must account
   for missing MLII records. Do not choose a channel using held-out accuracy.
5. **Keep fitted preprocessing inside training.** Scaling, PCA, templates, feature
   selection, sampling and threshold tuning must obey the patient split.
   Whole-record retrospective normalization is a separate availability assumption
   if the narrative implies streaming use. Beat-local normalization is possible
   but needs an explicit definition of what shape information it removes.
6. **Expose support and variation.** Report confusion counts, per-class recall,
   macro summaries, and per-person support/performance. A class absent from one
   person has undefined recall, not demonstrated perfect recognition. Thousands
   of beats do not supply thousands of independent people; any uncertainty
   analysis must respect patient clustering.

**Manageable cohort proposal:** acquire all 48 records, then apply an explicit
signal/label eligibility contract and patient-disjoint partitions. A fixed,
seeded cap on training beats can bound compute; keep the full eligible test
population and report excluded and retained counts. A small set of interpretable
waveform comparisons can answer this study without claiming broad diagnosis or
substituting the synthetic controls for the real ECG investigation.

**Required intake verification before source approval:** inventory all chosen
headers and hashes, verify actual current annotations and label counts, assert
sampling rate/lead mapping/record lengths, audit boundary-window exclusion and
group separation, and preserve the exact target population. Full waveforms and
the proposed analytical snapshot have not been independently inspected here.

## Preliminary verdict

Both collections have verified free official access paths and identifiable
published license metadata. Neither requires dropping the agreed study. The
critical remaining gates are actual-file intake, a reviewed fixed contract,
implementation invariants, and saved-result verification. Source documentation
supports the cautions above; it does not establish model validity or useful
forecast/recognition performance.
