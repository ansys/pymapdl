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

from math import isclose

import pytest

from conftest import TestClass


class TestLineCoordinateQueries(TestClass):

    @pytest.fixture(scope="class")
    def line_geometry(self, mapdl):
        k0 = mapdl.k(1, 0, 0, 0)
        k1 = mapdl.k(2, 1, 2, 2)
        l0 = mapdl.l(k0, k1)
        q = mapdl.queries
        return q, [k0, k1], l0

    def test_lx(self, line_geometry):
        q, kps, line = line_geometry
        x = q.lx(line, 0.5)
        assert x == 0.5

    def test_ly(self, line_geometry):
        q, kps, line = line_geometry
        y = q.ly(line, 0.5)
        assert y == 1.0

    def test_lz(self, line_geometry):
        q, kps, line = line_geometry
        z = q.lz(line, 0.5)
        assert z == 1.0


class TestLineSlopeQueries(TestClass):
    @pytest.fixture(scope="class")
    def line_geometry(self, mapdl):
        k0 = mapdl.k(1, 0, 0, 0)
        k1 = mapdl.k(2, 1, 2, 2)
        l0 = mapdl.l(k0, k1)
        q = mapdl.queries
        return q, [k0, k1], l0

    def test_lsx(self, line_geometry):
        q, kps, line = line_geometry
        sx = q.lsx(line, 0.5)
        actual = 1.0 / 3.0
        assert isclose(sx, actual)

    def test_lsy(self, line_geometry):
        q, kps, line = line_geometry
        sy = q.lsy(line, 0.5)
        actual = 2.0 / 3.0
        assert isclose(sy, actual)

    def test_lsz(self, line_geometry):
        q, kps, line = line_geometry
        sz = q.lsz(line, 0.5)
        actual = 2.0 / 3.0
        assert isclose(sz, actual)
