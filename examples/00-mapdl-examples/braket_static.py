"""

===================================
Static Analysis of a Corner Bracket
===================================

This is a jupyter notebook example adapted from a classic Ansys APDL tutorial
[<b>Static Analysis of a Corner Bracket</b>](https://ansyshelp.ansys.com/account/Secured?returnurl=/Views/Secured/corp/v231/en/ans_tut/structural_cb.html)

Some of the commands are easier in python, some are not possible and some work
arounds available in python are encouraged. When things are not required the
text will have a strike through.

Problem Specification
=====================

| Applicable Products: | Ansys Multiphysics, Ansys Mechanical, Ansys Structural|
| :- | :- |
| Level of Difficulty: | Easy|
| Interactive Time Required: | 60 to 90 minutes|
| Discipline: | Structural|
| Analysis Type: | Linear static|
| Element Types Used: | PLANE183|
| Features Demonstrated: | Solid modeling including primitives, Boolean operations, and fillets; tapered pressure load;<br> deformed shape and stress displays; listing of reaction forces; examination of structural energy error|
| Help Resources: | Structural Static Analysis and PLANE183 |

Problem Description
===================

This is a simple, single-load-step, structural static analysis of a corner angle
bracket. The upper-left pin hole is constrained (welded) around its entire
circumference, and a tapered pressure load is applied to the bottom of the
lower-right pin hole. The US Customary system of units is used.
The objective is to demonstrate a typical Mechanical APDL analysis procedure.

Bracket Model
~~~~~~~~~~~~~

The dimensions of the corner bracket are shown in the accompanying figure.
The bracket is made of A36 steel with a Young's modulus of 30E6 psi and Poisson's
ratio of .27.

![bracketImage.png](attachment:ab590723-e3c0-491e-a875-ca8dc5b65e38.png)

.. image::
    :alt: Bracket image


Approach and Assumptions
~~~~~~~~~~~~~~~~~~~~~~~~

Because the bracket is thin in the z direction (1/2 inch thickness) compared
to its x and y dimensions, and because the pressure load acts only in the x-y
plane, assume plane stress for the analysis.

Your approach is to use solid modeling to generate the 2D model and automatically
mesh it with nodes and elements. (An alternative approach is to create the nodes
and elements directly.)


Build the geometry
==================

This is the beginning of preprocessing.

Step 1: define rectangles
~~~~~~~~~~~~~~~~~~~~~~~~~

There are several ways to create the model geometry within Mechanical APDL, some more convenient than others. The first step is to recognize that you can construct the bracket easily with combinations of rectangles and circle Primitives.

Select an arbitrary global origin location, then define the rectangle and circle primitives relative to that origin. For this analysis, use the center of the upper-left hole. Begin by defining a rectangle relative to that location.

The APDL command **rectng** is used to create a rectangle with X1,X2,Y1,Y2 dimensions.
In PyMAPDL the mapdl namespace is used to call the APDL command.

.. raw:: html

    <pre>
    <code>
    <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.rectng.html#rectng">Mapdl.rectng(x1='', x2='', y1='', y2='', **kwargs)</a>
    </code>
    </pre>

**Dimension Box 1**:
Enter the following:

.. code:: python

    X1 = 0
    X2 = 6
    Y1 = -1
    Y2 = 1

Or use a python list to store the dimensions:

.. code:: python

    box1 = [0, 6, -1, 1]
    mapdl.rectng(box1[0], box1[1], box1[2], box1[3])

**Dimension Box 2**:
Enter the following:

.. code:: python

    X1 = 4
    X2 = 6
    Y1 = -1
    Y2 = -3

"""

# import packages and start an mapdl session
import tempfile

localTemp = tempfile.gettempdir()
print(localTemp)

# ! this keeps an exe running until forced to quit! Always include a mapdl.exit() at end
from ansys.mapdl.core import launch_mapdl

jobName = "bracket"  # optional

mapdl = launch_mapdl(run_location=localTemp, jobname=jobName, override=True)

###############################################################################
# parameterize everything, use python lists or whatever works for you
# Good practice would be to put all parameters near or at the top of the input file. But for this interactive tutorial they are inline.
box1 = [0, 6, -1, 1]
box2 = [4, 6, -1, -3]

