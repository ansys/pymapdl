# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Test legacy MAPDL console interface

This has been copied from test_mapdl.py

"""
import os
import time
from unittest.mock import patch
from warnings import catch_warnings

import pytest

from conftest import clear, has_dependency, requires

# skip entire module unless --console is enabled
pytestmark = requires("console")

import numpy as np
import pytest

if has_dependency("pyvista"):
    import pyvista

if has_dependency("ansys-mapdl-reader"):
    from ansys.mapdl.reader import examples

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.errors import MapdlRuntimeError


@pytest.fixture(scope="function")
def cleared(mapdl_console):
    clear(mapdl_console)


@pytest.fixture(scope="function")
def make_block(mapdl_console, cleared):
    mapdl_console.block(0, 1, 0, 1, 0, 1)
    mapdl_console.et(1, 186)
    mapdl_console.esize(0.25)
    mapdl_console.vmesh("ALL")


def test_jobname(mapdl_console, cleared):
    jobname = "abcdefg"
    assert mapdl_console.jobname != jobname
    mapdl_console.finish()
    mapdl_console.filname(jobname)
    assert mapdl_console.jobname == jobname

    other_jobname = "gfedcba"
    mapdl_console.jobname = other_jobname
    assert mapdl_console.jobname == other_jobname


def test_empty(mapdl_console, cleared):
    with pytest.raises(ValueError):
        mapdl_console.run("")


def test_str(mapdl_console, cleared):
    assert "Ansys Mechanical" in str(mapdl_console)


def test_version(mapdl_console, cleared):
    assert isinstance(mapdl_console.version, float)


def test_comment(cleared, mapdl_console):
    comment = "Testing..."
    resp = mapdl_console.com(comment)
    assert comment in resp


# @skip_grpc
# def test_output(cleared, mapdl):
#     tmp_file = 'tmp_redirect.txt'
#     resp = mapdl_console.output(tmp_file)
#     comment = 'Testing...'
#     resp = mapdl_console.com(comment)
#     mapdl_console.output()
#     output = open(os.path.join(mapdl_console.path, tmp_file)).read()
#     assert comment in output


def test_basic_command(cleared, mapdl_console):
    resp = mapdl_console.block(0, 1, 0, 1, 0, 1)
    assert "CREATE A HEXAHEDRAL VOLUME" in resp


def test_allow_ignore(mapdl_console, cleared):
    mapdl_console.allow_ignore = False
    assert mapdl_console.allow_ignore is False

    mapdl_console.finish()
    with pytest.raises(pymapdl.errors.MapdlInvalidRoutineError):
        mapdl_console.k()

    # Does not create keypoints and yet does not raise error
    mapdl_console.allow_ignore = True
    assert mapdl_console.allow_ignore is True
    mapdl_console.k()
    assert mapdl_console.geometry.n_keypoint == 0


def test_chaining(mapdl_console, cleared):
    mapdl_console.prep7()
    n_kp = 1000
    with mapdl_console.chain_commands:
        for i in range(1, 1 + n_kp):
            mapdl_console.k(i, i, i, i)

    assert mapdl_console.geometry.n_keypoint == 1000


def test_e(mapdl_console, cleared):
    mapdl_console.prep7()
    mapdl_console.et("", 183)
    n0 = mapdl_console.n("", 0, 0, 0)
    n1 = mapdl_console.n("", 1, 0, 0)
    n2 = mapdl_console.n("", 1, 1, 0)
    n3 = mapdl_console.n("", 0, 1, 1)
    n4 = mapdl_console.n("", 0, 1, -1)
    e0 = mapdl_console.e(n0, n1, n2, n3)
    assert e0 == 1
    e1 = mapdl_console.e(n0, n1, n2, n4)
    assert e1 == 2


def test_et(mapdl_console, cleared):
    n_plane183 = mapdl_console.et("", "PLANE183")
    assert n_plane183 == 1
    n_compare = int(mapdl_console.get_value("ETYP", item1="NUM", it1num="MAX"))
    assert n_plane183 == n_compare
    n_plane183 = mapdl_console.et(17, "PLANE183")
    assert n_plane183 == 17


def test_k(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl_console.k(2, 0, 0, 1)
    assert k1 == 2


def test_l(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    l0 = mapdl_console.l(k0, k1)
    assert l0 == 1


def test_a(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 0, 1, 0)
    a0 = mapdl_console.a(k0, k1, k2)
    assert a0 == 1


def test_v(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 0, 1, 0)
    k3 = mapdl_console.k("", 0, 0, 1)
    v0 = mapdl_console.v(k0, k1, k2, k3)
    assert v0 == 1


def test_n(cleared, mapdl_console):
    n0 = mapdl_console.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl_console.n(2, 0, 0, 1)
    assert n1 == 2


def test_bsplin(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 2, 1, 0)
    l0 = mapdl_console.bsplin(k0, k1, k2)
    assert l0 == 1


def test_a(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 1, 1, 0)
    k3 = mapdl_console.k("", 0, 1, 0)
    a0 = mapdl_console.a(k0, k1, k2, k3)
    assert a0 == 1


def test_al(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 1, 1, 0)
    k3 = mapdl_console.k("", 0, 1, 0)
    l0 = mapdl_console.l(k0, k1)
    l1 = mapdl_console.l(k1, k2)
    l2 = mapdl_console.l(k2, k3)
    l3 = mapdl_console.l(k3, k0)
    a0 = mapdl_console.al(l0, l1, l2, l3)
    assert a0 == 1


def test_invalid_area(mapdl_console, cleared):
    with pytest.raises(MapdlRuntimeError):
        mapdl_console.a(0, 0, 0, 0)


# def test_invalid_input(mapdl_console, cleared):
# with pytest.raises(FileNotFoundError):
# mapdl_console.input('thisisnotafile')


@requires("xserver")
def test_kplot(cleared, mapdl_console, tmpdir):
    with pytest.raises(MapdlRuntimeError):
        mapdl_console.kplot(vtk=True)

    mapdl_console.k("", 0, 0, 0)
    mapdl_console.k("", 1, 0, 0)
    mapdl_console.k("", 1, 1, 0)
    mapdl_console.k("", 0, 1, 0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl_console.kplot(savefig=filename)
    assert cpos is None
    assert os.path.isfile(filename)

    mapdl_console.kplot(knum=True, vtk=False)  # make sure legacy still works


@requires("xserver")
def test_aplot(cleared, mapdl_console):
    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 1, 1, 0)
    k3 = mapdl_console.k("", 0, 1, 0)
    l0 = mapdl_console.l(k0, k1)
    l1 = mapdl_console.l(k1, k2)
    l2 = mapdl_console.l(k2, k3)
    l3 = mapdl_console.l(k3, k0)
    mapdl_console.al(l0, l1, l2, l3)
    mapdl_console.aplot(show_area_numbering=True)
    mapdl_console.aplot(color_areas=True, show_lines=True, show_line_numbering=True)

    mapdl_console.aplot(quality=100)
    mapdl_console.aplot(quality=-1)

    # and legacy as well
    mapdl_console.aplot(vtk=False)


@requires("xserver")
@pytest.mark.parametrize("vtk", [True, False])
def test_vplot(cleared, mapdl_console, vtk):
    mapdl_console.block(0, 1, 0, 1, 0, 1)
    mapdl_console.vplot(vtk=vtk, color_areas=True)


def test_keypoints(cleared, mapdl_console):
    assert mapdl_console.geometry.n_keypoint == 0
    kps = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    i = 1
    knum = []
    for x, y, z in kps:
        mapdl_console.k(i, x, y, z)
        knum.append(i)
        i += 1

    assert mapdl_console.geometry.n_keypoint == 4
    assert np.allclose(kps, mapdl_console.geometry.keypoints)
    assert np.allclose(knum, mapdl_console.geometry.knum)


def test_lines(cleared, mapdl_console):
    assert mapdl_console.geometry.n_line == 0

    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 1, 1, 0)
    k3 = mapdl_console.k("", 0, 1, 0)
    l0 = mapdl_console.l(k0, k1)
    l1 = mapdl_console.l(k1, k2)
    l2 = mapdl_console.l(k2, k3)
    l3 = mapdl_console.l(k3, k0)

    lines = mapdl_console.geometry.lines
    assert isinstance(lines, pyvista.PolyData)
    assert np.allclose(mapdl_console.geometry.lnum, [l0, l1, l2, l3])
    assert mapdl_console.geometry.n_line == 4


@requires("xserver")
def test_lplot(cleared, mapdl_console, tmpdir):
    with pytest.raises(MapdlRuntimeError):
        mapdl_console.lplot(vtk=True)

    k0 = mapdl_console.k("", 0, 0, 0)
    k1 = mapdl_console.k("", 1, 0, 0)
    k2 = mapdl_console.k("", 1, 1, 0)
    k3 = mapdl_console.k("", 0, 1, 0)
    mapdl_console.l(k0, k1)
    mapdl_console.l(k1, k2)
    mapdl_console.l(k2, k3)
    mapdl_console.l(k3, k0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl_console.lplot(show_keypoint_numbering=True, savefig=filename)
    assert cpos is None
    assert os.path.isfile(filename)

    mapdl_console.lplot(vtk=False)  # make sure legacy still works


def test_logging(mapdl_console, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))
    if mapdl_console._log is None:
        mapdl_console.open_apdl_log(filename, mode="w")
    mapdl_console._close_apdl_log()

    # test append mode
    mapdl_console.open_apdl_log(filename, mode="a")

    # don't allow to double log
    with pytest.raises(MapdlRuntimeError):
        mapdl_console.open_apdl_log(filename, mode="w")

    mapdl_console.prep7()
    mapdl_console.k(1, 0, 0, 0)
    mapdl_console.k(2, 1, 0, 0)
    mapdl_console.k(3, 1, 1, 0)
    mapdl_console.k(4, 0, 1, 0)

    mapdl_console._apdl_log.flush()

    out = open(mapdl_console._apdl_log.name).read().strip().split()[-5:]
    assert "PREP7" in out[0]
    assert "K,4,0,1,0" in out[-1]


def test_nodes(tmpdir, cleared, mapdl_console):
    mapdl_console.n(1, 1, 1, 1)
    mapdl_console.n(11, 10, 1, 1)
    mapdl_console.fill(1, 11, 9)

    basename = "tmp.nodes"
    filename = str(tmpdir.mkdir("tmpdir").join(basename))
    mapdl_console.nwrite(filename)
    # mapdl_console.download(basename, filename)

    assert np.allclose(mapdl_console.mesh.nodes, np.loadtxt(filename)[:, 1:])
    assert mapdl_console.mesh.n_node == 11
    assert np.allclose(mapdl_console.mesh.nnum, range(1, 12))

    # test clear mapdl
    mapdl_console.clear()
    assert not mapdl_console.mesh.nodes.size
    assert not mapdl_console.mesh.n_node
    assert not mapdl_console.mesh.nnum.size


def test_enum(mapdl_console, make_block):
    assert mapdl_console.mesh.n_elem
    assert np.allclose(mapdl_console.mesh.enum, range(1, mapdl_console.mesh.n_elem + 1))


@pytest.mark.parametrize("knum", [True, False])
@requires("xserver")
def test_nplot_vtk(cleared, mapdl_console, knum):
    with pytest.raises(MapdlRuntimeError):
        mapdl_console.nplot()

    mapdl_console.n(1, 0, 0, 0)
    mapdl_console.n(11, 10, 0, 0)
    mapdl_console.fill(1, 11, 9)
    mapdl_console.nplot(vtk=True, knum=knum, background="w", color="k")


@requires("xserver")
def test_nplot(cleared, mapdl_console):
    mapdl_console.n(1, 0, 0, 0)
    mapdl_console.n(11, 10, 0, 0)
    mapdl_console.fill(1, 11, 9)
    mapdl_console.nplot(vtk=False, background="w", color="k")


def test_elements(cleared, mapdl_console):
    mapdl_console.et(1, 185)

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

    with mapdl_console.chain_commands:
        for cell in [cell1, cell2]:
            for x, y, z in cell:
                mapdl_console.n(x=x, y=y, z=z)

    mapdl_console.e(*list(range(1, 9)))
    mapdl_console.e(*list(range(9, 17)))
    expected = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 9, 10, 11, 12, 13, 14, 15, 16],
        ]
    )
    if "Grpc" in str(type(mapdl_console)):
        # no element number in elements
        expected[:, 8] = 0

    assert np.allclose(np.array(mapdl_console.mesh.elem), expected)


# this test is prone to fail on console
@pytest.mark.xfail
@pytest.mark.parametrize(
    "parm",
    (
        "my_string",
        1,
        10.0,
        [1, 2, 3],
        [[1, 2, 3], [1, 2, 3]],
        np.random.random((10000)),  # fails on gRPC at 100000
        np.random.random((10, 3)),
        np.random.random((10, 3, 3)),
    ),
)
def test_set_get_parameters(mapdl_console, cleared, parm):
    parm_name = pymapdl.misc.random_string(20)
    mapdl_console.parameters[parm_name] = parm
    if isinstance(parm, str):
        assert mapdl_console.parameters[parm_name] == parm
    else:
        assert np.allclose(mapdl_console.parameters[parm_name], parm)


def test_set_parameters_arr_to_scalar(mapdl_console, cleared):
    mapdl_console.parameters["PARM"] = np.arange(10)
    mapdl_console.parameters["PARM"] = 2


def test_set_parameters_string_spaces(mapdl_console, cleared):
    with pytest.raises(ValueError):
        mapdl_console.parameters["PARM"] = "string with spaces"


def test_builtin_parameters(mapdl_console, cleared):
    mapdl_console.prep7()
    assert mapdl_console.parameters.routine == "PREP7"

    mapdl_console.units("SI")
    assert mapdl_console.parameters.units == "SI"

    assert isinstance(mapdl_console.parameters.revision, float)

    if os.name == "posix":
        assert "LIN" in mapdl_console.parameters.platform

    mapdl_console.csys(1)
    assert mapdl_console.parameters.csys == 1

    mapdl_console.dsys(1)
    assert mapdl_console.parameters.dsys == 1

    mapdl_console.esys(0)
    assert mapdl_console.parameters.esys == 0
    assert mapdl_console.parameters.material == 1
    assert mapdl_console.parameters.section == 1
    assert mapdl_console.parameters.real == 1


def test_eplot_fail(mapdl_console, cleared):
    # must fail with empty mesh
    with pytest.raises(MapdlRuntimeError):
        mapdl_console.eplot()


@requires("xserver")
def test_eplot(mapdl_console, make_block):
    init_elem = mapdl_console.mesh.n_elem
    mapdl_console.aplot()  # check aplot and verify it doesn't mess up the element plotting
    mapdl_console.eplot(show_node_numbering=True, background="w", color="b")
    mapdl_console.aplot()  # check aplot and verify it doesn't mess up the element plotting
    assert mapdl_console.mesh.n_elem == init_elem


@requires("xserver")
def test_eplot_screenshot(mapdl_console, make_block, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    mapdl_console.eplot(
        background="w",
        show_edges=True,
        smooth_shading=True,
        window_size=[1920, 1080],
        savefig=filename,
    )
    assert os.path.isfile(filename)


def test_cyclic_solve(mapdl_console, cleared):
    # build the cyclic model
    mapdl_console.prep7()
    mapdl_console.shpp("off")
    mapdl_console.cdread("db", examples.sector_archive_file)
    mapdl_console.prep7()
    mapdl_console.cyclic()

    # set material properties
    mapdl_console.mp("NUXY", 1, 0.31)
    mapdl_console.mp("DENS", 1, 4.1408e-04)
    mapdl_console.mp("EX", 1, 16900000)
    mapdl_console.emodif("ALL", "MAT", 1)

    # setup and solve
    mapdl_console.modal_analysis("LANB", 1, 1, 100000, elcalc=True)
    mapdl_console.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    if mapdl_console._local:
        assert mapdl_console.result.nsets == 16


def test_partial_mesh_nnum(mapdl_console, make_block):
    allsel_nnum_old = mapdl_console.mesh.nnum
    mapdl_console.nsel("S", "NODE", vmin=100, vmax=200)
    allsel_nnum_now = mapdl_console.mesh.nnum_all
    assert np.allclose(allsel_nnum_old, allsel_nnum_now)

    mapdl_console.allsel()
    assert np.allclose(allsel_nnum_old, mapdl_console.mesh.nnum)


def test_partial_mesh_nnum(mapdl_console, make_block):
    mapdl_console.nsel("S", "NODE", vmin=1, vmax=10)
    mapdl_console.esel("S", "ELEM", vmin=10, vmax=20)
    assert mapdl_console.mesh._grid.n_cells == 11


def test_cyclic_solve(mapdl_console, cleared):
    # build the cyclic model
    mapdl_console.prep7()
    mapdl_console.shpp("off")
    mapdl_console.cdread("db", examples.sector_archive_file)
    mapdl_console.prep7()
    time.sleep(1.0)
    mapdl_console.cyclic()

    # set material properties
    mapdl_console.mp("NUXY", 1, 0.31)
    mapdl_console.mp("DENS", 1, 4.1408e-04)
    mapdl_console.mp("EX", 1, 16900000)
    mapdl_console.emodif("ALL", "MAT", 1)

    # setup and solve
    mapdl_console.modal_analysis("LANB", 1, 1, 100000, elcalc=True)
    mapdl_console.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    assert mapdl_console.result.nsets == 16  # multiple result files...


def test_load_table(mapdl_console, cleared):
    my_conv = np.array(
        [
            [0, 0.001],
            [120, 0.001],
            [130, 0.005],
            [700, 0.005],
            [710, 0.002],
            [1000, 0.002],
        ]
    )
    mapdl_console.load_table("my_conv", my_conv, "TIME")
    assert np.allclose(
        mapdl_console.parameters["my_conv"].reshape(-1, 1),
        my_conv[:, -1].reshape(-1, 1),
    )


def test_mode_console(mapdl_console, cleared):
    assert mapdl_console.mode == "console"
    assert not mapdl_console.is_grpc
    assert not mapdl_console.is_corba
    assert mapdl_console.is_console


@requires("console")
def test_console_apdl_logging_start(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))

    mapdl = pymapdl.launch_mapdl(log_apdl=filename, mode="console")

    mapdl.prep7()
    mapdl.run("!comment test")
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)

    mapdl.exit()

    with open(filename, "r") as fid:
        text = "".join(fid.readlines())

    assert "PREP7" in text
    assert "!comment test" in text
    assert "K,1,0,0,0" in text
    assert "K,2,1,0,0" in text
    assert "K,3,1,1,0" in text
    assert "K,4,0,1,0" in text


def test__del__console():
    from ansys.mapdl.core.mapdl_console import MapdlConsole

    class FakeProcess:
        def sendline(self, command):
            pass

    class DummyMapdl(MapdlConsole):
        @property
        def _process(self):
            return _proc

        def __init__(self):
            self._proc = FakeProcess()

    with (
        patch.object(DummyMapdl, "_process", autospec=True) as mock_process,
        patch.object(DummyMapdl, "_close_apdl_log") as mock_close_log,
    ):

        mock_close_log.return_value = None

        # Setup
        mapdl = DummyMapdl()

        del mapdl

        mock_close_log.assert_not_called()
        assert [each.args[0] for each in mock_process.sendline.call_args_list] == [
            "FINISH",
            "EXIT",
        ]


@pytest.mark.parametrize("close_log", [True, False])
def test_exit_console(mapdl_console, close_log):
    with (
        patch.object(mapdl_console, "_close_apdl_log") as mock_close_log,
        patch.object(mapdl_console, "_exit") as mock_exit,
    ):
        mock_exit.return_value = None
        mock_close_log.return_value = None

        with catch_warnings(record=True):
            mapdl_console.exit(close_log=close_log, timeout=1)

        if close_log:
            mock_close_log.assert_called_once()
        else:
            mock_close_log.assert_not_called()

        mock_exit.assert_called_once()
