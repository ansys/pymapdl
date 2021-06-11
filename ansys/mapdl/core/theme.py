"""Store parameters for a PyMAPDL-specific theme for pyvista"""
from pyvista import themes


class MapdlTheme(themes.DefaultTheme):
    """PyMAPDL-specific theme for pyvista."""

    def __init__(self):
        """Initialize the theme."""
        super().__init__()
        self.cmap = 'jet'
        self.interactive = True
        self.font.family = "courier"
        self.title = "pyansys"
