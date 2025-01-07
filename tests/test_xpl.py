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

"""Test xpl functionality"""
from ansys.tools.versioning.utils import SemanticVersion
import numpy as np
import pytest

from ansys.mapdl.core.errors import MapdlCommandIgnoredError, MapdlRuntimeError
from conftest import requires

# skip entire module unless HAS_GRPC
pytestmark = requires("grpc")


@pytest.fixture(scope="module")
def check_supports_extract(mapdl):
    # Hack until we can stabilsh
    if mapdl._server_version < SemanticVersion((0, 5, 0)):  # 2022R1
        pytest.skip("command not supported")


@pytest.fixture(scope="function")
def xpl(mapdl, cube_solve):
    xpl = mapdl.xpl
    xpl.open("file.full")
    return xpl


def test_close(xpl):
    xpl.close()
    with pytest.raises(MapdlCommandIgnoredError):
        xpl.list()


def test_xpl_str(xpl):
    assert "file.full" in str(xpl)


@requires("ansys-math-core")
def test_read_int32(xpl):
    vec = xpl.read("MASS")
    arr = vec.asarray()
    assert arr.size
    assert arr.dtype == np.int32


@requires("ansys-math-core")
def test_read_double(xpl):
    vec = xpl.read("DIAGK")
    arr = vec.asarray()
    assert arr.size
    assert arr.dtype == np.double


@requires("ansys-math-core")
def test_read_asarray(xpl):
    vec1 = xpl.read("MASS", asarray=True)
    vec2 = xpl.read("MASS")
    assert np.allclose(vec1, vec2.asarray())


def test_save(xpl):
    xpl.save()
    with pytest.raises(MapdlCommandIgnoredError):
        xpl.list()


def test_copy(mapdl, cleared, xpl):
    filename = "tmpfile.full"
    xpl.copy(filename)
    assert filename in mapdl.list_files()


def test_list(xpl):
    assert "::FULL::" in xpl.list(1)


def test_help(xpl):
    assert "SAVE" in xpl.help()


def test_step_where(xpl):
    xpl.step("MASS")
    assert "FULL::MASS" in xpl.where()

    with pytest.raises(MapdlRuntimeError):
        xpl.step("notarecord")


def test_info(xpl):
    assert "Record Size" in xpl.info("NGPH")


def test_print(xpl):
    assert "10" in xpl.print("MASS")


def test_json(xpl):
    json_out = xpl.json()
    assert json_out["name"] == "FULL"
    assert "children" in json_out


def test_up(xpl):
    xpl.step("MASS")
    xpl.up()
    assert "Current Location : FULL" in xpl.where()

    xpl.up("TOP")
    assert "Current Location : FULL" in xpl.where()


def test_goto(xpl):
    xpl.goto("MASS")
    assert "Current Location : FULL::MASS" in xpl.where()


@requires("ansys-math-core")
@pytest.mark.usefixtures("check_supports_extract")
def test_extract(xpl):
    # expecting fixture to already have a non-result file open
    assert xpl._filename[-3:] != "rst"
    with pytest.raises(MapdlRuntimeError, match="result files"):
        mat = xpl.extract("NSL")

    xpl.open("file.rst")

    with pytest.raises(ValueError, match="the only supported recordname is 'NSL'"):
        xpl.extract("NOD")

    mat = xpl.extract("NSL")
    assert mat.shape == (243, 10)
