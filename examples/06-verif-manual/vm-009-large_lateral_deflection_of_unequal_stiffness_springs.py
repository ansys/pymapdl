r"""
.. _ref_vm9_example:

Large Lateral Deflection of Unequal Stiffness Springs
-----------------------------------------------------
Problem Description:
 - A two-spring system is subjected to a force :math:`F` as shown below.
   Determine the strain energy of the system and
   the displacements :math:`\delta_x` and :math:`\delta_y`.

Reference:
 - G. N. Vanderplaats, *Numerical Optimization Techniques for Engineering
   Design with Applications*, McGraw-Hill Book Co., Inc., New York,
   NY,1984, pp. 72-73, ex. 3-1.

Analysis Type(s):
 - Nonlinear Transient Dynamic Analysis (``ANTYPE = 4``)

Element Type(s):
 - Spring-Damper Elements (COMBIN14)
 - Spring-Damper Elements (COMBIN40)

.. image:: ../../_static/vm9_setup_2.png
   :width: 400
   :alt: Geometry of COMBIN14 and COMBIN40

Material Properties
 - :math:`k_1 = 8\,N/cm`
 - :math:`k_2 = 1\,N/cm`
 - :math:`m = 1`

Geometric Properties:
 - :math:`l = 10\,cm`

Loading:
 - :math:`F = 5{\sqrt[2]{2}}\,N`
 - :math:`\alpha = 45\,º`

.. image:: ../../_static/vm9_setup.png
   :width: 400
   :alt: VM9 Problem Sketch

Analysis Assumptions and Modeling Notes:
 - The solution to this problem is best obtained by adding mass and using
   the "slow dynamics" technique with approximately critical damping.
   Combination elements ``COMBIN40`` are used to provide damping
   in the :math:`X` and :math:`Y` directions. Approximate damping coefficients
   :math:`c_x` and :math:`c_y`, in the :math:`X` and :math:`Y` directions respectively,
   are determined from:

   * :math:`c_x = \sqrt[2]{k_xm}`
   * :math:`c_y = \sqrt[2]{k_ym}`

   where m is arbitrarily assumed to be unity.

 - :math:`k_x` and :math:`k_y` cannot be known before solving so are approximated
   by :math:`k_y = k_2 = 1\,N/cm` and :math:`k_x = k_y/2 = 0.5\,N/cm`,
   hence :math:`c_x = 1.41` and :math:`c_y = 2.0`. Large deflection analysis is
   performed due to the fact that the resistance to the load is a function of
   the deformed position. ``POST1`` is used to extract results from
   the solution phase.

"""

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~
# Start MAPDL and import Numpy and Pandas libraries.

# sphinx_gallery_thumbnail_path = '_static/vm9_setup.png'

import numpy as np
import pandas as pd

from ansys.mapdl.core import launch_mapdl

# Start MAPDL.
mapdl = launch_mapdl()


###############################################################################
# Pre-Processing
# ~~~~~~~~~~~~~~
# Enter verification example mode and the pre-processing routine.

mapdl.clear()
mapdl.verify()
mapdl.prep7(mute=True)


###############################################################################
# Parameterization
# ~~~~~~~~~~~~~~~~
# Parameterization block includes main variables as :
#
# * :math:`l = 10\,cm` - spring length.
# * :math:`k_1 = 8\,N/cm` - stiffness of the 1st spring.
# * :math:`k_2 = 1\,N/cm` - stiffness of the 2nd spring.
# * :math:`m = 1` - mass.
# * :math:`F = 5\sqrt[2]{2}\,N` - main load
# * :math:`\alpha = 45\,º` - force angle
# * :math:`c_x = \sqrt[2]{k_xm} = 1,41` - damping coefficient, x-direction.
# * :math:`c_y = \sqrt[2]{k_ym} = 2.0` - damping coefficient, y-direction.

# Main variables:
length = 10
k_spring1 = 8
k_spring2 = 1
c_damp_x = 1.41
c_damp_y = 2.0
mass = 1

