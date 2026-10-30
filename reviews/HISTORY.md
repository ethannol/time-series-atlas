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

## 2026-10-30 — Restore the agreed full scope

Ethan challenged the lead agent for ending after the initial release. This was
an execution failure, not an authorized reduction of scope. The plan and AGENTS
instructions now require all eight investigations and an independent final audit.
The general critic also recovered the promised spectral control omitted from
the checklist. [Scope review](completion/general.md).

## 2026-10-30 — Verify the remaining source, design and implementation gates

R04–R06, R08–R11 and R14 moved beyond amended plans to checked source contracts
and implementations. The [completion matrix](completion/README.md) links each
verdict and exact inspected scope. The author response retains source facts,
design risks and demonstrated code defects as different categories.

The river origin-boundary risk and spectral grid ambiguity were discovered by
the author after earlier design approval. Independent reviewers acknowledged
those missed cases and verified the amended contracts before full runs.
Oil remains an accepted fetch-only archival limitation under R13; it did not
become an openly redistributable snapshot. R09 applies to person-held-out
annotation-centered classification, not automatic beat detection. R11 does not
imply a completed cointegration extension.

## 2026-10-30 — Complete numerical result audits, then revise interpretation

All nine run units executed under committed contracts. Independent critics
reconstructed scores and, where possible, predictions from saved parameters.
The new result records cover retail, oil, air quality, river flow, ECG and the
spectral control. General reviews required direct answers and visible tradeoffs.
The presentation refresh retained all numerical artifacts byte-for-byte.

R07 now includes retail's metric/volume disagreement, while interval evidence
remains scoped to CO₂. R10 includes the actual sampling control, with equal-power
aliases explicitly retained. R12 guards and R16 interpretations were checked per
study; full-checkout reproduction and final publication remain separate gates.
Publication copy review additionally caught an invented electricity-interval
claim and a mistaken creator attribution. Both were corrected and rechecked.

## 2026-10-30 — Full reproduction and live rollout verified

All sixty-eight outputs reproduced exactly in a fresh locked checkout, including
independent acquisition of the fetch-only oil history. Separate implementation
review verified the replay's source, input, output and test evidence. The full
collection and profile PRs merged at their expected non-draft heads; main CI
and Pages deployment passed. Live report paths, figures, numeric sources and
profile text matched the published revisions.

R13 is verified within its explicit oil archival limit; R15 has measured full-suite
resources. R16 publication content and rollout are checked, with the final general
full-scope audit required separately before the overall completion claim.
[Reproduction](../reports/verification/completion-reproduction.json) ·
[Rollout](../reports/verification/completion-rollout.json).

## 2026-10-30 — Independent full-scope closure audit

The general critic independently verified the full checklist against all nine
run units, the 68 retained/reproduced outputs and merged remote blobs, all 156
pinned live paths, nine report links, four published figure assets, the profile
copy, and successful PR/main/Pages checks. No study or publication-content
omission remained. [Exact audit scope and verdict](completion/completion-audit-general.md).
Publishing this dated record and its documentation-only CI/deployment follow-up
are separate from the already verified numerical result and live content.
