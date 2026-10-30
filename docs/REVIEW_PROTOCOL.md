# Recurring independent review

Ethan explicitly requested ongoing subagent review on 2026-10-29. Review is part
of the workflow from question selection onward, not a final cleanup step.

## Roles and timing

| Checkpoint | When | Required independent perspectives | Evidence reviewed |
| --- | --- | --- | --- |
| Source intake | Before freezing the study design | Data/implementation critic; statistical critic | Actual sample records, provider notes, provenance, units, flags, time semantics, access and redistribution terms |
| Question and design | Before fitting candidate models | General critic; statistical critic; data/implementation critic | Whether the question is compelling and answerable, target, allowed inputs, splits, metrics, baselines, tuning budget |
| Implementation | Before full model runs | Statistical critic; data/implementation critic | Loaders, real model inputs, splits, transforms, invariant checks, a bounded trial run |
| Results and interpretation | After first full results, before conclusions are finalized | Statistical critic; general critic | All attempted models and failures, prediction evidence, scoring, deviations, robustness, limitations |
| Publication | Before publishing the study or a material update | General critic; statistical critic; data/implementation critic | Exact proposed content, supporting results, process story, reproduction evidence, open findings and links |

For a small scope, the same non-authoring reviewer may return at later checkpoints.
At design and publication retain distinct general and technical perspectives.
Do not substitute the implementation author reviewing their own work for the
independent review requirement.

Adjacent checkpoints may share a review session when all their evidence is ready
(for example source/design or results/publication). Record a separate verdict for
each checkpoint and retain every required perspective. Never collapse a pre-run
implementation check into a review performed only after the full run.

## How to run a checkpoint

1. Identify the review scope and exact commit or file hashes. Give each reviewer
   the question and relevant artifacts, including failures and known limitations.
2. Request separate critiques before sharing other reviewers' conclusions. Ask
   for evidence and severity, not agreement with the author's preferred answer.
3. Save each review under `reviews/<study>/<checkpoint>/` with its role, date,
   scope, findings, evidence, and verdict. A project-level review may span studies.
4. Record the author's response for each finding: accepted, disputed with evidence,
   or an explicitly bounded limitation. Link the implementation/design change.
5. Have a non-authoring reviewer check the resolution against evidence. Update
   the central register; do not mark a finding verified merely because text changed.
6. Update the study story with a brief account of what changed and why. Record a
   review with no material findings honestly; do not invent a problem for the story.

Separate agent authorship provides another critical pass. It does not constitute
independent human validation, establish correctness, or remove shared-model bias.
Sources, executable checks, held-out evidence, and candid limitations remain
necessary. Record the automated nature of reviews and never invent human signoff.

## Status and stopping rules

Use these finding statuses:

- `identified`: evidence or a plausible risk has been recorded.
- `design amended`: the plan addresses it; behavior has not been verified.
- `implemented`: the change exists; independent verification remains.
- `verified`: a non-authoring reviewer checked linked evidence of the remedy.
- `accepted limitation`: the unresolved limitation, affected claims, and rationale
  are explicit and independently reviewed; this is not a claim it was fixed.
- `disputed`: the author and reviewer disagree; preserve both positions and seek
  evidence. This remains pending and cannot bypass a material blocker.
- `not adopted`: a recommendation was declined with recorded rationale and a
  non-authoring reviewer's acknowledgement. It is not a verified correction.

Keep an append-only status history for each finding or group of findings: date,
actor/reviewer role, old and new status, affected revision or file hashes, and
evidence or rationale. Link this history from the current register. Do not erase
an earlier verification when later changes reopen it; mark the affected finding
and checkpoint pending again and record why. A `not adopted` disposition cannot
be used to bypass an established result-invalidating defect.

Source/target errors, information leakage, invalid splits, and incorrect scoring
block affected full runs until resolved. Unsupported claims and unverified
publication-critical evidence block publication. Other useful work can continue.
Scope limits and optional extensions are not blockers by default.

Material changes to data, target, features, splits, metrics, or headline claims
reopen the relevant checkpoint. Cosmetic edits do not require full re-review.
Batch related repairs before rerunning expensive analyses or publishing a new head.

## Plain-language stories

Every study has `studies/<slug>/STORY.md`, linked prominently from the README.
Keep a short chronological record of substantive decisions using this pattern:

> **Date — Step.** What we did and why. What we learned or reconsidered.
> What changed next. Link to the detailed evidence. State what is still unknown.

Write for a hiring reader with a minute or two to spare. Explain consequences
before method names. Keep source facts, prospective risks, observed defects, and
empirical findings distinct. Do not bury a serious caveat in an appendix or turn
the story into a technical transcript.

When a story grows, keep a concise reading path and link to older dated entries;
preserve the history. A conclusion may change. Never rewrite chronology to make
an earlier choice appear informed by later results.
