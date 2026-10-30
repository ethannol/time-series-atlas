# Oil prices: frozen study contract

Draft for independent source/design review; no candidate models have run.

## Question and data

Can changes in uncertainty be forecast usefully when price direction remains
hard to predict? This supports understanding risk-model behavior, without a
trading, savings, or calibrated monetary-risk claim. Direction and volatility
are different tasks with separate scores; never compare their score magnitudes.

Use the pinned EIA WTI and Brent daily spot-price XLS files (Data 1, header row3),
freely accessible through EIA, which identifies Refinitiv as the price source.
EIA's generic reuse policy does not resolve third-party redistribution rights.
Keep raw workbooks, the normalized price input and the full true-change series
locally, outside Git. Publish our forecasts, score summaries, parameters and
hashes; reconstruct true changes locally when rescoring. Do not relabel the
underlying prices as government-owned or openly licensed. Source manifests and audit are in
`data/manifests/oil.json` and `reports/intake/oil.json`. Analysis ends 2025-12-31.
WTI includes a negative price on 2020-04-20: use dollar-per-barrel first
differences, never log returns or silent deletion of the episode.

Keep each market's own observed dates, no forward-fill and no artificial weekend
zeros. Target is next observed price change, after the current observed price
is assumed available. It is not a fixed calendar-day horizon. Save calendar-gap
length and show scores for gaps at most four days versus longer gaps. Revised
historical prices and unknown publication latency prevent literal real-time claims.

## Splits and models

Fit on observations 2000-01-01 through 2014-12-31; test 2015-01-01 through
2025-12-31. Prior data are retained for provenance but not fitted. No validation
tuning; all settings declared here. Fit separately for WTI and Brent.

Variance forecasts for the squared dollar change: fixed training mean square,
trailing 60 observed squared changes, EWMA with decay0.94, and zero-mean
GARCH(1,1). GARCH fit once on training observations by Gaussian quasi-likelihood,
constraints omega>0, alpha>=0, beta>=0, alpha+beta<=0.999; starting points
(alpha,beta)=(0.05,0.9),(0.1,0.8),(0.15,0.7), omega initialized to training
mean squared change*(1-alpha-beta). Choose smallest converged training objective only.
Save optimizer outcomes; a failure remains a reported failure. All recursions
update after observing each new change, never before scoring that change.
Variance floor1e-8 USD²/barrel² is a numerical safeguard recorded explicitly.

Compute changes on each entire observed series before assigning membership by
the target observation's date; the first 2000 change may use the final1999 price.
Pre-2000 changes may supply rolling/lag feature warm-up only; no pre-2000 target
enters a fitted objective, prevalence, scale or initial-variance statistic.
Use the training mean squared change as initial variance for both recursions,
then process every training change in chronological order to obtain the first
test variance. At index t, h[t]=omega+alpha*change[t-1]²+beta*h[t-1];
EWMA uses h[t]=0.94*h[t-1]+0.06*change[t-1]². During GARCH training, h[0]
is fixed to the training mean square. Minimize the mean objective via SLSQP,
max_iter500, ftol1e-9; save all three attempts and require success, finite
objective and constraint satisfaction. Standardize changes by training RMS
inside optimization for conditioning and convert omega/variance back to dollars.

Direction: training upward-change prevalence baseline versus logistic regression
(C1, standardized training features, max_iter1000). Features available at origin:
last change, mean of last5 changes, mean of last20, standard deviation of last20,
and current price. Label is strictly positive next change; zero joins non-upward.
Model fitted once on training examples with complete past features. No class
reweighting, threshold tuning, or model selection on final outcomes.
Both direction models use identical complete-feature training rows and identical
test rows. Rolling standard deviation uses population denominator ddof0.

## Evidence

Primary variance score: mean log(v)+change²/v, reported per market with paired
differences against the fixed variance. Also variance-proxy MAE, annual score,
and predeclared 2020 versus other-year breakdown. Squared changes are a noisy
proxy for latent volatility. No implication of calibrated tail probabilities.
Direction primary score Brier; also accuracy at0.5 and confusion counts. Annual
scores reveal instability; they do not establish profitable direction prediction.
Save all dated predictions, outcomes, gaps, parameters and optimizer diagnostics.
True change/price outcomes stay in ignored local evidence. Public files contain
original forecasts, date/gap identifiers, outcome hashes and aggregate scores.
Free source acquisition may later return revised data: require the normalized
through2025 analysis-input hash to match before claiming exact reproduction.
This explicit public acquisition limitation does not block local exact reproduction.

## Gates and deviations

Freeze after actual-file source/design reviews; implementation review precedes
full test scoring. Later choices must be recorded as protocol deviations with
whether results had already been inspected. Record the protocol commit.
