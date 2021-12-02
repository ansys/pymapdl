r"""
.. _ref_vm6_example:

Beam Stresses and Deflections
-----------------------------
Problem Description:
 - A standard 30 inch WF beam, with a cross-sectional area :math:`A`,
   is supported as shown below and loaded on the overhangs by a
   uniformly distributed load :math:`w`. Determine the maximum bending
   stress, :math:`\sigma_max`, in the middle portion of the beam and
   the deflection, :math:`\delta`, at the middle of the beam.

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
 - The deflection, :math:`\delta`, at the middle of the beam can be defined
   by the formulas of the transversally loaded beam:
   :math:`\delta = 0.182 in`

"""
# sphinx_gallery_thumbnail_path = '_static/vm2_setup.png'

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
# Set up the element type (a beam-type).

# Type of analysis: Static.
mapdl.antype("STATIC")

# Element type: BEAM188.
mapdl.et(1, "SHELL181")

# Special Features are defined by keyoptions of beam element:

# KEYOPT(3)
# Integration option:
# Full integration with incompatible modes.
mapdl.keyopt(1, 3, 2)  # Cubic shape function


###############################################################################


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material.

mapdl.mp("EX", 1, 10.5E6)
mapdl.mp("NUXY", 1, 0.3125)
print(mapdl.mplist())


###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a beam element.

w_f = 1.048394965
w_w = 0.6856481
sec_num = 1
mapdl.sectype(secid=sec_num, type_="SHELL", name='shell181')
mapdl.secdata(0.094,1,0,5)

#
# ###############################################################################
# CSYS,1
# K,1,4.953 ! DEFINE MODEL GEOMETRY
# K,2,4.953,,5.175
# KGEN,2,1,2,1,,90
# A,1,2,4,3
# ESIZE,,8
# AMESH,1
# CSYS,0
# ###############################################################################
#
#
# ###############################################################################
# NSEL,S,LOC,X,0
# DSYM,SYMM,X,0
# NSEL,S,LOC,Y,0
# DSYM,SYMM,Y,0
# NSEL,S,LOC,Z,0
# DSYM,SYMM,Z,0
# NSEL,ALL
# ###############################################################################
#
#
# ###############################################################################
# FK,3,FY,-25
# FINISH
# ###############################################################################
#
#
# ###############################################################################
# /SOLU
# SOLVE
# FINISH
# ###############################################################################
#
#
# ###############################################################################
# /POST1
# NSEL,S,LOC,Y,4.953 ! SELECT NODE AT LOAD APPLICATION
# NSEL,R,LOC,Z,0
# NSEL,R,LOC,X,0
# PRNSOL,U,COMP ! PRINT DISPLACEMENTS AND VECTOR SUM
# ###############################################################################
#
#
# ###############################################################################
# TOP_NODE = NODE (4.953,90,0)
# ###############################################################################
#
#
# ###############################################################################
# *GET,DISP,NODE,TOP_NODE,U,Y
# ###############################################################################
#
#
# ###############################################################################
# *DIM,LABEL,CHAR,1
# LABEL(1) = 'DEF_IN'
# ###############################################################################
#
#
# ###############################################################################
# *DIM,VALUE,,1,3
# *VFILL,VALUE(1,1),DATA,0.1139
# *VFILL,VALUE(1,2),DATA,ABS(DISP)
# *VFILL,VALUE(1,3),DATA,ABS( DISP /0.1139 )
# ###############################################################################
#
#
# ###############################################################################
# SAVE,TABLE_1
# FINISH
# ###############################################################################
#
#
#
#
#
#
# ###############################################################################
# ! VM6 with element SHELL281
# /CLEAR,NOSTART
# /TITLE, VM6, PINCHED CYLINDER
# C*** USING SHELL281 ELEMENTS
# ###############################################################################
#
#
# ###############################################################################
# /PREP7
# ANTYPE,STATIC
# ET,1,SHELL281
# SECTYPE,1,SHELL
# SECDATA,0.094,1,0,5
# ###############################################################################
#
#
# ###############################################################################
# MP,EX,,10.5E6
# MP,NUXY,,.3125
# ###############################################################################
#
#
# ###############################################################################
# CSYS,1
# K,1,4.953 ! DEFINE MODEL GEOMETRY
# K,2,4.953,,5.175
# KGEN,2,1,2,1,,90
# A,1,2,4,3
# ESIZE,,8
# AMESH,1
# CSYS,0
# ###############################################################################
#
#
# ###############################################################################
# NSEL,S,LOC,X,0
# DSYM,SYMM,X,0
# NSEL,S,LOC,Y,0
# DSYM,SYMM,Y,0
# NSEL,S,LOC,Z,0
# DSYM,SYMM,Z,0
# NSEL,ALL
# ###############################################################################
#
#
# ###############################################################################
# FK,3,FY,-25
# FINISH
# ###############################################################################
#
#
# ###############################################################################
# /SOLU
# SOLVE
# FINISH
# ###############################################################################
#
#
# ###############################################################################
# /POST1
# NSEL,S,LOC,Y,4.953 ! SELECT NODE AT LOAD APPLICATION
# NSEL,R,LOC,Z,0
# NSEL,R,LOC,X,0
# PRNSOL,U,COMP ! PRINT DISPLACEMENTS AND VECTOR SUM
# ###############################################################################
#
#
# ###############################################################################
# TOP_NODE = NODE (4.953,90,0)
# ###############################################################################
#
#
# ###############################################################################
# *GET,DISP,NODE,TOP_NODE,U,Y
# ###############################################################################
#
#
# ###############################################################################
# *DIM,LABEL,CHAR,1
# LABEL(1) = 'DEF_IN'
# ###############################################################################
#
#
# ###############################################################################
# *DIM,VALUE,,1,3
# *VFILL,VALUE(1,1),DATA,0.1139
# *VFILL,VALUE(1,2),DATA,ABS(DISP)
# *VFILL,VALUE(1,3),DATA,ABS( DISP /0.1139 )
# SAVE,TABLE_2
# ###############################################################################
#
#
# ###############################################################################
# RESUME,TABLE_1
# ###############################################################################
#
#
# ###############################################################################
# /COM
# /OUT,vm6,vrt
# /COM,------------------- VM6 RESULTS COMPARISON ---------------------
# /COM,
# /COM, | TARGET | Mechanical APDL | RATIO
# /COM,
# /COM,
# /COM,
# /COM,SHELL181
# /COM,
# *VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)
# (1X,A10,' ',F10.4,' ',F14.4,' ',1F13.3)
# /NOPR
# RESUME,TABLE_2
# /GOPR
# /COM,
# /COM,SHELL281
# /COM,
# *VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)
# (1X,A10,' ',F10.4,' ',F14.4,' ',1F13.3)
# /COM,-----------------------------------------------------------------
# /OUT
# FINISH
# ###############################################################################
#
#
# ###############################################################################
# /DEL,TABLE_1
# /DEL,TABLE_2
# FINISH
# ###############################################################################
#
#
# ###############################################################################
# *LIST,vm6,vrt
# ###############################################################################
