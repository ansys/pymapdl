# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Annotation:

    def an3d(self, **kwargs):
        r"""Specifies 3D annotation functions

        Mechanical APDL Command: `/AN3D <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AN3D.html>`_

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AN3D.html>`_
           for further explanations.

        .. _AN3D_notes:

        Because 3D annotation is applied in relation to the XYZ coordinates of the anchor, you can transform
        your model, and the annotation will maintain the spatial relationship with the model. This works
        within reason, and there are instances where changing the perspective or the size of the model will
        change the apparent relationship between the annotation and the model.

        The overall 3D dimensions of your model are defined by a bounding box. If portions of your model's
        bounding box lie outside of the visible area of your graphics window (if you are zoomed in on a
        specific area of your model), it can affect the placement of your 3D annotations. Zooming out will
        usually overcome this problem.

        3D annotation is valid for the Cartesian ( :ref:`csys`,0) coordinate system only. If you want to
        annotate a model you created in another coordinate system, use 2D annotation (note that 2D
        annotations do not remain anchored for dynamic rotations or transformations).

        When you apply user defined bitmaps, the size of the annotation can vary. Use the options menu of
        the 3D annotation widget to adjust the size and placement of your bitmaps.

        You cannot use the "!" and "$" characters in Mechanical APDL text annotation.

        The GUI generates this command during 3D annotation operations and inserts the command into the log
        file ( :file:`Jobname.LOG` ). You should NOT type this command directly during a Mechanical APDL
        session
        (although the command can be included in an input file for batch input or for use with the
        :ref:`input` command).
        """
        command = "/AN3D"
        return self.run(command, **kwargs)

    def annot(self, lab: str = "", val1: str = "", val2: str = "", **kwargs):
        r"""Activates graphics for annotating displays (GUI).

        Mechanical APDL Command: `/ANNOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANNOT.html>`_

        Parameters
        ----------
        lab : str
            Annotation control key:

            * ``OFF`` - Turns off annotation for each subsequent display (default).

            * ``ON`` - Turns on annotation for each subsequent display.

            * ``DELE`` - Deletes all annotation.

            * ``SAVE`` - Saves annotation on a file. Use ``VAL1`` for file name (defaults to :file:`Jobname` )
              and ``VAL2`` for the extension (defaults to ANO).

            * ``SCALE`` - Sets annotation scale factor (direct input only). Use ``VAL1`` for value (0.1 to 10.0)
              (defaults to 1.0).

            * ``XORIG`` - Sets the annotation x origin (direct input only). Use ``VAL1`` for value (-3.0 to
              3.0).

            * ``YORIG`` - Sets annotation y origin (direct input only). Use ``VAL1`` for value (-3.0 to 3.0).

            * ``SNAP`` - Sets annotation snap (menu button input only). Use ``VAL1`` for value (0.002 to 0.2)
              (defaults to 0.002).

            * ``STAT`` - Displays current annotation status.

            * ``DEFA`` - Sets annotation specifications to the default values.

            * ``REFR`` - Redisplays annotation graphics.

            * ``TMOD`` - Sets the annotation text mode. If ``VAL1`` = 1, annotation text will be drawn in
              scalable bitmap fonts (default). If ``VAL1`` = 0, annotation text will be drawn with stroke text.

        val1 : str
            Value (or file name) as noted with label above.

        val2 : str
            Value (or file name extension) as noted with label above.

        Notes
        -----

        .. _s-ANNOT_notes:

        This is a command generated by the GUI and will appear in the log file ( :file:`Jobname.LOG` ) if
        annotation is used. This command is not intended to be typed in directly in a Mechanical APDL
        session
        (although it can be included in an input file for batch input or for use with the :ref:`input`
        command).

        You cannot use the "!" and "$" characters in Mechanical APDL text annotation.

        :ref:`annot` activates annotation graphics for adding annotation to displays. Commands representing
        the annotation instructions are automatically created by the annotation functions in the GUI and
        written to :file:`JobnameLOG`.

        The annotation commands are :ref:`annot`, :ref:`anum`, :ref:`tlabel`, :ref:`slashline`,
        :ref:`slashlarc`, :ref:`lsymbol`, :ref:`polygon`, :ref:`pmore`, :ref:`pcircle`, :ref:`pwedge`,
        :ref:`tspec`, :ref:`lspec`, and :ref:`slashpspec`. Annotation graphics are relative to the full
        Graphics Window and are not affected by Mechanical APDL window-specific commands ( :ref:`window`,
        :ref:`view`, etc.).

        This command is valid in any processor.
        """
        command = f"/ANNOT,{lab},{val1},{val2}"
        return self.run(command, **kwargs)

    def anum(
        self,
        num: str = "",
        type_: int | str = "",
        xhot: str = "",
        yhot: str = "",
        **kwargs,
    ):
        r"""Specifies the annotation number, type, and hot spot (GUI).

        Mechanical APDL Command: `/ANUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ANUM.html>`_

        **Command default:**

        .. _s-ANUM_default:

        Number, type, and hot spot are automatically determined.

        Parameters
        ----------
        num : str
            Annotation number. Mechanical APDL automatically assigns the lowest available number. You cannot
            assign a higher number if a lower number is available; the program substitutes the lowest
            available number in place of any user-specified higher number.

        type_ : int or str
            Annotation internal type number. If ``TYPE`` = DELE, delete annotation ``NUM``.

            * ``1`` - Text

            * ``2`` - Block text (not available in GUI)

            * ``3`` - Dimensions

            * ``4`` - Lines

            * ``5`` - Rectangles

            * ``6`` - Circles

            * ``7`` - Polygons

            * ``8`` - Arcs

            * ``9`` - Wedges, pies

            * ``11`` - Symbols

            * ``12`` - Arrows

            * ``13`` - Bitmap

        xhot : str
            X hot spot (-1.0 < X < 2.0). Used for menu button item delete.

        yhot : str
            Y hot spot (-1.0 < Y < 1.0). Used for menu button item delete.

        Notes
        -----

        .. _s-ANUM_notes:

        This is a command generated by the GUI and will appear in the log file ( :file:`Jobname.LOG` ) if
        annotation is used. This command is not intended to be typed in directly in a Mechanical APDL
        session
        (although it can be included in an input file for batch input or for use with the :ref:`input`
        command).

        Type 13 (bitmap) annotation applies user defined bitmaps defined using the FILE option of the
        :ref:`txtre` command.

        This command is valid in any processor.
        """
        command = f"/ANUM,{num},{type_},{xhot},{yhot}"
        return self.run(command, **kwargs)

    def lspec(
        self, lcolor: str = "", linstl: int | str = "", xlnwid: str = "", **kwargs
    ):
        r"""Specifies annotation line attributes (GUI).

        Mechanical APDL Command: `/LSPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSPEC.html>`_

        Parameters
        ----------
        lcolor : str

        linstl : int or str
            Line style:

            * ``0`` - Solid line.

            * ``1`` - Dashed line.

        xlnwid : str
            Line width multiplier (1.0 to 20.0). Defaults to 1.0.

        Notes
        -----

        .. _s-LSPEC_notes:

        This command specifies annotation line attributes to control certain characteristics of the lines
        created via the :ref:`slashline`, :ref:`slashlarc`, :ref:`lsymbol`, :ref:`polygon`, :ref:`pmore`,
        :ref:`pcircle`, and :ref:`pwedge` commands.

        The command is generated by the Graphical User Interface (GUI) and appears in the log file (
        :file:`Jobname.LOG` ) if annotation is used. It is not intended to be typed in directly in a
        Mechanical APDL session (although it can be included in an input file for batch input or for use
        with the
        :ref:`input` command).

        This command is valid in any processor.
        """
        command = f"/LSPEC,{lcolor},{linstl},{xlnwid}"
        return self.run(command, **kwargs)

    def lsymbol(
        self,
        x: str = "",
        y: str = "",
        symang: str = "",
        symtyp: int | str = "",
        symsiz: str = "",
        keybmp: str = "",
        **kwargs,
    ):
        r"""Creates annotation symbols (GUI).

        Mechanical APDL Command: `/LSYMBOL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LSYMBOL.html>`_

        Parameters
        ----------
        x : str
            X location for symbol (-1.0 < X < 2.0).

        y : str
            Y location for symbol (-1.0 < Y < 1.0).

        symang : str
            Symbol orientation angle.

        symtyp : int or str
            Symbol type:

            * ``1`` - Arrow.

            * ``2`` - Tee.

            * ``3`` - Circle.

            * ``4`` - Triangle.

            * ``5`` - Star.

        symsiz : str
            Symbol size multiplier (0.1 to 20.0). Defaults to 1.0.

        keybmp : str
            If ``KEYBMP`` = 1, the annotation is a bitmap. ``SYMTYP`` will then be a number from 1-99,
            indicating the bitmap type (see notes), and ``X`` and ``Y`` will define the lower left corner of
            the bitmap. The ``SYMANG``, ``SYMSIZ`` arguments are ignored. If ``KEYBMP`` = 0, or blank, then
            the argument definitions above apply.

        Notes
        -----

        .. _s-LSYMBOL_notes:

        Defines annotation symbols to be written directly onto the display at a specified location. This is
        a command generated by the GUI and will appear in the log file ( :file:`Jobname.LOG` ) if annotation
        is used. This command is not intended to be typed in directly in a Mechanical APDL session (although
        it can
        be included in an input file for batch input or for use with the :ref:`input` command).

        All symbols are shown on subsequent displays unless the annotation is turned off or deleted. Use the
        :ref:`lspec` command to set the attributes of the symbol.

        The ``KEYBMP`` argument reads the symtype argument to determine which bitmap to insert. This bitmap
        is defined by an integer between 1 and 99. Numbers 1 through 40 correspond to the standard texture
        values found in the :ref:`txtre` command, while numbers 51 through 99 correspond to user supplied
        bitmaps, as defined using the Filename option of the :ref:`txtre` command. Numbers 51 through 57 are
        predefined (the logos, clamps and arrows available from the GUI) but can be overridden. Numbers 41
        through 50 are reserved.

        This command is valid in any processor.
        """
        command = f"/LSYMBOL,{x},{y},{symang},{symtyp},{symsiz},{keybmp}"
        return self.run(command, **kwargs)

    def pcircle(self, xcentr: str = "", ycentr: str = "", xlrad: str = "", **kwargs):
        r"""Creates an annotation circle (GUI).

        Mechanical APDL Command: `/PCIRCLE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PCIRCLE.html>`_

        Parameters
        ----------
        xcentr : str
            Circle X center location (-1.0 < X < 2.0).

        ycentr : str
            Circle Y center location (-1.0 < Y < 1.0).

        xlrad : str
            Circle radius length.

        Notes
        -----

        .. _s-PCIRCLE_notes:

        Creates an annotation circle to be written directly onto the display at a specified location. This
        is a command generated by the Graphical User Interface (GUI) and appears in the log file (
        :file:`Jobname.LOG` ) if annotation is used.

        This command is not intended to be typed in directly in a Mechanical APDL session (although it can
        be
        included in an input file for batch input or for use with the :ref:`input` command).

        All circles are shown on subsequent displays unless the annotation is turned off or deleted. Issue
        :ref:`lspec` and :ref:`slashpspec` to set the attributes of the circle.

        This command is valid in any processor.
        """
        command = f"/PCIRCLE,{xcentr},{ycentr},{xlrad}"
        return self.run(command, **kwargs)

    def pmore(
        self,
        x5: str = "",
        y5: str = "",
        x6: str = "",
        y6: str = "",
        x7: str = "",
        y7: str = "",
        x8: str = "",
        y8: str = "",
        **kwargs,
    ):
        r"""Creates an annotation polygon (GUI).

        Mechanical APDL Command: `/PMORE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PMORE.html>`_

        Parameters
        ----------

        x5 : str
            X location for vertex 5 of polygon (-1.0 < X < 2.0).

        y5 : str
            Y location for vertex 5 of polygon (-1.0 < Y < 1.0).

        x6 : str
            X location for vertex 6 of polygon (-1.0 < X < 2.0).

        y6 : str
            Y location for vertex 6 of polygon (-1.0 < Y < 1.0).

        x7 : str
            X location for vertex 7 of polygon (-1.0 < X < 2.0).

        y7 : str
            Y location for vertex 7 of polygon (-1.0 < Y < 1.0).

        x8 : str
            X location for vertex 8 of polygon (-1.0 < X < 2.0).

        y8 : str
            Y location for vertex 8 of polygon (-1.0 < Y < 1.0).

        Notes
        -----

        .. _s-PMORE_notes:

        Defines the 5th through 8th vertices of an annotation polygon ( :ref:`polygon` ). This is a command
        generated by the Graphical User Interface (GUI) and appears in the log file ( :file:`Jobname.LOG` )
        if annotation is used.

        The command is not intended to be typed in directly in a Mechanical APDL session (although it can be
        included in an input file for batch input or for use with the :ref:`input` command).

        This command is valid in any processor.
        """
        command = f"/PMORE,,{x5},{y5},{x6},{y6},{x7},{y7},{x8},{y8}"
        return self.run(command, **kwargs)

    def polygon(
        self,
        nvert: str = "",
        x1: str = "",
        y1: str = "",
        x2: str = "",
        y2: str = "",
        x3: str = "",
        y3: str = "",
        x4: str = "",
        y4: str = "",
        **kwargs,
    ):
        r"""Creates annotation polygons (GUI).

        Mechanical APDL Command: `/POLYGON <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_POLYGON.html>`_

        Parameters
        ----------
        nvert : str
            Number of vertices of polygon (3 :math:`equation not available`   ``NVERT``  :math:`equation not
            available`  8).  Use  :ref:`pmore` for polygons with more than 4 vertices.

        x1 : str
            X location for vertex 1 of polygon (-1.0 < X < 2.0).

        y1 : str
            Y location for vertex 1 of polygon (-1.0 < Y < 1.0).

        x2 : str
            X location for vertex 2 of polygon (-1.0 < X < 2.0).

        y2 : str
            Y location for vertex 2 of polygon (-1.0 < Y < 1.0).

        x3 : str
            X location for vertex 3 of polygon (-1.0 < X < 2.0).

        y3 : str
            Y location for vertex 3 of polygon (-1.0 < Y < 1.0).

        x4 : str
            X location for vertex 4 of polygon (-1.0 < X < 2.0).

        y4 : str
            Y location for vertex 4 of polygon (-1.0 < Y < 1.0).

        Notes
        -----

        .. _s-POLYGON_notes:

        Creates annotation polygons to be written directly onto the display at a specified location. This is
        a command generated by the Graphical User Interface (GUI) and will appear in the log file (
        :file:`Jobname.LOG` ) if annotation is used.

        The command is not intended to be typed in directly in a Mechanical APDL session (although it can be
        included in an input file for batch input or for use with :ref:`input` ).

        All polygons are shown on subsequent displays unless the annotation is turned off or deleted. Issue
        :ref:`lspec` and :ref:`slashpspec` to set the attributes of the polygon. Issue :ref:`pmore` to
        define the 5th through 8th vertices of the polygon.

        This command is valid in any processor.
        """
        command = f"/POLYGON,{nvert},{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4}"
        return self.run(command, **kwargs)

    def pwedge(
        self,
        xcentr: str = "",
        ycentr: str = "",
        xlrad: str = "",
        angle1: str = "",
        angle2: str = "",
        **kwargs,
    ):
        r"""Creates an annotation wedge (GUI).

        Mechanical APDL Command: `/PWEDGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PWEDGE.html>`_

        Parameters
        ----------
        xcentr : str
            Wedge X center location (-1.0 < X < 2.0).

        ycentr : str
            Wedge Y center location (-1.0 < Y < 1.0).

        xlrad : str
            Wedge radius length.

        angle1 : str
            Starting angle of wedge.

        angle2 : str
            Ending angle of wedge. The wedge is drawn counterclockwise from the starting angle, ``ANGLE1``,
            to the ending angle, ``ANGLE2``.

        Notes
        -----

        .. _s-PWEDGE_notes:

        Creates an annotation wedge to be written directly onto the display at a specified location. This is
        a command generated by the Graphical User Interface (GUI) and will appear in the log file (
        :file:`Jobname.LOG` ) if annotation is used.

        The command is not intended to be typed in directly in a Mechanical APDL session (although it can be
        included in an input file for batch input or for use with :ref:`input` ).

        All wedges are shown on subsequent displays unless the annotation is disabled or deleted. Issue
        :ref:`lspec` and :ref:`slashpspec` to set the attributes of the wedge.

        This command is valid in any processor.
        """
        command = f"/PWEDGE,{xcentr},{ycentr},{xlrad},{angle1},{angle2}"
        return self.run(command, **kwargs)

    def slashlarc(
        self,
        xcentr: str = "",
        ycentr: str = "",
        xlrad: str = "",
        angle1: str = "",
        angle2: str = "",
        **kwargs,
    ):
        r"""Creates annotation arcs (GUI).

        Mechanical APDL Command: `/LARC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LARC_sl.html>`_

        Parameters
        ----------
        xcentr : str
            Arc X center location (-1.0 < X < 1.0).

        ycentr : str
            Arc Y center location (-1.0 < Y < 1.0).

        xlrad : str
            Arc radius length.

        angle1 : str
            Starting angle of arc.

        angle2 : str
            Ending angle of arc. The arc is drawn counterclockwise from the starting angle, ``ANGLE1``, to
            the ending angle, ``ANGLE2``.

        Notes
        -----

        .. _s-LARC_notes:

        This command defines annotation arcs to be written directly onto the display at a specified
        location.

        The command is generated by the Graphical User Interface (GUI) and will appear in the log file (
        :file:`Jobname.LOG` ) if annotation is used. It is not intended to be typed in directly in a
        Mechanical APDL session (although it can be included in an input file for batch input or for use
        with the
        :ref:`input` command).

        All arcs are shown on subsequent displays unless the annotation is turned off or deleted. Issueu
        :ref:`lspec` to set the attributes of the arc.

        This command is valid in any processor.
        """
        command = f"/LARC,{xcentr},{ycentr},{xlrad},{angle1},{angle2}"
        return self.run(command, **kwargs)

    def slashline(
        self, x1: str = "", y1: str = "", x2: str = "", y2: str = "", **kwargs
    ):
        r"""Creates annotation lines (GUI).

        Mechanical APDL Command: `/LINE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LINE_sl.html>`_

        Parameters
        ----------
        x1 : str
            Line X starting location (-1.0 < X < 2.0).

        y1 : str
            Line Y starting location (-1.0 < Y < 1.0).

        x2 : str
            Line X ending location (-1.0 < X < 2.0).

        y2 : str
            Line Y ending location (-1.0 < Y < 1.0).

        Notes
        -----

        .. _s-LINE_notes:

        This command defines annotation lines to be written directly onto the display at a specified
        location.

        The command is generated by the Graphical User Interface (GUI) and appears in the log file (
        :file:`Jobname.LOG` ) if annotation is used. It is not intended to be typed in directly in a
        Mechanical APDL session (although it can be included in an input file for batch input or for use
        with the
        :ref:`input` command).

        All lines are shown on subsequent displays unless the annotation is turned off or deleted. Issue
        :ref:`lspec` to set the attributes of the line.

        This command is valid in any processor.
        """
        command = f"/LINE,{x1},{y1},{x2},{y2}"
        return self.run(command, **kwargs)

    def slashpspec(
        self,
        pcolor: int | str = "",
        kfill: int | str = "",
        kbordr: int | str = "",
        **kwargs,
    ):
        r"""Creates annotation polygon attributes (GUI).

        Mechanical APDL Command: `/PSPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSPEC_sl.html>`_

        Parameters
        ----------
        pcolor : int or str
            Polygon color (0 :math:`equation not available`   ``PCOLOR``  :math:`equation not available`  15):

            * ``0`` - Black.

            * ``1`` - Red-Magenta.

            * ``2`` - Magenta.

            * ``3`` - Blue-Magenta.

            * ``4`` - Blue.

            * ``5`` - Cyan-Blue.

            * ``6`` - Cyan.

            * ``7`` - Green-Cyan.

            * ``8`` - Green.

            * ``9`` - Yellow-Green.

            * ``10`` - Yellow.

            * ``11`` - Orange.

            * ``12`` - Red.

            * ``13`` - Dark Gray.

            * ``14`` - Light Gray.

            * ``15`` - White.

        kfill : int or str
            Polygon fill key:

            * ``0`` - Hollow polygon.

            * ``1`` - Filled polygon.

        kbordr : int or str
            Polygon border key:

            * ``0`` - No border.

            * ``1`` - Border.

        Notes
        -----

        .. _s-PSPEC_notes:

        Creates annotation polygon attributes to control certain characteristics of the polygons created via
        :ref:`polygon`, :ref:`pmore`, :ref:`pcircle`, and :ref:`pwedge`.

        This command is generated by the graphical user interface (GUI) and appears in the log file (
        :file:`Jobname.LOG` ) if annotation is used. It is not intended to be typed in directly in a
        Mechanical APDL session (although it can be included in an input file for batch input or for use
        with
        :ref:`input` ).

        This command is valid in any processor.
        """
        command = f"/PSPEC,{pcolor},{kfill},{kbordr}"
        return self.run(command, **kwargs)

    def tlabel(self, xloc: str = "", yloc: str = "", text: str = "", **kwargs):
        r"""Creates annotation text (GUI).

        Mechanical APDL Command: `/TLABEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TLABEL.html>`_

        Parameters
        ----------
        xloc : str
            Text ``X`` starting location (-1.0 < ``X`` < 1.6).

        yloc : str
            Text Y starting location (-1.0 < ``Y`` < 1.0).

        text : str
            Text string (60 characters maximum). Parameter substitution may be forced within the text by
            enclosing the parameter name or parametric expression within percent (%) signs.

        Notes
        -----

        .. _s-TLABEL_notes:

        Defines annotation text to be written directly onto the display at a specified location. This
        command is generated by the Graphical User Interface (GUI) and appears in the log file (
        :file:`Jobname.LOG` ) if annotation is used.

        The command is not intended to be typed in directly in a Mechanical APDL session (although it can be
        included in an input file for batch input or for use with :ref:`input` ).

        All text is shown on subsequent displays unless the annotation is disabled or deleted. Issue
        :ref:`tspec` to set the attributes of the text.

        This command is valid in any processor.
        """
        command = f"/TLABEL,{xloc},{yloc},{text}"
        return self.run(command, **kwargs)

    def tspec(
        self,
        tcolor: int | str = "",
        tsize: str = "",
        txthic: int | str = "",
        pangle: str = "",
        iangle: str = "",
        **kwargs,
    ):
        r"""Creates annotation text attributes (GUI).

        Mechanical APDL Command: `/TSPEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TSPEC.html>`_

        Parameters
        ----------
        tcolor : int or str
            Text color (0 :math:`equation not available`   ``TCOLOR``  :math:`equation not available`  15):

            * ``0`` - Black.

            * ``1`` - Red-Magenta.

            * ``2`` - Magenta.

            * ``3`` - Blue-Magenta.

            * ``4`` - Blue.

            * ``5`` - Cyan-Blue.

            * ``6`` - Cyan.

            * ``7`` - Green-Cyan.

            * ``8`` - Green.

            * ``9`` - Yellow-Green.

            * ``10`` - Yellow.

            * ``11`` - Orange.

            * ``12`` - Red.

            * ``13`` - Dark Gray.

            * ``14`` - Light Gray.

            * ``15`` - White.

        tsize : str
            Text size factor.

        txthic : int or str
            Text thickness key:

            * ``1`` - normal.

            * ``2`` - twice as thick.

            * ``3`` - three times as thick.

            * ``4`` - four times as thick.

        pangle : str
            Text path angle (0.0 < ``angle`` < 360.0).

        iangle : str
            Text italic angle (0.0 < ``angle`` < 45.0).

        Notes
        -----

        .. _s-TSPEC_notes:

        This command defines annotation text attributes to control certain characteristics of the text
        created via :ref:`tlabel`. This command is generated by the Graphical User Interface (GUI) and
        appears in the log file ( :file:`Jobname.LOG` ) if annotation is used.

        The command is not intended to be typed in directly in a Mechanical APDL session (although it can be
        included in an input file for batch input or for use with :ref:`input` ).

        This command is valid in any processor.
        """
        command = f"/TSPEC,{tcolor},{tsize},{txthic},{pangle},{iangle}"
        return self.run(command, **kwargs)
