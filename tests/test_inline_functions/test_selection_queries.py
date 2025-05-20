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

import pytest

from ansys.mapdl.core.inline_functions import SelectionStatus
from conftest import TestClass


class TestSelectionStatus:
    @pytest.mark.parametrize("value", [1, -1, 0, 1.0, -1.0, 0.0])
    def test_happy(self, value):
        select = SelectionStatus(value)
        assert select == value
        assert select is not value

    @pytest.mark.parametrize("value", [1.5, 999, 99.0, "1"])
    def test_unhappy(self, value):
        with pytest.raises(ValueError):
            SelectionStatus(value)


class TestXSEL(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def selection_test_geometry(mapdl):
        k0 = mapdl.k(1, 0, 0, 0)
        k1 = mapdl.k(2, 0, 0, 1)
        k2 = mapdl.k(3, 0, 1, 0)
        k3 = mapdl.k(4, 1, 0, 0)
        mapdl.v(k0, k1, k2, k3)
        mapdl.mshape(1, "3D")
        mapdl.et(1, "SOLID98")
        mapdl.esize(0.5)
        mapdl.vmesh("ALL")
        return mapdl.queries


class TestNSEL(TestXSEL):
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.nsel("S", "LOC", "X", 0)
        node = q.node(0, 0, 0)
        select = q.nsel(node)
        assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        node = q.node(0, 0, 0)
        q._mapdl.nsel("NONE")
        select = q.nsel(node)
        assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.nsel(999)
        assert select == 0


class TestKSEL(TestXSEL):
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.ksel("S", "LOC", "X", 0)
        node = q.kp(0, 0, 0)
        select = q.ksel(node)
        assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        node = q.kp(0, 0, 0)
        q._mapdl.ksel("NONE")
        select = q.ksel(node)
        assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.ksel(999)
        assert select == 0


class TestLSEL(TestXSEL):
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.lsel("all")
        # there are 6 lines numbered 1-6
        for line in range(1, 7, 1):
            select = q.lsel(line)
            assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.lsel("NONE")
        for line in range(1, 7, 1):
            select = q.lsel(line)
            assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.lsel(999)
        assert select == 0


class TestASEL(TestXSEL):
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.asel("all")
        # there are 4 areas numbered 1-4
        for area in range(1, 5, 1):
            select = q.asel(area)
            assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.asel("NONE")
        for area in range(1, 5, 1):
            select = q.asel(area)
            assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.asel(999)
        assert select == 0


class TestESEL(TestXSEL):
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.esel("all")
        # there are at least 4 elements numbered 1-4
        for element in range(1, 5, 1):
            select = q.esel(element)
            assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.esel("NONE")
        for element in range(1, 5, 1):
            select = q.esel(element)
            assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.esel(999)
        assert select == 0


class TestVSEL(TestXSEL):
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.vsel("all")
        select = q.vsel(1)
        assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.vsel("NONE")
        select = q.vsel(1)
        assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.vsel(999)
        assert select == 0


class TestNDNEXT(TestXSEL):
    def test_existing_nodes(
        self, selection_test_geometry, common_functions_and_classes
    ):
        (
            get_details_of_nodes,
            get_details_of_elements,
            _,
            _,
        ) = common_functions_and_classes
        q = selection_test_geometry
        nodes = get_details_of_nodes(q._mapdl)
        next_ = q.ndnext(1)
        assert next_ in nodes

    def test_unselected_nodes(
        self, selection_test_geometry, common_functions_and_classes
    ):
        (
            get_details_of_nodes,
            get_details_of_elements,
            _,
            _,
        ) = common_functions_and_classes
        q = selection_test_geometry
        nodes = get_details_of_nodes(q._mapdl)
        last_node = len(nodes)
        next_ = q.ndnext(last_node)
        assert next_ == 0

    def test_non_existing_nodes(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.ndnext(999)
        assert next_ == 0


class TestELNEXT(TestXSEL):
    def test_existing_elements(
        self, selection_test_geometry, common_functions_and_classes
    ):
        (
            get_details_of_nodes,
            get_details_of_elements,
            _,
            _,
        ) = common_functions_and_classes
        q = selection_test_geometry
        elements = get_details_of_elements(q._mapdl)
        next_ = q.elnext(1)
        assert next_ in elements

    def test_unselected_elements(
        self, selection_test_geometry, common_functions_and_classes
    ):
        (
            get_details_of_nodes,
            get_details_of_elements,
            _,
            _,
        ) = common_functions_and_classes
        q = selection_test_geometry
        elements = get_details_of_elements(q._mapdl)
        last_element = len(elements)
        next_ = q.elnext(last_element)
        assert next_ == 0

    def test_non_existing_elements(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.elnext(999)
        assert next_ == 0


class TestKPNEXT(TestXSEL):
    def test_existing_kps(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.kpnext(1)
        assert next_ == 2

    def test_unselected_kps(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.kpnext(4)
        assert next_ == 0

    def test_non_existing_kps(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.kpnext(999)
        assert next_ == 0


class TestLSNEXT(TestXSEL):
    def test_existing_lines(self, selection_test_geometry):
        # there are 6 lines in in the selection_test_geometry fixture
        q = selection_test_geometry
        next_ = q.lsnext(1)
        assert next_ == 2

    def test_unselected_lines(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.lsnext(6)
        assert next_ == 0

    def test_non_existing_lines(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.lsnext(999)
        assert next_ == 0


class TestARNEXT(TestXSEL):
    def test_existing_areas(self, selection_test_geometry):
        # there are 4 areas in in the selection_test_geometry fixture
        q = selection_test_geometry
        next_ = q.arnext(1)
        assert next_ == 2

    def test_unselected_areas(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.arnext(4)
        assert next_ == 0

    def test_non_existing_areas(self, selection_test_geometry):
        q = selection_test_geometry
        next_ = q.arnext(999)
        assert next_ == 0


class TestVLNEXT(TestXSEL):
    @staticmethod
    def make_volumes(mapdl):
        point1 = mapdl.k(999, 0, 10, 0)
        point2 = mapdl.k(99, 0, 0, 10)
        kps = [mapdl.k(i + 1, i, 0, 0) for i in range(10)]
        vols = [mapdl.v(i, i + 1, point1, point2) for i in kps[:-1]]
        return vols

    def test_existing_volumes(self, query):
        q = query
        _ = self.make_volumes(q._mapdl)
        next_ = q.vlnext(1)
        assert next_ == 2

    def test_unselected_volumes(self, query):
        q = query
        vols = self.make_volumes(q._mapdl)
        next_ = q.vlnext(len(vols))
        assert next_ == 0

    def test_non_existing_volumes(self, query):
        next_ = query.vlnext(999)
        assert next_ == 0
