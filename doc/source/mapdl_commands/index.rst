.. _ref_mapdl_commands:

.. toctree::
   :maxdepth: 1
   :hidden:
   :glob:

   *


==============
MAPDL commands
==============
This section gives an overview of the classic MAPDL commands that have
been wrapped pythonically via PyMAPDL. Most commands have been
wrapped, but there are a few commands that are not supported natively
or only have partial support within PyMAPDL.  See
:ref:`ref_unsupported_commands` for more details.

*******
Session
*******
These commands provide general control to the session. The commands
are grouped by capability.

.. toctree::
   :maxdepth: 1
   :glob:

   session/*


********
Database
********
These commands are used to operate on the database globally.

.. toctree::
   :maxdepth: 1
   :glob:

   database/*

********
Graphics
********
These commands are used to control the graphics of the program.

.. toctree::
   :maxdepth: 1
   :glob:

   graphics/*


****
APDL
****
These commands make up the ANSYS Parametric Design Language
(APDL).

.. toctree::
   :maxdepth: 1
   :glob:

   apdl/*

.. _ref_prep_commands:

*************
Preprocessing
*************

These commands are used to create and set up the model.


.. toctree::
   :maxdepth: 1
   :glob:

   prep7/*


********
Solution
********
These commands are used to load and solve the model.

.. toctree::
   :maxdepth: 1
   :glob:

   solution/*
   
*****
POST1
*****
These commands are used to postprocess the results with the database
processor.

.. toctree::
   :maxdepth: 1
   :glob:

   post1/*

******
POST26
******
These commands are used to postprocess the results with the
time-history processor.

.. toctree::
   :maxdepth: 1
   :glob:

   post26/*


****
AUX2
****
These commands are used to examine or manipulate the contents of
binary files produced by the program.

.. toctree::
   :maxdepth: 1
   :glob:

   aux2/*


****
AUX3
****
The auxiliary processor ``/AUX3`` allows you to operate on results
files by deleting sets or by changing values.

.. toctree::
   :maxdepth: 1
   :glob:

   aux3


*****
AUX12
*****
These commands are used to define radiation options for use in thermal
analyses.

.. toctree::
   :maxdepth: 1
   :glob:

   aux12/*


*****
AUX15
*****
These commands are used to read in an IGES file for analysis in ANSYS.

.. toctree::
   :maxdepth: 1
   :glob:

   aux15


*****************
Mapping processor
*****************
The ``/MAP`` processor allows you to map data from an external file
onto the existing geometry.

.. toctree::
   :maxdepth: 1
   :glob:

   map


***************
DISPLAY program
***************
These commands are used for the DISPLAY program. The DISPLAY program
is a companion program to ANSYS, used for recovering graphics displays
produced within ANSYS.

.. note::
   Many of these commands are not applicable when using PyMAPDL.

.. toctree::
   :maxdepth: 1
   :glob:

   display/*


**********************
REDUCED order modeling
**********************
These commands are used for the DISPLAY program. The DISPLAY program
is a companion program to ANSYS, used for recovering graphics displays
produced within ANSYS.

.. toctree::
   :maxdepth: 1
   :glob:

   reduced/*

*******************
Connection commands
*******************

These commands read in external CAD files into MAPDL.

.. toctree::
   :maxdepth: 1
   :glob:

   conn


**********************
Miscellaneous commands
**********************

Undocumented miscellaneous commands.

.. toctree::
   :maxdepth: 1
   :glob:

   misc


*****************************
Undocumented inquire commands
*****************************

Undocumented inquire commands.

.. warning:: 
   **DISCLAIMER**: 
   This function is un-documented in the official ANSYS Command Reference Guide.
   Hence its support is limited and it use is not encouraged.
   **Please use it with caution.**


.. toctree::
   :maxdepth: 1
   :glob:

   inqfun
