# Remaining studies — general design review

Reviewer: `/root/general_critic`, separate automated reviewer; not the design or
adapter author.
Date: 2026-10-30.
Checkpoint: question/design review for retail, oil, and air quality.

Read the three proposed contracts and their actual-file intake summaries alongside
the initial critique synthesis. The source summaries establish the intended
collections, dimensions, cohorts, and recorded caveats; this review did not
independently download sources or audit adapter code. No candidate models were
run, implementation written, or source rights independently adjudicated. Only
this review record was written.

## Retail verdict

**The question is compelling and the bounded sales-forecast comparison is
defensible. Ready from the general-design perspective after RG01's wording
correction. Technical source and implementation reviews remain required.**

The distinction between recorded positive sales and unmet demand is explicit,
including cancellations, missing customer IDs, sheet overlap, unresolved repeated
rows, product eligibility, and later discontinuations. Weekly totals are a useful
target for intermittent products. Zero, recent-history, and specialized
intermittent-sales methods provide meaningful comparisons without excessive scope.
Per-product/quarterly results and signed total error preserve information a single
macro score could hide. The fixed, nonrandom panel and its scale-normalized score
must remain visible in publication, especially given the broad training-volume
range in the intake summary.

### RG01 — Do not equate sales underforecasting with buying too little

Priority: low; required claim clarification before the contract is frozen.
Status: identified.

The question section says a weekly purchasing planner needs a warning about
"systematically buying too little." The rest of the contract correctly states
that the data do not establish availability, inventory needs, lead times, lost
sales, or optimal order quantities. A negative sales-forecast bias is not evidence
that a purchasing policy bought too little.

Replace that phrase with underforecasting recorded weekly sales. It is fine to
retain purchasing planning as motivation, provided the actual evaluated output is
identified as a forecast input rather than an evaluated inventory decision.
No change to targets, models, or metrics is requested.

## Oil verdict

**The question, separate scoring of direction and volatility, and bounded
comparisons are defensible from the general-design perspective. OG01 remains a
source/publication claim that must be resolved; this is not approval to mirror
the source data.**

The intake establishes an actual nonpositive WTI observation, and the contract
declares dollar changes rather than silently applying logs or deleting the event.
It correctly keeps each market's observed calendar, saves gap lengths, treats
squared changes as a noisy volatility proxy, and avoids profitable-trading or
calibrated-tail-risk claims. Annual and predeclared episode breakdowns can make
the stability of any average improvement inspectable. The question does not
require proving a stable WTI–Brent relationship; separate market results are an
appropriate bounded first investigation.

### OG01 — Reconcile the source-rights assertion with R13

Priority: medium; blocks an unsupported redistribution assertion or mirroring,
not analysis of legitimately acquired local files.
Status: identified.

The source section describes the EIA XLS files as "government data with EIA
attribution." Initial finding R13 explicitly records that EIA distinguishes
third-party material and that oil-price notes identify an external source. The
intake JSON records hashes and values but does not settle the redistribution
basis. Being served by EIA alone does not resolve the project's existing concern.

Required response: replace the broad source-rights characterization with the
actual documented provenance and a link to the recorded redistribution decision.
If rights to publish a snapshot remain unresolved, preserve the already-approved
path of acquisition instructions/local retained bytes and an explicit public
reproduction limitation. Do not claim that a checksum or source attribution alone
closes R13. This review makes no legal determination; source reviewers must check
the specific basis and the proposed published artifacts.

## Air-quality verdict

**The outage-nowcast question fits these data, and its principal comparison is
bounded and defensible. Resolve AQG01's outstanding event-evaluation commitment
before freezing the design or treating R08 as fully addressed.**

Calling the task a contemporaneous nowcast is valuable: current reports from
other stations are an explicit assumption, not future weather smuggled into an
advance warning. The source summary records real missingness, and the contract
only scores deliberately concealed observed truth. Prespecified block starts,
three durations, common availability for model comparisons, abstentions, and
explicit dependence of nested outages make the experiment inspectable.

The station-specific training quantile is clearly a relative research threshold,
not a health standard. Evaluation on complete blocks and a small calendar schedule
cannot establish performance on every natural outage; the contract recognizes
that limitation. Keep null metric denominators and per-station/season differences
visible even if some scheduled subsets contain few high-pollution hours.

### AQG01 — Account for the existing promise to evaluate warning episodes

Priority: medium for scope and interpretation.
Status: identified.

