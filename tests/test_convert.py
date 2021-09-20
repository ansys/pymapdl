import os
import pytest
from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import examples


def test_convert_no_use_function_names(tmpdir):
    vm_file = examples.vmfiles["vm1"]
    pyscript = str(tmpdir.mkdir("tmpdir").join("vm1.py"))
    clines = pymapdl.convert_script(
        vm_file, pyscript, loglevel="ERROR", use_function_names=False
    )
    assert clines


@pytest.mark.skipif(os.name == "nt", reason="Requires multiple instances")
def test_convert(tmpdir):
    vm_file = examples.vmfiles["vm1"]
    pyscript = str(tmpdir.mkdir("tmpdir").join("vm1.py"))
    clines = pymapdl.convert_script(vm_file, pyscript, loglevel="ERROR")
    assert clines
