# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

class FeSurfaceLoads:

    def sf(
        self,
        nlist: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        meshflag: str = "",
        **kwargs,
    ):
        r"""Defines surface loads on nodes.

        Mechanical APDL Command: `SF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SF.html>`_

        Parameters
        ----------
        nlist : str
            Nodes defining the surface upon which the load is to be applied. Use the label ALL or P, or a
            component name. If ALL, all selected nodes ( :ref:`nsel` ) are used (default). If P, graphical
            picking is enabled and all remaining command fields are ignored (valid only in the GUI).

        lab : str
            Valid surface load label. Load labels are listed under **Surface Loads** in the input table for each element type.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sf1:

            Thermal labels CONV and HFLUX are mutually exclusive.

            .. _sf2:

            For an acoustic analysis, apply the fluid-structure interaction flag (Label = FSI) to only the
            ``FLUID29``, ``FLUID30``, ``FLUID220``, and ``FLUID221`` elements.

        value : str
            Surface load value or table name reference for specifying tabular boundary conditions.

            If ``Lab`` = PRES, ``VALUE`` is the real component of the pressure.

            If ``Lab`` = CONV:

            * ``VALUE`` is typically the film coefficient and ``VALUE2`` (below) is typically the bulk
              temperature. If ``VALUE`` = - ``N``, the film coefficient may be a function of temperature and is
              determined from the HF property table for material ``N`` ( :ref:`mp` ). (See the :ref:`scopt`
              command for a way to override this option and use - ``N`` as the film coefficient.) The
              temperature used to evaluate the film coefficient is usually the average between the bulk and wall
              temperatures, but may be user-defined for some elements.
            * If :ref:`kbc`,0 has been issued for ramped loads, it affects only ``VALUE2``  :ref:`the bulk
              temperature, and the film coefficient specification is unaffected. <SF_V2CONV>`
            * In a viscous-thermal acoustic analysis, if ``Lab`` = CONV, ``VALUE`` is the real part of the heat
              flux and ``VALUE2`` is the imaginary part of the heat flux.

            If ``Lab`` = RAD, ``VALUE`` is surface emissivity.

            If ``Lab`` = PORT, ``VALUE`` is a port number representing a waveguide exterior port. The port
            number must be an integer between 1 and 50. For acoustic 2×2 transfer admittance matrix, the port
            number can be any positive integer. The smaller port number corresponds to the port 1 of the 2×2
            transfer admittance matrix and the greater number corresponds to the port 2. If one port of the
            transfer admittance matrix is connecting to the acoustic-structural interaction interface, the port
            number corresponds to the port 2 of the transfer admittance matrix. A pair of ports of the 2×2
            transfer admittance matrix must be defined in the same element. In an acoustic analysis, the
            positive port number defines a transparent port, through which the reflected sound pressure wave
            propagates to the infinity; the negative port number defines a vibro port that is the structural
            vibration surface.

            If ``Lab`` = SHLD, ``VALUE`` is the surface normal velocity in a harmonic analysis or in a transient
            analysis solved with the velocity potential formulation; ``VALUE`` is the surface normal
            acceleration in a transient analysis solved with the pressure formulation.

            If ``Lab`` = IMPD, ``VALUE`` is resistance in (N)(s)/m :sup:`3` if ``VALUE`` > 0 and is conductance
            in mho if ``VALUE`` < 0 for acoustic or harmonic response analyses. In acoustic transient analyses,
            ``VALUE2`` is not used.

            If ``Lab`` = RDSF, ``VALUE`` is the emissivity value; the following conditions apply: If ``VALUE``
            is between 0 and 1, apply a single value to the surface. If ``VALUE`` = - ``N``, the emissivity may
            be a function of the temperature, and is determined from the EMISS property table for material ``N``
            ( :ref:`mp` ). The material ``N`` does not need to correlate with the underlying solid thermal
            elements.

            If ``Lab`` = FSIN in a one-way structure-to-acoustic coupling, ``VALUE`` is the surface interface
            number.

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL to CFX analysis, ``VALUE`` is not used.

            If ``Lab`` = ATTN, ``VALUE`` is the absorption coefficient of the surface.

            If ``Lab`` = VIMP, ``VALUE`` is resistance of viscous impedance in (N)(s)/m :sup:`3`.

            If ``Lab`` = TIMP, ``VALUE`` is resistance of thermal impedance in (N)(s)/m :sup:`3`.

            If ``Lab`` = PERM, ``VALUE`` is permeability in m :sup:`2`.

        value2 : str
            Second surface load value (if any).

            If ``Lab`` = PRES, this value is the imaginary pressure component, used by the following supported elements:

            * Surface elements: ``SURF153``, ``SURF154`` and ``SURF159``.

            * Solid and solid-shell elements: ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``,
              ``SOLID187``, ``SOLSH190``, and ``SOLID285``.

            * Shell elements: ``SHELL181``, ``SHELL281``, ``SHELL208``, and ``SHELL209``.

            * Coupled-field elements with structural degrees of freedom: ``PLANE222``, ``PLANE223``,
              ``SOLID225``, ``SOLID226``, and ``SOLID227``.

            Supported analysis types in this case are:

            * Full harmonic ( :ref:`hropt`,FULL)

            * Mode-superposition harmonic ( :ref:`hropt`,MSUP), if the mode-extraction method is Block Lanczos (
              :ref:`modopt` ,LANB), PCG Lanczos ( :ref:`modopt`,LANPCG), Supernode ( :ref:`modopt`,SNODE),
              Subspace ( :ref:`modopt`,SUBSP), or Unsymmetric ( :ref:`modopt`,UNSYM)

            If ``Lab`` = CONV:

            * ``VALUE2`` is the bulk temperature for thermal analyses.
            * If :ref:`kbc`,0 has been issued for ramped loads, the bulk temperature is ramped from the value
              defined by :ref:`tunif` to the value specified by ``VALUE2`` for the first loadstep. If
              :ref:`tabular boundary conditions are defined, the <SF_tabBC>` :ref:`kbc` command is ignored and
              tabular values are used.
            * For viscous-thermal acoustics ``VALUE2`` is the imaginary part of heat flux.

            If ``Lab`` = RAD, ``VALUE2`` is the ambient temperature.

            If ``Lab`` = SHLD, ``VALUE2`` is the phase angle of the normal surface velocity (defaults to zero)
            for harmonic response analyses while ``VALUE2`` is not used for transient analyses in acoustics.

            If ``Lab`` = IMPD, ``VALUE2`` is reactance in (N)(s)/m :sup:`3` if ``VALUE`` > 0 and is the product
            of susceptance and angular frequency if ``VALUE`` < 0 for acoustics.

            If ``Lab`` = RDSF, ``VALUE2`` is the enclosure number. Radiation will occur between surfaces flagged
            with the same enclosure numbers. If the enclosure is open, radiation will also occur to ambient. If
            ``VALUE2`` is negative radiation direction is reversed and will occur inside the element for the
            flagged radiation surfaces.

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL to CFX analysis, ``VALUE2`` is the surface interface
            number (not available from within the GUI).

            If ``Lab`` = PORT, ``VALUE2`` is not used.

            If ``Lab`` = ATTN, ``VALUE2`` is the transmission loss (dB) of the coupled wall in an energy
            diffusion solution for room acoustics.

            If ``Lab`` = VIMP, ``VALUE2`` is reactance of viscous impedance in (N)(s)/m :sup:`3`.

            If ``Lab`` = TIMP, ``VALUE2`` is reactance of thermal impedance in (N)(s)/m :sup:`3`.

        meshflag : str
            Specifies how to apply normal pressure loading on the mesh. Valid in a `nonlinear adaptivity
            analysis <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVREZ.html>`_
            when ``Lab`` = PRES and ``Nlist`` is a nodal component defined prior to any remeshing activity.

            0 - Pressure loading occurs on the current mesh (default).

            1 - Pressure loading occurs on the initial mesh for nonlinear adaptivity.

        Notes
        -----

        .. _SF_notes:

        Individual nodes cannot be entered for this command. The node list is to identify a surface and the
        ``Nlist`` field must contain a sufficient number of nodes to define an element surface. The loads
        are internally stored on element faces defined by the specified nodes. All nodes on an element face
        (including midside nodes, if any) must be specified for the face to be used, and the element must be
        selected.

        If all nodes defining a face are shared by an adjacent face of another selected element, the face is
        not free and will not have a load applied. If more than one element can share the same nodes (for
        example, a surface element attached to a solid element), select the desired element type before
        issuing the :ref:`sf` command. The :ref:`sf` command applies only to area and volume elements.

        For shell elements, if the specified nodes include face one (which is usually the bottom face) along
        with other faces (such as edges), only face one is used. Where faces cannot be uniquely determined
        from the nodes, or where the face does not fully describe the load application, issue :ref:`sfe`
        instead of :ref:`sf`. A load key of 1 (which is typically the first loading condition on the first
        face) is used if the face determination is not unique. A uniform load value is applied over the
        element face.

        You can use these related surface-load commands with :ref:`sf` :

        * :ref:`sfe` - Defines surface loads on elements. You can also use it to apply tapered loads on
          individual element faces.
        * :ref:`sfbeam` - Applies surface loads to beam elements.
        * :ref:`sfcontrol` - Applies general (normal, tangential, and other) surface loads to `supported
          structural elements
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SFCONTROL.html#>`_.
        * :ref:`sfcum` - Accumulates (adds) surface loads applied via :ref:`sf`.
        * :ref:`sfdele` - Delete loads applied via :ref:`sf`.
        * :ref:`sffun` - Applies loads from a node-vs.-value function.
        * :ref:`sfgrad` - Applies an alternate tapered load.

        Tabular boundary conditions Tabular boundary conditions ( ``VALUE`` = ``tabname`` and/or ``VALUE2``
        = ``tabname``) are available
        for the following surface load labels ( ``Lab`` ) only: PRES (real and/or imaginary components),
        CONV (film coefficient and/or bulk temperature; or heat flux for viscous-thermal acoustics), HFLUX,
        DFLUX (diffusion flux), RAD (surface emissivity and ambient temperature), IMPD (resistance and
        reactance), SHLD (normal velocity and phase or acceleration), ATTN ( absorption coefficient or
        transmission loss ), VIMP (viscous impedance), and TIMP (thermal impedance). Issue :ref:`dim` to
        define a table.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in the PREP7 and :ref:`slashmap` processors.

        .. _SF_prodres:

        Ansys Mechanical Enterprise :ref:`sf`,FSI and :ref:`sf`,FSIN are available only in the Ansys
        Mechanical Enterprise family of products (Ansys Mechanical Enterprise,
        Ansys Mechanical Enterprise PrepPost, and Ansys Mechanical Enterprise Solver).
        """
        command = f"SF,{nlist},{lab},{value},{value2},,{meshflag}"
        return self.run(command, **kwargs)

    def sfbeam(
        self,
        elem: str = "",
        lkey: str = "",
        lab: str = "",
        vali: str = "",
        valj: str = "",
        val2i: str = "",
        val2j: str = "",
        ioffst: str = "",
        joffst: str = "",
        lenrat: int | str = "",
        **kwargs,
    ):
        r"""Specifies surface loads on beam and pipe elements.

        Mechanical APDL Command: `SFBEAM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFBEAM.html>`_

        Parameters
        ----------
        elem : str
            Element to which surface load is applied. If ALL, apply load to all selected beam elements (
            :ref:`esel` ). If ``Elem`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted in ``Elem``.

        lkey : str
            Load key associated with surface load (defaults to 1). Load keys (1, 2, 3, etc.) are listed
            under "Surface Loads" in the input table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. For beam
            and some pipe elements, the load key defines the load orientation.

        lab : str
            Valid surface load label. Load labels are listed under "Surface Loads" in the input table for
            each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.
            Structural labels: PRES (pressure).

        vali : str
            Surface load values at nodes I and J. If ``VALJ`` is blank, it defaults to ``VALI``. If ``VALJ``
            is zero, a zero is used.

        valj : str
            Surface load values at nodes I and J. If ``VALJ`` is blank, it defaults to ``VALI``. If ``VALJ``
            is zero, a zero is used.

        val2i : str
            Second surface load values at nodes I and J. Currently not used.

        val2j : str
            Second surface load values at nodes I and J. Currently not used.

        ioffst : str
            Offset distance from node I (toward node J) where ``VALI`` is applied, and offset distance from
            node J (toward node I) where ``VALJ`` is applied, respectively.

        joffst : str
            Offset distance from node I (toward node J) where ``VALI`` is applied, and offset distance from
            node J (toward node I) where ``VALJ`` is applied, respectively.

        lenrat : int or str
            Offset distance flag:

            * ``0`` - Offset is in terms of length units (default).

            * ``1`` - Offset is in terms of a length ratio (0.0 to 1.0).

        Notes
        -----

        .. _SFBEAM_notes:

        Specifies surface loads on the selected beam elements. Distributed loads are applied on a force-per-
        length basis (that is, the width of the underlying element is not considered). To list and delete
        surface loads applied with this command, use the :ref:`sfelist` and :ref:`sfedele` commands,
        respectively.

        If no offset values ( ``IOFFSET`` and ``JOFFSET`` ) are specified, the load is applied over the full
        element length. Values may also be input as length fractions, depending on the ``LENRAT`` setting.
        For example, assuming a line length of 5.0, an ``IOFFST`` of 2.0 with ``LENRAT`` = 0 or an
        ``IOFFST`` of 0.4 with ``LENRAT`` = 1 represent the same point. If ``JOFFST`` = -1, ``VALI`` is
        assumed to be a point load at the location specified via ``IOFFST``, and ``VALJ`` is ignored. (
        ``IOFFSET`` cannot be equal to -1.) The offset values are stepped even if you issue a :ref:`kbc`,0
        command.

        Offsets are only available for element types ``BEAM188`` and ``PIPE288`` if using the cubic shape
        function (KEYOPT(3) = 3) for those element types.

        To accumulate (add) surface loads applied with this command, use the :ref:`sfcum`,,ADD command. Use
        the same offset values used on the previous :ref:`sfbeam` command (for a given element face);
        otherwise, the loads do not accumulate. If no offsets are specified, the command applies the
        previous offset values.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"SFBEAM,{elem},{lkey},{lab},{vali},{valj},{val2i},{val2j},{ioffst},{joffst},{lenrat}"
        return self.run(command, **kwargs)

    def sfcontrol(
        self,
        kcsys: str = "",
        lcomp: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        ktaper: str = "",
        kuse: str = "",
        karea: str = "",
        kproj: str = "",
        kfollow: str = "",
        **kwargs,
    ):
        r"""Defines structural surface-load properties on selected elements and nodes for subsequent loading
        commands.

        Mechanical APDL Command: `SFCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFCONTROL.html>`_

        Parameters
        ----------
        kcsys : str
            Specifies how the load direction is determined:

            * 0 (or blank) - Use the coordinate system of an element face. A local coordinate system is
              projected onto the face, if defined ( ``VAL1`` ) (default).
            * 1 - Use a local coordinate system. A local coordinate system must be defined and is not projected
              onto the face.
            * 2 - Use a custom (user-defined) vector in the global Cartesian coordinate system.

        lcomp : str
            Load-component definition when ``KCSYS`` = 0 or 1. The following table shows how the component
            (or primary direction) is determined :ref:`based on the coordinate system: <SFCONTROL_fig1>`

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        val1 : str
            **When** ``KCSYS`` = 0:

            * ``VAL1`` - Determines the first tangential axis (x axis). Not valid for the edges of 3D shell or
              2D elements.
            * 0 - Aligns the x axis to the first parametric direction :math:`equation not available`  (default).
            * 1 - Aligns x axis to the second parametric direction :math:`equation not available`.
            * >10 - ID of the local coordinate system. The local coordinate system is projected to selected face
              of the element.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Rotation angle of a tangential load (optional). Not valid for the edges of 3D shell or
              2D elements. If this value is specified, the tangential load rotates further with respect to the
              surface normal. The load component ( ``LCOMP`` ) becomes the reference axis to rotate.

            **When** ``KCSYS`` = 1:

            * ``VAL1`` - ID of the local coordinate system for the load. The axes of the local coordinate system
              are fixed in the global cartesian coordinate system.
            * ``VAL2`` - Not used.
            * ``VAL3`` - Not used.
             **When** ``KCSYS`` = 2:

            * ``VAL1``, ``VAL2``, ``VAL3`` - The X / Y / Z components, respectively, of the direction vector in
              the global Cartesian coordinate system.

        val2 : str
            **When** ``KCSYS`` = 0:

            * ``VAL1`` - Determines the first tangential axis (x axis). Not valid for the edges of 3D shell or
              2D elements.
            * 0 - Aligns the x axis to the first parametric direction :math:`equation not available`  (default).
            * 1 - Aligns x axis to the second parametric direction :math:`equation not available`.
            * >10 - ID of the local coordinate system. The local coordinate system is projected to selected face
              of the element.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Rotation angle of a tangential load (optional). Not valid for the edges of 3D shell or
              2D elements. If this value is specified, the tangential load rotates further with respect to the
              surface normal. The load component ( ``LCOMP`` ) becomes the reference axis to rotate.

            **When** ``KCSYS`` = 1:

            * ``VAL1`` - ID of the local coordinate system for the load. The axes of the local coordinate system
              are fixed in the global cartesian coordinate system.
            * ``VAL2`` - Not used.
            * ``VAL3`` - Not used.
             **When** ``KCSYS`` = 2:

            * ``VAL1``, ``VAL2``, ``VAL3`` - The X / Y / Z components, respectively, of the direction vector in
              the global Cartesian coordinate system.

        val3 : str
            **When** ``KCSYS`` = 0:

            * ``VAL1`` - Determines the first tangential axis (x axis). Not valid for the edges of 3D shell or
              2D elements.
            * 0 - Aligns the x axis to the first parametric direction :math:`equation not available`  (default).
            * 1 - Aligns x axis to the second parametric direction :math:`equation not available`.
            * >10 - ID of the local coordinate system. The local coordinate system is projected to selected face
              of the element.

            * ``VAL2`` - Not used.

            * ``VAL3`` - Rotation angle of a tangential load (optional). Not valid for the edges of 3D shell or
              2D elements. If this value is specified, the tangential load rotates further with respect to the
              surface normal. The load component ( ``LCOMP`` ) becomes the reference axis to rotate.

            **When** ``KCSYS`` = 1:

            * ``VAL1`` - ID of the local coordinate system for the load. The axes of the local coordinate system
              are fixed in the global cartesian coordinate system.
            * ``VAL2`` - Not used.
            * ``VAL3`` - Not used.
             **When** ``KCSYS`` = 2:

            * ``VAL1``, ``VAL2``, ``VAL3`` - The X / Y / Z components, respectively, of the direction vector in
              the global Cartesian coordinate system.

        ktaper : str
            Global tapered load behavior (valid for :ref:`sfe` only):

            * 0 - Load does not vary (default).
            * 1 - Load varies with respect to the current element locations. The magnitude changes with respect
              to the element deformation.
            * 2 - Load varies with respect to the initial element locations. The load magnitude for each element
              remains constant throughout the solution..

            For more information, see :ref:`globaltaperedloads`.

        kuse : str
            Load direction with respect to the surface normal of the selected face:

            * 0 - Use the load as calculated (default).
            * 1 - Use a positive load only (negative set to zero, valid for ``LCOMP`` = 0 and ``KCSYS`` = 0).
            * 2 - Use a negative load only (positive set to zero, valid for ``LCOMP`` = 0 and ``KCSYS`` = 0).
            * 3 - Applied load is not used if the surface normal is oriented in the same general direction as
              the user-defined vector. Valid for ``KCSYS`` = 2 only.

        karea : str
            Loaded area during large deformation:

            * 0 - Use the current (deformed) area (default).
            * 1 - Use the initial area.

        kproj : str
            Vector-oriented load ( ``KCSYS`` = 2) behavior:

            * 0 - Apply the load on the full area and include the tangential component (default).
            * 1 - Apply the load on the projected area and include the tangential component.
            * 2 - Apply the load on the projected area and exclude the tangential component.

        kfollow : str
            Controls follower-load behavior. Valid when ``KCSYS`` = 1 or 2, or when ``KCSYS`` = 0 and ``VAL1`` >
            10.

            * 0 - The load maintains a fixed direction (default).
            * 1 -The load follows the element deformation.

            For more information, see :ref:`scfofollowloadbehav`.

        Notes
        -----

        .. _SFCONTROL_notes:

        :ref:`sfcontrol` defines the properties of structural distributed loads for all subsequent :ref:`sf`
        or :ref:`sfe` loading commands. ( :ref:`sfa` and :ref:`sfl` are not supported.)

        The command does not support analyses in which remeshing occurs, such as nonlinear mesh adaptivity
        and 2D to 3D analysis.

        To update a load property or properties, reissue :ref:`sfcontrol` with the new option(s) before
        issuing further :ref:`sf` or :ref:`sfe` commands.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        To list the current set of control data, issue :ref:`sfcontrol`,STAT.

        To reset all input values to defaults, issue :ref:`sfcontrol`,NONE.

        When ``KCSYS`` = 0, the positive normal load acts in the negative surface normal (- ``z`` )
        direction. The positive tangential loads act in the positive coordinate direction. A user-defined
        coordinate system ( ``VAL1`` ) is ignored if the load is applied on an edge of a plane element (
        ``PLANE182``, ``PLANE183``, ``SHELL208``, ``SHELL209``, ``PLANE222``, and ``PLANE223`` ).

        When ``KCSYS`` = 1, the loading direction follows the positive direction of the local coordinate
        system. The ID of a local coordinate system ( ``VAL1`` ) is required.

        The following figure shows how the coordinate directions are determined on a face of a solid or
        shell element with different ``KCSYS`` and ``VAL1`` input:

        Coordinate System for Load Application on the Faces of 3D Solid and Shell Elements
        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        * where:
        * z, x :sub:`1`, y :sub:`1` : normal and tangential directions (default surface coordinate system)
        * z, x :sub:`2`, y :sub:`2` : normal and user-defined tangential directions (user-defined surface
          coordinate system)
        * x :sub:`3`, y :sub:`3`, z :sub:`3` : x, y, and z directions defined by the local coordinate system
          when ``KCSYS`` = 1

        **When** ``KCSYS`` = 0:

        * The parametric direction determines the default coordinate system on a face. By default, the first
          parametric direction ( :math:`equation not available` ) becomes the first tangential direction (x
          direction). If           ``VAL1`` = 1, the second parametric direction ( :math:`equation not
          available` ) is selected as the x direction.
        * For the projected local coordinate system ( ``VAL1`` > 10), the direction of the first tangential
          axes (x :sub:`2` ) is determined by the projection of the local coordinate system onto the face.
          The projected tangential axes may rotate if the direction of the face normal (z) changes in the
          space during solution. If the direction of the face normal (z) is fixed (for in-plane rotation,
          for example), the tangential axes do not follow element deformation. To enable your coordinate
          system to always follow the element deformation, specify the follower option ( ``KFOLLOW`` ).
        * **Coordinate System vs. Load Direction**
        * For the loads defined in the default coordinate system ( ``KCSYS`` = 0), the tangential direction
          of a load is restricted because it is aligned to the direction of the axis ( ``LCOMP`` ). The load
          direction can be arbitrary by adding additional rotation to the load ( ``VAL3`` ). The following
          figure shows how the load direction is determined on the face of an element. If ``VAL3`` > 0,
          ``LCOMP`` becomes the reference axis to define the rotation.

        Load Direction in the Default Coordinate System
        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        **When** ``KCSYS`` = 1:

        * The positive direction of the x :sub:`3`, y :sub:`3`, and z :sub:`3` axes follow the direction of
          the local coordinate system without adjustment. Therefore, they do not follow element deformation.

        **When** ``KCSYS`` = 2:

        * The loading direction follows the positive direction of the orientation vector, defined via
          ``VAL1``, ``VAL2``, and ``VAL3``. The direction is calculated as :math:`equation not available`,
          where  :math:`equation not available`,  :math:`equation not available`, and  :math:`equation not
          available`  are unit vectors in the global Cartesian coordinate system. The loading
          direction is fixed and does not follow the deformation of a face of a selected element.
        * You can adjust the load magnitude ( ``KUSE`` and ``KPROJ`` ).
        * Use the follower option ( ``KFOLLOW`` ) to specify whether the load has a fixed direction (
          ``KCSYS`` = 1 or 2), or projects the local coordinate system to the element face to follow element
          deformation ( ``KCSYS`` = 0 and ``VAL1`` > 10).

        The following figure shows the default direction of the normal (z) and tangential (x) components on
        an edge of a 3D shell element ( ``SHELL181`` or ``SHELL281`` ).

        Default Coordinate System of Surface Load on the Edge of a 3D Shell Element
        If a local coordinate system is defined and ``KCSYS`` = 0 for the edge of the 3D shell element, the
        tangential directions are adjusted in the plane of the edge.

        Projected Coordinate System of Surface Load on the Edge of a 3D Shell Element
        The following figure shows the positive direction of the loads on the edge of a plane element when
        ``KCSYS`` = 0. The positive direction of the tangential load is defined by the definition of the
        faces (J-I, K-J, L-K, I-L).

        Positive Tangential Load on the Edge of a Plane Element
        If ``KCSYS`` = 1 or 2, the load direction does not change and ``KUSE`` = 1 or 2 is ignored.

        If ``KCSYS`` = 1 or 2, or ``KTAPER`` > 0, you cannot specify a gradient (slope) for surface loads (
        :ref:`sfgrad` ) or a varying surface load ( :ref:`sffun` ).

        This command is also valid in the PREP7 processor.

        .. _globaltaperedloads:

        If ``KTAPER`` = 1, the magnitude of the load is determined by the current location of a point:

        .. math::

            equation not available

        * where:
        * :math:`equation not available`  : Values on  :ref:`sfe` ( ``VAL1`` ~ ``VAL4`` )
        * :math:`equation not available`  : Global Cartesian coordinates at the current location of the
          point.

        If ``KTAPER`` = 2, the magnitude of the load is determined by the initial location of a point:

        .. math::

            equation not available

        * where:
        * :math:`equation not available`  : Values on  :ref:`sfe` ( ``VAL1`` ~ ``VAL4`` )
        * :math:`equation not available`  : Global Cartesian coordinates at the initial location of the
          point.

        ``KTAPER`` is not valid for use with :ref:`sf`.

        .. _scfofollowloadbehav:

        The follower option ( ``KFOLLOW`` ) determines whether the load maintains a fixed direction
        (default) or follows element deformation. The option applies to surface loads defined by a fixed
        direction ( ``KCSYS`` = 1 or 2) or by a projected user-defined coordinate system ( ``KCSYS`` = 0 and
        ``VAL1`` > 10).

        **When** ``KCSYS`` = 0 and ``VAL1`` > 10:

        The selected local coordinate system is projected onto the face at the initial state, then the
        projected tangential component ( ``LCOMP`` ) is attached to the orthonormal basis ( **e** :sub:`1`,
        **e** :sub:`2`, **e** :sub:`3` ) of the face. The orthonormal basis may or may not be coincident to
        the :math:`equation not available`  coordinate system. During solution, the basis is updated at the
        current        time step and the load direction is updated with respect to the basis.

        Follower Load Behavior in the Projected Coordinate System
        **When** ``KCSYS`` = 1 or 2:

        The global direction vector is attached to the orthonormal basis of selected face at the initial
        state. When ``KCSYS`` = 1, the direction of selected axis is considered as the direction vector and
        attached to the basis. During solution, the basis is updated at current time step and the load
        direction is updated with respect to the basis.

        Follower Load Behavior for a User-Defined Orientation
        **Follower loads on the edges of 3D shell and 2D elements:**

        The load is attached to the basis defined on the edge ( **e** :sub:`t`, **e** :sub:`ne`, **e**
        :sub:`nf` [tangential, edge-normal, and face-normal vector, respectively]). For 2D solid elements,
        the face-normal orientation ( **e** :sub:`nf` ) is that of the global Z axis. For 2D shell elements,
        the edge-normal ( **e** :sub:`ne` ) is that of the global Z axis.

        Follower Load Behavior on the Edges of 3D Shell and 2D Elements
        If it is necessary to use the follower option after the first load step or at the restart analysis,
        define the load direction with respect to the current geometry (that is, the current basis of an
        element face). The follower option for the local coordinate system ( ``KCSYS`` = 1) is not allowed
        after the first load step or at the restart analysis.

        Load-stiffness effects are included in the supported elements for the real part of all loads at the
        current configuration. All other load properties are included in the load vector of the elements.

        You can specify an unsymmetric matrix ( :ref:`nropt`,UNSYM) for the load-stiffness effects if
        needed.
        """
        command = f"SFCONTROL,{kcsys},{lcomp},{val1},{val2},{val3},{ktaper},{kuse},{karea},{kproj},{kfollow}"
        return self.run(command, **kwargs)

    def sfcum(
        self, lab: str = "", oper: str = "", fact: str = "", fact2: str = "", **kwargs
    ):
        r"""Specifies that surface loads are to be accumulated.

        Mechanical APDL Command: `SFCUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFCUM.html>`_

        Parameters
        ----------
        lab : str
            Valid surface load label. If ALL, use all appropriate labels.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sfcum1:

            Thermal labels CONV and HFLUX are mutually exclusive.

        oper : str
            Accumulation key:

            * ``REPL`` - Subsequent values replace the previous values (default).

            * ``ADD`` - Subsequent values are added to the previous values.

            * ``IGNO`` - Subsequent values are ignored.

        fact : str
            Scale factor for the first surface load value. A (blank) or '0' entry defaults to 1.0.

        fact2 : str
            Scale factor for the second surface load value. A (blank) or '0' entry defaults to 1.0.

        Notes
        -----

        .. _SFCUM_notes:

        Allows repeated surface loads (pressure, convection, etc.) to be replaced, added, or ignored.
        Surface loads are applied with the :ref:`sf`, :ref:`sfe`, and :ref:`sfbeam` commands. Issue the
        :ref:`sfelist` command to list the surface loads. The operations occur when the next surface load
        specifications are defined. For example, issuing the :ref:`sf` command with a pressure value of 25
        after a previous :ref:`sf` command with a pressure value of 20 causes the current value of that
        pressure to be 45 with the add operation, 25 with the replace operation, or 20 with the ignore
        operation. All new pressures applied with :ref:`sf` after the ignore operation will be ignored, even
        if no current pressure exists on that surface.

        Scale factors are also available to multiply the next value before the add or replace operation. A
        scale factor of 2.0 with the previous "add" example results in a pressure of 70. Scale factors are
        applied even if no previous values exist. Issue :ref:`sfcum`,STAT to show the current label,
        operation, and scale factors. Solid model boundary conditions are not affected by this command, but
        boundary conditions on the FE model are affected.

        The FE boundary conditions may still be overwritten by existing solid model boundary conditions if a
        subsequent boundary condition transfer occurs.

        :ref:`sfcum` does not work for tabular boundary conditions.

        This command is also valid in PREP7.
        """
        command = f"SFCUM,{lab},{oper},{fact},{fact2}"
        return self.run(command, **kwargs)

    def sfdele(self, nlist: str = "", lab: str = "", **kwargs):
        r"""Deletes surface loads.

        Mechanical APDL Command: `SFDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFDELE.html>`_

        Parameters
        ----------
        nlist : str
            Label defining where to find the list of nodes:

            * ``ALL`` - Use all selected nodes ( :ref:`nsel` ). A component label may be substituted for
              ``Nlist``.

        lab : str
            Valid surface load label. If ALL, use all appropriate labels. See the :ref:`sf` command for
            labels.

        Notes
        -----

        .. _SFDELE_notes:

        Deletes surface loads as applied via :ref:`sf`. Loads are deleted only for the specified nodes on
        external faces of selected area and volume elements. For shell elements, if the specified nodes
        include face one (which is usually the bottom face) along with other faces (such as edges), only the
        loads on face one will be deleted. The element faces are determined from the list of selected nodes
        as described for :ref:`sf`. Issue :ref:`sfedele` to delete loads explicitly by element faces.

        This command is also valid in PREP7.
        """
        command = f"SFDELE,{nlist},{lab}"
        return self.run(command, **kwargs)

    def sfe(
        self,
        elem: str = "",
        lkey: str = "",
        lab: str = "",
        kval: int | str = "",
        value1: str = "",
        value2: str = "",
        value3: str = "",
        value4: str = "",
        meshflag: str = "",
        **kwargs,
    ):
        r"""Defines surface loads on elements.

        Mechanical APDL Command: `SFE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFE.html>`_

        Parameters
        ----------
        elem : str
            Element to which surface load applies. If ALL, apply load to all selected elements ( :ref:`esel`
            ). If ``Elem`` = P, graphical picking is enabled and all remaining command fields are ignored
            (valid only in the GUI). A component name may be substituted for ``Elem``.

        lkey : str
            Load key or face number associated with surface load (defaults to 1). Load keys (1,2,3, etc.)
            are listed under "Surface Loads" in the input data table for each element type in the `Element
            Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

            If you issue :ref:`sfcontrol` before :ref:`sfe`, ``LKEY`` is the face number for `supported
            structural solid and shell elements
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SFCONTROL.html#>`_.

        lab : str
            Valid surface load label. Load labels are listed under "Surface Loads" in the input table for
            each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

            .. _sfe1:

            Thermal labels CONV and HFLUX are mutually exclusive.

            .. _sfe2:

            For an acoustic analysis, apply the fluid-structure interaction flag (Label = FSI) to only the
            ``FLUID29``, ``FLUID30``, ``FLUID220``, and ``FLUID221`` elements.

            .. _sfe4:

            When a load vector exists for a thermal superelement, it must be applied and have a scale factor
            of 1 ( :ref:`sfe`,,,SELV,,1).

        kval : int or str
            Value key. If ``Lab`` = PRES:

            * ``0 or 1`` - ``VALUE1`` through ``VALUE4`` are used as real components of pressures.

            * ``2`` - ``VALUE1`` through ``VALUE4`` are used as imaginary components of pressures.

            Value key. If ``Lab`` = CONV:

            * ``0 or 1`` - For thermal analyses, ``VALUE1`` through ``VALUE4`` are used as the film
              coefficients.

            * ``2`` - For thermal analyses, ``VALUE1`` through ``VALUE4`` are the bulk temperatures.

            * ``3`` - ``VALUE1`` through ``VALUE4`` are used as film effectiveness.

            * ``4`` - ``VALUE1`` through ``VALUE4`` are used as free stream temperature.

            Value key. If ``Lab`` = RAD:

            * ``0 or 1`` - ``VALUE1`` through ``VALUE4`` are used as the emissivities.

            * ``2`` - ``VALUE1`` through ``VALUE4`` are ambient temperatures.

            Value key. If ``Lab`` = RDSF:

            * ``0 or 1`` - ``VALUE1`` is the emissivity value between 0 and 1.

            * ``2`` - ``VALUE1`` is the enclosure number.

            Value key. If ``Lab`` = IMPD:

            * ``0 or 1`` - For acoustic harmonic analyses, VALUE1 through VALUE4 are used as the real part of
              the impedance.

            * ``2`` - For acoustic harmonic analyses, VALUE1 through VALUE4 are used as the imaginary part of
              the impedance.

            Value key. If ``Lab`` = SHLD:

            * ``0 or 1`` - For acoustic analyses, ``VALUE1`` through ``VALUE4`` are used as the normal velocity
              (harmonic) or normal acceleration (transient).

            * ``2`` - For acoustic analyses, ``VALUE1`` through ``VALUE4`` are used as the phase angle for
              harmonic response analyses.

            Value key. If ``Lab`` = ATTN:

            * ``0 or 1`` - For acoustic analyses, ``VALUE1`` through ``VALUE4`` are used as the absorption
              coefficient of the surface.

            * ``2`` - For acoustic analyses, ``VALUE1`` through ``VALUE4`` are used as the transmission loss
              (dB) of the coupled wall in an energy diffusion solution for room acoustics.

            Value key. If ``Lab`` = SELV:

            * ``0 or 1`` - ``VALUE1`` is the multiplier on real load vector ``LKEY``.

            * ``2`` - ``VALUE1`` is the multiplier on imaginary load vector ``LKEY``.

            If only one set of data is supplied, the other set of data defaults to previously specified values
            (or zero if not previously specified) in the all of the following cases:

            * Emissivities are supplied and ``Lab`` = RAD

            * Temperatures are supplied and ``Lab`` = RAD

            * Temperatures are supplied and ``Lab`` = CONV

            * Film coefficients are supplied and ``Lab`` = CONV

            * Normal velocity/acceleration for acoustics is supplied and ``Lab`` = SHLD

            * Phase angle for acoustics is supplied and ``Lab`` = SHLD

        value1 : str
            First surface load value (typically at the first node of the face), or the name of a table for
            specifying tabular boundary conditions.

            Face nodes are listed in the order given for **Surface Loads** in the input data table for each element type in the `Element Reference <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. For example, for ``SOLID185``, the item 1-JILK associates ``LKEY`` = 1 (face 1) with nodes J, I, L, and K. Surface load value ``VALUE1`` then applies to node J of face 1. To specify a table, enclose the table name in percent signs (%), for example, ``tabname``. Use the :ref:`dim` command to define a table. Only one table can be specified, and it must be specified in the ``VALUE1`` position; tables specified in the ``VALUE2``, ``VALUE3``, or ``VALUE4`` positions are ignored. ``VALUE2`` applies to node I, etc.

            If ``Lab`` = PRES and ``KVAL`` = 2, this value is the imaginary pressure component, used by the following supported elements:

            * Surface elements: ``SURF153``, ``SURF154`` and ``SURF159``.

            * Solid and solid-shell elements: ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``,
              ``SOLID187``, ``SOLSH190``, and ``SOLID285``.

            * Shell elements: ``SHELL181``, ``SHELL281``, ``SHELL208``, and ``SHELL209``.

            * Coupled-field elements with structural degrees of freedom: ``PLANE222``, ``PLANE223``,
              ``SOLID225``, ``SOLID226``, and ``SOLID227``.

            If ``Lab`` = CONV, ``KVAL`` = 0 or 1, and ``VALUE1`` = - ``N``, the film coefficient is assumed to
            be a function of temperature and is determined from the HF property table for material ``N`` (
            :ref:`mp` ). (See the :ref:`scopt` command for a way to override this option and use - ``N`` as the
            film coefficient.) The temperature used to evaluate the film coefficient is usually the average
            between the bulk and wall temperatures, but may be user-defined for some elements.

            If ``Lab`` = CONV, ``KVAL`` = 2, ``VALUE1`` specifies the bulk temperature. If :ref:`kbc`,0 has been
            issued for ramped loads, the bulk temperature is ramped from the value defined by :ref:`tunif` to
            that specified on ``VALUE1`` (for the first loadstep). If a table name is specified for ``VALUE1``,
            the :ref:`kbc` command is ignored and tabular values are used.

            If ``Lab`` = PORT, ``VALUE1`` is a port number representing a waveguide port. The port number must
            be an integer between 1 and 50. For an acoustic 2×2 transfer admittance matrix, the port number can
            be any positive integer. The smaller port number corresponds to port 1 of the 2×2 transfer
            admittance matrix, and the greater port number corresponds to port 2. If one port of the transfer
            admittance matrix is connecting to the acoustic-structural interaction interface, the port number
            corresponds to port 2 of the transfer admittance matrix. A pair of ports of the 2×2 transfer
            admittance matrix must be defined in the same element.

            If ``Lab`` = RDSF, ``KVAL`` = 0 or 1, and ``VALUE1`` = - ``N``, the emissivity is assumed to be a
            function of the temperature, and is determined from the EMISS property table for material ``N`` (
            :ref:`mp` ). The material ``N`` does not need to correlate with the underlying solid thermal
            elements. If ``Lab`` = RDSF, ``KVAL`` = 2, and ``VALUE1`` is negative, radiation direction is
            reversed and will occur inside the element for the flagged radiation surfaces.

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL-to-CFX analysis, ``VALUE1`` is not used.

            If ``Lab`` = SELV, ``VALUE1`` represents the scale factor (default = 0.0).

            If ``Lab`` = ATTN, ``VALUE1`` is the absorption coefficient.

        value2 : str
            Surface load values at the second, third, and fourth nodes (if any) of the face.

            If all three values are blank, all default to ``VALUE1``, giving a constant load. Zero or other
            blank values are used as zero.

            If ``VALUE2``, ``VALUE3``, or ``VALUE4`` are magnitudes of the load, they are ignored if
            ``VALUE1`` is a table. If ``VALUE2``, ``VALUE3``, or ``VALUE4`` are any other values, they are
            used even if ``VALUE1`` is a table (for example, the load direction for face 5 of ``SURF154`` ).

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL-to-CFX analysis, ``VALUE2`` is the surface
            interface number (not available in the GUI). ``VALUE3`` and ``VALUE4`` are not used.

        value3 : str
            Surface load values at the second, third, and fourth nodes (if any) of the face.

            If all three values are blank, all default to ``VALUE1``, giving a constant load. Zero or other
            blank values are used as zero.

            If ``VALUE2``, ``VALUE3``, or ``VALUE4`` are magnitudes of the load, they are ignored if
            ``VALUE1`` is a table. If ``VALUE2``, ``VALUE3``, or ``VALUE4`` are any other values, they are
            used even if ``VALUE1`` is a table (for example, the load direction for face 5 of ``SURF154`` ).

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL-to-CFX analysis, ``VALUE2`` is the surface
            interface number (not available in the GUI). ``VALUE3`` and ``VALUE4`` are not used.

        value4 : str
            Surface load values at the second, third, and fourth nodes (if any) of the face.

            If all three values are blank, all default to ``VALUE1``, giving a constant load. Zero or other
            blank values are used as zero.

            If ``VALUE2``, ``VALUE3``, or ``VALUE4`` are magnitudes of the load, they are ignored if
            ``VALUE1`` is a table. If ``VALUE2``, ``VALUE3``, or ``VALUE4`` are any other values, they are
            used even if ``VALUE1`` is a table (for example, the load direction for face 5 of ``SURF154`` ).

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL-to-CFX analysis, ``VALUE2`` is the surface
            interface number (not available in the GUI). ``VALUE3`` and ``VALUE4`` are not used.

        meshflag : str
            Specifies how to apply normal pressure loading on the mesh. Valid in a `nonlinear adaptivity
            analysis <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_nlad/Hlp_G_ADVREZ.html>`_
            when ``Lab`` = PRES and ``KVAL`` = 0 or 1.

            0 - Pressure loading occurs on the current mesh (default).

            1 - Pressure loading occurs on the initial mesh for nonlinear adaptivity.

        Notes
        -----

        .. _SFE_notes:

        :ref:`sfe` defines surface loads on selected elements.

        .. warning::

            You cannot use SFE with the INFIN110or INFIN111elements without prior knowledge of element-face
            orientation (that is, you must know which face is the exterior in order to flag it). Also, for
            surface-effect elements SURF153and SURF154, use LKEYto enable tangential and other loads. For
            supported structural solid and shell elements, issue SFCONTROL to define tangential and other
            loads.

        :ref:`sfe` can apply tapered loads over the faces of most elements.

        You can use these related surface-load commands with :ref:`sfe` :

        * :ref:`sf` - Defines surface loads on nodes.
        * :ref:`sfbeam` - For beam elements allowing lateral surface loads that can be offset from the
          nodes, this command specifies the loads and offsets.
        * :ref:`sfcontrol` - Applies general (normal, tangential, and other) surface loads to `supported
          structural elements
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SFCONTROL.html#>`_.
        * :ref:`sfcum` - Accumulates (adds) surface loads applied via :ref:`sfe`.
        * :ref:`sfdele` - Delete loads applied via :ref:`sfe`.
        * :ref:`sffun` - Applies loads from a node-vs.-value function.
        * :ref:`sfgrad` - Applies an alternate tapered load.

        The :ref:`sfe` command can also define fluid-pressure-penetration loads ( ``Lab`` = PRES) at a
        contact interface. For this type of load, ``LKEY`` = 1 is used to specify the normal pressure
        values, ``LKEY`` = 3 is used to specify the tangential pressure values along the x direction of
        :ref:`esys`, ``LKEY`` = 4 is used to specify the tangential pressure values along the y direction of
        :ref:`esys`, and ``LKEY`` = 2 is used to specify starting points and penetrating points. See
        `Applying Fluid Penetration Pressure
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctecfluidpress.html#fl_press_dir_2D>`_

        Film effectiveness and free-stream temperatures specified via ``Lab`` = CONV are valid only for
        ``SURF151`` and ``SURF152``. Film effectiveness must be between 0 and 1 and it defaults to 0. If
        film effectiveness is applied, bulk temperature is ignored. When film effectiveness and free stream
        temperatures are specified, the commands to specify a surface-load gradient ( :ref:`sfgrad` ) or
        surface-load accumulation ( :ref:`sfcum` ) are not valid. For more information about film
        effectiveness, see `Conduction, Convection, and Mass Transport (Advection)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat1.html#thyeq10conductnov1601>`_

        You can specify a table name only when using structural (PRES) and thermal (CONV [film coefficient,
        bulk temperature, film effectiveness, and free stream temperature], HFLUX), diffusion flux (DFLUX),
        surface emissivity and ambient temperature (RAD), impedance (IMPD), normal velocity or acceleration
        (SHLD), absorption coefficient (ATTN), and substructure (SELV) surface load labels.

        When a tabular function load is applied to an element, the load will not vary according to the
        positioning of the element in space.

        For cases where Lab=FSI, MXWF, FREE, and INF, VALUE is not needed.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in the PREP7 and :ref:`slashmap` processors.
        """
        command = f"SFE,{elem},{lkey},{lab},{kval},{value1},{value2},{value3},{value4},{meshflag}"
        return self.run(command, **kwargs)

    def sfedele(
        self, elem: str = "", lkey: str = "", lab: str = "", lcomp: str = "", **kwargs
    ):
        r"""Deletes surface loads from elements.

        Mechanical APDL Command: `SFEDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFEDELE.html>`_

        Parameters
        ----------
        elem : str
            Element to which surface load deletion applies. If ALL, delete load from all selected elements (
            :ref:`esel` ). If ``ELEM`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``ELEM``.

        lkey : str
            Load key associated with surface load (defaults to 1). If ALL, delete surface loads for all load
            keys. If :ref:`sfcontrol` is issued for selected elements, this value is the face number. If
            ALL, deletes the surface load based on ``Lcomp``.

        lab : str
            Surface load label. If ALL, use all appropriate labels. See :ref:`sfe` for valid labels.

        lcomp : str
            Label of surface-load components. Valid when the surface load is defined via :ref:`sfcontrol`.
            Valid labels are NORM, TANX, TAXY when ``KCSYS`` = 0, LOCX, LOCY, LOCZ when ``KCSYS`` = 1, and
            USER when ``KCSYS`` = 2. ( ``KCSYS`` is specified when issuing :ref:`sfcontrol`.) If ALL,
            deletes all component on the face defined by ``LKEY``.

        Notes
        -----

        .. _SFEDELE_notes:

        Deletes surface loads from selected elements. See the :ref:`sfdele` command for an alternate surface
        load deletion capability based upon selected nodes.

        This command is also valid in PREP7.
        """
        command = f"SFEDELE,{elem},{lkey},{lab},{lcomp}"
        return self.run(command, **kwargs)

    def sfelist(self, elem: str = "", lab: str = "", **kwargs):
        r"""Lists the surface loads for elements.

        Mechanical APDL Command: `SFELIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFELIST.html>`_

        Parameters
        ----------
        elem : str
            Element at which surface load is to be listed. If ALL (or blank), list loads for all selected
            elements ( :ref:`esel` ). If ``ELEM`` = P, graphical picking is enabled and all remaining
            command fields are ignored (valid only in the GUI). A component name may be substituted for
            ``ELEM``.

        lab : str
            Valid surface load label. If ALL (or blank), use all appropriate labels. See the :ref:`sfe`
            command for labels.

        Notes
        -----

        .. _SFELIST_notes:

        The surface loads listed correspond to the current database values. The database is not updated for
        surface loads in POST1. Surface loads specified in tabular form, however, do list their values
        corresponding to the current results set in POST1.

        For ``SURF151`` or ``SURF152`` elements with an extra node for radiation and/or convection
        calculations (KEYOPT(5) = 1), the bulk temperature listed is the temperature of the extra node. If
        the thermal solution does not converge, the extra node temperature is not available for listing.

        Film effectiveness and free stream temperatures specified by the :ref:`sfe` command ( ``Lab`` =
        CONV) can only be listed by this command. The command lists film coefficients and bulk temperatures
        first and then film effectiveness and free stream temperatures below those values.

        Distributed-Memory Parallel (DMP) Restriction In a DMP analysis within the SOLUTION processor,
        :ref:`sfelist` support is not available for
        elements ``SURF151`` and ``SURF152`` when surface loading is applied via extra nodes (KEYOPT(5 > 0).
        If the command is issued under these circumstances, the resulting surface loads shown are not
        reliable.

        This command is valid in any processor.
        """
        command = f"SFELIST,{elem},{lab}"
        return self.run(command, **kwargs)

    def sffun(self, lab: str = "", par: str = "", par2: str = "", **kwargs):
        r"""Specifies a varying surface load.

        Mechanical APDL Command: `SFFUN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFFUN.html>`_

        Parameters
        ----------
        lab : str
            Valid surface load label. Load labels are listed under "Surface Loads" in the input table for
            each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. Issue
            :ref:`sffun`,STATUS to list current command settings.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sffun1:

            Thermal labels CONV and HFLUX are mutually exclusive.

        par : str
            Parameter containing list of surface load values. If ``Lab`` = CONV, values are typically the
            film coefficients and ``Par2`` values (below) are typically the bulk temperatures.

        par2 : str
            Parameter containing list of second surface load values (if any). If ``Lab`` = CONV, the
            ``Par2`` values are typically the bulk temperatures. ``Par2`` is not used for other surface load
            labels.

        Notes
        -----

        .. _SFFUN_notes:

        Specifies a surface load "function" to be used when the :ref:`sf` or :ref:`sfe` command is issued.
        The function is supplied through an array parameter vector which contains nodal surface load values.
        Node numbers are implied from the sequential location in the array parameter. For example, a value
        in location 11 applies to node 11. The element faces are determined from the implied list of nodes
        when the :ref:`sf` or :ref:`sfe` command is issued. Zero values should be supplied for nodes that
        have no load. A tapered load value may be applied over the element face. These loads are in addition
        to any loads that are also specified with the :ref:`sf` or :ref:`sfe` commands. Issue :ref:`sffun`
        (with blank remaining fields) to remove this specification. Issue :ref:`sffun`,STATUS to list
        current settings.

        Starting array element numbers must be defined for each array parameter vector. For example,
        :ref:`sffun`,CONV,A(1,1),A(1,2) reads the first and second columns of array A (starting with the
        first array element of each column) and associates the values with the nodes. Operations continue on
        successive column array elements until the end of the column. Another example to show the order of
        the commands:

        .. code:: apdl

           *dim,nodepres,array,2
           nodepres(1)=11,12
           /prep7
           et,1,42
           n,1
           n,2,1
           n,3,1,1
           n,4,,1
           e,1,2,3,4
           sfe,1,1,pres,1,3
           sfelist ! expected answer: 3 at both nodes 1 and 2
           sfedel,all,pres,all
           sffun,pres, nodepres(1)
           sfe,1,1,pres,1,5
           sfelist ! expected answer: 5+11=16 at node 1, 5+12=17 at node 2
           fini

        :ref:`sffun` does not work for tabular boundary conditions.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"SFFUN,{lab},{par},{par2}"
        return self.run(command, **kwargs)

    def sfgrad(
        self,
        lab: str = "",
        slkcn: str = "",
        sldir: str = "",
        slzer: str = "",
        slope: str = "",
        **kwargs,
    ):
        r"""Specifies a gradient (slope) for surface loads.

        Mechanical APDL Command: `SFGRAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFGRAD.html>`_

        Parameters
        ----------
        lab : str
            Valid surface load label. Load labels are listed under "Surface Loads" in the input table for
            each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sfgrad1:

            Thermal labels CONV and HFLUX are mutually exclusive.

        slkcn : str
            Reference number of slope coordinate system (used with ``Sldir`` and ``SLZER`` to determine
            COORD). Defaults to 0 (the global Cartesian coordinate system).

        sldir : str
            Slope direction in coordinate system ``SLKCN`` :

            * ``X`` - Slope is along X direction (default). Interpreted as R direction for non-Cartesian
              coordinate systems.

            * ``Y`` - Slope is along Y direction. Interpreted as θ direction for non-Cartesian coordinate
              systems.

            * ``Z`` - Slope is along Z direction. Interpreted as Φ direction for spherical or toroidal
              coordinate systems.

        slzer : str
            Coordinate location (degrees for angular input) where slope contribution is zero (CVALUE =
            VALUE). Allows the slope contribution to be shifted along the slope direction. For angular
            input, ``SLZER`` should be between ±180° if the singularity ( :ref:`cscir` ) is at 180° and
            should be between 0° and 360° if the singularity is at 0°.

        slope : str
            Slope value (load per unit length or per degree).

        Notes
        -----

        .. _SFGRAD_notes:

        Specifies a gradient (slope) for surface loads. All surface loads issued with the :ref:`sf`,
        :ref:`sfe`, :ref:`sfl`, or :ref:`sfa` commands while this specification is active will have this
        gradient applied (for complex pressures, only the real component will be affected; for convections,
        only the bulk temperature will be affected). The load value, CVALUE, calculated at each node is:

        CVALUE = VALUE + ( ``SLOPE`` X (COORD- ``SLZER`` ))

        where VALUE is the load value specified on the subsequent :ref:`sf`, :ref:`sfe`, :ref:`sfl`, or
        :ref:`sfa` commands and COORD is the coordinate value (in the ``Sldir`` direction of coordinate
        system ``SLKCN`` ) of the node. Only one :ref:`sfgrad` specification may be active at a time
        (repeated use of this command replaces the previous specification with the new specification). Issue
        :ref:`sfgrad` (with blank fields) to remove the specification. Issue :ref:`sfgrad`,STAT to show the
        current command status. The :ref:`sfgrad` specification (if active) is removed when the
        :ref:`lsread` (if any) command is issued.

        :ref:`sfgrad` does not work for tabular boundary conditions.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"SFGRAD,{lab},{slkcn},{sldir},{slzer},{slope}"
        return self.run(command, **kwargs)

    def sflist(self, node: str = "", lab: str = "", **kwargs):
        r"""Lists surface loads.

        Mechanical APDL Command: `SFLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFLIST.html>`_

        Parameters
        ----------
        node : str
            Node at which surface load is to be listed. If ALL (or blank), list for all selected nodes (
            :ref:`nsel` ). If ``NODE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``NODE``.

        lab : str
            Valid surface load label. If ALL (or blank), use all appropriate labels. See the :ref:`sf`
            command for labels

        Notes
        -----

        .. _SFLIST_notes:

        Lists the surface loads as applied with the :ref:`sf` command. Loads are listed only for the
        specified nodes on external faces of selected area and volume elements. Use :ref:`sfelist` for line
        elements. The surface loads listed correspond to the current database values. The database is not
        updated for surface loads in POST1. Surface loads specified in tabular form, however, do list their
        values corresponding to the current results set in POST1.

        For ``SURF151`` or ``SURF152`` elements with an extra node for radiation and/or convection
        calculations (KEYOPT(5) = 1), the bulk temperature listed is the temperature of the extra node. If
        the thermal solution does not converge, the extra node temperature is not available for listing.

        This command is valid in any processor.
        """
        command = f"SFLIST,{node},{lab}"
        return self.run(command, **kwargs)

    def sfscale(self, lab: str = "", fact: str = "", fact2: str = "", **kwargs):
        r"""Scales surface loads on elements.

        Mechanical APDL Command: `SFSCALE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFSCALE.html>`_

        Parameters
        ----------
        lab : str
            Valid surface load label. If ALL, use all appropriate labels.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sfscale1:

            Thermal labels CONV and HFLUX are mutually exclusive.

        fact : str
            Scale factor for the first surface load value. Zero (or blank) defaults to 1.0. Use a small
            number for a zero scale factor.

        fact2 : str
            Scale factor for the second surface load value. Zero (or blank) defaults to 1.0. Use a small
            number for a zero scale factor.

        Notes
        -----

        .. _SFSCALE_notes:

        Scales surface loads (pressure, convection, etc.) in the database on the selected elements. Surface
        loads are applied with the :ref:`sf`, :ref:`sfe`, or :ref:`sfbeam` commands. Issue the
        :ref:`sfelist` command to list the surface loads. Solid model boundary conditions are not scaled by
        this command, but boundary conditions on the FE model are scaled.

        Such scaled FE boundary conditions may still be overwritten by unscaled solid model boundary
        conditions if a subsequent boundary condition transfer occurs.

        :ref:`sfscale` does not work for tabular boundary conditions.

        This command is also valid in PREP7 and in the :ref:`slashmap` processor.
        """
        command = f"SFSCALE,{lab},{fact},{fact2}"
        return self.run(command, **kwargs)
