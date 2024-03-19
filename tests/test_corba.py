"""Test legacy MAPDL CORBA interface.

This has been copied from test_mapdl.py

"""
import os
import time

from ansys.mapdl.reader import examples
import numpy as np
import pytest
import pyvista

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import MapdlRuntimeError
from conftest import skip_no_xserver

# skip entire module unless --corba is enabled
pytestmark = pytest.mark.corba


@pytest.fixture(scope="function")
def cleared(mapdl_corba):
    mapdl_corba.finish()
    # *MUST* be NOSTART.  With START fails after 20 calls...
    mapdl_corba.clear("NOSTART")
    mapdl_corba.prep7()
    yield


@pytest.fixture(scope="function")
def make_block(mapdl_corba, cleared):
    mapdl_corba.block(0, 1, 0, 1, 0, 1)
    mapdl_corba.et(1, 186)
    mapdl_corba.esize(0.25)
    mapdl_corba.vmesh("ALL")


def test_jobname(mapdl_corba, cleared):
    jobname = "abcdefg"
    assert mapdl_corba.jobname != jobname
    mapdl_corba.finish()
    mapdl_corba.filname(jobname)
    assert mapdl_corba.jobname == jobname

    other_jobname = "gfedcba"
    mapdl_corba.jobname = other_jobname
    assert mapdl_corba.jobname == other_jobname


def test_empty(mapdl_corba):
    with pytest.raises(ValueError):
        mapdl_corba.run("")


def test_str(mapdl_corba):
    assert "ANSYS Mechanical" in str(mapdl_corba)


def test_version(mapdl_corba):
    assert isinstance(mapdl_corba.version, float)


def test_comment(cleared, mapdl_corba):
    comment = "Testing..."
    resp = mapdl_corba.com(comment)
    assert comment in resp


def test_basic_command(cleared, mapdl_corba):
    resp = mapdl_corba.finish()
    assert "ROUTINE COMPLETED" in resp


def test_allow_ignore(mapdl_corba):
    mapdl_corba.clear()
    mapdl_corba.allow_ignore = False
    assert mapdl_corba.allow_ignore is False
    with pytest.raises(pymapdl.errors.MapdlInvalidRoutineError):
        mapdl_corba.k()

    # Does not create keypoints and yet does not raise error
    mapdl_corba.allow_ignore = True
    assert mapdl_corba.allow_ignore is True
    mapdl_corba.k()
    assert mapdl_corba.geometry.n_keypoint == 0


def test_e(mapdl_corba, cleared):
    mapdl_corba.et("", 183)
    n0 = mapdl_corba.n("", 0, 0, 0)
    n1 = mapdl_corba.n("", 1, 0, 0)
    n2 = mapdl_corba.n("", 1, 1, 0)
    n3 = mapdl_corba.n("", 0, 1, 1)
    n4 = mapdl_corba.n("", 0, 1, -1)
    e0 = mapdl_corba.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl_corba.e(n0, n1, n2, n4)
    assert e1 == 2


