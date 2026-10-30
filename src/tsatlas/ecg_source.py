"""Annotated-beat waveform intake; no fitted feature extraction or classifiers."""
import datetime as dt
import hashlib
import io
import json
import zipfile
from collections import Counter
import numpy as np
from scipy.signal import resample_poly
import wfdb
from .data import ROOT,digest,write_json
from .extended_data import raw_manifest,finish_intake

GROUPS={'N':'N','L':'N','R':'N','e':'N','j':'N','A':'S','a':'S','J':'S','S':'S','V':'V','E':'V','F':'F'}
BEAT_SYMBOLS=set('NLRaVFJASEj/e fQ'.replace(' ',''))
PACED={'102','104','107','217'}


def person(record): return '201' if record=='202' else record


def intake():
    manifest=raw_manifest('ecg');directory=ROOT/'data/raw/mitdb';directory.mkdir(exist_ok=True)
    stats={};waves=[];rows=[];members={}
    with zipfile.ZipFile(ROOT/'data/raw/mitdb.zip') as archive:
        prefix='mit-bih-arrhythmia-database-1.0.0/'
        records=archive.read(prefix+'RECORDS').decode().split()
        sums={line.split(maxsplit=1)[1].lstrip('*'):line.split()[0] for line in archive.read(prefix+'SHA256SUMS.txt').decode().splitlines()}
        if len(records)!=48:raise ValueError('Expected all48 record inventory')
        for name in ['RECORDS','SHA256SUMS.txt']+[r+s for r in records for s in ['.hea','.dat','.atr']]:
            data=archive.read(prefix+name);sha=hashlib.sha256(data).hexdigest()
            if name in sums and sha!=sums[name]:raise ValueError('Provider checksum mismatch')
            (directory/name).write_bytes(data);members[name]=sha
    for record in records:
        data=wfdb.rdrecord(str(directory/record));ann=wfdb.rdann(str(directory/record),'atr')
        if data.fs!=360 or data.sig_len!=650000:raise ValueError('Unexpected ECG sampling metadata')
        reason='paced_record' if record in PACED else 'no_MLII' if 'MLII' not in data.sig_name else None
        stat={'person':person(record),'leads':data.sig_name,'fs':data.fs,'samples':data.sig_len,
              'annotation_counts':dict(Counter(ann.symbol)),'excluded_record_reason':reason,'retained':0,'boundary_excluded':0,'no_previous_beat_excluded':0,'nonfinite_excluded':0}
        if reason is None:
            channel=data.sig_name.index('MLII');last_beat=None
            for center,symbol in zip(ann.sample,ann.symbol):
                if symbol not in BEAT_SYMBOLS:continue
                prior=last_beat;last_beat=int(center)
                if symbol not in GROUPS:continue
                if prior is None:
                    stat['no_previous_beat_excluded']+=1;continue
                if center<90 or center+90>data.sig_len:
                    stat['boundary_excluded']+=1;continue
                wave=data.p_signal[center-90:center+90,channel]
                if not np.isfinite(wave).all():stat['nonfinite_excluded']+=1;continue
                reduced=resample_poly(wave,up=1,down=3).astype(np.float32)
                waves.append(reduced);rows.append((record,person(record),int(center),symbol,GROUPS[symbol],(int(center)-prior)/360))
                stat['retained']+=1
        stats[record]=stat
    records_array=np.array(rows,dtype=[('record','U3'),('person','U3'),('sample','i4'),('symbol','U1'),('label','U1'),('previous_rr_seconds','f4')])
    path=ROOT/'data/snapshots/ecg-beats.npz'
    np.savez_compressed(path,waveforms=np.stack(waves),beats=records_array)
    audit={'records':stats,'members_sha256':members,'total_retained':len(rows),'class_counts':dict(Counter(records_array['label'])),
           'label_map':GROUPS,'window':'[-90,+90) samples around expert location at360Hz, resample_poly1/3 to60 samples',
           'snapshots':{path.name:{'sha256':digest(path),'bytes':path.stat().st_size}}}
    return finish_intake('ecg',audit,manifest)
