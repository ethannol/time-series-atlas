"""Verify retained outputs and historical source blobs without rewriting provenance."""
from pathlib import Path
import hashlib,json,subprocess,re
EXPECTED={'co2','electricity','synthetic','retail','oil','river-flow','air-quality','ecg','spectral'}


def validate(root,expected_studies=EXPECTED,require_private=False):
    records=list((root/'reports/results').glob('*/run.json'))
    found={p.parent.name for p in records}
    errors=[f'Missing expected study evidence: {name}' for name in sorted(expected_studies-found)]
    if found-expected_studies: errors.append(f'Unexpected study evidence: {sorted(found-expected_studies)}')
    for record in records:
        evidence=json.loads(record.read_text());study=record.parent.name
        if evidence.get('study')!=study: errors.append(f'{study}: study-name mismatch')
        revision=evidence.get('source_commit','')
        valid_revision=bool(re.fullmatch('[0-9a-f]{40}',revision))
        if not valid_revision:errors.append(f'{study}: missing or invalid source revision')
        for field in ['source_files','outputs']:
            entries=evidence.get(field)
            if not isinstance(entries,dict) or not entries:
                errors.append(f'{study}: empty or missing {field}');continue
            for name,expected in entries.items():
                if field=='source_files' and valid_revision:
                    result=subprocess.run(['git','show',f'{revision}:{name}'],cwd=root,capture_output=True)
                    actual=hashlib.sha256(result.stdout).hexdigest() if result.returncode==0 else None
                elif field=='outputs':
                    p=root/name;actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
                else:actual=None
                if actual!=expected:
                    errors.append(f'{study}: {field} mismatch: {name}')
        entries=evidence.get('snapshots')
        if not isinstance(entries,dict) or not entries:
            errors.append(f'{study}: empty or missing snapshots')
        else:
            for name,entry in entries.items():
                p=root/entry.get('path',f'data/snapshots/{name}')
                if entry.get('availability')=='fetch-only' and not p.is_file() and not require_private:
                    continue # explicit acquisition limit, never reported as an input-byte verification
                if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=entry['sha256']:
                    errors.append(f'{study}: snapshot mismatch: {name}')
        if evidence.get('source_stable_during_run') is not True: errors.append(f'{study}: source stability not verified')
    return errors


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1]
    errors=validate(root)
    print('Collection evidence: '+ ('\n'.join(errors) if errors else 'Required outputs and historical source hashes verified; fetch-only inputs checked when locally present.'))
    raise SystemExit(bool(errors))
