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

import inspect
from unittest.mock import patch

import numpy as np
import pytest

from ansys.mapdl.core.commands import (
    CMD_BC_LISTING,
    CMD_LISTING,
    BoundaryConditionsListingOutput,
    CommandListingOutput,
    CommandOutput,
    Commands,
    StringWithLiteralRepr,
)
from ansys.mapdl.core.examples.verif_files import vmfiles
from conftest import NullContext, TestClass, has_dependency, requires

if has_dependency("pandas"):
    import pandas as pd

LIST_OF_INQUIRE_FUNCTIONS = [
    "ndinqr",
    "elmiqr",
    "kpinqr",
    "lsinqr",
    "arinqr",
    "vlinqr",
    "rlinqr",
    "gapiqr",
    "masiqr",
    "ceinqr",
    "cpinqr",
    "csyiqr",
    "etyiqr",
    "foriqr",
    "sectinqr",
    "mpinqr",
    "dget",
    "fget",
    "erinqr",
]

# Generic args
ARGS_INQ_FUNC = {
    "node": 1,
    "key": 0,
    "ielem": 1,
    "knmi": 1,
    "line": 1,
    "anmi": 1,
    "vnmi": 1,
    "nreal": 1,
    "ngap": 1,
    "nce": 1,
    "ncp": 1,
    "ncsy": 1,
    "itype": 1,
    "nsect": 1,
    "mat": 1,
    "iprop": 1,
    "idf": 1,
    "kcmplx": 1,
}


set_list_0 = """*****  INDEX OF DATA SETS ON RESULTS FILE  *****

   SET   TIME/FREQ    LOAD STEP   SUBSTEP  CUMULATIVE
     1 0.20000             1         1         3
     2 0.40000             1         2         5
     3 0.70000             1         3         7
     4  1.0000             1         4         9"""

set_list_1 = """*****  INDEX OF DATA SETS ON RESULTS FILE  *****

   SET   TIME/FREQ    LOAD STEP   SUBSTEP  CUMULATIVE
     1 0.10000E-02         1        10        10
     2 0.20000E-02         2         1        11
     3 0.30000E-02         2         2        12
     4 0.40000E-02         2         3        13
     5 0.50000E-02         2         4        14
     6 0.60000E-02         2         5        15
 """

PRNSOL_OUT = """PRINT F    REACTION SOLUTIONS PER NODE
       1   0.1287512532E+008  0.4266737217E+007
       2  -0.1512012179E+007  0.2247558576E+007
       3  -0.7065315064E+007 -0.4038004530E+007
       4  -0.4297798077E+007 -0.2476291263E+007"""

PRNSOL_OUT_LONG = """PRINT F    REACTION SOLUTIONS PER NODE

 *** ANSYS - ENGINEERING ANALYSIS SYSTEM  RELEASE 2021 R2          21.2     ***
 DISTRIBUTED Ansys Mechanical Enterprise

 00000000  VERSION=LINUX x64     15:56:42  JAN 13, 2022 CP=      0.665





  ***** POST1 TOTAL REACTION SOLUTION LISTING *****

  LOAD STEP=     1  SUBSTEP=     1
   TIME=    1.0000      LOAD CASE=   0

  THE FOLLOWING X,Y,Z SOLUTIONS ARE IN THE GLOBAL COORDINATE SYSTEM

    NODE       FX           FY
       1  0.12875E+008 0.42667E+007
       2 -0.15120E+007 0.22476E+007
       3 -0.70653E+007-0.40380E+007
       4 -0.42978E+007-0.24763E+007

 TOTAL VALUES
 VALUE  -0.37253E-008 0.46566E-009
"""

CMD_DOC_STRING_INJECTOR = CMD_LISTING.copy()
CMD_DOC_STRING_INJECTOR.extend(CMD_BC_LISTING)


@pytest.fixture()
def beam_solve(mapdl, cleared):
    with mapdl.muted:
        mapdl.input(vmfiles["vm10"])

        mapdl.post1()
        mapdl.set(1, 2)


def test_cmd_class():
    output = """This is the output.
This is the second line.
These are numbers 1234567890.
These are symbols !"£$%^^@~+_@~€
This is for the format: {format1}-{format2}-{format3}"""

    cmd = "/INPUT"
    cmd_out = CommandOutput(output, cmd=cmd)

    assert isinstance(cmd_out, (str, CommandOutput))
    assert isinstance(cmd_out[1:], (str, CommandOutput))
    assert isinstance(cmd_out.splitlines(), list)
    assert isinstance(cmd_out.splitlines()[0], (str, CommandOutput))
    assert isinstance(cmd_out.replace("a", "c"), (str, CommandOutput))
    assert isinstance(cmd_out.partition("g"), tuple)
    assert isinstance(cmd_out.split("g"), list)


def test_cmd_class_prnsol_short():
    cmd = "PRRSOL,F"
    out = CommandListingOutput(PRNSOL_OUT, cmd=cmd)

    out_list = out.to_list()
    out_array = out.to_array()

    assert isinstance(out, CommandListingOutput)
    assert isinstance(out_list, list)
    assert out_list
    assert isinstance(out_array, np.ndarray) and out_array.size != 0

    if has_dependency("pandas"):
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty


def test_cmd_class_dlist_vm(mapdl, cleared):
    # Run only the first 100 lines of VM223
    DLIST_RESULT = [
        ["1", "UX", "10.0000000", "0.00000000"],
        ["3", "TEMP", "10.0000000", "0.00000000"],
        ["5", "UZ", "0.00000000", "0.00000000"],
        ["10", "UX", "0.00000000", "0.00000000"],
        ["10", "UY", "0.00000000", "0.00000000"],
        ["10", "UZ", "0.00000000", "0.00000000"],
        ["10", "TEMP", "0.00000000", "0.00000000"],
        ["10", "VOLT", "0.00000000", "0.00000000"],
        ["11", "TEMP", "20.0000000", "0.00000000"],
    ]
    mapdl.allsel()
    mapdl.prep7()
    mapdl.et(1, "SOLID227", 111)
    mapdl.block(0, 10, 0, 20, 0, 30)
    mapdl.esize(10)
    mapdl.vmesh("ALL")

    mapdl.d(1, "UX", 10)
    mapdl.d(3, "TEMP", 10)
    mapdl.d(5, "UZ", 0)

    mapdl.d(10, "ALL", 0)
    mapdl.d(11, "TEMP", 20)
    mapdl.d(11, "VOLT", 20)

    mapdl.allsel("all")
    out = mapdl.dlist()
    out_list = out.to_list()

    def are_the_same_result(a, b):
        for el1, el2 in zip(a, b):
            for el11, el22 in zip(el1, el2):
                assert el11 == el22
        return True

    assert isinstance(out, BoundaryConditionsListingOutput)
    assert isinstance(out_list, list)
    assert out_list
    assert are_the_same_result(out_list, DLIST_RESULT)


@pytest.mark.parametrize("func", LIST_OF_INQUIRE_FUNCTIONS)
def test_inquire_functions(mapdl, cleared, func):
    func_ = getattr(mapdl, func)
    func_args = inspect.getfullargspec(func_).args
    args = [
        ARGS_INQ_FUNC[each_arg] for each_arg in func_args if each_arg not in ["self"]
    ]
    output = func_(*args)
    if "GRPC" in mapdl.name:
        assert isinstance(output, (float, int))
    else:
        assert isinstance(output, str)
        assert "=" in output


@pytest.mark.parametrize("func", ["dlist", "flist"])
def test_bclist(mapdl, beam_solve, func):
    func_ = getattr(mapdl, func)
    out = func_()

    out_list = out.to_list()

    assert isinstance(out, BoundaryConditionsListingOutput)
    assert isinstance(out_list, list) and out_list
    with pytest.raises(ValueError):
        out.to_array()

    if has_dependency("pandas"):
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty


@pytest.mark.parametrize("method", CMD_DOC_STRING_INJECTOR)
def test_docstring_injector(mapdl, cleared, method):
    """Check if the docstring has been injected."""
    for name in dir(mapdl):
        if name[0:4].upper() == method and name in dir(
            Commands
        ):  # avoid matching Mapdl properties which starts with same letters as MAPDL commands.
            func = mapdl.__getattribute__(name)
            # If '__func__' not present (AttributeError) very likely it has not
            # been wrapped.
            docstring = func.__doc__

            assert "Returns" in docstring
            assert "to_list()" in docstring
            assert "to_array()" in docstring
            assert "to_dataframe()" in docstring


