"""
This script convert the file in `gmsh` format to ANSYS `CDB` format.
"""

from ansys.mapdl.reader import save_as_archive
import pyvista as pv

filename = "from_gmsh.msh"
mesh = pv.read_meshio(filename)
# mesh.plot()  # optionally plot the mesh
mesh.points /= 1000
save_as_archive("archive.cdb", mesh)