###############################################################################
# The :meth:`mapdl.prep7() <ansys.mapdl.core.mapdl.prep7>` command starts the APDL pre processor to start the build up of
# the analysis. This is the processor where the model geometry is created.
#
# .. raw:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/session/_autosummary/ansys.mapdl.core.mapdl.prep7.html#prep7">Mapdl.prep7(**kwargs)</a>
#     </code>
#    </pre>
#

mapdl.prep7()

# build your boxes
mapdl.rectng(box1[0], box1[1], box1[2], box1[3])
mapdl.rectng(box2[0], box2[1], box2[2], box2[3])


###############################################################################
# Step 2: change plot controls and replot
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# PyMapdl plot controls are in the properties of the
# :meth:`mapdl.aplot() <ansys.mapdl.core.mapdl.aplot>` command.
#
# .. raw:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/api/_autosummary/ansys.mapdl.core.mapdl.aplot.html#aplot">Mapdl.aplot(na1='', na2='', ninc='', degen='', scale='', vtk=None, quality=4, show_area_numbering=False, show_line_numbering=False, color_areas=False, show_lines=False, **kwargs)</a>
#     </code>
#    </pre>
#
# The area plot shows both rectangles, which are areas, in the same color.
# To more clearly distinguish between areas, turn on area numbers. The inputs
# for the plotting controls can be found by highlighting the command
# (:meth:`mapdl.aplot() <ansys.mapdl.core.mapdl.aplot>` and right clicking for *show contextual help*.
#

# Area plot command to be reused through analysis
mapdl.aplot(cpos="xy", show_lines=True)


###############################################################################
# Step 3: create first circle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# With the the use of logic/booleans, the original geometric parameters
# (box1, box2) can be used to locate the circles.
#
# Create the half circle at each end of the bracket. You will actually create
# a full circle on each end and then combine the circles and rectangles with a
# Boolean add operation (discussed in step 5).
#
# The APDL command to create the circles is :meth:`mapdl.cyl4() <ansys.mapdl.core.mapdl.cyl4>`.
#
# .. rst:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.cyl4.html#cyl4">Mapdl.cyl4(xcenter='', ycenter='', rad1='', theta1='', rad2='', theta2='', depth='', **kwargs)</a>
#     </code>
#    </pre>
#
# The first circle area is located on the left side at the X,Y location ( box1[0], (box1[2]+box1[3])/2). The radius is 1.

# Create the first circle
radius = 1
circle1_X = box1[0]
circle1_Y = (box1[2] + box1[3]) / 2
mapdl.cyl4(circle1_X, circle1_Y, radius)

mapdl.aplot(vtk=True, cpos="xy", show_area_numbering=True, show_lines=True)


###############################################################################
# Step 4: create second circle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The second circle to be created is at the X,Y location:
#

circle2_X = (box2[0] + box2[1]) / 2
circle2_Y = box2[3]

###############################################################################
# Use these parameter values to create the new area with the same radius of 1
# as the first circle area.

mapdl.cyl4(circle2_X, circle2_Y, radius)
mapdl.aplot(vtk=True, cpos="xy", show_area_numbering=True, show_lines=True)


###############################################################################
# Step 5: add areas
# ~~~~~~~~~~~~~~~~~
# Now that the appropriate pieces of the model (rectangles and circles) are defined,
# add them together so the model becomes one continuous area.
# Use the Boolean add operation :meth:`mapdl.aadd() <ansys.mapdl.core.mapdl.aadd>`
# to add the areas together.
#
# .. rst:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.aadd.html#aadd">Mapdl.aadd(na1='', na2='', na3='', na4='', na5='', na6='', na7='', na8='', na9='', **kwargs)</a>
#     </code>
#    </pre>
#
#
# Pick All for all areas to be added.
mapdl.aadd("all")

