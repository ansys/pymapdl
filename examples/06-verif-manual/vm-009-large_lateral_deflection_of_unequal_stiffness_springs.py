r"""
.. _ref_vm7_example:

Plastic Compression of a Pipe Assembly
--------------------------------------
Problem Description:
 - Two coaxial tubes, the inner one of 1020 CR steel and cross-sectional
   area :math:`A_{\mathrm{s}}`, and the outer one of 2024-T4 aluminum alloy
   and of area :math:`A_{\mathrm{a}}`, are compressed between heavy, flat end plates,
   as shown below. Determine the load-deflection curve of the assembly
   as it is compressed into the plastic region by an axial displacement.
   Assume that the end plates are so stiff that both tubes are shortened by
   exactly the same amount.

Reference:
 - S. H. Crandall, N. C. Dahl, An Introduction to the Mechanics of Solids,
   McGraw-Hill Book Co., Inc., New York, NY, 1959, pg. 180, ex. 5.1.

Analysis Type(s):
 - Static, Plastic Analysis (``ANTYPE=0``)

Element Type(s):
 - Plastic Straight Pipe Element (PIPE288)
 - 4-Node Finite Strain Shell (SHELL181)
 - 3-D Structural Solid Elements (SOLID185)

.. image:: ../../_static/vm7_setup_2.png
   :width: 400
   :alt: VM7 Finite Element Models

Material Properties
 - :math:`E_{\mathrm{s}} = 26875000\,psi`
 - :math:`\sigma_{\mathrm{(yp)s}} = 86000\,psi`
 - :math:`E_{\mathrm{a}} = 11000000\,psi`
 - :math:`\sigma_{\mathrm{(yp)a}} = 55000\,psi`
 - :math:`\nu = 0.3`

.. image:: ../../_static/vm7_setup_1.png
   :width: 300
   :alt: VM7 Material Model

Geometric Properties:
 - :math:`l = 10\,in`
 - :math:`A_{\mathrm{s}} = 7\,in^2`
 - :math:`A_{\mathrm{a}} = 12\,in^2`

Loading:
 - 1st Load Step: :math:`\delta = 0.032\,in`
 - 2nd Load Step: :math:`\delta = 0.050\,in`
 - 3rd Load Step: :math:`\delta = 0.100\,in`

.. image:: ../../_static/vm7_setup.png
   :width: 300
   :alt: VM7 Problem Sketch

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

# sphinx_gallery_thumbnail_path = '_static/vm9_setup.png'

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
#

mapdl.r(1, 1)  # SPRING STIFFNESS = 1
mapdl.r(2, 8)  # SPRING STIFFNESS = 8
mapdl.r(3, "", 1.41, 1)  # C = 1.41, M = 1
mapdl.r(4, "", 2, 1)  # C = 2, M = 1


###############################################################################
#

mapdl.n(1)
mapdl.n(2, "", 10)
mapdl.n(3, "", 20)
mapdl.n(4, -1, 10)
mapdl.n(5, "", 9)


###############################################################################
#

mapdl.e(1, 2)  # ELEMENT 1 IS SPRING ELEMENT WITH STIFFNESS 1
mapdl.real(2)
mapdl.e(2, 3)  # ELEMENT 2 IS SPRING ELEMENT WITH STIFFNESS 8
mapdl.type(3)
mapdl.real(3)
mapdl.e(4, 2)  # ELEMENT 3 IS COMBINATION ELEMENT WITH C = 1.41
mapdl.type(4)
mapdl.real(4)
mapdl.e(5, 2)  # ELEMENT 4 IS COMBINATION ELEMENT WITH C = 2


###############################################################################
#

mapdl.nsel("U", "NODE", "", 2)
mapdl.d("ALL", "ALL")
mapdl.nsel("ALL")
mapdl.finish()


###############################################################################
#

mapdl.run("/SOLU")
mapdl.antype("TRANS")  # FULL TRANSIENT DYNAMIC ANALYSIS
mapdl.nlgeom("ON")  # LARGE DEFLECTION
mapdl.kbc(1)  # STEP BOUNDARY CONDITION
mapdl.f(2, "FX", 5)
mapdl.f(2, "FY", 5)
mapdl.autots("ON")
mapdl.nsubst(30)
mapdl.outpr("", "LAST")
mapdl.outpr("VENG", "LAST")
mapdl.time(15)  # ARBITRARY TIME FOR SLOW DYNAMICS


###############################################################################
#
mapdl.solve()
mapdl.finish()


###############################################################################
#

mapdl.run("/POST1")

mapdl.set("", "", "", "", 15)  # USE ITERATION WHEN TIME = 15

mapdl.etable("SENE", "SENE")  # STORE STRAIN ENERGY

mapdl.ssum()  # SUM ALL ACTIVE ENTRIES IN ELEMENT STRESS TABLE

mapdl.run("*GET,ST_EN,SSUM,,ITEM,SENE")

mapdl.prnsol("U", "COMP")  # PRINT DISPLACEMENTS IN GLOBAL COORDINATE SYSTEM

mapdl.run("*GET,DEF_X,NODE,2,U,X")

mapdl.run("*GET,DEF_Y,NODE,2,U,Y")

mapdl.run("*DIM,LABEL,CHAR,3,2")

mapdl.run("*DIM,VALUE,,3,3")

mapdl.run("LABEL(1,1) = 'STRAIN E','DEF_X (C','DEF_Y (C'")
mapdl.run("LABEL(1,2) = ', N-cm  ','m)      ','m)      '")

mapdl.run("*VFILL,VALUE(1,1),DATA,24.01,8.631,4.533")
mapdl.run("*VFILL,VALUE(1,2),DATA,ST_EN ,DEF_X,DEF_Y")
mapdl.run("*VFILL,VALUE(1,3),DATA,ABS(ST_EN/24.01), ABS(8.631/DEF_X), ABS(DEF_Y/4.533 )")


###############################################################################
#

mapdl.run("/COM")
mapdl.run("/OUT,vm9,vrt")
mapdl.run("/COM,------------------- VM9 RESULTS COMPARISON ---------------------")
mapdl.run("/COM,")
mapdl.run("/COM,                 |   TARGET   |   Mechanical APDL   |   RATIO")
mapdl.run("/COM,")
mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
mapdl.run("(1X,A8,A8,'   ',F10.3,'  ',F14.3,'   ',1F15.3)")
mapdl.run("/COM,----------------------------------------------------------------")
mapdl.run("/OUT")
mapdl.run("/GOPR")
mapdl.finish()
