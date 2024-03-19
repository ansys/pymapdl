class Labelling:
    def cformat(self, nfirst="", nlast="", **kwargs):
        """Controls the graphical display of alphanumeric character strings for

        APDL Command: /CFORMAT
        parameters, components, assemblies, and tables.

        Parameters
        ----------
        nfirst
            Display the first n characters of the parameter, component,
            assembly, or table name, up to 32. Defaults to 32.

        nlast
            Display the last n characters of the parameter, component,
            assembly, or table name, up to 32. Defaults to 0.

        Notes
        -----
        Use this command to control the length of the character string that is
        shown in the graphics window for a parameter, component, assembly, or
        table name.

        The total number of characters (NFIRST + NLAST +3) cannot exceed 32.

        If NFIRST is greater than zero and NLAST = 0, only the NFIRST
        characters are displayed, followed by an ellipsis.

        If NFIRST = 0 and NLAST is greater than zero, only the NLAST characters
        are displayed, preceded by an ellipsis (...).

        If both NFIRST and NLAST are greater than zero, the name will be shown
        as NFIRST, followed by an ellipsis (...), followed by NLAST, up to a
        maximum of 32 characters.

        For example, if NFIRST = 6 and NLAST = 3, and the character string is
        LENGTHOFSIDEONE, then it will appear in the graphics window as
        LENGTH...ONE.

        If the actual length of the character string is less than the specified
        combination of NFIRST + NLAST +3, then the actual string will be used.

        This command is valid in any processor.
        """
        command = f"/CFORMAT,{nfirst},{nlast}"
        return self.run(command, **kwargs)

    def clabel(self, wn="", key="", **kwargs):
        """Specifies contour labeling.

        APDL Command: /CLABEL

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        key
            Labeling key:

            0 or 1 - Label contours with legend or color (default).

            -1 - No contour labeling.

            N - Same as 1 except show alphabetic legend only on every Nth element.

        Notes
        -----
        Labels contours for identification with alphabetic legend for vector
        displays and color for raster displays.  Number of contours is
        automatically reduced to 9 (or fewer) for clarity.  Use /CONTOUR
        command to increase (24 maximum for alphabetic labeling; no limit for
        color labeling).

        This command is valid in any processor.
        """
        command = f"/CLABEL,{wn},{key}"
        return self.run(command, **kwargs)

    def contour(self, wn="", ncont="", vmin="", vinc="", vmax="", **kwargs):
        """Specifies the uniform contour values on stress displays.

        APDL Command: /CONTOUR

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        ncont
            Number of contour values. NCONT defaults to 9 for X11 or WIN32 and
            to 128 for X11c or WIN32C.  The default graphics window display for
            3-D devices is a smooth continuous shading effect that spans the
            maximum of 128 contours available. Use the /DV3D command to create
            defined banding for your contour values (values of 9 and 128 are
            displayed in smooth shading only). The legend, however, will
            display only nine color boxes, which span the full range of colors
            displayed in the graphics window.

        vmin
            Minimum contour value.  If VMIN = AUTO, automatically calculate
            contour values based upon NCONT uniformly spaced values over the
            min-max extreme range.  Or, if VMIN = USER, set contour values to
            those of the last display (useful when last display automatically
            calculated contours).

        vinc
            Value increment (positive) between contour values.  Defaults to
            (VMAX-VMIN)/NCONT.

        vmax
            Maximum contour value.  Ignored if both VMIN and VINC are
            specified.

        Notes
        -----
        See the /CVAL command for alternate specifications.  Values represent
        contour lines in vector mode, and the algebraic maximum of contour
        bands in raster mode.

        Note:: : No matter how many contours (NCONT) are specified by /CONTOUR,
        the actual number of contours that appear on your display depends also
        on the device name, whether the display is directed to the screen or to
        a file, the display mode (vector or raster), and the number of color
        planes.  (All these items are controlled by /SHOW settings.) In any
        case, regardless of whether they are smoothed or banded, only 128
        contours can be displayed. See Creating Geometric Results Displays in
        the Basic Analysis Guide for more information on changing the number of
        contours.

        If the current ANSYS graphics are not displayed as Multi-Plots, then
        the following is true:  If the current device is a 3-D device
        [/SHOW,3D], the model contours in all active windows will be the same,
        even if separate /CONTOUR commands are issued for each active window.
        For efficiency, ANSYS 3-D graphics logic maintains a single data
        structure (segment), which contains precisely one set of contours.  The
        program displays the same segment in all windows.  The view settings of
        each window constitute the only differences in the contour plots in the
        active windows.

        This command is valid in any processor.
        """
        command = f"/CONTOUR,{wn},{ncont},{vmin},{vinc},{vmax}"
        return self.run(command, **kwargs)

    def cval(
        self,
        wn="",
        v1="",
        v2="",
        v3="",
        v4="",
        v5="",
        v6="",
        v7="",
        v8="",
        **kwargs,
    ):
        """Specifies nonuniform contour values on stress displays.

        APDL Command: /CVAL

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        v1, v2, v3, . . . , v8
            Up to 8 contour values may be specified (in ascending order).  The
            0.0 value (if any) must not be the last value specified.  If no
            values are specified, all contour specifications are erased and
            contours are automatically calculated.

        Notes
        -----
        This command is similar to the /CONTOUR command. With /CVAL, however,
        you define the upper level of each contour band instead of having the
        contours uniformly distributed over the range. The minimum value
        (including a zero value for the first band) for a contour band cannot
        be specified. If you use both /CONTOUR and /CVAL, the last command
        issued takes precedence.

        This command is valid in any processor.
        """
        command = f"/CVAL,{wn},{v1},{v2},{v3},{v4},{v5},{v6},{v7},{v8}"
        return self.run(command, **kwargs)

    def gformat(self, ftype="", nwidth="", dsignf="", **kwargs):
        """Specifies the format for the graphical display of numbers.

        APDL Command: /GFORMAT

        Parameters
        ----------
        ftype
            FORTRAN format types (G is the default if this field is left
            blank.)

            G - Gxx.yy.  xx and yy are described below.

            F - Fxx.yy

            E - Exx.yy

        nwidth
            Total width (12 maximum) of the field (the xx in Ftype).  Defaults
            to 12.

        dsignf
            Number of digits after the decimal point (yy in F or E format) or
            number of significant digits in G format.  Range is 1 to xx-6 for
            Ftype = G or E; and 0 to xx-3 for Ftype = F.  The default is a
            function of Ftype and NWIDTH.

        Notes
        -----
        Lets you control the format of the graphical display of floating point
        numbers.   Issue /GFORMAT,STAT to display the current settings; issue
        /GFORMAT,DEFA to let ANSYS choose the format for the graphical display
        of floating numbers.

        This command is valid in any processor.
        """
        command = f"/GFORMAT,{ftype},{nwidth},{dsignf}"
        return self.run(command, **kwargs)

    def hbc(self, wn="", key="", **kwargs):
        """Determines how boundary condition symbols are displayed in a display

        APDL Command: /HBC
        window.

        Parameters
        ----------
        wn
            Window reference number. This number can be any window numbered 1
            to 5, or ALL (for all active windows). Defaults to 1

        key
            Key to enable/disable hidden surface boundary condition symbol
            display for 2-D graphics devices and to request improved pressure
            contour display for 2-D and 3-D devices: Key = ON, YES or 1 will
            show your BC symbols on the hidden surfaces and use an improved
            pressure contour display. Key = OFF, NO or 0 (default) will hide
            the symbols .
        """
        command = f"/HBC,{wn},{key}"
        return self.run(command, **kwargs)

    def number(self, nkey="", **kwargs):
        """Specifies whether numbers, colors, or both are used for displays.

        APDL Command: /NUMBER

        Parameters
        ----------
        nkey
            Numbering style:

            * ``0`` : Color (terminal dependent) the numbered items
              and show numbers.

            * ``1`` : Color the numbered items.  Do not show the
              numbers.

            * ``2`` : Show the numbers.  Do not color the items.

            * ``-1`` : Do not color the items or show the numbers. For
              contour plots, the resulting display will vary (see below).

        Notes
        -----
        Specifies whether numbers, colors, or both are used for numbering
        displays [/PNUM] of nodes, elements, keypoints, lines, areas, and
        volumes.

        Shading is also available for terminals configured with more than 4
        color planes [/SHOW].  Color automatically appears for certain items
        and may be manually controlled (off or on) for other items.

        When you suppress color (NKEY = -1) your contour plots will produce
        different results, depending on your graphics equipment. For non-3-D
        devices (X11, Win32, etc.) your contour plot will be white (no color).
        For 3-D devices, such as OpenGL, the resulting display will be in
        color.

        The following items are automatically given discrete colors:  Boundary
        condition symbols [/PBC], curves on graph displays, and distorted
        geometry on postprocessing displays.  Contour lines in postprocessing
        displays are automatically colored based upon a continuous, rather than
        a discrete, spectrum so that red is associated with the highest contour
        value.  On terminals with raster capability [/SHOW], the area between
        contour lines is filled with the color of the higher contour.

        Explicit entity colors or the discrete color mapping may be changed
        with the /COLOR command.

        This command is valid in any processor.
        """
        command = f"/NUMBER,{nkey}"
        return self.run(command, **kwargs)

    def pbc(self, item="", key="", min_="", max_="", abs_="", **kwargs):
        """Shows boundary condition (BC) symbols and values on displays.

        APDL Command: /PBC

        Parameters
        ----------
        item
            Label identifying the item:

            U - Applied translational constraints (UX, UY, UZ).

            ROT - Applied rotational constraints (ROTX, ROTY, ROTZ).

            TEMP - Applied temperatures (TEMP, TBOT, TE2, TE3, . . ., TTOP).

            PRES - Applied fluid pressures.

            V - Applied flow velocities (VX, VY, VZ).

            VOLT - Applied voltages.

            MAG - Applied scalar magnetic potentials.

            A - Applied vector magnetic potentials.

            CONC - Concentration.

            CHRG - Applied electric charge.

            F or FORC - Applied structural forces (FX, FY, FZ).

            M or MOME - Applied structural moments (MX, MY, MZ).

            HEAT - Applied heat flows (HEAT, HBOT, HE2, HE3, . . ., HTOP).

            FLOW - Applied fluid flow.

            AMPS - Applied current flow.

            FLUX - Applied magnetic flux.

            CSG - Applied magnetic current segments.

            RATE - Diffusion flow rate.

            MAST - Master degrees of freedom.

            CP - Coupled nodes.

            CE - Nodes in constraint equations.

            NFOR - POST1 nodal forces.

            NMOM - POST1 nodal moments

            RFOR - POST1 reaction forces.

            RMOM - POST1 reaction moments (MX, MY, MZ).

            PATH - Path geometry (undistorted) associated with the PATH command after a PDEF or
                   PVECT command has been issued.

            ACEL - Global acceleration (ACELX, ACELY, ACELZ vector).

            OMEG - Global angular velocity (OMEGX, OMEGY, OMEGZ vector) and acceleration (DOMEGX,
                   DOMEGY, DOMEGZ vector).

            WELD - Applied spotwelds (ANSYS LS-DYNA).

            ALL - Represents all appropriate labels.

        key
            Symbol key:

            0 - Do not show symbol.

            1 - Show symbol.

            2 - Plot value next to symbol.

        min\_
            Minimum value in a range of values plotted on screen.

        max\_
            Maximum value in a range of values plotted on screen.

        abs\_
            Absolute number.  If KEY = 2 and ABS = 0, a number falling between
            the MIN and MAX is displayed.  If ABS is not specified, it defaults
            to 0.  If KEY = 2 and ABS = 1, an absolute value falling between
            the MIN and MAX is displayed.   ABS = 1 lets you eliminate the
            display of numbers whose absolute values are less than a desired
            tolerance.  For example, if ABS = 1, MIN = 10 and MAX = 1e8, values
            such as .83646 and -5.59737 are not displayed.

        Notes
        -----
        The ``mapdl.pbc`` command adds degree of freedom constraint, force load, and
        other symbols to displays.

        Symbols are applied to the selected nodes only.  All arrow and
        arrowhead symbols are oriented in the nodal coordinate system and lie
        in two perpendicular planes.  Force arrows are scaled proportional to
        their magnitude. (If KEY =  1, use /VSCALE to change arrow length.)
        For scalar quantities, the specific component direction (i.e., x, y, or
        z) of the symbol has no meaning, but the positive or negative sense
        (e.g., positive or negative x) represents a positive or negative scalar
        value, respectively.

        The effects of the ``mapdl.pbc`` command are not cumulative (that is, the
        command does not modify an existing setting from a previously issued
        ``mapdl.pbc`` command).  If you issue multiple ``mapdl.pbc`` commands
        during an analysis, only the setting specified by the most recent
        ``mapdl.pbc`` command applies.

        Use ``mapdl.pstatus()`` or ``mapdl.pbc('STAT')`` to display settings.
        Use ``mapdl.pbc('DEFA')`` to reset all specifications back to default.
        See the ``mapdl.psf`` and ``mapdl.pbf`` commands for other display symbols.

        In a cyclic symmetry analysis, the ``mapdl.pbc`` command is deactivated when
        cyclic expansion is active (/CYCEXPAND,,ON). To view boundary
        conditions on the basic sector, deactivate cyclic expansion
        (/CYCEXPAND,,OFF) and issue this command: ``mapdl.pbc('ALL', 1)``

        Issuing the command ``mapdl.pbc('PATH', 1)`` displays all defined paths.

        The ``mapdl.pbc`` command is valid in any processor.

        .. note:
            In APDL the /PBC command has an unused 3rd argument. This has been
            removed in PyMAPDL because of its redundancy, and should be
            kept in mind when translating between the two.

        Examples
        --------
        On all subsequent plots (after this command). Activate display of
        translational boundary condition symbols.

        >>> mapdl.pbc('U', 1)

        Display enforced nodal temperatures

        >>> mapdl.pbc('TEMP', 1)
        """
        command = f"/PBC,{item},,{key},{min_},{max_},{abs_}"
        return self.run(command, **kwargs)

    def pbf(self, item="", key="", **kwargs):
        """Shows magnitude of body force loads on displays.

        APDL Command: /PBF

        Parameters
        ----------
        item
            Label identifying the item:

            TEMP - Applied temperatures.

            FLUE - Applied fluences.

            HGEN - Applied heat generation rates.

            JS - Applied current density magnitude.

            JSX - X-component of current density.

            JSY - Y-component of current density.

            JSZ - Z-component of current density.

            PHASE - Phase angle of applied load.

            MVDI - Applied magnetic virtual displacements flag.

            CHRGD - Applied electric charge density.

            VLTG - Applied voltage drop.

        key
            Symbol key:

            0 - Do not show body force load contours.

            1 - Show body force load contours.

            2 - Show current density as a vector (not a contour).

        Notes
        -----
        Shows body force loads as contours on displays for the selected
        elements.

        The effects of the ``mapdl.pbf`` command are not cumulative (that is, the
        command does not modify an existing setting from a previously issued
        ``mapdl.pbf`` command).  If you issue multiple ``mapdl.pbf`` commands
        during an analysis, only the setting specified by the most recent
        ``mapdl.pbf`` command applies.

        Use ``mapdl.pstatus()`` or ``mapdl.pbf('STAT')`` to display settings.
        Use ``mapdl.pbf('DEFA')`` to reset all specifications back to default.
        See also the ``mapdl.psf`` and ``mapdl.pbc`` command
        for other display contours.

        Portions of this command are not supported by PowerGraphics
        [``mapdl.graphics('POWER')``].

        This command is valid in any processor.

        .. note:
            In APDL the /PBF command has an unused 2nd argument. This has been
            removed in PyMAPDL because of its redundancy, and should be
            kept in mind when translating between the two.

        Examples
        --------
        Activate display of body loads of structural temperature on subsequent plots
        by showing body force and contours.

        >>> mapdl.pbf('TEMP', 1)
        """
        return self.run(f"/PBF,{item},,{key}", **kwargs)

    def plopts(self, label="", key="", **kwargs):
        """Controls graphics options on subsequent displays.

        APDL Command: /PLOPTS

        Parameters
        ----------
        label
            Apply display items as selected from the following labels:

            INFO - Controls the display of the legend (ON or OFF) and allows the choice of preset
                   or Multi-legend placement. Control is provided by the KEY
                   values. (Defaults to KEY=3 when the GUI is on. Defaults to
                   KEY= 2 otherwise.)

            LEG1 - Header portion of legend column (defaults to ON).

            LEG2 - View portion of legend column (defaults to ON (except off with contour
                   displays)).

            LEG3 - View the contour section of the legend column (defaults to ON).

            FRAME - Frame border lines around windows (defaults to ON).

            TITLE - Title (bottom left text) (defaults to ON).

            MINM - Min-Max symbols on contour displays (defaults to ON).

            LOGO - ANSYS logo (defaults to OFF (displayed as text at top of legend column)).  If
                   KEY = ON, the text is removed from legend column but the
                   logo symbol is displayed in whichever active window is
                   either in the uppermost right corner and on top, or if there
                   is no window in that location, then in the window to the
                   furthest right of the screen.  Version information remains
                   in the legend column.

            WINS - Controls whether graphics windows automatically stretch or shrink to adjust to
                   screen size as the legend column is turned off or on
                   [/PLOPTS,INFO] (defaults to ON).  If WINS is on and the
                   legend column is changed from off to on, all windows are
                   shrunk regardless of what their correct size is.

            WP - Working plane (defaults to OFF).  The working plane is drawn as part of the
                 display (not just an overlaid image as in WPSTYL).  This
                 option is best used in combination with a hidden-line
                 technique [/TYPE].

            DATE - Controls the display of the date and time in your legend. Subsequent KEY values
                   control the display as follows:

            FILE - Controls the display of the ANSYS jobname in your legend. Subsequent KEY values
                   control the display as follows:

        key
            Switch:

            OFF or 0 - Do not apply this display item. For Label = DATE, no time or date are
                       displayed.

            ON or 1 - Apply this display item. For Label = DATE, show only the date.

            AUTO or 2 - For Label = INFO, initiate Auto-legend mode.  If the display has contours, the
                        legend is ON; if the display has no contours, the
                        legend is OFF. For Label = DATE, display both the date
                        and time.

            3 - For Label = INFO , switch to Multi-legend mode. See the /UDOC command for the
                available legend configurations.

        Notes
        -----
        Use /PLOPTS,STAT to display settings.  Use /PLOPTS,DEFA to reset all
        specifications back to their defaults.

        When you perform multiple results displays, contours on the legend
        column may be truncated.  To avoid this, specify /PLOPTS,LEG1,0.

        The Multi-legend mode provides a number of legend data item priority
        and placement options. These options are accessed via the GUI at
        Utility Menu> PlotCtrls> Window Controls> Window Options. The /UDOC
        command provides command line options for this capability.

        This command is valid in any processor.

        This command is not available for Academic Research or Teaching level
        products
        """
        command = f"/PLOPTS,{label},{key}"
        return self.run(command, **kwargs)

    def pnum(self, label="", key="", **kwargs):
        """Controls entity numbering/coloring on plots.

        APDL Command: /PNUM

        Parameters
        ----------
        label
            Type of numbering/coloring:

            NODE - Node numbers on node and element plots.

            ELEM - Element numbers and colors on element plots.

            SEC - Section numbers and colors on element and solid model plots (see "Notes").

            MAT - Material set numbers and colors on element and solid model plots  (see
                  "Notes").

            TYPE - Element type reference numbers and colors on element and solid model plots (see
                   "Notes").

            REAL - Real constant set numbers and colors on element and solid model plots (see
                   "Notes").

            ESYS - Element coordinate system numbers on element and solid model plots (see
                   "Notes").

            PART - Element part numbers and colors on element plots (applicable to ANSYS LS-DYNA
                   only).

            LOC - Location numbers/colors of the element in matrix assembly order on element
                  plots.

            Note:LOC and ELEM numbers will be the same unless the model has been reordered. - KP

            Keypoint numbers on solid model plots. - LINE

            Line numbers on solid model plots (both numbers and colors on line plots). - AREA

            Area numbers on solid model plots (both numbers and colors on area plots). - VOLU

            Volume numbers on solid model plots (both numbers and colors on volume plots). - SVAL

            Stress (or any contour) values on postprocessing plots, and surface load values and colors on model plots (when surface load symbols are on [/PSF]).  For tabular boundary conditions, the table-evaluated values will be displayed on node, element, or contour displays in POST1 when load symbols (/PBF, /PSF, /PBC) are on and TABNAM is OFF. - TABNAM

            Table names for tabular boundary conditions.  If this label is turned on, the table name appears next to the appropriate symbol, arrow, face outline, or contour as dictated by the /PSF, /PBC, and /PBF commands. - STAT

            Shows current settings for /PNUM. - DEFA

        key
            Switch:

            0 - Turns OFF numbers/colors for specified label.

            1 - Turns ON numbers/colors for specified label.

        Notes
        -----
        This command specifies entity numbering and coloring for subsequent
        plots.

        The MAT, TYPE, REAL, and ESYS labels activate both the numbering and
        coloring of the corresponding attributes for  EPLOT, KPLOT, LPLOT,
        APLOT, and VPLOT. The ELEM, MAT, TYPE, REAL, ESYS, PART (ANSYS LS-DYNA
        only), and LOC labels are mutually exclusive, i.e., only one can be
        specified at a time. Also, turning on a LINE, AREA, or VOLU label will
        turn off the MAT, TYPE, REAL, and PART labels.

        PowerGraphics [/GRAPHICS,POWER] displays for/PNUM can be problematic.
        /PNUM,ELEM will display erratically depending on other display command
        specifications, while /PNUM,LOC and /PNUM,ESYS are not supported.

        Element and volume numbers are not visible for 3-D elements and volumes
        when Z-buffering is turned on (/TYPE,,[6,7, or 8]).

        Use /PSTATUS or /PNUM,STAT to show settings. Use /PNUM,DEFA to reset
        all specifications back to default. Use the /NUMBER command to control
        whether numbers and colors are displayed together.

        This command is valid in any processor
        """
        command = f"/PNUM,{label},{key}"
        return self.run(command, **kwargs)

    def psf(self, item="", comp="", key="", kshell="", color="", **kwargs):
        """Shows surface load symbols on model displays.

        APDL Command: /PSF

        Parameters
        ----------
        item, comp
            Labels identifying the surface load to be shown; see
            Table 227: /PSF - Valid Item and Component Labels.

        key
            Key to turn surface load symbols on or off:

            0 - Off (default).

            1 - On, shown as face outlines.  Line surface loads (SFL) on solid model plots are
                shown as arrows.

            2 - On, shown as arrows.

            3 - On, shown as color filled surfaces.  Line and area surface loads (SFL and SFA)
                on solid model plots are shown as arrows.

        kshell
            Visibility key for shell elements.

            0 - Off (default),  surface load symbols are displayed only on visible load faces.

            1 - On, surface load symbols are displayed even if load face is not visible.

        color
            Visibility key for contour legend.

            ON - The symbols (arrows or face outlines) will show up in color with the legend
                 showing the corresponding color labels (default).

            OFF - The contour legend will not be displayed. The symbols (arrows or face outlines)
                  will show up in grey. The size of the arrows will be
                  proportional to the applied load.

        Notes
        -----
        The ``mapdl.psf`` command determines whether and how to show surface loads on
        subsequent model displays.

        If surface loads are applied to solid model entities, only solid model
        plots show the load symbols; node and element plots do not show them
        unless the loads are transferred (SFTRAN or SBCTRAN).  Similarly, solid
        model plots do not show the load symbols if surface loads are applied
        to nodes and elements.  For node and element plots of shell element
        models, the surface load symbols are shown only if the load face is
        visible from the current viewing direction.

        The effects of the ``mapdl.psf`` command are not cumulative (that is, the
        command does not modify an existing setting from a previously issued
        ``mapdl.psf`` command).  Only the setting specified via the most recent
        ``mapdl.psf`` command applies.

        If you issue a postprocessing (``mapdl.post1``) plot command that produces result
        contours (such as PLNSOL), the ``mapdl.psf`` command has no effect. This
        behavior prevents conflicting contours in the graphics window.

        When using the radiosity method (Item = RDSF and Comp = ENCL) with Key
        = 2, the radiation arrows point outward from any element face. When
        using SURF154 with KEYOPT(2) = 1, set the Item to PRES and leave the
        Component Label blank.

        ``mapdl.psf('STAT')`` displays current ``mapdl.psf`` settings, and
        ``mapdl.psf('DEFA')`` resets them back to default.

        Other useful commands are ``mapdl.pnum('SVAL', 1)`` to show the values of the
        surface loads, ``mapdl.vscale()`` to change arrow lengths, and
        ``mapdl.pbc`` and ``mapdl.pbf`` to activate other load symbols.

        For beam elements, only the colors representing shear (GREEN) and
        normal (RED) pressures are displayed for the arrows. The color of these
        arrows does not correspond to the magnitudes in the contour legend. The
        length of these arrows does, however, correlate to the relative
        magnitude of the pressures.

        For elements SURF159, SOLID272, SOLID273, PIPE288 and PIPE289, the /PSF
        command is not available when displaying elements with shapes
        determined from the real constants or section definition (``mapdl.eshape``).
        For PIPE288 and PIPE289, only external loads applied via the
        ``mapdl.sfbeam`` command are displayed.

        This command is valid in any processor.

        Table: 227:: : /PSF - Valid Item and Component Labels

        Pressure loads apply to the element coordinate system (KEYOPT(2) = 0).
        Adjust appropriately for a local coordinate system (KEYOPT(2) = 1). See
        Figure: 153.2:: Pressures in the Element Reference.

        Examples
        --------
        On subsequent plots display the surface loads of pressure as arrows.

        >>> mapd.psf('PRES', '', 2)

        Activate display of convection on surfaces using the element outline option.

        >>> mapdl.psf('CONV', '', 1)
        """
        command = f"/PSF,{item},{comp},{key},{kshell},{color}"
        return self.run(command, **kwargs)

    def psymb(self, label="", key="", **kwargs):
        """Shows various symbols on displays.

        APDL Command: /PSYMB

        Parameters
        ----------
        label
            Show symbols as selected from the following labels:

            CS - Local coordinate systems.

            NDIR - Nodal coordinate systems (on rotated nodes only).

            ESYS - Element coordinate systems (element displays only).

            LDIR - Line directions (line displays only).

            LDIV - Controls the display of element divisions on lines.

            ADIR - Area direction symbol (for keypoint, line, area and volume plots).

            LAYR - Layer orientations (relative to the projected element x-axis) or fiber
                   orientations in smeared reinforcing elements. Used only
                   within an element display. Use KEY to specify the layer
                   number.

            ECON - Element mesh symbols on keypoints and lines.

            DOT - Larger symbols displayed for node and keypoint locations.  When Label = DOT,
                  KEY = 1 by default.

            XNOD - Extra node of surface or circuit elements.

            FBCS - Force boundary condition scaling. Subsequent KEY value determines whether or
                   not to scale the applied and derived forces/moments to the
                   same maximum value.

            DEFA - Resets the symbol keys so that ANSYS displays none of the symbols controlled by
                   the /PSYMB command.  The value of the KEY field is ignored.

            STAT - Prints the status of the settings of the symbol
                   keys controlled by the /PSYMB command.  The KEY
                   field is ignored.

        key
            Symbol key:

            ``-1`` - Effective only if Label = LAYR and solid shape
                  element display (/ESHAPE) is active. Orientation of
                  all layers appears with the solid shape element
                  display.

            0 - No symbol (default). If Label = LDIV, then KEY= 0
                 indicates that the displayed element divisions will
                 correspond to the existing mesh (the word MESHED or
                 EXISTING can also be substituted). Also, for Label =
                 LDIV, if you execute any meshing command (such as
                 AMESH or VMESH), KEY is set to 0 (MESHED)
                 automatically. If Label = FBCS, then KEY= 0 indicates
                 that boundary condition scaling will not be
                 common. The applied and derived forces/moments will
                 be scaled to their respective maximum values.

            1 - Include symbol. If Label = LDIV, then KEY = 1
                 indicates that the displayed line divisions will
                 correspond to the value assigned by LESIZE (the word
                 LESIZE can also be substituted). Also, for Label =
                 LDIV, if you execute the LESIZE command, KEY is set
                 to 1 (LESIZE) automatically. If Label = FBCS, then
                 KEY= 1 indicates that boundary condition scaling will
                 be common. The applied and derived forces/moments
                 will be scaled to the same maximum value.

            N - If Label = LAYR, then N is equal to the layer
                 number. If Label = DOT, then N can be equal to
                 0,1,.....15, indicating the dot size. If Label =
                 LDIV, then KEY = -1, indicates that no element
                 divisions will be displayed (the word OFF can also be
                 substituted).

        Notes
        -----
        Includes various symbols on the display.  Triads are right-handed with
        x displayed as the longest leg.  Where color is displayed, x is white,
        y is green, and z is blue.  For beams, x is always along the length of
        the element.   For lines, an arrow represents the direction of a line,
        from the beginning keypoint to the end keypoint.  See /PLOPTS command
        for additional display options.  Use /PSTATUS or /PSYMB,STAT to display
        settings.  Use /PSYMB,DEFA to reset all specifications back to their
        defaults.  The command /PSYMB,ECON,1 causes the symbol "M" to be
        displayed on keypoints and lines associated with meshed entities.  When
        you issue the command /PSYMB,DOT,1, a larger symbol is displayed for
        each node and keypoint location.

        PowerGraphics (/GRAPHICS,POWER) does not support /PSYMB,ESYS and
        /PSYMB,LAYR.

        If KEY = N and PowerGraphics is off, the centroid of the surface
        elements is connected to the extra node using a gray line.  However, if
        PowerGraphics is on, the color of the line connecting the centroid to
        the extra node is the same as that for the elements themselves (as
        determined by /PNUM).

        When Label = LAYR, the layer systems can be visualized with all
        current-technology layered elements and the smeared reinforcing element
        REINF265. To use /PSYMB,LAYR with REINF265, first set the vector-mode
        graphics option (/DEVICE,VECTOR,1).

        This command is valid in any processor.

        """
        command = f"/PSYMB,{label},{key}"
        return self.run(command, **kwargs)

    def triad(self, lab="", **kwargs):
        """Shows the global XYZ coordinate triad on displays.

        APDL Command: /TRIAD

        Parameters
        ----------
        lab
            Display triad as follows:

            ORIG - Display triad at global origin (default).

            OFF - Turn off triad display.

            LBOT - Display triad in lower left screen corner.

            RBOT - Display triad in lower right screen corner.

            LTOP - Display triad in upper left screen corner.

            RTOP - Display triad in upper right screen corner.

        Notes
        -----
        For efficiency, ANSYS 3-D graphics logic maintains a single data
        structure (segment), which includes the triad as a 3-D data object.  If
        a 3-D device is involved (/SHOW,3D), and the ANSYS graphics are not
        being displayed as multi-plots, then the triad location is determined
        by the view settings for Window #1.  A request for triad display
        anywhere except for the origin could yield an improper display in
        windows 2 through 5. The program displays the same segment in all
        windows.  The view settings of each window constitute the only
        difference in the display in the active windows.

        This command is valid in any processor.
        """
        command = f"/TRIAD,{lab}"
        return self.run(command, **kwargs)

    def udoc(self, wind="", cl_ass="", key="", **kwargs):
        """Determines position and content for the multi-legend options.

        APDL Command: /UDOC

        Parameters
        ----------
        wind
            The window number to which the command applies. (defaults to 1)

        class
            The type (and relative importance) of legend item being displayed:

            CNTR - Contour legend. This legend item is controlled separately from the other legend
                   items (see note below).

            DATE - The items in the DATE class include the date and time, or the ANSYS graphical
                   logo (/PLOPTS,LOGO,1). This item is shown by default in all
                   plots.

            GWIN - The items in the GWIN class include the entity acronyms that appear in the
                   legend of a multiplot of entities (Nodes, Elements,
                   Keypoints, Lines, Areas, Volumes). GWIN items are shown by
                   default for all GPLOT displays.

            TYPE - Items in the TYPE class include the plot type (e.g. ELEMENTS, MATERIALS, NODAL
                   SOLUTIONS, etc.). TYPE items are shown by default in all
                   plots.

            TYP2 - Items in the TYP2 class include supplementary type information, such as DMAX
                   and SMAX for nodal solutions. TYP2 items are shown by
                   default in all plots.

            INUM - Items in the INUM class include the number labels generated by the /PNUM
                   command. This class is displayed by default in all plots
                   that contain /PNUM information.

            BCDC - The items in the BCDC class include labels created by the /PBC  command. This
                   class is shown by default in all plots which contain /PBC
                   information.

            VECT - Items in the VECT class include labels created by the PLVECT command. This
                   class is shown by default for all PLVECT plots.

            SURF - The items in the SURF class include labels from the /PSF legend. This class is
                   shown by default on all plots of surface boundary
                   conditions.

            BODY - Items from the BODY class include labels from the /PBF legend. This class is
                   shown by default in all plots of body forces.

            PSTA - Items from the PSTA class include stress scaling statistics, such as the
                   /SSCALE setting. This class is not shown as the default for
                   any type of plot, and must be specifically referenced to
                   display the included data.

            VIEW - The items in the VIEW class include view statistics. This class is not shown as
                   the default for any type of plot, and must be specifically
                   referenced to display the included data.

            MISC - The items in the MISC class include supplementary labels like /EXPANDED and
                   Stress Section Cross Section. This class is not shown as the
                   default for any type of plot, and must be specifically
                   referenced to display the included data.

        key
            Switch:

        Notes
        -----
        The legend classes conform to the controls specified in the window
        options panel (PlotCtrls> Window Controls> Window Options). In many
        instances, the legend controls specified with the /PLOPTS command will
        take precedence and override /UDOC specifications. For instance:

        /PLOPTS,LEG1,OFF will disable the TYPE, TYP2, INUM, and MISC classes,
        regardless of the /UDOC settings.

        /PLOPTS,LEG2,OFF will disable the VIEW class, regardless of the /UDOC
        settings.

        /PLOPTS,LEG3,OFF will disable the PSTA class, regardless of the /UDOC
        settings.

        All items in a class are listed with the same X coordinate (except for
        contours). The contents of the text classes are dumped onto the display
        window from top to bottom, in order of class importance.

        The font specification for text items that are included in the user-
        specified legends are controlled with the /DEVICE command (PlotCtrls>
        Font Controls> Anno/Graph Font).

        The floating point values for the data presented in the legend(s) are
        controlled by the /GFORMAT command.
        """
        command = f"/UDOC,{wind},{cl_ass},{key}"
        return self.run(command, **kwargs)
