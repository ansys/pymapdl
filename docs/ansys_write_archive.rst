Reading and Writing ANSYS Archives
==================================

Reading ANSYS Archives
----------------------
ANSYS archive files containing solid elements (both legacy and modern) can be loaded using Archive and then converted to a vtk object:

.. code:: python

    import pyansys
    from pyansys import examples

    # Sample *.cdb
    filename = examples.hexarchivefile

    # Read ansys archive file
    archive = pyansys.Archive(filename)

    # Print raw data from cdb
    for key in archive.raw:
       print("%s : %s" % (key, archive.raw[key]))

    # Create a vtk unstructured grid from the raw data and plot it
    grid = archive.parse_vtk(force_linear=True)
    grid.plot(color='w', show_edges=True)


You can also optionally read in any stored parameters within the archive file by enabling the ``read_parameters`` parameter.

.. code:: python

    import pyansys
    archive = pyansys.Archive('mesh.cdb')

    # parameters are stored as a dictionary
    print(archive.raw['parameters'])


Writing ANSYS Archives
----------------------
Unstructured grids generated using VTK can be converted to ANSYS APDL archive files and loaded into any version of ANSYS using ``pyansys.save_as_archive``.  The following example using the built-in archive file demonstrates this capability.

.. code:: python

    import pyvista as pv
    from pyvista import examples
    import pyansys

    grid = pv.UnstructuredGrid(examples.hexbeamfile)
    script_filename = '/tmp/grid.cdb'
    pyansys.save_as_archive(script_filename, grid)

    # read in archive in ANSYS and generate cell shape quality report
    ansys = pyansys.ANSYS()
    ansys.cdread('db', script_filename)
    ansys.prep7()
    ansys.shpp('SUMM')

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
