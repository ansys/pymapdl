ANSYS APDL Interactive Control Examples
=======================================
These examples are used to demonstrate how to convert an existing
ANSYS APDL script to a python ``pyansys`` script.  You could also
simply use the built-in ``convert_script`` function within pyansys:

.. code:: python

    import pyansys

    inputfile = 'ansys_inputfile.inp'
    pyscript = 'pyscript.py'
    pyansys.convert_script(inputfile, pyscript)


Torsional Load on a Bar using SURF154 Elements
----------------------------------------------
This ANSYS APDL script builds a bar and applies torque to it using
SURF154 elements.  This is a static analysis example.


Script Initialization
~~~~~~~~~~~~~~~~~~~~~
Beginning of ANSYS script:

.. code::

    !----------------------------------------
    ! Input torque applied (moment)
    ! Input radius, height, element size...
    !----------------------------------------
    TORQUE = 100
    RADIUS = 2
    H_TIP = 2
    HEIGHT = 20
    ELEMSIZE = 1
    PI = acos(-1)
    FORCE = 100/RADIUS
    PRESSURE = FORCE/(H_TIP*2*PI*RADIUS)

Corresponding ``pyansys`` script including the initialization of
pyansys:

.. code:: python

    import numpy as np
    import os
    import pyansys
    
    # start ANSYS in the current working directory with default jobname "file"
    mapdl = pyansys.launch_mapdl(run_location=os.getcwd(), interactive_plotting=True)
        
    # define cylinder and mesh parameters
    torque = 100
    radius = 2
    h_tip = 2
    height = 20
    elemsize = 0.5
    pi = np.arccos(-1)
    force = 100/radius
    pressure = force/(h_tip*2*np.pi*radius)


Model Creation
~~~~~~~~~~~~~~    
APDL Script:

.. code::

    !----------------------------------------
    ! Define higher-order SOLID186
    ! Define surface effect elements SURF154
    ! which is used to apply torque
    ! as a tangential pressure
    !----------------------------------------
    /prep7
    et, 1, 186
    et, 2, 154
    r,1,
    r,2,
    
    !----------------------------------------
    ! Aluminum properties (or something)
    !----------------------------------------
    mp,ex,1,10e6
    mp,nuxy,1,.3
    mp,dens,1,.1/386.1
    mp,dens,2,0
    
    !----------------------------------------
    ! Simple cylinder
    !----------------------------------------
    *do, ICOUNT, 1, 4
    cylind,RADIUS,,HEIGHTH_TIP,HEIGHT,90*(ICOUNT-1),90*ICOUNT
    *enddo
        
    nummrg,kp
    lsel,s,loc,x,0
    
    lsel,r,loc,y,0
    lsel,r,loc,z,0,HEIGHT-H_TIP
    lesize,all,ELEMSIZE*2
    mshape,0
    mshkey,1
    esize,ELEMSIZE
    allsel,all
    VSWEEP, ALL
    csys,1
    asel,s,loc,z,HEIGHT-H_TIP+0.0001,HEIGHT0.0001
    asel,r,loc,x,RADIUS
    local,11,1
    csys,0
    aatt,2,2,2,11
    amesh,all
    finish

Corresponding ``pyansys`` script:

.. code:: python

    # Define higher-order SOLID186
    # Define surface effect elements SURF154 to apply torque
    # as a tangential pressure
    mapdl.prep7()
    mapdl.et(1, 186)
    mapdl.et(2, 154)
    mapdl.r(1)
    mapdl.r(2)
    
    # Aluminum properties (or something)
    mapdl.mp('ex', 1, 10e6)
    mapdl.mp('nuxy', 1, 0.3)
    mapdl.mp('dens', 1, 0.1/386.1)
    mapdl.mp('dens', 2, 0)
    
    # Simple cylinder
    for i in range(4):
        mapdl.cylind(radius, '', '', height, 90*(i-1), 90*i)
    
    mapdl.nummrg('kp')
    
    # non-interactive volume plot (optional)
    mapdl.show()
    mapdl.menu('grph')
    mapdl.view(1, 1, 1, 1)
    mapdl.vplot()
    mapdl.wait(1)
    
    # mesh cylinder
    mapdl.lsel('s', 'loc', 'x', 0)
    mapdl.lsel('r', 'loc', 'y', 0)
    mapdl.lsel('r', 'loc', 'z', 0, height - h_tip)
    mapdl.lesize('all', elemsize*2)
    mapdl.mshape(0)
    mapdl.mshkey(1)
    mapdl.esize(elemsize)
    mapdl.allsel('all')
    mapdl.vsweep('ALL')
    mapdl.csys(1)
    mapdl.asel('s', 'loc', 'z', '', height - h_tip + 0.0001)
    mapdl.asel('r', 'loc', 'x', radius)
    mapdl.local(11, 1)
    mapdl.csys(0)
    mapdl.aatt(2, 2, 2, 11)
    mapdl.amesh('all')
    mapdl.finish()

    # plot elements and wait one second (optional)
    mapdl.eplot()
    mapdl.wait(1)

.. figure:: ./images/cylinder_eplot.png
    :width: 300pt

    Element plot from ``pyansys`` using ``matplotlib``


Solution
~~~~~~~~
APDL script:

