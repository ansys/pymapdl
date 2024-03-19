"""These DATABASE commands define and manipulate coordinate systems."""


class CoordinateSystem:
    def clocal(
        self,
        kcn="",
        kcs="",
        xl="",
        yl="",
        zl="",
        thxy="",
        thyz="",
        thzx="",
        par1="",
        par2="",
        **kwargs,
    ):
        """Defines a local coordinate system relative to the active coordinate

        APDL Command: CLOCAL
        system.

        Parameters
        ----------
        kcn
            Arbitrary reference number assigned to this coordinate system.
            Must be greater than 10.  A coordinate system previously defined
            with this number will be redefined.

        kcs
            Coordinate system type:

            0 or CART - Cartesian

            1 or CYLIN - Cylindrical (circular or elliptical)

            2 or SPHE - Spherical (or spheroidal)

            3 or TORO - Toroidal

        xl, yl, zl
            Location (in the active coordinate system) of the origin of the new
            coordinate system (R, θ, Z for cylindrical, R, θ,Φ for spherical or
            toroidal).

        thxy
            First rotation about local Z (positive X toward Y).

        thyz
            Second rotation about local X (positive Y toward Z).

        thzx
            Third rotation about local Y (positive Z toward X).

        par1
            Used for elliptical, spheroidal, or toroidal systems.  If KCS = 1
            or 2, PAR1 is the ratio of the ellipse Y-axis radius to X-axis
            radius (defaults to 1.0 (circle)).  If KCS = 3, PAR1 is the major
            radius of the torus.

        par2
            Used for spheroidal systems.  If KCS = 2, PAR2 = ratio of ellipse
            Z-axis radius to X-axis radius (defaults to 1.0 (circle)).

        Notes
        -----
        Defines and activates a local coordinate system by origin location and
        orientation angles relative to the active coordinate system.  This
        local system becomes the active coordinate system, and is automatically
        aligned with the active system (i.e., x is radial if a cylindrical
        system is active, etc.).  Nonzero rotation angles (degrees) are
        relative to this automatic rotation.  See the CS, CSKP, CSWPLA, and
        LOCAL commands for alternate definitions.  Local coordinate systems may
        be displayed with the /PSYMB command.

        This command is valid in any processor.
        """
        command = "CLOCAL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(kcn),
            str(kcs),
            str(xl),
            str(yl),
            str(zl),
            str(thxy),
            str(thyz),
            str(thzx),
            str(par1),
            str(par2),
        )
        return self.run(command, **kwargs)

    def cs(
        self, kcn="", kcs="", norig="", nxax="", nxypl="", par1="", par2="", **kwargs
    ):
        """Defines a local coordinate system by three node locations.

        APDL Command: CS

        Parameters
        ----------
        kcn
            Arbitrary reference number assigned to this coordinate system.
            Must be greater than 10.  A coordinate system previously defined
            with this number will be redefined.

        kcs
            Coordinate system type:

            0 or CART - Cartesian

            1 or CYLIN - Cylindrical (circular or elliptical)

            2 or SPHE - Spherical (or spheroidal)

            3 or TORO - Toroidal

        norig
            Node defining the origin of this coordinate system.  If NORIG = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        nxax
            Node defining the positive x-axis orientation of this coordinate
            system.

        nxypl
            Node defining the x-y plane (with NORIG and NXAX) in the first or
            second quadrant of this coordinate system.

        par1
            Used for elliptical, spheroidal, or toroidal systems.  If KCS = 1
            or 2, PAR1 is the ratio of the ellipse Y-axis radius to X-axis
            radius (defaults to 1.0 (circle)).  If KCS  = 3, PAR1 is the major
            radius of the torus.

        par2
            Used for spheroidal systems.  If KCS = 2, PAR2 = ratio of ellipse
            Z-axis radius to X-axis radius (defaults to 1.0 (circle)).

        Notes
        -----
        Defines and activates a local right-handed coordinate system by
        specifying three existing nodes: to locate the origin, to locate the
        positive x-axis, and to define the positive x-y plane.  This local
        system becomes the active coordinate system.  See the CLOCAL, CSKP,
        CSWPLA, and LOCAL commands for alternate definitions.  Local coordinate
        systems may be displayed with the /PSYMB command.

        This command is valid in any processor.
        """
        command = "CS,%s,%s,%s,%s,%s,%s,%s" % (
            str(kcn),
            str(kcs),
            str(norig),
            str(nxax),
            str(nxypl),
            str(par1),
            str(par2),
        )
        return self.run(command, **kwargs)

    def cscir(self, kcn="", kthet="", kphi="", **kwargs):
        """Locates the singularity for non-Cartesian local coordinate systems.

        APDL Command: CSCIR

        Parameters
        ----------
        kcn
            Number of the local coordinate system in which singularity location
            is to be changed.  Must be greater than 10.

        kthet
            Theta singularity location for cylindrical, spherical, and toroidal
            systems:

            0 - Singularity at ±180°.

            1 - Singularity at 0° (360°).

        kphi
            Phi singularity location for toroidal systems:

            0 - Singularity in phi direction at ±180°.

            1 - Singularity in phi direction at 0° (360°).

        Notes
        -----
        Continuous closed surfaces (circles, cylinders, spheres, etc.) have a
        singularity (discontinuity) at θ = ±180°. For local cylindrical,
        spherical, and toroidal coordinate systems, this singularity location
        may be changed to 0° (360°).

        An additional, similar singularity occurs in the toroidal coordinate
        system at: Φ = ±180° and can be moved with KPHI.  Additional
        singularities occur in the spherical coordinate system at: Φ = ±90°,
        but cannot be moved.

        This command is valid in any processor.
        """
        command = "CSCIR,%s,%s,%s" % (str(kcn), str(kthet), str(kphi))
        return self.run(command, **kwargs)

    def csdele(self, kcn1="", kcn2="", kcinc="", **kwargs):
        """Deletes local coordinate systems.

        APDL Command: CSDELE

        Parameters
        ----------
        kcn1, kcn2, kcinc
            Delete coordinate systems from KCN1 (must be greater than 10) to
            KCN2 (defaults to KCN1) in steps of KCINC (defaults to 1).  If KCN1
            = ALL, KCN2 and KCINC are ignored and all coordinate systems are
            deleted.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "CSDELE,%s,%s,%s" % (str(kcn1), str(kcn2), str(kcinc))
        return self.run(command, **kwargs)

    def cskp(
        self, kcn="", kcs="", porig="", pxaxs="", pxypl="", par1="", par2="", **kwargs
    ):
        """Defines a local coordinate system by three keypoint locations.

        APDL Command: CSKP

        Parameters
        ----------
        kcn
            Arbitrary reference number assigned to this coordinate system.
            Must be greater than 10.  A coordinate system previously defined
            with this number will be redefined.

        kcs
            Coordinate system type:

            0 or CART - Cartesian

            1 or CYLIN - Cylindrical (circular or elliptical)

            2 or SPHE - Spherical (or spheroidal)

            3 or TORO - Toroidal

        porig
            Keypoint defining the origin of this coordinate system.  If PORIG =
            P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        pxaxs
            Keypoint defining the positive x-axis orientation of this
            coordinate system.

        pxypl
            Keypoint defining the x-y plane (with PORIG and PXAXS) in the first
            or second quadrant of this coordinate system.

        par1
            Used for elliptical, spheroidal, or toroidal systems.  If KCS = 1
            or 2, PAR1 is the ratio of the ellipse Y-axis radius to X-axis
            radius (defaults to 1.0 (circle)).  If KCS = 3, PAR1 is the major
            radius of the torus.

        par2
            Used for spheroidal systems.  If KCS = 2, PAR2 = ratio of ellipse
            Z-axis radius to X-axis radius (defaults to 1.0 (circle)).

        Notes
        -----
        Defines and activates a local right-handed coordinate system by
        specifying three existing keypoints: to locate the origin, to locate
        the positive x-axis, and to define the positive x-y plane.  This local
        system becomes the active coordinate system.  See the CLOCAL, CS,
        CSWPLA, and LOCAL commands for alternate definitions.  Local coordinate
        systems may be displayed with the /PSYMB command.

        This command is valid in any processor.
        """
        command = "CSKP,%s,%s,%s,%s,%s,%s,%s" % (
            str(kcn),
            str(kcs),
            str(porig),
            str(pxaxs),
            str(pxypl),
            str(par1),
            str(par2),
        )
        return self.run(command, **kwargs)

    def cslist(self, kcn1="", kcn2="", kcinc="", **kwargs):
        """Lists coordinate systems.

        APDL Command: CSLIST

        Parameters
        ----------
        kcn1, kcn2, kcinc
            List coordinate systems from KCN1 to KCN2 (defaults to KCN1) in
            steps of KCINC (defaults to 1).  If KCN1 = ALL (default), KCN2 and
            KCINC are ignored and all coordinate systems are listed.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "CSLIST,%s,%s,%s" % (str(kcn1), str(kcn2), str(kcinc))
        return self.run(command, **kwargs)

    def cswpla(self, kcn="", kcs="", par1="", par2="", **kwargs):
        """Defines a local coordinate system at the origin of the working plane.

        APDL Command: CSWPLA

        Parameters
        ----------
        kcn
            Arbitrary reference number assigned to this coordinate system.
            Must be greater than 10.  A coordinate system previously defined
            with this number will be redefined.

        kcs
            Coordinate system type:

            0 or CART - Cartesian

            1 or CYLIN - Cylindrical (circular or elliptical)

            2 or SPHE - Spherical (or spheroidal)

            3 or TORO - Toroidal

        par1
            Used for elliptical, spheroidal, or toroidal systems.  If KCS = 1
            or 2, PAR1 is the ratio of the ellipse Y-axis radius to X-axis
            radius (defaults to 1.0 (circle)).  If KCS = 3, PAR1 is the major
            radius of the torus.

        par2
            Used for spheroidal systems.  If KCS = 2, PAR2 = ratio of ellipse
            Z-axis radius to X-axis radius (defaults to 1.0 (circle)).

        Notes
        -----
        Defines and activates a local right-handed coordinate system centered
        at the origin of the working plane.  The coordinate system's local x-y
        plane (for a Cartesian system) or R-θ plane (for a cylindrical or
        spherical system) corresponds to the working plane.  This local system
        becomes the active coordinate system.  See the CS, LOCAL, CLOCAL, and
        CSKP commands for alternate ways to define a local coordinate system.
        Local coordinate systems may be displayed with the /PSYMB command.

        This command is valid in any processor.
        """
        command = "CSWPLA,%s,%s,%s,%s" % (
            str(kcn),
            str(kcs),
            str(par1),
            str(par2),
        )
        return self.run(command, **kwargs)

    def csys(self, kcn="", **kwargs):
        """Activates a previously defined coordinate system.

        APDL Command: CSYS

        Parameters
        ----------
        kcn
            Specifies the active coordinate system, as follows:

            0 (default) - Cartesian

            1 - Cylindrical with global Cartesian Z as the axis of rotation

            2 - Spherical

            4 or WP - Working Plane

            5 - Cylindrical with global Cartesian Y as the axis of rotation

            11 or greater - Any previously defined local coordinate system

        Notes
        -----
        The CSYS command activates a previously defined coordinate system for
        geometry input and generation.  The LOCAL, CLOCAL, CS, CSKP, and CSWPLA
        commands also activate coordinate systems as they are defined. To set
        the active element coordinate system attribute pointer, issue the ESYS
        command.

        The active coordinate system for files created via the CDWRITE command
        is Cartesian

        >>> mapdl.csys(0)

        This command is valid in any processor.

        >>> mapdl.csys(4)
        >>> # or
        >>> mapdl.csys('WP')

        activates working plane tracking, which updates the
        coordinate system to follow working plane changes. To deactivate
        working plane tracking, activate any other coordinate system.

        >>> mapdl.csys(5)

        is a cylindrical coordinate system with global Cartesian Y as
        the axis. The local x, y and z axes are radial, θ, and axial
        (respectively). The R-Theta plane is the global X-Z plane, as it is for
        an axisymmetric model. Thus, at `θ = 0.0`, `mapdl.csys(5)` has a specific
        orientation: the local x is in the global +X direction, local y is in
        the global -Z direction, and local z (the cylindrical axis) is in the
        global +Y direction.

        Examples
        --------
        Create a cylindrical surface in cylindrical y (CSYS=5) with
        a radius of 6 and spanning `30 < θ < -90` and `0 < z < 4`.

        >>> mapdl.csys(5)
        >>> mapdl.k(1, 6, 30)
        >>> mapdl.k(2, 6, -90)
        >>> mapdl.k(3, 6, -90, 4)
        >>> mapdl.k(4, 6, 30, 4)
        >>> mapdl.a(1, 2, 3, 4)
        >>> mapdl.aplot()

        """
        command = "CSYS,%s" % (str(kcn))
        return self.run(command, **kwargs)

    def local(
        self,
        kcn="",
        kcs="",
        xc="",
        yc="",
        zc="",
        thxy="",
        thyz="",
        thzx="",
        par1="",
        par2="",
        **kwargs,
    ):
        """Defines a local coordinate system by a location and orientation.

        APDL Command: LOCAL

        Parameters
        ----------
        kcn
            Arbitrary reference number assigned to this coordinate system.
            Must be greater than 10.  A coordinate system previously defined
            with this number will be redefined.

        kcs
            Coordinate system type:

            0 or CART - Cartesian

            1 or CYLIN - Cylindrical (circular or elliptical)

            2 or SPHE - Spherical (or spheroidal)

            3 or TORO - Toroidal

        xc, yc, zc
            Location (in the global Cartesian coordinate system) of the origin
            of the new coordinate system.

        thxy
            First rotation about local Z (positive X toward Y).

        thyz
            Second rotation about local X (positive Y toward Z).

        thzx
            Third rotation about local Y (positive Z toward X).

        par1
            Used for elliptical, spheroidal, or toroidal systems.  If KCS = 1
            or 2, PAR1 is the ratio of the ellipse Y-axis radius to X-axis
            radius (defaults to 1.0 (circle)).  If KCS = 3, PAR1 is the major
            radius of the torus.

        par2
            Used for spheroidal systems.  If KCS = 2, PAR2 = ratio of ellipse
            Z-axis radius to X-axis radius (defaults to 1.0 (circle)).

        Notes
        -----
        Defines a local coordinate system by origin location and orientation
        angles.  The local coordinate system is parallel to the global
        Cartesian system unless rotated.  Rotation angles are in degrees and
        redefine any previous rotation angles.  See the CLOCAL, CS, CSWPLA, and
        CSKP commands for alternate definitions.  This local system becomes the
        active coordinate system [CSYS].  Local coordinate systems may be
        displayed with the /PSYMB command.

        This command is valid in any processor.
        """
        command = "LOCAL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(kcn),
            str(kcs),
            str(xc),
            str(yc),
            str(zc),
            str(thxy),
            str(thyz),
            str(thzx),
            str(par1),
            str(par2),
        )
        return self.run(command, **kwargs)
