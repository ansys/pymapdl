"""Test MAPDL Console, CORBA, and gRPC interface"""
import glob
import os
import sys

import pytest
import numpy as np
import pyvista
from pyvista.plotting.renderer import CameraPosition
from pyvista.plotting import system_supports_plotting

from pyansys.errors import MapdlRuntimeError
import pyansys

if sys.platform != 'darwin':
    from pyansys.mapdl_corba import MapdlCorba

path = os.path.dirname(os.path.abspath(__file__))


def get_ansys_bin(rver):
    if os.name == 'nt':
        ans_root = 'c:/Program Files/ANSYS Inc/'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin', 'winx64',
                                'ANSYS%s.exe' % rver)
    else:
        ans_root = '/usr/ansys_inc'
        mapdlbin = os.path.join(ans_root, 'v%s' % rver, 'ansys', 'bin',
                                'ansys%s' % rver)

    return mapdlbin


if 'PYANSYS_IGNORE_ANSYS' in os.environ:
    HAS_ANSYS = False
else:
    HAS_ANSYS = os.path.isfile(get_ansys_bin('194'))



skip_no_ansys = pytest.mark.skipif(not HAS_ANSYS, reason="Requires ANSYS installed")
skip_no_xserver = pytest.mark.skipif(not system_supports_plotting(),
                                     reason="Requires active X Server")

@pytest.fixture(scope="module", params=['grpc', 'console', 'corba'])
def mapdl(request):
    os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu

    mode = request.param
    if mode == 'corba':
        # v200 and newer don't work
        # v194 has issues exiting
        rver = '182'
    else:
        rver = '202'

    # if mode == 'grpc':
    #     from pyansys.mapdl_grpc import MapdlGrpc
    #     mapdl = MapdlGrpc(cleanup_on_exit=False)
    # else:
    return pyansys.launch_mapdl(get_ansys_bin(rver), override=True, mode=mode)


@pytest.fixture(scope='function')
def cleared(mapdl):
    mapdl.finish()
    mapdl.clear('NOSTART')  # *MUST* be NOSTART.  With START fails after 20 calls...
    mapdl.prep7()
    yield


@skip_no_ansys
def test_str(mapdl):
    assert 'ANSYS Mechanical' in str(mapdl)


def test_chaining(mapdl, cleared):
    mapdl.prep7()
    n_kp = 1000
    with mapdl.chain_commands:
        for i in range(1, 1 + n_kp):
            mapdl.k(i, i, i, i)

    assert mapdl.geometry.n_keypoint == 1000


def test_read_para():
    para_path = os.path.join(path, 'testfiles', 'para')
    para_files = glob.glob(os.path.join(para_path, '*.txt'))
    from pyansys.mapdl_old import load_parameters
    for para_file in para_files:
        arr, parm = load_parameters(para_file)


###############################################################################
# Building elements
###############################################################################
@skip_no_ansys
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


