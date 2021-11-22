r"""
.. _ref_vm2_example:

Beam Stresses and Deflections
------------------------------------------------

Problem Description:
-   A standard 30 inch WF beam, with a cross-sectional area ``A``, is supported
    as shown below and loaded on the overhangs by a uniformly distributed
    load w. Determine the maximum bending stress in the middle portion of
    the beam and the deflection :math:`\delta` at the middle of the beam.

Reference:
   -  S. Timoshenko, Strength of Material, Part I, Elementary Theory and
   Problems, 3rd Edition, D. Van Nostrand Co., Inc., New York, NY, 1955,
   pg. 98, problem 4.

Analysis Type(s):
 - Static Analysis ``ANTYPE=0``

Element Type(s):
 - 3-D 2 Node Beam (BEAM188)

.. image:: ../../_static/vm2_setup.png
   :width: 400
   :alt: VM2 Problem Sketch

Material Properties
 - :math:`E = 30 \cdot 10^6 psi`

Geometric Properties:
 - :math:`a = 120 in`
 - :math:`l = 240 in`
 - :math:`h = 30 in`
 - :math:`A = 50.65 in^2`
 - :math:`I_z = 7892 in^4`

Loading:
 - :math:`w = (10000/12) lb/in`

Analytical Equations:
 - :math:`P = R_1 + R_2` where :math:`P` is load.
 - :math:`\frac{R_2}{R_1} = \frac{a}{b}`
   Where :math:`a` and :math:`b` are the ratios of distances between
   the load and the wall.

"""


# sphinx_gallery_thumbnail_path = '_static/vm2_setup.png'

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~

from ansys.mapdl.core import launch_mapdl

# start mapdl and clear it
mapdl = launch_mapdl()
mapdl.clear()  # optional as MAPDL just started

# enter verification example mode and the pre-processing routine
mapdl.verify()
mapdl.prep7()

###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element type (a beam-type).

mapdl.antype("STATIC")
mapdl.et(1, "BEAM188")


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material and its type (a single material, with a beam-type section).

mapdl.mp("EX", 1, 30E6)
mapdl.mp("PRXY", "", 0.3)

###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section for a beam element.

mapdl.run("SECT,1,BEAM,I")
mapdl.run("W_F=1.048394965")
mapdl.run("W_W=0.6856481")
mapdl.run("SECD,15,15,28+(2*W_F),W_F,W_F,W_W")


###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~~~~~~~~
# Set up the keypoints, nodes and elements.  This creates a mesh just like 
# in the problem setup. We create a square of nodes and use `fill` to add
# mid-point nodes to two opposite sides.

mapdl.keyopt(1, 9, 3)  # Output at 9 intermediate locations
mapdl.keyopt(1, 3, 3)  # Cubic shape function
mapdl.n(1)  # Define nodes
mapdl.n(5, 480)
mapdl.n(6, 60, "1 $ N", 10, 420, 1)

mapdl.fill(1, 5)  # Generates a line of nodes between two existing nodes.
mapdl.fill(6, 10)   
mapdl.nplot(nnum=True, cpos="xy")  # Display nodes with their elements numbers.

mapdl.e(1, 2, 6)  # Define an element by node connectivity.
mapdl.egen(4, 1, 1)  # Generates elements from an existing pattern.
mapdl.eplot(show_node_numbering=True, cpos="xy") # Display elements with their nodes numbers.


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fix the nodes at the larger end (the "wall" end) and apply a vertical force
# to the whole structure.

mapdl.d(2, "UX", "", "", "", "", "UY")  # Application of boundary conditions.
mapdl.d(4, "UY")
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.d("ALL", "UZ")
mapdl.d("ALL", "ROTX")
mapdl.d("ALL", "ROTY")
mapdl.run("NALL")


###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# - Apply a distributed force of :math:`w = (10000/12) lb/in` in the y-direction

mapdl.sfbeam(1, 1, "PRES", "(10000/12)")
mapdl.sfbeam(4, 1, "PRES", "(1E4/12)")
mapdl.finish()



###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system.
mapdl.run("/SOLU")
mapdl.outpr("BASIC", 1)
with mapdl.non_interactive:
    mapdl.run("/OUT,SCRATCH")
    mapdl.solve()
    mapdl.finish()
    mapdl.run("/POST1")
    mapdl.set(1, 1)
    mapdl.run("/OUT,")
    mapdl.prnsol("U", "COMP")
    mapdl.prnsol("ROT", "COMP")
    mapdl.pldisp(1)
    mapdl.run("MID_NODE = NODE (240,,, )")
    mapdl.run("*GET,DISP,NODE,MID_NODE,U,Y")
    mapdl.run("MID_ELM = ENEARN (MID_NODE)")
    mapdl.etable("STRS", "LS", 1)
    mapdl.run("*GET,STRSS,ELEM,MID_ELM,ETAB,STRS")
    mapdl.run("*DIM,LABEL,CHAR,2")
    mapdl.run("*DIM,VALUE,,2,3")
    mapdl.run("LABEL(1) = 'STRS_psi','DEF_in'")
    mapdl.run("*VFILL,VALUE(1,1),DATA,-11400,0.182")
    mapdl.run("*VFILL,VALUE(1,2),DATA,STRSS,DISP")
    mapdl.run("*VFILL,VALUE(1,3),DATA,ABS(STRSS /11400 ) ,ABS( DISP /0.182 )")
    mapdl.run("/OUT,vm2,vrt")
    mapdl.run("/COM")
    mapdl.run("/COM,-------------------VM2 RESULTS COMPARISON ---------------------")
    mapdl.run("/COM,")
    mapdl.run("/COM,         |   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.run("/COM,")
    mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
    mapdl.run("(1X,A8,'   ',F10.3,'  ',F14.3,'   ',1F15.3)")
    mapdl.run("/COM,---------------------------------------------------------------")
    mapdl.run("/OUT")
    mapdl.run("/GOPR")
    mapdl.finish()
    mapdl.run("*LIST,vm2,vrt")
mapdl.exit()