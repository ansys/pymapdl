ANSYS APDL Interactive Control
==============================
ANSYS APDL allows for the direct scripting of ANSYS through ANSYS
input files.  Unfortunately, APDL relies on an outdated scripting
language that is difficult to read and control.  The weaknesses of
this language are often compensated by generating APDL scripts using a
secondary scripting tool like ``MATLAB`` or ``Python``.  However, this
added layer of complexity means that the development feedback loop is
quite long as the user must export and run an entire script before
determining if it ran correctly or of the results are valid.  This
module seeks to rectify that.

The interface control module requires ANSYS to be installed on the
system running ``pyansys`` for it to operate.


Initial Setup and Example
-------------------------
The ``ANSYS`` control module within ``pyansys`` creates an instance of
an interactive Shell of ``ANSYS`` in the background and sends commands
to that shell.  Errors and warnings are processed Pythonically letting
the user develop a script real-time without worrying about if it will
function correctly when deployed in batch mode.

To run, ``pyansys`` needs to know the location of the ANSYS binary.
When running for the first time, ``pyansys`` will request the location
of the ANSYS executable.  You can test your installation ``pyansys``
and set it up by running the following in python:

.. code:: python

    from pyansys import examples
    examples.ansys_cylinder_demo()

Python will automatically attempt to detect your ANSYS binary based on
environmental variables.  If it is unable to find a copy of ANSYS, you
will be prompted for the location of the ANSYS executable.  Here is a
sample input for Linux and Windows:

.. code::

    Enter location of ANSYS executable: /usr/ansys_inc/v182/ansys/bin/ansys182

.. code::

    Enter location of ANSYS executable: C:\Program Files\ANSYS Inc\v170\ANSYS\bin\winx64\ansys170.exe

The settings file is stored locally and do not need to enter it again.
If you need to change the default ansys path, run the following:

.. code:: python

    import pyansys
    new_path = 'C:\\Program Files\\ANSYS Inc\\v170\\ANSYS\\bin\\winx64\\ansys170.exe'
    pyansys.change_default_ansys_path(new_path)


Running MAPDL from ``pyansys``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ANSYS can be started from python using :func:`pyansys.launch_mapdl` .
this starts in a temporary directory by default.  You can change this
to your current directory with:

.. code:: python

    import os
    import pyansys

    path = os.getcwd()
    mapdl = pyansys.launch_mapdl(run_location=path)

ANSYS is now active and you can send commands to it as if it was just
a Python object.


Using ANSYS from ``pyansys``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For example, if we wanted to create a surface using keypoints we could run:

.. code:: python

    mapdl.run('/PREP7')
    mapdl.run('K, 1, 0, 0, 0')
    mapdl.run('K, 2, 1, 0, 0')
    mapdl.run('K, 3, 1, 1, 0')
    mapdl.run('K, 4, 0, 1, 0')
    mapdl.run('L, 1, 2')
    mapdl.run('L, 2, 3')
    mapdl.run('L, 3, 4')
    mapdl.run('L, 4, 1')
    mapdl.run('AL, 1, 2, 3, 4')

ANSYS interactively returns the result of each command and it is
stored to the logging module.  Errors are caught immediately.  For
example:

.. code:: python

    >>> mapdl.run('AL, 1, 2, 3')

   Exception: 
   AL, 1, 2, 3

   DEFINE AREA BY LIST OF LINES
   LINE LIST =     1    2    3
   (TRAVERSED IN SAME DIRECTION AS LINE     1)

   *** ERROR ***                           CP =       0.338   TIME= 09:45:36
   Keypoint 1 is referenced by only one line.  Improperly connected line   
   set for AL command.                                                     

This ``Exception`` was be caught immediately.  This means that you can
write your MAPDL scripts in python, run them interactively and then as
a batch without worrying if the script will run correctly if you had
instead outputted it to a script file.


Calling MAPDL Pythonically
~~~~~~~~~~~~~~~~~~~~~~~~~~
One advantage of writing scripts using ``pyansys`` is the ability to
call MAPDL commands as python functions from the ``Mapdl`` class.  For
example, instead of sending commands to MAPDL as in the area creation
example, we can instead run:

.. code:: python

    # clear existing geometry
    mapdl.finish()
    mapdl.clear()

    # create a square area using keypoints
    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)    
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 4)
    mapdl.l(4, 1)
    mapdl.al(1, 2, 3, 4)