def test_et(mapdl_corba, cleared):
    n_plane183 = mapdl_corba.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl_corba.get_value("ETYP", item1="NUM", it1num="MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl_corba.et(17, "PLANE183")
    assert n_plane183 == 17


def test_k(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl_corba.k(2, 0, 0, 1)
    assert k1 == 2


def test_l(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    l0 = mapdl_corba.l(k0, k1)
    assert l0 == 1


def test_a(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 0, 1, 0)
    a0 = mapdl_corba.a(k0, k1, k2)
    assert a0 == 1


def test_v(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 0, 1, 0)
    k3 = mapdl_corba.k("", 0, 0, 1)
    v0 = mapdl_corba.v(k0, k1, k2, k3)
    assert v0 == 1


def test_n(cleared, mapdl_corba):
    n0 = mapdl_corba.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl_corba.n(2, 0, 0, 1)
    assert n1 == 2


def test_bsplin(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 2, 1, 0)
    l0 = mapdl_corba.bsplin(k0, k1, k2)
    assert l0 == 1


def test_a(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 1, 1, 0)
    k3 = mapdl_corba.k("", 0, 1, 0)
    a0 = mapdl_corba.a(k0, k1, k2, k3)
    assert a0 == 1


def test_al(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 1, 1, 0)
    k3 = mapdl_corba.k("", 0, 1, 0)
    l0 = mapdl_corba.l(k0, k1)
    l1 = mapdl_corba.l(k1, k2)
    l2 = mapdl_corba.l(k2, k3)
    l3 = mapdl_corba.l(k3, k0)
    a0 = mapdl_corba.al(l0, l1, l2, l3)
    assert a0 == 1


def test_invalid_area(mapdl_corba):
    with pytest.raises(MapdlRuntimeError):
        mapdl_corba.a(0, 0, 0, 0)


# def test_invalid_input(mapdl_corba):
# with pytest.raises(FileNotFoundError):
# mapdl_corba.input('thisisnotafile')


@skip_no_xserver
def test_kplot(cleared, mapdl_corba, tmpdir):
    mapdl_corba.k("", 0, 0, 0)
    mapdl_corba.k("", 1, 0, 0)
    mapdl_corba.k("", 1, 1, 0)
    mapdl_corba.k("", 0, 1, 0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl_corba.kplot(savefig=filename)
    assert cpos is None
    assert os.path.isfile(filename)

    mapdl_corba.kplot(knum=True, vtk=False)  # make sure legacy still works


@skip_no_xserver
def test_aplot(cleared, mapdl_corba):
    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 1, 1, 0)
    k3 = mapdl_corba.k("", 0, 1, 0)
    l0 = mapdl_corba.l(k0, k1)
    l1 = mapdl_corba.l(k1, k2)
    l2 = mapdl_corba.l(k2, k3)
    l3 = mapdl_corba.l(k3, k0)
    mapdl_corba.al(l0, l1, l2, l3)
    mapdl_corba.aplot(show_area_numbering=True)
    mapdl_corba.aplot(color_areas=True, show_lines=True, show_line_numbering=True)

    mapdl_corba.aplot(quality=100)
    mapdl_corba.aplot(quality=-1)

    # and legacy as well
    mapdl_corba.aplot(vtk=False)


@skip_no_xserver
@pytest.mark.parametrize("vtk", [True, False])
def test_vplot(cleared, mapdl_corba, vtk):
    mapdl_corba.block(0, 1, 0, 1, 0, 1)
    mapdl_corba.vplot(vtk=vtk, color_areas=True)


def test_keypoints(cleared, mapdl_corba):
    assert mapdl_corba.geometry.n_keypoint == 0
    kps = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    i = 1
    knum = []
    for x, y, z in kps:
        mapdl_corba.k(i, x, y, z)
        knum.append(i)
        i += 1

    assert mapdl_corba.geometry.n_keypoint == 4
    assert np.allclose(kps, mapdl_corba.geometry.keypoints)
    assert np.allclose(knum, mapdl_corba.geometry.knum)


def test_lines(cleared, mapdl_corba):
    assert mapdl_corba.geometry.n_line == 0

    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 1, 1, 0)
    k3 = mapdl_corba.k("", 0, 1, 0)
    l0 = mapdl_corba.l(k0, k1)
    l1 = mapdl_corba.l(k1, k2)
    l2 = mapdl_corba.l(k2, k3)
    l3 = mapdl_corba.l(k3, k0)

    lines = mapdl_corba.geometry.lines
    assert isinstance(lines, pyvista.PolyData)
    assert np.allclose(mapdl_corba.geometry.lnum, [l0, l1, l2, l3])
    assert mapdl_corba.geometry.n_line == 4


@skip_no_xserver
def test_lplot(cleared, mapdl_corba, tmpdir):
    mapdl_corba.lplot(vtk=True)

    k0 = mapdl_corba.k("", 0, 0, 0)
    k1 = mapdl_corba.k("", 1, 0, 0)
    k2 = mapdl_corba.k("", 1, 1, 0)
    k3 = mapdl_corba.k("", 0, 1, 0)
    mapdl_corba.l(k0, k1)
    mapdl_corba.l(k1, k2)
    mapdl_corba.l(k2, k3)
    mapdl_corba.l(k3, k0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl_corba.lplot(show_keypoint_numbering=True, savefig=filename)
    assert cpos is None
    assert os.path.isfile(filename)

    mapdl_corba.lplot(vtk=False)  # make sure legacy still works


def test_logging(mapdl_corba, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))
    if mapdl_corba._log is None:
        mapdl_corba.open_apdl_log(filename, mode="w")
    mapdl_corba._close_apdl_log()

    # test append mode
    mapdl_corba.open_apdl_log(filename, mode="a")

    # don't allow to double log
    with pytest.raises(MapdlRuntimeError):
        mapdl_corba.open_apdl_log(filename, mode="w")

    mapdl_corba.prep7()
    mapdl_corba.k(1, 0, 0, 0)
    mapdl_corba.k(2, 1, 0, 0)
    mapdl_corba.k(3, 1, 1, 0)
    mapdl_corba.k(4, 0, 1, 0)

    mapdl_corba._apdl_log.flush()

    out = open(mapdl_corba._apdl_log.name).read().strip().split()[-5:]
    assert "PREP7" in out[0]
    assert "K,4,0,1,0" in out[-1]


def test_nodes(tmpdir, cleared, mapdl_corba):
    mapdl_corba.n(1, 1, 1, 1)
    mapdl_corba.n(11, 10, 1, 1)
    mapdl_corba.fill(1, 11, 9)

    basename = "tmp.nodes"
    filename = str(tmpdir.mkdir("tmpdir").join(basename))
    if mapdl_corba._local:
        mapdl_corba.nwrite(filename)
    else:
        mapdl_corba.nwrite(basename)
        mapdl_corba.download(basename, filename)

    assert np.allclose(mapdl_corba.mesh.nodes, np.loadtxt(filename)[:, 1:])
    assert mapdl_corba.mesh.n_node == 11
    assert np.allclose(mapdl_corba.mesh.nnum, range(1, 12))

    # test clear mapdl
    mapdl_corba.clear()
    assert not mapdl_corba.mesh.nodes.size
    assert not mapdl_corba.mesh.n_node
    assert not mapdl_corba.mesh.nnum.size


def test_enum(mapdl_corba, make_block):
    assert mapdl_corba.mesh.n_elem
    assert np.allclose(mapdl_corba.mesh.enum, range(1, mapdl_corba.mesh.n_elem + 1))


@pytest.mark.parametrize("nnum", [True, False])
@skip_no_xserver
def test_nplot_vtk(cleared, mapdl_corba, nnum):
    mapdl_corba.nplot()

    mapdl_corba.n(1, 0, 0, 0)
    mapdl_corba.n(11, 10, 0, 0)
    mapdl_corba.fill(1, 11, 9)
    mapdl_corba.nplot(vtk=True, nnum=nnum, background="w", color="k")


@skip_no_xserver
def test_nplot(cleared, mapdl_corba):
    mapdl_corba.n(1, 0, 0, 0)
    mapdl_corba.n(11, 10, 0, 0)
    mapdl_corba.fill(1, 11, 9)
    mapdl_corba.nplot(vtk=False, background="w", color="k")


def test_elements(cleared, mapdl_corba):
    mapdl_corba.et(1, 185)

    # two basic cells
    cell1 = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1],
    ]

    cell2 = [
        [0, 0, 2],
        [1, 0, 2],
        [1, 1, 2],
        [0, 1, 2],
        [0, 0, 3],
        [1, 0, 3],
        [1, 1, 3],
        [0, 1, 3],
    ]

    with mapdl_corba.non_interactive:
        for cell in [cell1, cell2]:
            for x, y, z in cell:
                mapdl_corba.n(x=x, y=y, z=z)

    mapdl_corba.e(*list(range(1, 9)))
    mapdl_corba.e(*list(range(9, 17)))
    expected = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 9, 10, 11, 12, 13, 14, 15, 16],
        ]
    )
    if "Grpc" in str(type(mapdl_corba)):
        # no element number in elements
        expected[:, 8] = 0

    assert np.allclose(np.array(mapdl_corba.mesh.elem), expected)


