import numpy as np
import pandas as pd
from tsatlas.river_flow import features,split_masks,event_ledger


def fixture():
    index=pd.date_range('2004-12-01',periods=60)
    return pd.DataFrame({'flow_cfs':np.arange(60)+1.,'qc':'A','precip_mm':1.,'tmax_c':10.,'tmin_c':2.},index=index)


def test_future_weather_and_flow_cannot_enter_earlier_features():
    f=fixture();a=features(f)
    f.iloc[30:,f.columns.get_indexer(['flow_cfs','precip_mm','tmax_c','tmin_c'])]=9999
    b=features(f);pd.testing.assert_frame_equal(a.iloc[:30],b.iloc[:30])
    f=fixture();f.loc[f.index[20],'qc']='A:e';x=features(f)
    assert x.flow_mean7.iloc[20:27].isna().all()


def test_three_day_split_cannot_see_later_calibration_outcomes():
    origin=pd.date_range('2004-12-28','2005-01-02')
    for h,expected in [(1,pd.Timestamp('2005-01-01')),(3,pd.Timestamp('2005-01-03'))]:
        target=origin+pd.Timedelta(days=h)
        _,_,test=split_masks(origin,target,'1999-12-31','2004-12-31','2014-12-31')
        assert target[test].min()==expected
        assert (origin[test]>=pd.Timestamp('2004-12-31')).all()


def test_onset_scoring_keeps_misses_and_separates_persistence():
    index=pd.date_range('2004-12-25',periods=20)
    f=pd.DataFrame({'flow_cfs':1.,'qc':'A'},index=index)
    f.loc['2005-01-03':'2005-01-05','flow_cfs']=10.
    targets=pd.date_range('2005-01-01','2005-01-13')
    pred=pd.DataFrame({'model':'fixture','target_date':targets,'alert':False})
    events=event_ledger(f,pred,5.,'test',3);high=events[events.type=='high_run']
    assert len(high)==1 and bool(high.eligible_onset.iloc[0]) and not bool(high.alerted_onset.iloc[0])
    # A preceding high day makes the apparent later transition continuation, not a new onset.
    f.loc['2005-01-02','flow_cfs']=10.
    events=event_ledger(f,pred,5.,'test',3)
    assert events[events.type=='high_run'].event_start.iloc[0]==pd.Timestamp('2005-01-02')


def test_unknown_following_truth_censors_event_and_alert_segment():
    index=pd.date_range('2004-12-25',periods=20)
    f=pd.DataFrame({'flow_cfs':1.,'qc':'A'},index=index)
    f.loc['2005-01-03':'2005-01-04','flow_cfs']=10.
    f.loc['2005-01-05','qc']='A:e'
    dates=pd.date_range('2005-01-01','2005-01-13')
    p=pd.DataFrame({'model':'fixture','target_date':dates,'alert':dates==pd.Timestamp('2005-01-06')})
    events=event_ledger(f,p,5.,'test',3)
    high=events[events.type=='high_run'].iloc[0]
    assert high.right_censored and high.origin==pd.Timestamp('2004-12-31') and high.target_date==pd.Timestamp('2005-01-03')
    assert (events.type=='unresolved_alert_segment').sum()==1
    assert not (events.type=='false_alert_episode').any()
