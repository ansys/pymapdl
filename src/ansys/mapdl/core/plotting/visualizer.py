"""Module for the MapdlPlotter class."""
from ansys.visualizer import MeshObjectPlot, PlotterInterface
from beartype.typing import Any, Iterable
import pyvista as pv

from ansys.mapdl.core.plotting.theme import MapdlTheme


class MapdlPlotter(PlotterInterface):
    """Plotter class for PyMapdl.
    
    This class is an implementation of the PlotterInterface class from the ansys-visualizer package.
    Picker is implemented in PyMAPDL specific classes due to the characteristics of the library.

    Parameters
    ----------
    use_trame : bool, optional
        Whether to use the trame interface or not, by default False.
    theme : pv.DefaultTheme, optional
        _description_, by default None
    """
    def __init__(self, use_trame: bool = False, theme: pv.Plotter.Theme = None, **plotter_kwargs):
        """Initialize the MapdlPlotter class."""

        super().__init__(use_trame, plot_picked_names=True, **plotter_kwargs)
        self._theme = theme
        if theme is None:
            self._theme = MapdlTheme()        
    
    def add_labels(self, points: List[float], labels: List[str], **plotting_options) -> None:
        """Add labels to the plotter.

        Parameters
        ----------
        points : List[float]
            List of points of the labels.
        labels : List[str]
            List of labels to be added.
        """
        _ = self.pv_interface.scene.add_point_labels(points, labels, **plotting_options)
    
    def add_points(self, points: List[float], **plotting_options) -> None:
        """Add points to the plotter.

        Parameters
        ----------
        points : List[float]
            List of points to be added to the plotter.
        """
        _ = self.pv_interface.scene.add_points(points, **plotting_options)
    
    def add_iter(
        self,
        plotting_list: Iterable[Any],
        filter: str = None,
        **plotting_options,
    ) -> None:
        """Add a list of objects to the plotter.

        Parameters
        ----------
        plotting_list : Iterable[Any]
            Iterable of objects to be added to the plotter.
        filter : str, optional
            Filter to be applied to the objects, by default None.
        """
        for object in plotting_list:
            _ = self.add(object, filter, **plotting_options)
            
    def add(self, object: Any, filter: str = None, **plotting_options) -> None:
        """Add an object to the plotter.

        Parameters
        ----------
        object : Any
            Object to be added to the plotter.
        filter : str, optional
            Filter to be applied to the object, by default None.
        """
        self.pv_interface.add(object, filter, **plotting_options)