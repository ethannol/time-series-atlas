"""Explicit, deterministic intake for the remaining real datasets. No model fitting."""
from __future__ import annotations
from collections import Counter, defaultdict
import datetime as dt
import gzip
import io
import json
import re
import zipfile
import numpy as np
import pandas as pd
from .data import ROOT, digest, write_json


def raw_manifest(study):
    manifest = json.loads((ROOT/'data/manifests'/f'{study}.json').read_text())
    for name, entry in manifest['files'].items():
        if digest(ROOT/'data/raw'/name) != entry['sha256']:
            raise ValueError(f'Changed pinned source: {name}')
    return manifest


def snapshot(frame, name, private=False):
    path = ROOT/('data/processed' if private else 'data/snapshots')/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(gzip.compress(frame.to_csv(index=False).encode(),mtime=0))
    entry={'sha256':digest(path),'bytes':path.stat().st_size}
    if private:entry.update({'path':str(path.relative_to(ROOT)),'availability':'fetch-only'})
    return {name:entry}


def finish_intake(study, audit, manifest):
    audit['source_sha256'] = {k:v['sha256'] for k,v in manifest['files'].items()}
    write_json(ROOT/'reports/intake'/f'{study}.json',audit)
    return audit


def retail_intake():
    import openpyxl
    manifest=raw_manifest('retail')
    counts=Counter(); sheet_audit=[]; sales=defaultdict(float)
    with zipfile.ZipFile(ROOT/'data/raw/retail.zip') as z:
        workbook=openpyxl.load_workbook(io.BytesIO(z.read('online_retail_II.xlsx')),read_only=True,data_only=True)
    cutover=dt.datetime(2010,12,1)
    for sheet_index, sheet in enumerate(workbook):
        dates=[]; n=0
        for invoice,code,description,quantity,when,price,customer,country in sheet.iter_rows(min_row=2,values_only=True):
            n+=1; dates.append(when); counts['raw_rows']+=1
            # The workbook's annual sheets overlap. Prefer the later sheet at its start date.
            if (sheet_index==0 and when>=cutover) or (sheet_index==1 and when<cutover):
                counts['excluded_sheet_overlap_rows']+=1; continue
            if country!='United Kingdom': counts['excluded_non_UK_rows']+=1; continue
            if str(invoice).upper().startswith('C'):
                counts['excluded_cancellation_rows']+=1
                counts['cancellation_signed_units']+=quantity
                continue
            if not re.fullmatch(r'\d{5}[A-Za-z]?',str(code)):
                counts['excluded_non_merchandise_code_rows']+=1; continue
            if quantity<=0 or price is None or price<=0:
                counts['excluded_nonpositive_quantity_or_price_rows']+=1; continue
            if customer is None: counts['retained_rows_without_customer_id']+=1
            counts['retained_rows']+=1
            sales[(when.date().isoformat(),str(code))]+=quantity
        sheet_audit.append({'sheet':sheet.title,'rows':n,'first':min(dates).isoformat(),'last':max(dates).isoformat()})
    long=pd.DataFrame([(d,c,q) for (d,c),q in sales.items()],columns=['date','product','units'])
    panel=long.pivot(index='date',columns='product',values='units').fillna(0)
    panel.index=pd.to_datetime(panel.index)
    panel=panel.reindex(pd.date_range('2009-12-01','2011-12-09'),fill_value=0)
    train=panel.loc['2010'];positive=(train>0).sum()
    eligible=train.columns[(positive>=10)&(positive<=int(.4*len(train)))&(train.loc[:'2010-06-30'].sum()>0)&(train.loc['2010-10-01':].sum()>0)]
    ranked=train[eligible].sum().sort_values(kind='stable')
    if len(ranked)<24: raise ValueError('Too few eligible intermittent products')
    selected=ranked.iloc[np.linspace(0,len(ranked)-1,24).round().astype(int)].index.tolist()
    result=panel[selected].copy();result.index.name='date'
    audit={'sheets':sheet_audit,'counts':dict(counts),'sheet_cutover':'2010-12-01','eligible_products':len(eligible),
           'selection_history_end':'2010-12-31','selected_products':selected,
           'train_2010_positive_days':positive[selected].to_dict(),
           'train_2010_units':train[selected].sum().to_dict(),
           'snapshot_rows':len(result),'snapshots':snapshot(result.reset_index(),'retail-daily-panel.csv.gz')}
    return finish_intake('retail',audit,manifest)


def oil_intake():
    manifest=raw_manifest('oil'); series=[]; source_stats={}
    for name in ['wti','brent']:
        frame=pd.read_excel(ROOT/'data/raw'/f'{name}.xls',sheet_name='Data 1',skiprows=2)
        frame.columns=['date',name]; frame['date']=pd.to_datetime(frame.date)
        if not frame.date.is_unique: raise ValueError('Duplicate oil dates')
        frame=frame.set_index('date').sort_index()
        source_stats[name]={'rows':len(frame),'first':str(frame.index.min().date()),'last':str(frame.index.max().date()),
                           'nonpositive_dates':frame.index[frame[name]<=0].strftime('%Y-%m-%d').tolist(),
                           'minimum':float(frame[name].min()),'missing':int(frame[name].isna().sum())}
        series.append(frame)
    panel=pd.concat(series,axis=1).loc['1987-05-20':'2025-12-31']
    # Keep each source's own missingness; next-observation differences are study-specific.
    audit={'series':source_stats,'snapshots':snapshot(panel.reset_index(),'oil-daily.csv.gz',private=True),
           'study_last_date':'2025-12-31','union_rows':len(panel),'common_observed_rows':int(panel.notna().all(axis=1).sum())}
    return finish_intake('oil',audit,manifest)


def air_quality_intake():
    manifest=raw_manifest('air-quality');series=[];stats={}
    with zipfile.ZipFile(ROOT/'data/raw/air-quality.zip') as outer:
        with zipfile.ZipFile(io.BytesIO(outer.read('PRSA2017_Data_20130301-20170228.zip'))) as archive:
            for name in sorted(archive.namelist()):
                if not name.endswith('.csv'): continue
                frame=pd.read_csv(archive.open(name));station=str(frame.station.iloc[0])
                frame.index=pd.to_datetime(frame[['year','month','day','hour']])
                expected=pd.date_range('2013-03-01','2017-02-28 23:00',freq='h')
                if not frame.index.equals(expected): raise ValueError('Unexpected station grid')
                values=frame['PM2.5'].rename(station)
                if (values.dropna()<0).any(): raise ValueError('Negative concentration needs review')
                stats[station]={'rows':len(values),'missing':int(values.isna().sum()),'min':float(values.min()),'max':float(values.max())}
                series.append(values)
    panel=pd.concat(series,axis=1);panel.index.name='hour'
    if len(panel.columns)!=12: raise ValueError('Expected 12 distinct stations')
    audit={'stations':stats,'time_convention':'Nominal provider hour, no timezone conversion; reporting latency unknown',
           'snapshots':snapshot(panel.reset_index(),'air-quality-hourly.csv.gz')}
    return finish_intake('air-quality',audit,manifest)
