import pytest
import pyansys


if pyansys.has_ansys:
    mapdl = pyansys.Mapdl(override=True)
    mapdl.prep7()


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_k():
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 is 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 is 2


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_l():
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 is 1
    

@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_a():
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 is 1


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_al():
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    a0 = mapdl.al(l0, l1, l2, l3)
    assert a0 is 1


@pytest.mark.skipif(not pyansys.has_ansys, reason="Requires ANSYS installed")
def test_invalid():
    with pytest.raises(Exception):
        mapdl.a(0, 0, 0, 0)
