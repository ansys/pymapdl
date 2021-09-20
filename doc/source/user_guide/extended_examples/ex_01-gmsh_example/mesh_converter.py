"""
This script convert the file in `gmsh` format to ANSYS `CDB` format.
"""

import pyvista as pv
from ansys.mapdl.reader import save_as_archive

filename = 'from_gmsh.msh'
mesh = pv.read_meshio(filename)
# mesh.plot()
mesh.points /= 1000
save_as_archive('archive.cdb', mesh)