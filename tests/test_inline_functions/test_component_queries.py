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

from conftest import TestClass, create_geometry, get_details_of_nodes


class TestCentroidGetter(TestClass):

    @pytest.fixture(scope="class")
    def box_geometry(self, mapdl):
        areas, keypoints = create_geometry(mapdl)
        q = mapdl.queries
        return q, keypoints, areas, get_details_of_nodes(mapdl)

    def test_centroid_getter_x(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        x = q.centrx(1)
        assert x is not None

    def test_centroid_getter_y(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        y = q.centry(1)
        assert y is not None

    def test_centroid_getter_z(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        z = q.centrz(1)
        assert z is not None

    def test_component_query_nx(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        x = q.nx(1)
        assert x == nodes[1].x

    def test_component_query_ny(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        y = q.ny(1)
        assert y == nodes[1].y

    def test_component_query_nz(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        z = q.nz(1)
        assert z == nodes[1].z

    def test_component_query_kx(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        # first kp at (0, 0, 0)
        x = q.kx(kps[0])
        assert x == 0.0

    def test_component_query_ky(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        y = q.ky(kps[0])
        assert y == 0.0

    def test_component_query_kz(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        z = q.kz(kps[0])
        assert z == 0.0

    @pytest.mark.parametrize("coords", [(0, 0, 0), (0.5, 0.5, 0.5), (100, 100, 100)])
    def test_inverse_get_node_at_coordinates(self, box_geometry, coords):
        q, kps, areas, nodes = box_geometry
        node = q.node(*coords)
        assert node in nodes

    def test_inverse_get_node_matches_known_node(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        for number, node in nodes.items():
            calculated_node = q.node(node.x, node.y, node.z)
            assert number == calculated_node

    @pytest.mark.parametrize("coords", [(0, 0, 0), (0.5, 0.5, 0.5), (100, 100, 100)])
    def test_inverse_get_keypoints_at_coordinates(self, box_geometry, coords):
        q, kps, areas, nodes = box_geometry
        kp = q.kp(*coords)
        assert kp in kps


class TestDisplacementComponentQueriesBox(TestClass):

    @pytest.fixture(scope="class")
    def solved_box(self, mapdl):
        with mapdl.muted:  # improve stability
            mapdl.et(1, "SOLID5")
            mapdl.block(0, 10, 0, 20, 0, 30)
            mapdl.esize(10)
            mapdl.vmesh("ALL")
            mapdl.units("SI")  # SI - International system (m, kg, s, K).
            # Define a material (nominal steel in SI)
            mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
            mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
            mapdl.mp("PRXY", 1, 0.3)  # Poisson's Ratio
            # Fix the left-hand side.
            mapdl.nsel("S", "LOC", "Z", 0)
            mapdl.d("ALL", "UX")
            mapdl.d("ALL", "UY")
            mapdl.d("ALL", "UZ")

            mapdl.nsel("S", "LOC", "Z", 30)
            mapdl.f("ALL", "FX", 1000)
            mapdl.run("/SOLU")
            mapdl.antype("STATIC")
            mapdl.solve()
            mapdl.finish()

        q = mapdl.queries
        return q, get_details_of_nodes(mapdl)

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


class TestDisplacementComponentQueriesSheet(TestClass):

    @pytest.fixture(scope="class")
    def twisted_sheet(self, mapdl):
        mapdl.et(1, "SHELL181")
        mapdl.mp("EX", 1, 2e5)
        mapdl.mp("PRXY", 1, 0.3)  # Poisson's Ratio
        mapdl.rectng(0, 1, 0, 1)
        mapdl.sectype(1, "SHELL")
        mapdl.secdata(0.1)
        mapdl.esize(0.5)
        mapdl.amesh("all")
        mapdl.run("/SOLU")
        mapdl.antype("STATIC")
        mapdl.nsel("s", "loc", "x", 0)
        mapdl.d("all", "all")
        mapdl.nsel("s", "loc", "x", 1)
        mapdl.d("all", "ux", -0.1)
        mapdl.d("all", "uy", -0.1)
        mapdl.d("all", "uz", -0.1)
        mapdl.allsel("all")
        mapdl.solve()
        mapdl.finish()
        q = mapdl.queries
        return q, get_details_of_nodes(mapdl)

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
