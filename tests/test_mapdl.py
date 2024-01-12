# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Test MAPDL interface"""
from datetime import datetime
import os
from pathlib import Path
import re
import shutil
import tempfile
import time

import grpc
import numpy as np
import psutil
import pytest

from conftest import has_dependency

if has_dependency("pyvista"):
    from pyvista import MultiBlock

if has_dependency("ansys-mapdl-reader"):
    from ansys.mapdl.reader.rst import Result

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.commands import CommandListingOutput
from ansys.mapdl.core.errors import (
    CommandDeprecated,
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlConnectionError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.launcher import launch_mapdl
from ansys.mapdl.core.mapdl_grpc import SESSION_ID_NAME
from ansys.mapdl.core.misc import random_string
from conftest import IS_SMP, ON_CI, ON_LOCAL, QUICK_LAUNCH_SWITCHES, requires

# Path to files needed for examples
PATH = os.path.dirname(os.path.abspath(__file__))
test_files = os.path.join(PATH, "test_files")

DEPRECATED_COMMANDS = [
    "edasmp",
    "edbound",
    "edbx",
    "edcgen",
    "edclist",
    "edcmore",
    "edcnstr",
    "edcontact",
    "edcrb",
    "edcurve",
    "eddbl",
    "eddc",
    "edipart",
    "edlcs",
    "edmp",
    "ednb",
    "edndtsd",
    "ednrot",
    "edpart",
    "edpc",
    "edsp",
    "edweld",
    "edadapt",
    "edale",
    "edbvis",
    "edcadapt",
    "edcpu",
    "edcsc",
    "edcts",
    "eddamp",
    "eddrelax",
    "eddump",
    "edenergy",
    "edfplot",
    "edgcale",
    "edhgls",
    "edhist",
    "edhtime",
    "edint",
    "edis",
    "edload",
    "edopt",
    "edout",
    "edpl",
    "edpvel",
    "edrc",
    "edrd",
    "edri",
    "edrst",
    "edrun",
    "edshell",
    "edsolv",
    "edstart",
    "edterm",
    "edtp",
    "edvel",
    "edwrite",
    "rexport",
]

CMD_BLOCK = """/prep7
! Mat
MP,EX,1,200000
MP,NUXY,1,0.3
MP,DENS,1,7.85e-09
! Elements
et,1,186
et,2,154
! Geometry
BLC4,0,0,1000,100,10
! Mesh
esize,5
vmesh,all
"""

## Testing CDREAD and CDWRITE
# DB file generated locally with ANSYS.
# Many of the commands could be deleted, but for the sake of good
# testing we are going to leave them.

CDB_FILE = """                                                                        S      1
/COM,ANSYS RELEASE 12.1BETAUP20090531       10:26:32    06/01/2009      S      2
/NOPR                                                                   S      3
/PREP7                                                                  S      4
/TITLE,                                                                 S      5
1H,,1H;,,18Hdisc_pad_model.cdb,                                         G      1
5HANSYS,22H  12.1BETA  UP20090531,,,,,,,1.0,,,,,13H000601.102632,       G      2
1.0000E-04,,,,9,,;                                                      G      3
S     29G      3D      0P      0                                        T      1
:CDWRITE      ! START OF CDWRITE DATA
/COM,ANSYS RELEASE 2021 R2           BUILD 21.2
/PREP7
/NOPR
/TITLE,'CDREAD and CDWRITE tests'
*IF,_CDRDOFF,EQ,1,THEN     !if solid model was read in
_CDRDOFF=             !reset flag, numoffs already performed
*ELSE              !offset database for the following FE model
*ENDIF
*SET,T_PAR,'asdf1234'
*SET,_RETURN ,  0.000000000000
*SET,_STATUS ,  0.000000000000
*SET,_UIQR   ,  1.000000000000
DOF,DELETE
EXTOPT,ATTR,      0,      0,      0
EXTOPT,ESIZE,  0,  0.0000
EXTOPT,ACLEAR,      0
TREF,  0.00000000
IRLF,  0
BFUNIF,TEMP,_TINY
ACEL,  0.00000000    ,  0.00000000    ,  0.00000000
OMEGA,  0.00000000    ,  0.00000000    ,  0.00000000
DOMEGA,  0.00000000    ,  0.00000000    ,  0.00000000
CGLOC,  0.00000000    ,  0.00000000    ,  0.00000000
CGOMEGA,  0.00000000    ,  0.00000000    ,  0.00000000
DCGOMG,  0.00000000    ,  0.00000000    ,  0.00000000

KUSE,     0
TIME,  0.00000000
ALPHAD,  0.00000000
BETAD,  0.00000000
DMPRAT,  0.00000000
DMPSTR,  0.00000000
CRPLIM, 0.100000000    ,   0
CRPLIM,  0.00000000    ,   1
NCNV,     1,  0.00000000    ,     0,  0.00000000    ,  0.00000000
NEQIT,     0

ERESX,DEFA
/GO
FINISH
"""


def clearing_cdread_cdwrite_tests(mapdl):
    mapdl.finish(mute=True)
    # *MUST* be NOSTART.  With START fails after 20 calls...
    # this has been fixed in later pymapdl and MAPDL releases
    mapdl.clear("NOSTART", mute=True)
    mapdl.prep7(mute=True)


def asserting_cdread_cdwrite_tests(mapdl):
    # Using ``in`` because of the padding APDL does on strings.
    return "asdf1234" in mapdl.parameters["T_PAR"]


def warns_in_cdread_error_log(mapdl, tmpdir):
    """Check for specific warns in the error log associated with using /INPUT with CDB files
    instead of CDREAD command."""
    if mapdl._local:
        pth = mapdl.directory

    else:
        list_files = mapdl.list_files()
        error_files = [each for each in list_files if each.endswith(".err")]
        pth = str(tmpdir.mkdir(random_string()))

        for each_file in error_files:
            mapdl.download(each_file, pth)

    list_files = os.listdir(pth)
    error_files = [each for each in list_files if each.endswith(".err")]

    # "S 1", "1 H" and "5 H Ansys" are character at the end of lines in the CDB_FILE variable.
    # They are allowed in the CDREAD command, but it gives warnings in the /INPUT command.
    warn_cdread_1 = "S1 is not a recognized"
    warn_cdread_2 = "1H is not a recognized"
    warn_cdread_3 = "5HANSYS is not a recognized"

    warns = []
    for each in error_files:
        with open(os.path.join(pth, each), errors="ignore") as fid:
            error_log = "".join(fid.readlines())
        warns.append(
            (warn_cdread_1 in error_log)
            or (warn_cdread_2 in error_log)
            or (warn_cdread_3 in error_log)
        )
        return any(warns)


@pytest.mark.parametrize("command", DEPRECATED_COMMANDS)
def test_deprecated_commands(mapdl, command):
    with pytest.raises(CommandDeprecated):
        method = getattr(mapdl, command)
        method()


@requires("grpc")
def test_internal_name_grpc(mapdl):
    assert str(mapdl._ip) in mapdl.name
    assert str(mapdl._port) in mapdl.name
    assert "GRPC" in mapdl.name

    assert mapdl.name
    assert mapdl.name == mapdl._name

    with pytest.raises(AttributeError):
        mapdl.name = "asfd"


def test_jobname(mapdl, cleared):
    jobname = "abcdefg"
    assert mapdl.jobname != jobname
    mapdl.finish()
    mapdl.filname(jobname)
    assert mapdl.jobname == jobname

    other_jobname = "gfedcba"
    mapdl.jobname = other_jobname
    assert mapdl.jobname == other_jobname


@requires("grpc")
def test_server_version(mapdl):
    if mapdl.version == 20.2:
        assert mapdl._server_version == (0, 0, 0)
    elif mapdl.version == 21.1:
        assert mapdl._server_version == (0, 3, 0)
    elif mapdl.version == 21.2:
        assert mapdl._server_version in [(0, 4, 0), (0, 4, 1)]
    else:
        # untested future version
        assert isinstance(mapdl._server_version, tuple)
        assert mapdl._server_version[1] >= 4
        assert mapdl._server_version[0] >= 0


@requires("grpc")
def test_global_mute(mapdl):
    mapdl.mute = True
    assert mapdl.mute is True
    assert mapdl.prep7() is None

    # commands like /INQUIRE must always return something
    jobname = "file"
    mapdl.jobname = jobname
    assert mapdl.inquire("", "JOBNAME") == jobname
    mapdl.mute = False


def test_parsav_parres(mapdl, cleared, tmpdir):
    arr = np.random.random((10, 3))

    mapdl.parameters["MYARR"] = arr
    mapdl.parsav("ALL", "db.txt")
    mapdl.download("db.txt")

    # Restoring
    mapdl.clear()
    mapdl.parres("ALL", "db.txt")
    assert np.allclose(mapdl.parameters["MYARR"], arr)

    # test no filename
    mapdl.clear()
    mapdl.parameters["MYARR"] = arr
    mapdl.parsav("ALL")

    mapdl.clear()
    mapdl.parres("ALL")
    assert np.allclose(mapdl.parameters["MYARR"], arr)

    # Test upload local
    mapdl.clear()
    if "db.txt" in mapdl.list_files():
        mapdl.slashdelete("db.txt")

    mapdl.parres("NEW", "db", "txt")
    assert np.allclose(mapdl.parameters["MYARR"], arr)

    # Test directory error
    mapdl.clear()
    with pytest.raises(FileNotFoundError):
        mapdl.parres("NEW", os.getcwd())

    # Test non-existing file
    mapdl.clear()
    with pytest.raises(FileNotFoundError):
        mapdl.parres("change", "mydummy", "file")

    os.remove("db.txt")


@requires("grpc")
def test_no_results(mapdl, cleared, tmpdir):
    pth = str(tmpdir.mkdir("tmpdir"))
    mapdl.jobname = random_string()
    with pytest.raises(FileNotFoundError):
        mapdl.download_result(pth)


def test_empty(mapdl):
    with pytest.raises(ValueError):
        mapdl.run("")


def test_multiline_fail(mapdl):
    with pytest.raises(ValueError, match="Use ``input_strings``"):
        mapdl.run(CMD_BLOCK)


def test_multiline_fail(mapdl, cleared):
    with pytest.warns(DeprecationWarning):
        resp = mapdl.run_multiline(CMD_BLOCK)
        assert "IS SOLID186" in resp, "not capturing the beginning of the block"
        assert (
            "GENERATE NODES AND ELEMENTS" in resp
        ), "not capturing the end of the block"


def test_input_strings_fail(mapdl, cleared):
    resp = mapdl.input_strings(CMD_BLOCK)
    assert "IS SOLID186" in resp, "not capturing the beginning of the block"
    assert "GENERATE NODES AND ELEMENTS" in resp, "not capturing the end of the block"


def test_input_strings(mapdl, cleared):
    assert isinstance(mapdl.input_strings(CMD_BLOCK), str)
    assert isinstance(mapdl.input_strings(CMD_BLOCK.splitlines()), str)


def test_str(mapdl):
    mapdl_str = str(mapdl)
    assert "Product:" in mapdl_str
    assert "MAPDL Version" in mapdl_str
    assert str(mapdl.version) in mapdl_str


def test_version(mapdl):
    assert isinstance(mapdl.version, float)  # Checking MAPDL version
    expected_version = float(
        datetime.now().year - 2000 + 1 + 1
    )  # the second +1 is to give some tolerance.
    assert 20.0 < mapdl.version < expected_version  # Some upper bound.


def test_pymapdl_version():
    from ansys.mapdl.core._version import __version__ as pymapdl_version

    assert isinstance(pymapdl_version, str)
    version_ = pymapdl_version.split(".")

    assert len(version_) == 3
    assert version_[0].isnumeric()
    assert version_[1].isnumeric()
    assert version_[2].isnumeric() or "dev" in version_[2]


def test_comment(cleared, mapdl):
    comment = "Testing..."
    resp = mapdl.com(comment)
    assert comment in resp


def test_basic_command(cleared, mapdl):
    resp = mapdl.prep7()
    resp = mapdl.finish()
    assert "ROUTINE COMPLETED" in resp


def test_allow_ignore(mapdl):
    mapdl.clear()
    mapdl.allow_ignore = False
    assert mapdl.allow_ignore is False
    with pytest.raises(pymapdl.errors.MapdlInvalidRoutineError):
        mapdl.k()

    # Does not create keypoints and yet does not raise error
    mapdl.allow_ignore = True
    assert mapdl.allow_ignore is True
    mapdl.k()
    with pytest.raises(ValueError, match="There are no KEYPOINTS defined"):
        mapdl.get_value("KP", 0, "count")
    mapdl.allow_ignore = False


def test_chaining(mapdl, cleared):
    # test chaining with distributed only
    if mapdl._distributed:
        with pytest.raises(MapdlRuntimeError):
            with mapdl.chain_commands:
                mapdl.prep7()
    else:
        mapdl.prep7()
        n_kp = 1000
        with mapdl.chain_commands:
            for i in range(1, 1 + n_kp):
                mapdl.k(i, i, i, i)

        assert mapdl.geometry.n_keypoint == 1000


def test_error(mapdl):
    with pytest.raises(MapdlRuntimeError):
        mapdl.prep7()
        mapdl.a(0, 0, 0, 0)


def test_ignore_error(mapdl):
    mapdl.ignore_errors = False
    assert not mapdl.ignore_errors
    mapdl.ignore_errors = True
    assert mapdl.ignore_errors is True

    # verify that an error is not raised
    mapdl.prep7(mute=True)
    out = mapdl._run("A, 0, 0, 0")
    assert "*** ERROR ***" in out

    mapdl.ignore_error = False
    assert mapdl.ignore_error is False


@requires("grpc")
def test_list(mapdl, tmpdir):
    """Added for backwards compatibility"""
    fname = "tmp.txt"
    filename = str(tmpdir.mkdir("tmpdir").join(fname))
    txt = "this is a test"
    with open(filename, "w") as fid:
        fid.write(txt)
    mapdl.upload(filename)

    output = mapdl.list(fname)
    assert output == txt


@requires("grpc")
def test_invalid_input(mapdl):
    with pytest.raises(FileNotFoundError):
        mapdl.input("thisisnotafile")


def test_keypoints(cleared, mapdl):
    assert mapdl.geometry.n_keypoint == 0
    kps = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]

    i = 1
    knum = []
    for i, (x, y, z) in enumerate(kps):
        mapdl.k(i + 1, x, y, z)
        knum.append(i + 1)

    assert mapdl.geometry.n_keypoint == 4
    assert np.allclose(knum, mapdl.geometry.knum)

    if has_dependency("pyvista"):
        assert isinstance(mapdl.geometry.keypoints, MultiBlock)
        assert np.allclose(kps, mapdl.geometry.get_keypoints(return_as_array=True))


