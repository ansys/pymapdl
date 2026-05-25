# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Using ``gmsh``, read the STEP file, mesh it, and save it as a MSH file."""

import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add("t20")

# Load a STEP file (using `importShapes' instead of `merge' allows to directly
# retrieve the tags of the highest dimensional imported entities):
filename = "pf_coil_case_1.stp"
v = gmsh.model.occ.importShapes(filename)


# Get the bounding box of the volume:
gmsh.model.occ.synchronize()

# Specify a global mesh size and mesh the partitioned model:
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 10)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", 10)
gmsh.model.mesh.generate(3)
gmsh.write("from_gmsh.msh")

gmsh.finalize()
