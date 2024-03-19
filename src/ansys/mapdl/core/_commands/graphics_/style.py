from typing import Optional, Union
import warnings

from ansys.mapdl.core.mapdl_types import MapdlInt


class Style:
    def cplane(self, key="", **kwargs):
        """Specifies the cutting plane for section and capped displays.

        APDL Command: /CPLANE

        Parameters
        ----------
        key
            Specifies the cutting plane:

            0 - Cutting plane is normal to the viewing vector [/VIEW] and passes through the
                focus point [/FOCUS] (default).

            1 - The working plane [WPLANE] is the cutting plane.

        Notes
        -----
        Defines the cutting plane to be used for section and capped displays
        [/TYPE,,(1, 5, or 7)].

        This command is valid in any processor.
        """
        command = f"/CPLANE,{key}"
        return self.run(command, **kwargs)

    def ctype(self, key="", dotd="", dots="", dshp="", tlen="", **kwargs):
        """Specifies the type of contour display.

        APDL Command: /CTYPE

        Parameters
        ----------
        key
            Type of display:

            0 - Standard contour display.

            1 - Isosurface display.

            2 - Particle gradient display.

            3 - Gradient triad display.

        dotd
            Maximum dot density for particle gradient display (KEY = 2).
            Density is expressed as dots per screen width (defaults to 30).

        dots
            Dot size for particle gradient display (KEY = 2).  Size is
            expressed as a fraction of the screen width (defaults to 0.0
            (single dot width)).

        dshp
            Spherical dot shape precision for particle gradient display (KEY =
            2).  (3-D options are supported only on 3-D devices):

            0 - Flat 2-D circular dot.

            1 - Flat-sided 3-D polyhedron.

            n - 3-D sphere with n (>1) polygon divisions per 90° of radius.

        tlen
            Maximum length of triads for gradient triad display (KEY = 3).
            Value is expressed as a fraction of the screen width (defaults to
            0.067).

        Notes
        -----
        Use /CTYPE,STAT to display the current settings.     Only the standard
        contour display [/CTYPE,0) and the isosurface contour display
        [/CTYPE,1] are supported by PowerGraphics [/GRAPHICS,POWER].

        This command is valid in any processor.
        """
        command = f"/CTYPE,{key},{dotd},{dots},{dshp},{tlen}"
        return self.run(command, **kwargs)

    def edge(self, wn="", key="", angle="", **kwargs):
        """Displays only the common lines ("edges") of an object.

        APDL Command: /EDGE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies. The default window
            is 1.

        key
            Edge key:

            0 - Display common lines between all adjacent element faces.

            1 - Display only the common lines between non-coplanar faces (that is, show only
                the edges).

        angle
            Largest angle between two faces for which the faces are considered
            to be coplanar (0° to 180°). Defaults to 45°. A smaller angle
            produces more edges, a larger angle produces fewer edges.

        Notes
        -----
        The ANGLE field is used in PowerGraphics to determine geometric
        discontinuities. It is a tolerance measure for the differences between
        the normals of the surfaces being considered. Values within the
        tolerance are accepted as coplanar (geometrically continuous). In
        postprocessing displays, results are not averaged across discontinuous
        surfaces.

        A surface can be displayed as an edge outline without interior detail.
        This is useful for both geometry and postprocessing displays. Element
        outlines are normally shown as solid lines for geometry and
        displacement displays. Lines common to adjacent "coplanar" element
        faces are removed from the display.  Midside nodes of elements are
        ignored.

        The /SHRINK option is ignored with the edge option.

        /EDGE is not supported for PLESOL and /ESHAPE displays when in
        PowerGraphics mode (/GRAPHICS,POWER).

        The /EDGE command is valid in any processor.
        """
        command = f"/EDGE,{wn},{key},{angle}"
        return self.run(command, **kwargs)

    def eshape(
        self, scale: Union[str, int] = "", key: MapdlInt = "", **kwargs
    ) -> Optional[str]:
        """Displays elements with shapes determined from the real constants or section definition.

        APDL Command: /ESHAPE


        Parameters
        ----------
        scale
            Scaling factor:

            * 0 - Use simple display of line and area elements. This
              value is the default.

            * 1 - Use real constants or section definition to form a
                solid shape display of the applicable elements.

            FAC - Multiply certain real constants, such as thickness,
                  by FAC (where FAC > 0.01) and use them to form a
                  solid shape display of elements.

        key
            Current shell thickness key:

            * 0 - Use current thickness in the displaced solid shape
                  display of shell elements (valid for SHELL181,
                  SHELL208, SHELL209, and SHELL281). This value is the
                  default.

            * 1 - Use initial thickness in the displaced solid shape
              display of shell elements.

        Notes
        -----
        The /ESHAPE command allows beams, shells, current sources, and
        certain special-purpose elements to be displayed as solids
        with the shape determined from the real constants or section
        types. Elements are displayed via the EPLOT command. No checks
        for valid or complete input are made for the display.

        Following are details about using this command with various
        element types:

        SOLID65 elements are displayed with internal lines that
        represent rebar sizes and orientations (requires vector mode
        [/DEVICE] with a basic type of display [/TYPE,,BASIC]). The
        rebar with the largest volume ratio in each element plots as a
        red line, the next largest as green, and the smallest as blue.

        COMBIN14, COMBIN39, and MASS21 are displayed with a graphics
        icon, with the offset determined by the real constants and
        KEYOPT settings.

        BEAM188, BEAM189, PIPE288, PIPE289 and ELBOW290 are displayed
        as solids with the shape determined via the section-definition
        commands (SECTYPE and SECDATA). The arbitrary section option
        (Subtype = ASEC) has no definite shape and appears as a thin
        rectangle to show orientation. The elements are displayed with
        internal lines representing the cross- section mesh.

        SOLID272 and SOLID273 are displayed as solids with the shape
        determined via the section-definition commands (SECTYPE and
        SECDATA).  The 2-D master plane is revolved around the
        prescribed axis of symmetry.

        Contour plots are available for these elements in
        postprocessing for PowerGraphics only (/GRAPHICS,POWER). To
        view 3-D deformed shapes for the elements, issue OUTRES,MISC
        or OUTRES,ALL for static or transient analyses. To view 3-D
        mode shapes for a modal or eigenvalue buckling analysis,
        expand the modes with element results calculation ON (Elcalc =
        YES for MXPAND).

        SOURC36, CIRCU124, and TRANS126 elements always plot using
        /ESHAPE when PowerGraphics is activated (/GRAPHICS,POWER).

        In most cases, /ESHAPE renders a thickness representation of
        your shell, plane and layered elements more readily in
        PowerGraphics (/GRAPHICS,POWER). This type of representation
        employs PowerGraphics to generate the enhanced representation,
        and will often provide no enhancement in Full Graphics
        (/GRAPHICS,FULL). This is especially true for POST1 results
        displays, where /ESHAPE is not supported for most element
        types with FULL graphics.

        When PowerGraphics is active, /ESHAPE may degrade the image if
        adjacent elements have overlapping material, such as shell
        elements which are not co-planar. Additionally, if adjacent
        elements have different thicknesses, the polygons depicting
        the connectivity between the "thicker" and "thinner" elements
        along the shared element edges may not always be displayed.

        For POST1 results displays (such as PLNSOL), the following
        limitations apply:

        Rotational displacements for beam elements are used to create
        a more realistic displacement display. When /ESHAPE is active,
        displacement plots (via PLNSOL,U,X and PLDISP, for example)
        may disagree with your PRNSOL listings. This discrepancy will
        become more noticeable when the SCALE value is not equal to
        one.

        When shell elements are not co-planar, the resulting PLNSOL
        display with /ESHAPE will actually be a PLESOL display as the
        non-coincident pseudo-nodes are not averaged. Additionally,
        /ESHAPE should not be used with coincident elements because
        the plot may incorrectly average the displacements of the
        coincident elements.

        When nodes are initially coincident and PowerGraphics is
        active, duplicate polygons are eliminated to conserve display
        time and disk space. The command may degrade the image if
        initially coincident nodes have different displacements. The
        tolerance for determining coincidence is 1E-9 times the
        model’s bounding box diagonal.

        If you want to view solution results (PLNSOL, etc.) on layered
        elements (such as SHELL181, SOLSH190, SOLID185 Layered Solid,
        SOLID186 Layered Solid, SHELL208, SHELL209, SHELL281, and
        ELBOW290), set KEYOPT(8) = 1 for the layer elements so that
        the data for all layers is stored in the results file.

        You can plot the through-thickness temperatures of elements
        SHELL131 and SHELL132 regardless of the thermal DOFs in use by
        issuing the PLNSOL,TEMP command (with PowerGraphics and
        /ESHAPE active).

        The /ESHAPE,1 and /ESHAPE,FAC commands are incompatible with
        the /CYCEXPAND command used in cyclic symmetry analyses.

        This command is valid in any processor.

        """
        warnings.warn(
            "pymapdl does not support /ESHAPE when plotting in "
            "Python using ``mapdl.eplot()``.  "
            "Use ``mapdl.eplot(vtk=False)`` "
        )
        command = f"/ESHAPE,{scale},{key}"
        return self.run(command, **kwargs)

    def facet(self, lab="", **kwargs):
        """Specifies the facet representation used to form solid model displays.

        APDL Command: /FACET

        Parameters
        ----------
        lab
            Valid labels:

            FINE - Use finer tessellation to increase the number of facets for the display.
                   Provides the best representation (but decreases speed of
                   operation).

            NORML - Use the basic number of facets for the display (default).

            COAR - Use a limited number of facets for the display. This option will increase the
                   speed of the operations, but may produce poor
                   representations for some imported models.

            WIRE - Display model with a wireframe representation (fast, but surfaces will not be
                   shown).

        Notes
        -----
        Specifies the facet (or polygon) representation used to form solid
        model displays.  Used only with the APLOT, ASUM, VPLOT, and VSUM
        commands.

        This command is valid in any processor.
        """
        command = f"/FACET,{lab}"
        return self.run(command, **kwargs)

    def gline(self, wn="", style="", **kwargs):
        """Specifies the element outline style.

        APDL Command: /GLINE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        style
            Outline key:

             0  - Solid element outlines (default)

             1  - Dashed element outlines

            -1  - No element outlines

        Notes
        -----
        Determines the element outline style.  Often used when node numbers are
        displayed to prevent element lines from overwriting node numbers.

        Unless you are using an OpenGL or Starbase driver, the dashed element
        outline option (/GLINE,WN,1) is not available in the following
        situations:

        Z-buffered displays (/TYPE,WN,6).

        Capped Z-buffered displays (/TYPE,WN,7).

        Qslice Z-buffered displays (/TYPE,WN,8).

        This command is valid in any processor.
        """
        command = f"/GLINE,{wn},{style}"
        return self.run(command, **kwargs)

    def gmarker(self, curve="", key="", incr="", **kwargs):
        """Specifies the curve marking style.

        APDL Command: /GMARKER

        Parameters
        ----------
        curve
            Curve number markers will be applied on (integer value between 1
            and 10).

        key
            Marker key:

            0 - No markers will be applied (default).

            1 - TRIANGLES will be applied.

            2 - SQUARES will be applied.

            3 - DIAMONDS  will be applied.

            4 - CROSSES will be applied.

        incr
            Determines the curve marking frequency. (a whole number value
            between 1 and 255). If INCR = 1, markers are displayed at every
            data point on the curve. If INCR = 2 then markers are displayed at
            every second data point. If INCR = 3 then they are displayed at
            every third data point.

        Notes
        -----
        The user-specified markers will not be drawn when the area under the
        curve is color-filled (/GROPT, FILL).
        """
        command = f"/GMARKER,{curve},{key},{incr}"
        return self.run(command, **kwargs)

    def gmface(self, lab="", n="", **kwargs):
        """Specifies the facet representation used to form solid models.

        APDL Command: GMFACE

        Parameters
        ----------
        lab
            Valid Labels:

            FINE - Value that determines how coarse the facets will be.

        n
            An integer value between one (small) and ten (large) that
            determines the tolerances that will be applied to the creation of
            arcs and surfaces. Ten will create many facets, which may in turn
            cause ANSYS to run very slowly. One will create fewer facets, which
            may in turn cause larger tolerance errors.
        """
        command = f"GMFACE,{lab},{n}"
        return self.run(command, **kwargs)

    def light(self, wn="", num="", int_="", xv="", yv="", zv="", refl="", **kwargs):
        """Specifies the light direction for the display window.

        APDL Command: /LIGHT

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        num
            Ambient or directional light key:

            0 - Ambient light (default).

            1 - Directional light.

        int\_
            Light intensity factor (defaults to 0.3 for ambient, 1.0 for
            directional). This option is valid only for 3-D devices).

        xv, yv, zv
            Light direction (valid only for NUM = 1).  The directional light
            source is parallel to the line from point XV, YV, ZV to the origin,
            in the global Cartesian system origin.  Defaults to the viewing
            direction [/VIEW].

        refl
            Light reflectance factor (valid only for NUM = 1 and 3-D devices).

        Notes
        -----
        Defines the light direction for the window.  Use this command only with
        3-D graphics devices or 2-D devices when Z-buffering is used [/TYPE,,(6
        or 7)].  The ambient light has no direction, only an intensity.  You
        can position the directional light source  by defining a point (in the
        global Cartesian coordinate system) representing a point along the
        light directional line.  This point, and the global Cartesian
        coordinate system origin, define the line along which the light is
        positioned looking toward the origin.  You can use any point along the
        light line; for example, both (1.,1.,1.) and (2.,2.,2.) give the same
        light effect.  For 3-D graphics devices only, the directional light
        source also has intensity and reflectance factors.

        By choosing the highest intensity ambient light for 3-D graphics
        devices (via the command /LIGHT,WN,0,1), you can nullify color shading
        and other effects of directional lighting.

        This command is valid in any processor.
        """
        command = f"/LIGHT,{wn},{num},{int_},{xv},{yv},{zv},{refl}"
        return self.run(command, **kwargs)

    def normal(self, wn="", key="", **kwargs):
        """Allows displaying area elements by top or bottom faces.

        APDL Command: /NORMAL

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        key
            Display key:

            0 - No face distinction.

            1 - Show only area elements having their positive normals directed toward the
                viewing point.

            -1 - Show only area elements having their positive normals directed away from the
                 viewing point.

        Notes
        -----
        /NORMAL allows you to select area elements and area plots by the top or
        bottom faces.  It is useful for checking the normal directions on shell
        elements.  The positive normal (element Z direction) is defined by the
        right-hand rule following the node I, J, K, L input direction.  This
        command is available only with raster or hidden-line displays, for
        WIN32 or X11 2-D displays only.

        This command is valid in any processor.
        """
        command = f"/NORMAL,{wn},{key}"
        return self.run(command, **kwargs)

    def shade(self, wn="", type_="", **kwargs):
        """Defines the type of surface shading used with Z-buffering.

        APDL Command: /SHADE

        Parameters
        ----------
        wn
            Window number (or ALL) to which command applies (defaults to 1).

        type\_
            Shading type:

            FACET or 0 - Facet shading (one color per area face) (default).

            GOURAUD or 1 - Gouraud smooth shading (smooth variation of color based on interpolated vertex
                           colors).

            PHONG or 2 - Phong smooth shading (smooth variation of color based on interpolated vertex
                         normals).

        Notes
        -----
        Defines the type of surface shading used on area, volume, and
        PowerGraphics [/GRAPHICS,POWER] displays when software Z-buffering is
        enabled [/TYPE].  This command is only functional for 2-D display
        devices.

        This command is valid in any processor.
        """
        command = f"/SHADE,{wn},{type_}"
        return self.run(command, **kwargs)

    def trlcy(self, lab="", tlevel="", n1="", n2="", ninc="", **kwargs):
        """Specifies the level of translucency.

        APDL Command: /TRLCY

        Parameters
        ----------
        lab
            Apply translucency level to the items specified by the following
            labels:

            ELEM - Elements.  Use N1, N2, NINC fields for element numbers.

            AREA - Solid model areas.  Use N1, N2, NINC fields for area numbers.

            VOLU - Solid model volumes.  Use N1, N2, NINC fields for volume numbers.

            ISURF - Isosurfaces (surfaces of constant stress, etc., value).  Translucency varies
                    with result value, to a maximum of the specified
                    translucency level.

            CM - Component group.  Use N1 for component name, ignore N2 and NINC.

            CURVE - Filled areas under curves of line graphs.  Use N1, N2, NINC fields for curve
                    numbers.

            ZCAP - If /TYPE,WN,ZCAP is the current display type, then /TRLCY,ZCAP,TLEVEL will
                   display the model in window WN with the portion of the model
                   in front of the section plane displayed at the translucency
                   level TLEVEL.

            ON, OFF - Sets the specified translucency display on or off. All other fields are
                      ignored.

        tlevel
            Translucency level:  0.0 (opaque) to 1.0 (transparent).

        n1, n2, ninc
            Used only with labels as noted above.  Apply translucency level to
            Lab items numbered N1 to N2 (defaults to N1) in steps of NINC
            (defaults to 1).  If N1 is blank or ALL, apply specified
            translucency level to entire selected range.  If Lab is CM, use
            component name for N1 and ignore N2 and NINC. A value of N1 = P
            allows you to graphically pick elements, areas, and volumes. You
            can then assign translucency levels to the entities via the picker.
            The Lab and TLEVEL fields are ignored when translucency is applied
            by picking.

        Notes
        -----
        Specifies the level of translucency for various items.  Issue
        /TRLCY,DEFA to reset the default (0) translucency levels.  This command
        is valid only on selected 2-D and 3-D graphics devices; see  in the
        Basic Analysis Guide for more information on applying translucency.

        For 2-D devices, ANSYS displays only the visible faces of the items
        being displayed.  The information behind the facing planes is not
        displayed.  Issuing the /SHRINK command will force the hardware to
        display information behind the translucent items.

        This command is valid in any processor.
        """
        command = f"/TRLCY,{lab},{tlevel},{n1},{n2},{ninc}"
        return self.run(command, **kwargs)