.. code::

    /solu
    antype,static,new
    eqslv,pcg,1e-8
    
    !----------------------------------------
    ! Apply tangential pressure
    !----------------------------------------
    esel,s,type,,2
    sfe,all,2,pres,,PRESSURE
    
    !----------------------------------------
    ! Constrain bottom of cylinder/rod
    !----------------------------------------
    asel,s,loc,z,0
    nsla,s,1
    d,all,all
    allsel,all
    /psf,pres,,2
    /pbc,u,1
    /title, Simple torsional example
    solve
    finish
    /post1
    set,last
    fsum
    esel,u,type,,2
    SAVE


Corresponding ``pyansys`` script:

.. code:: python

    # new solution
    mapdl.slashsolu()  # Using Slash instead of / due to duplicate SOLU command
    # ansys('/solu')  # could also use this line
    mapdl.antype('static', 'new')
    mapdl.eqslv('pcg', 1e-8)

    # Apply tangential pressure
    mapdl.esel('s', 'type', '', 2)
    mapdl.sfe('all', 2, 'pres', '', pressure)

    # Constrain bottom of cylinder/rod
    mapdl.asel('s', 'loc', 'z', 0)
    mapdl.nsla('s', 1)

    mapdl.d('all', 'all')
    mapdl.allsel()
    mapdl.psf('pres', '', 2)
    mapdl.pbc('u', 1)
    mapdl.solve()
    mapdl.exit()  # Finishes, saves, and exits


Access and plot the results within python using pyansys:

.. code:: python

    # open the result file using the path used in ANSYS
    resultfile = os.path.join(mapdl.path, 'file.rst')
    result = pyansys.read_binary(resultfile)

    # access element results as arrays
    nnum, stress = result.nodal_stress(0)
    element_stress, elemnum, enode = result.element_stress(0)
    nodenum, stress = result.nodal_stress(0)

    # plot interactively
    result.plot_nodal_solution(0, cmap='bwr')
    result.plot_nodal_stress(0, 'Sx', cmap='bwr')
    result.plot_principal_nodal_stress(0, 'SEQV', cmap='bwr')

    # plot and save non-interactively
    cpos = [(20.992831318277517, 9.78629316586435, 31.905115108541928),
            (0.35955395443745797, -1.4198191001571547, 10.346158032932495),
            (-0.10547549888485548, 0.9200673323892437, -0.377294345312956)]

    result.plot_nodal_solution(0, interactive=False, cpos=cpos,
                               screenshot=os.path.join(path, 'cylinder_disp.png'))

    result.plot_nodal_stress(0, 'Sx', cmap='bwr', interactive=False, cpos=cpos,
                             screenshot=os.path.join(path, 'cylinder_sx.png'))

    result.plot_principal_nodal_stress(0, 'SEQV', cmap='bwr', interactive=False,
                                       cpos=cpos, screenshot=os.path.join(path, 'cylinder_vonmises.png'))

.. figure:: ./images/cylinder_disp.png
    :width: 300pt

    Non-interactive Screenshot of Displacement from ``pyansys``

.. figure:: ./images/cylinder_sx.png
    :width: 300pt

    Non-interactive Screenshot of X Stress from ``pyansys``

.. figure:: ./images/cylinder_vonmises.png
    :width: 300pt

    Non-interactive Screenshot of von Mises Stress from ``pyansys``


Spotweld SHELL181 Example
-------------------------
This ANSYS APDL example demonstrates how to model spot welding on three thin sheets of metal.  This example has yet to be translated to a ``pyansys`` script.

.. code::

    !----------------------------------------
    ! Example problem for demonstrating 
    ! Spotweld technology 
    !----------------------------------------
    ! 
    !----------------------------------------
    ! Originated in 9.0 JJDoyle 2004/09/01
    !----------------------------------------
    /prep7
    /num,0
    /pnum,area,1
    
    k,1,2,10,
    k,2,10,10
    k,3,10,0.15
    k,4,14,0.15
    !
    l,1,2
    l,2,3
    l,3,4
    lfillt,1,2,3
    lfillt,2,3,2
    !
    k,9,,
    k,10,11,
    k,11,15,
    l,9,10
    l,10,11
    
    k,12,,10
    lsel,s,,,6,7
    AROTAT,all,,,,,,9,12,12,1,
    
    lsel,s,,,1,5
    AROTAT,all,,,,,,9,12,12,1,
    areverse,1
    areverse,2
    
    asel,s,,,3,7
    ARSYM,Y,all, , , ,0,0 
    allsel
    
    !********
    !define weld location with hardpoint
    !********
    HPTCREATE,AREA,7,0,COORD,12.9,0.15,-1.36,  
    
    /view,1,1,1,1
    gplo
    !
    et,1,181
    r,1,0.15
    r,2,0.1
    !
    mp,ex,1,30e6
    mp,prxy,1,0.3
    !
    esize,0.25
    real,1
    amesh,1
    amesh,2
    real,2
    asel,s,,,3,12
    amesh,all
    !
    lsel,s,,,1,9
    lsel,a,,,12,17
    lsel,a,,,26,38,3
    lsel,a,,,24,36,3
    nsll,s,1
    wpstyle,0.05,0.1,-1,1,0.003,0,0,,5  
    WPSTYLE,,,,,,,,1
    wpro,,-90.000000,
    CSWPLA,11,1,1,1, 
    csys,11 
    nrotat,all
    d,all,uy
    d,all,rotx
    
    csys,0
    
    lsel,s,,,23
    nsll,s,1
    d,all,uz
    
    lsel,s,,,17
    nsll,s,1
    d,all,uz,4
    
    ALLSEL
    /view,1,1,1,1
    /eshape,1
    ksel,s,,,33
    nslk,s,1
    *get,sw_node,node,,num,max
    
    /solu
    allsel
    nlgeom,on
    time,4
    nsubst,10,25,5
    outres,all,all
    fini
    
    !------------------------------------
    !build flex spotweld with BEAM188, run the solution,
    !and post process results
    !------------------------------------
    fini
    allsel
    /prep7
    mp,ex,2,28e6
    mp,prxy,2,0.3
    !
    SECTYPE,2,beam,csolid
    SECDATA,0.25
    !
    et,2,188
    type,2
    mat,2
    secnum,2
    
    SWGEN,sweld1,0.50,7,2,sw_node,,	
    SWADD,sweld1,,12
    
    /solu
    allsel
    nlgeom,on
    time,4
    nsubst,10,25,5
    outres,all,all
    solve
    FINISH

