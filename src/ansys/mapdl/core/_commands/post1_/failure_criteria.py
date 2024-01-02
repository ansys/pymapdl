class FailureCriteria:
    def fc(
        self,
        mat="",
        lab1="",
        lab2="",
        data1="",
        data2="",
        data3="",
        data4="",
        data5="",
        data6="",
        **kwargs,
    ):
        """Provides failure criteria information and activates a data

        APDL Command: FC
        table to input temperature-dependent stress and strain limits.

        Parameters
        ----------
        mat
            Material reference number. You can define failure criteria
            for up to 250 different materials.

        lab1
            Type of data.

            TEMP - Temperatures. Each of the materials you define can
            have a different set of temperatures to define the failure
            criteria.

            EPEL - Strains.

            S - Stresses.

        lab2
            Specific criteria. Not used if Lab1 = TEMP.

            XTEN - Allowable tensile stress or strain in the
            x-direction. (Must be positive.)

            XCMP - Allowable compressive stress or strain in the
            x-direction. (Defaults to negative of XTEN.)

            YTEN - Allowable tensile stress or strain in the
            y-direction. (Must be positive.)

            YCMP - Allowable compressive stress or strain in the
            y-direction. (Defaults to negative of YTEN.)

            ZTEN - Allowable tensile stress or strain in the
            z-direction. (Must be positive.)

            ZCMP - Allowable compressive stress or strain in the
            z-direction. (Defaults to negative of ZTEN.)

            XY - Allowable XY stress or shear strain. (Must be
            positive.)

            YZ - Allowable YZ stress or shear strain. (Must be
            positive.)

            XZ - Allowable XZ stress or shear strain. (Must be
            positive.)

            XYCP - XY coupling coefficient (Used only if Lab1 =
            S). Defaults to -1.0. [1]

            YZCP - YZ coupling coefficient (Used only if Lab1 =
            S). Defaults to -1.0. [1]

            XZCP - XZ coupling coefficient (Used only if Lab1 =
            S). Defaults to -1.0. [1]

        data1, data2, data3, . . . , data6
            Description of DATA1 through DATA6.

            T1, T2, T3, T4, T5, T6 - Temperature at which limit data
            is input. Used only when Lab1 = TEMP.

            V1, V2, V3, V4, V5, V6 - Value of limit stress or strain
            at temperature T1 through T6. Used only when Lab1 = S or
            EPEL.

        Notes
        -----
        The data table can be input in either PREP7 or POST1. This
        table is used only in POST1. When you postprocess failure
        criteria results defined via the FC command (PLESOL, PRESOL,
        PLNSOL, PRNSOL, PRRSOL, etc.), the active coordinate system
        must be the coordinate system of the material being
        analyzed. You do this using RSYS, SOLU. For layered
        applications, you also use the LAYER command. See the specific
        element documentation in the Element Reference for information
        on defining your coordinate system for layers.

        Some plotting and printing functions will not support Failure
        Criteria for your PowerGraphics displays. This could result in
        minor changes to other data when Failure Criteria are
        applied. See the appropriate plot or print command
        documentation for more information.
        """
        command = "FC,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(mat),
            str(lab1),
            str(lab2),
            str(data1),
            str(data2),
            str(data3),
            str(data4),
            str(data5),
            str(data6),
        )
        return self.run(command, **kwargs)

    def fccheck(self, **kwargs):
        """Checks both the strain and stress input criteria for all materials.

         APDL Command: FCCHECK

        Notes
        -----
        Issue the FCCHECK command to check the completeness of the input during
        the input phase.
        """
        command = "FCCHECK,"
        return self.run(command, **kwargs)

    def fcdele(self, mat="", **kwargs):
        """Deletes previously defined failure criterion data for the given

        APDL Command: FCDELE
        material.

        Parameters
        ----------
        mat
            Material number. Deletes all FC command input for this material.

        Notes
        -----
        This command is also valid in POST1.
        """
        command = "FCDELE,%s" % (str(mat))
        return self.run(command, **kwargs)

    def fclist(self, mat="", temp="", **kwargs):
        """To list what the failure criteria is that you have input.

        APDL Command: FCLIST

        Parameters
        ----------
        mat
             Material number (defaults to ALL for all materials).

        temp
            Temperature to be evaluated at (defaults to TUNIF).

        Notes
        -----
        This command allows you to see what you have already input for failure
        criteria using the FC commands.
        """
        return self.run(f"FCLIST,{mat},,{temp}", **kwargs)

    def fctyp(self, oper="", lab="", **kwargs):
        """Activates or removes failure-criteria types for postprocessing.

        APDL Command: FCTYP

        Parameters
        ----------
        oper
            Operation key:

            ADD - Activate failure-criteria types. This option is the default behavior.

            DELE - Remove failure-criteria types.

        lab
            Valid failure-criteria labels. If ALL, select all available
            (including user-defined) failure criteria.

            EMAX - Maximum strain criterion (default)

            SMAX - Maximum stress criterion (default)

            TWSI  - Tsai-Wu strength index (default)

            TWSR  - Inverse of Tsai-Wu strength ratio index (default)

            HFIB  - Hashin fiber failure criterion

            HMAT  - Hashin matrix failure criterion

            PFIB  - Puck fiber failure criterion

            PMAT  - Puck inter-fiber (matrix) failure criterion

            L3FB - LaRc03 fiber failure criterion

            L3MT - LaRc03 matrix failure criterion

            L4FB - LaRc04 fiber failure criterion

            L4MT - LaRc04 matrix failure criterion

            USR1 through USR9  - User-defined failure criteria

        Notes
        -----
        The FCTYP command modifies the list of active failure criteria.

        By default, active failure criteria include EMAX, SMAX, TWSI, and TWSR.

        The command affects any subsequent postprocessing listing and plotting
        commands (such as PRESOL, PRNSOL, PLESOL, PLNSOL, and ETABLE).

        A single FCTYP command allows up to six failure-criteria labels. If
        needed, reissue the command to activate or remove additional failure-
        criteria types.
        """
        command = f"FCTYP,{oper},{lab}"
        return self.run(command, **kwargs)
