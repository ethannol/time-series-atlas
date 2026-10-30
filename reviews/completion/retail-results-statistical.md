# Retail results and publication review: statistical perspective

Reviewer: `statistical_critic`, independent AI subagent. Date: 2026-10-30.
First full run: source `715ac6c89b1948609c67626c883a4cc63ec3abde`, frozen protocol
`b369cc865d4eafaabe8e8f4d3b7ba26ae36bb0ba`.

**Results verdict: approved.** Independent recalculation matched every primary,
per-product and quarterly metric. **Publication-content verdict: the report's
numerical claims, figure and bounded interpretation are approved.** Planned
exact reproduction is still pending and must not be described as completed.
The minor story correction below remains. No model was retuned, refitted or
chosen after this audit; review used saved predictions and pinned observations.

## Evidence independently checked

- All six result-file hashes match the run ledger. Source and protocol identities
  agree with the prior reviewed implementation/contract.
- There are 5,760 finite prediction rows: five methods on the same 1,152 unique
  product-weeks, with 24 products and 48 weeks each. There are no duplicate
  model/product/origin keys, differing targets across methods, or silently omitted
  product-weeks.
- Every saved target agrees with the seven-day sum of the pinned daily sales.
  Every scale agrees with seven times the product's mean 2010 daily sales.
  Independent direct sums also reproduce all zero, last-week and rolling-28
  predictions. Intermittent-method prediction recurrences were previously checked
  at the implementation gate; this audit does not claim a second model rerun.
- Primary macro MAE was recalculated as an explicit mean of per-product scaled
  MAEs, independently confirming the balanced-row implementation's weighting.
  Raw-unit MAE, signed means/totals, observed/forecast totals and underforecast
  counts all match. Every per-product and per-quarter metric matches too.
- The figure was visually inspected. Both axes, method ordering and scales agree
  with the saved summaries. Its bias panel makes zero's complete underforecast
  visible rather than presenting the primary-score winner as an ordering policy.

## The zero winner is a real, narrow result

Zero has normalized weekly MAE **0.986057**, versus **0.999305** for TSB and
**1.004962** for the 28-day mean. It forecasts no units while the cohort records
**33,858 units**. This is not a missing-target, denominator, or alignment error.

Descriptive audit of the saved outcomes found **669 of 1,152 product-weeks
(58.1%) have zero recorded sales**, and **16 of 24 products have a zero median
weekly target**. Absolute error favors conditional medians; sparse sales make a
zero forecast competitive under that loss. These post-run descriptions explain
the result and are not a new selection rule or a tuned alternative metric.
Zero attains a minimum per-product error on 15 products, counting ties; this
does not mean it is best for every product or every purpose.

The predeclared raw-unit endpoint answers a different question. TSB has the
lowest raw-unit MAE, **25.9212**, versus zero's **29.3906**, a descriptive 11.8%
reduction. Its total forecast is **31,923.6 units**, 5.7% below recorded units.
The largest product supplies 21,484 of the 33,858 units, explaining why summed-unit
and equal-product conclusions can differ. None of these comparisons establishes
statistical significance, inventory requirements, latent demand, profitability
or the superiority of one method beyond this fixed cohort.

The current report correctly keeps the primary-score conclusion narrow and
shows the other endpoints. As an optional explanation improvement, it can state
the observed sparsity and identify TSB as the raw-unit MAE winner. There is no
reason to change methods or thresholds to make the headline more attractive.

## Story and publication follow-up

The dated results entry honestly says first results exist and review is pending.
Its warning that low error does not determine what to order is supported. The
top **Data** sentence still says transactions are “to be aggregated,” although
the aggregation and evaluation are now complete. Update that current summary
to describe the acquired/aggregated panel, preserving the dated historical plan.
When reviews and reproduction finish, update the current status and add a dated
completion entry; do not rewrite the earlier uncertainty as foreknowledge.

“Other methods capture much more sales volume” is understandable in context,
but “other methods forecast totals much closer to recorded sales” would make
clear that these are predictions rather than actual business outcomes.

The retail study's evidence does not complete the remaining Atlas studies.
Root portfolio/README completion claims were not part of this review.

## Inspected SHA-256 identities

```text
7cc2937018564832c656dbed080dba3b7eba36c15327a87735addf0bcfcb5f68  reports/results/retail/REPORT.md
a0cb2c69370222904b3f0798069cd63bb0df6f44de8919636c53cbe9c8f391ff  reports/results/retail/metrics.json
7170a6f0d4cef2b390d5a04f9ebb3c5fee0c86c3fbfd0049df03607622ddc96b  reports/results/retail/run.json
ca96bcf0d9c4655635ab84e317126bb60038cbeee20112d4e61f6560211da2e6  reports/results/retail/predictions.csv.gz
0015d463a48c59bf9d30ce936c4df243a89126c847bf15195bdd6858f4d81350  reports/results/retail/per-product.csv
cd7d0e8be650b70e376c7595766414a8d0a1a621da950f047bbe41a29b1f5aa4  reports/results/retail/per-quarter.csv
d2261a87326367c7def22678a8199afb4235c1254ac0f28fc8d9988feaef89ce  reports/results/retail/weekly-sales.png
fde607a4c43cbb7c6c54cc12fa0bcdf5af627a594d94b43c5b34015e1ecd99c4  studies/retail/STORY.md
c99f629abc67df7eecf625f47bcdf8e294558f9a6a625747838bd48d317b7b53  data/snapshots/retail-daily-panel.csv.gz
```

2026-10-30, statistical reviewer: results approved; report content approved;
current story wording follow-up identified; exact reproduction pending. All
interpretations remain limited to this first frozen run and declared cohort.
