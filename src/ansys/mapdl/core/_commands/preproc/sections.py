class Sections:
    def bsax(self, val1="", val2="", t="", **kwargs):
        """Specifies the axial strain and axial force relationship for beam

        APDL Command: BSAX
        sections.

        Parameters
        ----------
        val1
            Axial strain component (ε).

        val2
            Axial force component (N).

        t
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The BSAX command, one of several nonlinear general beam section
        commands, specifies the relationship of axial strain and axial force
        for a beam section. The section data defined is associated with the
        section most recently defined (via the SECTYPE command).

        Unspecified values default to zero.

        Related commands are BSM1, BSM2, BSTQ, BSS1, BSS2, BSMD, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSAX,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bsm1(self, val1="", val2="", t="", **kwargs):
        """Specifies the bending curvature and moment relationship in plane XZ for

        APDL Command: BSM1
        beam sections.

        Parameters
        ----------
        val1
            Curvature component (κ1).

        val2
            Bending moment component (M1).

        t
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The BSM1 command, one of several nonlinear general beam section
        commands, specifies the bending curvature and moment for plane XZ of a
        beam section. The section data defined is associated with the section
        most recently defined (via the SECTYPE command).

        Unspecified values default to zero.

        Related commands are BSAX, BSM2, BSTQ, BSS1, BSS2, BSMD, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSM1,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bsm2(self, val1="", val2="", t="", **kwargs):
        """Specifies the bending curvature and moment relationship in plane XY for

        APDL Command: BSM2
        beam sections.

        Parameters
        ----------
        val1
            Curvature component (κ2).

        val2
            Bending moment component (M2).

        t
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The BSM2 command, one of several nonlinear general beam section
        commands, specifies the bending curvature and moment relationship for
        plane XY of a beam section. The section data defined is associated with
        the section most recently defined (via the SECTYPE command).

        Unspecified values default to zero.

        Related commands are BSAX, BSM1, BSTQ, BSS1, BSS2, BSMD, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSM2,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bsmd(self, dens="", **kwargs):
        """Specifies mass per unit length for a nonlinear general beam section.

        APDL Command: BSMD

        Parameters
        ----------
        dens
            Mass density.

        Notes
        -----
        The BSMD command, one of several nonlinear general beam section
        commands, specifies the mass density (assuming a unit area) for a beam
        section. The value specified is associated with the section most
        recently defined (via the SECTYPE command).

        Related commands are BSAX, BSM1, BSM2, BSTQ, BSS1, BSS2, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSMD,{dens}"
        return self.run(command, **kwargs)

    def bss1(self, val1="", val2="", t="", **kwargs):
        """Specifies the transverse shear strain and force relationship in plane

        APDL Command: BSS1
        XZ for beam sections.

        Parameters
        ----------
        val1
            Transverse shear strain component (γ1).

        val2
            Transverse shear force component (S1).

        t
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The BSS1 command, one of several nonlinear general beam section
        commands, specifies the transverse shear strain and transverse shear
        force relationship for plane XZ of a beam section. The section data
        defined is associated with the section most recently defined (via the
        SECTYPE command).

        Unspecified values default to zero.

        Related commands are BSAX, BSM1, BSM2, BSTQ, BSS2, BSMD, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSS1,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bss2(self, val1="", val2="", t="", **kwargs):
        """Specifies the transverse shear strain and force relationship in plane

        APDL Command: BSS2
        XY for beam sections.

        Parameters
        ----------
        val1
            Transverse shear strain component (γ2).

        val2
            Transverse shear force component (S2).

        t
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The BSS1 command, one of several nonlinear general beam section
        commands, specifies the transverse shear strain and transverse shear
        force relationship for plane XY of a beam section. The section data
        defined is associated with the section most recently defined (via the
        SECTYPE command).

        Unspecified values default to zero.

        Related commands are BSAX, BSM1, BSM2, BSTQ, BSS1, BSMD, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSS2,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bste(self, alpha="", **kwargs):
        """Specifies a thermal expansion coefficient for a nonlinear general beam

        APDL Command: BSTE
        section.

        Parameters
        ----------
        alpha
            Coefficient of thermal expansion for the cross section.

        Notes
        -----
        The BSTE command, one of several nonlinear general beam section
        commands, specifies a thermal expansion coefficient for a beam section.
        The value specified is associated with the section most recently
        defined (via the SECTYPE command).

        Related commands are BSAX, BSM1, BSM2, BSTQ, BSS1, BSS2, and BSMD.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSTE,{alpha}"
        return self.run(command, **kwargs)

    def bstq(self, val1="", val2="", t="", **kwargs):
        """Specifies the cross section twist and torque relationship for beam

        APDL Command: BSTQ
        sections.

        Parameters
        ----------
        val1
            Twist component (χ).

        val2
            Torque component (τ).

        t
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The BSTQ command, one of several nonlinear general beam section
        commands, specifies the cross section twist and torque relationship for
        a beam section. The section data defined is associated with the section
        most recently defined (via the SECTYPE command).

        Unspecified values default to zero.

        Related commands are BSAX, BSM1, BSM2, BSS1, BSS2, BSMD, and BSTE.

        For complete information, see Using Nonlinear General Beam Sections.
        """
        command = f"BSTQ,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def cbmd(
        self,
        row="",
        c_r__r_="",
        c_r__r_plus_1_="",
        c_r__r_plus_2_="",
        c_r__r_plus_3_="",
        c_r__r_plus_4_="",
        c_r__r_plus_5_="",
        **kwargs,
    ):
        """Specifies preintegrated section mass matrix for composite-beam

        APDL Command: CBMD
        sections.

        Parameters
        ----------
        row
            Row number of the matrix.

        c(r)(r), . . . , c(r)(r+5)
            Upper triangle of the cross-section mass matrix [C].

        Notes
        -----
        With a unit beam length, the section mass matrix relates the resultant
        forces and torques to accelerations and angular accelerations as
        follows (applicable to the local element coordinate system):

        The CBMD command, one of several composite beam section commands,
        specifies the section mass matrix (submatrix [C] data) for a composite
        beam section. The section data defined is associated with the section
        most recently defined (SECTYPE) at the specified temperature (CBTMP).

        Unspecified values default to zero.

        Related commands are CBTMP, CBTE, and CBMX.

        For complete information, see Using Preintegrated Composite Beam
        Sections.
        """
        command = f"CBMD,{row},{c_r__r_},{c_r__r_plus_1_},{c_r__r_plus_2_},{c_r__r_plus_3_},{c_r__r_plus_4_},{c_r__r_plus_5_}"
        return self.run(command, **kwargs)

    def cbmx(
        self,
        row="",
        s_r__r_="",
        s_r__r_plus_1_="",
        s_r__r_plus_2_="",
        s_r__r_plus_3_="",
        s_r__r_plus_4_="",
        s_r__r_plus_5_="",
        s_r__r_plus_6_="",
        **kwargs,
    ):
        """Specifies preintegrated cross-section stiffness for composite beam

        APDL Command: CBMX
        sections.

        Parameters
        ----------
        row
            Row number of the matrix.

        s(r)(r), . . . , s(r)(r+6)
            Upper triangle of the cross-section stiffness matrix [S].

        Notes
        -----
        The behavior of beam elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The CBMX command, one of several composite beam section commands,
        specifies the cross-section stiffness matrix (submatrix [S] data) for a
        composite beam section. The section data defined is associated with the
        section most recently defined (SECTYPE) at the specified temperature
        (CBTMP).

        Unspecified values default to zero.

        Related commands are CBTMP, CBTE, and CBMD.

        For complete information, see Using Preintegrated Composite Beam
        Sections.
        """
        command = f"CBMX,{row},{s_r__r_},{s_r__r_plus_1_},{s_r__r_plus_2_},{s_r__r_plus_3_},{s_r__r_plus_4_},{s_r__r_plus_5_},{s_r__r_plus_6_}"
        return self.run(command, **kwargs)

    def cbte(self, alpha="", **kwargs):
        """Specifies a thermal expansion coefficient for a composite beam section.

        APDL Command: CBTE

        Parameters
        ----------
        alpha
            Coefficient of thermal expansion for the cross section.

        Notes
        -----
        The CBTE command, one of several composite beam section commands,
        specifies a thermal expansion coefficient for a beam section. The value
        specified is associated with the section most recently defined
        (SECTYPE) at the specified temperature (CBTMP).

        Unspecified values default to zero.

        Related commands are CBTMP, CBMX, and CBMD.

        For complete information, see Using Preintegrated Composite Beam
        Sections.
        """
        command = f"CBTE,{alpha}"
        return self.run(command, **kwargs)

    def cbtmp(self, temp="", **kwargs):
        """Specifies a temperature for composite-beam input.

        APDL Command: CBTMP

        Parameters
        ----------
        temp
            Temperature value.

        Notes
        -----
        The CBTMP command, one of several composite beam-section commands,
        specifies a temperature to be associated with the data input via
        subsequent CBMX (preintegrated cross-section stiffness), CBMD
        (preintegrated section mass), or CBTE (thermal-expansion) commands.

        The specified temperature remains active until the next CBTMP command
        is issued.

        An unspecified temperature value defaults to zero.

        For complete information, see Using Preintegrated Composite Beam
        Sections.
        """
        command = f"CBTMP,{temp}"
        return self.run(command, **kwargs)

    def sdelete(self, sfirst="", slast="", sinc="", knoclean="", lchk="", **kwargs):
        """Deletes sections from the database.

        APDL Command: SDELETE

        Parameters
        ----------
        sfirst
            First section ID to be deleted; defaults to first available section
            in the database.

        slast
            Last section ID to be deleted; defaults to last available section
            in the database.

        sinc
            Increment of the section ID; defaults to 1.

        knoclean
            Pretension element cleanup key (pretension sections only).

            0 - Perform cleanup of pretension elements (delete pretension elements and
                reconnect elements split during PSMESH).

            1 - Do not perform cleanup.

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
        Deletes one or more specified sections and their associated data from
        the ANSYS database.
        """
        command = f"SDELETE,{sfirst},{slast},{sinc},{knoclean},{lchk}"
        return self.run(command, **kwargs)

    def secmodif(self, secid="", kywrd="", **kwargs):
        """Modifies a pretension section

        APDL Command: SECMODIF

        Parameters
        ----------
        secid
            Unique section number. This number must already be assigned to a
            section.

        norm
            Keyword specifying that the command will modify the pretension
            section normal direction.

        nx, ny, nz
            Specifies the individual normal components to modify.

        kcn
            Coordinate system number. This can be either 0 (Global Cartesian),
            1 (Global Cylindrical) 2 (Global Spherical), 4 (Working Plane), 5
            (Global Y Axis Cylindrical) or an arbitrary reference number
            assigned to a coordinate system.

        Notes
        -----
        The SECMODIF command either modifies the normal for a specified
        pretension section, or changes the name of the specified pretension
        surface.
        """
        command = f"SECMODIF,{secid},{kywrd}"
        return self.run(command, **kwargs)

    def secfunction(self, table="", kcn="", **kwargs):
        """Specifies shell section thickness as a tabular function.

        APDL Command: SECFUNCTION

        Parameters
        ----------
        table
            Table name or array parameter reference for specifying thickness.

        kcn
            Local coordinate system reference number or array interpretation
            pattern for this tabular function evaluation.

        Notes
        -----
        The SECFUNCTION command is associated with the section most recently
        defined via the SECTYPE command.

        A table (TABLE) can define tabular thickness as a function of
        coordinates. Alternatively, you can use an array parameter (indexed by
        node number) that expresses the function to be mapped. (For example,
        func (17) should be the desired shell thickness at node 17.)  To
        specify a table, enclose the table or array name in percent signs (%)
        (SECFUNCTION,%tablename%). Use the ``*DIM`` command to define a table.

        The table or array defines the total shell thickness at any point in
        space. In multilayered sections, the total thickness and each layer
        thickness are scaled accordingly.

        The Function Tool is a convenient way to define your thickness tables.
        For more information, see Using the Function Tool in the Basic Analysis
        Guide.

        If you do not specify a local coordinate system (KCN), the program
        interprets TABLE in global XYZ coordinates. (For information about
        local coordinate systems, see the LOCAL command documentation.)

        When KCN = NODE, the program interprets TABLE as an array parameter
        (indexed by node number) that expresses the function to be mapped.

        When KCN = NOD2, the program interprets TABLE as a 2-D array parameter
        (where columns contain node numbers and rows contain the corresponding
        thicknesses) that expresses the function to be mapped.
        """
        command = f"SECFUNCTION,{table},{kcn}"
        return self.run(command, **kwargs)

    def seccontrol(
        self,
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        val7="",
        val8="",
        val9="",
        val10="",
        val11="",
        val12="",
        val13="",
        **kwargs,
    ):
        """Supplements or overrides default section properties.

        APDL Command: SECCONTROL

        Parameters
        ----------
        val1, val2, val3, . . . , val13
            Values, such as the length of a side or the numbers of cells along
            the width, that describe the geometry of a section. See the "Notes"
            section of this command description for details about these values
            for the various section types.

        Notes
        -----
        The  SECCONTROL command is divided into these operation types: Beams,
        Links, Pipes, Shells, and Reinforcings.

        Values are associated with the most recently issued SECTYPE command.
        The data required is determined by the section type and is different
        for each type.

        SECCONTROL overrides the program-calculated transverse-shear stiffness.

        The command does not apply to thermal shell elements SHELL131 and
        SHELL132 or thermal solid elements SOLID278 and SOLID279.
        """
        command = f"SECCONTROL,{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12},{val13}"
        return self.run(command, **kwargs)

    def secdata(
        self,
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        val7="",
        val8="",
        val9="",
        val10="",
        val11="",
        val12="",
        **kwargs,
    ):
        """Describes the geometry of a section.

        APDL Command: SECDATA

        Parameters
        ----------
        val1, val2, val3, . . . , val12
            Values, such as thickness or the length of a side or the numbers of
            cells along the width, that describe the geometry of a section. The
            terms VAL1, VAL2, etc. are specialized for each type of cross-
            section.

        Notes
        -----
        The SECDATA command defines the data describing the geometry of a
        section. The command is divided into these section types: Beams, Links,
        Pipes, Axisymmetric, Taper, Shells, Pretension, Joints, Reinforcing,
        and Contact.

        The data input on the SECDATA command is interpreted based on the most
        recently issued SECTYPE command. The data required is determined by the
        section type and subtype, and is different for each one.

        Beam sections are referenced by BEAM188 and BEAM189 elements. Not all
        SECOFFSET location values are valid for each subtype.

        Type: BEAM, Subtype: RECT

        Type: BEAM, Subtype: QUAD

        Degeneration to triangle is permitted by specifying the same
        coordinates for cells along an edge.

        Type: BEAM, Subtype: CSOLID

        Type: BEAM, Subtype: CTUBE

        This subtype is similar to type PIPE. However, elements using PIPE
        account for internal or external pressures, whereas elements using
        CTUBE do not.

        Type: BEAM, Subtype: CHAN

        Type: BEAM, Subtype: I

        Type: BEAM, Subtype: Z

        Type: BEAM, Subtype: L

        If W2 is a negative value, the section will be flipped.

        Type: BEAM, Subtype: T

        If W2 is a negative value, the section will be flipped.

        Type: BEAM, Subtype: HATS
        """
        command = f"SECDATA,{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12}"
        return self.run(command, **kwargs)

    def secjoint(
        self,
        kywrd="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        **kwargs,
    ):
        """Defines local coordinate systems at joint element nodes and other data

        APDL Command: SECJOINT
        for joint elements.

        Parameters
        ----------
        kywrd
            Keyword that indicates the type of joint element data being
            defined.

            LSYS or blank - Define local coordinate systems at the nodes that form the MPC184 joint
                            element.

            RDOF - Define the relative degrees of freedom to be fixed for an MPC184-General joint
                   element.

            PITC - Define the pitch of an MPC184-Screw joint element.

            FRIC - Define the geometric quantities required for Coulomb frictional behavior in the
                   MPC184-Revolute or MPC184-Translational joint element.

        val1, val2, val3, val4, val5, val6
            The meaning of Val1 through Val6 changes, depending on the value of
            Kywrd.

        Notes
        -----
        Use this command to define additional section data for MPC184 joint
        elements. To overwrite the current values, issue another SECJOINT
        command with the same Kywrd value. The data input on this command is
        interpreted based on the most recently issued SECTYPE command.
        """
        command = f"SECJOINT,{kywrd},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def seclib(self, option="", path="", **kwargs):
        """Sets the default section library path for the SECREAD command.

        APDL Command: /SECLIB

        Parameters
        ----------
        option
            READ

            READ - Sets the read path (default).

            STATUS - Reports the current section library path setting to the Jobname.LOG file.

        path
            Defines the directory path from which to read section library
            files.

        Notes
        -----
        When the SECREAD command is issued without a directory path, the
        command searches for a section library in the following order:

        The user's home directory

        The current working directory

        The path specified by the /SECLIB command


        """
        command = f"/SECLIB,{option},{path}"
        return self.run(command, **kwargs)

    def seclock(
        self,
        dof1="",
        minvalue1="",
        maxvalue1="",
        dof2="",
        minvalue2="",
        maxvalue2="",
        dof3="",
        minvalue3="",
        maxvalue3="",
        **kwargs,
    ):
        """Specifies locks on the components of relative motion in a joint

        APDL Command: SECLOCK
        element.

        Parameters
        ----------
        dof
            Local degree of freedom to be locked.

        minvalue
            Low end of the range of allowed movement for the specified DOF.

        maxvalue
            High end of the range of allowed movement for the specified DOF.

        Notes
        -----
        Specify up to three DOFs to be locked. Locks are activated when the
        limit values are reached, and further motion in that DOF is frozen. If
        necessary, you may repeat the command.
        """
        command = f"SECLOCK,{dof1},{minvalue1},{maxvalue1},{dof2},{minvalue2},{maxvalue2},{dof3},{minvalue3},{maxvalue3}"
        return self.run(command, **kwargs)

    def secnum(self, secid="", **kwargs):
        """Sets the element section attribute pointer.

        APDL Command: SECNUM

        Parameters
        ----------
        secid
            Defines the section ID number to be assigned to the subsequently-
            defined elements.  Defaults to 1.  See SECTYPE for more information
            about the section ID number.
        """
        command = f"SECNUM,{secid}"
        return self.run(command, **kwargs)

    def secoffset(
        self,
        location="",
        offset1="",
        offset2="",
        cg_y="",
        cg_z="",
        sh_y="",
        sh_z="",
        **kwargs,
    ):
        """Defines the section offset for cross sections.

        APDL Command: SECOFFSET

        Parameters
        ----------
        location, offset1, offset2, cg-y, cg-z, sh-y, sh-z
            The location of the nodes in the section. All are dependent on the
            type. See the "Notes" section of this command description for
            details about these values for the various section types.

        Notes
        -----
        The SECOFFSET command is divided into three types: Beams, Pipes, and
        Shells.

        The offsets defined by the SECOFFSET command are associated with the
        section most recently defined using the SECTYPE command.  Not all
        SECOFFSET location values are valid for each subtype.

        For the thermal shell elements, SHELL131 and SHELL132, the node offset
        specified by SECOFFSET is used in thermal contact analyses.  Otherwise,
        the SECOFFSET command has no effect on the solution for these elements
        and is used only for visualization purposes.

        This command is not valid with thermal solid elements SOLID278 and
        SOLID279.
        """
        command = (
            f"SECOFFSET,{location},{offset1},{offset2},{cg_y},{cg_z},{sh_y},{sh_z}"
        )
        return self.run(command, **kwargs)

    def secplot(self, secid="", val1="", val2="", val3="", **kwargs):
        """Plots the geometry of a beam, pipe, shell, or reinforcing section to

        APDL Command: SECPLOT
        scale.

        Parameters
        ----------
        secid
            The section ID number (as defined via the SECTYPE command).

        val1, val2, val3
            Values that control the information to be plotted. See the "Notes"
            section of this command description for more information. For
            clarity, the labels VAL1, VAL2, and VAL3 are renamed according to
            the section type.

        Notes
        -----
        The SECPLOT command is valid only for "Beams and Pipes", "Shells", and
        "Reinforcings".

        SECPLOT cannot display the plot of an ASEC (arbitrary section) subtype.

        Plots the geometry of the beam or pipe section to scale depicting the
        centroid, shear center, and origin.  SECPLOT also lists various section
        properties such as Iyy, Iyz, and Izz.

        Data to be supplied in the value fields:

        Beam or pipe section mesh display options:

        Display section outline only.

        Display beam or pipe section mesh.

        Display the section mesh with node numbers.

        Display the section mesh with cell numbers.

        Display the section mesh with material numbers and colors.

        Display the section mesh with material colors only.

        Display the section mesh with the RST node numbers. RST nodes are
        section corner nodes where results are available. This is applicable
        when the averaged results format (KEYOPT(15) = 0 for BEAM188, BEAM189,
        PIPE288, and PIPE289) is used.

        Display the section mesh with the RST cell numbers. RST cells are
        section cells where results are available. This is applicable when the
        non-averaged results format (KEYOPT(15) = 1 for BEAM188, BEAM189,
        PIPE288, and PIPE289) is used.

        Options 2 through 6 do not depict centroid and shear center, nor do
        they list section properties.

        Following is a sample section plot for the beam section type:

        Plots the layer arrangement of the shell section showing the layer
        material and orientation.

        Data to be supplied in the value fields:

        The range of layer numbers to be displayed. If LAYR1 is greater than
        LAYR2, a reversed order display is produced. Up to 20 layers may be
        displayed at the same time. LAYR1 defaults to 1. LAYR2 defaults to
        LAYR1 if LAYR1 is input or to the number of layers (or to 19+LAYR1, if
        smaller) if LAYR1 is not input.

        Following is a sample section plot for the shell section type:

        Plots the arrangement of a reinforcing section within the base element.

        Data to be supplied in the value fields:

        REINF1, REINF2 -- The numerical range of reinforcings to be displayed.
        The default REINF1 value is 1. The default REINF2 value is the number
        of reinforcings.

        OVERLAY -- The section ID of the base element within which to display
        the reinforcing section. The section appears translucent and the
        reinforcing section is solid. Valid values are:

        SOLID -- Display a translucent solid block over the reinforcing section

        SECID -- A number corresponding to a specific section ID of the base
        element.

        If no OVERLAY value is specified, ANSYS displays the reinforcing
        section only.

        Following is a sample section plot for the reinforcing section type:

        For more information about reinforcing, see the documentation for the
        SECDATA command, and the REINF264 and REINF265 elements.
        """
        command = f"SECPLOT,{secid},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def secread(self, fname="", ext="", option="", **kwargs):
        """Reads a custom section library or a user-defined section mesh into

        APDL Command: SECREAD
        ANSYS.

        Parameters
        ----------
        fname
            Section library file name and directory path containing the section
            library file (248 characters maximum, including directory). If you
            do not specify a directory path, it will default to your working
            directory and you can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        option
            LIBRARY - Reads in a library of sections and
            theirassociated section data values; the default. A
            section library may be created by editing the
            section-defining portions of the Jobname.LOG file and
            saving it with a .SECT suffix.

        Notes
        -----
        The SECREAD command operates on the section specified via the
        most recently issued SECTYPE command. Issue a separate SECREAD
        command for each section ID that you want to read in.

        Here are excerpts from a sample user section mesh file for a
        section with 75 nodes, 13 cells, and 9 nodes per cell for a
        two-hole box section. Illustrations of the two-hole box
        section and the cell mesh for it appear later in this command
        description.

        The mesh file is divided into three sections: the First Line,
        the Cells Section, and the Nodes Section.  Here are brief
        descriptions of the contents of each.

        First Line: The First Line defines the number of nodes and the
        number of cells for the mesh.

        Cells Section: The Cells Section contains as many lines as
        there are cells.  In this example, there are thirteen cells,
        so there are thirteen lines in this section. In each line, the
        number "1" that follows the cell connectivity information is
        the material number.

        Cell nodal connectivity must be given in a counterclockwise
        direction, with the center node being the ninth node. For
        details, see Figure: 10:: Cell Mesh for the Two-hole Box
        Section.

        Nodes Section: The Nodes Section contains as many lines as
        there are nodes.  In this example, there are 75 nodes, so
        there are a total of 75 lines in this section.  Each node line
        contains the node's boundary flag, the Y coordinate of the
        node, and the Z coordinate of the node.  Currently, all node
        boundary flags appear as 0s in a cell mesh file (as
        illustrated in Figure: 9:: Two-hole Box Section). Since all
        node boundary flags are 0, SECREAD ignores them when it reads
        a cell mesh file into ANSYS.

        There cannot be any gaps in the node numbering of a cell mesh.
        The nodes in a cell mesh must be numbered consecutively, with
        the first node having a node number of 1, and the last node
        having a node number that is equal to the maximum number of
        nodes in the cell mesh.
        """
        return self.run(f"SECREAD,{fname},{ext},,{option}", **kwargs)

    def secstop(
        self,
        dof1="",
        minvalue1="",
        maxvalue1="",
        dof2="",
        minvalue2="",
        maxvalue2="",
        dof3="",
        minvalue3="",
        maxvalue3="",
        **kwargs,
    ):
        """Specifies stops on the components of relative motion in a joint

        APDL Command: SECSTOP
        element.

        Parameters
        ----------
        dof
            Local degree of freedom to be stopped.

        minvalue
            Low end of the range of allowed movement for the specified DOF.

        maxvalue
            High end of the range of allowed movement for the specified DOF.

        Notes
        -----
        Stops restrict motion in a DOF; motion beyond the MINVALUE or MAXVALUE
        is prevented (motion away from a limit is allowed). You can specify up
        to three stops. If necessary, you can repeat the command.
        """
        command = f"SECSTOP,{dof1},{minvalue1},{maxvalue1},{dof2},{minvalue2},{maxvalue2},{dof3},{minvalue3},{maxvalue3}"
        return self.run(command, **kwargs)

    def sectype(self, secid="", type_="", subtype="", name="", refinekey="", **kwargs):
        """Associates section type information with a section ID number.

        APDL Command: SECTYPE

        Parameters
        ----------
        secid
            Section identification number.

        type\_
            BEAM

            BEAM - Defines a beam section.

            TAPER - Defines a tapered beam or pipe section. The sections at the end points must be
                    topologically identical.

            GENB - Defines a nonlinear general (temperature-dependent) beam section.

            COMB - Defines a composite (temperature-dependent) beam section.

            PIPE - Defines a pipe section.

            LINK - Defines a link section.

            AXIS - Define the axis for a general axisymmetric section.

            SHELL - Defines a shell section.

            GENS - Defines a preintegrated general (temperature-dependent) shell section.

            PRETENSION - Defines a pretension section.

            JOINT - Defines a joint section.

            REINF - Defines a reinforcing section.

            CONTACT - Defines a contact section.

        subtype
            When Type = BEAM, the possible beam sections that can be defined
            for Subtype are:

        name
            An eight-character name for the section. Name can be a string such
            as "W36X210" or "HP13X73" for beam sections. Section name can
            consist of letters and numbers, but cannot contain punctuation,
            special characters, or spaces.

        refinekey
            Sets mesh refinement level for thin-walled beam sections. Valid
            values are 0 (the default - no mesh refinement) through 5 (high
            level of mesh refinement). This value has meaning only when Type =
            BEAM.

        Notes
        -----
        SECTYPE sets the section ID number, section type, and subtype for a
        section. If the section ID number is not specified, ANSYS increments
        the highest section ID number currently defined in the database by one.
        A previously-defined section with the same identification number will
        be redefined. The geometry data describing this section type is defined
        by a subsequent SECDATA command. Define the offsets by a subsequent
        SECOFFSET command. The SLIST command lists the section properties, and
        the SECPLOT command displays the section to scale. The SECNUM command
        assigns the section ID number to a subsequently-defined beam element.

        For a beam section (Type = BEAM), a subsequent SECDATA command builds a
        numeric model using a nine-node cell for determining the properties
        (Ixx, Iyy, etc.) of the section and for the solution to the Poisson's
        equation for torsional behavior. See Beam Analysis and Cross Sections
        in the Structural Analysis Guide for examples using the section
        commands.

        For a nonlinear general beam section (Type = GENB), the Subtype and
        REFINEKEY options do not apply. Subsequent commands are necessary to
        define the section: BSAX, BSM1, BSM2, BSTQ, BSS1, BSS2, BSMD, and BSTE
        are available. All other section commands are ignored for this section
        type.

        For a preintegrated composite-beam section (Type = COMB), the REFINEKEY
        options do not apply. Subsequent commands are necessary to define the
        section: CBTMP, CBMX, CBMD, and CBTE are available. All other section
        commands are ignored for this section type.

        For a tapered beam or pipe section (Type = TAPER), two subsequent
        SECDATA commands are required (one for each end section). Section ends
        must be topologically identical (same Subtype, number of cells and
        material IDs). For a tapered pipe section, end sections must have the
        same number of cells around the circumference and along the pipe wall,
        and the same shell section ID for a composite pipe wall.

        """
        command = f"SECTYPE,{secid},{type_},{subtype},{name},{refinekey}"
        return self.run(command, **kwargs)

    def secwrite(self, fname="", ext="", elem_type="", **kwargs):
        """Creates an ASCII file containing user mesh section information.

        APDL Command: SECWRITE

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        elem_type
            Element type attribute pointer (ET) for the elements that
            are part of the section.  See SECREAD for a detailed
            description.

        Notes
        -----
        Before creating a user mesh file, first create a model using
        2-D meshing. Use PLANE183 or MESH200 with KEYOPT(1) = 7
        (quadrilateral with 8 nodes option) to model the cells.
        SECWRITE creates an ASCII file that contains information about
        the nodes and cells that describe a beam section. For detailed
        information on how to create a user mesh file, see Creating
        Custom Cross Sections with a User-defined Mesh in the
        Structural Analysis Guide.
        """
        return self.run(f"SECWRITE,{fname},{ext},,{elem_type}", **kwargs)

    def sflex(self, ffax="", ffby="", ffbz="", ffto="", fftsy="", fftsz="", **kwargs):
        """Sets flexibility factors for the currently defined pipe element

        APDL Command: SFLEX
        section.

        Parameters
        ----------
        ffax
            Factor to increase axial flexibility. The default value is 1.0.

        ffby
            Factor to increase bending flexibility about element y axis
            (bending in the element x-z plane). The default value is 1.0.

        ffbz
            Factor to increase bending flexibility about element z axis
            (bending in the element x-y plane). The default value is FFBY.

        ffto
            Factor to increase torsional flexibility. The default value is 1.0.

        fftsy
            Factor to increase transverse shear flexibility in the element x-z
            plane. The default value is 1.0.

        fftsz
            Factor to increase transverse shear flexibility in the element x-y
            plane. The default value is FFTSY.

        Notes
        -----
        The SFLEX command sets section-flexibility factors for sections used by
        pipe elements.

        To increase stiffness, use a flexibility factor of less than 1.0.

        The FFBY and FFTSY arguments affect motion in the element x-z plane,
        and the FFBZ and FFTSZ arguments affect motion in the element x-y
        plane. For stout pipe structures with low slenderness ratios, set both
        FFBY and FFTSY--and/or both FFBZ and FFTSZ (the related bending and
        transverse shear factors)--to the same value to obtain the expected
        flexibility effect.

        When issued, the SFLEX command applies to the pipe section most
        recently defined via the SECTYPE command.

        SFLEX is valid only for linear material properties and small strain
        analyses. The command does not support offsets, temperature loading, or
        initial state loading. While the resulting displacements and reactions
        are valid, the stresses may not be valid.
        """
        command = f"SFLEX,{ffax},{ffby},{ffbz},{ffto},{fftsy},{fftsz}"
        return self.run(command, **kwargs)

    def slist(self, sfirst="", slast="", sinc="", details="", type_="", **kwargs):
        """Summarizes the section properties for all defined sections in the

        APDL Command: SLIST
        current session.

        Parameters
        ----------
        sfirst
            First section ID to be summarized. Defaults to first available
            section in the database.

        slast
            Last section ID to be summarized. Defaults to last available
            section in the database.

        sinc
            Increment of the section ID; defaults to 1.

        details
            Determines the content of the summarized information for beams and
            shells.

            BRIEF - For beams, lists only the section integrated properties (such as Area, Iyy, and
                    Iyz). This option is the default.

            FULL - For beams, lists the section integrated properties, as well as the section
                   nodal coordinates, section cell connectivity information,
                   and section cell integration point coordinates. For shells,
                   the section stiffness (membrane, bending, membrane-bending
                   coupling and transverse shear) are printed.

            The shell section stiffness listed considers elastic behavior of materials at reference temperature only. The elements that use the section data may alter the transverse shear stiffness based on slenderness considerations (in addition to the shear correction factors shown).  - Section stiffness terms listed via the FULL option do not include section
                              offsets. The ANSYS program considers section
                              offsets during the solution phase of the
                              analysis.

            GROUP - If a section calls other sections, this option lists those sections too.

        type\_
            The section type. Valid arguments are ALL (the default) and the
            types available on the SECTYPE command.

        Notes
        -----
        By default, the command lists information concerning all sections;
        however, you can limit the output to only beam or pretension sections
        via the Type key. Also, by default when ocean loading is present, the
        command lists the beam section properties used by ocean loading.

        Following is example output from the SLIST,,,,BRIEF command for a
        rectangular beam section subtype (SECTYPE,,BEAM,RECT):
        """
        command = f"SLIST,{sfirst},{slast},{sinc},{details},{type_}"
        return self.run(command, **kwargs)

    def sload(
        self,
        secid="",
        plnlab="",
        kinit="",
        kfd="",
        fdvalue="",
        lsload="",
        lslock="",
        **kwargs,
    ):
        """Load a pretension section.

        APDL Command: SLOAD

        Parameters
        ----------
        secid
            Unique section number. The number must already be assigned to a
            pretension section.

        plnlab
            Label representing the pretension load sequence number in the
            format "PLnn" where nn is an integer from 1 through 99 (for
            example, PL01 through PL99).

        kinit
            Initial action key for pretension load PL01. (This field is omitted
            for PL02 and up.) Three scenarios are possible:

            LOCK - Constrains (connects) the cutting plane on the pretension section. This value
                   is the default.

            SLID - Unconstrains (disconnects) the cutting plane on the pretension section.

            TINY - Applies a very small pretension load (0.1% of FDVALUE) before the desired load
                   is established. The small load prevents convergence problems
                   which can occur when the desired load is not established in
                   the first load step. This value is valid only if KFD = FORC.

        kfd
            Force/Displacement key. Specifies whether FDVALUE is a force or a
            displacement:

            FORC - Apply a force on the specified pretension section. This value is the default.

            DISP - Apply a displacement (adjustment) on the specified pretension section.

        fdvalue
            Pretension load value. If KFD = FORC, this value is a pretension
            force. If KFD = DISP, this value is a pretension displacement
            (adjustment).

        lsload
            Load step in which to apply the FDVALUE.

        lslock
            The load step in which the displacement value resulting from the
            pretension force is locked. This value is valid only if KFD = FORC.

        Notes
        -----
        The SLOAD command applies pretension loads to specified pretension
        sections (created via the PSMESH command). A pretension load is ramp-
        applied (KBC = 0) if it is a force (KFD = FORC), and step-applied (KBC
        = 1) if it is a displacement (KFD = DISP).

        You can "lock" the load value at a specified load step. When locked,
        the load changes from a force to a displacement, and ANSYS applies the
        load as a constant displacement in all future load steps. Locking is
        useful when applying additional loadings. The additional loadings alter
        the effect of the initial load value, but because locking transforms
        the load into a displacement, it preserves the initial load's effect.

        In modal and harmonic analyses, any pretension load (force,
        displacement, or locked) is ignored and no load is produced.

        The following command shows how to establish loads on a pretension
        section:

        SLOAD,1,PL01,TINY,FORC,5000,2,3

        In this example, the load is applied to pretension section 1, and the
        sequence begins with the initial action key, KINIT, set to TINY. A
        small stabilization load (5 = 0.10% of 5000) is applied in the first
        load step, as the actual pretension force is not applied until the
        second load step. The next four fields set the actual load: the KFD
        value FORC specifies the type of load, FDVALUE defines the pretension
        load value (5000), LSLOAD specifies the load step in which the force is
        applied (2), and the LSLOCK field specifies the load step in which the
        force is locked (3). Additional sets of four fields can be used to
        define additional loads.

        You can use the SLOAD command to edit (overwrite) existing loads on a
        pretension section. This example changes the load on pretension section
        1 (set above) to 6000:

        SLOAD,1,PL01,,,6000,2,3

        Unspecified values (blank fields), as shown in this example, remain
        unchanged from prior settings. If no prior specifications exist, then
        default values (KINIT = LOCK and KFD = FORC) apply.

        The command can also delete all loads on a specified pretension
        section, as shown here:

        SLOAD,1,DELETE

        For a prestressed modal analysis, this command locks the pretension
        element:

        SLOAD,1,PL01,LOCK,DISP,0,1,2
        """
        command = f"SLOAD,{secid},{plnlab},{kinit},{kfd},{fdvalue},{lsload},{lslock}"
        return self.run(command, **kwargs)

    def ssbt(self, bt11="", bt22="", bt12="", t="", **kwargs):
        """Specifies preintegrated bending thermal effects for shell sections.

        APDL Command: SSBT

        Parameters
        ----------
        bt11, bt22, bt12
            Bending thermal effects component [BT].

        t
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The SSBT command, one of several preintegrated shell section commands,
        specifies the bending thermal effects quantity (submatrix [BT] data)
        for a preintegrated shell section. The section data defined is
        associated with the section most recently defined (via the SECTYPE
        command).

        The [BT] quantity represents bending stress resultants caused by a unit
        raise in temperature on a fully constrained model. For a layered
        composite shell, it is usually necessary to specify both the [BT] and
        [MT] quantities (by issuing the SSBT and SSMT commands, respectively).

        Unspecified values default to zero.

        Related commands are SSPA, SSPB, SSPD, SSPE, SSMT, and SSPM.

        If you are using the SHELL181 or SHELL281 element's Membrane option
        (KEYOPT(1) = 1), it is not necessary to issue this command.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSBT,{bt11},{bt22},{bt12},{t}"
        return self.run(command, **kwargs)

    def ssmt(self, mt11="", mt22="", mt12="", t="", **kwargs):
        """Specifies preintegrated membrane thermal effects for shell sections.

        APDL Command: SSMT

        Parameters
        ----------
        mt11, mt22, mt12
            Membrane thermal effects component [MT].

        t
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The SSMT command, one of several preintegrated shell section commands,
        specifies the membrane thermal effects quantity (submatrix [MT] data)
        for a preintegrated shell section. The section data defined is
        associated with the section most recently defined (via the SECTYPE
        command).

        The [MT] quantity represents membrane stress resultants caused by a
        unit raise in temperature on a fully constrained model. For a layered
        composite shell, it is usually necessary to specify both the [MT] and
        [BT] quantities (by issuing the SSMT and SSBT commands, respectively).

        Unspecified values default to zero.

        Related commands are SSPA, SSPB, SSPD, SSPE, SSBT, and SSPM.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSMT,{mt11},{mt22},{mt12},{t}"
        return self.run(command, **kwargs)

    def sspa(self, a11="", a21="", a31="", a22="", a32="", a33="", t="", **kwargs):
        """Specifies a preintegrated membrane stiffness for shell sections.

        APDL Command: SSPA

        Parameters
        ----------
        a11, a21, a31, a22, a32, a33
            Membrane stiffness component (symmetric lower part of submatrix
            [A]).

        t
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The SSPA command, one of several preintegrated shell section commands,
        specifies the membrane stiffness quantity (submatrix [A]) for a
        preintegrated shell section. The section data defined is associated
        with the section most recently defined (via the SECTYPE command).

        Unspecified values default to zero.

        Related commands are SSPB, SSPD, SSPE, SSMT, SSBT, and SSPM.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSPA,{a11},{a21},{a31},{a22},{a32},{a33},{t}"
        return self.run(command, **kwargs)

    def sspb(
        self,
        b11="",
        b21="",
        b31="",
        b22="",
        b32="",
        b33="",
        t="",
        b12="",
        b13="",
        b23="",
        **kwargs,
    ):
        """Specifies a preintegrated coupling stiffness for shell sections.

        APDL Command: SSPB

        Parameters
        ----------
        b11, b21, b31, b22, b32, b33
            Coupling stiffness component (symmetric lower part of submatrix
            [B]).

        t
            Temperature.

        b12, b13, b23
            Upper part of submatrix [B]

        Notes
        -----
        The behavior of shell elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        If the coefficients B12, B13, B23 are undefined, ANSYS uses a symmetric
        form of submatrix [B].  If any one of the coefficients B12, B13, B23 is
        nonzero, ANSYS considers submatrix [B] to be unsymmetric.

        The SSPB command, one of several preintegrated shell section commands,
        specifies the coupling stiffness quantity (submatrix [B] data) for a
        preintegrated shell section. The section data defined is associated
        with the section most recently defined (via the SECTYPE command).

        Unspecified values default to zero.

        Related commands are SSPA, SSPD, SSPE, SSMT, SSBT, and SSPM.

        If you are using the SHELL181 or SHELL281 element's Membrane option
        (KEYOPT(1) = 1), it is not necessary to issue this command.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSPB,{b11},{b21},{b31},{b22},{b32},{b33},{t},{b12},{b13},{b23}"
        return self.run(command, **kwargs)

    def sspd(self, d11="", d21="", d31="", d22="", d32="", d33="", t="", **kwargs):
        """Specifies a preintegrated bending stiffness for shell sections.

        APDL Command: SSPD

        Parameters
        ----------
        d11, d21, d31, d22, d32, d33
            Bending stiffness component (symmetric lower part of submatrix
            [D]).

        t
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The SSPD command, one of several preintegrated shell section commands,
        specifies the bending stiffness quantity (submatrix [D] data) for a
        preintegrated shell section. The section data defined is associated
        with the section most recently defined (via the SECTYPE command).

        Unspecified commands default to zero.

        Related commands are SSPA, SSPB, SSPE, SSMT, SSBT, and SSPM.

        If you are using the SHELL181 or SHELL281 element's Membrane option
        (KEYOPT(1) = 1), it is not necessary to issue this command.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSPD,{d11},{d21},{d31},{d22},{d32},{d33},{t}"
        return self.run(command, **kwargs)

    def sspe(self, e11="", e21="", e22="", t="", **kwargs):
        """Specifies a preintegrated transverse shear stiffness for shell

        APDL Command: SSPE
        sections.

        Parameters
        ----------
        e11, e21, e22
            Transverse shear stiffness component (symmetric lower part of
            submatrix [E]).

        t
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-
        stress/generalized-strain relationship of the form:

        The SSPE command, one of several preintegrated shell section commands,
        specifies the transverse shear stiffness quantity (submatrix [E] data)
        for a preintegrated shell section. The section data defined is
        associated with the section most recently defined (via the SECTYPE
        command).

        Unspecified values default to zero.

        Related commands are SSPA, SSPB, SSPD, SSMT, SSBT, and SSPM.

        If you are using the SHELL181 or SHELL281 element's Membrane option
        (KEYOPT(1) = 1), it is not necessary to issue this command.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSPE,{e11},{e21},{e22},{t}"
        return self.run(command, **kwargs)

    def sspm(self, dens="", t="", **kwargs):
        """Specifies mass density for a preintegrated shell section.

        APDL Command: SSPM

        Parameters
        ----------
        dens
            Mass density.

        t
            Temperature.

        Notes
        -----
        The SSPM command, one of several preintegrated shell section commands,
        specifies the mass density (assuming a unit thickness) for a
        preintegrated shell section. The value specified is associated with the
        section most recently defined (via the SECTYPE command).

        Related commands are SSPA, SSPB, SSPD, SSPE, SSMT, and SSBT.

        For complete information, see Using Preintegrated General Shell
        Sections.
        """
        command = f"SSPM,{dens},{t}"
        return self.run(command, **kwargs)
