"""
.. _ref_load_shaft_result:

MAPDL 3D Beam Example
~~~~~~~~~~~~~~~~~~~~~

This is a simple example that loads an archive file containing a beam
and then runs a modal analysis using the simplified ``modal_analysis``
method.

"""

import os
from pyansys import examples
import pyansys

os.environ['I_MPI_SHM_LMT'] = 'shm'  # necessary on ubuntu
mapdl = pyansys.launch_mapdl(override=True)

mapdl.cdread('db', examples.hexarchivefile)
mapdl.esel('s', 'ELEM', vmin=5, vmax=20)
mapdl.cm('ELEM_COMP', 'ELEM')
mapdl.nsel('s', 'NODE', vmin=5, vmax=20)
mapdl.cm('NODE_COMP', 'NODE')

# boundary conditions
mapdl.allsel()

# dummy steel properties
mapdl.prep7()
mapdl.mp('EX', 1, 200E9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp('DENS', 1, 7800)  # Density in kg/m3
mapdl.mp('NUXY', 1, 0.3)  # Poissons Ratio
mapdl.emodif('ALL', 'MAT', 1)

# fix one end of the beam
mapdl.nsel('S', 'LOC', 'Z')
mapdl.d('all', 'all')
mapdl.allsel()

mapdl.mxpand(elcalc='YES')
mapdl.modal_analysis(nmode=6)
mapdl.exit()

# view the results using pyansys's result viewer
result = mapdl.result
result.animate_nodal_solution(0, show_edges=True, loop=False,
                              movie_filename='demo.gif')