R08's verification requirement explicitly calls for event-level false alarms,
misses, and delay. The new contract specifies hourly balanced accuracy, precision,
recall, false-positive rate, counts, and concentration error, but no episode-level
summary. Hourly classification can be a defensible primary endpoint, yet it does
not establish how many pollution episodes received an indication or how late the
first indication arrived. The planned story still concerns preserving useful
warnings during outages.

Required response: carry event-level false-alert/miss/delay summaries as declared
secondary outputs, with episode and delay definitions fixed before scoring; or
explicitly reconcile the earlier commitment through a recorded, authorized scope
disposition. These summaries can use the same saved hourly predictions and do not
require adding model families. Do not let a completed hourly-classification report
silently close an unperformed part of R08.

## Shared assessment and limits of these verdicts

All three studies now have a natural question, simple baselines, useful contrary
outcomes, and bounded claims. They add intermittent counts, market risk behavior,
and spatial sensor redundancy to the earlier trend/seasonality, pooled regression,
and detection work. A complicated model need not win for these to be worthwhile
portfolio studies.

The final reports should answer the declared questions directly and explain the
operational assumptions before method names. The full-collection completion
checklist remains open; this review does not declare these three studies, the
remaining two real-data studies, or their supporting controls implemented.

## Inspected SHA-256 hashes

```text
1c6c22952105781ff6a82369df958e152b18103a539b0af841dd2715ef3bf78a  studies/retail/DESIGN.md
71599f40f7a21a7acf3c09a2d35ec2d395468229b64fd5748b20d0ceb14e2987  studies/oil/DESIGN.md
6e13abab56781de90d59c0db6c456bf596139e65272ce1398e0700c9187481de  studies/air-quality/DESIGN.md
1335e7efa10e41ee7fc4a0a5cdf19294f1e77a6ba59fbec7a89f880d174324fc  reports/intake/retail.json
4120dd53e6db0c14b3a1277563fb9d934e94d3f3f56c0cc2d148a27c9e7549ca  reports/intake/oil.json
6c6eb61a5d4ef68ef2a187395b803de674c34abe7149beb672bf1950a02f02bd  reports/intake/air-quality.json
44573eb74b797d892de1e8b37ae2eac4240ee7bd235c678ab4592ed5ccca5781  reviews/01-design-review.md
```

## 2026-10-30 — Targeted amendment verification

Reviewer: `/root/general_critic`. Re-read the three amended contracts at the
hashes below. No implementation or output inventory was audited and no models
were run. This entry records design-level dispositions only.

- **RG01: identified → verified (design wording).** The retail question now
  describes systematically underforecasting recorded sales. It retains purchasing
  planning as motivation while explicitly excluding an evaluated inventory,
  latent-demand, or ROI claim. No sales-to-inventory inference is required by the
  contract. **Retail verdict: ready from the general-design perspective.**
- **OG01: identified → verified (unsupported ownership assertion removed), with
  an explicit reproduction limitation accepted at design level.** The oil
  contract now identifies the third-party price provenance rather than claiming
  government ownership. It specifies local-only raw/normalized prices and true
  changes, public original forecasts/aggregate scores/hashes, and reconstruction
  of outcomes from freely fetched inputs only after a normalized-input hash match.
  Future upstream revisions can prevent exact public reproduction; that limitation
  is now explicit rather than being hidden by attribution or a checksum.
  **Oil verdict: ready from the general-design perspective under that bounded
  acquisition/reproduction arrangement.** This is neither a legal determination
  of redistribution rights nor verification that the code/publication inventory
  actually enforces the arrangement. R13 requires later source, implementation,
  and publication evidence before it can be closed for this study.
- **AQG01: identified → verified (design commitment and definitions).** The
  air-quality contract now specifies block-local true-high episodes, missed
  events, false-alert episodes, and delay from event onset. It distinguishes
  left-censoring, conditional delay, abstention, and repeated/nested block scenarios.
  It does not claim that those block-local episodes are unique pollution incidents
  or operational alarm notifications. **Air-quality verdict: ready from the
  general-design perspective.** R08's actual mask construction and event scoring
  still require independent implementation/results verification.

All three questions remain compelling and bounded. These resolutions authorize
no claim that any model works, that source handling is implemented correctly, or
that the full Atlas task is complete. The technical pre-run gates and final
evidence reviews remain in force.

Amended contracts inspected:

```text
ccbbae99f581992fc1f9111d14d076fd316fa7db93e56dcad43fd21ae29df840  studies/retail/DESIGN.md
8bc0e4e5723e23beb7c729a2128f78ce62d5f2900700d558dce049fda8f8f16e  studies/oil/DESIGN.md
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
```
