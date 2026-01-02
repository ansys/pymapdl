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

"""Test mesh"""
import os

import numpy as np
import pytest

from conftest import has_dependency, requires

if has_dependency("pyvista"):
    import pyvista as pv

from ansys.mapdl.core import examples


def test_empty_model(mapdl, cleared):
    assert mapdl.mesh.nnum.size == 0
    assert mapdl.mesh.enum.size == 0

    assert mapdl.mesh.n_elem == 0
    assert mapdl.mesh.n_node == 0


def test_mesh_attributes(mapdl, cube_geom_and_mesh):
    mapdl.allsel()
    assert mapdl.mesh.n_node == mapdl.get("__par__", "node", "0", "count")
    assert mapdl.mesh.n_elem == mapdl.get("__par__", "elem", "0", "count")

    assert len(mapdl.mesh.nnum) == mapdl.get("__par__", "node", "0", "count")
    assert len(mapdl.mesh.enum) == mapdl.get("__par__", "elem", "0", "count")

    mapdl.dim("par", "", len(mapdl.mesh.nnum))
    mapdl.starvget("par", "NODE", "0", "NLIST")
    assert np.allclose(mapdl.parameters["par"].flatten(), mapdl.mesh.nnum)

    mapdl.dim("par", "", len(mapdl.mesh.enum))
    mapdl.starvget("par", "ELEM", "0", "ELIST")
    assert np.allclose(mapdl.parameters["par"].flatten(), mapdl.mesh.enum)


def test_elem_num_in_mesh_elem(mapdl, cube_geom_and_mesh):
    enums = np.array([each[8] for each in mapdl.mesh.elem])
    assert np.allclose(mapdl.mesh.enum, enums)


def test_repr(mapdl, cube_geom_and_mesh):
    out = str(mapdl.mesh)

    assert isinstance(out, str)
    assert "Number of Element Types" in out


def test_mapdl(mapdl, cleared):
    from ansys.mapdl.core.mapdl import MapdlBase

    assert isinstance(mapdl.mesh._mapdl, MapdlBase)


def test_local(mapdl, cleared):
    assert isinstance(mapdl.mesh.local, bool)
    assert mapdl._local == mapdl.mesh.local


@requires("pyvista")
def test_empty_mesh(mapdl, cleared):
    # Reset mesh grid
    mapdl.mesh._grid_cache = None
    assert mapdl.mesh.grid is not None

    # To avoid further cache updates
    with mapdl.mesh.ignore_cache_reset:

        if has_dependency("pyvista"):
            assert mapdl.mesh.grid.points.size == 0
            assert mapdl.mesh.grid.cells.size == 0
            assert mapdl.mesh.grid.n_points == 0
            assert mapdl.mesh.grid.n_cells == 0

        assert mapdl.mesh.n_node == 0
        assert mapdl.mesh.n_elem == 0
        assert mapdl.mesh.nnum_all.size == 0
        assert mapdl.mesh.enum_all.size == 0
        assert mapdl.mesh.nnum.size == 0
        assert mapdl.mesh.enum.size == 0
        assert mapdl.mesh.nodes.size == 0
        # assert mapdl.mesh.node_angles.size == 0 Not implemented

        # elem is a list
        assert len(mapdl.mesh.elem) == 0

        # Using size because it should be empty arrays
        assert mapdl.mesh.ekey.size == 0
        assert mapdl.mesh.et_id.size == 0
        assert mapdl.mesh.tshape.size == 0
        assert mapdl.mesh.material_type.size == 0
        assert mapdl.mesh.etype.size == 0
        assert mapdl.mesh.section.size == 0
        assert mapdl.mesh.element_coord_system.size == 0
        assert mapdl.mesh.elem_real_constant.size == 0
        assert mapdl.mesh.ekey.size == 0

        # should be empty dicts
        assert not mapdl.mesh.key_option
        assert not mapdl.mesh.tshape_key
        assert not mapdl.mesh.element_components
        assert not mapdl.mesh.node_components

        # bools
        assert not mapdl.mesh._has_elements
        assert not mapdl.mesh._has_nodes

        # Others
        if has_dependency("pyvista"):
            assert mapdl.mesh.grid.points.size == 0
            assert mapdl.mesh.grid.cells.size == 0
            assert mapdl.mesh.grid.n_points == 0
            assert mapdl.mesh.grid.n_cells == 0


