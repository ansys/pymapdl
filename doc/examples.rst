Archive Result File Examples
============================
These examples show how ANSYS binary and ASCII files can be read and displayed using pyansys.  These examples are meant to demonstrate the capabilities of pyansys.  For more details see the other reference pages.

Loading and Plotting an ANSYS Archive File
------------------------------------------

.. _examples_ref:

ANSYS archive files containing solid elements (both legacy and modern) can be loaded using ReadArchive and then converted to a vtk object.


.. code:: python

    import pyansys
    from pyansys import examples
    
    # Sample *.cdb
    filename = examples.hexarchivefile
    
    # Read ansys archive file
    archive = pyansys.ReadArchive(filename)
    
    # Print raw data from cdb
    for key in archive.raw:
       print("%s : %s" % (key, archive.raw[key]))
    
    # Create a vtk unstructured grid from the raw data and plot it
    grid = archive.ParseVTK(force_linear=True)
    grid.Plot()
    
    # write this as a vtk xml file 
    grid.Write('hex.vtu')


.. image:: ./images/hexbeam.png


You can then load this vtk file using vtkInterface or another program that uses VTK.
    
.. code:: python

    # Load this from vtk
    import vtkInterface
    grid = vtkInterface.UnstructuredGrid('hex.vtk')
    grid.Plot()


Loading and Plotting Results from an ANSYS Result File
------------------------------------------------------

Loading the Result File
~~~~~~~~~~~~~~~~~~~~~~~

This example reads in binary results from a modal analysis of a beam from ANSYS.  This section of code does not rely on ``VTK`` and can be used with only numpy installed.

.. code:: python

    # Load the reader from pyansys
    import pyansys
    from pyansys import examples
    
    # Sample result file
    rstfile = examples.rstfile
    
    # Create result object by loading the result file
    result = pyansys.ResultReader(rstfile)
    
    # Get beam natural frequencies
    freqs = result.GetTimeValues()
    
    # Get the node numbers in this result file
    nnum = result.nnum
    
    # Get the 1st bending mode shape.  Results are ordered based on the sorted 
    # node numbering (by default and same as `nnum` above).
    disp = result.GetNodalResult(0) # uses 0 based indexing 
    
.. code:: python

    >>> print(disp)
    [[  0.           0.           0.        ]
     [  0.           0.           0.        ]
     [  0.           0.           0.        ]
     ..., 
     [ 21.75315943 -14.01733637  -2.34010126]
     [ 26.60384371 -17.14955041  -2.40527841]
     [ 31.50985156 -20.31588852  -2.4327859 ]]


Plotting Nodal Results
~~~~~~~~~~~~~~~~~~~~~~
As the geometry of the model is contained within the result file, you can plot the result without having to load any additional geometry.  Below, displacement for the first bending mode of the beam is plotted using ``VTK``.  To use this functionality, ``VTK`` must be installed.

.. code:: python
    
    # Plot the displacement of Mode 0 in the x direction
    result.PlotNodalResult(0, 'x', label='Displacement')
    

.. image:: ./images/hexbeam_disp.png


Stress can be plotted as well using the below code.  The nodal stress is computed in the same manner that ANSYS uses by to determine the stress at each node by averaging the stress evaluated at that node for all attached elements.  For now, only component stresses can be displayed.

.. code:: python
    
    # Display node averaged stress in x direction for result 6
    result.PlotNodalStress(5, 'Sx')
    

.. image:: ./images/beam_stress.png

Here's the same result as viewed from ANSYS.

.. image:: ./images/ansys_stress.png



Built-In Examples
-----------------
The following examples can be run natively from pyansys by importing the examples subpackage.


Plot Cell Quality
~~~~~~~~~~~~~~~~~
This built in example displays the minimum scaled jacobian of each element of a tetrahedral beam:

.. code:: python

    from pyansys import examples
    examples.DisplayCellQual()

.. image:: ./images/cellqual.png

This is the source code for the example:

.. code:: python

    import pyansys

    # load archive file and parse for subsequent FEM queries
    from pyansys import examples
    # archive = pyansys.ReadArchive(examples.hexarchivefile)
    archive = pyansys.ReadArchive(examples.tetarchivefile)
            
    # create vtk object
    grid = archive.ParseVTK(force_linear=True)

    # get cell quality
    qual = grid.CellQuality()
    
    # plot cell quality
    grid.Plot(scalars=qual, stitle='Cell Minimum Scaled\nJacobian', rng=[0, 1])
    

Plot Nodal Stress
~~~~~~~~~~~~~~~~~
This built in example plots the x component stress from a hexahedral beam.
    
.. code:: python

    from pyansys import examples
    examples.DisplayStress()

.. image:: ./images/beam_stress.png

This is the source code for the example:

.. code:: python

    import pyansys
    from pyansys import examples
    filename = examples.rstfile
    
    # Create rsult object
    result = pyansys.ResultReader(filename)
    
    # Plot node averaged stress in x direction for result 6
    result.PlotNodalStress(5, 'Sx')
