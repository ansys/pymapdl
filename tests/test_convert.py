import os
import pytest
from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import examples
from ansys.mapdl.core.convert import convert_apdl_strings

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

cmblock = """CMBLOCK,PRESSURE_AREAS,NODE,    6
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
    mapdl.run("1     3.352881632E-03     1.110639271E-02     5.172433282E-03")
    mapdl.run("2     3.485685736E-03     1.110981270E-02     4.999255638E-03")
    mapdl.run("3     3.615164748E-03     1.111323677E-02     4.823719994E-03")
    mapdl.run("4     3.673859471E-03     1.111439119E-02     4.740300611E-03")
    mapdl.run("5     3.709417144E-03     1.111407057E-02     4.691582629E-03")"""

pyeblock = """with mapdl.non_interactive:
    mapdl.run("eblock,19,solid,,6240")
    mapdl.run("(19i9)")
    mapdl.run("1        1        1        1        0        0        0        0       20        0    38161   186586   186589   192999   193065   191265   191262   193063   193064")
    mapdl.run("194712   194731   213866   194716   210305   210306   213993   210310   194715   194730   213865   213995")
    mapdl.run("1        1        1        1        0        0        0        0       20        0    38162   186586   193065   192999   186589   186781   193066   192935   186784")
    mapdl.run("194716   213866   194731   194712   195560   213737   195572   195557   194714   213997   213736   194729")
    mapdl.run("1        1        1        1        0        0        0        0       20        0    38163   186781   193066   192935   186784   186976   193067   192871   186979")
    mapdl.run("195560   213737   195572   195557   196210   213608   196222   196207   195559   213998   213607   195571")
    mapdl.run("1        1        1        1        0        0        0        0       20        0    38164   186976   193067   192871   186979   187171   193068   192807   187174")
    mapdl.run("196210   213608   196222   196207   196860   213479   196872   196857   196209   213999   213478   196221")"""

pycmblock = """with mapdl.non_interactive:
    mapdl.run("CMBLOCK,PRESSURE_AREAS,NODE,    6")
    mapdl.run("(8i10)")
    mapdl.run("1688      1689      1690      1691      1700      1701      1702      1703")
    mapdl.run("1704      1705      1706      1707      1708      1709      1710      1711")
    mapdl.run("1712      1721      1723      1731      1736      1754      1755      1756")
    mapdl.run("1757      1758      1759      1760      1761      1762      1763      1764")
    mapdl.run("1765      1766      1767      1768      1769      1802      1803      1804")
    mapdl.run("1805      1806      1807      1808      1809      1831      1832      1833")"""

apdl_input = {
    'nblock': nblock,
    'eblock': eblock,
    'cmblock': cmblock
    }

pymapdl_output = {
    'nblock': pynblock,
    'eblock': pyeblock,
    'cmblock': pycmblock
    }

block_commands = ['nblock', 'eblock', 'cmblock']


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
    apdl_block = apdl_input[cmd].split('\n')
    pyblock = convert_apdl_strings(apdl_strings=apdl_block)
    pyblock = '\n'.join(pyblock)
    assert pymapdl_output[cmd] in pyblock
