pyansys Documentation
=====================
The ``pyansys`` provides various pythonic interfaces to the MAPDL
application and both ASCII and binary MAPDL files.  It allows you to:

 - Interactively control an instance of ANSYS v17.0 on and newer using
   Python on Windows or v13 and newer on Linux.
 - Extract data directly from binary ANSYS v14.5+ files and display or
   animate them.
 - Rapidly read in binary results (``.rst``, ``.rth``), binary mass
   and stiffness ``(.full)``, and ASCII block archive ``(.cdb)``, and
   element matrix ``(.emat)`` files.

This python module is a community driven work in progress with
additional features regularly added based on user requests.  Open an
issue at `pyansys Issues <https://github.com/akaszynski/pyansys/issues>`_
if you identity a bug or would like to request an additional method or
feature.

Take a look at the :ref:`sphx_glr_examples` gallery for several demos using ``pyansys``.


Installation
------------
Installation through pip::

    pip install pyansys

You can also visit `PyPi <http://pypi.python.org/pypi/pyansys>`_ or `GitHub <https://github.com/akaszynski/pyansys>`_ to download the source.

If you have any installation (or other) issues, please open an issue at `pyansys Issues <https://github.com/akaszynski/pyansys/issues>`_.


Quick Examples
--------------

Interactive Control
~~~~~~~~~~~~~~~~~~~
You can create an interactive instance of MAPDL using ``pyansys`` to
send commands to it Pythonically, plot meshes and geometry within
python, and access underlying results directly through python.  Here's
a sample code snippet.

.. code:: python

    import os
    import pyansys

    path = os.getcwd()
    mapdl = pyansys.launch_mapdl(run_location=path)

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
    mapdl.save()
    mapdl.exit()


Direct Access to Binary Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Here's a quick example code block to show how easy it is to load and
plots results directly from an ANSYS result file using ``pyansys``:

.. code:: python

    >>> import pyansys
    >>> result = pyansys.read_binary('rotor.rst')
    >>> nnum, stress = result.principal_nodal_stress(0)
    >>> print(stress[:3])
    array([[-1.2874937e-06,  1.2874934e-06,  5.6843419e-14,  0.0000000e+00,  8.1756007e-06, -8.1756007e-06],
           [-1.1674185e-04, -1.1674478e-04, -3.0856981e-04, -1.7892545e-06, -2.5823609e-05,  2.5835518e-05],
           [-5.7354209e-05, -5.5398770e-05, -1.4944717e-04, -1.0580692e-06, -1.7659733e-05, -3.5462126e-06]], dtype=float32)

    >>> estress, elem, enode = result.element_stress(0)  # element stress for result 0
    >>> estress[0]  # element stress for element 0
    array([[ 1.0236604e+04, -9.2875127e+03, -4.0922625e+04, -2.3697146e+03, -1.9239732e+04,  3.0364934e+03]
           [ 5.9612605e+04,  2.6905924e+01, -3.6161423e+03,  6.6281304e+03,  3.1407712e+02,  2.3195926e+04]
	   [ 3.8178301e+04,  1.7534495e+03, -2.5156013e+02, -6.4841372e+03, -5.0892783e+03,  5.2503605e+00]
	   [ 4.9787645e+04,  8.7987168e+03, -2.1928742e+04, -7.3025332e+03,  1.1294199e+04,  4.3000205e+03]])

    >>> elem[0]  # corresponding ansys element number for element 0
        32423

    >>> enode[0]  # corresponding nodes belonging to for element 0
        array([ 9012,  7614,  9009, 10920], dtype=int32)

    >>> result.plot_nodal_solution(0)

.. figure:: ./images/rotor.jpg
    :width: 500pt

--------

Contents
========
.. toctree::
   :maxdepth: 1
   :caption: Interactive MAPDL Python Interface

   mapdl/index

.. toctree::
   :maxdepth: 1
   :caption: ANSYS File Support

   archive
   loading_results
   examples
   loading_km
   loading_emat

.. toctree::
   :maxdepth: 1
   :caption: Example Gallery

   examples/index

.. toctree::
   :maxdepth: 1
   :caption: Miscellaneous
   :hidden:

   quality

--------

License and Acknowledgments
---------------------------
The ``pyansys`` module is licensed under the MIT license.

ANSYS documentation and functions build from html that was hosted on
`Sharcnet <https://www.sharcnet.ca/Software/Ansys/>`_.  They've since
taken down their documentation, but it was an excellent resource and I
appreciate their work.

This module, ``pyansys`` makes no commercial claim over ANSYS
whatsoever.  This tool extends the functionality of MAPDL by adding a
Python interface to both the core application and the binary files
behavior or license of the original software.  The interactive use of
MAPDL using ``pyansys`` requires a legally licensed local copy of
ANSYS.
