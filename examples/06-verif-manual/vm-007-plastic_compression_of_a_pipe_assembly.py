r"""
.. _ref_vm7_example:

Plastic Compression of a Pipe Assembly
--------------------------------------
Problem Description:
 - Two coaxial tubes, the inner one of 1020 CR steel and cross-sectional area As,
   and the outer one of 2024-T4 aluminum alloy and of area Aa, are compressed
   between heavy, flat end plates, as shown below. Determine the load-deflection
   curve of the assembly as it is compressed into the plastic region by
   an axial displacement. Assume that the end plates are so stiff that both tubes
   are shortened by exactly the same amount.

Reference:
 - S. H. Crandall, N. C. Dahl, An Introduction to the Mechanics of Solids, McGraw-Hill
   Book Co., Inc., New York, NY, 1959, pg. 180, ex. 5.1.

Analysis Type(s):
 - Static, Plastic Analysis (``ANTYPE=0``)

Element Type(s):
 - Plastic Straight Pipe Element (PIPE288)
 - 4-Node Finite Strain Shell (SHELL181)
 - 3-D Structural Solid Elements (SOLID185)

.. image:: ../../_static/vm7_setup.png
   :width: 400
   :alt: VM7 Problem Sketch

.. image:: ../../_static/vm7_setup_2.png
   :width: 400
   :alt: VM7 Finite Element Models

Material Properties
 -

Geometric Properties:
 -

Loading:
 - 1st Load Step: :math:`\delta = 0.032 in`
 - 2nd Load Step: :math:`\delta = 0.050 in`
 - 3rd Load Step: :math:`\delta = 0.100 in`

Analysis Assumptions and Modeling Notes:
 - The following tube dimensions, which provide the desired cross-sectional areas,
   are arbitrarily chosen. Inner (steel) tube: inside radius = 1.9781692 in.,
   wall thickness = 0.5 in. Outer (aluminum) tube: inside radius = 3.5697185 in.,
   wall thickness = 0.5 in.

 - The problem can be solved in three ways:
   • using PIPE288 - the plastic straight pipe element
   • using SOLID185 - the 3-D structural solid element
   • using SHELL181 - the 4-Node Finite Strain Shell

 - In the SOLID185 and SHELL181 cases, since the problem is axisymmetric, only a one
   element -sector is modeled. A small angle  = 6° is arbitrarily chosen to
   reasonably approximate the circular boundary with straight sided elements.
   The nodes at the boundaries have the UX (radial) degree of freedom coupled.
   In the SHELL181 model, the nodes at the boundaries additionally
   have the ROTY degree of freedom coupled.

"""
# sphinx_gallery_thumbnail_path = '_static/vm7_setup.png'

###############################################################################
# Start MAPDL
# ~~~~~~~~~~~

from ansys.mapdl.core import launch_mapdl

# Start mapdl.
mapdl = launch_mapdl()


###############################################################################
# Initiate Pre-Processing
# ~~~~~~~~~~~~~~~~~~~~~~~
# Enter verification example mode and the pre-processing routine.

def start_prep7():
    mapdl.clear()
    mapdl.verify()
    mapdl.prep7()


start_prep7()


###############################################################################
# Parameterization
# ~~~~~~~~~~~~~~~~

# Angle of the model sector.
theta = 6

# Deflection load steps.
defl_ls1 = -0.032
defl_ls2 = -0.05
defl_ls3 = -0.1

# Quantity of the load steps.
ls = 3


###############################################################################
# Define Element Type
# ~~~~~~~~~~~~~~~~~~~
# Set up the element types .

# Element type PIPE288.
mapdl.et(1, "PIPE288")

# Special Features are defined by keyoptions of shell element.
# KEYOPT(4)(2)
# Hoop strain treatment:
# Thick pipe theory.
mapdl.keyopt(1, 4, 2)  # Cubic shape function

# Element type SOLID185.
mapdl.et(2, "SOLID185")

# Element type SHELL181.
mapdl.et(3, "SHELL181")  # FULL INTEGRATION

# Special Features are defined by keyoptions of shell element.
# KEYOPT(3)(2)
# Integration option:
# Full integration with incompatible modes.
mapdl.keyopt(3, 3, 2)


###############################################################################
# Define Material
# ~~~~~~~~~~~~~~~
# Set up the material properties, where:
# Young Modulus is :math:`E = ... \cdot 10^6 psi`,
# Poisson's ratio is :math:`Nu = ...`.

