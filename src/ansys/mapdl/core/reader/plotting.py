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
        if not comp:
            comp = "X"

        if element_components:
            raise NotImplementedInDPFBackend(argument="element_components")

        if sel_type_all:
            raise NotImplementedInDPFBackend(argument="sel_type_all")

        if treat_nan_as_zero:
            raise NotImplementedInDPFBackend(argument="treat_nan_as_zero")

        field = self.nodal_displacement(rnum, nodes=nodes, return_field=True)
        field = self._component_selector(field, component_number=comp)

        # If the user requested to show displacement, we will
        # deform the mesh by the displacement field.
        deform_by: dpf.Field | None = field if show_displacement else None

        return self.mesh.plot(
            field, scale_factor=displacement_factor, deform_by=deform_by, **kwargs
        )
