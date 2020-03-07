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

QUADRATIC_CELL_TYPES = [VTK_QUADRATIC_TETRA,
                        VTK_QUADRATIC_PYRAMID,
                        VTK_QUADRATIC_WEDGE,
                        VTK_QUADRATIC_HEXAHEDRON]

try:
    test_path = os.path.dirname(os.path.abspath(__file__))
    testfiles_path = os.path.join(test_path, 'test_data')
except:
    testfiles_path = '/home/alex/afrl/python/source/pyansys/tests/archive/test_data'


def test_init_archive():
    archive = pyansys.Archive(examples.hexarchivefile)
    assert isinstance(archive.raw, dict)


def test_parse_vtk():
    archive = pyansys.Archive(examples.hexarchivefile)
    grid = archive.parse_vtk()
    assert grid.points.size
    assert grid.cells.size
    assert 'ansys_node_num' in grid.point_arrays
    assert np.all(grid.quality > 0)

    with pytest.raises(Exception):
        archive.parse_vtk(allowable_types=186)

    with pytest.raises(Exception):
        archive.parse_vtk(allowable_types=[1, 2, 3])


def test_invalid_archive(tmpdir):
    archive = pyansys.Archive(examples.hexarchivefile)
    # grid = archive.parse_vtk()

    try:
        nblock_filename = str(tmpdir.mkdir("tmpdir").join('nblock.cdb'))
    except:
        nblock_filename = '/tmp/nblock.cdb'
    pyansys.write_nblock(nblock_filename, archive.raw['nnum'],
                         archive.raw['nodes'][:, :3])
    archive = pyansys.Archive(nblock_filename)

    with pytest.raises(Exception):
        archive.parse_vtk()


def test_write_angle(tmpdir):
    archive = pyansys.Archive(examples.hexarchivefile)

    try:
        nblock_filename = str(tmpdir.mkdir("tmpdir").join('nblock.cdb'))
    except:
        nblock_filename = '/tmp/nblock.cdb'

    angles = archive.raw['nodes'][:, 3:]
    pyansys.write_nblock(nblock_filename, archive.raw['nnum'],
                         archive.raw['nodes'][:, :3], angles)

    archive2 = pyansys.Archive(nblock_filename)
    assert np.allclose(archive2.raw['nodes'], archive.raw['nodes'])

@pytest.mark.skipif(IS_MAC, reason="TODO: Unexplained behavior")
def test_missing_midside():
    archive_file = os.path.join(testfiles_path, 'mixed_missing_midside.cdb')
    archive = pyansys.Archive(archive_file)
    grid = archive.parse_vtk(allowable_types=['45', '95', '185', '186', '92', '187'])
    assert (grid.quality > 0.0).all()
    assert not np.any(grid.celltypes == VTK_TETRA)


def test_writehex(tmpdir):
    archive = pyansys.Archive(examples.hexarchivefile)
    grid = archive.parse_vtk()

    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(temp_archive, grid)

    archive2 = pyansys.Archive(temp_archive)
    grid2 = archive2.parse_vtk()

    assert np.allclose(grid.points, grid2.points)
    assert np.allclose(grid.cells, grid2.cells)


def test_writesector(tmpdir):
    archive = pyansys.Archive(examples.sector_archive_file)
    grid = archive.parse_vtk()

    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(temp_archive, grid)

    archive2 = pyansys.Archive(temp_archive)
    grid2 = archive2.parse_vtk()

    assert np.allclose(grid.points, grid2.points)
    assert np.allclose(grid.cells, grid2.cells)


def test_writehex_missing_elem_num(tmpdir):
    archive = pyansys.Archive(examples.hexarchivefile)
    grid = archive.parse_vtk()
    grid.cell_arrays['ansys_elem_num'][:10] = -1
    grid.cell_arrays['ansys_etype'] = np.ones(grid.number_of_cells)*-1
    grid.cell_arrays['ansys_elem_type_num'] = np.ones(grid.number_of_cells)*-1

    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(temp_archive, grid)

    archive2 = pyansys.Archive(temp_archive)
    grid2 = archive2.parse_vtk()

    assert np.allclose(grid.points.shape, grid2.points.shape)
    assert np.allclose(grid.cells.size, grid2.cells.size)


def test_writehex_missing_node_num(tmpdir):
    archive = pyansys.Archive(examples.hexarchivefile)
    grid = archive.parse_vtk()
    grid.point_arrays['ansys_node_num'][:-1] = -1

    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    pyansys.save_as_archive(temp_archive, grid)

    archive2 = pyansys.Archive(temp_archive)
    grid2 = archive2.parse_vtk()

    assert np.allclose(grid.points.shape, grid2.points.shape)
    assert np.allclose(grid.cells.size, grid2.cells.size)


