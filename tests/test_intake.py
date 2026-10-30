import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from tsatlas.data import co2_frame, quarter_to_hour, cohort, dst_days, verify_raw


def test_end_labels_keep_last_midnight_in_previous_day():
    frame=pd.DataFrame({'power':[4.,8.,12.,16.]},index=pd.date_range('2014-12-31 23:15',periods=4,freq='15min'))
    result=quarter_to_hour(frame)
    assert result.index[0]==pd.Timestamp('2014-12-31 23:00')
    assert result.iloc[0,0]==10.  # mean kW, NOT sum or kWh/quarter
    with pytest.raises(ValueError): quarter_to_hour(frame.iloc[:-1])


def test_quality_flags_do_not_confuse_scripps_with_noaa(tmp_path):
    p=tmp_path/'co2.txt'
    p.write_text('1974 4 1974.3 330 330 -1 -9.99 -0.99\n1974 5 1974.4 331 331 2 -9.99 0\n1974 6 1974.5 332 332 20 1 .1\n')
    frame=co2_frame(p)
    assert frame.unknown_scripps_metadata.tolist()==[True,False,False]
    assert frame.quality_suspect.tolist()==[False,True,False]
    assert frame.usable.tolist()==[False,False,True]


def test_cohort_cannot_use_future_values():
    idx=pd.date_range('2011-01-01','2014-12-31 23:00',freq='h')
    frame=pd.DataFrame(np.broadcast_to(np.arange(1,31),(len(idx),30)),index=idx)
    before=cohort(frame)
    frame.loc['2013':]=np.random.default_rng(5).normal(size=frame.loc['2013':].shape)
    assert cohort(frame)==before


def test_dst_mask_does_not_depend_on_zero_values():
    idx=pd.to_datetime(['2012-03-25 00:00','2012-03-26','2014-10-26'],format='mixed')
    assert dst_days(idx).tolist()==[True,False,True]


def test_changed_raw_bytes_are_rejected(tmp_path):
    (tmp_path/'data/raw').mkdir(parents=True)
    (tmp_path/'data/raw/input').write_text('changed')
    (tmp_path/'data/manifest.json').write_text(json.dumps({'files':{'input':{'sha256':'wrong'}}}))
    with pytest.raises(ValueError,match='changed pinned'): verify_raw(tmp_path)
