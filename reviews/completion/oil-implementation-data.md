# Oil pre-run implementation and acquisition review

Date: 2026-10-30. Reviewer: AI subagent `/root/implementation_critic`.
Scope: oil implementation against its frozen contract, fetch-only input/output
boundary, source acquisition guard, and bounded invariant tests. The reviewer
did not author implementation, run the full study, or compute 2015–2025 scores.
The active completion suite retains the parent's fresh baseline `bd85e01` and
fetch time recorded in the source manifests.

**Pre-run verdict: pass from the implementation perspective.** Commit the
reviewed source before a full run, satisfy the separate statistical review,
and retain the updated finite-only development trial. Results, public claims,
and clean-checkout reproduction remain later checkpoints.

## Information boundaries and computation

Each market drops only its own absent observations before computing dollar
changes. Negative prices remain; neither log returns nor weekend filling is
introduced. Target-date membership starts in 2000, with earlier observations
used only for lag warm-up. Training RMS, initial variance, GARCH objective,
direction prevalence, feature standardization, and logistic fitting use the
declared training interval. The two direction methods share their eligible rows.

Variance forecasts consume the previous change, while direction features shift
all change summaries and the price by one observed row. Training recursions
continue into evaluation without refitting parameters. Three declared GARCH
starts are attempted, diagnostics retained, and only a converged constraint-valid
training objective can select the result. Failure of every start raises rather
than silently substituting a model. QLIKE rejects mismatched/nonfinite inputs
and nonpositive variances. Annual, 2020, and gap-based summaries are separate
from direction scores; direction now also retains its gap breakdown.

The existing study-scoped input checks and committed-source/stable-source
guards remain in use. Public predictions omit actual dollar changes and
direction labels. Complete outcomes are stored under ignored `data/processed`;
public metrics identify those private evidence files and hashes. This verifies
the declared fetch-only boundary, not a new license determination.

## Findings and verification history

### C-I06 — Keep the variance floor in declared physical units

Status history: `identified` → `fixed` → `verified`, 2026-10-30.
The first inspected implementation applied `1e-8` to standardized variances
inside optimization as well as dollar-unit variances outside it. That made the
effective dollar floor depend on training RMS. The correction adds an explicit
floor parameter and uses `1e-8 / RMS²` inside the standardized objective.
The inspected test verifies conversion back to dollars with a non-unit scale.
This is a numerical contract correction before final evaluation, not an
observed effect on comparative performance.

### C-I07 — Preserve earlier private outcomes when a later run fails

Status history: `identified` → `fixed` → `verified`, 2026-10-30.
The first implementation wrote fixed-name private outcome files before public
output promotion, so a later failure could overwrite the evidence behind an
older successful report. Private evidence now uses content-addressed immutable
paths. New contents obtain a new path; an existing corrupt path raises. The
preservation test confirms writing different later contents leaves the original
bytes intact. A failed run may leave an unreferenced ignored file, but does not
replace the preceding report's outcome evidence.

The reviewer independently ran `pytest -q tests/test_oil.py`: **4 passed**.
These cover causal perturbation, negative-price handling and score validation,
floor-unit equivalence, and immutable private evidence. No full evaluation was
invoked by the tests.

## Revised-workbook acquisition probes

In temporary directories, the reviewer supplied the actual original workbook
dataframes through a mocked workbook reader and mocked network write. Changing
only observations after 2025 preserved the normalized input hash and was
accepted with `raw_bytes_match_original: false`. Changing January 2001 prices
raised the explicit historical-revision error and promoted no normalized input.
Both probes passed without downloads or changes to the real source files.

These checks verify the guard's behavior, not future upstream availability.
Exact new-user reproduction still depends on a provider workbook whose
historical window normalizes to the pinned bytes; historical revisions can make
that unavailable. Existing local exact input remains separately verifiable.

The initially inspected development-trial record refers to earlier oil source
hash `c7701a0…`, with finite-only January 2004 outputs and no accuracy scores.
It is not execution evidence for the corrected source below. The author is
refreshing that bounded trial; retain its actual revision rather than silently
treating the old record as current.

## Inspected hashes

```text
d3ab40ec71bae9cb94ac30829ae2dece45a124899f611cc8794663efb5456bf5  src/tsatlas/oil.py
b15b13e15064526b97e8615581521147800704caed6587ad933b85fe11517fe3  src/tsatlas/acquire.py
95a699e75a84da2651dc70268c942232abb62c7cdbd75f6e0454dc14788d3468  src/tsatlas/common.py
a57144b965db2d23066ec3a96e88ab7e8ade6edffc248382edb6691cda0ffb4d  src/tsatlas/data.py
cf44f073a01162c95a42c1f130e3f6c13337311fd7a1f0fde7f66a0aa959202a  tests/test_oil.py
64e2b98cd9f2a653bd8444412be50500a4007a211560045390e8f16e7515b2ef  studies/oil/DESIGN.md
0024217008da826cf749bee93fbe85200f5ce9abf8526e49616b804b911b3990  data/manifests/oil.json
a3a388c33094c2bd00af2cddb12ed32a634b161956c7040dbf49e03c4b39aa00  reports/intake/oil.json
d138ce02b7d858fd579c1570a65db3e7f23a900f2728b2e866a96496aa273cd9  data/processed/oil-daily.csv.gz
eeb0237ba442c2e604f44dc6cfe5a0a0a180223816b1072f9539de5e10d0c7c4  reports/verification/oil-development-trial.json
```

## 2026-10-30 — Updated bounded-trial evidence inspected

The refreshed author trial, timestamp `2026-10-30T21:54:06.102235+00:00`, names
the inspected `d3ab40e…` source. It retains training through 2003 and finite-only
January 2004 outputs, three successful GARCH starts, and explicitly states no
accuracy scores were computed. The record explains why the trial was repeated.
This closes the stale development-evidence observation; the pre-run verdict
above stands. The reviewer inspected this record rather than rerunning a fit.

```text
d49a8218ceb13370113505f102986e296984c77f0ecc1a0e1db75bcfc7622ec6  reports/verification/oil-development-trial.json
```