Here's the Python script using ``pyansys`` to access the results after
running the ANSYS analysis.

.. code:: python
    
    import pyansys
    
    # Open the result file and plot the displacement of time step 3
    resultfile = os.path.join('file.rst')
    result = pyansys.read_binary(resultfile)
    result.plot_nodal_solution(2)

.. figure:: ./images/spot_disp.png
    :width: 300pt

    Spot Weld: Displacement

Get the nodal and element component stress at time step 0.  Plot the
stress in the Z direction.

.. code:: python

    nodenum, stress = result.nodal_stress(0)
    element_stress, elemnum, enode = result.element_stress(0)
    
    # Plot the Z direction stress:
    # The stress at the contact element simulating the spot weld
    result.plot_nodal_stress(0, 'Sz')

.. figure:: ./images/spot_sz.png
    :width: 300pt

    Spot Weld: Z Stress

.. code:: python

    # Get the principal nodal stress and plot the von Mises Stress
    nnum, pstress = result.principal_nodal_stress(0)
    result.plot_principal_nodal_stress(0, 'SEQV')

.. figure:: ./images/spot_seqv.png
    :width: 300pt

    Spot Weld: von Mises Stress


Example: VM1 - Statically Indeterminate Reaction Force Analysis
---------------------------------------------------------------
ANSYS APDL contains over 200 verification files used for ANSYS
validation and demonstration.  These validation files are used here to
demo the use of the ``pyansys`` file translator ``pyansys.convert_script``.

This example translates the verification example ``"vm1.dat"``.
First, the MAPDL code:

.. code::

    /COM,ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150
    /VERIFY,VM1
    /PREP7
    /TITLE, VM1, STATICALLY INDETERMINATE REACTION FORCE ANALYSIS
    C***      STR. OF MATL., TIMOSHENKO, PART 1, 3RD ED., PAGE 26, PROB.10
    ANTYPE,STATIC                  ! STATIC ANALYSIS
    ET,1,LINK180
    SECTYPE,1,LINK
    SECDATA,1  			       ! CROSS SECTIONAL AREA (ARBITRARY) = 1
    MP,EX,1,30E6
    N,1
    N,2,,4
    N,3,,7
    N,4,,10
    E,1,2                          ! DEFINE ELEMENTS
    EGEN,3,1,1
    D,1,ALL,,,4,3                  ! BOUNDARY CONDITIONS AND LOADING
    F,2,FY,-500
    F,3,FY,-1000
    FINISH
    /SOLU    
    OUTPR,BASIC,1
    OUTPR,NLOAD,1
    SOLVE
    FINISH
    /POST1
    NSEL,S,LOC,Y,10
    FSUM
    *GET,REAC_1,FSUM,,ITEM,FY
    NSEL,S,LOC,Y,0
    FSUM
    *GET,REAC_2,FSUM,,ITEM,FY
    
    *DIM,LABEL,CHAR,2
    *DIM,VALUE,,2,3
    LABEL(1) = 'R1, lb','R2, lb '
    *VFILL,VALUE(1,1),DATA,900.0,600.0
    *VFILL,VALUE(1,2),DATA,ABS(REAC_1),ABS(REAC_2)
    *VFILL,VALUE(1,3),DATA,ABS(REAC_1 / 900) ,ABS( REAC_2 / 600)
    /OUT,vm1,vrt
    /COM
    /COM,------------------- VM1 RESULTS COMPARISON ---------------------
    /COM,
    /COM,         |   TARGET   |   Mechanical APDL   |   RATIO
    /COM,
    *VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)
    (1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)
    /COM,----------------------------------------------------------------
    /OUT
    FINISH
    *LIST,vm1,vrt

This verification file was translated using:

.. code:: python

    import pyansys
    pyansys.convert_script('vm1.dat', 'vm1.py')

Translated code:

