"""
.. _ref_load_cylindrical_result:

Cylindrical Nodal Stress
~~~~~~~~~~~~~~~~~~~~~~~~

Visualize the nodal stress in the radial direction.  This is equivalant to setting the result coordinate system to cylindrical in MAPDL (e.g. ``RSYS, 1``).

"""
################################################################################
# Download a small result file containing the corner of a thick pipe
import pyansys
rst = pyansys.download_corner_pipe()

# obtain the cylindrical_nodal_stress
nnum, stress = rst.cylindrical_nodal_stress(0)
print(stress)

# contains results for each node in following directions
# R, THETA, Z, RTHETA, THETAZ, and RZ
print(stress.shape)

################################################################################
# plot cylindrical nodal stress in the radial direction
_ = rst.plot_cylindrical_nodal_stress(0, 'R', show_edges=True, show_axes=True)

################################################################################
# plot cylindrical nodal stress in the theta direction
_ = rst.plot_cylindrical_nodal_stress(0, 'THETA', show_edges=True, show_axes=True,
                                      add_text=False)

################################################################################
# Plot cartesian stress in the "X" direction
_ = rst.plot_nodal_stress(0, 'X', show_edges=True, show_axes=True)
