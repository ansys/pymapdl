"""
.. _ref_academic_sector:

Understanding Nodal Diameters from a Cyclic Model Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example shows how to interpret modes from a cyclic analysis from
MAPDL result file from both single bladed sectors as well as
multi-bladed sectors from a modal analysis.

"""
# sphinx_gallery_thumbnail_number = 2

import numpy as np
import pyansys

###############################################################################
# Download the academic modal analysis file
rotor = pyansys.download_academic_rotor_result()
print(rotor)

###############################################################################
# Rotor Sector Order
# ~~~~~~~~~~~~~~~~~~
# 
# Note that the sector rotations follow the right-hand rule where the
# X-axis and Y-axis make up the horizontal plane and the Z-axis is
# vertical and positive upwards.  Rotation follows the right-hand
# rule, which looks anti-clockwise when looking downward onto the XY
# plane.
#

_ = rotor.plot_sectors(cpos='xy', stitle='Sector', smooth_shading=True, cmap='bwr')


###############################################################################
# Plot Nodal Displacement
#
# This modal analysis contains two modes for each harmonic index.
# Since this is a 24 sector rotor, it will contain the harmonic
# indices from 0 to N/2, which in this case is 12


# Print the harmonic indices with
print(rotor.harmonic_indices)

###############################################################################
# You can refer to the result set either using MAPDL's 1-based indexing
# which is (Load-step, sub-step).
_ = rotor.plot_nodal_displacement((2, 2), comp='norm', cpos='xy')

###############################################################################
# Alternatively, you can refer to the results using cumulative indexing.
_ = rotor.plot_nodal_displacement(10, comp='norm', cpos='xy')


###############################################################################
# Understanding Harmonic Indexing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ANSYS has great documentation on harmonic indexing within their
# internal documentation, but for the sake of completeness it will be repeated here.
# 
# The harmonic index used within MAPDL is an integer that determines
# the variation in the value of a single degree of freedom at points
# spaced at a circumferential angle equal to the sector angle.
#
# For this academic rotor, when the number of "blades" equals the
# number of MAPDL sectors, the harmonic index will always match the
# nodal diameter.  For example, the cumulative result 10 has a
# harmonic index of 5:

rnum = 10
print('Harmonic Index:', rotor.harmonic_indices[rnum])


# For the purpose of illustrating the nodal diameter content, we
# restrict the displacement to a narrow range and force the lower and
# upper ranges of the plot to indicate the phase of the displacement
#
# In this plot you can clearly see that the harmonic index is indeed 5
# as five, and only 5 lines can be drawn through the node lines
# spanning the circumference of the rotor.
r = 0.55
_ = rotor.plot_nodal_displacement(rnum, comp='norm', cpos='xy', rng=[r, r + 1E-2],
                                  stitle=None, add_text=False, cmap='bwr')


###############################################################################
# The same can be done for the simpler nodal diameter 1
rnum = 3
print(rotor.harmonic_indices[rnum])

r = 0
_ = rotor.plot_nodal_displacement(rnum, comp='z', cpos='xy', rng=[r, r + 1E-2],
                                  add_text=False, stitle=None, cmap='bwr')


# Therefore for this rotor with the number of sectors (N) equaling the
# number of blades, for each harmonic index there can only be one
# corresponding nodal diameter


###############################################################################
# Multi-Bladed Sectors
# ~~~~~~~~~~~~~~~~~~~~
#
# When there are multiple blades per sector as in the case of the
# following example, the relationship between the harmonic indices and
# nodal diameters becomes more complicated
#
# In this case, we use the following equation described in the MAPDL
# Cyclic Analysis Guide:
# d = m*N ± k
#
# where:
# - d is the nodal diameter
# - N is the number of sectors
# - k is the harmonic index
# - m is a set of integers from 0 to infinity
# 
# Therefore, for a 6 sector rotor, the first 4 possible nodal diameters at
# harmonic index 1 are:

N = 6  # number of sectors
k = 1  # harmonic index
print('Nodal Diameters :')
for m in range(5):
    if m > 0:
        print('%4d' % (m*N - k))
    print('%4d' % (m*N + k))

