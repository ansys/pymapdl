import os

from ansys.mapdl.core import examples


def test_load_verif():
    for filename in examples.vmfiles.values():
        assert os.path.isfile(filename)
