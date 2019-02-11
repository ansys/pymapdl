Write VTK Unstructured Grid as an ANSYS Archive
===============================================
Unstructured grids generated using VTK can be converted to ANSYS APDL archive files and loaded into any version of ANSYS using ``pyansys.save_as_archive``.  The following example using the built-in archive file demonstrates this capability.

.. code:: python

    import vtki
    from vtki import examples
    import pyansys

    grid = vtki.UnstructuredGrid(examples.hexbeamfile)
    script_filename = '/tmp/grid.cdb'
    pyansys.save_as_archive(script_filename, grid)

    # read in archive in ANSYS and generate cell shape quality report
    ansys = pyansys.ANSYS()
    ansys.Cdread('db', script_filename)
    ansys.Prep7()
    ansys.Shpp('SUMM')

Resulting ANSYS quality report:

.. code::

    ------------------------------------------------------------------------------
               <<<<<<          SHAPE TESTING SUMMARY           >>>>>>
               <<<<<<        FOR ALL SELECTED ELEMENTS         >>>>>>
    ------------------------------------------------------------------------------
                       --------------------------------------
                       |  Element count        40 SOLID185  |
                       --------------------------------------
   
     Test                Number tested  Warning count  Error count    Warn+Err %
     ----                -------------  -------------  -----------    ----------
     Aspect Ratio                 40              0             0         0.00 %
     Parallel Deviation           40              0             0         0.00 %
     Maximum Angle                40              0             0         0.00 %
     Jacobian Ratio               40              0             0         0.00 %
     Warping Factor               40              0             0         0.00 %
   
     Any                          40              0             0         0.00 %
    ------------------------------------------------------------------------------


Supported Elements
~~~~~~~~~~~~~~~~~~
At the moment, only solid elements are supported by the ``save_as_archive`` function, to include:

 - ``vtk.VTK_TETRA``
 - ``vtk.VTK_QUADRATIC_TETRA``
 - ``vtk.VTK_PYRAMID``
 - ``vtk.VTK_QUADRATIC_PYRAMID``
 - ``vtk.VTK_WEDGE``
 - ``vtk.VTK_QUADRATIC_WEDGE``
 - ``vtk.VTK_HEXAHEDRON``
 - ``vtk.VTK_QUADRATIC_HEXAHEDRON``

Linear element types will be written as SOLID185, quadratic elements will be written as SOLID186, except for quadratic tetrahedrals, which will be written as SOLID187.

Write Functions
---------------
.. automodule:: pyansys.archive
    :members:
