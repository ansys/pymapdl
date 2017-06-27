pyansys
=======

This Python module allows you to to extract data from ANSYS files and to display
them if vtk is installed.  Currently supports result (.rst), mass and stiffness (.full), and block archive (.cdb) files.

See the `Documentation <http://pyansys.readthedocs.io>`_ page for more details.


Installation
------------

Installation through pip::

    pip install pyansys

You can also visit `GitHub <https://github.com/akaszynski/pyansys>`_ to download the source.

Dependencies: ``numpy``, ``cython``, ``vtkInterface``. Optional: ``vtk``

Minimum requirements are numpy to extract results from a results file. To
convert the raw data to a VTK unstructured grid, VTK 5.0 or greater must
be installed with Python bindings.


Quick Examples
--------------

Many of the following examples are built in and can be run from the build-in
examples module.  For a quick demo, run:

.. code:: python

    from pyansys import examples
    examples.RunAll()

Loading and Plotting an ANSYS Archive File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ANSYS archive files containing solid elements (both legacy and current), can
be loaded using ReadArchive and then converted to a vtk object.


.. code:: python

    import pyansys
    from pyansys import examples
    
    # Sample *.cdb
    filename = examples.hexarchivefile
    
    # Read ansys archive file
    archive = pyansys.ReadArchive(filename)
    
    # Print raw data from cdb
    for key in archive.raw:
       print "%s : %s" % (key, archive.raw[key])
    
    # Create a vtk unstructured grid from the raw data and plot it
    archive.ParseFEM()
    archive.uGrid.Plot()
    
    # write this as a vtk xml file 
    archive.SaveAsVTK('hex.vtu')


You can then load this vtk file using vtkInterface or another program that uses
VTK.
    
.. code:: python

    # Load this from vtk
    import vtkInterface
    grid = vtkInterface.LoadGrid('hex.vtk')
    grid.Plot()


Loading and Plotting an ANSYS Result File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example reads in binary results from a modal analysis of a beam from
ANSYS.  This section of code does not rely on vtk and can be used solely with
numpy installed.

.. code:: python

    # Load the reader from pyansys
    import pyansys
    
    # Sample result file
    from pyansys import examples
    rstfile = examples.rstfile
    
    # Create result reader object by loading the result file
    result = pyansys.ResultReader(rstfile)
    
    # Get the solution time values (natural frequencies for this modal analysis)
    freqs = result.GetTimeValues()
    
    # Get the node numbers in this result file
    nnum = result.nnum
    
    # Get the 1st bending mode shape.  Nodes are ordered according to nnum.
    disp = result.GetNodalResult(0, True) # uses 0 based indexing 

    # it's just a numpy array
    print disp
    
.. code::

    [[  0.           0.           0.        ]
     [  0.           0.           0.        ]
     [  0.           0.           0.        ]
     ..., 
     [ 21.75315943 -14.01733637  -2.34010126]
     [ 26.60384371 -17.14955041  -2.40527841]
     [ 31.50985156 -20.31588852  -2.4327859 ]]

You can plot results as well directly from the file as well.

.. code:: python
    
    # Plot the displacement of the 1st in the x direction
    result.PlotNodalResult(0, 'x', label='Displacement')

    # Plot the nodal stress in the 'x' direction for the 6th result
    result.PlotNodalStress(5, 'Sx')


Reading a Full File
-------------------
This example reads in the mass and stiffness matrices associated with the above
example.

.. code:: python

    # Load the reader from pyansys
    import pyansys
    
    # load the full file
    fobj = pyansys.FullReader('file.full')
    dofref, k, m = fobj.LoadKM(utri=False)
    

If you have ``scipy`` installed, you can solve the eigensystem for its natural 
frequencies and mode shapes.

.. code:: python

    from scipy.sparse import linalg

    # Solve
    w, v = linalg.eigsh(k, k=20, M=m, sigma=10000)
    # System natural frequencies
    f = (np.real(w))**0.5/(2*np.pi)
    
    print('First four natural frequencies')
    for i in range(4):
        print '{:.3f} Hz'.format(f[i])
    
.. code::

    First four natural frequencies
    1283.200 Hz
    1283.200 Hz
    5781.975 Hz
    6919.399 Hz

License
-------

pyansys is licensed under the MIT license.


