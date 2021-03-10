"""
.. _ref_basic-geometry-volumes:

Volume Geometry
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
# Create a block with dimensions ``1 x 2 x 10`` with one corner of
# the block at ``(0, 0)`` of the current working plane.
#
# This method returns the volume number.
vnum = mapdl.blc4(1, 1, 1, 2, depth=10)
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
# Volume IDs
# ~~~~~~~~~~
# Return an array of the volume numbers.
lnum = mapdl.geometry.vnum
lnum


###############################################################################
# Volume Geometry
# ~~~~~~~~~~~~~~~
# Volume geometry can be accessed from the ``geometry.areas`` method.
volume_mesh = mapdl.geometry.areas(merge=True)
volume_mesh


###############################################################################
# Volume Selection
# ~~~~~~~~~~~~~~~~
# There are two approaches for selecting volumes, the old "legacy"
# style and the new style.  The old style is valuable for those who
# are comfortable with the existing MAPDL commands, and new style is
# useful for selecting volumes in a pythonic manner.
#
# This example generates a series of random volumes and selects them
mapdl.clear(); mapdl.prep7()


def generate_random_volume():
    start_x, start_y, height, width, depth = np.random.random(5)
    mapdl.blc4(start_x*10, start_y*10, height, width, depth)

# create 20 random volumes
for _ in range(20):
    generate_random_volume()

# Print the volume numbers
print(mapdl.geometry.vnum)


###############################################################################
# Select every other volume with the old style command.
mapdl.ksel('S', 'KP', '', 1, 20, 2)
print(mapdl.geometry.vnum)


###############################################################################
# Select every other volume with the new style command.
#
# Note that the item IDs are 1 based in MAPDL, while Python ranges are
# 0 based.
mapdl.geometry.volume_select(range(1, 21, 2))
print(mapdl.geometry.vnum)


###############################################################################
# Select volumes from a list
#
# Note that you can ``return_selected`` if you want to see what you
# have selected.  This is helpful when reselecting from existing
# areas.
#
# Note that you could use a numpy array here as well.
items = mapdl.geometry.volume_select([1, 5, 10, 20], return_selected=True)
print(items)


###############################################################################
# APDL Command: VPLOT
# ~~~~~~~~~~~~~~~~~~~
# Plot colored volumes while displaying the keypoint numbers.
#
# There are a variety of plotting options available for all the common
# plotting methods.

# mapdl.lplot(show_keypoint_numbering=True,
#             color_lines=True,
#             show_line_numbering=False,
#             background='black',
#             show_bounds=True,
#             line_width=5,
#             cpos='xy',
#             font_size=26)
