# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Store parameters for a PyMAPDL-specific theme for pyvista"""

import numpy as np

try:
    from matplotlib.colors import ListedColormap

    _HAS_MATPLOTLIB = True
except ModuleNotFoundError:
    _HAS_MATPLOTLIB = False


from ansys.mapdl.core import _HAS_PYVISTA

if _HAS_PYVISTA:
    from pyvista.plotting.colors import get_cycler

    try:
        from pyvista.plotting.themes import Theme

    except ImportError:
        from pyvista import __version__ as pyvista_version

        if "0.40" in pyvista_version:
            from pyvista.themes import Theme
        else:  # older versions
            from pyvista.themes import DefaultTheme as Theme

else:  # pragma: no cover

    class Theme:
        pass


MAPDL_colorbar = (
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

if _HAS_MATPLOTLIB:
    PyMAPDL_cmap: ListedColormap = ListedColormap(MAPDL_colorbar, name="PyMAPDL")


def get_ansys_colors(N=9):
    if not _HAS_MATPLOTLIB:
        raise ModuleNotFoundError(
            "'matplotlib' package is needed for 'get_ansys_colors'."
        )
    return np.array([PyMAPDL_cmap(i) for i in range(N)])


class MapdlTheme(Theme):
    """PyMAPDL-specific theme for Pyvista.

    Examples
    --------
    Create a custom theme with unique parameters from the base MapdlTheme.

    >>> from ansys.mapdl import core as pymapdl
    >>> my_theme = pymapdl.MapdlTheme()
    >>> my_theme.background = 'white'
    >>> my_theme.cmap = 'jet'  # colormap
    >>> my_theme.axes.show = False
    >>> my_theme.show_scalar_bar = False

    Apply this theme to element plotting.

    >>> mapdl.eplot(theme=theme)

    Apply this theme to area plotting.

    >>> mapdl.aplot(theme=theme)

    """

    def __init__(self):
        """Initialize the theme."""
        super().__init__()

        self.name = "PyMAPDL-Theme"
        self.title = "PyMAPDL"
        self.background = "paraview"
        self.interactive = True

        if _HAS_MATPLOTLIB:
            self.cmap = PyMAPDL_cmap

        self.font.size = 18
        self.font.title_size = 18
        self.font.label_size = 18
        self.font.color = "black"
        self.font.family = "arial"

        self.axes.x_color = "tomato"
        self.axes.y_color = "seagreen"
        self.axes.z_color = "blue"

        self.show_edges = False
        self.color = "lightblue"
        self.outline_color = "black"
        self.edge_color = "black"

        self.color_cycler = get_cycler(MAPDL_colorbar.tolist())
        self.render_points_as_spheres = True


def _apply_default_theme():
    import pyvista as pv

    pv.global_theme = MapdlTheme()
