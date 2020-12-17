"""Test MAPDL Console and CORBA interfaces"""
import os
import time

import pytest
import numpy as np
import pyvista
from pyvista.plotting.renderer import CameraPosition
from pyvista.plotting import system_supports_plotting

from pyansys.misc import get_ansys_bin
from pyansys.errors import MapdlRuntimeError
import pyansys

# check for a valid MAPDL install with CORBA
valid_rver = ['182', '190', '191', '192', '193', '194', '195', '201']
EXEC_FILE = None
for rver in valid_rver:
    if os.path.isfile(get_ansys_bin(rver)):
        EXEC_FILE = get_ansys_bin(rver)

if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = EXEC_FILE is not None

if not HAS_ANSYS:
    pytestmark = pytest.mark.skip("Requires ANSYS installed")

skip_no_xserver = pytest.mark.skipif(not system_supports_plotting(),
                                     reason="Requires active X Server")


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear('NOSTART')  # *MUST* be NOSTART.  With START fails after 20 calls...
    mapdl.prep7()
    yield


@pytest.fixture(scope='function')
def make_block(mapdl, cleared):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.25)
    mapdl.vmesh('ALL')


def test_empty(mapdl):
    with pytest.raises(ValueError):
        mapdl.run('')


def test_str(mapdl):
    assert 'ANSYS Mechanical' in str(mapdl)


def test_version(mapdl):
    assert isinstance(mapdl.version, float)


def test_comment(cleared, mapdl):
    comment = 'Testing...'
    resp = mapdl.com(comment)
    assert comment in resp


def test_output(cleared, mapdl):
    tmp_file = 'tmp_redirect.txt'
    resp = mapdl.output(tmp_file)
    comment = 'Testing...'
    resp = mapdl.com(comment)
    mapdl.output()
    output = open(os.path.join(mapdl.directory, tmp_file)).read()
    assert comment in output


def test_basic_command(cleared, mapdl):
    resp = mapdl.block(0, 1, 0, 1, 0, 1)
    assert 'CREATE A HEXAHEDRAL VOLUME' in resp


def test_allow_ignore(mapdl):
    mapdl.clear()
    mapdl.allow_ignore = False  # reset on __init__
    assert mapdl.allow_ignore is False
    with pytest.raises(pyansys.errors.MapdlInvalidRoutineError):
        mapdl.k()

    # Does not create keypoints and yet does not raise error
    mapdl.allow_ignore = True
    assert mapdl.allow_ignore is True
    mapdl.k()
    assert mapdl.geometry.n_keypoint is 0


def test_chaining(mapdl, cleared):
    mapdl.prep7()
    n_kp = 1000
    with mapdl.chain_commands:
        for i in range(1, 1 + n_kp):
            mapdl.k(i, i, i, i)

    assert mapdl.geometry.n_keypoint == 1000


def test_e(mapdl, cleared):
    mapdl.et("", 183)
    n0 = mapdl.n("", 0, 0, 0)
    n1 = mapdl.n("", 1, 0, 0)
    n2 = mapdl.n("", 1, 1, 0)
    n3 = mapdl.n("", 0, 1, 1)
    n4 = mapdl.n("", 0, 1, -1)
    e0 = mapdl.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl.e(n0, n1, n2, n4)
    assert e1 == 2


