"""Verify committed prediction/report bytes and the source they were produced from."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
records=list((root/'reports/results').glob('*/run.json'))
errors=[]
for record in records:
 evidence=json.loads(record.read_text())
 for field in ['source_files','outputs']:
  for name,expected in evidence[field].items():
   p=root/name
   if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
    errors.append(f'{record.parent.name}: {field} mismatch: {name}')
 for name,entry in evidence['snapshots'].items():
  p=root/'data/snapshots'/name
  if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
   errors.append(f'{record.parent.name}: snapshot mismatch: {name}')
 if not evidence['source_stable_during_run']: errors.append(f'{record}: source mutation')
print(f'Checked {len(records)} study evidence records. '+ ('\n'.join(errors) if errors else 'All recorded hashes match.'))
raise SystemExit(bool(errors))
