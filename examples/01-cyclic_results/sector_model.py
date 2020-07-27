"""
.. _ref_sector_model:

Cyclic Model Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~

Visualize and animate a full cyclic model.  This model is based on the
jetcat rotor.

First, load the rotor.  Notice how printing the rotor class reveals
the details of the rotor result file.
"""
# sphinx_gallery_thumbnail_number = 2
import pyansys

rotor = pyansys.download_sector_modal()
print(rotor)

###############################################################################
# Plot the rotor and rotor sectors
# 
# Note that additional keyword arguments can be passed to the plotting
# functions of ``pyansys``.  See ``help(pyvista.plot`` for the
# documentation on all the keyword arguments.
rotor.plot_sectors(cpos='xy', smooth_shading=True)
rotor.plot()


###############################################################################
# Plot nodal displacement for result 21.
#
# Note that pyansys uses 0 based cumulative indexing.  You could also
# use the (load step, sub step) ``(4, 3)``.
rotor.plot_nodal_displacement(20, show_displacement=True,
                              displacement_factor=0.001,
                              overlay_wireframe=True)  # same as (2, 4)


###############################################################################
# Animate Mode 21
# ~~~~~~~~~~~~~~~
# Disable movie_filename and increase nangles for a smoother plot
rotor.animate_nodal_solution(20, loop=False, movie_filename='rotor_mode.gif',
                             background='w', displacement_factor=0.001,
                             add_text=False,
                             nangles=30)
