"""
Build static beam to grab boundary conditions
"""

import os

import pyansys
from pyansys import examples

os.environ["I_MPI_SHM_LMT"] = "shm"  # necessary on ubuntu
mapdl = pyansys.launch_mapdl(override=True, additional_switches="-smp")

mapdl.cdread("db", examples.hexarchivefile)
mapdl.esel("s", "ELEM", vmin=5, vmax=20)
mapdl.cm("ELEM_COMP", "ELEM")
mapdl.nsel("s", "NODE", vmin=5, vmax=20)
mapdl.cm("NODE_COMP", "NODE")

# boundary conditions
mapdl.allsel()

# dummy steel properties
mapdl.prep7()
mapdl.mp("EX", 1, 200e9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
mapdl.mp("NUXY", 1, 0.3)  # Poissons Ratio
mapdl.emodif("ALL", "MAT", 1)

# fix one end of the beam
# mapdl.nsel('S', 'LOC', 'Z')
# mapdl.d('all', 'all')
# mapdl.allsel()

# mapdl.eplot(vtk=True, show_axes=True)
# mapdl.nodes[:, 2].max()
# mapdl.nnum[mapdl.nodes[:, 2] == 2.5]

mapdl.d(3, "ALL")

mapdl.d(25, "UX", 0.001)
mapdl.d(26, "UY", 0.0011)
mapdl.d(27, "UZ", 0.0012)

mapdl.f(52, "FX", 20)
mapdl.f(71, "FY", 30)
mapdl.f(127, "FZ", 40)

# mapdl.nsel('S', 'LOC', 'Z')
# mapdl.d('all', 'all')
# mapdl.allsel()
# 1/0

mapdl.run("/SOLU")
mapdl.antype("STATIC")
mapdl.solve()
mapdl.finish()

# mapdl.mxpand(elcalc='YES')
# mapdl.modal_analysis(nmode=6)
# mapdl.exit()

# # view the results using pyansys's result viewer
# result = mapdl.result
# result.animate_nodal_solution(0, show_edges=True, loop=False, displacement_factor=10,
#                               movie_filename='demo.gif')