@requires("pyvista")
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
    assert np.allclose(mapdl.geometry.lnum, [l0, l1, l2, l3])
    assert mapdl.geometry.n_line == 4

    if has_dependency("pyvista"):
        assert isinstance(lines, MultiBlock)


@requires("local")
def test_apdl_logging_start(tmpdir, mapdl):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))

    mapdl = launch_mapdl(
        port=mapdl.port - 1,  # It normally goes up, so 50051 should be free
        start_timeout=30,
        log_apdl=filename,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )

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


@requires("console")
def test_console_apdl_logging_start(tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.inp"))

    mapdl = launch_mapdl(log_apdl=filename, mode="console")

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


def test_apdl_logging(mapdl, tmpdir):
    tmp_dir = tmpdir.mkdir("tmpdir")
    file_name = "tmp_logger.log"
    file_path = str(tmp_dir.join(file_name))

    # Checking there is no apdl_logger
    if mapdl._apdl_log is not None:
        mapdl._close_apdl_log()

    assert mapdl._apdl_log is None
    assert file_name not in os.listdir()

    # Setting logger
    mapdl.open_apdl_log(file_path, "w")
    assert file_name in os.listdir(tmp_dir)

    # don't allow double logger:
    with pytest.raises(MapdlRuntimeError):
        mapdl.open_apdl_log(file_name, mode="w")

    # Testing
    mapdl.prep7()
    mapdl.com("This is a comment")

    # Testing non-interactive
    with mapdl.non_interactive:
        mapdl.com("This is a non-interactive command")
        mapdl.slashsolu()
        mapdl.prep7()

    file_input = str(tmp_dir.join("input.inp"))
    str_not_in_apdl_logger = "/com, this input should not appear"
    with open(file_input, "w") as fid:
        fid.write(str_not_in_apdl_logger)

    mapdl._apdl_log.flush()
    with open(file_path, "r") as fid:
        log = fid.read()

    assert "APDL" in log
    assert "ansys.mapdl.core" in log
    assert "PyMapdl" in log
    assert "/COM" in log
    assert "This is a comment" in log
    assert "This is a non-interactive command" in log
    assert "/SOLU" in log

    # The input of the ``non_interactive`` should not write to the apdl_logger.
    assert "/INP," not in log
    assert "'input.inp'" not in log
    assert "/OUT,_input_tmp_" not in log
    assert str_not_in_apdl_logger not in log

    # Testing /input, i
    mapdl.input(file_input)
    mapdl._apdl_log.flush()
    with open(file_path, "r") as fid:
        log = fid.read()

    # Testing /input PR #1455
    assert "/INP," in log
    assert "input.inp'" in log
    assert "/OUT,_input_tmp_" in log
    assert str_not_in_apdl_logger not in log

    # Closing
    mapdl._close_apdl_log()
    mapdl.com("This comment should not appear in the logger")

    with open(file_path, "r") as fid:
        log = fid.read()

    assert "This comment should not appear in the logger" not in log
    assert file_name in os.listdir(tmp_dir)


def test_nodes(tmpdir, cleared, mapdl):
    mapdl.n(1, 1, 1, 1)
    mapdl.n(11, 10, 1, 1)
    mapdl.fill(1, 11, 9)

    basename = "tmp.nodes"
    target_dir = tmpdir.mkdir("tmpdir")
    filename = str(target_dir.join(basename))
    if mapdl._local:
        mapdl.nwrite(filename)
    else:
        mapdl.nwrite(basename)
        mapdl.download(basename, target_dir=str(target_dir))

    assert np.allclose(mapdl.mesh.nodes, np.loadtxt(filename)[:, 1:])
    assert mapdl.mesh.n_node == 11
    assert np.allclose(mapdl.mesh.nnum, range(1, 12))

    # test clear mapdl
    mapdl.clear()
    assert not mapdl.mesh.nodes.size
    assert not mapdl.mesh.n_node
    assert not mapdl.mesh.nnum.size


def test_enum(mapdl, make_block):
    assert mapdl.mesh.n_elem
    assert np.allclose(mapdl.mesh.enum, range(1, mapdl.mesh.n_elem + 1))


def test_elements(cleared, mapdl):
    mapdl.et(1, 185)

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

    with mapdl.non_interactive:
        for cell in [cell1, cell2]:
            for x, y, z in cell:
                mapdl.n(x=x, y=y, z=z)

    mapdl.e(*list(range(1, 9)))
    mapdl.e(*list(range(9, 17)))
    expected = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8],
            [1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 9, 10, 11, 12, 13, 14, 15, 16],
        ]
    )

    assert np.allclose(np.array(mapdl.mesh.elem), expected)


