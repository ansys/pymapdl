pyansys
=======

This Python module allows you to to extract data from ANSYS files and to display
them if VTK is installed.  Currently supports result (.rst), mass and 
stiffness (.full), and block archive (.cdb) files.
 

.. image:: hexbeam_disp.png

Contents
========

.. toctree::
   :maxdepth: 2
   
   examples
   loading_results

Installation
------------

Installation through pip::

    pip install pyansys

You can also visit `PyPi <http://pypi.python.org/pypi/pyansys>`_ or 
`GitHub <https://github.com/akaszynski/pyansys>`_ to download the source.

Dependencies: ``numpy``, ``cython``, ``vtkInterface``. Optional: ``vtk``

Minimum requirements are numpy to extract results from a results file. To
convert the raw data to a VTK unstructured grid, VTK 5.0 or greater must
be installed with Python bindings.



License
-------

This module, pyansys is licensed under the MIT license.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
