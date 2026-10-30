import numpy as np
from tsatlas.metrics import interval_score, forecast_scores


def test_interval_score_penalizes_width_and_misses():
    assert np.allclose(interval_score([0,4,-2],[-1,-1,-1],[1,1,1]),[2,32,12])
    assert forecast_scores([0],[0],[-100],[100])['interval_score80']==200


def test_bias_keeps_sign_and_zero_targets_are_valid():
    result=forecast_scores([0,0],[1,3])
    assert result['mae']==2 and result['bias']==2
