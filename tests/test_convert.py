import os
import pytest
import ansys.mapdl.core as pymapdl

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


def test_convert_no_use_function_names(tmpdir):
    vm_file = os.path.join(testfiles_path, 'vm1.dat')
    pyscript = str(tmpdir.mkdir('tmpdir').join('vm1.py'))
    clines = pymapdl.convert_script(vm_file, pyscript, loglevel='ERROR',
                                    use_function_names=False)


@pytest.mark.skipif(os.name == 'nt', reason='Requires multiple instances')
def test_convert(tmpdir):
    vm_file = os.path.join(testfiles_path, 'vm1.dat')
    pyscript = str(tmpdir.mkdir('tmpdir').join('vm1.py'))
    clines = pymapdl.convert_script(vm_file, pyscript, loglevel='ERROR')
    assert len(clines)
