r"""
.. _ref_thermally_loaded_support_structure:

Thermally Loaded Support Structure
----------------------------------
Problem Descrption:
 - A prismatical bar with built-in ends is loaded axially at two
   intermediate cross sections.  Determine the reactions :math:`R_1`
   and :math:`R_2`.

Reference:
 - S. Timoshenko, Strength of Materials, Part I, Elementary Theory and
   Problems, 3rd Edition, D. Van Nostrand Co., Inc., New York, NY, 1955,
   pg. 30, problem 9.

Analysis Type(s):
 - Static Analysis ``ANTYPE=0``

Element Type(s):
 - 3-D Spar (or Truss) Elements (LINK180)

.. image:: ../../_static/vm3_setup.png
   :width: 400
   :alt: VM1 Problem Sketch

Material Properties
 - :math:`E_{copper} = 16 \cdot 10^6 psi`
 - :math:`E_{steel} = 30 \cdot 10^6 psi`
 - :math:`\alpha_{copper} = 70 \cdot 10^{-7} /K
 - :math:`\alpha_{steel} = 92 \cdot 10^{-7} /K

Geometric Properties:
 - :math:`a = b = 0.3`
 - :math:`l = 10 in`

Loading:
 - ?

Analytical Equations:
 - ?

"""
# sphinx_gallery_thumbnail_path = '_static/vm3_setup.png'

from ansys.mapdl.core import launch_mapdl

# start mapdl and clear it
mapdl = launch_mapdl()
mapdl.clear()  # optional as MAPDL just started

# enter verification example mode and the pre-processing routine
mapdl.verify()
mapdl.prep7()

###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the materials and their properties. We are using copper and
# steel here.
# - `EX` - X-direction elastic modulus
# - `ALPX` - Secant x - coefficient of thermal expansion

mapdl.antype('STATIC')
mapdl.et(1, 'LINK180')
mapdl.sectype(1, 'LINK')
mapdl.secdata(0.1)
mapdl.mp('EX', 1, 16e6)
mapdl.mp('ALPX', 1, 92e-7)
mapdl.mp('EX', 2, 30e6)
mapdl.mp('ALPX', 2, 70e-7)
# Define the reference temperature for the thermal strain calculations.
mapdl.tref(70)

###############################################################################
# Define Geometry: Nodes
# ~~~~~~~~~~~~~~~~~~~~~~
# Set up the nodes and elements.  This creates a mesh just like in the
# problem setup. We create a square of nodes and use `fill` to add
# mid-point nodes to two opposite sides.

mapdl.n(1, -10)
mapdl.n(3, 10)
mapdl.fill()
mapdl.n(4, -10, -20)
mapdl.n(6, 10, -20)
mapdl.fill()
mapdl.nplot(knum=True)

###############################################################################
# Define Geometry: Elements
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Create two elements (using material #1) that are two sides of our
# square, as links. Then create a single element using material #2
# between the first 2 that is parallel to them.

mapdl.e(1, 4)
mapdl.e(3, 6)
mapdl.mat(2)
mapdl.e(2, 5)
mapdl.eplot()

###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# - Couple the degrees of freedom in y-displacement across nodes 5, 4,
# and 6.
# - Fix nodes 1, 2, and 3 in place.
# - Apply a force of -4000 in the y-direction to node 5
# - Apply a uniform temperature of 80 to the whole body

mapdl.cp(1, 'UY', 5, 4, 6)
mapdl.d(1, 'ALL', '', '', 3)
mapdl.f(5, 'FY', -4000)
mapdl.bfunif('TEMP', 80)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# - Enter solution mode
# - Specify 1 timestep to be used for this load step
# - Solve the system.

mapdl.run('/SOLU')
mapdl.nsubst(1)
mapdl.solve()

###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# - Get a query instance
# - Find a steel node and a copper node
# - Then use these to get the steel and copper elements
# - Finally we extract the stress experienced by each element

mapdl.post1()
q = mapdl.query()
steel_n = q.node(0, 0, 0)
copper_n = q.node(10, 0, 0)
steel_e = q.enearn(steel_n)
copper_e = q.enearn(copper_n)
mapdl.etable('STRS_ST', 'LS', 1)
mapdl.etable('STRS_CO', 'LS', 1)

stress_steel = mapdl.get('_', 'ELEM', steel_e, 'ETAB', 'STRS_ST')
stress_copper = mapdl.get('_', 'ELEM', copper_e, 'ETAB', 'STRS_CO')

###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Now that we have the response we can compare the values to the
# expected stresses of 19695 and 10152 respectively.
#

steel_target = 19695
steel_ratio = stress_steel/steel_target
copper_target = 10152
copper_ratio = stress_copper/copper_target

message = f"""
------------------- VM3 RESULTS COMPARISON ---------------------

                 |   TARGET   |   Mechanical APDL   |   RATIO
----------------------------------------------------------------
    Steel            {steel_target}        {stress_steel}           {steel_ratio}
    Copper           {copper_target}        {stress_copper}           {copper_ratio}

----------------------------------------------------------------

"""
print(message)
