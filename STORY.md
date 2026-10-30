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

## 2026-10-30 — Check whether another checkout gets the same answer

A separate checkout, without downloaded raw archives, reproduced every published
result file from the committed analysis snapshots. Rebuilding from the pinned
original sources also reproduced the snapshots. The reviewers recalculated the
headline metrics and asked for a clearer plot so tiny customer gains would not
look more important than they were.

Publication review caught a different kind of mistake: an early portfolio build
linked to a commit that did not yet contain a new result table. Rebuilding after
committing the outputs corrected the links. Reproducibility, clear communication,
and working evidence links are all part of delivering the analysis.

[Final review and reproduction evidence](reviews/first-release/README.md#local-publication-gate).

## 2026-10-30 — Publish the first completed studies

The first release was merged to GitHub after its checks passed. The portfolio
and profile additions followed, with the existing portfolio checkout left
untouched. Portfolio tests and deployment succeeded, and the live project page
was checked for the result figures and recorded values. The analysis and review
commits were preserved so a reader can see that the designs preceded fitting.

The collection now has completed CO₂ and electricity studies plus the synthetic
detection control. The other five real-data studies remain planned.
[Rollout evidence](reports/verification/rollout.json) ·
[Live portfolio page](https://ethannol.github.io/portfolio/projects/time-series-atlas.html).

## 2026-10-30 — Correct an execution failure, too

The lead agent stopped after publishing three studies, although all eight agreed
investigations remained in scope. Ethan challenged that premature stopping.
The agent had invented its own finish line; there was no reported blocker or
user decision to reduce the scope.

We added an explicit full-project completion checklist and a required independent
audit before declaring the overall task complete. The remaining five studies
are outstanding work. This process change makes the stopping condition visible;
it is not evidence that the unfinished studies have been delivered.

## 2026-10-30 — Continue the collection and keep discovering source problems

Independent intake review found exact duplicated transactions across retail
workbook sheets, a negative WTI price, and third-party attribution behind the
public oil-price files. Each finding changed a concrete choice: overlap handling,
price transformation, or how inputs are distributed. The continuing review also
recovered a promised synthetic control that the completion checklist had missed.

The retail study then supplied a useful first result: an always-zero forecast
won one normalized error score while missing every recorded sale. That result
is under review. The remaining studies are underway; this is progress within
the agreed scope, not a completed collection.

## 2026-10-30 — Finish the remaining experiments and challenge their answers

The remaining real-data studies ran under their frozen contracts. Oil's variance
models improved one appropriate loss while direction prediction did not improve;
a different variance loss reversed the ranking. Nearby air-quality stations
preserved useful same-hour indications, but missing local observations limited
which simulated outages could be scored. River high-day recall hid many missed
new rises. ECG's high overall accuracy hid an entire missed rare beat group.

Separate agents reconstructed predictions or scores from the retained evidence.
They asked us to lead with these findings and their limits, not just describe
how the experiment was organized. We revised the reports and confirmed that the
numerical artifacts did not change.

## 2026-10-30 — Review can miss a problem, and the next pass still matters

The initial river design review missed a boundary case: a three-day forecast
could use calibration outcomes that were not yet known at its origin. The lead
agent later found it; the revised origin guards were independently checked before
the full run. The spectral control had a similar pre-run lesson: adding only the
true frequency's alias did not protect other candidate peaks from false certainty.
Its amended grid preserves sampling ambiguity throughout the search.

The completed synthetic experiment recovers frequency under irregular sampling,
yet regularly thinned observations retain two equally strong explanations.
That does not establish a physiological result. It demonstrates why knowing the
sampling process matters before interpreting a spectrum.

## 2026-10-30 — Audit the explanation as carefully as the computation

Publication review caught an invented electricity-interval capability in the
method guide and a source creator incorrectly split into two authors. Those
were actual copy errors, corrected before publication. The dataset guide, source
credits, per-study stories and full evidence matrix now make the analytical
process inspectable. Fresh-checkout reproduction and live publication remain the
next delivery gates; executing every experiment alone does not complete them.
