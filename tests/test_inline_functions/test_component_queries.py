# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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


class TestCentroidGetter:
    def test_x(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        x = q.centrx(1)
        assert x is not None

    def test_y(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        y = q.centry(1)
        assert y is not None

    def test_z(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        z = q.centrz(1)
        assert z is not None


class TestComponentQueries:
    def test_nx(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        x = q.nx(1)
        assert x == nodes[1].x

    def test_ny(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        y = q.ny(1)
        assert y == nodes[1].y

    def test_nz(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        z = q.nz(1)
        assert z == nodes[1].z

    def test_kx(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        # first kp at (0, 0, 0)
        x = q.kx(kps[0])
        assert x == 0.0

    def test_ky(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        y = q.ky(kps[0])
        assert y == 0.0

    def test_kz(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        z = q.kz(kps[0])
        assert z == 0.0


class TestInverseGetFunctions:
    @pytest.mark.parametrize("coords", [(0, 0, 0), (0.5, 0.5, 0.5), (100, 100, 100)])
    def test_get_node_at_coordinates(self, box_geometry, coords):
        q, kps, areas, nodes = box_geometry
        node = q.node(*coords)
        assert node in nodes

    def test_get_node_matches_known_node(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        for number, node in nodes.items():
            calculated_node = q.node(node.x, node.y, node.z)
            assert number == calculated_node

    @pytest.mark.parametrize("coords", [(0, 0, 0), (0.5, 0.5, 0.5), (100, 100, 100)])
    def test_get_keypoints_at_coordinates(self, box_geometry, coords):
        q, kps, areas, nodes = box_geometry
        kp = q.kp(*coords)
        assert kp in kps


class TestDisplacementComponentQueries:
    def test_ux(self, solved_box):
        q, nodes = solved_box
        displaced_nodes = [node for node in nodes if abs(q.ux(node)) > 0]
        assert len(displaced_nodes) > 0

    def test_uy(self, solved_box):
        q, nodes = solved_box
        displaced_nodes = [node for node in nodes if abs(q.uy(node)) > 0]
        assert len(displaced_nodes) > 0

    def test_uz(self, solved_box):
        q, nodes = solved_box
        displaced_nodes = [node for node in nodes if abs(q.uz(node)) > 0]
        assert len(displaced_nodes) > 0

    def test_rotx(self, twisted_sheet):
        q, nodes = twisted_sheet
        displaced_nodes = [node for node in nodes if abs(q.rotx(node)) > 0]
        assert len(displaced_nodes) > 0

    def test_roty(self, twisted_sheet):
        q, nodes = twisted_sheet
        displaced_nodes = [node for node in nodes if abs(q.roty(node)) > 0]
        assert len(displaced_nodes) > 0

    def test_rotz(self, twisted_sheet):
        q, nodes = twisted_sheet
        displaced_nodes = [node for node in nodes if abs(q.rotz(node)) > 0]
        assert len(displaced_nodes) > 0
