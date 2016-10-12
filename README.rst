pyansys
========

Python module to extract data from ANSYS binary files and to display
them if vtk is installed.  Currently only supports (*.rst) files.

Installation
------------

From source directory

``pip install .``

or

``python setup.py install``

License
-------

ANSYScdb is licensed under the MIT license. The full statement is
provided in the file named ``LICENSE``.

Dependencies
------------

Required: ``numpy``, ``ANSYScdb``. Optional: ``vtk``

Minimum requirements are numpy to extract results from a results file. To
convert the raw data to a VTK unstructured grid, vtk 5.0 or greater must
be installed with Python bindings.

Tests
-----

Test installation with the following from Python

.. code:: python

    from pyansys import Tests

    # Load a hexahedral beam modal analysis result file
    Tests.Reader.Load()

    # Display first bending mode of that beam
    Tests.Reader.Display()


Example Code
------------

Assumes you have the example files . Otherwise, replace
‘Beam.cdb’ with your own blocked \*.cdb file.

.. code:: python

    # Load the reader from pyansys
    from pyansys import Reader
    
    # Create result reader object
    fobj = Reader.ResultReader('file.rst')
    
    # Get mode frequencies
    freqs = fobj.tvalues
    
    # Get the node numbers in this result file
    nnum = fobj.nnum
    
    # Get the mode shape at mode 7 (ANSYS result 7)
    disp = fobj.GetResult(6) # uses 0 based indexing 
    
    # Load CDB (necessary for display)
    fobj.LoadCDB('mesh.cdb')
    
    # Plot the displacement of Mode 41 in the x direction
    fobj.PlotDisplacement(40, 'x')

