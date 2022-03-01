import os

import pytest

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import examples
from ansys.mapdl.core.convert import (
    COMMANDS_TO_NOT_BE_CONVERTED,
    FileTranslator,
    convert_apdl_block,
)

nblock = """nblock,3,,326253
(1i9,3e20.9e3)
        1     3.352881632E-03     1.110639271E-02     5.172433282E-03
        2     3.485685736E-03     1.110981270E-02     4.999255638E-03
        3     3.615164748E-03     1.111323677E-02     4.823719994E-03
        4     3.673859471E-03     1.111439119E-02     4.740300611E-03
        5     3.709417144E-03     1.111407057E-02     4.691582629E-03
-1"""

eblock = """eblock,19,solid,,6240
(19i9)
        1        1        1        1        0        0        0        0       20        0    38161   186586   186589   192999   193065   191265   191262   193063   193064
   194712   194731   213866   194716   210305   210306   213993   210310   194715   194730   213865   213995
        1        1        1        1        0        0        0        0       20        0    38162   186586   193065   192999   186589   186781   193066   192935   186784
   194716   213866   194731   194712   195560   213737   195572   195557   194714   213997   213736   194729
        1        1        1        1        0        0        0        0       20        0    38163   186781   193066   192935   186784   186976   193067   192871   186979
   195560   213737   195572   195557   196210   213608   196222   196207   195559   213998   213607   195571
        1        1        1        1        0        0        0        0       20        0    38164   186976   193067   192871   186979   187171   193068   192807   187174
   196210   213608   196222   196207   196860   213479   196872   196857   196209   213999   213478   196221
"""

cmblock = """CMBLOCK,PRESSURE_AREAS,NODE,    48
(8i10)
      1688      1689      1690      1691      1700      1701      1702      1703
      1704      1705      1706      1707      1708      1709      1710      1711
      1712      1721      1723      1731      1736      1754      1755      1756
      1757      1758      1759      1760      1761      1762      1763      1764
      1765      1766      1767      1768      1769      1802      1803      1804
      1805      1806      1807      1808      1809      1831      1832      1833"""

pynblock = """with mapdl.non_interactive:
    mapdl.run("nblock,3,,326253")
    mapdl.run("(1i9,3e20.9e3)")
    mapdl.run("        1     3.352881632E-03     1.110639271E-02     5.172433282E-03")
    mapdl.run("        2     3.485685736E-03     1.110981270E-02     4.999255638E-03")
    mapdl.run("        3     3.615164748E-03     1.111323677E-02     4.823719994E-03")
    mapdl.run("        4     3.673859471E-03     1.111439119E-02     4.740300611E-03")
    mapdl.run("        5     3.709417144E-03     1.111407057E-02     4.691582629E-03")
    mapdl.run("-1")"""

pyeblock = """with mapdl.non_interactive:
    mapdl.run("eblock,19,solid,,6240")
    mapdl.run("(19i9)")
    mapdl.run("        1        1        1        1        0        0        0        0       20        0    38161   186586   186589   192999   193065   191265   191262   193063   193064")
    mapdl.run("   194712   194731   213866   194716   210305   210306   213993   210310   194715   194730   213865   213995")
    mapdl.run("        1        1        1        1        0        0        0        0       20        0    38162   186586   193065   192999   186589   186781   193066   192935   186784")
    mapdl.run("   194716   213866   194731   194712   195560   213737   195572   195557   194714   213997   213736   194729")
    mapdl.run("        1        1        1        1        0        0        0        0       20        0    38163   186781   193066   192935   186784   186976   193067   192871   186979")
    mapdl.run("   195560   213737   195572   195557   196210   213608   196222   196207   195559   213998   213607   195571")
    mapdl.run("        1        1        1        1        0        0        0        0       20        0    38164   186976   193067   192871   186979   187171   193068   192807   187174")
    mapdl.run("   196210   213608   196222   196207   196860   213479   196872   196857   196209   213999   213478   196221")"""

pycmblock = """with mapdl.non_interactive:
    mapdl.run("CMBLOCK,PRESSURE_AREAS,NODE,    48")
    mapdl.run("(8i10)")
    mapdl.run("      1688      1689      1690      1691      1700      1701      1702      1703")
    mapdl.run("      1704      1705      1706      1707      1708      1709      1710      1711")
    mapdl.run("      1712      1721      1723      1731      1736      1754      1755      1756")
    mapdl.run("      1757      1758      1759      1760      1761      1762      1763      1764")
    mapdl.run("      1765      1766      1767      1768      1769      1802      1803      1804")
    mapdl.run("      1805      1806      1807      1808      1809      1831      1832      1833")"""


block_commands = ["nblock", "eblock", "cmblock"]

