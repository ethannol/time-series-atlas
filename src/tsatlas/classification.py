"""Explicit denominators for binary indications, with undefined rates kept null."""
import numpy as np


def rate(numerator,denominator):return float(numerator/denominator) if denominator else None


def binary_scores(truth,prediction):
    y=np.asarray(truth);p=np.asarray(prediction)
    if y.ndim!=1 or y.shape!=p.shape or not np.isin(y,[0,1]).all() or not np.isin(p,[0,1]).all():
        raise ValueError('Binary scores require aligned known binary labels')
    y=y.astype(bool);p=p.astype(bool)
    tp=int((y&p).sum());tn=int((~y&~p).sum());fp=int((~y&p).sum());fn=int((y&~p).sum())
    recall=rate(tp,tp+fn);specificity=rate(tn,tn+fp)
    return {'n':len(y),'tp':tp,'tn':tn,'fp':fp,'fn':fn,'precision':rate(tp,tp+fp),'recall':recall,
            'false_positive_rate':rate(fp,fp+tn),'balanced_accuracy':(recall+specificity)/2 if recall is not None and specificity is not None else None}


def runs(mask):
    """Half-open start/end indices of consecutive true entries."""
    values=np.asarray(mask,dtype=bool)
    if values.ndim!=1:raise ValueError('Runs need a vector')
    edges=np.diff(np.r_[False,values,False].astype(int))
    return list(zip(np.flatnonzero(edges==1).tolist(),np.flatnonzero(edges==-1).tolist()))