@pytest.mark.parametrize(
    "parm",
    (
        "my_string",
        1,
        10.0,
        [1, 2, 3],
        [[1, 2, 3], [1, 2, 3]],
        np.random.random((2000)),  # fails on gRPC at 100000
        np.random.random((10, 3)),
        np.random.random((10, 3, 3)),
    ),
)
def test_set_get_parameters(mapdl, parm):
    parm_name = pymapdl.misc.random_string(20)
    mapdl.parameters[parm_name] = parm

    if isinstance(parm, str):
        assert mapdl.parameters[parm_name] == parm
    elif isinstance(parm, (int, float)):
        assert np.allclose(mapdl.parameters[parm_name], parm)
    else:
        # For the cases where shape is (X,) # Empty second dimension
        parm = np.array(parm)
        if parm.ndim == 1:
            parm = parm.reshape((parm.shape[0], 1))
        assert np.allclose(mapdl.parameters[parm_name], parm)


def test_set_parameters_arr_to_scalar(mapdl, cleared):
    mapdl.parameters["PARM"] = np.arange(10)
    mapdl.parameters["PARM"] = 2


def test_set_parameters_string_spaces(mapdl):
    with pytest.raises(ValueError):
        mapdl.parameters["PARM"] = "string with spaces"


def test_set_parameters_too_long(mapdl):
    with pytest.raises(
        ValueError, match="Length of ``name`` must be 32 characters or less"
    ):
        mapdl.parameters["a" * 32] = 2

    with pytest.raises(
        ValueError, match="Length of ``value`` must be 32 characters or less"
    ):
        mapdl.parameters["asdf"] = "a" * 32


def test_builtin_parameters(mapdl, cleared):
    mapdl.prep7()
    assert mapdl.parameters.routine == "PREP7"

    mapdl.units("SI")
    assert mapdl.parameters.units == "SI"

    assert isinstance(mapdl.parameters.revision, float)

    # Platform could be either windows or Linux, without regards to
    # the testing OS.
    plat = mapdl.parameters.platform
    assert "L" in plat or "W" in plat

    mapdl.csys(1)
    assert mapdl.parameters.csys == 1

    mapdl.dsys(1)
    assert mapdl.parameters.dsys == 1

    mapdl.esys(0)
    assert mapdl.parameters.esys == 0
    assert mapdl.parameters.material == 1
    assert mapdl.parameters.section == 1
    assert mapdl.parameters.real == 1


def test_partial_mesh_nnum(mapdl, make_block):
    allsel_nnum_old = mapdl.mesh.nnum
    mapdl.nsel("S", "NODE", vmin=100, vmax=200)
    allsel_nnum_now = mapdl.mesh.nnum_all
    assert np.allclose(allsel_nnum_old, allsel_nnum_now)

    mapdl.allsel()
    assert np.allclose(allsel_nnum_old, mapdl.mesh.nnum)


@requires("pyvista")
def test_partial_mesh_nnum2(mapdl, make_block):
    mapdl.nsel("S", "NODE", vmin=1, vmax=10)
    mapdl.esel("S", "ELEM", vmin=10, vmax=20)
    assert mapdl.mesh._grid.n_cells == 11


def test_cyclic_solve(mapdl, cleared):
    # build the cyclic model
    mapdl.prep7()
    mapdl.shpp("off")
    mapdl.cdread("db", os.path.join(test_files, "sector.cdb"))
    mapdl.prep7()
    time.sleep(1.0)
    mapdl.cyclic()

    # set material properties
    mapdl.mp("NUXY", 1, 0.31)
    mapdl.mp("DENS", 1, 4.1408e-04)
    mapdl.mp("EX", 1, 16900000)
    mapdl.emodif("ALL", "MAT", 1)

    # setup and solve
    mapdl.modal_analysis("LANB", 1, 1, 100000, elcalc=True)
    mapdl.finish()

    # expect 16 result sets (1 mode, 16 blades, 16 modes in mode family)
    mapdl.post1()
    assert mapdl.post_processing.nsets == 16


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
def test_load_table(mapdl, dim_rows, dim_cols):
    my_conv = np.random.rand(dim_rows, dim_cols)
    my_conv[:, 0] = np.arange(dim_rows)  # "time" values

    mapdl.load_table("my_conv", my_conv, "TIME")
    assert np.allclose(mapdl.parameters["my_conv"], my_conv[:, 1:], 1e-7)


def test_load_table_error_ascending_row(mapdl):
    my_conv = np.ones((3, 3))
    my_conv[1, 0] = 4
    with pytest.raises(ValueError, match="requires that the first column is in"):
        mapdl.load_table("my_conv", my_conv)


@pytest.mark.parametrize("dimx", [1, 3, 10])
@pytest.mark.parametrize("dimy", [1, 3, 10])
def test_load_array(mapdl, dimx, dimy):
    my_conv = np.random.rand(dimx, dimy)
    mapdl.load_array("my_conv", my_conv)

    # flatten as MAPDL returns flat arrays when one dimension is 1.
    assert np.allclose(mapdl.parameters["my_conv"], my_conv, rtol=1e-7)


@pytest.mark.parametrize(
    "array",
    [
        np.zeros(
            3,
        ),
        np.zeros((3, 1)),
        np.zeros((3, 3)),
    ],
)
def test_load_array_types(mapdl, array):
    mapdl.load_array("myarr", array)
    assert np.allclose(mapdl.parameters["myarr"], array, rtol=1e-7)


@pytest.mark.parametrize("array", [[1, 3, 10], np.random.randint(1, 20, size=(5,))])
def test_load_array_failure_types(mapdl, array):
    array[0] = array[0] + 1  # This is to avoid having all elements equal #1061
    mapdl.load_array("myarr", array)
    array = np.array(array)
    assert not np.allclose(mapdl.parameters["myarr"], array, rtol=1e-7)
    assert mapdl.parameters["myarr"].shape != array.shape
    assert mapdl.parameters["myarr"].shape[0] == array.shape[0]
    assert (mapdl.parameters["myarr"].ravel() == array.ravel()).all()
    assert mapdl.parameters["myarr"].ndim == array.ndim + 1


@requires("grpc")
def test_lssolve(mapdl, cleared):
    mapdl.mute = True

    mapdl.run("/units,user,0.001,0.001,1,1,0,1,1,1")
    mapdl.prep7()
    mapdl.et(1, 182)
    mapdl.mp("ex", 1, 210e3)
    mapdl.mp("nuxy", 1, 0.33)
    mapdl.mp("dens", 1, 7.81e-06)
    mapdl.k(1, 0, 0)
    mapdl.k(2, 5, 0)
    mapdl.k(3, 5, 1)
    mapdl.k(4, 0, 1)
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 4)
    mapdl.l(4, 1)
    mapdl.al(1, 2, 3, 4)
    mapdl.lsel("s", "", "", 1, 4)
    mapdl.lesize("all", 0.5)
    mapdl.amesh(1)
    mapdl.allsel()
    mapdl.finish()
    mapdl.run("/solu")
    mapdl.antype("static'")
    mapdl.kbc(0)
    mapdl.lsel("s", "", "", 4)
    mapdl.nsll("s", 1)
    mapdl.d("all", "all", 0)
    mapdl.ksel("s", "", "", 3)
    mapdl.nslk("s")
    mapdl.f("all", "fy", 5)
    mapdl.allsel()
    mapdl.lswrite(1)
    mapdl.fdele("all", "all")
    mapdl.ksel("s", "", "", 3)
    mapdl.nslk("s")
    mapdl.f("all", "fy", -5)
    mapdl.allsel()

    lsnum = 2
    mapdl.lswrite(lsnum)
    mapdl.mute = False
    out = mapdl.lssolve(1, lsnum)
    assert f"Load step file number {lsnum}.  Begin solution ..." in out


