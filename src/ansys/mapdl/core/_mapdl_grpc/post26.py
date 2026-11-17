# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

"""POST26 time-history variables returned as arrays."""

from functools import wraps

import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core.lazy_array import LazyArray
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat, MapdlInt

from . import _GrpcMixinBase

VAR_IR = 9  # Default variable number for automatic variable retrieving (/post26)


class _GrpcPost26Mixin(_GrpcMixinBase):
    """POST26 time-history variables returned as arrays."""

    @wraps(MapdlBase.vget)
    def vget(  # numpydoc ignore=RT01
        self,
        par: str = "",
        ir: MapdlInt = "",
        tstrt: MapdlFloat = "",
        kcplx: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Wraps VGET and returns its values eagerly."""
        super().vget(par=par, ir=ir, tstrt=tstrt, kcplx=kcplx, **kwargs)  # type: ignore[misc]  # Resolved through MapdlGrpc's MRO.
        if self._store_commands:
            return None
        return self.parameters[par]

    def get_variable(
        self,
        ir: MapdlInt = "",
        tstrt: MapdlFloat = "",
        kcplx: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> LazyArray:
        """
        Obtain the POST26 time-history variable values lazily.

        This method uses the ``VGET`` command to copy a POST26 variable
        (for example, one created with
        :func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` or
        :func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`) into a private
        MAPDL array parameter. On gRPC connections, the returned
        :class:`LazyArray <ansys.mapdl.core.lazy_array.LazyArray>` downloads
        its values, and releases that private parameter, only when it is
        first used.

        Parameters
        ----------
        ir : int, optional
            Reference number of the variable (1 to NV [NUMVAR]). This is
            the same ``nvar`` reference number used when defining the
            variable, for example with
            :func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` or
            :func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`.

        tstrt : float, optional
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used. By default, retrieval starts at
            0.0.

        kcplx : int, optional
            Complex number key:

            * ``0`` - Use the real part of the IR data. Default.

            * ``1`` - Use the imaginary part of the IR data.

        Returns
        -------
        LazyArray
            Variable values downloaded from MAPDL when first used. Use
            :func:`numpy.asarray` or :meth:`LazyArray.resolve` to materialize
            the values explicitly.

        Examples
        --------
        Define a POST26 variable with
        :func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` for the ``UX``
        displacement of node 1, and then retrieve its values with
        ``get_variable``.

        >>> mapdl.post26()
        >>> mapdl.nsol(2, 1, "U", "X")
        >>> np.asarray(mapdl.get_variable(2))
        array([0.        , 0.00108135, 0.00300901, ..., 0.03407310])

        The same works for element results defined with
        :func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`, using
        ``tstrt`` to skip the initial time (or frequency) values.

        >>> mapdl.esol(3, 1, 1, "S", "Y")
        >>> np.asarray(mapdl.get_variable(3, tstrt=1.0))
        array([0.34632451, 0.36126732, ..., 0.38041256])
        """
        with self._reserved_lazy_array_parameter() as parameter_name:
            super().vget(  # type: ignore[misc]  # Resolved through MapdlGrpc's MRO.
                par=parameter_name,
                ir=ir,
                tstrt=tstrt,
                kcplx=kcplx,
                **kwargs,
            )

        return self._lazy_array(parameter_name)

    @wraps(MapdlBase.nsol)
    def nsol(  # numpydoc ignore=RT01
        self,
        nvar: MapdlInt = VAR_IR,
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Wraps NSOL to return the variable as an array."""
        super().nsol(  # type: ignore[misc]  # Resolved through MapdlGrpc's MRO.
            nvar=nvar,  # type: ignore[arg-type]
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            **kwargs,
        )
        return self.vget("_temp", nvar)  # type: ignore[arg-type]

    @wraps(MapdlBase.esol)
    def esol(  # numpydoc ignore=RT01
        self,
        nvar: MapdlInt = VAR_IR,
        elem: MapdlInt = "",
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Wraps ESOL to return the variable as an array."""
        super().esol(  # type: ignore[misc]  # Resolved through MapdlGrpc's MRO.
            nvar=nvar,  # type: ignore[arg-type]
            elem=elem,
            node=node,
            item=item,
            comp=comp,
            name=name,
            **kwargs,
        )
        return self.vget("_temp", nvar)  # type: ignore[arg-type]

    @wraps(MapdlBase.rpsd)
    def rpsd(  # numpydoc ignore=RT01
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        itype: int | str = "",
        datum: int | str = "",
        name: str = "",
        signif: str = "",
        **kwargs,
    ) -> NDArray[np.float64]:
        """Wraps RPSD to return the variable as an array."""
        super().rpsd(  # type: ignore[misc]  # Resolved through MapdlGrpc's MRO.
            ir=ir,
            ia=ia,
            ib=ib,
            itype=itype,
            datum=datum,
            name=name,
            signif=signif,
            **kwargs,
        )
        return self.vget("_temp", ir)  # type: ignore[arg-type]

    def get_nsol(
        self,
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """
        Get NSOL solutions

        Parameters
        ----------
        node : int
            Node for which data is to be stored.

        item : str
            Label identifying the item.  Valid item labels are shown in the
            table below. Some items also require a component label.

        comp : str
            Component of the item (if required).  Valid component labels are
            shown in the table below.

        name : str, optional
            Thirty-two character name identifying the item on printouts and
            displays.  The default is a label formed by concatenating the first
            four characters of the ``item`` and ``comp`` labels.

        sector : int, optional
            For a full harmonic cyclic symmetry solution, the sector number for
            which the results from NODE are to be stored.

        Returns
        -------
        numpy.ndarray
            Variable values

        Notes
        -----
        By default, this command store temporally the variable on the
        variable number set by ``VAR_IR`` in the class MapdlGrpc.
        Therefore, any variable in that slot will be deleted when using
        this command.

        Stores nodal degree of freedom and solution results in a variable. For
        more information, see Data Interpreted in the Nodal Coordinate System
        in the Modeling and Meshing Guide.

        For SECTOR>1, the result is in the nodal coordinate system of the base
        sector, and it is rotated to the expanded sector’s location. Refer to
        Using the /CYCEXPAND Command in the Cyclic Symmetry Analysis Guide for
        more information.

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels TBOT, TE2, TE3, . . ., TTOP instead of TEMP.
        """
        return self.nsol(
            VAR_IR,  # type: ignore[arg-type]
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            **kwargs,
        )

    def get_esol(
        self,
        elem: MapdlInt = "",
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: MapdlInt = "",
        tstrt: MapdlFloat = "",
        kcplx: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Get ESOL data.

        /POST26 APDL Command: ESOL

        Parameters
        ----------
        elem : int
            Element for which data are to be stored.

        node : int
            Node number on this element for which data are to be
            stored. If blank, store the average element value (except
            for ``FMAG`` values, which are summed instead of averaged).

        item : str
            Label identifying the item. Some items also require a component label.

        comp : str
            Component of the item (if required). If Comp is a sequence number (n),
            the ``NODE`` field will be ignored.

        name : str, optional
            Thirty-two character name for identifying the item on the
            printout and displays.  The default is a label formed by
            concatenating the first four characters of the ``item`` and
            ``comp`` labels.

        tstrt : str, optional
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used. By default it is the first value.

        kcplx : str, optional
            Complex number key:

            * ``0`` - Use the real part of the IR data. Default.

            * ``1`` - Use the imaginary part of the IR data.

        Returns
        -------
        numpy.ndarray
            Variable values

        Notes
        -----
        By default, this command store temporally the variable on the
        variable number set by ``VAR_IR`` in the class
        :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>`
        Therefore, any variable in that slot will be deleted when using
        this command.

        The ``ESOL`` command defines element results data to be stored
        from a results file (``FILE``). Not all items are valid for all
        elements. To see the available items for a given element,
        refer to the input and output summary tables in the
        documentation for that element.

        Two methods of data access are available via the ``ESOL``
        command. You can access some simply by using a generic label
        (component name method), while others require a label and
        number (sequence number method).

        Use the component name method to access general element data
        (that is, element data generally available to most element
        types or groups of element types).

        The sequence number method is required for data that is not
        averaged (such as pressures at nodes and temperatures at
        integration points), or data that is not easily described in a
        generic fashion (such as all derived data for structural line
        elements and contact elements, all derived data for thermal
        line elements, and layer data for layered elements).

        Element results are in the element coordinate system, except
        for layered elements where results are in the layer coordinate
        system.  Element forces and moments are in the nodal
        coordinate system. Results are obtainable for an element at a
        specified node. Further location specifications can be made
        for some elements via the ``SHELL``, ``LAYERP26``, and ``FORCE`` commands.

        For more information on the meaning of contact status and its
        possible values, see Reviewing Results in ``POST1`` in the Contact
        Technology Guide.
        """
        self.esol(
            VAR_IR,  # type: ignore[arg-type]
            elem=elem,
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            **kwargs,
        )
        # Materialize the private result to preserve this method's ndarray API.
        return self.get_variable(VAR_IR, tstrt=tstrt, kcplx=kcplx).resolve()
