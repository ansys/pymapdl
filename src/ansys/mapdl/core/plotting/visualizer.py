from ansys.visualizer import MeshObjectPlot, PlotterInterface
from beartype.typing import Any, List
import pyvista as pv

from ansys.mapdl.core.plotting.theme import MapdlTheme


class MapdlPlotter(PlotterInterface):
    def __init__(self, use_trame: bool = False, allow_picking: bool = False, theme = None, **plotter_kwargs):
        super().__init__(use_trame, allow_picking, plot_picked_names=True)
        self._theme = theme
        if theme is None:
            self._theme = MapdlTheme()        
    
    def add_labels(self, points, labels: List[str], **plotting_options) -> None:
        _ = self.pv_interface.scene.add_point_labels(points, labels, **plotting_options)
    
    def add_points(self, points, **plotting_options) -> None:
        _ = self.pv_interface.scene.add_points(points, **plotting_options)
    
    def add_iter(
        self,
        plotting_list: List[Any],
        filter: str = None,
        **plotting_options,
    ) -> None:
        for object in plotting_list:
            _ = self.add(object, filter, **plotting_options)
            
    def add(self, object: Any, filter: str = None, **plotting_options) -> None:
        self.pv_interface.add(object, filter, **plotting_options)