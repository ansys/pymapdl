"""Store parameters for a PyMAPDL-specific theme for pyvista"""
from matplotlib.colors import ListedColormap
import numpy as np

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

    base_class = Theme

else:  # pragma: no cover

    class myEmptyClass:
        pass

    base_class = myEmptyClass


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

PyMAPDL_cmap: ListedColormap = ListedColormap(MAPDL_colorbar, name="PyMAPDL", N=255)


def get_ansys_colors(N=9):
    return np.array([PyMAPDL_cmap(i) for i in range(N)])


class MapdlTheme(base_class):
    """PyMAPDL-specific theme for pyvista.

    Theme includes the following defaults:

    - ``'jet'`` (rainbow) colormap
    - Interactive plots
    - ``'Courier'`` for the font family
    - ``'PyMAPDL'`` as the plot title

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

        self.cmap = PyMAPDL_cmap

        self.font.size = 18
        self.font.title_size = 18
        self.font.label_size = 18
        self.font.color = "black"
        self.show_edges = False
        self.color = "lightblue"
        self.outline_color = "black"
        self.edge_color = "black"

        self.axes.x_color = "tomato"
        self.axes.y_color = "seagreen"
        self.axes.z_color = "blue"

        self.color_cycler = get_cycler(MAPDL_colorbar.tolist())
        self.render_points_as_spheres = True


def _apply_default_theme():
    import pyvista as pv

    pv.global_theme = MapdlTheme()