###############################################################################
# ## 2.1.3.6. step 6: create line fillet.
#
# The right angle between the two boxes will be improved using a fillet with a
# radius of 0.4.
# This can be done by selecting the lines around that area and creating a fillet.
#
# The APDL :meth:`mapdl.lsel() <ansys.mapdl.core.mapdl.lsel>` command is used
# to select lines. Here we use the X and Y location of the lines used to create
# the boxes to create our selection.
#
# .. raw:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/database/_autosummary/ansys.mapdl.core.mapdl.lsel.html#lsel">Mapdl.lsel(type_='', item='', comp='', vmin='', vmax='', vinc='', kswp='', **kwargs)</a>
#     </code>
#    </pre>
#
# After we select the line it needs to be written to a parameter so we can use
# it to generate the fillet line.
# That is done using the :meth:`mapdl.get() <ansys.mapdl.core.mapdl.get>` command
# from PyMAPDL or `GET` in pymapdl.
# Since we have selected one line, we can use the **MAX** and **NUM** arguments
# for the :meth:`mapdl.get() <ansys.mapdl.core.mapdl.get>` command.
#
# Select first line for fillet
line1 = mapdl.lsel("S", "LOC", "Y", box1[2])
l1 = mapdl.get("line1", "LINE", 0, "NUM", "MAX")


###############################################################################
#
# .. raw:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/api/_autosummary/ansys.mapdl.core.mapdl.get.html#get">Mapdl.get(par='__floatparameter__', entity='', entnum='', item1='', it1num='', item2='', it2num='', item3='', it3num='', item4='', it4num='', **kwargs)[source]
#    </a>
#     </code>
#    </pre>
#
# If we write the command to a python parameter (**line1**) we can use either
# the APDL parameter **l1** or the python parameter **line1** when we create
# the fillet line.
#
# Select second line for fillet, create python parameter
line2 = mapdl.lsel("S", "LOC", "X", box2[0])
l2 = mapdl.get("line2", "LINE", 0, "NUM", "MAX")

###############################################################################
# Once we have both lines selected we can use the APDL command
# :meth:`mapdl.lfillt() <ansys.mapdl.core.mapdl.lfillt>` to generate the fillet
# between the lines.
#
# .. raw:: html
#
#    <pre>
#     <code>
#      <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.lfillt.html#lfillt">Mapdl.lfillt(nl1='', nl2='', rad='', pcent='', **kwargs)</a>
#     </code>
#    </pre>
#
# <em>Note that python could return a list if more than one line is selected.</em>

###############################################################################
# Here we use a mix of the APDL parameter as a string **'LINE1'** and the **L2**
# python parameter to create the fillet line.
#
# Create fillet line using selected line (parameter names)
fillet_radius = 0.4
mapdl.allsel()
line3 = mapdl.lfillt("line1", l2, fillet_radius)

mapdl.allsel()
mapdl.lplot(vtk=True, cpos="xy")

###############################################################################
# Step 7: create fillet area
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To create the area delineated by line1, line2 and newly created line3, we use
# the :meth:`mapdl.al() <ansys.mapdl.core.mapdl.al>` command. The three lines
# are the input. If we select them all, we can use the 'ALL' argument to create
# the area.
#
# First we have to reselect the newly created lines in the fillet area.
# To do this we can use the fillet_radius parameter and the
# :meth:`mapdl.lsel() <ansys.mapdl.core.mapdl.lsel>` command.
#
# For the two newly created straight lines, the length will be the same as the
# fillet_radius. So we can use the length argument with the
# :meth:`mapdl.lsel() <ansys.mapdl.core.mapdl.lsel>` command.
#
mapdl.allsel()

# Select lines for the area
mapdl.lsel("S", "LENGTH", "", fillet_radius)

###############################################################################
# Additionally, we need the fillet line itself (line3) but we can use the
# :meth:`mapdl.lsel() <ansys.mapdl.core.mapdl.lsel>` command again with either
# the RADIUS argument if there is only one line with that radius in our model
# or more directly using the parameter name of the line.
# Note the **'A'** to additionally select items.
#
mapdl.lsel("A", "LINE", "", line3)

###############################################################################
#
# .. raw:: html
#
#     <pre>
#      <code>
#       <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.al.html#al">Mapdl.al(l1='', l2='', l3='', l4='', l5='', l6='', l7='', l8='', l9='', l10='', **kwargs)</a>
#      </code>
#     </pre>
#
#
# Create the area
mapdl.al("ALL")

