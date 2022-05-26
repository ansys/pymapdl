"""Store parameters for a PyMAPDL-specific theme for pyvista"""
from ansys.mapdl.core import _HAS_PYVISTA

if _HAS_PYVISTA:
    from pyvista import themes

    base_class = themes.DefaultTheme

else:  # pragma: no cover

    class myEmptyClass:
        pass

    base_class = myEmptyClass


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
        self.cmap = "jet"
        self.interactive = True
        self.font.family = "courier"
        self.title = "PyMAPDL"
