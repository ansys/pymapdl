""".. _ref_dcb_test_composite_delamination

Static simulation of double cantilever beam test via cohesive elements
----------------------------------------------------------------------

This example is inspired to a classic double cantilever beam test commonly used
to study mode I interfacial delamination of composite plates.

Objective
~~~~~~~~~

This example shows how to use PyMAPDL to simulate delamination in 
composite materials. PyDPF modules are also used for the post-processing of the results

Problem Figure
~~~~~~~~~~~~~~
.. image:: ../../../images/dcb_test.png
   :width: 400
   :alt: DCB experimental test setup

Procedure
~~~~~~~~~
* Launch MAPDL instance
* Setup the model
* Solve the model
* Plot results of interest using PyMAPDL
* Plot results using PyDPF

Additional Packages Used
~~~~~~~~~~~~~~~~~~~~~~~~
* `Matplotlib <https://matplotlib.org>`_ is used for plotting purposes.

"""

###############################################################################
# Starting MAPDL as a service
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This example begins by lunching Ansys Mechanical APDL 

from ansys.mapdl import core as pymapdl
from ansys.dpf.core import Model
from ansys.dpf import core as dpf
from ansys.dpf.core import locations
import pyvista as pv

# start MAPDL as a service
mapdl = pymapdl.launch_mapdl()
print(mapdl)

###############################################################################
# Setting up the model and adding material parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In this step the model setup is performed choosing the units system and the
# element types to be used in the simulations. In this case a fully 3D approach
# is chosen therefore SOLID186 elements are used for meshing volumes and 
# TARGE170/CONTA174 are used for modelling cohesive elements in between contact 
# surfaces. Furthermore, material properties are defined. Composite plates are 
# modelled using homogenous linear elastic orthotropic properties whereas a 
# bilinear cohesive law is used for cohesive elements. 

# entering the preprocessor and assign the unit system 
mapdl.prep7()
mapdl.units("mpa")  

# defining SOLID185, TARGE170 and CONTA174 elements along with the element size
mapdl.et(1, 185)
mapdl.et(2, 170)
mapdl.et(3, 174)
mapdl.esize(10.)

# defining a material properties for the composite plates
mapdl.mp("ex", 1, 61340)
mapdl.mp("dens", 1, 1.42E-09)
mapdl.mp("nuxy", 1, 0.1)

# defining the bilinear cohesive law
mapdl.mp("mu", 2, 0)
mapdl.tb("czm",2, 1,"","bili")
mapdl.tbtemp(25.)
mapdl.tbdata(1, 50., 0.5, 50, 0.5, 0.01, 2)

###############################################################################
# Creating the geometry in the model and meshing
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The two plates are generated as two parallelepipeds to which are assigned
# the composite material properties and the correct three-dimensional elements.

# generating the two composite plates
vnum0 = mapdl.block(0., 85., 0., 25., 0., 1.7)
vnum1 = mapdl.block(0., 85., 0., 25., 1.7, 3.4)

# assigning material properties and element type
mapdl.mat(1)
mapdl.type(1)

# performing the meshing
mapdl.vmesh(vnum0)
mapdl.vmesh(vnum1)
mapdl.eplot()

###############################################################################
# Generating cohesive elements in between the contact surfaces
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The generation of cohesive elements is the most delicate part of the
# modelling approach. In first instance the two contact surfaces are identified
# and defined as a components (in this case cm_1 and cm_2 respectively). 
# Successively, the CONTA174 and TARGE170 elements real constants, as well as 
# their keyoptions are set to capture the right behaviour. The meaning of each 
# of  these parameters can be found in the Ansys element documentation.
# Finally, elements are generated on top of the respective surfaces cm_1 and 
# cm_2.

# identifying the two touching areas and assigning them to components
_ = mapdl.allsel()
mapdl.asel("s", "loc", "z", 1.7)
areas = mapdl.geometry.anum
mapdl.geometry.area_select(areas[0], "r")
mapdl.nsla("r", 1)
mapdl.nsel("r", "loc", "x", 10, 86)
mapdl.cm("cm_1", "node")

_ = mapdl.allsel()
mapdl.asel("s", "loc", "z", 1.7)
areas = mapdl.geometry.anum
mapdl.geometry.area_select(areas[1], "r")
mapdl.nsla("r", 1)
mapdl.nsel("r", "loc", "x", 10, 86)
mapdl.cm("cm_2", "node")

# identifying all the elements before the creation of TARGE170 elements
_ = mapdl.allsel()
mapdl.cm("_elemcm", "elem")
mapdl.mat(2)

# assigning real constants and keyoptions
mapdl.r(3, "", "", 1.0, 0.1, 0, "")
mapdl.rmore("", "", 1.0E20, 0.0, 1.0, "")
mapdl.rmore(0.0, 0.0, 1.0, "", 1.0, 0.5)
mapdl.rmore(0.0, 1.0, 1.0, 0.0, "", 1.0)
mapdl.rmore("", "", "", "", "", 1.0)
mapdl.keyopt(3, 4, 0)
mapdl.keyopt(3, 5, 0)
mapdl.keyopt(3, 7, 0)
mapdl.keyopt(3, 8, 0)
mapdl.keyopt(3, 9, 0)
mapdl.keyopt(3, 10, 0)
mapdl.keyopt(3, 11, 0)
mapdl.keyopt(3, 12, 3)
mapdl.keyopt(3, 14, 0)
mapdl.keyopt(3, 18, 0)
mapdl.keyopt(3, 2, 0)
mapdl.keyopt(2, 5, 0)

# generating TARGE170 elements on top of cm_1
mapdl.nsel("s", "", "", "cm_1")
mapdl.cm("_target", "node")
mapdl.type(2)
mapdl.esln("s", 0)
mapdl.esurf()