# this is not that stable
@pytest.mark.parametrize(
    "parm",
    (
        "my_string",
        1,
        10.0,
        # [1, 2, 3],
        # [[1, 2, 3], [1, 2, 3]],
        # np.random.random((10000)),  # fails on gRPC at 100000
        np.random.random((10, 3)),
        np.random.random((10, 3, 3)),
    ),
)
def test_set_get_parameters(mapdl_corba, parm):
    parm_name = pymapdl.misc.random_string(20)
    mapdl_corba.parameters[parm_name] = parm
    if isinstance(parm, str):
        assert mapdl_corba.parameters[parm_name] == parm
    else:
        assert np.allclose(mapdl_corba.parameters[parm_name], parm)


def test_set_parameters_arr_to_scalar(mapdl_corba, cleared):
    mapdl_corba.parameters["PARM"] = np.arange(10)
    mapdl_corba.parameters["PARM"] = 2


def test_set_parameters_string_spaces(mapdl_corba):
    with pytest.raises(ValueError):
        mapdl_corba.parameters["PARM"] = "string with spaces"


def test_builtin_parameters(mapdl_corba, cleared):
    mapdl_corba.prep7()
    assert mapdl_corba.parameters.routine == "PREP7"

    mapdl_corba.units("SI")
    assert mapdl_corba.parameters.units == "SI"

    assert isinstance(mapdl_corba.parameters.revision, float)

    if os.name == "posix":
        assert "LIN" in mapdl_corba.parameters.platform

    mapdl_corba.csys(1)
    assert mapdl_corba.parameters.csys == 1

    mapdl_corba.dsys(1)
    assert mapdl_corba.parameters.dsys == 1

    mapdl_corba.esys(0)
    assert mapdl_corba.parameters.esys == 0
    assert mapdl_corba.parameters.material == 1
    assert mapdl_corba.parameters.section == 1
    assert mapdl_corba.parameters.real == 1


