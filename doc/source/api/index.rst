.. _ref_index_api:

=============
API Reference
=============
This section gives an overview of the API of several public PyMAPDL
classes, functions, and attributes.

These methods may include some MAPDL commands but are generally
specific to pymapdl specific methods and classes (i.e. methods that
extend existing MAPDL methods in a pythonic manner).  For classic
MAPDL commands mapped to PyMAPDL, see :ref:`ref_mapdl_commands`.


.. toctree::
   :maxdepth: 2

   mapdl
   math
   plotting
   helper

.. currentmodule:: ansys.mapdl.core


Mesh
====
.. _mesh_api:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   mesh_grpc.MeshGrpc


Database Explorer
=================
.. _xpl_api:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   xpl.ansXpl


Geometry
========
.. _geometry_api:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   mapdl_geometry.Geometry


Parameters
==========
.. _parameters_api:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   parameters.Parameters


Plotting
========
.. _plotting_api:

Various PyMAPDL specific plotting commands.

.. autosummary::
   :toctree: _autosummary

   plotting.general_plotter
   Mapdl.aplot
   Mapdl.eplot
   Mapdl.kplot
   Mapdl.lplot
   Mapdl.nplot
   Mapdl.vplot


Local MAPDL Pool
================
.. _pool_api:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   pool.LocalMapdlPool


Post-Processing
===============
.. _post_api:

This class contains an API to post-process directly from MAPDL.
Should you wish to post-process MAPDL result files outside of PyMAPDL,
you can use one of the following packages:

* `DPF-Core <https://dpfdocs.pyansys.com/>`_ : Post-Processing using the Data Processing Framework (DPF).  More complex yet and more powerful post-processing APIs.
* `DPF-Post <https://postdocs.pyansys.com/>`_ : Streamlined and simplified DPF Post Processing.  Higher level package and uses ``DPF-Core``.
* `Legacy PyMAPDL Reader <https://readerdocs.pyansys.com/>`_: Legacy result file reader.  Supports result files from MAPDL v14.5 to the current release.

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   pool.LocalMapdlPool


Solution
========
.. _solution_api:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   solution.Solution

