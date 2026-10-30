import numpy as np
import pandas as pd
from tsatlas.co2 import predict
from tsatlas.electricity import features,fit_month,safe_hours
from tsatlas.synthetic import first_alarm,scores,summarize


def test_co2_recovers_linear_seasonality_and_ignores_future():
    idx=pd.date_range('1980-01-01','2010-12-01',freq='MS')
    y=300+np.arange(len(idx))/6+2*np.sin(2*np.pi*idx.month/12)
    frame=pd.DataFrame({'average':y,'usable':True},index=idx)
    origin=pd.Timestamp('2000-12-01'); target=pd.Timestamp('2003-12-01')
    result=predict(frame,origin,target,'linear_expanding')
    assert abs(result-frame.loc[target,'average'])<1e-8
    frame.loc[frame.index>origin,'average']=1e9
    assert predict(frame,origin,target,'linear_expanding')==result


def test_forecast_day_features_never_use_that_days_values():
    idx=pd.date_range('2012-01-01',periods=24*30,freq='h')
    series=pd.Series(np.arange(len(idx),dtype=float),index=idx)
    before=features(series).loc['2012-01-20'].copy()
    series.loc['2012-01-20':]=1e9
    pd.testing.assert_frame_equal(features(series).loc['2012-01-20'],before)


def test_monthly_training_cannot_see_future_and_shared_model_handles_clipping():
    idx=pd.date_range('2012-01-01','2013-01-31 23:00',freq='h')
    y=10+np.sin(2*np.pi*idx.hour/24)
    panel=pd.DataFrame({'a':y,'b':y*10},index=idx)
    before,params=fit_month(panel,pd.Timestamp('2013-01-01'))
    assert all(x['last_train']<'2013-01-01' for x in params['local'])
    panel.loc['2013':]=1e5
    after,_=fit_month(panel,pd.Timestamp('2013-01-01'))
    for c in ['local_ridge','pooled_ridge']:
        np.testing.assert_allclose(before.loc[before.hour<'2013-01-02',c],after.loc[after.hour<'2013-01-02',c])
        assert (before[c]>=0).all()


def test_dst_exclusion_covers_target_plus_longest_lag():
    idx=pd.date_range('2014-03-29','2014-04-15',freq='h')
    flags=pd.Series(safe_hours(idx),index=idx)
    assert not flags.loc['2014-03-30':'2014-04-13'].any()
    assert flags.loc['2014-04-14'].all()


def test_alarm_is_strict_and_score_uses_frozen_baseline():
    assert first_alarm(np.array([1,2,3]),2)==102
    assert first_alarm(np.array([1,2]),2) is None
    x=np.tile([-1.,1.],200)
    before=scores(x)
    x[201:]+=1e4
    for m in before: np.testing.assert_allclose(before[m][:101],scores(x)[m][:101])


def test_detection_partition_includes_early_and_missed_runs():
    f=pd.DataFrame({'method':['cusum']*3,'rho':[0.]*3,'shift':[True]*3,'alarm':[150,210,np.nan]})
    s=summarize(f)['cusum/rho=0.0/shift']
    assert (s['prechange_alarms'],s['eligible'],s['detections'],s['misses'])==(1,2,1,1)
    assert s['eligible_detection_rate']==.5 and s['median_detected_delay']==10
