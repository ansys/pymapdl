r"""
.. _ref_vm7_example:

Plastic Compression of a Pipe Assembly
--------------------------------------
Problem Description:
 - Two coaxial tubes, the inner one of 1020 CR steel and cross-sectional area As,
   and the outer one of 2024-T4 aluminum alloy and of area Aa, are compressed
   between heavy, flat end plates, as shown below. Determine the load-deflection
   curve of the assembly as it is compressed into the plastic region by
   an axial displacement. Assume that the end plates are so stiff that both tubes
   are shortened by exactly the same amount.

Reference:
 - S. H. Crandall, N. C. Dahl, An Introduction to the Mechanics of Solids, McGraw-Hill
   Book Co., Inc., New York, NY, 1959, pg. 180, ex. 5.1.

Analysis Type(s):
 - Static, Plastic Analysis (``ANTYPE=0``)

Element Type(s):
 - Plastic Straight Pipe Element (PIPE288)
 - 4-Node Finite Strain Shell (SHELL181)
 - 3-D Structural Solid Elements (SOLID185)

.. image:: ../../_static/vm7_setup.png
   :width: 400
   :alt: VM7 Problem Sketch

Material Properties
 -

Geometric Properties:
 -

Loading:
 - 1st Load Step: :math:`\delta = 0.032 in`
 - 2nd Load Step: :math:`\delta = 0.050 in`
 - 3rd Load Step: :math:`\delta = 0.100 in`

Analytical Equations:
 -

"""
# sphinx_gallery_thumbnail_path = '_static/vm7_setup.png'

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~

from ansys.mapdl.core import launch_mapdl

# Start mapdl and clear it.
mapdl = launch_mapdl()
mapdl.clear()

# Enter verification example mode and the pre-processing routine.
mapdl.verify("VM7")
mapdl.prep7()


###############################################################################
#

mapdl.et(1, "PIPE288", "", "", "", 2)

mapdl.et(2, "SOLID185")

mapdl.et(3, "SHELL181", "", "", 2)  # FULL INTEGRATION

mapdl.sectype(1, "SHELL")

mapdl.secdata(0.5, 1, 0, 5)  # THICKNESS (SHELL181)

mapdl.sectype(2, "SHELL")

mapdl.secdata(0.5, 2, 0, 5)  # THICKNESS (SHELL181)

mapdl.sectype(3, "PIPE")

mapdl.secdata(4.9563384, 0.5)  # OUTSIDE DIA. AND WALL THICKNESS FOR INSIDE TUBE (PIPE288)

mapdl.sectype(4, "PIPE")

mapdl.secdata(8.139437, 0.5)  # OUTSIDE DIA. AND WALL THICKNESS FOR OUTSIDE TUBE (PIPE288)

mapdl.mp("EX", 1, 26.875E6)  # STEEL

mapdl.mp("PRXY", 1, 0.3)

mapdl.mp("EX", 2, 11E6)  # ALUMINUM

mapdl.mp("PRXY", 2, 0.3)

mapdl.tb("BKIN", 1, 1)  # DEFINE NON-LINEAR MATERIAL PROPERTY FOR STEEL

mapdl.tbtemp(0)

mapdl.tbdata(1, 86000, 0)

mapdl.tb("BKIN", 2, 1)  # DEFINE NON-LINEAR MATERIAL PROPERTY FOR ALUMINUM

mapdl.tbtemp(0)

mapdl.tbdata(1, 55000, 0)

mapdl.n(1)  # GENERATE NODES AND ELEMENTS FOR PIPE288

mapdl.n(2, "", "", 10)

mapdl.mat(1)

mapdl.secnum(3)  # STEEL (INSIDE) TUBE

mapdl.e(1, 2)

mapdl.mat(2)

mapdl.secnum(4)  # ALUMINUM (OUTSIDE) TUBE

mapdl.e(1, 2)

mapdl.csys(1)

mapdl.n(101, 1.9781692)  # GENERATE NODES AND ELEMENTS FOR SOLID185

mapdl.n(102, 2.4781692)

mapdl.n(103, 3.5697185)

mapdl.n(104, 4.0697185)

mapdl.n(105, 1.9781692, "", 10)

mapdl.n(106, 2.4781692, "", 10)

mapdl.n(107, 3.5697185, "", 10)

mapdl.n(108, 4.0697185, "", 10)

mapdl.ngen(2, 10, 101, 108, "", "", "THETA")  # GENERATE 2ND SET OF NODES TO FORM A THETA DEGREE SLICE

mapdl.nrotat(101, 118, 1)

mapdl.type(2)

mapdl.mat(1)  # INSIDE (STEEL) TUBE

mapdl.e(101, 102, 112, 111, 105, 106, 116, 115)

