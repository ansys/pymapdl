# Script to calculate the first natural frequecy of a rotor for a given set of properties
import click

# Importing packages
from ansys.mapdl.core import Mapdl


@click.command()
@click.argument(
    "n_blades",
)  # arguments are mandatory
@click.option("--blade_length", default=0.2, help="Length of each blade.")  # optionals
@click.option(
    "--elastic_modulus", default=200e9, help="Elastic modulus of the material."
)
@click.option("--density", default=7850, help="Density of the material.")
def main(n_blades, blade_length, elastic_modulus, density):
    print(
        "Initializing script with values:\n"
        f"Number of blades: {n_blades}\nBlade length: {blade_length} m\n"
        f"Elastic modulus: {elastic_modulus/1E9} GPa\nDensity: {density} Kg/m3"
    )
    # Launching MAPDL
    mapdl = Mapdl(port=50052)
    mapdl.clear()
    mapdl.prep7()

    # Converting input properties
    n_blades = float(n_blades)

    # Other properties
    center_radious = 0.1
    blade_thickness = 0.05
    section_length = 0.1

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

    mapdl.vplot(savefig="volumes.jpg")

    # Meshing
    mapdl.allsel()
    mapdl.et(1, "SOLID186")
    mapdl.esize(0.01)
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
    print("Solving...")
    output = mapdl.modal_analysis(nmode=nmodes)

    mapdl.post1()
    modes = mapdl.set("list").to_array()
    freqs = modes[:, 1]

    # Output values
    first_frequency = freqs[0]
    print(f"The first natural frequency is {first_frequency} Hz.")


if __name__ == "__main__":
    main()