def test_element_node_components(mapdl, contact_geom_and_mesh):
    mapdl.allsel()
    assert not mapdl.mesh.element_components
    assert "MYELEMCOMP" not in mapdl.mesh.element_components

    assert mapdl.mesh.node_components
    assert "TN.TGT" in mapdl.mesh.node_components
    assert "CMNODE" not in mapdl.mesh.node_components

    mapdl.cmsel("NONE")
    mapdl.cm("CMNODE", "NODE")
    mapdl.components["MYELEMCOMP"] = "ELEM", (1, 2, 3)

    assert mapdl.mesh.element_components
    assert "MYELEMCOMP" in mapdl.mesh.element_components

    assert mapdl.mesh.node_components
    assert "TN.TGT" not in mapdl.mesh.node_components
    assert "CMNODE" in mapdl.mesh.node_components

    mapdl.cmsel("NONE")
    assert not mapdl.mesh.element_components
    assert "MYELEMCOMP" not in mapdl.mesh.element_components

    assert not mapdl.mesh.node_components
    assert "TN.TGT" not in mapdl.mesh.node_components
    assert "CMNODE" not in mapdl.mesh.node_components

    mapdl.cmsel("S", "MYELEMCOMP")
    assert mapdl.mesh.element_components
    assert "MYELEMCOMP" in mapdl.mesh.element_components

    assert not mapdl.mesh.node_components
    assert "TN.TGT" not in mapdl.mesh.node_components
    assert "CMNODE" not in mapdl.mesh.node_components

    mapdl.cmsel("S", "CMNODE")
    assert mapdl.mesh.node_components
    assert "CMNODE" in mapdl.mesh.node_components
    assert "TN.TGT" not in mapdl.mesh.node_components

    mapdl.cmsel("all")
    assert mapdl.mesh.node_components
    assert "TN.TGT" in mapdl.mesh.node_components
    assert "CMNODE" in mapdl.mesh.node_components


def test_non_empty_mesh(mapdl, contact_geom_and_mesh):
    assert mapdl.mesh.n_node > 0
    assert mapdl.mesh.n_elem > 0
    assert mapdl.mesh.nnum_all.size > 0
    assert mapdl.mesh.enum_all.size > 0
    assert mapdl.mesh.nnum.size > 0
    assert mapdl.mesh.enum.size > 0
    assert mapdl.mesh.nodes.size > 0
    # assert mapdl.mesh.node_angles.size > 0 Not implemented

    # This should be a list of arrays.
    assert len(mapdl.mesh.elem) > 0
    assert mapdl.mesh.elem[0].size > 0

    # Using size because it should be non-empty arrays
    assert mapdl.mesh.ekey.size > 0
    assert mapdl.mesh.et_id.size > 0
    assert mapdl.mesh.tshape.size > 0
    assert mapdl.mesh.material_type.size > 0
    assert mapdl.mesh.etype.size > 0
    assert mapdl.mesh.section.size > 0
    assert mapdl.mesh.element_coord_system.size > 0
    assert mapdl.mesh.elem_real_constant.size > 0

    # should be non empty dicts
    assert mapdl.mesh.key_option
    assert len(mapdl.mesh.key_option.keys()) > 0
    assert mapdl.mesh.tshape_key
    assert len(mapdl.mesh.tshape_key.keys()) > 0

    mapdl.allsel()
    mapdl.cmsel("all")
    mapdl.cm("CMNODE", "NODE")
    mapdl.components["MYELEMCOMP"] = "ELEM", (1, 2, 3)

    assert mapdl.mesh.element_components
    assert "MYELEMCOMP" in mapdl.mesh.element_components
    assert mapdl.mesh.node_components
    assert "CMNODE" in mapdl.mesh.node_components

    # bools
    assert mapdl.mesh._has_elements
    assert mapdl.mesh._has_nodes

    # Others
    if has_dependency("pyvista"):
        assert isinstance(mapdl.mesh.grid, pv.UnstructuredGrid)

        assert mapdl.mesh.grid.n_cells > 0
        assert mapdl.mesh.grid.n_points > 0


def test_tshape_key(mapdl, contact_geom_and_mesh):
    tshape = mapdl.mesh.tshape_key
    assert isinstance(tshape, dict)
    assert len(tshape.keys()) > 0

    tshape = mapdl.mesh.tshape
    assert isinstance(tshape, np.ndarray)
    assert tshape.size > 0


