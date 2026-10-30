import json
import runpy
from pathlib import Path
validate=runpy.run_path(str(Path(__file__).resolve().parents[1]/'scripts/validate_evidence.py'))['validate']


def test_missing_study_records_cannot_pass(tmp_path):
    errors=validate(tmp_path)
    assert len(errors)==3
    for study in ['co2','electricity','synthetic']:
        p=tmp_path/'reports/results'/study;p.mkdir(parents=True)
        (p/'run.json').write_text(json.dumps({'study':study,'source_stable_during_run':True,'source_files':{},'outputs':{},'snapshots':{}}))
    errors=validate(tmp_path)
    assert any('empty or missing outputs' in x for x in errors)
    assert any('empty or missing source_files' in x for x in errors)
    assert any('empty or missing snapshots' in x for x in errors)


def test_wrong_study_name_cannot_pass(tmp_path):
    p=tmp_path/'reports/results/co2';p.mkdir(parents=True)
    (p/'run.json').write_text(json.dumps({'study':'electricity'}))
    assert any('study-name mismatch' in x for x in validate(tmp_path))
