import pytest
import pyansys

if pyansys.has_ansys:
    mapdl = pyansys.Mapdl(override=True)
    mapdl.prep7()


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_et():
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_float("ETYP", 0, "NUM", "MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17