@requires("pyvista")
def test_save(mapdl, cube_geom_and_mesh):
    # This test seems to fail when parallelized.
    fname = "mesh.vtk"
    for binary_ in [True, False]:
        mapdl.mesh.save(fname, binary_)
        assert os.path.exists(fname)

        os.remove(fname)


def test_key_option(mapdl, contact_geom_and_mesh):
    assert mapdl.mesh.key_option is not None
    assert isinstance(mapdl.mesh.key_option, dict)
    assert len(mapdl.mesh.key_option.keys()) > 0


def test_section(mapdl, cube_geom_and_mesh):
    assert mapdl.mesh.section is not None
    assert isinstance(mapdl.mesh.section, np.ndarray)
    assert mapdl.mesh.section.size > 0


def test_element_coord_system(mapdl, cube_geom_and_mesh):
    assert mapdl.mesh.element_coord_system is not None
    assert isinstance(mapdl.mesh.element_coord_system, np.ndarray)
    assert mapdl.mesh.element_coord_system.size > 0


def test_enum(mapdl, cube_geom_and_mesh):
    assert mapdl.mesh.enum is not None
    assert isinstance(mapdl.mesh.enum, np.ndarray)
    assert mapdl.mesh.enum.size > 0
    assert np.allclose(mapdl.mesh.enum, [1, 2, 3, 4, 5, 6, 7, 8])


def test_nnum(mapdl, cube_geom_and_mesh):
    assert mapdl.mesh.nnum is not None
    assert isinstance(mapdl.mesh.nnum, np.ndarray)
    assert mapdl.mesh.nnum.size == 81


def test_ekey(mapdl, cube_geom_and_mesh):
    assert mapdl.mesh.ekey is not None
    assert isinstance(mapdl.mesh.ekey, np.ndarray)
    assert mapdl.mesh.ekey.size > 0
    assert np.allclose(mapdl.mesh.ekey, [[1, 186]])


def test_nodes(mapdl, cube_geom_and_mesh):
    assert mapdl.mesh.nodes is not None
    assert isinstance(mapdl.mesh.nodes, np.ndarray)
    assert mapdl.mesh.nodes.shape == (81, 3)


def test_nodes_in_current_CS(mapdl, cleared, cube_geom_and_mesh):
    for icoord in range(6):
        mapdl.csys(icoord)
        mapdl.dsys(icoord)

        assert np.allclose(
            mapdl.mesh.nodes_in_current_CS, mapdl.nlist().to_array()[:, 1:4], atol=1e-3
        )  # nlist is not as accurate as 'nodes_in_current_CS'


def test_nodal_rotation(mapdl, cleared):
    with open(examples.verif_files.vmfiles["vm275"], "r") as fid:
        vm = fid.read()

    vm = vm.lower().replace("nrotate,all", "nrotate,all\n/eof")
    mapdl.finish()
    mapdl.input_strings(vm)
    nrotations = mapdl.mesh.nodes_rotation
    nrotation_ref = np.array(
        [
            [0.00, 0.00, 4.00],
            [0.00, 0.00, 4.00],
            [0.00, 0.00, 4.00],
            [0.00, 0.00, 4.00],
            [0.00, 0.00, 4.00],
            [0.00, 0.00, 4.00],
            [0.00, 0.00, 4.00],
        ]
    )
    assert np.allclose(nrotation_ref, nrotations[:7, :])


def test_esln(mapdl, two_dimensional_mesh):
    mapdl.nsel("S", "LOC", "X", 0)
    selected_ids = mapdl.esln("S", 0)
    expected_selected_ids = np.array([1, 41, 81, 121, 161, 201, 241, 281, 321, 361])
    assert all(selected_ids == expected_selected_ids)


def test_nsle(mapdl, two_dimensional_mesh):
    mapdl.esel("S", "CENT", "X", 0, 0.1)
    selected_ids = mapdl.nsle("S")
    expected_selected_ids = np.array(
        [
            1,
            3,
            52,
            91,
            92,
            93,
            94,
            95,
            96,
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            109,
        ]
    )
    assert all(selected_ids == expected_selected_ids)


@pytest.mark.parametrize("initial_state", [None, True, False])
def test_ignore_cache_reset_context(mapdl, cleared, initial_state):
    mesh = mapdl.mesh
    previous_state = mesh._ignore_cache_reset
    mesh._ignore_cache_reset = initial_state

    with mesh.ignore_cache_reset:
        assert mesh._ignore_cache_reset is True

    assert mesh._ignore_cache_reset == initial_state
    mesh._ignore_cache_reset = previous_state
