"""Scores in declared units; invalid/misaligned arrays fail rather than broadcast."""
import numpy as np


def matched(*values):
    arrays=[np.asarray(v,dtype=float) for v in values]
    if not arrays or any(a.ndim!=1 or a.shape!=arrays[0].shape or not len(a) or not np.isfinite(a).all() for a in arrays):
        raise ValueError('Scores require finite nonempty matched one-dimensional arrays')
    return arrays


def interval_score(actual,lower,upper,alpha=.2):
    actual,lower,upper=matched(actual,lower,upper)
    if np.any(upper<lower) or not 0<alpha<1: raise ValueError('Invalid interval or alpha')
    return upper-lower+(2/alpha)*np.maximum(lower-actual,0)+(2/alpha)*np.maximum(actual-upper,0)


def forecast_scores(actual,prediction,lower=None,upper=None):
    actual,prediction=matched(actual,prediction)
    result={'n':len(actual),'mae':float(np.mean(np.abs(prediction-actual))),'bias':float(np.mean(prediction-actual))}
    if (lower is None)!=(upper is None): raise ValueError('Both interval bounds are required')
    if lower is not None:
        actual,lower,upper=matched(actual,lower,upper)
        score=interval_score(actual,lower,upper)
        result.update(coverage80=float(np.mean((actual>=lower)&(actual<=upper))),
                      width80=float(np.mean(upper-lower)),interval_score80=float(score.mean()))
    return result
