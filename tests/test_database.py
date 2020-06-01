import pytest
import numpy as np
import pyansys

archive = pyansys.Archive(pyansys.examples.hexarchivefile)
d_v150 = pyansys.read_binary(pyansys.examples.hex_database_v150, debug=True)
d_v194 = pyansys.read_binary(pyansys.examples.hex_database_v194, debug=True)


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_nodes(database):
    assert np.allclose(database.nodes, archive.nodes[:, :3])


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_node_num(database):
    assert np.allclose(database.nnum, archive.nnum)


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_enum(database):
    assert np.allclose(database.enum, archive.enum)


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_elements(database):
    assert np.allclose(database.elem, archive.elem)


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_material(database):
    assert np.allclose(database.mtype, archive.material_type)


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_etype(database):
    assert np.allclose(database.etype, archive._raw['etype'])


@pytest.mark.parametrize('database', [d_v150, d_v194])
def test_parse_vtk(database):
    database.parse_vtk()

    assert np.allclose(database.grid.points, archive.grid.points)
    assert np.allclose(database.grid.cells, archive.grid.cells)

    assert len(database.grid.point_arrays) == len(archive.grid.point_arrays)
    for key in database.grid.point_arrays:
        np.allclose(database.grid.point_arrays[key],
                    archive.grid.point_arrays[key])

    assert len(database.grid.cell_arrays) == len(archive.grid.cell_arrays)
    for key in database.grid.cell_arrays:
        np.allclose(database.grid.cell_arrays[key],
                    archive.grid.cell_arrays[key])
