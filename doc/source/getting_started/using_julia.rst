.. _using_julia:


***********************
Using PyMAPDL in Julia
***********************

If you like to work with Julia, you can use python libraries as they were Julia packages.


Installing Julia
=================

To install Julia go to their website `<https://julialang.org/>`_ to the **Download** section and follow the instructions given there.


Setting Julia Environment
==========================

To have access to Python libraries, we need to install *PyCall* Julia package.
To install it, run Julia and switch to the package manager by pressing ``]`` key.

It is beneficial to create a virtual environment in Julia, in order to work with different package versions or applications if needed.
To create a virtual environment, use ``activate`` command with the name of the new environment you want to create or activate.

.. code:: julia

    (@1.7) pkg> activate julia_test
      Activating project at `C:\Users\USER\julia_test`


It should show a message that the new package (``julia_test``) has been activated and that environment name will now precede the command line.

.. code::

    (julia_test) pkg>

Then we proceed to install *PyCall* package by typing:

.. code:: julia

    (julia_test) pkg> add PyCall


To use PyCall, we go first to the Julia command line by pressing the backspace key.
Then we can use the *PyCall* package as:

.. code:: julia

    julia> using PyCall


This should be enough to use packages included in a basic Python distribution. 


For example:

.. code:: julia

    julia> math = pyimport("math")
    math.sin(math.pi/4) # returns ≈ 1/√2 = 0.70710678..



Installing PyMAPDL in Julia
============================

*PyCall* includes a lightweight Python environment which uses `Conda <https://conda.io>`_ to manage and access Python packages.
This environment is based on Python 3.9.7 (at the moment of writing this article) and includes the standard basic Python libraries.
However since it is a fully working Python environment, we can still use it from outside Julia command line and install Python packages using *pip*.

To install PyMAPDL we have first to locate the Python executable by typing:

.. code:: julia

    julia> PyCall.python
    "C:\\Users\\USER\\.julia\\conda\\3\\python.exe"


Now we will use that Python executable to install PyMAPDL:

.. code:: bash

    C:\Users\USER\.julia\conda\3\python.exe -m pip install ansys-mapdl-core

Finally we can import PyMAPDL using the same procedure as described above:

.. code:: julia
    
    julia> using PyCall
    julia> pymapdl = pyimport("ansys.mapdl.core")
    PyObject <module 'ansys.mapdl.core' from 'C:\\Users\\USER\\.julia\\conda\\3\\lib\\site-packages\\ansys\\mapdl\\core\\__init__.py'>
    julia> print(mapdl.__str__())
    Product:             Ansys Mechanical Enterprise
    MAPDL Version:       21.2
    ansys.mapdl Version: 0.60.6
    

A simple example can be shown below:

.. code-block:: julia

    julia> using PyCall
    julia> pymapdl = pyimport("ansys.mapdl.core")
    julia> mapdl = pymapdl.launch_mapdl()
    julia> np = pyimport("numpy")
    julia> # define cylinder and mesh parameters
    julia> torque = 100
    julia> radius = 2
    julia> h_tip = 2
    julia> height = 20
    julia> elemsize = 0.5
    julia> pi = np.arccos(-1)
    julia> force = 100/radius
    julia> pressure = force/(h_tip*2*np.pi*radius)
    julia> # Define higher-order SOLID186
    julia> # Define surface effect elements SURF154 to apply torque
    julia> # as a tangential pressure
    julia> mapdl.prep7()
    julia> mapdl.et(1, 186)
    julia> mapdl.et(2, 154)
    julia> mapdl.r(1)
    julia> mapdl.r(2)
    julia> # Aluminum properties (or something)
    julia> mapdl.mp("ex", 1, 10e6)
    julia> mapdl.mp("nuxy", 1, 0.3)
    julia> mapdl.mp("dens", 1, 0.1/386.1)
    julia> mapdl.mp("dens", 2, 0)
    julia> # Simple cylinder
    julia> for i in 1:5
                mapdl.cylind(radius, "", "", height, 90*(i-1), 90*i)
    julia> end
    julia> mapdl.nummrg("kp")
    julia> # interactive volume plot (optional)
    julia> mapdl.vplot()
    julia> # mesh cylinder
    julia> mapdl.lsel("s", "loc", "x", 0)
    julia> mapdl.lsel("r", "loc", "y", 0)
    julia> mapdl.lsel("r", "loc", "z", 0, height - h_tip)
    julia> mapdl.lesize("all", elemsize*2)
    julia> mapdl.mshape(0)
    julia> mapdl.mshkey(1)
    julia> mapdl.esize(elemsize)
    julia> mapdl.allsel("all")
    julia> mapdl.vsweep("ALL")
    julia> mapdl.csys(1)
    julia> mapdl.asel("s", "loc", "z", "", height - h_tip + 0.0001)
    julia> mapdl.asel("r", "loc", "x", radius)
    julia> mapdl.local(11, 1)
    julia> mapdl.csys(0)
    julia> mapdl.aatt(2, 2, 2, 11)
    julia> mapdl.amesh("all")
    julia> mapdl.finish()
    julia> # plot elements
    julia> mapdl.eplot()


.. note:: Do notice the changes in the strings (only ``"`` strings are allowed) and the loops.