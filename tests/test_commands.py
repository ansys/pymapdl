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
    StringWithLiteralRepr,
)
from ansys.mapdl.core.examples import verif_files

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

DLIST_RESULT = [
    ["1", "UX", "0.00000000", "0.00000000"],
    ["1", "UY", "0.00000000", "0.00000000"],
    ["1", "UZ", "0.00000000", "0.00000000"],
    ["1", "TEMP", "300.000000", "0.00000000"],
    ["1", "VOLT", "15.0000000", "0.00000000"],
    ["2", "UX", "0.00000000", "0.00000000"],
    ["2", "UY", "0.00000000", "0.00000000"],
    ["2", "UZ", "0.00000000", "0.00000000"],
    ["2", "TEMP", "300.000000", "0.00000000"],
    ["3", "UX", "0.00000000", "0.00000000"],
    ["3", "UY", "0.00000000", "0.00000000"],
    ["3", "UZ", "0.00000000", "0.00000000"],
    ["3", "TEMP", "300.000000", "0.00000000"],
    ["4", "UX", "0.00000000", "0.00000000"],
    ["4", "UY", "0.00000000", "0.00000000"],
    ["4", "UZ", "0.00000000", "0.00000000"],
    ["4", "TEMP", "300.000000", "0.00000000"],
    ["5", "UX", "0.00000000", "0.00000000"],
    ["5", "UY", "0.00000000", "0.00000000"],
    ["5", "UZ", "0.00000000", "0.00000000"],
    ["5", "TEMP", "300.000000", "0.00000000"],
    ["6", "UX", "0.00000000", "0.00000000"],
    ["6", "UY", "0.00000000", "0.00000000"],
    ["6", "UZ", "0.00000000", "0.00000000"],
    ["6", "TEMP", "300.000000", "0.00000000"],
    ["7", "UX", "0.00000000", "0.00000000"],
    ["7", "UY", "0.00000000", "0.00000000"],
    ["7", "UZ", "0.00000000", "0.00000000"],
    ["7", "TEMP", "300.000000", "0.00000000"],
    ["8", "UX", "0.00000000", "0.00000000"],
    ["8", "UY", "0.00000000", "0.00000000"],
    ["8", "UZ", "0.00000000", "0.00000000"],
    ["8", "TEMP", "300.000000", "0.00000000"],
    ["9", "UX", "0.00000000", "0.00000000"],
    ["9", "UY", "0.00000000", "0.00000000"],
    ["9", "UZ", "0.00000000", "0.00000000"],
    ["9", "TEMP", "300.000000", "0.00000000"],
    ["10", "UX", "0.00000000", "0.00000000"],
    ["10", "UY", "0.00000000", "0.00000000"],
    ["10", "UZ", "0.00000000", "0.00000000"],
    ["10", "TEMP", "300.000000", "0.00000000"],
    ["11", "UX", "0.00000000", "0.00000000"],
    ["11", "UY", "0.00000000", "0.00000000"],
    ["11", "UZ", "0.00000000", "0.00000000"],
    ["11", "TEMP", "300.000000", "0.00000000"],
    ["12", "UX", "0.00000000", "0.00000000"],
    ["12", "UY", "0.00000000", "0.00000000"],
    ["12", "UZ", "0.00000000", "0.00000000"],
    ["12", "TEMP", "300.000000", "0.00000000"],
    ["13", "UX", "0.00000000", "0.00000000"],
    ["13", "UY", "0.00000000", "0.00000000"],
    ["13", "UZ", "0.00000000", "0.00000000"],
    ["13", "TEMP", "300.000000", "0.00000000"],
    ["146", "UX", "0.00000000", "0.00000000"],
    ["146", "UY", "0.00000000", "0.00000000"],
    ["146", "UZ", "0.00000000", "0.00000000"],
    ["146", "TEMP", "300.000000", "0.00000000"],
    ["146", "VOLT", "0.00000000", "0.00000000"],
    ["158", "UX", "0.00000000", "0.00000000"],
    ["158", "UY", "0.00000000", "0.00000000"],
    ["158", "UZ", "0.00000000", "0.00000000"],
    ["158", "TEMP", "300.000000", "0.00000000"],
    ["159", "UX", "0.00000000", "0.00000000"],
    ["159", "UY", "0.00000000", "0.00000000"],
    ["159", "UZ", "0.00000000", "0.00000000"],
    ["159", "TEMP", "300.000000", "0.00000000"],
    ["160", "UX", "0.00000000", "0.00000000"],
    ["160", "UY", "0.00000000", "0.00000000"],
    ["160", "UZ", "0.00000000", "0.00000000"],
    ["160", "TEMP", "300.000000", "0.00000000"],
    ["161", "UX", "0.00000000", "0.00000000"],
    ["161", "UY", "0.00000000", "0.00000000"],
    ["161", "UZ", "0.00000000", "0.00000000"],
    ["161", "TEMP", "300.000000", "0.00000000"],
    ["162", "UX", "0.00000000", "0.00000000"],
    ["162", "UY", "0.00000000", "0.00000000"],
    ["162", "UZ", "0.00000000", "0.00000000"],
    ["162", "TEMP", "300.000000", "0.00000000"],
    ["163", "UX", "0.00000000", "0.00000000"],
    ["163", "UY", "0.00000000", "0.00000000"],
    ["163", "UZ", "0.00000000", "0.00000000"],
    ["163", "TEMP", "300.000000", "0.00000000"],
    ["164", "UX", "0.00000000", "0.00000000"],
    ["164", "UY", "0.00000000", "0.00000000"],
    ["164", "UZ", "0.00000000", "0.00000000"],
    ["164", "TEMP", "300.000000", "0.00000000"],
    ["165", "UX", "0.00000000", "0.00000000"],
    ["165", "UY", "0.00000000", "0.00000000"],
    ["165", "UZ", "0.00000000", "0.00000000"],
    ["165", "TEMP", "300.000000", "0.00000000"],
    ["166", "UX", "0.00000000", "0.00000000"],
    ["166", "UY", "0.00000000", "0.00000000"],
    ["166", "UZ", "0.00000000", "0.00000000"],
    ["166", "TEMP", "300.000000", "0.00000000"],
    ["167", "UX", "0.00000000", "0.00000000"],
    ["167", "UY", "0.00000000", "0.00000000"],
    ["167", "UZ", "0.00000000", "0.00000000"],
    ["167", "TEMP", "300.000000", "0.00000000"],
    ["168", "UX", "0.00000000", "0.00000000"],
    ["168", "UY", "0.00000000", "0.00000000"],
    ["168", "UZ", "0.00000000", "0.00000000"],
    ["168", "TEMP", "300.000000", "0.00000000"],
    ["169", "UX", "0.00000000", "0.00000000"],
    ["169", "UY", "0.00000000", "0.00000000"],
    ["169", "UZ", "0.00000000", "0.00000000"],
    ["169", "TEMP", "300.000000", "0.00000000"],
    ["171", "UX", "0.00000000", "0.00000000"],
    ["171", "UY", "0.00000000", "0.00000000"],
    ["171", "UZ", "0.00000000", "0.00000000"],
    ["171", "TEMP", "300.000000", "0.00000000"],
    ["172", "UX", "0.00000000", "0.00000000"],
    ["172", "UY", "0.00000000", "0.00000000"],
    ["172", "UZ", "0.00000000", "0.00000000"],
    ["172", "TEMP", "300.000000", "0.00000000"],
    ["173", "UX", "0.00000000", "0.00000000"],
    ["173", "UY", "0.00000000", "0.00000000"],
    ["173", "UZ", "0.00000000", "0.00000000"],
    ["173", "TEMP", "300.000000", "0.00000000"],
    ["174", "UX", "0.00000000", "0.00000000"],
    ["174", "UY", "0.00000000", "0.00000000"],
    ["174", "UZ", "0.00000000", "0.00000000"],
    ["174", "TEMP", "300.000000", "0.00000000"],
    ["175", "UX", "0.00000000", "0.00000000"],
    ["175", "UY", "0.00000000", "0.00000000"],
    ["175", "UZ", "0.00000000", "0.00000000"],
    ["175", "TEMP", "300.000000", "0.00000000"],
    ["176", "UX", "0.00000000", "0.00000000"],
    ["176", "UY", "0.00000000", "0.00000000"],
    ["176", "UZ", "0.00000000", "0.00000000"],
    ["176", "TEMP", "300.000000", "0.00000000"],
    ["177", "UX", "0.00000000", "0.00000000"],
    ["177", "UY", "0.00000000", "0.00000000"],
    ["177", "UZ", "0.00000000", "0.00000000"],
    ["177", "TEMP", "300.000000", "0.00000000"],
    ["178", "UX", "0.00000000", "0.00000000"],
    ["178", "UY", "0.00000000", "0.00000000"],
    ["178", "UZ", "0.00000000", "0.00000000"],
    ["178", "TEMP", "300.000000", "0.00000000"],
    ["179", "UX", "0.00000000", "0.00000000"],
    ["179", "UY", "0.00000000", "0.00000000"],
    ["179", "UZ", "0.00000000", "0.00000000"],
    ["179", "TEMP", "300.000000", "0.00000000"],
    ["314", "UX", "0.00000000", "0.00000000"],
    ["314", "UY", "0.00000000", "0.00000000"],
    ["314", "UZ", "0.00000000", "0.00000000"],
    ["314", "TEMP", "300.000000", "0.00000000"],
    ["315", "UX", "0.00000000", "0.00000000"],
    ["315", "UY", "0.00000000", "0.00000000"],
    ["315", "UZ", "0.00000000", "0.00000000"],
    ["315", "TEMP", "300.000000", "0.00000000"],
]

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


def test_cmd_class_dlist_vm(mapdl, cleared):
    # edit the input file
    with open(verif_files.vmfiles["vm223"]) as fid:
        cmds = fid.read()

    cmds = cmds.lower().replace("solve", "!solve")  # To avoid solving
    mapdl.input_strings(cmds)

    mapdl.allsel("all")
    out = mapdl.dlist()
    out_list = out.to_list()

    def are_the_same_result():
        for el1, el2 in zip(out_list, DLIST_RESULT):
            for el11, el22 in zip(el1, el2):
                if el11 != el22:
                    return False
        return True

    assert isinstance(out, BoundaryConditionsListingOutput)
    assert isinstance(out_list, list)
    assert out_list
    assert are_the_same_result()


@pytest.mark.parametrize("func", LIST_OF_INQUIRE_FUNCTIONS)
def test_inquire_functions(mapdl, func):
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


def test_string_with_literal():
    base_ = "asdf\nasdf"
    output = StringWithLiteralRepr(base_)
    assert output.__repr__() == output
    assert output.__repr__() == base_
    assert len(output.split()) == 2
