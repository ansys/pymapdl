Working with a ANSYS Result File (rst)
======================================

The ANSYS result file is a fortran formatted binary file containing the results
written from an ANSYS analysis.  The results, at a minimum, contain the geometry
of the model analyzed along with the nodal and element results.  Depending on
the analysis, these results could be anything from modal displacements to 
nodal temperatures.  At this time, only the following results are supported by
this code
    - Nodal DOF results from a static analysis or harmonic analysis.
    - Nodal averaged component stresses (i.e. x, y, z, xy, xz, yz)

We're working on adding additional plotting and retrival functions to the code 
If you would like us to add an additional result type to be loaded, 
please open an issue in `GitHub <https://github.com/akaszynski/pyansys>`_  and 
include result file for the result type you wish to load.


Loading the Result File
~~~~~~~~~~~~~~~~~~~~~~~

As the ANSYS result files are binary files, the entire file does not need to be
loaded into memory in order to retrieve results.  This module
accesses the results through a python object `result` which you can create with

.. code:: python

    import pyansys
    result = pyansys.ResultReader('file.rst')
    
Upon initialization this result file contains several properties to include the
time values from the analysis, node numbering, element numbering, etc.


Result File Properties
~~~~~~~~~~~~~~~~~~~~~~

The properties of the result file can be listed the below code.  At the moment,
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
~~~~~~~~
    
The geometry of the model can be accessed directly from the dictionary by 
accessing

.. code:: python

    result.geometry
    
Which contains the following keys

    - ``'nnum'`` (sorted node numbering )
    - ``'nodes'`` (node positions)
    - ``'etype'`` (element type)
    - ``'enum'`` (non-sorted element numbers associated with elem array)
    - ``'elem'`` (numpy array showing nodes associated with each element, -1 indicates unused entry)
    - ``'ekey'`` (2xn element type reference array)
    

Accessing Solution Results
~~~~~~~~~~~~~~~~~~~~~~~~~~

The DOF solution for an analysis for each node in the analysis can be obtained
using the code block below.  These results correspond to the node numbers in
the result file.  This array is sized by the number of nodes by the number of 
degrees of freedom.

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

Stress can be obtained as well using the below code.  The nodal stress is 
computed in the same manner that ANSYS uses by to determine the stress at each
node by averaging the stress evaluated at that node for all attached elements.
For now, only component stresses can be displayed.

.. code:: python
    
    # obtain the component node averaged stress for the first result
    # organized with one [Sx, Sy Sz, Sxy, Syz, Sxz] entry for each node
    stress = result.NodalStress(0) # results in a np array (nnod x 6)

    # Display node averaged stress in x direction for result 6
    result.PlotNodalStress(5, 'Sx')
    
  