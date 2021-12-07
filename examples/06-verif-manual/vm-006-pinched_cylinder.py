r"""
.. _ref_vm6_example:

Pinched Cylinder
----------------
Problem Description:
 - A thin-walled cylinder is pinched by a force F at the middle
   of the cylinder length. Determine the radial displacement :math:`\delta`
   at the point where the force :math:`F` is applied.
   The ends of the cylinder are free edges.

Reference:
 - R. D. Cook, Concepts and Applications of Finite Element Analysis, 2nd Edition,
   John Wiley and Sons, Inc., New York, NY, 1981, pp. 284-287.
   H. Takemoto, R. D. Cook, "Some Modifications of an Isoparametric Shell
   Element", International Journal for Numerical Methods in Engineering, Vol.7
   No. 3, 1973.

Analysis Type(s):
 - Static Analysis ``ANTYPE=0``

Element Type(s):
 - 4-Node Finite Strain Shell Elements (SHELL181)
 - 8-Node Finite Strain Shell Elements (SHELL281)

.. image:: ../../_static/vm6_setup.png
   :width: 400
   :alt: VM6 Pinched Cylinder Problem Sketch

Material Properties
 - :math:`E = 10.5 \cdot 10^6 psi`
 :math:`Nu = 0.3125`

Geometric Properties:
 - :math:`l = 10.35  in`
 - :math:`r = 4.953  in`
 - :math:`t = 0.094  in`

Loading:
 - :math:`F = 100  lb`

Analysis Assumptions and Modeling Notes:
 - A one-eighth symmetry model is used. One-fourth of the load is applied
   due to symmetry.

"""
# sphinx_gallery_thumbnail_path = '_static/vm6_setup.png'

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~

from ansys.mapdl.core import launch_mapdl

# Start mapdl and clear it.
mapdl = launch_mapdl()
mapdl.clear()

# Enter verification example mode and the pre-processing routine.
mapdl.verify()
mapdl.prep7()


###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element type (a shell-type).

# Type of analysis: Static.
mapdl.antype("STATIC")

# Define element number.
elem_num = 1

# Element type: SHELL181.
mapdl.et(elem_num, "SHELL181")

# Special Features are defined by keyoptions of shell element:

# KEYOPT(3)
# Integration option:
# Full integration with incompatible modes.
mapdl.keyopt(elem_num, 3, 2)  # Cubic shape function


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material.

# Define material number.
mat_num = 1

# Define material properties.
mapdl.mp("EX", mat_num, 10.5E6)
mapdl.mp("NUXY", mat_num, 0.3125)
print(mapdl.mplist())


###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a shell element.

# Parametrization of the shell thickness.
t = 0.094

# Define cross-section number.
sec_num = 1

# Define shell cross-section.
mapdl.sectype(secid=sec_num, type_="SHELL", name="shell181")
mapdl.secdata(t, mat_num, 0, 5)


###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# Set up the keypoints and area. Define line division of the lines, then
# mesh the area with shell elements.

# Define global cylindrical coordinate system.
mapdl.csys(1)

# Define keypoints by coordinates.
mapdl.k(1, 4.953)
mapdl.k(2, 4.953, "", 5.175)

# Generates additional keypoints from a pattern of keypoints.
mapdl.kgen(2, 1, 2, 1, "", 90)

# Create an area through keypoints.
mapdl.a(1, 2, 4, 3)

# Specify the default number of line divisions.
mapdl.esize("", 8)

# Mesh the area.
mapdl.amesh(1)

# Define global cartesian coordinate system.
mapdl.csys(0)


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of boundary conditions (BC).

# Select nodes by location and apply BC.
mapdl.nsel("S", "LOC", "X", 0)
mapdl.dsym("SYMM", "X", 0)
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.dsym("SYMM", "Y", 0)
mapdl.nsel("S", "LOC", "Z", 0)
mapdl.dsym("SYMM", "Z", 0)
mapdl.nsel("ALL")


###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Apply the force of :math:`F = (100/4) lb` in the y-direction.

# Parametrization of the :math:`F` load for the quarter of the model.
F = 100/4

# Application of the load to the model.
mapdl.fk(3, "FY", -F)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system. Print the solver output.

mapdl.run("/SOLU")
out = mapdl.solve()
mapdl.finish()
print(out)

