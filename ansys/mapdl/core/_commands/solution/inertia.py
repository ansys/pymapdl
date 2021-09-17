class Inertia:
    def acel(self, acel_x="", acel_y="", acel_z="", **kwargs):
        """Specifies the linear acceleration of the global Cartesian reference

        APDL Command: ACEL
        frame for the analysis.

        Parameters
        ----------
        acel_x, acel_y, acel_z
            Linear acceleration of the reference frame along global Cartesian
            X, Y, and Z axes, respectively.

        Notes
        -----
        In the absence of any other loads or supports, the acceleration of the
        structure in each of the global Cartesian (X, Y, and Z) axes would be
        equal in magnitude but opposite in sign to that applied in the ACEL
        command. Thus, to simulate gravity (by using inertial effects),
        accelerate the reference frame with an ACEL command in the direction
        opposite to gravity.

        You can define the acceleration for the following analyses types:

        Static (ANTYPE,STATIC)

        Harmonic (ANTYPE,HARMIC), full or mode-superposition method

        Transient (ANTYPE,TRANS)

        Substructure (ANTYPE,SUBSTR).

        For all transient dynamic (ANTYPE,TRANS) analyses, accelerations are
        combined with the element mass matrices to form a body force load
        vector term. The element mass matrix may be formed from a mass input
        constant or from a nonzero density (DENS) property, depending upon the
        element type.

        For analysis type ANTYPE,HARMIC, the acceleration is assumed to be the
        real component with a zero imaginary component.

        Units of acceleration and mass must be consistent to give a product of
        force units.

        The ACEL command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for ACEL_X, ACEL_Y, and ACEL_Z input
        values (``*DIM``) as a function of both time and frequency for full
        transient and harmonic analyses.

        Related commands for rotational effects are CMACEL, CGLOC, CGOMGA,
        DCGOMG, DOMEGA, OMEGA, CMOMEGA, and CMDOMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        This command is also valid in /PREP7.

        Examples
        --------
        Set global y-acceleration to 9.81

        >>> mapdl.acel(acel_y=9.81)
        """
        command = f"ACEL,{acel_x},{acel_y},{acel_z}"
        return self.run(command, **kwargs)

    def cgloc(self, xloc="", yloc="", zloc="", **kwargs):
        """Specifies the origin location of the acceleration coordinate system.

        APDL Command: CGLOC

        Parameters
        ----------
        xloc, yloc, zloc
            Global Cartesian X, Y, and Z coordinates of the acceleration
            coordinate system origin.

        Notes
        -----
        Specifies the origin location of the acceleration coordinate system
        with respect to the global Cartesian system.  The axes of this
        acceleration coordinate system are parallel to the global Cartesian
        axes.

        A structure may be rotating about the global Cartesian origin [OMEGA,
        DOMEGA], which may in turn be rotating about another point (the origin
        of the acceleration coordinate system), introducing Coriolis effects.
        The location of this point (relative to the global Cartesian origin) is
        specified with this CGLOC command.  For example, if Y is vertical and
        the global system origin is at the surface of the earth while the
        acceleration system origin is at the center of the earth, YLOC should
        be -4000 miles (or equivalent) if the rotational effects of the earth
        are to be included.  The rotational velocity of the global Cartesian
        system about this point is specified with the CGOMGA command, and the
        rotational acceleration is specified with the DCGOMG command.

        The rotational velocities and accelerations are mainly intended to
        include mass effects in a static (ANTYPE,STATIC) analysis.  If used in
        dynamic analyses, no coupling exists between the user input terms and
        the time history response of the structure.  See Acceleration Effect in
        the Mechanical APDL Theory Reference for details.  Related commands are
        ACEL, CGOMGA, DCGOMG, DOMEGA, and OMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        This command is also valid in PREP7.
        """
        command = f"CGLOC,{xloc},{yloc},{zloc}"
        return self.run(command, **kwargs)

    def cgomga(self, cgomx="", cgomy="", cgomz="", **kwargs):
        """Specifies the rotational velocity of the global origin.

        APDL Command: CGOMGA

        Parameters
        ----------
        cgomx, cgomy, cgomz
            Rotational velocity of the global origin about the acceleration
            system X, Y, and Z axes.

        Notes
        -----
        Specifies the rotational velocity of the global origin about each of
        the acceleration coordinate system axes.  The location of the
        acceleration coordinate system is defined with the CGLOC command.
        Rotational velocities may be defined in analysis types ANTYPE,STATIC,
        HARMIC (full or mode-superposition), TRANS (full or mode-
        superposition), and SUBSTR.  See Acceleration Effect in the Mechanical
        APDL Theory Reference for details.  Units are radians/time.  Related
        commands are ACEL, CGLOC, DCGOMG,   DOMEGA, and OMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        The CGOMGA command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for CGOMGA_X, CGOMGA_Y, and CGOMGA_Z
        input values (``*DIM``) for full transient and harmonic analyses.

        This command is also valid in PREP7.
        """
        command = f"CGOMGA,{cgomx},{cgomy},{cgomz}"
        return self.run(command, **kwargs)

    def cmacel(self, cm_name="", cmacel_x="", cmacel_y="", cmacel_z="", **kwargs):
        """Specifies the translational acceleration of an element component

        APDL Command: CMACEL

        Parameters
        ----------
        cm_name
            The name of the element component.

        cmacel_x, cmacel_y, cmacel_z
            Acceleration of the element component CM_NAME in the global
            Cartesian X, Y, and Z axis directions, respectively.

        Notes
        -----
        The CMACEL command specifies the translational acceleration of the
        element component in each of the global Cartesian (X, Y, and Z) axis
        directions.

        Components for which you want to specify acceleration loading must
        consist of elements only. The elements you use cannot be part of more
        than one component, and elements that share nodes cannot exist in
        different element components. You cannot apply the loading to an
        assembly of element components.

        To simulate gravity (by using inertial effects), accelerate the
        structure in the direction opposite to gravity. For example, apply a
        positive CMACELY to simulate gravity acting in the negative Y
        direction. Units are length/time2.

        You can define the acceleration for the following analyses types:

        Static (ANTYPE,STATIC)

        Harmonic (ANTYPE,HARMIC), full or mode-superposition method

        Transient (ANTYPE,TRANS), full or mode-superposition method

        Substructure (ANTYPE,SUBSTR)

        Accelerations are combined with the element mass matrices to form a
        body force load vector term. Units of acceleration and mass must be
        consistent to give a product of force units.

        In a modal harmonic or transient analysis, you must apply the load in
        the modal portion of the analysis. Mechanical APDL calculates a load
        vector and writes it to the mode shape file, which you can apply via
        the LVSCALE command.

        The CMACEL command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for CMACEL_X, CMACEL_Y, and CMACEL_Z
        input values (``*DIM``) as a function of both time and frequency for full
        transient and harmonic analyses.

        Related commands for inertia loads are ACEL, CGLOC, CGOMGA, DCGOMG,
        DOMEGA, OMEGA, CMOMEGA, and CMDOMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        This command is also valid in /PREP7.
        """
        command = f"CMACEL,{cm_name},{cmacel_x},{cmacel_y},{cmacel_z}"
        return self.run(command, **kwargs)

    def cmdomega(
        self,
        cm_name="",
        domegax="",
        domegay="",
        domegaz="",
        x1="",
        y1="",
        z1="",
        x2="",
        y2="",
        z2="",
        **kwargs,
    ):
        """Specifies the rotational acceleration of an element component about a

        APDL Command: CMDOMEGA
        user-defined rotational axis.

        Parameters
        ----------
        cm_name,
            The name of the element component.

        domegax, domegay, domegaz
            If the X2, Y2, Z2 fields are not defined, DOMEGAX, DOMEGAY, and
            DOMEGAZ specify the components of the rotational acceleration
            vector in the global Cartesian X, Y, Z directions.

        x1, y1, z1
            If the X2, Y2, Z2 fields are defined, X1, Y1, and Z1 define the
            coordinates of the beginning point of the rotational axis vector.
            Otherwise, X1, Y1, and Z1 are the coordinates of a point through
            which the rotational axis passes.

        x2, y2, z2
            The coordinates of the end point of the rotational axis vector.

        Notes
        -----
        Specifies the rotational acceleration components DOMEGAX, DOMEGAY, and
        DOMEGAZ of an element component CM_NAME about a user-defined rotational
        axis. The rotational axis can be defined either as a vector passing
        through a single point, or a vector connecting two points.

        You can define the rotational acceleration and rotational axis with the
        CMDOMEGA command for STATIC, HARMIC, TRANS, and SUBSTR analyses.
        Rotational velocities are combined with the element mass matrices to
        form a body force load vector term. Units are radians/time2.

        The CMDOMEGA command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for CMDOMEGA_X, CMDOMEGA_Y, and
        CMDOMEGA_Z input values (``*DIM``) for full transient and harmonic
        analyses.

        Related commands are ACEL, CGLOC, CGLOC, OMEGA, CMOMEGA, DCGOMG,
        DOMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        You can use the CMDOMEGA command in conjunction with any one of the
        following two groups of commands, but not with both groups
        simultaneously:

        Components for which you want to specify rotational loading must
        consist of elements only. The elements you use cannot be part of more
        than one component, and elements that share nodes cannot exist in
        different element components. You cannot apply the loading to an
        assembly of element components.

        In a modal harmonic or transient analysis, you must apply the load in
        the modal portion of the analysis. Mechanical APDL calculates a load
        vector and writes it to the mode shape file, which you can apply via
        the LVSCALE command.

        See Acceleration Effect in the Mechanical APDL Theory Reference for
        more information.

        This command is also valid in PREP7.
        """
        command = f"CMDOMEGA,{cm_name},{domegax},{domegay},{domegaz},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def cmomega(
        self,
        cm_name="",
        omegax="",
        omegay="",
        omegaz="",
        x1="",
        y1="",
        z1="",
        x2="",
        y2="",
        z2="",
        **kwargs,
    ):
        """Specifies the rotational velocity of an element component about a user-

        APDL Command: CMOMEGA
        defined rotational axis.

        Parameters
        ----------
        cm_name
            The name of the element component.

        omegax, omegay, omegaz
            If the X2, Y2, Z2 fields are not defined, OMEGAX, OMEGAY, and
            OMEGAZ specify the components of the rotational velocity vector in
            the global Cartesian X, Y, Z directions.

        x1, y1, z1
            If the X2, Y2, Z2 fields are defined,X1, Y1, and Z1 define the
            coordinates of the beginning point of the rotational axis vector.
            Otherwise, X1, Y1, and Z1 are the coordinates of a point through
            which the rotational axis passes.

        x2, y2, z2
            The coordinates of the end point of the rotational axis vector.

        Notes
        -----
        Specifies the rotational velocity components OMEGAX, OMEGAY, and OMEGAZ
        of an element component CM_NAME about a user-defined rotational axis.
        The rotational axis can be defined either as a vector passing through a
        single point or a vector connecting two points.

        You can define rotational velocity and rotational axis for these
        analysis types:

        Static (ANTYPE,STATIC)

        Harmonic (ANTYPE,HARMIC) -- Full or modal superposition

        Transient (ANTYPE,TRANS)  -- Full or modal superposition

        Substructuring (ANTYPE,SUBSTR)

        Modal (ANTYPE,MODAL)

        Rotational velocities are combined with the element mass matrices to
        form a body force load vector term. Units are radians/time. Related
        commands are ACEL, CGLOC, CGLOC,  CGOMGA, CMDOMEGA, DCGOMG, DOMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        You can use the CMOMEGA command in conjunction with either one of the
        following two groups of commands, but not with both groups
        simultaneously:

        Components for which you want to specify rotational loading must
        consist of elements only. The elements you use cannot be part of more
        than one component, and elements that share nodes cannot exist in
        different element components. You cannot apply the loading to an
        assembly of element components.

        If you have applied the Coriolis effect (CORIOLIS) using a stationary
        reference frame, the CMOMEGA command takes the gyroscopic damping
        matrix into account for the elements listed under "Stationary Reference
        Frame" in the notes section of the CORIOLIS command. ANSYS verifies
        that the rotation vector axis is parallel to the axis of the element;
        if not, the gyroscopic effect is not applied. If you issue a CMOMEGA
        command when the Coriolis or gyroscopic effect is present, a
        subsequently issued OMEGA command has no effect.

        The CMOMEGA command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for CMOMEGA_X, CMOMEGA_Y, and CMOMEGA_Z
        input values (``*DIM``) for full transient and harmonic analyses.

        In a mode-superposition harmonic or transient analysis, you must apply
        the load in the modal portion of the analysis. Mechanical APDL
        calculates a load vector and writes it to the MODE file, which you can
        apply via the LVSCALE command.
        """
        command = f"CMOMEGA,{cm_name},{omegax},{omegay},{omegaz},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def cmrotate(
        self,
        cm_name="",
        rotatx="",
        rotaty="",
        rotatz="",
        x1="",
        y1="",
        z1="",
        x2="",
        y2="",
        z2="",
        **kwargs,
    ):
        """Specifies the rotational velocity of an element component in a brake

        APDL Command: CMROTATE
        squeal analysis.

        Parameters
        ----------
        cm_name
            The name of the element component.

        rotatx, rotaty, rotatz
            If the X2, Y2, Z2 fields are not defined, ROTATX, ROTATY, and
            ROTATZ specify the components of the rotational angle vector in the
            global Cartesian X, Y, Z directions.

        x1, y1, z1
            If the X2, Y2, Z2 fields are defined, X1, Y1, and Z1 define the
            coordinates of the beginning point of the rotational axis vector.
            Otherwise, X1, Y1, and Z1 are the coordinates of a point through
            which the rotational axis passes.

        x2, y2, z2
            The coordinates of the end point of the rotational axis vector.

        Notes
        -----
        The CMROTATE command specifies the rotational motion velocity
        components ROTATX, ROTATY, and ROTATZ of an element component CM_Name
        about a user-defined rotational axis. The rotational axis can be
        defined either as a vector passing through a single point or a vector
        connecting two points. CMROTATE can be used in static analyses
        (ANTYPE,STATIC) and modal analyses (ANTYPE,MODAL).

        This command sets the constant rotational velocity on the nodes of the
        specified element component, despite any deformation at the nodes. This
        feature is primarily used for generating sliding contact at frictional
        contact interfaces in a brake squeal analysis. This type of analysis
        typically involves surface-to-surface contact between the brake pad and
        the rotating disk. The applicable contact elements, therefore, are
        CONTA173, CONTA174, and CONTA175.

        A brake squeal analysis generally involves a linear perturbation modal
        analysis subsequent to a large-deformation static analysis with the
        Newton-Raphson option set as NROPT,UNSYM. Therefore, CMROTATE is not
        applicable for multiple load step solves using the LSSOLVE command.

        This command is also valid in PREP7.
        """
        command = f"CMROTATE,{cm_name},{rotatx},{rotaty},{rotatz},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def coriolis(self, option="", refframe="", rotdamp="", rotmass="", **kwargs):
        """Applies the Coriolis effect to a rotating structure.

        APDL Command: CORIOLIS

        Parameters
        ----------
        option : str, bool, optional
            Flag to activate or deactivate the Coriolis effect:

            ``"ON"``, ``"YES"``, or ``True`` - Activate. This value is the default.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate.

        refframe : str, bool, optional
            Flag to activate or deactivate a stationary reference frame.

            ``"ON"``, ``"YES"``, or ``True`` - Activate.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate. This value is the default.

        rotdamp : str, bool, optional
            Flag to activate or deactivate rotating damping effect.

            ``"ON"``, ``"YES"``, or ``True`` - Activate.

            ``"OFF"``, ``"NO"``, or ``False`` - Deactivate. This value is the default.

        rotmass : str, bool, optional
           Flag to activate or deactivate rotor mass summary printout
           (only supported for ``refframe='on'``).

           ``"ON"``, ``"YES"``, or ``True`` - Activate.

           ``"OFF"``, ``"NO"``, or ``False`` - Deactivate. This value is the default.

        Notes
        -----
        The CORIOLIS command is used for analyses in either a rotating
        or a stationary reference frame, and performs differently
        according to the designated RefFrame value. Specific
        restrictions and elements apply to each case, as follows:

        ROTATING REFERENCE FRAME ``refframe=False``):

        The command applies the Coriolis effect in the following
        structural element types: MASS21, SHELL181, PLANE182,
        PLANE183, SOLID185, SOLID186, SOLID187, BEAM188, BEAM189,
        SOLSH190, SHELL281, PIPE288 and PIPE289. It also applies this
        effect in the PLANE223, SOLID226, and SOLID227 analyses with
        structural degrees of freedom.

        In a rotating reference frame, both the Coriolis and
        spin-softening effects contribute to the gyroscopic
        moment. Therefore, ANSYS applies spin-softening by default for
        dynamic analyses. If a rotational velocity is specified (OMEGA
        or CMOMEGA), centrifugal forces will be included.

        To include Coriolis effects in a large deflection prestressed
        analysis, follow the procedure for linear perturbation
        detailed in Considerations for Rotating Structures. In a
        nonlinear transient analysis (ANTYPE,TRANS and NLGEOM, ON),
        any spinning motion applied through either the IC of the D
        commands will include the Coriolis effect without having to
        issue the CORIOLIS command. Refer to Rotating Structure
        Analysis in the Advanced Analysis Guide for more information.

        STATIONARY REFERENCE FRAME ``refframe=True``):

        The command activates the gyroscopic damping matrix in the
        following structural elements: MASS21, BEAM188, SHELL181,
        BEAM189, SOLID185, SOLID186, SOLID187, SOLID272, SOLID273,
        SHELL281, PIPE288, PIPE289, and MATRIX50.

        The rotating structure must be axisymmetric about the axis of
        rotation.

        Static analysis (ANTYPE, STATIC) does not support Coriolis
        effects with a stationary reference frame. However, you can
        include the gyroscopic effects in a prestresses analysis
        follow the procedure detailed in Considerations for Rotating
        Structures.

        Rotating damping effect (RotDamp = ON) applies only for the
        stationary reference frame. Therefore, this effect is
        supported only by the elements listed above that generate a
        gyroscopic damping matrix.  Proportional damping must be
        present in the element (MP,BETD or BETAD).  It is also
        supported by element COMBI214 with non zero and axisymmetric
        damping characteristics (non zero real constants C11=C22 and
        C21=C12=0).

        For more information about using the CORIOLIS command, see
        Rotating Structure Analysis in the Advanced Analysis Guide and
        also in the Rotordynamic Analysis Guide. For details about the
        Coriolis and gyroscopic effect element formulations, see the
        Mechanical APDL Theory Reference.

        Elements with layered section properties do not support
        Coriolis effects (rotating and stationary reference frames).

        This command is also valid in PREP7.

        Examples
        --------
        Enable the coriolis effect with a stationary reference frame.

        >>> mapdl.coriolis('ON', refframe='ON')

        Alternatively, ``coriolis`` supports bool parameters.

        >>> mapdl.coriolis(True, refframe=True)

        """
        # handle bool instead of strings
        if isinstance(option, bool):
            option = int(option)

        if isinstance(refframe, bool):
            refframe = int(refframe)

        if isinstance(rotdamp, bool):
            rotdamp = int(rotdamp)

        if isinstance(rotmass, bool):
            rotmass = int(rotdamp)

        command = f"CORIOLIS,{option},,,{refframe},{rotdamp},{rotmass}"
        return self.run(command, **kwargs)

    def dcgomg(self, dcgox="", dcgoy="", dcgoz="", **kwargs):
        """Specifies the rotational acceleration of the global origin.

        APDL Command: DCGOMG

        Parameters
        ----------
        dcgox, dcgoy, dcgoz
            Rotational acceleration of the global origin about the acceleration
            system X, Y, and Z axes.

        Notes
        -----
        Specifies the rotational acceleration of the global origin about each
        of the acceleration coordinate system axes [CGLOC].  Rotational
        accelerations may be defined in analysis types ANTYPE,STATIC, HARMIC
        (full or mode-superposition), TRANS (full or mode-superposition), and
        SUBSTR. See Acceleration Effect in the Mechanical APDL Theory Reference
        for details.  Units are radians/time2.

        The DCGOMG command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for DCGOMG_X, DCGOMG_Y, and DCGOMG_Z
        input values (``*DIM``) for full transient and harmonic analyses.

         Related commands are ACEL, CGLOC, CGOMGA, DOMEGA, and OMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        This command is also valid in PREP7.
        """
        command = f"DCGOMG,{dcgox},{dcgoy},{dcgoz}"
        return self.run(command, **kwargs)

    def domega(self, domgx="", domgy="", domgz="", **kwargs):
        """Specifies the rotational acceleration of the structure.

        APDL Command: DOMEGA

        Parameters
        ----------
        domgx, domgy, domgz
            Rotational acceleration of the structure about the global Cartesian
            X , Y, and Z axes.

        Notes
        -----
        Specifies the rotational acceleration of the structure about each of
        the global Cartesian axes.  Rotational accelerations may be defined in
        analysis types ANTYPE,STATIC, HARMIC (full or mode-superposition),
        TRANS (full or mode-superposition), and SUBSTR.  See Acceleration
        Effect in the Mechanical APDL Theory Reference for details.  Units are
        radians/time2.

        The DOMEGA command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for DOMEGA_X, DOMEGA_Y, and DOMEGA_Z
        input values (``*DIM``) for full transient and harmonic analyses.

        Related commands are ACEL, CGLOC, CGOMGA, DCGOMG, and OMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        In a modal harmonic or transient analysis, you must apply the load in
        the modal portion of the analysis. Mechanical APDL calculates a load
        vector and writes it to the mode shape file, which you can apply via
        the LVSCALE command.

        This command is also valid in PREP7.
        """
        command = f"DOMEGA,{domgx},{domgy},{domgz}"
        return self.run(command, **kwargs)

    def irlf(self, key="", **kwargs):
        """Specifies that inertia relief calculations are to be performed.

        APDL Command: IRLF

        Parameters
        ----------
        key
            Calculation key:

             0  - No inertia relief calculations.

             1  - Counterbalance loads with inertia relief forces.

            -1  - Precalculate masses for summary printout only (no inertia relief).

        Notes
        -----
        The IRLF command specifies that the program is to calculate
        accelerations to counterbalance the applied loads (inertia relief).
        Displacement constraints on the structure should be only those
        necessary to prevent rigid-body motions (3 are needed for a 2-D
        structure and 6 for a 3-D structure).  The sum of the reaction forces
        at the constraint points will be zero.  Accelerations are calculated
        from the element mass matrices and the applied forces.  Data needed to
        calculate the mass (such as density) must be input.  Both translational
        and rotational accelerations may be calculated.

        This option applies only to the static (ANTYPE,STATIC) analysis.
        Nonlinearities, elements that operate in the nodal coordinate system,
        and axisymmetric or generalized plane strain elements are not allowed.
        Symmetry models are not valid for inertia relief analysis. Models with
        both 2-D and 3-D element types are not recommended.

        Loads may be input as usual.  Displacements and stresses are calculated
        as usual.

        Use IRLIST to print inertia relief calculation results.  The mass and
        moment of inertia summary printed before the solution is accurate
        (because of the additional pre-calculations required for inertia
        relief).  See Inertia Relief in the Mechanical APDL Theory Reference
        for calculation details.  See also the Structural Analysis Guide for
        procedural details.

        If the inertia relief calculation is to be performed in the second or
        later load step, you must specify EMATWRITE,YES in the initial load
        step for the element matrices needed to perform the calculations to be
        available.

        When a superelement (MATRIX50) is present in the model, any DOF
        constraints that you need to apply (D) on a degree of freedom (DOF)
        belonging to the superelement must be applied in the use pass of the
        MATRIX50 element (not in the generation pass). The command has no
        effect in the generation pass of a substructure. In the expansion pass,
        precalculation of masses for summary printout (IRLF,-1) occurs only on
        elements that are part of the substructure.

        This command is also valid in PREP7.
        """
        command = f"IRLF,{key}"
        return self.run(command, **kwargs)

    def omega(self, omegx="", omegy="", omegz="", **kwargs):
        """Specifies the rotational velocity of the structure.

        APDL Command: OMEGA

        Parameters
        ----------
        omegx, omegy, omegz
            Rotational velocity of the structure about the global Cartesian X,
            Y, and Z axes.

        Notes
        -----
        This command specifies the rotational velocity of the structure about
        each of the global Cartesian axes (right-hand rule).  Rotational
        velocities may be defined in these analysis types:

        Static (ANTYPE,STATIC)

        Harmonic (ANTYPE,HARMIC) -- Full or mode-superposition

        Transient (ANTYPE,TRANS)  -- Full or mode-superposition

        Substructuring (ANTYPE,SUBSTR)

        Modal (ANTYPE,MODAL)

        The OMEGA command supports tabular boundary conditions (%TABNAME_X%,
        %TABNAME_Y%, and %TABNAME_Z%) for OMEGA_X, OMEGA_Y, and OMEGA_Z input
        values (``*DIM``) for full transient and harmonic analyses.

        Rotational velocities are combined with the element mass matrices to
        form a body force load vector term.  Units are radians/time.  Related
        commands are ACEL, CGLOC, CGOMGA, DCGOMG, and DOMEGA.

        See Analysis Tools in the Mechanical APDL Theory Reference for more
        information.

        If you have applied the Coriolis effect (CORIOLIS) using a stationary
        reference frame, the OMEGA command takes the gyroscopic damping matrix
        into account for the elements listed in the "Stationary Reference
        Frame" heading in the notes section of the CORIOLIS command. The
        element axis must pass through the global Cartesian origin. ANSYS
        verifies that the rotation vector axis is parallel to the axis of the
        element; if not, the gyroscopic effect is not applied. After issuing
        the OMEGA command when the Coriolis or gyroscopic effect is present, a
        subsequently issued CMOMEGA command has no effect.

        In a mode-superposition harmonic or transient analysis, you must apply
        the load in the modal portion of the analysis. Mechanical APDL
        calculates a load vector and writes it to the MODE file, which you can
        apply via the LVSCALE command.

        This command is also valid in PREP7.
        """
        command = f"OMEGA,{omegx},{omegy},{omegz}"
        return self.run(command, **kwargs)

    def synchro(self, ratio="", cname="", **kwargs):
        """Specifies whether the excitation frequency is synchronous or

        APDL Command: SYNCHRO
        asynchronous with the rotational velocity of a structure.

        Parameters
        ----------
        ratio
            The ratio between the frequency of excitation and the frequency of
            the rotational velocity of the structure. This value must be
            greater than 0. The default is an unbalance excitation (RATIO =
            1.0).

        cname
            The name of the rotating component on which to apply the harmonic
            excitation.

        Notes
        -----
        The SYNCHRO command specifies whether the excitation frequency is
        synchronous or asynchronous with the rotational velocity of a structure
        in a harmonic analysis. Use the command to take into account rotating
        harmonic forces on rotating structures.

        Mechanical APDL calculatestes the rotational velocity Ω of the
        structure from the excitation frequency f, defined (via the HARFRQ
        command) as Ω = 2πf / RATIO. The rotational velocity is applied along
        the direction cosines of the rotation axis (specified via an OMEGA or
        CMOMEGA command).

        Specifying any value for RATIO causes a general rotational force
        excitation and not an unbalance force. To define an unbalance
        excitation force (F = Ω2 * Unb), RATIO should be left blank (the nodal
        unbalance Unb is specified via the F command).

        The SYNCHRO command is valid only for a full-solution harmonic analysis
        (HROPT,Method = FULL) and the Variational Technology method
        (HROPT,Method = VT) involving a rotating structure (OMEGA or CMOMEGA)
        with Coriolis enabled in a stationary reference frame
        (CORIOLIS,,,,RefFrame = ON).
        """
        command = f"SYNCHRO,{ratio},{cname}"
        return self.run(command, **kwargs)