# Fx and Fy has been obtained by the projection F on the X and Y axes.
f_x = 5
f_y = 5


###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element types.

# Element type COMBIN14.
mapdl.et(1, "COMBIN14")

# Special Features are defined by keyoptions of the element COMBIN14.
# KEYOPT(3)(2)
# Degree-of-freedom selection for 2-D and 3-D behavior:
# 2-D longitudinal spring-damper (2-D elements must lie in an X-Y plane)
mapdl.keyopt(1, 3, 2)

# Element type COMBIN40.
mapdl.et(3, "COMBIN40")

# Special Features are defined by keyoptions of the element COMBIN40.
# KEYOPT(3)(1)
# Element degrees of freedom:
# UX (Displacement along nodal X axes)
mapdl.keyopt(3, 3, 1)

# KEYOPT(6)(2)
# Mass location:
# Mass at node J
mapdl.keyopt(3, 6, 2)

# Element type COMBIN40.
mapdl.et(4, "COMBIN40")

# Special Features are defined by keyoptions of the element COMBIN40.
# KEYOPT(3)(2)
# Element degrees of freedom:
# UX (Displacement along nodal X axes)
mapdl.keyopt(4, 3, 2)

# KEYOPT(6)(2)
# Mass location:
# Mass at node J
mapdl.keyopt(4, 6, 2)

# Print the list of the elements and their attributes.
print(mapdl.etlist())


###############################################################################
# Define Real Constants
# ~~~~~~~~~~~~~~~~~~~~~
# Define damping coefficients :math:`c_x = 1.41`, :math:`c_y = 2.0` and
# stiffness values :math:`k_1 = 8\,N/cm`, :math:`k_2 = 1\,N/cm` for the
# spring elements.

# Define real constant 1 with stiffness k2.
mapdl.r(nset=1, r1=k_spring2)  # SPRING STIFFNESS = 1

# Define real constant 2 with stiffness k1.
mapdl.r(nset=2, r1=k_spring1)  # SPRING STIFFNESS = 8

# Define real constant 3 with damping coef. in X-direction and mass.
mapdl.r(nset=3, r2=c_damp_x, r3=mass)

# Define real constant 4 with damping coef. in y-direction and mass.
mapdl.r(nset=4, r2=c_damp_y, r3=mass)

# Print the real constant list.
print(mapdl.rlist())


###############################################################################
# Define Nodes
# ~~~~~~~~~~~~
# Set up the nodes coordinates using python ``for`` loop.

# Lists with nodes coordinates.
node_x_coord = [0, 0, 0, -1, 0]
node_y_coord = [0, 10, 20, 10, 9]

# Create nodes.
for i in range(0, 5):
    mapdl.n(node=i+1, x=node_x_coord[i], y=node_y_coord[i])

# Print the list of the created nodes.
print(mapdl.nlist())


###############################################################################
# Create Elements
# ~~~~~~~~~~~~~~~
# Create the elements through the nodes.

# Create  spring element COMBIN14 between nodes 1 nad 2
# with stiffness k_2 = 1 N/cm.
mapdl.type(1)
mapdl.real(1)
mapdl.e(1, 2)

# Create  spring element COMBIN14 between nodes 2 nad 3
# with stiffness k_1 = 8 N/cm.
mapdl.type(1)
mapdl.real(2)
mapdl.e(2, 3)

# Create  spring element COMBIN40 between nodes 4 nad 2
# with damping coefficient c_x = 1.41.
mapdl.type(3)
mapdl.real(3)
mapdl.e(4, 2)

# Create  spring element COMBIN40 between nodes 5 nad 2
# with damping coefficient c_y = 2.0.
mapdl.type(4)
mapdl.real(4)
mapdl.e(5, 2)

# Print the list of the created elements.
print(mapdl.elist())


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of boundary conditions (BC) for the spring model.

# Unselect the node where the force is applied.
mapdl.nsel("U", "NODE", vmin=2)

