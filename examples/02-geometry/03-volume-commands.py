"""
.. _ref_basic-geometry-volumes:

Volume Commands
---------------
This example shows how you can use PyMAPDL to create basic geometry
using Pythonic PREP7 volume commands.

"""

# start MAPDL and enter the pre-processing routine
from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
print(mapdl)


###############################################################################
# APDL Command: BLC4
# ~~~~~~~~~~~~~~~~~~
# Create a rectangular area or block volume by corner points.
#
# Create a block with dimensions ``1 x 2 x 10`` with one corner of
# the block at ``(0, 0)`` of the current working plane.
#
# This method returns the volume number.
mapdl.clear(); mapdl.prep7()

vnum = mapdl.blc4(1, 1, 1, 2, 10)
mapdl.vplot(show_lines=True)


###############################################################################
# APDL Command: CYL4
# ~~~~~~~~~~~~~~~~~~
# Create a half arc centered at the origin with an outer radius
# of 2 and an inner radius of 1, and a thickness of 0.55.
mapdl.clear(); mapdl.prep7()

anum = mapdl.cyl4(xcenter=0, ycenter=0, rad1=1, theta1=0, rad2=2, theta2=180,
                  depth=0.55)
mapdl.vplot(show_bounds=True)



###############################################################################
# Line IDs
# ~~~~~~~~
# Return an array of the line IDs
lnum = mapdl.geometry.lnum
lnum


###############################################################################
# Lines Geometry
# ~~~~~~~~~~~~~~~~~~~
# Get the VTK ``PolyData`` containing lines.  This VTK mesh can be
# saved or plotted.  For more details, visit https://docs.pyvista.com
lines = mapdl.geometry.lines
lines


###############################################################################
# APDL Command: KPLOT
# ~~~~~~~~~~~~~~~~~~~
# Plot colored lines while displaying the keypoint numbers.
#
# There are a variety of plotting options available for all the common
# plotting methods.

mapdl.lplot(show_keypoint_numbering=True,
            color_lines=True,
            show_line_numbering=False,
            background='black',
            show_bounds=True,
            line_width=5,
            cpos='xy',
            font_size=26)
