.. _ref_extended_examples_ex01:


Example 01: Gmsh Example
========================

Objective
---------
Demonstrate the interoperability of PyANSYS with ``gmsh``, a very wellknown open source Python meshing library.

For more information about ``gmsh`` please visit its website: `Gmsh <https://gmsh.info/>`_.

Description
-----------
In this example the interoperability of PyANSYS with other open source tools such as ``gmsh`` is shown.
For that purpose, using ``gmsh`` we import an external geometry file in STL format. 
The geometry is imported then to PyANSYS using PyANSYS Reader.

This example is composed of several files. 

* ``gmsh_converter.py``: In this file, the STL file is converted to the gmsh file format. 
* ``mesh_converter``: In this file, the mesh file in gmsh format is converted to ANSYS CDB database format file. 
* ``modal_analysis.py``: Import CDB database, setup the modal analysis and run it. It also shows an animation of the first mode and save it to a gif file called ``animation.gif``. 


Requirements
------------
You need to have ``gmsh`` installed. You can install it using PIP:

.. code-block:: 

    pip install gmsh


Source code
-----------

`gmsh_generator.py` file:

.. literalinclude:: gmsh_generator.py
    :linenos:
    :language: python


`mesh_converter.py` file:

.. literalinclude:: mesh_converter.py
    :linenos:
    :language: python


`modal_analysis.py` file:

.. literalinclude:: modal_analysis.py
    :linenos:
    :language: python



Notes
-----

It is recommended to copy all the files in a separate folder. 
