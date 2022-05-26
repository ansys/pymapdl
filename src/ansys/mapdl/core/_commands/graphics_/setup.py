class Setup:
    def color(self, lab="", clab="", n1="", n2="", ninc="", **kwargs):
        """Specifies the color mapping for various items.

        APDL Command: /COLOR

        Parameters
        ----------
        lab
            Apply color to the items specified by the following labels:

            AXES - Determines the color (specified in next argument, Clab) that the axes of a
                   graph will be plotted in.

            AXNUM - Determines the color (specified in next argument, Clab) that the numbering on
                    the axes of a graph will be plotted in.

            NUM - Discretely numbered items (such as element types, element materials, etc., as
                  shown on the /PNUM command).  Also specify number (1 to 11)
                  in the N1 field.  For example, /COLOR,NUM,RED,3 will assign
                  the color red to all items having the discrete number 3
                  (material displays would show elements having material 3 as
                  red).

            OUTL - Outline of elements, areas, and volumes.  Ex: /COLOR,OUTL,BLUE.

            ELEM - Elements. Use N1, N2, NINC fields for element numbers.

            LINE - Solid model lines.  Use N1, N2, NINC fields for line numbers.

            AREA - Solid model areas.  Use N1, N2, NINC fields for area numbers.

            VOLU - Solid model volumes.  Use N1, N2, NINC fields for volume numbers.

            ISURF - Isosurfaces (surfaces of constant stress, etc.).   This option is particularly
                    useful when capturing frames for animating a single
                    isosurface value.

            WBAK - Window background.  Use N1, N2, NINC fields for window numbers. The options
                   that you select using Lab = PBAK will supersede those
                   applied using Lab = WBAK.

            b.c.label - Boundary condition label.  Enter U, ROT, TEMP, PRES, V, VOLT, MAG, A, EMF,
                        CURR, F, M, HEAT, FLOW, VF, AMPS, FLUX, CSG, CURT,
                        VLTG, MAST, CP, CE, NFOR, NMOM, RFOR, RMOM, PATH. See
                        the /PBC command for boundary condition label
                        definitions.

            GRBAK - Graph background.

            GRID - Graph grid lines.

            AXLAB - Graph X and Y axis labels.

            CURVE - Graph curves (identify curve numbers (1-10) in N1, N2, NINC fields).

            CM - Component group.  Use N1 field for component name, ignore N2 and NINC.

            CNTR - ANSYS contour stress colors.  The maximum number of contours available is 128.
                   The number of colors that can be specified interactively
                   (GUI) is 9. (/CONTOUR, , 9). Any other setting will yield
                   inconsistent results.

            SMAX - Specifies that all stress values above the maximum value entered in /CONTOUR
                   will be displayed in the color designated in the Clab field.
                   Defaults to dark grey.

            SMIN - Specifies that all stress values below the minimum value entered in /CONTOUR
                   will be displayed in the color designated in the Clab field.
                   Defaults to dark grey.

            PBAK - Activates background shading options (see command syntax at end of argument
                   descriptions below). The options that you select using Lab =
                   PBAK will supersede those applied using Lab = WBAK.

        clab
            Valid color labels are:

            BLAC (0) - Black

            MRED (1) - Magenta-Red

            MAGE (2) - Magenta

            BMAG (3) - Blue-Magenta

            BLUE (4) - Blue

            CBLU (5) - Cyan-Blue

            CYAN (6) - Cyan

            GCYA ((7) - Green-Cyan

            GREE (8) - Green

            YGRE (9) - Yellow-Green

            YELL (10) - Yellow

            ORAN (11) - Orange

            RED (12) - Red

            DGRA (13) - Dark Gray

            LGRA (14) - Light Gray

            WHIT (15) - White

        n1, n2, ninc
            Apply color to Lab items numbered N1 to N2 (defaults to N1) in
            steps of NINC (defaults to 1).  If N1 is blank, apply color to
            entire selected range.  If Lab is CM, use component name for N1 and
            ignore N2 and NINC.  If N1 = P, graphical picking of elements,
            lines, areas and volumes is enabled; your can assign colors to the
            entities via the picker. When picking is enabled, the Lab and Clab
            fields are ignored.
        """
        command = f"/COLOR,{lab},{clab},{n1},{n2},{ninc}"
        return self.run(command, **kwargs)

    def device(self, label="", key="", **kwargs):
        """Controls graphics device options.

        APDL Command: /DEVICE

        Parameters
        ----------
        label
            Device function label:

            BBOX - Bounding box mode. For PowerGraphics plots involving elements with /SHOW,x11
                   and /SHOW,win32, ANSYS generally displays dynamic rotations
                   faster. If KEY = 1 (ON), then a bounding box (not the
                   elements) encompassing the model is displayed and rotated,
                   rather than the element outlines (ON is default in
                   preprocessing). When KEY = 0 (OFF), then dynamic rotations
                   may be slower (ANSYS redraws the element outlines) for plots
                   involving elements with /SHOW,x11 and /SHOW,win32.  OFF is
                   default in postprocessing. This command is ignored if
                   /EDGE,WN,1 is set for any WN. This is ignored in POST1 and
                   SOLUTION plots.

            For any PowerGraphics plots involving elements, regardless of /SHOW settings, plots will generally be displayed faster. - VECTOR

            Vector mode. In vector mode, areas, volumes, elements, and postprocessing display geometries are shown as outlines (wireframes).  When vector mode is off (default), these entities are shown filled with color. - DITHER

            When dithering is turned on (default), color intensity transitions are smoothed.  This selection a - applies only to smooth-shaded images, i.e., Z-buffered [/TYPE], or raster plots
                              with Gouraud or Phong shading [/SHADE].

            ANIM - Select the animation type used on 2-D devices on the PC platform. A KEY value
                   of BMP (or 0) sets animation mode to ANSYS Animation
                   Controller (default). A KEY value of AVI (or 2) sets
                   animation mode to AVI movie player file.

            FONT - Font selection for the ANSYS graphics window. When Label = FONT, the command
                   format is: /DEVICE,FONT,KEY,Val1,Val2,Val3,Val4,Val5,Val6
                   where KEY determines the type of font being controlled, and
                   values 1 through 6 control various font parameters. Note
                   that these values are device specific; using the same
                   command input file [/INPUT] on different machines may yield
                   different results.. The following KEY values determine the
                   font information that will be supplied to the appropriate
                   driver (e.g., Postscript, X11, Win32, JPEG, ...):

            KEY = 1 - The command controls the LEGEND (documentation column) font.

            KEY = 2 - The command controls the ENTITY (node and keypoint number) font.

            KEY = 3 - The command controls the ANNOTATION/GRAPH font.

            Linux: Values 1 through 4 are used to find a match in the X11 database of font strings. Values 1, 2, and 3 are character strings; value 4 is a nonzero integer:    - Val1

            Family name (e.g., Courier). If Val1 = MENU, all other values are ignored and a font selection menu appears (GUI must be active). - Val2

            Weight (e.g., medium) - Val3

            Slant (e.g., r) - Val4

            Pixel size (e.g., 14). Note that this value does no affect the annotation fonts (KEY = 3). Use the /TSPEC command for annotation font size.  - Val5

            Val1 - Family name (e.g., ``Courier*New``) Substitute an
                   asterisk (``*``) for any blank character that
                   appears in a family name. If Val1 = MENU, all other
                   values are ignored and a font selection menu
                   appears (GUI must be active). When this value is
                   blank ANSYS uses the first available resource it
                   finds.

            Val2 - Weight (0 - 1000)

            Val3 - Orientation (in tenths of a degree)

            Val4 - Height (in logical units)

            Val5 - Width (in logical units)

            Val6 - Italics (0 = OFF, 1 = ON)

            TEXT - Text size specification for the ANSYS Graphics window.  Using this label with
                   the /DEVICE command requires the following form:
                   /DEVICE,TEXT,KEY,PERCENT.  KEY = 1 for LEGEND fonts; KEY = 2
                   for ENTITY fonts.  PERCENT specifies the new text size as a
                   percent of the default text size.  If PERCENT = 100, the new
                   text size is precisely the default size.  If PERCENT = 200,
                   the new text size is twice the default text size.

        key
            Control key:

            OFF or 0 - Turns specified function off.

            ON or 1 - Turns specified function on or designates the LEGEND font.

            2 - Designates the ENTITY font.

            3 - Designates the ANNOTATION/GRAPH font.

        Notes
        -----
        This command is valid in any processor.

        The /DEVICE,BBOX command is ignored in POST1 and SOLUTION plots. Also,
        the elements are displayed and rotated if you use /DEVICE,BBOX,ON and
        /EDGE,WN,1,ANGLE (effectively ignoring the BBOX option).
        """
        command = f"/DEVICE,{label},{key}"
        return self.run(command, **kwargs)

    def dsys(self, kcn="", **kwargs):
        """Activates a display coordinate system for geometry listings and plots.

        APDL Command: DSYS

        Parameters
        ----------
        kcn
            Coordinate system reference number.  KCN may be 0,1,2 or any
            previously defined local coordinate system number.

        Notes
        -----
        Boundary condition symbols, vector arrows, and element coordinate
        system triads are not transformed to the display coordinate system. The
        display system orientation (for the default view) is X horizontal to
        the right, Y vertical upward, and Z out of the screen (normal).

        Line directions and area directions (/PSYMB,LDIR and /PSYMB,ADIR) are
        not plotted for DSYS > 0.

        When you create ANSYS 3-D annotation, the coordinates are stored to the
        database in the DSYS that was active at the time of creation. Changing
        the DSYS does not change the annotation coordinate data in the
        database.

        This command is valid in any processor.
        """
        command = f"DSYS,{kcn}"
        return self.run(command, **kwargs)

    def dv3d(self, lab="", key="", **kwargs):
        """Sets 3-D device option modes.

        APDL Command: /DV3D

        Parameters
        ----------
        lab
            Mode label:

            ACCU - Allows ANSYS to use the accumulation buffer for OpenGL graphics. Activating
                   this feature will provide faster model rotation when shaded
                   backgrounds are in use. This feature is off by default.

            ACTR - Label term to designate the cursor position as the center for automatic dynamic
                   rotational center capability.  The subsequent Key value (see
                   below) turns this capability on and off. This feature is on
                   by default. (Available for OpenGL displays only)

            ANIM - Animation mode.  The ANIM option allows you to create animation frames in
                   pixmap mode instead of display list mode.  This may improve
                   large model performance, but it eliminates local
                   manipulation while animation is in progress. This feature is
                   on by default.

            ANTI - Label term to control Anti-aliasing, a smoothing technique for your graph
                   plots. (see below) The subsequent Key value turns this
                   capability on and off. The default for this feature is off.
                   (Available for OpenGL displays only).

            CNTR - Switches banded contours on (1) or off (0) for your 3–D contour display. The
                   default is 1 (ON). Other contour parameters such as number
                   of contours or the increment and range are defined using the
                   /CONTOUR command. When either 9 or 128 contours are
                   specified via /CONTOUR, this command is ignored and a smooth
                   contour is always displayed.

            DGEN - Local manipulation degenerate mode.  You access the DGEN option to set wire-
                   frame local manipulation mode for 3-D devices (device
                   dependent). This feature is off by default.

            DLIST - With DLIST, you can specify whether screen updates and redraws will be
                    performed using the ANSYS Display List (off), or the 3-D
                    device's Display List (on). DLIST is on by default for
                    Windows systems, but off for Linux.

            DELS - You use DELS to suppress contour display screen overwrites when /NOERASE is
                   active. This prevents the bleed-through that occurs when you
                   overlay contour plots.

            TRIS - Triangle strip mode. Tri-stripping provides faster 3-D display capabilities and
                   is on by default. Some display enhancements, such as
                   texturing, are adversely affected by tri-stripping. You can
                   turn off tri-stripping in order to improve these display
                   functions. Be sure to turn tri-stripping on after the
                   desired output is obtained.

        key
            The following key options apply to Lab = ACCU:

            0 - (OFF)  The accumulation buffer is not accessed. (default)

            1 - (ON)  Access to the buffer is enabled.

        Notes
        -----
        ANSYS uses display list animation for its 3-D models. This memory
        resident array method interfaces with the OpenGL model information to
        allow the program to efficiently pan, zoom, rotate and dynamically
        manipulate your model during animation. The logo, legend, contour and
        other annotation items are produced in 2-D and will not appear when
        /DV3D, ANIM, 0 is in effect. To display these items, use /DV3D, ANIM,
        1. All screen data will be displayed, but manipulation of the model
        will not be possible.
        """
        command = f"/DV3D,{lab},{key}"
        return self.run(command, **kwargs)

    def gcmd(
        self,
        wn="",
        lab1="",
        lab2="",
        lab3="",
        lab4="",
        lab5="",
        lab6="",
        lab7="",
        lab8="",
        lab9="",
        lab10="",
        lab11="",
        lab12="",
        **kwargs,
    ):
        """Controls the type of element or graph display used for the GPLOT

        APDL Command: /GCMD
        command.

        Parameters
        ----------
        wn
            Window number (or ALL) to which this command applies (defaults to
            1)

        lab1, lab2, lab3, . . . , lab12
            Command labels (for example, PLNSOL,S,X)

        Notes
        -----
        This command controls the type of element or graph display that appears
        when you issue the GPLOT command when the /GTYPE,,(ELEM or GRPH) entity
        type is active.  If you have multiple plotting windows enabled, you can
        also use /GCMD to select one window when you wish to edit its contents.

        For related information, see the descriptions of the GPLOT and /GTYPE
        commands in this manual.

        This command is valid in any processor.
        """
        command = f"/GCMD,{wn},{lab1},{lab2},{lab3},{lab4},{lab5},{lab6},{lab7},{lab8},{lab9},{lab10},{lab11},{lab12}"
        return self.run(command, **kwargs)

    def gcolumn(self, curve="", string="", **kwargs):
        """Allows the user to apply a label to a specified curve.

        APDL Command: /GCOLUMN

        Parameters
        ----------
        curve
            Curve number on which label will be applied (integer value
            between 1 and 10).

        string
            Name or designation that will be applied to the curve (8
            characters max).

        Notes
        -----
        This command is used for an array parameter plot (a plot created by the
        ``*VPLOT`` command).  Normally the label for curve 1 is "COL 1", the label
        for curve 2 is "COL 2" and so on; the column number is the field
        containing the dependent variables for that particular curve. Issuing
        /GCOLUMN,CURVE, with no string value specified resets the label to the
        original value.
        """
        command = f"/GCOLUMN,{curve},{string}"
        return self.run(command, **kwargs)

    def gfile(self, size="", **kwargs):
        """Specifies the pixel resolution on Z-buffered graphics files.

        APDL Command: /GFILE

        Parameters
        ----------
        size
            Pixel resolution.  Defaults to a pixel resolution of 800.  Valid
            values are from 256 to 2400.

        Notes
        -----
        Defines the pixel resolution on subsequently written graphics files
        (Jobname.GRPH) for software Z-buffered displays [/TYPE].  Lowering the
        pixel resolution produces a "fuzzier" image; increasing the resolution
        produces a "sharper" image but takes a little longer.

        This command is valid in any processor.
        """
        command = f"/GFILE,{size}"
        return self.run(command, **kwargs)

    def gplot(self, **kwargs):
        """Controls general plotting.

        APDL Command: GPLOT

        Notes
        -----
        This command displays all entity types as specified via the /GTYPE
        command.  Only selected entities (NSEL, ESEL, KSEL, LSEL, ASEL, VSEL)
        will be displayed.  See the descriptions of the /GTYPE and /GCMD
        commands for methods of setting the entity types displayed.

        This command is valid in any processor.
        """
        command = f"GPLOT,"
        return self.run(command, **kwargs)

    def graphics(self, key="", **kwargs):
        """Defines the type of graphics display.

        APDL Command: /GRAPHICS

        Parameters
        ----------
        key
            Graphics key:

            FULL - Display all model geometry and results.

            POWER - Activate PowerGraphics (default when GUI is on).

        Notes
        -----
        The /GRAPHICS command specifies the type of graphics display. Key =
        POWER activates the PowerGraphics capability. PowerGraphics offers
        faster plotting than the Key = FULL option, and speeds up element,
        results, area, line, and volume displays. PowerGraphics mode (the
        default) is automatically invoked when the GUI is accessed. This action
        supersedes all prior macros or start up routines (start.ans,
        config.ans, etc.). Full graphics mode can be accessed only by issuing
        /GRAPHICS, FULL after the GUI is active.

        Results values (both printed and plotted) may differ between the Key =
        FULL and Key = POWER options because each option specifies a different
        set of data for averaging and display. For Key = FULL, all element and
        results values (interior and surface) are included.  For Key = POWER,
        only element and results values along the model exterior surface are
        processed.

        Caution:: : If you have specified one facet per element edge for
        PowerGraphics displays (via the /EFACET command or via choices from the
        General Postproc or Utility Menus), PowerGraphics does not plot midside
        nodes.

        The /EFACET command is only applicable to element type displays. (See
        the descriptions of these commands for more information.)

        Maximum values shown in plots can differ from printed maximum values.
        This is due to different averaging schemes used for plotted and printed
        maximum values.

        PowerGraphics displays do not average at geometric discontinuities. The
        printouts in PowerGraphics will, however, provide averaging information
        at geometric discontinuities if the models do not contain shell
        elements. Carefully inspect the data you obtain at geometric
        discontinuities.

        PowerGraphics does not support the following diffusion analysis
        results: CONC, CG, DF, EPDI.

        Note:: : In Full Graphics mode, it is possible to deselect an
        individual node, select all elements (including the element that
        contains that node), and then perform postprocessing calculations on
        those elements and have that unselected node not be considered in those
        calculations.  However, if PowerGraphics is active, postprocessing
        always displays based on selected elements.

        PowerGraphics does not support membrane shell elements such as SHELL41,
        and these elements using the membrane-stiffness-only option (KEYOPT1) =
        1): SHELL181, SHELL208, and SHELL209.

        Commands that are not supported by PowerGraphics are listed below.
        These commands are executed using the Key = FULL option, regardless of
        whether PowerGraphics is activated.  Only certain options for /CTYPE,
        /edge, /ESHAPE, ``*GET``, /PNUM, /PSYMB, SHELL, and ``*VGET`` are not supported
        by PowerGraphics.  (See the descriptions of these commands for more
        information.)
        """
        command = f"/GRAPHICS,{key}"
        return self.run(command, **kwargs)

    def gresume(self, fname="", ext="", **kwargs):
        """Sets graphics settings to the settings on a file.

        APDL Command: /GRESUME

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

        Notes
        -----
        Causes a file to be read to reset the graphics slash (/) commands as
        they were at the last  /GSAVE command.

        This command is valid in any processor.
        """
        command = f"/GRESUME,{fname},{ext}"
        return self.run(command, **kwargs)

    def gsave(self, fname="", ext="", **kwargs):
        """Saves graphics settings to a file for later use.

        APDL Command: /GSAVE

        Parameters
        ----------
        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).

        Notes
        -----
        This command does not save all graphics settings, but only those that
        may be reset by the /RESET command.  The database remains untouched.
        Use the /GRESUME command to read the file.  Repeated use of the /GSAVE
        command overwrites the previous data on the file.  The following
        commands are saved by /GSAVE:

        This command is valid in any processor.
        """
        command = f"/GSAVE,{fname},{ext}"
        return self.run(command, **kwargs)

    def gtype(self, wn="", label="", key="", **kwargs):
        """Controls the entities that the GPLOT command displays.

        APDL Command: /GTYPE

        Parameters
        ----------
        wn
            Window number (or ALL) to which this command applies (defaults to
            1)

        label
            This represents the type of entity to display:

            NODE - Nodes

            ELEM - Elements

            KEYP - Keypoints

            LINE - Lines

            AREA - Areas

            VOLU - Volumes

            GRPH - Graph displays

        key
            Switch:

            0 - Turns the entity type off.

            1 - Turns the entity type on.

        Notes
        -----
        The /GTYPE command controls which entities the GPLOT command displays.
        NODE, ELEM, KEYP, LINE, AREA, and VOLU are on by default.  When ELEM is
        activated, you can control the type of element displayed via the /GCMD
        command (which also controls the type of graph display).  When the GRPH
        entity type is activated, all other entity types are deactivated.
        Conversely, when any of the NODE, ELEM, KEYP, LINE, AREA, and VOLU
        entity types are active, the GRPH entity type is deactivated.

        The /GTYPE command gives you several options for multi-window layout:

        One window

        Two windows (left and right or top and bottom of the screen)

        Three windows (two at the top and one at the bottom of the screen, or
        one top and two bottom windows

        Four windows (two at the top and two at the bottom)



        Once you choose a window layout, you can choose one of the following:
        multiple plots, replotting, or no redisplay.

        This command is valid in any processor.
        """
        command = f"/GTYPE,{wn},{label},{key}"
        return self.run(command, **kwargs)

    def image(self, label="", fname="", ext="", **kwargs):
        """Allows graphics data to be captured and saved.

        APDL Command: /IMAGE

        Parameters
        ----------
        label
            Label specifying the operation to be performed:

            CAPTURE - Capture the image from the graphics window to a new window.

            RESTORE - Restore the image from a file to a new window.

            SAVE - Save the contents of the graphic window to a file.

            DELETE - Delete the window that contains the file.

        fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext
            Filename extension (eight-character maximum).
        """
        command = f"/IMAGE,{label},{fname},{ext}"
        return self.run(command, **kwargs)

    def jpeg(self, kywrd="", opt="", **kwargs):
        """Provides JPEG file export for ANSYS displays.

        APDL Command: JPEG

        Parameters
        ----------
        kywrd
            Specifies various JPEG file export options.

            QUAL - If Kywrd = QUAL, then OPT is an integer value defining the JPEG quality index
                   on an arbitrary scale ranging from 1 to 100. The default
                   value is 75.

            ORIENT - If Kywrd = ORIENT, then OPT will determine the orientation of the entire plot.
                     OPT can be either Horizontal (default) or Vertical.

            COLOR - If Kywrd = COLOR, then OPT will determine the color depth of the saved file.
                    OPT can be 0, 1, or 2, corresponding to Black and White,
                    Grayscale, and Color (default), respectively.

            TMOD - If Kywrd = TMOD, then OPT will determine the text method. OPT can be either 1
                   or 0, corresponding to bitmap text (default) or line stroke
                   text, respectively.

            DEFAULT - If Kywrd = DEFAULT, then all of the default values, for all of the Kywrd
                      parameters listed above, are active.

        opt
            OPT can have the following names or values, depending on the value
            for Kywrd (see above).

            1 to 100 - If Kywrd = QUAL, a value between 1 and 100 will determine the quality index of
                       the JPEG file.

            Horizontal, Vertical - If Kywrd = ORIENT, the terms Horizontal or Vertical determine the orientation
                              of the plot.

            0,1,2 - If Kywrd = COLOR, the numbers 0, 1, and 2 correspond to Black and White,
                    Grayscale and Color, respectively.

            1,0 - If Kywrd = TMOD, the values 1 and 0 determine whether bitmap (1) or stroke text
                  (0) fonts will be used
        """
        command = f"JPEG,{kywrd},{opt}"
        return self.run(command, **kwargs)

    def mrep(
        self,
        name="",
        arg1="",
        arg2="",
        arg3="",
        arg4="",
        arg5="",
        arg6="",
        arg7="",
        arg8="",
        arg9="",
        arg10="",
        arg11="",
        arg12="",
        arg13="",
        arg14="",
        arg15="",
        arg16="",
        arg17="",
        arg18="",
        **kwargs,
    ):
        """Enables you to reissue the graphics command macro "name" during a

        APDL Command: /MREP
        replot or zoom operation.

        Parameters
        ----------
        name
            The name identifying the macro file or macro block on a macro
            library file.  The name can contain up to eight characters maximum
            and must begin with a letter.

        arg1, arg2, arg3, . . . , arg18
            Values to be passed into the file or block.

        Notes
        -----
        This command reissues the graphics command macro "name" during a replot
        operation [/REPLOT] or a zoom [/ZOOM] operation.  The ANSYS program
        passes the command macro arguments to the replot and zoom feature for
        use by the graphics macro.  You should place the s-MREP command at the
        end of the graphics command macro, following the last graphics command
        within the macro, to enable the replot or zoom feature.
        """
        command = f"/MREP,{name},{arg1},{arg2},{arg3},{arg4},{arg5},{arg6},{arg7},{arg8},{arg9},{arg10},{arg11},{arg12},{arg13},{arg14},{arg15},{arg16},{arg17},{arg18}"
        return self.run(command, **kwargs)

    def pcopy(self, key="", **kwargs):
        """Automatically generates hard copies for HP UNIX work stations.

        APDL Command: /PCOPY

        Parameters
        ----------
        key
            Copy key:

            0 - No specification setting for automatic hard copy of display.

            1 - Set specification for automatic hard copy after each display.

            NOW - (Action) Produce hard copy of current display (KEY is not reset to 1).

        Notes
        -----
        Sets automatic hard copy specification.  This command is available only
        on HP work stations, and only during interactive runs with the /SHOW
        specification active (for terminals with hard copy capability).

        This command is valid in any processor.
        """
        command = f"/PCOPY,{key}"
        return self.run(command, **kwargs)

    def pngr(self, kywrd="", opt="", val="", **kwargs):
        """Provides PNG file export for ANSYS displays.

        APDL Command: PNGR

        Parameters
        ----------
        kywrd
            Specifies various PNG file export options.

            COMP - If Kywrd = COMP, then OPT is either ON or OFF (blank is interpreted as OFF).
                   This option allows you to turn PNG file compression ON or
                   OFF. If OPT = ON, then The VAL field is read to determine
                   the degree of compression. See the VALUE argument for
                   acceptable compression values.

            ORIENT - If Kywrd = ORIENT, then OPT will determine the orientation of the entire plot.
                     OPT can be either Horizontal (default) or Vertical.

            COLOR - If Kywrd = COLOR, then OPT will determine the color depth of the saved file.
                    OPT can be 0, 1, or 2, corresponding to Black and White,
                    Grayscale, and Color (default), respectively.

            TMOD - If Kywrd = TMOD, then OPT will determine the text method. OPT can be either 1
                   or 0, corresponding to bitmap text (default) or line stroke
                   text, respectively.

            DEFAULT - If Kywrd = DEFAULT, then all of the default values, for all of the Kywrd
                      parameters listed above, are active.

            STAT - Shows the current status of PNG file export.

        opt
            OPT can have the following names or values, depending on the value
            for Kywrd (see above).

            ON, OFF - If Kywrd = COMP, the values On and Off control the use of compression. The
                      degree of compression is determined by VAL

            Horizontal, Vertical - If Kywrd = ORIENT, the terms Horizontal or Vertical determine the orientation
                              of the plot.

            0, 1, 2 - If Kywrd = COLOR, the numbers 0, 1, and 2 correspond to Black and White,
                      Grayscale and Color, respectively.

            1, 0 - If Kywrd = TMOD, the values 1 and 0 determine whether bitmap (1) or stroke text
                   (0) fonts will be used

        val
            VAL is active only when Kywrd = COMP, and determines the degree of
            compression applied to the exported file (see above).

            1  - Apply the default, optimum value for compression. This value represents the
                 best combination of speed and compression. It varies according
                 to the release level of the ZLIB compression package.

            1-9  - Use this value to specify a specific compression level. 1 is the lowest
                   compression level (fastest) and 9 is the highest compression
                   level (slowest).
        """
        command = f"PNGR,{kywrd},{opt},{val}"
        return self.run(command, **kwargs)

    def pscr(self, kywrd="", key="", **kwargs):
        """Specifies various PostScript options.

        APDL Command: PSCR

        Parameters
        ----------
        index
            Color map index (0 to 15, 128 to 255).

        ired
            Red intensity (0 to 100).

        igrn
            Green intensity (0 to 100).

        iblu
            Blue intensity (0 to 100).

        Notes
        -----
        This command is available in both the ANSYS and DISPLAY programs.  It
        is valid for postscript format files chosen in ANSYS with the
        /SHOW,PSCR command, or in DISPLAY with /SHOWDISP,POSTSCRIPT.

        An output file is generated for each plot.  The ANSYS file is named
        JobnameNN.pscr.  In the DISPLAY program, this file is named PSCRnn.
        This file remains open for a subsequent /NOERASE plot, and will be
        incomplete until the program is closed (/EXIT), or until the next file
        is opened by the next /ERASE plot request.

        Issuing PSCR,STAT will list paper size, orientation and resolution
        modes.
        """
        command = f"PSCR,{kywrd},{key}"
        return self.run(command, **kwargs)

    def pstatus(self, wn="", **kwargs):
        """Displays the global or window display specifications.

        APDL Command: /PSTATUS

        Parameters
        ----------
        wn
            Window number for status (defaults to global specifications).

        Notes
        -----
        Displays the current global or window display specifications.  Global
        display specifications are common to all windows (e.g. /SHOW, etc.).
        Window display specifications are specific to one window (e.g. /VIEW,
        /TYPE, etc.).

        This command is valid in any processor.
        """
        command = f"/PSTATUS,{wn}"
        return self.run(command, **kwargs)

    def replot(self, label="", **kwargs):
        """Automatically reissues the last display command for convenience.

        APDL Command: /REPLOT

        Parameters
        ----------
        label
            Controls the type of replot.

            RESIZE - Issued internally when a graphics window resize occurs (Default).

            FAST - Only applicable for 3-D devices that allow a fast redisplay for changes in the
                   view characteristics only.

        Notes
        -----
        Reissues the last display command (NPLOT, EPLOT, KPLOT, PLNSOL, PLVAR,
        etc.), along with its parameters, for convenience.  The current display
        specifications are used.

        When the last display command is invalid in a particular processor, the
        use of the /REPLOT command is also invalid in that processor.  However,
        if you attempt a /REPLOT and the last display command is invalid in the
        current processor, ANSYS produces an element display [EPLOT] instead,
        as long as the last display command was PLNSOL, PLESOL, or PLDISP.
        ANSYS performs this substitution of /REPLOT with EPLOT for your
        convenience.

        For example, the PLNSOL command, which is used to display solution
        results as continuous contours, is a valid command in the general
        postprocessor [/POST1].  If you issue PLNSOL followed by /REPLOT while
        in the general postprocessor, the /REPLOT command effectively reissues
        your earlier PLNSOL command, along with its parameters.  But if you
        then exit the general postprocessor, enter the preprocessor [/PREP7],
        and issue the /REPLOT command again, ANSYS internally issues EPLOT
        instead.  This occurs because PLNSOL is not a valid command in the
        preprocessor.

        When you click on one of the buttons on the  Pan, Zoom, Rotate dialog
        box to manipulate the view of a model, the /REPLOT command is issued
        internally.  Thus, the substitution of /REPLOT with EPLOT as described
        above may occur not only for the PLNSOL, PLESOL, and PLDISP results
        display commands, but also for operations that you perform with the
        Pan, Zoom, Rotate dialog box.

        /REPLOT will not show boundary conditions if they are only applied to a
        solid model and the last display command (for example, EPLOT) displays
        the finite element model. To show boundary conditions, the following
        options are available:

        Issue /REPLOT after you issue the SBCTRAN command to transfer solid
        model boundary conditions to the finite element model.

        Issue /REPLOT after you issue a solid model display command (for
        example, VPLOT).

        This command is valid in any processor (except as noted above).
        """
        command = f"/REPLOT,{label}"
        return self.run(command, **kwargs)

    def slashreset(self, **kwargs):
        """Resets display specifications to their initial defaults.

        APDL Command: /RESET

        Notes
        -----
        Resets slash display specifications (/WINDOW, /TYPE, /VIEW, etc.) back
        to their initial default settings (for convenience).  Also resets the
        focus location to the geometric center of the object.

        This command is valid in any processor.
        """
        command = "/RESET,"
        return self.run(command, **kwargs)

    def seg(self, label="", aviname="", delay="", **kwargs):
        """Allows graphics data to be stored in the local terminal memory.

        APDL Command: /SEG

        Parameters
        ----------
        label
            Storage key:

            SINGL - Store subsequent display in a single segment (overwrites last storage).

            MULTI - Store subsequent displays in unique segments [ANIM].

            DELET - Delete all currently stored segments.

            OFF - Stop storing display data in segments.

            STAT - Display segment status.

            PC - This option only applies to PC versions of ANSYS and only when animating via
                 the AVI movie player (i.e., /DEVICE,ANIM,2).  This command
                 appends frames to the File.AVI, so that the animation goes in
                 both directions (i.e., forward--backward--forward).  You must
                 have a current animation file to use this option.

        aviname
            Name of the animation file that will be created when each frame is
            saved. The .AVI extension is applied automatically. Defaults to
            Jobname.AVI if no filename is specified.

        delay
            Delay factor between each frame, in seconds. Defaults to 0.015
            seconds if no value is specified.

        Notes
        -----
        Allows graphics data to be stored in the terminal local memory (device-
        dependent).  Storage occurs concurrently with the display.

        Although the information from your graphics window is stored as an
        individual segment, you cannot plot directly (GPLOT) from the segment
        memory.

        For the DISPLAY program, the Aviname and DELAY fields are ignored.

        This command is valid in any processor.
        """
        command = f"/SEG,{label},{aviname},{delay}"
        return self.run(command, **kwargs)

    def show(self, fname="", option="", vect="", ncpl="", **kwargs):
        """Specifies the device and other parameters for graphics displays.

        APDL Command: /SHOW

        Parameters
        ----------
        fname
            Device name, file name, or keyword, as listed below:

            <device name> - Any valid graphics display device name (e.g., X11, 3-D etc.).  Defaults to X11
                            for most systems.  See Getting Started with
                            Graphics in the Basic Analysis Guide for details.
                            A device name must be defined before activating the
                            Graphical User Interface (GUI).  Once the GUI is
                            activated, the device name cannot be changed for
                            that session, except for switching between X11 and
                            X11C.

            <filename> - Name of graphics file to which graphics displays are to be diverted (248
                         characters maximum).  Should not be the same as a
                         valid device name or any other Fname option. Plots are
                         written to the file Filename.Ext (or just Filename.Ext
                         if Ext is left blank) in the working directory. This
                         file can be appended only during the same session;
                         reissuing the same file name in a new session will
                         overwrite existing file names from previous sessions.
                         Although multiple file names can be used within one
                         session, only the last file created or accessed will
                         be appended.  Issuing /SHOW, CLOSE, or starting a new
                         session will prevent access to any previously created
                         files.

            TERM - Graphics displays are switched back to the last-specified device name.

            CLOSE - This option purges the graphics file buffer. The CLOSE option should be issued
                    any time you are changing graphics devices or file output
                    types during a session. Graphics displays are switched back
                    to the last-specified device name, and any open graphics
                    files are closed. The CLOSE option is similar to the TERM
                    option, however, with the CLOSE option, another process,
                    such as the DISPLAY program, can access the data in the
                    graphics file. The CLOSE option causes graphics file
                    buffers to be flushed to the graphics file.

            FILE - Graphics displays are switched back to the last-specified file name.

            OFF - Graphics display requests are ignored.

            (blank) - If blank in interactive mode, graphics will be displayed on screen as requested
                      by display commands (no file written);  If blank in batch
                      mode, graphics data will be written to Jobname.GRPH.

            PSCR - Creates PostScript graphic files that are named Jobnamennn.eps, where nnn is a
                   numeric value that is incremented by one as each additional
                   file is created; that is, Jobname000.eps, Jobname001.eps,
                   Jobname002.eps, and so on .  (See the PSCR command for
                   options.)  Ignores the Ext and NCPL fields.

            HPGL - Creates Hewlett-Packard Graphics Language files that are named Jobnamennn.hpgl,
                   where nnn is a numeric value that is incremented by one as
                   each additional file is created; that is, Jobname000.hpgl,
                   Jobname001.hpgl, Jobname002.hpgl, and so on.  (See the HPGL
                   command for options.)  Ignores the Ext and NCPL fields.

            HPGL2 - Creates Hewlett-Packard Graphics Language files that are named Jobnamennn.hpgl,
                    where nn is a numeric value that is incremented by one as
                    each additional file is created; that is, Jobname000.hpgl,
                    Jobname001.hpgl, Jobname02.hpgl, and so on.  The HPGL2
                    files have enhanced color.  (See the HPGL command for
                    options.)  Ignores the Ext field.

            JPEG - Creates JPEG files that are named Jobnamennn.jpg, where nnn is a numeric value
                   that is incremented by one as each additional file is
                   created; that is, Jobname000.jpg, Jobname001.jpg,
                   Jobname002.jpg, and so on. Ignores the Ext field.

            TIFF - Creates tagged image format files that are named Jobnamennn.tif, where nnn is a
                   numeric value that is incremented by one as each additional
                   file is created; that is, Jobname000.tif, Jobname001.tif,
                   Jobname002.tif, and so on. This value for the Fname argument
                   ignores the Ext field. (See the TIFF command for options.)

            PNG - Creates PNG (Portable Network Graphics) files that are named Jobnamennn.png,
                  where nnn is a numeric value that is incremented by one as
                  each additional file is created; that is, Jobname000.png,
                  Jobname001.png, Jobname002.png, and so on. This value for the
                  Fname argument ignores the Ext field. (See the PNGR command
                  for options.)

            VRML - Creates Virtual Reality Meta Language files named Jobname000.wrl that can be
                   displayed on 3-D Internet web browsers.  Ignores the Ext and
                   NCPL fields.

        option
            Assign a file name extension or specify reverse video output:

            Ext -  File name extension (eight-character maximum).

            REV - Reverse background/image (black/white) colors. Valid with Fname = PNG
                  (recommended), JPEG, PSCR, TIFF, and HPGL. This option is
                  ignored if a previously specified color map table  (/CMAP or
                  /RGB) is in effect.

        vect
            Specifies raster or vector display mode.  This affects area,
            volume, and element displays, as well as geometric results displays
            such as contour plots.  See the /DEVICE command for an alternate
            way to toggle between raster and vector mode.  Changing VECT also
            resets the /TYPE command to its default.

            0 - Raster display (color filled entities; default)

            1 - Vector display (outlined entities; i.e., "wireframe")

        ncpl
            Sets the number of color planes (4 to 8).  Default is device-
            dependent.  NCPL is not supported by all graphics devices.

        Notes
        -----
        Specifies the device to be used for graphics displays, and specifies
        other graphics display parameters.  Display may be shown at the time of
        generation (for interactive runs at a graphics display terminal) or
        diverted to a file for later processing with the DISPLAY program.
        Issue /PSTATUS for display status.

        Batch runs do not have access to the fonts available on your system.
        The Courier and Helvetica font files used for JPEG, PNG and TIFF batch
        output are copyrighted by Adobe Systems Inc. and Digital Equipment
        Corp. Permission to use these trademarks is hereby granted only in
        association with the images described above. Batch run JPEG output is
        produced at the default  quality index value of 75, unless specified
        otherwise.

        Interactive displays default to eight color planes (NCPL = 8) for most
        monitors, while graph file output defaults to eight color planes for
        VRML output, and four color planes for PSCR, HPGL, HPGL2, JPEG, PNG,
        TIFF and FILE33.

        This command is valid in any processor.
        """
        command = f"/SHOW,{fname},{option},{vect},{ncpl}"
        return self.run(command, **kwargs)

    def tiff(self, kywrd="", opt="", **kwargs):
        """Provides TIFF file Export for ANSYS Displays.

        APDL Command: TIFF

        Parameters
        ----------
        kywrd
            Specifies various TIFF file export options.

            COMP - If Kywrd = COMP, then OPT controls data compression
                   for the output file. If COMP = 0, then compression
                   is off. If COMP = 1 (default), then compression is
                   on.

            ORIENT - If Kywrd = ORIENT, then OPT will determine the
                     orientation of the entire plot.  OPT can be
                     either Horizontal (default) or Vertical.

            COLOR - If Kywrd = COLOR, then OPT will determine the
                    color attribute of the saved file. OPT can be 0,
                    1, or 2, corresponding to Black and White,
                    Grayscale, and Color (default), respectively.

            TMOD - If Kywrd = TMOD, then OPT will determine the text
                   method. OPT can be either 1 or 0, corresponding to
                   bitmap text (default) or line stroke text,
                   respectively.

            DEFAULT - If Kywrd = DEFAULT, then all of the default
                      values, for all of the Kywrd parameters listed
                      above, are active.

        opt
            OPT can have the following names or values, depending on
            the value for Kywrd (see above).

            1 or 0 - If Kywrd = COMP, a value or 1 (on) or 0 (off)
                     will control compression for the TIFF file.

            Horizontal, Vertical - If Kywrd = ORIENT, the terms
                                   Horizontal or Vertical determine
                                   the orientation of the plot.

            0, 1, 2 - If Kywrd = COLOR, the numbers 0, 1, and 2
                      correspond to Black and White , Grayscale and
                      Color, respectively.

            1, 0 - If Kywrd = TMOD, the values 1 and 0 determine
                   whether bitmap (1) or stroke text (0) fonts will be
                   used
        """
        command = f"TIFF,{kywrd},{opt}"
        return self.run(command, **kwargs)

    def window(self, wn="", xmin="", xmax="", ymin="", ymax="", ncopy="", **kwargs):
        """Defines the window size on the screen.

        APDL Command: /WINDOW

        Parameters
        ----------
        wn
            Window reference number (1 to 5).  Defaults to 1.  This number, or
            ALL (for all active windows), may be used on other commands.

        xmin, xmax, ymin, ymax
            Screen coordinates defining window size.  Screen coordinates are
            measured as -1.0 to 1.67 with the origin at the screen center.  For
            example, (-1,1.67,-1,1) is full screen, (-1,0,-1,0) is the left
            bottom quadrant.  If XMIN = OFF, deactivate this previously defined
            window; if ON, reactivate this previously defined window.  If FULL,
            LEFT, RIGH, TOP, BOT, LTOP, LBOT, RTOP, RBOT, form full, half, or
            quarter window.  If SQUA, form largest square window within the
            current graphics area.  If DELE, delete this window (cannot be
            reactivated with ON).

        ncopy
            Copies the current specifications from window NCOPY (1 to 5) to
            this window.  If NCOPY = 0 (or blank), no specifications are
            copied.

        Notes
        -----
        Defines the window size on the screen.  Windows may occupy a separate
        section of the screen or they may overlap.  Requested displays are
        formed in all windows according to the selected window specifications.

        This command is valid in any processor.
        """
        command = f"/WINDOW,{wn},{xmin},{xmax},{ymin},{ymax},{ncopy}"
        return self.run(command, **kwargs)
