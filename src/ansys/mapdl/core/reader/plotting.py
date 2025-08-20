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

"""Class to provide with plotting capabilities for DPF results"""
import ansys.dpf.core as dpf

from ansys.mapdl.core.reader.core import NotImplementedInDPFBackend
from ansys.mapdl.core.reader.data import DPFResultData
from ansys.mapdl.core.reader.types import (
    ComponentsDirections,
    Kwargs,
    MAPDLComponents,
    Nodes,
    Rnum,
)


class DPFResultPlotting(DPFResultData):
    """Provides plotting capabilities for DPF results."""

    def plot_nodal_stress(
        self,
        rnum: Rnum,
        comp: ComponentsDirections | int | None = None,
        show_displacement: bool = False,
        displacement_factor: int = 1,
        node_components: MAPDLComponents | None = None,
        element_components: MAPDLComponents | None = None,
        sel_type_all: bool | None = None,
        treat_nan_as_zero: bool | None = None,
        nodes: Nodes = None,
        **kwargs: Kwargs,
    ) -> list[float]:
        """Plots the stresses at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Stress component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``
            - ``"XY"``
            - ``"YZ"``
            - ``"XZ"``

        show_displacement
            If True, displays the displacement along with the stress
            plot. Default is False.

        displacement_factor
            Factor by which to scale the displacement plot. Default is 1.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default ``True``.

        treat_nan_as_zero : bool, optional
            Treat NAN values (i.e. stresses at midside nodes) as zero
            when plotting.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        **kwargs
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.

        Examples
        --------
        Plot the X component nodal stress while showing displacement.

        >>> mapdl.result.plot_nodal_stress(0, comp='x', show_displacement=True)
        """
        if element_components:
            raise NotImplementedInDPFBackend(argument="element_components")

        if node_components:
            raise NotImplementedInDPFBackend(argument="node_components")

        if sel_type_all:
            raise NotImplementedInDPFBackend(argument="sel_type_all")

        if treat_nan_as_zero:
            raise NotImplementedInDPFBackend(argument="treat_nan_as_zero")

        field: dpf.Field = self.nodal_stress(rnum, nodes=nodes, return_field=True)  # type: ignore
        field = self._component_selector(fc=field, component=comp)

        # If the user requested to show displacement, we will
        # deform the mesh by the displacement field.
        deform_by: dpf.Field | None = field if show_displacement else None

        return self.mesh.plot(
            field, scale_factor=displacement_factor, deform_by=deform_by, **kwargs
        )

    def plot_nodal_displacement(
        self,
        rnum: Rnum,
        comp: ComponentsDirections | int | None = None,
        show_displacement: bool = False,
        displacement_factor: int = 1,
        node_components: MAPDLComponents | None = None,
        element_components: MAPDLComponents | None = None,
        sel_type_all: bool | None = None,
        treat_nan_as_zero: bool | None = None,
        nodes: Nodes = None,
        in_nodal_coord_sys: bool = False,
        **kwargs: Kwargs,
    ) -> list[float]:
        """Plots the displacements at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Displacement component to display.  Available options:
            - ``"X"``
            - ``"Y"``
            - ``"Z"``

        show_displacement
            If True, displays the displacement along with the displacement
            plot. Default is False.

        displacement_factor
            Factor by which to scale the displacement plot. Default is 1.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default ``True``.

        treat_nan_as_zero : bool, optional
            Treat NAN values (i.e. displacements at midside nodes) as zero
            when plotting.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        in_nodal_coord_sys : bool, optional
            When ``True``, returns results in the nodal coordinate
            system.  Default ``False``.

        **kwargs
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.

        Examples
        --------
        Plot the X component nodal displacement while showing displacement.

        >>> mapdl.result.plot_nodal_displacement(0, comp='x', show_displacement=True)
        """
        if element_components:
            raise NotImplementedInDPFBackend(argument="element_components")

        if node_components:
            raise NotImplementedInDPFBackend(argument="node_components")

        if sel_type_all:
            raise NotImplementedInDPFBackend(argument="sel_type_all")

        if treat_nan_as_zero:
            raise NotImplementedInDPFBackend(argument="treat_nan_as_zero")

        field: dpf.Field = self.nodal_displacement(rnum, in_nodal_coord_sys=in_nodal_coord_sys, nodes=nodes, return_field=True)  # type: ignore
        field = self._component_selector(fc=field, component=comp)

        # If the user requested to show displacement, we will
        # deform the mesh by the displacement field.
        deform_by: dpf.Field | None = field if show_displacement else None

        return self.mesh.plot(
            field, scale_factor=displacement_factor, deform_by=deform_by, **kwargs
        )

    def plot_nodal_temperature(
        self,
        rnum: Rnum,
        comp: ComponentsDirections | int | None = None,
        show_displacement: bool = False,
        displacement_factor: int = 1,
        node_components: MAPDLComponents | None = None,
        element_components: MAPDLComponents | None = None,
        sel_type_all: bool | None = None,
        treat_nan_as_zero: bool | None = None,
        nodes: Nodes = None,
        **kwargs: Kwargs,
    ) -> list[float]:
        """Plots the temperature at each node in the solution.

        Parameters
        ----------
        rnum : int or list
            Cumulative result number with zero based indexing, or a
            list containing (step, substep) of the requested result.

        comp : str, optional
            Temperature component to display. Note: Temperature is a scalar
            field, so component selection may not apply.

        show_displacement
            If True, displays the displacement along with the temperature
            plot. Default is False.

        displacement_factor
            Factor by which to scale the displacement plot. Default is 1.

        node_components : list, optional
            Accepts either a string or a list strings of node
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        element_components : list, optional
            Accepts either a string or a list strings of element
            components to plot.  For example:
            ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``

        sel_type_all : bool, optional
            If node_components is specified, plots those elements
            containing all nodes of the component.  Default ``True``.

        treat_nan_as_zero : bool, optional
            Treat NAN values (i.e. temperatures at midside nodes) as zero
            when plotting.

        nodes
            Select a limited subset of nodes.  Can be a nodal
            component or array of node numbers.  For example

            * ``"MY_COMPONENT"``
            * ``['MY_COMPONENT', 'MY_OTHER_COMPONENT]``
            * ``np.arange(1000, 2001)``

        **kwargs
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.

        Examples
        --------
        Plot the nodal temperature while showing displacement.

        >>> mapdl.result.plot_nodal_temperature(0, show_displacement=True)
        """
        if element_components:
            raise NotImplementedInDPFBackend(argument="element_components")

        if node_components:
            raise NotImplementedInDPFBackend(argument="node_components")

        if sel_type_all:
            raise NotImplementedInDPFBackend(argument="sel_type_all")

        if treat_nan_as_zero:
            raise NotImplementedInDPFBackend(argument="treat_nan_as_zero")

        field: dpf.Field = self.nodal_temperature(rnum, nodes=nodes, return_field=True)  # type: ignore
        field = self._component_selector(fc=field, component=comp)

        # If the user requested to show displacement, we will
        # deform the mesh by the displacement field.
        deform_by: dpf.Field | None = None
        if show_displacement:
            # Get displacement field for deformation
            displacement_field: dpf.Field = self.nodal_displacement(rnum, nodes=nodes, return_field=True)  # type: ignore
            deform_by = displacement_field

        return self.mesh.plot(
            field, scale_factor=displacement_factor, deform_by=deform_by, **kwargs
        )
