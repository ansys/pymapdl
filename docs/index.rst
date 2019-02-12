pyansys Documentation
=====================
This Python module allows you to:
 - Interactively control an instance of ANSYS v17.0 + using Python.
 - Extract data directly from binary ANSYS v14.5+ files and to display or animate them.
 - Rapidly read in binary result ``(.rst)``, binary mass and stiffness ``(.full)``, and ASCII block archive ``(.cdb)`` files.

This python module is a community driven work in progress with additional features regularly added based on user requests.  Open an issue at `pyansys Issues <https://github.com/akaszynski/pyansys/issues>`_ if you identity a bug or would like to request an additional method or feature.


Installation
------------
Installation through pip::

    pip install pyansys


Quick Examples
--------------

Interactive Control
~~~~~~~~~~~~~~~~~~~
``pyansys`` lets you create an instance of ANSYS and send commands to it pythonically:

.. code:: python

    import os
    import pyansys

    path = os.getcwd()
    ansys = pyansys.ANSYS(run_location=path)

    # create a square area using keypoints
    ansys.Prep7()
    ansys.K(1, 0, 0, 0)
    ansys.K(2, 1, 0, 0)
    ansys.K(3, 1, 1, 0)
    ansys.K(4, 0, 1, 0)    
    ansys.L(1, 2)
    ansys.L(2, 3)
    ansys.L(3, 4)
    ansys.L(4, 1)
    ansys.Al(1, 2, 3, 4)
    ansys.Save()
    ansys.Exit()


Direct Access to Binary Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Here's a quick example code block to show how easy it is to load and plots results directly from an ANSYS result file using ``pyansys``:

.. code:: python

    >>> import pyansys
    >>> result = pyansys.ResultReader('rotor.rst')
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


Contents
========
.. toctree::
   :maxdepth: 2

   ansys_control
   ansys_functions
   apdl_conversion
   ansys_write_archive
   ansys_examples
   loading_results
   examples
   loading_km


Installation
------------
Installation through pip::

    pip install pyansys

You can also visit `PyPi <http://pypi.python.org/pypi/pyansys>`_ or `GitHub <https://github.com/akaszynski/pyansys>`_ to download the source.

Dependencies:

- ``numpy``
- ``cython``
- ``vtki``
- ``pexpect``
- ``appdirs``
- ``vtk``

Dependencies are installed automatically through ``pip``, except for Python 2.7 in Windows, which will require some additional work to install ``VTK``.  See `installing vtk <http://vtkinterface.readthedocs.io/en/latest/installation.html>`_ for more information.


License
-------
This module is licensed under the MIT license.  See the license file for more details.