#
# ###############################################################################
# # Post-processing
# # ~~~~~~~~~~~~~~~
#
#
#
# mapdl.run("/POST1")
#
# mapdl.nsel("S", "LOC", "Y", 4.953)  # SELECT NODE AT LOAD APPLICATION
#
# mapdl.nsel("R", "LOC", "Z", 0)
#
# mapdl.nsel("R", "LOC", "X", 0)
#
# mapdl.prnsol("U", "COMP")  # PRINT DISPLACEMENTS AND VECTOR SUM
#
# mapdl.run("TOP_NODE = NODE (4.953,90,0)")
#
# mapdl.get("DISP", "NODE", "TOP_NODE", "U", "Y")
#
# mapdl.run("*DIM,LABEL,CHAR,1")
#
# mapdl.run("*DIM,VALUE,,1,3")
#
# mapdl.run("LABEL(1) = 'DEF_IN'")
#
# mapdl.run("*VFILL,VALUE(1,1),DATA,0.1139")
#
# mapdl.run("*VFILL,VALUE(1,2),DATA,ABS(DISP)")
#
# mapdl.run("*VFILL,VALUE(1,3),DATA,ABS( DISP /0.1139 )")
#
# mapdl.save("TABLE_1")
#
# mapdl.finish()
#
# mapdl.run("/CLEAR,NOSTART")
#
# mapdl.title("VM6 PINCHED CYLINDER")
#
# mapdl.run("C*** USING SHELL281 ELEMENTS")
#
# mapdl.prep7()
#
# mapdl.run("SMRT,OFF")
#
# mapdl.antype("STATIC")
#
# mapdl.et(1, "SHELL281")
#
# mapdl.sectype(1, "SHELL")
#
# mapdl.secdata(0.094, 1, 0, 5)
#
# mapdl.mp("EX", "", 10.5E6)
#
# mapdl.mp("NUXY", "", .3125)
#
# mapdl.csys(1)
#
# mapdl.k(1, 4.953)  # DEFINE MODEL GEOMETRY
#
# mapdl.k(2, 4.953, "", 5.175)
#
# mapdl.kgen(2, 1, 2, 1, "", 90)
#
# mapdl.a(1, 2, 4, 3)
#
# mapdl.esize("", 8)
#
# mapdl.amesh(1)
#
# mapdl.csys(0)
#
# mapdl.nsel("S", "LOC", "X", 0)
#
# mapdl.dsym("SYMM", "X", 0)
#
# mapdl.nsel("S", "LOC", "Y", 0)
#
# mapdl.dsym("SYMM", "Y", 0)
#
# mapdl.nsel("S", "LOC", "Z", 0)
#
# mapdl.dsym("SYMM", "Z", 0)
#
# mapdl.nsel("ALL")
#
# mapdl.fk(3, "FY", -25)
#
# mapdl.finish()
#
# mapdl.run("/SOLU")
#
# mapdl.solve()
#
# mapdl.finish()
#
# mapdl.run("/POST1")
#
# mapdl.nsel("S", "LOC", "Y", 4.953)  # SELECT NODE AT LOAD APPLICATION
#
# mapdl.nsel("R", "LOC", "Z", 0)
#
# mapdl.nsel("R", "LOC", "X", 0)
#
# mapdl.prnsol("U", "COMP")  # PRINT DISPLACEMENTS AND VECTOR SUM
#
# mapdl.run("TOP_NODE = NODE (4.953,90,0)")
#
# mapdl.get("DISP", "NODE", "TOP_NODE", "U", "Y")
#
# mapdl.run("*DIM,LABEL,CHAR,1")
#
# mapdl.run("*DIM,VALUE,,1,3")
#
# mapdl.run("LABEL(1) = 'DEF_IN'")
#
# mapdl.run("*VFILL,VALUE(1,1),DATA,0.1139")
#
# mapdl.run("*VFILL,VALUE(1,2),DATA,ABS(DISP)")
#
# mapdl.run("*VFILL,VALUE(1,3),DATA,ABS( DISP /0.1139 )")
#
# mapdl.save("TABLE_2")
#
# mapdl.resume("TABLE_1")
#
# mapdl.run("/COM")
#
# with mapdl.non_interactive:
#     mapdl.run("/OUT,vm6,vrt")
#
#     mapdl.run("/COM,------------------- VM6 RESULTS COMPARISON ---------------------")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM, | TARGET | Mechanical APDL | RATIO")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,SHELL181")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
#
#     mapdl.run("(1X,A10,' ',F10.4,' ',F14.4,' ',1F13.3)")
#
#     mapdl._run("/NOPR")  # It is not recommended to use '/NOPR' in a normal PyMAPDL session.
#
#     mapdl.resume("TABLE_2")
#
#     mapdl.run("/GOPR")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,SHELL281")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
#
#     mapdl.run("(1X,A10,' ',F10.4,' ',F14.4,' ',1F13.3)")
#
#     mapdl.run("/COM,-----------------------------------------------------------------")
#
# mapdl.run("/OUT")
#
# mapdl.run("/GOPR")
#
# mapdl.finish()
#
# mapdl.run("/DEL,TABLE_1")
#
# mapdl.run("/DEL,TABLE_2")
#
# mapdl.finish()
#
# mapdl.run("*LIST,vm6,vrt")
#
# mapdl.exit()
