class Setup:
    def cmap(self, fname="", ext="", kywrd="", ncntr="", **kwargs):
        """Changes an existing or creates a new color mapping table.

        APDL Command: /CMAP

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

        kywrd
            Keyword indicating the disposition of the color map file.

            (blank) - Loads existing color map file.

            CREATE - Starts the CMAP utility and modifies or creates
            the specified file.

            SAVE - Writes the active color map to the specified file,
            which can be imported into future sessions.

        ncntr
            Number of contours to be defined. Default = 9 (even if an existing
            file is being modified). Maximum = 128.

        Notes
        -----
        Reads the color map file (RGB index specifications) to change
        from current specifications.  Only one color map may be active
        at a time.

        For 2-D drivers (especially Win32c), modifying the color map
        can produce anomalies, including legend/contour disagreement.

        When Kywrd equals CREATE, the 2-D drivers (X11c and Win32c)
        display the CMAP utility with an additional contour color
        picker called CONTOURS.  Colors selected via the CONTOURS
        picker affect result contour displays (such as stresses). No
        other drivers offer the CONTOURS picker in the CMAP utility.

        Changing the color map using the /CMAP command changes the
        meaning of the color labels on the /COLOR command. See /COLOR
        for other color controls.

        This command is valid anywhere.
        """
        return self.run(f"/CMAP,{fname},{ext},,{kywrd},{ncntr}", **kwargs)

    def devdisp(self, label="", key="", **kwargs):
        """Controls graphics device options.

        APDL Command: /DEVDISP

        Parameters
        ----------
        label
            Device function label:

            BBOX - Disables display information sorting for PowerGraphics displays. When activated
                   (KEY = 1 or ON), model rotations and replots are performed
                   without recalculating edge and surface data. This will speed
                   up the rotation (especially for 2-D displays) of large
                   models, although the display information will not be
                   resolved as quickly (you will see a bounding box instead of
                   the model during dynamic rotations). The default is OFF (KEY
                   = 0).

            DITHER - Dithering.  When turned on (default), dithering smooths transitions in color
                     intensity.  Applies only to Z-buffered displays.

            FONT - Font selection for the ANSYS graphics window.  When Label = FONT, the command
                   format is: /DEVDISP,FONT,KEY,Val1,Val2,Val3,VAL4,Val5,Val6,
                   where KEY determines the type of font being controlled, and
                   values 1 through 6 control various font parameters. Note
                   that these values are device specific; using the same
                   command input file [/INPUT] on different machines may yield
                   different results.The following KEY values determine the
                   font information that will be supplied to the appropriate
                   driver (e.g., Postscript, X11, Win32, JPEG, ...):

            KEY = 1 - The command controls the LEGEND (documentation column) font.

            KEY = 2 - The command controls the ENTITY (node and keypoint number) font.

            KEY = 3 - The command controls the ANNOTATION/GRAPH font.

            Linux: Values 1 through 4 are used to find a match in the X11 database of font strings.  Values 1, 2, and 3 are character strings; value 4 is a nonzero integer:    - Val1

            Family name (e.g., ``Courier*New``). Substitute an asterisk (``*``) for any blank character that appears in a family name. If Val1 = MENU, all other values are ignored, and a font selection menu appears (GUI must be active).  - Val2

            Weight (e.g., medium) - Val3

            Slant (e.g., r) - Val4

            Pixel size (e.g., 14). Note that this value does not affect the annotation fonts (KEY = 3). Use the /TSPEC command to control the pixel size of your annotation fonts.  - Val5

            unused - Val6

            unused - PC: The values are encoded in a PC logical font structure.  Value 1 is a
                     character string, and the remaining values are integers:

            Val1 - Family name (e.g., ``Courier*New``) Substitute an asterisk (``*``) for any blank
                   character that appears in a family name. If Val1 = MENU, all
                   other values are ignored and a font selection menu appears
                   (GUI must be active). A value containing all blank
                   characters causes ANSYS to use the first available resource
                   it finds.

            Val2 - Weight (0 - 1000)

            Val3 - Orientation (in tenths of a degree)

            Val4 - Height (in logical units) Note that this value does not affect the annotation
                   fonts (KEY =3). Use the /TSPEC command to control the height
                   of your annotation fonts.

            Val5 - Width (in logical units)

            Val6 - Italics (0 = OFF, 1 = ON)

            TEXT - Text size specification for the ANSYS Graphics window. When Label = TEXT, the
                   command format is: /DEVDISP,TEXT,KEY,PERCENT, where KEY
                   determines the type of text being controlled (1 for LEGEND,
                   and 2 for ENTITY), and PERCENT specifies the new text size
                   as a percent of the default text size.  If PERCENT = 100,
                   the new text size is precisely the default size.  If PERCENT
                   = 200, the new text size is twice the default text size.

        key
            Control key:

            OFF or 0 - Turns specified function off.

            ON or 1 - Turns specified function on.
        """
        command = f"/DEVDISP,{label},{key}"
        return self.run(command, **kwargs)

    def filedisp(self, fname="", ext="", **kwargs):
        """Specifies the file containing the graphics data.

        APDL Command: FILEDISP

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
        Specifies the input file containing the graphics data (defaults to
        File.GRPH).
        """
        command = f"FILEDISP,{fname},{ext}"
        return self.run(command, **kwargs)

    def nocolor(self, key="", **kwargs):
        """Removes color from graphics displays.

        APDL Command: NOCOLOR

        Parameters
        ----------
        key
            Color key:

            0 - Color the displays.

            1 - Do not color the displays.

            2 - Do not shade the displays.
        """
        command = f"NOCOLOR,{key}"
        return self.run(command, **kwargs)

    def showdisp(self, dname="", ncpl="", **kwargs):
        """Defines the display driver name.

        APDL Command: /SHOWDISP

        Parameters
        ----------
        dname
            Valid driver name (see Getting Started with Graphics in the Basic
            Analysis Guide for details):

            <device name> - Any linked terminal driver (such as X11, TEKTRONIX, etc.)

            HPGL - Hewlett-Packard Graphics Language

            HPGL2 - Hewlett-Packard Graphics Language with enhanced
                    color.  (See the HPGL command for options.)
                    Ignores the NCPL field.

            INTERLEAF - Interleaf ASCII Format, OPS Version 5.0

            POSTSCRIPT - PostScript, Version 1.0 Minimally Conforming

            DUMP - ASCII Text Dump

        ncpl
            Number of color planes (4 to 8).  Default is device-dependent.
        """
        return self.run(f"/SHOWDISP,{dname},,,{ncpl}", **kwargs)

    def trans(self, fname="", ext="", **kwargs):
        """Reformats File.GRPH for improved performance with plotters.

        APDL Command: TRANS

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
        Reformats current Fname.GRPH data (based on color) for improved
        performance with pen plotters.
        """
        command = f"TRANS,{fname},{ext}"
        return self.run(command, **kwargs)