###############################################################################
# ### 2.1.3.8. step 8: add areas together.
# Append all areas again with the :meth:`mapdl.aadd() <ansys.mapdl.core.mapdl.aadd>`. Since we have only the 2 areas to combine, use the 'ALL' argument.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.aadd.html#aadd">Mapdl.aadd(na1='', na2='', na3='', na4='', na5='', na6='', na7='', na8='', na9='', **kwargs)</a>
#  </code>
# </pre>
#


mapdl.lplot(vtk=True, cpos="xy", show_line_numbering=True)


# Add the area to the main area
mapdl.aadd("all")
mapdl.aplot(vtk=True, cpos="xy", show_area_numbering=True, show_lines=True)

###############################################################################
# ### 2.1.3.9. step 9: create first pin hole.
# The first pin hole is located at the left side of the first box, so we can use the box dimensions to locate our new circle.
#
# The X value/center of the pinhole is at box1, X1 (`box1[0]`). The Y value is the average of the two box1 Y values (`(box1[2] + box1[3])/2`).
#
#     pinhole_radius = 0.4
#     pinhole1_X = box1[0]
#     pinhole1_Y = (box1[2] + box1[3])/2
#     mapdl.cyl4(pinhole1_X, pinhole1_Y , pinhole_radius)
#
# * Note we set some of these areas to parameters to use later in the analysis.  This will later allow us to these lines that are used to create the areas :meth:`mapdl.asll() <ansys.mapdl.core.mapdl.asll>`
#


# Create the first pinhole
pinhole_radius = 0.4
pinhole1_X = box1[0]
pinhole1_Y = (box1[2] + box1[3]) / 2

pinhole1 = mapdl.cyl4(pinhole1_X, pinhole1_Y, pinhole_radius)

###############################################################################
# ### 2.1.3.10. step 10: create second pin hole.
# The second pin hole is located at the bottom of the second box, so again we can use the box 2 dimensions to locate the circle.
#
# For this pinhole, the X value is the average of the box 2 X values (`(box2[0] + box2[1])/2`) and the Y2 (`box2[3]`) value.
#
# Create the second pinhole
pinhole2_X = (box2[0] + box2[1]) / 2
pinhole2_Y = box2[3]

pinhole2 = mapdl.cyl4(pinhole2_X, pinhole2_Y, pinhole_radius)
pinhole2_lines = mapdl.asll("S", 0)

###############################################################################
# ### 2.1.3.11. step 11: subtract pin holes from bracket.
#
# If you use :meth:`mapdl.aplot() <ansys.mapdl.core.mapdl.aplot>` with lines at this point you will see we have created 2 circle areas overlapping the bracket. We can use the :meth:`mapdl.asba() <ansys.mapdl.core.mapdl.asba>` command, the boolean command to subtract areas, to remove the circles from the bracket.
#
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.asba.html#asba">Mapdl.asba(na1='', na2='', sepo='', keep1='', keep2='', **kwargs)</a>
#  </code>
# </pre>
#
# Since we have two pin hole circles, we will use the command twice.
#
# Remove pin hole areas from bracket
mapdl.asba("all", pinhole1)
bracket = mapdl.asba("all", pinhole2)
mapdl.aplot(vtk=True, show_area_numbering=True, show_lines=True, cpos="xy")

###############################################################################
# #### 2.1.3.12. step 12: save the database
# Probably a good idea at this point, if not earlier, to save the jupyter notebook.

# ### 2.1.4. define the materials
#
# #### 2.1.4.1. step 13: set preferences.
# Note we will do this later in the pymapdl code.
#
# #### 2.1.4.2. step 14: define material properties.
# To define material properties, there is only one material for the bracket, A36 Steel, with given values for Young's modulus of elasticity and Poisson's ratio.
#
#     Young's Modulus [units] = 30e6
#     Poisson's ratio = 0.27
#
# The :meth:`mapdl.mp() <ansys.mapdl.core.mapdl.mp>` command is used to define material properties in APDL.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.mp.html#mp">Mapdl.mp(lab='', mat='', c0='', c1='', c2='', c3='', c4='', **kwargs)</a>
#  </code>
# </pre>
#
#     mapdl.mp("EX", 1, ex)
#     mapdl.mp("PRXY", 1, prxy)  #  Poisson's ratio
#


