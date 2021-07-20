r"""
.. _ref_deflection_of_a_hinged_support:

Deflection of a Hinged Support
------------------------------
Problem Description:
 - ?

Reference:
 - S. Timoshenko, Strength of Materials, Part I, Elementary Theory and
   Problems, 3rd Edition, D. Van Nostrand Co., Inc., New York, NY, 1955,
   pg. 10, problem 2.

Analysis Type(s):
 - None?

Element Type(s):
 - 3-D Spar (or Truss) Elements (LINK180)

.. image:: ../../_static/vm4_setup.png
   :width: 400
   :alt: VM4 Problem Sketch

Material Properties
 - :math:`E = 30 \cdot 10^6 psi`

Geometric Properties:
 - ?

Loading:
 - ?

Analytical Equations:
 - ?

"""
# sphinx_gallery_thumbnail_path = '_static/vm4_setup.png'

from ansys.mapdl.core import launch_mapdl
from math import sin, cos, pi

# start mapdl and clear it
mapdl = launch_mapdl()
mapdl.clear()  # optional as MAPDL just started

# enter verification example mode and the pre-processing routine
mapdl.verify()
mapdl.prep7()

###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# This example demonstrates a simple hinge geometry.
# We use the `LINK180` element type to model this and an elastic modulus
# of 30e6.
# We store the x-coordinate of node 3 and the y-coordinate of node 2 for
# ease of use later on.

length_bar = 15*12
theta = 30
theta_rad = theta*pi/180.
node3_x = 2 * length_bar * cos(theta_rad)
node2_y = length_bar * sin(theta_rad)

mapdl.et(1, 'LINK180')
mapdl.sectype(1, 'LINK')
mapdl.secdata(.5)
mapdl.mp('EX', 1, 30e6)

###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# We create three nodes in an isosceles triangle shape, with elements
# along the equal sides, forming a hinge.

n1 = mapdl.n(1, 0, 0, 0)
n2 = mapdl.n(2, node3_x * .5, -node2_y, 0)
n3 = mapdl.n(3, node3_x, 0, 0)

mapdl.e(n1, n2)
mapdl.e(n2, n3)
mapdl.eplot(line_width=5)

###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# - Fix nodes 1 and 3 in place
# - Apply a force of -5000 in the negative y-direction to node 2
# - Then finish the prep7 section

mapdl.d(1, 'ALL', '', '', 3, 2)
mapdl.f(2, 'FY', -5000)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system.

mapdl.run('/SOLU')
out = mapdl.solve()
mapdl.finish()

###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing, get the results and view the nodal displacement
# as well as the equivalent stress on the nodes.
#
# We make the line width larger for ease of visualisation as well as
# using two perceptually linear colormaps to enhance display of the
# data.

mapdl.post1()
result = mapdl.result
result.plot_nodal_displacement(0,
                               cmap='magma',
                               line_width=5)

result.plot_principal_nodal_stress(0,
                                   'SEQV',
                                   cmap='viridis',
                                   line_width=5)


###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Now that we have the results we can compare the nodal displacement and
# stress experienced by node 2 to the known quantities 10000 psi and
# -0.12 inches. To do this we:
#
# - Find the mid-node from the coordinates using the `Query` class.
# - Get the y-displacement from node 2
# - Get the element nearest to node 2
# - Get the stress on this element
# - Compare.

q = mapdl.query()
mid_node = q.node(node3_x * .5, -node2_y, 0)
# *GET requires we assign to a variable in APDL, however, we just assign
# the result to a Python variable. So here we use a dummy variable '_'
# instead.
displacement = mapdl.get('_', 'NODE', mid_node, 'U', 'Y')
left_element = q.enearn(mid_node)
mapdl.etable('STRS', 'LS', 1)
stress = mapdl.get('_', 'ELEM', left_element, 'ETAB', 'STRS')

results = \
    f"""
    ---------------------  RESULTS COMPARISON  -----------------------
    |   TARGET         |  TARGET     |   Mechanical APDL   |   RATIO
    ------------------------------------------------------------------
    Stress [psi]          10000            {stress}              {stress/10000}
    Displacement [in]     -0.12            {displacement}                {abs(displacement) / 0.12}
    ------------------------------------------------------------------
    """
print(results)
