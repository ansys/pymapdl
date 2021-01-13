PyMapdl Documentation
=====================

Introduction and Purpose
------------------------
The ``ansys-mapdl-core`` module, under the ``PyAnsys`` development
project, is a Python module that allows you to interface with MAPDL
using Python.  This module provides:

- Low and high level scripting of MAPDL through both basic text
  commands and python commands.
- Plotting of MAPDL geometry and meshes using VTK from within a Python
  or jupyterlab environment.
- Access MAPDL arrays as Python objects (e.g. nodes, elements,
  internal arrays, results from MAPDL post-processing)

Ansys MAPDL allows for the direct scripting of structural analysis
problems through input files.  Unfortunately, MAPDL relies on an
legacy scripting language that can be difficult to read and control
and either requires the MAPDL GUI for an interactive session or a
basic text interface through a batch session.

The weaknesses of this language are often compensated by generating
APDL scripts using a secondary scripting tool like ``MATLAB`` or
``Python``.  However, this added layer of complexity means that the
development feedback loop is quite long as the user must export and
run an entire script before determining if it ran correctly or of the
results are valid.  This module seeks to rectify that by providing a
high level interface to script MAPDL.


Background
----------
ANSYS already has a method of interfacing with MAPDL through the use
of CORBA.  This interface allows you to send strings from the client
to the mapdl instance and run commands from a scripting software (such
as Python or MATLAB).  The ``PyMAPDL`` project using the
``ansys-mapdl-core`` module is an attempt to enhance this interface
through the use of an alternative protocol, GRPC.

Google remote procedure call or GRPC, establishes a secure connection
between a client and a server instance (either local or remote). A
client application can directly call methods on a remote application
as if it was a local object.  This GRPC interface is established by:

 - Define a service in a .proto file
 - Generate server and client code using the protocol buffer compiler
 - Create the server application, implementing the generated service
   interfaces and spawning the gRPC server
 - Create the client application, making RPC calls using generated
   stubs

The ``ansys-mapdl-core`` module bridges the gap between the GRPC client and
the user with an object oriented interface that should be both
familiar with established MAPDL coders unfamiliar with Python, and
Python programmers unfamiliar with MAPDL.


.. toctree::
   :hidden:

   getting_started/index
   user_guide/index
   api/index
   examples/index
   contributing


Project Index
-------------
* :ref:`genindex`
