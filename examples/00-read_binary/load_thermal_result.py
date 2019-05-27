"""
.. _ref_load_thermal_result:

Thermal Analysis
~~~~~~~~~~~~~~~~

Visualize the result of verification manual test 33.

"""
import pyansys

################################################################################
# Download the result file from verification manual test case 33
vm33 = pyansys.download_verification_result(33)

# get nodal thermal strain for result set 1
nnum, tstrain = vm33.nodal_thermal_strain(0)

# plot nodal thermal strain for result set 11 in the X direction
vm33.plot_nodal_thermal_strain(10, 'X', show_edges=True,
                               lighting=True, cmap='bwr', show_axes=True)

################################################################################
# Plot with contours

# Disable lighting and set number of colors to 10 to make an MAPDL-like plot
vm33.plot_nodal_thermal_strain(10, 'X', show_edges=True, n_colors=10,
                               interpolate_before_map=True,
                               lighting=False, show_axes=True)
