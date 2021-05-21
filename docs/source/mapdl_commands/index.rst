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

   session/run_controls
   session/processor_entry
   session/files
   session/list_controls


********
Database
********

These commands are used to operate on the database in a global
sense.

.. toctree::
   :maxdepth: 1

   database/setup
   database/selecting
   database/components
   database/working_plane
   database/coord_sys
   database/picking

..
   Graphics - N/A Not Documented

****
APDL
****
These commands make up the ANSYS Parametric Design Language
(APDL).

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

These commands are used to create and set up the model.


.. toctree::
   :maxdepth: 1

   prep7/database
   prep7/element_type
   prep7/real_constants
   prep7/materials
   prep7/material_data_tables

   ..
      Left off here

   prep7/primitives
   prep7/keypoints
   prep7/hard_points
   prep7/lines
   prep7/areas
   prep7/volumes
   prep7/booleans
   prep7/meshing
   prep7/nodes
   prep7/elements
   prep7/superelements
   prep7/digitizing
   prep7/coupled_dof
   prep7/constraint_equations
   prep7/status
   prep7/explicit_dynamics
   prep7/sections
   prep7/morphing
   prep7/artificially_matched_layers
   prep7/special_purpose


********
Solution
********
These commands are used to load and solve the model.

.. toctree::
   :maxdepth: 1

   solution/analysis_options
   solution/nonlinear_options
   solution/dynamic_options
   solution/spectrum_options
   solution/load_step_options
   solution/solid_constraints
   solution/solid_forces
   solution/solid_surface_loads
   solution/solid_body_loads
   solution/inertia
   solution/miscellaneous_loads
   solution/load_step_operations
   solution/master_dof
   solution/gap_conditions
   solution/rezoning
   solution/2d_to_3d_analysis
   solution/birth_and_death
   solution/fe_constraints
   solution/fe_forces
   solution/fe_surface_loads
   solution/fe_body_loads
   solution/ocean
   solution/solution_status
   solution/explicit_dynamics
   solution/radiosity
   solution/multi_field_solver_definition_commands
   solution/multi_field_solver_global_controls
   solution/multi_field_solver_time_controls
   solution/multi_field_solver_load_transfer
   solution/multi_field_solver_convergence_controls
   solution/multi_field_solver_interface_mapping
   
*****
POST1
*****
These commands are used to postprocess the results with the database processor.

   post1/setup
   post1/controls
   post1/results
   post1/element_table
   post1/listing
   post1/animation
   post1/path_operations
   post1/surface_operations
   post1/load_case
   post1/magnetics_calc
   post1/trace_points
   post1/special
   post1/status
   post1/failure_criteria
