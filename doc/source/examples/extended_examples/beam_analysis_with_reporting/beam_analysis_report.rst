.. _beam_analysis_report_example:

================================================
I-Beam Analysis with Automated Report Generation
================================================

This comprehensive example demonstrates how to perform a complete structural analysis
of an I-beam using PyMAPDL and automatically generate detailed engineering reports.
The example showcases advanced PyMAPDL capabilities including parameterized modeling,
result extraction, and automated documentation generation.

**What this example demonstrates:**

* Parameterized I-beam geometry creation
* Material property definition and assignment
* Simply supported boundary condition implementation
* Distributed load applied using nodal forces
* Comprehensive result extraction and post-processing
* Automated report generation in Markdown and Word formats
* Analytical verification of finite element results

Introduction
============

Engineering analysis often requires not just obtaining results, but also documenting
the analysis process, assumptions, and findings in a professional report format.
This example shows how PyMAPDL can be used to create a complete analysis workflow
that includes automated report generation.

The analysis focuses on a simply supported I-beam subjected to an uniformly distributed
load, a fundamental structural engineering problem. The results are verified against
analytical solutions and presented in professional report formats.

Problem Definition
==================

Analyze a simply supported I-beam with the following characteristics:

**Geometry:**

- Length: 5.0 meters
- I-section with typical structural steel proportions
- Clamped at both ends

**Loading:**

- Uniformly distributed load of 50 kN/m (downward)
- Static analysis (no dynamic effects)

**Material:**

- Structural steel (S355 grade)
- Linear elastic behavior assumed

**Objectives:**

- Determine maximum displacement and location
- Calculate maximum bending stress
- Verify safety against yielding
- Generate comprehensive documentation

Model Setup and Parametrisation
===============================

The example begins by defining all analysis parameters in dictionaries for easy
modification and reuse:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # I-beam geometric parameters
    :end-at: print(f"Load: {load_params['distributed_load']} N/mm")

This parameterized approach allows for:

* Easy modification of beam dimensions
* Material property changes
* Load case variations
* Design optimization studies

Preprocessing - Geometry and Meshing
====================================

Element Type Selection
----------------------

The analysis uses BEAM188 elements, which are:

* 3D linear finite strain beam elements
* Suitable for thin to moderately thick beam structures
* Capable of handling large deflection effects (if needed)
* Provide comprehensive stress output

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Define element type
    :end-at: mapdl.keyopt(1, 6, 1)

Cross-Section Definition
------------------------

The I-beam cross-section is defined using PyMAPDL's section commands:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: print(f"\n-- Setting MAPDL section properties --")
    :end-at: print(beam_info)

The ``SECDATA`` command defines the I-beam geometry where:

* First two parameters: top and bottom flange widths
* Third parameter: total beam height
* Fourth and fifth parameters: flange thicknesses  
* Sixth parameter: web thickness

Node and Element Generation
---------------------------

Nodes are created along the beam length with uniform spacing:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Create nodes along the beam length
    :end-at: mapdl.e(i + 1, i + 2)

The mesh uses 20 elements along the beam length, providing sufficient resolution
for accurate results while maintaining computational efficiency.

Boundary Conditions and Loading
===============================

Fully Constrained End Conditions
--------------------------------

Fully clamped boundary conditions on the ends are implemented as:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Apply simply supported boundary conditions
    :end-at: mapdl.d(last_node, "ROTZ", 0)

Distributed Load Application
----------------------------

The uniformly distributed load is applied as equivalent nodal forces:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Apply distributed load as nodal forces
    :end-at: mapdl.f(last_node, "FY", end_nodal_force)

This approach:

* Converts the continuous load to discrete nodal forces
* Maintains load equilibrium
* Provides accurate representation of the distributed loading

Alternatively, the load can be applied using the ``SFBEAM`` command for surface loads on BEAM and PIPE elements.

Solution Process
================

The static structural solution is configured and executed:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Enter solution processor
    :end-at: print("Solution completed successfully")

The solution uses:

* Static analysis type (no time-dependent effects)
* Linear analysis (small deflection theory)
* Direct solver for optimal accuracy

Post-Processing and Result Extraction
=====================================

Displacement Results
--------------------

The maximum displacement is extracted using the `post_processing` module:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Get nodal displacements
    :end-at: max_displacement_location = np.argmin(displacements) + 1

Moment Results
--------------

The Moment at both nodes are extracted using ``ETABLE`` command, with ``SMISC`` items:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Get moment values
    :end-at: max_moment_fem = max(max_moment_i, max_moment_j)

Bending Stress Results
----------------------

Again we use ``ETABLE`` to retrieve MAPDL values:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Get bending stress values
    :end-at: max_moment_fem = max(max_moment_i, max_moment_j)

Bending Strain Results
----------------------

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: # Get bending strain values
    :end-at: max_strain_fem = max(bending_strain_top, bending_strain_bottom)

Report Generation Features
==========================

Markdown Report
---------------

The Markdown report includes:

* Executive summary with key results
* Detailed model description with parameter tables
* Comprehensive results presentation
* Analytical verification section
* Professional formatting with tables and equations

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: def generate_markdown_report(data, output_dir):
    :end-at: return str(report_file)

Word Document Report
--------------------

The Word report provides:

* Professional document formatting
* Tables for organized data presentation
* Structured sections and headings
* Executive summary format

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: def generate_word_report(data, output_dir):
    :end-at: return str(word_file)

**Note:** Word report generation requires the ``python-docx`` package:

.. code-block:: bash

   pip install python-docx

Plot Generation
---------------

The example includes capability to generate analysis plots:

.. literalinclude:: ../../../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :dedent: 4
    :start-at: def generate_analysis_plots(mapdl, output_dir):
    :end-at: return plot_files

Generated plots include:

* Displacement contours showing deformed shape
* Stress contours highlighting critical regions
* Node and element plots for model verification

Running the Example
===================

Basic Execution
---------------

To run the complete analysis and generate reports:

.. code-block:: python

   from beam_with_report import create_ibeam_analysis_and_report

   # Run complete analysis
   results = create_ibeam_analysis_and_report()

Or execute the script directly:

.. code-block:: bash

   python beam_with_report.py

Output Files
------------

The analysis generates several output files in the ``beam_analysis_output`` directory:

* ``ibeam_analysis_report.md`` - Markdown report
* ``ibeam_analysis_report.docx`` - Word document
* ``displacement_plot.png`` - Displacement visualization
* ``stress_plot.png`` - Stress visualization

Customization Options
=====================

Parameter Modification
----------------------

Easily modify analysis parameters by changing the dictionaries:

.. code-block:: python

   # Modify beam dimensions
   beam_params["length"] = 8000.0  # Change to 8 meters
   beam_params["web_height"] = 500.0  # Increase height

   # Change material
   material_props["elastic_modulus"] = 200000.0  # Different steel grade

   # Modify loading
   load_params["distributed_load"] = -75.0  # Increase load intensity

Multiple Load Cases
-------------------

The framework can be extended for multiple load cases:

.. code-block:: python

   load_cases = [
       {"name": "Service Load", "distributed_load": -50.0},
       {"name": "Ultimate Load", "distributed_load": -75.0},
       {"name": "Wind Load", "distributed_load": -25.0},
   ]

   for case in load_cases:
       # Run analysis for each case
       # Generate separate reports
       results = create_ibeam_analysis_and_report(**case)

This parameterized approach enables design optimization studies:


Expected Results
================

When running this example, you should expect:

**Displacement Results:**

- Maximum displacement: ~40-50 mm at mid-span
- Smooth displacement profile along beam length

**Stress Results:**

- Maximum stress: ~150-200 MPa at extreme fibers
- Safety factor: ~2-3 against yielding
- Linear stress distribution through beam height

**Model Validation:**

- Finite element results match analytical predictions
- Mesh convergence demonstrates adequate discretisation
- Boundary conditions properly represent support conditions

**Report Quality:**

- Professional formatting and presentation
- Complete documentation of analysis process
- Tables, figures, and calculations clearly presented


Extensions and Modifications
============================

Advanced Analysis Options
--------------------------

The example can be extended for more sophisticated analyses:

**Nonlinear Analysis:**

.. code-block:: python

   # Enable geometric nonlinearity
   mapdl.nlgeom("ON")

   # Material nonlinearity
   mapdl.mp("BISO", 1, yield_strength, hardening_modulus)

**Dynamic Analysis:**

.. code-block:: python

   # Modal analysis
   mapdl.antype("MODAL")
   mapdl.modopt("LANB", 10)  # First 10 modes


Additional Report Features
--------------------------

**PDF Generation:**

.. code-block:: python

   # Convert Markdown to PDF using pandoc
   import subprocess

   subprocess.run(
       ["pandoc", "ibeam_analysis_report.md", "-o", "ibeam_analysis_report.pdf"]
   )

**email Reports:**

.. code-block:: python

   import smtplib
   from email.mime.multipart import MIMEMultipart
   from email.mime.base import MIMEBase

   # Send reports via email
   # Implementation details...

**Database Storage:**

.. code-block:: python

   import sqlite3

   # Store results in database
   conn = sqlite3.connect("analysis_results.db")
   # Insert results...

Conclusion
==========

This example demonstrates a complete PyMAPDL workflow that goes beyond simple
analysis to include professional documentation and reporting. The combination of:

* Parameterized modeling
* Comprehensive result extraction  
* Analytical verification
* Automated report generation

provides a foundation for developing robust engineering analysis tools and
workflows using PyMAPDL.

The approach shown here can be adapted for various structural analysis problems
and extended with additional features as needed for specific engineering applications.

References
==========

* PyMAPDL Documentation: https://mapdl.docs.pyansys.com/
* Ansys Mechanical APDL Element Reference

.. note::
   This example requires PyMAPDL 0.60+ and a valid Ansys license.