"""Parse element commands"""
import re
from typing import Optional, Union
from .mapdl_types import MapdlInt


def parse_e(msg: Optional[str]) -> Optional[int]:
    """Parse create element message and return element number."""
    if msg:
        res = re.search(r"(ELEMENT\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


def parse_et(msg: Optional[str]) -> Optional[int]:
    """Parse local element type number definition message
    and return element type number.
    """
    if msg:
        res = re.search(r"(ELEMENT TYPE\s*)([0-9]+)", msg)
        if res is not None:
            return int(res.group(2))


class _MapdlElementCommands:

    def e(self, i: MapdlInt = "", j: MapdlInt = "", k: MapdlInt = "", l: MapdlInt = "", m: MapdlInt = "",
          n: MapdlInt = "", o: MapdlInt = "", p: MapdlInt = "", **kwargs) -> Optional[int]:
        """APDL Command: E

        Defines an element by node connectivity.

        Parameters
        ----------
        i
            Number of node assigned to first nodal position (node I). If I = P,
            graphical picking is enabled and all remaining command fields are
            ignored (valid only in the GUI).

        j, k, l, m, n, o, p
            Number assigned to second (node J) through eighth (node P) nodal
            position, if any.

        Notes
        -----
        Defines an element by its nodes and attribute values. Up to 8 nodes may
        be specified with the E command.  If more nodes are needed for the
        element, use the EMORE command. The number of nodes required and the
        order in which they should be specified are described in Chapter 4 of
        the Element Reference for each element type.  Elements are
        automatically assigned a number [NUMSTR] as generated. The current (or
        default) MAT, TYPE, REAL, SECNUM and ESYS attribute values are also
        assigned to the element.

        When creating elements with more than 8 nodes using this command and
        the EMORE command, it may be necessary to turn off shape checking using
        the SHPP command before issuing this command. If a valid element type
        can be created without using the additional nodes on the EMORE command,
        this command will create that element. The EMORE command will then
        modify the element to include the additional nodes. If shape checking
        is active, it will be performed before the EMORE command is issued.
        Therefore, if the shape checking limits are exceeded, element creation
        may fail before the EMORE command modifies the element into an
        acceptable shape.
        """
        command = "E,{},{},{},{},{},{},{},{}".format(i, j, k, l, m, n, o, p)
        return parse_e(self.run(command, **kwargs))

    def et(self, itype: MapdlInt = "", ename: Union[str, int] = "", kop1: MapdlInt = "", kop2: MapdlInt = "",
           kop3: MapdlInt = "", kop4: MapdlInt = "", kop5: MapdlInt = "", kop6: MapdlInt = "",
           inopr: MapdlInt = "", **kwargs) -> Optional[int]:
        """APDL Command: ET

        Defines a local element type from the element library.

        Parameters
        ----------
        itype
            Arbitrary local element type number. Defaults to 1 + current
            maximum.

        ename
            Element name (or number) as given in the element library in Chapter
            4 of the Element Reference. The name consists of a category prefix
            and a unique number, such as PIPE288.  The category prefix of the
            name (PIPE for the example) may be omitted but is displayed upon
            output for clarity. If Ename = 0, the element is defined as a null
            element.

        kop1, kop2, kop3, kop4, kop5, kop6
            KEYOPT values (1 through 6) for this element, as described in the
            Element Reference.

        inopr
            If 1, suppress all element solution printout for this element type.

        Notes
        -----
        The ET command selects an element type from the element library and
        establishes it as a local element type for the current model.
        Information derived from the element type is used for subsequent
        commands, so the ET command(s) should be issued early. (The Element
        Reference describes the available elements.)

        A special option, Ename = 0, permits the specified element type to be
        ignored during solution without actually removing the element from the
        model. Ename may be set to zero only after the element type has been
        previously defined with a nonzero Ename.  The preferred method of
        ignoring elements is to use the select commands (such as ESEL).

        KOPn are element option keys. These keys (referred to as KEYOPT(n)) are
        used to turn on certain element options for this element. These options
        are listed under "KEYOPT" in the input table for each element type in
        the Element Reference.  KEYOPT values include stiffness formulation
        options, printout controls, and various other element options. If
        KEYOPT(7) or greater is needed, input their values with the KEYOPT
        command.

        The ET command only defines an element type local to your model (from
        the types in the element library). The TYPE or similar [KATT, LATT,
        AATT, or VATT] command must be used to point to the desired local
        element type before meshing.

        To activate the ANSYS program's LS-DYNA explicit dynamic analysis
        capability,  use the ET command or its GUI equivalent to choose an
        element that works only with LS-DYNA (such as SHELL163).  Choosing LS-
        DYNA in the Preferences dialog box does not activate LS-DYNA; it simply
        makes items and options related to LS-DYNA accessible in the GUI.
        """
        command = "ET,{},{},{},{},{},{},{},{},{}".format(itype, ename, kop1, kop2, kop3, kop4, kop5, kop6, inopr)
        return parse_et(self.run(command, **kwargs))

    def ewrite(self, fname="", ext="", kappnd="", format_="", **kwargs):
        """APDL Command: EWRITE

        Writes elements to a file.

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

        kappnd
            Append key:

            0 - Rewind file before the write operation.

            1 - Append data to the end of the existing file.

        format_
            Format key:

            SHORT - I6 format (the default).

            LONG - I8 format.

        Notes
        -----
        Writes the selected elements to a file. The write operation is
        not necessary in a standard ANSYS run but is provided as
        convenience to users wanting a coded element file. If issuing
        EWRITE from ANSYS to be used in ANSYS, you must also issue
        NWRITE to store nodal information for later use. Only elements
        having all of their nodes defined (and selected) are
        written. Data are written in a coded format. The data
        description of each record is: I, J, K, L, M, N, O, P, MAT,
        TYPE, REAL, SECNUM, ESYS, IEL, where MAT, TYPE, REAL, and ESYS
        are attribute numbers, SECNUM is the beam section number, and
        IEL is the element number.

        The format is (14I6) if Format is set to SHORT and (14I8) if
        the Format is set to LONG, with one element description per
        record for elements having eight nodes of less. For elements
        having more than eight nodes, nodes nine and above are written
        on a second record with the same format.
        """
        return self.run(f"EWRITE,{fname},{ext},,{kappnd},{format_}", **kwargs)

    def etable(self, lab="", item="", comp="", option="", **kwargs):
        """APDL Command: ETABLE

        Fills a table of element values for further processing.

        Parameters
        ----------
        lab
            Any unique user defined label for use in subsequent commands and
            output headings (maximum of eight characters and not a General
            predefined Item label). Defaults to an eight character label formed
            by concatenating the first four characters of the Item and Comp
            labels. If the same as a previous user label, this result item will
            be included under the same label. Up to 200 different labels may be
            defined. The following labels are predefined and are not available
            for user-defined labels:  REFL, STAT, and ERAS.  Lab = REFL refills
            all tables previously defined with the ETABLE commands (not the
            CALC module commands) according to the latest ETABLE specifications
            and is convenient for refilling tables after the load step (SET)
            has been changed. Remaining fields will be ignored if Lab is REFL.
            Lab = STAT displays stored table values.  Lab = ERAS erases the
            entire table.

        item
            Label identifying the item. General item labels are shown in the
            table below. Some items also require a component label. Character
            parameters may be used. Item = ERAS erases a Lab column.

        comp
            Component of the item (if required). General component labels are
            shown in the table below. Character parameters may be used.

        option
            Option for storing element table data:

            MIN - Store minimum element nodal value of the specified item component.

            MAX - Store maximum element nodal value of the specified item component.

            AVG - Store averaged element centroid value of the specified item component
                  (default).

        Notes
        -----
        The ETABLE command defines a table of values per element (the element
        table) for use in further processing. The element table is organized
        similar to spreadsheet, with rows representing all selected elements
        and columns consisting of result items which have been moved into the
        table (Item,Comp) via ETABLE. Each column of data is identified by a
        user-defined label (Lab) for listings and displays.

        After entering the data into the element table, you are not limited to
        merely listing or displaying your data (PLESOL, PRESOL, etc.). You may
        also perform many types of operations on your data, such as adding or
        multiplying columns (SADD, SMULT), defining allowable stresses for
        safety calculations (SALLOW), or multiplying one column by another
        (SMULT).  See Getting Started in theBasic Analysis Guide for more
        information.

        Various results data can be stored in the element table. For example,
        many items for an element are inherently single-valued (one value per
        element). The single-valued items include: SERR, SDSG, TERR, TDSG,
        SENE, SEDN, TENE, KENE, AENE, JHEAT, JS, VOLU, and CENT. All other
        items are multivalued (varying over the element, such that there is a
        different value at each node). Because only one value is stored in the
        element table per element, an average value (based on the number of
        contributing nodes) is calculated for multivalued items. Exceptions to
        this averaging procedure are FMAG and all element force items, which
        represent the sum only of the contributing nodal values.

        Two methods of data access can be used with the ETABLE command. The
        method you select depends upon the type of data that you want to store.
        Some results can be accessed via a generic label (Component Name
        method), while others require a label and number (Sequence Number
        method).

        The Component Name method is used to access the General element data
        (that is, element data which is generally available to most element
        types or groups of element types). All of the single-valued items and
        some of the more general multivalued items are accessible with the
        Component Name method.  Various element results depend on the
        calculation method and the selected results location (AVPRIN, RSYS,
        LAYER, SHELL, and ESEL).

        Although nodal data is readily available for listings and displays
        (PRNSOL, PLNSOL) without using the element table, you may also use the
        Component Name method to enter these results into the element table for
        further "worksheet" manipulation. (See Getting Started in theBasic
        Analysis Guide for more information.) A listing of the General Item and
        Comp labels for the Component Name method is shown below.

        The Sequence Number method allows you to view results for data that is
        not averaged (such as pressures at nodes, temperatures at integration
        points, etc.), or data that is not easily described in a generic
        fashion (such as all derived data for structural line elements and
        contact elements, all derived data for thermal line elements, layer
        data for layered elements, etc.). A table illustrating the Items (such
        as LS, LEPEL, LEPTH, SMISC, NMISC, SURF, etc.) and corresponding
        sequence numbers for each element is shown in the Output Data section
        of each element description found in the Element Reference.

        Some element table data are reported in the results coordinate system.
        These include all component results (for example, UX, UY, etc.; SX, SY,
        etc.). The solution writes component results in the database and on the
        results file in the solution coordinate system. When you issue the
        ETABLE command, these results are then transformed into the results
        coordinate system (RSYS) before being stored in the element table. The
        default results coordinate system is global Cartesian (RSYS,0).  All
        other data are retrieved from the database and stored in the element
        table with no coordinate transformation.

        Use the PRETAB, PLETAB, or ETABLE,STAT commands to display the stored
        table values. Issue ETABLE,ERAS to erase the entire table. Issue
        ETABLE,Lab,ERAS to erase a Lab column.

        When the GUI is on, if a Delete operation in a Define Element Table
        Data dialog box writes this command to a log file (Jobname.LOG or
        Jobname.LGW), you will observe that Lab is blank, Item = ERASE, and
        Comp is an integer number. In this case, the GUI has assigned a value
        of Comp that corresponds to the location of a chosen variable name in
        the dialog box's list. It is not intended that you type in such a
        location value for Comp in a session.  However, a file that contains a
        GUI-generated ETABLE command of this form can be used for batch input
        or for use with the /INPUT command.

        The element table data option (Option) is not available for all output
        items. See the table below for supported items.

        Table: 135:: : ETABLE - General Item and Component Labels
        """
        command = "ETABLE,%s,%s,%s,%s" % (str(lab), str(item), str(comp), str(option))
        return self.run(command, **kwargs)

    def eusort(self, **kwargs):
        """APDL Command: EUSORT

        Restores original order of the element table.

        Notes
        -----
        Changing the selected element set [ESEL] also restores the original
        element order.
        """
        command = "EUSORT,"
        return self.run(command, **kwargs)

    def edtp(self, option="", value1="", value2="", **kwargs):
        """APDL Command: EDTP

        Plots explicit elements based on their time step size.

        Parameters
        ----------
        option
             Plotting option (default = 1).

            1 - Plots the elements with the smallest time step sizes. The number of elements
                plotted and listed is equal to VALUE1 (which defaults to 100).
                Each element is shaded red or yellow based on its time step
                value (see "Notes" for details).

            2 - Produces the same plot as for OPTION = 1, and also produces a list of the
                plotted elements and their corresponding time step values.

            3 - Produces a plot similar to OPTION = 1, except that all selected elements are
                plotted. Elements beyond the first VALUE1 elements are blue and
                translucent. The amount of translucency is specified by VALUE2.
                This option also produces a list of the first VALUE1 elements
                with their corresponding time step values.

        value1
            Number of elements to be plotted and listed (default = 100). For
            example, if VALUE1 = 10, only the elements with the 10 smallest
            time step sizes are plotted and listed.

        value2
            Translucency level ranging from 0 to 1 (default = 0.9). VALUE2 is
            only used when OPTION = 3, and only for the elements plotted in
            blue. To plot these elements as non-translucent, set VALUE2 = 0.

        Notes
        -----
        EDTP invokes an ANSYS macro that plots and lists explicit elements
        based on their time step size. For OPTION = 1 or 2, the number of
        elements plotted is equal to VALUE1 (default = 100). For OPTION = 3,
        all selected elements are plotted.

        The elements are shaded red, yellow, or blue based on their time step
        size. Red represents the smallest time step sizes, yellow represents
        the intermediate time step sizes, and blue represents the largest time
        step sizes. For example, if you specify VALUE1 = 30, and if T1 is the
        smallest critical time step of all elements and T30 is the time step of
        the 30th smallest element, then the elements are shaded as follows:

        Translucent blue elements only appear when OPTION = 3.

        This command is also valid in PREP7.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "EDTP,%s,%s,%s" % (str(option), str(value1), str(value2))
        return self.run(command, **kwargs)

    def estif(self, kmult="", **kwargs):
        """APDL Command: ESTIF

        Specifies the matrix multiplier for deactivated elements.

        Parameters
        ----------
        kmult
            Stiffness matrix multiplier for deactivated elements (defaults to
            1.0E-6).

        Notes
        -----
        Specifies the stiffness matrix multiplier for elements deactivated with
        the EKILL command (birth and death).

        This command is also valid in PREP7.
        """
        command = "ESTIF,%s" % (str(kmult))
        return self.run(command, **kwargs)

    def emodif(self, iel="", stloc="", i1="", i2="", i3="", i4="", i5="",
               i6="", i7="", i8="", **kwargs):
        """APDL Command: EMODIF

        Modifies a previously defined element.

        Parameters
        ----------
        iel
            Modify nodes and/or attributes for element number IEL.  If ALL,
            modify all selected elements [ESEL].  If IEL = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI). A component name may also be substituted for IEL.

        stloc
            Starting location (n) of first node to be modified or the attribute
            label.

        i1, i2, i3, . . . , i8
            Replace the previous node numbers assigned to this element with
            these corresponding values. A (blank) retains the previous value
            (except in the I1 field, which resets the STLOC node number to
            zero).

        Notes
        -----
        The nodes and/or attributes (MAT, TYPE, REAL, ESYS, and SECNUM values)
        of an existing element may be changed with this command.
        """
        command = "EMODIF,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(iel), str(stloc), str(i1), str(i2), str(i3), str(i4), str(i5), str(i6), str(i7), str(i8))
        return self.run(command, **kwargs)

    def emore(self, q="", r="", s="", t="", u="", v="", w="", x="", **kwargs):
        """APDL Command: EMORE

        Adds more nodes to the just-defined element.

        Parameters
        ----------
        q, r, s, t, u, v, w, x
            Numbers of nodes typically assigned to ninth (node Q) through
            sixteenth (node X) nodal positions, if any. If Q = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

        Notes
        -----
        Repeat EMORE command for up to 4 additional nodes (20 maximum). Nodes
        are added after the last nonzero node of the element.  Node numbers
        defined with this command may be zeroes.
        """
        command = "EMORE,%s,%s,%s,%s,%s,%s,%s,%s" % (str(q), str(r), str(s), str(t), str(u), str(v), str(w), str(x))
        return self.run(command, **kwargs)

    def esol(self, nvar="", elem="", node="", item="", comp="", name="",
             **kwargs):
        """APDL Command: ESOL

        Specifies element data to be stored from the results file.

        Parameters
        ----------
        nvar
            Arbitrary reference number assigned to this variable (2 to NV
            [NUMVAR]). Overwrites any existing results for this variable.

        elem
            Element for which data are to be stored. If ELEM = P, graphical
            picking is enabled (valid only in the GUI).

        node
            Node number on this element for which data are to be stored. If
            blank, store the average element value (except for FMAG values,
            which are summed instead of averaged). If NODE = P, graphical
            picking is enabled (valid only in the GUI).

        item
            Label identifying the item. General item labels are shown in
            Table 134: ESOL - General Item and Component Labels below. Some
            items also require a component label.

        comp
            Component of the item (if required). General component labels are
            shown in Table 134: ESOL - General Item and Component Labels below.
            If Comp is a sequence number (n), the NODE field will be ignored.

        name
            Thirty-two character name for identifying the item on the printout
            and displays.  Defaults to a label formed by concatenating the
            first four characters of the Item and Comp labels.

        Notes
        -----
        See Table: 134:: ESOL - General Item and Component Labels for a list of
        valid item and component labels for element (except line element)
        results.

        The ESOL command defines element results data to be stored from a
        results file (FILE). Not all items are valid for all elements. To see
        the available items for a given element, refer to the input and output
        summary tables in the documentation for that element.

        Two methods of data access are available via the ESOL command. You can
        access some simply by using a generic label (component name method),
        while others require a label and number (sequence number method).

        Use the component name method to access general element data (that is,
        element data generally available to most element types or groups of
        element types).

        The sequence number method is required for data that is not averaged
        (such as pressures at nodes and temperatures at integration points), or
        data that is not easily described in a generic fashion (such as all
        derived data for structural line elements and contact elements, all
        derived data for thermal line elements, and layer data for layered
        elements).

        Element results are in the element coordinate system, except for
        layered elements where results are in the layer coordinate system.
        Element forces and moments are in the nodal coordinate system. Results
        are obtainable for an element at a specified node. Further location
        specifications can be made for some elements via the SHELL, LAYERP26,
        and FORCE commands.

        Table: 134:: : ESOL - General Item and Component Labels

        For more information on the meaning of contact status and its possible
        values, see Reviewing Results in POST1 in the Contact Technology Guide.
        """
        command = "ESOL,%s,%s,%s,%s,%s,%s" % (str(nvar), str(elem), str(node), str(item), str(comp), str(name))
        return self.run(command, **kwargs)

    def eshape(self, scale="", key="", **kwargs):
        """APDL Command: /ESHAPE

        Displays elements with shapes determined from the real constants or
        section definition.

        Parameters
        ----------
        scale
            Scaling factor:

            0 - Use simple display of line and area elements. This value is the default.

            1 - Use real constants or section definition to form a solid shape display of the
                applicable elements.

            FAC - Multiply certain real constants, such as thickness, by FAC (where FAC > 0.01)
                  and use them to form a solid shape display of elements.

        key
            Current shell thickness key:

            0 - Use current thickness in the displaced solid shape display of shell elements
                (valid for SHELL181, SHELL208, SHELL209, and SHELL281). This
                value is the default.

            1 - Use initial thickness in the displaced solid shape display of shell elements.

        Notes
        -----
        The /ESHAPE command allows beams, shells, current sources, and certain
        special-purpose elements to be displayed as solids with the shape
        determined from the real constants or section types. Elements are
        displayed via the EPLOT command. No checks for valid or complete input
        are made for the display.

        Following are details about using this command with various element
        types:

        SOLID65 elements are displayed with internal lines that represent rebar
        sizes and orientations (requires vector mode [/DEVICE] with a basic
        type of display [/TYPE,,BASIC]). The rebar with the largest volume
        ratio in each element plots as a red line, the next largest as green,
        and the smallest as blue.

        COMBIN14, COMBIN39, and MASS21 are displayed with a graphics icon, with
        the offset determined by the real constants and KEYOPT settings.

        BEAM188, BEAM189, PIPE288, PIPE289 and ELBOW290 are displayed as solids
        with the shape determined via the section-definition commands (SECTYPE
        and SECDATA). The arbitrary section option (Subtype = ASEC) has no
        definite shape and appears as a thin rectangle to show orientation. The
        elements are displayed with internal lines representing the cross-
        section mesh.

        SOLID272 and SOLID273 are displayed as solids with the shape determined
        via the section-definition commands (SECTYPE and SECDATA).  The 2-D
        master plane is revolved around the prescribed axis of symmetry.

        Contour plots are available for these elements in postprocessing for
        PowerGraphics only (/GRAPHICS,POWER). To view 3-D deformed shapes for
        the elements, issue OUTRES,MISC or OUTRES,ALL for static or transient
        analyses. To view 3-D mode shapes for a modal or eigenvalue buckling
        analysis, expand the modes with element results calculation ON (Elcalc
        = YES for MXPAND).

        SOURC36, CIRCU124, and TRANS126 elements always plot using /ESHAPE when
        PowerGraphics is activated (/GRAPHICS,POWER).

        In most cases, /ESHAPE renders a thickness representation of your
        shell, plane and layered elements more readily in PowerGraphics
        (/GRAPHICS,POWER). This type of representation employs PowerGraphics to
        generate the enhanced representation, and will often provide no
        enhancement in Full Graphics (/GRAPHICS,FULL). This is especially true
        for POST1 results displays, where /ESHAPE is not supported for most
        element types with FULL graphics.

        When PowerGraphics is active, /ESHAPE may degrade the image if adjacent
        elements have overlapping material, such as shell elements which are
        not co-planar. Additionally, if adjacent elements have different
        thicknesses, the polygons depicting the connectivity between the
        "thicker" and "thinner" elements along the shared element edges may not
        always be displayed.

        For POST1 results displays (such as PLNSOL), the following limitations
        apply:

        Rotational displacements for beam elements are used to create a more
        realistic displacement display. When /ESHAPE is active, displacement
        plots (via PLNSOL,U,X and PLDISP, for example) may disagree with your
        PRNSOL listings. This discrepancy will become more noticeable when the
        SCALE value is not equal to one.

        When shell elements are not co-planar, the resulting PLNSOL display
        with /ESHAPE will actually be a PLESOL display as the non-coincident
        pseudo-nodes are not averaged. Additionally, /ESHAPE should not be used
        with coincident elements because the plot may incorrectly average the
        displacements of the coincident elements.

        When nodes are initially coincident and PowerGraphics is active,
        duplicate polygons are eliminated to conserve display time and disk
        space. The command may degrade the image if initially coincident nodes
        have different displacements. The tolerance for determining coincidence
        is 1E-9 times the model’s bounding box diagonal.

        If you want to view solution results (PLNSOL, etc.) on layered elements
        (such as SHELL181, SOLSH190, SOLID185 Layered Solid, SOLID186 Layered
        Solid, SHELL208, SHELL209, SHELL281, and ELBOW290), set KEYOPT(8) = 1
        for the layer elements so that the data for all layers is stored in the
        results file.

        You can plot the through-thickness temperatures of elements SHELL131
        and SHELL132 regardless of the thermal DOFs in use by issuing the
        PLNSOL,TEMP command (with PowerGraphics and /ESHAPE active).

        The /ESHAPE,1 and /ESHAPE,FAC commands are incompatible with the
        /CYCEXPAND command used in cyclic symmetry analyses.

        This command is valid in any processor.
        """
        command = "/ESHAPE,%s,%s" % (str(scale), str(key))
        return self.run(command, **kwargs)

    def etype(self, **kwargs):
        """APDL Command: ETYPE

        Specifies "Element types" as the subsequent status topic.

        Notes
        -----
        This is a status [STAT] topic command. Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu> List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = "ETYPE,"
        return self.run(command, **kwargs)

    def etcontrol(self, eltech="", eldegene="", **kwargs):
        """APDL Command: ETCONTROL

        Control the element technologies used in element formulation (for
        applicable elements).

        Parameters
        ----------
        eltech
            Element technology control:

            SUGGESTION - The program offers a suggestion for the best element technology before solving.
                         If necessary, mixed u-P (KEYOPT(6)) is also included
                         and reset. This behavior is the default.

            SET - The program informs you of the best settings and resets any applicable KEYOPT
                  settings automatically. This action overrides any previous
                  manual settings.

            OFF - Deactivates automatic selection of element technology. No suggestions are
                  issued, and no automatic resetting occurs.

        eldegene
            Element degenerated shape control:

            ON - If element shapes are degenerated, the degenerated shape function is employed
                 and enhanced strain, simplified enhanced strain, and B-bar
                 formulations are turned off (default).

            OFF - If element shapes are degenerated, regular shape functions are still used, and
                  the specified element technologies (e.g., enhanced strain,
                  B-bar, uniform reduced integration) are still used.

        Notes
        -----
        The command default is ETCONTROL,SUGGESTION,ON.

        This command is valid for elements SHELL181, PLANE182, PLANE183,
        SOLID185, SOLID186, SOLID187, BEAM188, BEAM189, SHELL208, SHELL209,
        PLANE223, SOLID226, SOLID227, REINF264, SOLID272, SOLID273, SHELL281,
        SOLID285, PIPE288, PIPE289, ELBOW290.

        For more information, see Automatic Selection of Element Technologies
        and Formulations in the Element Reference.
        """
        command = "ETCONTROL,%s,%s" % (str(eltech), str(eldegene))
        return self.run(command, **kwargs)

    def enorm(self, enum="", **kwargs):
        """APDL Command: ENORM

        Reorients shell element normals or line element node connectivity.

        Parameters
        ----------
        enum
            Element number having the normal direction that the reoriented
            elements are to match. If ENUM = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the
            GUI).

        Notes
        -----
        Reorients shell elements so that their outward normals are consistent
        with that of a specified element. ENORM can also be used to reorder
        nodal connectivity of line elements so that their nodal ordering is
        consistent with that of a specified element.

        For shell elements, the operation reorients the element by reversing
        and shifting the node connectivity pattern. For example, for a 4-node
        shell element, the nodes in positions I, J, K and L of the original
        element are placed in positions J, I, L and K of the reoriented
        element. All 3-D shell elements in the selected set are considered for
        reorientation, and no element is reoriented more than once during the
        operation. Only shell elements adjacent to the lateral (side) faces are
        considered.

        The command reorients the shell element normals on the same panel as
        the specified shell element. A panel is the geometry defined by a
        subset of shell elements bounded by free edges or T-junctions (anywhere
        three or more shell edges share common nodes).

        Reorientation progresses within the selected set until either of the
        following conditions is true:

        The edge of the model is reached.

        More than two elements (whether selected or unselected) are adjacent to
        a lateral face.

        In situations where unselected elements might undesirably cause case b
        to control, consider using ENSYM,0,,0,ALL instead of ENORM.  It is
        recommended that reoriented elements be displayed and graphically
        reviewed.

        You cannot use the ENORM command to change the normal direction of any
        element that has a body or surface load. We recommend that you apply
        all of your loads only after ensuring that the element normal
        directions are acceptable.

        Real constant values are not reoriented and may be invalidated by an
        element reversal.
        """
        command = "ENORM,%s" % (str(enum))
        return self.run(command, **kwargs)

    def etdele(self, ityp1="", ityp2="", inc="", **kwargs):
        """APDL Command: ETDELE

        Deletes element types.

        Parameters
        ----------
        ityp1, ityp2, inc
            Deletes element types from ITYP1 to ITYP2 (defaults to ITYP1) in
            steps of INC (defaults to 1). If ITYP1 = ALL, ITYP2 and INC are
            ignored and all element types are deleted.  Element types are
            defined with the ET command.
        """
        command = "ETDELE,%s,%s,%s" % (str(ityp1), str(ityp2), str(inc))
        return self.run(command, **kwargs)

    def edele(self, iel1="", iel2="", inc="", **kwargs):
        """APDL Command: EDELE

        Deletes selected elements from the model.

        Parameters
        ----------
        iel1, iel2, inc
            Delete elements from IEL1 to IEL2 (defaults to IEL1) in steps of
            INC (defaults to 1). If IEL1 = ALL, IEL2 and INC are ignored and
            all selected elements [ESEL] are deleted. If IEL1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted
            for IEL1 (IEL2 and INC are ignored).

        Notes
        -----
        Deleted elements are replaced by null or "blank" elements. Null
        elements are used only for retaining the element numbers so that the
        element numbering sequence for the rest of the model is not changed by
        deleting elements. Null elements may be removed (although this is not
        necessary) with the NUMCMP command. If related element data (pressures,
        etc.) are also to be deleted, delete that data before deleting the
        elements. EDELE is for unattached elements only. You can use the xCLEAR
        family of commands to remove any attached elements from the database.
        """
        command = "EDELE,%s,%s,%s" % (str(iel1), str(iel2), str(inc))
        return self.run(command, **kwargs)

    def extopt(self, lab="", val1="", val2="", val3="", val4="", **kwargs):
        """APDL Command: EXTOPT

        Controls options relating to the generation of volume elements from
        area elements.

        Parameters
        ----------
        lab
            Label identifying the control option. The meanings of Val1, Val2,
            and Val3 will vary depending on Lab.

            ON - Sets carryover of the material attributes, real constant attributes, and
                 element coordinate system attributes of the pattern area
                 elements to the generated volume elements.  Sets the pattern
                 area mesh to clear when volume generations are done. Val1,
                 Val2, and Val3 are ignored.

            OFF - Removes all settings associated with this command. Val1, Val2, and Val3 are
                  ignored.

            STAT - Shows all settings associated with this command. Val1, Val2, Val3, and Val4 are
                   ignored.

            ATTR - Sets carryover of particular pattern area attributes (materials, real
                   constants, and element coordinate systems) of the pattern
                   area elements to the generated volume elements. (See 2.)
                   Val1 can be:

            0 - Sets volume elements to use current MAT command settings.

            1 - Sets volume elements to use material attributes of the pattern area elements.

            Val2 can be:  - 0

            Sets volume elements to use current REAL command settings. - 1

            Sets volume elements to use real constant attributes of the pattern area elements. - Val3 can be:

            0 - Sets volume elements to use current ESYS command settings.

            1 - Sets volume elements to use element coordinate system attributes of the pattern
                area elements.

            Val4 can be:  - 0

            Sets volume elements to use current SECNUM command settings. - 1

            Sets volume elements to use section attributes of the pattern area elements. -

            ESIZE - Val1 sets the number of element divisions in the direction of volume generation
                    or volume sweep. For VDRAG and VSWEEP, Val1 is overridden
                    by the LESIZE command NDIV setting. Val2 sets the spacing
                    ratio (bias) in the direction of volume generation or
                    volume sweep. If positive, Val2 is the nominal ratio of
                    last division size to first division size (if > 1.0, sizes
                    increase, if < 1.0, sizes decrease). If negative, Val2 is
                    the nominal ratio of center division(s) size to end
                    divisions size. Ratio defaults to 1.0 (uniform spacing).
                    Val3 and Val4 are ignored.

            ACLEAR - Sets clearing of pattern area mesh. (See 3.) Val1 can be:

            0 - Sets pattern area to remain meshed when volume generation is done.

            1 - Sets pattern area mesh to clear when volume generation is done. Val2, Val3 ,
                and Val4 are ignored.

            VSWE - Indicates that volume sweeping options will be set using Val1 and Val2.
                   Settings specified with EXTOPT,VSWE will be used the next
                   time the VSWEEP command is invoked. If Lab = VSWE, Val1
                   becomes a label. Val1 can be:

            AUTO - Indicates whether you will be prompted for the source and target used by VSWEEP
                   or if VSWE should automatically determine the source and
                   target. If Val1 = AUTO, Val2 is ON by default. VSWE will
                   automatically determine the source and target for VSWEEP.
                   You will be allowed to pick more than one volume for
                   sweeping. When Val2 = OFF, the user will be prompted for the
                   source and target for VSWEEP. You will only be allowed to
                   pick one volume for sweeping.

            TETS - Indicates whether VSWEEP will tet mesh non-sweepable volumes or leave them
                   unmeshed. If Val1 = TETS, Val2 is OFF by default. Non-
                   sweepable volumes will be left unmeshed. When Val2 = ON, the
                   non-sweepable volumes will be tet meshed if the assigned
                   element type supports tet shaped elements.

        val1, val2, val3, val4
            Additional input values as described under each option for Lab.

        Notes
        -----
        EXTOPT controls options relating to the generation of volume elements
        from pattern area elements using the VEXT, VROTAT, VOFFST, VDRAG, and
        VSWEEP commands.  (When using VSWEEP,  the pattern area is referred to
        as the source area.)

        Enables carryover of the attributes  of the pattern area elements to
        the generated volume elements when you are using VEXT, VROTAT, VOFFST,
        or VDRAG. (When using VSWEEP, since the volume already exists, use the
        VATT command to assign attributes before sweeping.)

        When you are using VEXT, VROTAT, VOFFST, or VDRAG, enables clearing of
        the pattern area mesh when volume generations are done. (When you are
        using VSWEEP, if selected, the area meshes on the pattern (source),
        target, and/or side areas clear when volume sweeping is done.)

        Neither EXTOPT,VSWE,AUTO nor EXTOPT,VSWE,TETS will be affected by
        EXTOPT,ON or EXTOPT, OFF.
        """
        command = "EXTOPT,%s,%s,%s,%s,%s" % (str(lab), str(val1), str(val2), str(val3), str(val4))
        return self.run(command, **kwargs)

    def ereinf(self, **kwargs):
        """APDL Command: EREINF

        Generates reinforcing elements from selected existing (base) elements.

        Notes
        -----
        The EREINF command generates reinforcing elements (REINF264 and
        REINF265) directly from selected base elements (that is, existing
        standard elements in your model). The command scans all selected base
        elements and generates (if necessary) a compatible reinforcing element
        type for each base element. (ANSYS allows a combination of different
        base element types.)

        Although predefining the reinforcing element type (ET) is not required,
        you must define the reinforcing element section type (SECTYPE);
        otherwise, ANSYS cannot generate the reinforcing element.

        The EREINF command does not create new nodes. The reinforcing elements
        and the base elements share the common nodes.

        Elements generated by this command are not associated with the solid
        model.

        After the EREINF command executes, you can issue ETLIST, ELIST, and
        EPLOT commands to verify the newly created reinforcing element types
        and elements.

        Reinforcing elements do not account for any subsequent modifications
        made to the base elements. ANSYS, Inc. recommends issuing the EREINF
        command only after the base elements are finalized. If you delete or
        modify base elements (via EDELE, EMODIF, ETCHG, EMID, EORIENT, NUMMRG,
        or NUMCMP commands, for example), remove all affected reinforcing
        elements and reissue the EREINF command to avoid inconsistencies.
        """
        command = "EREINF,"
        return self.run(command, **kwargs)

    def egen(self, itime="", ninc="", iel1="", iel2="", ieinc="", minc="",
             tinc="", rinc="", cinc="", sinc="", dx="", dy="", dz="",
             **kwargs):
        """APDL Command: EGEN

        Generates elements from an existing pattern.

        Parameters
        ----------
        itime, ninc
            Do this generation operation a total of ITIMEs, incrementing all
            nodes in the given pattern by NINC each time after the first. ITIME
            must be >1 if generation is to occur. NINC may be positive, zero,
            or negative. If DX, DY, and/or DZ is specified, NINC should be set
            so any existing nodes (as on NGEN) are not overwritten.

        iel1, iel2, ieinc
            Generate elements from selected pattern beginning with IEL1 to IEL2
            (defaults to IEL1) in steps of IEINC (defaults to 1). If IEL1 is
            negative, IEL2 and IEINC are ignored and the last |IEL1| elements
            (in sequence backward from the maximum element number) are used as
            the pattern to be repeated.  If IEL1 = ALL, IEL2 and IEINC are
            ignored and use all selected elements [ESEL] as pattern to be
            repeated. If P1 = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI).  A component
            name may also be substituted for IEL1 (IEL2 and INC are ignored).

        minc
            Increment material number of all elements in the given pattern by
            MINC each time after the first.

        tinc
            Increment type number by TINC.

        rinc
            Increment real constant table number by RINC.

        cinc
            Increment element coordinate system number by CINC.

        sinc
            Increment section ID number by SINC.

        dx, dy, dz
            Define nodes that do not already exist but are needed by generated
            elements (as though the NGEN,ITIME,INC,NODE1,,,DX,DY,DZ were issued
            before EGEN). Zero is a valid value. If blank, DX, DY, and DZ are
            ignored.

        Notes
        -----
        A pattern may consist of any number of previously defined elements. The
        MAT, TYPE, REAL, ESYS, and SECNUM numbers of the new elements are based
        upon the elements in the pattern and not upon the current specification
        settings.

        You can use the EGEN command to generate interface elements (INTER192,
        INTER193, INTER194, and INTER195) directly. However, because interface
        elements require that the element connectivity be started from the
        bottom surface, you must make sure that you use the correct element
        node connectivity. See the element descriptions for INTER192, INTER193,
        INTER194, and INTER195 for the correct element node definition.
        """
        command = "EGEN,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(itime), str(ninc), str(iel1), str(iel2), str(ieinc), str(minc), str(tinc), str(rinc), str(cinc), str(sinc), str(dx), str(dy), str(dz))
        return self.run(command, **kwargs)

    def ealive(self, elem="", **kwargs):
        """APDL Command: EALIVE

        Reactivates an element (for the birth and death capability).

        Parameters
        ----------
        elem
            Element to be reactivated:

            ALL  - Reactivates all selected elements (ESEL).

            P  - Enables graphical picking of elements. All remaining command fields are
                 ignored. (Valid only in the ANSYS GUI.)

            Comp - Specifies a component name.

        Notes
        -----
        Reactivates the specified element when the birth and death capability
        is being used. An element can be reactivated only after it has been
        deactivated (EKILL).

        Reactivated elements have a zero strain (or thermal heat storage, etc.)
        state.

        ANSYS, Inc. recommends using the element deactivation/reactivation
        procedure for analyses involving linear elastic materials only. Do not
        use element deactivation/reactivation in analyses involving time-
        dependent materials, such as viscoelasticity, viscoplasticity, and
        creep analysis.

        This command is also valid in PREP7.
        """
        command = "EALIVE,%s" % (str(elem))
        return self.run(command, **kwargs)

    def escheck(self, sele="", levl="", defkey="", **kwargs):
        """APDL Command: ESCHECK

        Perform element shape checking for a selected element set.

        Parameters
        ----------
        sele
            Specifies whether to select elements for checking:

            (blank) - List all warnings/errors from element shape checking.

            ESEL - Select the elements based on the .Levl criteria specified below.

        levl
            WARN

            WARN - Select elements producing warning and error messages.

            ERR - Select only elements producing error messages (default).

        defkey
            Specifies whether check should be performed on deformed element
            shapes. .

            0 - Do not update node coordinates before performing shape checks (default).

            1 - Update node coordinates using the current set of deformations in the database.

        Notes
        -----
        Shape checking will occur according to the current SHPP settings.
        Although ESCHECK is valid in all processors, Defkey  uses the current
        results in the database. If no results are available a warning will be
        issued.

        This command is also valid in PREP7, SOLUTION and POST1.
        """
        command = "ESCHECK,%s,%s,%s" % (str(sele), str(levl), str(defkey))
        return self.run(command, **kwargs)

    def esys(self, kcn="", **kwargs):
        """APDL Command: ESYS

        Sets the element coordinate system attribute pointer.

        Parameters
        ----------
        kcn
            Coordinate system number:

            0 - Use element coordinate system orientation as defined (either by default or by
                KEYOPT setting) for the element (default).

            N - Use element coordinate system orientation based on local coordinate system N
                (where N must be greater than 10). For global system 0, 1, or
                2, define a local system N parallel to appropriate system with
                the LOCAL or CS command (for example: LOCAL,11,1).

        Notes
        -----
        Identifies the local coordinate system to be used to define the element
        coordinate system of subsequently defined elements. Used only with area
        and volume elements. For non-layered volume elements, the local
        coordinate system N is simply assigned to be the element coordinate
        system. For shell and layered volume elements, the x and y axes of the
        local coordinate system N are projected onto the shell or layer plane
        to determine the element coordinate system. See Understanding the
        Element Coordinate System for more details. N refers to the coordinate
        system reference number (KCN) defined using the LOCAL (or similar)
        command. Element coordinate system numbers may be displayed [/PNUM].
        """
        command = "ESYS,%s" % (str(kcn))
        return self.run(command, **kwargs)

    def eslv(self, type_="", **kwargs):
        """APDL Command: ESLV

        Selects elements associated with the selected volumes.

        Parameters
        ----------
        type_
            Label identifying the type of element selected:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        Selects volume elements belonging to meshed [VMESH], selected [VSEL]
        volumes.

        This command is valid in any processor.
        """
        command = "ESLV,%s" % (str(type_))
        return self.run(command, **kwargs)

    def esla(self, type_="", **kwargs):
        """APDL Command: ESLA

        Selects those elements associated with the selected areas.

        Parameters
        ----------
        type_
            Label identifying the type of element select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        Selects area elements belonging to meshed [AMESH], selected [ASEL]
        areas.

        This command is valid in any processor.
        """
        command = "ESLA,%s" % (str(type_))
        return self.run(command, **kwargs)

    def errang(self, emin="", emax="", einc="", **kwargs):
        """APDL Command: ERRANG

        Specifies the element range to be read from a file.

        Parameters
        ----------
        emin, emax, einc
            Elements with numbers from EMIN (defaults to 1) to EMAX (defaults
            to 99999999) in steps of EINC (defaults to 1) will be read.

        Notes
        -----
        Defines the element number range to be read [EREAD] from the element
        file. If a range is also implied from the NRRANG command, only those
        elements satisfying both ranges will be read.
        """
        command = "ERRANG,%s,%s,%s" % (str(emin), str(emax), str(einc))
        return self.run(command, **kwargs)

    def erefine(self, ne1="", ne2="", ninc="", level="", depth="", post="",
                retain="", **kwargs):
        """APDL Command: EREFINE

        Refines the mesh around specified elements.

        Parameters
        ----------
        ne1, ne2, ninc
            Elements (NE1 to NE2 in increments of NINC) around which the mesh
            is to be refined. NE2 defaults to NE1, and NINC defaults to 1. If
            NE1 = ALL, NE2 and NINC are ignored and all selected elements are
            used for refinement. If NE1 = P, graphical picking is enabled and
            all remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for NE1 (NE2 and NINC are
            ignored).

        level
            Amount of refinement to be done. Specify the value of LEVEL as an
            integer from 1 to 5, where a value of 1 provides minimal
            refinement, and a value of 5 provides maximum refinement (defaults
            to 1).

        depth
            Depth of mesh refinement in terms of number of elements outward
            from the indicated elements, NE1 to NE2 (defaults to 0).

        post
            Type of postprocessing to be done after element splitting, in order
            to improve element quality:

            OFF - No postprocessing will be done.

            SMOOTH - Smoothing will be done. Node locations may change.

            CLEAN - Smoothing and cleanup will be done. Existing elements may be deleted, and node
                    locations may change (default).

        retain
            Flag indicating whether quadrilateral elements must be retained in
            the refinement of an all-quadrilateral mesh. (The ANSYS program
            ignores the RETAIN argument when you are refining anything other
            than a quadrilateral mesh.)

            ON - The final mesh will be composed entirely of quadrilateral elements, regardless
                 of the element quality (default).

            OFF - The final mesh may include some triangular elements in order to maintain
                  element quality and provide transitioning.

        Notes
        -----
        EREFINE performs local mesh refinement around the specified elements.
        By default, the surrounding elements are split to create new elements
        with 1/2 the edge length of the original elements (LEVEL = 1).

        EREFINE refines all area elements and tetrahedral volume elements that
        are adjacent to the specified elements. Any volume elements that are
        adjacent to the specified elements, but are not tetrahedra (for
        example, hexahedra, wedges, and pyramids), are not refined.

        You cannot use mesh refinement on a solid model that contains initial
        conditions at nodes [IC], coupled nodes [CP family of commands],
        constraint equations [CE family of commands], or boundary conditions or
        loads applied directly to any of its nodes or elements. This applies to
        nodes and elements anywhere in the model, not just in the region where
        you want to request mesh refinement.   If you have detached the mesh
        from the solid model, you must disable postprocessing cleanup or
        smoothing (POST = OFF) after the refinement to preserve the element
        attributes.

        For additional restrictions on mesh refinement, see Revising Your Model
        in the Modeling and Meshing Guide.

        This command is also valid for rezoning.
        """
        command = "EREFINE,%s,%s,%s,%s,%s,%s,%s" % (str(ne1), str(ne2), str(ninc), str(level), str(depth), str(post), str(retain))
        return self.run(command, **kwargs)

    def eintf(self, toler="", k="", tlab="", kcn="", dx="", dy="", dz="",
              knonrot="", **kwargs):
        """APDL Command: EINTF

        Defines two-node elements between coincident or offset nodes.

        Parameters
        ----------
        toler
            Tolerance for coincidence (based on maximum Cartesian coordinate
            difference for node locations and on angle differences for node
            orientations). Defaults to 0.0001. Only nodes within the tolerance
            are considered to be coincident.

        k
            Only used when the type of the elements to be generated is
            PRETS179. K is the pretension node that is common to the pretension
            section that is being created. If K is not specified, it will be
            created by ANSYS automatically and will have an ANSYS-assigned node
            number. If K is specified but does not already exist, it will be
            created automatically but will have the user-specified node number.
            K cannot be connected to any existing element.

        tlab
            Nodal number ordering. Allowable values are:

            LOW - The 2-node elements are generated from the lowest numbered node to the highest
                  numbered node.

            HIGH - The 2-node elements are generated from the highest numbered node to the lowest
                   numbered node.

            REVE - Reverses the orientation of the selected 2-node element.

        kcn
            In coordinate system KCN, elements are created between node 1 and
            node 2 (= node 1 + dx dy dz).

        dx, dy, dz
            Node location increments that define the node offset in the active
            coordinate system (DR, Dθ, DZ for cylindrical and DR, Dθ, DΦ for
            spherical or toroidal).

        knonrot
            When KNONROT = 0, the nodes coordinate system is not rotated. When
            KNONROT = 1, the nodes belonging to the elements created are
            rotated into coordinate system KCN (see NROTAT command
            description).

        Notes
        -----
        Defines 2-node elements (such as gap elements) between coincident or
        offset nodes (within a tolerance). May be used, for example, to "hook"
        together elements interfacing at a seam, where the seam consists of a
        series of node pairs. One element is generated for each set of two
        coincident nodes. For more than two coincident or offset nodes in a
        cluster, an element is generated from the lowest numbered node to each
        of the other nodes in the cluster. If fewer than all nodes are to be
        checked for coincidence, use the NSEL command to select the nodes.
        Element numbers are incremented by one from the highest previous
        element number. The element type must be set [ET] to a 2-node element
        before issuing this command. Use the CPINTF command to connect nodes by
        coupling instead of by elements. Use the CEINTF command to connect the
        nodes by constraint equations instead of by elements.

        For contact element CONTA178, the tolerance is based on the maximum
        Cartesian coordinate difference for node locations only. The angle
        differences for node orientations are not checked.
        """
        command = "EINTF,%s,%s,%s,%s,%s,%s,%s,%s" % (str(toler), str(k), str(tlab), str(kcn), str(dx), str(dy), str(dz), str(knonrot))
        return self.run(command, **kwargs)

    def ensym(self, iinc="", ninc="", iel1="", iel2="", ieinc="", **kwargs):
        """APDL Command: ENSYM

        Generates elements by symmetry reflection.

        Parameters
        ----------
        iinc
            Increment to be added to element numbers in existing set.

        ninc
            Increment nodes in the given pattern by NINC.

        iel1, iel2, ieinc
            Reflect elements from pattern beginning with IEL1 to IEL2
            (defaults to IEL1) in steps of IEINC (defaults to 1). If
            IEL1 = ALL, IEL2 and IEINC are ignored and pattern is all
            selected elements [ESEL].  If IEL1 = P, graphical picking
            is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be
            substituted for IEL1 (IEL2 and IEINC are ignored).

        Notes
        -----
        This command is the same as the ESYM command except it allows
        explicitly assigning element numbers to the generated set (in
        terms of an increment IINC). Any existing elements already
        having these numbers will be redefined.

        The operation generates a new element by incrementing the
        nodes on the original element, and reversing and shifting the
        node connectivity pattern.  For example, for a 4-node 2-D
        element, the nodes in positions I, J, K and L of the original
        element are placed in positions J, I, L and K of the reflected
        element.

        Similar permutations occur for all other element types. For
        line elements, the nodes in positions I and J of the original
        element are placed in positions J and I of the reflected
        element. In releases prior to ANSYS 5.5, no node pattern
        reversing and shifting occurred for line elements generated by
        ENSYM. To achieve the same results as you did in releases
        prior to ANSYS 5.5, use the ENGEN command instead.

        See the ESYM command for additional information about symmetry
        elements.

        The ENSYM command also provides a convenient way to reverse
        shell element normals. If the IINC and NINC argument fields
        are left blank, the effect of the reflection is to reverse the
        direction of the outward normal of the specified elements. You
        cannot use the ENSYM command to change the normal direction of
        any element that has a body or surface load. We recommend that
        you apply all of your loads only after ensuring that the
        element normal directions are acceptable. Also note that real
        constants (such as nonuniform shell thickness and tapered beam
        constants) may be invalidated by an element reversal. See
        Revising Your Model in the Modeling and Meshing Guide for more
        information about controlling element normals.
        """
        return self.run(f"ENSYM,{iinc},,{ninc},{iel1},{iel2},{ieinc}", **kwargs)

    def esym(self, ninc="", iel1="", iel2="", ieinc="", **kwargs):
        """APDL Command: ESYM

        Generates elements from a pattern by a symmetry reflection.

        Parameters
        ----------
        ninc
            Increment nodes in the given pattern by NINC.

        iel1, iel2, ieinc
            Reflect elements from pattern beginning with IEL1 to IEL2 (defaults
            to IEL1) in steps of IEINC (defaults to 1). If IEL1 = ALL, IEL2 and
            IEINC are ignored and pattern is all selected elements [ESEL].  If
            IEL1 = P, graphical picking is enabled and all remaining command
            fields are ignored (valid only in the GUI). A component name may
            also be substituted for IEL1 (IEL2 and IEINC are ignored).

        Notes
        -----
        Generates additional elements from a given pattern (similar to EGEN)
        except with a "symmetry" reflection. The operation generates a new
        element by incrementing the nodes on the original element, and
        reversing and shifting  the node connectivity pattern. For example, for
        a 4-node 2-D element, the nodes in positions I, J, K, and L of the
        original element are placed in positions J, I, L, and K of the
        reflected element.

        Similar permutations occur for all other element types. For line
        elements, the nodes in positions I and J of the original element are
        placed in positions J and I of the reflected element. In releases prior
        to ANSYS 5.5, no node pattern reversing and shifting occurred for line
        elements generated by ESYM. To achieve the same results with ANSYS 5.5
        as you did in prior releases, use the EGEN command instead.

        It is recommended that symmetry elements be displayed and graphically
        reviewed.

        If the nodes are also reflected (as with the NSYM command) this pattern
        is such that the orientation of the symmetry element remains similar to
        the original element (i.e., clockwise elements are generated from
        clockwise elements).

        For a non-reflected node pattern, the reversed orientation has the
        effect of reversing the outward normal direction (clockwise elements
        are generated from counterclockwise elements).

        Note:: : Since nodes may be defined anywhere in the model independently
        of this command, any orientation of the "symmetry" elements is
        possible. See also the ENSYM command for modifying existing elements.
        """
        return self.run(f"ESYM,,{ninc},{iel1},{iel2},{ieinc}", **kwargs)

    def esll(self, type_="", **kwargs):
        """APDL Command: ESLL

        Selects those elements associated with the selected lines.

        Parameters
        ----------
        type_
            Label identifying the type of element select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        Selects line elements belonging to meshed [LMESH], selected [LSEL]
        lines.

        This command is valid in any processor.
        """
        command = "ESLL,%s" % (str(type_))
        return self.run(command, **kwargs)

    def etlist(self, ityp1="", ityp2="", inc="", **kwargs):
        """APDL Command: ETLIST

        Lists currently defined element types.

        Parameters
        ----------
        ityp1, ityp2, inc
            Lists element types from ITYP1 to ITYP2 (defaults to ITYP1) in
            steps of INC (defaults to 1). If ITYP1 = ALL (default), ITYP2 and
            INC are ignored and all element types are listed.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "ETLIST,%s,%s,%s" % (str(ityp1), str(ityp2), str(inc))
        return self.run(command, **kwargs)

    def elist(self, iel1="", iel2="", inc="", nnkey="", rkey="", ptkey="",
              **kwargs):
        """APDL Command: ELIST

        Lists the elements and their attributes.

        Parameters
        ----------
        iel1, iel2, inc
            Lists elements from IEL1 to IEL2 (defaults to IEL1) in steps of INC
            (defaults to 1). If IEL1 = ALL (default), IEL2 and INC are ignored
            and all selected elements [ESEL] are listed. If IEL1 = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may also be substituted
            for IEL1 (IEL2 and INC are ignored).

        nnkey
            Node listing key:

            0 - List attribute references and nodes.

            1 - List attribute references but not nodes.

        rkey
            Real constant listing key:

            0 - Do not show real constants for each element.

            1 - Show real constants for each element. This includes default values chosen for
                the element.

        ptkey
            LS-DYNA part number listing key (applicable to ANSYS LS-DYNA only):

            0 - Do not show part ID number for each element.

            1 - Show part ID number for each element.

        Notes
        -----
        Lists the elements with their nodes and attributes (MAT, TYPE, REAL,
        ESYS, SECNUM, PART). See also the LAYLIST command for listing layered
        elements.

        This command is valid in any processor.
        """
        command = "ELIST,%s,%s,%s,%s,%s,%s" % (str(iel1), str(iel2), str(inc), str(nnkey), str(rkey), str(ptkey))
        return self.run(command, **kwargs)

    def eorient(self, etype="", dir_="", toler="", **kwargs):
        """APDL Command: EORIENT

        Reorients solid element normals.

        Parameters
        ----------
        etype
            Specifies which elements to orient.

            LYSL - Specifies that certain solid elements (such as SOLID185 with KEYOPT(3) = 1,
                   SOLID186 with KEYOPT(3) = 1, and SOLSH190) will be oriented.
                   This value is the default.

        Notes
        -----
        EORIENT renumbers the element faces, designating the face  most
        parallel to the XY plane of the element coordinate system (set with
        ESYS) as face 1 (nodes I-J-K-L, parallel to the layers in layered
        elements). It calculates the outward normal of each face and changes
        the node designation  of the elements so the face with a normal most
        nearly parallel with and in the same general direction as the target
        axis becomes face 1.

        The target axis, defined by Dir, is either the negative or positive
        indicated axis or the outward normal of face 1 of that element.

        All SOLID185 Layered Structural Solid, SOLID186 Layered Structural
        Solid, and SOLSH190 solid shell elements in the selected set are
        considered for reorientation.

        After reorienting elements, you should always display and graphically
        review results using the /ESHAPE command. When plotting models with
        many or symmetric layers, it may be useful to temporarily reduce the
        number of layers to two, with one layer being much thicker than the
        other.

        You cannot use EORIENT to change the normal direction of any element
        that has a body or surface load.  We recommend that you apply all of
        your loads only after ensuring that the element normal directions are
        acceptable.

        Prisms and tetrahedrals are also supported, within the current
        limitations of the SOLID185, SOLID186, and SOLSH190 elements. (Layers
        parallel to the four-node face of the prism are not supported.)
        """
        command = "EORIENT,%s,%s,%s" % (str(etype), str(dir_), str(toler))
        return self.run(command, **kwargs)

    def engen(self, iinc="", itime="", ninc="", iel1="", iel2="", ieinc="",
              minc="", tinc="", rinc="", cinc="", sinc="", dx="", dy="", dz="",
              **kwargs):
        """APDL Command: ENGEN

        Generates elements from an existing pattern.

        Parameters
        ----------
        iinc
            Increment to be added to element numbers in pattern.

        itime, ninc
            Do this generation operation a total of ITIMEs, incrementing all
            nodes in the given pattern by NINC each time after the first. ITIME
            must be > 1 if generation is to occur. NINC may be positive, zero,
            or negative.

        iel1, iel2, ieinc
            Generate elements from the pattern that begins with IEL1 to IEL2
            (defaults to IEL1) in steps of IEINC (defaults to 1). If IEL1 is
            negative, IEL2 and IEINC are ignored and use the last |IEL1|
            elements (in sequence backward from the maximum element number) as
            the pattern to be repeated.  If IEL1 = ALL, IEL2 and IEINC are
            ignored and all selected elements [ESEL] are used as the pattern to
            be repeated. If IEL1 = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI). A
            component name may also be substituted for IEL1 (IEL2 and IEINC are
            ignored).

        minc
            Increment material number of all elements in the given pattern by
            MINC each time after the first.

        tinc
            Increment type number by TINC.

        rinc
            Increment real constant table number by RINC.

        cinc
            Increment element coordinate system number by CINC.

        sinc
            Increment section ID number by SINC.

        dx, dy, dz
            Define nodes that do not already exist but are needed by generated
            elements (NGEN,ITIME,INC,NODE1,,,DX,DY,DZ). Zero is a valid value.
            If blank, DX, DY, and DZ are ignored.

        Notes
        -----
        Same as the EGEN command except it allows element numbers to be
        explicitly incremented (IINC) from the generated set. Any existing
        elements already having these numbers will be redefined.
        """
        command = "ENGEN,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(iinc), str(itime), str(ninc), str(iel1), str(iel2), str(ieinc), str(minc), str(tinc), str(rinc), str(cinc), str(sinc), str(dx), str(dy), str(dz))
        return self.run(command, **kwargs)

    def esln(self, type_="", ekey="", nodetype="", **kwargs):
        """APDL Command: ESLN

        Selects those elements attached to the selected nodes.

        Parameters
        ----------
        type_
            Label identifying the type of element selected:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        ekey
            Node set key:

            0 - Select element if any of its nodes are in the selected nodal set (default).

            1 - Select element only if all of its nodes are in the selected nodal set.

        nodetype
            Label identifying type of nodes to consider when selecting:

            ALL - Select elements considering all of their nodes (default).

            ACTIVE - Select elements considering only their active nodes. An active node is a node
                     that contributes DOFs to the model.

            INACTIVE - Select elements considering only their inactive nodes (such as orientation or
                       radiation nodes).

            CORNER - Select elements considering only their corner nodes.

            MID - Select elements considering only their midside nodes.

        Notes
        -----
        ESLN selects elements which have any (or all EKEY) NodeType nodes in
        the currently-selected set of nodes. Only elements having nodes in the
        currently-selected set can be selected.

        This command is valid in any processor.
        """
        command = "ESLN,%s,%s,%s" % (str(type_), str(ekey), str(nodetype))
        return self.run(command, **kwargs)

    def ematwrite(self, key="", **kwargs):
        """APDL Command: EMATWRITE

        Forces the writing of all the element matrices to File.EMAT.

        Parameters
        ----------
        key
            Write key:

            YES - Forces the writing of the element matrices to File.EMAT even if not normally
                  done.

            NO - Element matrices are written only if required. This value is the default.

        Notes
        -----
        The EMATWRITE command forces ANSYS to write the File.EMAT file. The
        file is necessary if you intend to follow the initial load step with a
        subsequent inertia relief calculation (IRLF). If used in the solution
        processor (/SOLU), this command is only valid within the first load
        step.

        This command is also valid in PREP7.
        """
        command = "EMATWRITE,%s" % (str(key))
        return self.run(command, **kwargs)

    def en(self, iel="", i="", j="", k="", l="", m="", n="", o="", p="",
           **kwargs):
        """APDL Command: EN

        Defines an element by its number and node connectivity.

        Parameters
        ----------
        iel
            Number assigned to element being defined. If IEL = P, graphical
            picking is enabled and all remaining command fields are ignored
            (valid only in the GUI).

        i
            Number of node assigned to first nodal position (node I).

        j, k, l, m, n, o, p
            Number assigned to second (node J) through eighth (node P) nodal
            position, if any.

        Notes
        -----
        Defines an element by its nodes and attribute values. Similar to the E
        command except it allows the element number (IEL) to be defined
        explicitly.  Element numbers need not be consecutive. Any existing
        element already having this number will be redefined.

        Up to 8 nodes may be specified with the EN command. If more nodes are
        needed for the element, use the EMORE command. The number of nodes
        required and the order in which they should be specified are described
        in the Element Reference for each element type.  The current (or
        default) MAT, TYPE, REAL, SECNUM, and ESYS attribute values are also
        assigned to the element.

        When creating elements with more than 8 nodes using this command and
        the EMORE command, it may be necessary to turn off shape checking using
        the SHPP command before issuing this command. If a valid element type
        can be created without using the additional nodes on the EMORE command,
        this command will create that element. The EMORE command will then
        modify the element to include the additional nodes. If shape checking
        is active, it will be performed before the EMORE command is issued.
        Therefore, if the shape checking limits are exceeded, element creation
        may fail before the EMORE command modifies the element into an
        acceptable shape.
        """
        command = "EN,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (str(iel), str(i), str(j), str(k), str(l), str(m), str(n), str(o), str(p))
        return self.run(command, **kwargs)

    def etchg(self, cnv="", **kwargs):
        """APDL Command: ETCHG

        Changes element types to their corresponding types.

        Parameters
        ----------
        cnv
            Converts the element types to the corresponding type. Valid labels
            are:

            ETI - Explicit to Implicit

            ITE - Implicit to Explicit

            TTE - Thermal to Explicit

            TTS - Thermal to Structural

            STT - Structural to Thermal

            MTT - Magnetic to Thermal

            FTS - Fluid to Structural

            ETS - Electrostatic to Structural

            ETT - Electrical to Thermal

        Notes
        -----
        Changes the currently defined element types to their corresponding
        types.  Elements without a companion element (listed above) are not
        switched and should be switched with the ET command to an appropriate
        element type or to a null element. The KEYOPT values for the switched
        element types are reset to zero or to their default values. You must
        check these values to see if they are still meaningful. Additionally,
        if Cnv = ETI, ITE, or TTE, all real constants are set to zero.

        If Cnv = ITE, you will need to choose a material model that corresponds
        to your previously-defined material properties. If working
        interactively, you will be prompted to do so.
        """
        command = "ETCHG,%s" % (str(cnv))
        return self.run(command, **kwargs)

    def elem(self, **kwargs):
        """APDL Command: ELEM

        Specifies "Elements" as the subsequent status topic.

        Notes
        -----
        This is a status [STAT] topic command. Status topic commands are
        generated by the GUI and will appear in the log file (Jobname.LOG) if
        status is requested for some items under Utility Menu>: List> Status.
        This command will be immediately followed by a STAT command, which will
        report the status for the specified topic.

        If entered directly into the program, the STAT command should
        immediately follow this command.
        """
        command = "ELEM,"
        return self.run(command, **kwargs)

    def einfin(self, compname="", pnode="", **kwargs):
        """APDL Command: EINFIN

        Generates structural infinite elements from selected nodes.

        Parameters
        ----------
        compname
            Component name containing one node to be used as the pole node for
            generating INFIN257 structural infinite elements. The pole node is
            generally located at or near the geometric center of the finite
            element domain.

        pnode
            Node number for the direct input of the pole node. A parameter or
            parametric expression is also valid. Specify this value when no
            CompName has been specified. If CompName is specified, this value
            is ignored.

        Notes
        -----
        The EINFIN command generates structural infinite elements (INFIN257)
        directly from the selected face of valid base elements (existing
        standard elements in your model). The command scans all base elements
        for the selected nodes and generates a compatible infinite element type
        for each base element. A combination of different base element types is
        allowed if the types are all compatible with the infinite elements.

        The infinite element type requires no predefinition (ET).

        The faces of base elements are determined from the selected node set
        (NSEL), and the geometry of the infinite element is determined based on
        the shape of the face. Element characteristics and options are
        determined according to the base element. For the face to be used, all
        nodes on the face of a base element must be selected

        Use base elements to model the near-field domain that interacts with
        the solid structures or applied loads. To apply the truncated far-field
        effect, a single layer of infinite elements must be attached to the
        near-field domain. The outer surface of the near-field domain must be
        convex.

        After the EINFIN command executes, you can verify the newly created
        infinite element types and elements (ETLIST, ELIST, EPLOT).

        Infinite elements do not account for any subsequent modifications made
        to the base elements. It is good practice to issue the EINFIN command
        only after the base elements are finalized. If you delete or modify
        base elements, remove all affected infinite elements and reissue the
        EINFIN command; doing so prevents inconsistencies.
        """
        command = "EINFIN,%s,%s" % (str(compname), str(pnode))
        return self.run(command, **kwargs)

    def eread(self, fname="", ext="", **kwargs):
        """APDL Command: EREAD

        Reads elements from a file.

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
        This read operation is not necessary in a standard ANSYS run
        but is provided as a convenience to users wanting to read a
        coded element file, such as from another mesh generator or
        from a CAD/CAM program.  Data should be formatted as produced
        with the EWRITE command. If issuing EREAD to acquire element
        information generated from ANSYS EWRITE, you must also issue
        NREAD before the EREAD command. The element types [ET] must be
        defined before the file is read so that the file may be read
        properly. Only elements that are specified with the ERRANG
        command are read from the file. Also, only elements that are
        fully attached to the nodes specified on the NRRANG command
        are read from the file. Elements are assigned numbers
        consecutively as read from the file, beginning with the
        current highest database element number plus one. The file is
        rewound before and after reading. Reading continues until the
        end of the file.
        """
        command = "EREAD,%s,%s" % (str(fname), str(ext))
        return self.run(command, **kwargs)

    def esel(self, type_="", item="", comp="", vmin="", vmax="", vinc="",
             kabs="", **kwargs):
        """APDL Command: ESEL

        Selects a subset of elements.

        Parameters
        ----------
        type_
            Label identifying the type of select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

            ALL - Restore the full set.

            NONE - Unselect the full set.

            INVE - Invert the current set (selected becomes unselected and vice versa).

            STAT - Display the current select status.

        Notes
        -----
        Selects elements based on values of a labeled item and component. For
        example, to select a new set of elements based on element numbers 1
        through 7, use ESEL,S,ELEM,,1,7.  The subset is used when the ALL label
        is entered (or implied) on other commands, such as ELIST,ALL.  Only
        data identified by element number are selected. Selected data are
        internally flagged; no actual removal of data from the database occurs.
        Different element subsets cannot be used for different load steps
        [SOLVE] in a /SOLU sequence.  The subset used in the first load step
        will be used for all subsequent load steps regardless of subsequent
        ESEL specifications.

        This command is valid in any processor.

        Elements crossing the named path (see PATH command) will be selected.
        This option is only available in PREP7 and POST1. If no geometry data
        has been mapped to the path (i.e., via PMAP and PDEF commands), the
        path will assume the default mapping option (PMAP,UNIFORM) to map the
        geometry prior to selecting the elements. If an invalid path name is
        given, the ESEL command is ignored (status of selected elements is
        unchanged). If there are no elements crossing the path, the ESEL
        command will return zero elements selected.

        For selections based on non-integer numbers (coordinates, results,
        etc.), items that are within the range VMIN -Toler and VMAX + Toler are
        selected. The default tolerance Toler is based on the relative values
        of VMIN and VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

        If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX - VMIN).

        Use the SELTOL command to override this default and specify Toler
        explicitly.

        Table: 133:: : ESEL - Valid Item and Component Labels
        """
        command = "ESEL,%s,%s,%s,%s,%s,%s,%s" % (str(type_), str(item), str(comp), str(vmin), str(vmax), str(vinc), str(kabs))
        return self.run(command, **kwargs)

    def esort(self, item="", lab="", order="", kabs="", numb="", **kwargs):
        """APDL Command: ESORT

        Sorts the element table.

        Parameters
        ----------
        item
            Label identifying the item:

            ETAB - (currently the only Item available)

        lab
            element table label:

            Lab - Any user-defined label from the ETABLE command (input in the Lab field of the
                  ETABLE command).

        order
            Order of sort operation:

            0 - Sort into descending order.

            1 - Sort into ascending order.

        kabs
            Absolute value key:

            0 - Sort according to real value.

            1 - Sort according to absolute value.

        numb
            Number of elements (element table rows) to be sorted in ascending
            or descending order (ORDER) before sort is stopped (remainder will
            be in unsorted sequence) (defaults to all elements).

        Notes
        -----
        The element table rows are sorted based on the column containing the
        Lab values. Use EUSORT to restore the original order. If ESORT is
        specified with PowerGraphics on [/GRAPHICS,POWER], then the nodal
        solution results listing [PRNSOL] will be the same as with the full
        graphics mode [/GRAPHICS,FULL].
        """
        command = "ESORT,%s,%s,%s,%s,%s" % (str(item), str(lab), str(order), str(kabs), str(numb))
        return self.run(command, **kwargs)

    def esurf(self, xnode="", tlab="", shape="", **kwargs):
        """APDL Command: ESURF

        Generates elements overlaid on the free faces of selected nodes.

        Parameters
        ----------
        xnode
            Node number that is used only in the following two cases:

        tlab
            Generates target, contact, and hydrostatic fluid elements with
            correct direction of normals.

            TOP - Generates target and contact elements over beam and shell elements, or
                  hydrostatic fluid elements over shell elements, with the
                  normals the same as the underlying beam and shell elements
                  (default).

            BOTTOM - Generates target and contact elements over beam and shell elements, or
                     hydrostatic fluid elements over shell elements, with the
                     normals opposite to the underlying beam and shell
                     elements.

            If target or contact elements and hydrostatic fluid elements are defined on the same underlying shell elements, you only need to use this option once to orient the normals opposite to the underlying shell elements. - REVERSE

            Reverses the direction of the normals on existing selected target elements, contact elements, and hydrostatic fluid elements. - If target or contact elements and hydrostatic fluid elements are defined on the
                              same underlying shell elements, you only need to
                              use this option once to reverse the normals for
                              all selected elements.

        shape
            Used to specify the element shape for target element TARGE170
            (Shape = LINE or POINT) or TARGE169 elements (Shape = POINT).

            (blank) - The target element takes the same shape as the external surface of the
                      underlying element (default).

            LINE - Generates LINE or PARA (parabolic) segments on exterior of selected 3-D
                   elements.

            POINT - Generates POINT segments on selected nodes.

        Notes
        -----
        The ESURF command generates elements of the currently active element
        type overlaid on the free faces of existing elements. For example,
        surface elements (such as SURF151, SURF152, SURF153, SURF154, or
        SURF159) can be generated over solid elements (such as PLANE55,
        SOLID70, PLANE182, SOLID185, or SOLID272, respectively).

        Element faces are determined from the selected node set (NSEL) and the
        load faces for that element type. The operation is similar to that used
        for generating element loads from selected nodes via the SF,ALL
        command, except that elements (instead of loads) are generated. All
        nodes on the face must be selected for the face to be used. For shell
        elements, only face one of the element is available. If nodes are
        shared by adjacent selected element faces, the faces are not free and
        no element is generated.

        Elements created by ESURF are oriented such that their surface load
        directions are consistent with those of the underlying elements.
        Carefully check generated elements and their orientations.

        Generated elements use the existing nodes and the active MAT, TYPE,
        REAL, and ESYS attributes. The exception is when Tlab = REVERSE. The
        reversed target and contact elements have the same attributes as the
        original elements. If the underlying elements are solid elements, Tlab
        = TOP or BOTTOM has no effect.

        When the command generates a target element, the shape is by default
        the same as that of the underlying element. Issue  ESURF,,,LINE or
        ESURF,,,POINT to generate LINE, PARA, and POINT segments.

        The ESURF command can also generate the 2-D or 3-D node-to-surface
        element CONTA175, based on the selected node components of the
        underlying solid elements. When used to generate CONTA175 elements, all
        ESURF arguments are ignored. (If CONTA175 is the active element type,
        the path Main Menu> Preprocessor> Modeling> Create> Elements> Node-to-
        Surf uses ESURF to generate elements.)

        To generate SURF151 or SURF152 elements that have two extra nodes from
        FLUID116 elements, KEYOPT(5) for SURF151 or SURF152 is first set to 0
        and ESURF is issued. Then KEYOPT(5) for SURF151 or SURF152 is set to 2
        and MSTOLE is issued. For more information, see Using the Surface
        Effect Elements in the Thermal Analysis Guide.

        For hydrostatic fluid elements HSFLD241 and HSFLD242, the ESURF command
        generates triangular (2-D) or pyramid-shaped (3-D) elements with bases
        that are overlaid on the faces of selected 2-D or 3-D solid or shell
        elements. The single vertex for all generated elements is at the
        pressure node specified as XNODE. The generated elements fill the
        volume enclosed by the solid or shell elements. The nodes on the
        overlaid faces have translational degrees of freedom, while the
        pressure node shared by all generated elements has a single hydrostatic
        pressure degree of freedom, HDSP (see HSFLD241 and HSFLD242 for more
        information about the pressure node).
        """
        command = "ESURF,%s,%s,%s" % (str(xnode), str(tlab), str(shape))
        return self.run(command, **kwargs)

    def eplot(self, **kwargs):
        """APDL Command: EPLOT

        Produces an element display.

        Notes
        -----
        Produces an element display of the selected elements. In full graphics,
        only those elements faces with all of their corresponding nodes
        selected are plotted. In PowerGraphics, all element faces of the
        selected element set are plotted irrespective of the nodes selected.
        However, for both full graphics and PowerGraphics, adjacent or
        otherwise duplicated faces of 3-D solid elements will not be displayed
        in an attempt to eliminate plotting of interior facets. See the DSYS
        command for display coordinate system issues.

        This command will display curvature in midside node elements when
        PowerGraphics is activated [/GRAPHICS,POWER] and /EFACET,2 or /EFACET,4
        are enabled.  (To display curvature, two facets per edge is recommended
        [/EFACET,2]).  When you specify /EFACET,1, PowerGraphics does not
        display midside nodes. /EFACET has no effect on EPLOT for non-midside
        node elements.

        This command is valid in any processor.
        """
        command = "EPLOT,"
        return self.run(command, **kwargs)

    def ekill(self, elem="", **kwargs):
        """APDL Command: EKILL

        Deactivates an element (for the birth and death capability).

        Parameters
        ----------
        elem
            Element to be deactivated. If ALL, deactivate all selected elements
            [ESEL]. If ELEM = P, graphical picking is enabled and all remaining
            command fields are ignored  (valid only in the GUI). A component
            name may also be substituted for ELEM.

        Notes
        -----
        Deactivates the specified element when the birth and death capability
        is being used. A deactivated element remains in the model but
        contributes a near-zero stiffness (or conductivity, etc.) value (ESTIF)
        to the overall matrix. Any solution-dependent state variables (such as
        stress, plastic strain, creep strain, etc.) are set to zero.
        Deactivated elements contribute nothing to the overall mass (or
        capacitance, etc.) matrix.

        The element can be reactivated with the EALIVE command.

        ANSYS, Inc. recommends using element deactivation/reactivation
        (EKILL/EALIVE) for linear elastic materials only. For all other
        materials, validate the results carefully before using them.

        This command is also valid in PREP7.
        """
        command = "EKILL,%s" % (str(elem))
        return self.run(command, **kwargs)
