Working with a ANSYS Result File (rst)
======================================
The ANSYS result file is a FORTRAN formatted binary file containing the results written from an ANSYS analysis.  The results, at a minimum, contain the geometry of the model analyzed along with the nodal and element results.  Depending on the analysis, these results could be anything from modal displacements to nodal temperatures.  At this time, only the following results are supported by this code:

    - Nodal DOF results from a static analysis or modal analysis.
    - Nodal DOF results from a cyclic static or modal analysis.
    - Nodal averaged component stresses (i.e. x, y, z, xy, xz, yz)
    - Nodal principal stresses (i.e. S1, S2, S3, SEQV, SINT)

We're working on adding additional plotting and retrieval functions to the code If you would like us to add an additional result type to be loaded, please open an issue in `GitHub <https://github.com/akaszynski/pyansys>`_  and include result file for the result type you wish to load.


Loading the Result File
-----------------------
As the ANSYS result files are binary files, the entire file does not need to be loaded into memory in order to retrieve results.  This module accesses the results through a python object `result` which you can create with:

.. code:: python

    import pyansys
    result = pyansys.ResultReader('file.rst')
    
Upon initialization the ``ResultReader`` object contains several properties to include the time values from the analysis, node numbering, element numbering, etc.


ResultReader Properties
-----------------------
The properties of the ``ResultReader`` are listed below.  At the moment,
the property listing is limited to only the number of results in the file.

.. code:: python

    result_dic = result.ResultsProperties()

To obtain the time or frequency values of an analysis use:
    
.. code:: python

    tval = result.GetTimeValues()
    
The sorted node and element numbering of a result can be obtained with:

.. code:: python

    # sorted node numbering
    nnum = result.nnum
    
    # sorted element numbering
    enum = result.enum
    
Geometry
--------
The geometry of the model can be accessed directly from the dictionary by 
accessing:

.. code:: python

    result.geometry
    
Which contains the following keys:

    - ``'nnum'`` (sorted node numbering )
    - ``'nodes'`` (node positions)
    - ``'etype'`` (element type)
    - ``'enum'`` (non-sorted element numbers associated with elem array)
    - ``'elem'`` (numpy array showing nodes associated with each element, -1 indicates unused entry)
    - ``'ekey'`` (2xn element type reference array)
    

Accessing Solution Results
--------------------------
The DOF solution for an analysis for each node in the analysis can be obtained using the code block below.  These results correspond to the node numbers in the result file.  This array is sized by the number of nodes by the number of degrees of freedom.

.. code:: python    

    # Create an array of results (nnod x dof)
    disp = result.GetNodalResult(0) # uses 0 based indexing 
    
    # which corresponds to the sorted node numbers from
    nnum = result.nnum

    # The same results can be plotted using 
    display_string = 'Displacement' # optional string
    result.PlotNodalResult(0, 'x', label=display_string) # x displacement

    # normalized displacement can be plotted by excluding the direction string
    result.PlotNodalResult(0, label='Normalized')

Stress can be obtained as well using the below code.  The nodal stress is computed in the same manner as ANSYS by averaging the stress evaluated at that node for all attached elements.

.. code:: python
    
    # obtain the component node averaged stress for the first result
    # organized with one [Sx, Sy Sz, Sxy, Syz, Sxz] entry for each node
    nodenum, stress = result.NodalStress(0) # results in a np array (nnod x 6)

    # Display node averaged stress in x direction for result 6
    result.PlotNodalStress(5, 'Sx')

    # Compute principal nodal stresses and plot SEQV for result 1
    nodenum, pstress = result.PrincipalNodalStress(0)
    result.PlotPrincipalNodalStress(0, 'SEQV')

Element stress can be obtained using the following segment of code.  Ensure that the element results are expanded for a modal analysis within ANSYS with::

    /SOLU
    MXPAND, ALL, , , YES

This block of code shows how you can access the non-averaged stresses for the first result from a modal analysis.

.. code:: python
    
    import pyansys
    result = pyansys.ResultReader('result.rst')
    estress, elem, enode = result.ElementStress(0)

    
These stresses can be verified using ANSYS using:

.. code:: python

    >>> estress[0]
    [[ 1.0236604e+04 -9.2875127e+03 -4.0922625e+04 -2.3697146e+03
      -1.9239732e+04  3.0364934e+03]
     [ 5.9612605e+04  2.6905924e+01 -3.6161423e+03  6.6281304e+03
       3.1407712e+02  2.3195926e+04]
     [ 3.8178301e+04  1.7534495e+03 -2.5156013e+02 -6.4841372e+03
      -5.0892783e+03  5.2503605e+00]
     [ 4.9787645e+04  8.7987168e+03 -2.1928742e+04 -7.3025332e+03
       1.1294199e+04  4.3000205e+03]]

    >>> elem[0]
        32423

    >>> enode[0]
        array([ 9012,  7614,  9009, 10920], dtype=int32)

