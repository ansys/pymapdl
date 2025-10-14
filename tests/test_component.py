# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import warnings

import numpy as np
import pytest

from ansys.mapdl.core.component import (
    Component,
    ComponentDoesNotExits,
    ComponentIsNotSelected,
    ComponentManager,
)
from ansys.mapdl.core.errors import ComponentNoData
from conftest import TestClass


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


def test_raise_empty_comp(mapdl, cleared):
    with pytest.raises(ComponentNoData):
        mapdl.cm("cm1", "nodes")


def test_componentmanager_wrong_object():
    with pytest.raises(TypeError):
        ComponentManager("asdf")


def test_component():
    cm = Component("NODE", [1, 2, 3])

    assert "NODE" in str(cm)
    assert all([str(each) in str(cm) for each in [1, 2, 3]])


def test_component_attributes():
    cm = Component("AREA", [1, 2, 3])

    assert "AREA" == cm.type
    assert 1 in cm
    assert 3 in cm


def test_component_wrong_init():
    with pytest.raises(ValueError, match="is not allowed for 'type' definition."):
        Component(1, 1)

    with pytest.raises(ValueError, match="is not allowed for 'type' definition."):
        Component("asdf", [1, 2, 3])


def test_logger(mapdl, cleared):
    assert mapdl.components.logger == mapdl.logger


def test_parsing_too_many_components(mapdl, cleared):
    mapdl.prep7()

    for i in range(1, 100):
        mapdl.nsel("NONE")
        mapdl.n(i, i, 0, 0)
        mapdl.cm(f"node_{i:03.0f}", "NODE")

    s = mapdl.components.__str__()
    assert len(mapdl.components._comp) == 99

    assert "VERIFICATION" not in s
    assert "***" not in s
    assert "*****MAPDL" not in s
    for i in range(1, 100):
        assert re.search(f"NODE_{i:03.0f}" + r"\s+: NODE", s)


class Test_components(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def setup(mapdl):
        # setup the full file
        mapdl.block(0, 1, 0, 1, 0, 1)
        mapdl.et(1, 186)
        mapdl.esize(0.5)
        mapdl.vmesh("all")

        # Define a material (nominal steel in SI)
        mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
        mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
        mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

        mapdl.vgen(3, "all")  # creating more volumes
        mapdl.save("components", slab="all")

    @staticmethod
    @pytest.fixture(scope="function")
    def reset(mapdl, setup):  # basic_components
        # cleaning
        mapdl.cmsel("all")
        for each in mapdl.components:
            mapdl.cmdele(each)

    @staticmethod
    @pytest.fixture(scope="function")
    def basic_components(mapdl, reset):
        # Reset the components
        mapdl.components["mycomp1"] = "NODE", [1, 2, 3]
        mapdl.components["mycomp2"] = "KP", [1, 3]

        mapdl.cmsel("s", "mycomp1")
        mapdl.cmsel("a", "mycomp2")

    @staticmethod
    @pytest.mark.parametrize("type_", ("node", "elem", "kp", "line", "area", "volu"))
    def test_set_item(mapdl, reset, type_):
        mapdl.prep7()
        # mapdl.vgen(3, "all")  # creating more volumes

        comp_name = "MYCOMP2"
        mapdl.components[comp_name] = type_, [1, 2, 3]

        cm_ = mapdl.run("cmlist").upper()
        assert (
            comp_name in cm_
        )  # the component should be selected already after creation

        mapdl.cmsel("S", comp_name)
        cm_ = mapdl.run("cmlist").upper()
        assert comp_name in cm_
        assert type_.upper() in cm_

        cm_ = mapdl.run(f"cmlist,{comp_name},1")
        assert comp_name in cm_
        assert type_.upper() in cm_
        assert re.search(r"1\s*2\s*3", cm_) is not None

    @staticmethod
    def test_set_item_no_type(mapdl, reset):
        mapdl.components["mycomp"] = (1, 2, 3)

        mapdl.cmsel("S", "MYCOMP")
        cm_ = mapdl.run("cmlist").upper()
        assert "MYCOMP" in cm_
        assert "NODE" in cm_

    @staticmethod
    def test_get_item(mapdl, reset):
        mapdl.components["mycomp"] = "node", [1, 2, 3]

        mapdl.cmsel("NONE")
        with pytest.raises(ComponentIsNotSelected):
            mapdl.components["mycomp"]

        with pytest.raises(ComponentDoesNotExits):
            mapdl.components["noexist"]

        mapdl.cmsel("S", "mycomp")
        comp = mapdl.components["mycomp"]

        assert comp == tuple([1, 2, 3])
        assert comp.type == "NODE"

    @staticmethod
    def test_get_item_autoselect_components(mapdl, reset):
        mapdl.components["mycomp"] = "node", [1, 2, 3]
        mapdl.cmsel("NONE")

        prev = mapdl.components._autoselect_components
        mapdl.components._autoselect_components = True
        cm_ = mapdl.run("cmlist").upper()
        assert "MYCOMP" not in cm_
        assert "NODE" not in cm_

        assert mapdl.components["mycomp"] == (1, 2, 3)
        mapdl.components._autoselect_components = prev

    @staticmethod
    def test_contains_all(mapdl, reset):
        mapdl.allsel()
        mapdl.cm("allnodes", "nodes")
        assert "allnodes" in mapdl.components
        assert np.allclose(mapdl.components["allnodes"], mapdl.mesh.nnum_all)

    @staticmethod
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
    def test_contains_entities(mapdl, reset, func, entity, selector, imax):
        func_ = getattr(mapdl, func)
        func_("S", vmin=1, vmax=imax)

        assert mapdl.get_value(entity[:4], 0, "count") == imax

        mapdl.cm("mycomp", entity)

        assert "mycomp" in mapdl.components
        assert len(mapdl.components["mycomp"]) == imax
        assert np.allclose(mapdl.components["mycomp"], list(range(1, imax + 1)))

    @staticmethod
    def test_defaul_entity_warning(mapdl, reset):
        mapdl.allsel()
        with pytest.warns(UserWarning):
            mapdl.components["mycomp"] = (1, 2, 3)

        mapdl.components.default_entity_warning = False
        with warnings.catch_warnings(record=True):
            mapdl.components["mycomp"] = (1, 2, 3)

        mapdl.components.default_entity_warning = True

    @staticmethod
    @pytest.mark.parametrize("type_", ("node", "elem", "kp", "line", "area", "volu"))
    def test_default_entity(mapdl, reset, type_):
        mapdl.prep7()
        # mapdl.vgen(3, "all")  # creating more volumes
        mapdl.allsel()

        comp_name = "MYCOMP2"
        mapdl.components.default_entity = type_
        mapdl.components[comp_name] = [1, 2, 3]

        mapdl.cmsel("S", comp_name)
        cm_ = mapdl.run("cmlist").upper()
        assert comp_name in cm_
        assert type_.upper() in cm_

        # Returning back to default
        mapdl.components.default_entity = "NODES"

    @staticmethod
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
    def test_set_only_type(mapdl, reset, func, entity, selector, imax):
        func_ = getattr(mapdl, func)
        func_("S", vmin=1, vmax=imax)  # selecting

        mapdl.components["mycomp"] = entity

        comp = mapdl.components["mycomp"]
        assert len(comp) == imax
        assert comp.type == entity.upper()

    @staticmethod
    def test_set_using_a_component(mapdl, reset):
        comp = Component("AREA", [1, 2])
        mapdl.components["myareacomp"] = comp

        mapdl.cmsel("s", "MYAREACOMP")
        assert "MYAREACOMP" in mapdl.components
        comp2 = mapdl.components["myareacomp"]
        assert comp2 == (1, 2)
        assert comp2.type == "AREA"

    @staticmethod
    def test_set_assign_wrong_objects(mapdl, reset):
        with pytest.raises(ValueError, match="Only strings are allowed for "):
            mapdl.components[1] = [1, 2]

        with pytest.raises(ValueError, match="is not allowed for 'type' definition."):
            mapdl.components["asdf"] = "asdf"

        with pytest.raises(
            ValueError, match="Only strings or tuples are allowed for assignment"
        ):
            mapdl.components["asdf"] = {"a": 1}

        with pytest.raises(ValueError, match="Only integers are allowed for component"):
            mapdl.components["asdf"] = [1, 2.2]

        with pytest.raises(ValueError, match="Only integers are allowed for component"):
            mapdl.components["asdf"] = [1, "asdf"]

        with pytest.raises(ValueError):
            mapdl.components["asdf"] = (1, "asdf")

        with pytest.raises(ValueError):
            mapdl.components["asdf"] = "asdf", [1, 1.1]

    @staticmethod
    def test_default_entity_error(mapdl, reset):
        with pytest.raises(
            ValueError, match="Only the following entities are allowed:"
        ):
            mapdl.components.default_entity = "asdf"

    @staticmethod
    def test__get_all_components_type(mapdl, reset):
        mapdl.allsel()
        mapdl.esel("s", "", "", 1)
        mapdl.nsel("s", "", "", 1)
        mapdl.cm("cmelem", "ELEM")
        mapdl.cm("cmnodes", "NODE")

        mapdl.nsel("a", "", "", 2)
        mapdl.esel("a", "", "", 2)
        mapdl.cm("cmnodes2", "NODE")
        mapdl.cm("cmelem2", "ELEM")

        comp_elem = mapdl.components._get_all_components_type("ELEM")

        expected_output = {"CMELEM": (1,), "CMELEM2": (1, 2)}
        assert comp_elem
        assert comp_elem == expected_output
        assert "CMNODES" not in comp_elem
        assert "CMNODES2" not in comp_elem

        # Nodes
        comp_nodes = mapdl.components._get_all_components_type("NODE")

        expected_output = {"CMNODES": (1,), "CMNODES2": (1, 2)}
        assert comp_nodes
        assert comp_nodes == expected_output
        assert "CMELEM" not in comp_nodes
        assert "CMELEM2" not in comp_nodes

    @staticmethod
    def test_dunder_methods_iter(mapdl, basic_components):
        for each1, each2 in zip(
            mapdl.components, (["NODE", [1, 2, 3]], ["KP", [1, 3]])
        ):
            comp = mapdl.components[each1]
            assert comp.type == each2[0]
            assert comp == tuple(each2[1])

    @staticmethod
    def test_dunder_methods_keys(mapdl, basic_components):
        assert ["MYCOMP1", "MYCOMP2"] == list(mapdl.components.names)

    @staticmethod
    def test_dunder_methods_types(mapdl, basic_components):
        assert ["NODE", "KP"] == list(mapdl.components.types)

    @staticmethod
    def test_dunder_methods_items(mapdl, basic_components):
        assert [("MYCOMP1", "NODE"), ("MYCOMP2", "KP")] == list(
            mapdl.components.items()
        )

    @staticmethod
    def test_dunder_methods_len(mapdl, basic_components):
        assert len(mapdl.components) == 2
        mapdl.components["mycomp3"] = "NODE", [1, 2]
        assert len(mapdl.components) == 3
        mapdl.nsel("s", vmin=1)
        mapdl.cm("asdf", "node")
        assert len(mapdl.components) == 4


def test_big_component(mapdl, cleared):
    mapdl.prep7()

    for i in range(1000):
        mapdl.n(i, i, 0, 0)

    mapdl.allsel()
    mapdl.cm("many_nodes", "NODE")

    print(mapdl.mesh)  # This will trigger COMP parsing

    assert "MANY_NODES" in str(mapdl.components)
    assert len(mapdl.components["many_nodes"]) == 999
    assert all(isinstance(item, int) for item in mapdl.components["many_nodes"])
