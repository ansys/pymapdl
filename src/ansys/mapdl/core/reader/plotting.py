# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

from ansys.mapdl.core.reader.core import DPFResultCore
from ansys.mapdl.core.reader.types import (
    ComponentsDirections,
    Kwargs,
    MAPDLComponents,
    Rnum,
)


class DPFResultPlotting(DPFResultCore):
    """Provides plotting capabilities for DPF results."""

    def plot_nodal_stress(
        self,
        rnum: Rnum,
        comp: ComponentsDirections | None = None,
        show_displacement: bool = False,
        displacement_factor: int = 1,
        node_components: MAPDLComponents | None = None,
        element_components: MAPDLComponents | None = None,
        sel_type_all: bool = True,
        treat_nan_as_zero: bool = True,
        **kwargs: Kwargs,
    ):
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

        **kwargs
            Additional keyword arguments.  See ``help(pyvista.plot)``

        Returns
        -------
        cpos : list
            3 x 3 vtk camera position.

        Examples
        --------
        Plot the X component nodal stress while showing displacement.

        >>> rst.plot_nodal_stress(0, comp='x', show_displacement=True)
        """
        # if not comp:
        #     comp = "X"

        # ind = COMPONENTS.index(comp)

        # op = self._get_nodes_result(
        #     rnum,
        #     "stress",
        #     nodes=node_components,
        #     in_nodal_coord_sys=False,
        #     return_operator=True,
        # )
        # fc = op.outputs.fields_as_fields_container()[0]

        raise NotImplementedError("WIP")
