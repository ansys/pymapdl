from typing import Optional

from ansys.mapdl.core.mapdl_types import MapdlInt


class ElementTable:
    def detab(
        self,
        elem="",
        lab="",
        v1="",
        v2="",
        v3="",
        v4="",
        v5="",
        v6="",
        **kwargs,
    ):
        """Modifies element table results in the database.

        APDL Command: DETAB

        Parameters
        ----------
        elem
            Element for which results are to be modified.  If ALL, modify all
            selected elements [ESEL] results.  If ELEM = P, graphical picking
            is enabled and all remaining command fields are ignored (valid only
            in the GUI).  A component name may also be substituted for ELEM.

        lab
            Label identifying results.  Valid labels are as defined with the
            ETABLE command.  Issue ETABLE,STAT to display labels and values.

        v1
            Value assigned to this element table result in the database.  If
            zero, a zero value will be assigned.  If blank, value remains
            unchanged.

        v2, v3, v4, . . . , v6
            Additional values (if any) assigned to consecutive element table
            columns.

        Notes
        -----
        Modifies element table [ETABLE] results in the database.  For example,
        DETAB,35,ABC,1000,2000,1000 assigns 1000, 2000, and 1000 to the first
        three table columns starting with label ABC for element 35.  Use the
        PRETAB command to list the current results.  After deleting a column of
        data using ETABLE,Lab,ERASE, the remaining columns of data are not
        shifted to compress the empty slot.  Therefore, the user must allocate
        null (blank) values for V1, V2...V6 for any ETABLE entries which have
        been deleted by issuing ETABLE,Lab,ERASE.  All data are stored in the
        solution coordinate system but will be displayed in the results
        coordinate system [RSYS].
        """
        command = f"DETAB,{elem},{lab},{v1},{v2},{v3},{v4},{v5},{v6}"
        return self.run(command, **kwargs)

    def esort(
        self,
        item: str = "",
        lab: str = "",
        order: MapdlInt = "",
        kabs: MapdlInt = "",
        numb: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Sorts the element table.

        APDL Command: ESORT

        Parameters
        ----------
        item
            Label identifying the item:
            ETAB - (currently the only Item available)

        lab
            element table label: Lab - Any user-defined label from
            the ETABLE command (input in the Lab field of the ETABLE
            command).

        order
            Order of sort operation:

            0 - Sort into descending order.

            1 - Sort into ascending order.

        kabs
            Absolute value key:

            0 - Sort according to real value.

            1 - Sort according to absolute value.

        numb
            Number of elements (element table rows) to be sorted in
            ascending or descending order (ORDER) before sort is
            stopped (remainder will be in unsorted sequence)
            (defaults to all elements).

        Notes
        -----
        The element table rows are sorted based on the column
        containing the Lab values. Use EUSORT to restore the original
        order. If ESORT is specified with PowerGraphics on
        [/GRAPHICS,POWER], then the nodal solution results listing
        [PRNSOL] will be the same as with the full graphics mode
        [/GRAPHICS,FULL].
        """
        command = f"ESORT,{item},{lab},{order},{kabs},{numb}"
        return self.run(command, **kwargs)

    def etable(
        self,
        lab: str = "",
        item: str = "",
        comp: str = "",
        option: str = "",
        **kwargs,
    ) -> Optional[str]:
        """Fills a table of element values for further processing.

        APDL Command: ETABLE

        The ETABLE command defines a table of values per element (the
        element table) for use in further processing. The element
        table is organized similar to spreadsheet, with rows
        representing all selected elements and columns consisting of
        result items which have been moved into the table (Item,Comp)
        via ETABLE. Each column of data is identified by a
        user-defined label (Lab) for listings and displays.

        After entering the data into the element table, you are not
        limited to merely listing or displaying your data (PLESOL,
        PRESOL, etc.). You may also perform many types of operations
        on your data, such as adding or multiplying columns (SADD,
        SMULT), defining allowable stresses for safety calculations
        (SALLOW), or multiplying one column by another (SMULT).  See
        Getting Started in the Basic Analysis Guide for more
        information.

        Various results data can be stored in the element table. For
        example, many items for an element are inherently
        single-valued (one value per element). The single-valued items
        include: SERR, SDSG, TERR, TDSG, SENE, SEDN, TENE, KENE, AENE,
        JHEAT, JS, VOLU, and CENT. All other items are multivalued
        (varying over the element, such that there is a different
        value at each node). Because only one value is stored in the
        element table per element, an average value (based on the
        number of contributing nodes) is calculated for multivalued
        items. Exceptions to this averaging procedure are FMAG and all
        element force items, which represent the sum only of the
        contributing nodal values.

        Two methods of data access can be used with the ETABLE
        command. The method you select depends upon the type of data
        that you want to store.  Some results can be accessed via a
        generic label (Component Name method), while others require a
        label and number (Sequence Number method).

        The Component Name method is used to access the General
        element data (that is, element data which is generally
        available to most element types or groups of element
        types). All of the single-valued items and some of the more
        general multivalued items are accessible with the Component
        Name method.  Various element results depend on the
        calculation method and the selected results location (AVPRIN,
        RSYS, LAYER, SHELL, and ESEL).

        Although nodal data is readily available for listings and
        displays (PRNSOL, PLNSOL) without using the element table, you
        may also use the Component Name method to enter these results
        into the element table for further "worksheet"
        manipulation. (See Getting Started in theBasic Analysis Guide
        for more information.) A listing of the General Item and Comp
        labels for the Component Name method is shown below.

        The Sequence Number method allows you to view results for data
        that is not averaged (such as pressures at nodes, temperatures
        at integration points, etc.), or data that is not easily
        described in a generic fashion (such as all derived data for
        structural line elements and contact elements, all derived
        data for thermal line elements, layer data for layered
        elements, etc.). A table illustrating the Items (such as LS,
        LEPEL, LEPTH, SMISC, NMISC, SURF, etc.) and corresponding
        sequence numbers for each element is shown in the Output Data
        section of each element description found in the Element
        Reference.

        Some element table data are reported in the results coordinate
        system.  These include all component results (for example, UX,
        UY, etc.; SX, SY, etc.). The solution writes component results
        in the database and on the results file in the solution
        coordinate system. When you issue the ETABLE command, these
        results are then transformed into the results coordinate
        system (RSYS) before being stored in the element table. The
        default results coordinate system is global Cartesian
        (RSYS,0).  All other data are retrieved from the database and
        stored in the element table with no coordinate transformation.

        Use the PRETAB, PLETAB, or ETABLE,STAT commands to display the
        stored table values. Issue ETABLE,ERAS to erase the entire
        table. Issue ETABLE,Lab,ERAS to erase a Lab column.

        The element table data option (Option) is not available for
        all output items.

        Parameters
        ----------
        lab
            Any unique user defined label for use in subsequent
            commands and output headings (maximum of eight characters
            and not a General predefined Item label). Defaults to an
            eight character label formed by concatenating the first
            four characters of the Item and Comp labels. If the same
            as a previous user label, this result item will be
            included under the same label. Up to 200 different labels
            may be defined. The following labels are predefined and
            are not available for user-defined labels: ``'REFL''`,
            ``'STAT'``, and ``'ERAS'``.  ``lab='REFL'`` refills all
            tables previously defined with the :meth:`etable` commands
            (not the CALC module commands) according to the latest
            ETABLE specifications and is convenient for refilling
            tables after the load step (SET) has been
            changed. Remaining fields will be ignored if
            ``Lab='REFL'``.  ``lab='STAT'`` displays stored table
            values.  ``lab='ERAS'`` erases the entire table.

        item
            Label identifying the item. General item labels are shown
            in the table below. Some items also require a component
            label. Character parameters may be used. ``item='eras'``
            erases a Lab column.

        comp
            Component of the item (if required). General component
            labels are shown in the table below. Character parameters
            may be used.

        option
            Option for storing element table data:

            * ``'MIN'`` - Store minimum element nodal value of the specified
              item component.
            * ``'MAX'`` - Store maximum element nodal value of the specified
              item component.
            * ``'AVG'`` - Store averaged element centroid value of the
              specified item component (default).

        Examples
        --------
        Print the volume of individual elements.

        >>> mapdl.clear()
        >>> output = mapdl.input(examples.vmfiles['vm6'])
        >>> mapdl.post1()
        >>> label = 'MYVOLU'
        >>> mapdl.etable(label, 'VOLU')
        >>> print(mapdl.pretab(label))
        PRINT ELEMENT TABLE ITEMS PER ELEMENT
           *****ANSYS VERIFICATION RUN ONLY*****
             DO NOT USE RESULTS FOR PRODUCTION
          ***** POST1 ELEMENT TABLE LISTING *****
            STAT     CURRENT
            ELEM     XDISP
               1  0.59135E-001
               2  0.59135E-001
               3  0.59135E-001
        ...

        """
        command = f"ETABLE,{lab},{item},{comp},{option}"
        return self.run(command, **kwargs)

    def eusort(self, **kwargs) -> Optional[str]:
        """Restore original order of the element table.

        APDL Command: EUSORT

        Notes
        -----
        Changing the selected element set [ESEL] also restores the original
        element order.

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.eusort()
        'ELEMENT SORT REMOVED'

        """
        return self.run("EUSORT", **kwargs)

    def pletab(self, itlab="", avglab="", **kwargs):
        """Displays element table items.

        APDL Command: PLETAB

        Parameters
        ----------
        itlab
            User-defined label, as specified with the ETABLE command, of item
            to be displayed.

        avglab
            Averaging operation:

            NOAV - Do not average element items at common nodes (default).

            AVG - Average the element items at common nodes.

        Notes
        -----
        Displays items stored in the table defined with the ETABLE command for
        the selected elements.  For display purposes, items are assumed to be
        constant over the element and assigned to each of its nodes.  Contour
        display lines (lines of constant value) are determined by linear
        interpolation within each element from the nodal values.  These nodal
        values have the option of being averaged (values are averaged at a node
        whenever two or more elements connect to the same node) or not averaged
        (discontinuous).  The discontinuity between contour lines of adjacent
        elements is an indication of the gradient across elements.

        Portions of this command are not supported by PowerGraphics
        [/GRAPHICS,POWER].
        """
        command = f"PLETAB,{itlab},{avglab}"
        return self.run(command, **kwargs)

    def plls(self, labi="", labj="", fact="", kund="", viewup="", **kwargs):
        """Displays element table items as contoured areas along elements.

        APDL Command: PLLS

        Parameters
        ----------
        labi
            Label of element table item (ETABLE) for node I magnitude.

        labj
            Label of element table item for node J magnitude.

        fact
            Scale factor for display (defaults to 1).  A negative scaling
            factor may be used to invert the display.

        kund
            Undisplaced shape key:

            0 - Display selected items on undeformed shape.

            1 - Display selected items on deformed shape.

        viewup
            View Up key:

            0 - Ignore the view-up (/VUP) vector when calculating trapezoid orientation
                (default).

            1 - Use the view-up (/VUP) vector to calculate trapezoid orientation.

        Notes
        -----
        Displays selected items (such as shears and moments) as a contoured
        area (trapezoid) display along line elements and 2-D axisymmetric shell
        elements (such as shear and moment diagrams).  Three sides of the
        trapezoid are formed by the element (one side) and lines at nodes I and
        J of length proportional to the item magnitude and displayed normal to
        the element and the viewing direction (the two parallel sides).

        When ViewUP = 1, the trapezoid is oriented within the plane created by
        the element and the global Cartesian coordinate system reference
        orientation (/VUP or view up) vector. In this case, the program does
        not perform the calculation involving the element and view direction.

        Portions of this command are not supported by PowerGraphics
        [/GRAPHICS,POWER].
        """
        command = f"PLLS,{labi},{labj},{fact},{kund},{viewup}"
        return self.run(command, **kwargs)

    def pretab(
        self,
        lab1="",
        lab2="",
        lab3="",
        lab4="",
        lab5="",
        lab6="",
        lab7="",
        lab8="",
        lab9="",
        **kwargs,
    ):
        """Print the element table items.

        APDL Command: PRETAB

        Parameters
        ----------
        lab1, lab2, lab3, ... , lab9
            Print selected items.  Valid labels are ``""`` or any
            label as specified with the ETABLE command.  Convenience
            labels may be used for Lab1 to select groups of labels (10
            labels maximum): GRP1 for first 10 stored items; GRP2 for
            items 11 to 20; GRP3 for items 21 to 30; GRP4 for items 31
            to 40; GRP5 for items 41 to 50.  Run ``etable("stat")``
            command to list stored item order.  If all labels are
            blank, print first 10 stored items (GRP1).

        Notes
        -----
        Prints the items stored in the table defined with the
        :func:`etable() <ansys.mapdl.core.Mapdl.etable>` command.
        Item values will be listed for the selected elements in the
        sorted sequence [ESORT].  :func:`force()
        <ansys.mapdl.core.Mapdl.force>` can be used to define which
        component of the nodal load is to be used (static, damping,
        inertia, or total).

        Examples
        --------
        Print out element displacement results.

        >>> mapdl.etable("values", "U", "X")
        STORE VALUES   FROM ITEM=U    COMP=X     FOR ALL SELECTED ELEMENTS

        Now print out the table.

        >>> mapdl.pretab().splitlines()[:4]
        ['PRINT ELEMENT TABLE ITEMS PER ELEMENT',
         '       1   0.1073961540E-005  0.1073961540E-005',
         '       2   0.3156317304E-005  0.3156317304E-005',
         '       3   0.5125435148E-005  0.5125435148E-005']

        Note that can access the array directly from APDL:

        >>> mapdl.get_array("elem", 1, "ETAB", "values")
        array([1.07396154e-06, 3.15631730e-06, 5.12543515e-06, ...,
               5.41204700e-06, 3.33649806e-06, 1.13836132e-06])

        """
        return self.run(
            f"PRETAB,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6},{lab7},{lab8},{lab9}",
            **kwargs,
        )

    def sabs(self, key="", **kwargs):
        """Specifies absolute values for element table operations.

        APDL Command: SABS

        Parameters
        ----------
        key
            Absolute value key:

            0 - Use algebraic values in operations.

            1 - Use absolute values in operations.

        Notes
        -----
        Causes absolute values to be used in the SADD, SMULT, SMAX, SMIN, and
        SSUM operations.
        """
        command = f"SABS,{key}"
        return self.run(command, **kwargs)

    def sadd(self, labr="", lab1="", lab2="", fact1="", fact2="", const="", **kwargs):
        """Forms an element table item by adding two existing items.

        APDL Command: SADD

        Parameters
        ----------
        labr
            Label assigned to results.  If same as existing label, the existing
            values will be overwritten by these results.

        lab1
            First labeled result item in operation.

        lab2
            Second labeled result item in operation (may be blank).

        fact1
            Scale factor applied to Lab1. A (blank) or '0' entry defaults to
            1.0.

        fact2
            Scale factor applied to Lab2. A (blank) or '0' entry defaults to
            1.0.

        const
            Constant value.

        Notes
        -----
        Forms a labeled result (see ETABLE command) for the selected elements
        by adding two existing labeled result items according to the operation:

        LabR = (FACT1 x Lab1) + (FACT2 x Lab2) + CONST

        May also be used to scale results for a single labeled result item.  If
        absolute values are requested [SABS,1], absolute values of Lab1 and
        Lab2 are used.
        """
        command = f"SADD,{labr},{lab1},{lab2},{fact1},{fact2},{const}"
        return self.run(command, **kwargs)

    def sallow(
        self,
        strs1="",
        strs2="",
        strs3="",
        strs4="",
        strs5="",
        strs6="",
        **kwargs,
    ):
        """Defines the allowable stress table for safety factor calculations.

        APDL Command: SALLOW

        Parameters
        ----------
        strs1, strs2, strs3, . . . , strs6
            Input up to six allowable stresses corresponding to the temperature
            points [TALLOW].

        Notes
        -----
        Defines the allowable stress table for safety factor calculations
        [SFACT,SFCALC].  Use the STAT command to list current allowable stress
        table.  Repeat SALLOW to zero table and redefine points (6 maximum).

        Safety factor calculations are not supported by PowerGraphics. Both the
        SALLOW and TALLOW commands must be used with the Full Model Graphics
        display method active.
        """
        command = f"SALLOW,{strs1},{strs2},{strs3},{strs4},{strs5},{strs6}"
        return self.run(command, **kwargs)

    def sexp(self, labr="", lab1="", lab2="", exp1="", exp2="", **kwargs):
        """Forms an element table item by exponentiating and multiplying.

        APDL Command: SEXP

        Parameters
        ----------
        labr
            Label assigned to results.  If same as existing label, the existing
            values will be overwritten by these results.

        lab1
            First labeled result item in operation.

        lab2
            Second labeled result item in operation (may be blank).

        exp1
            Exponent applied to Lab1.

        exp2
            Exponent applied to Lab2.

        Notes
        -----
        Forms a labeled result item (see ETABLE command) for the selected
        elements by exponentiating and multiplying two existing labeled result
        items according to the operation:

        ``LabR = (|Lab1|EXP1) x (|Lab2|EXP2)``

        Roots, reciprocals, and divides may also be done with this command.
        """
        command = f"SEXP,{labr},{lab1},{lab2},{exp1},{exp2}"
        return self.run(command, **kwargs)

    def sfact(self, type_="", **kwargs):
        """Allows safety factor or margin of safety calculations to be made.

        APDL Command: SFACT

        Parameters
        ----------
        type\_
            Type of calculation:

            0 - No nodal safety factor or margin of safety calculations.

            1 - Calculate and store safety factors in place of nodal stresses.

            2 - Calculate and store margins of safety in place of nodal stresses.

        Notes
        -----
        Allows safety factor (SF) or margin of safety (MS) calculations to be
        made for the average nodal stresses according to:

        ``SF = SALLOW/|Stress|``

        ``MS = (SALLOW/|Stress|) -- 1.0``

        Calculations are done during the display, select, or sort operation (in
        the active coordinate system [RSYS]) with results stored in place of
        the nodal stresses.  Use the PRNSOL or PLNSOL command to display the
        results.

        The results are meaningful only for the stress (SIG1, SIGE,
        etc.) upon which SALLOW is based.  Nodal temperatures used are those
        automatically stored for the node.  Related commands are SFCALC,
        SALLOW, TALLOW.
        """
        command = f"SFACT,{type_}"
        return self.run(command, **kwargs)

    def sfcalc(self, labr="", labs="", labt="", type_="", **kwargs):
        """Calculates the safety factor or margin of safety.

        APDL Command: SFCALC

        Parameters
        ----------
        labr
            Label assigned to results.  If same as existing label, the existing
            values will be overwritten by these results.

        labs
            Labeled result item corresponding to the element stress.

        labt
            Labeled result item corresponding to the element temperature.

        type\_
            Type of calculation:

            0 or 1 - Use safety factor (SF) calculation.

            2 - Use margin of safety (MS) calculation.

            3 - Use 1/SF calculation.

        Notes
        -----
        Calculates safety factor (SF) or margin of safety (MS) as described for
        the SFACT command for any labeled result item (see ETABLE command) for
        the selected elements.  Use the PRETAB or PLETAB command to display
        results.  Allowable element stress is determined from the SALLOW-TALLOW
        table [SALLOW, TALLOW].
        """
        command = f"SFCALC,{labr},{labs},{labt},{type_}"
        return self.run(command, **kwargs)

    def smax(self, labr="", lab1="", lab2="", fact1="", fact2="", **kwargs):
        """Forms an element table item from the maximum of two other items.

        APDL Command: SMAX

        Parameters
        ----------
        labr
            Label assigned to results.  If same as existing label, the existing
            values will be overwritten by these results.

        lab1
            First labeled result item in operation.

        lab2
            Second labeled result item in operation (may be blank).

        fact1
            Scale factor applied to Lab1. A (blank) or '0' entry defaults to
            1.0.

        fact2
            Scale factor applied to Lab2. A (blank) or '0' entry defaults to
            1.0.

        Notes
        -----
        Forms a labeled result item (see ETABLE command) for the selected
        elements by comparing two existing labeled result items according to
        the operation:

        LabR = (FACT1 x Lab1) cmx (FACT2 x Lab2)

        where "cmx" means "compare and save maximum."  If absolute values are
        requested [SABS,1], the absolute values of Lab1 and Lab2 are used.
        """
        command = f"SMAX,{labr},{lab1},{lab2},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def smin(self, labr="", lab1="", lab2="", fact1="", fact2="", **kwargs):
        """Forms an element table item from the minimum of two other items.

        APDL Command: SMIN

        Parameters
        ----------
        labr
            Label assigned to results.  If same as existing label, the existing
            values will be overwritten by these results.

        lab1
            First labeled result item in operation.

        lab2
            Second labeled result item in operation (may be blank).

        fact1
            Scale factor applied to Lab1. A (blank) or '0' entry defaults to
            1.0.

        fact2
            Scale factor applied to Lab2. A (blank) or '0' entry defaults to
            1.0.

        Notes
        -----
        Forms a labeled result item (see ETABLE command) for the selected
        elements by comparing two existing labeled result items according to
        the operation:

        LabR = (FACT1 x Lab1) cmn (FACT2 x Lab2)

        where "cmn" means "compare and save minimum."  If absolute values are
        requested [SABS,1], the absolute values of Lab1 and Lab2 are used.
        """
        command = f"SMIN,{labr},{lab1},{lab2},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def smult(self, labr="", lab1="", lab2="", fact1="", fact2="", **kwargs):
        """Forms an element table item by multiplying two other items.

        APDL Command: SMULT

        Parameters
        ----------
        labr
            Label assigned to results.  If same as existing label, the existing
            values will be overwritten by these results.

        lab1
            First labeled result item in operation.

        lab2
            Second labeled result item in operation (may be blank).

        fact1
            Scale factor applied to Lab1. A (blank) or '0' entry defaults to
            1.0.

        fact2
            Scale factor applied to Lab2. A (blank) or '0' entry defaults to
            1.0.

        Notes
        -----
        Forms a labeled result item (see ETABLE command) for the selected
        elements by multiplying two existing labeled result items according to
        the operation:

        LabR = (FACT1 x Lab1) x (FACT2 x Lab2)

        May also be used to scale results for a single labeled result item.  If
        absolute values are requested [SABS,1], the absolute values of Lab1 and
        Lab2 are used.
        """
        command = f"SMULT,{labr},{lab1},{lab2},{fact1},{fact2}"
        return self.run(command, **kwargs)

    def ssum(self, **kwargs):
        """Calculates and prints the sum of element table items.

        APDL Command: SSUM

        Notes
        -----
        Calculates and prints the tabular sum of each existing labeled result
        item [ETABLE] for the selected elements.  If absolute values are
        requested [SABS,1], absolute values are used.
        """
        command = f"SSUM,"
        return self.run(command, **kwargs)

    def tallow(
        self,
        temp1="",
        temp2="",
        temp3="",
        temp4="",
        temp5="",
        temp6="",
        **kwargs,
    ):
        """Defines the temperature table for safety factor calculations.

        APDL Command: TALLOW

        Parameters
        ----------
        temp1, temp2, temp3, . . . , temp6
            Input up to six temperatures covering the range of nodal
            temperatures.  Temperatures must be input in ascending order.

        Notes
        -----
        Defines the temperature table for safety factor calculations [SFACT,
        SALLOW].  Use STAT command to list current temperature table.  Repeat
        TALLOW command to zero table and redefine points (6 maximum).

        Safety factor calculations are not supported by PowerGraphics. Both the
        SALLOW and TALLOW commands must be used with the Full Model Graphics
        display method active.
        """
        command = f"TALLOW,{temp1},{temp2},{temp3},{temp4},{temp5},{temp6}"
        return self.run(command, **kwargs)

    def vcross(
        self,
        labxr="",
        labyr="",
        labzr="",
        labx1="",
        laby1="",
        labz1="",
        labx2="",
        laby2="",
        labz2="",
        **kwargs,
    ):
        """Forms element table items from the cross product of two vectors.

        APDL Command: VCROSS

        Parameters
        ----------
        labxr, labyr, labzr
            Label assigned to X, Y, and Z-component of resultant vector.

        labx1, laby1, labz1
            X, Y, and Z-component of first vector label.

        labx2, laby2, labz2
            X, Y, and Z-component of second vector label.

        Notes
        -----
        Forms labeled result items for the selected element from the cross
        product of two vectors:

        {LabXR, LabYR, LabZR} = {LabX1, LabY1, LabZ1} X {LabX2, LabY2, LabZ2}

        Data must be in a consistent coordinate system.  Labels are those
        associated with the ETABLE command.
        """
        command = f"VCROSS,{labxr},{labyr},{labzr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)

    def vdot(
        self,
        labr="",
        labx1="",
        laby1="",
        labz1="",
        labx2="",
        laby2="",
        labz2="",
        **kwargs,
    ):
        """Forms an element table item from the dot product of two vectors.

        APDL Command: VDOT

        Parameters
        ----------
        labr
            Label assigned to dot product result.

        labx1, laby1, labz1
            X, Y, and Z-component of first vector label.

        labx2, laby2, labz2
            X, Y, and Z-component of second vector label.

        Notes
        -----
        Forms labeled result items for the selected element from the dot
        product of two vectors:

        LabR = {LabX1, LabY1, LabZ1} : :  {LabX2, LabY2, LabZ2}

        Data must be in a consistent coordinate system.  Labels are those
        associated with the ETABLE command.
        """
        command = f"VDOT,{labr},{labx1},{laby1},{labz1},{labx2},{laby2},{labz2}"
        return self.run(command, **kwargs)
