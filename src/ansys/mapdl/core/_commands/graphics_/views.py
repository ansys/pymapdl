class Views:
    def angle(self, wn="", theta="", axis="", kincr="", **kwargs):
        """Rotates the display about an axis.

        APDL Command: /ANGLE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        theta
            Angle (degrees) for changing display orientation (positive,
            counterclockwise about specified axis).

        axis
            Rotation axis:  XS, YS, or ZS (default) for the screen axes;  XM,
            YM, or ZM for the global Cartesian model axes.  ZS is normal to the
            screen; all axes pass through the focus point.

        kincr
            Cumulative rotation key:

            0 - Do not use cumulative successive rotations.

            1 - Use cumulative rotations.  Rotations are relative to the previous rotation.
                View settings (/VIEW) are recalculated.

        Notes
        -----
        Default orientation is YS vertical. When the /XFRM command is set for
        rotation about two points, or for entities, the /ANGLE command is
        functional only for Axis = ZS or ZM and KINCR = 1.

        This command is valid in any processor.
        """
        command = f"/ANGLE,{wn},{theta},{axis},{kincr}"
        return self.run(command, **kwargs)

    def auto(self, wn="", **kwargs):
        """Resets the focus and distance specifications to "automatically

        APDL Command: /AUTO
        calculated."

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        Notes
        -----
        Focus point and distance will be automatically calculated during next
        display.  Settings may still be changed with the /FOCUS and /DIST
        commands after this command has been issued.  See also the /USER
        command.

        This command is valid in any processor.
        """
        command = f"/AUTO,{wn}"
        return self.run(command, **kwargs)

    def dist(self, wn="", dval="", kfact="", **kwargs):
        """Specifies the viewing distance for magnifications and perspective.

        APDL Command: /DIST

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        dval
            Distance along the view line from the observer to the focus point
            (defaults to value producing full-window display).  Distances "too
            close" to the object will produce excessive magnifications.  If
            DVAL = AUTO, zero, or blank, the program will calculate the
            distance automatically.  If DVAL = USER, the distance of last
            display will be used (useful when last display automatically
            calculated distance).

        kfact
            DVAL interpretation key:

            0 - Interpret numerical DVAL values as described above.

            1 - Interpret DVAL as a multiplier on the current distance (DVAL of 2 gives twice
                the current distance; 0.5 gives half the current distance,
                etc.).

        Notes
        -----
        The scale factor is relative to the window shape.  For example, for
        objects centered in a square window and with parallel projection (no
        perspective), a distance of :  /2 (+10%) produces a full window
        magnification, where :  is the largest in-plane vertical or horizontal
        dimension.  See also /AUTO and /USER commands.

        This command is valid in any processor.
        """
        command = f"/DIST,{wn},{dval},{kfact}"
        return self.run(command, **kwargs)

    def focus(self, wn="", xf="", yf="", zf="", ktrans="", **kwargs):
        """Specifies the focus point (center of the window).

        APDL Command: /FOCUS

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        xf, yf, zf
            Location of the object to be at the focus point (center of the
            window) in the global Cartesian coordinate system.  If XF = AUTO,
            allow automatic location calculation.  If XF = USER, use focus
            location of last display (useful when last display had auto focus).

        ktrans
            Translate key:

            0 - Interpret numerical XF, YF, ZF values as described above.

            1 - Interpret XF, YF, ZF values as multiples of half-screens to translate from the
                current position in the screen coordinate system.  Example: XF
                of 2.4 translates the display approximately 2.4 half-screens to
                the left in the screen X (horizontal) direction.

            2 - Interpret XF, YF, ZF values as multiples of half-screens to translate from the
                current position in the global Cartesian coordinate system.
                Example: XF of 1.5 translates the display approximately 1.5
                half-screens in the global Cartesian X direction of the model.

        Notes
        -----
        Specifies the location on (or off) the model which is to be located at
        the focus point (center of the window).  For section and capped
        displays, the cutting plane is also assumed to pass through this
        location (unless the working plane is used via /CPLANE).  See also
        /AUTO and /USER commands.

        This command is valid in any processor.
        """
        command = f"/FOCUS,{wn},{xf},{yf},{zf},{ktrans}"
        return self.run(command, **kwargs)

    def user(self, wn="", **kwargs):
        """Conveniently resets /FOCUS and /DIST to USER.

        APDL Command: /USER

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        Notes
        -----
        Conveniently resets scale parameters to USER on the /FOCUS and /DIST
        commands.  Scale parameters will be internally respecified to those
        used for the last display.  Convenient when the last scale parameters
        were automatically calculated.  User specified parameters hold until
        changed or removed [/AUTO].  Parameters may be reset on the individual
        commands after this command has been issued.

        This command is valid in any processor.
        """
        command = f"/USER,{wn}"
        return self.run(command, **kwargs)

    def vcone(self, wn="", phi="", **kwargs):
        """Defines the view cone angle for perspective displays.

        APDL Command: /VCONE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        phi
            View cone angle (0.0 to 85.°) to define perspective.  Use PHI =
            45.0° for typical perspective.   Increase angle for more
            perspective, decrease angle for less.  If the distance [/DIST] is
            not specified, it will be automatically calculated to give full
            window magnification.  If the distance is also specified, PHI
            controls both the perspective and the magnification.  The larger
            the angle, the more the perspective and the less the magnification.
            Defaults to 0.0 (no perspective).

        Notes
        -----
        Perspective shows the true depth of the object in the display.  A
        variable magnification results since the back plane of the object is
        further from the observer than the front plane.  The largest
        magnification occurs at the front plane.  With perspective, the
        magnification factor (MAGF) is not only a function of the distance from
        the object, but also the window shape and the perspective (or view
        cone) angle: Φ as follows:

        where , for square windows, is the largest in-plane vertical or
        horizontal dimension, d is the distance from the observer to the plane
        of:  (usually the front plane of the object), and: Φ is the view cone
        angle (defined with the /VCONE command).  The bigger the cone angle,
        the more the perspective.  The magnification factor proportionally
        decreases with increasing: Φ.  The distance can be defined with the
        /DIST or the /FOCUS command.  Note, the distance input on the /DIST
        command is equal to d only if the focus point is located on the plane
        of : .  It is recommended that if a general perspective is desired
        (i.e., not any specific cone angle), use Φ = 45.0 (since TAN(45.0) =
        1.0) and let the d value be automatically calculated for full window
        magnification.

        Note that any number of /DIST, /FOCUS, and /VCONE combinations can be
        used to produce the same magnification.  Distances less than the object
        depth will produce views from within the object.

        A magnification factor of 1.0 just fills the window.  If the automatic
        scaling option is used [/AUTO], the magnification factor is fixed at
        0.91 (to allow a 10% margin around the object) and d is automatically
        calculated for the given /VCONE and /FOCUS values.  Any value of Φ
        between 0.0 and 85.0 (usually 45.0) may be used to activate the
        perspective.  Views from inside the object are not possible when d is
        automatically calculated (use manual scaling [/USER] along with /DIST
        specification).

        This command is valid in any processor.
        """
        command = f"/VCONE,{wn},{phi}"
        return self.run(command, **kwargs)

    def view(self, wn="", xv="", yv="", zv="", **kwargs):
        """Defines the viewing direction for the display.

        APDL Command: /VIEW

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        xv, yv, zv
            The object is viewed along the line from point XV,YV,ZV (in the
            global coordinate system) to the global coordinate system origin.
            For section displays, the cutting plane is assumed to be
            perpendicular to this line.  If XV = WP, modify view to be normal
            to the currently defined working plane.  Defaults to (0,0,1).

        Notes
        -----
        The view line is always normal to the screen.  The view is selected by
        defining a point (in the global Cartesian coordinate system)
        representing a point along the viewing line.  This point, and the
        global Cartesian coordinate system origin, define the line along which
        the object is viewed while looking toward the origin.  Any point along
        the view line may be used, i.e., (1,1,1) and (2,2,2) give the same
        view.  The display orientation may be changed as desired [/ANGLE].  The
        display coordinate system type may be changed (from Cartesian to
        cylindrical, spherical, toroidal, etc.) with the DSYS command.

        This command is valid in any processor.
        """
        command = f"/VIEW,{wn},{xv},{yv},{zv}"
        return self.run(command, **kwargs)

    def vup(self, wn="", label="", **kwargs):
        """Specifies the global Cartesian coordinate system reference orientation.

        APDL Command: /VUP

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        label
            Orientation:

            * ``Y`` : Y vertical upward, X horizontal to the right, Z
              out from the screen (default).
            * ``-Y`` : Y vertical downward, X horizontal to the left,
              Z out from the screen.
            * ``X`` : X vertical upward, Y horizontal to the left, Z
              out from the screen.
            * ``-X`` : X vertical downward, Y horizontal to the right,
              Z out from the screen.
            * ``Z`` : Z vertical upward, Y horizontal to the right, X
              out from the screen.  With this choice, you should use a
              view other than the /VIEW default of (0,0,1).
            * ``-Z`` : Z vertical downward, Y horizontal to the left,
              X out from the screen.  With this choice, you should use
              a view other than the /VIEW default of (0,0,1).

        Notes
        -----
        Specifies the global Cartesian coordinate system reference orientation.
        The /VIEW and /ANGLE commands may be used to reorient the view and are
        relative to this reference orientation.  All coordinate systems are
        right-handed.

        This command is valid in any processor.
        """
        command = f"/VUP,{wn},{label}"
        return self.run(command, **kwargs)

    def xfrm(self, lab="", x1="", y1="", z1="", x2="", y2="", z2="", **kwargs):
        """Controls the centroid or the axis of dynamic rotation.

        APDL Command: /XFRM

        Parameters
        ----------
        lab
            The location or entity (centroid) used to define the center or axis
            of rotation.

            NODE - If NODE is chosen for the center of rotation, the node number will be X1. If
                   the rotation is to be about an axis, then X1 and Y1 define
                   the two nodes between which a line is drawn to determine the
                   axis. The remaining arguments are ignored.

            ELEMENT - If ELEMENT is chosen for the center of rotation, the element number will be X1.
                      If the rotation is to be about an axis, then X1 and Y1
                      define the two elements between which a line is drawn to
                      determine the axis. The remaining arguments are ignored.

            KP - If KP is chosen for the center of rotation, the keypoint number will be X1. If
                 the rotation is to be about an axis, then X1 and Y1 define the
                 two keypoints between which a line is drawn to determine the
                 axis.  The remaining arguments are ignored.

            LINE - If LINE is chosen for the center of rotation, the line number will be X1. If
                   the rotation is to be about an axis, then X1 and Y1 define
                   the two lines between which a line is drawn to determine the
                   axis. The remaining arguments are ignored.

            AREA - If AREA is chosen for the center of rotation, the area number will be X1. If
                   the rotation is to be about an axis, then X1 and Y1 define
                   the two areas between which a line is drawn to determine the
                   axis. The remaining arguments are ignored.

            VOLUME - If VOLUME is chosen for the center of rotation, the volume number will be X1.
                     If the rotation is to be about an axis, then X1 and Y1
                     define the two volumes between which a line is drawn to
                     determine the axis. The remaining arguments are ignored.

            XYZ - If XYZ is chosen for the center of rotation, the location of that center is
                  determined by the coordinates X1, Y1, Z1. If values are
                  specified for X2, Y2, Z2, then the axis of rotation will be
                  about the line between those two points.

            OFF - If LAB = OFF, DEFAULT, FOCUS or if no value is specified, then the center of
                  rotation is set at the FOCUS point, as defined by the /FOCUS
                  command.

        x1
            The entity number or X coordinate for the center of rotation.

        y1
            The entity number or Y coordinate for the center of rotation.

        z1
            The Z coordinate for the center of rotation.

        x2
            The X coordinate for the axis of rotation.

        y2
            The Y coordinate for the axis of rotation.

        z2
            The Z coordinate for the axis of rotation.

        Notes
        -----
        The /XFRM command is active only when the cumulative rotation key is
        specified ON for the /ANGLE command (KINCR = 1). This command affects
        dynamic manipulations only.

        For center rotation, the middle mouse button will rotate the model
        about the screen Z axis and the right mouse button will rotate the
        model about the screen X and Y axis.

        For rotation about an axis, the middle mouse button will rotate the
        model about the defined axis of rotation and the right mouse button
        will be deactivated.

        This command is valid in any processor.
        """
        command = f"/XFRM,{lab},{x1},{y1},{z1},{x2},{y2},{z2}"
        return self.run(command, **kwargs)

    def zoom(self, wn="", lab="", x1="", y1="", x2="", y2="", **kwargs):
        """Zooms a region of a display window.

        APDL Command: /ZOOM

        Parameters
        ----------
        wn
            Window number to which command applies (defaults to 1).

        lab
            Label to define the desired type of zoom:

            OFF - Turns zoom off (refits image of entire model to the window).

            BACK - Goes back to previous zoom setting (five successive back ups, maximum).

            SCRN - Interprets X1,Y1 as the screen coordinates of the center of a square zoom
                   region; X2,Y2 as the screen coordinates of a point on one
                   side of that square.

            RECT - Interprets X1,Y1 and X2,Y2 as the screen coordinates of two opposite corners of
                   a rectangular zoom region.

        Notes
        -----
        Zooms (centers and magnifies) the specified region of a display window.
        /ZOOM will operate on a display that has been formed by an explicit
        graphics action command (APLOT, EPLOT, etc.).  /ZOOM has no effect on
        an "immediate" graphics display.  When /ZOOM is executed, the display
        is automatically replotted such that the specified zoom region is
        centered and sized to fill the window.

        Auto resizing is disabled when you issue the /ZOOM command.  To restore
        auto resizing, issue the  /AUTO command, or select FIT from the Pan,
        Zoom, Rotate box.

        This command is valid in any processor.
        """
        command = f"/ZOOM,{wn},{lab},{x1},{y1},{x2},{y2}"
        return self.run(command, **kwargs)
