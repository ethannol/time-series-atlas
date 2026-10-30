# River flow, ECG, and spectral control — general design review

Reviewer: `/root/general_critic`, separate automated reviewer, not the design or
implementation author.
Date: 2026-10-30.
Checkpoint: question/design, before model comparisons.

Read all three contracts and the river-flow and ECG intake audits, including
record/gauge summaries. Spectral inputs are generated and have no observational
source audit. The previously inspected initial critique supplies the scope
context. No acquisition was repeated, classifier fitted, forecast produced,
or spectral experiment run. Only this review record was written.

## River-flow verdict

**Ready from the general-design perspective. No required correction identified.**

The question is naturally useful for hydrological analysis: whether recent weather
adds warning information beyond recent flow, with differences across known
catchments. Distinguishing continued high water from newly starting high flow is
especially valuable. The declared date offsets and assumed availability keep this
from being misrepresented as guaranteed operational warning time.

The actual intake records 17 gauges across 17 HUC regions, with region 09 absent.
The training-period-only selection, record of failed candidates, and approved-only
truth/input rule prevent replacing inconvenient gauges after seeing test results.
Flow-only versus flow-plus-weather is a focused comparison. Frozen alert cutoffs,
false-positive rates beside recall, onset/event ledgers, and per-gauge evidence
support a defensible answer even if added weather does not improve it.

Keep the known-gauge, nonrandom-panel and approved-observation limits prominent
when reporting results. Excluded estimates and gaps can affect which high flows
are evaluated. The cold-precipitation grouping is correctly described as a
training-derived proxy, not observed snowmelt or a causal explanation. This is
not approval of ungauged-river transfer or numerical implementation.

## ECG verdict

**Ready from the general-design perspective. No model-fit blocker identified.**

The question is about generalization to unseen people, and the contract explicitly
distinguishes annotation-centered classification from beat localization or clinical
diagnosis. The actual audit records 48 source records, 44 retained records, 43
retained people, shared person identity for records 201/202, and MLII in the second
channel of record 114. These details make the original review risks concrete.

The comparison spans a majority baseline, waveform templates, a linear classifier,
and a bounded nonlinear classifier. Patient-disjoint folds, capped training
membership, per-person/class results, and support counts make the planned evidence
useful. The N/S/V/F groups are clearly benchmark groupings; particularly, N is not
simply a healthy/ill label. Post-center waveform lookahead is explicitly disclosed.

Publication clarification to preserve: the template uses waveform shape alone,
whereas the logistic/forest pipeline includes amplitude and previous-RR features.
Their result is a comparison of the declared pipelines, not an isolated causal
effect of changing only the classifier. No extra ablation is required by this
general review. Technical reviewers must verify sampling, preprocessing, and
group separation in the actual implementation.

## Spectral-control verdict

**Ready from the general-design perspective. The control addresses the specific
R10 promise that the completion checklist previously omitted. No required
design expansion identified.**

The study asks a meaningful question about whether a spectral peak is identifiable
from the sampling pattern. Regular, irregular, and regularly thinned observations
give the comparison a clear narrative. Explicitly retaining the known alias and
declaring the tie rule prevents a lucky grid point from becoming a claimed
resolution of nonidentifiability. Same-realization method comparisons and fixed
example selection help make the resulting visual evidence inspectable.

The naive index FFT deliberately discards the true sampling intervals outside
the regular one-second condition. Present it as a known time-axis mistake/control,
not a fair general benchmark of FFT methods against Lomb–Scargle. The contract
already disallows universal superiority claims. Preserve that distinction in
the report and show why the aliased case cannot be uniquely solved from the
observations even if a selected peak happens to match the generating frequency.

This is a clean synthetic demonstration, not evidence of a physiological period
in the historical ECG data. The exact software behavior, frequency-grid handling,
noise generation, and ambiguity diagnostics remain for technical pre-run review.

## Combined conclusion and scope

These designs add known-gauge event forecasting, out-of-person waveform
classification, and irregular-sampling identifiability to the collection without
an excessive model catalogue. All can yield useful answers if simple methods win
or the declared recovery condition fails. No general-review blocker to proceeding
to implementation review was found.

The verdicts do not establish numerical correctness, approve publication of
unseen results, or complete the remaining full-project checklist. Preserve the
separate source/design, implementation, results, reproduction, and publication
evidence as each study progresses.

## Inspected SHA-256 hashes

```text
1cef0c1cee7dcfec1a04118752dc6b0750f5e3419b978ed4f58206d8527ba052  studies/river-flow/DESIGN.md
ed3eed51a1dd3c925e81d63c9571000ea858b16a25fa62709bc355ae28b8974e  studies/ecg/DESIGN.md
707cd450c0bd61a92409480fe2bc9b53b4fe5f1678f68326b65110221891f14c  studies/spectral/DESIGN.md
8426fccd9461d410d2fd76ffe700009b9fdc647eda42271cb1112a471c0ad775  reports/intake/river-flow.json
7744cb5569b699261bc2c3d18d278a6f5965b06c2f0477c89bdb842fff3e7937  reports/intake/ecg.json
```