mapdl.mat(2)  # OUTSIDE (ALUMINUM) TUBE

mapdl.e(103, 104, 114, 113, 107, 108, 118, 117)

mapdl.n(201, 2.2281692)  # GENERATE NODES AND ELEMENTS FOR SHELL181

mapdl.n(203, 2.2281692, "", 10)

mapdl.n(202, 3.8197185)

mapdl.n(204, 3.8197185, "", 10)

mapdl.ngen(2, 4, 201, 204, "", "", "THETA")  # GENERATE NODES TO FORM A THETA DEGREE SLICE

mapdl.type(3)

mapdl.secnum(1)  # INSIDE (STEEL) TUBE

mapdl.e(203, 201, 205, 207)

mapdl.secnum(2)  # OUTSIDE (ALUMINUM) TUBE

mapdl.e(204, 202, 206, 208)

mapdl.run("C*** APPLY CONSTRAINTS TO PIPE288 MODEL")

mapdl.d(1, "ALL")  # FIX ALL DOFS FOR BOTTOM END OF PIPE288

mapdl.d(2, "UX", "", "", "", "", "UY", "ROTX", "ROTY", "ROTZ")  # ALLOW ONLY UZ DOF AT TOP END OF PIPE288 MODEL

mapdl.run("C*** APPLY CONSTRAINTS TO SOLID185 AND SHELL181 MODELS")

mapdl.cp(1, "UX", 101, 111, 105, 115)  # COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SOLID185

mapdl.cpsgen(4, "", 1)

mapdl.cp(5, "UX", 201, 205, 203, 20)  # COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SHELL181

mapdl.cpsgen(2, "", 5)

mapdl.cp(7, "ROTY", 201, 205)  # COUPLE NODES AT BOUNDARY IN ROTY DIR FOR SHELL181

mapdl.cpsgen(4, "", 7)

mapdl.nsel("S", "NODE", "", 101, 212)  # SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS

mapdl.nsel("R", "LOC", "Y", 0)  # SELECT NODES AT THETA = 0 FROM THE SELECTED SET

mapdl.dsym("SYMM", "Y", 1)  # APPLY SYMMETRY BOUNDARY CONDITIONS

mapdl.nsel("S", "NODE", "", 101, 212)  # SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS

mapdl.nsel("R", "LOC", "Y", "THETA")  # SELECT NODES AT THETA FROM THE SELECTED SET

mapdl.dsym("SYMM", "Y", 1)  # APPLY SYMMETRY BOUNDARY CONDITIONS

mapdl.nsel("ALL")

mapdl.nsel("R", "LOC", "Z", 0)  # SELECT ONLY NODES AT Z = 0

mapdl.d("ALL", "UZ", 0)  # CONSTRAIN BOTTOM NODES IN Z DIRECTION

mapdl.nsel("ALL")

mapdl.finish()

mapdl.run("/SOLU")

mapdl.outpr("BASIC", "LAST")  # PRINT BASIC SOLUTION AT END OF LOAD STEP

mapdl.run("C*** APPLY DISPLACEMENT LOADS TO ALL MODELS")


def DISP(ARG1='', ARG2='', ARG3='', ARG4='', ARG5='', ARG6='', ARG7='', ARG8='', ARG9='', ARG10='', ARG11='', ARG12='',
         ARG13='', ARG14='', ARG15='', ARG16='', ARG17='', ARG18=''):

    mapdl.nsel("R", "LOC", "Z", 10)  # SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT

    mapdl.d("ALL", "UZ", ARG1)

    mapdl.nsel("ALL")

    with mapdl.non_interactive:

        mapdl.run("/OUT,SCRATCH")

        mapdl.solve()

