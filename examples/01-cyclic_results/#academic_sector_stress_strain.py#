"""
.. _ref_academic_sector:

Stress and Strain from a Cyclic Modal Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example shows how to extract strain and stress from a cyclic
modal analysis.

"""
# sphinx_gallery_thumbnail_number = 2

import numpy as np
import pyansys

###############################################################################
# Download the academic modal analysis file
# rotor = pyansys.download_academic_rotor_result()
rotor = pyansys.read_binary('/tmp/ansys2/file.rst')
print(rotor)


###############################################################################
# Plot nodal displacement for result ``(2, 2)``, which corresponds to
# the load step and sub step in fortran indexing.  You could have also
# used the python cumulative index 3.
# rotor._positive_cyclic_dir = True
_ = rotor.plot_nodal_displacement((2, 2), 'x', cpos='xy')


###############################################################################
# Extract the nodal elastic strain for the fourth cumulative result.
# Because pyansys uses zero based indexing, we have to input "3" here.
#
# Depending on the version of ANSYS, MAPDL either does or does not write the duplicate sector for a result.  If MAPDL does not write a duplicate sector, pyansys will search for a duplicate mode and use that as the duplicate sector in order to be able to expand to the full rotor.  Regardless of if there is or isn't a duplicate sector, only the master sector will be output.
# 
# .. warning::
#     Cyclic results extracted from pyansys may disagree with MAPDL
#     due to several issues/variations when extracting cyclic results
#     within MAPDL using ``PowerGraphics``.  By default, MAPDL uses
#     ``\EDGE,,,45``, which disables averaging across surface features
#     that exceed 45 degrees.  On the other hand ``pyansys`` always
#     averages, so you will see differences between MAPDL and
#     ``pyansys`` in these cases.


nnum, strain = rotor.nodal_elastic_strain(3, full_rotor=True)



###############################################################################
# Plot nodal elastic strain for result ``(2, 2)``.
#
# Note how the strains are not averaged across cyclic sector boundaries
_ = rotor.plot_nodal_elastic_strain((2, 2), 'x', cpos='xy')
# _ = rotor.plot_nodal_solution((2, 2), 'x', cpos='xy')


# ###############################################################################
# # Rotor Sector Order
# # ~~~~~~~~~~~~~~~~~~
# # 
# # Note that the sector rotations follow the right-hand rule where the
# # X-axis and Y-axis make up the horizontal plane and the Z-axis is
# # vertical and positive upwards.  Rotation follows the right-hand
# # rule, which looks anti-clockwise when looking downward onto the XY
# # plane.
# #

# _ = rotor.plot_sectors(cpos='xy', stitle='Sector', smooth_shading=True, cmap='bwr')


# ###############################################################################
# # Plot Nodal Displacement
# #
# # This modal analysis contains two modes for each harmonic index.
# # Since this is a 24 sector rotor, it will contain the harmonic
# # indices from 0 to N/2, which in this case is 12


# # Print the harmonic indices with
# print(rotor.harmonic_indices)

# ###############################################################################
# # You can refer to the result set either using MAPDL's 1-based indexing
# # which is (Load-step, sub-step).
# _ = rotor.plot_nodal_displacement((2, 2), comp='norm', cpos='xy')

# ###############################################################################
# # Alternatively, you can refer to the results using cumulative indexing.
# _ = rotor.plot_nodal_displacement(10, comp='norm', cpos='xy')


# ###############################################################################
# # Understanding Harmonic Indexing
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #
# # ANSYS has great documentation on harmonic indexing within their
# # internal documentation, but for the sake of completeness it will be repeated here.
# # 
# # The harmonic index used within MAPDL is an integer that determines
# # the variation in the value of a single degree of freedom at points
# # spaced at a circumferential angle equal to the sector angle.
# #
# # For this academic rotor, when the number of "blades" equals the
# # number of MAPDL sectors, the harmonic index will always match the
# # nodal diameter.  For example, the cumulative result 10 has a
# # harmonic index of 5:

# rnum = 10
# print('Harmonic Index:', rotor.harmonic_indices[rnum])


# # For the purpose of illustrating the nodal diameter content, we
# # restrict the displacement to a narrow range and force the lower and
# # upper ranges of the plot to indicate the phase of the displacement
# #
# # In this plot you can clearly see that the harmonic index is indeed 5
# # as five, and only 5 lines can be drawn through the node lines
# # spanning the circumference of the rotor.
# r = 0.55
# _ = rotor.plot_nodal_displacement(rnum, comp='norm', cpos='xy', rng=[r, r + 1E-2],
#                                   stitle=None, add_text=False, cmap='bwr')


# ###############################################################################
# # The same can be done for the simpler nodal diameter 1
# rnum = 3
# print(rotor.harmonic_indices[rnum])

# r = 0
# _ = rotor.plot_nodal_displacement(rnum, comp='z', cpos='xy', rng=[r, r + 1E-2],
#                                   add_text=False, stitle=None, cmap='bwr')


# # Therefore for this rotor with the number of sectors (N) equaling the
# # number of blades, for each harmonic index there can only be one
# # corresponding nodal diameter


# ###############################################################################
# # Multi-Bladed Sectors
# # ~~~~~~~~~~~~~~~~~~~~
# #
# # When there are multiple blades per sector as in the case of the
# # following example, the relationship between the harmonic indices and
# # nodal diameters becomes more complicated
# #
# # In this case, we use the following equation described in the MAPDL
# # Cyclic Analysis Guide:
# # d = m*N ± k
# #
# # where:
# # - d is the nodal diameter
# # - N is the number of sectors
# # - k is the harmonic index
# # - m is a set of integers from 0 to infinity
# # 
# # Therefore, for a 6 sector rotor, the first 4 possible nodal diameters at
# # harmonic index 1 are:

# N = 6  # number of sectors
# k = 1  # harmonic index
# print('Nodal Diameters :')
# for m in range(5):
#     if m > 0:
#         print('%4d' % (m*N - k))
#     print('%4d' % (m*N + k))

# ###############################################################################
# # Normally for a rotor where the number of blades per sector is 1,
# # nodal diameters higher than N are simply aliased back to 1 and these
# # solutions do not appear in the results.  However, when the sector
# # contains multiple blades per sector, these results do appear in the
# # analysis since they are not aliased back into a repeated mode.

# # Therefore in this example part of the above modes will be
# # back-aliased for a 24 blade, 6 sector rotor, and these can be
# # computed with:

# n_blades = 24  # 4 blades per sector
# nodal_diameters = []
# for m in range(5):
#     if m > 0:
#         nodal_diameters.append(m*N - k)
#     nodal_diameters.append(m*N + k)

# print('Nodal Diameters :')
# for d in nodal_diameters:
#     if d > n_blades:  # ignore
#         continue
#     elif d > n_blades//2:  # back alias
#         print('%4d' % -(n_blades-d))
#     else:
#         print('%4d' % d)


# ###############################################################################
# # Plot the Multi-Bladed Sector
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #
# # We can verify these results by analyzing a multi-sector rotor

# multi_blade_rotor = pyansys.read_binary('/home/alex/python/pyansys-data/data/academic_rotor_4_blade.rst')

# # multi_blade_rotor = pyansys.download_academic_rotor_4blade_result()

# # plot all the sectors
# _ = multi_blade_rotor.plot_sectors(cpos='xy', stitle='Sector',
#                                    smooth_shading=True, cmap='bwr')

# ###############################################################################
# # We can then see that the harmonic indices for harmonic index 1
# # indeed alias back to the expected nodal diameters in the following
# # plots.
# print(multi_blade_rotor.harmonic_indices)

# hi_1 = np.nonzero(multi_blade_rotor.harmonic_indices == 1)[0]
# print('Cumlative indices matching harmonic index 1:', hi_1)

# ###############################################################################
# # Cumulative result 8 and harmonic index 1
# rnum = 8
# text = 'Expected Nodal Diameter %2d' % nodal_diameters[0]
# _ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
#                                               cpos='xy', rng=[r, r + 1E-2],
#                                               add_text=text, stitle=None,
#                                               cmap='bwr')


# ###############################################################################
# # Cumulative result 10 and harmonic index 5
# rnum = 10
# text = 'Expected Nodal Diameter %2d' % nodal_diameters[1]
# _ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
#                                               cpos='xy', rng=[r, r + 1E-2],
#                                               add_text=text, stitle=None,
#                                               cmap='bwr')


# ###############################################################################
# # Cumulative result 13 and harmonic index 7
# rnum = 13
# text = 'Expected Nodal Diameter %2d' % nodal_diameters[2]
# _ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
#                                               cpos='xy', rng=[r, r + 1E-2],
#                                               add_text=text, stitle=None,
#                                               cmap='bwr')


# ###############################################################################
# # Cumulative result 15 and harmonic index 11
# rnum = 15
# text = 'Expected Nodal Diameter %2d' % nodal_diameters[3]
# _ = multi_blade_rotor.plot_nodal_displacement(rnum, comp='z',
#                                               cpos='xy', rng=[r, r + 1E-2],
#                                               add_text=text, stitle=None,
#                                               cmap='bwr')

