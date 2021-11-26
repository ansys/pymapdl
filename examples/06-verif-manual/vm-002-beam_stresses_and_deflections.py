r"""
.. _ref_vm2_example:
Beam Stresses and Deflections
------------------------------------------------
Problem Description:
-   A standard 30 inch WF beam, with a cross-sectional area :math:`A`, is supported
    as shown below and loaded on the overhangs by a uniformly distributed
    load :math:`w`. Determine the maximum bending stress, :math:`\sigma_max`, in the middle portion of
    the beam and the deflection, :math:`\delta`, at the middle of the beam.
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
 - :math:`M` is the bending moment for the middle portion of the beam:
   :math:`M = 10000 \cdot 10 \cdot 60 = 6 \cdot 10^6 lb \cdot in`
 - Determination of the maximum stress in the middle portion of the beam is:
   :math:`\sigma_max = \frac{M h}{2 I_z}`
 - The deflection, :math:`\delta`, at the middle of the beam could be defined
   by the formulas of the Transversally Loaded Beams:
   :math:`\delta = 0.182 in`
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
# Set up the material.

mapdl.mp("EX", 1, 30E6)
mapdl.mp("PRXY", 1, 0.3)

###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a beam element.

w_f = 1.048394965
w_w = 0.6856481
sec_num = 1
mapdl.sectype(sec_num, "BEAM", "I", "ISection")
mapdl.secdata(15, 15, 28 + (2 * w_f), w_f, w_f, w_w)

###############################################################################
# Define Geometry:
# ~~~~~~~~~~~~~~~~~~~~~~
# Set up the nodes and elements. Create nodes then creating elements
# bewtween nodes.

# Define nodes
mapdl.n(1)
mapdl.n(5, 480)
mapdl.n(6, 60, "1 $ N", 10, 420, 1)
mapdl.fill(1, 5)
mapdl.fill(6, 10)
print(mapdl.nlist())  # List of the created nodes.

# Define elements

mapdl.e(1, 2, 6)
mapdl.egen(4, 1, 1)
print(mapdl.elist())  # List of the created elements.

# Display elements with their nodes numbers.

mapdl.eplot(show_node_numbering=True, line_width=5, cpos="xy") 

###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of boundary conditions.

mapdl.d(2, "UX", lab2="UY") 
mapdl.d(4, "UY")
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.d("ALL", "UZ")
mapdl.d("ALL", "ROTX")
mapdl.d("ALL", "ROTY")
mapdl.nsel("ALL")

###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Application a distributed force of :math:`w = (10000/12) lb/in` 
# in the y-direction.

w = 10000/12  # (lb/in) - distributed load.
mapdl.sfbeam(1, 1, "PRES", w)
mapdl.sfbeam(4, 1, "PRES", w)
mapdl.finish()

###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system.

mapdl.run("/SOLU")
out = mapdl.solve()
mapdl.finish()
print(out)

result = mapdl.result
print(result)


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing. To get the stress and deflection results
# from the middle node and cross-section of the beam we can use
# mapdl.get().

mapdl.post1()  # Start Post-Processing
mapdl.set(1)  # Select first Load Step

# Define Maximum Stress

s_eqv_max_str = (mapdl.get('stress_eqv', 'secr', 2, 's', 'eqv', 'max')).split()
s_eqv_max = -float(s_eqv_max_str[0])

# Difine deflection at the middle of the beam

mid_node_uy = mapdl.get('disp', 'node', 3, 'u', 'y')

###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Now that we have the results we can compare the nodal displacement and stress
# experienced by middle node of the beam to the known stresses -11400 psi and 
# 0.182 inches of the deflection. 

stress_target = -11400.000
stress_ratio = s_eqv_max / stress_target
deflection_target = 0.182
deflection_ratio = mid_node_uy / deflection_target

output = f"""
-------------------------- VM3 RESULTS COMPARISON --------------------------
              |   TARGET   |   Mechanical APDL   |   RATIO   |
----------------------------------------------------------------------------
    Stress     {stress_target:.3f}        {s_eqv_max:.3f}         {stress_ratio:.3f}
    Deflection    {deflection_target:.3f}            {mid_node_uy:.3f}            {deflection_ratio:.3f}
----------------------------------------------------------------------------
"""

print(output)
