"""pymapdl examples"""
import os

from matplotlib.colors import ListedColormap
import numpy as np

from ansys.mapdl.core.examples.verif_files import vmfiles

# get location of this folder and the example files
dir_path = os.path.dirname(os.path.realpath(__file__))

# add any files you'd like to import here.  For example:
wing_model = os.path.join(dir_path, "wing.dat")

# Canonical Examples
static_thermal_example = vmfiles["vm5"]
static_coupled_thermal = vmfiles["vm33"]
modal_piezoelectric = vmfiles["vm175"]
harmonic_piezoelectric = vmfiles["vm176"]
shell_static_example = vmfiles["vm6"]
static_electro_thermal_compliant_microactuator = vmfiles["vm223"]
static_piezoelectric = vmfiles["vm231"]


# be sure to add the input file directly in this directory
# This way, files can be loaded with:
# from ansys.mapdl.core import examples
# examples.wing_model


def ansys_colormap():
    """Return the default ansys color map made of 9 colours (blue-green-red)."""
    colors = (
        np.array(
            [
                [0, 0, 255],
                [0, 178, 255],
                [0, 255, 255],
                [0, 255, 178],
                [0, 255, 0],
                [178, 255, 0],
                [255, 255, 0],
                [255, 178, 0],
                [255, 0, 0],
            ],
            dtype=float,
        )
        / 255
    )
    return ListedColormap(colors)
