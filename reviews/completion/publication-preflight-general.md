# Full-collection publication preflight — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Scope: current README, plan, portfolio metadata, root story, all eight study
stories, review register/history, original R01–R16, data credits, review protocol,
and the supporting spectral design. Also inspected current CLI command selection
and dependency declarations to identify documentation mismatches. No code,
project copy, model, test, or publication action was authored or executed.

## Verdict and timing

**This is a list of final-publication obligations, not a completion verdict.**
River, ECG, and the supporting spectral experiment are still pending execution
at this checkpoint; retail, oil, and air quality have measured results but retain
presentation/reproduction gates. First-release completion evidence remains
scoped to CO₂, electricity, and synthetic change detection.

The plan now names the full agreed scope correctly. I found no additional
unqualified core experiment missing beyond the already-restored spectral control.
Do not add unneeded models merely to make the toolkit sound broader. The concrete
gaps are evidence reconciliation and the reader-facing account of what has
actually been delivered. The known first-release-only root copy should be updated
after the remaining results are reviewed, not used as a reason to stop those runs.

## PPF01 — Produce the promised full gate matrix and reconcile findings

Priority: high before a final completion claim; currently pending.

The current register says all five later studies remain planned and that their
source intake has not occurred. The actual study stories and review files are
farther ahead. A hiring reader cannot currently follow the newer corrections
from the central index, and a future blanket "verified" status would hide scope.

Create the already-promised linked evidence matrix. It needs rows for the eight
investigations, with synthetic detection and spectral recovery separately visible
as run units. Each row must identify source/redistribution evidence, frozen design
revision, pre-run technical reviews, run source/protocol, result evidence and
figures, independent result/claim verdicts, reproduction, current story, and final
published revision. Include unresolved or accepted limitations and links to author
responses plus independent rechecks. A checkmark or an author's reply alone does
not establish the gate. The final general audit must inspect this matrix against
actual files and the final publication state.

Reconcile original and later findings with their true scopes:

- **R01, R12, R16:** resolve for each actual task, including the added control;
  first-release approval is not full-collection approval.
- **R02–R03:** retain the original source/quality limitations and checked evidence;
  do not imply the providers' conventions were repaired by this project.
- **R04–R05:** distinguish the evaluated known-gauge warning task and explicit
  information-timing assumptions from any unevaluated ungauged transfer task.
  An allowlisted current model does not establish that an ungauged model works.
- **R06–R08:** link real target/cohort/scoring/outage/event evidence. Retail's
  point-forecast study must not be described as providing calibrated retail
  uncertainty merely because R07 also discusses probabilistic evaluation.
- **R09–R10:** retain subject disjointness and class/person evidence; state that
  detection tolerance is not applicable to annotation-centered classification.
  Require actual spectral results, including ambiguity, before closing that
  accepted control promise. Do not count it as a ninth independent real study.
- **R11:** link the nonpositive-price/calendar audit and separate out-of-sample
  task scores. A cointegration/relationship extension was not performed and is
  not implied by the oil chapter's completion.
- **R13:** distinguish mirrored, reconstructible inputs from oil's accepted
  archival limitation. A successful local reproduction does not create public
  archival rights or guarantee future access to unchanged official history.
- **R14:** document actual range/member acquisition and its integrity evidence;
  do not describe it as downloading or verifying the complete multi-gigabyte
  archive when that was not done.
- **R15:** use measured final runtime/resource and installation evidence. The
  current package installs specialized dependencies together; do not claim
  optional groups already exist. Either record the bounded-installation choice
  explicitly or implement the intended grouping if it is useful. This does not
  require a new framework.

Preserve the original initial-review wording as historical evidence. Update the
current register and append status history instead of rewriting what was known
before implementation. Add later discoveries to the index with their type:
source fact/discrepancy, proposed design risk, demonstrated implementation defect,
measured result, or execution/publication failure. The river calibration-boundary
amendment is particularly useful evidence that review can miss a problem; retain
the recorded acknowledgement rather than claiming the first approval caught it.

## PPF02 — Supply the dataset-quality and evaluated-method guide

Priority: medium; currently absent as a reader-facing artifact.