def test_coriolis(mapdl, cleared):
    """Simply test that we're formatting the input parm for coriolis"""
    # must be v190 or newer
    resp = mapdl.coriolis(True, True, True, True)
    assert "CORIOLIS IN STATIONARY REFERENCE FRAME" in resp
    assert "GYROSCOPIC DAMPING MATRIX WILL BE CALCULATED" in resp
    assert "ROTATING DAMPING MATRIX ACTIVATED" in resp
    assert "PRINT ROTOR MASS SUMMARY ACTIVATED" in resp


def test_title(mapdl, cleared):
    title = "title1"  # the title cannot be longer than 7 chars. Check *get,parm,active,0,title for more info.
    mapdl.title(title)
    assert title == mapdl.get("par", "active", "0", "title")


def test_cdread(mapdl, cleared):
    random_letters = random_string(4)

    mapdl.run(f"PARMTEST='{random_letters}'")
    mapdl.cdwrite("all", "model2", "cdb")

    mapdl.clear()
    mapdl.cdread("db", "model2", "cdb")
    assert random_letters in mapdl.parameters["PARMTEST"]

    # Testing arguments
    mapdl.clear()
    mapdl.cdread(option="db", fname="model2", extension="cdb")
    assert random_letters in mapdl.parameters["PARMTEST"]

    # Testing arguments
    mapdl.clear()
    mapdl.cdread("db", fname="model2", extension="cdb")
    assert random_letters in mapdl.parameters["PARMTEST"]

    # Testing arguments
    mapdl.clear()
    mapdl.cdread("db", "model2", extension="cdb")
    assert random_letters in mapdl.parameters["PARMTEST"]

    with pytest.raises(ValueError):
        mapdl.cdread("all", "model2", "cdb")

    with pytest.raises(ValueError):
        mapdl.cdread("test", "model2", "cdb")


@requires("local")
def test_cdread_different_location(mapdl, cleared, tmpdir):
    random_letters = mapdl.directory.split("/")[0][-3:0]
    dirname = "tt" + random_letters

    curdir = mapdl.directory
    subdir = tmpdir.mkdir(dirname)

    mapdl.run(f"parmtest='{random_letters}'")
    mapdl.cdwrite("all", subdir.join("model2"), "cdb")

    mapdl.clear()
    mapdl.cwd(subdir)
    mapdl.cdread("db", "model2", "cdb")
    mapdl.cwd(curdir)  # Going back

    assert random_letters == mapdl.parameters["parmtest"]


