"""
Things to fill
"""

from ansys.mapdl.core import launch_mapdl
import numpy as np

mapdl = launch_mapdl()
print(mapdl)

# Beam dimensions
_width = 10
_height = 10
_length = 100

# Create simple 3D Cantilever Beam
mapdl.clear()
mapdl.prep7()
mapdl.mp("EX", 1, 70000)
mapdl.mp("NUXY", 1, 0.3)
mapdl.csys(0)
mapdl.blc4(0, 0, _width, _height, _length)
mapdl.et(1, "SOLID186")
mapdl.esize(5)
mapdl.vmesh("ALL")
mapdl.eplot()

mapdl.slashsolu()
mapdl.nsel("s", "loc", "z", 0)
mapdl.d("all", "all")

mapdl.nsel("s", "loc", "z", 100)
mapdl.d("all", "uy",1)
mapdl.allsel()
mapdl.solve()

mapdl.post1()
mapdl.set("last")

#Get Node Count
ncount = len(mapdl.mesh.nnum)

#Create dummy arrays of length as node count and with all values = 1 
dispx_np = np.ones(ncount)
dispy_np = np.ones(ncount)
dispz_np = np.ones(ncount)

arr = np.array([10, 20, 30])
mapdl.set_parameter_array(arr, 'MYARR')

mapdl.set_parameter_array(dispx_np, 'dispx')
mapdl.set_parameter_array(dispy_np, 'dispy')
mapdl.set_parameter_array(dispz_np, 'dispz')

#Convert Numpy Arrays to APDL arrays
#mapdl.dim("dispx","array",ncount)
#mapdl.parameters['dispx'] = dispx_np
#mapdl.dim("dispy","array",ncount)
#mapdl.parameters['dispy'] = dispy_np
#mapdl.dim("dispz","array",ncount)
#mapdl.parameters['dispz'] = dispz_np

#Replace Ux, Uy and Uz results with User-defined Arrays DispX, DispY and Disp Z
mapdl.starvput("dispx","node",1,"u","x")
mapdl.starvput("dispy","node",1,"u","y")
mapdl.starvput("dispz","node",1,"u","z")


# Plot USUM - which should be constant sqrt(1^2 + 1^2 + 1^2) = sqrt(3)
mapdl.post_processing.plot_nodal_displacement()

#Plot U Vector showing Values as Vectors and store it as a png
mapdl.view(1,0.42,0.23,0.88)
mapdl.angle(1,4.6) 
mapdl.show("png")
mapdl.plvect("u",mode="vect")
mapdl.show("close")

mapdl.exit()
