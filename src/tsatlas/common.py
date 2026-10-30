from __future__ import annotations
import datetime
import gzip
import hashlib
import json
import platform
import resource
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data import ROOT, digest, verify_snapshots, write_json


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def source_snapshot(study):
    paths=sorted((ROOT/'src').rglob('*.py'))+sorted((ROOT/'tests').rglob('*.py'))+sorted((ROOT/'scripts').glob('*.py'))
    paths += [ROOT/'pyproject.toml',ROOT/'uv.lock',ROOT/'studies'/study/'DESIGN.md',ROOT/'data/manifest.json',ROOT/'reports/intake/audit.json']
    paths += [p for p in [ROOT/'data/manifests'/f'{study}.json',ROOT/'reports/intake'/f'{study}.json'] if p.exists()]
    paths += sorted((ROOT/'studies'/study).glob('*.json'))
    return {str(p.relative_to(ROOT)):digest(p) for p in paths}


def start_run(study):
    inputs=verify_snapshots(study=study,require_private=True)
    # Full runs start from committed source. Reviews and result-only edits may coexist.
    source_paths=['src','tests','scripts','pyproject.toml','uv.lock',f'studies/{study}/DESIGN.md','data/manifest.json','reports/intake/audit.json']
    source_paths += [f'data/manifests/{study}.json',f'reports/intake/{study}.json']
    source_paths += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'studies'/study).glob('*.json'))]
    if git('status','--porcelain','--',*source_paths):
        raise ValueError('Commit source/design/configuration before a full run')
    temp_parent=ROOT/'reports/runs';temp_parent.mkdir(parents=True,exist_ok=True)
    out=Path(tempfile.mkdtemp(prefix=study+'-',dir=temp_parent))
    evidence={'started':time.perf_counter(),'started_at':datetime.datetime.now(datetime.UTC).isoformat(),
        'source_commit':git('rev-parse','HEAD'),'protocol_commit':git('log','-1','--format=%H','--',f'studies/{study}/DESIGN.md'),
        'source_files':source_snapshot(study),'snapshots':inputs['snapshots']}
    plt.rcParams.update({'figure.dpi':130,'savefig.dpi':160,'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    return out,evidence


def save_frame(frame,path):
    path.write_bytes(gzip.compress(frame.to_csv(index=False).encode(),mtime=0))


def finish_run(study,out,started,config):
    if source_snapshot(study)!=started['source_files']:
        raise ValueError('Source/design/configuration changed during run; results not published')
    verify_snapshots(study=study,require_private=True)
    target=ROOT/'reports/results'/study
    outputs={str((target/p.name).relative_to(ROOT)):digest(p) for p in sorted(out.iterdir()) if p.is_file() and p.name!='run.json'}
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    evidence={k:v for k,v in started.items() if k!='started'}
    evidence.update({'study':study,'recorded_at':datetime.datetime.now(datetime.UTC).isoformat(),
        'source_patch_sha256':hashlib.sha256(b'').hexdigest(),'source_stable_during_run':True,
        'python':platform.python_version(),'platform':platform.platform(),'elapsed_seconds':time.perf_counter()-started['started'],
        'process_lifetime_peak_rss_bytes':rss if platform.system()=='Darwin' else rss*1024,'configuration':config,'outputs':outputs})
    write_json(out/'run.json',evidence)
    target.parent.mkdir(parents=True,exist_ok=True)
    backup=out.parent/(out.name+'-previous')
    if target.exists(): target.rename(backup)
    try:
        out.rename(target)
    except BaseException:
        if backup.exists(): backup.rename(target)
        raise
    if backup.exists(): shutil.rmtree(backup)


def markdown_table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,row))+' |\n' for row in rows)
