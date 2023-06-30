import re
import warnings

import numpy as np
import pytest

from ansys.mapdl.core.errors import (
    ComponentDoesNotExits,
    ComponentIsNotSelected,
    ComponentNoData,
)


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


@pytest.mark.parametrize("type_", ("node", "elem", "kp", "line", "area", "volu"))
def test_set_item(mapdl, cube_solve, type_):
    mapdl.prep7()
    mapdl.vgen(3, "all")  # creating more volumes

    comp_name = "MYCOMP2"
    mapdl.components[comp_name] = type_, [1, 2, 3]

    cm_ = mapdl.run("cmlist").upper()
    assert comp_name not in cm_

    mapdl.cmsel("S", comp_name)
    cm_ = mapdl.run("cmlist").upper()
    assert comp_name in cm_
    assert type_.upper() in cm_

    cm_ = mapdl.run(f"cmlist,{comp_name},1")
    assert comp_name in cm_
    assert type_.upper() in cm_
    assert re.search(r"1\s*2\s*3", cm_) is not None


def test_set_item_no_type(mapdl, cube_solve):
    mapdl.components["mycomp"] = (1, 2, 3)

    mapdl.cmsel("S", "MYCOMP")
    cm_ = mapdl.run("cmlist").upper()
    assert "MYCOMP" in cm_
    assert "NODE" in cm_


def test_get_item(mapdl, cube_solve):
    mapdl.components["mycomp"] = "node", [1, 2, 3]

    with pytest.raises(ComponentIsNotSelected):
        mapdl.components["mycomp"]

    with pytest.raises(ComponentDoesNotExits):
        mapdl.components["noexist"]

    mapdl.cmsel("S", "mycomp")
    comp = mapdl.components["mycomp"]

    assert comp == tuple([1, 2, 3])
    assert comp.type == "NODE"


def test_get_item_lose_mode(mapdl, cube_solve):
    mapdl.components["mycomp"] = "node", [1, 2, 3]

    mapdl.components._lose_mode = True
    cm_ = mapdl.run("cmlist").upper()
    assert "MYCOMP" not in cm_
    assert "NODE" not in cm_

    assert mapdl.components["mycomp"] == (1, 2, 3)


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

    if entity == "line":
        # it is a pyvista.polydata
        assert count.n_cells == imax
    elif entity == "area":
        assert len(count()) == imax
    else:
        assert len(count) == imax

    mapdl.cm("mycomp", entity)

    assert "mycomp" in mapdl.components
    assert len(mapdl.components["mycomp"]) == imax
    assert np.allclose(mapdl.components["mycomp"], list(range(1, imax + 1)))


def test_defaul_entity_warning(mapdl, cube_solve):
    mapdl.allsel()
    with pytest.warns(UserWarning):
        mapdl.components["mycomp"] = (1, 2, 3)

    mapdl.components.default_entity_warning = False
    with warnings.catch_warnings():
        mapdl.components["mycomp"] = (1, 2, 3)

    mapdl.components.default_entity_warning = True


@pytest.mark.parametrize("type_", ("node", "elem", "kp", "line", "area", "volu"))
def test_default_entity(mapdl, cube_solve, type_):
    mapdl.prep7()
    mapdl.vgen(3, "all")  # creating more volumes
    mapdl.allsel()

    comp_name = "MYCOMP2"
    mapdl.components.default_entity = type_
    mapdl.components[comp_name] = [1, 2, 3]

    mapdl.cmsel("S", comp_name)
    cm_ = mapdl.run("cmlist").upper()
    assert comp_name in cm_
    assert type_.upper() in cm_


@pytest.mark.parametrize(
    "func,entity,selector,imax",
    (
        ["nsel", "node", "nodes", 2],
        ["esel", "elem", "elem", 3],
        ["ksel", "kp", "keypoints", 4],
        ["lsel", "line", "lines", 5],
        ["asel", "area", "areas", 6],
        ["vsel", "volu", "vnum", 1],
    ),
)
def test_set_only_type(mapdl, cube_solve, func, entity, selector, imax):
    func_ = getattr(mapdl, func)
    func_("S", vmin=1, vmax=imax)  # selecting

    mapdl.components["mycomp"] = entity

    comp = mapdl.components["mycomp"]
    assert len(comp) == imax
    assert comp.type == entity.upper()
