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


class Fatigue(CommandsBase):

    def fe(
        self, nev: str = "", cycle: str = "", fact: str = "", title: str = "", **kwargs
    ):
        r"""Defines a set of fatigue event parameters.

        Mechanical APDL Command: `FE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FE.html>`_

        Parameters
        ----------
        nev : str
            Reference number for this event (within ``MXEV`` ).

        cycle : str
            Number of required cycles (defaults to 1). If -1, erase all parameters and fatigue stresses for
            this event.

        fact : str
            Scale factor to be applied to all loadings in this event (defaults to 1.0).

        title : str
            User defined identification title for this event (up to 20 characters).

        Notes
        -----

        .. _FE_notes:

        Repeat FE command to define additional sets of event parameters ( ``MXEV`` limit), to redefine event
        parameters, or to delete event stress conditions.

        The set of fatigue event parameters is associated with all loadings and all locations. See the
        FTSIZE command for the maximum set of events ( ``MXEV`` ) allowed.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FE,{nev},{cycle},{fact},{title}"
        return self.run(command, **kwargs)

    def felist(self, nev1: str = "", nev2: str = "", ninc: str = "", **kwargs):
        r"""Lists the fatigue event parameters.

        Mechanical APDL Command: `FELIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FELIST.html>`_

        Parameters
        ----------
        nev1 : str
            List event parameters from ``NEV1`` (defaults to 1) to ``NEV2`` (defaults to ``NEV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NEV1`` = ALL, ``NEV2`` and ``NINC`` are ignored and all events
            are listed.

        nev2 : str
            List event parameters from ``NEV1`` (defaults to 1) to ``NEV2`` (defaults to ``NEV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NEV1`` = ALL, ``NEV2`` and ``NINC`` are ignored and all events
            are listed.

        ninc : str
            List event parameters from ``NEV1`` (defaults to 1) to ``NEV2`` (defaults to ``NEV1`` ) in steps
            of ``NINC`` (defaults to 1). If ``NEV1`` = ALL, ``NEV2`` and ``NINC`` are ignored and all events
            are listed.

        Notes
        -----

        .. _FELIST_notes:

        Fatigue event parameters are defined via the FE command.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FELIST,{nev1},{nev2},{ninc}"
        return self.run(command, **kwargs)

    def fl(
        self,
        nloc: str = "",
        node: str = "",
        scfx: str = "",
        scfy: str = "",
        scfz: str = "",
        title: str = "",
        **kwargs,
    ):
        r"""Defines a set of fatigue location parameters.

        Mechanical APDL Command: `FL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FL.html>`_

        Parameters
        ----------
        nloc : str
            Reference number for this location (within ``MXLOC`` ). When defining a new location, defaults
            to lowest unused location. If the specified ``NODE`` is already associated with a location,
            ``NLOC`` defaults to that existing location.

        node : str
            Node number corresponding to this location (must be unique). Used only to associate a node with
            a new location or to find an existing location (if ``NLOC`` is not input). If ``NODE`` = -1 (or
            redefined), erase all parameters and fatigue stresses for this location.

        scfx : str
            Stress concentration factors applied to the total stresses. Factors are applied in the global X,
            Y, and Z directions unless the axisymmetric option of the :ref:`fssect` is used (that is,
            ``RHO`` is nonzero), in which case the factors are applied in the section x, y, and z (radial,
            axial, and hoop) directions.

        scfy : str
            Stress concentration factors applied to the total stresses. Factors are applied in the global X,
            Y, and Z directions unless the axisymmetric option of the :ref:`fssect` is used (that is,
            ``RHO`` is nonzero), in which case the factors are applied in the section x, y, and z (radial,
            axial, and hoop) directions.

        scfz : str
            Stress concentration factors applied to the total stresses. Factors are applied in the global X,
            Y, and Z directions unless the axisymmetric option of the :ref:`fssect` is used (that is,
            ``RHO`` is nonzero), in which case the factors are applied in the section x, y, and z (radial,
            axial, and hoop) directions.

        title : str
            User-defined title for this location (up to 20 characters).

        Notes
        -----

        .. _FL_notes:

        Repeat FL command to define additional sets of location parameters ( ``MXLOC`` limit), to redefine
        location parameters, or to delete location stress conditions.

        One location must be defined for each node of interest and only one node can be associated with each
        location. See the FTSIZE command for the maximum locations ( ``MXLOC`` ) allowed. A location will be
        automatically defined for a node not having a location when the FSSECT, FSNODE, or FS command is
        issued. Automatically defined locations are assigned the lowest available location number, unity
        stress concentration factors, and no title.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FL,{nloc},{node},{scfx},{scfy},{scfz},{title}"
        return self.run(command, **kwargs)

    def fllist(self, nloc1: str = "", nloc2: str = "", ninc: str = "", **kwargs):
        r"""Lists the fatigue location parameters.

        Mechanical APDL Command: `FLLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FLLIST.html>`_

        Parameters
        ----------
        nloc1 : str
            List location parameters from ``NLOC1`` (defaults to 1) to ``NLOC2`` (defaults to ``NLOC1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NLOC1`` = ALL, ``NLOC2`` and ``NINC`` are ignored and
            all locations are listed.

        nloc2 : str
            List location parameters from ``NLOC1`` (defaults to 1) to ``NLOC2`` (defaults to ``NLOC1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NLOC1`` = ALL, ``NLOC2`` and ``NINC`` are ignored and
            all locations are listed.

        ninc : str
            List location parameters from ``NLOC1`` (defaults to 1) to ``NLOC2`` (defaults to ``NLOC1`` ) in
            steps of ``NINC`` (defaults to 1). If ``NLOC1`` = ALL, ``NLOC2`` and ``NINC`` are ignored and
            all locations are listed.

        Notes
        -----

        .. _FLLIST_notes:

        No additional usage notes are available for this command.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FLLIST,{nloc1},{nloc2},{ninc}"
        return self.run(command, **kwargs)

    def fp(
        self,
        stitm: int | str = "",
        c1: str = "",
        c2: str = "",
        c3: str = "",
        c4: str = "",
        c5: str = "",
        c6: str = "",
        **kwargs,
    ):
        r"""Defines the fatigue S vs. N and Sm vs. T tables.

        Mechanical APDL Command: `FP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FP.html>`_

        Parameters
        ----------
        stitm : int or str
            Starting item number for entering properties (defaults to 1). If 1, data input in field ``C1`` of this command is entered as the first item in the list; if 7, data input in field ``C1`` of this command is entered as the seventh item in the list; etc. If the item number is negative, ``C1`` - ``C6`` are ignored and the item is deleted. If -ALL, the table is erased. Items are as follows (items 41-62 are required only if simplified elastic-plastic code calculations are to be performed):

            * ``1,2,...20`` - N1, N2,... N20

            * ``21,22,...40`` - S1, S2,... S20

            * ``41,42,...50`` - T1, T2,... T10

            * ``51,52,...60`` - Sm1, Sm2,..., Sm10

            * ``61`` - M (first elastic-plastic material parameter)

            * ``62, `` - N (second elastic-plastic material parameter)

        c1 : str
            Data inserted into six locations starting with ``STITM``. If a value is already in one of these
            locations, it will be redefined. A blank retains the previous value.

        c2 : str
            Data inserted into six locations starting with ``STITM``. If a value is already in one of these
            locations, it will be redefined. A blank retains the previous value.

        c3 : str
            Data inserted into six locations starting with ``STITM``. If a value is already in one of these
            locations, it will be redefined. A blank retains the previous value.

        c4 : str
            Data inserted into six locations starting with ``STITM``. If a value is already in one of these
            locations, it will be redefined. A blank retains the previous value.

        c5 : str
            Data inserted into six locations starting with ``STITM``. If a value is already in one of these
            locations, it will be redefined. A blank retains the previous value.

        c6 : str
            Data inserted into six locations starting with ``STITM``. If a value is already in one of these
            locations, it will be redefined. A blank retains the previous value.

        Notes
        -----

        .. _FP_notes:

        Defines the fatigue alternating stress (S) vs. cycles (N) table and the design stress-intensity
        value (Sm) vs. temperature (T) table. Can also be used to modify any previously stored property
        tables. Log-log interpolation is used in the S vs. N table and linear interpolation is used in the
        Sm vs. T table. Cycles and temperatures must be input in ascending order; S and Sm values in
        descending order. Table values must be supplied in pairs, that is, every N entry must have a
        corresponding S entry, etc. Not all property pairs per curve need be used. If no S vs. N table is
        defined, the fatigue evaluation will not produce usage factor results.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FP,{stitm},{c1},{c2},{c3},{c4},{c5},{c6}"
        return self.run(command, **kwargs)

    def fplist(self, **kwargs):
        r"""Lists the property table stored for fatigue evaluation.

        Mechanical APDL Command: `FPLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FPLIST.html>`_

        Notes
        -----
        This command has no arguments, and no additional usage notes are available.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = "FPLIST"
        return self.run(command, **kwargs)

    def fs(
        self,
        node: str = "",
        nev: str = "",
        nlod: str = "",
        stitm: int | str = "",
        c1: str = "",
        c2: str = "",
        c3: str = "",
        c4: str = "",
        c5: str = "",
        c6: str = "",
        **kwargs,
    ):
        r"""Stores fatigue stress components at a node.

        Mechanical APDL Command: `FS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FS.html>`_

        Parameters
        ----------
        node : str
            Node number corresponding to this location. Used only to associate a node with a new location or
            to find an existing location.

        nev : str
            Event number to be associated with these stresses (defaults to 1).

        nlod : str
            Loading number to be associated with these stresses (defaults to 1).

        stitm : int or str
            Starting item number for entering stresses (defaults to 1). If 1, data input in field ``C1`` of this command is entered as the first item in the list; if 7, data input in field ``C1`` of this command is entered as the seventh item in the list; etc. Items are as follows:

            * ``1-6`` - SX, SY, SZ, SXY, SYZ, SXZ total stress components

            * ``7`` - Temperature

            * ``8-13`` - SX, SY, SZ, SXY, SYZ, SXZ membrane-plus-bending stress components.

            * ``14`` - Time

        c1 : str
            Stresses assigned to six locations starting with ``STITM``. If a value is already in one of
            these locations, it will be redefined. A blank retains the previous value (except in the ``C1``
            field, which resets the ``STITM`` item to zero).

        c2 : str
            Stresses assigned to six locations starting with ``STITM``. If a value is already in one of
            these locations, it will be redefined. A blank retains the previous value (except in the ``C1``
            field, which resets the ``STITM`` item to zero).

        c3 : str
            Stresses assigned to six locations starting with ``STITM``. If a value is already in one of
            these locations, it will be redefined. A blank retains the previous value (except in the ``C1``
            field, which resets the ``STITM`` item to zero).

        c4 : str
            Stresses assigned to six locations starting with ``STITM``. If a value is already in one of
            these locations, it will be redefined. A blank retains the previous value (except in the ``C1``
            field, which resets the ``STITM`` item to zero).

        c5 : str
            Stresses assigned to six locations starting with ``STITM``. If a value is already in one of
            these locations, it will be redefined. A blank retains the previous value (except in the ``C1``
            field, which resets the ``STITM`` item to zero).

        c6 : str
            Stresses assigned to six locations starting with ``STITM``. If a value is already in one of
            these locations, it will be redefined. A blank retains the previous value (except in the ``C1``
            field, which resets the ``STITM`` item to zero).

        Notes
        -----

        .. _FS_notes:

        Stores fatigue stress components at a node as input on this command instead of from the current data
        in the database. Stresses are stored according to the event number and loading number specified. The
        location is associated with that previously defined for this node ( :ref:`fl` ) or else it is
        automatically defined. May also be used to modify any previously stored stress components. Stresses
        input with this command should be consistent with the global coordinate system for any :ref:`fsnode`
        or :ref:`fssect` stresses used at the same location.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FS,{node},{nev},{nlod},{stitm},{c1},{c2},{c3},{c4},{c5},{c6}"
        return self.run(command, **kwargs)

    def fsdele(self, nloc: str = "", nev: str = "", nlod: str = "", **kwargs):
        r"""Deletes a stress condition for a fatigue location, event, and loading.

        Mechanical APDL Command: `FSDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSDELE.html>`_

        Parameters
        ----------
        nloc : str
            Delete stresses associated with location ``NLOC``. Defaults to zero.

        nev : str
            Delete stresses associated with event ``NEV``. Defaults to zero.

        nlod : str
            Delete stresses associated with loading ``NLOD``. Defaults to zero.

        Notes
        -----

        .. _FSDELE_notes:

        Deletes a stress condition stored for a particular fatigue location, event, and loading. Use FE
        command to delete all stresses for a particular event or FL command to delete all stresses for a
        particular location.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FSDELE,{nloc},{nev},{nlod}"
        return self.run(command, **kwargs)

    def fslist(
        self,
        nloc1: str = "",
        nloc2: str = "",
        ninc: str = "",
        nev: str = "",
        nlod: str = "",
        **kwargs,
    ):
        r"""Lists the stresses stored for fatigue evaluation.

        Mechanical APDL Command: `FSLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSLIST.html>`_

        Parameters
        ----------
        nloc1 : str
            List stresses from ``NLOC1`` (defaults to 1) to ``NLOC2`` (defaults to ``NLOC1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NLOC1`` = ALL, ``NLOC2`` and ``NINC`` are ignored and stresses
            for all locations are listed.

        nloc2 : str
            List stresses from ``NLOC1`` (defaults to 1) to ``NLOC2`` (defaults to ``NLOC1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NLOC1`` = ALL, ``NLOC2`` and ``NINC`` are ignored and stresses
            for all locations are listed.

        ninc : str
            List stresses from ``NLOC1`` (defaults to 1) to ``NLOC2`` (defaults to ``NLOC1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NLOC1`` = ALL, ``NLOC2`` and ``NINC`` are ignored and stresses
            for all locations are listed.

        nev : str
            Event number for stress listing (defaults to ALL).

        nlod : str
            Loading number for stress listing (defaults to ALL).

        Notes
        -----

        .. _FSLIST_notes:

        Stresses may be listed per location, per event, per loading, or per stress condition. Use FELIST and
        FLLIST if only event and location parameters (no stresses) are to be listed.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FSLIST,{nloc1},{nloc2},{ninc},{nev},{nlod}"
        return self.run(command, **kwargs)

    def fsnode(self, node: str = "", nev: str = "", nlod: str = "", **kwargs):
        r"""Calculates and stores the stress components at a node for fatigue.

        Mechanical APDL Command: `FSNODE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSNODE.html>`_

        Parameters
        ----------
        node : str
            Node number for which stress components are stored.

        nev : str
            Event number to be associated with these stresses (defaults to 1).

        nlod : str
            Loading number to be associated with these stresses (defaults to 1).

        Notes
        -----

        .. _FSNODE_notes:

        Calculates and stores the total stress components at a specified node for fatigue. Stresses are
        stored according to the event number and loading number specified. The location is associated with
        that previously defined for this node (FL) or else it is automatically defined. Stresses are stored
        as six total components (SX through SYZ). Temperature and current time are also stored along with
        the total stress components. Calculations are made from the stresses currently in the database (last
        :ref:`set` or :ref:`lcase` command). Stresses stored are in global Cartesian coordinates, regardless
        of the active results coordinate system ( :ref:`rsys` ).

        You can issue the FSLIST command to list stresses, and the FS command to modify stored stresses.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FSNODE,{node},{nev},{nlod}"
        return self.run(command, **kwargs)

    def fsplot(self, nloc: str = "", nev: str = "", item: int | str = "", **kwargs):
        r"""Displays a fatigue stress item for a fatigue location and event.

        Mechanical APDL Command: `FSPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FSPLOT.html>`_

        Parameters
        ----------
        nloc : str
            Display stresses associated with location ``NLOC``.

        nev : str
            Display stresses associated with event ``NEV``.

        item : int or str
            Display stresses associated with item number ``ITEM``. Items are as follows:

            * ``1-6`` - SX, SY, SZ, SXY, SYZ, SXZ total stress components

            * ``7`` - Temperature

            * ``8-13`` - SX, SY, SZ, SXY, SYZ, SXZ membrane-plus-bending stress components.

            * ``14`` - Time

        Notes
        -----

        .. _FSPLOT_notes:

        Displays a fatigue stress item as a function of loading number for a particular fatigue location and
        event.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FSPLOT,{nloc},{nev},{item}"
        return self.run(command, **kwargs)

    def ftcalc(self, nloc: str = "", node: str = "", **kwargs):
        r"""Performs fatigue calculations for a given node location.

        Mechanical APDL Command: `FTCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FTCALC.html>`_

        Parameters
        ----------
        nloc : str
            Location number of stress conditions to be used for fatigue calculation.

        node : str
            Node number (used only for convenience if ``NLOC`` is not input).

        Notes
        -----

        .. _FTCALC_notes:

        No additional usage notes are available for this command.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FTCALC,{nloc},{node}"
        return self.run(command, **kwargs)

    def ftsize(self, mxloc: str = "", mxev: str = "", mxlod: str = "", **kwargs):
        r"""Defines the fatigue data storage array.

        Mechanical APDL Command: `FTSIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FTSIZE.html>`_

        Parameters
        ----------
        mxloc : str
            Maximum number of fatigue locations (defaults to 5).

        mxev : str
            Maximum number of fatigue events (defaults to 10).

        mxlod : str
            Maximum number of loadings in each event (defaults to 3).

        Notes
        -----

        .. _FTSIZE_notes:

        Defines the size and erases the stress conditions for the fatigue data storage array. A stress
        condition is a loading (stresses) at a particular location (node) for a particular event. Size is
        defined in terms of the maximum number of locations, events, and loadings. The array size cannot be
        changed once data storage has begun (without erasing all previously stored data). If a size change
        is necessary, see the :ref:`ftwrite` command.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FTSIZE,{mxloc},{mxev},{mxlod}"
        return self.run(command, **kwargs)

    def ftwrite(self, fname: str = "", ext: str = "", **kwargs):
        r"""Writes all currently stored fatigue data on a file.

        Mechanical APDL Command: `FTWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FTWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name (defaults to :file:`Jobname` ).

        ext : str
            File name extension (defaults to FATG if ``Fname`` ).

        Notes
        -----

        .. _FTWRITE_notes:

        Data are written in terms of the equivalent POST1 fatigue commands (FTSIZE, FL, FS, etc.) which you
        can then edit and resubmit to POST1 (via the :ref:`input` command).

        After you have created a fatigue data file, each subsequent use of the FTWRITE command overwrites
        the contents of that file.

        .. warning::

            This command is archived in the latest version of the software.
        """
        command = f"FTWRITE,{fname},{ext}"
        return self.run(command, **kwargs)
