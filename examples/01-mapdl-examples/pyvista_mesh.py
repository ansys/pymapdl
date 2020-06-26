"""
.. _ref_pyvista_mesh:

PyVista Mesh Integration
~~~~~~~~~~~~~~~~~~~~~~~~

Run a modal analysis from a mesh generated from pyvista within MAPDL

"""
import os
import pyvista as pv
import pyansys

# launch MAPDL and run a modal analysis
mapdl = pyansys.launch_mapdl(loglevel='WARNING', override=True)

# Create a simple plane mesh centered at (0, 0, 0) on the XY plane
mesh = pv.Plane(i_resolution=100, j_resolution=100)

mesh.plot(color='w', show_edges=True)
 
###############################################################################
# Write the mesh to an archive file
archive_filename = os.path.join(mapdl.path, 'tmp.cdb')
pyansys.save_as_archive(archive_filename, mesh)


###############################################################################
# mapdl = pyansys.launch_mapdl(prefer_pexpect=True, override=True)

# Read in the archive file
response = mapdl.cdread('db', archive_filename)
mapdl.prep7()
print(mapdl.shpp('SUMM'))

# specify shell thickness
mapdl.sectype(1, "shell")
mapdl.secdata(0.01)
mapdl.emodif('ALL', 'SECNUM', 1)

# specify material properties
# using aprox values for AISI 5000 Series Steel
# http://www.matweb.com/search/datasheet.aspx?matguid=89d4b891eece40fbbe6b71f028b64e9e
mapdl.units('SI')  # not necessary, but helpful for book keeping
mapdl.mp('EX', 1, 200E9)  # Elastic moduli in Pa (kg/(m*s**2))
mapdl.mp('DENS', 1, 7800)  # Density in kg/m3
mapdl.mp('NUXY', 1, 0.3)  # Poissons Ratio
mapdl.emodif('ALL', 'MAT', 1)

# Run an unconstrained modal analysis
mapdl.run('/SOLU')
mapdl.antype('MODAL')  # default NEW
mapdl.modopt('LANB', 20, 1)  # First 6 modes above 1 Hz
mapdl.solve()

###############################################################################
# Load the result file within pyansys
result = mapdl.result

# Plot the 8th mode
result.plot_nodal_displacement(7, show_displacement=True, displacement_factor=0.4)

###############################################################################
# plot the 1st mode using contours
result.plot_nodal_displacement(0, show_displacement=True,
                               displacement_factor=0.4, n_colors=10)

###############################################################################
# Animate a high frequency mode
result.animate_nodal_displacement(18, loop=False, add_text=False,
                                  nangles=30, max_disp=0.2, show_axes=False,
                                  background='w',
                                  movie_filename='plane_vib.gif')

# Get a smoother plot by disabling movie_filename and increasing `nangles`
# also, enable a continous plot with `loop=True`