def test_et(mapdl, cleared):
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_value("ETYP", item1="NUM", it1num="MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17


def test_k(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 == 2


def test_l(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 == 1


def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2)
    assert a0 == 1


def test_v(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    k3 = mapdl.k("", 0, 0, 1)
    v0 = mapdl.v(k0, k1, k2, k3)
    assert v0 == 1


def test_n(cleared, mapdl):
    n0 = mapdl.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl.n(2, 0, 0, 1)
    assert n1 == 2


def test_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 1, 0)
    l0 = mapdl.bsplin(k0, k1, k2)
    assert l0 == 1


def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 == 1


def test_al(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    a0 = mapdl.al(l0, l1, l2, l3)
    assert a0 == 1


def test_invalid_area():
    with pytest.raises(Exception):
        mapdl.a(0, 0, 0, 0)


@skip_no_xserver
def test_aplot(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    mapdl.al(l0, l1, l2, l3)
    mapdl.aplot(show_area_numbering=True)
    mapdl.aplot(color_areas=True, show_lines=True,
                show_line_numbering=True)

    mapdl.aplot(quality=100)
    mapdl.aplot(quality=-1)

    # and legacy as well
    mapdl.aplot(vtk=False)


@skip_no_xserver
@pytest.mark.parametrize('vtk', [True, False])
def test_vplot(cleared, mapdl, vtk):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.vplot(vtk=vtk, color_areas=True)


def test_keypoints(cleared, mapdl):
    assert mapdl.geometry.n_keypoint == 0
    kps = [[0, 0, 0],
           [1, 0, 0],
           [1, 1, 0],
           [0, 1, 0]]

    i = 1
    knum = []
    for x, y, z in kps:
        mapdl.k(i, x, y, z)
        knum.append(i)
        i += 1

    assert mapdl.geometry.n_keypoint == 4
    assert np.allclose(kps, mapdl.geometry.keypoints)
    assert np.allclose(knum, mapdl.geometry.knum)


@skip_no_xserver
def test_kplot(cleared, mapdl, tmpdir):
    with pytest.raises(MapdlRuntimeError):
        mapdl.kplot(vtk=True)

    mapdl.k("", 0, 0, 0)
    mapdl.k("", 1, 0, 0)
    mapdl.k("", 1, 1, 0)
    mapdl.k("", 0, 1, 0)

    filename = str(tmpdir.mkdir("tmpdir").join('tmp.png'))
    cpos = mapdl.kplot(screenshot=filename)
    assert isinstance(cpos, CameraPosition)
    assert os.path.isfile(filename)

    mapdl.kplot(knum=True, vtk=False)    # make sure legacy still works


def test_lines(cleared, mapdl):
    assert mapdl.geometry.n_line == 0

    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)

    lines = mapdl.geometry.lines
    assert isinstance(lines, pyvista.PolyData)
    assert np.allclose(mapdl.geometry.lnum, [l0, l1, l2, l3])
    assert mapdl.geometry.n_line == 4


@skip_no_xserver
def test_lplot(cleared, mapdl, tmpdir):
    with pytest.raises(MapdlRuntimeError):
        mapdl.lplot(vtk=True)

    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    mapdl.l(k0, k1)
    mapdl.l(k1, k2)
    mapdl.l(k2, k3)
    mapdl.l(k3, k0)

    filename = str(tmpdir.mkdir("tmpdir").join('tmp.png'))
    cpos = mapdl.lplot(show_keypoint_numbering=True, screenshot=filename)
    assert isinstance(cpos, CameraPosition)
    assert os.path.isfile(filename)

    mapdl.lplot(vtk=False)  # make sure legacy still works


def test_logging(mapdl, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.inp'))
    mapdl.open_apdl_log(filename, mode='w')
    mapdl._close_apdl_log()

    # test append mode
    mapdl.open_apdl_log(filename, mode='a')

    # don't allow to double log
    with pytest.raises(RuntimeError):
        mapdl.open_apdl_log(filename, mode='w')

    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl._apdl_log.flush()

    out = open(mapdl._apdl_log.name).read().strip().split()[-5:]
    assert 'PREP7' in out[0]
    assert 'K,4,0,1,0' in out[-1]
    mapdl._close_apdl_log()


def test_nodes(tmpdir, cleared, mapdl):
    mapdl.n(1, 1, 1, 1)
    mapdl.n(11, 10, 1, 1)
    mapdl.fill(1, 11, 9)

    filename = str(tmpdir.mkdir("tmpdir").join('tmp.nodes'))
    mapdl.nwrite(filename)
    assert np.allclose(mapdl.mesh.nodes, np.loadtxt(filename)[:, 1:])
    assert mapdl.mesh.n_node == 11
    assert np.allclose(mapdl.mesh.nnum, range(1, 12))

    # test clear mapdl
    mapdl.clear()
    assert not mapdl.mesh.nodes.size
    assert not mapdl.mesh.n_node
    assert not mapdl.mesh.nnum.size



@pytest.mark.parametrize('knum', [True, False])
@skip_no_xserver
def test_nplot_vtk(cleared, mapdl, knum):
    with pytest.raises(RuntimeError):
        mapdl.nplot()

    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=True, knum=knum, background='w', color='k')


@skip_no_xserver
def test_nplot(cleared, mapdl):
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=False, background='w', color='k')


def test_elements(cleared, mapdl):
    mapdl.et(1, 185)

    # two basic cells
    cell1 = [[0, 0, 0],
             [1, 0, 0],
             [1, 1, 0],
             [0, 1, 0],
             [0, 0, 1],
             [1, 0, 1],
             [1, 1, 1],
             [0, 1, 1]]

    cell2 = [[0, 0, 2],
             [1, 0, 2],
             [1, 1, 2],
             [0, 1, 2],
             [0, 0, 3],
             [1, 0, 3],
             [1, 1, 3],
             [0, 1, 3]]

    with mapdl.chain_commands:
        for cell in [cell1, cell2]:
            for x, y, z in cell:
                mapdl.n(x=x, y=y, z=z)

    mapdl.e(*list(range(1, 9)))
    mapdl.e(*list(range(9, 17)))
    expected = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
                         [1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 9, 10, 11, 12, 13, 14, 15, 16]])

    assert np.allclose(np.array(mapdl.mesh.elem), expected)