# STEEL material model.
# Define Young's moulus and Poisson ratio for Steel.
mapdl.mp("EX", 1, 26.875E6)
mapdl.mp("PRXY", 1, 0.3)

# Define non-linear material properties for Steel.
mapdl.tb("BKIN", 1, 1)
mapdl.tbtemp(0)
mapdl.tbdata(1, 86000, 0)


# ALUMINUM material model.
# Define Young's moulus and Poisson ratio for Aluminium.
mapdl.mp("EX", 2, 11E6)
mapdl.mp("PRXY", 2, 0.3)

# Define non-linear material properties for Aluminium.
mapdl.tb("BKIN", 2, 1)
mapdl.tbtemp(0)
mapdl.tbdata(1, 55000, 0)


###############################################################################
# Plot Stress - Strain Curve.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as plt

# Define Stress - Strain properties of the steel.
steel = {"stress_s": [0, 86000, 86000, 86000],
         "strain_s": [0, 0.032, 0.1, 0.2]}

# Define Stress - Strain point of the steel on the curve.
Xp = steel["strain_s"][1]
Yp = steel["stress_s"][1]

# Set up the settings of the graph.
plt.plot(steel["strain_s"], steel["stress_s"],
         label="1020 CR STEEL", linewidth=2,
         color='steelblue', linestyle="-", marker="o")
plt.plot(Xp, Yp, marker='o')

plt.annotate('sigma_y_steel', xy=(0.032, 86000), xytext=(0.05, 75000),
             arrowprops=dict(facecolor='steelblue', shrink=0.05),
             bbox=dict(facecolor='steelblue', edgecolor='black', boxstyle='round,pad=1'))


# Define dictionary with stress - strain properties of the aluminium.
aluminium = {"stress_a": [0, 55000, 55000, 55000],
             "strain_a": [0, 0.05, 0.1, 0.2]}

Xp = aluminium["strain_a"][1]
Yp = aluminium["stress_a"][1]

# Set up the settings of the graph.
plt.plot(aluminium["strain_a"], aluminium["stress_a"],
         label="2024-T4 ALUMINIUM", linewidth=2,
         color='sandybrown', linestyle="-", marker="o")
plt.plot(Xp, Yp, marker='o')

plt.annotate('sigma_y_aluminium', xy=(Xp, Yp), xytext=(0.07, 45000),
             arrowprops=dict(facecolor='sandybrown', shrink=0.05),
             bbox=dict(facecolor='sandybrown', edgecolor='black', boxstyle='round,pad=1'))


plt.grid(True)
plt.legend()
plt.title("Stress - Strain Curve", fontsize=18)
plt.show()


###############################################################################
# Define Section
# ~~~~~~~~~~~~~~
# Set up the cross-section properties for a shell element.

# Shell cross-section for inside (STEEL) tube.
mapdl.sectype(1, "SHELL")

# THICKNESS (SHELL181)
mapdl.secdata(0.5, 1, 0, 5)


# Shell cross-section for outside (ALUMINUM) tube.
mapdl.sectype(2, "SHELL")

# THICKNESS (SHELL181)
mapdl.secdata(0.5, 2, 0, 5)


# Define Pipe cross-section for inside (STEEL) tube, where:
mapdl.sectype(3, "PIPE")

# OUTSIDE DIA. AND WALL THICKNESS FOR INSIDE TUBE (PIPE288)
mapdl.secdata(4.9563384, 0.5)


# Pipe cross-section for outside (ALUMINUM) tube.
mapdl.sectype(4, "PIPE")

# OUTSIDE DIA. AND WALL THICKNESS FOR OUTSIDE TUBE (PIPE288)
mapdl.secdata(8.139437, 0.5)


###############################################################################
# Define Geometry
# ~~~~~~~~~~~~~~~
# Set up the keypoints and create the area through the keypoints.

# GENERATE NODES AND ELEMENTS FOR PIPE288
mapdl.n(1, x=0, y=0, z=0)
mapdl.n(2, x=0, y=0, z=10)

# Create element for steel(inside) tube cross-section.
mapdl.mat(1)
mapdl.secnum(3)
mapdl.e(1, 2)

# Create element for aluminium(outside) tube cross-section.
mapdl.mat(2)
mapdl.secnum(4)
mapdl.e(1, 2)

# Activate the global cylindrical coordinate system.
mapdl.csys(1)