## Material parameter, best practice would be to have all parameters in one block/cell early in the script
ex = 30e6
prxy = 0.27
mapdl.mp("EX", 1, ex)
mapdl.mp("PRXY", 1, prxy)
#  Poisson's ratio

###############################################################################
# #### 2.1.4.3. step 15: define element types and options.
# In any analysis, you select elements from a library of element types and define the appropriate ones for the analysis. In this case, only one element type is used: PLANE183, a 2D, quadratic, structural, higher-order element.
#
# The command to select an element is :meth:`mapdl.et() <ansys.mapdl.core.mapdl.et>`.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.et.html#et">Mapdl.et(itype='', ename='', kop1='', kop2='', kop3='', kop4='', kop5='', kop6='', inopr='', **kwargs)</a>
#  </code>
# </pre>
#
#
# A higher-order element enables you to have a coarser mesh than with lower-order elements while still maintaining solution accuracy. Also, Mechanical APDL generates some triangle-shaped elements in the mesh that would otherwise be inaccurate when using used lower-order elements.
#
# Specify plane stress with thickness as an option for PLANE183. (Thickness is defined as a real constant in Step 16: Define real constants..)
#
#
# Options for PLANE183 are to be defined.
#
# Select plane stress with thickness option for element behavior. To find this information you would have to look in the full Ansys documentation regarding the :meth:`mapdl.plane183() <ansys.mapdl.core.mapdl.plane183>` element definition. But it is set using the element keyoption 3.
# <pre>
#  <code>
#   <a href="https://ansyshelp.ansys.com/account/Secured?returnurl=/Views/Secured/corp/v231/en/ans_elem/Hlp_E_PLANE183.html">PLANE183</a>
#  </code>
# </pre>
#
#     mapdl.et(1, "PLANE183", kop3=3)


# define a PLANE183 element type with thickness
mapdl.et(1, "PLANE183", kop3=3)

###############################################################################
#  #### 2.1.4.4. step 16: define real constants.
# Assuming plane stress with thickness, enter the thickness as a real constant for PLANE183:
#
# The :meth:`mapdl.r() <ansys.mapdl.core.mapdl.r>` command is used to set real constants.
#
#  <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.r.html#r">Mapdl.r(nset='', r1='', r2='', r3='', r4='', r5='', r6='', **kwargs)</a>
#  </code>
# </pre>
#
#     thick = 0.5
#     mapdl.r(1, thick)  # thickness of 0.5 length units)
#


# Set element thickness

thick = 0.5
mapdl.r(1, thick)  # thickness of 0.5 length units)

###############################################################################
# ### 2.1.5. generate the mesh
#
# #### 2.1.5.1. step 17: mesh the area.
# You can mesh the model without specifying mesh-size controls. If you are unsure of how to determine mesh density, you can allow Mechanical APDL to apply a default mesh. For this model, however, you will specify a global element size to control overall mesh density.
# Set Global Size control using the :meth:`mapdl.esize() <ansys.mapdl.core.mapdl.esize>` command. Set a size of 0.5 or a slightly smaller value to improve the mesh.
#
#  <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.esize.html#esize">Mapdl.esize(size='', ndiv='', **kwargs)</a>
#  </code>
# </pre>
#
# Mesh the areas using the :meth:`mapdl.amesh() <ansys.mapdl.core.mapdl.amesh>` command.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/prep7/_autosummary/ansys.mapdl.core.mapdl.amesh.html#amesh">Mapdl.amesh(na1='', na2='', ninc='', **kwargs)</a>
#  </code>
# </pre>
#
#
# Your mesh may vary slightly from the mesh shown. You may see slightly different results during postprocessing. For a discussion of results accuracy, see Planning Your Approach.
#
# And now we can use eplot to see the mesh.


