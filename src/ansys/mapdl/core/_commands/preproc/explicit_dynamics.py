from typing import Optional

from ansys.mapdl.core.mapdl_types import MapdlFloat, MapdlInt


class ExplicitDynamics:
    def edasmp(
        self,
        option="",
        asmid="",
        part1="",
        part2="",
        part3="",
        part4="",
        part5="",
        part6="",
        part7="",
        part8="",
        part9="",
        part10="",
        part11="",
        part12="",
        part13="",
        part14="",
        part15="",
        part16="",
        **kwargs,
    ):
        """Creates a part assembly to be used in an explicit dynamic analysis.

        APDL Command: EDASMP

        Parameters
        ----------
        option
            Label identifying the part assembly option to be performed.

            ADD - Adds a part assembly (default).

            DELETE - Deletes a part assembly.

            LIST - Lists each part assembly number, and the part numbers that make up each part
                   assembly.

        asmid
            User defined part assembly ID number. The part assembly number
            cannot be the same as any currently defined part ID number.

        part1, part2, part3, . . . , part16
            Part numbers to be included in the assembly (up to 16 different
            parts).

        Notes
        -----
        Several ANSYS LS-DYNA commands (such as EDCGEN, EDPVEL, and EDIS) refer
        to assembly ID numbers. If you intend to use assembly ID numbers with
        these commands, you must first define the assembly ID numbers using
        EDASMP.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDASMP,{option},{asmid},{part1},{part2},{part3},{part4},{part5},{part6},{part7},{part8},{part9},{part10},{part11},{part12},{part13},{part14},{part15},{part16}"
        return self.run(command, **kwargs)

    def edbound(
        self,
        option="",
        lab="",
        cname="",
        xc="",
        yc="",
        zc="",
        cname2="",
        copt="",
        **kwargs,
    ):
        """Defines a boundary plane for sliding or cyclic symmetry.

        APDL Command: EDBOUND

        Parameters
        ----------
        option
            Label identifying the symmetry plane option to be performed.

            ADD - Define a sliding or cyclic symmetry plane.

            DELE - Delete a specified sliding or cyclic symmetry plane.

            LIST - List defined sliding or cyclic symmetry planes.

        lab
            Valid boundary options for defining a symmetry plane. A valid label
            must always be specified for adding, deleting, or listing boundary
            planes.

            SLIDE - Sliding symmetry plane.

            CYCL - Cyclic symmetry plane.

        cname
            Name of existing component [CM] to which boundary symmetry is to be
            applied or deleted. Component must consist of nodes. For Option =
            LIST, a component is not required because all defined symmetry
            planes are listed for the specified Lab.  For Option = DELE, use
            Cname = ALL to delete all symmetry planes currently defined for the
            specified Lab.

        xc, yc, zc
            X, Y, and Z coordinates of the head of the vector defining normal
            (Lab = SLIDE) or axis of rotation (Lab = CYCL). The tail of the
            vector is at the global origin.

        cname2
            Name of existing nodal component [CM] for which second cyclic
            boundary plane is to be applied. Each node in Cname2 component is
            constrained to a corresponding node in the first component set.
            Therefore, component Cname2 must have the same number of nodes as
            the Cname component. Cname2 is valid only for Lab = CYCL.

        copt
            Specified constraint option for sliding plane symmetry. COPT is
            valid only for Lab = SLIDE. Valid COPT options are:

            0 - Nodes move on normal plane (default).

            1 - Nodes move only in vector direction.

        Notes
        -----
        For cyclic symmetry, the node numbers in component Cname2 must differ
        from the node numbers in Cname by a constant offset value. In addition,
        the nodes in Cname2 must have locations which, if given in cylindrical
        coordinates, all differ by the same angle from the nodes in Cname. The
        following figure shows how you would define components for a cyclic
        symmetry plane.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDBOUND,{option},{lab},{cname},{xc},{yc},{zc},{cname2},{copt}"
        return self.run(command, **kwargs)

    def edbx(
        self,
        option="",
        boxid="",
        xmin="",
        xmax="",
        ymin="",
        ymax="",
        zmin="",
        zmax="",
        **kwargs,
    ):
        """Creates a box shaped volume to be used in a contact definition for

        APDL Command: EDBX
        explicit dynamics.

        Parameters
        ----------
        option
            Label identifying the contact box definition option to be
            performed.

            ADD - Adds a contact box definition (default).

            DELETE - Deletes a contact box definition.

            LIST - Lists each box ID number, and the coordinates that make up each box shaped
                   volume.

        boxid
            User defined list ID number.

        xmin
            Minimum x-coordinate.

        xmax
            Maximum x-coordinate.

        ymin
            Minimum y-coordinate.

        ymax
            Maximum y-coordinate.

        zmin
            Minimum z-coordinate.

        zmax
            Maximum z-coordinate.

        Notes
        -----
        The ANSYS LS-DYNA command EDCGEN allows you to define contact and
        target volumes using box ID numbers BOXID1 and BOXID2, respectively. If
        you use these arguments to define contact volumes, you must first
        define their coordinates using the EDBX command.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDBX,{option},{boxid},{xmin},{xmax},{ymin},{ymax},{zmin},{zmax}"
        return self.run(command, **kwargs)

    def edcgen(
        self,
        option="",
        cont="",
        targ="",
        fs="",
        fd="",
        dc="",
        vc="",
        vdc="",
        v1="",
        v2="",
        v3="",
        v4="",
        btime="",
        dtime="",
        boxid1="",
        boxid2="",
        **kwargs,
    ):
        """Specifies contact parameters for an explicit dynamics analysis.

        APDL Command: EDCGEN

        Parameters
        ----------
        option
            Label identifying the contact behavior (dictates the meaning of V1
            through V4).

            AG - Automatic general contact.

            ANTS - Automatic nodes-to-surface contact.

            ASSC - Automatic single surface contact.

            ASS2D - Automatic 2-D single surface contact.

            ASTS - Automatic surface-to-surface contact.

            DRAWBEAD - Drawbead contact

            ENTS - Eroding nodes-to-surface contact.

            ESS - Eroding single surface contact.

            ESTS - Eroding surface-to-surface contact.

            FNTS - Forming nodes-to-surface contact.

            FOSS - Forming one way surface-to-surface contact.

            FSTS - Forming surface-to-surface contact.

            NTS - Nodes-to-surface contact.

            OSTS - One way surface-to-surface contact.

            RNTR - Rigid nodes to rigid body contact.

            ROTR - Rigid body to rigid body (one way) contact.

            SE - Single edge contact.

            SS - Single surface contact.

            STS - Surface-to-surface contact.

            TDNS - Tied nodes-to-surface contact.

            TSES - Tied shell edge-to-surface contact.

            TDSS - Tied surface-to-surface contact.

            TNTS - Tiebreak nodes-to-surface contact

            TSTS - Tiebreak surface-to-surface contact.

        cont
            Contact surface identified by a component name [CM] , a part ID
            number [EDPART], or an assembly ID number [EDASMP]. If a component
            name is input, the component must contain nodes that represent the
            contact surface (assemblies are not valid for a component name).
            Alternatively, a part number may be input that identifies a group
            of elements as the contact surface, or an assembly number may be
            input containing a maximum of 16 parts. The assembly ID number must
            be greater than the highest number used for the part ID. Cont is
            not required for automatic general contact, single edge contact,
            and single surface contact options (Option = AG, SE, ASSC, ESS, and
            SS). For automatic 2-D single surface contact (ASS2D), Cont must be
            defined as a part assembly. For eroding node-to-surface contact
            (ENTS), Cont must be defined as a nodal component. For eroding
            single surface contact (ESS) and eroding surface-to-surface contact
            (ESTS), Cont must be defined as a part ID or part assembly.

        targ
            Target surface identified by a component name [CM] , a part ID
            number [EDPART], or an assembly ID number [EDASMP]. If a component
            name is input, the component must contain nodes that represent the
            target surface (assemblies are not valid for a component name).
            Alternatively, a part number may be input that identifies a group
            of elements as the target surface, or an assembly number may be
            input containing a maximum of 16 parts. The assembly ID number must
            be greater than the highest number used for the part ID. Targ is
            not defined for automatic general contact, single edge contact,
            automatic single surface contact, eroding single surface contact,
            single surface contact, and automatic 2-D single surface contact
            options (Option = AG, SE, ASSC, ESS, SS, and ASS2D). For eroding
            node-to-surface contact (ENTS) and eroding surface-to-surface
            contact (ESTS), Targ must be defined as a part ID or part assembly.

        fs
            Static friction coefficient (defaults to 0).

        fd
            Dynamic friction coefficient (defaults to 0).

        dc
            Exponential decay coefficient (defaults to 0).

        vc
            Coefficient for viscous friction (defaults to 0).

        vdc
            Viscous damping coefficient in percent of critical damping
            (defaults to 0).

        v1, v2, v3, v4
            Additional input for drawbead, eroding, rigid, and tiebreak
            contact.  The meanings of V1-V4 will vary, depending on Option. See
            the table below for V1-V4 definitions.

            V1 - Load curve ID giving the bending component of the restraining force per unit
                 draw bead length as a function of draw bead displacement. V1
                 must be specified.

            V2 - Load curve ID giving the normal force per unit draw bead length as a function
                 of draw bead displacement. V2 is optional.

            V3 - Draw bead depth.

            V4 - Number of equally spaced integration points along the draw bead (default = 0,
                 in which case ANSYS LS-DYNA calculates this value based on the
                 size of the elements that interact with the draw bead).
        """
        command = f"EDCGEN,{option},{cont},{targ},{fs},{fd},{dc},{vc},{vdc},{v1},{v2},{v3},{v4},{btime},{dtime},{boxid1},{boxid2}"
        return self.run(command, **kwargs)

    def edclist(self, num="", **kwargs):
        """Lists contact entity specifications in an explicit dynamics analysis.

        APDL Command: EDCLIST

        Parameters
        ----------
        num
            Number identifying contact entity to be listed. Use NUM = ALL to
            list all contact entities (ALL is the default).

        Notes
        -----
        Lists contact entity specifications previously defined with the EDCGEN
        command. The listing will include any contact parameters defined using
        the EDCMORE command.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCLIST,{num}"
        return self.run(command, **kwargs)

    def edcmore(self, option="", num="", val1="", val2="", **kwargs):
        """Specifies additional contact parameters for a given contact definition

        APDL Command: EDCMORE
        in an explicit dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            ADD - Define contact parameters for the contact entity
            specified by NUM (default).

            DELE - Delete contact parameters (VAL1 and VAL2) for the
                   contact entity specified by NUM. If NUM = ALL, all
                   contact parameters previously defined by EDCMORE
                   are deleted.

        num
            Contact entity number. This contact entity must have been
            previously defined with the EDCGEN command. Use EDCLIST to
            obtain a list of contact entity numbers.

        val1
            Penalty scale factor for slave (contact) surface (SFS);
            default = 1.

        val2
            Penalty scale factor for master (target) surface (SFM);
            default = 1.

        Notes
        -----
        You can use the EDCMORE command to specify two additional
        contact parameters (SFS and SFM) for a specific contact
        definition. These parameters will apply only to the contact
        entity number entered on the NUM field. Use the EDCLIST
        command to obtain a list of contact definitions and their
        corresponding contact entity numbers. The listing produced by
        EDCLIST will include any contact parameters specified with the
        EDCMORE command.

        When you use the EDDC command to delete a contact definition,
        any parameters you specified with EDCMORE for that contact
        definition will also be deleted. To delete only the parameters
        specified by EDCMORE for a given contact definition, use the
        command EDCMORE,DELE,NUM.

        Note: When you delete a contact definition with the EDDC
        command, the contact entity numbers will be renumbered for the
        remaining contact definitions. Therefore, you should always
        issue EDCLIST to obtain a current list of contact entity
        numbers before adding or deleting contact parameters with the
        EDCMORE command.

        The EDCMORE command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported
        in Distributed ANSYS.
        """
        return self.run(f"EDCMORE,{option},{num},,{val1},{val2}", **kwargs)

    def edcnstr(self, option="", ctype="", comp1="", comp2="", val1="", **kwargs):
        """Defines various types of constraints for an explicit dynamic analysis.

        APDL Command: EDCNSTR

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            ADD - Define a constraint (default).

            DELE - Delete the constraint specified by Ctype, Comp1, and Comp2. If Ctype = ALL, all
                   constraints are deleted.

            LIST - List all of the constraints previously defined by the EDCNSTR command.

        ctype
            Constraint type. The command format will vary, depending on the
            Ctype value.

            ENS - Extra node set added to an existing rigid body.

            NRB - Nodal rigid body.

            STS - Tie between a shell edge and solid elements.

            RIVET - Massless rivet between two noncoincident nodes.

        Notes
        -----
        The EDCNSTR command allows you to define several types of constraints
        in an explicit dynamic analysis. A brief description of each constraint
        type is given below. See Constraints and Initial Conditions in the
        ANSYS LS-DYNA User's Guide for more information.

        Extra Node Set Added to a Rigid Body (Ctype = ENS)

        The ability to add extra nodes to an existing rigid body has many
        potential applications, including placing nodes where joints will be
        attached between rigid bodies, defining nodes where point loads will be
        applied, and defining a lumped mass at a specific location. The extra
        nodes specified by Comp2 may be located anywhere in the model and may
        have coordinates outside those of the original rigid body specified by
        Comp1.

        Nodal Rigid Body (Ctype = NRB)

        Unlike typical rigid bodies that are defined with the EDMP command,
        nodal rigid bodies defined with the EDCNSTR command are not associated
        with a part number. This can be advantageous for modeling rigid
        (welded) joints in a model. For a rigid joint, portions of different
        flexible components (having different MAT IDs) act together as a rigid
        body. It is difficult to define this type of rigid body with a unique
        MAT ID (and corresponding part number). However, the rigid joint can be
        easily defined using a nodal rigid body.

        Shell Edge to Solid Tie (Ctype = STS)

        The STS option ties regions of solid elements to regions of shell
        elements. A single shell node may be tied to up to nine brick element
        nodes that define a "fiber" vector. Solid element nodes constrained in
        this way remain linear throughout the analysis but can move relative to
        each other in the fiber direction.

        Rivet between Two Nodes (Ctype = RIVET)

        The RIVET option defines a massless rigid constraint between two nodes,
        similar to spotwelds defined with the EDWELD command. Unlike a
        spotweld, however, rivets contain nodes that are noncoincident, and
        failure cannot be specified. When a rivet is defined, the distance
        between the nodes is kept constant throughout any motion that occurs
        during a simulation. Nodes connected by a rivet cannot be part of any
        other constraints specified in the model.

        The EDCNSTR command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCNSTR,{option},{ctype},{comp1},{comp2},{val1}"
        return self.run(command, **kwargs)

    def edcontact(
        self,
        sfsi="",
        rwpn="",
        ipck="",
        shtk="",
        peno="",
        stcc="",
        orie="",
        cspc="",
        penchk="",
        **kwargs,
    ):
        """Specifies contact surface controls for an explicit dynamics analysis.

        APDL Command: EDCONTACT

        Parameters
        ----------
        sfsi
            Scale factor for sliding interface penalties. Defaults to 0.1.

        rwpn
            Scale factor for rigid wall penalties (defaults to 0). If RWPN = 0,
            rigid bodies interacting with rigid walls are not considered. If
            RWPN>0, rigid bodies interact with fixed rigid walls. A value of
            1.0 should be optimal; however, this may be problem dependent.

        ipck
            Initial contact surface penetration checking option:

            1 - No checking.

            2 - Full check of initial penetration is performed (default).

        shtk
            Shell thickness contact option for surface-to-surface and nodes-to-
            surface contact (see Notes below):

            0 - Thickness is not considered (default).

            1 - Thickness is considered, except in rigid bodies.

            2 - Thickness is considered, including rigid bodies.

        peno
            Penalty stiffness option (options 4 and 5 are useful for metal
            forming calculations):

            1 - Minimum of master segment and slave node (default).

            2 - Use master segment stiffness.

            3 - Use slave node value.

            4 - Use area or mass weighted slave node value.

            5 - Use slave node value inversely proportional to shell thickness. (This may
                require special scaling and is not generally recommended.)

        stcc
            Shell thickness change option for single surface contact:

            1 - Shell thickness changes are not considered (default).

            2 - Shell thickness changes are included.

        orie
            Option for automatic reorientation of contact surface segments
            during initialization:

            1 - Activate for automated (part ID) input only (default).

            2 - Activate for manual (nodal component) and automated (part ID) input.

            3 - Do not activate.

        cspc
            Contact surface penetration check multiplier, used if small
            penetration checking is on (PENCHK = 1 or 2). Defaults to 4.

        penchk
            Small penetration check, used only for contact types STS, NTS,
            OSTS, TNTS, and TSTS. If the contact surface node penetrates more
            than the target thickness times CSPC, the penetration is ignored
            and the contacting node is set free. The target thickness is the
            element thickness for shell elements, or 1/20 of the shortest
            diagonal for solid elements.

            0 - Penetration checking is off (default).

            1 - Penetration checking is on.

            2 - Penetration checking is on, but shortest diagonal is used.

        Notes
        -----
        The thickness offsets are always included in single surface, automatic
        surface-to-surface, and automatic nodes-to-surface contact. The shell
        thickness change option must be used [EDSHELL,,,1] and a nonzero value
        must be specified for SHTK before the shell thickness changes can be
        included in the surface-to-surface contact type. Additionally, STCC
        must be set to 2 if thickness changes are to be included in the single
        surface contact algorithms.

        To reset the contact options to default values, issue the EDCONTACT
        command with no fields specified.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCONTACT,{sfsi},{rwpn},{ipck},{shtk},{peno},{stcc},{orie},{cspc},{penchk}"
        return self.run(command, **kwargs)

    def edcrb(self, option="", neqn="", partm="", parts="", **kwargs):
        """Constrains two rigid bodies to act as one in an explicit dynamics

        APDL Command: EDCRB
        analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed:

            ADD - Define an equation to constrain two rigid bodies (default).

            DELE - Delete the equation (specified by NEQN) that constrains two rigid bodies. If
                   NEQN is blank, all equations constraining rigid bodies are
                   deleted.

            LIST - List constrained rigid bodies specified by NEQN. If NEQN is blank, all
                   constrained rigid bodies are listed.

        neqn
            Equation reference number. Defaults to PARTS.  NEQN should be a
            unique number for each pair of PARTM and PARTS. If it is not
            unique, the equation reference number defined last will overwrite
            any previously defined NEQN with the same number.

        partm
            PART number [EDPART] identifying the master rigid body. This value
            is ignored if the DELE or LIST labels are specified. No default;
            you must enter a value.

        parts
            PART number [EDPART] identifying the slave rigid body. This value
            is ignored if the DELE or LIST labels are specified. No default;
            you must enter a value.

        Notes
        -----
        EDCRB is valid only for materials defined as rigid bodies with the
        EDMP,RIGID command. EDCRB automatically generates a constraint equation
        to force the specified rigid bodies to behave as a single rigid body.
        The slave rigid body takes on the material properties and loading of
        the master rigid body. Any loads [EDLOAD] existing on the slave rigid
        body are ignored.

        To create a single large rigid body from several smaller bodies, use a
        series of EDCRB commands. With the first command, specify a master and
        slave to create the first combined rigid body. Then, using that body as
        the master, specify another slave to create a larger rigid body.
        Continue the process, using the expanding rigid body as the master and
        adding slave bodies until you have defined the desired large rigid
        body. All slave rigid bodies will take on the material properties and
        loading of the original master rigid body. Note that you will need to
        use different NEQN values for each pair of PARTM and PARTS.  This
        command will be ignored if you specify the previously-defined master
        rigid body as a slave rigid body in the same analysis. To change the
        master and slave definitions, first use the DELE option to delete all
        master and slave definitions, and then use the ADD option to redefine
        them.

        The equation number, NEQN, is a reference number by which the
        constrained bodies can be identified for listing and deleting purposes
        on the EDCRB command. For any other reference to the constrained bodies
        (loading, contact definitions, etc.), use the master body part number
        (PARTM).

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCRB,{option},{neqn},{partm},{parts}"
        return self.run(command, **kwargs)

    def edcurve(self, option="", lcid="", par1="", par2="", **kwargs):
        """Specifies data curves for an explicit dynamic analysis.

        APDL Command: EDCURVE

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            ADD - Define a data curve (default). If Option = ADD, Par1 and Par2 must be
                  previously defined array parameters.

            DELE - Delete the specified data curve (LCID). If LCID is blank, all data curves are
                   deleted. Par1 and Par2 are ignored for this option.

            LIST - List defined data curve (LCID). If LCID is blank, all data curves are listed.
                   Par1 and Par2 are ignored for this option.

            PLOT - Plot defined data curve (LCID). If Option = PLOT, LCID must be previously
                   defined with an EDCURVE command. Otherwise a warning message
                   will report that LCID has not been defined. Par1 and Par2
                   are ignored for this option.

        lcid
            Data curve ID number (no default). Must be a positive integer.

        par1
            Name of user-defined array parameter that contains the abscissa
            values of the curve data (e.g., time, effective plastic strain,
            effective strain rate, displacement, etc.).

        par2
            Name of user-defined array parameter that contains the ordinate
            values of the curve data (e.g., damping coefficients, initial yield
            stress, elastic modulus, force, etc.) corresponding to the abscissa
            values in Par1.

        Notes
        -----
        EDCURVE can be used to define material data curves (e.g., stress-
        strain) and load data curves (force-deflection) associated with
        material models in an explicit dynamics analysis. Material data
        specified by this command is typically required to define a particular
        material behavior (e.g., TB,HONEY), and the LCID number is used as
        input on the TBDATA command.

        EDCURVE can also be used to define load curves that represent time
        dependent loads (force, displacement, velocity, etc.). Par1 must
        contain the time values, and Par2 must contain the corresponding load
        values. The LCID number assigned to the load curve can be used as input
        on the EDLOAD command.

        Note:: : You cannot update a previously defined data curve by changing
        the array parameters that were input as Par1 and Par2. The data curve
        definition is written to the database at the time EDCURVE is issued.
        Therefore, subsequent changes to the array parameters that were used as
        input on EDCURVE will not affect the load curve definition. If you need
        to change the load curve definition, you must delete the load curve
        (EDCURVE,DELE,LCID) and define it again.

        LCID identifies the data curve. If the value input for LCID is the same
        as the ID number for a data curve previously defined by EDCURVE, the
        previous data will be overwritten. Use EDCURVE,LIST and EDCURVE,PLOT to
        check existing data curves.

        A starting array element number must be specified for Par1 and Par2.
        The input for these fields must be a single column array parameter, or
        a specific column from a multi-column array parameter. When using the
        GUI with multi-column parameters, you must specify the parameter name
        and starting position for Par1 and Par2 by typing the EDCURVE command
        in the Input Window. This is because only the parameter name is
        available through the dialog box, which pulls in the first position of
        a single-column array parameter.

        If you need to change a curve definition in an explicit dynamic small
        restart analysis, issue EDSTART,2 first (to specify the restart), then
        issue the EDCURVE command. The revised curve must contain the same
        number of points as the curve it replaces. This limitation does not
        apply to a full restart analysis (EDSTART,3).

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCURVE,{option},{lcid},{par1},{par2}"
        return self.run(command, **kwargs)

    def eddbl(self, key="", **kwargs):
        """Selects a numerical precision type of the explicit dynamics analysis.

        APDL Command: EDDBL

        Parameters
        ----------
        key
            Number or name identifying numerical precision to be used.

            0 or SINGLE - Select single precision version of LS-DYNA (default).

            1 or DOUBLE - Select double precision version of LS-DYNA.

            STAT - Check the status of the numerical precision in effect.

        Notes
        -----
        Sets the single or double precision version of LS-DYNA into effect.
        Please check the availability of the double precision version of LS-
        DYNA on your system before using the command. If it is not available,
        use the command default.

        The double precision version may be up to 20% slower than the single
        precision version. The results may also vary based on problem
        specifications.

        In addition to EDDBL,STAT, you can use the GUI dialog box to verify
        which precision version is currently chosen. The GUI is based on the
        database and is updated to reflect changes.

        See Double Precision LS-DYNA for more information.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDDBL,{key}"
        return self.run(command, **kwargs)

    def eddc(self, option="", ctype="", cont="", targ="", **kwargs):
        """Deletes or deactivates/reactivates contact surface specifications in an

        APDL Command: EDDC
        explicit dynamic analysis.

        Parameters
        ----------
        option
            Option to be performed for contact definition specified by Ctype,
            Cont, and Targ.

            DELE - Delete the specified contact definition (default); valid only in a new
                   analysis.

            DACT - Deactivate the specified contact definition; valid only in a small restart.

            RACT - Reactivate the specified contact definition (which was previously deactivated);
                   valid only in a small restart.

        ctype
            Contact behavior label (see EDCGEN command for valid labels).

        cont
            Component name or part number [EDPART] identifying the contact
            surface.

        targ
            Component name or part number [EDPART] identifying the target
            surface.

        Notes
        -----
        This command allows you to delete or deactivate/reactivate a particular
        contact specification that was defined by EDCGEN. The contact
        definition is identified by Ctype, Cont, and Targ (Note that Cont and
        Targ may not be required for Ctype = AG, SE, ASSC, ESS, and SS). The
        delete option (Option = DELE) permanently deletes the contact from the
        database. Any additional contact parameters defined with the EDCMORE
        command for the contact definition identified on this command will also
        be deleted or deactivated/reactivated.

        You cannot delete contact specifications in an explicit dynamic small
        restart (EDSTART,2). However, you can use Option = DACT to deactivate a
        contact definition that is not needed in the small restart. That
        contact definition may then be reactivated in a subsequent small
        restart by using Option = RACT.

        To delete or deactivate/reactivate all contact specifications for the
        entire model, use EDDC,Option,ALL.

        The EDDC command is not supported in an explicit dynamic full restart
        analysis (EDSTART,3). Thus, you cannot delete, deactivate, or
        reactivate contact specifications in a full restart that were defined
        in the previous analysis.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDDC,{option},{ctype},{cont},{targ}"
        return self.run(command, **kwargs)

    def edipart(
        self,
        part="",
        option="",
        cvect="",
        tm="",
        ircs="",
        ivect="",
        vvect="",
        cid="",
        **kwargs,
    ):
        """Defines inertia for rigid parts in an explicit dynamics analysis.

        APDL Command: EDIPART

        Parameters
        ----------
        part
            Part number for which the inertia is defined (the part number must
            have been previously generated using the EDPART command).  The part
            should be composed of a rigid material (EDMP,RIGID). For Option =
            ADD, you must input a value; there is no default. For Option = DELE
            or LIST, PART defaults to all parts.

        option


            ADD - Define inertia for the specified PART (default).

            DELE - Delete the inertia properties for the specified PART. The remaining fields are
                   ignored. If PART is blank, inertia properties previously
                   specified using EDIPART are deleted for all rigid parts.

            LIST - List the inertia properties for the specified PART. The remaining fields are
                   ignored. If PART is blank, inertia properties are listed for
                   all rigid parts.

        cvect
            The vector containing the global Cartesian coordinates of the
            center of mass for the part. This vector must have been previously
            defined with a dimension of three (``*DIM`` command) and filled in as
            shown below. If Cvect is blank, the global Cartesian origin (0,0,0)
            is used as the center of mass.

        tm
            Translation mass (no default, must be defined).

        ircs
            Flag for inertia tensor reference coordinate system.

            0 (or blank) - Global inertia tensor (default). You must supply all six inertia tensor
                           components (see Ivect).

            1 - Principal moments of inertia with orientation vectors. You must supply IXX,
                IYY, IZZ (see Ivect) and CID.

        ivect
            The name of a vector containing the components of the inertia
            tensor. This vector must have been previously defined (``*DIM``
            command) with a dimension of six and filled in as shown below.
            Vector entries 2, 3, and 5 are ignored if IRCS = 1. There is no
            default for this vector; it must be specified.

        vvect
            The name of a vector containing the initial velocity (relative to
            the global Cartesian coordinate system) of the rigid part. This
            vector must have been previously defined (``*DIM`` command) with a
            dimension of six and filled in as shown below. If Vvect is blank,
            the initial velocity defaults to zero.

        cid
            Local coordinate system ID. This coordinate system must have been
            previously defined with the EDLCS command. You must input CID if
            IRCS = 1 (no default).

        Notes
        -----
        The EDIPART command applies only to rigid parts (EDMP,RIGID). It allows
        you to input the inertia properties for the rigid part rather than
        having the program calculate the properties from the finite element
        mesh.

        This command is also valid in Solution.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDIPART,{part},{option},{cvect},{tm},{ircs},{ivect},{vvect},{cid}"
        return self.run(command, **kwargs)

    def edlcs(
        self,
        option="",
        cid="",
        x1="",
        y1="",
        z1="",
        x2="",
        y2="",
        z2="",
        x3="",
        y3="",
        z3="",
        **kwargs,
    ):
        """Defines a local coordinate system for use in explicit dynamics

        APDL Command: EDLCS
        analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed:

            ADD - Define a coordinate system (default).

            DELE - Delete a coordinate system. If CID is blank, all coordinate systems are
                   deleted.

            LIST - List defined coordinate systems. If CID is blank, all coordinate systems are
                   listed.

        cid
            Coordinate system ID.

        x1, y1, z1
            X, Y, and Z coordinates of a point on the local x-axis.

        x2, y2, z2
            X, Y, and Z coordinates of a point on the local x-y plane.

        x3, y3, z3
            X, Y, and Z coordinates of the origin. X3, Y3, and Z3 all default
            to zero.

        Notes
        -----
        Local coordinate systems defined by this command are used in an
        explicit dynamic analysis. For example, a local coordinate system may
        be used when defining orthotropic material properties (see EDMP).

        The coordinate system is defined by 2 vectors, one from the origin (X3,
        Y3, Z3) to a point on the x-axis (X1, Y1, Z1), and one from the origin
        to a point on the x-y plane (X2, Y2, Z2).  The cross product of these
        two vectors determines the z-axis, and the cross product of the z-axis
        vector and x-axis vector determines the y-axis. If X3, Y3, and Z3 are
        not specified, the global origin (0,0,0) is used by default (as shown
        in the figure below).

        The x-axis vector and the xy vector should be separated by a reasonable
        angle to avoid numerical inaccuracies.

        When you use the local coordinate system (defined by the EDLCS command)
        to define a load (EDLOAD command), the direction of the load will
        depend on the load type. For force and moment loads (Lab = FX, MX, etc.
        on EDLOAD), the load will be applied in the direction of the local
        coordinate system defined by EDLCS. For prescribed motion degrees of
        freedom (Lab = UX, ROTX, VX, AX, etc. on EDLOAD), the motion will act
        in the direction of a vector from point (X1, Y1, Z1) to point (X2, Y2,
        Z2) as input on EDLCS. See the EDLOAD command for more information.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDLCS,{option},{cid},{x1},{y1},{z1},{x2},{y2},{z2},{x3},{y3},{z3}"
        return self.run(command, **kwargs)

    def edmp(
        self,
        lab="",
        mat="",
        val1="",
        val2="",
        val3="",
        val4="",
        val5="",
        val6="",
        **kwargs,
    ):
        """Defines material properties for an explicit dynamics analysis.

        APDL Command: EDMP

        Parameters
        ----------
        lab
            Valid material property label. Applicable labels are listed under
            "Material Properties" in the input table for each explicit dynamics
            element type in the Element Reference.

            HGLS - Hourglass and bulk viscosity properties (valid for PLANE162, SHELL163, SOLID164
                   using reduced integration, and SOLID168).  VAL1 through VAL6
                   are also used. For those elements using full integration,
                   HGLS is not applicable and the input has no effect.

            RIGID - Rigid body constraint (valid for LINK160, BEAM161, PLANE162, SHELL163,
                    SOLID164, and SOLID168). VAL1 and VAL2 are also used.

            CABLE - Cable properties (valid for LINK167).  VAL1 is optional input (see Notes).

            ORTHO - Defines a material coordinate system for the orthotropic material model (valid
                    for PLANE162, SHELL163, SOLID164, and SOLID168) or the
                    anisotropic material model (valid for SOLID164 and
                    SOLID168).  VAL1 is also used.

            FLUID - Fluid properties (valid for PLANE162, SOLID164, and SOLID168). VAL1 is optional
                    input (see Notes).

        mat
            Material reference number (defaults to the current MAT setting on
            MAT command).

        val1, val2, val3, . . . , val6
            Additional input for specified Lab material property. The meaning
            of VAL1 through VAL6 will vary, depending on Lab. See the table
            below for VAL1 through VAL6 definitions.

            VAL1 - Hourglass control type. For solid elements (PLANE162, SOLID164, and SOLID168),
                   5 options are available. For quadrilateral shell and
                   membrane elements (SHELL163) with reduced integration, the
                   hourglass control is based on the formulation of Belytschko
                   and Tsay; i.e., options 1-3 are identical and options 4-5
                   are identical.

            0, 1 - Standard LS-DYNA viscous form (default).

            2 - Flanagan-Belytschko viscous form.

            3 - Flanagan-Belytschko viscous form with exact volume integration for solid
                elements.

            4 - Flanagan-Belytschko stiffness form.

            5 - Flanagan-Belytschko stiffness form with exact volume integration for solid
                elements.

            VAL2 - Hourglass coefficient. (Defaults to 0.1.) Values greater than 0.15 may cause
                   instabilities. The recommended default applies to all
                   options.  The stiffness forms can stiffen the response
                   (especially if deformations are large) and, therefore,
                   should be used with care. For the shell and membrane
                   elements, the value input for VAL1 is the membrane hourglass
                   coefficient. VAL5 and VAL6 can also be input, but generally
                   VAL2 = VAL5 = VAL6 is adequate.

            VAL3 - Quadratic bulk viscosity coefficient. (Defaults to 1.5.)

            VAL4 - Linear bulk viscosity coefficient. (Defaults to 0.06.)

            VAL5 - Hourglass coefficient for shell bending. (Defaults to VAL2.)

            VAL6 - Hourglass coefficient for shell warping. (Defaults to VAL2.)
        """
        command = f"EDMP,{lab},{mat},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def ednb(self, option="", cname="", ad="", as_="", **kwargs):
        """Defines a nonreflecting boundary in an explicit dynamic analysis.

        APDL Command: EDNB

        Parameters
        ----------
        option
            Label identifying the nonreflecting boundary option to be
            performed.

            ADD - Define a nonreflecting boundary (default).

            DELE - Delete a nonreflecting boundary.

            LIST - List all defined nonreflecting boundaries (remaining fields are ignored).

        cname
            Name of existing nodal component to which the nonreflecting
            boundary is to be added or deleted. For Option = DELE, use Cname =
            ALL to delete all defined nonreflecting boundaries.

        ad
            Activation flag for dilatational waves (dampers normal to waves).

            0 - Dilatational activation flag is off (default).

            1 - Dilatational activation flag is on.

        as_
            Activation flag for shear waves (dampers tangent to waves).

            0 - Shear activation flag is off (default).

            1 - Shear activation flag is on.

        Notes
        -----
        Nonreflecting boundaries can be defined on the external surfaces of
        SOLID164 and SOLID168 elements that are being used to model an infinite
        domain. They are typically used in geomechanical applications to limit
        the size of the model. For example, when a half space is being modeled
        with a finite geometry, the nonreflecting boundary option can be used
        to prevent artificial stress wave reflections generated at the boundary
        from reentering the model and contaminating the results.

        When using nonreflecting boundaries, you should not constrain the nodes
        at the boundary; doing so would negate the presence of the dampers.
        Usually, the large mass of the finite domain is sufficient to resist
        motion.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDNB,{option},{cname},{ad},{as_}"
        return self.run(command, **kwargs)

    def edndtsd(
        self,
        vect1="",
        vect2="",
        datap="",
        fitpt="",
        vect3="",
        vect4="",
        disp="",
        **kwargs,
    ):
        """Allows smoothing of noisy data for explicit dynamics analyses and

        APDL Command: EDNDTSD
        provides a graphical representation of the data.

        Parameters
        ----------
        vect1
            Name of the first vector that contains the noisy data set (i.e.,
            independent variable). You must create and fill this vector before
            issuing EDNDTSD.

        vect2
            Name of the second vector that contains the dependent set of data.
            Must be the same length as the first vector. You must create and
            fill this vector before issuing EDNDTSD.

        datap
            Number of data points to be fitted, starting from the beginning of
            the vector. If left blank, the entire vector will be fitted. The
            maximum number of data points is 100,000 (or greater, depending on
            the memory of the computer).

        fitpt
            Curve fitting order to be used as a smooth representation of the
            data. This number should be less than or equal to the number of
            data points. However, because high order polynomial curve fitting
            can cause numerical difficulties, a polynomial order less than 7 is
            suggested. The default (blank) is one-half the number of data
            points or 7, which ever is less. The following values are
            available:

            1 - Curve is the absolute average of all of the data points.

            2 - Curve is the least square average of all of the data points.

            3 or more - Curve is a polynomial of the order (n-1), where n is the number of data fitting
                        order points.

        vect3
            Name of the vector that contains the smoothed data of the
            independent variable. This vector should have a length equal to or
            greater than the number of smoothed data points. In batch (command)
            mode, you must create this vector before issuing the EDNDTSD
            command. In interactive mode, the GUI automatically creates this
            vector (if it does not exist). If you do not specify a vector name,
            the GUI will name the vector smth_ind.

        vect4
            Name of the vector that contains the smoothed data of the dependent
            variable.  This vector must be the same length as Vect3.  In batch
            (command) mode, you must create this vector before issuing the
            EDNDTSD command. In interactive mode, the GUI automatically creates
            this vector (if it does not exist). If you do not specify a vector
            name, the GUI will name the vector smth_dep.

        disp
            Specifies how you want to display data. No default; you must
            specify an option.

            1 - Unsmoothed data only

            2 - Smoothed data only

            3 - Both smoothed and unsmoothed data

        Notes
        -----
        You can control the attributes of the graph using standard ANSYS
        controls (/GRID, /GTHK, /COLOR, etc.). If working interactively, these
        controls appear in this dialog box for convenience, as well as in their
        standard dialog boxes. You must always create Vect1 and Vect2 (using
        ``*DIM``) and fill these vectors before smoothing the data. If you're
        working interactively, ANSYS automatically creates Vect3 and Vect4, but
        if you're working in batch (command) mode, you must create Vect3 and
        Vect4 (using ``*DIM``) before issuing EDNDTSD.  Vect3 and Vect4 are then
        filled automatically by ANSYS.  In addition, ANSYS creates an
        additional TABLE type array that contains the smoothed array and the
        unsmoothed data to allow for plotting later with ``*VPLOT``.  Column 1 in
        this table corresponds to Vect1, column 2 to Vect2, and column 3 to
        Vect4.  This array is named Vect3_SMOOTH, up to a limit of 32
        characters. For example, if the array name is X1, the table name is
        X1_SMOOTH.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDNDTSD,{vect1},{vect2},{datap},{fitpt},{vect3},{vect4},{disp}"
        return self.run(command, **kwargs)

    def ednrot(
        self,
        option="",
        cid="",
        cname="",
        dof1="",
        dof2="",
        dof3="",
        dof4="",
        dof5="",
        dof6="",
        **kwargs,
    ):
        """Applies a rotated coordinate nodal constraint in an explicit dynamics

        APDL Command: EDNROT
        analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed:

            ADD - Add a rotated nodal coordinate constraint (default).

            DELE - Delete specified rotated nodal coordinate constraints.

            LIST - List all rotated nodal coordinate constraints.

        cid
            Coordinate system ID for which rotated nodal constraints will be
            added or deleted. The CID must have been previously defined with
            the EDLCS command. If Option = DELE, use CID = ALL to delete all
            previously specified nodal constraints.

        cname
            Nodal component set to which the rotated coordinate constraint will
            be applied. Cname must be previously specified using the CM
            command.

        dof1, dof2, dof3, . . . , dof6
            Degrees of freedom for which the rotated nodal constraint will be
            applied.  Valid degree of freedom labels include UX, UY, UZ, ROTX,
            ROTY, and ROTZ.  If DOF1 = ALL, rotated nodal constraints will be
            applied to all degrees of freedom.

        Notes
        -----
        Constraints applied with EDNROT are zero displacement constraints.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = (
            f"EDNROT,{option},{cid},{cname},{dof1},{dof2},{dof3},{dof4},{dof5},{dof6}"
        )
        return self.run(command, **kwargs)

    def edpart(self, option="", partid="", cname="", **kwargs):
        """Configures parts for an explicit dynamics analysis.

        APDL Command: EDPART

        Parameters
        ----------
        option
            Option used to organize parts. (No default; Option must be
            specified.)

            CREATE - Creates new PART IDs assigned to groups of elements with unique combinations of
                     MAT, TYPE, and REAL set numbers. If this option is issued
                     repeatedly, the part list is overwritten, except for PART
                     IDs created with the ADD option. Remaining fields are
                     ignored for this option.

            UPDATE - Updates the PART IDs for the element groups without changing the order of the
                     existing part list. If elements are redefined (or new
                     elements are created) with different MAT, TYPE, or REAL
                     set numbers, then use this option to create an updated
                     list of PART IDs. Remaining fields are ignored for this
                     option.

            ADD - Assigns a user-specified PART ID (PARTID) to the elements contained in the
                  element component Cname, or to the currently selected set of
                  elements if Cname = ALL. Use this option to assign a specific
                  PART ID to an element group that has the same combination of
                  MAT, TYPE, and REAL set numbers. An UPDATE operation is
                  automatically performed on the currently selected set of
                  elements immediately following the ADD operation.

            DELE - Deletes a PART ID assigned by the ADD option. PARTID is also required. An
                   UPDATE operation is automatically performed on the currently
                   selected set of elements immediately following the DELE
                   operation.

            LIST - Lists the PART IDs for the element groups. The part list consists of five
                   columns of numbers, one each for PART, MAT, TYPE, and REAL
                   numbers, and one to indicate if the PART ID is used
                   (including how many elements use it). The part list is based
                   on the last CREATE or UPDATE operation. Remaining fields are
                   ignored for this option.

        partid
            A positive integer to be used as PART ID for the elements specified
            by Cname (no default). The number input must not be currently used
            for an existing part (except when Option = DELE). Any previously
            defined PART IDs for the elements, whether assigned by the user or
            created by ANSYS LS-DYNA, will be overwritten. The user-specified
            PART ID will not be changed by subsequent EDPART,CREATE or
            EDPART,UPDATE commands.

        cname
            Element component name for user-specified PART ID definition
            (Option = ADD). If Cname = ALL (default), all currently selected
            elements are considered for the part. The elements in the element
            component (or the currently selected set of elements if Cname = ALL
            or blank) must have the same combination of MAT, TYPE, and REAL set
            numbers, or the ADD option will be ignored.

        Notes
        -----
        Certain ANSYS LS-DYNA commands (such as EDCGEN, EDLOAD, EDREAD, etc.)
        refer to PART IDs. You must define PART IDs (EDPART,CREATE or
        EDPART,ADD) before using these commands.

        If parts are repeatedly created using Option = CREATE, the part list is
        continuously overwritten. This may cause problems for previously
        defined commands that reference a part number that has changed. To
        avoid this problem, the part list should be updated (Option = UPDATE)
        rather than recreated to obtain the current part list.

        EDPART,ADD allows you to assign a specific part number to a group of
        elements instead of a number generated by the ANSYS LS-DYNA program.
        The user-specified PART IDs will not be changed by subsequent
        EDPART,CREATE or EDPART,UPDATE commands. Thus, you can use EDPART,ADD
        to specify PART IDs for some element groups, and use EDPART,CREATE or
        EDPART,UPDATE to assign PART IDs for the remaining element groups. Use
        EDPART,DELE to delete a PART ID generated by the ADD option. In this
        case, ANSYS LS-DYNA will generate a new PART ID for those elements
        associated with the deleted PART ID.

        After creating or updating the part list, use EDPART,LIST to list the
        PART IDs and choose the correct one for use with other ANSYS LS-DYNA
        commands. For a detailed discussion on PART IDs, see The Definition of
        Part in the ANSYS LS-DYNA User's Guide.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDPART,{option},{partid},{cname}"
        return self.run(command, **kwargs)

    def edpc(self, min_="", max_="", inc="", **kwargs):
        """Selects and plots explicit dynamic contact entities.

        APDL Command: EDPC

        Parameters
        ----------
        min\_
            Minimum contact entity number to be selected and plotted (default
            = 1).

        max\_
            Maximum contact entity number to be selected and plotted (default =
            MIN).

        inc
            Contact entity number increment (default = 1).

        Notes
        -----
        EDPC invokes an ANSYS macro which selects and plots explicit dynamic
        contact entities. The plot will consist of nodes or elements, depending
        on the method (node components or parts) that was used to define the
        contact surfaces (see the EDCGEN command). For single surface contact
        definitions, all external surfaces within the model are plotted.

        Note:: : EDPC changes the selected set of nodes and elements. After
        plotting contact entities, you must reselect all nodes and elements
        (NSEL and ESEL) required for subsequent operations, such as SOLVE

        Use the EDCLIST command to list the contact entity numbers for all
        defined contact.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDPC,{min_},{max_},{inc}"
        return self.run(command, **kwargs)

    def edsp(self, option="", min_="", max_="", inc="", **kwargs):
        """Specifies small penetration checking for contact entities in an

        APDL Command: EDSP
        explicit dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed (no default).

            ON   - Turn small penetration checking on for specified contact entities.

            OFF - Turn small penetration checking off for specified contact entities.

            LIST   - List current setting for penetration checking.

        min\_
            Minimum contact entity number for which to turn on/off small
            penetration check (default = 1).

        max\_
            Maximum contact entity number for which to turn on/off small
            penetration check (defaults to MIN).

        inc
            Contact entity number increment (default = 1).

        Notes
        -----
        This command controls small penetration checking in an explicit dynamic
        analysis. EDSP is applicable only to the following contact types: STS,
        NTS, OSTS, TNTS, and TSTS. The penetration checking specified by EDSP
        is similar to PENCHK on the EDCONTACT command. However, EDSP controls
        penetration checking for individual contact entities whereas PENCHK is
        a global control that applies to all defined contact (of the types
        mentioned above). EDSP can be used in a new analysis, or in a small
        restart (EDSTART,2).

        Use the EDCLIST command to list the contact entity numbers for all
        defined contact.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDSP,{option},{min_},{max_},{inc}"
        return self.run(command, **kwargs)

    def edweld(
        self,
        option="",
        nweld="",
        n1="",
        n2="",
        sn="",
        ss="",
        expn="",
        exps="",
        epsf="",
        tfail="",
        nsw="",
        cid="",
        **kwargs,
    ):
        """Defines a massless spotweld or generalized weld for use in an explicit

        APDL Command: EDWELD
        dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed:

            ADD - Define a weld (default). This weld may be a spotweld between two nodes or a
                  generalized weld. A massless spotweld will be defined if
                  valid node numbers are specified in fields N1 and N2. A
                  generalized weld will be defined if a node component is
                  specified in field N1.

            DELE - Delete specified weld. If NWELD is blank, all welds are deleted.

            LIST - List specified weld. If NWELD is blank, all welds are listed.

        nweld
            Reference number identifying the spotweld or generalized weld.

        n1, n2
            For a spotweld, N1 and N2 are the nodes which are connected by the
            spotweld. For a generalized weld, input a nodal component name in
            N1 and leave N2 blank. The nodal component should contain all nodes
            that are to be included in the generalized weld.

        sn
            Normal force at spotweld failure.

        ss
            Shear force at spotweld failure.

        expn
            Exponent for normal spotweld force.

        exps
            Exponent for shear spotweld force.

        epsf
            Effective plastic strain at ductile failure (used only for a
            generalized weld).

        tfail
            Failure time for constraint set (used only for a generalized weld);
            default = 1.0e20.

        nsw
            Number of spot welds for the generalized weld.

        cid
            Coordinate system ID number (CID) to be used for output data (used
            only for a generalized weld). The coordinate system must be
            previously defined with the EDLCS command.

        Notes
        -----
        This command can be used to define a massless spotweld between two
        nodes or a generalized weld for a group of nodes.  For a spotweld, the
        nodes specified by N1 and N2 must not be coincident. For a generalized
        weld, coincident nodes are permitted, but CID must be specified when
        using coincident nodes. EDWELD is not updated after a node merge
        operation; therefore, node merging [NUMMRG,NODE] should be done before
        any EDWELD definitions. Nodes connected by a spotweld or generalized
        weld cannot be constrained in any other way.

        Failure of the weld occurs when:

        where fn and fs are normal and shear interface forces. Normal interface
        force fn is nonzero for tensile values only.

        You can graphically display spotwelds by issuing the command
        /PBC,WELD,,1.

        This command is also valid in SOLUTION.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDWELD,{option},{nweld},{n1},{n2},{sn},{ss},{expn},{exps},{epsf},{tfail},{nsw},{cid}"
        return self.run(command, **kwargs)

    def edadapt(self, part="", key="", **kwargs):
        """Activates adaptive meshing in an explicit dynamic analysis.

        APDL Command: EDADAPT

        Parameters
        ----------
        part
            Part ID (number) for which adaptive meshing is to be turned on (or
            off). Use PART = STAT to list the current adaptive meshing
            definitions.

        key
            Adaptivity key:

            OFF - Do not use adaptive meshing for the specified part ID (default).

            ON - Use adaptive meshing for the specified part ID.

        Notes
        -----
        When adaptive meshing (adaptivity) is turned on, the mesh will
        automatically be regenerated to ensure adequate element aspect ratios.
        Adaptive meshing is most commonly used in the analysis of large
        deformation processes such as metal forming, in which the blank would
        need to be adaptively meshed.

        Adaptive meshing is only valid for parts consisting of SHELL163
        elements. By default, adaptive meshing is OFF for all parts in the
        model. To specify adaptive meshing for more than one part in the model,
        you must issue the EDADAPT command for each part ID. Use the EDPART
        command to create and list valid part IDs. Use the EDCADAPT command to
        define additional adaptive meshing parameters.

        The EDADAPT command is not supported in an explicit dynamic full
        restart analysis (EDSTART,3). In addition, a full restart cannot be
        performed successfully if adaptive meshing was used in the previous
        analysis.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDADAPT,{part},{key}"
        return self.run(command, **kwargs)

    def edale(
        self,
        option="",
        afac="",
        bfac="",
        dfac="",
        efac="",
        start="",
        end="",
        **kwargs,
    ):
        """Assigns mesh smoothing to explicit dynamic elements that use

        APDL Command: EDALE
        the ALE formulation.

        Parameters
        ----------
        option
            Label identifying the option to be performed:

            ADD - Add smoothing controls (default).

            DELETE - Delete smoothing controls.

            LIST - List smoothing controls.

        afac
            Simple average smoothing weight factor (default = 0).

        bfac
            Volume weighted smoothing weight factor (default = 0).

        dfac
            Equipotential smoothing weight factor (default = 0).

        efac
            Equilibrium smoothing weight factor (default = 0). EFAC is only
            applicable to PLANE162 elements.

        start
            Start time for ALE smoothing (default = 0).

        end
            End time for ALE smoothing (default = 1e20).

        Notes
        -----
        Mesh smoothing specified by the EDALE command is only
        applicable to PLANE162 and SOLID164 elements that are flagged
        to use the ALE formulation (KEYOPT(5) = 1). To activate the
        ALE formulation, you must specify at least one smoothing
        weight factor on this command and the number of cycles between
        advection (NADV) on the EDGCALE command. See Arbitrary
        Lagrangian-Eulerian Formulation in the ANSYS LS-DYNA User's
        Guide for more information.

        The EDALE command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDALE,{option},,{afac},{bfac},,{dfac},{efac},{start},{end}"
        return self.run(command, **kwargs)

    def edbvis(self, qvco="", lvco="", **kwargs):
        """Specifies global bulk viscosity coefficients for an explicit dynamics

        APDL Command: EDBVIS
        analysis.

        Parameters
        ----------
        qvco
            Quadratic viscosity coefficient (defaults to 1.5).

        lvco
            Linear viscosity coefficient (defaults to 0.06).

        Notes
        -----
        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDBVIS,{qvco},{lvco}"
        return self.run(command, **kwargs)

    def edcadapt(
        self,
        freq="",
        tol="",
        opt="",
        maxlvl="",
        btime="",
        dtime="",
        lcid="",
        adpsize="",
        adpass="",
        ireflg="",
        adpene="",
        adpth="",
        maxel="",
        **kwargs,
    ):
        """Specifies adaptive meshing controls for an explicit dynamic analysis.

        APDL Command: EDCADAPT

        Parameters
        ----------
        freq
            Time interval between adaptive mesh refinements (default = 0.0).
            Use FREQ = STAT to list the current adaptive meshing control
            settings.

        tol
            Adaptive angle tolerance (in degrees) for which adaptive meshing
            will occur (default = 1e31). If the relative angle change between
            elements exceeds the specified tolerance value, the elements will
            be refined.

        opt
            Adaptivity option:

            1 - Angle change (in degrees) of elements is based on original mesh configuration
                (default).

            2 - Angle change (in degrees) of elements is incrementally based on previously
                refined mesh.

        maxlvl
            Maximum number of mesh refinement levels (default = 3). This
            parameter controls the number of times an element can be remeshed.
            Values of 1, 2, 3, 4, etc. allow a maximum of 1, 4, 16, 64, etc.
            elements, respectively, to be created for each original element.

        btime
            Birth time to begin adaptive meshing (default = 0.0).

        dtime
            Death time to end adaptive meshing (default = 1e31).

        lcid
            Data curve number (previously defined on the EDCURVE command)
            identifying the interval of remeshing (no default). The abscissa of
            the data curve is time, and the ordinate is the varied adaptive
            time interval. If LCID is nonzero, the adaptive frequency (FREQ) is
            replaced by this load curve. Note that a nonzero FREQ value is
            still required to initiate the first adaptive loop.

        adpsize
            Minimum element size to be adapted based on element edge length
            (default = 0.0).

        adpass
            One or two pass adaptivity option.

            0 - Two pass adaptivity (default).

            1 - One pass adaptivity.

        ireflg
            Uniform refinement level flag (no default). Values of 1, 2, 3, etc.
            allow 4, 16, 64, etc. elements, respectively, to be created
            uniformly for each original element.

        adpene
            Adaptive mesh flag for starting adaptivity when approaching
            (positive ADPENE value) or penetrating (negative ADPENE value) the
            tooling surface (default = 0.0).

        adpth
            Absolute shell thickness level below which adaptivity should begin.
            This option works only if the adaptive angle tolerance (TOL) is
            nonzero. If thickness based adaptive remeshing is desired without
            angle change, set TOL to a large angle. The default is ADPTH = 0.0,
            which means this option is not used.

        maxel
            Maximum number of elements at which adaptivity will be terminated
            (no default). Adaptivity is stopped if this number of elements is
            exceeded.

        Notes
        -----
        The EDCADAPT command globally sets the control options for all part IDs
        that are to be adaptively meshed (see the EDADAPT command). Because
        FREQ defaults to zero, you must input a nonzero value in this field in
        order to activate adaptive meshing. You must also specify a reasonable
        value for TOL since the default adaptive angle tolerance (1e31) will
        not allow adaptive meshing to occur.

        The EDCADAPT command is not supported in an explicit dynamic full
        restart analysis (EDSTART,3).

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCADAPT,{freq},{tol},{opt},{maxlvl},{btime},{dtime},{lcid},{adpsize},{adpass},{ireflg},{adpene},{adpth},{maxel}"
        return self.run(command, **kwargs)

    def edcpu(self, cputime="", **kwargs):
        """Specifies CPU time limit for an explicit dynamics analysis.

        APDL Command: EDCPU

        Parameters
        ----------
        cputime
            CPU time limit (in seconds) for the current phase of the analysis
            (defaults to 0). If CPUTIME = 0, no CPU time limit is set. CPUTIME
            values below 0 are not allowed.

        Notes
        -----
        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCPU,{cputime}"
        return self.run(command, **kwargs)

    def edcsc(self, key="", **kwargs):
        """Specifies whether to use subcycling in an explicit dynamics analysis.

        APDL Command: EDCSC

        Parameters
        ----------
        key
            Subcycling key:

            OFF - Do not use subcycling (default).

            ON - Use subcycling.

        Notes
        -----
        Subcycling can be used to speed up an analysis when element sizes
        within a model vary significantly. Relatively small elements will
        result in a small time step size. When subcycling is on, the minimum
        time step size is increased for the smallest elements.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCSC,{key}"
        return self.run(command, **kwargs)

    def edcts(self, dtms="", tssfac="", **kwargs):
        """Specifies mass scaling and scale factor of computed time step for an

        APDL Command: EDCTS
        explicit dynamics analysis.

        Parameters
        ----------
        dtms
            Time step size for mass scaled solutions (defaults to 0).

        tssfac
            Scale factor for computed time step. Defaults to 0.9; if high
            explosives are used, the default is lowered to 0.67.

        Notes
        -----
        If DTMS is positive, the same time step size will be used for all
        elements and mass scaling will be done for all elements.  Therefore,
        positive values should only be used if inertial effects are
        insignificant.

        If DTMS is negative, mass scaling is applied only to elements whose
        calculated time step size is smaller than DTMS.  Negative values should
        only be used in transient analyses if the mass increases are
        insignificant.

        In order to use mass scaling in an explicit dynamic small restart
        analysis (EDSTART,2) or full restart analysis (EDSTART,3), mass scaling
        must have been active in the original analysis. The time step and scale
        factor used in the original analysis will be used by default in the
        restart. You can issue EDCTS in the restart analysis to change these
        settings.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDCTS,{dtms},{tssfac}"
        return self.run(command, **kwargs)

    def eddamp(self, part="", lcid="", valdmp="", **kwargs):
        """Defines mass weighted (Alpha) or stiffness weighted (Beta) damping for

        APDL Command: EDDAMP
        an explicit dynamics model.

        Parameters
        ----------
        part
            PART number [EDPART] identifying the group of elements to which
            damping should be applied. If PART = ALL (default), damping is
            applied to the entire model.

        lcid
            Load curve ID (previously defined with the EDCURVE command)
            identifying the damping coefficient versus time curve. If time-
            dependent damping is defined, an LCID is required.

        valdmp
            Constant system damping coefficient or a scale factor applied to
            the curve defining damping coefficient versus time.

        Notes
        -----
        Mass-weighted (Alpha) or stiffness-weighted (Beta) damping can be
        defined with the EDDAMP command. Generally, stiffness proportional or
        beta damping is effective for oscillatory motion at high frequencies.
        This type of damping is orthogonal to rigid body motion and so will not
        damp out rigid body motion. On the other hand, mass proportional or
        alpha damping is more effective for low frequencies and will damp out
        rigid body motion. The different possibilities are described below:

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.

        Mass-weighted or Alpha damping

        When PART = (blank) or ALL (default), mass-weighted global damping can
        be defined in the following two ways. In this case, the same damping is
        applied for the entire structure.

        When the damping coefficient versus time curve (LCID) is specified
        using the EDCURVE command, VALDMP is ignored by LS-DYNA (although it is
        written in the LS-DYNA input file Jobname.K).  The damping force
        applied to each node in the model is given by fd = d(t)mv, where d(t)
        is the damping coefficient as a function of time defined by the EDCURVE
        command, m is the mass, and v is the velocity.

        When the LCID is 0 or blank (default), a constant mass-weighted system
        damping coefficient can be specified using VALDMP.

        The constant and time-dependent damping, described above, cannot be
        defined simultaneously. The last defined global damping will overwrite
        any previously defined global damping.

        Mass-weighted or Alpha damping

        When both a valid PART number is specified and the damping coefficient
        versus time curve (LCID) is specified using the EDCURVE command, mass-
        weighted time-dependent damping will be defined for the particular
        PART.  In this case, VALDMP will act as a scaling factor for the
        damping versus time curve (if VALDMP is not specified, it will default
        to 1). A valid PART number must be specified to define this type of
        damping. For example, use PART =1 (and not blank) when the entire model
        consists of only one PART.  Issue the command repeatedly with different
        PART numbers in order to specify alpha damping for different PARTS.

        Stiffness-weighted or Beta damping

        When a valid PART number is specified with LCID = 0 or (blank)
        (default), a stiffness-weighted (Beta) constant damping coefficient for
        this particular PART can be defined by VALDMP. The stiffness-weighted
        value corresponds to the percentage of damping in the high frequency
        domain. For example, 0.1 roughly corresponds to 10% damping in the high
        frequency domain. Recommended values range from 0.01 to 0.25. Values
        lower than 0.01 may have little effect. If a value larger than 0.25 is
        used, it may be necessary to lower the time step size significantly
        (see the EDCTS command). Issue the command repeatedly with different
        PART numbers in order to specify beta damping for different PARTS.
        Time-dependent stiffness-weighted damping is not available in ANSYS LS-
        DYNA.

        The mass-weighted and stiffness-weighted damping, described above,
        cannot be defined simultaneously for a particular PART number. The last
        defined damping for the particular PART number will overwrite any
        previously defined mass-weighted or stiffness-weighted damping for this
        PART.

        In order to define the mass-weighted and stiffness-weighted damping
        simultaneously, you can use the MP,BETD command (instead of the
        EDDAMP,PART, ,VALDMP command) to define stiffness-weighted (Beta)
        constant damping coefficient. However, do not use both of these
        commands together to define stiffness-weighted (Beta) constant damping
        coefficient for a particular PART. If you do, duplicate stiffness-
        weighted (Beta) constant damping coefficients for this PART will be
        written to the LS-DYNA input file Jobname.K.  The last defined value
        will be used by LS-DYNA. Also, note that the MP,BETD command is applied
        on the MAT number, and not on the PART number. Since a group of
        elements having the same MAT ID may belong to more than one PART (the
        opposite is not true), you need to issue the MP,BETD command only once
        for this MAT ID and the stiffness-weighted (Beta) damping coefficients
        will be automatically defined for all the PARTs with that MAT ID.

        Mass-weighted and stiffness-weighted damping can be defined
        simultaneously using the EDDAMP command only when mass-weighted damping
        (constant or time-dependent) is defined as global damping (EDDAMP, ALL,
        LCID, VALDMP) and stiffness-weighted damping is defined for all
        necessary PARTs (EDDAMP,PART, ,VALDMP).

        To remove defined global damping, reissue the EDDAMP, ALL command with
        LCID and VALDMP set to 0. To remove damping defined for a particular
        PART, reissue EDDAMP, PART, where PART is the PART number, with LCID
        and VALDMP set to 0. There is no default for the EDDAMP command, i.e.,
        issuing the EDDAMP command with PART = LCID = VALDMP = 0 will result in
        an error. Stiffness-weighted damping defined by the MP,BETD command can
        be deleted using MPDELE, BETD, MAT.

        In an explicit dynamic small restart (EDSTART,2) or full restart
        analysis (EDSTART,3), you can only specify global alpha damping. This
        damping will overwrite any alpha damping input in the original
        analysis. If you do not input global alpha damping in the restart, the
        damping properties input in the original analysis will carry over to
        the restart.

        Damping specified by the EDDAMP command can be listed, along with other
        explicit dynamics specifications, by typing the command string
        EDSOLV$STAT into the ANSYS input window. Beta damping specified by the
        MP,BETD command can be listed by MPLIST, MAT command.

        This command is also valid in PREP7.
        """
        command = f"EDDAMP,{part},{lcid},{valdmp}"
        return self.run(command, **kwargs)

    def eddrelax(
        self,
        option="",
        nrcyck="",
        drtol="",
        dffctr="",
        drterm="",
        tssfdr="",
        irelal="",
        edttl="",
        **kwargs,
    ):
        """Activates initialization to a prescribed geometry or dynamic relaxation

        APDL Command: EDDRELAX
        for the explicit analysis.

        Parameters
        ----------
        option
            Specifies when dynamic relaxation is activated.

            ANSYS - Stresses are initialized in ANSYS LS-DYNA to a prescribed geometry for small
                    strains, according to the solution of an ANSYS (implicit)
                    run. The explicit solution is based on the implicit X,Y,Z
                    displacements and rotations contained in the drelax file
                    (created with the REXPORT command).

            DYNA - Dynamic relaxation is on. When you use this option, you can specify some or all
                   of the parameters NRCYCK, DRTOL, DFFCTR, DRTERM, TSSFDR,
                   IRELAL, and EDTTL. Any parameters that you do not specify
                   are set to their default values.

            OFF - Turn off initialization to a prescribed geometry (Option = ANSYS) or dynamic
                  relaxation (Option = DYNA).

        nrcyck
            Number of iterations between convergence checks for dynamic
            relaxation option. Default = 250.

        drtol
            Convergence tolerance for dynamic relaxation option. Default =
            0.001.

        dffctr
            Dynamic relaxation factor. Default = 0.995.

        drterm
            Optional termination time for dynamic relaxation. Termination
            occurs at this time, or when convergence is attained, whichever
            comes first. Default = infinity.

        tssfdr
            Scale factor for computed time step during dynamic relaxation. If
            zero, the value is set to TSSFAC (defined on the EDCTS command).
            After converging, the scale factor is reset to TSSFAC.

        irelal
            Automatic control for dynamic relaxation option based on algorithm
            of Papadrakakis.

            0 - Not active (default).

            1 - Active.

        edttl
            Convergence tolerance on automatic control of dynamic relaxation
            (default = 0.04).

        Notes
        -----
        Use Option = ANSYS when running an implicit-to-explicit sequential
        solution to initialize the structure to a static solution performed
        earlier by the ANSYS implicit solver. Use Option = DYNA to perform
        dynamic relaxation within the LS-DYNA program. Use Option = OFF to turn
        off previously specified stress initialization or dynamic relaxation.
        You must specify the Option you want; there is no default.

        In LS-DYNA, the dynamic relaxation is performed before the regular
        transient analysis. The convergence process of the dynamic relaxation
        is not written to the ANSYS history file. The ANSYS results files only
        include the converged result of the dynamic relaxation, which is the
        result at time zero in the Jobname.HIS and Jobname.RST files.

        You can restart a dynamic relaxation analysis (EDSTART,2 or EDSTART,3)
        from a previous transient analysis or a previous dynamic relaxation
        analysis. In the restart, you can change or set the convergence
        criteria with the EDDRELAX command. Only the load curves that are
        flagged for dynamic relaxation (PHASE = 1 or 2 on EDLOAD) are applied
        after restarting. If you restart the explicit portion of an implicit-
        to-explicit sequential solution, you do not need to reissue the REXPORT
        command because displacement information contained in the drelax file
        is already included in the LS-DYNA restart file. If the dynamic
        relaxation is activated from a regular transient analysis, LS-DYNA
        continues the output of data to ANSYS results files. This is unlike the
        dynamic relaxation phase at the beginning of the calculation for which
        only the converged solution is written.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDDRELAX,{option},{nrcyck},{drtol},{dffctr},{drterm},{tssfdr},{irelal},{edttl}"
        return self.run(command, **kwargs)

    def eddump(self, num="", dt="", **kwargs):
        """Specifies output frequency for the explicit dynamic restart file

        APDL Command: EDDUMP
        (d3dump).

        Parameters
        ----------
        num
            Number of d3dump (restart) files written during the analysis
            (defaults to 1). When you specify NUM, the time interval between
            restart files is TIME / NUM, where TIME is the analysis end-time
            specified on the TIME command.

        dt
            Time interval at which the d3dump (restart) files are written. If
            NUM is input, DT is ignored.

        Notes
        -----
        You can use NUM or DT to specify the time interval at which d3dump
        restart files will be written. You should not specify both quantities;
        if both are input, NUM will be used. The restart files are written
        sequentially as d3dump01, d3dump02, etc.

        In LS-DYNA, the restart file output is specified in terms of number of
        time steps. Because the total number of time steps is not known until
        the LS-DYNA solution finishes, Mechanical APDL calculates an
        approximate number of time steps for the solution, and then uses NUM or
        DT to calculate the required LS-DYNA input. This approximated number of
        time steps may be different from the total number reached in LS-DYNA
        after the solution finishes. Therefore, the number of restart dump
        files or the output interval may differ slightly from what you
        requested using NUM or DT.

        In an explicit dynamic small restart (EDSTART,2) or full restart
        analysis (EDSTART,3), the EDDUMP setting will default to the NUM or DT
        value used in the original analysis. You can issue EDDUMP in the
        restart to change this setting.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDDUMP,{num},{dt}"
        return self.run(command, **kwargs)

    def edenergy(self, hgen="", swen="", sien="", rlen="", **kwargs):
        """Specifies energy dissipation controls for an explicit dynamics

        APDL Command: EDENERGY
        analysis.

        Parameters
        ----------
        hgen
            Hourglass energy control key:

            OFF or 0 - Hourglass energy is not computed.

            ON or 1 - Hourglass energy is computed and included in the energy balance (default).

        swen
            Stonewall energy dissipation control key:

            OFF or 0 - Stonewall energy dissipation is not computed.

            ON or 1 - Stonewall energy dissipation is computed and included in the energy balance
                      (default).

        sien
            Sliding interface energy dissipation control key:

            OFF or 0 - Sliding interface energy dissipation is not computed.

            ON or 1 - Sliding interface energy dissipation is computed and included in the energy
                      balance (default).

        rlen
            Rayleigh (damping) energy dissipation control key:

            OFF or 0 - Rayleigh energy dissipation is not computed.

            ON or 1 - Rayleigh energy dissipation is computed and included in the energy balance
                      (default).

        Notes
        -----
        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDENERGY,{hgen},{swen},{sien},{rlen}"
        return self.run(command, **kwargs)

    def edfplot(self, key="", **kwargs):
        """Allows plotting of explicit dynamics forces and other load symbols.

        APDL Command: EDFPLOT

        Parameters
        ----------
        key
            Load symbol plotting key.

            ON or 1 - Turn display of load symbols on (default).

            OFF or 0 - Turn display of load symbols off.

        Notes
        -----
        You must issue EDFPLOT,ON to display explicit dynamics load symbols.
        The explicit load symbols are erased automatically upon a subsequent
        plot command.

        An explicit load symbol always indicates a positive load direction
        (e.g., positive X direction for FX load), even if the load value is
        negative. The load symbol does not reflect the load magnitude. You can
        use standard ANSYS symbol controls to control the appearance of the
        load symbol. No load symbol is displayed for temperature loads.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDFPLOT,{key}"
        return self.run(command, **kwargs)

    def edgcale(self, nadv="", meth="", **kwargs):
        """Defines global ALE controls for an explicit dynamic analysis.

        APDL Command: EDGCALE

        Parameters
        ----------
        nadv
            Number of cycles between advection (default = 0).

        meth
            Advection method.

            0 - Donor cell + Half Index Shift (first order accurate) (default).

            1 - Van Leer + Half Index Shift (second order accurate).

        Notes
        -----
        This command sets global ALE controls in an explicit dynamic analysis.
        These ALE controls apply to all PLANE162 or SOLID164 elements in the
        model that are flagged to use the ALE formulation (KEYOPT(5) = 1). To
        activate the ALE formulation, you must specify the number of cycles
        between advection on this command and at least one smoothing weight
        factor on the EDALE command. See Arbitrary Lagrangian-Eulerian
        Formulation in the ANSYS LS-DYNA User's Guide for more information.

        To see the current EDGCALE settings, issue the command EDALE,LIST.

        The EDGCALE command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDGCALE,{nadv},{meth}"
        return self.run(command, **kwargs)

    def edhgls(self, hgco="", **kwargs):
        """Specifies the hourglass coefficient for an explicit dynamics analysis.

        APDL Command: EDHGLS

        Parameters
        ----------
        hgco
            Hourglass coefficient value (defaults to 0.1). Values greater than
            0.15 may cause instabilities.

        Notes
        -----
        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDHGLS,{hgco}"
        return self.run(command, **kwargs)

    def edhist(self, comp="", **kwargs):
        """Specifies time-history output for an explicit dynamic analysis.

        APDL Command: EDHIST

        Parameters
        ----------
        comp
            Name of the component containing nodes or elements for which output
            is desired. Comp is required.

        Notes
        -----
        The time-history output is written to the file Jobname.HIS.  Output is
        written only for the nodes or elements contained in Comp.  The data is
        written at time intervals specified on the EDHTIME command. If no time
        interval is specified, output is written at 1000 steps over the
        analysis. (See also the EDOUT command which controls time-history
        output in ascii form for an explicit dynamics analysis.)

        Use EDHIST,LIST to list the time-history output specification. (The
        listing will include output requested with the EDOUT command.) Use
        EDHIST,DELE to delete the time-history output specification.

        Jobname.HIS is a binary file that is read by the ANSYS time-history
        postprocessor (POST26). If LS-DYNA output has been requested on the
        EDWRITE command [EDWRITE,LSDYNA or EDWRITE,BOTH], the file D3THDT will
        also be written. D3THDT is a binary file that is read by the LS-POST
        postprocessor.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDHIST,{comp}"
        return self.run(command, **kwargs)

    def edhtime(self, nstep="", dt="", **kwargs):
        """Specifies the time-history output interval for an explicit dynamics

        APDL Command: EDHTIME
        analysis.

        Parameters
        ----------
        nstep
            Number of steps at which output is written to the time-history
            file, Jobname.HIS, and the ASCII output files. Defaults to 1000.
            The time increment between output is TIME / NSTEP, where TIME is
            the analysis end-time specified on the TIME command.

        dt
            Time interval at which output is written to the time-history file,
            Jobname.HIS, and the ASCII output files. If NSTEP is input, DT is
            ignored.

        Notes
        -----
        EDHTIME controls the number of steps at which output will be written to
        the time-history file, Jobname.HIS (see the EDHIST command), and any
        ASCII files requested on the EDOUT command. You can use NSTEP or DT to
        specify the output interval. You should not specify both quantities; if
        both are input, NSTEP will be used.

        In an explicit dynamic small restart (EDSTART,2) or full restart
        analysis (EDSTART,3), the EDHTIME setting will default to the NSTEP or
        DT value used in the original analysis. You can issue EDHTIME in the
        restart to change this setting.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDHTIME,{nstep},{dt}"
        return self.run(command, **kwargs)

    def edint(self, shellip="", beamip="", **kwargs):
        """Specifies number of integration points for explicit shell and beam

        APDL Command: EDINT
        output.

        Parameters
        ----------
        shellip
            Number of shell integration points used for output (defaults to 3).
            For element SHELL163, each integration point is associated with a
            layer. SHELLIP must be  3. If SHELLIP = 3, results are written for
            the shell top, middle, and bottom. If SHELLIP >3, then the results
            for the first SHELLIP layers are written.

        beamip
            Number of beam integration points used for stress output for
            BEAM161 (defaults to 4).

        Notes
        -----
        The number of integration points is defined by the element real
        constant NIP for both the beam elements (in the cross section) and the
        shell elements (through the thickness).

        For shell elements that have only 1 or 2 integration points (NIP = 1 or
        2), use the default of SHELLIP = 3. If NIP = 1, the same results are
        reported at the top, middle, and bottom layers.  If the NIP = 2, the
        results at the bottom correspond to integration point 1, the results at
        the top correspond to integration point 2, and the results at the
        middle are an average of the top and bottom results.

        For shell elements with 2 x 2 integration points in the plane, the data
        from the four points are averaged, and there is a single output value
        for each layer.

        If you set BEAMIP = 0, no stress output is written for BEAM161
        elements. In this case, the beams will not appear in any POST1 plots
        because the program assumes they are failed elements.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDINT,{shellip},{beamip}"
        return self.run(command, **kwargs)

    def edis(self, option="", pidn="", pido="", **kwargs):
        """Specifies stress initialization in an explicit dynamic full restart

        APDL Command: EDIS
        analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            ADD - Define stress initialization between parts (default).

        pidn
            New part ID or part assembly ID in the full restart analysis
            (defaults to all parts in the model).

        pido
            Old part ID or part assembly ID in the previous analysis, (default
            to PIDN).

        Notes
        -----
        The EDIS command is only valid in an explicit dynamic full restart
        analysis (EDSTART,3). (EDIS is ignored if it is not preceded by the
        EDSTART,3 command.) Use EDIS to specify which parts and/or part
        assemblies should undergo stress initialization in the restart based on
        the stresses from the previous analysis. You can specify stress
        initialization for multiple parts (or part assemblies) by issuing EDIS
        multiple times. If you issue EDIS with no arguments, stress
        initialization is performed for all parts in the restart analysis that
        have a corresponding part (having the same part ID) in the previous
        analysis.

        In a full restart analysis, the complete database is written as an LS-
        DYNA input file, Jobname_nn.K. When the LS-DYNA solution begins, LS-
        DYNA performs the stress initialization using file Jobname_nn.K and the
        restart dump file (d3dumpnn specified on the EDSTART command) from the
        previous analysis. At the end of initialization, all the parts that
        were specified by the EDIS commands are initialized from the data saved
        in the restart dump file. In order for the stress initialization to be
        performed successfully, the new parts in the full restart analysis and
        the old parts in the previous analysis must have the same number of
        elements, same element order, and same element topology. (The parts may
        have different identifying numbers.) If this is not the case, the
        stresses cannot be initialized. If part assemblies are used, the part
        assemblies must contain the same number of parts. (See A Full Restart
        in the ANSYS LS-DYNA User's Guide for more details).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDIS,{option},{pidn},{pido}"
        return self.run(command, **kwargs)

    def edload(
        self,
        option="",
        lab="",
        key="",
        cname="",
        par1="",
        par2="",
        phase="",
        lcid="",
        scale="",
        btime="",
        dtime="",
        **kwargs,
    ):
        """Specifies loads for an explicit dynamics analysis.

        APDL Command: EDLOAD

        Parameters
        ----------
        option
            Label identifying the load option to be performed.

            ADD - Define a load (default). If Option = ADD, Cname must be a valid node or element
                  component name (or PART number). You must also specify a load
                  curve using Par1 and Par2 (previously defined array
                  parameters) or LCID (a previously defined load curve).

            DELE - Delete specified load. If Lab and Cname are blank, all loads are deleted. Par1,
                   Par2, PHASE, and LCID are ignored for this option.

            LIST - List specified load. If Lab and Cname are blank, all loads are listed. Par1,
                   Par2, PHASE, and LCID are ignored for this option.

        lab
            Valid load labels for loads applied to nodes:

            FX, FY, FZ - Forces.

            MX, MY, MZ - Moments.

            UX, UY, UZ - Displacements.

            ROTX, ROTY, ROTZ - Rotations.

            VX, VY, VZ - Velocities.

            OMGX, OMGY, OMGZ - Angular velocities.

            AX, AY, AZ - Accelerations (on nodes).

            ACLX, ACLY, ACLZ - Base accelerations.

            TEMP - Temperature.

        key
            When Lab = PRESS, KEY = Load key (face number) associated with a
            surface pressure load. Load keys (1,2,3, etc.) are listed under
            "Surface Loads" in the input data tables for each element type in
            the Element Reference.

        cname
            Name of existing component [CM] or PART number [EDPART] to which
            this load is to be applied.  For all load labels except the
            pressure load (Lab = PRESS) and the rigid body loads (Lab = RBxx),
            the component must consist of nodes. For pressure loads, the
            component must consist of elements. For rigid body loads, a part
            number must be input instead of a component name. The part number
            must correspond to a set of elements that has been identified as a
            rigid body [EDMP,RIGID,MAT].

        par1
            Name of user-defined array parameter that contains the time values
            of the load.

        par2
            Name of user-defined array parameter that contains the "data"
            values of the load corresponding to the time values in Par1.

        phase
            Phase of the analysis in which the load curve is to be used.

            0 - Curve is used in transient analysis only (default).

            1 - Curve is used in stress initialization or dynamic relaxation only.

            2 - Curve is used in both stress initialization (or dynamic relaxation) and
                transient analysis.

        lcid
            Data curve ID number representing the load curve to be applied. The
            load curve must have been previously defined using the EDCURVE
            command. If LCID is specified, Par1 and Par2 must be left blank (in
            the GUI, select "None" for Par1 and Par2).

        scale
            Load curve scale factor applied to the specified load curve. The
            scale value is applied to the data in Par2 or to the ordinate data
            in the load curve specified by LCID.

        btime
            Birth time, or time when imposed motion is activated. The default
            is 0.0. Some load types do not support birth and death time; see
            Table 132: Birth Time, Death Time, and CID Support in the Notes
            section for more information.

        dtime
            Death time, or time when imposed motion is removed. The default is
            1 x 1038. Some load types do not support birth and death time; see
            Table 132: Birth Time, Death Time, and CID Support in the Notes
            section for more information.

        Notes
        -----
        If a component name is input (Cname) and the specified component
        definition is changed before the SOLVE command, the last definition
        will be used.

        You can specify the load data by inputting LCID (the ID number of a
        previously defined load curve) or by inputting the two array parameters
        Par1 and Par2 (which contain time and load values, respectively). The
        input for Par1 and Par2 may be a single column array parameter, or a
        specific column from a multi-column array parameter. A starting array
        element number can be specified for Par1 and Par2; if none is
        specified, array element 1 is used by default.
        """
        command = f"EDLOAD,{option},{lab},{key},{cname},{par1},{par2},{phase},{lcid},{scale},{btime},{dtime}"
        return self.run(command, **kwargs)

    def edopt(self, option="", value="", **kwargs):
        """Specifies the type of output for an explicit dynamics analysis.

        APDL Command: EDOPT

        Parameters
        ----------
        option
            Label identifying the option to be performed:

            ADD - Define an output type specification (default).

            DELE - Delete an output type specification.

            LIST - List the current output type specification.

        value
            Label identifying the type of output that the LS-DYNA
            solver should produce:

            ANSYS - Write results files for the ANSYS postprocessors
                    (default). The files that will be written are
                    Jobname.RST and Jobname.HIS (see "Notes" below).

            LSDYNA - Write results files for the LS-DYNA postprocessor
                     (LS-POST). The files that will be written are
                     D3PLOT, and files specified by EDOUT and EDHIST
                     (see "Notes" below).

            BOTH - Write results files for both ANSYS and LS-DYNA
            postprocessors.

        Notes
        -----
        By default, LS-DYNA will write the ANSYS results file
        Jobname.RST (see the EDRST command.)  If Jobname.HIS is
        desired, you must also issue EDHIST.

        Value = LSDYNA or BOTH will cause LS-DYNA to write results
        files for the LS-POST postprocessor. The D3PLOT file is always
        written for these two options. If other LS-POST files are
        desired, you must issue the appropriate EDHIST and EDOUT
        commands.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        return self.run(f"EDOPT,{option},,{value}", **kwargs)

    def edout(self, option="", **kwargs):
        """Specifies time-history output (ASCII format) for an explicit dynamics

        APDL Command: EDOUT
        analysis.

        Parameters
        ----------
        option
            Output data option. Each option corresponds to a separate file that
            is written by the LS-DYNA solver. If Option = ALL, all files except
            NODOUT and ELOUT are written. Valid options are:

            GLSTAT - Global data (default).

            BNDOUT - Boundary condition forces and energy.

            RWFORC - Wall force.

            DEFORC - Discrete element data.

            MATSUM - Material energies data.

            NCFORC - Nodal interface forces.

            RCFORC - Resultant interface force data.

            DEFGEO - Deformed geometry data.

            SPCFORC - SPC reaction force data.

            SWFORC - Nodal constraint reaction force data (spotwelds and rivets).

            RBDOUT - Rigid body data.

            GCEOUT - Geometry contact entities.

            SLEOUT - Sliding interface energy.

            JNTFORC - Joint force data.

            NODOUT - Nodal data.

            ELOUT - Element data.

        Notes
        -----
        This command specifies output to be written during an explicit dynamics
        solution. The data corresponding to each Option is written to a
        separate ASCII file having the same name as the Option label. The data
        is written for the entire model at time intervals specified by the
        EDHTIME command. If no time interval is specified, output is written at
        1000 steps over the analysis. (See also the EDHIST command which
        specifies time-history output for a portion of the model.)  The data
        written to the MATSUM file is actually for each PART number (EDPART) at
        time intervals specified by the EDHTIME command, but the data is listed
        following the Mat no. in the file.

        For Option = NODOUT and ELOUT, you must specify a component; you must
        issue EDHIST before issuing EDOUT,NODOUT or EDOUT,ELOUT.

        Use EDOUT,LIST to list the current time-history output specifications.
        (The listing will include output requested with the EDHIST command.)
        Use EDOUT,DELE to delete all output specifications that have been
        defined with the EDOUT command.

        In order for the specified output files to be written, you must also
        request that explicit dynamics results be written to an LS-DYNA output
        file [EDWRITE,LSDYNA or EDWRITE,BOTH].

        In an explicit dynamic small restart analysis (EDSTART,2) or full
        restart analysis (EDSTART,3), the same ASCII files that were requested
        for the original analysis are written by default for the restart. You
        can request different files by issuing the appropriate EDOUT commands
        in the restart analysis.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDOUT,{option}"
        return self.run(command, **kwargs)

    def edpl(self, ldnum="", **kwargs):
        """Plots a time dependent load curve in an explicit dynamic analysis.

        APDL Command: EDPL

        Parameters
        ----------
        ldnum
             Load number.

        Notes
        -----
        EDPL invokes an ANSYS macro which produces a load vs. time graph for a
        load defined with the EDLOAD command. Only one load curve can be
        plotted at a time. Use EDLOAD,LIST to obtain a list of loads and
        corresponding load numbers.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDPL,{ldnum}"
        return self.run(command, **kwargs)

    def edpvel(
        self,
        option="",
        pid="",
        vx="",
        vy="",
        vz="",
        omegax="",
        omegay="",
        omegaz="",
        xc="",
        yc="",
        zc="",
        angx="",
        angy="",
        angz="",
        **kwargs,
    ):
        """Applies initial velocities to parts or part assemblies in an explicit

        APDL Command: EDPVEL
        dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            VGEN - Define initial velocities for the part or part assembly based on translational
                   velocities (relative to global Cartesian) and the rotational
                   velocity about an arbitrary axis. For this option, use the
                   fields VX, VY, VZ to specify the translational velocities,
                   and use OMEGAX, XC, YC, ZC, ANGX, ANGY, ANGZ to specify the
                   rotational velocity and the axis of rotation.

            VELO - Define initial velocity for the part or part assembly based on translational
                   velocities and nodal rotational velocities input relative to
                   the global Cartesian axes. For this option, use the
                   following fields to define the initial velocity: VX, VY, VZ,
                   OMEGAX, OMEGAY, OMEGAZ.

            LIST - List initial velocity for the part or part assembly specified by PID. If PID is
                   blank, all initial velocities defined on parts and part
                   assemblies are listed. Remaining fields are ignored for this
                   option.

            DELE - Delete initial velocity defined for the part or part assembly specified by PID.
                   If PID is blank, all initial velocities defined on parts and
                   part assemblies are deleted. Remaining fields are ignored
                   for this option.

        pid
            Part ID or part assembly ID to which the initial velocity is to be
            applied. The part or assembly ID must be defined (EDPART or EDASMP)
            before issuing this command.

        vx
            Initial velocity in X direction. Defaults to 0.

        vy
            Initial velocity in Y direction. Defaults to 0.

        vz
            Initial velocity in Z direction. Defaults to 0.

        omegax
            For Option = VGEN, OMEGAX is the initial rotational velocity of the
            part or part assembly about the specified rotational axis. For
            Option = VELO, OMEGAX is the initial nodal rotational velocity
            about the X-axis. OMEGAX defaults to 0.

        omegay
            Initial nodal rotational velocity about the Y-axis (used only if
            Option = VELO). Defaults to 0.

        omegaz
            Initial nodal rotational velocity about the Z-axis (used only if
            Option = VELO). Defaults to 0.

        Notes
        -----
        You cannot mix the two methods of initial velocity input (Option = VELO
        and Option = VGEN) in the same analysis. You must use only one method
        for all initial velocity definitions.

        The VGEN and VELO methods differ in how the rotational velocity is
        defined. Use Option = VGEN to input the initial velocities of a
        rotating part or part assembly. Use Option = VELO to apply the
        rotations directly to the nodes' rotation degrees of freedom. Since
        only shell and beam elements have rotation degrees of freedom, the
        rotations input with Option = VELO are only applicable to SHELL163 and
        BEAM161 elements. The rotational velocities input with Option = VELO
        are ignored for nodes not having rotational degrees of freedom (such as
        nodes attached to a SOLID164 or SOLID168 element).

        It is normally acceptable to mix nodes belonging to deformable bodies
        and rigid bodies in the part assembly used in an initial velocity
        definition. However, when defining initial velocities in an implicit-
        to-explicit sequential solution, this is not an acceptable practice. In
        order for the initial velocities to be defined correctly in this type
        of analysis, you must define the initial velocities on the deformable
        body nodes separately from the initial velocities on the rigid body
        nodes.

        Issuing the EDPVEL command again for the same part or part assembly
        (PID) will overwrite previous initial velocities defined for that part
        or part assembly.

        To set the initial velocities to zero, issue the EDPVEL command with
        only the Option (use VELO or VGEN) and PID fields specified.

        In a small restart analysis (EDSTART,2), you can only use the Option =
        VELO method to change initial velocities. When used in a small restart,
        the command EDPVEL,VELO changes the velocity of the specified part or
        part assembly. If you don't change the velocity of the parts and
        assemblies, their velocity at the beginning of the restart will be the
        same as the velocity at the end of the previous analysis.

        Except for the LIST option, the EDPVEL command is not supported in a
        full restart analysis (EDSTART,3). You can list initial velocities
        defined in the previous analysis with the command EDPVEL,LIST. However,
        you cannot change initial velocities for parts that existed in the
        previous analysis; their velocity at the beginning of the analysis will
        be the same as the velocity at the end of the previous analysis. In
        addition, you cannot define initial velocities for any parts that are
        added in the full restart; the velocity of new parts will be zero.

        To apply initial velocities to node components or nodes, use the EDVEL
        command.

        You can use EDPVEL and EDVEL in the same analysis. If a node or node
        component input on the EDVEL command shares common nodes with a part or
        part assembly input on the EDPVEL command, the initial velocities
        defined on the common nodes will be determined by the last command
        input.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDPVEL,{option},{pid},{vx},{vy},{vz},{omegax},{omegay},{omegaz},{xc},{yc},{zc},{angx},{angy},{angz}"
        return self.run(command, **kwargs)

    def edrc(self, option="", nrbf="", ncsf="", dtmax="", **kwargs):
        """Specifies rigid/deformable switch controls in an explicit dynamic

        APDL Command: EDRC
        analysis.

        Parameters
        ----------
        option
            Label identifying option to be performed.

            ADD - Define rigid/deformable controls (default).

            DELE - Delete rigid/deformable controls.

            LIST - List rigid/deformable controls.

        nrbf
            Flag to delete/activate nodal rigid bodies. If nodal rigid bodies
            or generalized weld definitions are active in the deformable bodies
            that are switched to rigid, then the definitions should be deleted
            to avoid instabilities.

            0 - No change from previous status (default).

            1 - Delete.

            2 - Activate.

        ncsf
            Flag to delete/activate nodal constraint set. If nodal
            constraint/spotweld definitions are active in the deformable bodies
            that are switched to rigid, then the definitions should be deleted
            to avoid instabilities.

            0 - No change from previous status (default).

            1 - Delete.

            2 - Activate.

        tdmax
            Maximum allowed time step after restart (no default).

        Notes
        -----
        This command is only valid in an explicit dynamic small
        restart analysis (EDSTART,2). Use this command when you do a
        rigid/deformable switch (EDRD command) and you want to control
        constraints defined by other means for the deformable body
        (such as nodal constraints or a weld). For example, if a
        deformable body has nodal constraints defined and it is
        switched to a rigid body, the nodal constraints should be
        deleted since they are invalid for the rigid body. Later on,
        if you want to switch the rigid body to deformable again and
        retain the nodal constraints, you can use EDRC to activate the
        constraints previously defined for the deformable
        body. Otherwise, the nodal constraints remain deactivated.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported
        in Distributed ANSYS.
        """
        return self.run(f"EDRC,{option},{nrbf},{ncsf},,{dtmax}", **kwargs)

    def edrd(self, option="", part="", mrb="", **kwargs):
        """Switches a part from deformable to rigid or from rigid to deformable in

        APDL Command: EDRD
        an explicit dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            D2R - Change specified part from deformable to rigid (default).

            R2D - Change specified part from rigid to deformable. Use this option to switch a
                  part back to a deformable state after it has been changed to
                  rigid using EDRD,D2R.

            LIST - List parts that are flagged to change from deformable to rigid or rigid to
                   deformable.

        part
            Part number for part to be changed (no default).

        mrb
            Part number of the master rigid body to which the part is merged.
            MRB is used only if Option = D2R. If MRB = 0 (which is the
            default), the part becomes an independent rigid body.

        Notes
        -----
        This command is valid in a new explicit dynamic analysis or in a
        restart. It is only possible to switch parts (D2R or R2D) in a restart
        if part switching is first activated in the original analysis. If part
        switching is not required in the original analysis but will be used in
        the restart, you must issue EDRD,D2R with no further arguments in the
        original analysis. You can use the EDRI command to define inertia
        properties for newly created rigid bodies (D2R).

        Parts that are defined as rigid using EDMP,RIGID are permanently rigid
        and cannot be changed to deformable.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDRD,{option},{part},{mrb}"
        return self.run(command, **kwargs)

    def edri(
        self,
        option="",
        part="",
        xc="",
        yc="",
        zc="",
        tm="",
        ixx="",
        iyy="",
        izz="",
        ixy="",
        iyz="",
        ixz="",
        **kwargs,
    ):
        """Defines inertia properties for a new rigid body that is created when a

        APDL Command: EDRI
        deformable part is switched to rigid in an explicit dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            ADD - Define inertia for specified part (default).

            DELE - Delete inertia definition for specified part.

            LIST - List inertia definitions.

        part
            Part number for which inertia is defined (no default).

        xc, yc, zc
            X, Y, and Z-coordinates of the center of mass (no defaults).

        tm
            Translational mass (no default).

        ixx, iyy, izz, ixy, iyz, ixz
            Components (xx, yy, etc.) of inertia tensor. IXX, IYY, and IZZ must
            be input (no defaults). IXY, IYZ, and IXZ default to zero.

        Notes
        -----
        Use this command to define inertia properties for a rigid body that is
        created when a deformable part is switched to rigid (using the EDRD,D2R
        command) in an explicit dynamic analysis. If these properties are not
        defined, LS-DYNA will compute the new rigid body properties from the
        finite element mesh (which requires an accurate mesh representation of
        the body). When rigid bodies are merged to a master rigid body, the
        inertia properties defined for the master rigid body apply to all
        members of the merged set.

        EDRI can only be issued in a new analysis. Therefore, if you are going
        to use inertia properties in a subsequent restart analysis, you must
        issue EDRI in the original analysis for the part that will later be
        switched to rigid in the restart.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDRI,{option},{part},{xc},{yc},{zc},{tm},{ixx},{iyy},{izz},{ixy},{iyz},{ixz}"
        return self.run(command, **kwargs)

    def edrst(self, nstep="", dt="", **kwargs):
        """Specifies the output interval for an explicit dynamic analysis.

        APDL Command: EDRST

        Parameters
        ----------
        nstep
            Number of steps at which output is written to the results file
            (Jobname.RST). Defaults to 100. When you specify NSTEP, NSTEP+2
            results are written to the Jobname.RST file. The time interval
            between output is TIME / NSTEP, where TIME is the analysis end-time
            specified on the TIME command. Do not specify a value of NSTEP = 0.

        dt
            Time interval at which output is written to the results file
            (Jobname.RST). If NSTEP is input, DT is ignored.

        Notes
        -----
        You can use NSTEP or DT to specify the output interval to be used for
        Jobname.RST. You should not specify both quantities; if both are input,
        NSTEP will be used.

        In an explicit dynamic small restart (EDSTART,2) or full restart
        analysis (EDSTART,3), the EDRST setting will default to the NSTEP or DT
        value used in the original analysis. You can issue EDRST in the restart
        to change this setting.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDRST,{nstep},{dt}"
        return self.run(command, **kwargs)

    def edrun(self, option="", cons="", ncpu="", **kwargs):
        """Specify LS-DYNA serial or parallel processing.

        APDL Command: EDRUN

        Parameters
        ----------
        option
             LS-DYNA processing option

            SERIAL - Use serial processing (default)

            SMP - Use Shared Memory Parallel processing

        cons
            Consistency setting (only applicable when Option = SMP)

            0 - Result consistency is not required (default)

            1 - Result consistency is required

        ncpu
            Number of processors to use (applicable only with Option = SMP)

        Notes
        -----
        The EDRUN command specifies either serial (one CPU) processing or
        shared (multiple CPU) memory parallel processing (SMP). When using SMP,
        the calculations may be executed in a different order, depending on CPU
        availability and the load on each CPU. You may therefore see slight
        differences in the results when running the same job multiple times,
        either with the same number or a different number of processors.
        Comparing nodal accelerations often shows wider discrepancies. To avoid
        such differences, you can specify that consistency be maintained by
        setting CONS = 1. Maintaining consistency can result in an increase of
        up to 15 percent in CPU time.

        The parallel processing setting is only effective when you have
        multiple CPUs and licenses for the appropriate number of ANSYS LS-DYNA
        SMP tasks. If your site does not meet both requirements, the EDRUN
        command sets serial processing, regardless of command settings.

        For more information on using SMP, see Solution Features in the ANSYS
        LS-DYNA User's Guide.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDRUN,{option},{cons},{ncpu}"
        return self.run(command, **kwargs)

    def edshell(self, wpan="", shnu="", shtc="", wpbt="", shpl="", itrst="", **kwargs):
        """Specifies shell computation controls for an explicit dynamics analysis.

        APDL Command: EDSHELL

        Parameters
        ----------
        wpan
            Maximum shell element warpage angle in degrees. Defaults to 20.

        shnu
            Hughes-Liu shell normal update option:

            -2 - Unique nodal fibers. This option is required for SHELL163 (KEYOPT(1) = 1, 6, or
                 7) if the real constant NLOC = 1 or -1.

            -1 - Compute normals each cycle (default). This option is recommended.

            1 - Compute on restarts.

            n - Compute every nth substep.

        shtc
            Shell thickness change option:

            0 - No change.

            1 - Membrane straining causes thickness change. Important in sheet metal forming
                (default).

        wpbt
            Warping stiffness option for Belytschko-Tsay shells:

            1 - Belytschko-Wong-Chiang warping stiffness added. This option is recommended.

            2 - Belytschko-Tsay warping stiffness (default).

        shpl
            Shell plasticity option. This option is only valid for these
            material models: strain rate independent plastic kinematic, strain
            rate dependent plasticity, power law plasticity, and piecewise
            linear plasticity.

            1 - Iterative plasticity with 3 secant iterations (default).

            2 - Full iterative plasticity.

            3 - Radial return noniterative plasticity. (Use this option with caution; it may
                lead to inaccurate results.)

        itrst
            Triangular shell sorting option. If sorting is on, degenerate
            quadrilateral shell elements are treated as triangular shells.

            1 - Full sorting (default).

            2 - No sorting.

        Notes
        -----
        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDSHELL,{wpan},{shnu},{shtc},{wpbt},{shpl},{itrst}"
        return self.run(command, **kwargs)

    def edsolv(self, **kwargs):
        """Specifies "explicit dynamics solution" as the subsequent status topic.

        APDL Command: EDSOLV

        Notes
        -----
        This is a status [STAT] topic command. Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDSOLV,"
        return self.run(command, **kwargs)

    def edstart(self, restart="", memory="", fsize="", dumpfile="", **kwargs):
        """Specifies status (new or restart) of an explicit dynamics analysis.

        APDL Command: EDSTART

        Parameters
        ----------
        restart
            Status of the analysis (new or restart).

            0 - New analysis (default).

            1 - Simple restart.

            2 - Small restart.

            3 - Full restart.

        memory
            Memory to be used (in words). If blank, LS-DYNA assigns a value
            (default). If more or less memory is needed, specify the number of
            words (a word is usually 32 bits on a workstation).

        fsize
            Scale factor for binary file sizes. Defaults to 7, which is
            (7x262144) = 1835008 words.

        dumpfile
            Name of dump file to use during a restart (for example, d3dumpnn,
            where nn = 01, 02, 03,...,99 and defaults to 01). Leave this field
            blank when running a new analysis (RESTART = 0) so that the default
            dump file d3dump01 will be created.

        Notes
        -----
        EDSTART can be issued before the SOLVE command to specify a new
        analysis, a simple restart, a small restart, or a full restart as
        described below.

        New analysis: For a new analysis, you do not need to issue EDSTART
        unless you want to change the MEMORY or FSIZE option. If you do not
        specify the dump file name, d3dump01 will be created by default.

        Simple restart: This option assumes that the database has not been
        altered. Upon restarting, results will be appended to the existing
        results files. Issue EDSTART,1,,,d3dumpnn to indicate which restart
        file to use as a starting point. The dump file to be used must have
        been created in an earlier run and must be available at the time this
        command is issued.  You would typically use a simple restart when you
        interrupt the LS-DYNA run via Ctrl+C and terminate the run prematurely
        by issuing the "sense switch control" key SW1 (see Solution Control and
        Monitoring in the ANSYS LS-DYNA User's Guide). At this point you should
        be able to view the partial solution using ANSYS postprocessors. After
        you are done viewing the partial solution, you can reenter the solution
        processor and issue EDSTART,1,,,d3dumpnn, followed by SOLVE to continue
        with the analysis. The results will be appended to the results files
        Jobname.RST and Jobname.HIS.  You can perform multiple simple restarts
        by issuing EDSTART,1,,,d3dumpnn multiple times, as needed. The
        solutions in the Jobname.RST file will all be in load step number 1.

        Small restart: This option can be used when minor changes in the
        database are necessary. For example, you can reset the termination
        time, reset the output interval, add displacement constraints, change
        initial velocities, switch parts from a deformable to rigid state, etc.
        (See A Small Restart in theANSYS LS-DYNA User's Guide for a complete
        description of database items that can be changed.) Issue
        EDSTART,2,,,d3dumpnn followed by the commands required to change the
        database, then issue SOLVE. The results will be appended to the results
        files Jobname.RST and Jobname.HIS. You can perform multiple restarts by
        issuing EDSTART,2,,,d3dumpnn multiple times, as needed. The additional
        restart solutions will be stored in Jobname.RST as load step numbers 2,
        3, etc.

        Full restart: A full restart is appropriate when many modifications to
        the database are required. For example, you can change the model
        geometry, apply different loading conditions, etc. Issue
        EDSTART,3,,,d3dumpnn to denote a full restart analysis. The Jobname
        will automatically be changed to Jobname_nn, (nn = 01 initially, and
        will be incremented each time EDSTART,3 is issued for subsequent full
        restarts). After the EDSTART command, you can input any commands needed
        to change the database. (Most commands which are applicable to an ANSYS
        LS-DYNA new analysis are also applicable to full restart analysis. A
        few commands related to contact specifications, initial velocity
        definitions, and adaptive meshing are not supported.) Then issue the
        EDIS command to specify which portions of the model should be
        initialized in the full restart using results data from the d3dumpnn
        file. Finally, issue the SOLVE command. At this point, new results
        files, Jobname_nn.RST and Jobname_nn.HIS, will be created. Time and
        output intervals in the new results files are continuous from the
        previous results files; the time is not reset to zero. (See A Full
        Restart in the ANSYS LS-DYNA User's Guide for a complete description of
        a full restart analysis.)

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDSTART,{restart},{memory},{fsize},{dumpfile}"
        return self.run(command, **kwargs)

    def edterm(self, option="", lab="", num="", stop="", maxc="", minc="", **kwargs):
        """Specifies termination criteria for an explicit dynamic analysis.

        APDL Command: EDTERM

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            ADD - Define termination criteria (default).

            DELE - Delete termination criteria.

            LIST - List termination criteria.

        lab
            Label identifying the type of termination (no default).

            NODE - Terminate solution based on nodal point coordinates. The analysis terminates
                   when the current position of the specified node reaches
                   either the maximum or minimum coordinate value (STOP = 1, 2,
                   or 3), or when the node picks up force from any contact
                   surface (STOP = 4).

            PART - Terminate solution based on rigid body (part) displacements. The analysis
                   terminates when the displacement of the center of mass of
                   the specified rigid body reaches either the maximum or
                   minimum value (STOP = 1, 2, or 3), or when the displacement
                   magnitude of the center of mass is exceeded (STOP = 4).

        num
            Node number (if Lab = NODE) or rigid body Part ID (if Lab = PART).
            (No default.)

        stop
            Criterion for stopping the solution (no default).

            1 - Global X-direction.

            2 - Global Y-direction.

            3 - Global Z-direction.

            4 - For Lab = NODE, stop the solution if contact occurs. For Lab = PART, stop the
                solution if the displacement magnitude is exceeded for the
                specified rigid body (use MAXC to define the displacement
                magnitude).

        maxc
            Maximum (most positive) coordinate value (Lab = NODE) or
            displacement (Lab = PART). MAXC defaults to 1.0e21

        minc
            Minimum (most negative) coordinate value (Lab = NODE) or
            displacement (Lab = PART). MINC defaults to -1.0e21.

        Notes
        -----
        You may specify multiple termination criteria using EDTERM; the
        solution will terminate when any one of the criteria is satisfied, or
        when the solution end time (specified on the TIME command) is reached.

        In an explicit dynamic small restart analysis (EDSTART,2) or full
        restart analysis (EDSTART,3), the termination criteria set in the
        previous analysis (the original analysis or the previous restart) are
        carried over to the restart. If the previous analysis terminated due to
        one of these criteria, that specific criterion must be modified so that
        it will not cause the restart to terminate prematurely. In particular,
        if a termination condition based on nodal contact (Lab = NODE, STOP =
        4) is satisfied, this condition must be deleted and replaced with a
        condition based on nodal coordinates for that same node. (If a
        condition based on nodal coordinates already exists for that node, the
        replacement is not necessary.) In the restart, the number of
        termination criteria specified using EDTERM cannot exceed a maximum of
        10 or the number specified in the original analysis.

        Note that the termination criteria set by EDTERM are not active during
        dynamic relaxation (EDDRELAX).

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDTERM,{option},{lab},{num},{stop},{maxc},{minc}"
        return self.run(command, **kwargs)

    def edtp(
        self,
        option: MapdlInt = "",
        value1: MapdlInt = "",
        value2: MapdlFloat = "",
        **kwargs,
    ) -> Optional[str]:  # pragma: no cover
        """Plots explicit elements based on their time step size.

        APDL Command: EDTP

        Parameters
        ----------
        option
             Plotting option (default = 1).

            1 - Plots the elements with the smallest time step
                sizes. The number of elements plotted and listed is
                equal to VALUE1 (which defaults to 100).  Each element
                is shaded red or yellow based on its time step value
                (see "Notes" for details).

            2 - Produces the same plot as for OPTION = 1, and also
                produces a list of the plotted elements and their
                corresponding time step values.

            3 - Produces a plot similar to OPTION = 1, except that all
                selected elements are plotted. Elements beyond the
                first VALUE1 elements are blue and translucent. The
                amount of translucency is specified by VALUE2.  This
                option also produces a list of the first VALUE1
                elements with their corresponding time step values.

        value1
            Number of elements to be plotted and listed (default =
            100). For example, if VALUE1 = 10, only the elements with
            the 10 smallest time step sizes are plotted and listed.

        value2
            Translucency level ranging from 0 to 1 (default =
            0.9). VALUE2 is only used when OPTION = 3, and only for
            the elements plotted in blue. To plot these elements as
            non-translucent, set VALUE2 = 0.

        Notes
        -----
        EDTP invokes an ANSYS macro that plots and lists explicit
        elements based on their time step size. For OPTION = 1 or 2,
        the number of elements plotted is equal to VALUE1 (default =
        100). For OPTION = 3, all selected elements are plotted.

        The elements are shaded red, yellow, or blue based on their
        time step size. Red represents the smallest time step sizes,
        yellow represents the intermediate time step sizes, and blue
        represents the largest time step sizes. For example, if you
        specify VALUE1 = 30, and if T1 is the smallest critical time
        step of all elements and T30 is the time step of the 30th
        smallest element, then the elements are shaded as follows:

        Translucent blue elements only appear when OPTION = 3.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDTP,{option},{value1},{value2}"
        return self.run(command, **kwargs)

    def edvel(
        self,
        option="",
        cname="",
        vx="",
        vy="",
        vz="",
        omegax="",
        omegay="",
        omegaz="",
        xc="",
        yc="",
        zc="",
        angx="",
        angy="",
        angz="",
        **kwargs,
    ):
        """Applies initial velocities to nodes or node components in an explicit

        APDL Command: EDVEL
        dynamic analysis.

        Parameters
        ----------
        option
            Label identifying the option to be performed.

            VGEN - Define initial velocities based on translational velocities (relative to global
                   Cartesian) and the rotational velocity about an arbitrary
                   axis. For this option, use the fields VX, VY, VZ to specify
                   the translational velocities, and use OMEGAX, XC, YC, ZC,
                   ANGX, ANGY, ANGZ to specify the rotational velocity and the
                   axis of rotation.

            VELO - Define initial velocity based on translational velocities and nodal rotational
                   velocities input relative to the global Cartesian axes. For
                   this option, use the following fields to define the initial
                   velocity: VX, VY, VZ, OMEGAX, OMEGAY, OMEGAZ.

            LIST - List initial velocity for the component or node specified by Cname. If Cname is
                   blank, all initial velocities defined on nodes and node
                   components are listed. Remaining fields are ignored for this
                   option.

            DELE - Delete initial velocity defined for the component or node specified by Cname.
                   If Cname is blank, all initial velocities defined on nodes
                   and node components are deleted. Remaining fields are
                   ignored for this option.

        cname
            Name of existing component [CM] or node number to which the initial
            velocity is to be applied. If a component is used, it must consist
            of nodes.

        vx
            Initial velocity in X direction. Defaults to 0.

        vy
            Initial velocity in Y direction. Defaults to 0.

        vz
            Initial velocity in Z direction. Defaults to 0.

        omegax
            For Option = VGEN, OMEGAX is the initial rotational velocity of the
            component (or node) about the specified rotational axis. For Option
            = VELO, OMEGAX is the initial nodal rotational velocity about the
            X-axis. OMEGAX defaults to 0.

        omegay
            Initial nodal rotational velocity about the Y-axis (used only if
            Option = VELO). Defaults to 0.

        omegaz
            Initial nodal rotational velocity about the Z-axis (used only if
            Option = VELO). Defaults to 0.

        Notes
        -----
        You cannot mix the two methods of initial velocity input (Option = VELO
        and Option = VGEN) in the same analysis. You must use only one method
        for all initial velocity definitions.

        The VGEN and VELO methods differ in how the rotational velocity is
        defined. Use Option = VGEN to input the initial velocities of a
        rotating component. Use Option = VELO to apply the rotations directly
        to the nodes' rotation degrees of freedom. Since only shell and beam
        elements have rotation degrees of freedom, the rotations input with
        Option = VELO are only applicable to SHELL163 and BEAM161 elements. The
        rotational velocities input with Option = VELO are ignored for nodes
        not having rotational degrees of freedom (such as nodes attached to a
        SOLID164 or SOLID168 element).

        It is normally acceptable to mix nodes belonging to deformable bodies
        and rigid bodies in the nodal component used in an initial velocity
        definition. However, when defining initial velocities in an implicit-
        to-explicit sequential solution, this is not an acceptable practice. In
        order for the initial velocities to be defined correctly in this type
        of analysis, you must define the initial velocities on the deformable
        body nodes separately from the initial velocities on the rigid body
        nodes.

        Issuing the EDVEL command again for the same component or node (Cname)
        will overwrite previous initial velocities defined for that component
        or node.

        To set the initial velocities to zero, issue the EDVEL command with
        only the Option (use VELO or VGEN) and Cname fields specified.

        In a small restart analysis (EDSTART,2), you can only use the Option =
        VELO method to change initial velocities. When used in a small restart,
        the command EDVEL,VELO changes the velocity of the specified nodes. If
        you don't change the velocity of the nodes, their velocity at the
        beginning of the restart will be the same as the velocity at the end of
        the previous analysis.

        Except for the LIST option, the EDVEL command is not supported in a
        full restart analysis (EDSTART,3). You can list initial velocities
        defined in the previous analysis with the command EDVEL,LIST. However,
        you cannot change initial velocities for nodes or node components that
        existed in the previous analysis; their velocity at the beginning of
        the analysis will be the same as the velocity at the end of the
        previous analysis. In addition, you cannot define initial velocities
        for any nodes that are added in the full restart; the velocity of new
        nodes will be zero.

        To apply initial velocities to parts or part assemblies, use the EDPVEL
        command.

        You can use EDPVEL and EDVEL in the same analysis. If a node or node
        component input on the EDVEL command shares common nodes with a part or
        part assembly input on the EDPVEL command, the initial velocities
        defined on the common nodes will be determined by the last command
        input.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDVEL,{option},{cname},{vx},{vy},{vz},{omegax},{omegay},{omegaz},{xc},{yc},{zc},{angx},{angy},{angz}"
        return self.run(command, **kwargs)

    def edwrite(self, option="", fname="", ext="", **kwargs):
        """Writes explicit dynamics input to an LS-DYNA input file.

        APDL Command: EDWRITE

        Parameters
        ----------
        option
            Sets a flag in the LS-DYNA input file (Fname.Ext) to produce
            desired output.

            ANSYS - Set a flag to write results files for the ANSYS
                    postprocessors (default).  The files that will be
                    written are Jobname.RST and Jobname.HIS (see Notes
                    below).

            LSDYNA - Set a flag to write results files for the LS-DYNA
                     postprocessor (LS-POST).  The files that will be
                     written are D3PLOT, and files specified by EDOUT
                     and EDHIST (see Notes below).

            BOTH - Set a flag to write results files for both ANSYS
            and LS-DYNA postprocessors.

        fname
            File name and directory path (80 characters maximum,
            including directory; this limit is due to an LS-DYNA
            program limitation). If you do not specify a directory
            path, it will default to your working directory. The file
            name defaults to Jobname. Previous data on this file, if
            any, are overwritten.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        This command writes an LS-DYNA input file for the LS-DYNA
        solver.  EDWRITE is only valid if explicit dynamic elements
        have been specified.  This command is not necessary if the
        LS-DYNA solver is invoked from within ANSYS, in which case
        Jobname.K (or Jobname.R) is written automatically when the
        solution is initiated. (If LS-DYNA is invoked from within
        ANSYS, use EDOPT to specify desired output.)

        If the analysis is a small restart (EDSTART,2), the file that
        is written will have the name Jobname.R (by default) and will
        only contain changes from the original analysis.

        If the analysis is a full restart (EDSTART,3), the file that
        is written will have the name Jobname_nn.K (by default) and
        will contain all the information from the database. In a full
        restart, the jobname is changed to Jobname_nn (nn = 01
        initially, and is incremented for each subsequent full
        restart.)

        A command is included in the LS-DYNA input file to instruct
        the LS-DYNA solver to write the results files indicated by
        Option.  By default, LS- DYNA will write the ANSYS results
        file Jobname.RST (see the EDRST command).  If Jobname.HIS is
        desired, you must also issue EDHIST.

        Option = LSDYNA or BOTH will cause LS-DYNA to write results
        files for the LS-POST postprocessor. The D3PLOT file is always
        written for these two options. If other LS-POST files are
        desired, you must issue the appropriate EDHIST and EDOUT
        commands.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"EDWRITE,{option},{fname},{ext}"
        return self.run(command, **kwargs)

    def rexport(self, target="", lstep="", sbstep="", fname="", ext="", **kwargs):
        """Exports displacements from an implicit run to ANSYS LS-DYNA.

        APDL Command: REXPORT

        Parameters
        ----------
        target
            The type of analysis run to which displacements are exported.

            OFF - Ignore initial displacements.

            DYNA - Get initial displacements from an earlier implicit
                   (ANSYS) run and export to an explicit ANSYS LS-DYNA
                   run (Default).

        lstep
            Load step number of data to be exported.  Defaults to the last load
            step.

        sbstep
            Substep number of data to be exported.  Defaults to the last
            substep.

        fname
            File name and directory path (248 characters maximum,
            including the characters needed for the directory path).
            An unspecified directory path defaults to the working
            directory; in this case, you can use all 248 characters
            for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        This command exports the displacements, rotations, and temperatures
        calculated in an ANSYS implicit analysis into the `drelax' file, which
        is subsequently read in by ANSYS LS-DYNA when a dynamic relaxation or
        stress initialization is conducted ``EDDRELAX``.

        This command is not written to the Jobname.CDB file when the CDWRITE
        command is issued.
        """
        command = f"REXPORT,{target},,,{lstep},{sbstep},{fname},{ext}"
        return self.run(command, **kwargs)
