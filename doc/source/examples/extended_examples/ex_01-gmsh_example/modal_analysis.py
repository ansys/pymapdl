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

"""Import the CDB database, setup modal analysis and run it."""

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl(override=True, additional_switches="-smp")
filename = "archive.cdb"
mapdl.cdread("db", filename)
mapdl.save()

# verify cells are valid
mapdl.prep7()
mapdl.shpp("SUMM")

# specify material properties
# using approximated values for AISI 5000 Series Steel
mapdl.units("SI")
mapdl.mp("EX", 1, 200e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7700)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poissons Ratio
mapdl.et(1, 181)  # ! ET,1,SHELL181 ! SHELL181
mapdl.keyopt(
    1, 3, 2
)  # ! Option for the shell. Integration option: 'Full integration with incompatible modes'
mapdl.sectype(1, "SHELL")
mapdl.secdata(1, 1, 0, 3)  # ! which means: SECDATA,TK, MAT, THETA, NUMPT, LayerName
mapdl.emodif("ALL", "MAT", 1)  # ! Setting material id
mapdl.emodif("ALL", "REAL", 1)  # ! Setting real constant

# By setting the section type (`SECTYPE`) the model will run and solve.

# The model has solid and shell elements.
# We don't need both, hence I'm going to delete the shell elements.
mapdl.esel("S", "type", "", 4)  # selecting elements with type 4 = shell181
mapdl.edele("all")
mapdl.allsel()

# Run an unconstrained modal analysis
mapdl.run("/SOLU")
mapdl.outres("all")
mapdl.antype("MODAL")  # default NEW
mapdl.modopt("LANB", 20, 1)
mapdl.solve(verbose=False)
mapdl.save("solved")

mapdl.post1()
mapdl.set("FIRST")

result = mapdl.result

result.animate_nodal_displacement(
    4,
    show_edges=False,
    lighting=True,
    loop=True,
    add_text=False,
    nangles=30,
    # displacement_factor=50,
    n_frames=100,
    movie_filename="animation.gif",
)

mapdl.exit()
