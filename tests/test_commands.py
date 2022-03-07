import inspect

import numpy as np
import pytest

from ansys.mapdl.core import examples
from ansys.mapdl.core.commands import (
    CMD_BC_LISTING,
    CMD_LISTING,
    BoundaryConditionsListingOutput,
    CommandListingOutput,
    CommandOutput,
    Commands,
)

try:
    import pandas as pd

    HAS_PANDAS = True

except ModuleNotFoundError:
    HAS_PANDAS = False

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


@pytest.fixture(scope="module")
def plastic_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()
    mapdl.input(examples.verif_files.vmfiles["vm273"])

    mapdl.post1()
    mapdl.set(1, 2)
    mapdl.mute = False


@pytest.fixture(scope="module")
def beam_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()
    mapdl.input(examples.verif_files.vmfiles["vm10"])

    mapdl.post1()
    mapdl.set(1, 2)
    mapdl.mute = False


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

    if HAS_PANDAS:
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty


@pytest.mark.parametrize("func", LIST_OF_INQUIRE_FUNCTIONS)
def test_inquire_functions(mapdl, func):
    func_ = getattr(mapdl, func)
    func_args = inspect.getfullargspec(func_).args
    args = [
        ARGS_INQ_FUNC[each_arg] for each_arg in func_args if each_arg not in ["self"]
    ]
    output = func_(*args)
    if "GRPC" in mapdl._name:
        assert isinstance(output, (float, int))
    else:
        assert isinstance(output, str)
        assert "=" in output


@pytest.mark.parametrize(
    "func,args",
    [("prnsol", ("U", "X")), ("presol", ("S", "X")), ("presol", ("S", "ALL"))],
)
def test_output_listing(mapdl, plastic_solve, func, args):
    mapdl.post1()
    func_ = getattr(mapdl, func)
    out = func_(*args)

    out_list = out.to_list()
    out_array = out.to_array()

    assert isinstance(out, CommandListingOutput)
    assert isinstance(out_list, list) and out_list
    assert isinstance(out_array, np.ndarray) and out_array.size != 0

    if HAS_PANDAS:
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty


@pytest.mark.parametrize("func", ["dlist", "flist"])
def test_bclist(mapdl, beam_solve, func):
    func_ = getattr(mapdl, func)
    out = func_()

    out_list = out.to_list()

    assert isinstance(out, BoundaryConditionsListingOutput)
    assert isinstance(out_list, list) and out_list
    with pytest.raises(ValueError):
        out.to_array()

    if HAS_PANDAS:
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty


@pytest.mark.parametrize("method", CMD_DOC_STRING_INJECTOR)
def test_docstring_injector(mapdl, method):
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
            assert "``str.to_list()``" in docstring
            assert "``str.to_array()``" in docstring
            assert "``str.to_dataframe()``" in docstring
