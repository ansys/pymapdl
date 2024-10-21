# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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
from conftest import has_dependency, requires

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

DLIST_RESULT = [
    ["1", "UX", "0.00000000", "0.00000000"],
    ["1", "UY", "0.00000000", "0.00000000"],
    ["1", "UZ", "0.00000000", "0.00000000"],
    ["1", "TEMP", "300.000000", "0.00000000"],
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
    ["316", "UX", "0.00000000", "0.00000000"],
    ["316", "UY", "0.00000000", "0.00000000"],
    ["316", "UZ", "0.00000000", "0.00000000"],
    ["316", "TEMP", "300.000000", "0.00000000"],
    ["317", "UX", "0.00000000", "0.00000000"],
    ["317", "UY", "0.00000000", "0.00000000"],
    ["317", "UZ", "0.00000000", "0.00000000"],
    ["317", "TEMP", "300.000000", "0.00000000"],
    ["318", "UX", "0.00000000", "0.00000000"],
    ["318", "UY", "0.00000000", "0.00000000"],
    ["318", "UZ", "0.00000000", "0.00000000"],
    ["318", "TEMP", "300.000000", "0.00000000"],
    ["319", "UX", "0.00000000", "0.00000000"],
    ["319", "UY", "0.00000000", "0.00000000"],
    ["319", "UZ", "0.00000000", "0.00000000"],
    ["319", "TEMP", "300.000000", "0.00000000"],
    ["320", "UX", "0.00000000", "0.00000000"],
    ["320", "UY", "0.00000000", "0.00000000"],
    ["320", "UZ", "0.00000000", "0.00000000"],
    ["320", "TEMP", "300.000000", "0.00000000"],
    ["321", "UX", "0.00000000", "0.00000000"],
    ["321", "UY", "0.00000000", "0.00000000"],
    ["321", "UZ", "0.00000000", "0.00000000"],
    ["321", "TEMP", "300.000000", "0.00000000"],
    ["322", "UX", "0.00000000", "0.00000000"],
    ["322", "UY", "0.00000000", "0.00000000"],
    ["322", "UZ", "0.00000000", "0.00000000"],
    ["322", "TEMP", "300.000000", "0.00000000"],
    ["323", "UX", "0.00000000", "0.00000000"],
    ["323", "UY", "0.00000000", "0.00000000"],
    ["323", "UZ", "0.00000000", "0.00000000"],
    ["323", "TEMP", "300.000000", "0.00000000"],
    ["324", "UX", "0.00000000", "0.00000000"],
    ["324", "UY", "0.00000000", "0.00000000"],
    ["324", "UZ", "0.00000000", "0.00000000"],
    ["324", "TEMP", "300.000000", "0.00000000"],
    ["330", "UX", "0.00000000", "0.00000000"],
    ["330", "UY", "0.00000000", "0.00000000"],
    ["330", "UZ", "0.00000000", "0.00000000"],
    ["330", "TEMP", "300.000000", "0.00000000"],
    ["331", "UX", "0.00000000", "0.00000000"],
    ["331", "UY", "0.00000000", "0.00000000"],
    ["331", "UZ", "0.00000000", "0.00000000"],
    ["331", "TEMP", "300.000000", "0.00000000"],
    ["332", "UX", "0.00000000", "0.00000000"],
    ["332", "UY", "0.00000000", "0.00000000"],
    ["332", "UZ", "0.00000000", "0.00000000"],
    ["332", "TEMP", "300.000000", "0.00000000"],
    ["334", "UX", "0.00000000", "0.00000000"],
    ["334", "UY", "0.00000000", "0.00000000"],
    ["334", "UZ", "0.00000000", "0.00000000"],
    ["334", "TEMP", "300.000000", "0.00000000"],
    ["335", "UX", "0.00000000", "0.00000000"],
    ["335", "UY", "0.00000000", "0.00000000"],
    ["335", "UZ", "0.00000000", "0.00000000"],
    ["335", "TEMP", "300.000000", "0.00000000"],
    ["336", "UX", "0.00000000", "0.00000000"],
    ["336", "UY", "0.00000000", "0.00000000"],
    ["336", "UZ", "0.00000000", "0.00000000"],
    ["336", "TEMP", "300.000000", "0.00000000"],
    ["340", "UX", "0.00000000", "0.00000000"],
    ["340", "UY", "0.00000000", "0.00000000"],
    ["340", "UZ", "0.00000000", "0.00000000"],
    ["340", "TEMP", "300.000000", "0.00000000"],
    ["341", "UX", "0.00000000", "0.00000000"],
    ["341", "UY", "0.00000000", "0.00000000"],
    ["341", "UZ", "0.00000000", "0.00000000"],
    ["341", "TEMP", "300.000000", "0.00000000"],
    ["342", "UX", "0.00000000", "0.00000000"],
    ["342", "UY", "0.00000000", "0.00000000"],
    ["342", "UZ", "0.00000000", "0.00000000"],
    ["342", "TEMP", "300.000000", "0.00000000"],
    ["343", "UX", "0.00000000", "0.00000000"],
    ["343", "UY", "0.00000000", "0.00000000"],
    ["343", "UZ", "0.00000000", "0.00000000"],
    ["343", "TEMP", "300.000000", "0.00000000"],
    ["348", "UX", "0.00000000", "0.00000000"],
    ["348", "UY", "0.00000000", "0.00000000"],
    ["348", "UZ", "0.00000000", "0.00000000"],
    ["348", "TEMP", "300.000000", "0.00000000"],
    ["349", "UX", "0.00000000", "0.00000000"],
    ["349", "UY", "0.00000000", "0.00000000"],
    ["349", "UZ", "0.00000000", "0.00000000"],
    ["349", "TEMP", "300.000000", "0.00000000"],
    ["350", "UX", "0.00000000", "0.00000000"],
    ["350", "UY", "0.00000000", "0.00000000"],
    ["350", "UZ", "0.00000000", "0.00000000"],
    ["350", "TEMP", "300.000000", "0.00000000"],
    ["351", "UX", "0.00000000", "0.00000000"],
    ["351", "UY", "0.00000000", "0.00000000"],
    ["351", "UZ", "0.00000000", "0.00000000"],
    ["351", "TEMP", "300.000000", "0.00000000"],
    ["352", "UX", "0.00000000", "0.00000000"],
    ["352", "UY", "0.00000000", "0.00000000"],
    ["352", "UZ", "0.00000000", "0.00000000"],
    ["352", "TEMP", "300.000000", "0.00000000"],
    ["353", "UX", "0.00000000", "0.00000000"],
    ["353", "UY", "0.00000000", "0.00000000"],
    ["353", "UZ", "0.00000000", "0.00000000"],
    ["353", "TEMP", "300.000000", "0.00000000"],
    ["354", "UX", "0.00000000", "0.00000000"],
    ["354", "UY", "0.00000000", "0.00000000"],
    ["354", "UZ", "0.00000000", "0.00000000"],
    ["354", "TEMP", "300.000000", "0.00000000"],
    ["355", "UX", "0.00000000", "0.00000000"],
    ["355", "UY", "0.00000000", "0.00000000"],
    ["355", "UZ", "0.00000000", "0.00000000"],
    ["355", "TEMP", "300.000000", "0.00000000"],
    ["356", "UX", "0.00000000", "0.00000000"],
    ["356", "UY", "0.00000000", "0.00000000"],
    ["356", "UZ", "0.00000000", "0.00000000"],
    ["356", "TEMP", "300.000000", "0.00000000"],
    ["357", "UX", "0.00000000", "0.00000000"],
    ["357", "UY", "0.00000000", "0.00000000"],
    ["357", "UZ", "0.00000000", "0.00000000"],
    ["357", "TEMP", "300.000000", "0.00000000"],
    ["358", "UX", "0.00000000", "0.00000000"],
    ["358", "UY", "0.00000000", "0.00000000"],
    ["358", "UZ", "0.00000000", "0.00000000"],
    ["358", "TEMP", "300.000000", "0.00000000"],
    ["359", "UX", "0.00000000", "0.00000000"],
    ["359", "UY", "0.00000000", "0.00000000"],
    ["359", "UZ", "0.00000000", "0.00000000"],
    ["359", "TEMP", "300.000000", "0.00000000"],
    ["360", "UX", "0.00000000", "0.00000000"],
    ["360", "UY", "0.00000000", "0.00000000"],
    ["360", "UZ", "0.00000000", "0.00000000"],
    ["360", "TEMP", "300.000000", "0.00000000"],
    ["361", "UX", "0.00000000", "0.00000000"],
    ["361", "UY", "0.00000000", "0.00000000"],
    ["361", "UZ", "0.00000000", "0.00000000"],
    ["361", "TEMP", "300.000000", "0.00000000"],
    ["362", "UX", "0.00000000", "0.00000000"],
    ["362", "UY", "0.00000000", "0.00000000"],
    ["362", "UZ", "0.00000000", "0.00000000"],
    ["362", "TEMP", "300.000000", "0.00000000"],
    ["363", "UX", "0.00000000", "0.00000000"],
    ["363", "UY", "0.00000000", "0.00000000"],
    ["363", "UZ", "0.00000000", "0.00000000"],
    ["363", "TEMP", "300.000000", "0.00000000"],
    ["364", "UX", "0.00000000", "0.00000000"],
    ["364", "UY", "0.00000000", "0.00000000"],
    ["364", "UZ", "0.00000000", "0.00000000"],
    ["364", "TEMP", "300.000000", "0.00000000"],
    ["365", "UX", "0.00000000", "0.00000000"],
    ["365", "UY", "0.00000000", "0.00000000"],
    ["365", "UZ", "0.00000000", "0.00000000"],
    ["365", "TEMP", "300.000000", "0.00000000"],
    ["366", "UX", "0.00000000", "0.00000000"],
    ["366", "UY", "0.00000000", "0.00000000"],
    ["366", "UZ", "0.00000000", "0.00000000"],
    ["366", "TEMP", "300.000000", "0.00000000"],
    ["520", "UX", "0.00000000", "0.00000000"],
    ["520", "UY", "0.00000000", "0.00000000"],
    ["520", "UZ", "0.00000000", "0.00000000"],
    ["520", "TEMP", "300.000000", "0.00000000"],
    ["572", "UX", "0.00000000", "0.00000000"],
    ["572", "UY", "0.00000000", "0.00000000"],
    ["572", "UZ", "0.00000000", "0.00000000"],
    ["572", "TEMP", "300.000000", "0.00000000"],
    ["573", "UX", "0.00000000", "0.00000000"],
    ["573", "UY", "0.00000000", "0.00000000"],
    ["573", "UZ", "0.00000000", "0.00000000"],
    ["573", "TEMP", "300.000000", "0.00000000"],
    ["574", "UX", "0.00000000", "0.00000000"],
    ["574", "UY", "0.00000000", "0.00000000"],
    ["574", "UZ", "0.00000000", "0.00000000"],
    ["574", "TEMP", "300.000000", "0.00000000"],
    ["575", "UX", "0.00000000", "0.00000000"],
    ["575", "UY", "0.00000000", "0.00000000"],
    ["575", "UZ", "0.00000000", "0.00000000"],
    ["575", "TEMP", "300.000000", "0.00000000"],
    ["576", "UX", "0.00000000", "0.00000000"],
    ["576", "UY", "0.00000000", "0.00000000"],
    ["576", "UZ", "0.00000000", "0.00000000"],
    ["576", "TEMP", "300.000000", "0.00000000"],
    ["628", "UX", "0.00000000", "0.00000000"],
    ["628", "UY", "0.00000000", "0.00000000"],
    ["628", "UZ", "0.00000000", "0.00000000"],
    ["628", "TEMP", "300.000000", "0.00000000"],
    ["645", "UX", "0.00000000", "0.00000000"],
    ["645", "UY", "0.00000000", "0.00000000"],
    ["645", "UZ", "0.00000000", "0.00000000"],
    ["645", "TEMP", "300.000000", "0.00000000"],
    ["708", "UX", "0.00000000", "0.00000000"],
    ["708", "UY", "0.00000000", "0.00000000"],
    ["708", "UZ", "0.00000000", "0.00000000"],
    ["708", "TEMP", "300.000000", "0.00000000"],
    ["709", "UX", "0.00000000", "0.00000000"],
    ["709", "UY", "0.00000000", "0.00000000"],
    ["709", "UZ", "0.00000000", "0.00000000"],
    ["709", "TEMP", "300.000000", "0.00000000"],
    ["710", "UX", "0.00000000", "0.00000000"],
    ["710", "UY", "0.00000000", "0.00000000"],
    ["710", "UZ", "0.00000000", "0.00000000"],
    ["710", "TEMP", "300.000000", "0.00000000"],
    ["711", "UX", "0.00000000", "0.00000000"],
    ["711", "UY", "0.00000000", "0.00000000"],
    ["711", "UZ", "0.00000000", "0.00000000"],
    ["711", "TEMP", "300.000000", "0.00000000"],
    ["712", "UX", "0.00000000", "0.00000000"],
    ["712", "UY", "0.00000000", "0.00000000"],
    ["712", "UZ", "0.00000000", "0.00000000"],
    ["712", "TEMP", "300.000000", "0.00000000"],
    ["713", "UX", "0.00000000", "0.00000000"],
    ["713", "UY", "0.00000000", "0.00000000"],
    ["713", "UZ", "0.00000000", "0.00000000"],
    ["713", "TEMP", "300.000000", "0.00000000"],
    ["757", "UX", "0.00000000", "0.00000000"],
    ["757", "UY", "0.00000000", "0.00000000"],
    ["757", "UZ", "0.00000000", "0.00000000"],
    ["757", "TEMP", "300.000000", "0.00000000"],
    ["758", "UX", "0.00000000", "0.00000000"],
    ["758", "UY", "0.00000000", "0.00000000"],
    ["758", "UZ", "0.00000000", "0.00000000"],
    ["758", "TEMP", "300.000000", "0.00000000"],
    ["784", "UX", "0.00000000", "0.00000000"],
    ["784", "UY", "0.00000000", "0.00000000"],
    ["784", "UZ", "0.00000000", "0.00000000"],
    ["784", "TEMP", "300.000000", "0.00000000"],
    ["785", "UX", "0.00000000", "0.00000000"],
    ["785", "UY", "0.00000000", "0.00000000"],
    ["785", "UZ", "0.00000000", "0.00000000"],
    ["785", "TEMP", "300.000000", "0.00000000"],
    ["831", "UX", "0.00000000", "0.00000000"],
    ["831", "UY", "0.00000000", "0.00000000"],
    ["831", "UZ", "0.00000000", "0.00000000"],
    ["831", "TEMP", "300.000000", "0.00000000"],
    ["832", "UX", "0.00000000", "0.00000000"],
    ["832", "UY", "0.00000000", "0.00000000"],
    ["832", "UZ", "0.00000000", "0.00000000"],
    ["832", "TEMP", "300.000000", "0.00000000"],
    ["833", "UX", "0.00000000", "0.00000000"],
    ["833", "UY", "0.00000000", "0.00000000"],
    ["833", "UZ", "0.00000000", "0.00000000"],
    ["833", "TEMP", "300.000000", "0.00000000"],
    ["835", "UX", "0.00000000", "0.00000000"],
    ["835", "UY", "0.00000000", "0.00000000"],
    ["835", "UZ", "0.00000000", "0.00000000"],
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

    if has_dependency("pandas"):
        out_df = out.to_dataframe()
        assert isinstance(out_df, pd.DataFrame) and not out_df.empty


def test_cmd_class_dlist_vm(mapdl, cleared):
    # Run only the first 100 lines of VM223
    with open(verif_files.vmfiles["vm223"]) as fid:
        cmds = fid.read()

    mapdl.finish()
    ind = cmds.find("NSEL,ALL")
    mapdl.input_strings(cmds[:ind])

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

    if has_dependency("pandas"):
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

    if has_dependency("pandas"):
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


def test_cmlist(mapdl):
    mapdl.clear()

    mapdl.prep7()
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


class Test_bc_cmdlist_solid:

    def solid_model(self, mapdl):
        # Solid model (Geometry)

        mapdl.clear()

        mapdl.prep7()

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

    @requires("pandas")
    def test_dklist(self, mapdl):

        df_dk = pd.DataFrame(
            {
                "KEYPOINT": [1],
                "LABEL": ["UX"],
                "REAL": [0.0],
                "IMAG": [0.0],
                "EXP KEY": ["0"],
            }
        )

        self.solid_model(mapdl)
        mapdl.dk(1, "UX", 0)

        dklist_result = mapdl.dklist().to_dataframe()

        assert not dklist_result.empty
        assert dklist_result.compare(df_dk).empty

    @requires("pandas")
    def test_dllist(self, mapdl):

        df_dl = pd.DataFrame(
            {
                "LINE": [2, 2],
                "LABEL": ["UX", "UY"],
                "REAL": [0.0, 0.0],
                "IMAG": [0.0, 0.0],
                "NAREA": ["0", "0"],
            }
        )

        self.solid_model(mapdl)
        mapdl.dl(2, 1, "ALL", 0)

        dllist_result = mapdl.dllist().to_dataframe()

        assert not dllist_result.empty
        assert dllist_result.compare(df_dl).empty

    @requires("pandas")
    def test_dalist(self, mapdl):

        df_da = pd.DataFrame(
            {
                "AREA": [1],
                "LABEL": ["UZ"],
                "REAL": [0.0],
                "IMAG": [0.0],
            }
        )

        self.solid_model(mapdl)
        mapdl.da(1, "UZ", 0)

        dalist_result = mapdl.dalist().to_dataframe()

        assert not dalist_result.empty
        assert dalist_result.compare(df_da).empty

    @requires("pandas")
    def test_fklist(self, mapdl):

        df_fk = pd.DataFrame(
            {
                "KEYPOINT": [2, 3],
                "LABEL": ["FY", "FY"],
                "REAL": [200.0, 100.0],
                "IMAG": [0.0, 0.0],
            }
        )

        self.solid_model(mapdl)
        mapdl.fk(2, "FY", 200)
        mapdl.fk(3, "FY", 100)

        fklist_result = mapdl.fklist().to_dataframe()

        assert not fklist_result.empty
        assert fklist_result.compare(df_fk).empty

    @requires("pandas")
    def test_sfllist(self, mapdl):

        df_sfl = pd.DataFrame(
            {
                "LINE": [2, 3],
                "LABEL": ["PRES", "PRES"],
                "VALI": [50.0, 50.0],
                "VALJ": [500.0, 500.0],
            }
        )

        self.solid_model(mapdl)
        mapdl.sfl(2, "PRES", 50, 500)
        mapdl.sfl(3, "PRES", 50, 500)

        sfllist_result = mapdl.sfllist().to_dataframe()

        assert not sfllist_result.empty
        assert sfllist_result.compare(df_sfl).empty

    @requires("pandas")
    def test_bfklist(self, mapdl):

        df_bfk = pd.DataFrame(
            {
                "KEYPOINT": [2],
                "LABEL": ["TEMP"],
                "VALUE": [10.0],
            }
        )

        self.solid_model(mapdl)
        mapdl.bfk(2, "TEMP", 10)

        bfklist_result = mapdl.bfklist().to_dataframe()

        assert not bfklist_result.empty
        assert bfklist_result.compare(df_bfk).empty

    @requires("pandas")
    def test_bfllist(self, mapdl):

        df_bfl = pd.DataFrame(
            {
                "LINE": [3],
                "LABEL": ["TEMP"],
                "VALUE": [15.0],
            }
        )

        self.solid_model(mapdl)
        mapdl.bfl(3, "TEMP", 15)

        bfllist_result = mapdl.bfllist().to_dataframe()

        assert not bfllist_result.empty
        assert bfllist_result.compare(df_bfl).empty

    @requires("pandas")
    def test_bfalist(self, mapdl):

        df_bfa = pd.DataFrame(
            {
                "AREA": [1],
                "LABEL": ["TEMP"],
                "VALUE": [20.0],
            }
        )

        self.solid_model(mapdl)
        mapdl.bfa(1, "TEMP", 20)

        bfalist_result = mapdl.bfalist().to_dataframe()

        assert not bfalist_result.empty
        assert bfalist_result.compare(df_bfa).empty


class Test_bc_cmdlist_model:

    def solid_model(self, mapdl):
        # Solid model (Geometry)

        mapdl.clear()

        mapdl.prep7()

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

    def fe_model(self, mapdl):
        # FE model (Mesh)

        self.solid_model(mapdl)

        mapdl.esize(0.02)
        mapdl.mshape(0, "2D")
        mapdl.mshkey(0)
        mapdl.amesh(1, 1, 1)

    @requires("pandas")
    def test_dlist(self, mapdl):

        df_d = pd.DataFrame(
            {
                "NODE": [2, 2],
                "LABEL": ["UX", "UY"],
                "REAL": [0.0, 0.0],
                "IMAG": [0.0, 0.0],
            }
        )

        self.fe_model(mapdl)
        mapdl.d(2, "UX", 0)
        mapdl.d(2, "UY", 0)

        dlist_result = mapdl.dlist().to_dataframe()

        assert not dlist_result.empty
        assert dlist_result.compare(df_d).empty

    @requires("pandas")
    def test_flist(self, mapdl):

        df_f = pd.DataFrame(
            {
                "NODE": [4, 4],
                "LABEL": ["FX", "FY"],
                "REAL": [10.0, 20.0],
                "IMAG": [0.0, 0.0],
            }
        )

        self.fe_model(mapdl)
        mapdl.f(4, "FX", 10)
        mapdl.f(4, "FY", 20)

        flist_result = mapdl.flist().to_dataframe()

        assert not flist_result.empty
        assert flist_result.compare(df_f).empty


class Test_MAPDL_commands:
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
        "mwrite",
        "nplot",
        "sys",
        "vplot",
        "vwrite",
    ]

    @staticmethod
    def fake_wrap(*args, **kwags):
        return args[0]

    MAPDL_cmds = [each for each in dir(Commands) if not each.startswith("_")]

    @pytest.mark.parametrize("cmd", MAPDL_cmds)
    @patch("ansys.mapdl.core.mapdl_grpc.MapdlGrpc._send_command", fake_wrap)
    # Skip post processing the plot in PLESOL commands like.
    @patch("ansys.mapdl.core.mapdl_core.PLOT_COMMANDS", [])
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
        wrapped = False
        while hasattr(func, "__wrapped__"):
            func = func.__wrapped__
            wrapped = True

        if cmd in self.SKIP:
            pytest.skip("This function is overwritten in a subclass.")

        parm = inspect.signature(func).parameters
        assert "kwargs" in parm, "'kwargs' argument is missing in function signature."

        args = [f"arg{i}" for i in range(len(parm) - 1)]  # 3 = self, cmd, kwargs

        if list(parm)[0].lower() == "self":
            args = args[:-1]
            post = func(mapdl, *args)
        else:
            post = func(*args)

        for arg in args:
            assert arg in post
