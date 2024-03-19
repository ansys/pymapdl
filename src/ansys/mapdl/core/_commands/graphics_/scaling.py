class Scaling:
    def iclwid(self, factor="", **kwargs):
        """Scales the line width of circuit builder icons.

        APDL Command: /ICLWID

        Parameters
        ----------
        factor
            Multiplication factor applied to the default line width (defaults
            to 1). The minimum is 1 and the maximum is 6.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"/ICLWID,{factor}"
        return self.run(command, **kwargs)

    def icscale(self, wn="", factor="", **kwargs):
        """Scales the icon size for elements supported in the circuit builder.

        APDL Command: /ICSCALE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        factor
            Factor applied to the default icon size (defaults to 1).

        Notes
        -----
        Scaling the icon size can provide better visualization of the circuit
        components when using the Circuit Builder (an interactive builder
        available in the ANSYS GUI).

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"/ICSCALE,{wn},{factor}"
        return self.run(command, **kwargs)

    def ratio(self, wn="", ratox="", ratoy="", **kwargs):
        """Distorts the object geometry.

        APDL Command: /RATIO

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        ratox
            Distort object in the window X direction by this factor (defaults
            to 1.0).

        ratoy
            Distort object in the window Y direction by this factor (defaults
            to 1.0).

        Notes
        -----
        Distorts the object geometry in a particular direction.  An example of
        this command's use would be to allow long narrow sections to be
        distorted to a more square area for better display visualization.

        This command is valid in any processor.
        """
        command = f"/RATIO,{wn},{ratox},{ratoy}"
        return self.run(command, **kwargs)

    def shrink(self, ratio="", **kwargs):
        """Shrinks elements, lines, areas, and volumes for display clarity.

        APDL Command: /SHRINK

        Parameters
        ----------
        ratio
            Shrinkage ratio (input as a decimal (0.0 to 0.5)).  Defaults to 0.0
            (no shrinkage).  Values greater than 0.5 default to 0.1 (10%
            shrinkage).

        Notes
        -----
        Shrinks the elements, lines, areas, and volumes so that adjacent
        entities are separated for clarity.  Portions of this command are not
        supported by PowerGraphics [/GRAPHICS,POWER].

        If only the common lines of non-coplanar faces are drawn (as per the
        /EDGE command), then this command is ignored.

        This command is valid in any processor.
        """
        command = f"/SHRINK,{ratio}"
        return self.run(command, **kwargs)

    def sscale(self, wn="", smult="", **kwargs):
        """Sets the contour multiplier for topographic displays.

        APDL Command: /SSCALE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        smult
            Contour multiplier that factors in results based on the product of
            the multiplier and the result being plotted. Defaults to 0.0 (no
            topographic effects).

        Notes
        -----
        Use this command to scale values to the geometry when the contours are
        shown elevated.  For section displays [/TYPE], the elevation is
        performed perpendicular to the section face.

        Nonzero contour multipliers factoring in large results (stresses or
        displacements) can produce very large distortion, causing images to
        disappear.  To bring a distorted image back into view, reduce the
        contour multiplier value.

        Portions of this command are not supported by PowerGraphics
        [/GRAPHICS,POWER].
        """
        command = f"/SSCALE,{wn},{smult}"
        return self.run(command, **kwargs)

    def txtre(self, lab="", num="", n1="", n2="", ninc="", **kwargs):
        """Controls application of texture to selected items.

        APDL Command: /TXTRE

        Parameters
        ----------
        lab
            You can apply texture according to the following labels:

            ELEM - Apply texture to elements N1 through N2 in steps of NINC.

            AREA - Apply texture to areas N1 through N2 in steps of NINC.

            VOLU - Apply texture to volumes N1 through N2 in steps of NINC.

            CM - Apply texture to the component named in N1. N2 and
            NINC are ignored.

            ON, OFF - Sets the specified texture display on or
            off. All other fields are ignored.

            File - If Lab = File, the command format is /TXTRE, File,
                   Key_Index, Fname, Fext, --, Format (This variant of
                   the command is applicable to 2-D drivers).

            Key_Index - The texture index associated with the file. If
                        the number fifty-one (51) is used, the
                        imported bitmap will be used as the window's
                        logo.

            Fname - File name and directory path (248 characters
                    maximum, including the characters needed for the
                    directory path).  An unspecified directory path
                    defaults to the working directory; in this case,
                    you can use all 248 characters for the file name.

            Fext - Filename extension (eight-character maximum).

            Format - The file format. If Format = 0, the file is a
                     pixmap (Linux) or Bitmap (PC).  The file cannot
                     contain a compressed image, and the PC file must
                     be 8 or 24 bit BI_RGB format. If Format = 1 or
                     JPEG, then the file is in JPEG (Joint
                     Photographic Experts Group) format. If Format = 2
                     or PNG, then the file is in PNG (Portable Network
                     Graphics) format.

        num
            Select the texture index number from the following list:

            0 - No Texturing

            1 - Aluminum

            2 -  Aluminum, Brushed

            3 - Steel With Bumps

            4 - Steel, Embossed

            5 - Iron

            6 - Steel, Pattern

            7 - Steel, Riveted

            8 - Steel, Scratched

            9 - Tin

            10 - Metal

            11 - Steel, Etched

            12 - Metal, Hot

            13 - Iron, Grainy

            14 - Metal, Rusty

            15 - Brick

            16 - Block

            17 - Wood

            18 - Wood, Light

            19 - Wood, Walnut

            20 - Plastic, Hard Blue

            21 - Plastic, Light Blue

            22 - Plastic, Hard Red

            31 - Gold

            32 - Brass

            33 - Silver

            34 -  Plastic, Black

            35 - Plastic, Ivory

            36 - Plastic, Blue

            37 - Plastic, Red

            38 - Plastic, Yellow

            39 - Plastic, Green

            40 - Plastic, Brown

        n1, n2, ninc
            Apply texture to Lab items numbered N1 through N2 in steps of NINC
            (defaults to 1). If Lab = CM, then N1 is used to for the component
            name and N2 and NINC are ignored. If Lab = ELEM, AREA, or VOLU and
            N1 = blank or ALL, then the specified texture will be applied to
            all entities of type Lab. If N1 = P, then graphical picking is
            enabled.

        Notes
        -----
        This command is available for 3-D Open GL devices. 2-D devices are
        supported only for the Lab = File variation of the command, allowing
        imported bitmaps to be used for texturing and annotation. Textures can
        affect the speed of many of your display operations. You can increase
        the speed by temporarily turning the textures off (Utility Menu>
        PlotCtrls> Style> Texturing(3D)> Display Texturing). This menu
        selection toggles your textures on and off. When textures are toggled
        off, all of the texture information is retained and reapplied when
        texturing is toggled back on.

        For some displays, the texture will appear distorted because of a
        technique used to enhance 3-D displays (/DV3D,TRIS,1). Disabling this
        function (/DV3D,TRIS,0) will improve the quality of some texture
        displays. Disabling the TRIS option of the /DV3D command will slow down
        3-D displays significantly. Be sure to reapply the TRIS option after
        you obtain a satisfactory output.

        Specifying /TXTRE,DEFA removes all texturing.
        """
        command = f"/TXTRE,{lab},{num},{n1},{n2},{ninc}"
        return self.run(command, **kwargs)

    def vscale(self, wn="", vratio="", key="", **kwargs):
        """Scales the length of displayed vectors.

        APDL Command: /VSCALE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        vratio
            Ratio value applied to the automatically calculated scale factor
            (defaults to 1.0, i.e., use scale factor as automatically
            calculated).

        key
            Relative scaling key:

            0 - Use relative length scaling among vectors based on magnitudes.

            1 - Use uniform length scaling for all vector lengths.

        Notes
        -----
        Allows scaling of the vector length displayed with the PLVECT command
        of POST1 and the /PBC and /PSF commands.  Also allows the scaling of
        the  element (i.e., /PSYMB,ESYS) and the nodal (i.e., /PSYMB,NDIR)
        coordinate system symbols.

        This command is valid in any processor.
        """
        command = f"/VSCALE,{wn},{vratio},{key}"
        return self.run(command, **kwargs)
