# Script to calculate the first natural frequecy of
# a rotor for a given set of properties

# Importing packages
import numpy as np

from ansys.mapdl.core import launch_mapdl

# Launching MAPDL
mapdl = launch_mapdl(port=50052)
mapdl.clear()
mapdl.prep7()

# Input properties
n_blades = 4
blade_length = 1

elastic_modulus = 200e9  # N/m2
density = 7850  # kg/m3

# Other properties
center_radious = 0.5
blade_thickness = 0.1
section_length = 0.5


## Material definition
# Material 1: Steel
mapdl.mp("NUXY", 1, 0.31)
mapdl.mp("DENS", 1, density)
mapdl.mp("EX", 1, elastic_modulus)

## Geometry
# Plotting center
area_cyl = mapdl.cyl4(0, 0, center_radious)

# define path for dragging
k0 = mapdl.k(x=0, y=0, z=0)
k1 = mapdl.k(x=0, y=0, z=section_length)

line_path = mapdl.l(k0, k1)

mapdl.vdrag(area_cyl, nlp1=line_path)
center_vol = mapdl.geometry.vnum[0]

complex = False
if complex:
    # Creating pline
    precision = 10
    advance = 0.1

    spline = []
    for i in range(precision + 1):
        if i != 0:
            k0 = mapdl.k("", x_, y_, z_)
        angle_ = i * (360 / n_blades) / precision
        x_ = section_length * np.cos(np.deg2rad(angle_))
        y_ = section_length * np.sin(np.deg2rad(angle_))
        z_ = 0.1 * i

        if i != 0:
            k1 = mapdl.k("", x_, y_, z_)
            spline.append(mapdl.l(k0, k1))

    mapdl.spline(*spline)

    # dragging
    point_0 = mapdl.k("", center_radious * 0.95, -blade_thickness / 2, 0)
    point_1 = mapdl.k("", center_radious + blade_length, -blade_thickness / 2, 0)
    point_2 = mapdl.k("", center_radious + blade_length, blade_thickness / 2, 0)
    point_3 = mapdl.k("", center_radious, blade_thickness / 2, 0)
    blade_area = mapdl.a(point_0, point_1, point_2, point_3)

    mapdl.vdrag(
        blade_area,
        nlp1=spline[0],
        nlp2=spline[1],
        nlp3=spline[2],
        nlp4=spline[3],
        nlp5=spline[4],
    )

else:
    point_0 = mapdl.k("", center_radious * 0.95, -blade_thickness / 2, 0)
    point_1 = mapdl.k("", center_radious + blade_length, -blade_thickness / 2, 0)
    point_2 = mapdl.k("", center_radious + blade_length, blade_thickness / 2, 0)
    point_3 = mapdl.k("", center_radious, blade_thickness / 2, 0)
    blade_area = mapdl.a(point_0, point_1, point_2, point_3)

    mapdl.vdrag(blade_area, nlp1=line_path)

blade_volu = 2

# Cutting blade and circle.
mapdl.vsbv(blade_volu, center_vol, keep2="keep")
blade_volu = 3

# Symmetry
mapdl.csys(1)  # switching to cylindrical
mapdl.vgen(n_blades, blade_volu, dy=360 / n_blades, imove=0)

# glueing
mapdl.vglue("all")
center_vol = mapdl.geometry.vnum[-1]

# Meshing
mapdl.allsel()
mapdl.et(1, "SOLID186")
mapdl.vsweep("all")

# Applying loads
mapdl.vsel("s", vmin=center_vol)
mapdl.eslv("S")
mapdl.nsle("r")
mapdl.nsel("r", "loc", "z", 0)
mapdl.d("all", "ux", 0)
mapdl.d("all", "uy", 0)
mapdl.d("all", "uz", 0)

# Solving
mapdl.allsel()
mapdl.slashsolu()
nmodes = 10  # Get the first 10 modes
output = mapdl.modal_analysis(nmode=nmodes)

mapdl.post1()
modes = mapdl.set("list").to_array()
freqs = modes[:, 1]

# Output values
first_frequency = freqs[0]
print(f"The first natural frequency is {first_frequency} Hz.")
