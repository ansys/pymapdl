pyansys
========

Python module to extract data from ANSYS binary files and to display
them if vtk is installed.  Currently supports (*.rst) and (*.full) files.

Installation
------------

From PyPi directory

``pip install pyansys``

or

``python setup.py install``

License
-------

ANSYScdb is licensed under the MIT license. The full statement is
provided in the file named ``LICENSE``.

Dependencies
------------

Required: ``numpy``, ``cython``, ``ANSYScdb``. Optional: ``vtk``

Minimum requirements are numpy to extract results from a results file. To
convert the raw data to a VTK unstructured grid, vtk 5.0 or greater must
be installed with Python bindings.

Tests
-----

Test installation with the following

.. code:: python

    from pyansys import Tests

    # Load a hexahedral beam modal analysis result file
    Tests.Reader.Load()

    # Display first bending mode of that beam
    Tests.Reader.Display()

    # Load mass and stiffness matrices from the beam
    Tests.Reader.LoadKM()


Example: Reading a Result File
------------------------------
This example reads in binary results from a modal analysis from ANSYS.

Example files can be found within the Tests folder in installation folder.

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


Example: Reading a full file
----------------------------
This example reads in mass and stiffness matrices associated with `Beam.cdb`

Example files can be found within the Tests folder in installation folder.

.. code:: python

    # Load the reader from pyansys
    from pyansys import Reader
    
    # Create result reader object
    fobj = Reader.FullReader('file.full')
    
    # Read in full file
    fobj.LoadFullKM()

    # Data from the full file can now be accessed from the object
    # Can be used construct a sparse matrix and solve it

    # from scipy.sparse import csc_matrix, linalg
    #ndim = fobj.nref.size
    #k = csc_matrix((fobj.kdata, (fobj.krows, fobj.kcols)), shape=(ndim, ndim))
    #m = csc_matrix((fobj.mdata, (fobj.mrows, fobj.mcols)), shape=(ndim, ndim))
    # Solve
    #w, v = linalg.eigsh(k, k=20, M=m, sigma=10000)
    # System natural frequencies
    #f = np.sqrt(real(w))/(2*np.pi)

    

