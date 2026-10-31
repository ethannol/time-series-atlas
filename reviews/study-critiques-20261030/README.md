# Dedicated investigation critiques — 2026-10-30

Ethan requested a new subagent dedicated to each investigation's implementation,
findings and presentation after the full collection was published. These fresh
critics inspect the implementation before consulting previous verdicts. Earlier
review approval does not substitute for new evidence.

Baseline: freshly fetched `origin/main`,
`71999b34ccfd7127840b173efb287ac0a66b2a26`; see [execution record](baseline.json).
Eight dedicated critics cover seven real datasets and both synthetic controls,
with at most three active concurrently. Reviews are automated, not independent
human validation. Each records inspected files, checks, limitations and evidence.

| Investigation | Assigned independent critic | Implementation | Findings | Presentation |
| --- | --- | --- | --- | --- |
| [CO₂](co2.md) | `critique_co2` | Accepted | Qualify starting level versus growth | Correction pending verification |
| [Electricity](electricity.md) | `critique_electricity` | Accepted | Accepted | Accepted; optional extensions |
| [Retail](retail.md) | `critique_retail` | Accepted | Accepted | Disclose stock-code identity limit |
| [Oil](oil.md) | `critique_oil` | Accepted | Accepted | OIL-01: disclose recoverable squared outcomes |
| [River flow](river-flow.md) | `critique_river_flow` | Accepted | Accepted within observed subset | RF-C01: show coverage and sparse-gauge support |
| [Air quality](air-quality.md) | `critique_air_quality` | Accepted | Aggregate result accepted | AQ-C01: show quarter/station exceptions |
| [ECG](ecg.md) | `critique_ecg` | Accepted | Accepted | Accepted; optional extensions |
| [Synthetic detection and sampling](synthetic.md) | `critique_synthetic` | Both accepted | Accepted for fixed procedures | Detection accepted; SYN-01/SYN-02 qualify sampling comparison |

The synthesis distinguishes demonstrated defects, unsupported or
underqualified interpretations, accepted limitations and optional future work.
No model is retuned because a critic dislikes its final score. Any new diagnostic
is labeled as post-publication and preserves the original frozen comparison.
Author responses and independent repair checks will be linked before closure.

[Author response and status history](RESPONSE.md).

## Synthesis

All eight dedicated reviews are complete. No result-invalidating calculation,
split or leakage defect was established in the inspected scope. Seven actionable
findings across six investigations concern interpretation, disclosure or omitted
context. Electricity and ECG need no correction; the detection control also
passes. Critics independently recomputed saved evidence rather than relying on
prior approval. Each report states what it did not verify.

The practical lesson is that reproducing a score does not finish the analysis.
The right follow-up question may concern the baseline's starting error, the
identity of a series, what a public artifact reveals, which dates contributed,
where an aggregate advantage reverses, or which frequencies a method could select.
These findings are explicit later discoveries, not retroactive claims that the
original design anticipated them.

Corrections are implemented in the report generators and stories. Independent
repair checks, report regeneration, numerical invariance checks and publication
are still pending. The original scores and frozen comparisons are preserved.
