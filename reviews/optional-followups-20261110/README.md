# Optional follow-ups — 2026-11-10

Ethan explicitly requested the optional presentation and analytical improvements
after the seven required corrections had been published. The original outcomes
were already known. New comparisons are exploratory, with a finite contract
declared before their runs; they do not become retroactive confirmatory results.

[Baseline](baseline.json) · [Shared contract](../../studies/followups/DESIGN.md) ·
[Earlier recommendations](../study-critiques-20261030/RESPONSE.md).

## Completion checklist for this extension

- [x] Freeze a finite question, comparator, seed and scoring plan for every addition.
- [x] Obtain independent statistical, data/implementation and general design review.
- [x] Implement CO₂ anchoring and explanatory figure; retain target-site sensitivity.
- [x] Implement electricity effect sizes, concentration and high-load tables.
- [x] Implement retail median comparator, all-code influence and bias diagnostics.
- [x] Implement oil score explanations and complete annual context.
- [x] Implement river figure captions and air-quality support/denominator context.
- [x] Implement ECG precision, patient bootstrap and all three additional assignments.
- [x] Implement detection grid, denominators and pointwise simulation intervals.
- [x] Implement matched-band spectra and all declared robustness cells.
- [x] Complete non-authoring implementation review and meaningful invariant checks.
- [ ] Execute from committed source; retain all attempted comparisons and failures.
- [ ] Verify every original numerical artifact remains byte-identical.
- [ ] Complete independent numerical, interpretation and presentation reviews.
- [ ] Update every story and the portfolio's claims to the actual findings.
- [ ] Follow final PR/main checks, deployment and live verification to completion.

## Reviews and chronological decisions

The [statistical](design-statistical.md), [data/implementation](design-data.md)
and [general](design-general.md) critics accepted the finite design. Their
clarifications were incorporated before full runs: anchored CO₂ retains the
site-target sensitivity; oil contribution denominators stay within each market;
ECG repeated assignments are whole-procedure sensitivity because assignment also
changes cap draws and fold-specific random seeds. Implementation gates passed before execution. Automated review is additional scrutiny, not independent human validation.

Earlier optional `not adopted` dispositions remain historical. On 2026-11-10,
the user reopened these options; their status is now **design amended**. No new
model or metric is chosen because it makes an old result more attractive.
Source redistribution and oil artifact-removal decisions remain unchanged;
clarified disclosures already address those accepted limits.

## 2026-11-10 — Implementation gate and execution repair

The non-authoring [statistical](implementation-statistical.md),
[data/implementation](implementation-data.md) and [general](implementation-general.md)
critics accepted the implemented additions. The data critic found a real execution
defect: libraries imported inside the thread-limit context could miss the cap.
The CLI now imports study libraries before entering that context and sets native
thread environment caps before NumPy loads. Independent fresh-process probes
verified both commands and the final repair. Apple Accelerate is controlled by
its environment setting; it is not enumerated by threadpoolctl, so this is not
a measurement of its internal thread count. No full follow-up run preceded this gate.
