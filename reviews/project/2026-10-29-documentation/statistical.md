# Documentation review — statistical perspective

Reviewer: `statistical_critic`, a separate AI subagent.
Date: 2026-10-29.
Scope: the review synthesis, register, recurring protocol, root README, and eight study stories at the hashes below.
Independence: the reviewer supplied the earlier statistical critique but did not author the primary agent's documentation being reviewed.
Record: the review below preserves the reviewer's final response, with local file-link destinations normalized to repository-relative links for portability. Later corrections and resolution verification are separate evidence; the original inspected hashes remain unchanged here.

---

**Docs-only verdict: acceptable with two minor wording improvements. No blocking statistical or evidence-status issue found.** I reviewed the three requested review/protocol documents, the root README, and all eight study stories. I did not run models, inspect analysis implementations, or independently recheck every external citation in this pass.

The synthesis faithfully separates source facts, prospective risks, proposed remedies, and verification still needed. “Design amended” is consistently used without implying executed fixes. Automated authorship and the absence of human validation are explicit. The recurring review protocol is substantive and preserves disagreement rather than treating agent agreement as proof.

1. **Low priority — retail story briefly implies a demand/inventory target.**  
   [studies/retail/STORY.md:11](../../../studies/retail/STORY.md) says a forecast could miss “the amount needed over a week.” The available outcome is observed sales, not inventory requirement or unmet demand. Replace with “the total sold over a week.” At line 19, prefer “so the tradeoffs of an always-zero forecast remain visible” over “so an always-zero forecast cannot look useful”; the evaluation should expose tradeoffs without prescribing the winner.

2. **Low priority now; resolve in the frozen contract — oil’s cross-task comparison needs a definition.**  
   [studies/oil/STORY.md:3](../../../studies/oil/STORY.md) asks whether swing size is predictable “more reliably” than direction. The story correctly promises separate benchmarks, but raw direction and volatility scores are not directly comparable. Add that each task will be evaluated against its own baseline and that the study asks where reproducible skill exists. The plain-language question could be: **“Can we forecast changes in price volatility even when price direction remains hard to predict?”**

No additional mandatory review stage is missing. The explicit source-intake checkpoint, separation of known-series versus new-series claims, and independent resolution checks cover the consequential issues identified earlier.

Hashes were unchanged between initial inspection and the end-of-review hash check:

```text
2034d742557aadd0b6fc6b95043613f68db5741f535163be680551a87764af57  reviews/01-design-review.md
07b79374beb5b33cf81598b0859c3528b544e9307e8c83892f8a8ac1b39b207e  reviews/README.md
dc41bbad4ad7823fdf5dd451f6f96d540dd1683338e53bc84669f14e8b09a8d1  docs/REVIEW_PROTOCOL.md
0f668f745126e075765b2d547495d098f329dc06ed56a5b864f61384971ef969  README.md
e633263cb4cf6af7fb6e4f99b3b2ae3188aadaffaeff5bcba8e08cfcb90b1232  studies/air-quality/STORY.md
f67b6209cc3ef5576313a420a180d323b877d6fcc2f84648d20810f79dec7a7a  studies/co2/STORY.md
52ead2bf9921c496b2a2e5b38f65cc2fba7b001dcec75a6cd14b625f2af7d785  studies/ecg/STORY.md
9bf088a7536083891c93eb916d10841c5a112adbc4862cd38d7735acca5e32e6  studies/electricity/STORY.md
6eeb592aaa07ffdcd377418710b9c1ddcd4ce9d4d15e181102109068bb088914  studies/oil/STORY.md
9009bb0a0c7fceb8ff52ab6ee11c40c07392f9ed977f330585fcecfdaeb494e0  studies/retail/STORY.md
981c2dcfbeeada33ef531aac8497811d2a272a8cc5dea3e896f8a2e658c9f31c  studies/river-flow/STORY.md
3aab85ef0ed557d9293308ad0b65560df92787dddfcf6d0227ba3f9e719b51af  studies/synthetic/STORY.md
```

This verdict approves the documentation’s representation of the design review. It does **not** close R01–R16 or validate future analysis behavior.