This approach has some obvious advantages, chiefly that it's a bit
easier to script as ``pyansys`` takes care of the string formatting
for you.  For example, inputting points from a numpy array:

.. code:: python

   import numpy as np

   # make 10 random keypoints in MAPDL
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       mapdl.k(i + 1, x, y, z)

Additionally, each function with the MAPDL class has help associated
within it.  For example:

.. code:: python

    >>> help(mapdl.k)

    Help on method K in module pyansys.MapdlCorba:

    k(npt='', x='', y='', z='') method of pyansys.mapdl_corba.MapdlCorba instance
        APDL Command: K
        
        Defines a keypoint.
        
        Parameters
        ----------
        npt
            Reference number for keypoint.  If zero, the lowest available
            number is assigned [NUMSTR].
        
        x, y, z
            Keypoint location in the active coordinate system (may be R, θ, Z
            or R, θ, Φ).  If X = P, graphical picking is enabled and all other
            fields (including NPT) are ignored (valid only in the GUI).
        
        Notes
        -----
        Defines a keypoint in the active coordinate system [CSYS] for line,
        area, and volume descriptions.  A previously defined keypoint of the
        same number will be redefined.  Keypoints may be redefined only if it
        is not yet attached to a line or is not yet meshed.  Solid modeling in
        a toroidal system is not recommended.


Translating Scripts
-------------------
Existing ANSYS scripts can be translated using:

.. code:: python

    import pyansys

    inputfile = 'ansys_inputfile.inp'
    pyscript = 'pyscript.py'
    pyansys.convert_script(inputfile, pyscript)

For example, verification file vm1.dat:

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
    
    Translates to:
    
.. code:: python

    """ Script generated by pyansys version 0.30.1"""
    import pyansys
    mapdl = pyansys.launch_mapdl()
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

Some of the commands with ``/`` are not directly translated to
functions and are instead run as commands.  Also, please note that the
``*VWRITE`` command requires a command immediately following it.  This
normally locks CORBA, so it's implemented in the background as an
input file using ``mapdl.non_interactive``.  See the following Caveats
and Notes section for more details.

Additional examples with more conversion options can be found in the
APDL conversion page.


Caveats and Notes
-----------------

Command Naming Conventions and Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When calling MAPDL commands as functions, each command has been
translated from its original MAPDL all CAPS format to a PEP8
compatible format.  For example, ``ESEL`` is now ``esel``.
Additionally, MAPDL commands containing a ``/`` or ``*`` have had
those characters removed, unless this causes a conflict with an
existing name.  Most notable is ``/SOLU`` which would conflict with
``SOLU``.  Therefore, the ``/SOLU`` has been renamed to ``slashsolu``
to differentiate it from ``solu``.  Out of the 1500 MAPDL commands,
about 15 start with ``slash`` and 8 with ``star``.  Check the ``MAPDL
Object Methods`` reference below when necessary.

MAPDL commands that normally have an empty space, such as ``ESEL, S,
TYPE, , 1`` should include an empty string when called by Python:

.. code:: python

    mapdl.esel('s', 'type', '', 1)

or these commands can be called using parameters:

.. code:: python

    mapdl.esel('s', 'type', vmin=1)

None of these restrictions apply to commands run with ``run``:

.. code:: python

    mapdl.run('/SOLU')
    mapdl.solve()

Some commands can only be run non-interactively in a script.
``pyansys`` gets around this restriction by writing the commands to a
temporary input file and then reading the input file.  To run a group
of commands that must be run non-interactively, set the ``MAPDL``
object to run a series of commands as an input file by using
``non_interactive`` as in this example:

.. code:: python

    with mapdl.non_interactive:
        mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")

Also note that macros created within pyansys (rather than loaded from
a file) do not appear to run correctly.  For example, the macro
``DISP`` created using the ``*CREATE`` command within APDL:

.. code::

    *CREATE,DISP
    NSEL,R,LOC,Z,10                      ! SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
    D,ALL,UZ,ARG1
    NSEL,ALL
    /OUT,SCRATCH
    SOLVE
    *END

    ! Call the function
    *USE,DISP,-.032
    *USE,DISP,-.05
    *USE,DISP,-.1

Should be written as:

.. code:: python

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

If you have an existing input file with a macro, it can be converted
using the ``convert_script`` function:

.. code:: python

    pyansys.convert_script(apdl_inputfile, pyscript, macros_as_functions=True)

See the ``vm7.dat`` example in the APDL Conversion Examples page.



