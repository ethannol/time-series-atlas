# Heartbeat recognition across people: the process story

**Question:** Does a model that recognizes abnormal heartbeat shapes work on people it has never seen?

**Data:** [PhysioNet MIT-BIH Arrhythmia Database](https://physionet.org/content/mitdb/1.0.0/); 48 roughly half-hour ECG recordings sampled at 360 Hz, with beat annotations.

**Current status (2026-10-30):** source intake complete; later dated entries
record implementation and results status. Earlier entries preserve the original plan. Ethan set the direction and requested the critical
review; agents proposed and critiqued the design described below.

## 2026-10-29 — Choose a question worth investigating

We selected annotated heartbeat recordings to extend the project beyond forecasting into waveform recognition. The useful question is whether a learned pattern transfers to a different person.

## 2026-10-29 — Challenge the first plan

Review found that two recordings belong to the same person, so separating files alone would not guarantee a fair test. It also surfaced artifacts introduced by the original recording apparatus and deliberate inclusion of unusual rhythms.

## 2026-10-29 — Change the design before fitting

People, rather than files or individual beats, will be kept apart in evaluation. Signal processing and interpretation must respect the recording artifacts. Clean demonstrations of irregular-sampling frequency recovery will move to synthetic controls. Benchmark recognition is not proof of clinical effectiveness.

Technical evidence and outstanding checks: [R09–R10](../../reviews/01-design-review.md#r09--separate-people-not-just-files).

## Next at planning time — 2026-10-29

Audit person/record mappings and annotations, then freeze the recognition task and evaluation. No recognition accuracy, diagnostic performance, or clinical benefit has been established.

Future entries will summarize actual source intake, benchmarks, implementation
reviews, results, and revisions in plain language. Detailed evidence stays linked
from the [review register](../../reviews/README.md).


## 2026-10-30 — Make the person and the signal explicit

We acquired the complete recording collection and checked its current files
against provider checksums. The intake selects the MLII lead by name, including
a recording where channel order is reversed, and preserves the shared-person
identity of records 201 and 202. Paced recordings and non-target annotations are
accounted for explicitly.

The compact input contains 100,662 eligible annotated beats. These are waveform
classification examples with expert-provided beat locations, not an end-to-end
diagnostic system. The proposed evaluation keeps people apart and will report
class support and variation between people. No classifier has run yet.

[Source review](../../reviews/completion/source-statistical.md).
