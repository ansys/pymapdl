# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

from conftest import TestClass, create_geometry, get_details_of_nodes


class TestConnectivityQueries(TestClass):

    @pytest.fixture(scope="class")
    def box_geometry(self, mapdl):
        areas, keypoints = create_geometry(mapdl)
        q = mapdl.queries
        return q, keypoints, areas, get_details_of_nodes(mapdl)

    def test_nelem(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        ns = [q.nelem(1, i) for i in range(1, 21)]
        for n in ns:
            assert n in nodes or n == 0

    def test_enextn(self, box_geometry, common_functions_and_classes):
        _, get_details_of_elements, _, _ = common_functions_and_classes
        q, kps, areas, nodes = box_geometry
        es = [q.enextn(n, 1) for n in nodes]
        for e in es:
            assert e > 0