Conditional Statements and Loops
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
APDL conditional statements such as ``*IF`` must be either implemented
pythonically or using ``with mapdl.non_interactive:``.  See the
``vm8.dat`` example in the APDL Conversion Examples page.  For
example:

.. code:: 

    *IF,ARG1,EQ,0,THEN
      *GET,ARG4,NX,ARG2     ! RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
      *GET,ARG5,NY,ARG2
      *GET,ARG6,NZ,ARG2
      *GET,ARG7,NX,ARG3
      *GET,ARG8,NY,ARG3
      *GET,ARG9,NZ,ARG3
    *ELSE
      *GET,ARG4,KX,ARG2     ! RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
      *GET,ARG5,KY,ARG2
      *GET,ARG6,KZ,ARG2
      *GET,ARG7,KX,ARG3
      *GET,ARG8,KY,ARG3
      *GET,ARG9,KZ,ARG3
    *ENDIF

Should be implemented as:

.. code:: python

    with mapdl.non_interactive:
        mapdl.run("*IF,ARG1,EQ,0,THEN")
        mapdl.run("*GET,ARG4,NX,ARG2     ")  # RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
        mapdl.run("*GET,ARG5,NY,ARG2")
        mapdl.run("*GET,ARG6,NZ,ARG2")
        mapdl.run("*GET,ARG7,NX,ARG3")
        mapdl.run("*GET,ARG8,NY,ARG3")
        mapdl.run("*GET,ARG9,NZ,ARG3")
        mapdl.run("*ELSE")
        mapdl.run("*GET,ARG4,KX,ARG2     ")  # RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
        mapdl.run("*GET,ARG5,KY,ARG2")
        mapdl.run("*GET,ARG6,KZ,ARG2")
        mapdl.run("*GET,ARG7,KX,ARG3")
        mapdl.run("*GET,ARG8,KY,ARG3")
        mapdl.run("*GET,ARG9,KZ,ARG3")
        mapdl.run("*ENDIF")

Or pythonically as:

.. code:: python

    # MAPDL parameters can be obtained using load_parameters
    if ARG1 == 0:
        mapdl.run("*GET,ARG4,NX,ARG2     ")  # RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
        mapdl.run("*GET,ARG5,NY,ARG2")
        mapdl.run("*GET,ARG6,NZ,ARG2")
        mapdl.run("*GET,ARG7,NX,ARG3")
        mapdl.run("*GET,ARG8,NY,ARG3")
        mapdl.run("*GET,ARG9,NZ,ARG3")
    else:
        mapdl.run("*GET,ARG4,KX,ARG2     ")  # RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
        mapdl.run("*GET,ARG5,KY,ARG2")
        mapdl.run("*GET,ARG6,KZ,ARG2")
        mapdl.run("*GET,ARG7,KX,ARG3")
        mapdl.run("*GET,ARG8,KY,ARG3")
        mapdl.run("*GET,ARG9,KZ,ARG3")

APDL loops using ``*DO`` or ``*DOWHILE`` should also be implemetned using ``mapdl.non_interactive`` or pythonically.


Warnings and Errors
~~~~~~~~~~~~~~~~~~~
Errors are handled pythonically.  For example:

.. code:: python

    try:
        mapdl.solve()
    except:
        # do something else with MAPDL

Commands that are ignored within MAPDL are flagged as errors.  This is different than MAPDL's default behavior where commands that are ignored are treated as warnings.  For example, in ``pyansys`` running a command in the wrong session raises an error:

.. code:: python

    >>> mapdl.finish()
    >>> mapdl.k()

    Exception: 
    K, , , , 

     *** WARNING ***                         CP =       0.307   TIME= 11:05:01
     K is not a recognized BEGIN command, abbreviation, or macro.  This      
     command will be ignored.

You can change this behavior so ignored commands can be logged as warnings not raised as an exception by setting:

.. code:: python

   mapdl.allow_ignore = True
   mapdl.k()  # error ignored


Prompts
~~~~~~~
Prompts from MAPDL automatically continued as if MAPDL is in batch mode.  Commands requiring user input, such as ``*VWRITE`` will fail and must be entered in non-interactively.


APDL Command Logging
--------------------
While ``pyansys`` is designed to make it easier to control an APDL session by calling it using Python, it may be necessary to call MAPDL again using an input file generated from a pyansys script.  This is automatically enabled with the ``log_apdl='apdl.log'`` parameter.  Enabling this parameter will cause ``pyansys`` to write each command run from a ``Mapdl`` object into a log file named ``"apdl.log"`` in the MAPDL working directory of the active ``mapdl`` object.  For example

