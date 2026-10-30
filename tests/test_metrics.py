import numpy as np
from tsatlas.metrics import interval_score, forecast_scores


def test_interval_score_penalizes_width_and_misses():
    assert np.allclose(interval_score([0,4,-2],[-1,-1,-1],[1,1,1]),[2,32,12])
    assert forecast_scores([0],[0],[-100],[100])['interval_score80']==200


def test_bias_keeps_sign_and_zero_targets_are_valid():
    result=forecast_scores([0,0],[1,3])
    assert result['mae']==2 and result['bias']==2


def test_invalid_shapes_and_interval_endpoints_cannot_silently_score():
    import pytest
    with pytest.raises(ValueError): forecast_scores([1,2],[[1],[2]])
    with pytest.raises(ValueError): forecast_scores([1,2],[1,2],[0,np.nan],[2,3])
    with pytest.raises(ValueError): forecast_scores([1],[1],upper=[2])


def test_panel_scoring_rejects_missing_predictions_and_duplicate_rows():
    import pandas as pd
    import pytest
    from tsatlas.electricity import summarize,MODELS
    f=pd.DataFrame({'hour':pd.to_datetime(['2014-01-01','2014-01-01 01:00'],format='mixed'),'client':['a','a'],'actual':[10.,20.]})
    for m in MODELS: f[m]=[10.,20.]
    means=pd.Series({'a':10.});peaks=pd.Series({'a':15.})
    assert summarize(f,means,peaks)['pooled_ridge']['aggregate_mae_kw']==0
    with pytest.raises(ValueError): summarize(pd.concat([f,f]),means,peaks)
    f.loc[0,'pooled_ridge']=np.nan
    with pytest.raises(ValueError): summarize(f,means,peaks)


def test_aggregate_score_sums_before_absolute_error():
    import pandas as pd
    from tsatlas.electricity import summarize,MODELS
    f=pd.DataFrame({'hour':pd.to_datetime(['2014-01-01']*2),'client':['a','b'],'actual':[10.,20.]})
    for m in MODELS: f[m]=[12.,18.]
    score=summarize(f,pd.Series({'a':10.,'b':20.}),pd.Series({'a':15.,'b':25.}))
    assert score['pooled_ridge']['aggregate_mae_kw']==0
    assert score['pooled_ridge']['customers']['a']['mae_kw']==2
