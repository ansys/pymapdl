ANSYS Examples
==============
These examples are used to demonstrate ANSYS examples and reading them in using ``pyansys``.


Torsional Load on a Bar using SURF154 Elements
----------------------------------------------
This ANSYS APDL script builds a bar and applies torque to it using SURF154 elements.  This is a static analysis example.

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

Read and plot the results within python using:
.. code:: python

    import pyansys
    result = pyansys.ResultReader('file.rst')

    # node numbers and nodal stress
    nodennum, stress = result.NodalStress(0)

    # stress at each element
    element_stress, elemnum, enode = result.ElementStress(0)

    # plot result
    result.PlotNodalResult(0)



Spotweld SHELL181 Example
-------------------------
This ANSYS APDL example demonstrates how to model spot welding on three thin sheets of metal.

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

Here's the Python script using ``pyansys`` to access the results after running the ANSYS analysis.

.. code:: python
    
    import pyansys
    
    # Open the result file and plot the displacement of time step 3
    resultfile = os.path.join('file.rst')
    result = pyansys.ResultReader(resultfile)
    result.PlotNodalResult(2)

.. figure:: ./images/spot_disp.png
    :width: 300pt

    Spot Weld: Displacement

Get the nodal and element component stress at time step 0.  Plot the stress in the Z direction.

.. code:: python

    nodenum, stress = result.NodalStress(0)
    element_stress, elemnum, enode = result.ElementStress(0)
    
    # plot the Z direction stress (the stress at the contact element simulating
    # the spot weld)
    result.PlotNodalStress(0, 'Sz')

.. figure:: ./images/spot_sz.png
    :width: 300pt

    Spot Weld: Z Stress

.. code:: python

    # Get the principal nodal stress and plot the von Mises Stress
    nnum, pstress = result.PrincipalNodalStress(0)
    result.PlotPrincipalNodalStress(0, 'SEQV')

.. figure:: ./images/spot_seqv.png
    :width: 300pt

    Spot Weld: von Mises Stress
