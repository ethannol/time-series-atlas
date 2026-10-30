"""Scores in declared units; no cross-task composite leaderboard."""
import numpy as np


def interval_score(actual, lower, upper, alpha=.2):
    actual, lower, upper = map(np.asarray, (actual, lower, upper))
    if np.any(upper < lower) or not 0 < alpha < 1:
        raise ValueError('Invalid interval or alpha')
    return upper-lower + (2/alpha)*np.maximum(lower-actual, 0) + (2/alpha)*np.maximum(actual-upper, 0)


def forecast_scores(actual, prediction, lower=None, upper=None):
    actual, prediction = np.asarray(actual), np.asarray(prediction)
    if len(actual) == 0 or not np.isfinite(actual).all() or not np.isfinite(prediction).all():
        raise ValueError('Scores require nonempty finite observations and predictions')
    result = {'n':len(actual), 'mae':float(np.mean(np.abs(prediction-actual))), 'bias':float(np.mean(prediction-actual))}
    if lower is not None:
        lower, upper = np.asarray(lower), np.asarray(upper)
        result.update(coverage80=float(np.mean((actual>=lower)&(actual<=upper))),
                      width80=float(np.mean(upper-lower)), interval_score80=float(interval_score(actual,lower,upper).mean()))
    return result
