import json
import runpy
from pathlib import Path
module=runpy.run_path(str(Path(__file__).resolve().parents[1]/'scripts/validate_evidence.py'))
validate=module['validate']


def test_missing_study_records_cannot_pass(tmp_path):
    errors=validate(tmp_path)
    assert len(errors)==len(module['EXPECTED'])
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


def test_historical_source_survives_new_code_but_corruption_fails(tmp_path):
    import subprocess,hashlib
    def git(*args):return subprocess.check_output(['git',*args],cwd=tmp_path,text=True).strip()
    git('init','-b','main');(tmp_path/'source.py').write_text('original source\n');git('add','source.py')
    git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Fixture source')
    revision=git('rev-parse','HEAD');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    source_hash=sha(tmp_path/'source.py');(tmp_path/'source.py').write_text('subsequent unrelated source\n')
    out=tmp_path/'reports/results/co2';out.mkdir(parents=True);(out/'metrics.json').write_text('{"mae":1}\n')
    inp=tmp_path/'data/snapshots/input.txt';inp.parent.mkdir(parents=True);inp.write_text('pinned data\n')
    record={'study':'co2','source_commit':revision,'source_stable_during_run':True,'source_files':{'source.py':source_hash},
            'outputs':{'reports/results/co2/metrics.json':sha(out/'metrics.json')},'snapshots':{'input.txt':{'sha256':sha(inp)}}}
    path=out/'run.json';path.write_text(json.dumps(record))
    assert validate(tmp_path,{'co2'})==[]
    record['source_files']['source.py']='0'*64;path.write_text(json.dumps(record))
    assert any('source_files mismatch' in x for x in validate(tmp_path,{'co2'}))
    record['source_files']['source.py']=source_hash;path.write_text(json.dumps(record));(out/'metrics.json').write_text('corrupt')
    assert any('outputs mismatch' in x for x in validate(tmp_path,{'co2'}))


def test_missing_historical_revision_is_not_a_pass(tmp_path):
    out=tmp_path/'reports/results/co2';out.mkdir(parents=True)
    (out/'run.json').write_text(json.dumps({'study':'co2','source_commit':'f'*40,'source_files':{'x':'0'*64}}))
    assert any('source_files mismatch' in x for x in validate(tmp_path,{'co2'}))