.. code:: python

    import pyansys

    ansys = pyansys.launch_mapdl(log_apdl='apdl.log')
    ansys.prep7()
    ansys.k(1, 0, 0, 0)
    ansys.k(2, 1, 0, 0)
    ansys.k(3, 1, 1, 0)
    ansys.k(4, 0, 1, 0)    

Will write the following to ``"apdl.log"``

.. code::

    ! APDL script generated using pyansys 0.40.1
    /PREP7,
    K,1,0,0,0
    K,2,1,0,0
    K,3,1,1,0
    K,4,0,1,0

This allows for the translation of a Python script to an APDL script
except for conditional statements, loops, or functions.


Plotting Non-Interactively
--------------------------
It is often useful to plot geometry and meshes as they are generated
and for debugging (or scripting) purposes it can be useful to plot
within ``pyansys`` as well.  To enable interactive plotting, set
``interactive_plotting=True`` when starting ANSYS.  Plotting commands
such as ``APLOT``, ``EPLOT``, and ``KPLOT`` will open up a
``matploblib``.

.. code:: python

    import pyansys

    # run ansys with interactive plotting enabled
    mapdl = pyansys.launch_mapdl(interactive_plotting=True)

    # create a square area using keypoints
    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)    
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 4)
    mapdl.l(4, 1)
    mapdl.al(1, 2, 3, 4)

    # sets the view to "isometric"
    mapdl.view(1, 1, 1, 1)
    mapdl.pnum('kp', 1)  # enable keypoint numbering
    mapdl.pnum('line', 1)  # enable line numbering

    # each of these will create a matplotlib figure and pause execution
    mapdl.aplot()
    mapdl.lplot()
    mapdl.kplot()

.. figure:: ./images/aplot.png
    :width: 300pt

    Area Plot from ANSYS using ``pyansys``


Interactive Breakpoint
----------------------
In most circumstances it is not possible, especially when generating
geometry, to go without opening up the APDL GUI.  Identifying geometry
items can't be done easy using inline plotting, so ``pyansys`` has an
``open_gui`` method that allows you to seamlessly open up the GUI
without loosing work or having to restart your session.  For example:

.. code:: python

    import pyansys

    # run ansys with interactive plotting enabled
    mapdl = pyansys.launch_mapdl()

    # create a square area using keypoints
    mapdl.prep7()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)
    mapdl.k(4, 0, 1, 0)    
    mapdl.l(1, 2)
    mapdl.l(2, 3)
    mapdl.l(3, 4)
    mapdl.l(4, 1)
    mapdl.al(1, 2, 3, 4)

    # open up the gui
    mapdl.open_gui()

    # it resumes where you left off...
    mapdl.et(1, 'MESH200', 6)
    mapdl.amesh('all')
    mapdl.eplot()    

This approach avoids the hassle of having to switch back and forth
between an interactive session and a scripting session.  Instead, you
can have one scripting session and open up a GUI from the scripting
session without losing work or progress.  Additionally, none of the
changes made in the GUI will affect the script.  You can experiment in
the GUI and the script will be left unaffected.


Running a Batch
---------------
Instead of running an ANSYS batch by calling ANSYS with an input file,
you can instead define a function that runs MAPDL.  This example runs
a mesh convergence study based on the maximum stress of a cylinder
with torsional loading.

