"""
.. _ref_spotweld:

=================================================
Running an input file - spotweld SHELL181 example
=================================================

This MAPDL example demonstrates how to model spot welding on three
thin sheets of metal. Here, the full input file is simply run using
the PyMAPDL interface.

Using the following commands, you can directly use an APDL
script within a PyMAPDL session with the following
commands:

"""

import os

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
if mapdl._local:
    mapdl.upload("./spotweld/spot_weld.inp")
    mapdl.input("spot_weld.inp")
else:
    mapdl.input("./spotweld/spot_weld.inp")

######################################################################
# Here is the Python script using
# `ansys-mapdl-reader <legacy_reader_docs_>`_ package to access
# the results after running the MAPDL analysis.

from ansys.mapdl import reader as pymapdl_reader

######################################################################
# Open the result file and plot the displacement of time step 3

resultfile = os.path.join(mapdl.directory, "file.rst")
result = pymapdl_reader.read_binary(resultfile)
result.plot_nodal_solution(2)


######################################################################
# Get the nodal and element component stress at time step 0. Plot the
# stress in the Z direction.

nodenum, stress = result.nodal_stress(0)
element_stress, elemnum, enode = result.element_stress(0)


######################################################################
# Plot the Z direction stress:
# The stress at the contact element simulating the spot weld
result.plot_nodal_stress(0, "z")


######################################################################
# Get the principal nodal stress and plot the von Mises stress

nnum, pstress = result.principal_nodal_stress(0)
result.plot_principal_nodal_stress(0, "SEQV")

###############################################################################
# Stop MAPDL
#
mapdl.finish()
mapdl.exit()
