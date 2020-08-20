Pythonic Data Access of Mesh and Geometry
-----------------------------------------
The ``pyansys.Mapdl`` class allows you to access the mesh and geometry
without writing to an intermediate file or interperting the text
output from various MAPDL commands.  For example, to access the nodes
and elements of a model, normally one would list the nodes within
MAPDL ``NLIST``, but this generates a string and array access either
requires cumbersome MAPDL GET commands, or requires the nodes be
written to a archive file and then read in within other software.  For
example:

.. code::

    NLIST

 LIST ALL SELECTED NODES.   DSYS=      0

    NODE        X             Y             Z           THXY     THYZ     THZX
        1   0.0000        0.0000        0.0000          0.00     0.00     0.00
        2   1.0000        0.0000        0.0000          0.00     0.00     0.00
        3   0.2500        0.0000        0.0000          0.00     0.00     0.00


However, with ``pyansys``, it's possible to interface with a current
instance of ``mapdl`` and access the current nodes coordinates with:

.. code:: python

   >>> mapdl.mesh.nodes
   [[0.   0.   0.  ]
    [1.   0.   0.  ]
    [0.25 0.   0.  ]
    ...,
    [0.75 0.5  3.5 ]
    [0.75 0.5  4.  ]
    [0.75 0.5  4.5 ]]


Both the ``geometry`` and ``mesh`` properties support additional, lower level access to MAPDL data.  Access them with:

.. code:: python

    >>> mapdl.mesh
    >>> mapdl.geometry


The MAPDL Geometry Class
------------------------
.. autoclass:: pyansys.mapdl_geometry.Geometry
    :members:


The MAPDL Mesh Class
--------------------
.. autoclass:: pyansys.mesh.Mesh
    :members:
    :show-inheritance:
    :noindex:
