"""Run offline checks and retain actual execution evidence."""
import hashlib,json,subprocess,sys,time,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1]
started=time.perf_counter()
command=[sys.executable,'-m','pytest','-q']
def hashes():
 paths=list((root/'src').rglob('*.py'))+list((root/'tests').rglob('*.py'))+list((root/'scripts').glob('*.py'))+[root/'uv.lock',root/'pyproject.toml']
 return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
before=hashes()
result=subprocess.run(command,cwd=root,text=True,capture_output=True)
stable=before==hashes()
evidence={'source_stable_during_checks':stable,'checked_at':datetime.datetime.now(datetime.UTC).isoformat(),'command':'uv run python scripts/check.py (runs python -m pytest -q)',
 'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'source_files':before,
 'exit_code':result.returncode if stable else 1,'elapsed_seconds':time.perf_counter()-started,'stdout':result.stdout,'stderr':result.stderr}
out=root/'reports/verification';out.mkdir(parents=True,exist_ok=True)
(out/'checks.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(result.stdout[-2000:]);print(result.stderr[-1000:]);sys.exit(evidence['exit_code'])
