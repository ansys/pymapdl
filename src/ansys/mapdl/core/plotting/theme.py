# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Store parameters for a PyMAPDL-specific theme for PyVista"""

import numpy as np

try:
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap

    _HAS_MATPLOTLIB = True
except ModuleNotFoundError:
    _HAS_MATPLOTLIB = False


from ansys.mapdl.core import _HAS_PYVISTA

if _HAS_PYVISTA:
    from cycler import Cycler
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


def get_ansys_cmap(N: int = 9) -> "LinearSegmentedColormap":
    """Returns a Matplotlib colormap of given length.

    Returns a Matplotlib colormap which is the result of interpolate the MAPDL
    colormap to obtain a colormap of a given number of colors.

    Parameters
    ----------
    N : int, optional
        Number of colours, by default 9

    Returns
    -------
    matplotlib.colors.LinearSegmentedColormap
        Colormap
    """
    return LinearSegmentedColormap.from_list("PyMAPDL", MAPDL_colorbar.tolist(), N=N)


def get_ansys_colors(N: int = 9) -> np.array:
    """Get N number of colors as array.

    Obtain N unique colors as a Numpy array (N x 4). Transparency is included.
    This function uses `get_ansys_cmap` to interpolate between the colors given
    in `PyMAPDL_cmap`.

    Parameters
    ----------
    N : int, optional
        Number of colors, by default 9

    Returns
    -------
    np.array
        Color array

    Raises
    ------
    ModuleNotFoundError
        Matplotlib can not be found.
    """
    if not _HAS_MATPLOTLIB:
        raise ModuleNotFoundError(
            "'matplotlib' package is needed for 'get_ansys_colors'."
        )

    cmap = get_ansys_cmap(N=N)
    return cmap([i for i in range(N)])


def get_ansys_color_cycle(N: int = 9) -> np.array:
    """Get a color cycler

    Give an array of N colors which is the result of cycling through the MAPDL
    colormap. Only m unique colors can be provided through this function, where
    m is the minimal of 9 or N.

    Parameters
    ----------
    N : int, optional
        Number of colors, by default 9

    Returns
    -------
    np.array
        Array of colors
    """
    from cycler import cycler

    cyc_ = cycler(color=MAPDL_colorbar.tolist())()
    return np.array([each["color"] for i, each in zip(range(N), cyc_)])


class MapdlTheme(Theme):
    """Provides the PyMAPDL-specific theme for PyVista.

    The theme includes these defaults:

    - PyMAPDL colormap as default colormap.
    - ``'Courier'`` font family for an interactive plot
    - ``'PyMAPDL'`` for the title of an interactive plot

    Examples
    --------
    Create a custom theme with unique parameters from the ``MapdlTheme`` base.

    >>> from ansys.mapdl import core as pymapdl
    >>> my_theme = pymapdl.MapdlTheme()
    >>> my_theme.background = 'white'
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

        self.name: str = "PyMAPDL-Theme"
        self.title: str = "PyMAPDL"
        self.background: str = "paraview"
        self.interactive: bool = True

        if _HAS_MATPLOTLIB:
            self.cmap = PyMAPDL_cmap
        self.font.family: str = "arial"

        self.font.size: int = 18
        self.font.title_size: int = 18
        self.font.label_size: int = 18
        self.font.color: str = "black"

        self.axes.x_color: str = "tomato"
        self.axes.y_color: str = "seagreen"
        self.axes.z_color: str = "blue"

        self.show_edges: bool = False
        self.color: str = "lightblue"
        self.outline_color: str = "black"
        self.edge_color: str = "black"

        self.color_cycler: Cycler = get_cycler(MAPDL_colorbar.tolist())
        self.render_points_as_spheres: bool = True


def _apply_default_theme():
    import pyvista as pv

    pv.global_theme = MapdlTheme()
