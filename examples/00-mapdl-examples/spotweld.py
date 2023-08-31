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

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
if mapdl.is_local:
    mapdl.upload("./spotweld/spot_weld.inp")
    mapdl.input("spot_weld.inp")
else:
    mapdl.input("./spotweld/spot_weld.inp")

######################################################################
# Open the result file
# --------------------

# access the result from the mapdl result
result = mapdl.result


######################################################################
# Displacements
# -------------
# Plot the time step 1 and 3.

result.plot_nodal_solution(0)
result.plot_nodal_solution(2)

######################################################################
# Stress
# ------

# Get the nodal and element component stress at time step 1.
nodenum, stress = result.nodal_stress(0)

# Plot the element stress.
element_stress, elemnum, enode = result.element_stress(0)

######################################################################
# The stress at the contact element simulating the spot weld.
#
# Plot the nodal stress in the Z direction.
result.plot_nodal_stress(0, "z")


######################################################################
# Get the principal nodal stress and plot the von Mises stress.

nnum, pstress = result.principal_nodal_stress(0)
result.plot_principal_nodal_stress(0, "SEQV")

###############################################################################
# Stop MAPDL
#
mapdl.finish()
mapdl.exit()