apdl_input = dict(zip(block_commands, [nblock, eblock, cmblock]))
pymapdl_output = dict(zip(block_commands, [pynblock, pyeblock, pycmblock]))

APDL_CMDS = """
/CLE,NOSTART
FINISH,
/PREP7
!comment
/SOLU,
/COM,Time step: 1
ACEL,0.0,9.80665,0.0
F,1,fx,30,,,
TIME,0.02
SOLVE,
/POST1,
SET,last,,,,,,,
/SOLU,
/COM,Time step: 2
ACEL,0.0,9.80665,0.0
F,1,fx,-30,,,
TIME,0.04
/INQUIRE,,DIRECTORY
SOLVE,
/POST1,
SET,last,,,,,,,
LSSOLVE
/out,test,inp !testing *get insider non_interactive
*get,dummy,node,0,u,x
/out
!testing if
aa = 1
*if,aa,eq,1
/prep7
*endif

! comment
! empty line
/prep7

!testing
/out,term

*cfopen
*cfclos

/prep7

!non accepted command
/test
"""

APDL_MACRO = """
/PREP7
*CREATE,SLV
/SOLU
ACEL,,386
aa = ARG1
KBC,1 ! STEP BOUNDARY CONDITION
D,1,UZ,,,2
D,1,UX,,,,,UY
TIME,.01 ! INITIAL L.S. TO ATTAIN FINAL ACCELERATION
NSUBST,5
OUTRES,,1
LSWRITE,1 ! WRITE LOAD STEP FILE 1
*END
*USE,SLV"""


def test_convert_no_use_function_names(tmpdir):
    vm_file = examples.vmfiles["vm1"]
    pyscript = str(tmpdir.mkdir("tmpdir").join("vm1.py"))
    clines = pymapdl.convert_script(
        vm_file, pyscript, loglevel="ERROR", use_function_names=False
    )
    assert clines


@pytest.mark.skipif(os.name == "nt", reason="Requires multiple instances")
def test_convert(tmpdir):
    vm_file = examples.vmfiles["vm1"]
    pyscript = str(tmpdir.mkdir("tmpdir").join("vm1.py"))
    clines = pymapdl.convert_script(vm_file, pyscript, loglevel="ERROR")
    assert clines


@pytest.mark.parametrize("cmd", block_commands)
def test_convert_block_commands(tmpdir, cmd):
    apdl_block = apdl_input[cmd]
    pyblock = convert_apdl_block(apdl_strings=apdl_block.split("\n"))
    pyblock = "\n".join(pyblock)
    assert pymapdl_output[cmd] in pyblock


def test_logger(capsys):

    apdl_ = """FINISH
    /PREP7
    """.split(
        "\n"
    )

    translator = FileTranslator(line_ending="\n", show_log=True)
    for line in apdl_:
        translator.translate_line(line)
    std = capsys.readouterr()
    assert all(
        ["Converted" in each for each in std.err.split("\n")[:-1]]
    )  # last one is an empty line.


def test_add_import():
    assert "launch_mapdl" in convert_apdl_block(APDL_CMDS, add_imports=True)
    assert "ansys.mapdl.core" in convert_apdl_block(APDL_CMDS, add_imports=True)

    assert "launch_mapdl" not in convert_apdl_block(APDL_CMDS, add_imports=False)
    assert "ansys.mapdl.core" not in convert_apdl_block(APDL_CMDS, add_imports=False)


def test_auto_exit():
    assert "mapdl.exit" in convert_apdl_block(APDL_CMDS, auto_exit=True)
    assert "mapdl.exit" not in convert_apdl_block(APDL_CMDS, auto_exit=False)

    # add_import overwrite
    assert "mapdl.exit" in convert_apdl_block(
        APDL_CMDS, auto_exit=True, add_imports=True
    )
    assert "mapdl.exit" not in convert_apdl_block(
        APDL_CMDS, auto_exit=False, add_imports=True
    )

    assert "mapdl.exit" not in convert_apdl_block(
        APDL_CMDS, auto_exit=True, add_imports=False
    )
    assert "mapdl.exit" not in convert_apdl_block(
        APDL_CMDS, auto_exit=False, add_imports=False
    )


def test_comment_solve():
    assert (
        'MAPDL.COM("SOLVE' in convert_apdl_block(APDL_CMDS, comment_solve=True).upper()
    )
    assert (
        'MAPDL.COM("LSSOLVE'
        in convert_apdl_block(APDL_CMDS, comment_solve=True).upper()
    )
    assert (
        "THE FOLLOWING LINE HAS BEEN COMMENTED DUE TO `COMMENT_SOLVE`"
        in convert_apdl_block(APDL_CMDS, comment_solve=True).upper()
    )

    assert (
        'MAPDL.COM("SOLVE'
        not in convert_apdl_block(APDL_CMDS, comment_solve=False).upper()
    )
    assert (
        'MAPDL.COM("LSSOLVE'
        not in convert_apdl_block(APDL_CMDS, comment_solve=False).upper()
    )
    assert (
        "THE FOLLOWING LINE HAS BEEN COMMENTED DUE TO `COMMENT_SOLVE`"
        not in convert_apdl_block(APDL_CMDS, comment_solve=False).upper()
    )

    assert "mapdl.solve" in convert_apdl_block(APDL_CMDS, comment_solve=False)
    assert "mapdl.lssolve" in convert_apdl_block(APDL_CMDS, comment_solve=False)


