# Finding status history

Append status changes here or link a dated study-specific history. Preserve old
entries. This history distinguishes changes to a plan from verified behavior.

## 2026-10-29 — Initial design critique recorded

Actor: primary agent, synthesizing the separate general, statistical, and
data/implementation critics. Scope: the proposal in this conversation, before
source acquisition or code implementation; no source-code revision existed.

- R01–R16: unrecorded → `identified` → `design amended`.
- Evidence: [initial synthesis and individual reports](01-design-review.md).
- Response: [revised plan](../PLAN.md) and per-study stories.
- Verification: none of the implementation-dependent remedies has been checked.
  Each remains open for the evidence specified in the register.

## 2026-10-29 — Documentation critique and author repairs

Actor: primary agent responding to three non-authoring reviewers. Scope: the
initial Markdown scaffold; each reviewer report records inspected file hashes.

- Documentation D01–D08: `identified` → `implemented` (awaiting verification).
- Evidence and changes: [documentation response](project/2026-10-29-documentation/response.md).
- R01–R16 remain `design amended`. Documentation review is not analysis validation.

## 2026-10-29 — Documentation corrections independently verified

Actors: non-authoring general, statistical, and implementation critics; primary
agent recording their verdicts. The reports contain the inspected file hashes.

- D01–D04: `implemented` → `verified` by the
  [general critic](project/2026-10-29-documentation/general-verification.md).
- D02–D03: additionally verified by the
  [statistical critic](project/2026-10-29-documentation/statistical-verification.md).
- D05–D08: `implemented` → `verified` by the
  [implementation critic](project/2026-10-29-documentation/implementation-verification.md).
- Scope: wording, source identification, review-record retention, workflow, and
  a heading-link correction only. R01–R16 remain `design amended` and unverified
  as analytical remedies. Registry/status updates record these verdicts; they do
  not alter the inspected study text or protocol.

## 2026-10-30 — Scoped implementation and empirical evidence

R01–R03, R07, R12–R13, and R15: `design amended` → verified for the first-release
scope, with limitations preserved and remaining study-specific work pending.
R04–R06, R08–R11, and R14 remain design-only. R16 claims are subject to the final
publication review, not presumed correct because scripts emitted numbers.

Evidence: [source/design/implementation/results reviewers](first-release/README.md),
[recorded tests](../reports/verification/checks.json), and
[fresh-checkout reproduction](../reports/verification/reproduction-final.json).
The first-release scopes are CO₂ forecasting, electricity forecasting, and the
synthetic detection control, not all planned methods on those datasets.

New observed issues and their resolutions are preserved in their original reports:
source metadata/DST discrepancies, invalid-input scoring defects, source-stability
evidence gaps, and a missing-record validation defect. No known result changed
because of those defects: scoring fixes preceded full runs, and the publication
changes left predictions and metrics unchanged.

## 2026-10-30 — Local publication and integration review complete

R16: first-release claim scope → independently verified by general/statistical
review, with wider planned-study claims still pending. This includes the exact
reports, figures, README, process stories, portfolio card, and profile addition.

RI04: stale portfolio revision links identified → rebuilt after committed outputs
→ independently verified locally. The final metadata commit is followed by another
strict build before rollout. No analysis computation changed for this correction.

[Publication verdicts](first-release/README.md#local-publication-gate) retain exact
scopes and hashes. Actual GitHub checks and deployment are separate rollout gates.
