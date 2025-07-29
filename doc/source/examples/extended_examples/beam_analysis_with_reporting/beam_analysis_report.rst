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
* Distributed load application using nodal forces
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

We analyze a simply supported I-beam with the following characteristics:

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

Model Setup and Parameterization
=================================

The example begins by defining all analysis parameters in dictionaries for easy
modification and reuse:

.. literalinclude:: ../examples/00-mapdl-examples/beam_with_report.py
    :language: python
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

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Define element type
    :end-at: mapdl.keyopt(1, 6, 1)

Cross-Section Definition
------------------------

The I-beam cross-section is defined using PyMAPDL's section commands:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Define I-beam cross-section
    :end-at: beam_params["web_thickness"]/10

The ``SECDATA`` command defines the I-beam geometry where:

* First two parameters: top and bottom flange widths
* Third parameter: total beam height
* Fourth and fifth parameters: flange thicknesses  
* Sixth parameter: web thickness

Node and Element Generation
---------------------------

Nodes are created along the beam length with uniform spacing:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Create nodes along the beam length
    :end-at: mapdl.e(i + 1, i + 2)

The mesh uses 20 elements along the beam length, providing sufficient resolution
for accurate results while maintaining computational efficiency.

Boundary Conditions and Loading
===============================

Simply Supported Conditions
----------------------------

Simply supported boundary conditions are implemented as:

* **Left support (Pin):**
  Constrains vertical (UY), out-of-plane (UZ), and rotational degrees of freedom
* **Right support (Roller):**
  Same constraints as pin, but allows horizontal movement

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Apply simply supported boundary conditions
    :end-at: mapdl.d(last_node, "ROTZ", 0)

Distributed Load Application
----------------------------

The uniformly distributed load is applied as equivalent nodal forces:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Apply distributed load as nodal forces
    :end-at: mapdl.f(last_node, "FY", end_nodal_force)

This approach:

* Converts the continuous load to discrete nodal forces
* Maintains load equilibrium
* Provides accurate representation of the distributed loading

Solution Process
================

The static structural solution is configured and executed:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
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

The maximum displacement is extracted and compared with analytical theory:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Get nodal displacements
    :end-at: max_displacement_location = np.argmin(displacements[:, 1]) + 1

Theoretical Verification
------------------------

Results are verified against classical beam theory:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: # Theoretical maximum displacement
    :end-at: theoretical_stress = (theoretical_moment * c) / I

**Key formulas used:**

* **Maximum displacement:** :math:`\delta_{max} = \frac{5wL^4}{384EI}`
* **Maximum moment:** :math:`M_{max} = \frac{wL^2}{8}`
* **Maximum stress:** :math:`\sigma_{max} = \frac{Mc}{I}`

Where:

- :math:`w` = distributed load intensity
- :math:`L` = beam span
- :math:`E` = elastic modulus
- :math:`I` = moment of inertia
- :math:`c` = distance to extreme fiber

Section Property Calculations
=============================

The example includes a function to calculate I-beam section properties:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: def calculate_moment_of_inertia(beam_params):
    :end-at: }

This function calculates:

* Cross-sectional area
* Moment of inertia about the strong axis
* Section modulus
* Centroidal properties

The calculations use composite section analysis principles, considering the
I-beam as two flanges plus a web.

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

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
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

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
    :start-at: def generate_word_report(data, output_dir):
    :end-at: return str(word_file)

**Note:** Word report generation requires the ``python-docx`` package:

.. code-block:: bash

   pip install python-docx

Plot Generation
---------------

The example includes functionality to generate analysis plots:

.. literalinclude:: ../../../examples/00-mapdl-examples/beam_with_report.py
    :language: python
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
       {"name": "Service Load", "magnitude": -50.0},
       {"name": "Ultimate Load", "magnitude": -75.0},
       {"name": "Wind Load", "magnitude": -25.0},
   ]

   for case in load_cases:
       # Run analysis for each case
       # Generate separate reports
       pass

Design Optimization
-------------------

The parameterized approach enables design optimization studies:

.. code-block:: python

   # Optimization loop
   for height in range(300, 600, 50):  # Test different heights
       beam_params["web_height"] = height
       results = create_ibeam_analysis_and_report()
       # Evaluate design criteria

Expected Results
================

When running this example, you should expect:

**Displacement Results:**

- Maximum displacement: ~40-50 mm at mid-span
- Excellent agreement with theory (< 1% error)
- Smooth displacement profile along beam length

**Stress Results:**

- Maximum stress: ~150-200 MPa at extreme fibers
- Safety factor: ~2-3 against yielding
- Linear stress distribution through beam height

**Model Validation:**

- Finite element results match analytical predictions
- Mesh convergence demonstrates adequate discretization
- Boundary conditions properly represent support conditions

**Report Quality:**

- Professional formatting and presentation
- Complete documentation of analysis process
- Tables, figures, and calculations clearly presented

Troubleshooting
===============

Common Issues and Solutions
---------------------------

**MAPDL License Issues:**

If you encounter licensing problems:

.. code-block:: python

   # Use student version if available
   mapdl = launch_mapdl(mode="grpc", version=231)

**Plot Generation Errors:**

If plots fail to generate:

.. code-block:: python

   # Check graphics capabilities
   mapdl = launch_mapdl(additional_switches="-grpc")

**Missing Dependencies:**

Install required packages:

.. code-block:: bash

   pip install numpy python-docx matplotlib

**File Permission Errors:**

Ensure write permissions for output directory:

.. code-block:: python

   import os

   os.chmod("beam_analysis_output", 0o755)

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

**Buckling Analysis:**

.. code-block:: python

   # Linear buckling
   mapdl.antype("BUCKLE")
   mapdl.bucopt("LANB", 5)  # First 5 modes

Additional Report Features
--------------------------

**PDF Generation:**

.. code-block:: python

   # Convert Markdown to PDF using pandoc
   import subprocess

   subprocess.run(["pandoc", "report.md", "-o", "report.pdf"])

**Email Reports:**

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

* Ansys Mechanical APDL Element Reference
* "Formulas for Stress and Strain" by Roark and Young
* "Theory of Plates and Shells" by Timoshenko and Woinowsky-Krieger
* PyMAPDL Documentation: https://mapdl.docs.pyansys.com/

.. note::
   This example requires PyMAPDL 0.60+ and a valid Ansys license.
   For optimal report generation, install python-docx: ``pip install python-docx``