# ECG results and publication — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Run source: `6dc5e504690ae141dceac03b773f6d199f5774ec`.
Protocol: `fbd9a70b6b5ca5fa83f41cb86d3b2559cc5325df`.

Read the report, design, story, complete summary metrics, fold-score table and run
metadata; visually inspected both figures. Other linked artifacts were hashed
to identify the evidence scope, not independently rebuilt here. No classifier,
test, row-level rescoring, clinical evaluation, or exact reproduction was run.

## Results verdict

**The saved scores support partial transfer of useful classification signal,
with substantial class-specific failures. They do not support a broad claim
that abnormal-beat recognition works reliably on unseen people.** The patient-
held-out design addresses the declared benchmark question, and the report keeps
expert-provided beat centers, post-center windows, and population limits explicit.

Forest has the highest pooled four-class macro F1, 0.4340 versus majority's
0.2361, logistic's 0.3895, and template's 0.2505. Its accuracy is 0.8961, barely
above the majority baseline's 0.8948, showing why accuracy is not the whole answer
in this imbalanced dataset. Forest's S recall is 302/2781 = 10.9%; its F recall
is 0/802. The overall macro F1 gain does not repair those failures. Forest has
stronger N/V recall, while logistic has higher S recall with its own precision
tradeoff. No tested pipeline recognizes F well.

Fold variation also matters: forest macro F1 ranges from 0.3241 to 0.5263 and is
below logistic in fold 3. The fixed pooled comparison does not establish universal
forest superiority or an isolated causal advantage of its model family. The
report correctly says the pipelines differ in more than the classifier and
distinguishes fixed-four-class pooled scores from per-person supported-class
summaries. These are descriptive benchmark comparisons, not significance claims.

## Publication verdict

**The scoped interpretation is supportable; the answer/labels and actual-run
story need the updates below before publication.** Separate technical reviews,
reproduction, and final release checks remain necessary. No tuning or additional
model comparison is requested.

### GECG01 — Lead with the partial success and the classes it misses

Priority: medium; status: identified, parent has accepted a presentation update.

The opening explains the split but does not answer the question. State that the
best tested pipeline improves the equal-class macro F1 comparison while leaving
serious recognition gaps. Include the near-tie in accuracy with majority and the
S/F failures above. A generic "patterns transfer" conclusion would conceal the
important limitation already visible in the saved metrics.

The class table currently translates group letters only into more source symbols.
Add source-grounded readable benchmark group names, preserving the explicit warning
that N is not a healthy-person diagnosis. The plotted N/S/V/F labels are fine when
that translation is directly available. Briefly identify the template as a class-
mean waveform comparison; keep the different feature pipelines explicit.

Both figures are useful: the class panel exposes failures and the person panel
shows heterogeneity; the template plot makes the signal representation tangible
and labels its training-only scope. Do not use the high right-panel values as
proof of consistent four-class success, since each person's present-class
denominator differs. The text already explains this correctly. In the opening,
"43 distinct patient groups" would be more precise than treating their statistical
independence as proven; the key fact is the distinct people, not a guarantee of
independent clinical trials.

### GECG02 — Update the story to the executed comparison

Priority: medium; status: pending parent update.

The inspected status still says source intake complete and the last dated entry
says no classifier has run. Append the actual-run answer, readable class failures,
and pending review/reproduction status with links. Clarify the retained 44 records
from 43 people, rather than letting the raw 48-record source count stand in for
the evaluated sample. Keep the source collection and retained cohort distinct.

The current broad question emphasizes shapes; the actual logistic/forest pipelines
also use amplitude and previous beat timing. Make that clear in the executed
story so the result is not attributed to shape alone. Expert beat locations and
the post-center window remain part of the task. Preserve earlier planning text,
the shared-person finding, agent attribution, and the separate supporting spectral
control's still-pending status. No clinical or end-to-end detection claim follows.

## Scope hashes

```text
406d566c64603e6b81e096d8edfc83c2957ac39e1309b989d0453c62efd65f65  reports/results/ecg/REPORT.md
f3d1ef9a6a2c2cd88c581a1f675a9765cea20690db4655751b647d847274f359  reports/results/ecg/metrics.json
03dab31e3088e973981620eaa3b74dfc898d8bac309e3965655707b349ef1ecf  reports/results/ecg/fold-scores.csv
a8b75c7366b5b33dc826ef69782bdeed6a5ac094234017974d3b7bc6b757fe7d  reports/results/ecg/people-and-classes.png
22ddffc2768290e343182e6feb3cc9547bafeb6160bc16b9db6e39617f325f6d  reports/results/ecg/training-templates.png
56330dfd54803a6216d916b2b01f9a9a5365ae67ec0ce2ddec3022ca23fb916b  reports/results/ecg/model-audit.json
1b8fd4054e02943d17c2f6b94214ed6375baaeb6a33e64a38095ef0582210855  reports/results/ecg/person-class-scores.csv
b6e3d9e7503ebddf5f3dfbc72af5bb59e59e1de6d8df48d7e581e9a051f0d67c  reports/results/ecg/person-scores.csv
1c728814c63da383b0440cc5d2bd25f43517e2a07e3303a8af5b5e0b3facc3e8  reports/results/ecg/predictions.csv.gz
915d3f3a207cc7114654908b9f4a6088a3290636ea4065b940d4b5126852fa46  reports/results/ecg/run.json
2ec4be305773555d86dc19ccaa5051af17d3fd303700c9b84bb16905090f2776  reports/results/ecg/training-membership.csv.gz
70ea0f6bc5fe539448afc659e898eb72febb92aa777c1be86c4795dbcff34a59  studies/ecg/DESIGN.md
6f1ab6e71c7820246b5daf190e05a0fcb42c819ba3f874a44aff62af15674379  studies/ecg/STORY.md
```
