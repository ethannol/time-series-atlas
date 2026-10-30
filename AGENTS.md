# Working on Time Series Atlas

Follow Ethan's global repository-freshness and execution guidance. All work may
run locally with bounded concurrency and session-managed processes. The Mac mini
is unavailable. Stop session-owned processes when finished; leave unrelated work
and personal Chrome alone.

## Mandatory recurring independent reviews

Ethan explicitly requires subagents as part of this project. Follow
`docs/REVIEW_PROTOCOL.md`. Use separate agents for the relevant statistical and
data/implementation checks, and include a general critic at design and
publication checkpoints. Reviewers must not author the work they review.

Record findings and resolutions before dependent work proceeds. Source/target,
leakage, split, or scoring defects block affected full runs. Unsupported claims
block publication. Continue unrelated work where possible. Routine fixes and
reviews do not require asking Ethan again for permission.

An agent's approval is not scientific validation. Require concrete evidence, and
record unresolved disagreements and accepted limitations. Do not manufacture
findings or require a quota of criticism. Repeat the relevant review after a
material change; do not rerun every review for cosmetic edits.

## Story and provenance are deliverables

Update `STORY.md` for project milestones and `studies/<slug>/STORY.md` when that
study's question, data, implementation, evidence, or interpretation changes.
Write short chronological entries: what we did, why, what changed, and what
remains unknown. Link technical detail instead of putting it in the narrative.

Keep the initial review prominent in the README. Add later discoveries honestly;
do not claim a proposed risk occurred, a remedy was verified before it was
checked, or a result was known before the analysis. Do not rewrite earlier
entries to make the work appear prescient. Correct them with dated amendments.

Distinguish source facts, design risks, observed defects, empirical findings,
and limitations. Identify the human/agent contribution accurately. Never invent
Ethan's personal motivations, decisions, reviews, or professional experience.

## Evidence and scope

One primary question per study; a small set of justified comparisons. Freeze
targets, available inputs, selection rules, splits, metrics, and tuning budget
before full model runs. Separate forecasting, retrospective reconstruction, and
online detection. Archive protocol deviations rather than silently changing the
question after seeing the answer.

Use a shared results format, not a universal score or a universal data adapter.
Keep acquisition, exact-byte reproduction, and explicit refresh separate. Preserve
predictions/detections and run metadata so metrics can be audited without fitting
again. Check source redistribution terms before mirroring data.

A study is complete only with its reviewed report, figures, reproducible command,
result evidence, process story, and resolved or explicitly accepted findings.
