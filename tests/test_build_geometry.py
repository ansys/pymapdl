import os
import pytest
import pyansys


if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    has_ansys = False
else:
    has_ansys = pyansys.has_ansys



@pytest.fixture(scope='module')
def mapdl():
    return pyansys.Mapdl(override=True)


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear()
    mapdl.prep7()
    yield


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_k(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 is 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 is 2


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_l(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 is 1


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2)
    assert a0 is 1


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_v(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    k3 = mapdl.k("", 0, 0, 1)
    v0 = mapdl.v(k0, k1, k2, k3)
    assert v0 is 1


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_n(cleared, mapdl):
    n0 = mapdl.n("", 0, 0, 0)
    assert n0 is 1
    n1 = mapdl.n(2, 0, 0, 1)
    assert n1 is 2


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 1, 0)
    l0 = mapdl.bsplin(k0, k1, k2)
    assert l0 is 1


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 is 1


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_al(cleared, mapdl):
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


@pytest.mark.skipif(not has_ansys, reason="Requires ANSYS installed")
def test_invalid():
    with pytest.raises(Exception):
        mapdl.a(0, 0, 0, 0)
