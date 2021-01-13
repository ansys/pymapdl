PyMAPDL Documentation
=====================

Introduction and Purpose
------------------------
PyMAPDL is part of the larger PyAnsys effort to facilitate the use 
of Ansys technologies directly from Python. Its primary package,
``ansys-mapdl-core``, provides:

- scripting of MAPDL through both Python and Ansys Parametric Design
  Language (APDL) syntax
- plotting of MAPDL geometry and meshes using VTK from within a Python
  script or an interactive Jupyter notebook
- access to MAPDL arrays as Python objects (e.g. nodes, elements,
  solution matrices, and results)

With PyMAPDL it is easier than ever to integrate the simulation capabilities 
of the Ansys MAPDL multi-physics solver direcly into novel applications 
thanks to an API that will look familiar to APDL and Python users alike.
The package presents a Python-friendly interface to drive the software
that manages the submission of low-level APDL commands, while exchanging
data through high-performance gRPC interfaces.

Accelerate the preparation of your simulations using PyMAPDL. Combine the
expressiveness of general-purpose Python code to control the flow in your
input decks with methods that drive the solver. Explore proof of concept 
studies or capture knowledge using interactive Jupyter notebooks.  Tap
the solver as the physics engine in your next Artificial Intelligence
application. It is now open source: Enjoy it! Contributions are welcome.


Background
----------
PyMAPDL, based on gRPC, represents an improvement over its predecessor based
on CORBA. These technologies allow the MAPDL solver to function as a server, 
ready to respond to connecting clients.  

Google remote procedure calls, or gRPC, are used to establish secure 
connections so that a client application can directly call methods on 
a potentially remote MAPDL instance as if it were a local object. The 
use of HTTP/2 makes it friendly to modern internet infrastructures. 
This, along with the use of binary transmission formats, favors higher
performance. Using gRPC, PyMAPDL can convert Python statements into APDL 
commands that can then be transmitted to an MAPDL instance running anywhere, 
while producing network footprints that are compact and efficient.

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
