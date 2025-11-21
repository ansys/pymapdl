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

from ansys.mapdl.core._commands import CommandsBase


class TracePoints(CommandsBase):

    def pltrac(
        self,
        analopt: str = "",
        item: str = "",
        comp: str = "",
        trpnum: str = "",
        name: str = "",
        mxloop: str = "",
        toler: str = "",
        escl: str = "",
        mscl: str = "",
        **kwargs,
    ):
        r"""Displays a charged particle trace on an element display.

        Mechanical APDL Command: `PLTRAC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLTRAC.html>`_

        Parameters
        ----------
        analopt : str
            Analysis option

            * ``ELEC`` - Particle trace in electric field

            * ``MAGN`` - Particle trace in magnetic field

            * ``EMAG`` - Particle trace in presence of both electric and magnetic fields (default)

        item : str
            Label identifying the item to be contoured. Valid item labels are shown in :ref:`pltrac_tab_1`
            below. Some items also require a component label. If ``Item`` is blank, display only the path
            trajectory.

        comp : str
            Component of the item (if required). Valid component labels are shown in :ref:`pltrac_tab_1`
            below.

        trpnum : str
            Trace point number for storing trajectory data for use with :ref:`path` logic. Defaults to 0 (no
            trajectory path data is stored for further processing with :ref:`path` logic).

        name : str
            Name of prefix of array variable. Defaults to TRAC. ``Name`` POIN stores trajectory path points
            for trace point number ``TRPNum``. If ``Analopt`` = ELEC, MAGN, or EMAG, two additional array
            parameters, ``Name`` DATA and ``Name`` LABL, store trajectory path data and labels for the same
            ``TRPNum``.

        mxloop : str
            Maximum number of loops traced by a particle. Defaults to 1000.

        toler : str
            Length tolerance used for particle trajectory geometry calculation. Valid for ``Analopt`` =
            ELEC, MAGN, or EMAG. If particle trace appears to terminate inside an element, adjusting the
            length tolerance may be necessary. Defaults to 1.0 x 10 :sup:`-8`.

        escl : str
            Electric field scale factor. Setting this scale factor affects only the tracing, not the field
            solution results. A negative factor corresponds to the opposite vector direction. Valid only for
            ``Analopt`` = ELEC or EMAG. Defaults to 1.

        mscl : str
            Magnetic field scale factor. Setting this scale factor affects only the tracing, not the field
            solution results. A negative factor corresponds to the opposite vector direction. Valid only for
            ``Analopt`` = MAGN or EMAG. Defaults to 1.

        Notes
        -----

        .. _PLTRAC_notes:

        For a specified item, the variation of the item is displayed along the particle trace as a color-
        contoured ribbon. The :ref:`trpoin` command must be used to define a point on the trajectory path.
        Multiple traces may be displayed simultaneously by defining multiple trace points. Issue the
        :ref:`trplis` command to list the current tracing points. Issue the :ref:`trpdel` command to delete
        tracing points defined earlier. Use the :ref:`paput` command with the POIN option to retrieve the
        particle trajectory points as path points.

        The model must be 3D for the ELEC, MAGN, and EMAG analysis options.

        Three array parameters are created at the time of the particle trace: TRACPOIN, TRACDATA and
        TRACLABL. These array parameters can be used to put the particle velocity and the elapsed time into
        path form. The procedure to put the arrays into a path named PATHNAME is as follows:

        .. code:: apdl

           *get,npts,PARM,TRACPOIN,DIM,x
           PATH,PATHNAME,npts,9,1
           PAPUT,TRACPOIN,POINTS
           PAPUT,TRACDATA,TABLES
           PAPUT,TRACLABL,LABELS
           PRPATH,S,T_TRACE,VX_TRACE,VY_TRACE,VZ_TRACE,VS_TRACE

        If working in the GUI, use the "All information" option to retrieve information from all three
        arrays at once.

        .. _pltrac_tab_1:

        PLTRAC - Valid Item and Component Labels
        ****************************************

        .. flat-table::
           :header-rows: 1

           * - Item
             - Comp
             - Description
           * - **Valid item labels for** ``Analopt`` = ELEC nodal results are:
           * - VOLT
             -
             - Electric potential.
           * - **Valid item labels for** ``Analopt`` = MAGN or EMAG nodal results are:
           * - None
             -
             - Color contour displayed.

        See the `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for more
        information on charged particle traces. See `Animation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS15_7.html>`_ in the
        `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for information
        on particle trace animation.
        """
        command = f"PLTRAC,{analopt},{item},{comp},{trpnum},{name},{mxloop},{toler},,{escl},{mscl}"
        return self.run(command, **kwargs)

    def trpdel(self, ntrp1: str = "", ntrp2: str = "", trpinc: str = "", **kwargs):
        r"""Deletes charged particle trace points.

        Mechanical APDL Command: `TRPDEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TRPDEL.html>`_

        Parameters
        ----------
        ntrp1 : str
            Delete points from ``NTRP1`` to ``NTRP2`` (defaults to ``NTRP1`` ) in steps of ``TRPINC``
            (defaults to 1). If ``NTRP1`` = ALL, ``NTRP2`` and ``TRPINC`` are ignored and all trace points
            are deleted. If ``NTRP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        ntrp2 : str
            Delete points from ``NTRP1`` to ``NTRP2`` (defaults to ``NTRP1`` ) in steps of ``TRPINC``
            (defaults to 1). If ``NTRP1`` = ALL, ``NTRP2`` and ``TRPINC`` are ignored and all trace points
            are deleted. If ``NTRP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        trpinc : str
            Delete points from ``NTRP1`` to ``NTRP2`` (defaults to ``NTRP1`` ) in steps of ``TRPINC``
            (defaults to 1). If ``NTRP1`` = ALL, ``NTRP2`` and ``TRPINC`` are ignored and all trace points
            are deleted. If ``NTRP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        Notes
        -----

        .. _TRPDEL_notes:

        Deletes charged particle trace points defined with the :ref:`trpoin` command.
        """
        command = f"TRPDEL,{ntrp1},{ntrp2},{trpinc}"
        return self.run(command, **kwargs)

    def trplis(
        self,
        ntrp1: str = "",
        ntrp2: str = "",
        trpinc: str = "",
        opt: str = "",
        **kwargs,
    ):
        r"""Lists charged particle trace points.

        Mechanical APDL Command: `TRPLIS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TRPLIS.html>`_

        Parameters
        ----------
        ntrp1 : str
            List points from ``NTRP1`` to ``NTRP2`` (defaults to ``NTRP1`` ) in steps of ``TRPINC``
            (defaults to 1). If ``NTRP1`` = ALL, ``NTRP2`` and ``TRPINC`` are ignored and all trace points
            are listed. If ``NTRP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        ntrp2 : str
            List points from ``NTRP1`` to ``NTRP2`` (defaults to ``NTRP1`` ) in steps of ``TRPINC``
            (defaults to 1). If ``NTRP1`` = ALL, ``NTRP2`` and ``TRPINC`` are ignored and all trace points
            are listed. If ``NTRP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        trpinc : str
            List points from ``NTRP1`` to ``NTRP2`` (defaults to ``NTRP1`` ) in steps of ``TRPINC``
            (defaults to 1). If ``NTRP1`` = ALL, ``NTRP2`` and ``TRPINC`` are ignored and all trace points
            are listed. If ``NTRP1`` = P, graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        opt : str
            ``Opt`` = LOC lists the trace point number location (X, Y, Z). Default.

            ``Opt`` = PART lists the trace point number particle settings (velocity, charge, mass).

        Notes
        -----

        .. _TRPLIS_notes:

        Lists the charged particle trace points in the active display coordinate system ( :ref:`dsys` ).
        Trace points are defined with the :ref:`trpoin` command.
        """
        command = f"TRPLIS,{ntrp1},{ntrp2},{trpinc},{opt}"
        return self.run(command, **kwargs)

    def trpoin(
        self,
        x: str = "",
        y: str = "",
        z: str = "",
        vx: str = "",
        vy: str = "",
        vz: str = "",
        chrg: str = "",
        mass: str = "",
        **kwargs,
    ):
        r"""Defines a point through which a charged particle trace will travel.

        Mechanical APDL Command: `TRPOIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TRPOIN.html>`_

        Parameters
        ----------
        x : str
            Coordinate location of the trace point (in the active coordinate system). If ``X`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI).

        y : str
            Coordinate location of the trace point (in the active coordinate system). If ``X`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI).

        z : str
            Coordinate location of the trace point (in the active coordinate system). If ``X`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI).

        vx : str
            Particle velocities in the X, Y and Z directions (in the active coordinate system).

        vy : str
            Particle velocities in the X, Y and Z directions (in the active coordinate system).

        vz : str
            Particle velocities in the X, Y and Z directions (in the active coordinate system).

        chrg : str
            Particle charge.

        mass : str
            Particle mass.

        Notes
        -----

        .. _TRPOIN_notes:

        Defines a point through which a charged particle trace ( :ref:`pltrac` ) will travel. Multiple
        points (50 maximum) may be defined which will result in multiple particle traces. Use :ref:`trplis`
        to list the currently defined trace points and :ref:`trpdel` to delete trace points.

        The VX, VY, VZ, CHRG, and MASS arguments only apply to charged particles.
        """
        command = f"TRPOIN,{x},{y},{z},{vx},{vy},{vz},{chrg},{mass}"
        return self.run(command, **kwargs)
