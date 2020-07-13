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
    nblock_expected = np.array([
        [3.7826539829200E+00, 1.2788958692644E+00, -1.0220880953640E+00],
        [3.7987359490873E+00, 1.2312085780780E+00, -1.0001885444969E+00],
        [3.8138798206653E+00, 1.1833200772896E+00, -9.7805743587145E-01],
        [3.7751258193793E+00, 1.2956563072306E+00, -9.9775569295981E-01],
        [3.7675976558386E+00, 1.3124167451968E+00, -9.7342329055565E-01],
        [3.8071756567432E+00, 1.2018089624856E+00, -9.5159140433025E-01],
        [3.8004714928212E+00, 1.2202978476816E+00, -9.2512537278904E-01],
        [3.7840345743299E+00, 1.2663572964392E+00, -9.4927433167235E-01],
        [3.8682501483615E+00, 1.4211343558710E+00, -9.2956245308371E-01],
        [3.8656154427804E+00, 1.4283573726940E+00, -9.3544082975315E-01],
        [3.8629807371994E+00, 1.4355803895169E+00, -9.4131920642259E-01],
        [3.8698134427618E+00, 1.4168612083433E+00, -9.3457292477788E-01],
        [3.8645201728196E+00, 1.4314324609914E+00, -9.4526873324423E-01],
        [3.8713767371621E+00, 1.4125880608155E+00, -9.3958339647206E-01],
        [3.8687181728010E+00, 1.4199362966407E+00, -9.4440082826897E-01],
        [3.8660596084399E+00, 1.4272845324660E+00, -9.4921826006588E-01],
        [3.7847463501820E+00, 1.2869612289286E+00, -1.0110875234148E+00],
        [3.7882161293470E+00, 1.2952473975570E+00, -1.0006326084202E+00],
        [3.7840036708439E+00, 1.3089808408341E+00, -9.8189659453120E-01],
        [3.7736944340897E+00, 1.3175655146540E+00, -9.6829193559890E-01],
        [3.7797912123408E+00, 1.3227142841112E+00, -9.6316058064216E-01],
        [3.8163322819008E+00, 1.1913589544053E+00, -9.6740419078720E-01],
        [3.8046827481496E+00, 1.2474593204382E+00, -9.7922600135387E-01],
        [3.8202228218151E+00, 1.1995824283636E+00, -9.5733187068101E-01],
        [3.9797161316330E+00, 2.5147820926190E-01, -5.1500799817626E-01],
        [3.9831382922541E+00, 2.0190980565891E-01, -5.0185526897444E-01],
        [3.9810868976408E+00, 2.3910377061737E-01, -5.4962360790281E-01],
        [3.9772930845240E+00, 2.8865001362748E-01, -5.6276585706615E-01],
        [3.9816265976187E+00, 2.1428739259987E-01, -4.6723916677654E-01],
        [3.9839413943097E+00, 1.8949722823843E-01, -5.3648152416530E-01],
        [3.7962006776348E+00, 1.2764624207283E+00, -9.3931008487698E-01],
        [3.8126101429289E+00, 1.2302105573453E+00, -9.1545958911180E-01],
        [3.8065408178751E+00, 1.2252542025135E+00, -9.2029248095042E-01],
        [3.8164164823720E+00, 1.2148964928545E+00, -9.3639572989640E-01],
        [3.8972892823450E+00, 2.7547119775919E-01, -5.6510422311694E-01],
        [3.9015993648189E+00, 2.0235606714652E-01, -4.6987255385930E-01],
        [3.9023812010290E+00, 1.7705558022279E-01, -5.3881795411458E-01],
        [3.9019902829240E+00, 1.8970582368465E-01, -5.0434525398694E-01],
        [3.8998352416870E+00, 2.2626338899099E-01, -5.5196108861576E-01],
        [3.8994443235820E+00, 2.3891363245285E-01, -5.1748838848812E-01],
        [3.9372911834345E+00, 2.8206060569333E-01, -5.6393504009155E-01],
        [3.9416129812188E+00, 2.0832172987319E-01, -4.6855586031792E-01],
        [3.9431612976694E+00, 1.8327640423061E-01, -5.3764973913994E-01],
        [3.8619577233846E+00, 1.4192189812407E+00, -9.2587403626770E-01],
        [3.8507167163959E+00, 1.4238788373222E+00, -9.3661710728291E-01],
        [3.8651039358730E+00, 1.4201766685559E+00, -9.2771824467570E-01],
        [3.8624692302920E+00, 1.4273996853788E+00, -9.3359662134515E-01],
        [3.8610467267790E+00, 1.4182334490688E+00, -9.3810025187748E-01],
        [3.8563372198902E+00, 1.4215489092814E+00, -9.3124557177530E-01],
        [3.8568487267976E+00, 1.4297296134196E+00, -9.3896815685275E-01],
        [3.8583881624179E+00, 1.4255816848941E+00, -9.4291768367439E-01],
        [3.8594834323787E+00, 1.4225065965966E+00, -9.3308978018331E-01]])

    assert np.allclose(nblock_expected, all_solid_cells_archive.nodes)

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

    filename = os.path.join(testfiles_path, 'hypermesh.cdb')
    archive = pyansys.Archive(filename, verbose=True)
    assert np.allclose(archive.nodes[:6], expected)
