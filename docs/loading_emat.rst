Working with a ANSYS Element Matrix File (.emat)
================================================
The ANSYS element matrix file is a FORTRAN formatted binary file containing the following for each element.

 - Stiffness matrix
 - Mass matrix
 - Damping matrix
 - Stress stiffening matrix
 - Complex stiffness matrix
 - Element force vectors


Example
-------
Load the element matrix file:

.. code:: python

    import pyansys
    emat_file = pyansys.read_binary('file.emat')

Read a single element from the result file:

.. code:: python

    element_data = emat_file.read_element(0)

The dictionary ``element_data`` contains the entries used to construct stiffness, mass, and damping matrices.  If recorded, the dictionary will also applied force vectors.


Applied Force
~~~~~~~~~~~~~
Read accumulated applied force for all nodes:

.. code:: python

    applied_force = emat_file.global_applied_force()

See ``emat_file.nnum`` for the sorted nodes this applied force corresponds to.

EmatFile Object Methods
-----------------------
.. autoclass:: pyansys.emat.EmatFile
    :members:
