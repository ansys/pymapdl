r"""
.. _ref_vm6_example:

Pinched Cylinder
----------------
Problem Description:
 - A thin-walled cylinder is pinched by a force :math:`F` at the middle
   of the cylinder length. Determine the radial displacement :math:`\delta`
   at the point where the force :math:`F` is applied.
   The ends of the cylinder are free edges.

Reference:
 - R. D. Cook, Concepts and Applications of Finite Element Analysis, 2nd Edition,
   John Wiley and Sons, Inc., New York, NY, 1981, pp. 284-287.
   H. Takemoto, R. D. Cook, "Some Modifications of an Isoparametric Shell
   Element", International Journal for Numerical Methods in Engineering, Vol.7
   No. 3, 1973.

Analysis Type(s):
 - Static Analysis ``ANTYPE=0``

Element Type(s):
 - 4-Node Finite Strain Shell Elements (SHELL181)
 - 8-Node Finite Strain Shell Elements (SHELL281)

.. image:: ../../_static/vm6_setup.png
   :width: 400
   :alt: VM6 Pinched Cylinder Problem Sketch

Material Properties
 - :math:`E = 10.5 \cdot 10^6 psi`
 :math:`Nu = 0.3125`

Geometric Properties:
 - :math:`l = 10.35  in`
 - :math:`r = 4.953  in`
 - :math:`t = 0.094  in`

Loading:
 - :math:`F = 100  lb`

Analysis Assumptions and Modeling Notes:
 - A one-eighth symmetry model is used. One-fourth of the load is applied
   due to symmetry.

"""
# sphinx_gallery_thumbnail_path = '_static/vm6_setup.png'

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~

from ansys.mapdl.core import launch_mapdl

# Start mapdl and clear it.
mapdl = launch_mapdl()
mapdl.clear()

# Enter verification example mode and the pre-processing routine.
mapdl.verify()
mapdl.prep7()


###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element type (a shell-type).

# Type of analysis: Static.
mapdl.antype("STATIC")

# Define element number.
elem_num = 1

# Element type: SHELL181.
mapdl.et(elem_num, "SHELL181")

# Special Features are defined by keyoptions of shell element:

# KEYOPT(3)
# Integration option:
# Full integration with incompatible modes.
mapdl.keyopt(elem_num, 3, 2)  # Cubic shape function


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material.

# Define material number.
mat_num = 1

# Define material properties.
mapdl.mp("EX", mat_num, 10.5E6)
mapdl.mp("NUXY", mat_num, 0.3125)
print(mapdl.mplist())


###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a shell element.

# Parametrization of the shell thickness.
t = 0.094

# Define cross-section number.
sec_num = 1

# Define shell cross-section.
mapdl.sectype(secid=sec_num, type_="SHELL", name="shell181")
mapdl.secdata(t, mat_num, 0, 5)


###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# Set up the keypoints and create the area through the keypoints.

# Define global cylindrical coordinate system.
mapdl.csys(1)

# Define keypoints by coordinates.
mapdl.k(1, 4.953)
mapdl.k(2, 4.953, "", 5.175)

# Generates additional keypoints from a pattern of keypoints.
mapdl.kgen(2, 1, 2, 1, "", 90)

# Create an area through keypoints.
mapdl.a(1, 2, 4, 3)

# Define the number of the keypoint where F is applied using inline function.
q = mapdl.queries
top_keypoint = q.kp(4.953, 90, 0)

# Plot the lines.
mapdl.lplot(color_lines=True, cpos='iso')

# Plot the area using PyVista properties.
mapdl.aplot(title="Display the selected area",
            cpos="iso",
            vtk=True,
            color="#06C2AC",
            show_line_numbering=True,
            show_area_numbering=True,
            show_lines=True)


###############################################################################
# Meshing
# ~~~~~~~
# Define line division of the lines, then mesh the area with shell elements.

# Specify the default number of line divisions.
mapdl.esize("", 8)

# Mesh the area.
mapdl.amesh(1)

# Define global cartesian coordinate system.
mapdl.csys(0)

# Plot the mesh.
mapdl.eplot(title="Plot the currently selected elements",
            vtk=True,
            cpos="iso",
            show_edges=True,
            edge_color="white",
            show_node_numbering=True,
            color="purple")

# Print the list of elements.
print(mapdl.elist())

# Plot the nodes using VTK.
mapdl.nplot(vtk=True,
            nnum=True,
            background="",
            cpos="iso",
            show_bounds=True,
            point_size=10)

# Print the list of nodes.
print(mapdl.nlist())


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of symmetric boundary conditions for simplified model.

# Select nodes by location and apply BC.
mapdl.nsel("S", "LOC", "X", 0)
mapdl.dsym("SYMM", "X", 0)
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.dsym("SYMM", "Y", 0)
mapdl.nsel("S", "LOC", "Z", 0)
mapdl.dsym("SYMM", "Z", 0)
mapdl.nsel("ALL")


###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Apply the force of :math:`F = (100/4) lb` in the y-direction.

# Parametrization of the :math:`F` load for the quarter of the model.
F = 100 / 4

# Application of the load to the model.
mapdl.fk(top_keypoint, "FY", -F)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system. Print the solver output.

mapdl.run("/SOLU")
out = mapdl.solve()
mapdl.finish()
print(out)


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing for the model with elements ``shell181``.
# Plotting nodal displacement.
# Get the the radial displacement at the node where force F is applied.

mapdl.post1()
mapdl.set(1)


###############################################################################
# Plotting
# ~~~~~~~~
# Plot nodal displacement with PyVista functionality.
mapdl.post_processing.plot_nodal_displacement(
    title="Nodal Displacements",
    component="Y",
    cpos="zx",
    scalar_bar_args={"title": "Nodal Displacements", "vertical": True},
    show_node_numbering=True,
    show_axes=True,
    show_edges=True
)


###############################################################################
# Getting the radial displacements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# To determine the radial displacement :math:`\delta` at the point
# where F is applied, we can use :meth:`Mapdl.get_value <ansys.mapdl.core.Mapdl.get_value>`.

# Select keypoint by its number ``top_keypoint``.
mapdl.ksel("S", vmin="top_keypoint")

# Select the node associated with the selected keypoint.
mapdl.nslk()

# Get the number of the selected node by :meth:`Mapdl.get <ansys.mapdl.core.Mapdl.get>`
top_node = int(mapdl.get("_", "node", 0, "num", "max"))

# Check the number of the selected node.
print(top_node)

# Define radial displacement at the node where F is applied.
deflect_shell_181 = mapdl.get_value(entity='node',
                                    entnum=top_node,
                                    item1='u',
                                    it1num='y')

# Use ``round()`` function to obtain needed number of decimals.
print(round(deflect_shell_181, 4))


###############################################################################
# Redo with Shell 281
# ~~~~~~~~~~~~~~~~~~~

mapdl.clear()

# Enter verification example mode and the pre-processing routine.
mapdl.verify()
mapdl.prep7()


###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element type (a shell-type).

# Type of analysis: Static.
mapdl.antype("STATIC")

# Define element number.
elem_num = 1

# Element type: SHELL181.
mapdl.et(elem_num, "SHELL281")

# Special Features are defined by keyoptions of shell element:


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material.

# Define material number.
mat_num = 1

# Define material properties.
mapdl.mp("EX", mat_num, 10.5E6)
mapdl.mp("NUXY", mat_num, 0.3125)
print(mapdl.mplist())


###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a shell element.

# Parametrization of the shell thickness.
t = 0.094

# Define cross-section number.
sec_num = 1

# Define shell cross-section.
mapdl.sectype(secid=sec_num, type_="SHELL", name="shell181")
mapdl.secdata(t, mat_num, 0, 5)


###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# Set up the keypoints and create the area through the keypoints.

# Define global cylindrical coordinate system.
mapdl.csys(1)

# Define keypoints by coordinates.
mapdl.k(1, 4.953)
mapdl.k(2, 4.953, "", 5.175)

# Generates additional keypoints from a pattern of keypoints.
mapdl.kgen(2, 1, 2, 1, "", 90)

# Create an area through keypoints.
mapdl.a(1, 2, 4, 3)

# Define the number of the keypoint where F is applied using inline function.
q = mapdl.queries
top_keypoint = q.kp(4.953, 90, 0)


###############################################################################
# Meshing
# ~~~~~~~
# Define line division of the lines, then mesh the area with shell elements.

# Specify the default number of line divisions.
mapdl.esize("", 8)