def test_string_with_literal():
    base_ = "asdf\nasdf"
    output = StringWithLiteralRepr(base_)
    assert output.__repr__() == output
    assert output.__repr__() == base_
    assert len(output.split()) == 2


@requires("pandas")
@pytest.mark.parametrize("output,last_element", [(set_list_0, 9), (set_list_1, 15)])
def test_magicwords(output, last_element):
    magicwords = ["SET"]
    obj = CommandListingOutput(
        output,
        magicwords=magicwords,
        columns_names=[
            "SET",
            "TIME/FREQ",
            "LOAD STEP",
            "SUBSTEP",
            "CUMULATIVE",
        ],
    )

    assert obj.to_list() is not None
    assert obj.to_array() is not None
    assert obj.to_dataframe() is not None

    arr = obj.to_array()
    assert arr[-1, -1] == last_element


def test_nlist_to_array(mapdl, beam_solve):
    # This kinternal include the internal points, so it matches the
    # number of nodes with midside nodes.
    nlist = mapdl.nlist(kinternal="internal")
    assert isinstance(nlist.to_list(), list)
    assert isinstance(nlist.to_array(), np.ndarray)

    # above asserts should be removed once fixed the midside issue.
    assert len(nlist.to_list()) == len(mapdl.mesh.nodes)
    assert len(nlist.to_array()) == len(mapdl.mesh.nodes)
    assert np.allclose(nlist.to_array()[:, 1:4], mapdl.mesh.nodes)


def test_cmlist(mapdl, cleared):
    # setup the full file
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 186)
    mapdl.esize(0.5)
    mapdl.vmesh("all")

    mapdl.cm("myComp", "node")
    mapdl.cm("_myComp", "node")
    mapdl.cm("_myComp_", "node")

    cmlist = mapdl.cmlist()
    assert "MYCOMP" in cmlist

    cmlist_all = mapdl.cmlist("all")
    assert "_MYCOMP_" in cmlist_all
    assert "_MYCOMP" in cmlist_all
    assert "MYCOMP" in cmlist_all

    assert ["MYCOMP"] == mapdl.cmlist().to_list()

    assert "_MYCOMP_" in cmlist_all.to_list()
    assert "_MYCOMP" in cmlist_all.to_list()
    assert "MYCOMP" in cmlist_all.to_list()

    assert len(cmlist_all.to_array()) == len(cmlist_all.to_list())
    for each_ in cmlist_all.to_list():
        assert each_ in cmlist_all


def solid_FE_model(mapdl):
    # Define keypoints, lines and area
    # --------------------
    mapdl.k(1, 0, 0)
    mapdl.k(2, 1, 0)
    mapdl.k(3, 1, 1)
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 1)
    mapdl.a(1, 2, 3)

    # Define a material
    # --------------------
    mapdl.mp("EX", 1, 30e6)
    mapdl.mp("NUXY", 1, 0.25)  # Poisson's Ratio

    # Define section
    # --------------------
    mapdl.et(1, "PLANE183")
    mapdl.keyopt(1, 1, 0)
    mapdl.keyopt(1, 3, 3)
    mapdl.keyopt(1, 6, 0)
    mapdl.r(1, 0.01)


