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
.. _ref_how_to_use_query:

Using Inline Functions (Query)
------------------------------

This example shows you how to use the inline functions in PyMAPDL.

Inline functions like ``UX`` have been implemented in PyMAPDL as methods
on the ``mapdl.inline_functions.Query`` object. In this example we set
up a simple simulation and use ``Query`` to demonstrate some of its
functionality.

First, get an instance of
:class:`ansys.mapdl.core.inline_functions.Query` below, using the
``mapdl`` property ``queries``.

"""

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

# clear at the start and enter the preprocessing routine
mapdl.clear()
mapdl.prep7()
q = mapdl.queries

###############################################################################
# Setup Mesh
# ~~~~~~~~~~
# - Assign element type ``SOLID5`` to element type 1
# - Create a cuboid ``mapdl.block`` 10 x 20 x 30 in dimension
# - Set element size to 2
# - Mesh the block
# - Plot the elements created

mapdl.et(1, "SOLID5")
mapdl.block(0, 10, 0, 20, 0, 30)
mapdl.esize(2)
mapdl.vmesh("ALL")
mapdl.eplot()

###############################################################################
# Setup Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# - Assign an Elastic modulus in the x-direction to material 1 of 21e9
# - And a poisson's ratio of 0.3
# - Select all nodes at the ``z = 30`` end of the block
# - Remove all degrees of freedom for all nodes in the selection
# - Select all nodes at the ``z = 0`` end
# - Apply a x-direction force of 10000 to all of these
# - Finish preprocessing

mapdl.mp("EX", 1, 210e9)
mapdl.mp("PRXY", 1, 0.3)
mapdl.nsel("S", "LOC", "Z", 30)
mapdl.d("ALL", "UX")
mapdl.d("ALL", "UY")
mapdl.d("ALL", "UZ")
mapdl.nsel("S", "LOC", "Z", 0)
mapdl.f("ALL", "FX", 10000)
mapdl.finish()

###############################################################################
# Setup Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# - Enter solution (``mapdl.slashsolu`` also works)
# - Set the analysis type to ``STATIC``
# - Select all nodes
# - Solve the model
# - Finish solution

mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.allsel()
mapdl.solve()
mapdl.finish(mute=True)

###############################################################################
# Post-Processing
# ~~~~~~~~~~~~~~~
# - Get the result from the ``mapdl`` instance
# - Plot the equivalent stress results
#   - Show the edges so that we can see the element boundaries
#   - Use the "plasma" colormap because it is perceptually uniform

result = mapdl.result
result.plot_principal_nodal_stress(0, "SEQV", show_edges=True, cmap="plasma")

###############################################################################
# Using ``Query``
# ~~~~~~~~~~~~~~~
# - Use ``Query`` to get the nodes nearest to (5, 0, 0) and (5, 10, 0)
# - Use the ``Query`` instance to examine the x, y, and z displacement.
# - Print the results in a formatted string.

node1 = q.node(5.0, 0.0, 0.0)
node2 = q.node(5.0, 10.0, 0.0)

for node in [node1, node2]:
    x_displacement = q.ux(node)
    y_displacement = q.uy(node)
    z_displacement = q.uz(node)

    message = f"""
    ************************
    Displacement at Node {node}:
    ************************
    X | {x_displacement}
    Y | {y_displacement}
    Z | {z_displacement}

    """
    print(message)


###############################################################################
# Stop mapdl
# ~~~~~~~~~~
#
mapdl.exit()