@skip_no_ansys
def test_et(mapdl, cleared):
    n_plane183 = mapdl.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl.get_value("ETYP", item1="NUM", it1num="MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl.et(17, "PLANE183")
    assert n_plane183 == 17


###############################################################################
# Building geometry
###############################################################################
@skip_no_ansys
def test_k(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 == 2


@skip_no_ansys
def test_l(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 == 1


@skip_no_ansys
def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2)
    assert a0 == 1


@skip_no_ansys
def test_v(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    k3 = mapdl.k("", 0, 0, 1)
    v0 = mapdl.v(k0, k1, k2, k3)
    assert v0 == 1


@skip_no_ansys
def test_n(cleared, mapdl):
    n0 = mapdl.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl.n(2, 0, 0, 1)
    assert n1 == 2


@skip_no_ansys
def test_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 1, 0)
    l0 = mapdl.bsplin(k0, k1, k2)
    assert l0 == 1


@skip_no_ansys
def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 == 1


@skip_no_ansys
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


@skip_no_ansys
def test_invalid():
    with pytest.raises(Exception):
        mapdl.a(0, 0, 0, 0)


# @skip_no_ansys
# def test_aplot(cleared, mapdl):
#     k0 = mapdl.k("", 0, 0, 0)
#     k1 = mapdl.k("", 1, 0, 0)
#     k2 = mapdl.k("", 1, 1, 0)
#     k3 = mapdl.k("", 0, 1, 0)
#     l0 = mapdl.l(k0, k1)
#     l1 = mapdl.l(k1, k2)
#     l2 = mapdl.l(k2, k3)
#     l3 = mapdl.l(k3, k0)
#     a0 = mapdl.al(l0, l1, l2, l3)
#     mapdl._show_matplotlib_figures = False
#     response = mapdl.aplot()
#     assert 'WRITTEN TO FILE' in response


@skip_no_ansys
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


@skip_no_ansys
@skip_no_xserver
def test_kplot(cleared, mapdl):
    with pytest.raises(MapdlRuntimeError):
        mapdl.kplot(vtk=True)

    mapdl.k("", 0, 0, 0)
    mapdl.k("", 1, 0, 0)
    mapdl.k("", 1, 1, 0)
    mapdl.k("", 0, 1, 0)

    cpos = mapdl.kplot(vtk=True, off_screen=True)
    assert isinstance(cpos, CameraPosition)
    mapdl.kplot()    # make sure legacy still works



@skip_no_ansys
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


@skip_no_ansys
@skip_no_xserver
def test_lplot(cleared, mapdl):
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

    cpos = mapdl.lplot(vtk=True, show_keypoints=True, off_screen=True)
    assert isinstance(cpos, CameraPosition)
    mapdl.lplot()  # make sure legacy still works


@skip_no_ansys
def test_logging(mapdl, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join('tmp.inp'))
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


@skip_no_ansys
def test_nodes(tmpdir, cleared, mapdl):
    mapdl.n(1, 1, 1, 1)
    mapdl.n(11, 10, 1, 1)
    mapdl.fill(1, 11, 9)

    filename = str(tmpdir.mkdir("tmpdir").join('tmp.nodes'))
    mapdl.nwrite(filename)
    assert np.allclose(mapdl.mesh.nodes, np.loadtxt(filename)[:, 1:])

    # test clear mapdl
    mapdl.clear()
    assert not mapdl.mesh.nodes.size


@skip_no_ansys
def test_nnum(cleared, mapdl):
    mapdl.prep7()
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    assert np.allclose(mapdl.mesh.nnum, range(1, 12))

@pytest.mark.parametrize("knum", [True, False])
@skip_no_ansys
def test_nplot_vtk(cleared, mapdl, knum):
    mapdl.prep7()
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=True, knum=knum, background='w', color='k', off_screen=True)


@skip_no_ansys
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
    expected = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8],
                         [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 9, 10, 11, 12, 13, 14, 15, 16]])
    assert np.allclose(np.array(mapdl.mesh.elem), expected)


@pytest.mark.parametrize("arr", ([1, 2, 3],
                                 [[1, 2, 3], [1, 2, 3]],
                                 np.random.random((10)),
                                 np.random.random((10, 3)),
                                 np.random.random((10, 3, 3))))
@skip_no_ansys
def test_load_array(cleared, mapdl, arr):
    try:
        mapdl.load_array(arr, 'MYARR')
    except:  # flush for CORBA
        pass
    mapdl.load_array(arr, 'MYARR')
    parm, mapdl_arrays = mapdl.load_parameters()
    assert np.allclose(mapdl_arrays['MYARR'], arr)


@skip_no_ansys
def test_load_array_err(cleared, mapdl):
    with pytest.raises(TypeError):
        mapdl.load_array(['apple'], 'MYARR')

    with pytest.raises(ValueError):
        mapdl.load_array(np.empty((1, 1, 1, 1)), 'MYARR')


def test_get_array(cleared, mapdl):
    # start with an empty array
    array = mapdl.get_array('NODE', item1='NLIST')
    assert array.size == 0

    mapdl.cdread('db', pyansys.examples.hexarchivefile)
    array = mapdl.get_array('NODE', item1='NLIST')
    assert np.allclose(array, np.arange(1, 322))


# must be at end as this uses a scoped fixture
@skip_no_ansys
def test_exit(mapdl):
    mapdl.exit()
    with pytest.raises(RuntimeError):
        mapdl.prep7()

    assert not os.path.isfile(mapdl._lockfile)