class Test_bc_cmdlist_solid(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def solid_model(mapdl):
        solid_FE_model(mapdl)

    @requires("pandas")
    def test_dklist(self, mapdl, solid_model):

        df_dk = pd.DataFrame(
            {
                "KEYPOINT": [1],
                "LABEL": ["UX"],
                "REAL": [0.0],
                "IMAG": [0.0],
                "EXP KEY": ["0"],
            }
        )
        mapdl.dk(1, "UX", 0)

        dklist_result = mapdl.dklist().to_dataframe()

        assert not dklist_result.empty
        assert dklist_result.compare(df_dk).empty

    @requires("pandas")
    def test_dllist(self, mapdl, solid_model):

        df_dl = pd.DataFrame(
            {
                "LINE": [2, 2],
                "LABEL": ["UX", "UY"],
                "REAL": [0.0, 0.0],
                "IMAG": [0.0, 0.0],
                "NAREA": ["0", "0"],
            }
        )

        mapdl.dl(2, 1, "ALL", 0)

        dllist_result = mapdl.dllist().to_dataframe()

        assert not dllist_result.empty
        assert dllist_result.compare(df_dl).empty

    @requires("pandas")
    def test_dalist(self, mapdl, solid_model):

        df_da = pd.DataFrame(
            {
                "AREA": [1],
                "LABEL": ["UZ"],
                "REAL": [0.0],
                "IMAG": [0.0],
            }
        )

        mapdl.da(1, "UZ", 0)

        dalist_result = mapdl.dalist().to_dataframe()

        assert not dalist_result.empty
        assert dalist_result.compare(df_da).empty

    @requires("pandas")
    def test_fklist(self, mapdl, solid_model):

        df_fk = pd.DataFrame(
            {
                "KEYPOINT": [2, 3],
                "LABEL": ["FY", "FY"],
                "REAL": [200.0, 100.0],
                "IMAG": [0.0, 0.0],
            }
        )

        mapdl.fk(2, "FY", 200)
        mapdl.fk(3, "FY", 100)

        fklist_result = mapdl.fklist().to_dataframe()

        assert not fklist_result.empty
        assert fklist_result.compare(df_fk).empty

    @requires("pandas")
    def test_sfllist(self, mapdl, solid_model):

        df_sfl = pd.DataFrame(
            {
                "LINE": [2, 3],
                "LABEL": ["PRES", "PRES"],
                "VALI": [50.0, 50.0],
                "VALJ": [500.0, 500.0],
            }
        )

        mapdl.sfl(2, "PRES", 50, 500)
        mapdl.sfl(3, "PRES", 50, 500)

        sfllist_result = mapdl.sfllist().to_dataframe()

        assert not sfllist_result.empty
        assert sfllist_result.compare(df_sfl).empty

    @requires("pandas")
    def test_bfklist(self, mapdl, solid_model):

        df_bfk = pd.DataFrame(
            {
                "KEYPOINT": [2],
                "LABEL": ["TEMP"],
                "VALUE": [10.0],
            }
        )

        mapdl.bfk(2, "TEMP", 10)

        bfklist_result = mapdl.bfklist().to_dataframe()

        assert not bfklist_result.empty
        assert bfklist_result.compare(df_bfk).empty

    @requires("pandas")
    def test_bfllist(self, mapdl, solid_model):

        df_bfl = pd.DataFrame(
            {
                "LINE": [3],
                "LABEL": ["TEMP"],
                "VALUE": [15.0],
            }
        )

        mapdl.bfl(3, "TEMP", 15)

        bfllist_result = mapdl.bfllist().to_dataframe()

        assert not bfllist_result.empty
        assert bfllist_result.compare(df_bfl).empty

    @requires("pandas")
    def test_bfalist(self, mapdl, solid_model):

        df_bfa = pd.DataFrame(
            {
                "AREA": [1],
                "LABEL": ["TEMP"],
                "VALUE": [20.0],
            }
        )

        mapdl.bfa(1, "TEMP", 20)

        bfalist_result = mapdl.bfalist().to_dataframe()

        assert not bfalist_result.empty
        assert bfalist_result.compare(df_bfa).empty


class Test_bc_cmdlist_model(TestClass):

    @pytest.fixture(scope="class")
    def fe_model(self, mapdl):
        solid_FE_model(mapdl)

        mapdl.esize(0.02)
        mapdl.mshape(0, "2D")
        mapdl.mshkey(0)
        mapdl.amesh(1, 1, 1)

    @requires("pandas")
    def test_dlist(self, mapdl, fe_model):

        df_d = pd.DataFrame(
            {
                "NODE": [2, 2],
                "LABEL": ["UX", "UY"],
                "REAL": [0.0, 0.0],
                "IMAG": [0.0, 0.0],
            }
        )

        mapdl.d(2, "UX", 0)
        mapdl.d(2, "UY", 0)

        dlist_result = mapdl.dlist().to_dataframe()

        assert not dlist_result.empty
        assert dlist_result.compare(df_d).empty

    @requires("pandas")
    def test_flist(self, mapdl, fe_model):

        df_f = pd.DataFrame(
            {
                "NODE": [4, 4],
                "LABEL": ["FX", "FY"],
                "REAL": [10.0, 20.0],
                "IMAG": [0.0, 0.0],
            }
        )

        mapdl.f(4, "FX", 10)
        mapdl.f(4, "FY", 20)

        flist_result = mapdl.flist().to_dataframe()

        assert not flist_result.empty
        assert flist_result.compare(df_f).empty


class Test_MAPDL_commands(TestClass):
    SKIP = [
        "aplot",
        "cfopen",
        "cmatrix",
        "create",
        "end",
        "eplot",
        "geometry",
        "input",
        "kplot",
        "lgwrite",
        "lplot",
        "lsread",
        "mpread",
        "mpwrite",
        "mwrite",
        "nplot",
        "sys",
        "vplot",
        "vwrite",
    ]

    RAISE_WARNINGS = ["eshape"]
    RAISE_EXCEPTIONS = []

    @staticmethod
    def fake_wrap(*args, **kwags):
        return args[0]

    MAPDL_cmds = [each for each in dir(Commands) if not each.startswith("_")]

    @pytest.mark.parametrize("cmd", MAPDL_cmds)
    @patch("ansys.mapdl.core.mapdl_grpc.MapdlGrpc._send_command", fake_wrap)
    # Skip post processing the plot in PLESOL commands like.
    @patch("ansys.mapdl.core.mapdl_core.PLOT_COMMANDS", [])
    # skip retrieving value
    @patch("ansys.mapdl.core.mapdl_grpc.MapdlGrpc.scalar_param", fake_wrap)
    # Skip output the entity id after geometry manipulation
    @patch("ansys.mapdl.core._commands.parse.parse_a", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_e", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_et", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_k", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_knode", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_kdist", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_kl", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_kpoint", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_line_no", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_line_nos", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_n", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_ndist", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_output_areas", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_output_volume_area", fake_wrap)
    @patch("ansys.mapdl.core._commands.parse.parse_v", fake_wrap)
    def test_command(self, mapdl, cmd):
        func = getattr(mapdl, cmd)

        # Avoid wraps
        while hasattr(func, "__wrapped__"):
            func = func.__wrapped__

        if cmd in self.SKIP:
            pytest.skip("This function is overwritten in a subclass.")

        parm = inspect.signature(func).parameters
        assert "kwargs" in parm, "'kwargs' argument is missing in function signature."

        args = [f"arg{i}" for i in range(len(parm) - 1)]  # 3 = self, cmd, kwargs

        if cmd in self.RAISE_WARNINGS:
            context = pytest.warns(UserWarning)
        elif cmd in self.RAISE_EXCEPTIONS:
            context = pytest.raises(Exception)
        else:
            context = NullContext()

        with context:
            if list(parm)[0].lower() == "self":
                args = args[:-1]
                post = func(mapdl, *args)
            else:
                post = func(*args)

        for arg in args:
            assert arg in post

        # assert ",".join(args) in post.replace(",,", ",").replace(" ", "")
        cmd_ = cmd.upper()
        if cmd_.startswith("SLASH"):
            cmd_ = cmd_.replace("SLASH_", "/").replace("SLASH", "/")

        if cmd_.startswith("STAR"):
            cmd_ = cmd_.replace("STAR", "*")

        assert cmd_ in post.upper()

        # Restoring defaults
        if "show" in cmd:
            mapdl.show("PNG")


class Test_output_listing(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def plastic_solve_output(mapdl):
        with mapdl.muted:
            mapdl.input(vmfiles["vm273"])

            mapdl.post1()
            mapdl.set(1, 2)

    @staticmethod
    @pytest.mark.parametrize(
        "func,args",
        [("prnsol", ("U", "X")), ("presol", ("S", "X")), ("presol", ("S", "ALL"))],
    )
    def test_output_listing(mapdl, plastic_solve_output, func, args):
        mapdl.post1()
        func_ = getattr(mapdl, func)
        out = func_(*args)

        out_list = out.to_list()
        out_array = out.to_array()

        assert isinstance(out, CommandListingOutput)
        assert isinstance(out_list, list) and out_list
        assert isinstance(out_array, np.ndarray) and out_array.size != 0

        if has_dependency("pandas"):
            out_df = out.to_dataframe()
            assert isinstance(out_df, pd.DataFrame) and not out_df.empty
