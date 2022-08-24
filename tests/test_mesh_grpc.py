"""Test mesh """
import os

import numpy as np
import pytest


def test_empty_model(mapdl):
    mapdl.clear()

    assert mapdl.mesh.nnum.size == 0
    assert mapdl.mesh.enum.size == 0

    assert mapdl.mesh.n_elem == 0
    assert mapdl.mesh.n_node == 0


def test_mesh_attributes(mapdl, cube_solve):
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


def test_elem_num_in_mesh_elem(mapdl, cube_solve):
    enums = np.array([each[8] for each in mapdl.mesh.elem])
    assert np.allclose(mapdl.mesh.enum, enums)


def test_repr(mapdl, cube_solve):
    out = str(mapdl.mesh)

    assert isinstance(out, str)
    assert "Number of Element Types" in out


def test_mapdl(mapdl):
    from ansys.mapdl.core.mapdl import _MapdlCore

    assert isinstance(mapdl.mesh._mapdl, _MapdlCore)


def test_local(mapdl):
    assert isinstance(mapdl.mesh.local, bool)
    assert mapdl._local == mapdl.mesh.local


def test_empty_mesh(mapdl, cleared):
    assert mapdl.mesh.n_node == 0
    assert mapdl.mesh.n_elem == 0
    assert mapdl.mesh.nodes.size == 0


def test_non_empty_mesh(mapdl, cube_solve):
    assert mapdl.mesh.n_node > 0
    assert mapdl.mesh.n_elem > 0

    assert mapdl.mesh.nodes is not None
    assert isinstance(mapdl.mesh.nodes, np.ndarray)


def test_tshape_key(mapdl, contact_solve):
    tshape = mapdl.mesh.tshape_key
    assert isinstance(tshape, dict)
    assert len(tshape.keys()) > 0

    tshape = mapdl.mesh.tshape
    assert isinstance(tshape, np.ndarray)
    assert tshape.size > 0


def test_save(mapdl, cube_solve):
    # This test seems to fail when paralelized.
    fname = "mesh.vtk"
    for binary_ in [True, False]:
        mapdl.mesh.save(fname, binary_)
        assert os.path.exists(fname)

        os.remove(fname)


def test_key_option(mapdl, contact_solve):
    assert mapdl.mesh.key_option is not None
    assert isinstance(mapdl.mesh.key_option, dict)
    assert len(mapdl.mesh.key_option.keys()) > 0


def test_section(mapdl, cube_solve):
    assert mapdl.mesh.section is not None
    assert isinstance(mapdl.mesh.section, np.ndarray)
    assert mapdl.mesh.section.size > 0


def test_element_coord_system(mapdl, cube_solve):
    assert mapdl.mesh.element_coord_system is not None
    assert isinstance(mapdl.mesh.element_coord_system, np.ndarray)
    assert mapdl.mesh.element_coord_system.size > 0


def test_enum(mapdl, cube_solve):
    assert mapdl.mesh.enum is not None
    assert isinstance(mapdl.mesh.enum, np.ndarray)
    assert mapdl.mesh.enum.size > 0
    assert np.allclose(mapdl.mesh.enum, [1, 2, 3, 4, 5, 6, 7, 8])


def test_nnum(mapdl, cube_solve):
    assert mapdl.mesh.nnum is not None
    assert isinstance(mapdl.mesh.nnum, np.ndarray)
    assert mapdl.mesh.nnum.size == 81


def test_ekey(mapdl, cube_solve):
    assert mapdl.mesh.ekey is not None
    assert isinstance(mapdl.mesh.ekey, np.ndarray)
    assert mapdl.mesh.ekey.size > 0
    assert np.allclose(mapdl.mesh.ekey, [[1, 186]])


def test_nodes(mapdl, cube_solve):
    assert mapdl.mesh.nodes is not None
    assert isinstance(mapdl.mesh.nodes, np.ndarray)
    assert mapdl.mesh.nodes.shape == (81, 3)


def test_node_angles(mapdl, cube_solve):
    with pytest.raises(NotImplementedError):
        mapdl.mesh.node_angles