The original user wanted methods across distinctive types of data, and specifically
asked why each dataset's qualities matter. The question-led chapters preserve
coherence, but the README currently provides only questions and status. Add one
compact guide linking the actual reports. Useful fields are: dataset/source,
distinctive data quality, task and question, methods actually evaluated, one key
evaluation constraint, and result link/status. A separate long method encyclopedia
is unnecessary.

Qualities that should survive that compression:

| Investigation | Distinctive quality the guide should explain |
| --- | --- |
| CO₂ | Long monthly trend and annual cycle; changing growth and published-data processing/revisions |
| Electricity | Multiple series with different scale and shared calendar patterns; customer versus aggregate outcomes and clock conventions |
| Retail | Event transactions converted to sparse sales series; many zero weeks, returns/overlap, and the effect of metric weighting |
| Oil | Irregular observed dates, negative levels, large changing fluctuations; uncertainty and direction are different targets |
| River flow | Catchments respond differently to past weather; quality flags, delayed daily information, and new-event versus continuing-high-flow warnings |
| Air quality | Spatial peer measurements and contiguous outages; same-hour input availability differs from available scoring truth |
| ECG | High-rate waveforms with expert annotations, rare classes, person dependence, and recording artifacts |
| Synthetic controls | Known changes/frequencies and deliberately mismatched assumptions; persistent noise and sampling ambiguity reveal failures that real-data scores cannot prove |

Name only evaluated methods as demonstrated capabilities. Keep Bayesian,
neural/pretrained, reconciliation, and other conditional extensions visibly
deferred. Forecasting, classification, nowcasting, detection, and frequency
estimation should remain distinct tasks with their own metrics; there is no
meaningful collection-wide winner or universal score.

## PPF03 — Complete source credits and final-scope reproduction instructions

Priority: high before publishing the final collection; currently incomplete.

`data/README.md` currently covers only CO₂ and electricity. Add the other five
collections' exact provider/version/citation, access and redistribution basis,
what subset or transformation is published, selection/mapping/quality conventions,
and links to input manifests/audits. Describe generated controls separately.
The oil exception belongs here and in the quickstart, not only deep in its report.

The README's command comments and approximately eleven-second runtime describe
the first release. The inspected CLI now selects nine run units for `atlas all`.
The final instructions must state what a clean checkout can run offline, how to
fetch and verify oil inputs explicitly, what fails when historical bytes change,
and how to run individual studies or the full declared suite. Keep data refresh
separate. A verify command that reports an absent fetch-only input must not be
presented as proof that all inputs were checked. Report the final measured
runtime/resource scope honestly; do not reuse the first-release measurement as
the final-suite cost.

The final reproduction artifact must list the actual run units and tested source
revision, including unchanged first-release results, rather than relying on the
old artifact name or its existence. Final CI and live deployment evidence remain
separate from successful local analysis reproduction.

## PPF04 — Refresh hiring-reader claims and story endpoints coherently

Priority: medium; known final update pending.

The current stories retain useful chronology and candid agent attribution.
Preserve both. After results and reproduction, each story needs a current status,
a plain answer with a small number of actual values, the consequence of the
main correction, the strongest limitation, and direct report/review links. Do
not turn these into technical transcripts or require a dramatic finding in
every study.

Specific endpoints still requiring attention:

- Retail's last entry still says results review is pending while its current
  status says independently checked. Add the raw-unit versus normalized-score
  lesson and final gate status in a dated continuation, preserving chronology.
- Oil and air-quality stories now contain the actual-run step and appropriately
  pending reproduction. Verify their later completion updates against evidence;
  do not pre-approve them here.
- River's data header still says the subset is to be fixed although the story
  records the selected subset. After execution, distinguish one/three-day date
  offsets and retrospective-weather availability assumptions from demonstrated
  operational lead time. Keep the boundary-correction story and actual attribution.
- ECG must make the retained records/people/classes and expert-provided beat
  locations clear. Its story should reflect the evaluated feature pipelines,
  which may include timing as well as shape; no end-to-end detection or clinical
  claim follows from person-held-out benchmark classification.
- Synthetic must link both completed controls once reviewed. Explain frequency
  ambiguity and the deliberately incorrect timestamp assumption plainly, without
  promoting a favorable example into universal spectral-method superiority.

