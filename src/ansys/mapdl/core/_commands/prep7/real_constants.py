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

class RealConstants:

    def r(self, nset: str = "", r1: str = "", r2: str = "", r3: str = "", r4: str = "", r5: str = "", r6: str = "", **kwargs):
        r"""Defines the element real constants.

        Mechanical APDL Command: `R <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_R.html>`_

        Parameters
        ----------
        nset : str
            Real constant set identification number (arbitrary). If same as a previous set number, set is
            redefined. Set number relates to that defined with the element ( :ref:`real` ). Note that the
            GUI automatically assigns this value.

        r1 : str
            Real constant values (interpreted as area, moment of inertia, thickness, etc., as required for
            the particular element type using this set), or table names for tabular input of boundary
            conditions. Use :ref:`rmore` command if more than six real constants per set are to be input.

        r2 : str
            Real constant values (interpreted as area, moment of inertia, thickness, etc., as required for
            the particular element type using this set), or table names for tabular input of boundary
            conditions. Use :ref:`rmore` command if more than six real constants per set are to be input.

        r3 : str
            Real constant values (interpreted as area, moment of inertia, thickness, etc., as required for
            the particular element type using this set), or table names for tabular input of boundary
            conditions. Use :ref:`rmore` command if more than six real constants per set are to be input.

        r4 : str
            Real constant values (interpreted as area, moment of inertia, thickness, etc., as required for
            the particular element type using this set), or table names for tabular input of boundary
            conditions. Use :ref:`rmore` command if more than six real constants per set are to be input.

        r5 : str
            Real constant values (interpreted as area, moment of inertia, thickness, etc., as required for
            the particular element type using this set), or table names for tabular input of boundary
            conditions. Use :ref:`rmore` command if more than six real constants per set are to be input.

        r6 : str
            Real constant values (interpreted as area, moment of inertia, thickness, etc., as required for
            the particular element type using this set), or table names for tabular input of boundary
            conditions. Use :ref:`rmore` command if more than six real constants per set are to be input.

        Notes
        -----

        .. _R_notes:

        Defines the element real constants. The real constants required for an element are shown in the
        Input Summary of each element description in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. Constants
        must be input in the same order
        as shown in that table. If more than the required number of element real constants are specified in
        a set, only those required are used. If fewer than the required number are specified, zero values
        are assumed for the unspecified constants.

        If using table inputs ( ``COMBIN14``, ``FLUID116``, ``SURF151``, ``SURF152``, ``CONTA172``,
        ``CONTA174``, ``CONTA175``, ``CONTA177``, and ``COMBI214`` only), enclose the table name in % signs
        (for example, ``%tabname%`` ).

        When copying real constants to new sets, Ansys, Inc. recommends that you use the command
        input. If you do use the GUI, restrict the real constant copy to only the first six real constants
        (real constants seven and greater will be incorrect for both the master and copy set).

        This command is also valid in SOLUTION.
        """
        command = f"R,{nset},{r1},{r2},{r3},{r4},{r5},{r6}"
        return self.run(command, **kwargs)



    def rdele(self, nset1: str = "", nset2: str = "", ninc: str = "", lchk: str = "", **kwargs):
        r"""Deletes real constant sets.

        Mechanical APDL Command: `RDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RDELE.html>`_

        Parameters
        ----------
        nset1 : str
            Delete real constant sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NSET1`` = ALL, ignore ``NSET2`` and ``NINC`` and all real
            constant sets are deleted.

        nset2 : str
            Delete real constant sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NSET1`` = ALL, ignore ``NSET2`` and ``NINC`` and all real
            constant sets are deleted.

        ninc : str
            Delete real constant sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NSET1`` = ALL, ignore ``NSET2`` and ``NINC`` and all real
            constant sets are deleted.

        lchk : str
            Specifies the level of element-associativity checking:

            * ``NOCHECK`` - No element-associativity check occurs. This option is the default.

            * ``WARN`` - When a section, material, or real constant is associated with an element, the program
              issues a message warning that the necessary entity has been deleted.

            * ``CHECK`` - The command terminates, and no section, material, or real constant is deleted if it is
              associated with an element.

        Notes
        -----

        .. _RDELE_notes:

        Deletes real constant sets defined with the :ref:`r` command.

        This command is also valid in SOLUTION.
        """
        command = f"RDELE,{nset1},{nset2},{ninc},{lchk}"
        return self.run(command, **kwargs)



    def rlist(self, nset1: str = "", nset2: str = "", ninc: str = "", **kwargs):
        r"""Lists the real constant sets.

        Mechanical APDL Command: `RLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RLIST.html>`_

        Parameters
        ----------
        nset1 : str
            List real constant sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NSET1`` = ALL (default), ignore ``NSET2`` and ``NINC`` and list
            all real constant sets ( :ref:`r` ).

        nset2 : str
            List real constant sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NSET1`` = ALL (default), ignore ``NSET2`` and ``NINC`` and list
            all real constant sets ( :ref:`r` ).

        ninc : str
            List real constant sets from ``NSET1`` to ``NSET2`` (defaults to ``NSET1`` ) in steps of
            ``NINC`` (defaults to 1). If ``NSET1`` = ALL (default), ignore ``NSET2`` and ``NINC`` and list
            all real constant sets ( :ref:`r` ).

        Notes
        -----

        .. _RLIST_notes:

        The real constant sets listed contain only those values specifically set by the user. Default values
        for real constants set automatically within the various elements are not listed.

        This command is valid in any processor.
        """
        command = f"RLIST,{nset1},{nset2},{ninc}"
        return self.run(command, **kwargs)



    def rmodif(self, nset: str = "", stloc: str = "", v1: str = "", v2: str = "", v3: str = "", v4: str = "", v5: str = "", v6: str = "", **kwargs):
        r"""Modifies real constant sets.

        Mechanical APDL Command: `RMODIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RMODIF.html>`_

        Parameters
        ----------
        nset : str
            Number of existing real constant set to be modified.

            The labels CONT and GCN are also valid input for defining or modifying real constants associated
            with contact elements (see :ref:`Notes). <RMODIF_notes>`

        stloc : str
            Starting location in table for modifying data. For example, if ``STLOC`` = 1, data input in the
            ``V1`` field is the first constant in the set. If ``STLOC`` = 7, data input in the ``V1`` field
            is the seventh constant in the set, etc. Must be greater than zero.

        v1 : str
            New values assigned to constants in the next five locations. If blank, the value remains
            unchanged.

        v2 : str
            New values assigned to constants in the next five locations. If blank, the value remains
            unchanged.

        v3 : str
            New values assigned to constants in the next five locations. If blank, the value remains
            unchanged.

        v4 : str
            New values assigned to constants in the next five locations. If blank, the value remains
            unchanged.

        v5 : str
            New values assigned to constants in the next five locations. If blank, the value remains
            unchanged.

        v6 : str
            New values assigned to constants in the next five locations. If blank, the value remains
            unchanged.

        Notes
        -----

        .. _RMODIF_notes:

        Allows modifying (or adding) real constants to an existing set ( :ref:`r` ) at any location.

        Specify ``NSET`` = CONT to define or modify real constants for all real constant sets associated
        with contact elements in pair-based contact definitions. Specify ``NSET`` = GCN to define or modify
        real constants for real constant sets that were previously assigned by the :ref:`gcdef` command;
        that is, real constants used in `general contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_
        interactions.

        This command is also valid in SOLUTION. For important information about using this command within
        the solution phase, see in the `Advanced Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_adv/advoceanloading.html>`_.
        """
        command = f"RMODIF,{nset},{stloc},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)



    def rmore(self, r7: str = "", r8: str = "", r9: str = "", r10: str = "", r11: str = "", r12: str = "", **kwargs):
        r"""Adds real constants to a set.

        Mechanical APDL Command: `RMORE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RMORE.html>`_

        Parameters
        ----------
        r7 : str
            Add real constants 7 to 12 (numerical values or table names) to the most recently defined set.

        r8 : str
            Add real constants 7 to 12 (numerical values or table names) to the most recently defined set.

        r9 : str
            Add real constants 7 to 12 (numerical values or table names) to the most recently defined set.

        r10 : str
            Add real constants 7 to 12 (numerical values or table names) to the most recently defined set.

        r11 : str
            Add real constants 7 to 12 (numerical values or table names) to the most recently defined set.

        r12 : str
            Add real constants 7 to 12 (numerical values or table names) to the most recently defined set.

        Notes
        -----

        .. _RMORE_notes:

        Adds six more real constants to the most recently defined set. Repeat the :ref:`rmore` command for
        constants 13 to 18, again for 19-24, etc.

        If using table inputs ( ``SURF151``, ``SURF152``, ``FLUID116``, ``CONTA172``, ``CONTA174``,
        ``CONTA175``, and ``CONTA177`` only), enclose the table name in % signs (for example, ``%tabname%``
        ).

        When copying real constants to new sets, Ansys, Inc. recommends that you use the command
        input. If you do use the GUI, restrict the real constant copy to only the first six real constants
        (real constants seven and greater will be incorrect for both the master and copy set).

        This command is also valid in SOLUTION.
        """
        command = f"RMORE,{r7},{r8},{r9},{r10},{r11},{r12}"
        return self.run(command, **kwargs)



    def setfgap(self, gap: str = "", ropt: int | str = "", pamb: str = "", acf1: str = "", acf2: str = "", pref: str = "", mfp: str = "", **kwargs):
        r"""Updates or defines the real constant table for squeeze film elements.

        Mechanical APDL Command: `SETFGAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SETFGAP.html>`_

        Parameters
        ----------
        gap : str
            Gap separation.

        ropt : int or str
            Real constant set option.

            * ``0`` - Creates separate real constant sets for each selected element with the specified real
              constant values (default).

            * ``1`` - Updates existing real constant sets. The gap separation is updated from displacement
              results in the database. Other real constants are updated as specified in the command input
              parameters.

        pamb : str
            Ambient pressure.

        acf1 : str
            Accommodation factor 1 and 2.

        acf2 : str
            Accommodation factor 1 and 2.

        pref : str
            Reference pressure for mean free path.

        mfp : str
            Mean free path.

        Notes
        -----

        .. _SETFGAP_notes:

        This command is used for large signal cases to update the gap separation real constant on a per-
        element basis. Issue this command prior to solution using the default ``ROPT`` value to initialize
        real constant sets for every fluid element. After a solution, you can re-issue the command to update
        the real constant set for a subsequent analysis. See for more information on thin film analyses.
        """
        command = f"SETFGAP,{gap},{ropt},,{pamb},{acf1},{acf2},{pref},{mfp}"
        return self.run(command, **kwargs)


