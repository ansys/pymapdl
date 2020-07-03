"""
.. _ref_sector_model:

Cyclic Model Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize a full cyclic model

"""
# sphinx_gallery_thumbnail_number = 2

import pyansys

###############################################################################
# load a sector modal analysis file
rotor = pyansys.download_sector_modal()
rotor._positive_cyclic_dir = True  # necessary for this example
print(rotor)

###############################################################################
# plot the rotor
rotor.plot(smooth_shading=False)


###############################################################################
# plot nodal displacement for result 10
rotor.plot_nodal_displacement(9)


###############################################################################
# animate mode 11
rotor.animate_nodal_solution(10, loop=False, movie_filename='rotor_mode.gif',
                             nangles=30)
# Disable movie_filename and increase nangles for a smoother plot
