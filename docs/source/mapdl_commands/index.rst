.. _ref_mapdl_commands:

==============
MAPDL Commands
==============
This section gives an overview of the classic MAPDL commands that have
been wrapped pythonically via PyMapdl.  Not all commands have been
wrapped, most notably there are a variety of commands that are not
supported natively or only have partial support within PyMAPDL.  

*******
Session
*******
These commands provide general control to the session. The commands
are grouped by functionality.

.. toctree::
   :maxdepth: 1

   run_controls
   processor_entry
   files
   list_controls

..
   Database - TODO

..
   Graphics - N/A Not Documented

****
APDL
****
These commands make up the ANSYS Parametric Design Language
(APDL). The commands are grouped by functionality.

.. toctree::
   :maxdepth: 1

   apdl/parameter_definition
   apdl/macro_files
   apdl/abbreviations
   apdl/array_parm
   apdl/matrix_op


*************
Preprocessing
*************

These commands are used to create and set up the model. The commands
are grouped by functionality.


.. toctree::
   :maxdepth: 1

   database
   element_type
   real_constants
   materials
   material_data_tables

   ..
      Left off here

   primitives
   keypoints
   hard_points
   lines
   areas
   volumes
   booleans
   meshing
   nodes
   elements
   superelements
   digitizing
   coupled_dof
   constraint_equations
   status
   explicit_dynamics
   sections
   morphing
   artificially_matched_layers
   special_purpose


********
Solution
********
These commands are used to load and solve the model. The commands are
grouped by functionality.

.. toctree::
   :maxdepth: 1

   analysis_options
   nonlinear_options
   dynamic_options
   spectrum_options
   load_step_options
   solid_constraints
   solid_forces
   solid_surface_loads
   solid_body_loads
   inertia
   miscellaneous_loads
   load_step_operations
   master_dof
   gap_conditions
   rezoning
   2d_to_3d_analysis
   birth_and_death
   fe_constraints
   fe_forces
   fe_surface_loads
   fe_body_loads
   ocean
   solution_status
   explicit_dynamics
   radiosity
   multi_field_solver_definition_commands
   multi_field_solver_global_controls
   multi_field_solver_time_controls
   multi_field_solver_load_transfer
   multi_field_solver_convergence_controls
   multi_field_solver_interface_mapping
   

..
   Miscellaneous
