# Air-quality results and publication — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Results source: `89f0031ba2f232a84ba8639a53e32c2a0fea1487`.
Protocol: `715ac6c89b1948609c67626c883a4cc63ec3abde`.

Read the frozen design, report, metrics, run metadata, and current study story;
visually inspected the figure and inspected examples/schema from station and
quarter evidence. Hashed the linked evidence files to identify the reviewed
snapshot. This was a claims/readability review, not a row-by-row metric rebuild,
implementation audit, model run, or exact-reproduction check.

## Results/interpretation verdict

**The saved metrics support a bounded positive answer: contemporaneous peer
readings preserve more of the high-pollution classification signal than holding
the last local reading, in these simulated single-station outages.** Both network
methods beat persistence on the declared macro station balanced accuracy at all
three durations. For the simple peer median, the scores are 0.9384, 0.8460, and
0.8866 at 6, 24, and 72 hours, versus persistence's 0.8357, 0.7535, and 0.6451.
All twelve stations contribute to each primary average.

Learned ridge calibration changes balanced accuracy by less than 0.001 in either
direction at every duration. It reduces concentration MAE (12.8 versus 13.2,
19.0 versus 20.4, and 25.0 versus 27.9 micrograms/m³), which is a different
objective. The measured classification advantage mainly comes from using other
stations' current readings, not an established classification benefit of the
learned calibration. These are descriptive comparisons, not significance claims.

The report appropriately separates same-hour availability assumptions from a
future forecast, and a relative research threshold from a health or regulatory
threshold. It also keeps event misses beside delay. Median onset delay of zero
is conditional on detected, non-left-censored events; it does not imply all
events are detected. For example, the 72-hour peer-median run misses 43 of 187
block-local high events despite a zero median delay among 133 qualifying detected
onsets. Likewise, zero false-alert episodes for persistence does not mean zero
false-positive hours: a sustained alert can overlap true high hours and therefore
not meet this study's false-episode definition.

## Coverage and comparison boundaries

The denominator distinction is correct and worth keeping prominent. Peer inputs
are available in 100% of the prescheduled hours here. Scoreable coverage is
92.4%, 89.6%, and 73.6%, because scoring also needs complete local truth and a
preceding local reading. The lower 72-hour fraction is not evidence of peer-network
failure. Neither percentage establishes real operational uptime.

The 72-hour balanced accuracy exceeding the 24-hour value is not a causal benefit
of longer outages. The eligible blocks differ, extra hours change the target
distribution, and durations are dependent scenarios. The report already warns
about this cohort difference; preserve it beside the main interpretation. The
study also does not establish performance during correlated multi-station
failures or unknown event-dependent natural missingness.

## Publication verdict

**Results interpretation is acceptable within the above scope. Publication is
pending the direct answer and actual-run story below, plus separate reproduction
and release gates.** No model, tuning, or scoring change is requested.

### GAIR01 — Give the reader the actual answer before the tables

Priority: medium; status: identified.

The opening describes what kind of task this is but does not yet state what was
learned. Add a short answer saying that the peer median improves balanced accuracy
over the held local reading at every tested duration; learned calibration has
nearly the same classification score while lowering concentration error. Make
the comparison conditional on the simulated single-station schedule and current
peer reporting. State explicitly that the 72-hour versus 24-hour difference is
not a causal duration effect. The detailed table already supplies the numbers;
the opening need not repeat all twelve rows.

The plot uses readable labels and keeps performance separate from coverage.
The green peer-median and red learned-network series overlap almost completely,
so one appears absent. A short near-tie caption is sufficient; different marker
shapes or line styles would also help. This is an explanation/layout suggestion,
not a numerical concern or a reason to refit anything.

### GAIR02 — Complete the execution step in the process story

Priority: medium; status: pending parent update, known before this review.

The inspected story still says "design only" and ends at the dated planning
stage. Update current status and append the source/implementation/run/result
steps, linking the actual report and reviews. Explain in plain language what
the peer comparison found, why calibration did not materially improve the
classification objective, and why truth eligibility limits the answer. Keep
review/reproduction gates honestly pending until checked, retain dated planning
history, and do not imply that Ethan performed agent-authored numerical work or
that the remaining collection is complete.

## Inspected SHA-256 hashes

The full prediction/event/parameter and subgroup files are identified as linked
evidence; hashing them does not imply a complete row-by-row content audit.

```text
06bb7d366a2f9b6efbf94d03f292661f571c61a13ba9d709bd23ca311c387664  reports/results/air-quality/REPORT.md
21c4e8fbe9c6804cd15628fa023d2e3633f0c1eeebb9b040c1d89a5860497ffd  reports/results/air-quality/metrics.json
c0fe245ef25a72d39aea2a8729fbc14139b95e3e790cbddfc2d8551ee5740ea0  reports/results/air-quality/outage-warnings.png
d5d2e37bfa3cdd3f47d8b07302f54c39fd7913473e242b0e8636eca9cb7fda4b  reports/results/air-quality/run.json
2792d1cf8e45ad6b9df123161cd06236a7fea3cb59cd061eb105d7b4d4c19a47  reports/results/air-quality/available-hour-scores.csv
1e90e651ffee8219cd7ec176c06bf8833dda9972da2b0f74f2e69d6d13fbac14  reports/results/air-quality/events.csv.gz
66479107f6c560c17321da6a3bad46b4dd8bd4fcb78a8c11387e0f34cf57affe  reports/results/air-quality/outages.csv
c5d5bf97101dcb31042369133f83da76f8a785a104b9d4023132f0ed942d36ad  reports/results/air-quality/parameters.json
e04843cb83cc6e81274d05ed0c0abab7102a931b07d2f60b0c30b5920372bf01  reports/results/air-quality/predictions.csv.gz
cc2f9de86546188238b7b8a9b41380c3d7af071f6e4abf28b0d84b6665f6de5e  reports/results/air-quality/quarter-scores.csv
2792d1cf8e45ad6b9df123161cd06236a7fea3cb59cd061eb105d7b4d4c19a47  reports/results/air-quality/station-scores.csv
734e21cddbee577d55e8d6ac470b26fd6bae262144d12ae4785d3163a31a498a  studies/air-quality/STORY.md
1882931a691d8da2df1bd2532011a0f4aff55b2e12e2e60d00f1156d991e2b32  studies/air-quality/DESIGN.md
```
