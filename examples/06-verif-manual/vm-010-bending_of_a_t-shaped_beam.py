r"""
.. _ref_vm10_example:

Bending of a Tee-Shaped Beam
----------------------------
Problem Description:
 - Find the maximum tensile and compressive bending stresses in
   an unsymmetric ``T-beam`` subjected to uniform bending :math:`M_z`, with dimensions
   and geometric properties as shown below.

Reference:
 - S. H. Crandall, N. C. Dahl, An Introduction to the Mechanics of Solids,
   McGraw-Hill Book Co., Inc., New York, NY, 1959, pg. 294, ex. 7.2.

Analysis Type(s):
 - Static Analysis (``ANTYPE = 0``)

Element Type(s):
 - 3-D 2 Node Beam (BEAM188)

.. image:: ../../_static/vm10_setup_1.png
   :width: 400
   :alt: VM10 Geometry of Beam188 and Element Model

Material Properties
 - :math:`E = 30 \cdot 10^6 psi`
 - :math:`\nu = 0.3`

Geometric Properties:
 - :math:`h = 1.5\,in`
 - :math:`b = 8\,in`

Loading:
 - :math:`M_z = 100,000\,in-lb`

.. image:: ../../_static/vm10_setup.png
   :width: 300
   :alt: VM10 Problem Sketch

Analysis Assumptions and Modeling Notes:
 - The following tube dimensions, which provide the desired cross-sectional
   areas, are arbitrarily chosen:

   * Inner (steel) tube: inside radius = 1.9781692 in., wall thickness = 0.5 in.
   * Outer (aluminum) tube: inside radius = 3.5697185 in., wall thickness = 0.5 in.

 - The problem can be solved in three ways:

   * using ``PIPE288`` - the plastic straight pipe element
   * using ``SOLID185`` - the 3-D structural solid element
   * using ``SHELL181`` - the 4-Node Finite Strain Shell

 - In the SOLID185 and SHELL181 cases, since the problem is axisymmetric,
   only a one element :math:`\theta` -sector is modeled. A small angle :math:`\theta = 6°`
   is arbitrarily chosen to reasonably approximate the circular boundary
   with straight sided elements.
   The nodes at the boundaries have the ``UX`` (radial) degree of freedom coupled.
   In the SHELL181 model, the nodes at the boundaries additionally have
   the ``ROTY`` degree of freedom coupled.

"""

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~
# Start MAPDL and import Numpy and Pandas libraries.

# sphinx_gallery_thumbnail_path = '_static/vm10_setup.png'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ansys.mapdl.core import launch_mapdl

# Start MAPDL.
mapdl = launch_mapdl()


###############################################################################
# Pre-Processing
# ~~~~~~~~~~~~~~
# Enter verification example mode and the pre-processing routine.

mapdl.clear()
mapdl.verify()
_ = mapdl.prep7()


###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element type (a beam-type).

# Type of analysis: Static.
mapdl.antype("STATIC")

# Element type: BEAM188.
mapdl.et(1, "BEAM188")

# Special Features are defined by keyoptions of beam element:

# KEYOPT(3)
# Shape functions along the length:
# Cubic
mapdl.keyopt(1, 3, 3)  # Cubic shape function


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material.

mapdl.mp("EX", 1, 30E6)
mapdl.mp("PRXY", 1, 0.3)
print(mapdl.mplist())


###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a beam element.

sec_num = 1
mapdl.sectype(sec_num, "BEAM", "T")
mapdl.secdata(9, 20, 4, 1.5)


###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# Set up the nodes and elements. Create nodes then create elements
# between nodes.

# Define nodes
mapdl.n(1)
mapdl.n(2, 100)

# Define one node for the orientation of the beam T-section.
mapdl.n(3, "", 1)

# Print the list of the created nodes.
print(mapdl.nlist())

###############################################################################
# Define elements
mapdl.e(1, 2, 3)

# Print the list of the created elements.
print(mapdl.elist())

# Display elements with their nodes numbers.
mapdl.eplot(show_node_numbering=True, line_width=5, cpos="xy", font_size=40)


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of boundary conditions (BC).

mapdl.d(1, "ALL")
mapdl.d("ALL", "UZ", "", "", "", "", "ROTX", "ROTY")


###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Apply a distributed force of :math:`w = (10000/12) lb/in`
# in the y-direction.

# Parametrization of the bending moment.
bending_mz = 100000

# Application of the surface load to the beam element.
mapdl.f(2, "MZ", bending_mz)
_ = mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system.

# Start solution procedure.
mapdl.slashsolu()

# Define solution function.
mapdl.nsubst(1)
mapdl.outpr("ALL", 1)
_ = mapdl.solve()


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing.

# Enter the post-processing routine.
_ = mapdl.post1()


###############################################################################
# Getting Displacements
# ~~~~~~~~~~~~~~~~~~~~~
# Using :meth:`Mapdl.etable <ansys.mapdl.core.Mapdl.etable>` get the results of
# the the maximum tensile and compressive bending stresses in
# an unsymmetric ``T-beam`` with :meth:`Mapdl.get_value <ansys.mapdl.core.Mapdl.get_value>`.


mapdl.etable("STRS_B", "LS", 1)
mapdl.etable("STRS_T", "LS", 31)

mapdl.get("STRSS_B", "ELEM", 1, "ETAB", "STRS_B")
mapdl.get("STRSS_T", "ELEM", 1, "ETAB", "STRS_T")


###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Finally we have the results of the the maximum tensile and
# compressive bending stresses, which can be compared with expected target
# values:
#
# - Strain energy of the system :math:`U_{\mathrm{(energy)}} = 24.01\,N-cm`.
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
df2 = pd.DataFrame(main_columns, index=row_names)

# Apply style settings for the dataframe.
df2.style.set_table_styles([
                            {
                              "selector": "th",
                              "props": [('font-size', '16px')]
                            },
                            {
                              "selector": "td",
                              "props": [('font-size', '16px')]
                            },
                            {
                                "selector": "td:hover",
                                "props": [("background-color", "#FFF8DC")]
                            }]).set_properties(**
                                               {
                                                    "color": "black",
                                                    "text-align": "center"
                                               }).format("{:.2f}")