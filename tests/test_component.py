import numpy as np
import pytest

from ansys.mapdl.core.errors import ComponentNoData


def test_str_rep(mapdl, cleared):
    assert "Components" in str(mapdl.components)
    assert "CM1" not in str(mapdl.components)
    assert "NODE" not in str(mapdl.components)
    assert len(mapdl.components.__str__().splitlines()) == 2
    mapdl.n()  # We need at least one node
    mapdl.cm("cm1", "nodes")
    assert "CM1" in str(mapdl.components)
    assert "NODE" in str(mapdl.components)
    assert len(mapdl.components.__str__().splitlines()) == 3


def test_set_item(mapdl, cube_solve):
    mapdl.components["mycomp"] = "node", [1, 2, 3]


def test_raise_empty_comp(mapdl, cleared):
    with pytest.raises(ComponentNoData):
        mapdl.cm("cm1", "nodes")


def test_contains_all(mapdl, cube_solve):
    mapdl.allsel()
    mapdl.cm("allnodes", "nodes")
    assert "allnodes" in mapdl.components
    assert np.allclose(mapdl.components["allnodes"], mapdl.mesh.nnum_all)


@pytest.mark.parametrize(
    "func,entity,selector,imax",
    (
        ["nsel", "nodes", "nodes", 2],
        ["esel", "elem", "elem", 3],
        ["ksel", "kp", "keypoints", 4],
        ["lsel", "line", "lines", 5],
        ["asel", "area", "areas", 6],
        ["vsel", "volu", "vnum", 1],
    ),
)
def test_contains_entities(mapdl, cube_solve, func, entity, selector, imax):
    func_ = getattr(mapdl, func)
    func_("S", vmin=1, vmax=imax)

    if entity in ["nodes", "elem"]:
        count = getattr(mapdl.mesh, selector)
    else:
        count = getattr(mapdl.geometry, selector)

    assert len(count) == imax
    mapdl.cm("mycomp", entity)

    assert "mycomp" in mapdl.components
    assert len(mapdl.components["mycomp"]) == imax
    assert np.allclose(mapdl.components["mycomp"], list(range(1, imax + 1)))
