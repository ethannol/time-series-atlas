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
- [x] Execute from committed source; retain all attempted comparisons and failures.
- [x] Verify every original numerical artifact remains byte-identical.
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

## Executed findings, with original comparisons preserved

| Investigation | What the follow-up adds | Interpretation boundary |
| --- | --- | --- |
| CO₂ | Anchoring cuts all-history three-year MAE from 6.964 to 2.361 ppm and recent-fit MAE from 1.119 to 0.860 ppm | Starting level matters; revised hindcasts and dependent targets are not causal evidence |
| Electricity | Pooled macro normalized error rises 3.89%; aggregate error rises 2.12%; all customer peak scores are visible | Load concentration is different from attribution of aggregate forecast error |
| Retail | Weekly median leads both losses, forecasts 18,002.5 of 33,858 units; excluding the dominant code changes the raw-unit winner | Error minimization does not identify an inventory policy; exact codes are not verified product identities |
| Oil | Full annual tables expose concentration of the net EWMA gain and years that offset it | Signed contributions are within-market descriptions, not causal explanations or stable annual gains |
| River | Figure and portfolio captions put assumed next-morning inputs beside misses, false alerts and missing truth | No new operational latency evidence |
| Air | Calendar baseline issues no high-hour indications; event-boundary counts explain delay eligibility | Overlapping censor counts are not additional misses; natural missing truth stays unknown |
| ECG | All three additional assignments complete; forest leads macro F1 in all four assignments, ranging 0.400–0.449; paired bootstrap contrast spans zero | Conditional patient-composition and whole-procedure sensitivity, not population guarantees or clinical validation |
| Synthetic detection | All 3,200 streams retain early alarms, misses, both detection denominators and pointwise intervals | Original calibration stays frozen; survival conditioning can flatter detection |
| Synthetic sampling | Common-band interpolation recovery becomes 79/100 versus 74/100; all 900 new realizations and 90 method cells retained | Common bands do not match bins; regular thinning stays analytically ambiguous |

[Full execution](../../reports/verification/optional-execution.json) took 219 seconds
with a process lifetime peak of 614 MiB. [Preservation evidence](../../reports/verification/optional-preservation.json)
confirms all 49 original numerical artifacts unchanged and 59 new outputs.
The full run used committed source `2446d4b1defbff7b5fd341171d9130381e279eb4`.
Reviewers then requested a prominent retail opening answer and explicit original
five-method scope. Source `a90ceb1` implements that presentation repair; its
[rerun comparison](../../reports/verification/optional-retail-presentation.json)
shows only the report and run metadata changed. No comparison was retuned.