@skip_no_xserver
def test_eplot(mapdl_corba, make_block):
    init_elem = mapdl_corba.mesh.n_elem
    mapdl_corba.aplot()  # check aplot and verify it doesn't mess up the element plotting
    mapdl_corba.eplot(show_node_numbering=True, background="w", color="b")
    mapdl_corba.aplot()  # check aplot and verify it doesn't mess up the element plotting
    assert mapdl_corba.mesh.n_elem == init_elem


@skip_no_xserver
def test_eplot_screenshot(mapdl_corba, make_block, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    mapdl_corba.eplot(
        background="w",
        show_edges=True,
        smooth_shading=True,
        window_size=[1920, 1080],
        savefig=filename,
    )
    assert os.path.isfile(filename)


def test_cyclic_solve(mapdl_corba, cleared):
    # build the cyclic model
    mapdl_corba.prep7()
    mapdl_corba.shpp("off")
    mapdl_corba.cdread("db", examples.sector_archive_file)
    mapdl_corba.prep7()
    mapdl_corba.cyclic()

    # set material properties
    mapdl_corba.mp("NUXY", 1, 0.31)
    mapdl_corba.mp("DENS", 1, 4.1408e-04)
    mapdl_corba.mp("EX", 1, 16900000)
    mapdl_corba.emodif("ALL", "MAT", 1)

    # setup and solve
    mapdl_corba.modal_analysis("LANB", 1, 1, 100000, elcalc=True)
    mapdl_corba.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    if mapdl_corba._local:
        assert mapdl_corba.result.nsets == 16


def test_partial_mesh_nnum(mapdl_corba, make_block):
    allsel_nnum_old = mapdl_corba.mesh.nnum
    mapdl_corba.nsel("S", "NODE", vmin=100, vmax=200)
    allsel_nnum_now = mapdl_corba.mesh.nnum_all
    assert np.allclose(allsel_nnum_old, allsel_nnum_now)

    mapdl_corba.allsel()
    assert np.allclose(allsel_nnum_old, mapdl_corba.mesh.nnum)


def test_partial_mesh_nnum(mapdl_corba, make_block):
    mapdl_corba.nsel("S", "NODE", vmin=1, vmax=10)
    mapdl_corba.esel("S", "ELEM", vmin=10, vmax=20)
    assert mapdl_corba.mesh._grid.n_cells == 11


def test_cyclic_solve(mapdl_corba, cleared):
    # build the cyclic model
    mapdl_corba.prep7()
    mapdl_corba.shpp("off")
    mapdl_corba.cdread("db", examples.sector_archive_file)
    mapdl_corba.prep7()
    time.sleep(1.0)
    mapdl_corba.cyclic()

    # set material properties
    mapdl_corba.mp("NUXY", 1, 0.31)
    mapdl_corba.mp("DENS", 1, 4.1408e-04)
    mapdl_corba.mp("EX", 1, 16900000)
    mapdl_corba.emodif("ALL", "MAT", 1)

    # setup and solve
    mapdl_corba.modal_analysis("LANB", 1, 1, 100000, elcalc=True)
    mapdl_corba.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    assert mapdl_corba.result.nsets == 16  # multiple result files...


# Using ``np.ones(5)*2`` to test specifically the case for two columns #883
@pytest.mark.parametrize("dim_rows", np.random.randint(2, 100, size=4, dtype=int))
@pytest.mark.parametrize(
    "dim_cols",
    np.concatenate(
        (
            np.ones(2, dtype=int) * 2,
            np.random.randint(2, 100, size=2, dtype=int),
        )
    ),
)
def test_load_table(mapdl_corba, dim_rows, dim_cols):
    my_conv = np.random.rand(dim_rows, dim_cols)
    my_conv[:, 0] = np.arange(dim_rows)
    my_conv[0, :] = np.arange(dim_cols)

    mapdl_corba.load_table("my_conv", my_conv)
    if (
        dim_cols == 2
    ):  # because mapdl output arrays with shape (x,1) not (X,) See issue: #883
        assert np.allclose(
            mapdl_corba.parameters["my_conv"],
            my_conv[1:, 1].reshape((dim_rows - 1, 1)),
            1e-7,
        )
    else:
        assert np.allclose(mapdl_corba.parameters["my_conv"], my_conv[1:, 1:], 1e-7)


def test_mode_corba(mapdl_corba):
    assert mapdl_corba.mode == "corba"
    assert not mapdl_corba.is_grpc
    assert mapdl_corba.is_corba
    assert not mapdl_corba.is_console
