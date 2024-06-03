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

"""Module for the MapdlPlotter class."""
from ansys.tools.visualization_interface import Plotter
from ansys.tools.visualization_interface.backends.pyvista import PyVistaBackendInterface
from beartype.typing import Any, Iterable
import pyvista as pv

from ansys.mapdl.core.plotting.theme import MapdlTheme


class MapdlPlotterBackend(PyVistaBackendInterface):
    """Provides the plotter for PyMAPDL.

    This class is an implementation of the ``PlotterInterface`` class from the ``ansys-visualizer`` package.
    Picker is implemented in PyMAPDL-specific classes due to the characteristics of the library.

    Parameters
    ----------
    use_trame : bool, optional
        Whether to use the Trame interface or not. The default is ``False``.
    theme : pv.DefaultTheme, optional
        _description_, by default None1
    """

    def __init__(
        self, use_trame: bool = False, plot_picked_names: bool = True, **plotter_kwargs
    ):
        """Initialize the ``MapdlPlotter`` class."""
        super().__init__(
            use_trame=use_trame, plot_picked_names=plot_picked_names, **plotter_kwargs
        )

    def plot_iter(
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
            self.plot(object, filter, **plotting_options)

    def plot(self, plottable_object: Any, name_filter: str = None, **plotting_options):
        self.pv_interface.plot(
            plottable_object=plottable_object,
            name_filter=name_filter,
            **plotting_options,
        )

    def show(
        self,
        plottable_object: Any = None,
        screenshot: str = None,
        name_filter: bool = None,
        **plotting_options,
    ):
        if object is not None:
            self.plot(plottable_object, name_filter, **plotting_options)
        self.pv_interface.show(screenshot=screenshot)


class MapdlPlotter(Plotter):
    """Plotter class for PyMapdl.

    This class is an implementation of the PlotterInterface class from the ansys-visualizer package.
    Picker is implemented in PyMAPDL specific classes due to the characteristics of the library.

    Parameters
    ----------
    use_trame : bool, optional
        Whether to use the trame interface or not, by default False.
    theme : pv.DefaultTheme, optional
        _description_, by default None1
    """

    def __init__(
        self, use_trame: bool = False, theme: pv.Plotter.theme = None, **plotter_kwargs
    ):
        """Initialize the MapdlPlotter class."""
        self._backend = MapdlPlotterBackend(use_trame=use_trame, **plotter_kwargs)
        super().__init__(backend=self._backend)
        self._theme = theme
        if theme is None:
            self._theme = MapdlTheme()

    def add_labels(
        self, points: Iterable[float], labels: Iterable[str], **plotting_options
    ) -> None:
        """Add labels to the plotter.

        Parameters
        ----------
        points : List[float]
            List of points of the labels.
        labels : List[str]
            List of labels to add.
        """
        _ = self._backend.pv_interface.scene.add_point_labels(
            points, labels, **plotting_options
        )

    def add_points(self, points: Iterable[float], **plotting_options) -> None:
        """Add points to the plotter.

        Parameters
        ----------
        points : List[float]
            List of points to add to the plotter.
        """
        _ = self._backend.pv_interface.scene.add_points(points, **plotting_options)

    def plot_iter(
        self,
        plotting_list: Iterable[Any],
        filter: str = None,
        **plotting_options,
    ) -> None:
        """Add a list of objects to the plotter.

        Parameters
        ----------
        plotting_list : Iterable[Any]
            Iterable of objects to add to the plotter.
        filter : str, optional
            Filter to apply to the objects. The default is ``None``.
        """
        for object in plotting_list:
            self.plot(object, filter, **plotting_options)

    def plot(
        self, plottable_object: Any, name_filter: str = None, **plotting_options
    ) -> None:
        """Add an object to the plotter.

        Parameters
        ----------
        object : Any
            Object add to the plotter.
        filter : str, optional
            Filter to apply to the object. The default is ``None``.
        """
        self._backend.plot(plottable_object, name_filter, **plotting_options)
