ANSYS Functions
===============
These functions can be called directly from an ``ANSYS`` object.  This is to simplifiy calling ANSYS, especially when inputs are variables within Python.  For example, the following two commands are equivalent:

.. code:: python

    ansys.K(1, 0, 0, 0)
    ansys.Run('K, 1, 0, 0, 0')

This approach has some obvious advantages, chiefly that it's a bit easier to script as ``pyansys`` takes care of the string formatting for you.  For example, inputting points from a numpy array:

.. code:: python

   # make 10 random keypoints in ANSYS
   points = np.random.random((10, 3))
   for i, (x, y, z) in enumerate(points):
       ansys.K(i + 1, x, y, z)

Additionally, exceptions are caught and handled within Python.

.. code:: python

    >>> ansys.Run('AL, 1, 2, 3')

   Exception: 
   AL, 1, 2, 3

   DEFINE AREA BY LIST OF LINES
   LINE LIST =     1    2    3
   (TRAVERSED IN SAME DIRECTION AS LINE     1)

   *** ERROR ***                           CP =       0.338   TIME= 09:45:36
   Keypoint 1 is referenced by only one line.  Improperly connected line   
   set for AL command.                                                     


Available Commands
==================
.. autoclass:: pyansys.ansys_functions._InternalANSYS
    :members:
