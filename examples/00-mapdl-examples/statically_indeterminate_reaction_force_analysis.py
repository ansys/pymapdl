"""
.. _ref_how_to_add_an_example_reference_key:

Statically Indeterminate Reaction Force Analysis
------------------------------------------------
Taken from "The Strength of Materials" - Timoshenko, Part 1, 3rd Edition, Page 26, Problem 10

Find the reaction forces at opposite, fixed, ends of a linking element 10 units long, with
forces applied in the dimension of the element of 500 and 1000 at 4 and 7 units along the
element.
"""
from ansys.mapdl.core import launch_mapdl

# start MAPDL and enter the pre-processing routine
mapdl = launch_mapdl()
mapdl.clear()
#
mapdl.run("/VERIFY,VM1")
mapdl.prep7()

###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material and its type (a single material, with a linking-type
# section and an enthalpy of 30e6).

mapdl.antype('STATIC')
mapdl.et(1, 'LINK180')
mapdl.sectype(1, 'LINK')
mapdl.secdata(1)
mapdl.mp('EX', 1, 30e6)

###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# Set up the nodes and elements.

mapdl.n(1)
mapdl.n(2, '', 4)
mapdl.n(3, '', 7)
mapdl.n(4, '', 10)
mapdl.e(1, 2)
mapdl.egen(3, 1, 1)

###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set nodes 1 and 4 to have no degrees of freedom, by incrementing from node 1
# to node 4 in steps of 3. Apply y-direction forces to nodes 2 and 3, with
# values of -500 and -1000 respectively. Then exit prep7.

mapdl.d(1, 'ALL', '', '', 4, 3)
mapdl.f(2, 'FY', -500)
mapdl.f(3, 'FY', -1000)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system.

mapdl.run('/SOLU')
mapdl.solve()
mapdl.finish()

###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing. Select the nodes at y=10 & y=0, and sum the forces
# there. Then store the y-components in two variables: ``reaction_1`` and
# ``reaction_2``.

mapdl.post1()
mapdl.nsel('S', 'LOC', 'Y', 10)
mapdl.fsum()
reaction_1 = mapdl.get('REAC_1', 'FSUM', '', 'ITEM', 'FY')
mapdl.nsel('S', 'LOC', 'Y', 0)
mapdl.fsum()
reaction_2 = mapdl.get('REAC_2', 'FSUM', '', 'ITEM', 'FY')


###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Now we have the reaction forces we can compare them to the expected values of
# 900 and 600 for reaction 1 and 2 respectively.

results = \
    f"""
    ---------------------  RESULTS COMPARISON  ---------------------
    |   TARGET   |   Mechanical APDL   |   RATIO
    /INPUT FILE=    LINE=       0
    R1, lb          900.0       {abs(reaction_1)}   {abs(reaction_1) / 900}
    R2, lb          600.0       {abs(reaction_2)}   {abs(reaction_2) / 600}
    ----------------------------------------------------------------
    """
print(results)