@pytest.mark.parametrize("parm", ('my_string',
                                  1,
                                  10.0,
                                  [1, 2, 3],
                                  [[1, 2, 3], [1, 2, 3]],
                                  np.random.random((10000)),
                                  np.random.random((10, 3)),
                                  np.random.random((10, 3, 3))))
def test_set_get_parameters(mapdl, parm):
    parm_name = pyansys.misc.random_string(20)
    mapdl.parameters[parm_name] = parm
    if isinstance(parm, str):
        assert mapdl.parameters[parm_name] == parm
    else:
        arr = mapdl.parameters[parm_name]
        try:
            assert np.allclose(arr, parm)
        except:  # MAPDL internal bug
            assert np.allclose(arr, 0)

def test_set_parameters_arr_to_scalar(mapdl, cleared):
    mapdl.parameters['PARM'] = np.arange(10)
    mapdl.parameters['PARM'] = 2


def test_set_parameters_string_spaces(mapdl):
    with pytest.raises(ValueError):
        mapdl.parameters['PARM'] = "string with spaces"


def test_builtin_parameters(mapdl, cleared):
    mapdl.prep7()
    assert mapdl.parameters.routine == "PREP7"

    mapdl.units("SI")
    assert mapdl.parameters.units == "SI"

    assert isinstance(mapdl.parameters.revision, float)

    if os.name == 'posix':
        assert 'LIN' in mapdl.parameters.platform

    mapdl.csys(1)
    assert mapdl.parameters.csys == 1

    mapdl.dsys(1)
    assert mapdl.parameters.dsys == 1

    mapdl.esys(0)
    assert mapdl.parameters.esys == 0
    assert mapdl.parameters.material == 1
    assert mapdl.parameters.section == 1
    assert mapdl.parameters.real == 1


def test_eplot_fail(mapdl):
    # must fail with empty mesh
    with pytest.raises(RuntimeError):
        mapdl.eplot()


@skip_no_xserver
def test_eplot(mapdl, make_block):
    init_elem = mapdl.mesh.n_elem
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    mapdl.eplot(show_node_numbering=True, background='w', color='b')
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    assert mapdl.mesh.n_elem == init_elem


@skip_no_xserver
def test_eplot_screenshot(mapdl, make_block, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.png'))
    mapdl.eplot(background='w', show_edges=True, smooth_shading=True,
                window_size=[1920, 1080], screenshot=filename)
    assert os.path.isfile(filename)


def test_cyclic_solve(mapdl, cleared):
    # build the cyclic model
    mapdl.prep7()
    mapdl.shpp('off')
    mapdl.cdread('db', pyansys.examples.sector_archive_file)
    mapdl.prep7()
    time.sleep(1.0)
    mapdl.cyclic()

    # set material properties
    mapdl.mp('NUXY', 1, 0.31)
    mapdl.mp('DENS', 1, 4.1408E-04)
    mapdl.mp('EX', 1, 16900000)
    mapdl.emodif('ALL', 'MAT', 1)

    # setup and solve
    mapdl.modal_analysis('LANB', 1, 1, 100000, elcalc=True)
    mapdl.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    assert mapdl.result.nsets == 16  # multiple result files...


def test_load_table(mapdl):
    my_conv = np.array([[0, 0.001],
                        [120, 0.001],
                        [130, 0.005],
                        [700, 0.005],
                        [710, 0.002],
                        [1000, 0.002]])
    mapdl.load_table('my_conv', my_conv, 'TIME')
    assert np.allclose(mapdl.parameters['my_conv'], my_conv[:, -1])