# GENERATE NODES AND ELEMENTS FOR SOLID185
mapdl.n(node=101, x=1.9781692)
mapdl.n(node=102, x=2.4781692)
mapdl.n(node=103, x=3.5697185)
mapdl.n(node=104, x=4.0697185)
mapdl.n(node=105, x=1.9781692, z=10)
mapdl.n(node=106, x=2.4781692, z=10)
mapdl.n(node=107, x=3.5697185, z=10)
mapdl.n(node=108, x=4.0697185, z=10)
mapdl.ngen(itime=2, inc=10, node1=101, node2=108, dy=theta)  # GENERATE 2ND SET OF NODES TO FORM A THETA DEGREE SLICE
mapdl.nrotat(node1=101, node2=118, ninc=1)

# INSIDE (STEEL) TUBE
mapdl.type(2)
mapdl.mat(1)
mapdl.e(101, 102, 112, 111, 105, 106, 116, 115)

# OUTSIDE (ALUMINUM) TUBE
mapdl.mat(2)
mapdl.e(103, 104, 114, 113, 107, 108, 118, 117)

# GENERATE NODES AND ELEMENTS FOR SHELL181
mapdl.n(node=201, x=2.2281692)
mapdl.n(node=203, x=2.2281692, z=10)
mapdl.n(node=202, x=3.8197185)
mapdl.n(node=204, x=3.8197185, z=10)

# GENERATE NODES TO FORM A THETA DEGREE SLICE
mapdl.ngen(itime=2, inc=4, node1=201, node2=204, dy=theta)

# INSIDE (STEEL) TUBE
mapdl.type(3)
mapdl.secnum(1)
mapdl.e(203, 201, 205, 207)

# OUTSIDE (ALUMINUM) TUBE
mapdl.secnum(2)
mapdl.e(204, 202, 206, 208)

# plot elements
cpos = [(19.67899462804619, 17.856836088414664, 22.644135378046194),
        (2.03485925, 0.21270071036846988, 5.0),
        (0.0, 0.0, 1.0)]
mapdl.eplot(cpos=cpos)


###############################################################################
# Define Boundary Conditions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Application of symmetric boundary conditions for simplified model.

mapdl.run("C*** APPLY CONSTRAINTS TO PIPE288 MODEL")

mapdl.d(node=1, lab="ALL")  # FIX ALL DOFS FOR BOTTOM END OF PIPE288
mapdl.d(node=2, lab="UX", lab2="UY", lab3="ROTX", lab4="ROTY", lab5="ROTZ")  # ALLOW ONLY UZ DOF AT TOP END OF PIPE288 MODEL

mapdl.run("C*** APPLY CONSTRAINTS TO SOLID185 AND SHELL181 MODELS")

mapdl.cp(nset=1, lab="UX", node1=101, node2=111, node3=105, node4=115)  # COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SOLID185
mapdl.cpsgen(itime=4, nset1=1)

mapdl.cp(5, lab="UX", node1=201, node2=205, node3=203, node4=20)  # COUPLE NODES AT BOUNDARY IN RADIAL DIR FOR SHELL181
mapdl.cpsgen(itime=2, nset1=5)

mapdl.cp(7, lab="ROTY", node1=201, node2=205)  # COUPLE NODES AT BOUNDARY IN ROTY DIR FOR SHELL181
mapdl.cpsgen(itime=4, nset1=7)

mapdl.nsel("S", "NODE", "", 101, 212)  # SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
mapdl.nsel("R", "LOC", "Y", 0)  # SELECT NODES AT THETA = 0 FROM THE SELECTED SET
mapdl.dsym("SYMM", "Y", 1)  # APPLY SYMMETRY BOUNDARY CONDITIONS
mapdl.nsel("S", "NODE", "", 101, 212)  # SELECT ONLY NODES IN SOLID185 AND SHELL181 MODELS
mapdl.nsel("R", "LOC", "Y", theta)  # SELECT NODES AT THETA FROM THE SELECTED SET

mapdl.dsym("SYMM", "Y", 1)  # APPLY SYMMETRY BOUNDARY CONDITIONS

mapdl.nsel("ALL")
mapdl.nsel("R", "LOC", "Z", 0)  # SELECT ONLY NODES AT Z = 0

mapdl.d("ALL", "UZ", 0)  # CONSTRAIN BOTTOM NODES IN Z DIRECTION

mapdl.nsel("ALL")
mapdl.finish()

###############################################################################
# Solve
# ~~~~~
# Enter solution mode and solve the system. Print the solver output.

# Start solution presederu
mapdl.run("/SOLU")