def test_macro_to_function():
    assert "def SLV(" in convert_apdl_block(APDL_MACRO, macros_as_functions=True)
    assert "SLV()" in convert_apdl_block(APDL_MACRO, macros_as_functions=True)
    assert "\n\n\ndef SLV" in convert_apdl_block(APDL_MACRO, macros_as_functions=True)
    assert "\n\n\nSLV" in convert_apdl_block(APDL_MACRO, macros_as_functions=True)


def test_out():
    assert "with mapdl.non_interactive" in convert_apdl_block("/OUT,file.txt")
    assert "with mapdl.non_interactive" not in convert_apdl_block("/OUT")
    assert 'mapdl.run("/OUT")' in convert_apdl_block("/OUT")
    assert 'mapdl.run("/GOPR")' in convert_apdl_block("/OUT")


def test_nopr():
    assert "mapdl._run" in convert_apdl_block("/NOPR")


def test_header():
    assert "Script generated by ansys-mapdl-core version" in convert_apdl_block("/com")
    assert "Script generated by ansys-mapdl-core version" in convert_apdl_block(
        "/com", header=True
    )
    assert "Script generated by ansys-mapdl-core version" not in convert_apdl_block(
        "/com", header=False
    )
    assert '"""My header"""' in convert_apdl_block("/com", header="My header")


def test_com():
    converted_output = convert_apdl_block(
        "/com, this is a comment !inline comment!", header=False, add_imports=False
    )

    assert 'mapdl.com("this is a comment")' in converted_output
    assert "this is a comment" in converted_output
    assert "# inline comment" in converted_output


def test_do_loops():
    cmd = """*do,1,1,10
/prep7
*enddo
/com, asdf
"""
    output = convert_apdl_block(cmd, add_imports=False, header=False)

    assert "with mapdl.non_interactive:\n    " in output
    assert '    mapdl.run("*do,1,1,10")' in output
    assert '    mapdl.run("*enddo")' in output
    assert '("*enddo")\nmapdl' in output


def test_empty_line():
    assert "" == convert_apdl_block("", add_imports=False, header=False)


def test_repeat():
    assert "with mapdl.non_interactive:" in convert_apdl_block(
        "/prep7\n*rep,", header=False, add_imports=False
    )
    assert "    mapdl.prep7()" in convert_apdl_block(
        "/prep7\n*rep,", header=False, add_imports=False
    )
    assert '    mapdl.run("*rep' in convert_apdl_block(
        "/prep7\n*rep, ", header=False, add_imports=False
    )


@pytest.mark.parametrize("cmd", COMMANDS_TO_NOT_BE_CONVERTED)
def test_commands_to_not_be_converted(cmd):
    assert f'mapdl.run("{cmd}")' in convert_apdl_block(
        cmd, header=False, add_imports=False
    )


@pytest.mark.parametrize("ending", ["\n", "\r\n"])
def test_detect_line_ending(ending):
    assert ending in convert_apdl_block(
        f"/com First line{ending}/com Second line", header=False, add_imports=False
    )
    assert ending in convert_apdl_block(
        f"/com First line{ending}/com Second line",
        header=False,
        add_imports=False,
        line_ending="\r\n",
    )


def test_no_macro_as_functions():
    output = convert_apdl_block(
        APDL_MACRO, macros_as_functions=False, add_imports=False, header=False
    )
    assert "with mapdl.non_interactive" in output
    assert '    mapdl.run("*CREATE,SLV")' in output
    assert '    mapdl.run("*END")' in output


def test_format_ouput():
    """Just testing it runs."""
    non_formated = "def(a,b):return a + b"
    converted = FileTranslator().format_using_autopep8(non_formated)
    if converted:
        assert converted == "def(a, b): return a + b\n"
        assert isinstance(converted, str)
    else:
        assert converted is None


def test_header_error():
    with pytest.raises(TypeError):
        convert_apdl_block("asdf", header=2)


def test_print_com_in_converter():
    assert "print_com=True" in convert_apdl_block("/prep7\nN,,,,")  # Default
    assert "print_com=True" in convert_apdl_block("/prep7\nN,,,,", print_com=True)
    assert "print_com=True" not in convert_apdl_block("/prep7\nN,,,,", print_com=False)