Update the root story with the later substantive findings and final publication
evidence; retain the premature-stopping entry. The first critique should remain
prominent in the README. Preserve the distinction between risks caught before
code, defects actually demonstrated, and empirical answers. The existing clear
AI ownership paragraph is valuable; a full collection is not evidence of human
authorship or independent human validation.

## PPF05 — Match portfolio/profile metadata to the published evidence

Priority: high before the final integration claim; known update pending.

Review these actual `portfolio.json` fields together after the remaining results:
`status`, `scope`, `conclusion`, `summary`, `data`, `techniques`, `finding`,
`not_claimed`, `documents`, `figures`, and `verification`. They currently describe
the first release. Exact numeric headlines should resolve through the final
saved metric sources with their denominators/horizons clear. A single backing
ledger is fine if extra sources are explicit; it does not represent every study.

Keep the card concise: a few representative findings and figures can demonstrate
range, while a complete linked index makes all studies and spectral evidence
discoverable. Do not require nine headline numbers or nine card figures. Ensure
the profile and portfolio agree on the completed scope and retain limitations
where they affect those selected headlines. Update generalized timing claims
carefully because annotation-centered ECG classification is a different task
from forecast-origin evaluation.

Build links from a revision that actually contains the final outputs, then verify
the exact publication revision, profile integration, latest CI, and deployed
page. The earlier stale-commit-link defect shows why a local build alone is not
the full release gate. This preflight did not inspect or approve any future
external integration changes.

## Snapshot hashes

Files were read during ongoing parent work; these hashes identify this preflight
snapshot rather than a final release. The spectral design was context only;
this review does not replace its specialized design verdicts.

```text
ab27a5138fb5e9e969019f69a775f1de2b62e9b6cef19f24b0219cf83a2bb9f3  README.md
f0ea1313c5e9c5bc61a07209bf216e26095f495a560808e63f1d3b6d383e65fc  PLAN.md
8d58cba8b31629d8a84e8b2c31a09cad084bdda99d3637fdf4e98abf6ec087ca  STORY.md
5ac08ff58dd4bc552693ecd50ad8d11226995fbf6c0a7f9d295fd9f6035635a3  portfolio.json
d5424ce179f153a9dbf8ec4e50495605dcd156f5b24871a6eae83176ea429a41  reviews/README.md
69ce091a6e774282a45bf2b73b0ce78b8b0466a991b0c8c79b23130cc13f1569  reviews/HISTORY.md
44573eb74b797d892de1e8b37ae2eac4240ee7bd235c678ab4592ed5ccca5781  reviews/01-design-review.md
bb1a6a00af7f401616aa2d644d27ce52ba9f30432f5de3f91124a2f18df37b4b  data/README.md
675275bf09409edec4459817e0652743b0e2b745d9723c74585062d246253f1f  docs/REVIEW_PROTOCOL.md
902861f217c542630204a72d9b5a544fc7a9e7ef39824bd2c0b328e64468ba8a  studies/co2/STORY.md
5b4310e708b854ce1180af3bc00524fde47a059a128ee56159e5d231ddd2413f  studies/electricity/STORY.md
d83db1f2327f24e26c73e0876b3bbd9c5eff216b321c3da4e72a7596cc0f00ef  studies/retail/STORY.md
4e5c8d5c8fa28ca16987d271e670ad81c3b4b0601403de100fb2f70119c10828  studies/oil/STORY.md
b80ef263a8a86d186be77dd437960ce14f553e1397af865a28d1c8d0494e73bb  studies/river-flow/STORY.md
2ba7fbbe85bd60b509c3a94f100e9489e17dc277d3ca96c239e2d096cd149cee  studies/air-quality/STORY.md
6f1ab6e71c7820246b5daf190e05a0fcb42c819ba3f874a44aff62af15674379  studies/ecg/STORY.md
718fb2a856d39ee8df2bcd564433b70ee1056489b1f0902a8789be9d91f07f18  studies/synthetic/STORY.md
eb205ebe3249cf4a9fd5051e1e2deee086ca80a4c669d45e98890ad01c5be994  studies/spectral/DESIGN.md
344f8b05f5a8edb8cf825855ab7aa5e0cf7df92303bc24eb1b8ebaeaaf07d7e1  pyproject.toml
8ded82ddfaa1d7d1cfaae756419e614e991eb8b2bc699c59a746c8d23e3930dc  src/tsatlas/cli.py
```
