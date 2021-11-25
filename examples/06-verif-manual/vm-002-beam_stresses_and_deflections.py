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
mapdl.keyopt(1, 9, 3)  # Output at 9 intermediate locations
mapdl.keyopt(1, 3, 3)  # Cubic shape function


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material and its type (a single material, with a beam-type section).

mapdl.mp("EX", 1, 30E6)
mapdl.mp("PRXY", 1, 0.3)

###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section for a beam element.

w_f = 1.048394965
w_w = 0.6856481
sec_num = 1
mapdl.sectype(sec_num, "BEAM", "I", "ISection")
mapdl.secdata(15, 15, 28+(2*w_f), w_f, w_f, w_w)


###############################################################################
# Define Geometry:
# ~~~~~~~~~~~~~~~~~~~~~~
# Set up the nodes and elements.  This creates a mesh just like
# in the problem setup. We create a square of nodes and use `fill` to add
# mid-point nodes to two opposite sides.

# Define nodes
mapdl.n(1)
mapdl.n(5, 480)
mapdl.n(6, 60, "1 $ N", 10, 420, 1)

print(mapdl.mesh.nodes)  # list the node coordinates

print(mapdl.mesh.nnum)  # list the node numbers

mapdl.fill(1, 5)  # Generates a line of nodes between two existing nodes.
mapdl.fill(6, 10)
mapdl.e(1, 2, 6)  # Define an element by node connectivity.
mapdl.egen(4, 1, 1)  # Generates elements from an existing pattern.
mapdl.eplot(show_node_numbering=True, line_width=5, cpos="xy")  # Display elements with their nodes numbers.


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Fix the nodes at the larger end (the "wall" end) and apply a vertical force
# to the whole structure.

mapdl.d(2, "UX", lab2="UY")  # Application of boundary conditions.
mapdl.d(4, "UY")
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.d("ALL", "UZ")
mapdl.d("ALL", "ROTX")
mapdl.d("ALL", "ROTY")
mapdl.nsel("ALL")


###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# - Apply a distributed force of :math:`w = (10000/12) lb/in` in the y-direction

mapdl.sfbeam(1, 1, "PRES", 10000/12)
mapdl.sfbeam(4, 1, "PRES", 1E4/12)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system.

mapdl.run("/SOLU")
out = mapdl.solve()
print(out)
mapdl.finish()


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing. Select the nodes at ``y=10`` and ``y=0``, and
# sum the forces there. Then store the y-components in two variables:
# ``reaction_1`` and ``reaction_2``.

mapdl.post1()  # Start Post-Processing
mapdl.set(1)  # Select first Load Step

# Define Maximum Stress


a = mapdl.post_processing.nodal_elastic_eqv


# print(seqv_max)

# # Difine deflection at the middle of the beam
# mid_node_uy = mapdl.get('disp', 'node', 3, 'u', 'y')
# print(mid_node_uy)
# print(type(mid_node_uy))
#
# ###############################################################################
# # Check Results
# # ~~~~~~~~~~~~~
# # Now that we have the response we can compare the values to the
# # expected stresses of 19695 and 10152 respectively.
# #
#
# stress_target = -11400.000
# print(type(stress_target))
# stress_ratio = seqv_max / stress_target
# deflection_target = 0.182
# deflection_ratio = mid_node_uy / deflection_target
#
# output = f"""
# ------------------- VM3 RESULTS COMPARISON ---------------------
#              |   TARGET   |   Mechanical APDL   |   RATIO
# ----------------------------------------------------------------
#     Steel        {stress_target}        {seqv_max}            {stress_ratio:.6f}
#     Copper       {deflection_target}        {mid_node_uy}            {deflection_ratio:.6f}
# ----------------------------------------------------------------
# """
# print(output)
