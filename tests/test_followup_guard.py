"""The shared follow-up contract must be committed and stable during execution."""
import subprocess
import pytest
from tsatlas import common


@pytest.mark.parametrize('mutation',['edit','delete'])
def test_shared_contract_dirty_and_midrun_changes_are_rejected(tmp_path,monkeypatch,mutation):
    paths=['pyproject.toml','uv.lock','studies/co2/DESIGN.md','studies/followups/DESIGN.md',
           'data/manifest.json','reports/intake/audit.json']
    for name in paths:
        p=tmp_path/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('initial\n')
    def git(*args):
        return subprocess.check_output(['git',*args],cwd=tmp_path,text=True).strip()
    git('init','-b','main');git('add','.')
    git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Contracts')
    monkeypatch.setattr(common,'ROOT',tmp_path)
    monkeypatch.setattr(common,'verify_snapshots',lambda **kwargs:{'snapshots':{'fixture':{}}})
    contract=tmp_path/'studies/followups/DESIGN.md';contract.write_text('changed before run\n')
    with pytest.raises(ValueError,match='Commit source/design'):
        common.start_run('co2')
    contract.unlink()
    with pytest.raises(ValueError,match='Commit source/design'):
        common.start_run('co2')
    contract.write_text('amended\n')
    git('add','.');git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Amendment')
    out,started=common.start_run('co2')
    assert 'studies/followups/DESIGN.md' in started['source_files']
    if mutation=='delete':contract.unlink()
    else:contract.write_text('changed during run\n')
    with pytest.raises((ValueError,FileNotFoundError)):
        common.finish_run('co2',out,started,{})
    assert not (tmp_path/'reports/results/co2').exists()
