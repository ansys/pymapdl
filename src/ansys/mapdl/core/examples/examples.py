"""pymapdl examples"""
import os

from matplotlib.colors import ListedColormap
import numpy as np

# get location of this folder and the example files
dir_path = os.path.dirname(os.path.realpath(__file__))

# add any files you'd like to import here.  For example:
wing_model = os.path.join(dir_path, "wing.dat")

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
