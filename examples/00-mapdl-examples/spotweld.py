"""
.. _ref_spotweld:

Running an input file - spotweld SHELL181 example
=================================================

This MAPDL example demonstrates how to model spot welding on three
thin sheets of metal. Here, the full input file is simply run using
the PyMAPDL interface.

Using the following commands, you can directly use an APDL
script within a PyMAPDL session with the following
commands:

"""

##############################################################################
# Script initialization
# ---------------------

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

##############################################################################
# Upload and run an MAPDL script.

if mapdl.is_local:
    mapdl.upload("./spotweld/spot_weld.inp")
    mapdl.input("spot_weld.inp")
else:
    mapdl.input("./spotweld/spot_weld.inp")

######################################################################
# Displacements
# -------------

# Enter post-processor
mapdl.post1()

# Plot the time step 1.
mapdl.set(1, 1)
mapdl.post_processing.plot_nodal_displacement(cmap="bwr")

# Plot the time step 3.
mapdl.set(1, 3)
mapdl.post_processing.plot_nodal_displacement(cmap="bwr")


######################################################################
# Stress
# ------

# Get the nodal and element component stress at time step 1.
mapdl.set(1, 1)
nodal_stress = mapdl.post_processing.nodal_stress_intensity()
print("Nodal stress : ", nodal_stress)

# Plot the element stress.
element_stress = mapdl.post_processing.element_stress("int")
print("Element stress : ", element_stress)

######################################################################
# The stress at the contact element simulating the spot weld.
#
# Plot the nodal stress in the Z direction.
mapdl.post_processing.plot_nodal_component_stress("z")


######################################################################
# Get the cumulative equivalent stress and plot the von Mises stress.

eqv_stress = mapdl.post_processing.nodal_eqv_stress()
print("Cumulative equivalent stress : ", eqv_stress)
mapdl.post_processing.plot_nodal_eqv_stress()

###############################################################################
# Stop MAPDL
#
mapdl.finish()
mapdl.exit()
