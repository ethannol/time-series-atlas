import numpy as np
import pandas as pd
from tsatlas.air_quality import network_features,event_rows,outage
from tsatlas.classification import binary_scores


def test_hidden_station_values_never_enter_network_features():
    index=pd.date_range('2015-01-01',periods=8,freq='h');panel=pd.DataFrame(np.arange(40).reshape(8,5),index=index,columns=list('abcde'))
    a,ca=network_features(panel,'a');panel['a']=999999;b,cb=network_features(panel,'a')
    pd.testing.assert_frame_equal(a,b);pd.testing.assert_series_equal(ca,cb)
    panel[['b','c','d']]=np.nan;_,count=network_features(panel,'a');assert (count==1).all()


def test_absent_class_has_undefined_balanced_accuracy():
    scores=binary_scores([0,0],[0,0]);assert scores['balanced_accuracy'] is None and scores['recall'] is None and scores['precision'] is None


def test_outage_predictions_ignore_hidden_truth_and_later_endpoint():
    class Identity:
        def predict(self,x):return x['median'].to_numpy()
    times=pd.date_range('2015-01-01',periods=48,freq='h')
    panel=pd.DataFrame(np.arange(240).reshape(48,5),index=times,columns=list('abcde'))
    fitted={'model':Identity(),'calendar':pd.Series(dtype=float),'fallback':10.,'threshold':20.}
    a,ledger=outage(panel,'a',times[24],6,fitted)
    panel.loc[times[24]:,'a']=99999
    b,_=outage(panel,'a',times[24],6,fitted)
    np.testing.assert_array_equal(a.prediction,b.prediction)
    assert len(a)==6*4 and a.hour.max()==times[29] and ledger['end_exclusive']==times[30]
    panel.loc[times[25],'a']=np.nan
    missing,ledger=outage(panel,'a',times[24],6,fitted)
    assert missing is None and not ledger['eligible'] and ledger['peer_available_hours']==6


def test_event_misses_censoring_delays_and_false_episodes():
    times=pd.date_range('2016-01-01',periods=10,freq='h')
    frame=pd.DataFrame({'station':'a','start':times[0],'duration':10,'model':'test','hour':times,'threshold':1,
                        'observed':[2,2,0,0,2,2,0,2,2,0],'prediction':[2,0,2,0,0,2,0,np.nan,0,0]})
    events=event_rows(frame);high=events[events.type=='high_event']
    assert len(high)==3 and high.left_censored.sum()==1
    assert list(high.detected)==[True,True,False]
    assert high.delay_hours.dropna().tolist()==[1.]
    assert (events.type=='false_alert').sum()==1