def test_cdread_in_python_directory(mapdl, cleared, tmpdir):
    # Writing db file in python directory.
    # Pyansys should upload it when it detects it is not in the APDL directory.
    fullpath = str(tmpdir.join("model.cdb"))
    with open(fullpath, "w") as fid:
        fid.write(CDB_FILE)

    # check if pymapdl is smart enough to determine if it can access
    # the archive from the current working directory.
    old_cwd = os.getcwd()
    try:
        # We are not checking yet if the file is read correctly, just if the file
        # can be read.
        os.chdir(tmpdir)
        mapdl.cdread(
            "COMB", "model", "cdb"
        )  # 'COMB' is needed since we use the CDB with the strange line endings.
        assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(
            mapdl, tmpdir
        )

        clearing_cdread_cdwrite_tests(mapdl)
        mapdl.cdread("COMB", "model.cdb")
        assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(
            mapdl, tmpdir
        )

        clearing_cdread_cdwrite_tests(mapdl)
        mapdl.cdread("COMB", "model")
        assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(
            mapdl, tmpdir
        )

    finally:
        # always change back to the previous directory
        os.chdir(old_cwd)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = str(tmpdir.join("model.cdb"))
    mapdl.cdread("COMB", fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(
        mapdl, tmpdir
    )

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = str(tmpdir.join("model"))
    mapdl.cdread("COMB", fullpath, "cdb")
    assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(
        mapdl, tmpdir
    )

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = str(tmpdir.join("model"))
    mapdl.cdread("COMB", fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl) and not warns_in_cdread_error_log(
        mapdl, tmpdir
    )


def test_cdread_in_apdl_directory(mapdl, cleared):
    # Writing a db file in apdl directory, using APDL.
    # Using APDL to write the archive as there are be cases where the
    # python code cannot reach the APDL execution directory because it
    # is remote.
    mapdl.run("*SET,T_PAR,'asdf1234'")
    mapdl.run("CDWRITE,'DB','model','cdb'")

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread("db", "model", "cdb")
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread("db", "model.cdb")
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread("db", "model")
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = os.path.join(mapdl.directory, "model.cdb")
    mapdl.cdread("db", fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = os.path.join(mapdl.directory, "model")
    mapdl.cdread("db", fullpath, "cdb")
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    fullpath = os.path.join(mapdl.directory, "model")
    mapdl.cdread("db", fullpath)
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread(option="db", fname="model", ext="cdb")
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread("db", fname="model", ext="cdb")
    assert asserting_cdread_cdwrite_tests(mapdl)

    clearing_cdread_cdwrite_tests(mapdl)
    mapdl.cdread("db", "model", ext="cdb")
    assert asserting_cdread_cdwrite_tests(mapdl)


@pytest.mark.parametrize(
    "each_cmd", ["*END", "*vwrite", "/eof", "cmatrix", "*REpeAT", "lSread"]
)
def test_inval_commands(mapdl, cleared, each_cmd):
    """Test the output of invalid commands"""
    with pytest.raises(MapdlRuntimeError):
        mapdl.run(each_cmd)


def test_inval_commands_silent(mapdl, tmpdir, cleared):
    assert mapdl.run("parm = 'asdf'")  # assert it is not empty
    mapdl.nopr()
    assert mapdl.run("parm = 'asdf'")  # assert it is not empty

    assert not mapdl._run("/nopr")  # setting /nopr and assert it is empty
    assert not mapdl.run("parm = 'asdf'")  # assert it is not empty

    mapdl._run("/gopr")  # getting settings back


@requires("local")
def test_path_without_spaces(mapdl, path_tests):
    old_path = mapdl.directory
    try:
        resp = mapdl.cwd(path_tests.path_without_spaces)
        assert resp is None
    finally:
        mapdl.directory = old_path


@requires("local")
def test_path_with_spaces(mapdl, path_tests):
    old_path = mapdl.directory
    try:
        resp = mapdl.cwd(path_tests.path_with_spaces)
        assert resp is None
    finally:
        mapdl.directory = old_path


@requires("local")
def test_path_with_single_quote(mapdl, path_tests):
    with pytest.raises(MapdlRuntimeError):
        mapdl.cwd(path_tests.path_with_single_quote)


def test_cwd(mapdl, tmpdir):
    old_path = mapdl.directory
    if mapdl._local:
        tempdir_ = tmpdir
    else:
        if mapdl.platform == "linux":
            mapdl.sys("mkdir -p /tmp")
            tempdir_ = "/tmp"
        elif mapdl.platform == "windows":
            tempdir_ = "C:\\Windows\\Temp"
        else:
            raise ValueError("Unknown platform")
    try:
        mapdl.directory = str(tempdir_)
        assert str(mapdl.directory) == str(tempdir_).replace("\\", "/")

        wrong_path = "wrong_path"
        with pytest.raises(IncorrectWorkingDirectory, match="working directory"):
            mapdl.directory = wrong_path

    finally:
        mapdl.cwd(old_path)


@requires("nocicd")
@requires("local")
def test_inquire(mapdl):
    # Testing basic functions (First block: Functions)
    assert "apdl" in mapdl.inquire("", "apdl").lower()

    # **Returning the Value of an Environment Variable to a Parameter**
    env = list(os.environ.keys())[0]
    if os.name == "nt":
        env_value = os.getenv(env).split(";")[0]
    elif os.name == "posix":
        env_value = os.getenv(env).split(":")[0]
    else:
        raise Exception("Not supported OS.")

    env_ = mapdl.inquire("", "ENV", env, 0)
    assert env_ == env_value

    # **Returning the Value of a Title to a Parameter**
    title = "This is the title"
    mapdl.title(title)
    assert title == mapdl.inquire("", "title")

    # **Returning Information About a File to a Parameter**
    jobname = mapdl.inquire("", "jobname")
    assert float(mapdl.inquire("", "exist", jobname + ".lock")) in [0, 1]
    assert float(mapdl.inquire("", "exist", jobname, "lock")) in [0, 1]


def test_ksel(mapdl, cleared):
    mapdl.k(1, 0, 0, 0)
    mapdl.prep7()
    assert "SELECTED" in mapdl.ksel("S", "KP", vmin=1, return_mapdl_output=True)
    assert "SELECTED" in mapdl.ksel("S", "KP", "", 1, return_mapdl_output=True)

    assert 1 in mapdl.ksel("S", "KP", vmin=1)


def test_get_file_path(mapdl, tmpdir):
    fname = "dummy.txt"
    fobject = tmpdir.join(fname)
    fobject.write("Dummy file for testing")

    assert fobject not in mapdl.list_files()
    assert fobject not in os.listdir()

    mapdl._local = True
    fname_ = mapdl._get_file_path(fobject)
    assert fname in fname_
    assert fobject not in mapdl.list_files()
    assert os.path.exists(fname_)

    mapdl._local = False
    fname_ = mapdl._get_file_path(fobject)
    # If we are not in local, now it should have been uploaded
    assert fname in mapdl.list_files()


@pytest.mark.parametrize(
    "option2,option3,option4",
    [
        ("expdata.dat", "", ""),
        ("expdata", ".dat", ""),
        ("expdata", "dat", "DIR"),
    ],
)
def test_tbft(mapdl, tmpdir, option2, option3, option4):
    fname = "expdata.dat"
    dirpath = tmpdir.mkdir("tmpdir")
    fpath = dirpath.join(fname)

    with open(fpath, "w") as fid:
        fid.write(
            """0.819139E-01 0.82788577E+00
        0.166709E+00 0.15437247E+01
        0.253960E+00 0.21686152E+01
        0.343267E+00 0.27201819E+01
        0.434257E+00 0.32129833E+0"""
        )

    if option4 == "DIR":
        option4 = dirpath
    else:
        option2 = os.path.join(dirpath, option2)

    mapdl.prep7(mute=True)
    mat_id = mapdl.get_value("MAT", 0, "NUM", "MAX") + 1
    mapdl.tbft("FADD", mat_id, "HYPER", "MOONEY", "3", mute=True)
    mapdl.tbft("EADD", mat_id, "UNIA", option2, option3, option4, "", "", "", mute=True)

    assert fname in mapdl.list_files()


def test_tbft_not_found(mapdl):
    with pytest.raises(FileNotFoundError):
        mapdl.prep7(mute=True)
        mat_id = mapdl.get_value("MAT", 0, "NUM", "MAX") + 1
        mapdl.tbft("FADD", mat_id, "HYPER", "MOONEY", "3", mute=True)
        mapdl.tbft("EADD", mat_id, "UNIA", "non_existing.file", "", "", mute=True)


def test_rescontrol(mapdl):
    # Making sure we have the maximum number of arguments.
    mapdl.rescontrol("DEFINE", "", "", "", "", "XNNN")  # This is default


def test_get_with_gopr(mapdl):
    """Get should work independently of the /gopr state."""

    mapdl._run("/gopr")
    assert mapdl.wrinqr(1) == 1
    par = mapdl.get("__par__", "ACTIVE", "", "TIME", "WALL")
    assert mapdl.scalar_param("__par__") is not None
    assert par is not None
    assert np.allclose(mapdl.scalar_param("__par__"), par)

    mapdl._run("/nopr")
    assert mapdl.wrinqr(1) == 0
    par = mapdl.get("__par__", "ACTIVE", "", "TIME", "WALL")
    assert mapdl.scalar_param("__par__") is not None
    assert par is not None
    assert np.allclose(mapdl.scalar_param("__par__"), par)

    mapdl._run("/gopr")  # Going back
    assert mapdl.wrinqr(1) == 1


def test_print_com(mapdl, capfd):
    mapdl.print_com = True
    string_ = "Testing print"
    mapdl.com(string_)
    out, err = capfd.readouterr()
    assert string_ in out

    mapdl.print_com = False
    string_ = "Testing disabling print"
    mapdl.com(string_)
    out, err = capfd.readouterr()
    assert string_ not in out

    mapdl.print_com = True
    mapdl.mute = True
    mapdl.com(string_)
    out, err = capfd.readouterr()
    assert string_ not in out

    mapdl.print_com = True
    mapdl.mute = False
    mapdl.com(string_, mute=True)
    out, err = capfd.readouterr()
    assert string_ not in out

    mapdl.print_com = True
    mapdl.mute = True
    mapdl.com(string_, mute=True)
    out, err = capfd.readouterr()
    assert string_ not in out

    mapdl.print_com = True
    mapdl.mute = False
    mapdl.com(string_, mute=False)
    out, err = capfd.readouterr()
    assert string_ in out

    # Not allowed type for mapdl.print_com
    for each in ["asdf", (1, 2), 2, []]:
        with pytest.raises(ValueError):
            mapdl.print_com = each


def test_extra_argument_in_get(mapdl, make_block):
    assert isinstance(
        mapdl.get("_MAXNODENUM_", "node", 0, "NUM", "MAX", "", "", "INTERNAL"),
        float,
    )


@pytest.mark.parametrize("value", [1e-6, 1e-5, 1e-3, None])
def test_seltol(mapdl, value):
    if value:
        assert "SELECT TOLERANCE=" in mapdl.seltol(value)
    else:
        assert "SELECT TOLERANCE SET TO DEFAULT" == mapdl.seltol(value)


def test_mpfunctions(mapdl, cube_solve, capsys):
    mapdl.prep7()

    # check writing to file
    fname = "test"
    ext = "mp1"

    assert f"WRITE OUT MATERIAL PROPERTY LIBRARY TO FILE=" in mapdl.mpwrite(fname, ext)
    assert f"{fname}.{ext}" in mapdl.list_files()

    # asserting downloading
    ext = "mp2"
    assert f"WRITE OUT MATERIAL PROPERTY LIBRARY TO FILE=" in mapdl.mpwrite(
        fname, ext, download_file=True
    )
    assert f"{fname}.{ext}" in mapdl.list_files()
    assert os.path.exists(f"{fname}.{ext}")

    ## Checking reading
    # Uploading a local file
    with open(f"{fname}.{ext}", "r") as fid:
        text = fid.read()

    os.remove(f"{fname}.{ext}")  # remove temp file

    ext = ext + "2"
    fname_ = f"{fname}.{ext}"
    new_nuxy = "MPDATA,NUXY,       1,   1, 0.4000000E+00,"
    nuxy = float(new_nuxy.split(",")[4])
    ex = 0.2100000e12

    with open(fname_, "w") as fid:
        fid.write(text.replace("MPDATA,NUXY,       1,   1, 0.3000000E+00,", new_nuxy))

    # file might be left behind from a previous test
    if fname_ in mapdl.list_files():
        mapdl.slashdelete(fname_)
        assert fname_ not in mapdl.list_files()

    mapdl.clear()
    mapdl.prep7()
    captured = capsys.readouterr()  # To flush it
    output = mapdl.mpread(fname, ext)
    captured = capsys.readouterr()
    if has_dependency("tqdm"):
        # Printing uploading requires tqdm
        assert f"Uploading {fname}.{ext}:" in captured.err

    assert "PROPERTY TEMPERATURE TABLE    NUM. TEMPS=  1" in output
    assert "TEMPERATURE TABLE ERASED." in output
    assert "0.4000000" in output
    # check if materials are read into the db
    assert mapdl.get_value("NUXY", "1", "TEMP", 0) == nuxy
    assert np.allclose(mapdl.get_value("EX", 1, "TEMP", 0), ex)

    # Reading file in remote
    fname_ = f"{fname}.{ext}"
    mapdl.upload(fname_)
    os.remove(fname_)
    assert not os.path.exists(fname_)
    assert f"{fname}.{ext}" in mapdl.list_files()

    mapdl.clear()
    mapdl.prep7()
    output = mapdl.mpread(fname, ext)
    assert "PROPERTY TEMPERATURE TABLE    NUM. TEMPS=  1" in output
    assert "TEMPERATURE TABLE ERASED." in output
    assert "0.4000000" in output
    assert np.allclose(mapdl.get_value("NUXY", "1", "TEMP", 0), nuxy)
    assert np.allclose(mapdl.get_value("EX", 1, "TEMP", 0), ex)

    # Test non-existing file
    with pytest.raises(FileNotFoundError):
        mapdl.mpread(fname="dummy", ext="dummy")

    # Test not implemented error
    with pytest.raises(NotImplementedError):
        mapdl.mpread(fname="dummy", ext="dummy", lib="something")

    # Test suppliying a dir path when in remote
    with pytest.raises(IOError):
        mapdl.mpwrite("/test_dir/test", "mp")


def test_mapdl_str(mapdl):
    out = str(mapdl)
    assert "ansys" in out.lower()
    assert "Product" in out
    assert "MAPDL Version" in out


def test_equal_in_comments_and_title(mapdl):
    mapdl.com("=====")
    mapdl.title("This is = ")
    mapdl.title("This is '=' ")


def test_result_file(mapdl, solved_box):
    assert mapdl.result_file
    assert isinstance(mapdl.result_file, str)


@requires("local")
def test_file_command_local(mapdl, cube_solve, tmpdir):
    rst_file = mapdl.result_file

    # check for raise of non-exising file
    with pytest.raises(FileNotFoundError):
        mapdl.file("potato")

    assert rst_file in mapdl.list_files()
    rst_fpath = os.path.join(mapdl.directory, rst_file)

    # change directory
    old_path = mapdl.directory
    tmp_dir = tmpdir.mkdir("asdf")
    mapdl.directory = str(tmp_dir)
    assert Path(mapdl.directory) == tmp_dir

    mapdl.clear()
    mapdl.post1()
    assert "DATA FILE CHANGED TO FILE" in mapdl.file(rst_fpath)

    mapdl.clear()
    mapdl.post1()
    assert "DATA FILE CHANGED TO FILE" in mapdl.file(
        rst_fpath.replace(".rst", ""), "rst"
    )

    # always revert to preserve state
    mapdl.directory = old_path


def test_file_command_remote(mapdl, cube_solve, tmpdir):
    with pytest.raises(FileNotFoundError):
        mapdl.file("potato")

    mapdl.post1()
    # this file should exist remotely
    rst_file_name = "file.rst"
    assert rst_file_name in mapdl.list_files()

    mapdl.file(rst_file_name)  # checking we can read it.

    with pytest.raises(FileNotFoundError):
        mapdl.file()

    # We are going to download the rst, rename it and
    # tell PyMAPDL to read (it will upload it then)
    tmpdir = str(tmpdir)
    mapdl.download(rst_file_name, tmpdir)
    local_file = os.path.join(tmpdir, rst_file_name)
    new_local_file = os.path.join(tmpdir, "myrst.rst")
    os.rename(local_file, new_local_file)
    assert os.path.exists(new_local_file)
    output = mapdl.file(new_local_file)
    assert "DATA FILE CHANGED TO FILE" in output

    new_local_file2 = os.path.join(tmpdir, "myrst2.rst")
    os.rename(new_local_file, new_local_file2)
    assert os.path.exists(new_local_file2)
    output = mapdl.file(new_local_file2.replace(".rst", ""), "rst")
    assert "DATA FILE CHANGED TO FILE" in output


@requires("linux")
def test_lgwrite(mapdl, cleared, tmpdir):
    filename = str(tmpdir.join("file.txt"))

    # include some muted and unmuted commands to ensure all /OUT and
    # /OUT,anstmp are removed
    mapdl.prep7(mute=True)
    mapdl.k(1, 0, 0, 0, mute=True)
    mapdl.k(2, 2, 0, 0)

    # test the extension
    mapdl.lgwrite(filename[:-4], "txt", kedit="remove", mute=True)

    with open(filename) as fid:
        lines = [line.strip() for line in fid.readlines()]

    assert "K,1,0,0,0" in lines
    for line in lines:
        assert "OUT" not in line

    # must test with no filename
    mapdl.lgwrite()
    assert mapdl.jobname + ".lgw" in mapdl.list_files()


@pytest.mark.parametrize("value", [2, np.array([1, 2, 3]), "asdf"])
def test_parameter_deletion(mapdl, value):
    mapdl.parameters["mypar"] = value
    assert "mypar".upper() in mapdl.starstatus()
    del mapdl.parameters["mypar"]

    assert "mypar" not in mapdl.starstatus()
    assert "mypar" not in mapdl.parameters


def test_get_variable_nsol_esol_wrappers(mapdl, coupled_example):
    mapdl.post26()
    nsol_1 = mapdl.nsol(2, 1, "U", "X")
    assert nsol_1[0] > 0
    assert nsol_1[1] > 0

    variable = mapdl.get_variable(2)
    assert np.allclose(variable, nsol_1)

    variable = mapdl.get_nsol(1, "U", "X")
    assert np.allclose(variable, nsol_1)

    esol_1 = mapdl.esol(3, 1, 1, "S", "Y")
    assert esol_1[0] > 0
    assert esol_1[1] > 0
    variable = mapdl.get_variable(3)
    assert np.allclose(variable, esol_1)

    variable = mapdl.get_esol(1, 1, "S", "Y")
    assert np.allclose(variable, esol_1)


def test_retain_routine(mapdl):
    mapdl.prep7()
    routine = "POST26"
    with mapdl.run_as_routine(routine):
        assert mapdl.parameters.routine == routine
    assert mapdl.parameters.routine == "PREP7"


def test_non_interactive(mapdl, cleared):
    with mapdl.non_interactive:
        mapdl.prep7()
        mapdl.k(1, 1, 1, 1)
        mapdl.k(2, 2, 2, 2)

    assert mapdl.get_value("KP", 0, "count") == 2


def test_ignored_command(mapdl, cleared):
    mapdl.ignore_errors = False
    mapdl.prep7(mute=True)
    mapdl.n(mute=True)
    with pytest.raises(MapdlCommandIgnoredError, match="command is ignored"):
        mapdl.f(1, 1, 1, 1)


def test_lsread(mapdl, cleared):
    mapdl.n(1, mute=True)
    mapdl.n(2, 1, 0, 0, mute=True)
    mapdl.et(1, 188, mute=True)
    mapdl.e(1, 2, mute=True)
    mapdl.slashsolu(mute=True)
    mapdl.f("all", "FX", 1, mute=True)
    mapdl.lswrite(mute=True)
    mapdl.fdele("all", "all", mute=True)
    assert "No nodal" in mapdl.flist()
    mapdl.lsread(mute=True)
    assert "No nodal" not in mapdl.flist()


def test_get_fallback(mapdl, cleared):
    with pytest.raises(ValueError, match="There are no NODES defined"):
        mapdl.get_value("node", 0, "num", "maxd")

    with pytest.raises(ValueError, match="There are no ELEMENTS defined"):
        mapdl.get_value("elem", 0, "num", "maxd")


def test_use_uploading(mapdl, cleared, tmpdir):
    mymacrofile_name = "mymacrofile.mac"
    msg = "My macros is being executed"
    # Checking does not exits in remote
    assert mymacrofile_name not in mapdl.list_files()

    # Creating macro
    mymacrofile = tmpdir.join(mymacrofile_name)
    with open(mymacrofile, "w") as fid:
        fid.write(f"/prep7\n/com, {msg}\n/eof")

    with pytest.raises(ValueError, match="Missing `name` argument"):
        mapdl.use()

    # Uploading from local
    out = mapdl.use(name=mymacrofile)
    assert f"USE MACRO FILE  {mymacrofile_name}" in out
    assert msg in out
    assert mymacrofile_name in mapdl.list_files()

    os.remove(mymacrofile)
    assert mymacrofile not in os.listdir()
    out = mapdl.use(mymacrofile)
    assert f"USE MACRO FILE  {mymacrofile_name}" in out
    assert msg in out
    assert mymacrofile_name in mapdl.list_files()
    mapdl.slashdelete(mymacrofile_name)

    # Raises an error.
    with pytest.raises(MapdlRuntimeError):
        mapdl.use("myinexistentmacro.mac")

    # Raise an error
    with pytest.raises(FileNotFoundError):
        mapdl.use("asdf/myinexistentmacro.mac")


def test_set_list(mapdl, cube_solve):
    mapdl.post1()
    obj = mapdl.set("list")

    assert isinstance(obj, CommandListingOutput)

    assert obj.to_array() is not None
    assert obj.to_array().size != 0

    obj = mapdl.set("list", 1)

    assert not isinstance(obj, CommandListingOutput)


def test_mode(mapdl):
    assert mapdl.connection == "grpc"
    assert mapdl.is_grpc
    assert not mapdl.is_corba
    assert not mapdl.is_console

    mapdl._mode = "corba"  # overwriting underlying parameter
    assert not mapdl.is_grpc
    assert mapdl.is_corba
    assert not mapdl.is_console

    mapdl._mode = "console"  # overwriting underlying parameter
    assert not mapdl.is_grpc
    assert not mapdl.is_corba
    assert mapdl.is_console

    mapdl._mode = "grpc"  # Going back to default


def test_remove_lock_file(mapdl, tmpdir):
    tmpdir_ = tmpdir.mkdir("ansys")
    lock_file = tmpdir_.join("file.lock")
    with open(lock_file, "w") as fid:
        fid.write("test")

    mapdl._remove_lock_file(tmpdir_)
    assert not os.path.exists(lock_file)


def test_is_local(mapdl):
    assert mapdl.is_local == mapdl._local


def test_on_docker(mapdl):
    assert mapdl.on_docker == mapdl._on_docker


def test_deprecation_allow_ignore_warning(mapdl):
    with pytest.warns(DeprecationWarning, match="'allow_ignore' is being deprecated"):
        mapdl.allow_ignore = True


def test_deprecation_allow_ignore_errors_mapping(mapdl):
    mapdl.allow_ignore = True
    assert mapdl.allow_ignore == mapdl.ignore_errors

    mapdl.allow_ignore = False
    assert mapdl.allow_ignore == mapdl.ignore_errors

    mapdl.ignore_errors = True
    assert mapdl.allow_ignore == mapdl.ignore_errors

    mapdl.ignore_errors = False
    assert mapdl.allow_ignore == mapdl.ignore_errors


def test_check_stds(mapdl):
    mapdl._stdout = "everything is going ok"
    mapdl._check_stds()

    mapdl._stdout = "one error"
    with pytest.raises(MapdlConnectionError, match="one error"):
        mapdl._check_stds()

    mapdl._stderr = ""
    mapdl._stdout = None  # resetting
    mapdl._check_stds()

    mapdl._stderr = "my error"
    with pytest.raises(MapdlConnectionError, match="my error"):
        mapdl._check_stds()

    # priority goes to stderr
    mapdl._stdout = "one error"
    mapdl._stderr = "my error"
    with pytest.raises(MapdlConnectionError, match="my error"):
        mapdl._check_stds()


def test_connection_by_channel_failure():
    # Check error reporting during connection
    bad_channel = grpc.insecure_channel("willnotwork")
    with pytest.raises(MapdlConnectionError, match="willnotwork"):
        pymapdl.Mapdl(channel=bad_channel, timeout=1)

    class PassThru(grpc.UnaryUnaryClientInterceptor):
        """GRPC interceptor doing nothing"""

        def intercept_unary_unary(continuation, client_call_details, request):
            return continuation(client_call_details, request)

    bad_channel_with_interceptor = grpc.intercept_channel(
        grpc.insecure_channel("willnotwork"), PassThru()
    )
    with pytest.raises(MapdlConnectionError, match="willnotwork"):
        pymapdl.Mapdl(channel=bad_channel_with_interceptor, timeout=1)


def test_post_mortem_checks_no_process(mapdl):
    # Early exit
    old_process = mapdl._mapdl_process
    old_mode = mapdl._mode

    mapdl._mapdl_process = None
    assert mapdl._post_mortem_checks() is None
    assert mapdl._read_stds() is None

    mapdl._mapdl_process = True
    mapdl._mode = "console"
    assert mapdl._post_mortem_checks() is None

    # No process
    mapdl._mapdl_process = None
    mapdl._mode = "grpc"
    assert mapdl._read_stds() is None

    mapdl._mapdl_process = old_process
    mapdl._mode = old_mode


def test_avoid_non_interactive(mapdl):
    with mapdl.non_interactive:
        mapdl.com("comment A")
        mapdl.com("comment B", avoid_non_interactive=True)
        mapdl.com("comment C")

        stored_commands = mapdl._stored_commands
        assert any(["comment A" in cmd for cmd in stored_commands])
        assert all(["comment B" not in cmd for cmd in stored_commands])
        assert any(["comment C" in cmd for cmd in stored_commands])


def test_get_file_name(mapdl):
    file_ = "asdf/qwert/zxcv.asd"
    assert mapdl._get_file_name(file_) == file_
    assert mapdl._get_file_name(file_, "asdf") == file_ + ".asdf"
    assert mapdl._get_file_name(file_, default_extension="qwer") == file_
    assert (
        mapdl._get_file_name(file_.replace(".asd", ""), default_extension="qwer")
        == file_.replace(".asd", "") + ".qwer"
    )


@requires("local")
def test_cache_pids(mapdl):
    if mapdl.version == 23.2:
        pytest.skip(f"Flaky test in MAPDL 23.2")  # I'm not sure why.

    assert mapdl._pids
    mapdl._cache_pids()  # Recache pids

    for each in mapdl._pids:
        assert "ansys" in "".join(psutil.Process(each).cmdline())


@requires("local")
def test_process_is_alive(mapdl):
    assert mapdl.process_is_alive


def test_force_output(mapdl):
    mapdl.mute = True
    with mapdl.force_output:
        assert mapdl.prep7()
    assert not mapdl.prep7()

    mapdl._run("nopr")
    with mapdl.force_output:
        assert mapdl.prep7()
    assert not mapdl.prep7()

    mapdl.mute = False
    mapdl._run("gopr")
    with mapdl.force_output:
        assert mapdl.prep7()
    assert mapdl.prep7()

    with mapdl.force_output:
        assert mapdl.prep7()
    assert mapdl.prep7()


def test_session_id(mapdl, running_test):
    assert mapdl._session_id is not None

    # already checking version
    mapdl._checking_session_id_ = True
    assert mapdl._check_session_id() is None

    # Not having pymapdl session id
    mapdl._checking_session_id_ = False
    copy_ = mapdl._session_id_
    mapdl._session_id_ = None
    assert mapdl._check_session_id() is None

    # Checking real case
    mapdl._session_id_ = copy_
    with running_test():
        assert isinstance(mapdl._check_session_id(), bool)

    id_ = "123412341234"
    mapdl._session_id_ = id_
    mapdl._run(f"{SESSION_ID_NAME}='{id_}'")
    assert mapdl._check_session_id()

    mapdl._session_id_ = "qwerqwerqwer"
    assert not mapdl._check_session_id()

    mapdl._session_id_ = id_


def test_check_empty_session_id(mapdl):
    # it should run normal
    mapdl._session_id_ = None
    assert mapdl._check_session_id() is None

    assert mapdl.prep7()


@requires("requests")  # Requires 'requests' package
def test_igesin_whitespace(mapdl, cleared, tmpdir):
    bracket_file = pymapdl.examples.download_bracket()
    assert os.path.isfile(bracket_file)

    # moving to another location
    tmpdir_ = tmpdir.mkdir("directory with white spaces")
    fname = os.path.basename(bracket_file)
    dest = os.path.join(tmpdir_, fname)
    shutil.copy(bracket_file, dest)

    # Reading file
    mapdl.aux15()
    out = mapdl.igesin(dest)
    n_ent = re.findall(r"TOTAL NUMBER OF ENTITIES \s*=\s*(\d*)", out)
    assert int(n_ent[0]) > 0


@requires("local")
@requires("nostudent")
def test_save_on_exit(mapdl, cleared):
    mapdl2 = launch_mapdl(
        license_server_check=False, additional_switches=QUICK_LAUNCH_SWITCHES
    )
    mapdl2.parameters["my_par"] = "initial_value"

    db_name = mapdl2.jobname + ".db"
    db_dir = mapdl2.directory
    db_path = os.path.join(db_dir, db_name)

    mapdl2.save(db_name)
    assert os.path.exists(db_path)

    mapdl2.parameters["my_par"] = "final_value"
    mapdl2.exit()

    mapdl2 = launch_mapdl(
        license_server_check=False, additional_switches=QUICK_LAUNCH_SWITCHES
    )
    mapdl2.resume(db_path)
    if mapdl.version >= 24.1:
        assert mapdl2.parameters["my_par"] == "initial_value"
    else:
        # This fails in earlier versions of MAPDL
        assert mapdl2.parameters["my_par"] != "initial_value"
        assert mapdl2.parameters["my_par"] == "final_value"

    mapdl2.parameters["my_par"] = "new_initial_value"
    db_name = mapdl2.jobname + ".db"  # reupdating db path
    db_dir = mapdl2.directory
    db_path = os.path.join(db_dir, db_name)
    mapdl2.exit(save=True)

    mapdl2 = launch_mapdl(
        license_server_check=False, additional_switches=QUICK_LAUNCH_SWITCHES
    )
    mapdl2.resume(db_path)
    assert mapdl2.parameters["my_par"] == "new_initial_value"
    mapdl2.exit()


def test_input_strings_inside_non_interactive(mapdl, cleared):
    cmd = """/com General Kenobi. You are a bold one.  Kill him!\n/prep7"""
    with mapdl.non_interactive:
        mapdl.com("Hello there")
        mapdl.input_strings(cmd)
        mapdl.com("Back away! I will deal with this Jedi slime myself.")

    assert "Hello there" in mapdl._response
    assert "PREP7" in mapdl._response
    assert "General Kenobi. You are a bold one.  Kill him!" in mapdl._response
    assert "Back away! I will deal with this Jedi slime myself." in mapdl._response


def test_input_inside_non_interactive(mapdl, cleared):
    cmd = """/com General Kenobi. You are a bold one.  Kill him!\n/prep7"""
    with open("myinput.inp", "w") as fid:
        fid.write(cmd)

    with mapdl.non_interactive:
        mapdl.com("Hello there")
        mapdl.input("myinput.inp")
        mapdl.com("Back away! I will deal with this Jedi slime myself.")

    assert "Hello there" in mapdl._response
    assert "PREP7" in mapdl._response
    assert "General Kenobi. You are a bold one.  Kill him!" in mapdl._response
    assert "Back away! I will deal with this Jedi slime myself." in mapdl._response

    os.remove("myinput.inp")


def test_rlblock_rlblock_num(mapdl):
    def num_():
        return np.round(np.random.random(), 4)

    comparison = {
        1: [num_() for _ in range(18)],
        2: [num_() for _ in range(18)],
        4: [num_() for _ in range(18)],
    }

    mapdl.prep7()
    for i in comparison.keys():
        mapdl.r(i, *comparison[i][0:6])
        mapdl.rmore(*comparison[i][6:12])
        mapdl.rmore(*comparison[i][12:18])

    rlblock = mapdl.mesh.rlblock

    for i in [1, 2, 4]:
        for j in range(18):
            assert comparison[i][j] == rlblock[i][j]

    assert [1, 2, 4] == mapdl.mesh.rlblock_num


@requires("ansys-mapdl-reader")
def test_download_results_non_local(mapdl, cube_solve):
    assert mapdl.result is not None
    assert isinstance(mapdl.result, Result)


def test__flush_stored(mapdl):
    with mapdl.non_interactive:
        mapdl.com("mycomment")
        mapdl.com("another comment")

        assert any(["mycomment" in each for each in mapdl._stored_commands])
        assert len(mapdl._stored_commands) >= 2

    assert not mapdl._stored_commands


def test_exited(mapdl):
    assert mapdl.exited == mapdl._exited
    assert isinstance(mapdl.exited, bool)


def test_exiting(mapdl):
    assert mapdl.exiting == mapdl._exiting
    assert isinstance(mapdl.exiting, bool)


def test_check_status(mapdl):
    assert mapdl.check_status == "OK"

    mapdl._exited = True
    assert mapdl.exited
    assert mapdl.check_status == "exited"
    mapdl._exited = False

    mapdl._exiting = True
    assert mapdl.exiting
    assert mapdl.check_status == "exiting"
    mapdl._exiting = False


def test_ip(mapdl):
    assert mapdl._ip == mapdl.ip
    assert isinstance(mapdl.ip, str)


def test_port(mapdl):
    assert mapdl.port == mapdl._port
    assert isinstance(mapdl.port, int)


def test_distributed(mapdl):
    if ON_CI and IS_SMP and not ON_LOCAL:
        assert not mapdl._distributed
    else:
        assert mapdl._distributed


def test_non_used_kwargs(mapdl):
    with pytest.warns(UserWarning):
        mapdl.prep7(non_valid_argument=2)

    with pytest.warns(UserWarning):
        mapdl.run("/prep7", True, False, unvalid_argument=2)

    kwarg = {"unvalid_argument": 2}
    with pytest.warns(UserWarning):
        mapdl.run("/prep7", True, None, **kwarg)


def test_non_valid_kwarg(mapdl):
    mapdl.prep7()
    mapdl.blc4(0, 0, 1, 1, 1)

    with pytest.warns(UserWarning):
        mapdl.cdwrite(options="DB", fname="test1", ext="cdb")


def test_check_parameter_names(mapdl):
    with pytest.raises(ValueError):
        mapdl.parameters["_dummy"] = 1

    mapdl.check_parameter_names = False
    mapdl.parameters["_dummy"] = 1
    mapdl.check_parameter_names = True  # returning to default


@requires("pyvista")
def test_components_selection_keep_between_plots(mapdl, cube_solve):
    mapdl.cm("mycm", "volu")
    assert "MYCM" in mapdl.cmlist()
    assert "mycm" in mapdl.components

    mapdl.vplot()

    assert "MYCM" in mapdl.cmlist()
    assert "mycm" in mapdl.components


def test_saving_selection_context(mapdl, cube_solve):
    mapdl.allsel()

    for i in range(1, 4):
        mapdl.nsel("s", "", "", i)
        mapdl.cm(f"nod_selection_{i}", "node")

    for i in range(1, 4):
        mapdl.esel("s", "", "", i)
        mapdl.cm(f"elem_selection_{i}", "elem")

    mapdl.cmsel("s", "nod_selection_1")
    assert "nod_selection_1".upper() in mapdl.cmlist()
    assert "nod_selection_1" in mapdl.components

    mapdl.cmsel("a", "elem_selection_1")
    assert "elem_selection_1".upper() in mapdl.cmlist()
    assert "elem_selection_1" in mapdl.components
    assert "nod_selection_1".upper() in mapdl.cmlist()
    assert "nod_selection_1" in mapdl.components

    with mapdl.save_selection:
        mapdl.cmsel("a", "nod_selection_2")
        assert "nod_selection_2".upper() in mapdl.cmlist()
        assert "nod_selection_2" in mapdl.components

        mapdl.cmsel("a", "elem_selection_2")
        assert "nod_selection_2".upper() in mapdl.cmlist()
        assert "nod_selection_2" in mapdl.components
        assert "elem_selection_2".upper() in mapdl.cmlist()
        assert "elem_selection_2" in mapdl.components

        assert "elem_selection_1".upper() in mapdl.cmlist()
        assert "elem_selection_1" in mapdl.components
        assert "nod_selection_1".upper() in mapdl.cmlist()
        assert "nod_selection_1" in mapdl.components

        mapdl.nsel("s", "", "", 4)
        mapdl.cm("nod_selection_4", "node")

        with mapdl.save_selection:
            mapdl.cmsel("s", "nod_selection_3")
            assert "nod_selection_3".upper() in mapdl.cmlist()
            assert "nod_selection_3" in mapdl.components

            mapdl.cmsel("a", "elem_selection_3")
            assert "elem_selection_3".upper() in mapdl.cmlist()
            assert "elem_selection_3" in mapdl.components
            assert "nod_selection_3".upper() in mapdl.cmlist()
            assert "nod_selection_3" in mapdl.components

            # Erased because the previous cmsel("s")
            assert "nod_selection_4".upper() not in mapdl.cmlist()
            assert "nod_selection_4" not in mapdl.components

            assert "nod_selection_2".upper() not in mapdl.cmlist()
            assert "nod_selection_2" not in mapdl.components
            assert "elem_selection_2".upper() not in mapdl.cmlist()
            assert "elem_selection_2" not in mapdl.components

            assert "elem_selection_1".upper() not in mapdl.cmlist()
            assert "elem_selection_1" not in mapdl.components
            assert "nod_selection_1".upper() not in mapdl.cmlist()
            assert "nod_selection_1" not in mapdl.components

        # Checking correctly exiting contexts
        assert "nod_selection_2".upper() in mapdl.cmlist()
        assert "nod_selection_2" in mapdl.components
        assert "elem_selection_2".upper() in mapdl.cmlist()
        assert "elem_selection_2" in mapdl.components

        assert "elem_selection_3".upper() not in mapdl.cmlist()
        assert "elem_selection_3" not in mapdl.components
        assert "nod_selection_3".upper() not in mapdl.cmlist()
        assert "nod_selection_3" not in mapdl.components

        assert "nod_selection_4".upper() in mapdl.cmlist()
        assert "nod_selection_4" in mapdl.components

    assert "elem_selection_1".upper() in mapdl.cmlist()
    assert "elem_selection_1" in mapdl.components
    assert "nod_selection_1".upper() in mapdl.cmlist()
    assert "nod_selection_1" in mapdl.components

    assert "nod_selection_2".upper() not in mapdl.cmlist()
    assert "nod_selection_2" not in mapdl.components
    assert "nod_selection_2".upper() not in mapdl.cmlist()
    assert "nod_selection_2" not in mapdl.components

    assert "elem_selection_3".upper() not in mapdl.cmlist()
    assert "elem_selection_3" not in mapdl.components
    assert "nod_selection_3".upper() not in mapdl.cmlist()
    assert "nod_selection_3" not in mapdl.components

    assert "nod_selection_4".upper() not in mapdl.cmlist()
    assert "nod_selection_4" not in mapdl.components


def test_inquire_invalid(mapdl):
    with pytest.raises(ValueError, match="Arguments of this method have changed"):
        mapdl.inquire("directory")

    with pytest.raises(ValueError, match="The arguments "):
        mapdl.inquire("dummy", "hi")


def test_inquire_default(mapdl):
    mapdl.title = "heeeelloo"
    assert mapdl.directory == mapdl.inquire()


def test_vwrite_error(mapdl):
    with pytest.raises(MapdlRuntimeError):
        mapdl.vwrite("adf")


def test_vwrite(mapdl):
    with mapdl.non_interactive:
        mapdl.run("/out,test_vwrite.txt")
        mapdl.vwrite("'hello'")
        mapdl.run("(1X, A8)")
        mapdl.run("/out")

    mapdl.download("test_vwrite.txt")

    with open("test_vwrite.txt", "r") as fid:
        content = fid.read()

    assert "hello" == content.strip()
    os.remove("test_vwrite.txt")


def test_get_array_non_interactive(mapdl, solved_box):
    mapdl.allsel()
    with pytest.raises(MapdlRuntimeError):
        with mapdl.non_interactive:
            mapdl.get_array("asdf", "2")


def test_default_file_type_for_plots(mapdl):
    assert mapdl.default_file_type_for_plots

    with pytest.raises(ValueError):
        mapdl.default_file_type_for_plots = "dummy"

    mapdl.default_file_type_for_plots = "PNG"


@requires("matplotlib")
def test_use_vtk(mapdl):
    assert isinstance(mapdl.use_vtk, bool)

    prev = mapdl.use_vtk
    mapdl.use_vtk = False
    mapdl.eplot()

    mapdl.use_vtk = prev


@requires("local")
def test_remove_temp_dir_on_exit(mapdl, tmpdir):
    path = os.path.join(tempfile.gettempdir(), "ansys_" + random_string())
    os.makedirs(path)
    filename = os.path.join(path, "file.txt")
    with open(filename, "w") as f:
        f.write("Hello World")
    assert os.path.exists(filename)

    prev = mapdl.remove_temp_dir_on_exit
    mapdl.remove_temp_dir_on_exit = True
    mapdl._local = True  # Sanity check
    mapdl._remove_temp_dir_on_exit(path)
    mapdl.remove_temp_dir_on_exit = prev

    assert os.path.exists(filename) is False
    assert os.path.exists(path) is False


def test_sys(mapdl):
    assert "hi" in mapdl.sys("echo 'hi'")
