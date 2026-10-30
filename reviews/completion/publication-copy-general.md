# Publication copy preflight — general review

Reviewer: `/root/general_critic`, separate automated reviewer.
Date: 2026-10-30.
Scope: `data/README.md`, `docs/METHODS.md`, river/ECG report-generating text and
current stories; existing CO₂/electricity reports as method-coverage evidence.
Checked the official UCI creator/citation entry for the attribution below.
No project copy, code, model, test, or generated report was changed by this review.

**Verdict: the new structure and revised river/ECG answers are suitable, with the
copy corrections below. This is source-copy review only; generated reports and
figures, numerical-artifact preservation, reproduction and final publication
remain pending.**

## Required corrections

1. **PCG01 — Electricity intervals are an unevaluated capability.** The method
   guide lists "calibrated residual intervals" in the electricity row, but the
   executed report explicitly states that no intervals are claimed. Remove that
   item from electricity; CO₂ has the interval evaluation. If the row is intended
   as the complete model list, include yesterday's persistence alongside last
   week's. Change "score people" to "score customers" to match the unit observed.

2. **PCG02 — Correct the air-quality creator's name.** `data/README.md` says
   "Song and Chen (2017)". The official source lists one creator, Song Chen, with
   the citation Chen, S. (2017). Use that attribution. This is a checked source
   fact, not a new ambiguity in reuse rights.
   [Official UCI creator/citation](https://archive.ics.uci.edu/dataset/501/beijing%2Bmulti%2Bsite%2Bair%2Bquality).

3. **PCG03 — Preserve the distinction between the river score populations.**
   The new numerical opening correctly shows a small weather gain, the onset
   counts, and false-alert burden. Its sentence "Continued high flow is easier
   to recognize than a new rise" is broader than the displayed direct contrast:
   the high-day score includes onsets, weights gauges equally, and uses a
   different cohort from pooled eligible onsets. State the demonstrated result
   instead: high-day recall did not translate into equally high eligible-onset
   recall. The later denominator explanation is good and should remain.

## Small presentation/status items to finish with regeneration

- River's `model.replace('_', ' + ')` produces "flow + only". Use an explicit
  readable label map for last-flow score, flow only, and flow plus past weather;
  the table can use the same names. This is a label correction, not a model change.
- The method guide currently calls the spectral methods "actually evaluated"
  and links a report that does not yet exist. Keep the row pending until the
  promised execution and review have happened. If both occur before this copy is
  published, resolve the status against that evidence rather than adding stale
  pending language to the final document.
- Air quality is a same-hour nowcast under the stated peer-arrival assumption.
  That description is precise in the guide row; use it consistently in the
  introductory task list and data credits so "reconstruction" is not read as
  using post-outage endpoints. Existing limitations already exclude that use.

## What the revisions now do well

The credits cover every observational source, transformations and cohort scope,
generated controls, oil's fetch-only limitation, and the CAMELS member-level
integrity boundary. This general review does not re-audit every licence or
transformation claim; the linked source reviews remain the technical basis.
The compact question/quality/method table supplies the previously missing route
through the collection without creating a universal leaderboard or counting
deferred methods as accomplishments.

River's current story has the selected panel, execution status, small weather
gain and increased alert-episode burden; it preserves the pre-run boundary
correction and acknowledged missed review. ECG now leads with uneven transfer,
the majority-accuracy comparison, S/F failures, readable benchmark groups, and
rare-class concentration in the frozen split. Its story identifies the retained
44-record/43-person cohort and inputs beyond shape. Both keep reproduction and
publication pending. These source changes address GRIV02/GECG02 and the main
GRIV01/GECG01 requests, subject to the small river wording correction and later
inspection of the actual regenerated artifacts.

## Inspected source-copy hashes

```text
b3e563e699bbe9fe1b1b55d763bc98f4d3e6fddd59b08a1b982869ac8cb137de  data/README.md
7dbe843839a088635ca7e33cb427a14a9c598e510ff46f4a8a5ce5ef238c4a89  docs/METHODS.md
7f2799251a0af2ad0c26d68c9f48ed98871abe7e770c387a4ea0249d9c74a545  src/tsatlas/river_flow.py
e22c1ca033feb5ca17d2fba32c3417a108c447260105caebbe07d64f5e9a062b  src/tsatlas/ecg.py
dc4dcb282eb44726d551372529c14dde56fc1c1d0c432d9bcfdb2398a1d979ea  studies/river-flow/STORY.md
5518625c5a45ea56c5d6079cf9876dc022ff67ddb96f3327236cfe84105a8f6d  studies/ecg/STORY.md
```

## 2026-10-30 — Immediate copy-fix recheck

Re-read the changed method guide, air-quality credit and river label mapping.
**PCG01's substantive capability error and PCG02's creator attribution are
verified corrected in source copy.** Electricity no longer claims interval
evaluation and now lists both persistence baselines; intervals are assigned to
CO₂. The creator is identified as the single person Song Chen. These were actual
copy errors caught before publication, not hypothetical design risks.

The explicit river legend map also removes the "flow + only" artifact at source
level. Rendered-figure verification still follows regeneration. The small
"score people" wording remains in the electricity guide row. PCG03's river
comparison sentence remains pending at this recheck, and spectral evaluated
status still requires its actual run/review. No final publication verdict is
being issued by these scoped source-copy closures.

```text
b0634ffa29493a7a300b832d7b9679a5fc92034d04e7d8e3c7df4fc23fa50afc  data/README.md
498f05dcabe54eef79d0bc90b683a784cea6aa40480127a8437ff99dfd24d27a  docs/METHODS.md
04fae88b90b9f112cc42a9814fb94406b9ea67353b29aa6a7d8d1879cd5107d0  src/tsatlas/river_flow.py
```