# generating the CONTA174 elements on top of cm_2
mapdl.cmsel("s", "_elemcm")
mapdl.nsel("s", "", "", "cm_2")
mapdl.cm("_contact", "node")
mapdl.type(3)
mapdl.esln("s", 0)
mapdl.esurf()

###############################################################################
# Generating boundary conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In this final step the boundary conditions are assigned to replicate the real
# test conditions. In particular, one end of the two composite plates
# is fixed against translation along x, y and z. On the other hand, on the 
# opposite side of the plate the displacement conditions are applied to
# simulate the interfacial crack opening. These conditions are applied to the
# top and bottom nodes corresponding to the geometrical edges located at 
# x = 0.0, z = 0.0 and x = 0.0, z = 3.4 respectively. Two different components 
# are assigned to these sets of nodes for a faster identification of the nodes 
# bearing reaction forces.

# applying the two displacement conditions
_ = mapdl.allsel()
mapdl.nsel(type_="s", item="loc", comp = "x" ,vmin = 0.0, vmax = 0.0)
mapdl.nsel(type_="r", item="loc", comp = "z" ,vmin = 3.4, vmax = 3.4)
mapdl.d(node="all", lab="uz", value = 10)
mapdl.cm("top_nod","node" )

_ = mapdl.allsel()
mapdl.nsel(type_="s", item="loc", comp = "x" ,vmin = 0.0, vmax = 0.0)
mapdl.nsel(type_="r", item="loc", comp = "z" ,vmin = 0.0, vmax = 0.0)
mapdl.d(node="all", lab="uz", value = -10)
mapdl.cm("bot_nod","node" )

# applying the fix condition
_ = mapdl.allsel()
mapdl.nsel(type_="s", item="loc", comp = "x" ,vmin = 85.0, vmax = 85.0)
mapdl.d(node="all", lab="ux", value = 0.0)
mapdl.d(node="all", lab="uy", value = 0.0)
mapdl.d(node="all", lab="uz", value = 0.0)

###############################################################################
# Run the non-linear static analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# A non-linear static analysis is run to in this very last step. One hundreds 
# substeps are requested in this case to have a smooth crack opening 
# progression as well as to facilitate convergency for the static solver.

# entering the solution processor and defining the analysis settings
_ = mapdl.allsel()
mapdl.finish()
mapdl.run("/SOLU")
mapdl.antype("static")

# activating non-linear geometry
mapdl.nlgeom("on")

# requesting substeps
mapdl.autots(key = "on")
mapdl.nsubst(nsbstp = 100, nsbmx=100, nsbmn=100)
mapdl.kbc(key=0)
mapdl.outres("all","all")

# solving
output = mapdl.solve()
print(output)

###############################################################################
# Post-processing of the results using PyMAPDL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This section illustrates how to perform a quick prost-processing of the
# the results using PyMAPDL. In this particular case as one of the key part is 
# measuring the delamination length, the cohesive damage parameter is plotted. 
# Although, the damage parameter is an element parameter, the result is 
# provided in terms of nodal result. Therefore, in this case we present the 
# result for just one of the four-noded cohesive element i.e. NMISC = 70. 
# The result for the other nodes are present at NMISC = 71,72,73.
# The actual damage parameter nodal values can also be retrieved from the 
# solved model in form of table (or array).

# entering the postprocessing processor 
mapdl.post1()

#selecting the substep
mapdl.set(1,100)

# selecting CONTA174 elements
_ = mapdl.allsel()
mapdl.esel("s", "ename", "", 174)

# plotting the element values
mapdl.post_processing.plot_element_values(
    "nmisc", 70, scalar_bar_args={"title": "nmisc, dparam"}
)

# extracting the nodal values of the damage parameter
_ = mapdl.allsel()
mapdl.esel("s", "ename", "", 174)
mapdl.etable("damage", "nmisc", 70)
print(mapdl.pretab("damage"))

###############################################################################
# Exit MAPDL
mapdl.exit()

###############################################################################
# Post-processing of the results using PyDPF
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PyDPF can be used in this context to visualise the crack opening throughout
# the simulation as an animation. The steps for producing that are provided in 
# below.

data_src = dpf.DataSources("file.rst")

model = Model(data_src)
plotter = pv.Plotter()
plotter.open_gif("dcb.gif")

for i in range(1, 100):
    dam_op = dpf.operators.result.nmisc()
    dam_op.inputs.data_sources(data_src)
    dam_op.inputs.time_scoping([i])
    item_index = int(70)
    dam_op.inputs.item_index.connect(item_index)
    damage_value = dam_op.outputs.fields_container()

    disp_op = dpf.Operator("U")
    disp_op.inputs.data_sources.connect(model.metadata.data_sources)

    meshed_region = model.metadata.meshed_region
    Mesh_field = meshed_region.field_of_properties(dpf.common.nodal_properties.coordinates)

    disp = model.results.displacement(time_scoping=i).eval()
    op = dpf.operators.math.add()
    my_fieldA = dpf.Field()
    my_fieldA.location = locations.nodal
    op.inputs.fieldA.connect(Mesh_field)
    my_fieldB = dpf.Field()
    my_fieldB.location = locations.nodal
    op.inputs.fieldB.connect(disp[0])
    result_field = op.outputs.field()
    mesh = model.metadata.meshed_region.grid

    plotter.add_mesh(
    mesh,
    lighting=False,
    show_edges=True,
    scalar_bar_args={"title": "Damage"},
    clim=[0, 1],
    opacity=0.3)
    plotter.update_coordinates(result_field.data)
    model.metadata.meshed_region.plot(damage_value, opacity=0.3, scalar_bar_args={"title": "Damage"},
        clim=[0, 1])
    plotter.write_frame()
