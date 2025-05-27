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
import re

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


class Test_xpl:
    full_file = None

    def create_cube(self, mapdl):
        from conftest import clear

        # Delete files
        self.full_file = mapdl.jobname + ".full"

        if "full.file" in mapdl.list_files():
            mapdl.slashdelete("full.file")

        if mapdl.result_file in mapdl.list_files():
            mapdl.slashdelete(mapdl.result_file)

        clear(mapdl)

        # Delete files
        self.full_file = mapdl.jobname + ".full"

        if "full.file" in mapdl.list_files():
            mapdl.slashdelete("full.file")

        if mapdl.result_file in mapdl.list_files():
            mapdl.slashdelete(mapdl.result_file)

        # Delete files
        if "cube_solve_xpl" in mapdl.list_files():
            mapdl.slashdelete("cube_solve_xpl.db")

        # set up the full file
        mapdl.clear("NOSTART")
        mapdl.prep7()
        mapdl.block(0, 1, 0, 1, 0, 1)
        mapdl.et(1, 186)

        # Define a material (nominal steel in SI)
        mapdl.mp("EX", 1, 210e9)  # Elastic modulus in Pa (kg/(m*s**2))
        mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
        mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

        mapdl.esize(0.5)
        mapdl.vmesh("all")

        # solve first 10 non-trivial modes
        mapdl.modal_analysis(nmode=10, freqb=1)
        mapdl.save("cube_solve_xpl", "db", slab="all")

    @pytest.fixture(scope="class")
    def cube_solve(self, mapdl):
        self.create_cube(mapdl)

    @pytest.fixture(scope="function")
    def xpl(self, mapdl, cube_solve):
        mapdl.prep7()
        mapdl.resume("cube_solve_xpl", "db")

        xpl = mapdl.xpl
        if not self.full_file and not self.full_file in mapdl.list_files():
            self.create_cube(mapdl)

        xpl.open(self.full_file)

        yield xpl

        if xpl.opened:
            xpl.close()

    def test_close(self, xpl):
        xpl.close()
        with pytest.raises(MapdlCommandIgnoredError):
            xpl.list()

    @staticmethod
    def test_xpl_str(xpl):
        assert re.search(r"file\d*\.full", str(xpl))

    @staticmethod
    @requires("ansys-math-core")
    def test_read_int32(xpl):
        vec = xpl.read("MASS")
        arr = vec.asarray()
        assert arr.size
        assert arr.dtype == np.int32

    @staticmethod
    @requires("ansys-math-core")
    def test_read_double(xpl):
        vec = xpl.read("DIAGK")
        arr = vec.asarray()
        assert arr.size
        assert arr.dtype == np.double

    @staticmethod
    @requires("ansys-math-core")
    def test_read_asarray(xpl):
        vec1 = xpl.read("MASS", asarray=True)
        vec2 = xpl.read("MASS")
        assert np.allclose(vec1, vec2.asarray())

    @staticmethod
    def test_save(xpl):
        xpl.save()
        with pytest.raises(MapdlCommandIgnoredError):
            xpl.list()

    @staticmethod
    def test_copy(mapdl, cleared, xpl):
        filename = "tmpfile.full"
        if filename in mapdl.list_files():
            mapdl.slashdelete(filename)

        xpl.copy(filename)
        assert filename in mapdl.list_files()

    @staticmethod
    def test_list(xpl):
        assert "::FULL::" in xpl.list(1)

    @staticmethod
    def test_help(xpl):
        assert "SAVE" in xpl.help()

    @staticmethod
    def test_step_where(xpl):
        xpl.step("MASS")
        assert "FULL::MASS" in xpl.where()

        with pytest.raises(MapdlRuntimeError):
            xpl.step("notarecord")

    @staticmethod
    def test_info(xpl):
        assert "Record Size" in xpl.info("NGPH")

    @staticmethod
    def test_print(xpl):
        assert "10" in xpl.print("MASS")

    @staticmethod
    def test_json(xpl):
        json_out = xpl.json()
        assert json_out["name"] == "FULL"
        assert "children" in json_out

    @staticmethod
    def test_up(xpl):
        xpl.step("MASS")
        xpl.up()
        assert "Current Location : FULL" in xpl.where()

        xpl.up("TOP")
        assert "Current Location : FULL" in xpl.where()

    @staticmethod
    def test_goto(xpl):
        xpl.goto("MASS")
        assert "Current Location : FULL::MASS" in xpl.where()

    @requires("ansys-math-core")
    @pytest.mark.usefixtures("check_supports_extract")
    def test_extract(self, xpl):
        # expecting fixture to already have a non-result file open
        assert xpl._filename[-3:] != "rst"
        with pytest.raises(MapdlRuntimeError, match="result files"):
            mat = xpl.extract("NSL")

        xpl.open(xpl._mapdl.result_file)

        with pytest.raises(ValueError, match="the only supported recordname is 'NSL'"):
            xpl.extract("NOD")

        mat = xpl.extract("NSL")
        assert mat.shape == (243, 10)

    def test_opened(self, xpl):
        assert xpl.opened
        xpl.close()
        assert not xpl.opened
        xpl.open(self.full_file)
        assert xpl.opened
