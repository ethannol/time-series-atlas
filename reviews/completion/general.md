# Overall completion contract — general review

Reviewer: `/root/general_critic`, a separate automated reviewer.
Date: 2026-10-30.
Scope: the resumed full-project completion contract and its consistency with the
remaining study stories and initial critique. No implementation or study design
was authored by this review.

The parent reported fetching `origin/main` at 2026-10-30T21:17:43Z. During this
review it resolved to `bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e`. The parent had
uncommitted changes to AGENTS.md, PLAN.md, and STORY.md; the hashes below identify
the exact contract reviewed rather than treating the base commit as its contents.

## Verdict

**The revised contract correctly restores all eight agreed investigations and
explicitly prohibits treating an interim release as overall completion. It is
suitable for continuing the work, with one concrete scope gap to resolve and
two completion-audit clarifications below. It is not a completion certificate.**

Retail, oil, river flow, air quality, and ECG remain unfinished. The earlier
general-review approval covered the first-release artifacts and integration copy
only; it did not authorize stopping the full task. This review does not rerun
or revalidate the first three studies. Their checked boxes reflect their earlier
release evidence, which the final audit must inspect again within the final scope.

The new project-story entry accurately distinguishes the stopping failure from
analytical errors and does not pretend that a checklist has delivered the missing
studies. Continued acquisition and unrelated work need not wait for editorial
clarifications to the contract.

## CG01 — A promised supporting control is absent from the completion checklist

Priority: high for the final completion claim, not a blocker to acquiring data.
Status: identified.

The checklist marks "Synthetic controls" complete based on the first
change-detection experiment. However, R10 in `reviews/01-design-review.md` says
clean irregular-sampling spectral recovery will use synthetic controls, and the
current ECG story explicitly says these demonstrations "will move to synthetic
controls." The review register still has R10 at `design amended`; it does not
record this supporting control as withdrawn or deferred.

Required response: track that supporting control explicitly as pending, while
retaining the completed status of the existing change-detection experiment.
If its scope is to change, record the decision and its authority rather than
silently counting the first control as fulfillment of the whole promise. The
new contract says only Ethan can reduce agreed scope; an agent-authored final
status must not erase an accepted deliverable.

This does not require every method ever suggested in the original brainstorming.
Neural/pretrained models, Bayesian extensions, and reconciliation are explicitly
deferred in the register. The problem is the specific unqualified spectral-control
promise that still appears in the current story and accepted initial remedy.

## CG02 — Make the final audit trace every gate and open remedy

Priority: medium; needed before an overall-completion verdict.
Status: identified.

The checklist includes the right core studies and publication requirements, but
a single checkmark per study can hide a missing source review, incomplete
reproduction, or unresolved finding. The existing protocol already requires
these gates; the completion audit should make their evidence easy to inspect.

Recommended contract clarification: require a linked per-study evidence matrix
covering source intake/provenance and redistribution basis, frozen design,
pre-run implementation review, recorded execution, results/claim review,
reproduction, publication revision, and process story. Include each applicable
initial finding R01–R16 and later observed findings, with its final scoped
disposition and evidence. This is an audit aid for existing obligations, not a
new experimental framework.

In particular, a finding marked verified only for first-release scope must not
become globally verified merely because the other studies now have reports.
Accepted limitations must describe their affected claims; they cannot stand in
for an omitted core investigation. Live portfolio/profile links and final CI
must correspond to the actual final published scope, as the checklist requires.

## CG03 — Give the final coverage item a concrete reader-facing output

Priority: low; completion-criterion clarification.
Status: recommendation.

The final documentation/method-coverage item is useful but generic. The original
project aim was to showcase multiple methods across different data types, while
later review correctly narrowed each investigation to a meaningful question.
Both aims can be retained without inflating the method count.

Specify a compact question-to-study/method guide or coverage matrix linking the
actual evaluated methods, data types, and reports. Mark explicit extensions as
deferred and describe why they are outside the completed core. This gives a hiring
reader a coherent way through the finished collection and prevents an empty
method name or planned feature from masquerading as demonstrated capability.

## Scope carried by the remaining five stories

These are completion checks derived from the existing stories and R01–R16,
not new designs or additional findings:

| Study | Meaningful question that must survive implementation | Evidence/limits the final audit must find |
| --- | --- | --- |
| Retail | Forecast next week's observed sales for intermittently selling products | Actual transaction/cancellation audit; eligibility from permissible history; weekly outcomes and bias beside zero/simple baselines; no inferred unmet demand or optimized inventory claim |
| Oil | Determine whether volatility and direction improve on their own baselines | Both named WTI/Brent sources accounted for; nonpositive values/calendar conventions handled; frozen transformations and separate task scores; no presumed stable relationship or trading-profit claim; explicit source-snapshot/reproduction disposition |
| River flow | Measure useful high-flow warning from recent permissible observations across catchment types | Actual official CAMELS file/version intake; a justified fixed subset; input-availability trace; no future observed weather in an operational claim; target-derived descriptors excluded where the declared setting forbids them |
| Air quality | Assess warnings when a local station is unavailable | Contiguous simulated outages with stated lengths; concealed observed truth; contemporaneous/past input timing; warning misses/false alerts/delay; natural missing data not treated as known truth |
| ECG | Test abnormal-beat recognition on unseen people | Actual subject-to-record mapping and disjoint splits, including the shared subject; per-class/person results; artifact-aware processing/interpretation; benchmark recognition distinguished from clinical validity; the spectral-control promise explicitly accounted for |

The final audit should also confirm that plain-language stories explain what was
done, what review changed, and what the measured answer supports. Public criticism
must distinguish prospective risks, demonstrated source/code defects, and actual
results. Completing every checkbox is not a reason to manufacture a positive
finding or an exciting failure.

## Review method and remaining availability

Read the updated global contract in the repository's AGENTS.md, PLAN.md, and
STORY.md, all five remaining study stories, the initial critique synthesis, and
the current findings/disposition register. No experiments, model calls, data
acquisition, tests, or publication actions were performed. Only this review record
was written.

This critic remains available for separate design, results, publication, and
the eventual full-collection audit. The next reviews should inspect actual
artifacts at declared hashes; this contract review cannot pre-approve them.

## Inspected SHA-256 hashes

```text
8d7d26ffbac03badc31ccd895b70525c9ebe116b1dea600b11ae78af06dadf96  AGENTS.md
00dfc8d01c0f7f20efac17e79701bb9b9ba8a0b5cfe9f67ba2e2b5318253318c  PLAN.md
b23bdf1f400d02aba36ddd5da8737e3d66fcc182b679d3bb449dd312163d84cb  STORY.md
319caa900f95292c43f31e5e572cb96d468400dda9b963018a91008f16d4b5f9  studies/retail/STORY.md
71a2699ad2e0ee2ae52040e8b72d52dc354b3e25d861081eb479dad7935a1e8a  studies/oil/STORY.md
55ee7aa2a44d311cc0b7b471f03c682bc79d6d5c85ff8c8665ec43130bab5f43  studies/river-flow/STORY.md
6bf9ccf999b7d26b4e9797ec62527b84ac9b444ba6b2ea8203d706306942d43b  studies/air-quality/STORY.md
51b4d2b630ad437553aa43feb74db849b1adef5ea0bc4ec84e108cd6fe53b589  studies/ecg/STORY.md
44573eb74b797d892de1e8b37ae2eac4240ee7bd235c678ab4592ed5ccca5781  reviews/01-design-review.md
d5424ce179f153a9dbf8ec4e50495605dcd156f5b24871a6eae83176ea429a41  reviews/README.md
```
