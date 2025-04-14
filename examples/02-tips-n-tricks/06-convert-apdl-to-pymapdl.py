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

'''
.. _ref_converting_apdl_to_pymapdl:

==================================
Converting APDL scripts to PyMAPDL
==================================

There two methods to convert APDL scripts to PyMAPDL ones in PyMAPDL,

* `convert_apdl_block()`
* `convert_script()`

which work with strings and files respectively.

This example considers a modified version of the APDL verification example 45
as the source to be converted.
'''

from ansys.mapdl.core import launch_mapdl, convert_script, convert_apdl_block
import tempfile

# start MAPDL
mapdl = launch_mapdl()

apdl_script = """
/COM,ANSYS MEDIA REL. 2023R2 (05/12/2023) REF. VERIF. MANUAL: REL. 2023R2
/VERIFY,VM45
/PREP7
/TITLE, VM45, NATURAL FREQUENCY OF A SPRING-MASS SYSTEM
C*** VIBRATION THEORY AND APPLICATIONS, THOMSON, 2ND PRINTING, PAGE 6, EX. 1.2-2
ANTYPE,MODAL
MODOPT,LANB,1
ET,1,COMBIN14,,,2     ! TWO-DIMENSIONAL LONGITUDINAL SPRING
ET,2,MASS21,,,4       ! TWO-DIMENSIONAL MASS
R,1,48
R,2,.006477
N,1
N,2,,1
E,1,2
TYPE,2
REAL,2
E,2
OUTPR,ALL,1
OUTRES,ALL,0
D,1,ALL
D,2,UX
FINISH
/SOLU    
SOLVE
*GET,FREQ,MODE,1,FREQ
*DIM,LABEL,CHAR,1,2
*DIM,VALUE,,1,3
LABEL(1,1) = '      F,'
LABEL(1,2) = ' (Hz)   '
*VFILL,VALUE(1,1),DATA,13.701
*VFILL,VALUE(1,2),DATA,FREQ 
*VFILL,VALUE(1,3),DATA,ABS(FREQ/13.701)
/COM
/OUT,vm45,vrt
/COM,------------------- VM45 RESULTS COMPARISON ---------------
/COM,
/COM,                 |   TARGET   |   Mechanical APDL   |   RATIO
/COM,
*VWRITE,LABEL(1,1),LABEL(1,2),VALUE(1,1),VALUE(1,2),VALUE(1,3)
(1X,A8,A8,'   ',F10.3,'  ',F14.3,'   ',1F15.3)
/COM,-----------------------------------------------------------

/OUT
FINISH
*LIST,vm45,vrt
"""


###############################################################################
# Convert 'inline'
# ~~~~~~~~~~~~~~~~
# Calling `convert_apdl_block()` converts the supplied string to a list of translated
# lines of code.
#

result = convert_apdl_block(apdl_script)
print(result)

###############################################################################
# Quality of Life kwargs
# ~~~~~~~~~~~~~~~~~~~~~~
# This function also includes several kwargs that cover common use cases when converting 
# from APDL to PyMAPDL, such as adding the necessary python imports when `add_imports`
# is set to True, or adding an `mapdl.exit()` to the end when `auto_exit` is set to True.
# Some of the most useful commands are below.
#
# * `print_com` - change `/COM` commands to `print()`
# * `clear_at_start` - call `mapdl.clear()` after `launch_mapdl`
# * `add_imports` - add Python import lines at the start of the script
# * `auto_exit` - When True, this appends a `mapdl.exit()` to the end of the file
# * `cleanup_output` - when True format output using `autopep8` (if you have it installed)
#

result = convert_apdl_block(apdl_script, print_com=True, clear_at_start=True,
                             add_imports=True, auto_exit=True)
print(result)

###############################################################################
# Converting from file
# ~~~~~~~~~~~~~~~~~~~~
# The function `convert_script` is also available and covers all the same functionality
# but converts from a file to a list of translated strings, and provides the 
# additional option to save the result to file  automatically. This functionality 
# is not available in `convert_apdl_block()`.
#

new_file, filename = tempfile.mkstemp(suffix='.inp')
with open(filename, 'w') as f:
    f.write(apdl_script)
print(filename)
result = convert_script(filename, print_com=True, clear_at_start=True,
                        add_imports=True, auto_exit=True)
print('\n'.join(result))


mapdl.exit()