.. code:: python

    """ Script generated by pyansys version 0.42.0"""
    import pyansys
    mapdl = pyansys.launch_mapdl("/usr/ansys_inc/v182/ansys/bin/ansys182",
                                 loglevel="INFO")
    mapdl.run("/COM,ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150")
    mapdl.run("/VERIFY,VM1")
    mapdl.run("/PREP7")
    mapdl.run("/TITLE, VM1, STATICALLY INDETERMINATE REACTION FORCE ANALYSIS")
    mapdl.run("C***      STR. OF MATL., TIMOSHENKO, PART 1, 3RD ED., PAGE 26, PROB.10")
    mapdl.antype("STATIC")  #STATIC ANALYSIS
    mapdl.et(1, "LINK180")
    mapdl.sectype(1, "LINK")
    mapdl.secdata(1)  #CROSS SECTIONAL AREA (ARBITRARY) = 1
    mapdl.mp("EX", 1, 30E6)
    mapdl.n(1)
    mapdl.n(2, "", 4)
    mapdl.n(3, "", 7)
    mapdl.n(4, "", 10)
    mapdl.e(1, 2)  #DEFINE ELEMENTS
    mapdl.egen(3, 1, 1)
    mapdl.d(1, "ALL", "", "", 4, 3)  #BOUNDARY CONDITIONS AND LOADING
    mapdl.f(2, "FY", -500)
    mapdl.f(3, "FY", -1000)
    mapdl.finish()
    mapdl.run("/SOLU")
    mapdl.outpr("BASIC", 1)
    mapdl.outpr("NLOAD", 1)
    mapdl.solve()
    mapdl.finish()
    mapdl.run("/POST1")
    mapdl.nsel("S", "LOC", "Y", 10)
    mapdl.fsum()
    mapdl.run("*GET,REAC_1,FSUM,,ITEM,FY")
    mapdl.nsel("S", "LOC", "Y", 0)
    mapdl.fsum()
    mapdl.run("*GET,REAC_2,FSUM,,ITEM,FY")
    mapdl.run("*DIM,LABEL,CHAR,2")
    mapdl.run("*DIM,VALUE,,2,3")
    mapdl.run("LABEL(1) = 'R1, lb','R2, lb '")
    mapdl.run("*VFILL,VALUE(1,1),DATA,900.0,600.0")
    mapdl.run("*VFILL,VALUE(1,2),DATA,ABS(REAC_1),ABS(REAC_2)")
    mapdl.run("*VFILL,VALUE(1,3),DATA,ABS(REAC_1 / 900) ,ABS( REAC_2 / 600)")
    mapdl.run("/OUT,vm1,vrt")
    mapdl.run("/COM")
    mapdl.run("/COM,------------------- VM1 RESULTS COMPARISON ---------------------")
    mapdl.run("/COM,")
    mapdl.run("/COM,         |   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.run("/COM,")
    with mapdl.non_interactive:
        mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
    mapdl.run("/COM,----------------------------------------------------------------")
    mapdl.run("/OUT")
    mapdl.finish()
    mapdl.run("*LIST,vm1,vrt")
    mapdl.exit()


Results from running the converted file:

.. code::

    2018-08-20 23:23:35,022 [INFO] pyansys.ansys:
    ------------------- VM1 RESULTS COMPARISON ---------------------
    |   TARGET   |   Mechanical APDL   |   RATIO
    /INPUT FILE=    LINE=       0
    R1, lb          900.0       900.0   1.000
    R2, lb          600.0       600.0   1.000
    ----------------------------------------------------------------

You can verify the reaction forces with:

.. code::

   >>> rst = mapdl.result
   >>> nnum, forces = rst.nodal_static_forces(0)
   >>> print(forces)
   [[   0. -600.    0.]
    [   0.  250.    0.]
    [   0.  500.    0.]
    [   0. -900.    0.]]

Note that some of the commands with ``/`` are not directly translated
to functions and are instead run as commands.  Also, please note that
the ``*VWRITE`` command requires a command immediately following it.
This normally locks CORBA, so it's implemented in the background as an
input file using ``mapdl.non_interactive``.  See the following Caveats
and Notes section for more details.


VM7 - Plastic Compression of a Pipe Assembly
--------------------------------------------
ANSYS APDL code:

.. code::

    /COM,ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150
    /VERIFY,VM7
    /PREP7
    /TITLE, VM7, PLASTIC COMPRESSION OF A PIPE ASSEMBLY
    C***          MECHANICS OF SOLIDS, CRANDALL AND DAHL, 1959, PAGE 180, EX. 5.1
    C***          USING PIPE288, SOLID185 AND SHELL181 ELEMENTS
    THETA=6                              ! SUBTENDED ANGLE
    ET,1,PIPE288,,,,2
    ET,2,SOLID185
    ET,3,SHELL181,,,2                    ! FULL INTEGRATION
    SECTYPE,1,SHELL
    SECDATA,0.5,1,0,5	                   ! THICKNESS (SHELL181)
    SECTYPE,2,SHELL
    SECDATA,0.5,2,0,5	                   ! THICKNESS (SHELL181)
    SECTYPE,3,PIPE
    SECDATA,4.9563384,0.5                ! OUTSIDE DIA. AND WALL THICKNESS FOR INSIDE TUBE (PIPE288)
    SECTYPE,4,PIPE
    SECDATA,8.139437,0.5                 ! OUTSIDE DIA. AND WALL THICKNESS FOR OUTSIDE TUBE (PIPE288)
    MP,EX  ,1,26.875E6                   ! STEEL
    MP,PRXY,1,0.3
    MP,EX  ,2,11E6                       ! ALUMINUM
    MP,PRXY,2,0.3
    TB,BKIN,1,1                          ! DEFINE NON-LINEAR MATERIAL PROPERTY FOR STEEL
    TBTEMP,0
    TBDATA,1,86000,0
    TB,BKIN,2,1                          ! DEFINE NON-LINEAR MATERIAL PROPERTY FOR ALUMINUM
    TBTEMP,0
    TBDATA,1,55000,0
    N,1                                  ! GENERATE NODES AND ELEMENTS FOR PIPE288
    N,2,,,10
    MAT,1  
    SECNUM,3                             ! STEEL (INSIDE) TUBE
    E,1,2
    MAT,2  
    SECNUM,4                             ! ALUMINUM (OUTSIDE) TUBE
    E,1,2
    CSYS,1
    N,101,1.9781692                      ! GENERATE NODES AND ELEMENTS FOR SOLID185
    N,102,2.4781692
    N,103,3.5697185
    N,104,4.0697185
    N,105,1.9781692,,10
    N,106,2.4781692,,10
    N,107,3.5697185,,10
    N,108,4.0697185,,10
    NGEN,2,10,101,108,,,THETA            ! GENERATE 2ND SET OF NODES TO FORM A THETA DEGREE SLICE
    NROTAT,101,118,1
    TYPE,2
    MAT,1                                ! INSIDE (STEEL) TUBE
    E,101,102,112,111,105,106,116,115
    MAT,2                                ! OUTSIDE (ALUMINUM) TUBE
    E,103,104,114,113,107,108,118,117
    N,201,2.2281692                      ! GENERATE NODES AND ELEMENTS FOR SHELL181
    N,203,2.2281692,,10
    N,202,3.8197185
    N,204,3.8197185,,10
    NGEN,2,4,201,204,,,THETA             ! GENERATE NODES TO FORM A THETA DEGREE SLICE
    TYPE,3
    SECNUM,1                             ! INSIDE (STEEL) TUBE
    E,203,201,205,207
    SECNUM,2                             ! OUTSIDE (ALUMINUM) TUBE
    E,204,202,206,208
    C*** APPLY CONSTRAINTS TO PIPE288 MODEL
    D,1,ALL                              ! FIX ALL DOFS FOR BOTTOM END OF PIPE288
    D,2,UX,,,,,UY,ROTX,ROTY,ROTZ         ! ALLOW ONLY UZ DOF AT TOP END OF PIPE288 MODEL
    C*** APPLY CONSTRAINTS TO SOLID185 AND SHELL181 MODELS
    CP,1,UX,101,111,105,115              ! COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SOLID185
    CPSGEN,4,,1
    CP,5,UX,201,205,203,20               ! COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SHELL181
    CPSGEN,2,,5
    CP,7,ROTY,201,205                    ! COUPLE NODES AT BOUNDARY IN ROTY DIR FOR SHELL181
    CPSGEN,4,,7
    NSEL,S,NODE,,101,212                 ! SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    NSEL,R,LOC,Y,0                       ! SELECT NODES AT THETA = 0 FROM THE SELECTED SET
    DSYM,SYMM,Y,1                        ! APPLY SYMMETRY BOUNDARY CONDITIONS
    NSEL,S,NODE,,101,212                 ! SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    NSEL,R,LOC,Y,THETA                   ! SELECT NODES AT THETA FROM THE SELECTED SET
    DSYM,SYMM,Y,1                        ! APPLY SYMMETRY BOUNDARY CONDITIONS
    NSEL,ALL
    NSEL,R,LOC,Z,0                       ! SELECT ONLY NODES AT Z = 0
    D,ALL,UZ,0                           ! CONSTRAIN BOTTOM NODES IN Z DIRECTION
    NSEL,ALL
    FINISH
    /SOLU    
    OUTPR,BASIC,LAST                     ! PRINT BASIC SOLUTION AT END OF LOAD STEP
    C*** APPLY DISPLACEMENT LOADS TO ALL MODELS
    *CREATE,DISP
    NSEL,R,LOC,Z,10                      ! SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
    D,ALL,UZ,ARG1
    NSEL,ALL
    /OUT,SCRATCH
    SOLVE
    *END
    *USE,DISP,-.032
    *USE,DISP,-.05
    *USE,DISP,-.1
    FINISH
    /OUT,
    /POST1
    C*** CREATE MACRO TO GET RESULTS FOR EACH MODEL
    *CREATE,GETLOAD
    NSEL,S,NODE,,1,2                    ! SELECT NODES IN PIPE288 MODEL
    NSEL,R,LOC,Z,0
    /OUT,SCRATCH
    FSUM                                ! FZ IS TOTAL LOAD FOR PIPE288 MODEL
    *GET,LOAD_288,FSUM,,ITEM,FZ
    NSEL,S,NODE,,101,118                ! SELECT NODES IN SOLID185 MODEL
    NSEL,R,LOC,Z,0
    FSUM
    *GET,ZFRC,FSUM,0,ITEM,FZ
    LOAD=ZFRC*360/THETA                 ! MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
    *STATUS,LOAD
    LOAD_185 = LOAD
    NSEL,S,NODE,,201,212                ! SELECT NODES IN SHELL181 MODEL
    NSEL,R,LOC,Z,0
    FSUM
    /OUT,
    *GET,ZFRC,FSUM,0,ITEM,FZ
    LOAD=ZFRC*360/THETA                 ! MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
    *STATUS,LOAD
    LOAD_181 = LOAD
    *VFILL,VALUE_288(1,1),DATA,1024400,1262000,1262000
    *VFILL,VALUE_288(I,2),DATA,ABS(LOAD_288)
    *VFILL,VALUE_288(I,3),DATA,ABS(LOAD_288)/(VALUE_288(I,1))
    *VFILL,VALUE_185(1,1),DATA,1024400,1262000,1262000
    *VFILL,VALUE_185(J,2),DATA,ABS(LOAD_185)
    *VFILL,VALUE_185(J,3),DATA,ABS(LOAD_185)/(VALUE_185(J,1))
    *VFILL,VALUE_181(1,1),DATA,1024400,1262000,1262000
    *VFILL,VALUE_181(K,2),DATA,ABS(LOAD_181)
    *VFILL,VALUE_181(K,3),DATA,ABS(LOAD_181)/(VALUE_181(K,1))
    *END
    C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.032
    C*** ---------------------------------------
    SET,1,1
    I = 1
    J = 1
    K = 1
    *DIM,LABEL,CHAR,3,2
    *DIM,VALUE_288,,3,3
    *DIM,VALUE_185,,3,3
    *DIM,VALUE_181,,3,3
    *USE,GETLOAD
    C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.05
    C*** --------------------------------------
    SET,2,1
    I = I + 1
    J = J + 1
    K = K + 1
    *USE,GETLOAD
    C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.1
    C*** -------------------------------------
    SET,3,1
    I = I +1
    J = J + 1
    K = K + 1
    *USE,GETLOAD
    LABEL(1,1) = 'LOAD, lb','LOAD, lb','LOAD, lb'
    LABEL(1,2) = ' UX=.032',' UX=0.05',' UX=0.10'
    FINISH
    /OUT,vm7,vrt
    /COM,------------------- VM7 RESULTS COMPARISON ---------------------
    /COM,
    /COM,                 |   TARGET   |   Mechanical APDL   |   RATIO
    /COM,
    /COM,RESULTS FOR PIPE288:
    /COM,
    *VWRITE,LABEL(1,1),LABEL(1,2),VALUE_288(1,1),VALUE_288(1,2),VALUE_288(1,3)
    (1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)
    /COM,
    /COM,RESULTS FOR SOLID185:
    /COM,
    *VWRITE,LABEL(1,1),LABEL(1,2),VALUE_185(1,1),VALUE_185(1,2),VALUE_185(1,3)
    (1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)
    /COM,
    /COM,RESULTS FOR SHELL181:
    /COM,
    *VWRITE,LABEL(1,1),LABEL(1,2),VALUE_181(1,1),VALUE_181(1,2),VALUE_181(1,3)
    (1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)
    /COM,
    /COM,-----------------------------------------------------------------
    /OUT
    *LIST,vm7,vrt

Convert the verfication file with:

.. code:: python

    import pyansys
    pyansys.convert_script('vm7.dat', 'vm7.py')

Here is the translated Python script:

.. code:: python

    """ Script generated by pyansys version 0.42.0"""
    import pyansys
    mapdl = pyansys.launch_mapdl("/usr/ansys_inc/v182/ansys/bin/ansys182",
                                 loglevel="ERROR")
    mapdl.run("/COM,ANSYS MEDIA REL. 150 (11/8/2013) REF. VERIF. MANUAL: REL. 150")
    mapdl.run("/VERIFY,VM7")
    mapdl.run("/PREP7")
    mapdl.run("/TITLE, VM7, PLASTIC COMPRESSION OF A PIPE ASSEMBLY")
    mapdl.run("C***          MECHANICS OF SOLIDS, CRANDALL AND DAHL, 1959, PAGE 180, EX. 5.1")
    mapdl.run("C***          USING PIPE288, SOLID185 AND SHELL181 ELEMENTS")
    mapdl.run("THETA=6                              ")  # SUBTENDED ANGLE
    mapdl.et(1, "PIPE288", "", "", "", 2)
    mapdl.et(2, "SOLID185")
    mapdl.et(3, "SHELL181", "", "", 2)  #FULL INTEGRATION
    mapdl.sectype(1, "SHELL")
    mapdl.secdata(0.5, 1, 0, 5)  #THICKNESS (SHELL181)
    mapdl.sectype(2, "SHELL")
    mapdl.secdata(0.5, 2, 0, 5)  #THICKNESS (SHELL181)
    mapdl.sectype(3, "PIPE")
    mapdl.secdata(4.9563384, 0.5)  #OUTSIDE DIA. AND WALL THICKNESS FOR INSIDE TUBE (PIPE288)
    mapdl.sectype(4, "PIPE")
    mapdl.secdata(8.139437, 0.5)  #OUTSIDE DIA. AND WALL THICKNESS FOR OUTSIDE TUBE (PIPE288)
    mapdl.mp("EX", 1, 26.875E6)  #STEEL
    mapdl.mp("PRXY", 1, 0.3)
    mapdl.mp("EX", 2, 11E6)  #ALUMINUM
    mapdl.mp("PRXY", 2, 0.3)
    mapdl.tb("BKIN", 1, 1)  #DEFINE NON-LINEAR MATERIAL PROPERTY FOR STEEL
    mapdl.tbtemp(0)
    mapdl.tbdata(1, 86000, 0)
    mapdl.tb("BKIN", 2, 1)  #DEFINE NON-LINEAR MATERIAL PROPERTY FOR ALUMINUM
    mapdl.tbtemp(0)
    mapdl.tbdata(1, 55000, 0)
    mapdl.n(1)  #GENERATE NODES AND ELEMENTS FOR PIPE288
    mapdl.n(2, "", "", 10)
    mapdl.mat(1)
    mapdl.secnum(3)  #STEEL (INSIDE) TUBE
    mapdl.e(1, 2)
    mapdl.mat(2)
    mapdl.secnum(4)  #ALUMINUM (OUTSIDE) TUBE
    mapdl.e(1, 2)
    mapdl.csys(1)
    mapdl.n(101, 1.9781692)  #GENERATE NODES AND ELEMENTS FOR SOLID185
    mapdl.n(102, 2.4781692)
    mapdl.n(103, 3.5697185)
    mapdl.n(104, 4.0697185)
    mapdl.n(105, 1.9781692, "", 10)
    mapdl.n(106, 2.4781692, "", 10)
    mapdl.n(107, 3.5697185, "", 10)
    mapdl.n(108, 4.0697185, "", 10)
    mapdl.ngen(2, 10, 101, 108, "", "", "THETA")  #GENERATE 2ND SET OF NODES TO FORM A THETA DEGREE SLICE
    mapdl.nrotat(101, 118, 1)
    mapdl.type(2)
    mapdl.mat(1)  #INSIDE (STEEL) TUBE
    mapdl.e(101, 102, 112, 111, 105, 106, 116, 115)
    mapdl.mat(2)  #OUTSIDE (ALUMINUM) TUBE
    mapdl.e(103, 104, 114, 113, 107, 108, 118, 117)
    mapdl.n(201, 2.2281692)  #GENERATE NODES AND ELEMENTS FOR SHELL181
    mapdl.n(203, 2.2281692, "", 10)
    mapdl.n(202, 3.8197185)
    mapdl.n(204, 3.8197185, "", 10)
    mapdl.ngen(2, 4, 201, 204, "", "", "THETA")  #GENERATE NODES TO FORM A THETA DEGREE SLICE
    mapdl.type(3)
    mapdl.secnum(1)  #INSIDE (STEEL) TUBE
    mapdl.e(203, 201, 205, 207)
    mapdl.secnum(2)  #OUTSIDE (ALUMINUM) TUBE
    mapdl.e(204, 202, 206, 208)
    mapdl.run("C*** APPLY CONSTRAINTS TO PIPE288 MODEL")
    mapdl.d(1, "ALL")  #FIX ALL DOFS FOR BOTTOM END OF PIPE288
    mapdl.d(2, "UX", "", "", "", "", "UY", "ROTX", "ROTY", "ROTZ")  #ALLOW ONLY UZ DOF AT TOP END OF PIPE288 MODEL
    mapdl.run("C*** APPLY CONSTRAINTS TO SOLID185 AND SHELL181 MODELS")
    mapdl.cp(1, "UX", 101, 111, 105, 115)  #COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SOLID185
    mapdl.cpsgen(4, "", 1)
    mapdl.cp(5, "UX", 201, 205, 203, 20)  #COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SHELL181
    mapdl.cpsgen(2, "", 5)
    mapdl.cp(7, "ROTY", 201, 205)  #COUPLE NODES AT BOUNDARY IN ROTY DIR FOR SHELL181
    mapdl.cpsgen(4, "", 7)
    mapdl.nsel("S", "NODE", "", 101, 212)  #SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    mapdl.nsel("R", "LOC", "Y", 0)  #SELECT NODES AT THETA = 0 FROM THE SELECTED SET
    mapdl.dsym("SYMM", "Y", 1)  #APPLY SYMMETRY BOUNDARY CONDITIONS
    mapdl.nsel("S", "NODE", "", 101, 212)  #SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
    mapdl.nsel("R", "LOC", "Y", "THETA")  #SELECT NODES AT THETA FROM THE SELECTED SET
    mapdl.dsym("SYMM", "Y", 1)  #APPLY SYMMETRY BOUNDARY CONDITIONS
    mapdl.nsel("ALL")
    mapdl.nsel("R", "LOC", "Z", 0)  #SELECT ONLY NODES AT Z = 0
    mapdl.d("ALL", "UZ", 0)  #CONSTRAIN BOTTOM NODES IN Z DIRECTION
    mapdl.nsel("ALL")
    mapdl.finish()
    mapdl.run("/SOLU")
    mapdl.outpr("BASIC", "LAST")  #PRINT BASIC SOLUTION AT END OF LOAD STEP
    mapdl.run("C*** APPLY DISPLACEMENT LOADS TO ALL MODELS")


    def DISP(ARG1='', ARG2='', ARG3='', ARG4='', ARG5='', ARG6='',
             ARG7='', ARG8='', ARG9='', ARG10='', ARG11='', ARG12='',
             ARG13='', ARG14='', ARG15='', ARG16='', ARG17='', ARG18=''):
        mapdl.nsel("R", "LOC", "Z", 10)  #SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
        mapdl.d("ALL", "UZ", ARG1)
        mapdl.nsel("ALL")
        mapdl.run("/OUT,SCRATCH")
        mapdl.solve()


    DISP(-.032)
    DISP(-.05)
    DISP(-.1)
    mapdl.finish()
    mapdl.run("/OUT,")
    mapdl.run("/POST1")
    mapdl.run("C*** CREATE MACRO TO GET RESULTS FOR EACH MODEL")


    def GETLOAD(ARG1='', ARG2='', ARG3='', ARG4='', ARG5='', ARG6='',
                ARG7='', ARG8='', ARG9='', ARG10='', ARG11='', ARG12='',
                ARG13='', ARG14='', ARG15='', ARG16='', ARG17='', ARG18=''):
        mapdl.nsel("S", "NODE", "", 1, 2)  #SELECT NODES IN PIPE288 MODEL
        mapdl.nsel("R", "LOC", "Z", 0)
        mapdl.run("/OUT,SCRATCH")
        mapdl.fsum()  #FZ IS TOTAL LOAD FOR PIPE288 MODEL
        mapdl.run("*GET,LOAD_288,FSUM,,ITEM,FZ")
        mapdl.nsel("S", "NODE", "", 101, 118)  #SELECT NODES IN SOLID185 MODEL
        mapdl.nsel("R", "LOC", "Z", 0)
        mapdl.fsum()
        mapdl.run("*GET,ZFRC,FSUM,0,ITEM,FZ")
        mapdl.run("LOAD=ZFRC*360/THETA                 ")  # MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
        mapdl.run("*STATUS,LOAD")
        mapdl.run("LOAD_185 = LOAD")
        mapdl.nsel("S", "NODE", "", 201, 212)  #SELECT NODES IN SHELL181 MODEL
        mapdl.nsel("R", "LOC", "Z", 0)
        mapdl.fsum()
        mapdl.run("/OUT,")
        mapdl.run("*GET,ZFRC,FSUM,0,ITEM,FZ")
        mapdl.run("LOAD=ZFRC*360/THETA                 ")  # MULTIPLY BY 360/THETA FOR FULL 360 DEGREE RESULTS
        mapdl.run("*STATUS,LOAD")
        mapdl.run("LOAD_181 = LOAD")
        mapdl.run("*VFILL,VALUE_288(1,1),DATA,1024400,1262000,1262000")
        mapdl.run("*VFILL,VALUE_288(I,2),DATA,ABS(LOAD_288)")
        mapdl.run("*VFILL,VALUE_288(I,3),DATA,ABS(LOAD_288)/(VALUE_288(I,1))")
        mapdl.run("*VFILL,VALUE_185(1,1),DATA,1024400,1262000,1262000")
        mapdl.run("*VFILL,VALUE_185(J,2),DATA,ABS(LOAD_185)")
        mapdl.run("*VFILL,VALUE_185(J,3),DATA,ABS(LOAD_185)/(VALUE_185(J,1))")
        mapdl.run("*VFILL,VALUE_181(1,1),DATA,1024400,1262000,1262000")
        mapdl.run("*VFILL,VALUE_181(K,2),DATA,ABS(LOAD_181)")
        mapdl.run("*VFILL,VALUE_181(K,3),DATA,ABS(LOAD_181)/(VALUE_181(K,1))")


    mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.032")
    mapdl.run("C*** ---------------------------------------")
    mapdl.set(1, 1)
    mapdl.run("I = 1")
    mapdl.run("J = 1")
    mapdl.run("K = 1")
    mapdl.run("*DIM,LABEL,CHAR,3,2")
    mapdl.run("*DIM,VALUE_288,,3,3")
    mapdl.run("*DIM,VALUE_185,,3,3")
    mapdl.run("*DIM,VALUE_181,,3,3")
    GETLOAD()
    mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.05")
    mapdl.run("C*** --------------------------------------")
    mapdl.set(2, 1)
    mapdl.run("I = I + 1")
    mapdl.run("J = J + 1")
    mapdl.run("K = K + 1")
    GETLOAD()
    mapdl.run("C*** GET TOTAL LOAD FOR DISPLACEMENT = 0.1")
    mapdl.run("C*** -------------------------------------")
    mapdl.set(3, 1)
    mapdl.run("I = I +1")
    mapdl.run("J = J + 1")
    mapdl.run("K = K + 1")
    GETLOAD()
    mapdl.run("LABEL(1,1) = 'LOAD, lb','LOAD, lb','LOAD, lb'")
    mapdl.run("LABEL(1,2) = ' UX=.032',' UX=0.05',' UX=0.10'")
    mapdl.finish()
    mapdl.run("/OUT,vm7,vrt")
    mapdl.run("/COM,------------------- VM7 RESULTS COMPARISON ---------------------")
    mapdl.run("/COM,")
    mapdl.run("/COM,                 |   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.run("/COM,")
    mapdl.run("/COM,RESULTS FOR PIPE288:")
    mapdl.run("/COM,")
    with mapdl.non_interactive:
        mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_288(1,1),VALUE_288(1,2),VALUE_288(1,3)")
        mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
        mapdl.run("/COM,")
        mapdl.run("/COM,RESULTS FOR SOLID185:")
        mapdl.run("/COM,")
        mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_185(1,1),VALUE_185(1,2),VALUE_185(1,3)")
        mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
        mapdl.run("/COM,")
        mapdl.run("/COM,RESULTS FOR SHELL181:")
        mapdl.run("/COM,")
        mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE_181(1,1),VALUE_181(1,2),VALUE_181(1,3)")
        mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F14.0,'   ',1F15.3)")
        mapdl.run("/COM,")
        mapdl.run("/COM,-----------------------------------------------------------------")
        mapdl.run("/OUT")
        mapdl.run("*LIST,vm7,vrt")
    mapdl.exit()
