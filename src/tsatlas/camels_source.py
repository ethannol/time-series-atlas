"""Bounded official ZIP-member acquisition; never download a 3.4GB fallback body."""
import datetime as dt
import hashlib
import io
import json
import zipfile
import requests
import pandas as pd
from .data import ROOT,digest,write_json
from .extended_data import snapshot,finish_intake,raw_manifest

URL='https://zenodo.org/api/records/15529996/files/basin_timeseries_v1p2_metForcing_obsFlow.zip/content'
SIZE=3406626583
PREFIX='basin_dataset_public_v1p2/'


class RangeReader(io.RawIOBase):
    def __init__(self): self.pos=0; self.transferred=0
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self,offset,whence=0):
        self.pos=offset if whence==0 else self.pos+offset if whence==1 else SIZE+offset
        if self.pos<0 or self.pos>SIZE: raise ValueError('Out-of-bounds ZIP seek')
        return self.pos
    def read(self,n=-1):
        if n<0:n=SIZE-self.pos
        n=min(n,SIZE-self.pos)
        if n==0:return b''
        if n>5_000_000:raise ValueError('Unbounded range request')
        end=self.pos+n-1
        with requests.get(URL,headers={'Range':f'bytes={self.pos}-{end}'},stream=True,timeout=45) as r:
            if r.status_code!=206 or r.headers.get('Content-Range')!=f'bytes {self.pos}-{end}/{SIZE}':
                raise ValueError('Server did not honor exact bounded ZIP range')
            data=r.raw.read(n+1)
        if len(data)!=n:raise ValueError('Wrong range length')
        self.pos+=n;self.transferred+=n
        return data


def flow_frame(raw):
    f=pd.read_csv(io.BytesIO(raw),sep=r'\s+',header=None,names=['gauge','year','month','day','flow_cfs','qc'],dtype={'gauge':str,'qc':str})
    f.index=pd.to_datetime(f[['year','month','day']]);f.index.name='date'
    if not f.index.is_unique:raise ValueError('Duplicate flow date')
    return f


def acquire():
    """Initial cohort uses metadata geography and 1980–1999 flow coverage only."""
    path=ROOT/'data/manifests/river-flow.json'
    previous=json.loads(path.read_text()) if path.exists() else None
    reader=RangeReader();entries={};trials=[];selected=[]
    with zipfile.ZipFile(reader) as archive:
        def member(name):
            info=archive.getinfo(name);relative='camels/'+name.removeprefix(PREFIX)
            target=ROOT/'data/raw'/relative;target.parent.mkdir(parents=True,exist_ok=True)
            data=archive.read(name) # zipfile verifies the member's CRC
            entry={'url':URL,'member':name,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'crc32':info.CRC}
            if previous and entry['sha256']!=previous['files'][relative]['sha256']:
                raise ValueError('Pinned CAMELS member changed')
            target.write_bytes(data)
            entries[relative]=entry
            return data
        if previous:
            for entry in previous['files'].values():member(entry['member'])
            return {'transferred_bytes':reader.transferred,'verified_members':len(entries)}
        for filename in ['readme_FIRST.txt','readme_basin_mean_forcing.txt','readme_streamflow.txt']:
            member(PREFIX+filename)
        metadata=member(PREFIX+'basin_metadata/gauge_information.txt').decode()
        gauges=[]
        for line in metadata.splitlines()[1:]:
            parts=line.split()
            if not parts:continue
            gauges.append({'huc':parts[0],'gauge':parts[1],'name':' '.join(parts[2:-3]),'latitude':float(parts[-3]),'longitude':float(parts[-2]),'area_km2':float(parts[-1])})
        for huc in sorted({g['huc'] for g in gauges}):
            for g in sorted((g for g in gauges if g['huc']==huc),key=lambda x:x['gauge']):
                flow=flow_frame(member(PREFIX+f"usgs_streamflow/{huc}/{g['gauge']}_streamflow_qc.txt"))
                training=flow.reindex(pd.date_range('1980-01-01','1999-12-31'))
                good=(training.qc=='A')&(training.flow_cfs>=0)
                fraction=float(good.mean());trials.append({'gauge':g['gauge'],'huc':huc,'training_approved_fraction':fraction})
                if fraction<.95:continue
                member(PREFIX+f"basin_mean_forcing/daymet/{huc}/{g['gauge']}_lump_cida_forcing_leap.txt")
                selected.append(g);break
    manifest={'acquired_at':dt.datetime.now(dt.UTC).isoformat(),'baseline':'bd85e01cb3e3e9af6be5a3a093a70a71e359ef6e',
              'archive':{'url':URL,'bytes':SIZE,'provider_md5':'8e9a466710e8270b58f01d332a87184f','whole_archive_checksum_verified':False,'license':'CC-BY-4.0','version':'1.2'},
              'transferred_bytes':reader.transferred,'files':entries,'cohort_trials':trials,'selected_gauges':selected}
    write_json(path,manifest)
    return {'selected':len(selected),'members':len(entries),'transferred_bytes':reader.transferred}


def intake():
    manifest=raw_manifest('river-flow');frames=[];stats={}
    for g in manifest['selected_gauges']:
        base=ROOT/'data/raw/camels';gauge=g['gauge'];huc=g['huc']
        flow=flow_frame((base/f'usgs_streamflow/{huc}/{gauge}_streamflow_qc.txt').read_bytes())
        p=base/f'basin_mean_forcing/daymet/{huc}/{gauge}_lump_cida_forcing_leap.txt'
        header=p.read_text().splitlines()[:3]
        forcing=pd.read_csv(p,sep=r'\s+',skiprows=3)
        forcing.index=pd.to_datetime(dict(year=forcing.iloc[:,0],month=forcing.iloc[:,1],day=forcing.iloc[:,2]))
        if not forcing.index.equals(pd.date_range('1980-01-01','2014-12-31')):raise ValueError('Forcing date grid mismatch')
        frame=flow.reindex(forcing.index)[['flow_cfs','qc']].copy()
        frame['precip_mm']=forcing['prcp(mm/day)'];frame['tmax_c']=forcing['tmax(C)'];frame['tmin_c']=forcing['tmin(C)']
        frame['gauge']=gauge;frame['huc']=huc;frame['area_km2']=g['area_km2']
        frame.index.name='date';frames.append(frame.reset_index())
        stats[gauge]={'qc_counts':frame.qc.fillna('no_source_row').value_counts().to_dict(),'negative_flow_days':int((frame.flow_cfs<0).sum()),
                      'forcing_header':header,'forcing_hours':sorted(forcing.iloc[:,3].unique().astype(int).tolist()),'metadata':g}
    panel=pd.concat(frames,ignore_index=True)
    audit={'gauges':stats,'selection':'First gauge by ID in each HUC with >=95% approved nonnegative 1980–1999 flow',
           'snapshot_rows':len(panel),'snapshots':snapshot(panel,'river-daily-panel.csv.gz')}
    return finish_intake('river-flow',audit,manifest)
