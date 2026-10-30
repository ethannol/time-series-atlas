import numpy as np
import pandas as pd
import pytest
from tsatlas.retail import intermittent_rates,forecast,predict


def test_tsb_decays_during_inactivity_while_croston_does_not():
    history=np.tile([0.,0.,0.,4.],20)
    before=intermittent_rates(history);after=intermittent_rates(np.r_[history,np.zeros(50)])
    assert after[0]==before[0]
    assert after[1]==pytest.approx(before[1]*.9**50)
    assert forecast(np.zeros(40))==dict.fromkeys(['zero','last_week','rolling_28','croston_sba','tsb'],0.)


def test_target_and_future_mutations_cannot_change_weekly_forecast():
    index=pd.date_range('2009-12-01','2011-01-16');panel=pd.DataFrame({'item':np.arange(len(index))%5},index=index)
    origin=pd.Timestamp('2011-01-03');a=predict(panel,[origin])
    panel.loc[origin:,'item']=9999;b=predict(panel,[origin])
    np.testing.assert_array_equal(a.prediction,b.prediction)
    assert (a.observed!=b.observed).all()
    assert b.observed.eq(7*9999).all()


def test_sales_validation_rejects_unknown_or_signed_values():
    for bad in [[1,np.nan],[1,-1],[[1,2]]]:
        with pytest.raises(ValueError):intermittent_rates(bad)