# Apply BC to the selected set of the nodes.
mapdl.d("ALL", "ALL")
mapdl.nsel("ALL")

# Finish pre-processing mode.
mapdl.finish(mute=True)


###############################################################################
# Solution settings
# ~~~~~~~~~~~~~~~~~
# Enter solution mode and apply settings for *Transient Dynamic Analysis*.

# Starts solution (/solu) mode.
mapdl.slashsolu()

# Define transient analysis with large deflection setting.
mapdl.antype("TRANS")
mapdl.nlgeom("ON")

# Specifies the stepped loading condition within a load step.
mapdl.kbc(1)

# Apply forces to the node 2.
mapdl.f(2, "FX", f_x)
mapdl.f(2, "FY", f_y)

# Uses automatic time stepping.
mapdl.autots("ON")

# Specifies the number of substeps to be taken this load step.
mapdl.nsubst(30)

# Controls the solution printout.
mapdl.outpr("", "LAST")
mapdl.outpr("VENG", "LAST")

# Sets the time for a load step.
mapdl.time(15, mute=True)


###############################################################################
# Solve
# ~~~~~
# Solve the system , avoiding the printing output.

# Run the simulation.
mapdl.solve()
mapdl.finish(mute=True)


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing, avoiding the printing output.

# Enter the post-processing mode.
mapdl.post1(mute=True)


###############################################################################
# Getting Displacements
# ~~~~~~~~~~~~~~~~~~~~~
# Enter post-processing. To get results of the strain energy and displacements
# in X and Y directions from the node where the force is applied using
# :meth:`Mapdl.get_value <ansys.mapdl.core.Mapdl.get_value>`.

# Defines the data set to be read from the results file by the time-point.
mapdl.set(time=15)

# Fills a table of element values for further processing for strain energy.
mapdl.etable("SENE", "SENE")

# Sum all active entries in element stress table.
mapdl.ssum()

# Get the value of the stain energy of the spring elements.
strain_energy = mapdl.get_value(entity="SSUM",
                                entnum=0,
                                item1="ITEM",
                                it1num="SENE")

# Prints nodal solution results of the X, Y, and Z structural displacements
# and vector sum.
print(mapdl.prnsol("U", "COMP"))

# Get the value of the displacements in X-direction.
disp_x = mapdl.get_value(entity="NODE",
                         entnum=2,
                         item1="U",
                         it1num="X")

# Get the value of the displacements in Y-direction.
disp_y = mapdl.get_value(entity="NODE",
                         entnum=2,
                         item1="U",
                         it1num="Y")


###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Finally we have the results of the strain energy and
# displacements in :math:`X` and :math:`Y` directions, which can be compared with
# expected target values:
#
# - Strain energy of the system :math:`U_{\mathrm{(energy)}} = 24.01\;N\,cm`.
# - Displacement in X-direction :math:`U_x = 8.631\,cm`.
# - Displacement in Y-direction :math:`U_y = 4.533\,cm`.
#
# For better representation of the results we can use ``pandas`` dataframe
# with following settings below:

# Define the names of the rows.
row_names = ["Strain Energy, N-cm",
             "Deflection-x , cm",
             "Deflection-y , cm"]

# Define the names of the columns.
col_names = ['Target',
             'Mechanical APDL',
             'RATIO']

# Define the values of the target results.
target_res = np.asarray([24.01, 8.631, 4.533])

# Create an array with outputs of the simulations.
simulation_res = np.asarray([strain_energy, disp_x, disp_y])

# Identifying and filling corresponding columns.
main_columns = {
    "Target": target_res,
    "Mechanical APDL": simulation_res,
    "Ratio": list(np.divide(simulation_res, target_res))
}

# Create and fill the output dataframe with pandas.
df2 = pd.DataFrame(main_columns, index=row_names).round(2)

# Apply settings for the dataframe.
df2.head()

###############################################################################
# stop mapdl
mapdl.exit()
