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


Mapdl Class Specific Classes or Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. currentmodule:: ansys.mapdl.core

.. autoclass:: ansys.mapdl.core.mapdl._MapdlCore

.. autosummary::
   :toctree: _autosummary

   Mapdl.add_file_handler
   Mapdl.allow_ignore
   Mapdl.chain_commands
   Mapdl.directory
   Mapdl.geometry
   Mapdl.get
   Mapdl.get_array
   Mapdl.get_value
   Mapdl.ignore_errors
   Mapdl.jobname
   Mapdl.last_response
   Mapdl.load_table
   Mapdl.mesh
   Mapdl.modal_analysis
   Mapdl.open_apdl_log
   Mapdl.open_gui
   Mapdl.parameters
   Mapdl.result
   Mapdl.run
   Mapdl.run_multiline
   Mapdl.set_log_level
   Mapdl.version

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   xpl.ansXpl
   mapdl_geometry.Geometry
   parameters.Parameters
   pool.LocalMapdlPool
   post.PostProcessing
   solution.Solution


MapdlMath Class Specific Classes or Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These classes are specific to the ``MapdlMath`` module:

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst

   math.MapdlMath
   math.ApdlMathObj
   math.AnsVec
   math.AnsMat
   math.AnsSolver


Plotting
~~~~~~~~
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


Helper Functions
~~~~~~~~~~~~~~~~
These methods simplify launching MAPDL, converting existing scripts,
or automating other tasks.

.. autosummary::
   :toctree: _autosummary

   convert_script
   launch_mapdl
