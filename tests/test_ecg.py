import numpy as np
import pytest
from tsatlas.ecg import fold_indices,beat_features,classification_scores


def test_shared_patient_records_are_never_split_and_cap_is_per_person():
    beats=np.array([('201','201'),('202','201'),('100','100'),('101','101')]*8,dtype=[('record','U3'),('person','U3')])
    mapping={'201':0,'100':1,'101':2}
    train,test=fold_indices(beats,mapping,0,cap=5)
    assert set(beats['record'][test])=={'201','202'}
    assert not(set(beats['person'][train])&set(beats['person'][test]))
    assert len(train)==10
    np.testing.assert_array_equal(train,fold_indices(beats,mapping,0,cap=5)[0])


def test_beat_normalization_is_local_and_preserves_declared_extra_features():
    wave=np.vstack([np.arange(60),np.arange(60)+10.]);rr=np.array([1.,.5])
    shape,extra=beat_features(wave,rr)
    np.testing.assert_allclose(shape[0],shape[1]);assert extra[1,1]==pytest.approx(np.log(.5))
    wave[1]*=999;shape2,_=beat_features(wave,rr);np.testing.assert_array_equal(shape[0],shape2[0])


def test_class_absence_is_visible_and_unknown_labels_fail():
    scores=classification_scores(['N','N'],['N','N'])
    assert scores['accuracy']==1 and scores['macro_f1']==.25 and scores['supported_macro_f1']==1
    assert scores['per_class'][1]['recall'] is None and scores['per_class'][1]['precision'] is None
    with pytest.raises(ValueError):classification_scores(['N'],['unknown'])
