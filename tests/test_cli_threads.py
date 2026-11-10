"""Exercise library discovery in a fresh CLI process without fitting models."""
import os
import subprocess
import sys
import pytest


@pytest.mark.parametrize('command',['ecg','all'])
def test_cli_caps_libraries_loaded_by_dynamic_study_imports(command):
    script=r'''
import importlib, json, sys, os
from tsatlas import cli
from threadpoolctl import threadpool_info
assert os.environ['VECLIB_MAXIMUM_THREADS']=='1'
# Exercise the runtime context independently of the environment fallback: a
# library loaded late must still be limited if its own startup default differs.
os.environ['OMP_NUM_THREADS']='4'
original_import=importlib.import_module
observed=[]
def instrumented_import(name, package=None):
    module=original_import(name, package)
    if name.startswith('tsatlas.'):
        def probe():
            info=threadpool_info()
            assert info and all(row['num_threads']==1 for row in info), info
            observed.append(name)
        module.run=probe
    return module
importlib.import_module=instrumented_import
cli.main()
assert len(observed)==(9 if sys.argv[1]=='all' else 1), observed
print(json.dumps(observed))
'''
    environment=os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        environment.pop(key,None)
    result=subprocess.run([sys.executable,'-c',script,command],env=environment,text=True,capture_output=True,timeout=30)
    assert result.returncode==0,result.stdout+result.stderr
