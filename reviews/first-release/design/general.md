# First-release design review — general critic

Reviewer: `/root/general_critic` (separate automated reviewer, not the design author).
Date: 2026-10-30.
Checkpoint: question and design, before implementation or model fitting.
Baseline: `d7218096c7920e30da3ad722a3d1bffbede8fa4e`; both local HEAD and
`origin/main` resolved to this commit during review. The parent reported fetching
this baseline at 2026-10-30T16:14:39Z. The design documents were reviewed by the
hashes below, including any uncommitted content.

## Verdict

**The three designs have compelling questions, bounded scope, and useful planned
evidence. No implementation-blocking issue was found from the general-review
perspective. Two small claim-scope clarifications should be recorded before the
contracts are frozen and carried into the eventual reports.** Neither requires
expanding the experiments or adding methods.

This is not approval of unimplemented statistical remedies or of model behavior.
The statistical and implementation perspectives remain separate requirements.
No source downloads were repeated, no external facts independently rechecked,
and no models or tests run in this review.

## Findings

### GD01 — Clarify that the primary CO₂ result concerns December targets

Severity: medium for interpretation; no requested change to the selected target.
Status: identified.
Evidence: `studies/co2/DESIGN.md` specifies annual December origins and a primary
36-month horizon, alongside the broad multiyear-forecasting question.

The primary evaluation therefore concerns December observations three years after
each origin. It does not score a complete three-year forecast path or establish
performance for every month of the seasonal cycle. The 12-month target is also
December; the 1-month target is January. A hiring reader could otherwise infer
broader seasonal coverage from the annual-cycle language.

Required clarification: explicitly state this target-month restriction in the
contract's evidence/limitations section and keep it visible in the eventual
report. Describe the primary finding as three-year-ahead December performance.
Do not expand to all forecast months solely to address this wording issue.

### GD02 — Name the electricity peak subset by its frozen threshold

Severity: low; reporting clarity.
Status: identified.
Evidence: `studies/electricity/DESIGN.md` calls the secondary subset the "top 10%
actual load hours," then specifies a per-customer threshold computed from 2012.

The selected 2014 observations need not constitute 10% of 2014 hours. The frozen
historical threshold is sensible, but its label should describe what is scored.

Required clarification: call these "hours exceeding the customer's 2012 90th-
percentile load threshold" and report the evaluated count or fraction. Preserve
the existing training-period threshold rather than redefining peaks using the
evaluation year.

## Assessment of the requested angles

- **Question fit:** CO₂ makes a concrete comparison about changing growth;
  electricity asks who benefits from shared learning across a defined customer
  panel; synthetic detection examines the false-alarm/delay tradeoff under known
  truth. None needs an invented business narrative.
- **Bounded scope:** four prespecified CO₂ models, matched local/pooled Ridge
  comparisons, and two detectors form a feasible first release. The electricity
  exclusion of intervals is explicit and a reasonable scope limit. More advanced
  methods are not needed to make these initial comparisons worthwhile.
- **Hiring readability:** each design leads with its question and states what the
  analysis cannot establish. The plain-language report should translate the
  technical contracts; the contracts themselves can retain precise terminology.
  The source-intake summary provides a meaningful story about how actual records
  changed assumptions before fitting, without claiming those changes are already
  verified in model code.
- **Evidence usefulness:** prediction-level records, paired error comparisons,
  customer scatter and aggregation, and detection outcomes with denominators
  support inspectable conclusions. The designs leave room for a simple baseline
  to win and do not promise measured savings, real-time historical reconstruction,
  population-wide effects, or field detection guarantees.

No additional method catalogue, dataset, dashboard, or broader benchmark is
recommended at this checkpoint. The next useful evidence is a reviewed
implementation faithfully realizing these bounded contracts.

## Inspected SHA-256 hashes

```text
f02fa27d7e43e6ab190467893aed717f62ce6a5918ffae0789ad768b76f78b46  AGENTS.md
675275bf09409edec4459817e0652743b0e2b745d9723c74585062d246253f1f  docs/REVIEW_PROTOCOL.md
c21d3bfb2b4a8ad6fa9dd68221829d4a7589c469693b43e36e2919e7efae574a  reports/intake/README.md
355de8b3405b26f4ebfd21e2ca3a665d5b43a0b46062a3aaafe7cd25edc89fad  studies/co2/DESIGN.md
51bce01c2f693200434c8e480f5ec2d3e0cea30051dfb5dad80529d65634faa1  studies/electricity/DESIGN.md
ce8b0b9ef22f4c7f4d56f8b38487ad16e2834bf6510922a0c3f5e0a4158bfac5  studies/synthetic/DESIGN.md
```

## 2026-10-30 — Targeted amendment verification and contract-freeze verdict

Reviewer: `/root/general_critic`. Re-read all three amended contracts at the
hashes below. This entry preserves the earlier review and records the subsequent
disposition; it does not replace the original inspected versions.

- **GD01: identified → verified (design clarification only).** The CO₂ contract
  now explicitly limits the experiments to December origins, January targets at
  horizon 1, and December targets at horizons 12/36, and states that all-month
  trajectories are not evaluated. This resolves the claimed-scope ambiguity.
- **GD02: identified → verified (design clarification only).** The electricity
  contract now labels the subset as hours exceeding the fixed per-customer 2012
  90th-percentile threshold and explicitly says these need not be 10% of
  evaluation hours. This resolves the peak-subset wording.

**Contract-freeze verdict: ready from the general-review perspective.** The
amended contracts retain compelling questions, bounded scope, and honest claim
limits. The additional explicit penalty/clipping rules and detector definitions
do not introduce a new narrative or scope concern. Their technical correctness
and implementation remain matters for the statistical and implementation
checkpoints; this reviewer does not certify them by reading the prose.

No implementation, fitting, tests, or results were reviewed. No analytical
remedy is marked behaviorally verified by this design-only verdict. Carry the
target-month and peak-subset qualifications into the eventual reports.

Amended contracts inspected:

```text
e3a18e9a3df89cdbb9ab48b5d89de155474d3bc7311570469aca1523afd222f8  studies/co2/DESIGN.md
7237e98c225fdc788fc84c311ca39a34adf0a006b9c495353df9590753e3e09a  studies/electricity/DESIGN.md
28ab0483542d77bc66fadcd3b87dead99c203a3181eaeb3094c4000576420964  studies/synthetic/DESIGN.md
```
