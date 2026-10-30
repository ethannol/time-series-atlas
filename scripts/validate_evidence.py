"""Require all first-release evidence, then verify its recorded bytes."""
from pathlib import Path
import hashlib,json
EXPECTED={'co2','electricity','synthetic'}


def validate(root):
    records=list((root/'reports/results').glob('*/run.json'))
    found={p.parent.name for p in records}
    errors=[f'Missing expected study evidence: {name}' for name in sorted(EXPECTED-found)]
    if found-EXPECTED: errors.append(f'Unexpected study evidence: {sorted(found-EXPECTED)}')
    for record in records:
        evidence=json.loads(record.read_text());study=record.parent.name
        if evidence.get('study')!=study: errors.append(f'{study}: study-name mismatch')
        for field in ['source_files','outputs']:
            entries=evidence.get(field)
            if not isinstance(entries,dict) or not entries:
                errors.append(f'{study}: empty or missing {field}');continue
            for name,expected in entries.items():
                p=root/name
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
                    errors.append(f'{study}: {field} mismatch: {name}')
        entries=evidence.get('snapshots')
        if not isinstance(entries,dict) or not entries:
            errors.append(f'{study}: empty or missing snapshots')
        else:
            for name,entry in entries.items():
                p=root/'data/snapshots'/name
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
                    errors.append(f'{study}: snapshot mismatch: {name}')
        if evidence.get('source_stable_during_run') is not True: errors.append(f'{study}: source stability not verified')
    return errors


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    errors=validate(root)
    print('First-release evidence: '+ ('\n'.join(errors) if errors else 'All expected study records and hashes verified.'))
    raise SystemExit(bool(errors))
