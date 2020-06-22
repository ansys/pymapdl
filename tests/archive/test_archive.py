from sys import platform
import os

import pytest
import numpy as np
from vtk import (VTK_TETRA, VTK_QUADRATIC_TETRA, VTK_PYRAMID,
                 VTK_QUADRATIC_PYRAMID, VTK_WEDGE,
                 VTK_QUADRATIC_WEDGE, VTK_HEXAHEDRON,
                 VTK_QUADRATIC_HEXAHEDRON)
from pyvista import examples as pyvista_examples
import pyvista as pv

import pyansys
from pyansys import examples


IS_MAC = platform == 'darwin'

LINEAR_CELL_TYPES = [VTK_TETRA,
                     VTK_PYRAMID,
                     VTK_WEDGE,
                     VTK_HEXAHEDRON]

test_path = os.path.dirname(os.path.abspath(__file__))
testfiles_path = os.path.join(test_path, 'test_data')


@pytest.fixture(scope='module')
def hex_archive():
    return pyansys.Archive(examples.hexarchivefile)


@pytest.fixture(scope='module')
def all_solid_cells_archive():
    return pyansys.Archive(os.path.join(testfiles_path, 'all_solid_cells.cdb'))


@pytest.fixture(scope='module')
def all_solid_cells_archive_linear():
    return pyansys.Archive(os.path.join(testfiles_path, 'all_solid_cells.cdb'),
                           force_linear=True)


def test_read_mesh200():
    archive = pyansys.Archive(os.path.join(testfiles_path, 'mesh200.cdb'))
    assert archive.grid.n_cells == 1000


def test_archive_init(hex_archive):
    assert isinstance(hex_archive._raw, dict)
    assert isinstance(hex_archive.grid, pv.UnstructuredGrid)


def test_parse_vtk(hex_archive):
    grid = hex_archive.grid
    assert grid.points.size
    assert grid.cells.size
    assert 'ansys_node_num' in grid.point_arrays
    assert np.all(hex_archive.quality > 0)

    with pytest.raises(TypeError):
        hex_archive._parse_vtk(allowable_types=-1)

    with pytest.raises(TypeError):
        hex_archive._parse_vtk(allowable_types=3.0)


def test_invalid_archive(tmpdir, hex_archive):
    nblock_filename = str(tmpdir.mkdir("tmpdir").join('nblock.cdb'))
    pyansys.write_nblock(nblock_filename, hex_archive.nnum,
                         hex_archive.nodes)

    archive = pyansys.Archive(nblock_filename)
    with pytest.raises(AttributeError):
        archive.grid


def test_write_angle(tmpdir, hex_archive):
    nblock_filename = str(tmpdir.mkdir("tmpdir").join('nblock.cdb'))
    pyansys.write_nblock(nblock_filename, hex_archive.nnum,
                         hex_archive.nodes, hex_archive.node_angles)

    archive = pyansys.Archive(nblock_filename, parse_vtk=False)
    assert np.allclose(archive.nodes, hex_archive.nodes)


@pytest.mark.skipif(IS_MAC, reason="TODO: Unexplained behavior")
def test_missing_midside():
    allowable_types = [45, 95, 185, 186, 92, 187]
    archive_file = os.path.join(testfiles_path, 'mixed_missing_midside.cdb')
    archive = pyansys.Archive(archive_file, allowable_types=allowable_types)
    assert (archive.quality > 0.0).all()
    assert not np.any(archive.grid.celltypes == VTK_TETRA)


def test_writehex(tmpdir, hex_archive):
    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(temp_archive, hex_archive.grid)
    archive_new = pyansys.Archive(temp_archive)
    assert np.allclose(hex_archive.grid.points, archive_new.grid.points)
    assert np.allclose(hex_archive.grid.cells, archive_new.grid.cells)


def test_writesector(tmpdir):
    archive = pyansys.Archive(examples.sector_archive_file)

    filename = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(filename, archive.grid)
    archive_new = pyansys.Archive(filename)

    assert np.allclose(archive.grid.points, archive_new.grid.points)
    assert np.allclose(archive.grid.cells, archive_new.grid.cells)


def test_writehex_missing_elem_num(tmpdir, hex_archive):
    grid = hex_archive.grid
    grid.cell_arrays['ansys_elem_num'][:10] = -1
    grid.cell_arrays['ansys_etype'] = np.ones(grid.number_of_cells)*-1
    grid.cell_arrays['ansys_elem_type_num'] = np.ones(grid.number_of_cells)*-1

    filename = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(filename, grid)
    archive_new = pyansys.Archive(filename)

    assert np.allclose(hex_archive.grid.points, archive_new.grid.points)
    assert np.allclose(hex_archive.grid.cells, archive_new.grid.cells)


