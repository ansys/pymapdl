"""
.. _ref_sector_model:

Shaft Modal Analysis
~~~~~~~~~~~~~~~~~~~~

Visualize a full cyclic model

"""
import pyansys

###############################################################################
# load a sector modal analysis file
rotor = pyansys.download_sector_modal()
print(rotor)


###############################################################################
# plot the rotor
rotor.plot(smooth_shading=True)


###############################################################################
# plot a sector of the rotor
rotor.mas_grid.plot(color='w', smooth_shading=True)


###############################################################################
# plot a nodal solution
rotor.plot_nodal_solution(0)


###############################################################################
# animate a mode
rotor.animate_nodal_solution(10, loop=False)
# set loop to True to enable continuous plotting
