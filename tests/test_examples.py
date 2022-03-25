import os
import re

from ansys.mapdl.core import examples


def test_load_verif():
    for filename in examples.vmfiles.values():
        assert os.path.isfile(filename)


def test_bracket(mapdl, cleared):
    # note that this method just returns a file path
    bracket_file = examples.download_bracket()
    assert os.path.isfile(bracket_file)

    # load the bracket and then print out the geometry
    mapdl.aux15()
    out = mapdl.igesin(bracket_file)
    n_ent = re.findall(r"TOTAL NUMBER OF ENTITIES \s*=\s*(\d*)", out)
    assert int(n_ent[0]) > 0
