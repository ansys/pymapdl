"""
.. _ref_academic_sector_stress_strain:

Stress and Strain from a Cyclic Modal Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example shows how to extract strain and stress from a cyclic
modal analysis.

"""
# sphinx_gallery_thumbnail_number = 2

import pyansys

###############################################################################
# Download the academic modal analysis file
rotor = pyansys.download_academic_rotor_result()
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
# Depending on the version of ANSYS, MAPDL either does or does not
# write the duplicate sector for a result.  If MAPDL does not write a
# duplicate sector, pyansys will search for a duplicate mode and use
# that as the duplicate sector in order to be able to expand to the
# full rotor.  Regardless of if there is or isn't a duplicate sector,
# only the master sector will be output.
# 
# .. warning::
#     Cyclic results extracted from pyansys may disagree with MAPDL
#     due to several issues/variations when extracting cyclic results
#     within MAPDL using ``PowerGraphics``.  By default, MAPDL uses
#     ``\EDGE,,,45``, which disables averaging across surface features
#     that exceed 45 degrees, but only writes one value when outputting
#     with ``PRNSOL``.  On the other hand ``pyansys`` always averages,
#     so you will see differences between MAPDL and ``pyansys`` in
#     these cases.
nnum, strain = rotor.nodal_elastic_strain(3, full_rotor=True)



###############################################################################
# Plot the nodal elastic strain in the "Z" direction for result ``(5, 2)``.
#
# `pyansys` can plot the displacements while also plotting the
# stress/strain.  Since modal results may or may not be normalized,
# you will have to adjust the ``displacement_factor`` to scale up or
# down the displacement to get a reasonable looking result.  Disable
# plotting the displacement by setting ``show_displacement=False``.
#
# Additionally, you can also save screenshots by setting
# ``screenshot`` to a filename with
# ``screenshot='elastic_strain.png'``.  If you wish to do this without
# manually closing the plotting screen, set ``off_screen=True``.  This
# can help you automate saving screenshots.

_ = rotor.plot_nodal_elastic_strain((5, 2), 'Z', show_displacement=True,
                                    displacement_factor=0.01)


###############################################################################
# Plot the nodal elastic stress in the "Z" direction for this rotor.  Since this is plotting the other pair of modes for the 5th loadstep, the displacement of this response is 90 degrees out of phase of result ``(5, 2)``
#
# Available stress components are ``['Y', 'Z', 'XY', 'YZ', 'XZ']``
_ = rotor.plot_nodal_stress((5, 1), 'Z', show_displacement=True,
                            displacement_factor=0.01)


###############################################################################
# You can also plot the nodal von mises principal stress.  This plot
# shows the principal stress for result ``(5, 2)``.
#
# Available stress components are ``['S1', 'S2', 'S3', 'SINT', 'SEQV']``.
_ = rotor.plot_principal_nodal_stress((5, 2), 'SEQV', show_displacement=True,
                                      displacement_factor=0.01)