def test_writehex_missing_node_num(tmpdir, hex_archive):
    hex_archive.grid.point_arrays['ansys_node_num'][:-1] = -1

    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(temp_archive, hex_archive.grid)
    archive_new = pyansys.Archive(temp_archive)

    assert np.allclose(hex_archive.grid.points.shape, archive_new.grid.points.shape)
    assert np.allclose(hex_archive.grid.cells.size, archive_new.grid.cells.size)


def test_write_non_ansys_grid(tmpdir):
    grid = pv.UnstructuredGrid(pyvista_examples.hexbeamfile)
    del grid.point_arrays['sample_point_scalars']
    del grid.cell_arrays['sample_cell_scalars']
    archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(archive_file, grid)


def test_read_complex_archive(all_solid_cells_archive):
    grid = all_solid_cells_archive.grid
    assert grid.number_of_cells == 4
    assert np.unique(grid.celltypes).size == 4
    assert np.all(grid.celltypes > 20)
    assert np.all(all_solid_cells_archive.quality > 0.0)


def test_read_complex_archive_linear(all_solid_cells_archive_linear):
    grid = all_solid_cells_archive_linear.grid
    assert np.all(grid.celltypes < 20)
    assert np.all(all_solid_cells_archive_linear.quality > 0.0)


@pytest.mark.parametrize('celltype', [VTK_QUADRATIC_TETRA,
                                      VTK_QUADRATIC_PYRAMID,
                                      VTK_QUADRATIC_WEDGE,
                                      VTK_QUADRATIC_HEXAHEDRON])
def test_write_quad_complex_archive(tmpdir, celltype, all_solid_cells_archive):
    grid = all_solid_cells_archive.grid
    mask = grid.celltypes == celltype
    assert mask.any()
    grid = grid.extract_cells(mask)

    try:
        tmp_archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    except:
        tmp_archive_file = '/tmp/nblock.cdb'

    pyansys.save_as_archive(tmp_archive_file, grid)
    new_archive = pyansys.Archive(tmp_archive_file)
    assert np.allclose(grid.cells, new_archive.grid.cells)
    assert np.allclose(grid.points, new_archive.grid.points)
    assert (new_archive.quality > 0.0).all()


@pytest.mark.parametrize('celltype', LINEAR_CELL_TYPES)
def test_write_lin_archive(tmpdir, celltype, all_solid_cells_archive_linear):
    linear_grid = all_solid_cells_archive_linear.grid

    mask = linear_grid.celltypes == celltype
    assert mask.any()
    linear_grid = linear_grid.extract_cells(mask)

    tmp_archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))

    pyansys.save_as_archive(tmp_archive_file, linear_grid)
    new_archive = pyansys.Archive(tmp_archive_file)
    assert new_archive.quality > 0
    assert np.allclose(linear_grid.celltypes, new_archive.grid.celltypes)


def test_write_component(tmpdir):
    items = np.array([1, 20, 50, 51, 52, 53])
    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))

    comp_name = 'TEST'
    pyansys.write_cmblock(temp_archive, items, comp_name, 'node')
    archive = pyansys.Archive(temp_archive)
    assert np.allclose(archive.node_components[comp_name], items)


def test_read_parm():
    filename = os.path.join(testfiles_path, 'parm.cdb')
    archive = pyansys.Archive(filename)
    with pytest.raises(AttributeError):
        archive.parameters

    archive = pyansys.Archive(filename, read_parameters=True)
    assert len(archive.parameters) == 2
    for parm in archive.parameters:
        assert isinstance(archive.parameters[parm], np.ndarray)


def test_read_wb_nblock():
    expected = np.array([[9.89367578e-02, -8.07092192e-04,  8.53764953e+00],
                         [9.65803244e-02,  2.00906704e-02,  8.53744951e+00],
                         [9.19243555e-02,  3.98781615e-02,  8.53723652e+00]])
    filename = os.path.join(testfiles_path, 'workbench_193.cdb')
    archive = pyansys.Archive(filename)
    assert np.allclose(archive.nodes, expected)
    assert np.allclose(archive.node_angles, 0)


def test_read_hypermesh():
    expected = np.array([[-6.01203, 2.98129, 2.38556],
                         [-3.03231, 2.98067, 2.38309],
                         [-0.03485, 2.98004, 2.3805],
                         [2.98794, 2.97941, 2.37773],
                         [5.98956, 2.97878, 2.37488],
                         [5.98956, 5.97878, 2.37488]])

    filename = os.path.join(testfiles_path, 'U_SHAPE.cdb')
    archive = pyansys.Archive(filename, verbose=True)
    assert np.allclose(archive.nodes[:6], expected)
