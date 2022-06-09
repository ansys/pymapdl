"""Test mesh """
import numpy as np


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