.. code:: python

    import numpy as np
    import pyansys

    def cylinder_batch(elemsize, plot=False):
        """ Report the maximum von Mises stress of a Cantilever supported cylinder"""

        # clear
        mapdl.finish()
        mapdl.clear()

        # cylinder parameters
        radius = 2
        h_tip = 2
        height = 20
        force = 100/radius
        pressure = force/(h_tip*2*np.pi*radius)

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

        # mesh cylinder
        mapdl.lsel('s', 'loc', 'x', 0)
        mapdl.lsel('r', 'loc', 'y', 0)
        mapdl.lsel('r', 'loc', 'z', 0, height - h_tip)
        # mapdl.lesize('all', elemsize*2)
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

        if plot:
            mapdl.view(1, 1, 1, 1)
            mapdl.eplot()

        # new solution
        mapdl.slashsolu()
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
        mapdl.finish()

        # access results using ANSYS object
        result = mapdl.result

        # to access the results you could have run:
        # resultfile = os.path.join(mapdl.path, '%s.rst' % mapdl.jobname)
        # result = pyansys.read_binary(result file)

        # Get maximum von Mises stress at result 1
        nodenum, stress = result.principal_nodal_stress(0)  # 0 as it's zero based indexing

        # von Mises stress is the last column
        # must be nanmax as the shell element stress is not recorded
        maxstress = np.nanmax(stress[:, -1])

        # return number of nodes and max stress
        return nodenum.size, maxstress


    # initialize ANSYS
    mapdl = pyansys.launch_mapdl(override=True, loglevel='ERROR')

    result_summ = []
    for elemsize in np.linspace(0.6, 0.15, 15):
        # run the batch and report the results
        nnode, maxstress = cylinder_batch(elemsize, plot=False)
        result_summ.append([nnode, maxstress])
        print('Element size %f: %6d nodes and maximum vom Mises stress %f'
              % (elemsize, nnode, maxstress))

    # Exit ANSYS
    mapdl.exit()

This is the result from the script:

.. code::

    Element size 0.600000:   9657 nodes and maximum vom Mises stress 142.623505
    Element size 0.567857:  10213 nodes and maximum vom Mises stress 142.697800
    Element size 0.535714:  10769 nodes and maximum vom Mises stress 142.766510
    Element size 0.503571:  14177 nodes and maximum vom Mises stress 142.585388
    Element size 0.471429:  18371 nodes and maximum vom Mises stress 142.825684
    Element size 0.439286:  19724 nodes and maximum vom Mises stress 142.841202
    Element size 0.407143:  21412 nodes and maximum vom Mises stress 142.945984
    Element size 0.375000:  33502 nodes and maximum vom Mises stress 142.913437
    Element size 0.342857:  37877 nodes and maximum vom Mises stress 143.033401
    Element size 0.310714:  59432 nodes and maximum vom Mises stress 143.328842
    Element size 0.278571:  69106 nodes and maximum vom Mises stress 143.176086
    Element size 0.246429: 110547 nodes and maximum vom Mises stress 143.499329
    Element size 0.214286: 142496 nodes and maximum vom Mises stress 143.559128
    Element size 0.182143: 211966 nodes and maximum vom Mises stress 143.953430
    Element size 0.150000: 412324 nodes and maximum vom Mises stress 144.275406


Chaining Commands in MAPDL
--------------------------
MAPDL permits several commands on one line by using the separation
character ``"$"``.  This can be utilized within ``pyansys`` to
effectively chain several commands together rather and send them to
MAPDL for execution rather than executing them individually.  This can
be helpful when you need to execute thousands of commands in a python
loop and don't need the individual results for each command.  For
example, if you wish to create a 1000 keypoints along the X axis you
would run:

.. code:: python

    xloc = np.linspace(0, 1, 1000)
    for x in xloc:
        mapdl.k(x=x)


However, since each command executes individually and returns a
response, it is much faster to send the commands to be executed by
MAPDL in groups and have ``pyansys`` handle grouping the commands by
running ``with mmapdl.chain_commands``:

.. code:: python

    xloc = np.linspace(0, 1, 1000)
    with mapdl.chain_commands:
        for x in xloc:
            mapdl.k(x=x)

The execution time on this generally 4 to 10 times faster than running each command
individually.


Sending Arrays to MAPDL
-----------------------
You can send ``numpy`` arrays or Python lists directly to MAPDL using
``load_array``.  This is far more efficient than individually sending
parameters to MAPDL through python or MAPDL.  It uses ``*VREAD``
behind the scenes and will be replaced with a faster interface in the
future.

.. code:: python

    import pyansys
    import numpy as np
    mapdl = pyansys.launch_mapdl()
    arr = np.random.random((5, 3))
    mapdl.load_array(arr, 'MYARR')

Verify the data has been propertly loaded to MAPDL by accessing the
first element.  Note that MAPDL uses fortran (1) based indexing.

.. code:: python

   >>> mapdl.read_float_parameter('MYARR(1, 1)')
   2020-07-03 21:49:54,387 [INFO] pyansys.mapdl: MYARR(1, 1) = MYARR(1, 1)

   PARAMETER MYARR(1,1) =    0.7960742456

   >>> arr[0]
   0.7960742456194109


MAPDL Object Methods
--------------------
.. autoclass:: pyansys.mapdl._MapdlCore
    :members:
