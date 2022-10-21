# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 14:24:13 2022

@author: pmaroneh
"""

""".. _ref_buckling_postbuckling_ring_stiffened_cylinder:

Buckling and post-buckling analysis of a ring-stiffened
cylinder using nonlinear stabilization
======================================================

This examples shows how to use PyMAPDL to import an existing FE model and to
perform a nonlinear buckling and postbuckling analysis using nonlinear
stabilization. The problem uses a stiffened cylinder subjected to uniform
external pressure to show how to find the nonlinear buckling loads,
achieve convergence at the post-buckling stage, and interpret the results.

This example is inspired from the model and analysis defined in Chapter 21 of
the Mechanical APDL Technology Showcase Manual.

"""

###############################################################################
# Setting up model
# ----------------
#
# The original FE model is given in the Ansys Mechanical APDL Technology
# Showcase Manual.  The .cdb contains a FE model of a ring-stiffened cylinder.
#
# A circular cylinder made of bare 2024-T3 aluminum alloy is stiffened inside
# with five Z-section rings. Its ends are closed with thick aluminum bulkheads.
# A riveted L section exists between the top plate and the top ring and the
# bottom plate and bottom ring.
# The cylinder is subjected to a differential external pressure. The pressure
# causes a local buckling phenomenon characterized by buckling of the skin
# between stiffening rings, leading eventually to collapse.
#
# The finite element model of the ring stiffened cylinder is meshed with
# SHELL281 elements with an element size of 10 mm. The fine mesh is required
# for buckling analysis, and a full 360-degree model is necessary because
# the deformation is no longer axisymmetric after buckling occurs.
#
# All shell elements have uniform thickness. Five sections are created in the
# model with no offsets, so the shell sections are offset to the midplane
# by default.
#
# Starting MAPDL as a service and importing an external model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples import download_tech_demo_data

# define geometric parameters
bs = 95.3  # Ring spacing (mm)
ts = 1.034  # Skin thickness (mm)
tw = 0.843  # Ring thickness (mm)
r = 344 * ts  # Radius of cylinder (mm)
L = 431.8 + 2 * (19 - 9.5)  # Length of cylinder (mm)
pext = 0.24  # Differential external pressure (MPa)

# start MAPDL as a service
mapdl = launch_mapdl()
print(mapdl)

mapdl.filname("buckling")  # change filename
# mapdl.nerr(nmerr=200, nmabt=10000, abort=-1, ifkey=0, num=0)

# enter preprocessor
mapdl.prep7()

# define material properties for 2024-T3 Alluminum alloy
EX = 73000  # Young's Modulus (MPA)
ET = 73  # Tangent modulus
mapdl.mp("ex", 1, EX)  # Young's Modulus (MPA)
mapdl.mp("prxy", 1, 0.33)  # Poisson's ratio
EP = EX * ET / (EX - ET)
mapdl.tb("biso", 1)
mapdl.tbdata(1, 268.9, EP)
# create material plot
mapdl.show("png")
mapdl.tbplot("biso", 1)
mapdl.show("close")

# define shell elements and their sections
mapdl.et(1, 181)
# cylinder
mapdl.sectype(1, "shell")
mapdl.secdata(ts, 1)
# L
mapdl.sectype(2, "shell")
mapdl.secdata(ts + 1.64, 1)
# Z shaped ring stiffener
mapdl.sectype(3, "shell")
mapdl.secdata(tw, 1)
# Plate at z=0 with thickness=25 mm
mapdl.sectype(4, "shell")
mapdl.secdata(25, 1)
# Plate at z=L  with thickness=25 mm
mapdl.sectype(5, "shell")
mapdl.secdata(25, 1)


# read model of stiffened cylinder
# download the cdb file
ring_mesh_file = download_tech_demo_data(
    "td-21", "ring_stiffened_cylinder_mesh_file.cdb"
)

# read in cdb
mapdl.cdread("db", ring_mesh_file)
mapdl.allsel()
mapdl.eplot(background="w")
mapdl.cmsel("all")

###############################################################################
# Define static prestress analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Displacement boundary conditions are defined to prevent the six rigid body
# motions. A total of six displacements are therefore applied to three nodes
# located on the top plate at 0, 90, and 270 degrees; the nodes are restricted
# so that all rigid translations and rotations are not possible for the
# cylinder.
#
# Loading consists of a uniformly distributed external differential
# pressure: Pext = 0.24 MPa

mapdl.csys(1)  # activate cylindrical coordinate system

# Define pressure on plate at z=0
mapdl.nsel("s", "loc", "z", 0)
mapdl.esln("s", 1)
mapdl.sfe("all", 2, "pres", 1, pext)
mapdl.allsel()

# Define pressure on the rim of plate at z=0
mapdl.nsel("s", "loc", "z", 0)
mapdl.nsel("r", "loc", "x", r - ts / 2, 760 / 2)
mapdl.esln("s", 1)
mapdl.sfe("all", 1, "pres", 1, pext)
mapdl.allsel()

# Define pressure on plate at z=L
mapdl.nsel("s", "loc", "z", L)
mapdl.esln("s", 1)
mapdl.sfe("all", 2, "pres", 1, pext)
mapdl.allsel()

# Define pressure on the rim of plate at z=L
mapdl.nsel("s", "loc", "z", L)
mapdl.nsel("r", "loc", "x", r - ts / 2, 760 / 2)
mapdl.esln("s", 1)
mapdl.sfe("all", 1, "pres", 1, pext)
mapdl.allsel()

# Define pressure on cylinder
mapdl.nsel("s", "loc", "x", r - ts / 2)
mapdl.esln("s", 1)
mapdl.sfe("all", 2, "pres", 1, pext)
mapdl.allsel()

# Define displacement BSs to avoid rigid body motion
mapdl.csys(0)  # activate cartesian coordinate system
mapdl.nsel("s", "loc", "x", r - ts / 2)
mapdl.nsel("r", "loc", "y", 0)
mapdl.nsel("r", "loc", "z", 0)
mapdl.d("all", "ux", 0)
mapdl.d("all", "uy", 0)
mapdl.d("all", "uz", 0)
mapdl.allsel()
#
mapdl.nsel("s", "loc", "x", 0)
mapdl.nsel("r", "loc", "y", r - ts / 2)
mapdl.nsel("r", "loc", "z", 0)
mapdl.d("all", "uz", 0)
mapdl.allsel()
#
mapdl.nsel("s", "loc", "x", 0)
mapdl.nsel("r", "loc", "y", -(r - ts / 2))
mapdl.nsel("r", "loc", "z", 0)
mapdl.d("all", "uy", 0)
mapdl.d("all", "uz", 0)
mapdl.allsel()
#

# Print DOF constraints
print(mapdl.dlist())

# Solve static prestress analysis
mapdl.slashsolu()
mapdl.pstres("on")
mapdl.antype("STATIC")
output = mapdl.solve()
print(output)

# Plot total deformation
mapdl.post1()
mapdl.set("last")
mapdl.post_processing.plot_nodal_displacement("NORM", smooth_shading=True)
#%%
###############################################################################
# Run linear buckling analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This preliminary analysis predicts the theoretical buckling pressure of the
# ideal linear elastic structure (perfect cylinder) and the buckled mode shapes
# used in the next step to generate the imperfections.
# It is also an efficient way to check the completeness and
# correctness of modeling.
# To run the linear buckling analysis, a static solution with prestress effects
# must be obtained, followed by the eigenvalue buckling solution using the
# Block Lanczos method and mode expansion.

# Define and solve linear buckling analysis
mapdl.slashsolu()
mapdl.outres("all", "all")
mapdl.antype("BUCKLE")
mapdl.bucopt("lanb", "10")
mapdl.mxpand(10)
output = mapdl.solve()
print(output)

# Plot total deformation of first and 10th mode
mapdl.post1()
mapdl.set(1, 1)
mapdl.post_processing.plot_nodal_displacement("NORM", smooth_shading=True)
mapdl.set(1, 10)
mapdl.post_processing.plot_nodal_displacement("NORM", smooth_shading=True)
#%%
###############################################################################
# Generate imperfections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# If a structure is perfectly symmetric, nonsymmetric buckling does not occur
# numerically, and a nonlinear buckling analysis fails because
# nonsymmetric buckling responses cannot be triggered. In this problem,
# the geometry, elements, and pressure are all axisymmetric.
# It is not possible, therefore, to simulate nonaxisymmetric buckling with
# the initial model. To overcome this problem, small geometric imperfections
# (similar to those caused by manufacturing a real structure) must be
# introduced to trigger the buckling responses.
# Because the radius of the cylinder is 355.69 mm and the maximum
# displacement of a mode shape is 1 mm, a factor of 0.1 is applied when
# updating the geometry with mode shapes. The factor assumes the manufacturing
# tolerance of the radius to be on the order of 0.1.
mapdl.finish()
mapdl.prep7()
for i in range(1, 11):
    mapdl.upgeom(0.1, 1, i, "buckling", "rst")  # Add imperfections as a tenth of each
    # mode shape
mapdl.finish()
#%%
###############################################################################
# Run nonlinear static analysis on geometry with imperfections
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The nonlinear buckling analysis is a static analysis performed after adding
# imperfections with large deflection active (NLGEOM,ON), extended to a point
# where the stiffened cylinder can reach its limit load.
# To perform the analysis, the load must be allowed to increase using very
# small time increments so that the expected critical buckling load can
# be predicted accurately.
# Note - as this is a buckling analysis, divergence is expected.

mapdl.slashsolu()
mapdl.antype("STATIC")
mapdl.nlgeom("on")
mapdl.pred("on")
mapdl.time(1)
mapdl.nsubst(100, 10000, 10)
mapdl.rescontrol("define", "all", 1)
mapdl.outres("all", "all")
mapdl.ncnv(2)  # Do not terminate the program execution if the solution diverges
output = mapdl.solve()
print(output)
mapdl.finish()

#%%
###############################################################################
# Post-buckling analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# An unconverged solution of the nonlinear static analysis could mean that
# buckling has occurred. In this example, the change in time (or load)
# increment, and displacement value, occurs between substeps 10 and 11,
# which corresponds to TIME = 0.51781 and TIME = 0.53806 and to a pressure
# between 0.124 MPa and 0.129 MPa. It is therefore very likely that buckling
# occurred at this time; to be sure, the analysis is continued. The goal is to
# verify the assessment made at this stage by obtaining the load-displacement
# behavior over a larger range. Because the post-buckling state is unstable,
# special techniques are necessary to compensate, in this case, nonlinear
# stabilization is used.

mapdl.slashsolu()  # Restart analysis with stabilization
mapdl.antype("static", "restart", 1, 10)
mapdl.nsubst(100, 50000, 10)
mapdl.rescontrol("define", "last")
mapdl.stabilize("constant", "energy", 0.000143)  # Use energy option
output = mapdl.solve()
print(output)
mapdl.finish()

#%%
###############################################################################
# Postprocess buckling analysis in POST1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
mapdl.post1()
mapdl.set("last")
mapdl.post_processing.plot_nodal_displacement("NORM", smooth_shading=True)
mapdl.post_processing.plot_nodal_eqv_stress()
mapdl.finish()
#%%
###############################################################################
# Postprocess buckling analysis in POST26
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
mapdl.post26()


mapdl.numvar(100)  # allow storage for 100 variables
mapdl.enersol(13, "sene")  # store stiffness energy
mapdl.enersol(14, "sten")  # store artificial stabilization energy

# time history plot of stiffness and stabilization energies
mapdl.show("png")
mapdl.plvar(13, 14)
mapdl.show("close")

# pressure versus axial shortening for some nodes under the upper ring
mapdl.nsol(2, 67319, "U", "Z", "UZ1")
mapdl.prod(
    ir=3, ia=2, ib="", ic="", name="strain1", facta="", factb="", factc=-1 / 431.8
)
mapdl.prod(ir=12, ia=1, ib="", ic="", name="Load", facta="", factb="", factc=0.24)
mapdl.xvar(3)
mapdl.show("png")
mapdl.xrange(0.01)
mapdl.yrange(0.24)
mapdl.axlab("X", "Axial Shortening")
mapdl.aylab("Y", "Applied Pressure ")
mapdl.plvar(12)
mapdl.show("close")
mapdl.xvar(3)
mapdl.show("png")
mapdl.xrange(0.002)
mapdl.yrange(1)
mapdl.axlab("X", "Axial Shortening")
mapdl.aylab("Y", "Time")
mapdl.plvar(1)
mapdl.show("close")

# pressure versus radial displacement for the node with max. deformation
mapdl.nsol(6, 65269, "U", "Y", "UY_1")
mapdl.prod(ir=7, ia=6, ib=6, ic="", name="UY2_1")
mapdl.nsol(8, 65269, "U", "X", "UX_1")
mapdl.prod(ir=9, ia=8, ib=8, ic="", name="UX2_1")
mapdl.add(10, 7, 9, "sum")
mapdl.sqrt(ir=11, ia=10, name="Urad")
mapdl.xvar(11)
mapdl.show("png")
mapdl.xrange(4)
mapdl.yrange(0.24)
mapdl.axlab("X", "Radial Displacement")
mapdl.aylab("Y", "Applied Pressure")
mapdl.plvar(12)
mapdl.show("close")
mapdl.finish()

#%%
###############################################################################
# Exit MAPDL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Exit MAPDL instance

mapdl.exit()