# Mesh the area.
mapdl.amesh(1)

# Define global cartesian coordinate system.
mapdl.csys(0)

# Plot the mesh.
mapdl.eplot(title="Plot the currently selected elements",
            vtk=True,
            cpos="iso",
            show_edges=True,
            edge_color="white",
            show_node_numbering=True,
            color="purple")

# Print the list of elements.
print(mapdl.elist())

# Plot the nodes using VTK.
mapdl.nplot(vtk=True,
            nnum=True,
            cpos="iso",
            show_bounds=True,
            point_size=10)

# Print the list of nodes.
print(mapdl.nlist())


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of symmetric boundary conditions for simplified model.

# Select nodes by location and apply BC.
mapdl.nsel("S", "LOC", "X", 0)
mapdl.dsym("SYMM", "X", 0)
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.dsym("SYMM", "Y", 0)
mapdl.nsel("S", "LOC", "Z", 0)
mapdl.dsym("SYMM", "Z", 0)
mapdl.nsel("ALL")


###############################################################################
# Define Distributed Loads
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Apply the force of :math:`F = (100/4) lb` in the y-direction.

# Parametrization of the :math:`F` load for the quarter of the model.
F = 100 / 4

# Application of the load to the model.
mapdl.fk(top_keypoint, "FY", -F)
mapdl.finish()


###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system. Print the solver output.

mapdl.run("/SOLU")
out = mapdl.solve()
mapdl.finish()
print(out)


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing for the model with elements ``shell281``.
# Plotting nodal displacement.
# Get the the radial displacement at the node where force F is applied.

mapdl.post1()
mapdl.set(1)


###############################################################################
# Plotting
# ~~~~~~~~
# Plot nodal displacement with PyVista functionality.
mapdl.post_processing.plot_nodal_displacement(
    title="Nodal Displacements",
    component="Y",
    cpos="zx",
    scalar_bar_args={"title": "Nodal Displacements", "vertical": True},
    show_node_numbering=True,
    show_axes=True,
    show_edges=True
)


###############################################################################
# Getting the radial displacements
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# To determine the radial displacement :math:`\delta` at the point
# where F is applied, we can use :meth:`Mapdl.get_value <ansys.mapdl.core.Mapdl.get_value>`.

# Select keypoint by its number ``top_keypoint``.
mapdl.ksel("S", vmin="top_keypoint")

# Select the node associated with the selected keypoint.
mapdl.nslk()

# Get the number of the selected node by :meth:`Mapdl.get <ansys.mapdl.core.Mapdl.get>`
top_node_try = int(mapdl.get("_", "node", 0, "num", "max"))
print(top_node_try)

# Define radial displacement at the node where F is applied.
deflect_shell_281 = mapdl.get_value(entity='node',
                                    entnum=top_node_try,
                                    item1='u',
                                    it1num='y')

# Use ``round()`` function to obtain needed number of decimals.
print(round(deflect_shell_281, 4))


###############################################################################
# Check Results
# ~~~~~~~~~~~~~
# Now we have the deflections, we can compare them to the expected values
# of radial deflection at the node where force :math:`F` is was applied
# for both simulations. The expected value for :math:`\delta_{\mathrm{shell181}}` is 0.1139,
# and :math:`\delta_{\mathrm{shell281}}` is 0.1139.

# Results obtained by hand-calculations.
deflect_target_181 = 0.1139
deflect_target_281 = 0.1139

# Calculate the deviation.
deflect_ratio_shell_181 = abs(deflect_shell_181) / deflect_target_181
deflect_ratio_shell_281 = abs(deflect_shell_281) / deflect_target_281

# Print output results.
output = f"""
----------------------------------------------------------------------------
------------------------- VM3 RESULTS COMPARISON ---------------------------
----------------------------------------------------------------------------
                            |   TARGET   |   Mechanical APDL   |   RATIO   |
----------------------------------------------------------------------------
    Deflection, in SHELL181{deflect_target_181:11.4f} {abs(deflect_shell_181):17.4f} {deflect_ratio_shell_181:15.4f}
    Deflection, in SHELL281{deflect_target_281:11.4f} {abs(deflect_shell_281):17.4f} {deflect_ratio_shell_281:15.4f}
----------------------------------------------------------------------------
"""
print(output)
