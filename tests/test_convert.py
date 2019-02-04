import os
import pyansys

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'testfiles')


def test_convert(tmpdir):
    vm_file = os.path.join(testfiles_path, 'vm1.dat')
    pyscript = str(tmpdir.mkdir("tmpdir").join('vm1.py'))
    clines = pyansys.convert_script(vm_file, pyscript, loglevel='ERROR')
    assert len(clines)

    if pyansys.has_ansys:
        exec(open(pyscript).read())
