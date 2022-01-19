###############################################################################
#

from ansys.mapdl.core import launch_mapdl
mapdl = launch_mapdl(loglevel="WARNING")


###############################################################################
#

mapdl.prep7()

###############################################################################
#

mapdl.et(1, "COMBIN14", "", "", 2)  # UX AND UY DOF ELEMENT
mapdl.et(3, "COMBIN40", "", "", "", "", "", 2)  # ALL MASS IS AT NODE J, UX DOF ELEMENT
mapdl.et(4, "COMBIN40", "", "", 2, "", "", 2)  # ALL MASS IS AT NODE J, UY DOF ELEMENT


###############################################################################
#

mapdl.r(1, 1)  # SPRING STIFFNESS = 1
mapdl.r(2, 8)  # SPRING STIFFNESS = 8
mapdl.r(3, "", 1.41, 1)  # C = 1.41, M = 1
mapdl.r(4, "", 2, 1)  # C = 2, M = 1


###############################################################################
#

mapdl.n(1)
mapdl.n(2, "", 10)
mapdl.n(3, "", 20)
mapdl.n(4, -1, 10)
mapdl.n(5, "", 9)


###############################################################################
#

mapdl.e(1, 2)  # ELEMENT 1 IS SPRING ELEMENT WITH STIFFNESS 1
mapdl.real(2)
mapdl.e(2, 3)  # ELEMENT 2 IS SPRING ELEMENT WITH STIFFNESS 8
mapdl.type(3)
mapdl.real(3)
mapdl.e(4, 2)  # ELEMENT 3 IS COMBINATION ELEMENT WITH C = 1.41
mapdl.type(4)
mapdl.real(4)
mapdl.e(5, 2)  # ELEMENT 4 IS COMBINATION ELEMENT WITH C = 2


###############################################################################
#

mapdl.nsel("U", "NODE", "", 2)
mapdl.d("ALL", "ALL")
mapdl.nsel("ALL")
mapdl.finish()


###############################################################################
#

mapdl.run("/SOLU")
mapdl.antype("TRANS")  # FULL TRANSIENT DYNAMIC ANALYSIS
mapdl.nlgeom("ON")  # LARGE DEFLECTION
mapdl.kbc(1)  # STEP BOUNDARY CONDITION
mapdl.f(2, "FX", 5)
mapdl.f(2, "FY", 5)
mapdl.autots("ON")
mapdl.nsubst(30)
mapdl.outpr("", "LAST")
mapdl.outpr("VENG", "LAST")
mapdl.time(15)  # ARBITRARY TIME FOR SLOW DYNAMICS


###############################################################################
#
mapdl.solve()
mapdl.finish()


###############################################################################
#

mapdl.run("/POST1")

mapdl.set("", "", "", "", 15)  # USE ITERATION WHEN TIME = 15

mapdl.etable("SENE", "SENE")  # STORE STRAIN ENERGY

mapdl.ssum()  # SUM ALL ACTIVE ENTRIES IN ELEMENT STRESS TABLE

mapdl.run("*GET,ST_EN,SSUM,,ITEM,SENE")

mapdl.prnsol("U", "COMP")  # PRINT DISPLACEMENTS IN GLOBAL COORDINATE SYSTEM

mapdl.run("*GET,DEF_X,NODE,2,U,X")

mapdl.run("*GET,DEF_Y,NODE,2,U,Y")

mapdl.run("*DIM,LABEL,CHAR,3,2")

mapdl.run("*DIM,VALUE,,3,3")

mapdl.run("LABEL(1,1) = 'STRAIN E','DEF_X (C','DEF_Y (C'")
mapdl.run("LABEL(1,2) = ', N-cm  ','m)      ','m)      '")

mapdl.run("*VFILL,VALUE(1,1),DATA,24.01,8.631,4.533")
mapdl.run("*VFILL,VALUE(1,2),DATA,ST_EN ,DEF_X,DEF_Y")
mapdl.run("*VFILL,VALUE(1,3),DATA,ABS(ST_EN/24.01), ABS(8.631/DEF_X), ABS(DEF_Y/4.533 )")


###############################################################################
#

mapdl.run("/COM")
mapdl.run("/OUT,vm9,vrt")
mapdl.run("/COM,------------------- VM9 RESULTS COMPARISON ---------------------")
mapdl.run("/COM,")
mapdl.run("/COM,                 |   TARGET   |   Mechanical APDL   |   RATIO")
mapdl.run("/COM,")
mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
mapdl.run("(1X,A8,A8,'   ',F10.3,'  ',F14.3,'   ',1F15.3)")
mapdl.run("/COM,----------------------------------------------------------------")
mapdl.run("/OUT")
mapdl.run("/GOPR")
mapdl.finish()