###############################################################################
# Normally for a rotor where the number of blades per sector is 1,
# nodal diameters higher than N are simply aliased back to 1 and these
# solutions do not appear in the results.  However, when the sector
# contains multiple blades per sector, these results do appear in the
# analysis since they are not aliased back into a repeated mode.

# Therefore in this example part of the above modes will be
# back-aliased for a 24 blade, 6 sector rotor, and these can be
# computed with:

n_blades = 24  # 4 blades per sector
nodal_diameters = []
for m in range(5):
    if m > 0:
        nodal_diameters.append(m*N - k)
    nodal_diameters.append(m*N + k)

print('Nodal Diameters :')
for d in nodal_diameters:
    if d > n_blades:  # ignore
        continue
    elif d > n_blades//2:  # back alias
        print('%4d' % -(n_blades-d))
    else:
        print('%4d' % d)


###############################################################################
# Plot the Multi-Bladed Sector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# We can verify these results by analyzing a multi-sector rotor

multi_blade_rotor = pyansys.read_binary('/home/alex/python/pyansys-data/data/academic_rotor_4_blade.rst')

# multi_blade_rotor = pyansys.download_academic_rotor_4blade_result()

# plot all the sectors
_ = multi_blade_rotor.plot_sectors(cpos='xy', stitle='Sector',
                                   smooth_shading=True, cmap='bwr')

###############################################################################
# We can then see that the harmonic indices for harmonic index 1
# indeed alias back to the expected nodal diameters in the following
# plots.
print(multi_blade_rotor.harmonic_indices)

hi_1 = np.nonzero(multi_blade_rotor.harmonic_indices == 1)[0]
print('Cumulative indices matching harmonic index 1:', hi_1)

###############################################################################
# Cumulative result 8 and harmonic index 1
rnum = 8
text = 'Expected Nodal Diameter %2d' % nodal_diameters[0]
_ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
                                              cpos='xy', rng=[r, r + 1E-2],
                                              add_text=text, stitle=None,
                                              cmap='bwr')


###############################################################################
# Cumulative result 10 and harmonic index 5
rnum = 10
text = 'Expected Nodal Diameter %2d' % nodal_diameters[1]
_ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
                                              cpos='xy', rng=[r, r + 1E-2],
                                              add_text=text, stitle=None,
                                              cmap='bwr')


###############################################################################
# Cumulative result 13 and harmonic index 7
rnum = 13
text = 'Expected Nodal Diameter %2d' % nodal_diameters[2]
_ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
                                              cpos='xy', rng=[r, r + 1E-2],
                                              add_text=text, stitle=None,
                                              cmap='bwr')


###############################################################################
# Cumulative result 15 and harmonic index 11
rnum = 15
text = 'Expected Nodal Diameter %2d' % nodal_diameters[3]
_ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
                                              cpos='xy', rng=[r, r + 1E-2],
                                              add_text=text, stitle=None,
                                              cmap='bwr')


###############################################################################
# Traveling Wave Animation
# ~~~~~~~~~~~~~~~~~~~~~~~~
# You can animate the traveling wave for a cyclic result using
# ``animate_nodal_displacement``.  For a modal result, be sure to
# modify ``displacement_factor`` to a value that properly scales the
# modal solution.  Recall that solutions to a modal analysis from
# MAPDL may or may not be scaled to unity or the mass matrix depending
# on the settings within the modal analysis.
#
# Set ``loop=True`` to allow for a continuous plot, and modify
# ``nangles`` to allow for a smoother or faster plot.  See
# ``help(pyvista.plot)`` for additional keyword arguments.
#
_ = rotor.animate_nodal_displacement((3, 1), displacement_factor=0.03,
                                     nangles=30, show_axes=False, background='w',
                                     loop=False, add_text=False,
                                     movie_filename='EO3_Mode1.gif')


###############################################################################
# Note how you can plot the backwards traveling wave by selecting the
# second mode in the mode pair ``(3, 2)`` instead of ``(3, 1)``.
#
_ = rotor.animate_nodal_displacement((3, 2), displacement_factor=0.03,
                                     nangles=30, show_axes=False, background='w',
                                     loop=False, add_text=False,
                                     movie_filename='EO3_Mode1.gif')
