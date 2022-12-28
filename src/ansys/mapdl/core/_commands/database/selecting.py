"""These DATABASE commands are used to select subsets of database
entities for further operations.
"""

from typing import Optional, Union

from ansys.mapdl.core.mapdl_types import MapdlInt


class Selecting:
    def allsel(self, labt="", entity="", **kwargs):
        """Selects all entities with a single command.

        APDL Command: ALLSEL

        Parameters
        ----------
        labt
            Type of selection to be made:

            ALL - Selects all items of the specified entity type and all
                  items of lower entity types (default).

            BELOW - Selects all items directly associated with and below
                    the selected items of the specified entity type.

        entity
            Entity type on which selection is based:

            ALL - All entity types (default).

            VOLU - Volumes.

            AREA - Areas.

            LINE - Lines.

            KP - Keypoints.

            ELEM - Elements.

            NODE - Nodes.

        Notes
        -----
        ALLSEL is a convenience command that allows the user to select all
        items of a specified entity type or to select items associated with the
        selected items of a higher entity.

        An entity hierarchy is used to decide what entities will be available
        in the selection process.  This hierarchy from top to bottom is as
        follows:  volumes, areas, lines, keypoints, elements, and nodes.  The
        hierarchy may also be divided into two branches:  the solid model and
        the finite element model.  The label ALL selects items based on one
        branch only, while BELOW uses the entire entity hierarchy.  For
        example, ALLSEL,ALL,VOLU selects all volumes, areas, lines, and
        keypoints in the data base.  ALLSEL,BELOW,AREA selects all lines
        belonging to the selected areas; all keypoints belonging to those
        lines; all elements belonging to those areas, lines, and keypoints; and
        all nodes belonging to those elements.

        The $ character should not be used after the  ALLSEL  command.

        This command is valid in any processor.

        Examples
        --------
        >>> mapdl.allsel()
        """
        command = "ALLSEL,%s,%s" % (str(labt), str(entity))
        return self.run(command, **kwargs)

    def asll(self, type_="", arkey="", **kwargs):
        """Selects those areas containing the selected lines.

        APDL Command: ASLL

        Parameters
        ----------
        type\_
            Label identifying the type of area select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        arkey
            Specifies whether all contained area lines must be selected [LSEL]:

            0 - Select area if any of its lines are in the selected line set.

            1 - Select area only if all of its lines are in the selected line set.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "ASLL,%s,%s" % (str(type_), str(arkey))
        return self.run(command, **kwargs)

    def asel(
        self,
        type_="",
        item="",
        comp="",
        vmin="",
        vmax="",
        vinc="",
        kswp="",
        **kwargs,
    ):
        """Selects a subset of areas.

        APDL Command: ASEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Select a new set (default)

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

            ALL - Restore the full set.

            NONE - Unselect the full set.

            INVE - Invert the current set (selected becomes unselected and vice versa).

            STAT - Display the current select status.


        The following fields are used only with Type = S, R, A, or U:

        Item
            Label identifying data. Valid item labels are shown in Table 105: ASEL - Valid Item and Component
            Labels (p. 185). Some items also require a component label. If Item = PICK (or simply "P"), graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). Defaults
            to AREA.

        Comp
            Component of the item (if required). Valid component labels are shown in Table 105: ASEL - Valid
            Item and Component Labels (p. 185).

        VMIN
            Minimum value of item range. Ranges are area numbers, coordinate values, attribute numbers, etc.,
            as appropriate for the item. A component name (as specified on the CM (p. 338) command) may
            also be substituted for VMIN (VMAX and VINC are ignored). If Item = MAT, TYPE, REAL, or ESYS
            and if VMIN is positive, the absolute value of Item is compared against the range for selection; if
            VMIN is negative, the signed value of Item is compared. See the ALIST (p. 106) command for a
            discussion of signed attributes.

        VMAX
            Maximum value of item range. VMAX defaults to VMIN.

        VINC
            Value increment within range. Used only with integer ranges (such as for area numbers). Defaults
            to 1. VINC cannot be negative.

        KSWP
            Specifies whether only areas are to be selected:

                - `kswp = 0` - Select areas only.
                - `kswp = 1` - Select areas, as well as keypoints, lines, nodes, and elements associated with selected areas.

            Valid only with Type = S.


        Notes
        -----
        Selects a subset of areas. For example, to select those areas with area
        numbers 1 through 7, use

        >>> mapdl.asel('S','AREA', '', 1, 7)

        The selected subset is then used when the ALL label is entered
        (or implied) on other commands, such as

        >>> mapdl.alist('ALL')

        Only data identified by area number are selected.  Data
        are flagged as selected and unselected; no data are actually deleted
        from the database.

        In a cyclic symmetry analysis, area hot spots can be modified.
        Consequently, the result of an area selection may be different before
        and after the CYCLIC command.

        If Item = ACCA, the command selects only those areas that were created
        by concatenation.  The KSWP field is processed, but the Comp, VMIN,
        VMAX, and VINC fields are ignored.

        This command is valid in any processor.

        For Selects based on non-integer numbers (coordinates, results, etc.),
        items that are within the range VMIN-Toler and VMAX+Toler are selected.
        The default tolerance Toler is based on the relative values of VMIN and
        VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

        If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX-VMIN).

        Use the SELTOL command to override this default and specify Toler
        explicitly.

        Table: 127:: : ASEL - Valid Item and Component Labels

        Examples
        --------
        Select area(s) at location x == 0.  Note that value of seltol is
        used since ``vmin == vmax``.

        >>> mapdl.asel('S', 'LOC', 'X', 0)

        Select areas between ``y == 2`` and ``y == 4``

        >>> mapdl.asel('S', 'LOC', 'Y', 2, 4)

        """
        command = f"ASEL,{type_},{item},{comp},{vmin},{vmax},{vinc},{kswp}"
        return self.run(command, **kwargs)

    def aslv(self, type_="", **kwargs):
        """Selects those areas contained in the selected volumes.

        APDL Command: ASLV

        Parameters
        ----------
        type\_
            Label identifying the type of area select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        This command is valid in any processor.
        """
        return self.run(f"ASLV,{type_}", **kwargs)

    def dofsel(
        self,
        type_="",
        dof1="",
        dof2="",
        dof3="",
        dof4="",
        dof5="",
        dof6="",
        **kwargs,
    ):
        """Selects a DOF label set for reference by other commands.

        APDL Command: DOFSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Select a new set of labels.

            A - Add labels to the current set.

            U - Unselect (remove) labels from the current set.

            ALL - Restore the full set of labels.

            STAT - Display the current select status.

        dof1, dof2, dof3, . . . , dof6
            Used only with Type = S, A, or U.  Valid structural labels:  UX,
            UY, or UZ (displacements); U (UX, UY, and UZ);  ROTX, ROTY, or ROTZ
            (rotations); ROT (ROTX, ROTY, and ROTZ);  DISP (U and ROT); HDSP
            (Hydrostatic pressure). Valid thermal labels: TEMP, TBOT, TE2, TE3,
            . . ., TTOP (temperature).  Valid acoustic labels:  PRES
            (pressure); UX, UY, or UZ (displacements for FSI coupled elements).
            Valid electric labels:  VOLT (voltage); EMF (electromotive force
            drop); CURR (current).  Valid magnetic labels:  MAG (scalar
            magnetic potential); AX, AY or AZ (vector magnetic potentials); A
            (AX, AY and AZ); CURR (current).  Valid structural force labels:
            FX, FY, or FZ (forces); F (FX, FY, and FZ); MX, MY, or MZ
            (moments); M (MX, MY, and MZ);  FORC (F and M); DVOL (fluid mass
            flow rate).  Valid thermal force labels:  HEAT, HBOT, HE2, HE3, . .
            ., HTOP (heat flow).  Valid fluid flow force labels:  FLOW (fluid
            flow).  Valid electric force labels:  AMPS (current flow); CHRG
            (electric charge).  Valid magnetic force labels:  FLUX (scalar
            magnetic flux); CSGX, CSGY, or CSGZ (magnetic current segments);
            CSG (CSGX, CSGY, and CSGZ). Valid diffusion labels: CONC
            (concentration); RATE (diffusion flow rate).

        Notes
        -----
        Selects a degree of freedom label set for reference by other commands.
        The label set is used on certain commands where ALL is either input in
        the degree of freedom label field or implied.  The active label set has
        no effect on the solution degrees of freedom.  Specified labels which
        are not active in the model (from the ET or DOF command) are ignored.
        As a convenience, a set of force labels corresponding to the degree of
        freedom labels is also selected.  For example, selecting UX also causes
        FX to be selected (and vice versa).  The force label set is used on
        certain commands where ALL is input in the force label field.

        This command is valid in any processor.
        """
        command = "DOFSEL,%s,%s,%s,%s,%s,%s,%s" % (
            str(type_),
            str(dof1),
            str(dof2),
            str(dof3),
            str(dof4),
            str(dof5),
            str(dof6),
        )
        return self.run(command, **kwargs)

    def esel(
        self,
        type_: str = "",
        item: str = "",
        comp: str = "",
        vmin: Union[str, int, float] = "",
        vmax: Union[str, int, float] = "",
        vinc: MapdlInt = "",
        kabs: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Selects a subset of elements.

        APDL Command: ESEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            - S - Select a new set (default).
            - R - Reselect a set from the current set.
            - A - Additionally select a set and extend the current set.
            - U - Unselect a set from the current set.
            - ALL - Restore the full set.
            - NONE - Unselect the full set.
            - INVE - Invert the current set (selected becomes
              unselected and vice versa).
            - STAT - Display the current select status.

        item
            Label identifying data, see Table 110: ESEL - Valid Item
            and Component Labels. Some items also require a
            component label. Defaults to ELEM. If Item = STRA
            (straightened), elements are selected whose midside nodes
            do not conform to the curved line or non-flat area on
            which they should lie. (Such elements are sometimes
            formed during volume meshing (VMESH) in an attempt to
            avoid excessive element distortion.) You should
            graphically examine any such elements to evaluate their
            possible effect on solution accuracy.

        comp
            Component of the item (if required). Valid component
            labels are shown in Table 110: ESEL - Valid Item and
            Component Labels below.

        vmin
            Minimum value of item range. Ranges are element numbers,
            attribute numbers, load values, or result values
            as appropriate for the item. A component name (as
            specified via the CM command) can also be substituted for
            VMIN (in which case VMAX and VINC are ignored).

        vmax
            Maximum value of item range. VMAX defaults to VMIN for
            input values. For result values, VMAX defaults to infinity if VMIN is
            positive, or to zero if VMIN is negative.

        vinc
            Value increment within range. Used only with integer
            ranges (such as for element and attribute numbers).
            Defaults to 1. VINC cannot be negative.

        kabs
            Absolute value key:

                - `kabs = 0` - Check sign of value during selection.
                - `kabs = 1` - Use absolute value during selection (sign
                  ignored).

        Notes
        -----
        The fields `item`, `comp`, `vmin`, `vmax`, `vinc` and `kabs` are
        used only with `type_` = `"S"`, `"R"`, `"A"`, or `"U"`.

        Selects elements based on values of a labeled item and
        component. For example, to select a new set of elements
        based on element numbers 1
        through 7, use

        >>> mapdl.esel('S', 'ELEM', '', 1, 7)

        The subset is used when the ALL label is entered (or implied)
        on other commands, such as

        >>> mapdl.elist('ALL')

        Only data identified by element number are
        selected. Selected data are internally flagged; no actual
        removal of data from the database occurs. Different element
        subsets cannot be used for different load steps [SOLVE] in a
        /SOLU sequence.  The subset used in the first load step
        will be used for all subsequent load steps regardless of
        subsequent ESEL specifications.

        This command is valid in any processor.

        Elements crossing the named path (see PATH command) will be
        selected. This option is only available in PREP7 and POST1.
        If no geometry data has been mapped to the path (i.e.,
        via PMAP and PDEF commands), the path will assume the default
        mapping option (PMAP,UNIFORM) to map the geometry prior to
        selecting the elements. If an invalid path name is
        given, the ESEL command is ignored (status of selected
        elements is unchanged). If there are no elements crossing the
        path, the ESEL command will return zero elements selected.

        For selections based on non-integer numbers (coordinates,
        results, etc.), items that are within the range VMIN -Toler
        and VMAX + Toler are selected. The default tolerance Toler is
        based on the relative values of VMIN and VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

        If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX - VMIN).

        Use the SELTOL command to override this default and specify
        Toler explicitly.

        Table: 133:: : ESEL - Valid Item and Component Labels

        Examples
        --------
        Select elements using material numbers 2, 4 and 6.

        >>> mapdl.esel('S', 'MAT', '', 2, 6, 2)

        Of these, reselect SOLID185 element types

        >>> mapdl.esel('R', 'ENAME', '', 185)

        Select elements assigned to material property 2

        >>> mapdl.esel('S', 'MAT', '', 2)

        Note, this command is equivalent to:

        >>> mapdl.esel('S', 'MAT', vmin=2)

        """
        command = f"ESEL,{type_},{item},{comp},{vmin},{vmax},{vinc},{kabs}"
        return self.run(command, **kwargs)

    def esla(self, type_: str = "", **kwargs) -> Optional[str]:
        """Selects those elements associated with the selected areas.

        APDL Command: ESLA

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
        Selects area elements belonging to meshed [AMESH], selected
        [ASEL] areas.

        This command is valid in any processor.
        """
        command = f"ESLA,{type_}"
        return self.run(command, **kwargs)

    def esll(self, type_: str = "", **kwargs) -> Optional[str]:
        """Selects those elements associated with the selected lines.

        APDL Command: ESLL

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
        Selects line elements belonging to meshed [LMESH], selected
        [LSEL] lines.

        This command is valid in any processor.
        """
        command = f"ESLL,{type_}"
        return self.run(command, **kwargs)

    def esln(
        self, type_: str = "", ekey: MapdlInt = "", nodetype: str = "", **kwargs
    ) -> Optional[str]:
        """Selects those elements attached to the selected nodes.

        APDL Command: ESLN

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

            0 - Select element if any of its nodes are in the
            selected nodal set (default).

            1 - Select element only if all of its nodes are in the
            selected nodal set.

        nodetype
            Label identifying type of nodes to consider when selecting:

            ALL - Select elements considering all of their nodes (
                  default).

            ACTIVE - Select elements considering only their active
                     nodes. An active node is a node
                     that contributes DOFs to the model.

            INACTIVE - Select elements considering only their
                       inactive nodes (such as orientation or
                       radiation nodes).

            CORNER - Select elements considering only their corner
                     nodes.

            MID - Select elements considering only their midside nodes.

        Notes
        -----
        ESLN selects elements which have any (or all EKEY) NodeType
        nodes in the currently-selected set of nodes. Only elements
        having nodes in the currently-selected set can be selected.

        This command is valid in any processor.
        """
        command = f"ESLN,{type_},{ekey},{nodetype}"
        return self.run(command, **kwargs)

    def eslv(self, type_: str = "", **kwargs) -> Optional[str]:
        """Selects elements associated with the selected volumes.

        APDL Command: ESLV

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
        Selects volume elements belonging to meshed [VMESH], selected
        [VSEL]
        volumes.

        This command is valid in any processor.
        """
        command = f"ESLV,{type_}"
        return self.run(command, **kwargs)

    def ksel(
        self,
        type_="",
        item="",
        comp="",
        vmin="",
        vmax="",
        vinc="",
        kabs="",
        **kwargs,
    ):
        """Selects a subset of keypoints or hard points.

        APDL Command: KSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S
              Select a new set (default).

            R
              Reselect a set from the current set.

            A
              Additionally select a set and extend the current set.

            U
              Unselect a set from the current set.

            ALL
              Restore the full set.

            NONE
              Unselect the full set.

            INVE
              Invert the current set (selected becomes unselected and vice versa).

            STAT
              Display the current select status.


        The following fields are used only with Type = S, R, A, or U:

        Item
            Label identifying data. Valid item labels are shown in the table below. Some items also require a
            component label. If Item = PICK (or simply "P"), graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). Defaults to KP.

        Comp
            Component of the item (if required). Valid component labels are shown in the table below.

        VMIN
            Minimum value of item range. Ranges are keypoint numbers, coordinate values, attribute numbers,
            etc., as appropriate for the item. A component name (as specified on the CM (p. 338) command)
            may also be substituted for VMIN (VMAX and VINC are ignored). If Item = MAT, TYPE, REAL, or
            ESYS and if VMIN is positive, the absolute value of Item is compared against the range for selection;
            if VMIN is negative, the signed value of Item is compared. See the KLIST (p. 942) command for a
            discussion of signed attributes.

        VMAX
            Maximum value of item range. VMAX defaults to VMIN.

        VINC
            Value increment within range. Used only with integer ranges (such as for keypoint numbers). Defaults
            to 1. VINC cannot be negative.

        KABS
            Absolute value key:

                - `kabs = 0` - Check sign of value during selection.
                - `kabs = 1` - Use absolute value during selection (sign ignored).

        Notes
        -----
        Selects a subset of keypoints or hard points.  For example, to select a
        new set of keypoints based on keypoint numbers 1 through 7, use

        >>> mapdl.ksel('S', 'KP', '', 1, 7)

        The selected subset is used when the ALL label is
        entered (or implied) on other commands, such as KLIST,ALL.  Only data
        identified by keypoint number are selected.  Data are flagged as
        selected and unselected; no data are actually deleted from the
        database.

        This command is valid in any processor.

        For selections based on non-integer numbers (coordinates, results,
        etc.), items that are within the range VMIN -Toler and VMAX + Toler are
        selected. The default tolerance Toler is based on the relative values
        of VMIN and VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

         If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX - VMIN).

        Use the SELTOL command to override this default and specify Toler
        explicitly.

        Table: 203:: : KSEL - Valid Item and Component Labels

        Examples
        --------
        To select a single keypoint (keypoint 1)

        >>> mapdl.ksel('S', 'KP', '', 1)
        """
        command = "KSEL,%s,%s,%s,%s,%s,%s,%s" % (
            str(type_),
            str(item),
            str(comp),
            str(vmin),
            str(vmax),
            str(vinc),
            str(kabs),
        )
        return self.run(command, **kwargs)

    def ksll(self, type_="", **kwargs):
        """Selects those keypoints contained in the selected lines.

        APDL Command: KSLL

        Parameters
        ----------
        type\_
            Label identifying the type of keypoint select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "KSLL,%s" % (str(type_))
        return self.run(command, **kwargs)

    def ksln(self, type_="", **kwargs):
        """Selects those keypoints associated with the selected nodes.

        APDL Command: KSLN

        Parameters
        ----------
        type\_
            Label identifying the type of keypoint select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        Valid only if the nodes were generated by a meshing operation [KMESH,
        LMESH, AMESH, VMESH] on a solid model that contains the associated
        keypoints.

        This command is valid in any processor.
        """
        command = "KSLN,%s" % (str(type_))
        return self.run(command, **kwargs)

    def lsel(
        self,
        type_="",
        item="",
        comp="",
        vmin="",
        vmax="",
        vinc="",
        kswp="",
        **kwargs,
    ):
        """Selects a subset of lines.

        APDL Command: LSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

            ALL - Restore the full set.

            NONE - Unselect the full set.

            INVE - Invert the current set (selected becomes unselected and vice versa).

            STAT - Display the current select status.


        The following fields are used only with Type = S, R, A, or U:

        Item
            Label identifying data. Valid item labels are shown in the table
            below. Some items also require a component label. If Item = PICK
            (or simply "P"), graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). Defaults to
            LINE.

        Comp
            Component of the item (if required). Valid component labels are
            shown in the table below.

        VMIN
            Minimum value of item range. Ranges are line numbers, coordinate
            values, attribute numbers, etc., as appropriate for the item. If
            VMIN = 0.0, a tolerance of ±1.0E-6 is used, or ±0.005 x VMIN if
            VMIN = VMAX. A component name (as specified on the CM (p. 338)
            command) may also be substituted for VMIN (VMAX and VINC are
            ignored). If Item = MAT, TYPE, REAL, ESYS, or NDIV and if VMIN is
            positive, the absolute value of Item is compared against the range
            for selection; if VMIN is negative, the signed value of Item is
            compared. See the LLIST (p. 1011) command for a discussion of
            signed attributes.

        VMAX
            Maximum value of item range. VMAX defaults to VMIN.

        VINC
            Value increment within range. Used only with integer ranges (such
            as for line numbers). Defaults to 1. VINC cannot be negative.

        KSWP
            Specifies whether only lines are to be selected:

                - ``kswp=0`` - Select lines only.  ``kswp=1`` - Select lines,
                - as well as keypoints, nodes, and elements associated with
                - selected lines. Valid only with ``type="s"``.

        Notes
        -----
        Selects lines based on values of a labeled item and component.  For
        example, to select a new set of lines based on line numbers 1 through
        7, use LSEL,S,LINE,,1,7.  The subset is used when the ALL label is
        entered (or implied) on other commands, such as LLIST,ALL.  Only data
        identified by line number are selected.  Data are flagged as selected
        and unselected; no data are actually deleted from the database.

        If Item = LCCA, the command selects only those lines that were created
        by concatenation.  The KSWP field is processed, but the Comp, VMIN,
        VMAX, and VINC fields are ignored.

        If Item = HPT, the command selects only those lines that contain hard
        points.

        Item = RADIUS is only valid for lines that are circular arcs.

        LSEL is valid in any processor.

        For selections based on non-integer numbers (coordinates, results,
        etc.), items that are within the range VMIN -Toler and VMAX +Toler are
        selected. The default tolerance Toler is based on the relative values
        of VMIN and VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

        If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX - VMIN).

        Use the SELTOL command to override this default and specify Toler
        explicitly.

        """
        command = "LSEL,%s,%s,%s,%s,%s,%s,%s" % (
            str(type_),
            str(item),
            str(comp),
            str(vmin),
            str(vmax),
            str(vinc),
            str(kswp),
        )
        return self.run(command, **kwargs)

    def lsla(self, type_="", **kwargs):
        """Selects those lines contained in the selected areas.

        APDL Command: LSLA

        Parameters
        ----------
        type\_
            Label identifying the type of line select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "LSLA,%s" % (str(type_))
        return self.run(command, **kwargs)

    def lslk(self, type_="", lskey="", **kwargs):
        """Selects those lines containing the selected keypoints.

        APDL Command: LSLK

        Parameters
        ----------
        type\_
            Label identifying the type of line select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        lskey
            Specifies whether all contained line keypoints must be selected
            [KSEL]:

            0 - Select line if any of its keypoints are in the selected keypoint set.

            1 - Select line only if all of its keypoints are in the selected keypoint set.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "LSLK,%s,%s" % (str(type_), str(lskey))
        return self.run(command, **kwargs)

    def nsel(
        self,
        type_="",
        item="",
        comp="",
        vmin="",
        vmax="",
        vinc="",
        kabs="",
        **kwargs,
    ):
        """Selects a subset of nodes.

        APDL Command: NSEL

        Parameters
        ----------
        type\_
            Label identifying the type of select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

            ALL - Restore the full set.

            NONE - Unselect the full set.

            INVE - Invert the current set (selected becomes unselected and vice versa).

            STAT - Display the current select status.


        The following fields are used only with Type = S, R, A, or U:

        Item
            Label identifying data. Valid item labels are shown in the table below. Some items also require a
            component label. If Item = PICK (or simply "P"), graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). Defaults to NODE.

        Comp
            Component of the item (if required). Valid component labels are shown in the table below.

        VMIN
            Minimum value of item range. Ranges are node numbers, set numbers, coordinate values, load
            values, or result values as appropriate for the item. A component name (as specified on the CM (p. 338)
            command) may also be substituted for VMIN (VMAX and VINC are ignored).

        VMAX
            Maximum value of item range. VMAX defaults to VMIN for input values. For result values, VMAX
            defaults to infinity if VMIN is positive, or to zero if VMIN is negative.

        VINC
            Value increment within range. Used only with integer ranges (such as for node and set numbers).
            Defaults to 1. VINC cannot be negative.

        KABS
            Absolute value key:

            - `kabs = 0` - Check sign of value during selection.
            - `kabs = 1` - Use absolute value during selection (sign ignored)

        Notes
        -----
        Selects a subset of nodes.  For example, to select a new set of nodes
        based on node numbers 1 through 7, do

        >>> mapdl.nsel('S','NODE','',1,7)

        The subset is used when the `'ALL'` label is entered (or implied)
        on other commands, such as

        >>> mapdl.nlist('ALL')

        Only data identified by node number are selected.  Data
        are flagged as selected and unselected; no data are actually deleted
        from the database.

        When selecting nodes by results, the full graphics value is used,
        regardless of whether PowerGraphics is on.

        Solution result data consists of two types, 1) nodal degree of freedom
        --results initially calculated at the nodes (such as displacement,
        temperature, pressure, etc.), and 2) element--results initially
        calculated elsewhere (such as at an element integration point or
        thickness location) and then recalculated at the nodes (such as
        stresses, strains, etc.).  Various element results also depend upon the
        recalculation method and the selected results location [AVPRIN, RSYS,
        FORCE, LAYER and SHELL].

        You must have all the nodes (corner and midside nodes) on the external
        face of the element selected to use Item = EXT.

        This command is valid in any processor.

        For Selects based on non-integer numbers (coordinates, results, etc.),
        items that are within the range VMIN-Toler and VMAX+Toler are selected.
        The default tolerance Toler is based on the relative values of VMIN and
        VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

         If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX-VMIN).

        Use the SELTOL command to override this default and specify Toler
        explicitly.

        Table: 208:: : NSEL - Valid Item and Component Labels

        Table: 209:: : NSEL - Valid Item and Component Labels for Nodal DOF
        Result Values

        Examples
        --------
        Select nodes at `x == 0`, Of these, reselect nodes between ``1 < Y
        < 10``, then finally unselect nodes between ``5 < Y < 6``.

        >>> mapdl.nsel('S', 'LOC', 'X', 0)
        >>> mapdl.nsel('R', 'LOC', 'Y', 1, 10)
        >>> mapdl.nsel('U', 'LOC', 'Y', 5, 6)

        For other coordinate systems activate the coord system first.
        First, change to cylindrical coordinate system, select nodes at
        ``radius == 5``.  Reselect nodes from 0 to 90 degrees.

        >>> mapdl.csys(1)
        >>> mapdl.nsel('S', 'LOC', 'X', 5)
        >>> mapdl.nsel('R', 'LOC', 'Y', 0, 90)

        Note that the labels X, Y, and Z are always used, regardless of which
        coordinate system is activated. They take on different meanings in
        different systems Additionally, angles are always in degrees and
        NOT radians.

        Select elements assigned to material property 2

        >>> mapdl.esel('S', 'MAT', '', 2)

        Select the nodes these elements use

        >>> mapdl.nsle()

        Reselect nodes on the element external surfaces

        >>> mapdl.nsel('R', 'EXT')

        Change to cylindrical coordinates

        >>> mapdl.csys(1)

        Reselect nodes with radius=5

        >>> mapdl.nsel('R', 'LOC', 'X', 5)
        """
        command = "NSEL,%s,%s,%s,%s,%s,%s,%s" % (
            str(type_),
            str(item),
            str(comp),
            str(vmin),
            str(vmax),
            str(vinc),
            str(kabs),
        )
        return self.run(command, **kwargs)

    def nsla(self, type_="", nkey="", **kwargs):
        """Selects those nodes associated with the selected areas.

        APDL Command: NSLA

        Parameters
        ----------
        type\_
            Label identifying the type of node select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        nkey
            Specifies whether only interior area nodes are to be selected:

            0 - Select only nodes interior to selected areas.

            1 - Select all nodes (interior to area, interior to lines, and at keypoints)
                associated with the selected areas.

        Notes
        -----
        Valid only if the nodes were generated by an area meshing operation
        [AMESH, VMESH] on a solid model that contains the selected areas.

        This command is valid in any processor.

        Examples
        --------
        Select area(s) at location x=0.  Note that the selection tolerance
        above and below 0 will depend on the value of ``mapdl.seltol``

        >>> mapdl.asel('S', 'LOC', 'X', 0)

        Select nodes residing on those areas.

        >>> mapdl.nsla('S', 1)
        """
        command = "NSLA,%s,%s" % (str(type_), str(nkey))
        return self.run(command, **kwargs)

    def nsle(self, type_="", nodetype="", num="", **kwargs):
        """Selects those nodes attached to the selected elements.

        APDL Command: NSLE

        Parameters
        ----------
        type\_
            Label identifying the type of node select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        nodetype
            Label identifying type of nodes to consider when selecting:

            ALL - Select all nodes of the selected elements (default).

            ACTIVE - Select only the active nodes. An active node is a node that contributes DOFs to
                     the model.

            INACTIVE - Select only inactive  nodes (such as orientation or radiation).

            CORNER - Select only corner nodes.

            MID - Select only midside nodes.

            POS - Select nodes in position Num.

            FACE - Select nodes on face Num.

        num
            Position or face number for NodeType = POS or FACE.

        Notes
        -----
        NSLE selects NodeType nodes attached to the currently-selected set of
        elements. Only nodes on elements in the currently-selected element set
        can be selected.

        .. note::
            When using degenerate hexahedral elements, NSLE, U,CORNER and
            NSLE,S,MID will not select the same set of nodes because some
            nodes appear as both corner and midside nodes.

        This command is valid in any processor.

        Examples
        --------
        Select elements assigned to material property 2 and then select
        the nodes these elements use.

        >>> mapdl.esel('S', 'MAT', '', 2)
        >>> mapdl.nsle()
        """
        command = "NSLE,%s,%s,%s" % (str(type_), str(nodetype), str(num))
        return self.run(command, **kwargs)

    def nslk(self, type_="", **kwargs):
        """Selects those nodes associated with the selected keypoints.

        APDL Command: NSLK

        Parameters
        ----------
        type\_
            Label identifying the type of node select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        Notes
        -----
        Valid only if the nodes were generated by a keypoint meshing operation
        [KMESH, LMESH, AMESH, VMESH] on a solid model that contains the
        selected keypoints.

        This command is valid in any processor.
        """
        command = "NSLK,%s" % (str(type_))
        return self.run(command, **kwargs)

    def nsll(self, type_="", nkey="", **kwargs):
        """Selects those nodes associated with the selected lines.

        APDL Command: NSLL

        Parameters
        ----------
        type\_
            Label identifying the type of node select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        nkey
            Specifies whether only interior line nodes are to be selected:

            0 - Select only nodes interior to selected lines.

            1 - Select all nodes (interior to line and at keypoints)
                associated with the selected lines.

        Notes
        -----
        Valid only if the nodes were generated by a line meshing
        operation [LMESH, AMESH, VMESH] on a solid model that contains
        the associated lines.

        This command is valid in any processor.
        """
        command = "NSLL,%s,%s" % (str(type_), str(nkey))
        return self.run(command, **kwargs)

    def nslv(self, type_="", nkey="", **kwargs):
        """Selects those nodes associated with the selected volumes.

        APDL Command: NSLV

        Parameters
        ----------
        type\_
            Label identifying the type of node select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        nkey
            Specifies whether only interior volume nodes are to be selected:

            0 - Select only nodes interior to selected volumes.

            1 - Select all nodes (interior to volume, interior to areas, interior to lines, and
                at keypoints) associated with the selected volumes.

        Notes
        -----
        Valid only if the nodes were generated by a volume meshing operation
        [VMESH] on a solid model that contains the selected volumes.

        This command is valid in any processor.
        """
        command = "NSLV,%s,%s" % (str(type_), str(nkey))
        return self.run(command, **kwargs)

    def partsel(self, type_="", pmin="", pmax="", pinc="", **kwargs):
        """Selects a subset of parts in an explicit dynamic analysis.

        APDL Command: PARTSEL

        Parameters
        ----------
        type\_
            Label identifying type of select. Because PARTSEL is a command
            macro, the label must be enclosed in single quotes.

            'S' - Select a new set (default).

            'R' - Reselect a set from the current set.

            'A' - Additionally select a set and extend the current set.

            'U' - Unselect a set from the current set.

            'ALL' - Select all parts.

            'NONE' - Unselect all parts.

            'INVE' - Invert the current selected set.

        Notes
        -----
        PARTSEL invokes an ANSYS macro that selects parts in an explicit
        dynamic analysis. When PARTSEL is executed, an element component is
        automatically created for each existing part. For example, the elements
        that make up PART 1 are grouped into the element component
        _PART1. Each time the PARTSEL command is executed, components
        for unselected parts will be unselected. To plot selected parts,
        choose Utility Menu> Plot> Parts in the GUI or issue the
        command PARTSEL,'PLOT'.

        After selecting parts, if you change the selected set of nodes or
        elements and then plot parts, the nodes and elements associated with
        the previously selected parts (from the last PARTSEL command) will
        become the currently selected set.

        Note:: : A more efficient way to select and plot parts is to use the
        ESEL (with ITEM = PART) and EPLOT commands. We recommend using ESEL
        instead of PARTSEL since PARTSEL will be phased out in a future
        release. Note that the menu path mentioned above for plotting parts
        does not work with the ESEL command; use Utility Menu> Plot> Elements
        instead.

        In an explicit dynamic small restart analysis (EDSTART,2), PARTSEL can
        be used to unselect a part during the solution even if it is referenced
        in some way (such as in a contact definition). (Note that ESEL cannot
        be used for this purpose.) However, in a new analysis or a full restart
        analysis (EDSTART,3), all parts that are used in some type of
        definition must be selected at the time of solution.

        This command is valid in any processor.

        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = "PARTSEL,%s,%s,%s,%s" % (
            str(type_),
            str(pmin),
            str(pmax),
            str(pinc),
        )
        return self.run(command, **kwargs)

    def vsel(
        self,
        type_="",
        item="",
        comp="",
        vmin="",
        vmax="",
        vinc="",
        kswp="",
        **kwargs,
    ):
        """Selects a subset of volumes.

        APDL Command: VSEL

        Parameters
        ----------
        type\_
            Label identifying the type of volume select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

            ALL - Restore the full set.

            NONE - Unselect the full set.

            INVE - Invert the current set (selected becomes unselected and vice versa).

            STAT - Display the current select status.

        item : str, optional
            Label identifying data. Valid item labels are shown in the table
            below. Some items also require a component label. Defaults to
            VOLU.

        comp : str, optional
            Component of the item (if required).

        vmin : int, optional
            Minimum value of item range. Ranges are volume numbers, coordinate
            values, attribute numbers, etc., as appropriate for the item. A
            component name (as specified on the CM (p. 338) command) may also
            be substituted for VMIN (VMAX and VINC are ignored). If Item = MAT,
            TYPE, REAL, or ESYS and if VMIN is positive, the absolute value of
            Item is compared against the range for selection; if VMIN is
            negative, the signed value of Item is compared. See the VLIST
            (p. 2050) command for a discussion of signed attributes.

        vmax : int, optional
            Maximum value of item range. VMAX defaults to VMIN.

        vinc : int, optional
            Value increment within range. Used only with integer ranges (such
            as for volume numbers). Defaults to 1. VINC cannot be negative.

        kswp : int, optional
            Specifies whether only volumes are to be selected:

            - ``kswp=0`` - Select volumes only.
            - ``kswp=1`` - Select volumes, as well as keypoints, lines, areas,
              nodes, and elements associated with selected volumes. Valid only
              with Type = S.

        Notes
        -----
        Selects volumes based on values of a labeled item and component.  For
        example, to select a new set of volumes based on volume numbers 1
        through 7, use VSEL,S,VOLU,,1,7.  The subset is used when the ALL label
        is entered (or implied) on other commands, such as VLIST,ALL.  Only
        data identified by volume number are selected.  Data are flagged as
        selected and unselected; no data are actually deleted from the
        database.

        This command is valid in any processor.

        For Selects based on non-integer numbers (coordinates, results, etc.),
        items that are within the range VMIN-Toler and VMAX+Toler are selected.
        The default tolerance Toler is based on the relative values of VMIN and
        VMAX as follows:

        If VMIN = VMAX, Toler = 0.005 x VMIN.

        If VMIN = VMAX = 0.0, Toler = 1.0E-6.

        If VMAX ≠ VMIN, Toler = 1.0E-8 x (VMAX-VMIN).

        Use the SELTOL command to override this default and specify Toler
        explicitly.

        """
        command = "VSEL,%s,%s,%s,%s,%s,%s,%s" % (
            str(type_),
            str(item),
            str(comp),
            str(vmin),
            str(vmax),
            str(vinc),
            str(kswp),
        )
        return self.run(command, **kwargs)

    def vsla(self, type_="", vlkey="", **kwargs):
        """Selects those volumes containing the selected areas.

        APDL Command: VSLA

        Parameters
        ----------
        type\_
            Label identifying the type of volume select:

            S - Select a new set (default).

            R - Reselect a set from the current set.

            A - Additionally select a set and extend the current set.

            U - Unselect a set from the current set.

        vlkey
            Specifies whether all contained volume areas must be selected
            [ASEL]:

            0 - Select volume if any of its areas are in the selected area set.

            1 - Select volume only if all of its areas are in the selected area set.

        Notes
        -----
        This command is valid in any processor.
        """
        command = "VSLA,%s,%s" % (str(type_), str(vlkey))
        return self.run(command, **kwargs)

    def seltol(self, toler="", **kwargs):
        """Select those volumes containing the selected areas.

        APDL Command: SELTOL

        Parameters
        ----------
        toler
            Tolerance value. If blank or None, restores the default tolerance
            logic.

        Notes
        -----
        For selects based on non-integer numbers (e.g. coordinates,
        results, etc.), items within the range VMIN - Toler and VMAX +
        Toler are selected, where VMIN and VMAX are the range values input
        on the xSEL commands (ASEL, ESEL, KSEL, LSEL, NSEL, and VSEL).

        The default tolerance logic is based on the relative values of
        VMIN and VMAX as follows:

        If ``vmin == vmax``, ``toler = 0.005*vmin``

        If ``vmin == vmax == 0.0``, ``toler = 1.0E-6``.

        If ``vmax != vmin``, ``toler = 1.0E-8 x (vmax - vmin)``.

        This command is typically used when ``vmax - vmin`` is very large so
        that the computed default tolerance is therefore large and the
        xSEL commands selects more than what is desired.

        Toler remains active until respecified by a subsequent seltol
        command. ``seltol()`` resets back to the default toler value.

        Examples
        --------
        Set selection tolarance to 1E-5

        >>> seltol(1E-5)

        """
        if toler:
            cmd = f"SELTOL,{toler}"
        else:
            cmd = "SELTOL"
        return self.run(cmd, **kwargs)
