"""Compare the fixed pre-follow-up evidence with current files; never rewrite it."""
from pathlib import Path
import subprocess,json,hashlib,datetime

ROOT=Path(__file__).resolve().parents[1]
BASELINE='1a0ec0180b857f7d98b092a8104a575657d53445'


def main():
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,'reports/results'],cwd=ROOT,text=True).splitlines()
    rows=[]
    for name in names:
        path=Path(name)
        if path.name=='run.json':continue
        old=subprocess.check_output(['git','show',f'{BASELINE}:{name}'],cwd=ROOT)
        current=(ROOT/name).read_bytes()
        rows.append({'path':name,'kind':'presentation' if path.suffix in {'.md','.png'} else 'numerical',
            'baseline_sha256':hashlib.sha256(old).hexdigest(),'current_sha256':hashlib.sha256(current).hexdigest(),
            'unchanged':old==current})
    numerical=[r for r in rows if r['kind']=='numerical']
    assert len(numerical)==49, 'Unexpected baseline scope'
    changed=[r['path'] for r in numerical if not r['unchanged']]
    added=sorted(str(p.relative_to(ROOT)) for p in (ROOT/'reports/results').rglob('*') if p.is_file() and str(p.relative_to(ROOT)) not in names)
    evidence={'baseline_commit':BASELINE,'checked_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'checked_at':datetime.datetime.now(datetime.UTC).isoformat(),'original_outputs':rows,
        'original_numerical_count':len(numerical),'numerical_changes':changed,'added_outputs':added,'ok':not changed}
    (ROOT/'reports/verification/optional-preservation.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(f'{len(numerical)} original numerical artifacts; {len(changed)} changes; {len(added)} additions')
    raise SystemExit(bool(changed))


if __name__=='__main__':main()
