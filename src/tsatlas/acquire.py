"""Explicit acquisition, separate from offline study execution."""
import datetime as dt
import gzip
import json
import subprocess
import pandas as pd
from .data import ROOT,digest,write_json


def fetch_study(study):
    manifest=json.loads((ROOT/'data/manifests'/f'{study}.json').read_text())
    if study=='oil':return fetch_oil(manifest)
    files=manifest['files']
    if all((ROOT/'data/raw'/n).exists() and digest(ROOT/'data/raw'/n)==e['sha256'] for n,e in files.items()):return
    if study=='river-flow':
        from .camels_source import acquire
        return acquire()
    for name,entry in files.items():
        target=ROOT/'data/raw'/name;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and digest(target)==entry['sha256']:continue
        temporary=target.with_suffix(target.suffix+'.part')
        try:
            subprocess.run(['curl','--fail','--location','--retry','2','-o',str(temporary),entry['url']],check=True)
            if digest(temporary)!=entry['sha256']:raise ValueError('Changed upstream source; explicit refresh/review required')
            temporary.replace(target)
        finally:temporary.unlink(missing_ok=True)


def fetch_oil(manifest):
    """Allow a growing workbook only if its normalized historical input matches exactly."""
    audit=json.loads((ROOT/'reports/intake/oil.json').read_text())
    name='oil-daily.csv.gz';expected=audit['snapshots'][name]['sha256']
    target=ROOT/'data/processed'/name
    if target.exists() and digest(target)==expected:return {'status':'existing exact normalized input'}
    series=[];raw_hashes={}
    for market in ['wti','brent']:
        filename=market+'.xls';entry=manifest['files'][filename];p=ROOT/'data/raw'/filename
        if not p.exists() or digest(p)!=entry['sha256']:
            p=ROOT/'data/raw/oil-reproduction'/filename;p.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['curl','--fail','--location','--retry','2','-o',str(p),entry['url']],check=True)
        raw_hashes[filename]=digest(p)
        f=pd.read_excel(p,sheet_name='Data 1',skiprows=2);f.columns=['date',market]
        f['date']=pd.to_datetime(f.date)
        if not f.date.is_unique:raise ValueError('Duplicate oil dates')
        series.append(f.set_index('date').sort_index())
    frame=pd.concat(series,axis=1).loc['1987-05-20':'2025-12-31'].reset_index()
    target.parent.mkdir(parents=True,exist_ok=True);temporary=target.with_suffix('.part')
    try:
        temporary.write_bytes(gzip.compress(frame.to_csv(index=False).encode(),mtime=0))
        if digest(temporary)!=expected:raise ValueError('Historical oil input changed; exact reproduction unavailable from current provider files')
        temporary.replace(target)
    finally:temporary.unlink(missing_ok=True)
    result={'at':dt.datetime.now(dt.UTC).isoformat(),'raw_sha256':raw_hashes,'normalized_sha256':expected,'normalized_bytes_match':True,
            'raw_bytes_match_original':all(raw_hashes[n]==e['sha256'] for n,e in manifest['files'].items())}
    write_json(ROOT/'reports/runs/oil-acquisition.json',result)
    return result
