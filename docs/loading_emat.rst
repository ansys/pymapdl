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

    dof_ref, element_data = emat_file.read_element(0)

The dictionary ``element_data`` contains the entries used to construct stiffness, mass, and damping matrices.  If recorded, the dictionary will also applied force vectors.


Applied Force
~~~~~~~~~~~~~
Read accumulated applied force for all nodes:

.. code:: python

    applied_force = emat_file.global_applied_force()

See ``emat_file.nnum`` for the sorted nodes this applied force corresponds to.


DOF Reference
~~~~~~~~~~~~~
Each degree of freedom index from ``read_element`` corresponds to a
physical degree of freedom.  The table of this correspondence is
below:

+---------+---------+
| Index   | DOF     |
+---------+---------+
| 1       | UX      |
+---------+---------+
| 2       | UY      |
+---------+---------+
| 3       | UZ      |
+---------+---------+
| 4       | ROTX    |
+---------+---------+
| 5       | ROTY    |
+---------+---------+
| 6       | ROTZ    |
+---------+---------+
| 7       | AX      |
+---------+---------+
| 8       | AY      |
+---------+---------+
| 9       | AZ      |
+---------+---------+
| 10      | VX      |
+---------+---------+
| 11      | VY      |
+---------+---------+
| 12      | VZ      |
+---------+---------+
| 16      | WARP    |
+---------+---------+
| 17      | CONC    |
+---------+---------+
| 18      | HDSP    |
+---------+---------+
| 19      | PRES    |
+---------+---------+
| 20      | TEMP    |
+---------+---------+
| 21      | VOLT    |
+---------+---------+
| 22      | MAG     |
+---------+---------+
| 23      | ENKE    |
+---------+---------+
| 24      | ENDS    |
+---------+---------+
| 25      | EMF     |
+---------+---------+
| 26      | CURR    |
+---------+---------+
| 27 - 32 | Spares  |
+---------+---------+


EmatFile Object Methods
-----------------------
.. autoclass:: pyansys.emat.EmatFile
    :members:
