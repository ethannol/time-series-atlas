"""Explicit source adapters. Intake is not a forecasting evaluation."""
from __future__ import annotations
import gzip
import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def verify_raw(root: Path = ROOT) -> dict:
    manifest = json.loads((root / 'data/manifest.json').read_text())
    for name, entry in manifest['files'].items():
        path = root / 'data/raw' / name
        if not path.exists() or digest(path) != entry['sha256']:
            raise ValueError(f'Missing or changed pinned source: {name}; no silent refresh allowed')
    return manifest


def fetch(root: Path = ROOT) -> None:
    """Acquire pinned bytes. A changed upstream file fails, rather than refreshing."""
    manifest = json.loads((root / 'data/manifest.json').read_text())
    for name, entry in manifest['files'].items():
        target = root / 'data/raw' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if digest(target) != entry['sha256']:
                raise ValueError(f'Changed existing source: {name}')
            continue
        temporary = target.with_suffix(target.suffix + '.part')
        try:
            subprocess.run(['curl', '--fail', '--location', '--retry', '2', '--output', str(temporary), entry['url']], check=True)
            if digest(temporary) != entry['sha256']:
                raise ValueError(f'Provider bytes changed: {name}; obtain the pinned snapshot')
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)


def co2_frame(path: Path) -> pd.DataFrame:
    cols = ['year','month','decimal_date','average','deseasonalized','days','stdev','uncertainty']
    frame = pd.read_csv(path, sep=r'\s+', comment='#', names=cols)
    frame.index = pd.to_datetime(dict(year=frame.year, month=frame.month, day=1))
    frame.index.name = 'date'
    if not frame.index.is_unique or not frame.index.equals(pd.date_range(frame.index.min(), frame.index.max(), freq='MS', name='date')):
        raise ValueError('CO2 dates must be unique and monthly without gaps')
    noaa = frame.index >= '1974-05-01'
    frame['unknown_scripps_metadata'] = ~noaa
    frame['quality_suspect'] = noaa & ((frame.stdev < 0) | (frame.uncertainty < 0))
    frame['site_substitution'] = (frame.index >= '2022-12-01') & (frame.index <= '2023-07-01')
    frame['usable'] = noaa & ~frame.quality_suspect & (frame.average > 0)
    return frame


def quarter_to_hour(frame: pd.DataFrame) -> pd.DataFrame:
    """Nominal end-labeled quarter hours -> start-labeled hours, mean kW.

    This is an explicit interval-label convention, not a reconstructed UTC clock.
    """
    frame = frame.copy()
    frame.index = pd.to_datetime(frame.index) - pd.Timedelta(minutes=15)
    counts = frame.resample('h').size()
    if not (counts == 4).all():
        raise ValueError('Every nominal hour must have four quarter-hour records')
    return frame.resample('h').mean()


def dst_days(index: pd.DatetimeIndex) -> np.ndarray:
    """Whole nominal transition days, conservatively flagged in March/October."""
    return np.asarray(index.month.isin([3, 10]) & (index.dayofweek == 6) & (index.day >= 25))


def cohort(hourly: pd.DataFrame, count: int = 24) -> list[str]:
    """Selection uses 2011/2012 only, not later sales/activation or test outcomes."""
    history = hourly.loc['2011':'2012']
    first_year_positive = (history.loc['2011'] > 0).any()
    train = history.loc['2012']
    daily_positive = (train.resample('D').sum() > 0).sum()
    mean = train.mean()
    eligible = mean[(daily_positive >= 350) & first_year_positive & (mean > 0)].sort_values(kind='stable')
    if len(eligible) < count:
        raise ValueError('Insufficient eligible customers for the declared panel')
    ranks = np.linspace(0, len(eligible) - 1, count).round().astype(int)
    return eligible.index[ranks].tolist()


def intake(root: Path = ROOT) -> dict:
    manifest = verify_raw(root)
    output = root / 'data/snapshots'
    output.mkdir(parents=True, exist_ok=True)
    co2 = co2_frame(root / 'data/raw/co2_mm_mlo.txt')
    shutil.copyfile(root / 'data/raw/co2_mm_mlo.txt', output / 'co2_mm_mlo.txt')
    chunks = []
    raw_rows = 0
    raw_first = raw_last = None
    negative = nonfinite = 0
    with zipfile.ZipFile(root / 'data/raw/electricity.zip') as archive:
        with archive.open('LD2011_2014.txt') as stream:
            for chunk in pd.read_csv(stream, sep=';', decimal=',', index_col=0, chunksize=96*31):
                raw_rows += len(chunk)
                raw_first = raw_first or str(chunk.index[0])
                raw_last = str(chunk.index[-1])
                values = chunk.to_numpy()
                nonfinite += int((~np.isfinite(values)).sum())
                negative += int((values < 0).sum())
                chunks.append(quarter_to_hour(chunk))
    hourly = pd.concat(chunks)
    expected = pd.date_range('2011-01-01', '2014-12-31 23:00', freq='h')
    if not hourly.index.equals(expected) or nonfinite or negative:
        raise ValueError('Unexpected electricity timestamps/values; inspect before analysis')
    clients = cohort(hourly)
    selected = hourly[clients]
    selected.index.name = 'hour'
    panel = output / 'electricity-hourly-panel.csv.gz'
    panel.write_bytes(gzip.compress(selected.to_csv().encode(), mtime=0))
    # Source-only audit; no model or forecast scores are computed here.
    audit = {
        'source_sha256': {k:v['sha256'] for k,v in manifest['files'].items()},
        'co2': {'rows':len(co2),'first':str(co2.index.min().date()),'last':str(co2.index.max().date()),
                'scripps_unknown_metadata_rows':int(co2.unknown_scripps_metadata.sum()),
                'noaa_quality_suspect_dates':co2.index[co2.quality_suspect].strftime('%Y-%m').tolist(),
                'site_substitution_dates':co2.index[co2.site_substitution].strftime('%Y-%m').tolist()},
        'electricity':{'raw_rows':raw_rows,'customers':len(hourly.columns),'first_label':raw_first,'last_label':raw_last,
                       'negative_values':negative,'nonfinite_values':nonfinite,'nominal_hourly_rows':len(hourly),
                       'selection_history_end':'2012-12-31','selected_customers':clients,
                       '2012_mean_kw':selected.loc['2012'].mean().to_dict(),
                       'zero_hours_by_selected_customer':(selected==0).sum().to_dict(),
                       'transition_days':hourly.index[dst_days(hourly.index)].normalize().unique().strftime('%Y-%m-%d').tolist(),
                       'time_convention':'Provider nominal clock; assume end-labeled quarters; subtract 15 min then hourly mean kW; no UTC conversion'},
        'snapshots':{p.name:{'sha256':digest(p),'bytes':p.stat().st_size} for p in [output/'co2_mm_mlo.txt',panel]},
    }
    write_json(root / 'reports/intake/audit.json', audit)
    return audit


def verify_snapshots(root: Path = ROOT, study=None, require_private=False) -> dict:
    if study in ['co2','electricity','synthetic','spectral']:
        paths=[root/'reports/intake/audit.json']
    elif study:
        paths=[root/'reports/intake'/f'{study}.json']
    else:
        paths=sorted((root/'reports/intake').glob('*.json'))
    combined={'snapshots':{},'not_mirrored':[]}
    for audit_path in paths:
        audit=json.loads(audit_path.read_text())
        for name,entry in audit.get('snapshots',{}).items():
            path=root/entry.get('path',f'data/snapshots/{name}')
            if not path.exists() and entry.get('availability')=='fetch-only' and not require_private:
                combined['not_mirrored'].append(name)
            elif not path.exists() or digest(path)!=entry['sha256']:
                raise ValueError(f'Missing or changed analysis snapshot: {name}')
            combined['snapshots'][name]=entry
    if not combined['snapshots']:raise ValueError('No declared input snapshots')
    return combined