# Define solution function.
def solution(deflect=None):
    mapdl.nsel("R", "LOC", "Z", 10)
    mapdl.d(node="ALL", lab="UZ", value=deflect)
    mapdl.nsel("ALL")
    mapdl.solve()


# Run each load step to reproduce needed deflection subsequently.
# Load Step 1
solution(deflect=defl_ls1)

# Load Step 2
solution(deflect=defl_ls2)

# Load Step 3
solution(deflect=defl_ls3)
mapdl.finish()


###############################################################################
# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processing.

# Enter the post-processing routine
mapdl.run("/OUT,")
mapdl.post1()


###############################################################################
# Define loads.
# ~~~~~~~~~~~~~
# Set up the function.

def getload():
    ####
    # Select the nodes in the PIPE288 element model.
    mapdl.nsel("S", "NODE", "", 1, 2)
    mapdl.nsel("R", "LOC", "Z", 0)
    mapdl.run("/OUT,SCRATCH")

    # Sum the nodal force contributions of elements.
    mapdl.fsum()

    # Extrapolation of the force results in the full 360 (deg) model.
    load_288 = mapdl.get_value("FSUM", 0, "ITEM", "FZ")

    ####
    # Select the nodes in the SOLID185 element model.
    mapdl.nsel("S", "NODE", "", 101, 118)
    mapdl.nsel("R", "LOC", "Z", 0)
    mapdl.fsum()

    # Get the force value of the simplified model.
    load_185_theta = mapdl.get_value("FSUM", 0, "ITEM", "FZ")

    # Extrapolation of the force results in the full 360 (deg) model.
    load_185 = load_185_theta * 360 / theta
    mapdl.run("*STATUS,LOAD")

    ####
    # Select the nodes in the SHELL181 element model.
    mapdl.nsel("S", "NODE", "", 201, 212)  # SELECT NODES IN SHELL181 MODEL
    mapdl.nsel("R", "LOC", "Z", 0)

    # Sum the nodal force contributions of elements.
    mapdl.fsum()
    mapdl.run("/OUT,")

    # Get the force value of the simplified model.
    load_181_theta = mapdl.get_value("FSUM", 0, "ITEM", "FZ")

    # Extrapolation of the force results in the full 360 (deg) model.
    load_181 = load_181_theta * 360 / theta
    mapdl.run("*STATUS,LOAD")

    # Return load results of each element model.
    return load_288, load_185, load_181


###############################################################################
# Define loads for load step 1

for i in range(1, ls + 1):
    mapdl.set(1, 1)
    load_288, load_185, load_181 = getload()
    results_load_deflection = f"""
    LOAD STEP {i}
    PIPE288_LS{i}= {abs(round(load_288,0))}
    SOLID185_LS{i} = {abs(round(load_185,0))}
    SHELL181_LS{i} = {abs(round(load_181,0))}
    
    """
    print(results_load_deflection)


###############################################################################
# Check Results with Pandas


# ###############################################################################
# # Check Results
# # ~~~~~~~~~~~~~
# # Now we have the deflections, we can compare them to the expected values
# # of radial deflection at the node where force :math:`F` was applied
# # for both simulations. The expected value for :math:`\delta_{\mathrm{shell181}}` is 0.1139,
# # and :math:`\delta_{\mathrm{shell281}}` is 0.1139.
#
#
# deflect_shell_181 = 0
# deflect_shell_281 = 0
# # Results obtained by hand-calculations.
# deflect_target_181 = 0.1139
# deflect_target_281 = 0.1139
#
# # Calculate the deviation.
# deflect_ratio_shell_181 = abs(deflect_shell_181) / deflect_target_181
# deflect_ratio_shell_281 = abs(deflect_shell_281) / deflect_target_281
#
# # Print output results.
# output = f"""
# ----------------------------------------------------------------------------
# ------------------------- VM3 RESULTS COMPARISON ---------------------------
# ----------------------------------------------------------------------------
#                             |   TARGET   |   Mechanical APDL   |   RATIO   |
# ----------------------------------------------------------------------------
#     Deflection, in SHELL181{deflect_target_181:11.4f} {abs(deflect_shell_181):17.4f} {deflect_ratio_shell_181:15.4f}
#     Deflection, in SHELL281{deflect_target_281:11.4f} {abs(deflect_shell_281):17.4f} {deflect_ratio_shell_281:15.4f}
# ----------------------------------------------------------------------------
# """
# print(output)