def test_write_non_ansys_grid(tmpdir):
    grid = pv.UnstructuredGrid(pyvista_examples.hexbeamfile)
    del grid.point_arrays['sample_point_scalars']
    del grid.cell_arrays['sample_cell_scalars']

    try:
        archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    except:
        archive_file = '/tmp/nblock.cdb'

    pyansys.save_as_archive(archive_file, grid)


def test_read_complex_archive():
    archive_file = os.path.join(testfiles_path, 'all_solid_cells.cdb')
    archive = pyansys.Archive(archive_file)
    grid = archive.parse_vtk()
    assert grid.number_of_cells == 4
    assert np.unique(grid.celltypes).size == 4
    assert np.all(grid.celltypes > 20)
    assert np.all(grid.quality > 0.0)

    linear_grid = archive.parse_vtk(force_linear=True)
    assert np.all(linear_grid.celltypes < 20)
    assert np.all(linear_grid.quality > 0.0)


@pytest.mark.parametrize('celltype', QUADRATIC_CELL_TYPES)
def test_write_quad_complex_archive(tmpdir, celltype):
    # celltype = 24
    archive_file = os.path.join(testfiles_path, 'all_solid_cells.cdb')
    archive = pyansys.Archive(archive_file)
    grid = archive.parse_vtk()

    mask = grid.celltypes == celltype
    assert mask.any()
    grid = grid.extract_cells(mask)

    try:
        tmp_archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    except:
        tmp_archive_file = '/tmp/nblock.cdb'

    pyansys.save_as_archive(tmp_archive_file, grid)
    new_archive = pyansys.Archive(tmp_archive_file)
    new_grid = new_archive.parse_vtk()
    assert np.allclose(grid.cells, new_grid.cells)
    assert np.allclose(grid.points, new_grid.points)
    assert (new_grid.quality > 0.0).all()


@pytest.mark.parametrize('celltype', LINEAR_CELL_TYPES)
def test_write_lin_archive(tmpdir, celltype):
    archive_file = os.path.join(testfiles_path, 'all_solid_cells.cdb')
    archive = pyansys.Archive(archive_file)
    linear_grid = archive.parse_vtk(force_linear=True)

    mask = linear_grid.celltypes == celltype
    assert mask.any()
    linear_grid = linear_grid.extract_cells(mask)

    try:
        tmp_archive_file = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))
    except:
        tmp_archive_file = '/tmp/nblock.cdb'

    pyansys.save_as_archive(tmp_archive_file, linear_grid)
    new_archive = pyansys.Archive(tmp_archive_file)
    new_linear_grid = new_archive.parse_vtk()
    assert np.allclose(linear_grid.cells, new_linear_grid.cells)
    assert np.allclose(linear_grid.points, new_linear_grid.points)


def test_write_component(tmpdir):
    items = np.array([1, 20, 50, 51, 52, 53])
    temp_archive = str(tmpdir.mkdir("tmpdir").join('tmp.cdb'))

    comp_name = 'TEST'
    pyansys.write_cmblock(temp_archive, items, comp_name, 'node')
    archive = pyansys.Archive(temp_archive)
    assert np.allclose(archive.raw['node_comps'][comp_name], items)


def test_read_mesh200():
    archive = pyansys.Archive(os.path.join(testfiles_path, 'mesh200.cdb'))
    grid = archive.parse_vtk()
    assert grid.n_cells == 1000


def test_read_parm():
    filename = os.path.join(testfiles_path, 'parm.cdb')
    archive = pyansys.Archive(filename)
    assert len(archive.raw['parameters']) == 0

    archive = pyansys.Archive(filename, read_parameters=True)
    assert len(archive.raw['parameters']) == 2
    for parm in archive.raw['parameters']:
        assert isinstance(archive.raw['parameters'][parm], np.ndarray)


def test_read_wb_nblock():
    expected = np.array([[9.89367578e-02, -8.07092192e-04,  8.53764953e+00,
                          0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
                         [9.65803244e-02,  2.00906704e-02,  8.53744951e+00,
                          0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
                         [9.19243555e-02,  3.98781615e-02,  8.53723652e+00,
                          0.00000000e+00,  0.00000000e+00,  0.00000000e+00]])
    filename = os.path.join(testfiles_path, 'workbench_193.cdb')
    archive = pyansys.Archive(filename)
    assert np.allclose(archive.raw['nodes'], expected)


if __name__ == '__main__':
    test_init_archive()
