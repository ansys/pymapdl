# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

from typing import TYPE_CHECKING, Any

import numpy as np

from ansys.mapdl.core import _HAS_MATPLOTLIB, _HAS_PYVISTA

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
    from matplotlib.colors import ListedColormap

    PyMAPDL_cmap: ListedColormap = ListedColormap(MAPDL_colorbar, name="PyMAPDL")

if _HAS_PYVISTA:
    from ansys.tools.versioning.utils import version_string_as_tuple  # type: ignore
    from cycler import Cycler
    from pyvista import __version__ as pyvista_version
    from pyvista.plotting.colors import get_cycler  # type: ignore

    version = version_string_as_tuple(pyvista_version)

    if version[1] >= 41:
        from pyvista.plotting.themes import Theme  # type: ignore
    elif version[1] >= 40:
        from pyvista.themes import Theme  # type: ignore
    else:
        from pyvista.themes import DefaultTheme as Theme  # type: ignore

else:  # pragma: no cover
    from dataclasses import dataclass

    @dataclass
    class Font:
        """Font class for PyVista theme."""

        family: str = "arial"
        size: int = 18
        title_size: int = 18
        label_size: int = 18
        color: str = "black"

    @dataclass
    class Axes:
        """Axes class for PyVista theme."""

        x_color: str = "tomato"
        y_color: str = "seagreen"
        z_color: str = "blue"

    @dataclass
    class Theme:  # type: ignore
        name: str = "PyMAPDL-Theme"
        title: str = "PyMAPDL"
        background: str = "paraview"
        interactive: bool = True
        cmap: Any = None
        font = Font()
        axes = Axes()

        show_edges: bool = False
        color: str = "lightblue"
        outline_color: str = "black"
        edge_color: str = "black"
        color_cycler: Any = None
        render_points_as_spheres: bool = True


if _HAS_MATPLOTLIB and TYPE_CHECKING:
    from matplotlib.colors import LinearSegmentedColormap


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

    Raises
    ------
    ModuleNotFoundError
        If matplotlib is not installed.
    """
    if not _HAS_MATPLOTLIB:
        raise ModuleNotFoundError(
            "'matplotlib' package is needed for 'get_ansys_cmap'."
        )
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list("PyMAPDL", MAPDL_colorbar.tolist(), N=N)


def get_ansys_colors(N: int = 9) -> np.ndarray[Any, Any]:
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
    return np.array(cmap([i for i in range(N)]), dtype=np.float64)


def get_ansys_color_cycle(N: int = 9) -> np.ndarray[Any, Any]:
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
    return np.array([each["color"] for _, each in zip(range(N), cyc_)])


class MapdlTheme(Theme):  # type: ignore
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

    def __init__(self) -> None:  # type: ignore
        """Initialize the theme."""
        super().__init__()

        self.name: str = "PyMAPDL-Theme"
        self.title: str = "PyMAPDL"
        self.background: str = "paraview"
        self.interactive: bool = True

        if _HAS_MATPLOTLIB:
            self.cmap = PyMAPDL_cmap

        self.font.family: str = "arial"  # type: ignore

        self.font.size: int = 18  # type: ignore
        self.font.title_size: int = 18  # type: ignore
        self.font.label_size: int = 18  # type: ignore
        self.font.color: str = "black"  # type: ignore

        self.axes.x_color: str = "tomato"  # type: ignore
        self.axes.y_color: str = "seagreen"  # type: ignore
        self.axes.z_color: str = "blue"  # type: ignore

        self.show_edges: bool = False
        self.color: str = "lightblue"
        self.outline_color: str = "black"
        self.edge_color: str = "black"

        self.color_cycler: Cycler = get_cycler(MAPDL_colorbar.tolist())  # type: ignore
        self.render_points_as_spheres: bool = True


def _apply_default_theme() -> None:
    import pyvista as pv

    pv.global_theme = MapdlTheme()