# DISP(-.032)
#
# DISP(-.05)
#
# DISP(-.1)
#
# mapdl.finish()
#
# with mapdl.non_interactive:
#
#     mapdl.run("/OUT,")
#
#     mapdl.run("/POST1")
#
#     mapdl.run("C*** CREATE MACRO TO GET RESULTS FOR EACH MODEL")
#
#
#
#
#
# def GETLOAD(ARG1='', ARG2='', ARG3='', ARG4='', ARG5='', ARG6='',            ARG7='', ARG8='', ARG9='', ARG10='', ARG11='', ARG12='',            ARG13='', ARG14='', ARG15='', ARG16='', ARG17='', ARG18=''):
#
#         mapdl.nsel("S", "NODE", "", 1, 2)  # SELECT NODES IN PIPE288 MODEL
#
#         mapdl.nsel("R", "LOC", "Z", 0)
#
#         mapdl.run("/OUT,SCRATCH")
#
#         mapdl.fsum()  # FZ IS TOTAL LOAD FOR PIPE288 MODEL
#
#         mapdl.run("*GET,LOAD_288,FSUM,,ITEM,FZ")
#
#         mapdl.nsel("S", "NODE", "", 101, 118)  # SELECT NODES IN SOLID185 MODEL
#
#         mapdl.nsel("R", "LOC", "Z", 0)
#
#         mapdl.fsum()
#
#         mapdl.run("*GET,ZFRC,FSUM,0,ITEM,FZ")
#
#         mapdl.run("LOAD=ZFRC*360/THETA                 ")  # MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
#
#         mapdl.run("*STATUS,LOAD")
#
#         mapdl.run("LOAD_185 = LOAD")
#
#         mapdl.nsel("S", "NODE", "", 201, 212)  # SELECT NODES IN SHELL181 MODEL
#
#         mapdl.nsel("R", "LOC", "Z", 0)
#
#         mapdl.fsum()
#
#         mapdl.run("/OUT,")
#
#         mapdl.run("*GET,ZFRC,FSUM,0,ITEM,FZ")
#
#         mapdl.run("LOAD=ZFRC*360/THETA                 ")  # MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
#
#         mapdl.run("*STATUS,LOAD")
#
#         mapdl.run("LOAD_181 = LOAD")
#
#         mapdl.run("*VFILL,VALUE_288(1,1),DATA,1024400,1262000,1262000")
#
#         mapdl.run("*VFILL,VALUE_288(I,2),DATA,ABS(LOAD_288)")
#
#         mapdl.run("*VFILL,VALUE_288(I,3),DATA,ABS(LOAD_288)/(VALUE_288(I,1))")
#
#         mapdl.run("*VFILL,VALUE_185(1,1),DATA,1024400,1262000,1262000")
#
#         mapdl.run("*VFILL,VALUE_185(J,2),DATA,ABS(LOAD_185)")
#
#         mapdl.run("*VFILL,VALUE_185(J,3),DATA,ABS(LOAD_185)/(VALUE_185(J,1))")
#
#         mapdl.run("*VFILL,VALUE_181(1,1),DATA,1024400,1262000,1262000")
#
#         mapdl.run("*VFILL,VALUE_181(K,2),DATA,ABS(LOAD_181)")
#
#         mapdl.run("*VFILL,VALUE_181(K,3),DATA,ABS(LOAD_181)/(VALUE_181(K,1))")
#
#
#     mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.032")
#
#     mapdl.run("C*** ---------------------------------------")
#
#     mapdl.set(1, 1)
#
#     mapdl.run("I = 1")
#
#     mapdl.run("J = 1")
#
#     mapdl.run("K = 1")
#
#     mapdl.run("*DIM,LABEL,CHAR,3,2")
#
#     mapdl.run("*DIM,VALUE_288,,3,3")
#
#     mapdl.run("*DIM,VALUE_185,,3,3")
#
#     mapdl.run("*DIM,VALUE_181,,3,3")
#
#
# GETLOAD()
#
#     mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.05")
#
#     mapdl.run("C*** --------------------------------------")
#
#     mapdl.set(2, 1)
#
#     mapdl.run("I = I + 1")
#
#     mapdl.run("J = J + 1")
#
#     mapdl.run("K = K + 1")
#
# GETLOAD()
#
#     mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.1")
#
#     mapdl.run("C*** -------------------------------------")
#
#     mapdl.set(3, 1)
#
#     mapdl.run("I = I +1")
#
#     mapdl.run("J = J + 1")
#
#     mapdl.run("K = K + 1")
#
# GETLOAD()
#
#     mapdl.run("LABEL(1,1) = 'LOAD, lb','LOAD, lb','LOAD, lb'")
#
#     mapdl.run("LABEL(1,2) = ' UX=.032',' UX=0.05',' UX=0.10'")
#
#     mapdl.finish()
#
#     mapdl.run("/OUT,vm7,vrt")
#
#     mapdl.run("/COM,------------------- VM7 RESULTS COMPARISON ---------------------")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,                 |   TARGET   |   Mechanical APDL   |   RATIO")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,RESULTS FOR PIPE288:")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_288(1,1),VALUE_288(1,2),VALUE_288(1,3)")
#
#     mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,RESULTS FOR SOLID185:")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_185(1,1),VALUE_185(1,2),VALUE_185(1,3)")
#
#     mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,RESULTS FOR SHELL181:")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_181(1,1),VALUE_181(1,2),VALUE_181(1,3)")
#
#     mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
#
#     mapdl.run("/COM,")
#
#     mapdl.run("/COM,-----------------------------------------------------------------")
#
#     mapdl.run("/OUT")
#
#     mapdl.run("/GOPR")
#
#     mapdl.run("*LIST,vm7,vrt")
#
# mapdl.exit()