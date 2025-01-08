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

"""
.. _ref_xpl_example:

Binary MAPDL File Explorer
--------------------------

This tutorial will demonstrate how to explore the content of binary
files generated by a MAPDL Session and extract pertinent records.

These files include most of the binary files generated by APDL
(e.g. `.RST`, `.FULL`, etc.).

"""

from ansys.mapdl.core import launch_mapdl

# Start MAPDL as a service and disable all but error messages.
from ansys.mapdl.core.examples import vmfiles

mapdl = launch_mapdl()

# A specific property under the mapdl class is dedicated for XPL. It's
# based on the APDLMath `*XPL` command.
xpl = mapdl.xpl

# Many commands are directly accessible through the xpl class:
help(xpl)


###############################################################################
# Open and explore a file
# ~~~~~~~~~~~~~~~~~~~~~~~
# First you need to open an existing file.  We can create an example
# result file by running a verification manual input file and then
# opening the result file that it creates.
#
# NOTE: for now only one file can be opened at a time

# run Verification Manual 1 and opening the result file it creates
mapdl.input(vmfiles["vm1"])
print(xpl.open("file.rst"))

###############################################################################
# Using the `list` function, you can list the records available at
# the current level.
#
print(xpl.list())


###############################################################################
# Using the `step` and `up` functions, you can go down into a specific
# branch of the tree, or go up to the top level
xpl.step("GEO")
print(xpl.list())


###############################################################################
# Display where you are in the tree or records:
#
print(xpl.where())


###############################################################################
# Go up one level to move back to the top and then list the records at
# the current point.
xpl.up()
print(xpl.list())


###############################################################################
# Read a record into an APDLMath Vector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The `info` method will give you information about a record
# (e.g. length, data type, etc.)
#
# Using the `read` method, you can read a specific record and fill an
# APDLMath object.
#
print(xpl.info("DOF"))
v = xpl.read("DOF")
print(v)


###############################################################################
# To get this vector into a NumPy array you need to explicitly use `asarray`:
#
nod = v.asarray()
print(nod)


###############################################################################
# Read the first nodal solution
# First we go into the first solution set
#
print(xpl.goto("DSI::SET1"))
print(xpl.list())


###############################################################################
# Then we read the Nodal solution vector `"NSL"` into a numpy array
#
u = xpl.read("NSL")
un = u.asarray()
print(un)


###############################################################################
# Close an opened file
print(xpl.close())


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