# mesh
element_size = 0.5
mapdl.esize(element_size)
mapdl.amesh(bracket)
mapdl.eplot(
    vtk=True,
    cpos="xy",
    show_edges=True,
    show_axes=False,
    line_width=2,
    background="w",
)
# mapdl.nplot(vtk=True, cpos="xy",)

###############################################################################
# #### 2.1.5.2. step 18: save the jupyter notebook
# Save

# ### 2.1.6. apply loading
# To solve an Ansys FE analysis you have to be in the Solution processor, which is activated using the APDL :meth:`mapdl.slashsolu() <ansys.mapdl.core.mapdl.slashsolu>` command. Loading is considered part of the :meth:`mapdl.solu() <ansys.mapdl.core.mapdl.solu>` or solution processor in APDL.
#
# This is a bit of an orphan command due to the backslash, so we use the :meth:`mapdl.run() <ansys.mapdl.core.mapdl.run>` command in pymapdl which can be used to run any APDL command.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/api/_autosummary/ansys.mapdl.core.mapdl.run.html#run">Mapdl.run(command, write_to_log=True, mute=None, **kwargs)</a>
#  </code>
# </pre>
#
#     mapdl.run("/SOLU")
#
# Here we can set the analysis type with the :meth:`mapdl.antype() <ansys.mapdl.core.mapdl.antype>` command.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/solution/_autosummary/ansys.mapdl.core.mapdl.antype.html#antype">Mapdl.antype(antype='', status='', ldstep='', substep='', action='', **kwargs)</a>
#  </code>
# </pre>
#
#     mapdl.antype("STATIC")
#

###############################################################################
# #### 2.1.6.1. step 19: apply displacement constraints.
# This is where we add boundary conditions to the model. First we want to fix the model so it doesn't fly off into space. We do that by setting a zero displacement at the first pinhold.
# You can apply displacement constraints directly to lines.
#
# To do this without the graphical interface we would need to replot the lines or we can booleans and generate the lines from the pinholes locations/box parameters. By using the parameters we have created we can grab the lines and fix one end of the bracket.
#
# Pick the four lines around left-hand hole using the :meth:`mapdl.lsel() <ansys.mapdl.core.mapdl.lsel>` command and the pinehole1 parameters.
#
#     bc1 = mapdl.lsel('S','LOC','X' , pinhole1_X -pinhole_radius, pinhole1_X + pinhole_radius)
#
# Then for loading, select and apply the boundary condition to the nodes attached to those lines.
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/database/_autosummary/ansys.mapdl.core.mapdl.nsll.html#nsll">Mapdl.nsll(type_='', nkey='', **kwargs)</a>
#  </code>
# </pre>
#
#     fixNodes = mapdl.nsll(type = 'S')
#
# And then use the :meth:`mapdl.d() <ansys.mapdl.core.mapdl.d>` command to set the displacement to zero (fixed constraint).
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/solution/_autosummary/ansys.mapdl.core.mapdl.d.html#d">Mapdl.d(node='', lab='', value='', value2='', nend='', ninc='', lab2='', lab3='', lab4='', lab5='', lab6='', **kwargs)</a>
#  </code>
# </pre>
#
#     mapdl.d("ALL", "ALL" , 0) # The 0 is not required, without an input it will default to zero
#

# SOL processor
mapdl.allsel()
mapdl.run("/SOLU")
mapdl.antype("STATIC")

# set up boundary conditions
bc1 = mapdl.lsel(
    "S", "LOC", "X", pinhole1_X - pinhole_radius, pinhole1_X + pinhole_radius
)
print("Number of lines selected : " + str(len(bc1)))
fixNodes = mapdl.nsll(type="S")
mapdl.d("ALL", "ALL", 0)
mapdl.allsel()

