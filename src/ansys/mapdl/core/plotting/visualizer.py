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