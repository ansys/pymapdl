###############################################################################
# Check the Warning with PyVista
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   Examples -> 02-geometry -> 02-areas.py
import numpy as np
from ansys.mapdl.core import launch_mapdl

# start MAPDL and enter the pre-processing routine
mapdl = launch_mapdl()
mapdl.clear()
mapdl.prep7()
print(mapdl)


###############################################################################
# APDL Command: A
# ~~~~~~~~~~~~~~~
# Create a simple triangle in the XY plane using three keypoints.

k0 = mapdl.k("", 0, 0, 0)
k1 = mapdl.k("", 1, 0, 0)
k2 = mapdl.k("", 0, 1, 0)
a0 = mapdl.a(k0, k1, k2)

# Plot areas.
mapdl.aplot(show_lines=True, line_width=5, show_bounds=True, cpos="xy")