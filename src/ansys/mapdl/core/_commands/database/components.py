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

"""These DATABASE commands allow selected subsets of entities to be
named as components for easy selection later on.
"""
from typing import Any, Dict, Literal


class Components:
    def cm(
        self,
        cname: str = "",
        entity: Literal["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE", ""] = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Groups geometry items into a component.

        APDL Command: CM

        Parameters
        ----------
        cname
            An alphanumeric name used to identify this component. Cname may be
            up to 32 characters, beginning with a letter and containing only
            letters, numbers, and underscores.  Component names beginning with
            an underscore (e.g., _LOOP) are reserved for use by ANSYS and
            should be avoided.  Components named "ALL," "STAT," and "DEFA" are
            not permitted. Overwrites a previously defined name.

        entity
            Label identifying the type of geometry items to be grouped:

            VOLU
                Volumes.

            AREA
                Areas.

            LINE
                Lines.

            KP
                Keypoints.

            ELEM
                Elements.

            NODE
                Nodes.

        Notes
        -----
        Components may be further grouped into assemblies [CMGRP].  The
        selected items of the specified entity type will be stored as the
        component.  Use of this component in the select command [CMSEL] causes
        all these items to be selected at once, for convenience.

        A component is a grouping of some geometric entity that can then be
        conveniently selected or unselected.  A component may be redefined by
        reusing a previous component name.  The following entity types may
        belong to a component: nodes, elements, keypoints, lines, areas, and
        volumes.  A component may contain only 1 entity type, but an individual
        item of any entity may belong to any number of components.  Once
        defined, the items contained in a component may then be easily selected
        or unselected [CMSEL].  Components may be listed [CMLIST], modified
        [CMMOD] and deleted [CMDELE].  Components may also be further grouped
        into assemblies [CMGRP].  Other entities associated with the entities
        in a component (e.g., the lines and keypoints associated with areas)
        may be selected by the ALLSEL command.

        An item will be deleted from a component if it has been deleted by
        another operation (see the KMODIF command for an example).  Components
        are automatically updated to reflect deletions of one or more of their
        items.  Components are automatically deleted and a warning message is
        issued if all their items are deleted.  Assemblies are also
        automatically updated to reflect deletions of one or more of their
        components or subassemblies, but are not deleted if all their
        components and subassemblies are deleted.

        This command is valid in any processor.

        Examples
        --------

        Create a component selection named ``"PRES_A"`` after
        selecting the areas located in the Y plane at `loc`.

        >>> mapdl.asel('S', 'LOC', 'Y', loc)
        >>> mapdl.cm('PRES_A', 'AREA')
        """
        command = f"CM,{cname}, {entity}"
        return self.run(command, **kwargs)

    def cmdele(self, name: str = "", **kwargs: Dict[Any, Any]) -> None:
        """Deletes a component or assembly definition.

        APDL Command: CMDELE

        Parameters
        ----------
        name
            Name of the component or assembly whose definition is to be
            removed.

        Notes
        -----
        Entities contained in the component, or the components within the
        assembly, are unaffected.  Only the grouping relationships are deleted.
        Assemblies are automatically updated to reflect deletion of their
        components or subassemblies, but they are not automatically deleted
        when all their components or subassemblies are deleted.

        This command is valid in any processor.
        """
        command = f"CMDELE, {name}"
        return self.run(command, **kwargs)

    def cmedit(
        self,
        aname: str = "",
        oper: str = "",
        cnam1: str = "",
        cnam2: str = "",
        cnam3: str = "",
        cnam4: str = "",
        cnam5: str = "",
        cnam6: str = "",
        cnam7: str = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Edits an existing assembly.

        APDL Command: CMEDIT

        Parameters
        ----------
        aname
            Name of the assembly to be edited.

        oper
            Operation label:

            ADD
                To add more components.  The level of any assembly to be added must be lower
                than that of the assembly Aname (see CMGRP command).

            DELE
                To remove components.

        cnam1, cnam2, cnam3, . . . , cnam7
            Names of components and assemblies to be added to or deleted from
            the assembly.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"CMEDIT,{aname},{oper},{cnam1},{cnam2},{cnam3},{cnam4},{cnam5},{cnam6},{cnam7}"  # noqa : E501
        return self.run(command, **kwargs)

    def cmgrp(
        self,
        aname: str = "",
        cnam1: str = "",
        cnam2: str = "",
        cnam3: str = "",
        cnam4: str = "",
        cnam5: str = "",
        cnam6: str = "",
        cnam7: str = "",
        cnam8: str = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Groups components and assemblies into an assembly.

        APDL Command: CMGRP

        Parameters
        ----------
        aname
            An alphanumeric name used to identify this assembly.  Aname may be
            up to 32 characters, beginning with a letter and containing only
            letters, numbers, and underscores.  Overwrites a previously defined
            Aname (and removes it from higher level assemblies, if any).

        cnam1, cnam2, cnam3, . . . , cnam8
            Names of existing components or other assemblies to be included in
            this assembly.

        Notes
        -----
        Groups components and other assemblies into an assembly identified by a
        name.  CMGRP is used for the initial definition of an assembly.  An
        assembly is used in the same manner as a component.  Up to 5 levels of
        assemblies within assemblies may be used.

        An assembly is a convenient grouping of previously defined components
        and other assemblies.  Assemblies may contain components only, other
        assemblies, or any combination.  A component may belong to any number
        of assemblies.  Up to 5 levels of nested assemblies may be defined.
        Components and assemblies may be added to or deleted from an existing
        assembly by the CMEDIT command.  Once defined, an assembly may be
        listed, deleted, selected, or unselected using the same commands as for
        a component.  Assemblies are automatically updated to reflect deletions
        of one or more of their components or lower-level assemblies.
        Assemblies are not automatically deleted when all their components or
        subassemblies are deleted.

        This command is valid in any processor.
        """
        command = f"CMGRP,{aname},{cnam1},{cnam2},{cnam3},{cnam4},{cnam5},{cnam6},{cnam7},{cnam8}"  # noqa : E501
        return self.run(command, **kwargs)

    def cmlist(
        self,
        name: str = "",
        key: str = "",
        entity: Literal["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE", ""] = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Lists the contents of a component or assembly.

        APDL Command: CMLIST

        Parameters
        ----------
        name
            Name of the component or assembly to be listed (if blank, list all
            selected components and assemblies). If Name is specified, then
            Entity  is ignored.

        key
            Expansion key:

            0
                Do not list individual entities in the component.

            1 or EXPA
                List individual entities in the component.

        entity
            If Name is blank, then the following entity types can be specified:

            VOLU
                List the volume components only.

            AREA
                List the area components only.

            LINE
                List the line components only.

            KP
                List the keypoint components only

            ELEM
                List the element components only.

            NODE
                List the node components only.

        Notes
        -----
        This command is valid in any processor.  For components, it lists the
        type of geometric entity. For assemblies, it lists the components
        and/or assemblies that make up the assembly.

        Examples of possible usage:
        """
        command = f"CMLIST,{name},{key},{entity}"
        return self.run(command, **kwargs)

    def cmmod(
        self,
        cname: str = "",
        keyword: str = "",
        value: str = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Modifies the specification of a component.

        APDL Command: CMMOD

        Parameters
        ----------
        cname
            Name of the existing component or assembly to be modified.

        keyword
            The label identifying the type of value to be modified.

        value
            If Keyword is NAME, then the value is the alphanumeric label to be
            applied. See the CM command for naming convention details. If a
            component named Value already exists, the command will be ignored
            and an error message will be generated.

        Notes
        -----
        The naming conventions for components, as specified in the CM command,
        apply for CMMOD (32 characters, "ALL", "STAT" and "DEFA" are not
        allowed, etc.). However, if you choose a component name that is already
        designated for another component, an error message will be issued and
        the command will be ignored.

        This command is valid in any processor.
        """
        command = f"CMMOD,{cname},{keyword},{value}"
        return self.run(command, **kwargs)

    def cmplot(
        self,
        label: str = "",
        entity: str = "",
        keyword: str = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Plots the entities contained in a component or assembly.

        APDL Command: CMPLOT

        Parameters
        ----------
        label
            Name of the component or assembly to be plotted.

            (blank)
                All selected components and assemblies are plotted (default).  If fewer than 11
                components are selected, then all  are plotted.  If more
                than 11 components are selected, then only the first 11
                are plotted.

            ALL
                All selected components are plotted. If number of selected components is
                greater than 11, then the legend showing component names will
                not be shown.

            N
                Next set of defined components and assemblies is plotted.

            P
                Previous set of defined components and assemblies is plotted.

            Cname
                The specified component or assembly is plotted.

            SetNo.
                The specified set number is plotted.

        entity
            If Label is BLANK or ALL, then the following entity types can be
            specified:

            VOLU
                Plot the volume components only.

            AREA
                Plot the area components only.

            LINE
                Plot the line components only.

            KP
                Plot the keypoint components only.

            ELEM
                Plot the element components only.

            NODE
                Plot the node components only.

        keyword
            For Keyword = ALL, plot the specified component name in the Label
            field in the context of all entities of the same type. Not valid if
            Label field is BLANK or ALL.

        Notes
        -----
        Components are plotted with their native entities.  For assemblies, all
        native entities for the underlying component types are plotted
        simultaneously.  Although more components can be plotted, the legend
        displays only 11 at a time. When more than eleven are plotted, the
        legend is not displayed.

        Possible usage:

        This command is valid in any processor.
        """
        command = f"CMPLOT,{label},{entity},{keyword}"
        return self.run(command, **kwargs)

    def cmsel(
        self,
        type_: str = "",
        name: str = "",
        entity: Literal["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE", ""] = "",
        **kwargs: Dict[Any, Any],
    ) -> None:
        """Selects a subset of components and assemblies.

        APDL Command: CMSEL

        Parameters
        ----------
        type_

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
                Also select all components.

            NONE
                Unselect all components.

        name
            Name of component or assembly whose items are to be selected (valid
            only if Type = S, R, A, or U).

        entity
            If Name is blank, then the following entity types can be specified:

            VOLU
                Select the volume components only.

            AREA
                Select the area components only.

            LINE
                Select the line components only.

            KP
                Select the keypoint components only.

            ELEM
                Select the element components only.

            NODE
                Select the node components only.

        Notes
        -----
        Selecting by component is a convenient adjunct to individual item
        selection (e.g., VSEL, ESEL, etc.). CMSEL, ALL allows you to select
        components in addition to other items you have already selected.

        If Type = R for an assembly selection [CMSEL,R,<assembly-name>], the
        reselect operation is performed on each component in the assembly in
        the order in which the components make up the assembly.  Thus, if one
        reselect operation results in an empty set, subsequent operations will
        also result in empty sets.  For example, if the first reselect
        operation tries to reselect node 1 from the selected set of nodes 3, 4,
        and 5, the operation results in an empty set (that is, no nodes are
        selected).  Since the current set is now an empty set, if the second
        reselect operation tries to reselect any nodes, the second operation
        also results in an empty set, and so on.  This is equivalent to
        repeating the command CMSEL,R,<component-name> once for each component
        making up the assembly.

        This command is valid in any processor.
        """
        command = f"CMSEL,{type_},{name},{entity}"
        return self.run(command, **kwargs)

    def cmwrite(
        self,
        fname: str = "",
        ext: str = "",
        fmat: str = "",
        **kwargs: Dict[Any, Any],
    ) -> str:
        """Writes node and element components and assemblies to a file.

        APDL Command: CMWRITE

        Parameters
        ----------
        Fname
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path). An unspecified directory
            path defaults to the working directory; in this case, you can use
            all 248 characters for the file name.
            The file name defaults to ``Jobname``.
        Ext
            Filename extension (eight-character maximum).
            The extension defaults to ``CM`` if ``fname`` is blank.

        Fmat
            Format of the output file (defaults to ``BLOCKED``).

            * ``BLOCKED``: Blocked format. This format allows faster
              reading of the file.

            * ``UNBLOCKED``: Unblocked format.

        """
        command = f"CMWRITE,{fname},{ext},,,{fmat}"
        return self.run(command, **kwargs)
