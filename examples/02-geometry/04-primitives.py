"""
.. _ref_basic-geometry-volumes:

Primitives
---------------
This example shows how you can use PyMAPDL to create basic geometry
using Pythonic PREP7 volume commands.

"""

import numpy as np
from ansys.mapdl.core import launch_mapdl

# start MAPDL and enter the pre-processing routine
mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
print(mapdl)


###############################################################################
# APDL Command: BLC4
# ~~~~~~~~~~~~~~~~~~
# Create a rectangular area or block volume by corner points.
#
# Create a ``0.5 x 0.5`` rectangle starting at ``(0.25, 0.25)``
mapdl.clear(); mapdl.prep7()

anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')


###############################################################################
# Create a block with dimensions ``1 x 2 x 10`` with one corner of
# the block at ``(0, 0)`` of the current working plane.
#
# This method returns the volume number.
mapdl.clear(); mapdl.prep7()

vnum = mapdl.blc4(1, 1, 1, 2, depth=10)
mapdl.vplot(show_lines=True)


###############################################################################
# APDL Command: CYL4
# ~~~~~~~~~~~~~~~~~~
# Creates a circular area or cylindrical volume anywhere on the working plane.
#
# Create a half arc centered at the origin with an outer radius
# of 2 and an inner radius of 1.
#
# Note that the ``depth`` keyword argument is unset, which will
# generate an area rather than a volume.  Setting depth to a value
# greater than 0 will generate a volume.
mapdl.clear(); mapdl.prep7()

anum = mapdl.cyl4(xcenter=0, ycenter=0, rad1=1, theta1=0, rad2=2, theta2=180)
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos='xy')


###############################################################################
# Create a half arc centered at the origin with an outer radius
# of 2 and an inner radius of 1, and a thickness of 0.55.
mapdl.clear(); mapdl.prep7()

anum = mapdl.cyl4(xcenter=0, ycenter=0, rad1=1, theta1=0, rad2=2, theta2=180,
                  depth=0.55)
mapdl.vplot(show_bounds=True)
