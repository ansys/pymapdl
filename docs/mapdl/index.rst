ANSYS MAPDL Interactive Control
===============================
ANSYS MAPDL allows for the direct scripting of structural analysis
problems through input files.  Unfortunately, MAPDL relies on an
outdated scripting language that can be difficult to read and control
and either requires the MAPDL GUI for an interactive session or a
basic text interface through a batch session.

The weaknesses of this language are often compensated by generating
APDL scripts using a secondary scripting tool like ``MATLAB`` or
``Python``.  However, this added layer of complexity means that the
development feedback loop is quite long as the user must export and
run an entire script before determining if it ran correctly or of the
results are valid.  This module seeks to rectify that with:

- Low and high level scripting of MAPDL through both basic text
  commands and python commands.
- Plotting of MAPDL geometry and meshes using VTK from within a Python
  environment
- Access MAPDL arrays as Python objects (e.g. nodes, elements,
  internal arrays, results from MAPDL post-processing)


.. toctree::
   :maxdepth: 1
   :caption: Basic Features

   functions
   mesh_geometry
   plotting
   parameters

.. toctree::
   :maxdepth: 1
   :caption: Advanced Features

   mapdl
   conversion
   post

.. toctree::
   :maxdepth: 1
   :caption: Examples

   examples


Initial Setup and Example
-------------------------
To run, ``pyansys`` needs to know the location of the MAPDL binary.
When running for the first time, ``pyansys`` will request the location
of the MAPDL executable.  You can test your installation ``pyansys``
and set it up by running the following in python:

.. code:: python

    from pyansys import examples
    examples.ansys_cylinder_demo()

Python will automatically attempt to detect your MAPDL binary based on
environmental variables.  If it is unable to find a copy of MAPDL, you
will be prompted for the location of the MAPDL executable.  Here is a
sample input for Linux and Windows:

.. code::

    Enter location of MAPDL executable: /usr/ansys_inc/v182/ansys/bin/ansys182

.. code::

    Enter location of MAPDL executable: C:\Program Files\ANSYS Inc\v182\ANSYS\bin\winx64\ansys182.exe

The settings file is stored locally and you will not not need to enter
the path again.  If you need to change the default ansys path
(i.e. changing the default version of MAPDL), run the following:

.. code:: python

    import pyansys
    new_path = 'C:\\Program Files\\ANSYS Inc\\v182\\ANSYS\\bin\\winx64\\ansys182.exe'
    pyansys.change_default_ansys_path(new_path)


PyANSYS MAPDL Basics
--------------------
The ``MAPDL`` control module within ``pyansys`` creates an instance of
an interactive Shell of ``MAPDL`` in the background and sends commands
to that shell.  Errors and warnings are processed Pythonically letting
the user develop a script real-time without worrying about if it will
function correctly when deployed in batch mode.

MAPDL can be started from python using :func:`pyansys.launch_mapdl`.
This starts MAPDL in a temporary directory by default.  You can change
this to your current directory with:

.. code:: python

    import os
    import pyansys

    path = os.getcwd()
    mapdl = pyansys.launch_mapdl(run_location=path)

MAPDL is now active and you can send commands to it as a genuine a
Python class.  For example, if we wanted to create a surface using
keypoints we could run:

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

MAPDL interactively returns the result of each command and it is
stored to the logging module.  Errors are caught immediately.  For
example, if you input an invalid command:

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

The Python ``mapdl`` class supports much more than just sending text
to MAPDL and includes higher level wrapping allowing for better
scripting and interaction with MAPDL.  See the examples gallery for an
overview of the various advanced methods to visualize, script, and
interact with MAPDL.


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


.. autofunction:: pyansys.launch_mapdl
   