.. code::

  POST1:
  ESEL, S, ELEM, , 32423
  PRESOL, S

  ***** POST1 ELEMENT NODAL STRESS LISTING *****                                
 
  LOAD STEP=     1  SUBSTEP=     1                                             
   FREQ=    47.852      LOAD CASE=   0                                         
 
  THE FOLLOWING X,Y,Z VALUES ARE IN GLOBAL COORDINATES                         
 
  ELEMENT=   32423        SOLID187
    NODE    SX          SY          SZ          SXY         SYZ         SXZ     
    9012   10237.     -9287.5     -40923.     -2369.7     -19240.      3036.5    
    7614   59613.      26.906     -3616.1      6628.1      314.08      23196.    
    9009   38178.      1753.4     -251.56     -6484.1     -5089.3      5.2504    
   10920   49788.      8798.7     -21929.     -7302.5      11294.      4300.0    


Results from a Cyclic Analysis
------------------------------
``pyansys`` can load and display the results of a cyclic analysis:

.. code:: python

    import pyansys

    # load the result file    
    result = pyansys.ResultReader('rotor.rst')
    
You can reference the load step table and harmonic index tables by printing the result header dictionary keys ``'ls_table'`` and ``'hindex'``:

.. code:: python

    >>> print(result.resultheader['ls_table'])
    # load step, sub step, cumulative index
    array([[ 1,  1,  1], 
           [ 1,  2,  2],
           [ 1,  3,  3],
           [ 1,  4,  4],
           [ 1,  5,  5],
           [ 2,  1,  6],

    >>> print(result.resultheader['hindex'])
    array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4,
           4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7], dtype=int32)

Where each harmonic index entry corresponds a cumulative index.  For example, result number 11 is the first mode for the 2nd harmonic index:

.. code:: python

    >>> result.resultheader['ls_table'][10] # Result 11 (using zero based indexing)
    array([ 3,  1, 11], dtype=int32)
    
    >>> result.resultheader['hindex'][10]
    2

Results from a cyclic analysis require additional post processing to be  displayed correctly.  Mode shapes are stored within the result file as unprocessed parts of the real and imaginary parts of a modal solution.  ``pyansys`` combines these values into a single complex array and varies the phase of the solution when plotting.  Running ``GetCyclicNodalResult`` returns the unprocessed complex solution for a sector for a given cumulative index:

.. code:: python

    >>> ms = result.GetCyclicNodalResult(10) # mode shape of result 11
    >>> print(ms[:3])
    [[ 44.700-19.263j, 45.953+44.856j, 38.717+23.216]
     [ 42.339-14.645j, 48.516+43.742j, 52.475+24.255]
     [ 36.000-12.764j, 33.121+40.970j, 39.044+22.881j]]

These results correspond to the nodes of the master sector, whose node numbers can be found in the ``cyc_nnum`` array:

.. code:: python

    >>> result.cyc_nnum # sorted node numbers from the master cyclic sector
    array([  1,   2,   4,   6,   9,  10,  12, ...


The real displacement of the sector is always the real component of the mode shape ``ms``, and this can be varied by multiplying the mode shape by a complex value for a given phase.  To change the phase by 90 degrees simply:

.. code:: python
    
    >>> from math import sin, cos
    >>> angle = 3.1415/2 # 90 degrees
    >>> ms *= cos(angle) + 1j*sin(angle)


The results of a single sector can be displayed as well using the ``PlotCyclicNodalResult`` command with the ``expand=False``

.. code:: python

    # Plot the result from the 11th cumulative result
    result.PlotCyclicNodalResult(10, label='Displacement', expand=False)
    
.. image:: ./images/sector.jpg
    
By default the phase of the sector results is changed such that the normalized displacement of the mode shape will be maximized at the highest responding node.  The full rotor can be shown by running:
    
.. code:: python

    >>> result.PlotCyclicNodalResult(10, label='Displacement')

.. image:: ./images/rotor.jpg

The phase of the result can be changed by modifying the ``phase`` option.  See ``help(result.PlotCyclicNodalResult)`` for details on its implementation.
        

Exporting to ParaView
---------------------
ParaView is a visualization application that can be used for rapid generation of plots and graphs using VTK through a GUI.  ``pyansys`` can translate the ANSYS result files to ParaView compatible files containing the geometry and nodal results from the analysis:

.. code:: python

    import pyansys
    from pyansys import examples
    
    # load example beam result file
    result = pyansys.ResultReader(examples.rstfile)
    
    # save as a binary vtk xml file
    result.SaveAsVTK('beam.vtu')

The vtk xml file can now be loaded using ParaView.  This screenshot shows the nodal displacement of the first result from the result file plotted within `ParaView <https://www.paraview.org/>`_.  Within the vtk file are two point arrays (``NodalResult`` and ``NodalStress``) for each result in the result file.  The nodal result values will depend on the analysis type, while nodal stress will always be the node average stress in the Sx, Sy Sz, Sxy, Syz, and Sxz directions.

.. image:: ./images/paraview.jpg


ResultReader Object Methods
---------------------------

.. autoclass:: pyansys.ResultReader
    :members:
