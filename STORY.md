# The story of Time Series Atlas

**Audience:** someone considering hiring Ethan as a data scientist.
This is a short account of the decisions, not a technical report.

## 2026-10-29 — Start with range

Ethan proposed a project showing time series methods on different kinds of data.
The initial agent-written plan selected seven free collections, from electricity
and retail transactions to river flows and heartbeat recordings. The intent was
to demonstrate a broad toolkit through reproducible studies.

**What was still missing:** a method list did not establish that each dataset
could support the proposed question or that the evaluation would be fair.

## 2026-10-29 — Ask for criticism before building

Ethan explicitly requested several critical agents, including a general critic.
Separate agents examined the project as a portfolio, as a statistical analysis,
and as an implementation and data-acquisition task.

They found consequential details the original plan had not surfaced. Some
river-basin descriptors already summarize the river flow we might try to predict.
Two heartbeat recordings belong to the same person. The CO₂ record contains
filled-in observations and a temporary change of observing site.

**What changed:** the plan gained explicit restrictions on predictors, people
kept apart during evaluation, and checks on how observations were produced.
These were design risks caught early. No model had been run, so we cannot claim
that those risks had already become errors—or know the results they would cause.

Read the [initial review](reviews/01-design-review.md) for the evidence.

## 2026-10-29 — Make the questions worth answering

Ethan asked for questions that arise in business, then clarified that a compelling
scientific or engineering question is equally appropriate when it fits the data.

**What changed:** each study now has one primary question. Electricity asks who
benefits from learning across customers. Retail asks how to plan around
intermittent sales. ECG asks whether a model generalizes to new people. The
broad questions became specific comparisons that can guide the choice of methods
and evaluation.

## 2026-10-29 — Make correction part of the public story

Ethan asked that the review discoveries be prominent, that independent agent
reviews recur throughout the work, and that every study keep a plain-language
account of its steps for prospective employers.

**What changed:** this repository now has a visible findings register, required
review checkpoints, and a process story for every planned study. Future entries
will record what actually happened, including failed approaches and revisions.
The process is intended to expose mistakes earlier, not to certify that agents
will catch every mistake.

## 2026-10-29 — Review the story itself

The three critics then read the new documentation. They caught wording that could
imply inventory needs where only sales were observed, and an oil question that
suggested comparing scores for different prediction tasks as if they were the
same. They also asked for named data sources, the individual original critiques,
and a clearer record of rejected suggestions and reopened findings.

**What changed:** those passages and the review workflow were revised. The
[documentation review](reviews/project/2026-10-29-documentation/response.md)
records the changes and their verification status. These are corrections to the
plan and its explanation, not evidence that the proposed models work.

## Where the work stood on 2026-10-29

The plan and initial source-documentation review exist. Full dataset acquisition,
implementation, model evaluation, and final scientific conclusions do not yet
exist. Next comes source intake: checking actual files before freezing the first
two studies' analysis designs.

## 2026-10-30 — Start with real files, not just source pages

The planning scaffold was published to GitHub. We acquired the two initial real
datasets and preserved their source hashes and analysis snapshots. Independent
source review found discrepancies between provider descriptions and actual
quality flags and clock-change values. Those are observed source findings, beyond
the prospective risks found in the original plan.

## 2026-10-30 — Review the implementation before accepting its scores

The analysis designs were committed before fitting. A bounded development trial
then exercised the pipeline without choosing models on final evaluation results.
Independent review found that malformed predictions could silently produce
misleading scores, and that run evidence needed stronger protection against code
changing mid-execution. The scoring paths now reject those malformed inputs;
run evidence captures and checks source stability and only promotes completed
outputs. A test-fixture failure was also corrected, separately from those defects.

These repairs are recorded in the [first-release review](reviews/first-release/README.md).
They establish safeguards to check; they do not establish forecast skill.

## 2026-10-30 — Let the first results answer the questions

The committed first release ran without changing its model choices after seeing
evaluation scores. Adapting the CO₂ growth estimate improved the declared longer
forecasts. Sharing electricity-model coefficients generally did not help this
panel. A change detector's apparent speed hid a high false-alert rate when noise
became persistent. These are different lessons, rather than one leaderboard.

The next checkpoint challenges these interpretations against the saved predictions
and outcomes. Process stories, original critiques, and source evidence remain
visible beside the results.
