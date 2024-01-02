class Graphs:
    def axlab(self, axis="", lab="", **kwargs):
        """Labels the X and Y axes on graph displays.

        APDL Command: /AXLAB

        Parameters
        ----------
        axis
            Axis specifier:

            X - Apply label to X axis.

            Y - Apply label to Y axis.

        lab
            Axis label (user defined text up to 30 characters long).  Leave
            blank to reestablish the default for Axis axis.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"/AXLAB,{axis},{lab}"
        return self.run(command, **kwargs)

    def grid(self, key="", **kwargs):
        """Selects the type of grid on graph displays.

        APDL Command: /GRID

        Parameters
        ----------
        key
            Grid key:

            0 (OFF) - No grid.

            1 (ON) - Full grid (X and Y grid lines).

            2 (X) - Partial grid (X grid lines only).

            3 (Y) - Partial grid (Y grid lines only)

        Notes
        -----
        Selects the type of grid on graph displays.  Graphs with multiple
        Y-axes can have multiple grids [/GRTYP].  The grid of the first curve
        is also used as the background grid (above and behind the curve).
        Grids for other curves are limited to be under the curves.  See also
        /GTHK and /GROPT for other grid options.

        This command is valid in any processor.
        """
        command = f"/GRID,{key}"
        return self.run(command, **kwargs)

    def gropt(self, lab="", key="", **kwargs):
        """Sets various line graph display options.

        APDL Command: /GROPT

        Parameters
        ----------
        lab
            Apply display style as selected from the following labels:

            AXDV - Axis division (tick) marks (defaults to KEY = ON).

            AXNM - Axis scale numbers (defaults to KEY = ON, which puts numbers at the back plane
                   of the graph).  If KEY = FRONT, numbers are on the front
                   plane of the graph.

            AXNSC - Axis number size scale factor.  Input the scale value for KEY (defaults to
                    1.0).

            ASCAL - Automatic scaling of additional Y-axes for multi-curve [/GRTYP, 2 or 3] graphs
                    (defaults to KEY = ON).  If KEY = OFF, use base Y-axis
                    scaling (see the /YRANGE command).

            LOGX - Log X scale (defaults to KEY = OFF (linear)).

            LOGY - Log Y scale (applies only to the base Y axis) (defaults to KEY = OFF (linear)).

            FILL - Color fill areas under curves (defaults to KEY = OFF).

            CGRID - Superimpose background grid [/GRID] over areas under filled curves (defaults to
                    KEY = OFF).

            DIG1 - Number of significant digits before decimal point for axis values.  Input the
                   value for KEY (defaults to 4).

            DIG2 - Number of significant digits after decimal point for axis values.  Input the
                   value for KEY (defaults to 3).

            VIEW - View key for graph displays (defaults to KEY = OFF, in which case the view is
                   (0,0,1) for 2-D graph displays or (1,2,3) for 3-D graph
                   displays).  If KEY = ON, the view settings for graph
                   displays are the same as the view settings for the model.

            REVX - Plots the values on the X-axis in reverse order.

            REVY - Plots the values on the Y-axis in reverse order.

            DIVX - Determines the number of divisions (grid markers) that will be plotted on the X
                   axis.

            DIVY - Determines the number of divisions (grid markers) that will be plotted on the Y
                   axis.

            LTYP - Determines whether ANSYS generated (KEY = 1) or system derived (KEY = 0) fonts
                   will be used for the axis labels.

            CURL - Determines the position of the curve labels. If (KEY = 1), the curve label will
                   be plotted in the legend column, and the label will be
                   displayed in the same color as the curve. If (KEY = 0) the
                   curve labels will be plotted near the curve. (default).

            XAXO - When you use this label, the subsequent KEY value will determine an offset
                   amount from the default (along the bottom) location for the
                   X axis. If KEY = 1.0, a full offset occurs (the X axis is
                   moved to the top of the graph). If KEY = 0.5, the axis is
                   offset to the midpoint of the graph, and if KEY = 0 the axis
                   remains in the original position, along the bottom of the
                   graph. For any offset, a grey copy of the original axis
                   (containing the axis numbering) remains at the original
                   location.

            YAXO - When you use this label, the subsequent KEY value will determine an offset
                   amount from the default (along the left side of the graph)
                   location for the Y axis. If KEY = 1.0, a full offset occurs
                   (the Y axis is moved to the right side of the graph). If KEY
                   = 0.5, the axis is offset to the midpoint of the graph, and
                   if KEY = 0 the axis remains in the original position, along
                   the left side of the graph. For any offset, a gray copy of
                   the original axis (containing the axis numbering) remains at
                   the original location.

        key
            Option values:

            OFF (0) - Do not apply selected style.

            ON (1) - Apply selected style.

            nnnn - If Lab is DIG1 or DIG2, input the number of digits.

            nn - If Lab is AXNSC, input the scale factor.

            FRONT - If Lab is AXNM, FRONT may also be input.

            Ndiv - If Lab is DIVX or DIVY, determines the number of divisions (1-99) that will be
                   applied to the axis.

            Kfont - If Lab is LTYP, Kfont is ON (1) or OFF(0).  ON will use ANSYS generated fonts
                    for the axis labels, while OFF will use SYSTEM (Windows,
                    X-system, etc.) fonts. The default value is ON (ANSYS
                    fonts).

        Notes
        -----
        Sets various line graph display options.  Issue /GROPT,STAT to display
        the current settings.  Issue /GROPT,DEFA to reset the default
        specifications.  ANSYS informs you that graph view manipulation is
        inactive unless you have issued the /GROPT,VIEW,ON command.  See the
        /AXLAB, /GRTYP, /GRID, and /GTHK commands for other graph control
        options.

        Automatic scaling using the /XRANGE and /YRANGE commands will often
        yield inappropriate range values for logarithmic scales (/GROPT, LOGX
        or /GROPT, LOGY).

        This command is valid in any processor.
        """
        command = f"/GROPT,{lab},{key}"
        return self.run(command, **kwargs)

    def grtyp(self, kaxis="", **kwargs):
        """Selects single or multiple Y-axes graph displays.

        APDL Command: /GRTYP

        Parameters
        ----------
        kaxis
            Axis selection key:

            0 or 1 - Single Y-axis.  Up to 10 curves scaled to a single Y-axis.

            2 - Additional Y-axes (one for each curve) (3 curves maximum).  Allows better
                scaling of curves with widely differing numbering ranges.

            3 - Same as 2 but with additional Y-axis and curves projected out of the plane (6
                curves maximum).  Allows clearer display with an isometric
                view.  The default view when KAXIS = 3 is View,1,1,2,3.

        Notes
        -----
        The basic line graph has one or more curves plotted against the same Y
        and X axes.  Multiple curve graphs can also be plotted with individual
        Y axes and the same X axis.  The Y axis of the first curve is referred
        to as the base Y-axis and the Y axes of the other curves as additional
        Y axes.  Curves are numbered sequentially from 1 (the base curve) in
        the order in which they are displayed.  See the /AXLAB, /GROPT, /GRID,
        and /GTHK commands for other display options.

        This command is valid in any processor.
        """
        command = f"/GRTYP,{kaxis}"
        return self.run(command, **kwargs)

    def gthk(self, label="", thick="", **kwargs):
        """Sets line thicknesses for graph lines.

        APDL Command: /GTHK

        Parameters
        ----------
        label
            Apply thicknesses as selected from the following labels:

            AXIS - Modify thickness of ordinate and abscissa axes on graph displays.

            GRID - Modify thickness of grid lines on graph displays.

            CURVE - Modify thickness of curve lines (when no area fill [/GROPT]).

        thick
            Thickness ratio (whole numbers only, from -1 to 10):

            -1 - Do not draw the curve, but show only the markers specified by /GMARKER.

            0 or 1 - Thin lines.

            2 - The default thickness.

            3 - 1.5 times the default thickness.

            etc. - (up to 10)

        Notes
        -----
        Sets line thicknesses for graph lines (in raster mode only).  Use
        /GTHK,STAT to show settings.

        This command is valid in any processor.
        """
        command = f"/GTHK,{label},{thick}"
        return self.run(command, **kwargs)

    def xrange(self, xmin="", xmax="", **kwargs):
        """Specifies a linear abscissa (X) scale range.

        APDL Command: /XRANGE

        Parameters
        ----------
        xmin
            Minimum abscissa scale value.

        xmax
            Maximum abscissa scale value.

        Notes
        -----
        Specifies a linear abscissa (X) scale range for the line graph display.
        Use /XRANGE,DEFAULT to return to automatic scaling.

        Automatic scaling will often yield inappropriate range values for
        logarithmic scales (/GROPT, LOGX).

        This command is valid in any processor.
        """
        command = f"/XRANGE,{xmin},{xmax}"
        return self.run(command, **kwargs)

    def yrange(self, ymin="", ymax="", num="", **kwargs):
        """Specifies a linear ordinate (Y) scale range.

        APDL Command: /YRANGE

        Parameters
        ----------
        ymin
            Minimum ordinate scale value.

        ymax
            Maximum ordinate scale value.

        num
            Y-axis number to which range applies (defaults to 1).  Valid
            numbers are 1 to 3 for /GRTYP,2 and 1 to 6 for /GRTYP,3.  If ALL,
            apply to all Y-axes.

        Notes
        -----
        Specifies a linear ordinate (Y) scale range for the line graph display.
        Use /YRANGE,DEFAULT to return to automatic scaling.  For multiple
        Y-axes graphs [/GRTYP], see /GROPT, ASCAL to automatically scale the
        additional Y-axes.

        Automatic scaling will often yield inappropriate range values for
        logarithmic scales (/GROPT, LOGY).

        This command is valid in any processor.
        """
        command = f"/YRANGE,{ymin},{ymax},{num}"
        return self.run(command, **kwargs)
