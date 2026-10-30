import numpy as np
import pandas as pd
import pytest
from tsatlas.oil import variance_path,direction_features,qlike


def test_variance_and_direction_only_use_previous_observations():
    changes=np.array([1.,2.,-3.,4.,5.]);a=variance_path(changes,.1,.2,.7,2.)
    assert a[0]==2 and a[1]==pytest.approx(.1+.2+1.4)
    changes[3:]=1000;b=variance_path(changes,.1,.2,.7,2.)
    np.testing.assert_array_equal(a[:4],b[:4])
    p=pd.Series(np.arange(50,dtype=float),index=pd.bdate_range('2000-01-01',periods=50));a=direction_features(p)
    p.iloc[30:]=-1000;b=direction_features(p)
    pd.testing.assert_frame_equal(a.iloc[:31],b.iloc[:31])


def test_negative_price_changes_remain_finite_without_logs():
    p=pd.Series([20.,-36.98,10.]);assert np.isfinite(p.diff().dropna()).all()
    assert np.isfinite(qlike(p.diff().dropna(),[2.,3.]))
    for bad in [[0.,1.],[np.nan,1.],[[1.,2.]]]:
        with pytest.raises(ValueError):qlike([1.,2.],bad)


def test_variance_floor_keeps_dollar_units_after_standardization():
    changes=np.array([.01,.02,.03]);scale=100.
    raw=variance_path(changes,1e-12,0.,0.,1e-12)
    standardized=variance_path(changes/scale,1e-12/scale**2,0.,0.,1e-12/scale**2,floor=1e-8/scale**2)
    np.testing.assert_allclose(raw,standardized*scale**2,rtol=1e-12)


def test_private_evidence_does_not_replace_previous_run(tmp_path,monkeypatch):
    import tsatlas.oil as oil
    monkeypatch.setattr(oil,'ROOT',tmp_path)
    old=oil.save_private(pd.DataFrame({'outcome':[1.]}),'fixture')
    before=(tmp_path/old['path']).read_bytes()
    new=oil.save_private(pd.DataFrame({'outcome':[2.]}),'fixture')
    assert old['path']!=new['path']
    assert (tmp_path/old['path']).read_bytes()==before
