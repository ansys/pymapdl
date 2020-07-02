import os
from pyansys import examples
import pyansys

os.environ['I_MPI_SHM_LMT'] = 'shm'
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

mapdl.modal_analysis(nmode=1)

# view the results using pyansys's result viewer
result = mapdl.result
result.animate_nodal_solution(3, show_edges=True, loop=True)