###############################################################################
# #### 2.1.6.2. step 20: apply pressure load. apply the tapered pressure load to the bottom-right pin hole. (tapered here means varying linearly.)
#
# When a circle is created in Mechanical APDL, four lines define the perimeter; therefore, apply the pressure to two lines making up the lower half of the circle. Because the pressure tapers from a maximum value (500 psi) at the bottom of the circle to a minimum value (50 psi) at the sides, apply pressure in two separate steps, with reverse tapering values for each line.
#
#     p1 = 50
#     p2 = 500
#
# The Mechanical APDL convention for pressure loading is that a positive load value represents pressure into the surface (compressive).
#
# To pick the line use the same method used in the previous cell block (:meth:`mapdl.LSEL() <ansys.mapdl.core.mapdl.lsel>`) and then convert the lines to a nodal selection with the :meth:`mapdl.nsel() <ansys.mapdl.core.mapdl.nsel>` command.
#
# Note we have a slightly more complicated picking procedure for the two quarters of the full circle.
# A method to select the lines would be to grab the lower half of the second pinhole circle.
#
#     mapdl.lsel('S','LOC','Y' , pinhole2_Y -pinhole_radius, pinhole2_Y)
#
# And then repick from that selection the lines less than the X center of that pinhole.
#
#     mapdl.lsel('R','LOC','X' , -1e6, pinhole2_X)
#
# Here we use an extreme value of -1e6 to make sure we select all lines from the negative side up to pinhole2_X.
#
# Once we have the correct line we can use the :meth:`mapdl.sf() <ansys.mapdl.core.mapdl.sf>` command to load the line with a varying surface load.
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/solution/_autosummary/ansys.mapdl.core.mapdl.sf.html#sf">Mapdl.sf(nlist='', lab='', value='', value2='', **kwargs)</a>
#  </code>
# </pre>
#
#     mapdl.sf('ALL','PRES' , p1, p2)
#

# here we load the left side of the lower half of second pin hole
p1 = 50
p2 = 500

mapdl.lsel("S", "LOC", "Y", pinhole2_Y - pinhole_radius, pinhole2_Y)
mapdl.lsel("R", "LOC", "X", 0, pinhole2_X)

mapdl.lplot(vtk=True, cpos="xy")

mapdl.sf("ALL", "PRES", p1, p2)
mapdl.allsel()


# here we load the right of the lower half of the pinhole 2
mapdl.lsel("S", "LOC", "Y", pinhole2_Y - pinhole_radius, pinhole2_Y)
mapdl.lsel("R", "LOC", "X", pinhole2_X, pinhole2_X + pinhole_radius)

mapdl.lplot(
    vtk=True,
    cpos="xy",
    show_line_numbering=True,
)

mapdl.sf("ALL", "PRES", p2, p1)
mapdl.allsel()

###############################################################################
# ### 2.1.7. obtain the solution
#
# #### 2.1.7.1. step 21: solve.
#
# To solve an Ansys FE analysis you have to be in the Solution processor, which is activated using the APDL :meth:`mapdl.slashsolu() <ansys.mapdl.core.mapdl.slashsolu>`* command. This was done a few steps earlier.
#
# So the model is ready to solve using the :meth:`mapdl.solve() <ansys.mapdl.core.mapdl.solve>` command.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/solution/_autosummary/ansys.mapdl.core.mapdl.solve.html#solve">Mapdl.solve(action='', **kwargs)</a>
#  </code>
# </pre>
#     output = mapdl.solve()
#
# Review the information in the status window, then select File> Close (Windows), or Close (Linux), to close the window.
#
# Mechanical APDL stores the results of this single-load-step problem in the database and in the results file, Jobname.RST (or Jobname.RTH for thermal, Jobname.RMG for magnetic). The database can contain only one set of results at any given time, so in a multiple-load-step or multiple-substep analysis, Mechanical APDL stores only the final solution in the database.
#
# Mechanical APDL stores all solutions in the results file.


# Solve the model
output = mapdl.solve()
print(output)

###############################################################################
# ### 2.1.8. review the results
# This step represents the beginning of the postprocessing phase.
#
# The results you see may vary slightly from what is shown due to variations in the mesh.
#
# #### 2.1.8.1. step 22: enter the general postprocessor and read in the results.
# The Ansys APDL postprocessor a separate processor and is called with the :meth:`mapdl.post1() <ansys.mapdl.core.mapdl.post1>` command.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/session/_autosummary/ansys.mapdl.core.mapdl.post1.html#post1">MMapdl.post1(**kwargs)</a>
#  </code>
# </pre>
#
#     mapdl.post1()
#
# ### 2.1.8.2. step 23: plot the deformed shape.
# Here the method is to set the results to a parameter (:meth:`mapdl.result() <ansys.mapdl.core.mapdl.result>`) and then use the available results for plotting.
#
# In jupyter notebooks you can right click on a command to get the contextual help which will pop up on screen.
#
#     result = mapdl.result
#     disp_fact = 1e5
#     result.plot_nodal_displacement(0, cpos='xy',displacement_factor  = disp_fact,show_displacement = True, show_edges=True)
#
#
# Make selections in the Animation Controller (not shown), if necessary, then select Close.
#
#


