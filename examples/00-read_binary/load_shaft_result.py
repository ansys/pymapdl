"""
.. _ref_load_shaft_result:

Shaft Modal Analysis
~~~~~~~~~~~~~~~~~~~~

Visualize a shaft modal analysis

"""
# sphinx_gallery_thumbnail_number = 6

import pyansys

# Download an example shaft modal analysis result file
shaft = pyansys.download_shaft_modal()

###############################################################################
# Geometry is stored as a class
print(shaft.geometry)

###############################################################################
# ...as a VTK object
print(shaft.grid)

###############################################################################
# Plot the shaft
shaft.plot()

# list shaft node components
###############################################################################
print(shaft.element_components.keys())

###############################################################################
# Plot a node component
cpos = [(-115.35773008378118, 285.36602704380107, -393.9029392590675),
        (126.12852038381345, 0.2179228023931401, 5.236408799851887),
        (0.37246222812978824, 0.8468424028124546, 0.37964435122285495)]
shaft.plot(element_components=['SHAFT_MESH'], cpos=cpos)
# get cpos from cpos = shaft.plot()


###############################################################################
# Plot a node component as a wireframe
shaft.plot(element_components=['SHAFT_MESH'], cpos=cpos, style='wireframe',
           lighting=False)


###############################################################################
# Plot the shaft with edges and with a blue color
shaft.plot(show_edges=True, color='cyan')

###############################################################################
# Plot the shaft without lighting but with edges and with a blue color
shaft.plot(lighting=False, show_edges=True, color='cyan')


###############################################################################
# plot a mode shape without contours
shaft.plot_nodal_solution(1, element_components=['SHAFT_MESH'],
                          show_displacement=True, max_disp=10, overlay_wireframe=True,
                          cpos=cpos)

###############################################################################
# plot a mode shape with contours
shaft.plot_nodal_solution(1, element_components=['SHAFT_MESH'], n_colors=10,
                          show_displacement=True, max_disp=10, overlay_wireframe=True,
                          cpos=cpos)

###############################################################################
# Animate a mode of a component the shaft
shaft.animate_nodal_solution(5, element_components='SHAFT_MESH', comp='norm',
                             max_disp=10, show_edges=True, cmap='bwr', cpos=cpos,
                             loop=False, movie_filename='demo.gif', nangles=30)

# set loop to True to plot continiously
# Disable movie_filename and increase nangles for a smoother plot
