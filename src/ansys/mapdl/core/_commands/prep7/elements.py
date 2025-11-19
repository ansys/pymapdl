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

from ansys.mapdl.core._commands import parse


class Elements:

    def afsurf(self, sarea: str = "", tline: str = "", **kwargs):
        r"""Generates surface elements overlaid on the surface of existing solid elements and assigns the extra
        node as the closest fluid element node.

        Mechanical APDL Command: `AFSURF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AFSURF.html>`_

        Parameters
        ----------
        sarea : str
            Component name for the surface areas of the meshed solid volumes. The component name must be 32
            characters or less.

        tline : str
            Component name for the target lines meshed with fluid elements. The component name must be 32
            characters or less.

        Notes
        -----

        .. _AFSURF_notes:

        This command macro is used to generate surface effect elements overlaid on the surface of existing
        solid elements and, based on proximity, to determine and assign the extra node for each surface
        element. The underlying volumes of the solid region and the fluid lines must be meshed prior to
        calling this command macro. The active element type must be ``SURF152`` with appropriate settings
        for KEYOPT(4), KEYOPT(5), KEYOPT(6), and KEYOPT(8).

        The surface areas of the solid and the target lines of the fluid are grouped into components and
        named using the :ref:`cm` command. The names must be enclosed in single quotes (for example, '
        ``SAREA`` ') when the :ref:`afsurf` command is manually typed in.

        When using the GUI method, node and element components are created through the picking dialog boxes
        associated with this command.

        The macro is applicable for the ``SURF152`` and ``FLUID116`` element types.
        """
        command = f"AFSURF,{sarea},{tline}"
        return self.run(command, **kwargs)

    def dflab(self, dof: str = "", displab: str = "", forcelab: str = "", **kwargs):
        r"""Changes degree-of-freedom labels for user custom elements.

        Mechanical APDL Command: `/DFLAB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DFLAB.html>`_

        Parameters
        ----------
        dof : str
            Number between 1 and 32 indicating which degree of freedom is to have its labels changed. For a list
            of these quantities, see the degree-of-freedom table in the :file:`echprm.inc` file. The first few quantities follow:

            * 1 = UX,FX
            * 2 = UY,FY
            * 3 = UZ,FZ
            * 4 = ROTX,MX

        displab : str
            New label (four-character maximum) for the displacement label. The prior label is no longer
            valid.

        forcelab : str
            New label (four-character maximum) for the force label for this degree of freedom. The prior
            label is no longer valid.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DFLAB.html>`_
           for further explanations.

        **Argument Descriptions**

        .. _s-DFLAB_argdescript:

        * ``dof : str`` - Number between 1 and 32 indicating which degree of freedom is to have its labels
        changed. For a list
          of these quantities, see the degree-of-freedom table in the :file:`echprm.inc` file. The first few quantities follow:

          * 1 = UX,FX
          * 2 = UY,FY
          * 3 = UZ,FZ
          * 4 = ROTX,MX

        * ``displab : str`` - New label (four-character maximum) for the displacement label. The prior label
          is no longer valid.

        * ``forcelab : str`` - New label (four-character maximum) for the force label for this degree of
          freedom. The prior label is no longer valid.

        .. _s-DFLAB_notes:

        The :ref:`dflab` command is rarely used. Use it if you are writing a custom element and want to use
        degrees of freedom that are not part of the standard element set.
        """
        command = f"/DFLAB,{dof},{displab},{forcelab}"
        return self.run(command, **kwargs)

    def e(
        self,
        i: str = "",
        j: str = "",
        k: str = "",
        l: str = "",
        m: str = "",
        n: str = "",
        o: str = "",
        p: str = "",
        **kwargs,
    ):
        r"""Defines an element by node connectivity.

        Mechanical APDL Command: `E <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_E.html>`_

        Parameters
        ----------
        i : str
            Number of node assigned to first nodal position (node I). If ``I`` = P, graphical picking is
            enabled and all remaining command fields are ignored (valid only in the GUI).

        j : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        k : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        l : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        m : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        n : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        o : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        p : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        Notes
        -----

        .. _E_notes:

        Defines an element by its nodes and attribute values. You can specify up to eight nodes. You can add
        more nodes if needed ( :ref:`emore` ).

        The number of nodes required and the order in which they are specified are described in `Element
        Input
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_1.html#aWe8sq3b3ldm>`_
        :ref:`numstr` ) as generated. The current (or default) MAT, TYPE, REAL, SECNUM and ESYS attribute
        values are also assigned to the element.

        When creating elements with more than eight nodes ( :ref:`e` followed by :ref:`emore` ), it may be
        necessary disable shape-checking ( :ref:`shpp` ) before issuing this command.

        If a valid element type can be created without using additional nodes ( :ref:`emore` ), this command
        creates that element. :ref:`emore` then modifies the element to include the additional nodes. If
        shape-checking is active, it occurs before :ref:`emore` is issued. If the shape-checking limits are
        exceeded, therefore, element creation may fail before :ref:`emore` modifies the element into an
        acceptable shape.

        Examples
        --------
        Create a single SURF154 element.

        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SURF154')
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(2, 1, 0, 0)
        >>> mapdl.n(3, 1, 1, 0)
        >>> mapdl.n(4, 0, 1, 0)
        >>> mapdl.e(1, 2, 3, 4)
        1

        Create a single hexahedral SOLID185 element

        >>> mapdl.et(2, 'SOLID185')
        >>> mapdl.type(2)
        >>> mapdl.n(5, 0, 0, 0)
        >>> mapdl.n(6, 1, 0, 0)
        >>> mapdl.n(7, 1, 1, 0)
        >>> mapdl.n(8, 0, 1, 0)
        >>> mapdl.n(9, 0, 0, 1)
        >>> mapdl.n(10, 1, 0, 1)
        >>> mapdl.n(11, 1, 1, 1)
        >>> mapdl.n(12, 0, 1, 1)
        >>> mapdl.e(5, 6, 7, 8, 9, 10, 11, 12)
        2
        """
        command = f"E,{i},{j},{k},{l},{m},{n},{o},{p}"
        return parse.parse_e(self.run(command, **kwargs))

    def ecpchg(self, **kwargs):
        r"""Optimizes degree-of-freedom usage in a coupled acoustic model.

        Mechanical APDL Command: `ECPCHG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ECPCHG.html>`_

        Notes
        -----

        .. _ECPCHG_notes:

        The :ref:`ecpchg` command converts uncoupled acoustic element types to coupled acoustic element
        types that are attached to the fluid-structure interaction interface. Or it converts coupled
        acoustic element types to uncoupled acoustic element types that are not attached to the fluid-
        structure interaction interface. Issuing :ref:`ecpchg` can dramatically reduce the size of the
        :file:`Jobname.EMAT` file, compared to the model fully meshed with the coupled acoustic elements.

        Performing the :ref:`ecpchg` conversion on meshed volumes can create circumstances in which more
        than one element type is defined for a single volume.

        If the acoustic elements are coupled with shell elements ( ``SHELL181`` or ``SHELL281`` ), you must
        set the fluid-structure interaction (FSI) flag by issuing the :ref:`sf`,,FSI command before the
        :ref:`ecpchg` command.

        :ref:`ecpchg` may add new element types to your model, or it may change the element type for
        existing acoustic elements. You should verify the defined element types with :ref:`etlist` and the
        element attributes with :ref:`elist` after using this command.
        """
        command = "ECPCHG"
        return self.run(command, **kwargs)

    def edele(self, iel1: str = "", iel2: str = "", inc: str = "", **kwargs):
        r"""Deletes selected elements from the model.

        Mechanical APDL Command: `EDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EDELE.html>`_

        Parameters
        ----------
        iel1 : str
            Delete elements from ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in steps of ``INC`` (defaults
            to 1). If ``IEL1`` = ALL, ``IEL2`` and ``INC`` are ignored and all selected elements (
            :ref:`esel` ) are deleted. If ``IEL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``IEL1`` ( ``IEL2`` and ``INC`` are ignored).

        iel2 : str
            Delete elements from ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in steps of ``INC`` (defaults
            to 1). If ``IEL1`` = ALL, ``IEL2`` and ``INC`` are ignored and all selected elements (
            :ref:`esel` ) are deleted. If ``IEL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``IEL1`` ( ``IEL2`` and ``INC`` are ignored).

        inc : str
            Delete elements from ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in steps of ``INC`` (defaults
            to 1). If ``IEL1`` = ALL, ``IEL2`` and ``INC`` are ignored and all selected elements (
            :ref:`esel` ) are deleted. If ``IEL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``IEL1`` ( ``IEL2`` and ``INC`` are ignored).

        Notes
        -----

        .. _EDELE_notes:

        Deleted elements are replaced by null or "blank" elements. Null elements are used only for retaining
        the element numbers so that the element numbering sequence for the rest of the model is not changed
        by deleting elements. Null elements may be removed (although this is not necessary) with the
        :ref:`numcmp` command. If related element data (pressures, etc.) are also to be deleted, delete that
        data before deleting the elements. :ref:`edele` is for unattached elements only. You can use the
        **xCLEAR** family of commands to remove any attached elements from the database.
        """
        command = f"EDELE,{iel1},{iel2},{inc}"
        return self.run(command, **kwargs)

    def eembed(self, **kwargs):
        r"""Generates bonded connections between intersecting elements.

        Mechanical APDL Command: `EEMBED <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EEMBED.html>`_

        Notes
        -----

        .. _EEMBED_notes:

        From selected elements, :ref:`eembed` identifies embedded elements that are partially or completely
        enclosed within other (base) elements, determines the interior intersection surfaces between the
        embedded and base elements, and generates special-purpose ``REINF265`` reinforcing elements
        representing the bonded connection stiffness of the interior intersection surfaces.

        Supported base elements are 3D structural solids ( ``SOLID185``, ``SOLID186``, ``SOLID187``, and
        ``SOLID285`` ) and thermal solids ( ``SOLID278``, ``SOLID279``, and ``SOLID291`` ). Supported
        embedded elements are 3D structural links and beams ( ``LINK180``, ``BEAM188``, and ``BEAM189`` )
        and thermal link ( ``LINK33`` ).

        Before issuing :ref:`eembed`, define the base and embedded elements, then select the elements to be
        included for embedded connections. Mesh conformity between the base and embedded elements is not
        required. A combination of supported base and embedded element types is allowed.

        The command has no arguments. Simply issue the command to perform the embedding procedure.

        You can inspect newly created reinforcing element types, sections, and elements ( :ref:`etlist`,
        :ref:`slist`, :ref:`elist`, or :ref:`eplot` ).

        Do not issue other preprocessing commands (such as :ref:`et`, :ref:`e`, :ref:`emodif`, and
        :ref:`sectype` ) to create or modify the special-purpose reinforcing elements, element types, and
        sections.

        Elements generated by :ref:`eembed` are not associated with the solid model.

        Reinforcing elements do not account for subsequent modifications made to the base and embedded
        elements. To avoid inconsistencies, issue :ref:`eembed` only after the base elements are finalized.
        If you delete or modify base or embedded elements (for example, via :ref:`edele`, :ref:`emodif`,
        :ref:`etchg`, :ref:`emid`, :ref:`eorient`, :ref:`nummrg`, or :ref:`numcmp` ), remove all affected
        reinforcing elements and associated sections, and reissue :ref:`eembed`.

        :ref:`eembed` creates new reinforcing sections (of ``Subtype`` = `GCON
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SECTYPE.html#SECTYPE.menupath>`_
        ) containing details about the created ``REINF265`` elements, then applies them to all newly
        generated special-purpose ``REINF265`` elements. The number of new reinforcing sections depends on
        the number of new ``REINF265`` elements. (You can examine the properties of new sections (
        :ref:`slist` ).) The program sets the ID number of the newest reinforcing section to the highest
        available section ID number in the model. After issuing :ref:`eembed`, the command shows the
        highest-numbered IDs (element type, element, and section). Do not overwrite a new reinforcing
        section when defining subsequent sections.

        If performing a subsequent structural analysis after the thermal analysis, you can use :ref:`eembed`
        to convert the reinforcing elements for the structural analysis, as follows:

        Convert the thermal base and embedded elements to the appropriate structural element ( :ref:`et` or
        :ref:`emodif` ).

        Select the reinforcing elements generated by :ref:`eembed` in the previous thermal analysis only.

        Issue :ref:`eembed`.

        Result : The program modifies the attributes of the selected reinforcing elements so that they are
        compatible with the converted base and embedded elements.

        For more information about using this command, see `Direct-Embedding Workflow
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_directembed.html#dirembedsimpost>`_
        """
        command = "EEMBED"
        return self.run(command, **kwargs)

    def egen(
        self,
        itime: str = "",
        ninc: str = "",
        iel1: str = "",
        iel2: str = "",
        ieinc: str = "",
        minc: str = "",
        tinc: str = "",
        rinc: str = "",
        cinc: str = "",
        sinc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        **kwargs,
    ):
        r"""Generates elements from an existing pattern.

        Mechanical APDL Command: `EGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EGEN.html>`_

        Parameters
        ----------
        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the given pattern
            by ``NINC`` each time after the first. ``ITIME`` must be >1 if generation is to occur. ``NINC``
            may be positive, zero, or negative. If ``DX``, ``DY``, and/or ``DZ`` is specified, ``NINC``
            should be set so any existing nodes (as on :ref:`ngen` ) are not overwritten.

        ninc : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the given pattern
            by ``NINC`` each time after the first. ``ITIME`` must be >1 if generation is to occur. ``NINC``
            may be positive, zero, or negative. If ``DX``, ``DY``, and/or ``DZ`` is specified, ``NINC``
            should be set so any existing nodes (as on :ref:`ngen` ) are not overwritten.

        iel1 : str
            Generate elements from selected pattern beginning with ``IEL1`` to ``IEL2`` (defaults to
            ``IEL1`` ) in steps of ``IEINC`` (defaults to 1). If ``IEL1`` is negative, ``IEL2`` and
            ``IEINC`` are ignored and the last \| ``IEL1`` \| elements (in sequence backward from the maximum
            element number) are used as the pattern to be repeated. If ``IEL1`` = ALL, ``IEL2`` and
            ``IEINC`` are ignored and use all selected elements ( :ref:`esel` ) as pattern to be repeated.
            If ``P1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``IEL1`` ( ``IEL2`` and ``INC``
            are ignored).

        iel2 : str
            Generate elements from selected pattern beginning with ``IEL1`` to ``IEL2`` (defaults to
            ``IEL1`` ) in steps of ``IEINC`` (defaults to 1). If ``IEL1`` is negative, ``IEL2`` and
            ``IEINC`` are ignored and the last \| ``IEL1`` \| elements (in sequence backward from the maximum
            element number) are used as the pattern to be repeated. If ``IEL1`` = ALL, ``IEL2`` and
            ``IEINC`` are ignored and use all selected elements ( :ref:`esel` ) as pattern to be repeated.
            If ``P1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``IEL1`` ( ``IEL2`` and ``INC``
            are ignored).

        ieinc : str
            Generate elements from selected pattern beginning with ``IEL1`` to ``IEL2`` (defaults to
            ``IEL1`` ) in steps of ``IEINC`` (defaults to 1). If ``IEL1`` is negative, ``IEL2`` and
            ``IEINC`` are ignored and the last \| ``IEL1`` \| elements (in sequence backward from the maximum
            element number) are used as the pattern to be repeated. If ``IEL1`` = ALL, ``IEL2`` and
            ``IEINC`` are ignored and use all selected elements ( :ref:`esel` ) as pattern to be repeated.
            If ``P1`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may also be substituted for ``IEL1`` ( ``IEL2`` and ``INC``
            are ignored).

        minc : str
            Increment material number of all elements in the given pattern by ``MINC`` each time after the
            first.

        tinc : str
            Increment element type number by ``TINC``. The element types with incremented numbers must be
            defined before issuing the :ref:`egen` command.

        rinc : str
            Increment real constant table number by ``RINC``.

        cinc : str
            Increment element coordinate system number by ``CINC``.

        sinc : str
            Increment section ID number by ``SINC``.

        dx : str
            Define nodes that do not already exist but are needed by generated elements (as though the
            :ref:`ngen`, ``ITIME,INC,NODE1,,,DX,DY,DZ`` were issued before :ref:`egen` ). Zero is a valid
            value. If blank, ``DX``, ``DY``, and ``DZ`` are ignored.

        dy : str
            Define nodes that do not already exist but are needed by generated elements (as though the
            :ref:`ngen`, ``ITIME,INC,NODE1,,,DX,DY,DZ`` were issued before :ref:`egen` ). Zero is a valid
            value. If blank, ``DX``, ``DY``, and ``DZ`` are ignored.

        dz : str
            Define nodes that do not already exist but are needed by generated elements (as though the
            :ref:`ngen`, ``ITIME,INC,NODE1,,,DX,DY,DZ`` were issued before :ref:`egen` ). Zero is a valid
            value. If blank, ``DX``, ``DY``, and ``DZ`` are ignored.

        Notes
        -----

        .. _EGEN_notes:

        A pattern may consist of any number of previously defined elements. The MAT, TYPE, REAL, ESYS, and
        SECNUM numbers of the new elements are based upon the elements in the pattern and not upon the
        current specification settings.

        You can use the :ref:`egen` command to generate interface elements ( ``INTER192``, ``INTER193``,
        ``INTER194``, and ``INTER195`` ) directly. However, because interface elements require that the
        element connectivity be started from the bottom surface, you must make sure that you use the correct
        element node connectivity. See the element descriptions for ``INTER192``, ``INTER193``,
        ``INTER194``, and ``INTER195`` for the correct element node definition.
        """
        command = f"EGEN,{itime},{ninc},{iel1},{iel2},{ieinc},{minc},{tinc},{rinc},{cinc},{sinc},{dx},{dy},{dz}"
        return self.run(command, **kwargs)

    def egid(self, val: str = "", **kwargs):
        r"""Specifies a global identifier for a set of ``MESH200`` elements.

        Mechanical APDL Command: `EGID <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EGID.html>`_

        Parameters
        ----------
        val : str
            An integer for identifying a set of ``MESH200`` elements used in a `reinforcing
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
            analysis. Default = 1.

        Notes
        -----
        ``VAL`` is a global identifier that you assign to a set of ``MESH200`` elements in a `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        analysis. The command is valid only when using the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
        defining reinforcing.

        The global identifier that you specify is transferred to the reinforcing members (individual
        reinforcings) when they are generated ( :ref:`ereinf` ).

        Issue :ref:`egid`  before generating the ``MESH200`` elements.

        If necessary, you can change the global identifier for an existing set of ``MESH200`` elements (
        :ref:`emodif` ).

        For more information about using this command in a mesh-independent reinforcing analysis, see
        `Selecting and Displaying Groups of Reinforcing Members
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_
        """
        command = f"EGID,{val}"
        return self.run(command, **kwargs)

    def einfin(
        self,
        compname: str = "",
        pnode_nref1: str = "",
        nref2: str = "",
        nref3: str = "",
        matid: str = "",
        **kwargs,
    ):
        r"""Generates structural infinite elements from selected nodes.

        Mechanical APDL Command: `EINFIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EINFIN.html>`_

        Parameters
        ----------
        compname : str
            Component name containing the reference nodes for calculating the position of poles for generating
            ``INFIN257`` structural infinite elements.

            The number of poles and their positions are based on the number of included nodes:

            * If the component includes only one node, the node becomes the pole node. The pole node is
              typically located at or near the geometric center of the finite element domain if there is a
              single pole.

            * If the component includes two (2D) or three nodes (3D), the program constructs an infinite line or
              area, then calculates the pole positions by drawing a perpendicular line from a selected node to
              the line or area.

            * If the component includes more than two (2D) or three nodes (3D), the program uses the first two
              or three nodes calculate the position of poles.

        pnode_nref1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EINFIN.html>`_ for
            further information.

        nref2 : str
            Node number of the second reference node used to calculate pole positions. (A parameter or
            parametric expression is also valid.) Specify this value when no ``CompName`` has been
            specified. (If ``CompName`` is specified, this value is ignored.) To input this value, first
            specify ``NREF1`` (replacing ``PNODE`` ). Pole positions are calculated on an infinite line
            defined by ``NREF1`` and ``NREF2``.

        nref3 : str
            Node number of the third reference node used to calculate pole positions. (A parameter or
            parametric expression is also valid.) Specify this value when no ``CompName`` has been
            specified. (If ``CompName`` is specified, this value is ignored.) To input this value, first
            specify ``NREF1`` (replacing ``PNODE`` ) and ``NREF2``. Pole positions are calculated on an
            infinite line defined by ``NREF1``, ``NREF2``, and ``NREF3``.

        matid : str
            Optional material ID of the structural infinite element. (A parameter or parametric expression
            is also valid.) If specified, this value defines the material properties of the structural
            infinite elements explicitly; otherwise, the material ID is copied from the base elements.

        Notes
        -----

        .. _EINFIN_notes:

        The :ref:`einfin` command generates structural infinite elements ( ``INFIN257`` ) directly from the
        selected face of `valid base elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_INFIN257.html#infin257.tab.1>`_
        (existing standard elements in your model). The command scans all base elements for the selected
        nodes and generates a compatible infinite element type for each base element. A combination of
        different base element types is allowed if the types are all compatible with the infinite elements.

        The infinite element type requires no predefinition ( :ref:`et` ).

        The faces of base elements are determined from the selected node set ( :ref:`nsel` ), and the
        geometry of the infinite element is determined based on the shape of the face. Element
        characteristics and options are determined according to the base element. For the face to be used,
        all nodes on the face of a base element must be selected

        Use base elements to model the near-field domain that interacts with the solid structures or applied
        loads. To apply the truncated far-field effect, a single layer of infinite elements must be attached
        to the near-field domain. The outer surface of the near-field domain must be convex.

        The material of the structural infinite elements can be defined in either of two ways. If ``MATID``
        is specified, the command uses that value to define the material property of the structural infinite
        elements. If ``MATID`` is not specified, the material ID of the base element is copied to the
        attached infinite element. Although only isotropic material is allowed for the infinite elements,
        these options enable you to define anisotropic material for the base elements in a static analysis.
        (In a transient analysis, however, use the same isotropic material for both base elements and
        infinite elements.)

        After the :ref:`einfin` command executes, you can verify the newly created infinite element types
        and elements ( :ref:`etlist`, :ref:`elist`, :ref:`eplot` ).

        Infinite elements do not account for any subsequent modifications made to the base elements. It is
        good practice to issue the :ref:`einfin` command only after the base elements are finalized. If you
        delete or modify base elements (via :ref:`edele`, :ref:`emodif`, :ref:`etchg`, :ref:`emid`,
        :ref:`eorient`, :ref:`nummrg`, or :ref:`numcmp` commands, for example) after generating the
        structural infinite elements, remove all affected infinite elements and reissue the :ref:`einfin`
        command; doing so prevents inconsistencies.

        **Command Usage Examples**
          **Example: Single Reference Node (Pole)**

          **2D Elements:**

          .. code:: apdl

             /prep7
             et,1,182
             mp,ex,1,1e9
             mp,nuxy,1,0.3

             type,1             ! Generate solid elements
             mat,1
             rect,0,4,0,4
             elsize,1
             allsel
             mshkey,1
             amesh,1

             n1 = node(0,4,0)   ! Select reference node
             nsel,s,loc,x,4     ! Select nodes on base element
             nsel,a,loc,y,0
             EINFIN,,n1

          **3D Elements:**

          .. code:: apdl

             /prep7
             et,1,185          ! Generate solid elements
             mp,ex,1,1e9
             mp,nuxy,1,0.3

             type,1
             mat,1
             block,0,4,0,4,0,4
             elsize,1

             mshkey,1
             vmesh,1

             n1 = node(0,0,4)  ! Select reference node
             nsel,,loc,x,4     ! Select nodes on base elements
             nsel,a,loc,y,4
             nsel,a,loc,z,0
             EINFIN,,n1

          **Example: Two Reference Nodes**

          **2D Elements:**

          .. code:: apdl

             /prep7
             et,1,182            ! Generate solid elements
             mp,ex,1,1e9
             mp,nuxy,1,0.3
             type,1
             mat,1
             rect,0,4,0,4
             elsize,1
             allsel
             mshkey,1
             amesh,1

             n1 = node(0,0,0)    ! Select reference nodes
             n2 = node(0,4,0)

             nsel,,loc,x,4       ! Select nodes on base elements
             EINFIN,,n1,n2

          Following is the equivalent input with a component:

          .. code:: apdl

             /prep7
             et,1,182            ! Generate solid elements  mp,ex,1,1e9
             mp,nuxy,1,0.3
             type,1
             mat,1
             rect,0,4,0,4
             elsize,1
             allsel
             mshkey,1
             amesh,1

             n1 = node(0,0,0)     ! Select  reference nodes
             n2 = node(0,4,0)
             nsel,,node,,n1
             nsel,a,node,,n2
             cm, nrefs, node      ! Define component
             allsel
             nsel,,loc,x,4        ! Select nodes on base elements
             EINFIN, nrefs

          **3D Elements:**

          .. code:: apdl

             /prep7

             et,1,185             ! Generate solid elements
             mp,ex,1,1e9
             mp,nuxy,1,0.3

             type,1
             mat,1
             block,0,4,0,4,0,4
             elsize,1
             mshkey,1
             vmesh,1

             n1 = node(0,0,4)    ! Select reference nodes
             n2 = node(0,4,4)
             nsel,,loc,x,4       ! Select nodes on base elements
             EINFIN,,n1, n2

          **Example: Three Reference Nodes**

          **3D Elements Only:**

          .. code:: apdl

             /prep7

             et,1,185            ! Generate solid elements
             mp,ex,1,1e9
             mp,nuxy,1,0.3

             type,1
             mat,1
             block,0,4,0,4,0,4
             elsize,1
             mshkey,1
             vmesh,1

             n1 = node(0,4,4)    ! Select reference nodes
             n2 = node(0,0,4)
             n3 = node(0,0,0)
             nsel,,loc,x,4       ! Select nodes on base elements
             EINFIN,,n1,n2,n3

          **Example: Multiple EINFIN Commands**

          **2D Elements:**

          .. code:: apdl

             /prep7
             et,1,182
             mp,ex,1,1e9
             mp,nuxy,1,0.3

             type,1             ! Generate solid elements
             mat,1
             rect,0,4,0,4
             elsize,1
             allsel
             mshkey,1
             amesh,1

             n1 = node(0,0,0)
             n2 = node(0,4,0)
             nsel,,loc,x,4,
             nsel,r,loc,y,0.5,5
             EINFIN,,n1,n2      ! upper right quad. elements
             nsel,all
             nsel,,loc,x,4
             nsel,r,loc,y,0,1.5
             EINFIN,,n2         ! Lower corner element
             nsel,all
             n3 = node(4,4,0)
             nsel,s,loc,y,0
             EINFIN,,n2,n3      ! Lower elements (y<0)

          **3D Elements:**

          .. code:: apdl

             /prep7

             et,1,185             ! Generate solid elements
             mp,ex,1,1e9
             mp,nuxy,1,0.3

             type,1
             mat,1

             block,0,4,0,4,0,4
             elsize,1

             mshkey,1
             vmesh,1

             n1 = node(0,0,0)
             n2 = node(0,0,4)
             n3 = node(0,4,4)

             nsel,s,loc,x,4,
             nsel,u,loc,z,0
             EINFIN, n1, n2, n3  ! Upper right part
             allsel
             nsel,s,loc,x,4
             nsel,r,loc,z,-0.1,1.2
             EINFIN,,n2,n3         ! Corner element
             allsel
             n5 = node(4,4,4)
             nsel,s,loc,z,0
             EINFIN,,n2,n3,n5      ! Lower part (z<0)
        """
        command = f"EINFIN,{compname},{pnode_nref1},{nref2},{nref3},{matid}"
        return self.run(command, **kwargs)

    def eintf(
        self,
        toler: str = "",
        k: str = "",
        tlab: str = "",
        kcn: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        knonrot: str = "",
        **kwargs,
    ):
        r"""Defines two-node elements between coincident or offset nodes.

        Mechanical APDL Command: `EINTF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EINTF.html>`_

        Parameters
        ----------
        toler : str
            Tolerance for coincidence (based on maximum Cartesian coordinate difference for node locations
            and on angle differences for node orientations). Defaults to 0.0001. Only nodes within the
            tolerance are considered to be coincident.

        k : str
            Only used when the type of the elements to be generated is ``PRETS179``. ``K`` is the pretension
            node that is common to the pretension section that is being created. If ``K`` is not specified,
            it is created automatically and will have an Mechanical APDL-assigned node number. If ``K`` is
            specified but does not already exist, it will be created automatically but will have the user-
            specified node number. ``K`` cannot be connected to any existing element.

        tlab : str
            Nodal number ordering. Allowable values are:

            * ``LOW`` - The 2-node elements are generated from the lowest numbered node to the highest numbered
              node.

            * ``HIGH`` - The 2-node elements are generated from the highest numbered node to the lowest numbered
              node.

            * ``REVE`` - Reverses the orientation of the selected 2-node element.

        kcn : str
            In coordinate system ``KCN``, elements are created between node 1 and node 2 (= node 1 + dx dy
            dz).

        dx : str
            Node location increments that define the node offset in the active coordinate system (DR, Dθ, DZ
            for cylindrical and DR, Dθ, DΦ for spherical or toroidal).

        dy : str
            Node location increments that define the node offset in the active coordinate system (DR, Dθ, DZ
            for cylindrical and DR, Dθ, DΦ for spherical or toroidal).

        dz : str
            Node location increments that define the node offset in the active coordinate system (DR, Dθ, DZ
            for cylindrical and DR, Dθ, DΦ for spherical or toroidal).

        knonrot : str
            When ``KNONROT`` = 0, the nodes coordinate system is not rotated. When ``KNONROT`` = 1, the
            nodes belonging to the elements created are rotated into coordinate system ``KCN`` (see
            :ref:`nrotat`  command description).

        Notes
        -----

        .. _EINTF_notes:

        Defines 2-node elements (such as gap elements) between coincident or offset nodes (within a
        tolerance). May be used, for example, to "hook" together elements interfacing at a seam, where the
        seam consists of a series of node pairs. One element is generated for each set of two coincident
        nodes. For more than two coincident or offset nodes in a cluster, an element is generated from the
        lowest numbered node to each of the other nodes in the cluster. If fewer than all nodes are to be
        checked for coincidence, use the :ref:`nsel` command to select the nodes. Element numbers are
        incremented by one from the highest previous element number. The element type must be set (
        :ref:`et` ) to a 2-node element before issuing this command. Use the :ref:`cpintf` command to
        connect nodes by coupling instead of by elements. Use the :ref:`ceintf` command to connect the nodes
        by constraint equations instead of by elements.

        For contact element ``CONTA178``, the tolerance is based on the maximum Cartesian coordinate
        difference for node locations only. The angle differences for node orientations are not checked.
        """
        command = f"EINTF,{toler},{k},{tlab},{kcn},{dx},{dy},{dz},{knonrot}"
        return self.run(command, **kwargs)

    def elbow(
        self,
        transkey: str = "",
        tol: str = "",
        dof: str = "",
        cons1: str = "",
        cons2: str = "",
        cons3: str = "",
        cons4: str = "",
        **kwargs,
    ):
        r"""Specifies degrees of freedom to be coupled for end release and applies section constraints to elbow
        elements.

        Mechanical APDL Command: `ELBOW <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ELBOW.html>`_

        Parameters
        ----------
        transkey : str
            Pipe-to-elbow transition flag:

            * ``OFF`` - Do not automatically transition pipes to elbows. (This behavior is the default.)

            * ``ON`` - Automatically convert straight ``PIPE289`` elements to ``ELBOW290`` elements where it is
              beneficial. The program converts elements in transition regions where curved ``ELBOW290`` elements
              are connected to straight ``PIPE289`` elements.

        tol : str
            Angle tolerance (in degrees) between adjacent ``ELBOW290`` elements. The default value is 20. A
            value of -1 specifies all selected ``ELBOW290`` elements.

        dof : str
            Degrees of freedom to couple:

            * ``ALL`` - Couple all nodal degrees of freedom (UX, UY, UZ, ROTX, ROTY, and ROTZ). This behavior is
              the default.

            * ``BALL`` - Create ball joints (equivalent to releasing ROTX, ROTY, and ROTZ).

        cons1 : str
            Section degrees of freedoms to constrain. If ``Cons1`` through ``Cons4`` are unspecified, no section constraints are applied:

            * ``SECT`` - All section deformation

            * ``SE`` - Section radial expansion

            * ``SO`` - Section ovalization

            * ``SW`` - Section warping

            * ``SRA`` - Local shell normal rotation about cylindrical axis t2

            * ``SRT`` - Local shell normal rotation about cylindrical axis t1

        cons2 : str
            Section degrees of freedoms to constrain. If ``Cons1`` through ``Cons4`` are unspecified, no section constraints are applied:

            * ``SECT`` - All section deformation

            * ``SE`` - Section radial expansion

            * ``SO`` - Section ovalization

            * ``SW`` - Section warping

            * ``SRA`` - Local shell normal rotation about cylindrical axis t2

            * ``SRT`` - Local shell normal rotation about cylindrical axis t1

        cons3 : str
            Section degrees of freedoms to constrain. If ``Cons1`` through ``Cons4`` are unspecified, no section constraints are applied:

            * ``SECT`` - All section deformation

            * ``SE`` - Section radial expansion

            * ``SO`` - Section ovalization

            * ``SW`` - Section warping

            * ``SRA`` - Local shell normal rotation about cylindrical axis t2

            * ``SRT`` - Local shell normal rotation about cylindrical axis t1

        cons4 : str
            Section degrees of freedoms to constrain. If ``Cons1`` through ``Cons4`` are unspecified, no section constraints are applied:

            * ``SECT`` - All section deformation

            * ``SE`` - Section radial expansion

            * ``SO`` - Section ovalization

            * ``SW`` - Section warping

            * ``SRA`` - Local shell normal rotation about cylindrical axis t2

            * ``SRT`` - Local shell normal rotation about cylindrical axis t1

        Notes
        -----

        .. _ELBOW_notes:

        The :ref:`elbow` command specifies end releases and section constraints for ``ELBOW290`` elements
        and converts straight ``PIPE289`` elements to ``ELBOW290`` elements.

        Curved ``PIPE289`` elements are not converted to ``ELBOW290`` elements.

        ``ELBOW290`` elements are generated only if there are existing  ``ELBOW290`` elements in the curved
        areas.

        The command works on currently selected nodes and elements. It creates end releases on any two
        connected elbow elements whose angle at connection exceeds the specified tolerance. From within the
        GUI, the Picked node option generates an end release and section constraints at the selected node
        regardless of the angle of connection (that is, the angle tolerance [ ``TOL`` ] is set to -1).


        Elbow and pipe elements must share the same section ID in order for the pipe-to-elbow transition to
        occur.

        To list the elements altered by the :ref:`elbow` command, issue an :ref:`elist` command.

        To list the coupled sets generated by the :ref:`elbow` command, issue a :ref:`cplist` command.

        To list the section constraints generated by the :ref:`elbow` command, issue a :ref:`dlist` command.
        """
        command = f"ELBOW,{transkey},{tol},{dof},{cons1},{cons2},{cons3},{cons4}"
        return self.run(command, **kwargs)

    def elist(
        self,
        iel1: str = "",
        iel2: str = "",
        inc: str = "",
        nnkey: int | str = "",
        rkey: int | str = "",
        **kwargs,
    ):
        r"""Lists the elements and their attributes.

        Mechanical APDL Command: `ELIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ELIST.html>`_

        Parameters
        ----------
        iel1 : str
            Lists elements from ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in steps of ``INC`` (defaults
            to 1). If ``IEL1`` = ALL (default), ``IEL2`` and ``INC`` are ignored and all selected elements (
            :ref:`esel` ) are listed. If ``IEL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``IEL1`` ( ``IEL2`` and ``INC`` are ignored).

        iel2 : str
            Lists elements from ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in steps of ``INC`` (defaults
            to 1). If ``IEL1`` = ALL (default), ``IEL2`` and ``INC`` are ignored and all selected elements (
            :ref:`esel` ) are listed. If ``IEL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``IEL1`` ( ``IEL2`` and ``INC`` are ignored).

        inc : str
            Lists elements from ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in steps of ``INC`` (defaults
            to 1). If ``IEL1`` = ALL (default), ``IEL2`` and ``INC`` are ignored and all selected elements (
            :ref:`esel` ) are listed. If ``IEL1`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may also be substituted for
            ``IEL1`` ( ``IEL2`` and ``INC`` are ignored).

        nnkey : int or str
            Node listing key:

            * ``0`` - List attribute references and nodes.

            * ``1`` - List attribute references but not nodes.

        rkey : int or str
            Real constant listing key:

            * ``0`` - Do not show real constants for each element.

            * ``1`` - Show real constants for each element. This includes default values chosen for the element.

        Notes
        -----

        .. _ELIST_notes:

        Lists the elements with their nodes and attributes (MAT, TYPE, REAL, ESYS, SECNUM, PART). See also
        the :ref:`laylist` command for listing layered elements.

        This command is valid in any processor.
        """
        command = f"ELIST,{iel1},{iel2},{inc},{nnkey},{rkey}"
        return self.run(command, **kwargs)

    def emid(self, key: str = "", edges: str = "", **kwargs):
        r"""Adds or removes midside nodes.

        Mechanical APDL Command: `EMID <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMID.html>`_

        Parameters
        ----------
        key : str
            Add or remove key:

            * ``ADD`` - Add midside node to elements (default).

            * ``REMOVE`` - Remove midside nodes from elements.

        edges : str

            * ``ALL`` - Add (or remove) midside nodes to (from) all edges of all selected elements, independent
              of which nodes are selected (default).

            * ``EITHER`` - Add (or remove) midside nodes only to (from) element edges which have either corner
              node selected.

            * ``BOTH`` - Add (or remove) midside nodes only to (from) element edges which have both corner nodes
              selected.

        Notes
        -----

        .. _EMID_notes:

        This command adds midside nodes to (or removes midside nodes from) the selected elements. For this
        to occur, the selected elements must be midside node capable, the active element type ( :ref:`type`
        ) must allow midside node capability, and the relationship between the finite element model and the
        solid model (if any) must first be disassociated ( :ref:`modmsh` ).

        By default, :ref:`emid` generates a midside node wherever a zero (or missing) midside node occurs
        for that element. You can control this and add (or remove) midside nodes selectively by using the
        ``Edges`` argument. Nodes are located midway between the two appropriate corner nodes based on a
        linear Cartesian interpolation. Nodal coordinate system rotation angles are also linearly
        interpolated. Connected elements share the same midside node. Node numbers are generated
        sequentially from the maximum node number.

        The :ref:`emid` command is useful for transforming linear element types to quadratic element types
        having the same corner node connectivity.

        :ref:`emid` is also useful for transforming elements created outside of the program.
        """
        command = f"EMID,{key},{edges}"
        return self.run(command, **kwargs)

    def emodif(
        self,
        iel: str = "",
        stloc: str = "",
        i1: str = "",
        i2: str = "",
        i3: str = "",
        i4: str = "",
        i5: str = "",
        i6: str = "",
        i7: str = "",
        i8: str = "",
        **kwargs,
    ):
        r"""Modifies a previously defined element.

        Mechanical APDL Command: `EMODIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMODIF.html>`_

        Parameters
        ----------
        iel : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        stloc : str
            Starting location ( ``n`` ) of first node to be modified or the attribute label.

            If ``n``, modify element node positions ``n``, ``n`` +1, etc. ( ``n`` = 1 to 20). For example,
            if ``STLOC`` = 1, ``I1`` refers to the first node, ``I2``, the second, etc. If ``STLOC`` = 9,
            ``I1`` refers to the ninth node, ``I2``, the tenth, etc. Attributes are also modified to the
            currently specified values.

            Use - ``n`` to modify only nodes and not attributes.

            If zero, modify only the attributes to the currently specified values.

            If MAT, TYPE, REAL, ESYS, SECNUM, or EGID, modify only that attribute to the ``I1`` value.

        i1 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i2 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i3 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i4 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i5 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i6 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i7 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        i8 : str
            Replace the previous node numbers assigned to this element with these corresponding values. A
            (blank) retains the previous value (except in the ``I1`` field, which resets the ``STLOC`` node
            number to zero).

            For attributes ( ``STLOC`` = MAT, TYPE, etc.), replace the existing value with the ``I1`` value
            (or the default if ``I1`` is zero or blank).

            For attributes MAT and REAL, inputting the label GCN for ``I1`` replaces the existing attribute
            value with zero for the specified elements. This is a special case used only for converting
            contact elements ( ``TARGE169`` through ``CONTA177`` ) from a pair-based definition to a
            `general contact definition
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_.

        Notes
        -----

        .. _EMODIF_notes:

        The nodes and/or attributes (MAT, TYPE, REAL, ESYS, SECNUM, or EGID values) of an existing element
        can be changed with this command.

        The EGID attribute is valid only for ``MESH200`` elements when they are used to generate
        `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements (REINF ``nnn`` ) via the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
        defining reinforcing.
        """
        command = f"EMODIF,{iel},{stloc},{i1},{i2},{i3},{i4},{i5},{i6},{i7},{i8}"
        return self.run(command, **kwargs)

    def emore(
        self,
        q: str = "",
        r: str = "",
        s: str = "",
        t: str = "",
        u: str = "",
        v: str = "",
        w: str = "",
        x: str = "",
        **kwargs,
    ):
        r"""Adds more nodes to the just-defined element.

        Mechanical APDL Command: `EMORE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMORE.html>`_

        Parameters
        ----------
        q : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        r : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        s : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        t : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        u : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        v : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        w : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        x : str
            Numbers of nodes typically assigned to ninth (node ``Q`` ) through sixteenth (node ``X`` ) nodal
            positions, if any. If ``Q`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI).

        Notes
        -----

        .. _EMORE_notes:

        Repeat :ref:`emore` command for up to 4 additional nodes (20 maximum). Nodes are added after the
        last nonzero node of the element. Node numbers defined with this command may be zeroes.
        """
        command = f"EMORE,{q},{r},{s},{t},{u},{v},{w},{x}"
        return self.run(command, **kwargs)

    def emsel(
        self, type_: str = "", vmin: str = "", vmax: str = "", vinc: str = "", **kwargs
    ):
        r"""Selects a group of `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        members via a predefined global identifier.

        Mechanical APDL Command: `EMSEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMSEL.html>`_

        Parameters
        ----------
        type_ : str
            Specifies the selection type for the reinforcing elements:

            * S - Select a new set (default).
            * A - Select an additional set and add it to the current set.
            * U - Unselect a set from the current set.
            * ALL - Restore the full set.
            * STAT - Display the current selection status.

            The following arguments are valid only when ``Type`` = S, A, or U:

        vmin : str
            Minimum value of a group-identifier range.

        vmax : str
            Maximum value of global identifier range. Default = VMIN for input values.

        vinc : str
            Value increment within the specified range. Default = 1.

        Notes
        -----
        Understanding Reinforcing Member Groups When using the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
        defining reinforcing, the global identifier for a set of ``MESH200`` elements (specified via
        :ref:`egid` ) is transferred from the ``MESH200`` elements to the reinforcing members (individual
        reinforcings) when the reinforcing elements (REINF ``nnn`` ) are generated ( :ref:`ereinf` ).

        The :ref:`emsel` command selects groups of reinforcing members (individual reinforcings) via
        specified global identifiers.

          **Example: Selecting Reinforcing Member Groups**

          The following command selects a new group of reinforcing members based on global identifiers 1
          through 7:

          .. code:: apdl

             EMSEL,S,,,1,7

        ``VMIN``, ``VMAX``, and ``VINC`` are positive integer values.

        This command is valid in PREP7 and POST1.

        For more information about using this command in a mesh-independent reinforcing analysis, see
        `Selecting and Displaying Groups of Reinforcing Members
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"EMSEL,{type_},,,{vmin},{vmax},{vinc}"
        return self.run(command, **kwargs)

    def emtgen(
        self,
        ncomp: str = "",
        ecomp: str = "",
        pncomp: str = "",
        dof: str = "",
        gap: str = "",
        gapmin: str = "",
        fkn: str = "",
        epzero: str = "",
        smethod: str = "",
        **kwargs,
    ):
        r"""Generates a set of ``TRANS126`` elements.

        Mechanical APDL Command: `EMTGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMTGEN.html>`_

        Parameters
        ----------
        ncomp : str
            Component name of the surface nodes of a structure which attach to the ``TRANS126`` elements.
            The component name must be 32 characters or less, and you must enclose the name in single quotes
            in the :ref:`emtgen` command line.

        ecomp : str
            Component name of the ``TRANS126`` elements generated. The component name must be 32 characters
            or less, and you must enclose the name in single quotes in the :ref:`emtgen` command line.
            Defaults to EMTELM.

        pncomp : str
            Component name of the plane nodes generated by the command at an offset ( ``GAP`` ) from the
            surface nodes. The component name must be 32 characters or less, and you must enclose the name
            in single quotes in the :ref:`emtgen` command line. Defaults to EMTPNO.

        dof : str
            Active structural degree of freedom (DOF) for ``TRANS126`` elements in the Cartesian coordinate system. You must enclose the DOF label in single quotes:

            * ``UX`` - Displacement in X direction.

            * ``UY`` - Displacement in Y direction.

            * ``UZ`` - Displacement in Z direction.

        gap : str
            Initial gap distance from the surface nodes to the plane. Be sure to use the correct sign with
            respect to Ncomp node location.

        gapmin : str
            Minimum gap distance allowed (GAPMIN real constant) for ``TRANS126`` elements. Defaults to the
            absolute value of ( ``GAP`` )\*0.05.

        fkn : str
            Contact stiffness factor used as a multiplier for a contact stiffness appropriate for bulk
            deformation. Defaults to 0.1. A negative value is interpreted as the modulus of elasticity on
            which the contact stiffness will be based.

        epzero : str
            Free-space permittivity. Defaults to 8.854e-6 (μMKS units).

        smethod : str
            Stiffness method for ``TRANS126`` elements (KEYOPT(6) setting). You must enclose the following labels in single quotes:

            * ``AUGM`` - Augmented stiffness method (default).

            * ``FULL`` - Full stiffness method. This method must be used in a linear perturbation harmonic
              analysis.

        Notes
        -----

        .. _EMTGEN_notes:

        The :ref:`emtgen` command generates a set of ``TRANS126`` elements between the surface nodes of a
        moveable structure and a plane of nodes, typically representing a ground plane. The plane of nodes
        is created by the command at a specified offset ( ``GAP`` ). Each element attaches to a surface node
        and to a corresponding node representing the plane. The generated plane nodes should be constrained
        appropriately for the analysis.

        By default, the created elements use the augmented stiffness method (KEYOPT(6) = 1), which can help
        convergence. You can change to the full stiffness method (KEYOPT(6) = 0) by setting ``Smethod`` =
        FULL. The full stiffness method is required for a linear perturbation harmonic analysis.

        You can use ``TRANS126`` elements for simulating fully coupled electrostatic structural coupling
        between a MEMS device and a plane, if the gap distance between the device and the plane is small
        compared to the overall surface area dimensions of the device. This assumption allows for a point-
        wise closed-form solution of capacitance between the surface nodes and the plane; i.e. CAP =
        EPZERO\2AREA/GAP, where EPZERO if the free-space permittivity, AREA is the area associated with the
        node, and GAP is the gap between the node and the plane. The area for each node is computed using
        the ARNODE function. See the :ref:`get` command description for more information on the ARNODE
        function.

        With a distributed set of ``TRANS126`` elements attached directly to the structure and a plane (such
        as a ground plane), you can perform a full range of coupled electrostatic-structural simulations,
        including:

        * Static analysis (due to a DC voltage or a mechanical load)

        * Prestressed modal analysis (eigenfrequencies, including frequency-shift effects of a DC bias
          voltage)

        * Prestressed harmonic analysis (system response to a small-signal AC excitation with a DC bias
          voltage or mechanical load)

        * Large signal transient analysis (time-transient solution due to an arbitrary time-varying voltage
          or mechanical excitation)

        The ``TRANS126`` element also employs a node-to-node gap feature so you can perform contact-type
        simulations where the structure contacts a plane (such as a ground plane). The contact stiffness
        factor, FKN, is used to control contact penetration once contact is initiated. A smaller value
        provides for easier convergence, but with more penetration.
        """
        command = f"EMTGEN,{ncomp},{ecomp},{pncomp},{dof},{gap},{gapmin},{fkn},{epzero},,{smethod}"
        return self.run(command, **kwargs)

    def en(
        self,
        iel: str = "",
        i: str = "",
        j: str = "",
        k: str = "",
        l: str = "",
        m: str = "",
        n: str = "",
        o: str = "",
        p: str = "",
        **kwargs,
    ):
        r"""Defines an element by its number and node connectivity.

        Mechanical APDL Command: `EN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EN.html>`_

        Parameters
        ----------
        iel : str
            Number assigned to element being defined. If ``IEL`` = P, graphical picking is enabled and all
            remaining command fields are ignored (valid only in the GUI).

        i : str
            Number of node assigned to first nodal position (node I).

        j : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        k : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        l : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        m : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        n : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        o : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        p : str
            Number assigned to second (node J) through eighth (node P) nodal position, if any.

        Notes
        -----

        .. _EN_notes:

        Defines an element by its nodes and attribute values. Similar to the :ref:`e` command except it
        allows the element number ( ``IEL`` ) to be defined explicitly. Element numbers need not be
        consecutive. Any existing element already having this number will be redefined.

        Up to 8 nodes may be specified with the :ref:`en` command. If more nodes are needed for the element,
        use the :ref:`emore` command. The number of nodes required and the order in which they should be
        specified are described in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ for each
        element type. The current (or default) MAT, TYPE,
        REAL, SECNUM, and ESYS attribute values are also assigned to the element.

        When creating elements with more than 8 nodes using this command and the :ref:`emore` command, it
        may be necessary to turn off shape checking using the :ref:`shpp` command before issuing this
        command. If a valid element type can be created without using the additional nodes on the
        :ref:`emore` command, this command will create that element. The :ref:`emore` command will then
        modify the element to include the additional nodes. If shape checking is active, it will be
        performed before the :ref:`emore` command is issued. Therefore, if the shape checking limits are
        exceeded, element creation may fail before the :ref:`emore` command modifies the element into an
        acceptable shape.
        """
        command = f"EN,{iel},{i},{j},{k},{l},{m},{n},{o},{p}"
        return self.run(command, **kwargs)

    def endrelease(
        self,
        tolerance: str = "",
        dof1: str = "",
        dof2: str = "",
        dof3: str = "",
        dof4: str = "",
        kjct: str = "",
        kcheck: str = "",
        **kwargs,
    ):
        r"""Specifies degrees of freedom to be decoupled for end release.

        Mechanical APDL Command: `ENDRELEASE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENDRELEASE.html>`_

        Parameters
        ----------

        tolerance : str
            Angle tolerance (in degrees) between adjacent elements ( ``KCHECK`` = 0), or a percentage
            tolerance value for comparing cross-section properties between adjacent elements ( ``KCHECK`` =
            1). Default = 20.

            To release all selected elements, set ``TOLERANCE`` = -1.

            See :ref:`ENDRELEASE_notes` for information about using this argument with ``KCHECK``.

        dof1 : str
            Degrees of freedom to release. If ``Dof1`` is blank, WARP is assumed and ``Dof2``, ``Dof3``, and
            ``Dof4`` are ignored.

            * ``WARP`` - Release the warping degree of freedom (default).

            * ``ROTX`` - Release rotations in the X direction.

            * ``ROTY`` - Release rotations in the Y direction.

            * ``ROTZ`` - Release rotations in the Z direction.

            * ``UX`` - Release displacements in the X direction.

            * ``UY`` - Release displacements in the Y direction.

            * ``UZ`` - Release displacements in the Z direction.

            * ``BALL`` - Create ball joints (equivalent to releasing WARP, ROTX, ROTY, and ROTZ).

        dof2 : str
            Degrees of freedom to release. If ``Dof1`` is blank, WARP is assumed and ``Dof2``, ``Dof3``, and
            ``Dof4`` are ignored.

            * ``WARP`` - Release the warping degree of freedom (default).

            * ``ROTX`` - Release rotations in the X direction.

            * ``ROTY`` - Release rotations in the Y direction.

            * ``ROTZ`` - Release rotations in the Z direction.

            * ``UX`` - Release displacements in the X direction.

            * ``UY`` - Release displacements in the Y direction.

            * ``UZ`` - Release displacements in the Z direction.

            * ``BALL`` - Create ball joints (equivalent to releasing WARP, ROTX, ROTY, and ROTZ).

        dof3 : str
            Degrees of freedom to release. If ``Dof1`` is blank, WARP is assumed and ``Dof2``, ``Dof3``, and
            ``Dof4`` are ignored.

            * ``WARP`` - Release the warping degree of freedom (default).

            * ``ROTX`` - Release rotations in the X direction.

            * ``ROTY`` - Release rotations in the Y direction.

            * ``ROTZ`` - Release rotations in the Z direction.

            * ``UX`` - Release displacements in the X direction.

            * ``UY`` - Release displacements in the Y direction.

            * ``UZ`` - Release displacements in the Z direction.

            * ``BALL`` - Create ball joints (equivalent to releasing WARP, ROTX, ROTY, and ROTZ).

        dof4 : str
            Degrees of freedom to release. If ``Dof1`` is blank, WARP is assumed and ``Dof2``, ``Dof3``, and
            ``Dof4`` are ignored.

            * ``WARP`` - Release the warping degree of freedom (default).

            * ``ROTX`` - Release rotations in the X direction.

            * ``ROTY`` - Release rotations in the Y direction.

            * ``ROTZ`` - Release rotations in the Z direction.

            * ``UX`` - Release displacements in the X direction.

            * ``UY`` - Release displacements in the Y direction.

            * ``UZ`` - Release displacements in the Z direction.

            * ``BALL`` - Create ball joints (equivalent to releasing WARP, ROTX, ROTY, and ROTZ).

        kjct : str
            Behavior at a junction node (a node shared by more than two elements):

            * 0 (or blank) - Release all elements. ``TOLERANCE`` is ignored.
            * 1 - Release noncontinuous elements (if only one pair of continuous elements exists).

            This argument is ignored (due to ambiguity) if ``KJCT`` = 1 and multiple pairs of continuous
            elements exist.

            This argument is ignored if ``TOLERANCE`` = -1.

        kcheck : str
            Controls how connected elements are checked at selected nodes.

            * 0 (or blank) - Check only the angle between connected elements at the selected nodes (default).
            * 1 - Check the angle and other cross-section properties (including offsets and orientations)
              between connected elements at the selected nodes.

            This argument is ignored if ``TOLERANCE`` = -1.

        Notes
        -----

        .. _ENDRELEASE_notes:

        :ref:`endrelease` specifies end releases for the ``BEAM188``, ``BEAM189``, ``PIPE288``, and
        ``PIPE289`` elements. The command works on currently selected nodes and elements.

        Depending on the specified ``KCHECK``, the command generates end releases on any two connected
        elements whose angle at the connection is > ``TOLERANCE``, or whose cross-section properties have a
        difference > ``TOLERANCE`` percent.

        From within the GUI, the Picked node option (equivalent to ``TOLERANCE`` = -1) generates an end
        release at the selected node regardless of the angle of connection or cross-section properties.

        When ``KCHECK`` = 1:

        * The specified ``TOLERANCE`` serves as a percentage for comparing cross-section properties between
          adjacent elements. (For example, if using the default ``TOLERANCE`` = 20, the tolerance is
          considered to be 20 percent.)

        * In addition to the angle between connected elements, the section integrated properties (such as
          area, Iyy, Iyz, Izz, warping constant, and torsion constant), offsets, and cross-section
          orientations are also compared at the selected nodes. If the difference in any of the properties
          (or angles) is > ``TOLERANCE``, the requested degrees of freedom are released for those nodes.

        * For comparing cross-section orientations, the Y axes of cross-sections are compared after being
          projected onto the middle plane (the plane having a normal vector equal to the average of element
          X axes).

        * For comparing offsets, the differences in the centers of cross-sections are compared against the
          approximate maximum section size of the connected elements.

        Examples: End-Release Conditions at a Junction Node when KJCT= 1 and KCHECK= 0
        ******************************************************************************

        .. flat-table::
           :header-rows: 1

           * - Example Junction Node (E - Element)
             - Behavior
           * -
             - E2 is not released. E3 is released. A new node is generated for E3.
           * -
             - E2 and E3 are released if the angles between E1-E2 and E1-E3 are within tolerance (two continuous pairs).
           * -
             - E2, E3, and E4 are released regardless of ``KJCT`` (two continuous pairs).
           * -
             - E4 is not released. E2 and E3 are released. New nodes are generated for E2 and E3.

        Examples: Using KCHECKwith TOLERANCE= 20
        ****************************************

        .. flat-table::
           :header-rows: 1

           * - Example (E - Element, N - Node)
             - Behavior when ``KCHECK`` = 0
             - Behavior when ``KCHECK`` = 1
           * -
             - E1 and E2 are connected at an angle > 20°, so an end release is generated at N2.
             - E1 and E2 have the same section properties but are connected at an angle > 20°, so an end release is generated at N2.
           * -
             - E3 and E4 are continuous (angle between them is < 20°), so an end release is not generated at N4.
             - E3 and E4 use different beam sections, so an end release is generated at N4.
           * -
             - E5 and E6 are continuous (angle between them is less than 20°), so an end release is not generated at N6.
             - The difference between the section properties of E5 and E6 is > 20%, so an end release is generated at N6.
           * -
             - E7 and E8 are continuous (angle between them are < 20°), so an end release is not generated at N8.
             - The difference between the section offsets of E7 and E8 is > 20%, so an end release is generated at N8.
           * -
             - E9 and E10 are continuous (angle between them is < 20°), so an end release is not generated at N10.
             - The difference between the cross-section orientations of E9 and E10 is > 20°, so an end release is generated at N10.

        To list the coupled sets generated by this command, issue :ref:`cplist`.

        Exercise engineering judgement when using this command. Improper use may result in mechanics that
        render a solution impossible.
        """
        command = f"ENDRELEASE,,{tolerance},{dof1},{dof2},{dof3},{dof4},{kjct},{kcheck}"
        return self.run(command, **kwargs)

    def engen(
        self,
        iinc: str = "",
        itime: str = "",
        ninc: str = "",
        iel1: str = "",
        iel2: str = "",
        ieinc: str = "",
        minc: str = "",
        tinc: str = "",
        rinc: str = "",
        cinc: str = "",
        sinc: str = "",
        dx: str = "",
        dy: str = "",
        dz: str = "",
        **kwargs,
    ):
        r"""Generates elements from an existing pattern.

        Mechanical APDL Command: `ENGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENGEN.html>`_

        Parameters
        ----------
        iinc : str
            Increment to be added to element numbers in pattern.

        itime : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the given pattern
            by ``NINC`` each time after the first. ``ITIME`` must be > 1 if generation is to occur. ``NINC``
            may be positive, zero, or negative.

        ninc : str
            Do this generation operation a total of ``ITIME`` s, incrementing all nodes in the given pattern
            by ``NINC`` each time after the first. ``ITIME`` must be > 1 if generation is to occur. ``NINC``
            may be positive, zero, or negative.

        iel1 : str
            Generate elements from the pattern that begins with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` )
            in steps of ``IEINC`` (defaults to 1). If ``IEL1`` is negative, ``IEL2`` and ``IEINC`` are
            ignored and use the last \| ``IEL1`` \| elements (in sequence backward from the maximum element
            number) as the pattern to be repeated. If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            all selected elements ( :ref:`esel` ) are used as the pattern to be repeated. If ``IEL1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are
            ignored).

        iel2 : str
            Generate elements from the pattern that begins with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` )
            in steps of ``IEINC`` (defaults to 1). If ``IEL1`` is negative, ``IEL2`` and ``IEINC`` are
            ignored and use the last \| ``IEL1`` \| elements (in sequence backward from the maximum element
            number) as the pattern to be repeated. If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            all selected elements ( :ref:`esel` ) are used as the pattern to be repeated. If ``IEL1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are
            ignored).

        ieinc : str
            Generate elements from the pattern that begins with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` )
            in steps of ``IEINC`` (defaults to 1). If ``IEL1`` is negative, ``IEL2`` and ``IEINC`` are
            ignored and use the last \| ``IEL1`` \| elements (in sequence backward from the maximum element
            number) as the pattern to be repeated. If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            all selected elements ( :ref:`esel` ) are used as the pattern to be repeated. If ``IEL1`` = P,
            graphical picking is enabled and all remaining command fields are ignored (valid only in the
            GUI). A component name may also be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are
            ignored).

        minc : str
            Increment material number of all elements in the given pattern by ``MINC`` each time after the
            first.

        tinc : str
            Increment type number by ``TINC``.

        rinc : str
            Increment real constant table number by ``RINC``.

        cinc : str
            Increment element coordinate system number by ``CINC``.

        sinc : str
            Increment section ID number by ``SINC``.

        dx : str
            Define nodes that do not already exist but are needed by generated elements ( :ref:`ngen`,
            ``ITIME,INC,NODE1,,,DX,DY,DZ`` ). Zero is a valid value. If blank, ``DX``, ``DY``, and ``DZ``
            are ignored.

        dy : str
            Define nodes that do not already exist but are needed by generated elements ( :ref:`ngen`,
            ``ITIME,INC,NODE1,,,DX,DY,DZ`` ). Zero is a valid value. If blank, ``DX``, ``DY``, and ``DZ``
            are ignored.

        dz : str
            Define nodes that do not already exist but are needed by generated elements ( :ref:`ngen`,
            ``ITIME,INC,NODE1,,,DX,DY,DZ`` ). Zero is a valid value. If blank, ``DX``, ``DY``, and ``DZ``
            are ignored.

        Notes
        -----

        .. _ENGEN_notes:

        Same as the :ref:`egen` command except it allows element numbers to be explicitly incremented (
        ``IINC`` ) from the generated set. Any existing elements already having these numbers will be
        redefined.
        """
        command = f"ENGEN,{iinc},{itime},{ninc},{iel1},{iel2},{ieinc},{minc},{tinc},{rinc},{cinc},{sinc},{dx},{dy},{dz}"
        return self.run(command, **kwargs)

    def enorm(self, enum: str = "", **kwargs):
        r"""Reorients shell element normals or line element node connectivity.

        Mechanical APDL Command: `ENORM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENORM.html>`_

        Parameters
        ----------
        enum : str
            Element number having the normal direction that the reoriented elements are to match. If
            ``ENUM`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI).

        Notes
        -----

        .. _ENORM_notes:

        Reorients shell elements so that their outward normals are consistent with that of a specified
        element. :ref:`enorm` can also be used to reorder nodal connectivity of line elements so that their
        nodal ordering is consistent with that of a specified element.

        For shell elements, the operation reorients the element by reversing and shifting the node
        connectivity pattern. For example, for a 4-node shell element, the nodes in positions I, J, K and L
        of the original element are placed in positions J, I, L and K of the reoriented element. All 3D
        shell elements in the selected set are considered for reorientation, and no element is reoriented
        more than once during the operation. Only shell elements adjacent to the lateral (side) faces are
        considered.

        The command reorients the shell element normals on the same panel as the specified shell element. A
        panel is the geometry defined by a subset of shell elements bounded by free edges or T-junctions
        (anywhere three or more shell edges share common nodes).

        Reorientation progresses within the selected set until either of the following conditions is true:

        * The edge of the model is reached.

        * More than two elements (whether selected or unselected) are adjacent to a lateral face.

        In situations where unselected elements might undesirably cause case b to control, consider using
         :ref:`ensym`,0,,0,ALL instead of :ref:`enorm`. It is recommended that reoriented elements be displayed and graphically reviewed.

        You cannot use the :ref:`enorm` command to change the normal direction of any element that has a
        body or surface load. We recommend that you apply all of your loads only after ensuring that the
        element normal directions are acceptable.

        Real constant values are not reoriented and may be invalidated by an element reversal.
        """
        command = f"ENORM,{enum}"
        return self.run(command, **kwargs)

    def ensym(
        self,
        iinc: str = "",
        ninc: str = "",
        iel1: str = "",
        iel2: str = "",
        ieinc: str = "",
        **kwargs,
    ):
        r"""Generates elements by symmetry reflection.

        Mechanical APDL Command: `ENSYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ENSYM.html>`_

        Parameters
        ----------
        iinc : str
            Increment to be added to element numbers in existing set.

        ninc : str
            Increment nodes in the given pattern by ``NINC``.

        iel1 : str
            Reflect elements from pattern beginning with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in
            steps of ``IEINC`` (defaults to 1). If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            pattern is all selected elements ( :ref:`esel` ). If ``IEL1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are ignored).

        iel2 : str
            Reflect elements from pattern beginning with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in
            steps of ``IEINC`` (defaults to 1). If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            pattern is all selected elements ( :ref:`esel` ). If ``IEL1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are ignored).

        ieinc : str
            Reflect elements from pattern beginning with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in
            steps of ``IEINC`` (defaults to 1). If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            pattern is all selected elements ( :ref:`esel` ). If ``IEL1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are ignored).

        Notes
        -----

        .. _ENSYM_notes:

        The :ref:`ensym` command is similar to the :ref:`esym` command except that it enables explicitly
        assigned element numbers to the generated set (in terms of an increment ``IINC`` ). Any existing
        elements already having these numbers are redefined.

        The operation generates a new element by incrementing the nodes on the original element, and
        reversing and shifting the node connectivity pattern. For example, for a 4-node 2D element, the
        nodes in positions I, J, K and L of the original element are placed in positions J, I, L and K of
        the reflected element.

        Similar permutations occur for all other element types. For line elements, the nodes in positions I
        and J of the original element are placed in positions J and I of the reflected element.

        See the :ref:`esym` command for additional information about symmetry elements.

        This command also provides a convenient way to reverse shell element normals. If the ``IINC`` and
        ``NINC`` argument fields are left blank, the effect of the reflection is to reverse the direction of
        the outward normal of the specified elements. You cannot use this command to change the normal
        direction of any element that has a body or surface load. It is best to apply all loading only after
        ensuring that the element normal directions are acceptable.

        Real constants (such as nonuniform shell thickness and tapered beam constants) may be invalidated by
        an element reversal.

        For more information about controlling element normals, see `Revising Your Model
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD8_6.html>`_.
        """
        command = f"ENSYM,{iinc},,{ninc},{iel1},{iel2},{ieinc}"
        return self.run(command, **kwargs)

    def eplot(self, **kwargs):
        r"""Produces an element display.

        Mechanical APDL Command: `EPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EPLOT.html>`_

        Notes
        -----

        .. _EPLOT_notes:

        Produces an element display of the selected elements. In full graphics, only those elements faces
        with all of their corresponding nodes selected are plotted. In PowerGraphics, all element faces of
        the selected element set are plotted irrespective of the nodes selected. However, for both full
        graphics and PowerGraphics, adjacent or otherwise duplicated faces of 3D solid elements will not be
        displayed in an attempt to eliminate plotting of interior facets. See the :ref:`dsys` command for
        display coordinate system issues.

        This command will display curvature in midside node elements when PowerGraphics is activated (
        :ref:`graphics` ,POWER) and :ref:`efacet`,2 or :ref:`efacet`,4 are enabled. (To display curvature,
        two facets per edge is recommended ( :ref:`efacet`,2)). When you specify :ref:`efacet`,1,
        PowerGraphics does not display midside nodes. :ref:`efacet` has no effect on :ref:`eplot` for non-
        midside node elements.

        This command is valid in any processor.
        """
        command = "EPLOT"
        return self.run(command, **kwargs)

    def eread(self, fname: str = "", ext: str = "", **kwargs):
        r"""Reads elements from a file.

        Mechanical APDL Command: `EREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EREAD.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to ELEM if ``Fname`` is
            blank.

        Notes
        -----

        .. _EREAD_notes:

        This read operation is not necessary in a standard anlaysis run but is provided as a convenience for
        those wanting to read a coded element file, such as from another mesh generator or from a CAD/CAM
        program.

        Data should be formatted as generated via :ref:`ewrite`.

        If issuing :ref:`eread` to acquire element information generated from :ref:`ewrite`, you must also
        issue :ref:`nread` before the :ref:`eread` command. The element types ( :ref:`et` ) must be defined
        before the file is read so that the file may be read properly. Only elements that are specified via
        :ref:`errang` are read from the file. Also, only elements that are fully attached to the nodes
        specified via :ref:`nrrang` are read from the file.

        Elements are assigned numbers consecutively as read from the file, beginning with the current
        highest database element number plus one. The file is rewound before and after reading. Reading
        continues until the end of the file.
        """
        command = f"EREAD,{fname},{ext}"
        return self.run(command, **kwargs)

    def ereinf(self, koffalim: str = "", ktri: str = "", **kwargs):
        r"""Generates reinforcing elements from selected existing (base) elements.

        Mechanical APDL Command: `EREINF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EREINF.html>`_

        Parameters
        ----------
        koffalim : str
            Enable or disable the limit of the angle between a ``MESH200`` element and a base element. Valid for
            the `mesh-independent method
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ only.

            * 0 - Enable the angle limit (default).
            * 1 - Disable the angle limit.

        ktri : str
            Specify the shape of 3D smeared reinforcing members. Valid for the `mesh-independent method
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ only.

            * 0 - Generate quad-dominant (mixed quadrilateral and triangular) reinforcing members (default).
            * 1 - Generate triangular reinforcing members only.

        Notes
        -----
        :ref:`ereinf` generates reinforcing elements ( ``REINF263``, ``REINF264`` and ``REINF265`` )
        directly from selected base elements (that is, existing standard structural elements in your model).
        The command scans all selected base elements and generates (if necessary) a compatible reinforcing
        element type for each base element. (You can select a combination of different base element types.)

        Before issuing :ref:`ereinf`, first define the reinforcing geometry, material, and orientation via
        one of two methods:

        `Mesh-Independent Method:
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_  Use
        ``MESH200`` elements to temporarily represent the geometry of the reinforcing fibers or smeared
        reinforcing surfaces. Define additional data including material, fiber cross-section area, fiber
        spacing, and fiber orientation via reinforcing sections with the mesh pattern ( :ref:`secdata` ) and
        assign the sections to corresponding ``MESH200`` elements. (Predefining the reinforcing element type
        ( :ref:`et` ) is not required.)

        `Standard Method:
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_  Define
        reinforcing section types ( :ref:`sectype` ) with standard reinforcing location patterns (
        :ref:`secdata` ). The standard reinforcing location input are given with respect to the selected
        base elements; therefore, a change in the base mesh may require redefining the (mesh-dependent)
        reinforcing section types.

        Standard element-definition commands (such as :ref:`et` and :ref:`e` ) are not used for defining
        reinforcing elements.

        :ref:`ereinf` creates no new nodes. The reinforcing elements and the base elements share the common
        nodes.

        Elements generated by :ref:`ereinf` are not associated with the solid model.

        After :ref:`ereinf` executes, you can issue :ref:`etlist`, :ref:`elist`, or :ref:`eplot` to verify
        the newly created reinforcing element types and elements.

        Reinforcing elements do not account for any subsequent modifications made to the base elements.
        Ansys, Inc. recommends issuing :ref:`ereinf` only after the base elements are finalized. If
        you delete or modify base elements (via :ref:`edele`, :ref:`emodif`, :ref:`etchg`, :ref:`emid`,
        :ref:`eorient`, :ref:`nummrg`, or :ref:`numcmp`, for example), remove all affected reinforcing
        elements and reissue :ref:`ereinf` to avoid inconsistencies.

        If you define reinforcing via the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_,
        :ref:`ereinf` creates new reinforcing sections containing details of the created reinforcing
        elements, then applies them to all newly generated reinforcing elements. The number of new
        reinforcing sections depends on the number of new reinforcing elements. (You can examine the
        properties of new sections ( :ref:`slist` ).) The program sets the ID number of the newest
        reinforcing section to the highest section ID number in the model. After issuing :ref:`ereinf`, the
        command shows the highest-numbered IDs (element type, element, and section). Do not overwrite a new
        reinforcing section when defining subsequent sections.

        For the 3D smeared-reinforcing element ( ``REINF265`` ) with the `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_, you can
        select the shape of the reinforcing members via ``KTri``. The default behavior ( ``KTri`` = 0)
        generates quad-dominant members (primarily quadrilaterals but with some triangles).

        :ref:`ereinf` can generate the reinforcing elements with thermal properties if the base elements are
        thermal solid elements ( ``SOLID278`` or ``SOLID279`` ):

        * If using the `mesh-independent method
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
          defining reinforcing, apply element body-force loading ( :ref:`bfe`,,HGEN) or nodal body-force
          loading ( :ref:`bf`,,HGEN) on the ``MESH200`` elements.

        * If using the `standard method
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_ for
          defining reinforcing, apply element body-force loading ( :ref:`bfe`,,HGEN) on the reinforcing
          members directly. (Do not apply nodal body-force loading ( :ref:`bf`,,HGEN).)

        If performing a subsequent structural analysis after the thermal analysis, :ref:`ereinf` can convert
        the reinforcing elements for the structural analysis: Convert the thermal base elements to the
        appropriate structural element ( :ref:`et` or :ref:`emodif` ).

        Select the reinforcing elements only.

        Issue :ref:`ereinf`.

        Result : The selected reinforcing elements are converted to elements compatible with the converted
        base elements.

        Solution accuracy can be affected if the volume ratio between reinforcing elements and base elements
        is high, particularly when body loading (such as heat generation) is applied via the reinforcing
        elements. If the program detects a high volume ratio of reinforcing elements generated via the
        `mesh-independent method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strreinfworkflow.html#>`_, it issues
        a warning message and saves affected base and ``MESH200`` elements (used to generate the reinforcing
        elements) into a component for close model inspection. Only the volume of reinforcing elements
        created by the current  :ref:`ereinf` command is considered in the volume-ratio calculation (that
        is, no volume accumulation occurs over multiple :ref:`ereinf` commands).

        For more information, see `Element Embedding
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        """
        command = f"EREINF,{koffalim},{ktri}"
        return self.run(command, **kwargs)

    def errang(self, emin: str = "", emax: str = "", einc: str = "", **kwargs):
        r"""Specifies the element range to be read from a file.

        Mechanical APDL Command: `ERRANG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ERRANG.html>`_

        Parameters
        ----------
        emin : str
            Elements with numbers from ``EMIN`` (defaults to 1) to ``EMAX`` (defaults to 999999999) in steps
            of ``EINC`` (defaults to 1) will be read.

        emax : str
            Elements with numbers from ``EMIN`` (defaults to 1) to ``EMAX`` (defaults to 999999999) in steps
            of ``EINC`` (defaults to 1) will be read.

        einc : str
            Elements with numbers from ``EMIN`` (defaults to 1) to ``EMAX`` (defaults to 999999999) in steps
            of ``EINC`` (defaults to 1) will be read.

        Notes
        -----

        .. _ERRANG_notes:

        Defines the element number range to be read ( :ref:`eread` ) from the element file. If a range is
        also implied from the :ref:`nrrang` command, only those elements satisfying both ranges will be
        read.
        """
        command = f"ERRANG,{emin},{emax},{einc}"
        return self.run(command, **kwargs)

    def esurf(self, xnode: str = "", tlab: str = "", shape: str = "", **kwargs):
        r"""Generates elements overlaid on the free faces of selected nodes.

        Mechanical APDL Command: `ESURF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESURF.html>`_

        Parameters
        ----------
        xnode : str
            Node number that is used only in the following two cases:

            * ``XNODE`` is a single extra node number (ID) used for generating SURF151 or SURF152 elements when
              KEYOPT(5)=1.
            * ``XNODE`` is a single pressure node number (ID) used for generating ``HSFLD241`` or ``HSFLD242``
              elements.

            There is no default. ``XNODE`` must be specified for the above cases. If ``XNODE`` = P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI). A parameter
            or parametric expression can be substituted for ``XNODE``.

        tlab : str
            Generates target, contact, and hydrostatic fluid elements with correct direction of normals.

            This option is valid only with ``TARGE169``, ``TARGE170``, ``CONTA172``, ``CONTA174``, ``CONTA177``, ``HSFLD241``, and ``HSFLD242`` elements.

            * ``TOP`` - Generates target and contact elements over beam and shell elements, or hydrostatic fluid
              elements over shell elements, with the normals the same as the underlying beam and shell elements
              (default).

            * ``BOTTOM`` - Generates target and contact elements over beam and shell elements, or hydrostatic
              fluid elements over shell elements, with the normals opposite to the underlying beam and shell
              elements.

              If target or contact elements and hydrostatic fluid elements are defined on the same underlying
              shell elements, you only need to use this option once to orient the normals opposite to the
              underlying shell elements.

            * ``REVERSE`` - Reverses the direction of the normals on existing selected target elements, contact
              elements, and hydrostatic fluid elements.

              If target or contact elements and hydrostatic fluid elements are defined on the same underlying
              shell elements, you only need to use this option once to reverse the normals for all selected
              elements.

        shape : str
            Used to specify the element shape for target element ``TARGE170`` ( ``Shape`` = LINE or POINT) or ``TARGE169`` elements ( ``Shape`` = POINT).

            * ``(blank)`` - The target element takes the same shape as the external surface of the underlying
              element (default).

            * ``LINE`` - Generates LINE or PARA (parabolic) segments on exterior of selected 3D elements.

            * ``POINT`` - Generates POINT segments on selected nodes.

        Notes
        -----

        .. _ESURF_notes:

        The :ref:`esurf` command generates elements of the currently active element type overlaid on the
        free faces of existing elements. For example, surface elements (such as ``SURF151``, ``SURF152``,
        ``SURF153``, ``SURF154``, or ``SURF159`` ) can be generated over solid elements (such as
        ``PLANE55``, ``SOLID70``, ``PLANE182``, ``SOLID185``, or ``SOLID272``, respectively).

        Element faces are determined from the selected node set ( :ref:`nsel` ) and the load faces for that
        element type. The operation is similar to that used for generating element loads from selected nodes
        via the :ref:`sf`,ALL command, except that elements (instead of loads) are generated. All nodes on
        the face must be selected for the face to be used. For shell elements, only face one of the element
        is available. If nodes are shared by adjacent selected element faces, the faces are not free and no
        element is generated.

        Elements created by :ref:`esurf` are oriented such that their surface load directions are consistent
        with those of the underlying elements. Carefully check generated elements and their orientations.

        Generated elements use the existing nodes and the active :ref:`mat`, :ref:`type`, :ref:`real`, and
        :ref:`esys` attributes. The exception is when ``Tlab`` = REVERSE. The reversed target and contact
        elements have the same attributes as the original elements. If the underlying elements are solid
        elements, ``Tlab`` = TOP or BOTTOM has no effect.

        When the command generates a target element, the shape is by default the same as that of the
        underlying element. Issue :ref:`esurf`,,,LINE or :ref:`esurf`,,,POINT to generate LINE, PARA, and
        POINT segments.

        The :ref:`esurf` command can also generate the 2D or 3D node-to-surface element ``CONTA175``, based
        on the selected node components of the underlying solid elements. When used to generate ``CONTA175``
        elements, all :ref:`esurf` arguments are ignored. (If ``CONTA175`` is the active element type, the
        path Main Menu> Preprocessor> Modeling> Create> Elements> Node-to-Surf uses :ref:`esurf` to generate
        elements.)

        To generate ``SURF151`` or ``SURF152`` elements that have two extra nodes from ``FLUID116``
        elements, KEYOPT(5) for ``SURF151`` or ``SURF152`` is first set to 0 and :ref:`esurf` is issued.
        Then KEYOPT(5) for ``SURF151`` or ``SURF152`` is set to 2 and :ref:`mstole` is issued. For more
        information, see `Using the Surface Effect Elements
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE2_5.html#>`_ in the
        `Thermal Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4.html>`_.

        For hydrostatic fluid elements ``HSFLD241`` and ``HSFLD242``, the :ref:`esurf` command generates
        triangular (2D) or pyramid-shaped (3D) elements with bases that are overlaid on the faces of
        selected 2D or 3D solid or shell elements. The single vertex for all generated elements is at the
        pressure node specified as ``XNODE``. The generated elements fill the volume enclosed by the solid
        or shell elements. The nodes on the overlaid faces have translational degrees of freedom, while the
        pressure node shared by all generated elements has a single hydrostatic pressure degree of freedom,
        HDSP (see ``HSFLD241`` and ``HSFLD242`` for more information about the pressure node).
        """
        command = f"ESURF,{xnode},{tlab},{shape}"
        return self.run(command, **kwargs)

    def esym(
        self, ninc: str = "", iel1: str = "", iel2: str = "", ieinc: str = "", **kwargs
    ):
        r"""Generates elements from a pattern by a symmetry reflection.

        Mechanical APDL Command: `ESYM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ESYM.html>`_

        Parameters
        ----------

        ninc : str
            Increment nodes in the given pattern by ``NINC``.

        iel1 : str
            Reflect elements from pattern beginning with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in
            steps of ``IEINC`` (defaults to 1). If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            pattern is all selected elements ( :ref:`esel` ). If ``IEL1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are ignored).

        iel2 : str
            Reflect elements from pattern beginning with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in
            steps of ``IEINC`` (defaults to 1). If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            pattern is all selected elements ( :ref:`esel` ). If ``IEL1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are ignored).

        ieinc : str
            Reflect elements from pattern beginning with ``IEL1`` to ``IEL2`` (defaults to ``IEL1`` ) in
            steps of ``IEINC`` (defaults to 1). If ``IEL1`` = ALL, ``IEL2`` and ``IEINC`` are ignored and
            pattern is all selected elements ( :ref:`esel` ). If ``IEL1`` = P, graphical picking is enabled
            and all remaining command fields are ignored (valid only in the GUI). A component name may also
            be substituted for ``IEL1`` ( ``IEL2`` and ``IEINC`` are ignored).

        Notes
        -----

        .. _ESYM_notes:

        Generates additional elements from a given pattern (similar to :ref:`egen` ) except with a symmetry
        reflection. The operation generates a new element by incrementing the nodes on the original element,
        and reversing and shifting the node connectivity pattern. For example, for a 4-node 2D element, the
        nodes in positions I, J, K, and L of the original element are placed in positions J, I, L, and K of
        the reflected element.

        Similar permutations occur for all other element types. For line elements, the nodes in positions I
        and J of the original element are placed in positions J and I of the reflected element.

        It is recommended that symmetry elements be displayed and graphically reviewed.

        If the nodes are also reflected (as with the :ref:`nsym` command), this pattern is such that the
        orientation of the symmetry element remains similar to the original element (that is, clockwise
        elements are generated from clockwise elements).

        For a non-reflected node pattern, the reversed orientation has the effect of reversing the outward
        normal direction (clockwise elements are generated from counterclockwise elements).

        Because nodes may be defined anywhere in the model independently of this command, any orientation of
        the symmetry elements is possible. See also the :ref:`ensym` command for modifying existing
        elements.
        """
        command = f"ESYM,,{ninc},{iel1},{iel2},{ieinc}"
        return self.run(command, **kwargs)

    def ewrite(
        self,
        fname: str = "",
        ext: str = "",
        kappnd: int | str = "",
        format_: str = "",
        **kwargs,
    ):
        r"""Writes elements to a file.

        Mechanical APDL Command: `EWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (up to 248 characters, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name.

            The file name defaults to :file:`Jobname`.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to ELEM if ``Fname`` is
            blank.

        kappnd : int or str
            Append key:

            * ``0`` - Rewind file before the write operation.

            * ``1`` - Append data to the end of the existing file.

        format_ : str
            Format key:

            * ``SHORT`` - I6 format (default).

            * ``LONG`` - I8 format. Switches automatically to I10 if entity IDs are large.

        Notes
        -----

        .. _EWRITE_notes:

        Writes the selected elements to a file. The write operation is unnecessary in a standard Mechanical
        APDL
        run but is provided as convenience to users wanting a coded element file.

        If issuing :ref:`ewrite` from Mechanical APDL to be used in Mechanical APDL, issue :ref:`nwrite` to
        store nodal
        information for later use.

        Only elements having all of their nodes defined (and selected) are written. Data are written in a
        coded format. The data description of each record is: I, J, K, L, M, N, O, P, MAT, TYPE, REAL,
        SECNUM, ESYS, IEL, where MAT, TYPE, REAL, and ESYS are attribute numbers, SECNUM is the beam section
        number, and IEL is the element number.

        The format is (14I6) if ``Format`` = SHORT, and (14I8 or 14I10) if ``Format`` = LONG.

        One element description per record is written for elements having <= 8 nodes. For elements having >
        8 nodes, nodes 9 and above are written on a second record using the same format.
        """
        command = f"EWRITE,{fname},{ext},,{kappnd},{format_}"
        return self.run(command, **kwargs)

    def gcdef(
        self,
        option: str = "",
        sect1: str = "",
        sect2: str = "",
        matid: str = "",
        realid: str = "",
        sect1end: str = "",
        sect2end: str = "",
        **kwargs,
    ):
        r"""Defines interface interactions between general contact surfaces.

        Mechanical APDL Command: `GCDEF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GCDEF.html>`_

        Parameters
        ----------
        option : str
            Option to be performed.

            * ``(blank)`` - Retain the previous ``Option`` setting between ``SECT1`` and ``SECT2``.

            * ``AUTO`` - Define auto asymmetric contact between surfaces ``SECT1`` and ``SECT2``.

            * ``SYMM`` - Define symmetric contact between surfaces ``SECT1`` and ``SECT2``.

            * ``ASYM`` - Define asymmetric contact with ``SECT1`` as the source (contact) surface and ``SECT2``
              as the target surface.

            * ``EXCL`` - Exclude contact between surfaces ``SECT1`` and ``SECT2``. ``MATID``, ``REALID``,
              ``SECT1END``, and ``SECT2END`` are ignored.

            * ``DELETE`` - Remove the given definition from the :ref:`gcdef` table. ``MATID``, ``REALID``,
              ``SECT1END``, and ``SECT2END`` are ignored.

              Note that :ref:`gcdef`,DELETE,ALL,ALL does not remove the entire :ref:`gcdef` table; it merely
              removes any existing :ref:`gcdef`,,ALL,ALL definitions, while leaving intact any existing
              :ref:`gcdef` definitions that are more specific.

              To remove the entire :ref:`gcdef` table, issue :ref:`gcdef`,DELETE,TOTAL.

              It is good practice to list all definitions using :ref:`gcdef`,LIST before and after a
              :ref:`gcdef`,DELETE command.

            * ``LIST`` - List stored :ref:`gcdef` data entries. ``MATID`` and ``REALID`` are ignored.

              :ref:`gcdef`,LIST lists all defined interactions. :ref:`gcdef`,LIST, ``SECT1``, ``SECT2`` lists the
              entry for the specific ``SECT1`` / ``SECT2`` interaction. :ref:`gcdef`,LIST,ALL,ALL lists only the
              ALL,ALL entry (if any).

            * ``TABLE`` - List interpreted general contact definitions in tabular format. ``MATID`` and
              ``REALID`` are ignored.

              By default, rows/columns of the table that match neighboring rows/columns are compressed to simplify
              the table. Issue :ref:`gcdef`,TABLE,TOTAL to list the entire :ref:`gcdef` table without removal of
              duplicate rows and columns.

            * ``TABLESOL`` - List a table showing actual interactions considered during solution. This option is
              only available after the :ref:`solve` command. ``MATID`` and ``REALID`` are ignored.

              The table shows MAT and REAL entries considered during the solution (actual contact may or may not
              have occurred). This is in contrast to :ref:`gcdef`,TABLE, which shows the user specifications. For
              auto asymmetric contact, TABLESOL indicates which of the possible contact versus target surface
              combinations was considered.

        sect1 : str
            Section numbers representing contact ( ``SECT1`` ) and target ( ``SECT2`` ) general contact surfaces
            (no defaults). (In most cases, the actual determination of contact versus target surfaces takes
            place during :ref:`solve`.)

            A node component name is also valid input for ``SECT1`` and ``SECT2``. The component name is not
            stored. Instead, the program loops through all valid section IDs found in the component and creates
            :ref:`gcdef` entries for all possible SECT1/SECT2 combinations that result. These entries are
            reflected in the ``Option`` = LIST and TABLE output. Section IDs can be further controlled by adding
            an extension (_EDGE, _FACE, _VERT, _TOP, or _BOT) to the end of the component name. See in the
            `Contact Technology Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_flpressexamp.html>`_ for more information.

            The following labels are also valid input:

            * ``SELF`` - Self contact.

            * ``ALL`` - All general contact sections IDs.

            * ``ALL_EDGE`` - Section IDs of all ``CONTA177`` general contact line elements (which may be on the
              edges of 3D solid and shell base elements, or on beam base elements).

            * ``ALL_FACE`` - Section IDs of all general contact elements on faces of solid or shell base
              elements (both top and bottom faces of shell elements).

            * ``ALL_VERT`` - Section IDs of all ``CONTA175`` general contact vertex elements (which may be on
              convex corners of solid and shell base elements, and on endpoints of beam base elements).

            * ``ALL_TOP`` - Section IDs of all general contact elements on top faces of shell base elements, and
              faces of solid base elements.

            * ``ALL_BOT`` - Section IDs of general contact elements on bottom faces of shell base elements, and
              faces of solid base elements.

            The ALL labels apply to all defined general contact element section IDs in the model without regard
            to the select status of the elements or attached nodes.

            See :ref:`sect12interact` ``SECT1`` / ``SECT2`` Interactions for a description of how the various
            inputs for ``SECT1`` and ``SECT2`` are interpreted.

        sect2 : str
            Section numbers representing contact ( ``SECT1`` ) and target ( ``SECT2`` ) general contact surfaces
            (no defaults). (In most cases, the actual determination of contact versus target surfaces takes
            place during :ref:`solve`.)

            A node component name is also valid input for ``SECT1`` and ``SECT2``. The component name is not
            stored. Instead, the program loops through all valid section IDs found in the component and creates
            :ref:`gcdef` entries for all possible SECT1/SECT2 combinations that result. These entries are
            reflected in the ``Option`` = LIST and TABLE output. Section IDs can be further controlled by adding
            an extension (_EDGE, _FACE, _VERT, _TOP, or _BOT) to the end of the component name. See in the
            `Contact Technology Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_flpressexamp.html>`_ for more information.

            The following labels are also valid input:

            * ``SELF`` - Self contact.

            * ``ALL`` - All general contact sections IDs.

            * ``ALL_EDGE`` - Section IDs of all ``CONTA177`` general contact line elements (which may be on the
              edges of 3D solid and shell base elements, or on beam base elements).

            * ``ALL_FACE`` - Section IDs of all general contact elements on faces of solid or shell base
              elements (both top and bottom faces of shell elements).

            * ``ALL_VERT`` - Section IDs of all ``CONTA175`` general contact vertex elements (which may be on
              convex corners of solid and shell base elements, and on endpoints of beam base elements).

            * ``ALL_TOP`` - Section IDs of all general contact elements on top faces of shell base elements, and
              faces of solid base elements.

            * ``ALL_BOT`` - Section IDs of general contact elements on bottom faces of shell base elements, and
              faces of solid base elements.

            The ALL labels apply to all defined general contact element section IDs in the model without regard
            to the select status of the elements or attached nodes.

            See :ref:`sect12interact` ``SECT1`` / ``SECT2`` Interactions for a description of how the various
            inputs for ``SECT1`` and ``SECT2`` are interpreted.

        matid : str
            Material ID number for general contact interaction properties at the ``SECT1`` / ``SECT2``
            interface. If zero or blank, the previous setting of ``MATID`` for ``SECT1`` / ``SECT2`` (if
            any) is retained.

            As an example, you could specify "always bonded" contact behavior at the interface by setting
            ``MATID`` to 2 and issuing the command :ref:`tb`,INTER,2,,,ABOND.

            The coefficient of friction MU is also defined by ``MATID``. Since the default is ``MATID`` = 0,
            frictionless contact (MU = 0) is assumed by default.

        realid : str
            Real constant ID number for general contact interaction properties at the ``SECT1`` / ``SECT2``
            interface. If zero or blank, the previous setting of ``REALID`` for ``SECT1`` / ``SECT2`` (if
            any) is retained.

            As an example, you could specify contact stiffness (FKN) = 10 at the interface by setting
            ``REALID`` to 14 and issuing the command :ref:`r`,14,,,10.

        sect1end : str
            Last section number in the range. For ``Option`` = LIST, TABLE, or TABLESOL, data entries are
            processed for contact section numbers in the range from ``SECT1`` to ``SECT1END``, and target
            section numbers in the range from ``SECT2`` to ``SECT2END``. ``SECT1END`` and ``SECT2END`` are
            ignored for all other ``Option`` labels.

        sect2end : str
            Last section number in the range. For ``Option`` = LIST, TABLE, or TABLESOL, data entries are
            processed for contact section numbers in the range from ``SECT1`` to ``SECT1END``, and target
            section numbers in the range from ``SECT2`` to ``SECT2END``. ``SECT1END`` and ``SECT2END`` are
            ignored for all other ``Option`` labels.

        Notes
        -----

        .. _GCDEF_notes:

        :ref:`gcdef` defines the interface interaction between general contact surfaces identified by
        ``SECT1`` and ``SECT2``. :ref:`gcdef` commands are order independent in most cases.

        :ref:`gcdef` definitions should be issued after :ref:`gcgen`. They are saved in the database and are
        written to and read from :file:`.CDB` files.

        See `General Contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_

        .. _sect12interact:

        .. rubric:: **SECT1/ SECT2 Interactions**

        The most specific types of general contact definitions are those described below:

        * ``SECT1`` = any valid general surface section ID and ``SECT2`` = any different valid general
          surface section ID: ``Option``, ``MATID``, and ``REALID`` apply to general surface interactions
          between ``SECT1`` and ``SECT2``. This is one of the most specific types of general contact
          definitions and is never overridden.
        * ``SECT1`` = any valid general surface section ID and ``SECT2`` = ``SECT1`` : ``Option``,
          ``MATID``, and ``REALID`` apply to general surface self contact interactions involving ``SECT1``.
          This is one of the most specific types of general contact definitions and is never overridden.

        The remaining general contact definition types can be overridden by the above two general contact
        definition types:

        * ``SECT1`` = ALL and ``SECT2`` = ALL: ``Option``, ``MATID``, and ``REALID`` apply to all general
          surface interactions, except where overridden by a more specific :ref:`gcdef` command.
        * ``SECT1`` = ALL and ``SECT2`` = SELF or ``SECT1`` = SELF and ``SECT2`` = ALL: ``Option``,
          ``MATID``, and ``REALID`` apply to all general surface self contact interactions, except where
          overridden by a more specific :ref:`gcdef` command.
        * ``SECT1`` = ALL and ``SECT2`` = any valid general surface section ID: ``Option``, ``MATID``, and
          ``REALID`` apply to all general surface interactions that include ``SECT2``, except where
          overridden by a more specific :ref:`gcdef` command.
        * ``SECT1`` = any valid general surface section ID and ``SECT2`` = ALL: ``Option``, ``MATID``, and
          ``REALID`` apply to all general surface interactions that include ``SECT1``, except where
          overridden by a more specific :ref:`gcdef` command.
        """
        command = (
            f"GCDEF,{option},{sect1},{sect2},{matid},{realid},{sect1end},{sect2end}"
        )
        return self.run(command, **kwargs)

    def gcgen(
        self,
        option: str = "",
        featureangle: str = "",
        edgekey: int | str = "",
        splitkey: str = "",
        selopt: str = "",
        **kwargs,
    ):
        r"""Creates contact elements for general contact.

        Mechanical APDL Command: `GCGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GCGEN.html>`_

        Parameters
        ----------
        option : str
            Option to be performed.

            * ``NEW`` - Create a new general contact definition. This option removes all existing general
              contact elements and generates new elements with new section IDs. Any existing :ref:`gcdef`
              specifications, general contact :ref:`sectype` / :ref:`secdata` data, and general contact element
              types are also removed. If no general contact elements or data exist, this option behaves the same
              as ``Option`` = UPDATE.

            * ``UPDATE`` - Generate general contact elements on newly added (or selected) base elements. Newly
              generated contact elements are assigned new Section IDs. Existing general contact elements remain
              with their previously assigned section IDs and element attributes. Existing :ref:`gcdef` and
              :ref:`sectype` / :ref:`secdata` general contact data are respected. (This is the default option.)

            * ``DELETE`` - Remove all existing general contact elements. Existing :ref:`gcdef` specifications,
              general contact :ref:`sectype` / :ref:`secdata` data, and general contact element types are also
              removed.

            * ``SELECT`` - Select all existing general contact elements.

        featureangle : str
            Angle tolerance for determining feature edges ( ``EdgeKEY`` ) and general surfaces (
            ``SplitKey`` ). Default = 42 degrees.

        edgekey : int or str
            Key that controls creation of general contact line and vertex elements ( ``CONTA177``, ``CONTA175`` ) on base elements. Line elements are overlaid on feature edges of 3D deformable bodies and on perimeter edges of 3D shell structures; vertex elements are overlaid on convex corners of deformable bodies and shell structures (2D or 3D), and on endpoints of 3D beam structures. See :ref:`Understanding <usingfeatang>` ``FeatureANGLE`` for an explanation of the feature edge criteria.

            * ``0`` - Exclude all edges and vertices (default).

            * ``1`` - Include ``CONTA177`` elements on feature edges only.

            * ``2`` - Include ``CONTA177`` elements on shell perimeter edges only.

            * ``3`` - Include ``CONTA177`` elements on feature edges and shell perimeter edges.

            * ``4`` - Include ``CONTA177`` elements on feature edges and shell perimeter edges, and ``CONTA175``
              elements on vertices.

            * ``5`` - Include ``CONTA175`` elements on vertices only.

            ``EdgeKey`` > 0 is intended to add extra contact constraint between an edge or vertex of one surface
            and other 3D surfaces. Both edge and vertex contact always use the penalty method and only include
            structural degrees of freedom (UX, UY, UZ).

            :ref:`gcgen` always creates ``CONTA177`` elements on base beam elements, regardless of the
            ``EdgeKEY`` setting.

        splitkey : str
            Key that controls how section IDs and contact element type IDs are assigned to surfaces.

            * ``SPLIT`` - Assign a different section ID and contact element type ID for every general surface of
              the selected base elements (default). See :ref:`Understanding <usingfeatang>` ``FeatureANGLE`` for
              an explanation of the split criteria. Different section IDs are assigned to the top and bottom
              surfaces of 2D shell and 3D shell bodies. This allows different :ref:`gcdef` specifications for
              different portions of the assembly.

            * ``PART`` - Assign a different section ID and contact element type ID for every general surface
              which covers a physical part. Compared to the SPLIT option, this option produces fewer unique
              section IDs, which can make it easier to specify interactions via :ref:`gcdef`. However, it may also
              result in a less accurate and/or less efficient solution.

        selopt : str
            Key that controls which base elements are considered for general contact.

            * ``ATTACH`` - Use a recursive adjacency selection to obtain complete physical parts (default). This
              selection starts from the selected base elements, progressively adding elements adjacent to the
              faces of selected elements until the edge of a part is reached. Then general contact elements are
              generated.

            * ``SELECT`` - Use only the initially selected base elements to generate general contact elements.

        Notes
        -----

        .. _GCGEN_notes:

        :ref:`gcgen` creates general contact elements on the exterior faces of selected base elements. The
        base elements can be 2D or 3D solids, 3D beams, 2D shells (top and bottom), or 3D shells (top and
        bottom). The contact element types can be ``CONTA172``, ``CONTA174``, ``CONTA175``, and/or
        ``CONTA177``, depending upon the types of base elements in the model and the specified :ref:`gcgen`
        options. General contact elements are identified by a real constant ID equal to zero.

        You can control contact interactions between specific general contact surfaces that could
        potentially be in contact by using the :ref:`gcdef` command. See `General Contact
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_

        .. _usingfeatang:

        .. rubric:: **Understanding FeatureANGLE**

        The exterior facets of the selected base solid and shell elements are divided into subsets based on
        the angle between the normals of neighboring faces. On a flat or smooth surface, adjacent exterior
        element faces have normals that are parallel or nearly parallel; that is, the angle between the
        adjacent normals is near zero degrees.

        When the angle between the normals of two adjacent faces is greater than ``FeatureANGLE``, the two
        faces are considered to be on two separate surfaces ( ``SplitKey`` = SPLIT). The edge between the
        faces may be convex or concave. A convex (or outside) edge is considered to be a feature edge and
        may be affected by the ``EdgeKEY`` setting. For more information, see `Feature Angle ( FeatureANGLE)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_generategc.html#gencontsurf>`_
        """
        command = f"GCGEN,{option},{featureangle},{edgekey},{splitkey},{selopt}"
        return self.run(command, **kwargs)

    def laylist(
        self,
        iel: str = "",
        layr1: str = "",
        layr2: str = "",
        mplab1: str = "",
        mplab2: str = "",
        **kwargs,
    ):
        r"""Lists real constants material properties for layered elements.

        Mechanical APDL Command: `LAYLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LAYLIST.html>`_

        Parameters
        ----------
        iel : str
            Element number to be listed. If ALL, list all selected elements ( :ref:`esel` ) of the
            appropriate type. If blank and the current element type is a layered element type, list data
            from the current real constant table in the layered format.

        layr1 : str
            Range of layer numbers to be listed. If ``LAYR1`` is greater than ``LAYR2``, a reverse order
            list is produced. ``LAYR1`` defaults to 1. ``LAYR2`` defaults to ``LAYR1`` if ``LAYR1`` is input
            or to the number of layers if ``LAYR1`` is not input.

        layr2 : str
            Range of layer numbers to be listed. If ``LAYR1`` is greater than ``LAYR2``, a reverse order
            list is produced. ``LAYR1`` defaults to 1. ``LAYR2`` defaults to ``LAYR1`` if ``LAYR1`` is input
            or to the number of layers if ``LAYR1`` is not input.

        mplab1 : str
            Material property labels (for example, EX) to be listed along with the layer real constants.

        mplab2 : str
            Material property labels (for example, EX) to be listed along with the layer real constants.

        Notes
        -----

        .. _LAYLIST_notes:

        Lists real constants and any two material properties for layered shell and solid elements.

        If matrix input is selected (KEYOPT(2) = 2 or 3), ``LAYR1``, ``LAYR2``, ``Mplab1``, and ``Mplab2``
        are not used.

        This command is valid in any processor.
        """
        command = f"LAYLIST,{iel},{layr1},{layr2},{mplab1},{mplab2}"
        return self.run(command, **kwargs)

    def layplot(self, iel: str = "", layr1: str = "", layr2: str = "", **kwargs):
        r"""Displays the layer stacking sequence for layered elements.

        Mechanical APDL Command: `LAYPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LAYPLOT.html>`_

        Parameters
        ----------
        iel : str
            Element number for the display. If blank and the current element type is a layered element type,
            display data from the current real constant table.

        layr1 : str
            Range of layer numbers to be displayed. If ``LAYR1`` is greater than ``LAYR2``, a reversed order
            display is produced. Up to 20 layers may be displayed at a time. ``LAYR1`` defaults to 1.
            ``LAYR2`` defaults to ``LAYR1`` if ``LAYR1`` is input or to the number of layers (or to 19+
            ``LAYR1``, if smaller) if ``LAYR1`` is not input.

        layr2 : str
            Range of layer numbers to be displayed. If ``LAYR1`` is greater than ``LAYR2``, a reversed order
            display is produced. Up to 20 layers may be displayed at a time. ``LAYR1`` defaults to 1.
            ``LAYR2`` defaults to ``LAYR1`` if ``LAYR1`` is input or to the number of layers (or to 19+
            ``LAYR1``, if smaller) if ``LAYR1`` is not input.

        Notes
        -----

        .. _LAYPLOT_notes:

        Displays the layer-stacking sequence as defined in the real constant table for layered shell and
        solid elements in a form where the layers are visible (like a sheared deck of cards).

        The element x-axis is shown as 0.0 degrees.

        Layers are cross-hatched and color-coded for clarity. The hatch lines indicate the layer angle (real
        constant THETA) and the color coding is for material identification (real constant MAT).

        The actual orientation of a specific layer in three-  dimensional space can be seen using
        :ref:`psymb`,LAYR. To use :ref:`psymb`,LAYR with smeared reinforcing elements ( ``REINF265`` ),
        first set the vector-mode graphics option ( :ref:`device`,VECTOR,1).

        Layer thickness can be displayed using the :ref:`eshape` and :ref:`eplot` commands.

        This command is valid in any processor.
        """
        command = f"LAYPLOT,{iel},{layr1},{layr2}"
        return self.run(command, **kwargs)

    def lfsurf(self, sline: str = "", tline: str = "", **kwargs):
        r"""Generates surface elements overlaid on the edge of existing solid elements and assigns the extra
        node as the closest fluid element node.

        Mechanical APDL Command: `LFSURF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LFSURF.html>`_

        Parameters
        ----------
        sline : str
            Component name for the surface lines of the meshed solid areas. The component name must be 32
            characters or less.

        tline : str
            Component name for the target lines meshed with fluid elements. The component name must be 32
            characters or less.

        Notes
        -----

        .. _LFSURF_notes:

        This command macro is used to generate surface effect elements overlaid on the surface of existing
        plane elements and, based on proximity, to determine and assign the extra node for each surface
        element. The underlying areas of the solid region and the fluid lines must be meshed prior to
        calling this command macro. The active element type must be ``SURF151`` with appropriate settings
        for KEYOPT(4), KEYOPT(5), KEYOPT(6), and KEYOPT(8).

        The surface lines of the solid and the target lines of the fluid are grouped into components and
        named using the :ref:`cm` command. The names must be enclosed in single quotes (for example, '
        ``SLINE`` ') when the :ref:`lfsurf` command is manually typed in.

        When using the GUI method, node and element components are created through the picking dialog boxes
        associated with this command.

        The macro is applicable for the ``SURF151`` and ``FLUID116`` element types.
        """
        command = f"LFSURF,{sline},{tline}"
        return self.run(command, **kwargs)

    def ndsurf(self, snode: str = "", telem: str = "", dimn: int | str = "", **kwargs):
        r"""Generates surface elements overlaid on the edge of existing elements and assigns the extra node as
        the closest fluid element node.

        Mechanical APDL Command: `NDSURF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NDSURF.html>`_

        Parameters
        ----------
        snode : str
            Component name for the surface nodes of the solid elements. The component name must be 32
            characters or less.

        telem : str
            Component name for the target fluid elements. The component name must be 32 characters or less.

        dimn : int or str
            Model dimensionality:

            * ``2`` - 2D model.

            * ``3`` - 3D model.

        Notes
        -----

        .. _NDSURF_notes:

        This command macro is used to generate surface effect elements ( ``SURF151`` or ``SURF152`` )
        overlaid on the surface of existing plane or solid elements and, based on proximity, to determine
        and assign the extra node ( ``FLUID116`` ) for each surface element. The active element type must be
        ``SURF151`` or ``SURF152`` with appropriate settings for KEYOPT(4), KEYOPT(5), KEYOPT(6), and
        KEYOPT(8).

        The surface nodes of the plane or solid elements must be grouped into a node component and the fluid
        elements must be grouped into an element component and named using the :ref:`cm` command. The names
        must be enclosed in single quotes (for example, 'NOD') when the :ref:`ndsurf` command is manually
        typed in.

        When using the GUI method, node and element components are created through the picking dialog boxes
        associated with this command.

        The macro is applicable for the ``SURF151``, ``SURF152``, and ``FLUID116`` element types.
        """
        command = f"NDSURF,{snode},{telem},{dimn}"
        return self.run(command, **kwargs)

    def shsd(
        self,
        rid: str = "",
        action: str = "",
        chch_opt: str = "",
        cgap: str = "",
        cpen: str = "",
        **kwargs,
    ):
        r"""Creates or deletes a shell-solid interface to be used in shell-to-solid assemblies.

        Mechanical APDL Command: `SHSD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SHSD.html>`_

        Parameters
        ----------
        rid : str
            The real constant set ID that identifies the contact pair on which a shell-to-solid assembly is
            defined. If ALL, all selected contact pairs will be considered for assembly.

        action : str
            Action to be performed:

            * ``EDGE`` - Create virtual shell elements based on the shell edge (default).

            * ``SURFACE`` - Create virtual shell elements based on the solid element surface.

            * ``DELETE`` - Delete the nodes and elements created during a previous execution of :ref:`shsd` for
              the real constant set identified by ``RID``.

        chch_opt : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SHSD.html>`_ for further
            information.

        cgap : str
            Control parameter for opening gap; must be greater than or equal to zero. Close the gap if the
            gap distance is smaller than the ``CGAP`` value. ``CGAP`` defaults to 0.25\\*PINB (where PINB is
            the pinball radius) for bonded and no-separation contact. Otherwise, it defaults to the value of
            real constant ICONT.

        cpen : str
            Control parameter for initial penetration; must be greater than or equal to zero. Close the
            penetration if the penetration distance is smaller than the ``CPEN`` value. ``CPEN`` defaults to
            0.25\\*PINB (where PINB is the pinball radius) for any type of interface behavior (either bonded
            or standard contact).

        Notes
        -----

        .. _SHSD_notes:

        The :ref:`shsd` command creates a shell-solid interface to be used in shell-to-solid assemblies, or
        deletes a previously-created shell-solid interface. Virtual shell elements and additional
        ``CONTA175``  or ``CONTA177``  elements are created at the contact pair identified by ``RID`` when
        ``Action`` = EDGE or SURFACE. Set ``Action`` = DELETE to remove the generated nodes and elements at
        the contact pair identified by ``RID``.

        The :ref:`shsd` command is active only when the following element KEYOPTs of associated ``CONTA175``
        or ``CONTA177``  element types are predefined:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        When ``ACTION`` = EDGE, the virtual shell elements are built perpendicular to the pre-existing shell
        elements attached to the contact elements. They geometrically follow the contact interface edge and
        are built on both sides of this interface in such a way that each new shell element ( ``SHELL181`` )
        has two nodes that belong to the associated pre-existing shell element in the shell edge. (See
        :ref:`shsdcontact`.) The width of the new shell elements is half the thickness of the pre-existing
        shell element. If ``CONTA175`` is used at the shell nodes, the ``CONTA175`` elements are then
        created at each node of the virtual shell elements where no ``CONTA175`` element exists. If
        ``CONTA177`` is used at the shell edge, new ``CONTA174`` elements are created and overlayed on the
        virtual shell. The new contact elements are identified by the same contact pair ID as the pre-
        existing contact elements. The virtual shell elements are assigned the next available element type
        number and material number.

        .. figure:: ../../../images/_commands/gSHSDcontact.eps

           Virtual Shell Elements Following the Contact Interface Edge

        When ``ACTION`` = SURFACE, the virtual shell elements ( ``SHELL181`` - low order; ``SHELL281`` -
        high order) overlap the existing low or high order target elements identified with the ``RID``
        argument, and share their nodes. Only those target elements close enough to the contact interface
        (identified using the PINB real constant) are overlapped. The program uses the FTOLN real constant
        (defaults to half the shell element thickness) to define an influence distance. The associated
        virtual shell elements are created only for target elements that lie partially inside the influence
        distance region (see :ref:`shsdoverlap` ).

        .. figure:: ../../../images/_commands/gSHSDoverlap.eps

           Virtual Shell Elements Overlapping Target Elements

        For the bonded always option (KEYOPT(12) = 5), any contact node inside the pinball region (gap <
        PINB) is included in the KEYOPT(5) = 2 process. A relatively small PINB value may be used to prevent
        false contact. PINB defaults to 25% of the contact depth for small deformation analyses.

        For the bonded initial option (KEYOPT(12) = 6), only those contact nodes which initially lie inside
        the adjustment zone (gap < ICONT) are always included in the KEYOPT(5) = 2 process. ICONT defaults
        to 5% of the contact depth.

        For both processes, the new nodes and elements are stored in internally-named components. The
        internal naming convention is based on the real constant set ID specified by ``RID``, as illustrated
        in the following table.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        Issuing :ref:`shsd`, ``RID``,DELETE deletes components based on their generated names. Only
        components whose names match the internal naming convention will be deleted.

        .. warning::

            Do not rename or manually delete generated components. Use the SHSD command to delete generated
            components. Renaming or manually deleting generated components will cause these components to be
            ignored when SHSD, RID,DELETE is executed and when the program searches for these components to
            verify if SHSD, RID,EDGE or SURFACE can be safely executed. Manually renaming or deleting
            generated components and reissuing SHSD, RID,EDGE or SURFACE may result in erroneous generation
            of virtual shell or contact elements.

        :ref:`shsd` does not support assemblies that contain a preintegrated shell section (
        :ref:`sectype`,,GENS).

        See `Modeling a Shell-Solid Assembly
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_solshel.html#shell_sol_ko5eq2>`_
        """
        command = f"SHSD,{rid},{action},{chch_opt},{cgap},{cpen}"
        return self.run(command, **kwargs)

    def swadd(
        self,
        ecomp: str = "",
        shrd: str = "",
        ncm1: str = "",
        ncm2: str = "",
        ncm3: str = "",
        ncm4: str = "",
        ncm5: str = "",
        ncm6: str = "",
        ncm7: str = "",
        ncm8: str = "",
        ncm9: str = "",
        **kwargs,
    ):
        r"""Adds more surfaces to an existing spot weld set.

        Mechanical APDL Command: `SWADD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SWADD.html>`_

        Parameters
        ----------
        ecomp : str
            Name of an existing spot weld set that was previously defined using :ref:`swgen`.

        shrd : str
            Search radius. Defaults to 4 times the spot weld radius defined for the spot weld set ( ``SWRD``
            on :ref:`swgen` ).

        ncm1 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm2 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm3 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm4 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm5 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm6 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm7 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm8 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        ncm9 : str
            Surfaces to be added to the spot weld set. Each surface can be input as a predefined node
            component or a meshed area number.

        Notes
        -----
        This command adds surfaces to an existing spot weld set defined by the :ref:`swgen` command. You can
        add additional surfaces by repeating the :ref:`swadd` command. However, the maximum number of
        allowable surfaces (including the 2 surfaces used for the original set defined by :ref:`swgen` ) for
        each spot weld set is 11. See `Adding Surfaces to a Basic Set
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_spwdset.html#ctecreordersurf>`_
         for more information.
        """
        command = f"SWADD,{ecomp},{shrd},{ncm1},{ncm2},{ncm3},{ncm4},{ncm5},{ncm6},{ncm7},{ncm8},{ncm9}"
        return self.run(command, **kwargs)

    def swdel(self, ecomp: str = "", **kwargs):
        r"""Deletes spot weld sets.

        Mechanical APDL Command: `SWDEL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SWDEL.html>`_

        Parameters
        ----------
        ecomp : str
            Name of an existing spot weld set that was previously defined using :ref:`swgen`. If ``Ecomp`` =
            ALL (default) all spot welds are deleted.

        Notes
        -----
        This command deletes spot weld sets previously defined by the :ref:`swgen` command.
        """
        command = f"SWDEL,{ecomp}"
        return self.run(command, **kwargs)

    def swgen(
        self,
        ecomp: str = "",
        swrd: str = "",
        ncm1: str = "",
        ncm2: str = "",
        snd1: str = "",
        snd2: str = "",
        shrd: str = "",
        dirx: str = "",
        diry: str = "",
        dirz: str = "",
        itty: str = "",
        icty: str = "",
        **kwargs,
    ):
        r"""Creates a new spot weld set.

        Mechanical APDL Command: `SWGEN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SWGEN.html>`_

        Parameters
        ----------
        ecomp : str
            Name to identify the new spot weld, used for the element component containing the new contact,
            target, and beam elements generated for the spot weld set.

        swrd : str
            Spot weld radius.

        ncm1 : str
            Name of a component containing nodes on the first spot weld surface, or a meshed area number for
            the surface.

        ncm2 : str
            Name of a component containing nodes on the second spot weld surface, or a meshed area number
            for the surface.

        snd1 : str
            Node number of the first spot weld node corresponding to the first surface ( ``NCM1`` ). This
            node can be on or close to the first surface.

            To define multiple spot welds between two surfaces, input the name of a table array parameter
            containing the node information for each spot weld. The table name must be enclosed in % signs
            (for example, ``tabname``). If ``SND1`` is defined by tabular input, ``SND2`` is ignored.

        snd2 : str
            Node number of the second spot weld node corresponding to the second surface ( ``NCM2`` ). This
            node can be on or close to the second surface. Mechanical APDL creates the node if not
            specified.

        shrd : str
            Search radius. Defaults to 4 times the spot weld radius ``SWRD``.

        dirx : str
            Spot weld projection direction in terms of normal X, Y, and Z components.

        diry : str
            Spot weld projection direction in terms of normal X, Y, and Z components.

        dirz : str
            Spot weld projection direction in terms of normal X, Y, and Z components.

        itty : str
            Target element type ID.

        icty : str
            Contact element type ID.

        Notes
        -----
        This command creates a new spot weld set. You can add more surfaces to the set using :ref:`swadd`
        after the initial :ref:`swgen` command. However, the maximum number of allowable surfaces (including
        the two surfaces used for the original set) for each spot weld set is 11.

        ``Ecomp``, ``SWRD``, ``NCM1``, ``NCM2``, and ``SND1`` must be specified. ``SND2``, ``SHRD``,
        ``DIRX``, ``DIRY``, ``DIRZ``, ``ITTY``, ``ICTY`` are optional inputs. If the second spot weld node (
        ``SND2`` ) is specified, that node is used to determine the spot weld projection direction, and
        ``DIRX``, ``DIRY`` and ``DIRZ`` are ignored.

        If ``ITTY`` (target element ID) is specified, the following corresponding target element key option
        must be set: KEYOPT(2) = 1.

        If ``ICTY`` (contact element ID) is specified, the following corresponding contact element key
        options must be set: KEYOPT(2) = 2, KEYOPT(4) = 1, KEYOPT(12) = 5.

        After ``SND1`` and ``SND2`` are projected onto surface 1 and surface 2, respectively, two new pilot
        nodes (which represent the spot weld nodes) are generated at the locations of ``SND1`` and ``SND2``
        and meshed with ``TARGE170`` target elements ( :ref:`tshap`,PILO).

        By default, the contact pair created at each spot weld surface is an MPC-based `force-distributed
        constraint
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_surfcon.html#strbeamso1703>`_.
        To use force-distributed constraints based on the Lagrange multiplier method, you must set KEYOPT(2)
        = 3 for the contact elements after :ref:`swgen` is issued.

        To automatically define multiple spot welds between two surfaces, use tabular input in the ``SND1``
        field. The table array that you input must be a 2D array parameter. For more information, see
        `Automatic Generation of Multiple Spot Welds
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctecautogenmultisw.html#>`_

        To use the relaxation method to eliminate overconstraint, you must set KEYOPT(11) = 1 for the target
        elements after :ref:`swgen` is issued.

        Issue :ref:`swlist` and :ref:`swdel` to list or delete spot welds, respectively. For more
        information about defining spot welds, see `Creating a Basic Spot Weld Set with SWGEN
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/Hlp_ctec_spwdset.html#ctecswsrchrad>`_
        """
        command = f"SWGEN,{ecomp},{swrd},{ncm1},{ncm2},{snd1},{snd2},{shrd},{dirx},{diry},{dirz},{itty},{icty}"
        return self.run(command, **kwargs)

    def swlist(self, ecomp: str = "", **kwargs):
        r"""Lists spot weld sets.

        Mechanical APDL Command: `SWLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SWLIST.html>`_

        Parameters
        ----------
        ecomp : str
            Name of an existing spot weld set that was previously defined using :ref:`swgen`. If ``Ecomp`` =
            ALL (default), all spot weld sets are listed.

        Notes
        -----
        This command lists spot weld node, beam, and contact pair information for all defined spot weld
        sets, or for the specified set. To ensure that all defined spotwelds are listed, issue
        :ref:`cmsel`,ALL (to select all components) before issuing the :ref:`swlist` command.

        When :ref:`swlist` is issued in POST1, the beam forces and moments are output. For the case of a
        deformable spot weld, the stresses are also output in the beam local coordinate system.
        """
        command = f"SWLIST,{ecomp}"
        return self.run(command, **kwargs)

    def tshap(self, shape: str = "", **kwargs):
        r"""Defines simple 2D and 3D geometric surfaces for target segment elements.

        Mechanical APDL Command: `TSHAP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TSHAP.html>`_

        Parameters
        ----------
        shape : str
            Specifies the geometric shapes for target segment elements ``TARGE169`` and ``TARGE170``.

            * ``LINE`` - Straight line (2D, 3D) (Default for 2D)

            * ``PARA`` - Parabola (2D, 3D)

            * ``ARC`` - Clockwise arc (2D)

            * ``CARC`` - Counterclockwise arc (2D)

            * ``CIRC`` - Complete circle (2D)

            * ``TRIA`` - Three-node triangle (3D) (Default for 3D)

            * ``TRI6`` - Six-node triangle (3D)

            * ``QUAD`` - Four-node quadrilateral (3D)

            * ``QUA8`` - Eight-node quadrilateral (3D)

            * ``CYLI`` - Cylinder (3D)

            * ``CONE`` - Cone (3D)

            * ``SPHE`` - Sphere (3D)

            * ``PILO`` - Pilot node (2D, 3D)

            * ``POINT`` - Point (rigid surface node) (2D, 3D)

        Notes
        -----

        .. _TSHAP_notes:

        Use this command to specify the target segment shapes for the rigid target surface associated with
        surface-to-surface contact ( ``TARGE169``, ``CONTA172`` (2D) and ``TARGE170``, ``CONTA174`` (3D)),
        3D beam-to-beam contact ( ``TARGE170`` and ``CONTA177`` ), and 3D line-to-surface contact (
        ``TARGE170`` and ``CONTA177`` ). Once you issue :ref:`tshap`, all subsequent target elements
        generated via the direct element generation technique will have the same shape, until you issue
        :ref:`tshap` again with a different ``Shape`` value.
        """
        command = f"TSHAP,{shape}"
        return self.run(command, **kwargs)

    def upgeom(
        self,
        factor: str = "",
        lstep: str = "",
        sbstep: str = "",
        fname: str = "",
        ext: str = "",
        upesys: str = "",
        **kwargs,
    ):
        r"""Adds displacements from a previous analysis and updates the geometry to the deformed configuration.

        Mechanical APDL Command: `UPGEOM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_UPGEOM.html>`_

        Parameters
        ----------
        factor : str
            Multiplier for displacements being added to coordinates. The value 1.0 adds the full value of
            the displacements to the geometry of the finite element model. Defaults to 1.0.

        lstep : str
            Load step number of data to be imported. Defaults to the last load step.

        sbstep : str
            Substep number of data to be imported. Defaults to the last substep.

        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The field must be input (no default).

        ext : str
            Filename extension (eight-character maximum). The extension must be :file:`RST`.

        upesys : str
            Update behavior for the element coordinate system ( :ref:`esys` ):

            0 -- Do not update the element coordinate system (default).

            1 -- Update the element coordinate system to match the material orientation from a previous
            analysis.

        Notes
        -----

        .. _UPGEOM_notes:

        This command updates the geometry of the finite element model according to the displacement results
        of the previous analysis and creates a revised geometry at the deformed configuration. This command
        works on all nodes (default) or on a selected set of nodes. If this command is issued repeatedly, it
        creates a revised geometry of the finite element model in a cumulative fashion, that is, it adds
        displacement results on the previously generated deformed geometry. The solid model geometry is not
        updated by this command.

        When :ref:`upgeom` is issued, the current finite element model is overwritten by finite element
        information from the results file. For this reason, it is important that the finite element
        information in the results file matches the finite element model in which the nodal coordinates are
        being updated. No changes should be made to the model before the :ref:`upgeom` command is issued.

        ``UPESYS`` = 1 is available for homogeneous structural solid elements ( ``SOLID185``, ``SOLID186``,
        and ``SOLID187`` ) only and generates only Cartesian coordinate systems. The option is especially
        useful when conducting a `loop test
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strnonlininversesol.html#figlooptest>`_
        when orthotropic material is used. For more information, see `Nonlinear Static Analysis with Inverse
        Solving
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/strnonlininversesol.html#strinvsolvlimit>`_

        .. warning::

            Orientation nodes for beams and pipes always have zero displacements. Therefore, although this
            command may alter the locations of other beam and pipe nodes, it has no effect on orientation
            nodes. Carefully inspect the element coordinate systems on the updated model.
        """
        command = f"UPGEOM,{factor},{lstep},{sbstep},{fname},{ext},,{upesys}"
        return self.run(command, **kwargs)

    def usrdof(
        self,
        action: str = "",
        dof1: str = "",
        dof2: str = "",
        dof3: str = "",
        dof4: str = "",
        dof5: str = "",
        dof6: str = "",
        dof7: str = "",
        dof8: str = "",
        dof9: str = "",
        dof10: str = "",
        **kwargs,
    ):
        r"""Specifies the degrees of freedom for the user-defined element ``USER300``.

        Mechanical APDL Command: `USRDOF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USRDOF.html>`_

        Parameters
        ----------
        action : str
            One of the following command operations:

            * ``DEFINE`` - Specify the degrees of freedom (DOFs). This value is the default.

            * ``LIST`` - List all previously specified DOFs.

            * ``DELETE`` - Delete all previously specified DOFs.

        dof1 : str
            The list of DOFs.

        dof2 : str
            The list of DOFs.

        dof3 : str
            The list of DOFs.

        dof4 : str
            The list of DOFs.

        dof5 : str
            The list of DOFs.

        dof6 : str
            The list of DOFs.

        dof7 : str
            The list of DOFs.

        dof8 : str
            The list of DOFs.

        dof9 : str
            The list of DOFs.

        dof10 : str
            The list of DOFs.

        Notes
        -----
        The :ref:`usrdof` command specifies the degrees of freedom for the user-defined element ``USER300``.

        Although you can intersperse other commands as necessary for your analysis, issue the :ref:`usrdof`
        command as part of the following general sequence of commands:

        Issue the :ref:`et` command for element ``USER300``, followed by the related :ref:`type` command.

        Issue both the :ref:`usrelem` and :ref:`usrdof` commands (in either order).

        Define your element using ``USER300``.

        The DOF list ( ``DOF1`` through ``DOF10`` ) can consist of up to 10 DOFs. Use any valid and
        appropriate DOF (such as UX, UY, UZ, ROTX, ROTY, ROTZ, AX, AY, AZ, VX, VY, VZ, PRES, WARP, TEMP,
        VOLT, MAG, EMF, and CURR).

        You can specify a maximum of 10 DOFs per :ref:`usrdof` command. To define additional DOFs, issue the
        command again.

        The maximum number of DOFs for a user-defined element--the number of nodes times the number of DOFs
        per node--cannot exceed 480.

        To learn more about user-defined elements, see `Creating a New Element
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_UPFNEWEL.html#upfcreateelem2>`_
        """
        command = f"USRDOF,{action},{dof1},{dof2},{dof3},{dof4},{dof5},{dof6},{dof7},{dof8},{dof9},{dof10}"
        return self.run(command, **kwargs)

    def usrelem(
        self,
        nnodes: str = "",
        ndim: str = "",
        keyshape: str = "",
        nreal: str = "",
        nsavevars: str = "",
        nrsltvar: str = "",
        keyansmat: int | str = "",
        nintpnts: str = "",
        kestress: int | str = "",
        keysym: int | str = "",
        **kwargs,
    ):
        r"""Specifies the characteristics of the user-defined element ``USER300``.

        Mechanical APDL Command: `USRELEM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_USRELEM.html>`_

        Parameters
        ----------
        nnodes : str
            The number of nodes.

        ndim : str
            The number of dimensions (of nodal coordinates). Valid values are 2 or 3.

        keyshape : str
            One of the following element shape options:

            * ``ANYSHAPE`` - Any shape (that is, no specified shape). This value is the default.

            * ``POINT`` - Point.

            * ``LINE`` - Straight line.

            * ``TRIAN`` - Triangle.

            * ``QUAD`` - Quadrilateral. This shape can be degenerated to a triangle.

            * ``TET`` - Tetrahedron.

            * ``BRICK`` - Brick. This shape can be degenerated to a wedge, pyramid, or tetrahedron.

        nreal : str
            The number of real constants.

        nsavevars : str
            The number of saved variables.

        nrsltvar : str
            The number of variables saved in results files.

        keyansmat : int or str
            Key for element formulation control:

            * ``0`` - Create your own material codes within the element formulation. In this case, the real
              constants are available to input material properties. You can also input linear material properties
              via :ref:`mp` and :ref:`mpdata` commands.

            * ``1`` - Use standard material routines or the UserMat subroutine to form structural material data.
              Material properties must be input in the standard way (as you would for non-user-defined elements).
              This value is invalid when KeyShape = ANYSHAPE.

        nintpnts : str
            The maximum number of integration points (used when ``KEYANSMAT`` = 1).

        kestress : int or str
            Key for the element stress state (used when ``KEYANSMAT`` = 1):

            * ``0`` - Plane stress elements.

            * ``1`` - Axisymmetric elements.

            * ``2`` - Plane strain elements.

            * ``3`` - 3D solid elements.

            * ``4`` - 3D solid-shell elements.

            * ``5`` - Generalized plane strain elements.

            * ``6`` - Beam elements.

            * ``7`` - Link/truss elements.

            * ``8`` - 3D shell elements.

            * ``9`` - Axisymmetric shell elements.

        keysym : int or str
            Key for specifying whether element stiffness matrices are symmetric or unsymmetric:

            * ``0`` - Symmetric.

            * ``1`` - Unsymmetric.

        Notes
        -----
        The :ref:`usrelem` command specifies the characteristics of the user-defined element ``USER300``.

        Although you can intersperse other commands as necessary for your analysis, issue the :ref:`usrelem`
        command as part of the following general sequence of commands:

        Issue the :ref:`et` command for element ``USER300``, followed by the related :ref:`type` command.

        Issue both the :ref:`usrelem` and :ref:`usrdof` commands (in either order).

        Define your element using ``USER300``.

        The number of real constants ( ``NREAL`` ) can refer to geometry quantities, material quantities, or
        any parameters for element formulation.

        ANSYS saves variables in the :file:`.esav` file to preserve element data when you specify a positive
        ``NSAVEVARS`` value. When ``KEYANSMAT`` = 0, all variables of both material and kinematic
        formulation are saved. When ``KEYANSMAT`` = 1, only the variables for kinematic formulation (such as
        deformation gradient tensor) are saved; in this case, the material routine saves all necessary
        material data automatically.

        Element data saved in results files ( ``NRSLTVAR`` ) are accessible only as nonsummable
        miscellaneous data. ANSYS saves stress and total strain data for structural elements in the
        :file:`.rst` file automatically (as it does for equivalent variables such as thermal gradient and
        thermal flux in thermal elements); therefore, ``NRSLTVAR`` does not need to include stress and total
        strain data.

        To learn more about creating user-defined elements, see `Creating a New Element
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Hlp_P_UPFNEWEL.html#upfcreateelem2>`_
        """
        command = f"USRELEM,{nnodes},{ndim},{keyshape},{nreal},{nsavevars},{nrsltvar},{keyansmat},{nintpnts},{kestress},{keysym}"
        return self.run(command, **kwargs)

    def wtbcreate(self, iel: str = "", node: str = "", damp: int | str = "", **kwargs):
        r"""Creates a ``USER300`` element to model the turbine for full aeroelastic coupling analysis and
        specifies relevant settings for the analysis.

        Mechanical APDL Command: `WTBCREATE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/None>`_

        Parameters
        ----------
        iel : str
            Element number (next available number by default).

        node : str
            Node number connecting support structure and turbine.

        damp : int or str
            Damping option for the turbine:

            * ``0`` - Damping matrix obtained from the aeroelastic code plus Rayleigh damping (default).

            * ``1`` - Rayleigh damping only.

            * ``2`` - Damping from the aeroelastic code only.

        Notes
        -----

        .. _WTBCREATE_notes:

        :ref:`wtbcreate` invokes a predefined Mechanical APDL macro that automatically generates a turbine
        element
        and issue relevant data commands that are necessary to run a full aeroelastic coupling analysis. For
        detailed information on how to perform a fully coupled aeroelastic analysis, see `Fully Coupled Wind
        Turbine Example in Mechanical APDL
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/advaerorefs.html>`_

        The generated ``USER300`` turbine element will have 9 nodes with node numbers NODE, NMAX+1,
        NMAX+2,..., NMAX+8, where NMAX is the maximum node number currently in the model.

        There are six freedoms on the first node of the element: UX, UY, UZ, ROTX, ROTY, ROTZ, and these are
        true structural freedoms. For all the other nodes (that is, nodes 2 to 9), only the translational
        freedoms (UX, UY, UZ) are used. These are generalized freedoms that are internal to the turbine
        element and are used by the aeroelastic code only.

        The element type integer of the ``USER300`` element is the current maximum element type integer plus
        one.

        The command will also set up the analysis settings appropriate for a full aeroelastic coupling
        analysis. These include full Newton-Raphson solution ( :ref:`nropt`,FULL) and a :ref:`usrcal`
        command to activate the relevant user routines.
        """
        command = f"WTBCREATE,{iel},{node},{damp}"
        return self.run(command, **kwargs)
