"""
These PREP7 commands define the model real constants.
"""


class RealConstants:
    def r(self, nset="", r1="", r2="", r3="", r4="", r5="", r6="", **kwargs):
        """APDL Command: R

        Defines the element real constants.

        Parameters
        ----------
        nset
            Real constant set identification number (arbitrary).  If same as a
            previous set number, set is redefined. Set number relates to that
            defined with the element [REAL]. Note that the GUI automatically
            assigns this value.

        r1, r2, r3, . . . , r6
            Real constant values (interpreted as area, moment of inertia,
            thickness, etc., as required for the particular element type using
            this set), or table names for tabular input of boundary conditions.
            Use RMORE command if more than six real constants per set are to be
            input.

        Notes
        -----
        Defines the element real constants.  The real constants required for an
        element are shown in the Input Summary of each element description in
        the Element Reference.  Constants must be input in the same order as
        shown in that table.  If more than the required number of element real
        constants are specified in a set, only those required are used.  If
        fewer than the required number are specified, zero values are assumed
        for the unspecified constants.

        If using table inputs (SURF151, SURF152, FLUID116, CONTA171, CONTA172,
        CONTA173, CONTA174, and CONTA175 only), enclose the table name in %
        signs (e.g., %tabname%).

        Specify NSET = GCN to define real constants for real constant sets that
        were previously assigned by the GCDEF command (that is, real constants
        used in general contact interactions).

        When copying real constants to new sets, ANSYS, Inc. recommends that
        you use the command input. If you do use the GUI, restrict the real
        constant copy to only the first six real constants (real constants
        seven and greater will be incorrect for both the master and copy set).

        This command is also valid in SOLUTION.
        """
        command = "R,%s,%s,%s,%s,%s,%s,%s" % (
            str(nset),
            str(r1),
            str(r2),
            str(r3),
            str(r4),
            str(r5),
            str(r6),
        )
        return self.run(command, **kwargs)

    def rdele(self, nset1="", nset2="", ninc="", lchk="", **kwargs):
        """APDL Command: RDELE

        Deletes real constant sets.

        Parameters
        ----------
        nset1, nset2, ninc
            Delete real constant sets from NSET1 to NSET2 (defaults to NSET1)
            in steps of NINC (defaults to 1).  If NSET1 = ALL, ignore NSET2 and
            NINC and all real constant sets are deleted.

        lchk
            Specifies the level of element-associativity checking:

            NOCHECK - No element-associativity check occurs. This option is the default.

            WARN - When a section, material, or real constant is associated with an element, ANSYS
                   issues a message warning that the necessary entity has been
                   deleted.

            CHECK - The command terminates, and no section, material, or real constant is deleted
                    if it is associated with an element.

        Notes
        -----
        Deletes real constant sets defined with the R command.

        This command is also valid in SOLUTION.
        """
        command = "RDELE,%s,%s,%s,%s" % (
            str(nset1),
            str(nset2),
            str(ninc),
            str(lchk),
        )
        return self.run(command, **kwargs)

    def rlist(self, nset1="", nset2="", ninc="", **kwargs):
        """APDL Command: RLIST

        Lists the real constant sets.

        Parameters
        ----------
        nset1, nset2, ninc
            List real constant sets from NSET1 to NSET2 (defaults to NSET1) in
            steps of NINC (defaults to 1).  If NSET1 = ALL (default), ignore
            NSET2  and NINC and list all real constant sets [R].

        Notes
        -----
        The real constant sets listed contain only those values specifically
        set by the user.  Default values for real constants set automatically
        within the various elements are not listed.

        This command is valid in any processor.
        """
        command = "RLIST,%s,%s,%s" % (str(nset1), str(nset2), str(ninc))
        return self.run(command, **kwargs)

    def rmodif(
        self,
        nset="",
        stloc="",
        v1="",
        v2="",
        v3="",
        v4="",
        v5="",
        v6="",
        **kwargs,
    ):
        """APDL Command: RMODIF

        Modifies real constant sets.

        Parameters
        ----------
        nset
            Number of existing real constant set to be modified.

        stloc
            Starting location in table for modifying data.  For example, if
            STLOC = 1, data input in the V1 field is the first constant in the
            set.  If STLOC = 7, data input in the V1 field is the seventh
            constant in the set, etc.  Must be greater than zero.

        v1
            New value assigned to constant in location STLOC.  If zero (or
            blank), a zero value will be assigned.

        v2, v3, v4, . . . , v6
            New values assigned to constants in the next five locations.  If
            blank, the value remains unchanged.

        Notes
        -----
        Allows modifying (or adding) real constants to an existing set [R] at
        any location.

        Specify NSET = GCN to define/modify real constants for real constant
        sets that were previously assigned by the GCDEF command (that is, real
        constants used in general contact interactions).

        This command is also valid in SOLUTION. For important information about
        using this command within the solution phase, see What Are Nonstandard
        Uses? in the Advanced Analysis Guide.
        """
        command = "RMODIF,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(nset),
            str(stloc),
            str(v1),
            str(v2),
            str(v3),
            str(v4),
            str(v5),
            str(v6),
        )
        return self.run(command, **kwargs)

    def rmore(self, r7="", r8="", r9="", r10="", r11="", r12="", **kwargs):
        """APDL Command: RMORE

        Adds real constants to a set.

        Parameters
        ----------
        r7, r8, r9, . . . , r12
            Add real constants 7 to 12 (numerical values or table names) to the
            most recently defined set.

        Notes
        -----
        Adds six more real constants to the most recently defined set.  Repeat
        the RMORE command for constants 13 to 18, again for 19-24, etc.

        If using table inputs (SURF151, SURF152, FLUID116, CONTA171, CONTA172,
        CONTA173, CONTA174, and CONTA175 only), enclose the table name in %
        signs (e.g., %tabname%).

        When copying real constants to new sets, ANSYS, Inc. recommends that
        you use the command input. If you do use the GUI, restrict the real
        constant copy to only the first six real constants (real constants
        seven and greater will be incorrect for both the master and copy set).

        This command is also valid in SOLUTION.
        """
        command = "RMORE,%s,%s,%s,%s,%s,%s" % (
            str(r7),
            str(r8),
            str(r9),
            str(r10),
            str(r11),
            str(r12),
        )
        return self.run(command, **kwargs)

    def setfgap(
        self,
        gap="",
        ropt="",
        pamb="",
        acf1="",
        acf2="",
        pref="",
        mfp="",
        **kwargs,
    ):
        """APDL Command: SETFGAP

        Updates or defines the real constant table for squeeze film elements.

        Parameters
        ----------
        gap
            Gap separation.

        ropt
            Real constant set option.

            0 - Creates separate real constant sets for each selected element with the
                specified real constant values (default).

            1 - Updates existing real constant sets. The gap separation is updated from
                displacement results in the database. Other real constants are
                updated as specified in the command input parameters.

        pamb
            Ambient pressure.

        acf1, acf2
            Accommodation factor 1 and 2.

        pref
            Reference pressure for mean free path.

        mfp
            Mean free path.

        Notes
        -----
        This command is used for large signal cases to update the gap
        separation real constant on a per-element basis.  Issue this command
        prior to solution using the default ROPT value to initialize real
        constant sets for every fluid element.  After a solution, you can re-
        issue the command to update the real constant set for a subsequent
        analysis. See Introduction for more information on thin film analyses.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"SETFGAP,{gap},{ropt},,{pamb},{acf1},{acf2},{pref},{mfp}"
        return self.run(command, **kwargs)