# plot the nodal displacement
mapdl.post1()
result = mapdl.result
disp_fact = 1e10
result.plot_nodal_displacement(
    0, cpos="xy", displacement_factor=5, show_displacement=True, show_edges=True
)

###############################################################################
# #### 2.1.8.3. step 24: plot the von mises equivalent stress.
#
# Stress plots are also available using the :meth:`mapdl.plot_principal_nodal_stress() <ansys.mapdl.core.mapdl.plot_principal_nodal_stress>` command.
#
#     result.plot_principal_nodal_stress( 0,"SEQV", cpos="xy", background="w",text_color="k",add_text=False,show_edges=True,)
#


result.plot_principal_nodal_stress(
    0,
    "SEQV",
    cpos="xy",
    background="w",
    text_color="k",
    add_text=True,
    show_edges=True,
)

nnum, stress = result.principal_nodal_stress(0)
von_mises = stress[
    :, -1
]  # von-Mises stress is the last column in the stress results [-1]


# ## Iyi:
# The original tutorial () also demonstrated how to create a animation plot of a result. This is not natively available in pymapdl but since this is python, you can google for ideas and create your own animation.
#
# One idea is to create a series of plots and then stitch them together. This can be done with the python imageio.v2 library.
#
#     import imageio.v2 as imageio
#     from IPython.display import display, clear_output
#     subfolder = 'figs'
#     if subfolder not in os.listdir():
#         os.mkdir(subfolder)
#
#     picList = []
#     for ctr in range(10):
#         fileName = os.path.join(jobLocation, subfolder , 'file' + str(ctr) + '.jpg')
#         picList.append(fileName)
#         result.plot_nodal_displacement(0, cpos='xy',off_screen=True,displacement_factor  = ctr*1000,show_displacement = True, show_edges=True, screenshot=fileName)
#         clear_output()
#     myfile = 'myAnime.mp4'
#
#     aniSave = os.path.join(jobLocation, myfile)
#     images = []
#     for filename in picList:
#         images.append(imageio.imread(filename))
#     imageio.mimsave(aniSave, images)
#     myfile = 'myAnime.mp4'
#     writer = imageio.get_writer(myfile, fps=40)
#
#     for im in picList:
#         writer.append_data(imageio.imread(im))
#     writer.close()
#
#     import webbrowser
#     webbrowser.open(aniSave)

###############################################################################
# #### 2.1.8.4. step 25: list reaction solution.
#
# List the FY reactions forces. the adpl :meth:`mapdl.prrsol() <ansys.mapdl.core.mapdl.prrsol>` command will print the constrained node reaction solution.
#
# <pre>
#  <code>
#   <a href="https://mapdl.docs.pyansys.com/version/stable/mapdl_commands/post1/_autosummary/ansys.mapdl.core.mapdl.prrsol.html#prrsol">Mapdl.prrsol(lab='', **kwargs)</a>
#  </code>
# </pre>
#
#     reactForces = mapdl.prrsol(lab='FY')
#     print(reactForces)
#
# The values shown are representative and may vary from the values that you obtain.
#
# Many other options are available for reviewing results in the general postprocessor. You will see some other options in other tutorials. [<b>APDL Tutorials link</b>](https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v231/en/ans_tut/Hlp_UI_Tutorials.html)


reactForces = mapdl.prrsol(lab="FY")
print(reactForces)

###############################################################################
# #### 2.1.8.5. step 26: exit the mechanical apdl program.
# Exit the Mechanical APDL program.
#
#


# Most important command or an mapdl instance remains open
mapdl.exit()
