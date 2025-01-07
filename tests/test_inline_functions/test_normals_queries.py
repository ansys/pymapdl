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

from conftest import TestClass


class TestNormalsNodeQueries(TestClass):
    @staticmethod
    def build_plane(mapdl, plane: str):
        n1 = mapdl.n(1, 0, 0, 0)
        if plane == "xy":
            n2 = mapdl.n(2, 0, 1, 0)
            n3 = mapdl.n(3, 1, 1, 0)
        elif plane == "xz":
            n2 = mapdl.n(2, 1, 0, 0)
            n3 = mapdl.n(3, 1, 0, 1)
        elif plane == "yz":
            n2 = mapdl.n(2, 0, 1, 0)
            n3 = mapdl.n(3, 0, 1, 1)
        return n1, n2, n3

    def test_normnx(self, query):
        nodes = self.build_plane(query._mapdl, "yz")
        cosine = query.normnx(*nodes)
        assert abs(cosine) == 1.0

    def test_normny(self, query):
        nodes = self.build_plane(query._mapdl, "xz")
        cosine = query.normny(*nodes)
        assert abs(cosine) == 1.0

    def test_normnz(self, query):
        nodes = self.build_plane(query._mapdl, "xy")
        cosine = query.normnz(*nodes)
        assert abs(cosine) == 1.0


class TestNormalsKeypointsQueries(TestClass):
    @staticmethod
    def build_plane(mapdl, plane: str):
        k1 = mapdl.k(1, 0, 0, 0)
        if plane == "xy":
            k2 = mapdl.k(2, 0, 1, 0)
            k3 = mapdl.k(3, 1, 1, 0)
        elif plane == "xz":
            k2 = mapdl.k(2, 1, 0, 0)
            k3 = mapdl.k(3, 1, 0, 1)
        elif plane == "yz":
            k2 = mapdl.k(2, 0, 1, 0)
            k3 = mapdl.k(3, 0, 1, 1)
        return k1, k2, k3

    def test_normkx(self, query):
        keypoints = self.build_plane(query._mapdl, "yz")
        cosine = query.normkx(*keypoints)
        assert abs(cosine) == 1.0

    def test_normky(self, query):
        keypoints = self.build_plane(query._mapdl, "xz")
        cosine = query.normky(*keypoints)
        assert abs(cosine) == 1.0

    def test_normkz(self, query):
        keypoints = self.build_plane(query._mapdl, "xy")
        cosine = query.normkz(*keypoints)
        assert abs(cosine) == 1.0
