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


class Radiosity:

    def hemiopt(self, hres: str = "", tolerance: str = "", **kwargs):
        r"""Specifies options for Hemicube view factor calculation.

        Mechanical APDL Command: `HEMIOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HEMIOPT.html>`_

        Parameters
        ----------
        hres : str
            Hemicube resolution. Increase value to increase the accuracy of the view factor calculation.
            Defaults to 10.

        tolerance : str
            Tolerance value that controls whether or not facets are subdivided in view factor calculations
            to increase view factor accuracy. ``TOLERANCE`` is closely related to the spacing between
            facets. Defaults to 1e-6.
        """
        command = f"HEMIOPT,{hres},{tolerance}"
        return self.run(command, **kwargs)

    def qsopt(self, opt: str = "", **kwargs):
        r"""Specifies quasi static radiation options.

        Mechanical APDL Command: `QSOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_QSOPT.html>`_

        Parameters
        ----------
        opt : str
            Quasi static option:

            * ``OFF`` - Do not run transient radiation problem to steady-state (default).

            * ``ON`` - Run transient radiation problem to steady-state.

        Notes
        -----

        .. _QSOPT_notes:

        For more information on solving a static problem using a false transient approach, see.
        """
        command = f"QSOPT,{opt}"
        return self.run(command, **kwargs)

    def radopt(
        self,
        fluxtol: str = "",
        solver: int | str = "",
        maxiter: str = "",
        toler: str = "",
        overrlex: str = "",
        maxfluxiter: int | str = "",
        conservation: int | str = "",
        **kwargs,
    ):
        r"""Specifies Radiosity Solver options.

        Mechanical APDL Command: `RADOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RADOPT.html>`_

        Parameters
        ----------

        fluxtol : str
            Convergence tolerance for radiation flux. Defaults to 0.0001. This value is a relative
            tolerance.

        solver : int or str
            Choice of solver for radiosity calculation:

            * ``0`` - Gauss-Seidel iterative solver.

            * ``1`` - Direct solver.

            * ``2`` - Jacobi iterative solver (default).

        maxiter : str
            Maximum number of iterations for the iterative solvers ( ``SOLVER`` = 0 or 2). Defaults to 1000.

        toler : str
            Convergence tolerance for the iterative solvers ( ``SOLVER`` = 0 or 2). Defaults to 0.1.

            If ``TOLER`` ≥ 0, the value is interpreted as an absolute tolerance. If ``TOLER`` < 0, it is
            interpreted as a relative tolerance.

        overrlex : str
            Over-relaxation factor applied to the iterative solvers ( ``SOLVER`` = 0 or 2). Defaults to 0.1.

        maxfluxiter : int or str
            Maximum number of flux iterations to be performed according to the specified solver type:

            * ``0`` - If the FULL solver is specified ( :ref:`thopt`,FULL), convergence criteria are monitored
              and iterations are performed until convergence occurs. If the QUASI solver is specified (
              :ref:`thopt`,QUASI), convergence criteria are ignored and one iteration is performed. This value is
              the default.

            * ``1, 2, 3,...N`` - If the FULL solver is specified ( :ref:`thopt`,FULL), convergence criteria are
              monitored and iterations are performed until convergence occurs, or until the specified number of
              iterations has been completed, whichever comes first. If the QUASI solver is specified (
              :ref:`thopt`,QUASI), convergence criteria are ignored and the specified number of iterations are
              completed.

            To view ``MAXFLUXITER`` usage illustrations, see and.

        conservation : int or str
            Key to account for the midside node temperature of underlying solid elements for radiosity
            calculations. Under normal circumstations using lower order elements, this option does not need to
            be activated. However, when using higher elements, you can improve energy conservation by setting ``CONSERVATION`` = 1.

            * ``0`` - Not active (default). The midside node temperatures are not accounted for in the radiosity
              calculations.

            * ``1`` - Active. The midside node temperatures are accounted for in the radiosity calculations. To
              work effectively, ``CONSERVATION`` requires a one-to-one correspondance between the surface elements
              and their underlying solid elements. Therefore, it cannot be activated if the :ref:`rdec` command
              was issued when generating ``SURF251`` or ``SURF252`` elements.

        Notes
        -----

        .. _RADOPT_notes:

        The radiation heat flux is linearized, resulting in robust convergence.

        The radiation flux norm for ``FLUXTOL`` is expressed as:

        .. math::

            equation not available

        where i is the pass or iteration number and j is the surface facet for radiation.

        For a sufficiently small absolute tolerance value, relative tolerance converges in fewer iterations
        than absolute tolerance. For a sufficiently large absolute tolerance value, relative tolerance may
        cause convergence difficulties.

        For more information about ``FLUXTOL`` and ``MAXFLUXITER`` usage, see and in the `Thermal Analysis
        Guide <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4.html>`_.

        In and (under `Solving for Temperature and Radiosity
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/thermsolualgors.html#the_trans_quasimethfig>`_
        :sub:`Q` Q = F:sub:`Q` equation system via the iterative method.

        If ``TOLER`` ≥ 0, the iterative solver ( ``SOLVER`` = 0 or 2) is converged for maximum value over a
        different ``j`` as shown:

        .. math::

            equation not available

        If ``TOLER`` < 0, the iterative solver ( ``SOLVER`` = 0 or 2) is converged for maximum value over a
        different ``j`` as shown:

        .. math::

            equation not available

        where:

        * ``j`` = number of radiation facets
        * ``k`` = number of iterations ( ``k`` = 1 to ``MAXITER`` )

        The Jacobi iterative solver ( ``SOLVER`` = 2) is the only solver choice that runs in a fully
        distributed parallel fashion. Therefore, it is typically the best choice for optimal performance
        when running in distributed-memory parallel mode.
        """
        command = f"RADOPT,,{fluxtol},{solver},{maxiter},{toler},{overrlex},,,,,{maxfluxiter},{conservation}"
        return self.run(command, **kwargs)

    def rdec(self, option: str = "", reduc: str = "", nplace: str = "", **kwargs):
        r"""Defines the decimation parameters used by the radiosity solver method.

        Mechanical APDL Command: `RDEC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RDEC.html>`_

        Parameters
        ----------
        option : str
            Command options:

            * ``DEFINE`` - Defines the decimation parameters (default).

            * ``STAT`` - Shows the status/listing. Other command options are ignored.

        reduc : str
            Approximate reduction in the number of surface elements. Valid range is from 0.0 (no decimation,
            the default) to 1.0. This number is a factor applied to the initial number of element radiosity
            surfaces.

        nplace : str
            Node placement algorithm

            * ``OPTI`` - Optimal placement. An edge is collapsed by moving both nodes (I and J in the figure
              below) to a new location.

            * ``SUBS`` - Subset placement. An edge is collapsed by moving one node to another one. In the figure
              below, node I is moved to node J.

              .. figure::../../../images/_commands/gRDEC.svg

        Notes
        -----
        The :ref:`rdec` command sets decimation parameters. These parameters are used by the next
        :ref:`rsurf` command to generate radiosity surface elements.

        Decimation is the process of simplifying a fine surface mesh into a coarse one. This process is
        accomplished by a sequence of edge collapses.

        The maximum degree of decimation (1.0) is unreachable. The real degree of decimation is always less
        than 1.0 because the decimated mesh must always consist of at least one element.
        """
        command = f"RDEC,{option},{reduc},,{nplace}"
        return self.run(command, **kwargs)

    def rsopt(
        self, opt: str = "", filename: str = "", ext: str = "", dir_: str = "", **kwargs
    ):
        r"""Creates or loads the radiosity mapping data file for ``SURF251`` or ``SURF252`` element types.

        Mechanical APDL Command: `RSOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSOPT.html>`_

        Parameters
        ----------
        opt : str
            File option:

            * ``SAVE`` - Write the radiosity mapping data to a file. (Default)

            * ``LOAD`` - Read in the specified mapping data file.

        filename : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSOPT.html>`_ for further
            information.

        ext : str
            Filename extension for radiosity mapping data file (default = :file:`.rsm` ).

        dir_ : str
            Directory path for radiosity mapping data file. If you do not specify a directory path, it will
            default to your working directory.

        Notes
        -----
        Use this command to manually create or load a radiosity mapping data file. This command is useful if
        you want to create the mapping data file without issuing :ref:`save` or :ref:`cdwrite`, or if you
        want to specify that the file be located in a directory other than your working directory. Also use
        this command to manually load an existing mapping data file during a restart. Distributed-Memory
        Parallel (DMP) Restriction This command is not supported in a DMP solution.
        """
        command = f"RSOPT,{opt},{filename},{ext},{dir_}"
        return self.run(command, **kwargs)

    def rsurf(self, options: str = "", delopts: str = "", etnum: str = "", **kwargs):
        r"""Generates the radiosity surface elements and stores them in the database.

        Mechanical APDL Command: `RSURF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSURF.html>`_

        Parameters
        ----------
        options : str
            Command options:

            * ``CLEAR`` - Deletes radiosity surface elements and nodes. The set of elements and nodes to be
              deleted is defined by ``Delopts``. ``ETNUM`` is ignored.

            * ``DEFINE`` - Creates the radiosity surface elements and nodes (default).

            * ``STAT`` - Shows the status/listing. Other command options are ignored.

        delopts : str
            Deletion options

            * ``ALL`` - Deletes all radiosity surface elements and nodes.

            * ``LAST`` - Deletes radiosity surface elements and nodes created by the last :ref:`rsurf` command.

        etnum : str
            Element type number. Leave blank to indicate the next available number.

        Notes
        -----
        This command generates the radiosity surface elements ( ``SURF251``, ``SURF252`` ) based on the
        :ref:`rsymm` and :ref:`rdec` parameters and stores them in the database. It works only on the faces
        of selected underlying elements that have RDSF flags on them and all corner nodes selected. You can
        issue multiple :ref:`rsurf` commands to build the radiosity model. However, all :ref:`rsurf`
        commands must be issued after issuing the :ref:`rsymm` command, and after the model is complete
        (that is, after all meshing operations are complete).

        If you do issue multiple :ref:`rsurf` commands for different regions, you must first mesh the
        different regions, and then generate the radiosity surface elements on each meshed region
        individually. Use :ref:`rsurf`,,,ETNUM to assign a separate element type number to each region. This
        procedure allow you to identify the individual regions later in the multi-field analysis.

        If the underlying solid elements are higher order, the radiosity surface elements are always lower
        order (4- or 3-node in 3D or 2-node in 2D). Decimation will always occur before any symmetry
        operations.

        For 2D axisymmetric YR models, the newly-generated nodes can have only positive Y coordinates.

        The :ref:`rsurf` command assigns real constant set number 1 to all ``SURF251`` and ``SURF252``
        elements generated, irrespective of the current real constant set attribute pointer ( :ref:`real`
        command). If the generated elements require a real constant set other than number 1, you must
        manually change the set number for those elements by using the :ref:`emodif`,,REAL command.

        If you have already issued :ref:`rsurf` for a surface and you issue :ref:`rsurf` again, the program
        creates a new set of radiosity surface elements and nodes over the existing set, resulting in an
        erroneous solution. Distributed-Memory Parallel (DMP) Restriction This command is not supported in a
        DMP solution.

        This is an action command (that creates or deletes surface meshes) and is serial in nature. Even if
        a DMP solution is running, the :ref:`rsurf` command runs serially.
        """
        command = f"RSURF,{options},{delopts},{etnum}"
        return self.run(command, **kwargs)

    def rsymm(
        self,
        option: str = "",
        cs: str = "",
        axis: str = "",
        nsect: str = "",
        condvalue: str = "",
        sval: str = "",
        eval_: str = "",
        **kwargs,
    ):
        r"""Defines symmetry, rotation, or extrusion parameters for the radiosity method.

        Mechanical APDL Command: `RSYMM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSYMM.html>`_

        Parameters
        ----------
        option : str
            Command options:

            * ``CLEAR`` - Deletes all symmetry/extrusion definitions. Other command options are ignored.

            * ``DEFINE`` - Defines the symmetry/extrusion definition (default).

            * ``STAT`` - Shows the status/listing. Other command options are ignored.

            * ``COND`` - Activates or deactivates condensation for all defined radiation symmetries/extrusions,
              which reduces the size of the radiosity equation system (see :ref:`cmd_rsymm_fig1` ). Default is
              off.

              Condensation via :ref:`rsymm`,COND is not recommended as the most efficient solution for symmetric
              models. To best leverage model symmetry to improve efficiency, use view factor condensation via the
              :ref:`vfco` command, which condenses the view factor matrix in addition to simplifying the radiosity
              equations (see :ref:`RSYMM_VFCO_notes` for details).

        cs : str
            Local coordinate system ( :math:`equation not available` 11) as defined using the  :ref:`local`
            or :ref:`cs` commands or the global coordinate system (0). For planar reflection, the coordinate
            system origin must be on the plane of symmetry (POS) and one of its axes must be normal to the
            POS. For cyclic reflection, the coordinate system origin must be coincident with the center of
            rotation (COR). Only Cartesian systems are valid.

        axis : str
            Axis label of the coordinate system ( ``CS`` ) that is normal to the POS for planar reflection, or
            label to indicate the type of extrusion. For cyclic reflection, this field must be blank, and it is
            assumed that the Z axis is aligned with the axis of rotation.

            * ``X, Y, or Z`` - Planar reflection. For 2D model planar reflections, valid labels are X or Y. For
              3D model planar reflections, valid labels are X, Y, or Z.

            * ``ZEXT`` - Linear extrusion of a line element in the X-Y plane, in the Z direction, to create
              4-noded ``SURF252`` elements. ``NSECT`` indicates how many elements will be created. ``SVAL`` is the
              starting Z value, and ``EVAL`` is the ending Z value. ``CS`` must be 0.

            * ``CEXT`` - Circumferential extrusion (theta direction) around the global Y-axis. A 2-noded line
              element in the X-Y plane is extruded to create 4-noded ``SURF252`` elements. ``NSECT`` indicates how
              many elements will be created. ``SVAL`` is the starting angle, and EVAL is the ending angle (in
              degrees). The angles are with respect to the global X-axis. ``CS`` must be 0.

            * ``(blank)`` - Cyclic reflection.

        nsect : str
            Number of cyclic reflections to be done, or number of elements in the extrusion direction.

            For planar reflection, this field must be 0 or blank.

            For cyclic reflection, this field must be ≥ 1 or ≤ -1. Use a positive value if you want the
            sector angle to be computed automatically. Use a negative value if you want the sector angle to
            be computed manually. See `Notes
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_RSYMM.html#cmd_rsymm_fig1>`_
            Notes for details.

        condvalue : str
            Condensation key. Valid only when ``Option`` = COND.

            * ``ON`` - Activates condensation in the radiosity solver for all defined radiation
              symmetries/extrusions.

            * ``OFF`` - Deactivates condensation in the radiosity solver for all defined radiation
              symmetries/extrusions (default).

        sval : str
            Starting and ending Z values (if ``Axis`` = ZEXT) or angle values (if ``Axis`` = CEXT) used for
            the extrusion. Not used for planar or cyclic reflection.

        eval_ : str
            Starting and ending Z values (if ``Axis`` = ZEXT) or angle values (if ``Axis`` = CEXT) used for
            the extrusion. Not used for planar or cyclic reflection.

        Notes
        -----

        .. _rsymm_notes:

        The :ref:`rsymm` command is used to define the plane of symmetry (POS) for planar reflection or the
        center of rotation (COR) for cyclic reflection. It can also be used to set parameters for a linear
        or circumferential extrusion. The input provided on this command is used to generate radiosity
        surface elements ( ``SURF251`` / ``SURF252`` ) when the :ref:`rsurf` command is issued.

        The :ref:`rsymm` command must be issued before :ref:`rsurf`, and it may be issued multiple times to
        have more than one planar/cyclic reflection or extrusion. The :ref:`rsurf` command processes
        :ref:`rsymm` commands in the order they are issued.

        For planar reflection, you must define a local coordinate system ( :math:`equation not available`
        11) with its origin on the POS. One of its axes must be aligned so that it is   normal to the plane.
        If possible, use the existing global coordinate system (0).

        For cyclic reflection, you must define a local coordinate system ( :math:`equation not available`
        11) with its origin coincident with the COR. Reflections occur about the local   Z-axis in the
        counterclockwise direction. You must align the Z-axis properly. If possible, use   the existing
        global coordinate system (0).

        For cyclic reflection, ``NSECT`` is used as follows:

        :math:`equation not available`

        :math:`equation not available`

        where θ:sub:`max` and θ:sub:`min` are computed internally based on location of the
        RDSF (surface-to-surface radiation) flagged surfaces.

        See :ref:`cmd_rsymm_fig2` for an example of ``NSECT`` usage.

        For linear or circumferential extrusion ( ``Axis`` = ZEXT or CEXT), you must ensure that the
        extruded area matches the area of the underlying element; otherwise, the results may not be correct.
        For example, in the case of ``PLANE55`` elements with a planar depth = 10, use ``Axis`` = ZEXT and
        set ``SVAL`` and ``EVAL`` such that ``EVAL`` - ``SVAL`` = 10. Likewise, for axisymmetric ``PLANE55``
        elements, use ``Axis`` = CEXT and set ``SVAL`` and ``EVAL`` such that ``EVAL`` - ``SVAL`` = 360. You
        must also issue :ref:`v2dopt`,1 for the axisymmetric case. See :ref:`cmd_rsymm_fig3` for extrusion
        examples.

        The ``Axis`` = ZEXT and CEXT options are not valid for ``SHELL131`` and ``SHELL132`` elements.

        New surface elements generated by the :ref:`rsymm` command inherit the properties of the original
        elements.

        For 2D axisymmetric models, :ref:`rsymm` can be used only for symmetrization in the YR plane. It
        cannot be used for the theta direction. Use :ref:`v2dopt` in that case.

        For 2D axisymmetric YR models, the newly-generated nodes can have only positive X coordinates.

        Usage Example: Positive and Negative ``NSECT`` Values
        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. figure::../../../images/_commands/gcmdrsymm3.png

           Usage Example: Extrusions with Axis= ZEXT and CEXT

        .. _RSYMM_VFCO_notes:

        Considerations for View Factor Condensation
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        View Factor Condensation via the :ref:`vfco` command is the recommended method to improve solution
        efficiency for models with symmetry, which are defined with the :ref:`rsymm` command.

        When the :ref:`rsymm` command is used, it implies that some radiation facets ( ``SURF251`` or
        ``SURF252`` ) created by the :ref:`rsurf` command will be a reflection of others. By definition,
        radiation facets with an underlying solid element are independent facets. Dependent facets are
        copies of the independent facets having the same dimensions but at different locations. The
        following figures illustrate solid elements (grey) and independent (blue) and dependent (red) facets
        for models with different types of symmetry. View factor condensation improves efficiency by
        condensing the view factor matrix to calculate view factors only for independent facets ( ) and
        simplifying the radiosity equations to solve only for the independent radiosity flux ( `Radiosity
        Equations Simplified for Models with Symmetry
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat5.html#eqd7803bd4-5251-4d80-bd90-e01d7fdcb8bb>`_
        `Example of a 3D Open Enclosure with Symmetry: Radiation Analysis with Condensed View Factor
        Calculation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/the_example_rad_condensedVF.html#>`_

        Independent and Dependent Facets in a Model with Planar Symmetry Employing View Factor Condensation

        Independent and Dependent Facets in a Model with Cyclic Symmetry Employing View Factor Condensation

        Independent and Dependent Facets for a Model Built by Extrusions Employing View Factor Condensation
        Although it is not the recommended method, the following figure illustrates condensation via
        :ref:`rsymm`,COND. The efficiency gains by condensation via :ref:`rsymm`,COND are less than those
        obtained with view factor condensation via the :ref:`vfco` command, which reduces the view factor
        matrix in addition to simplifying the radiosity equations, as described in and `Radiosity Equations
        Simplified for Models with Symmetry
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat5.html#eqd7803bd4-5251-4d80-bd90-e01d7fdcb8bb>`_

        .. figure::../../../images/_commands/gcmdrsymm1.png

           Usage Example: Option= COND

        **Example Usage**

        .. _RSYMM_example:

        2D Radiation Analysis Using the Radiosity Method with Decimation and Symmetry

        `3D Open Enclosure with Symmetry: Radiation Analysis with Condensed View Factor Calculation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/the_example_rad_condensedVF.html#>`_
        """
        command = f"RSYMM,{option},{cs},{axis},{nsect},{condvalue},{sval},{eval_}"
        return self.run(command, **kwargs)

    def spcnod(self, encl: str = "", node: str = "", **kwargs):
        r"""Defines a space node for radiation using the Radiosity method.

        Mechanical APDL Command: `SPCNOD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPCNOD.html>`_

        Parameters
        ----------
        encl : str
            Radiating surface enclosure number. Defaults to 1. If ENCL = STAT, the command lists all
            enclosure space nodes. If ENCL = DELE, the command deletes all enclosure space nodes.

        node : str
            Node defined to be the space node.

        Notes
        -----

        .. _SPCNOD_notes:

        For open systems, an enclosure may radiate to a space node ( ``NODE`` ).

        Open systems may be characterized by one or more enclosures ( ``ENCL`` ). Each enclosure may radiate
        to a different space node ( ``NODE`` ).

        For a space node that is not part of the finite element model, specify the temperature using the
        :ref:`d` command. For the first load step, the space node temperature ramps from the uniform
        temperature specified by the :ref:`tunif` command to the temperature specified by the :ref:`d`
        command. For subsequent load steps, it ramps from the previous value of the space node temperature.
        For intermediate load steps, use the :ref:`spcnod`,DELETE command and specify the space node
        temperature again to ramp from the uniform temperature.

        For a space node that is part of the finite element model, the temperature is that calculated during
        the finite element solution.
        """
        command = f"SPCNOD,{encl},{node}"
        return self.run(command, **kwargs)

    def spctemp(self, encl: str = "", temp: str = "", **kwargs):
        r"""Defines a free-space ambient temperature for radiation using the Radiosity method.

        Mechanical APDL Command: `SPCTEMP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPCTEMP.html>`_

        Parameters
        ----------
        encl : str
            Radiating surface enclosure number. Defaults to 1. If ``ENCL`` = STAT, the command lists all
            enclosure space temperatures. If ``ENCL`` = DELE, the command deletes all enclosure space
            temperatures.

        temp : str
            Temperature of free-space in the reference temperature system. The temperature will be offset by
            the value specified in the :ref:`toffst` command for internal calculations.

        Notes
        -----

        .. _SPCTEMP_notes:

        For open systems, an enclosure may radiate to the free-space ambient temperature ( ``TEMP`` ).

        Open systems may be characterized by one or more enclosures ( ``ENCL`` ). Each enclosure may radiate
        to a different free-space ambient temperature ( ``TEMP`` ).

        For the first load step, the space temperature ramps from the uniform temperature specified by the
        :ref:`tunif` command to the temperature specified by the :ref:`spctemp` command. For subsequent load
        steps, it ramps from the previous value of the space temperature. For intermediate load steps, use
        the :ref:`spctemp`,DELETE command and specify the space temperature again to ramp from the uniform
        temperature.

        Reissuing :ref:`spctemp` does not overwrite the previous value. To change the free-space ambient
        temperature ( ``TEMP`` ) between loadsteps, you must issue :ref:`spctemp`,DELETE and then reissue
        :ref:`spctemp`, ``ENCL``, ``TEMP``.
        """
        command = f"SPCTEMP,{encl},{temp}"
        return self.run(command, **kwargs)

    def v2dopt(
        self,
        geom: int | str = "",
        ndiv: str = "",
        hidopt: int | str = "",
        nzone: str = "",
        **kwargs,
    ):
        r"""Specifies 2D/axisymmetric view factor calculation options.

        Mechanical APDL Command: `V2DOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_V2DOPT.html>`_

        **Command default:**

        .. _V2DOPT_default:

        By default, a planar geometry is assumed ( ``GEOM`` = 0) and the hidden viewing option is used (
        ``HIDOPT`` = 0).

        The view factor algorithm sets the number of rays as follows, depending on whether a planar or
        axisymmetric geometry is specified:

        * For ``GEOM`` = 0, ``HIDOPT`` = 0 and ``NZONE`` = 0, the number of zones used in view the factor
          calculation is 200.

        * For ``GEOM`` = 1, ``HIDOPT`` = 0, and ``NZONE`` = 0, the number of zones used in the view factor
          calculation is 20.

        Parameters
        ----------
        geom : int or str
            Choice of geometry:

            * ``0`` - Planar (default).

            * ``1`` - Axisymmetric

        ndiv : str
            Number of divisions for axisymmetric geometry (that is, the number of circumferential segments).
            Default is 50. There is no maximum limit if ``HIDOPT`` = 0; the maximum is 90 if ``HIDOPT`` = 1.
            If ``NDIV`` is ≤ 6, it is reset to 50.

            For more information, see `View Factors of Axisymmetric Bodies
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat5.html#thyeq2viewbodynov1901>`_

        hidopt : int or str
            Viewing option:

            * ``0`` - Hidden (default).

            * ``1`` - Non-hidden

        nzone : str
            Number of zones (that is, the number of rays emanating from a surface) for view factor
            calculation. This is used if ``HIDOPT`` = 0.

            If ``NZONE`` is blank, it is set to 0 and the view factor algorithm sets the number of rays.
            (See Command Default below.)

            If ``NZONE`` is < 0 or > 1000, it is set to 200.

        Notes
        -----

        .. _V2DOPT_notes:

        :ref:`v2dopt` sets 2D view factor calculation options for the radiosity solver method. For 2D view
        factor calculations, the ray-emanation method is used.

        The geometry type can be either 2D planar (default) or axisymmetric. For the axisymmetric case, you
        can define the number of circumferential segments (defaults to 20). You can also specify the hidden
        or non-hidden viewing option (defaults to hidden) and the number of zones for the view factor
        calculation. For more information, see `Process for Using the Radiosity Solver Method
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/Hlp_G_THE4_7.html#theapploadtlm61499620>`_
        """
        command = f"V2DOPT,{geom},{ndiv},{hidopt},{nzone}"
        return self.run(command, **kwargs)

    def vfopt(
        self,
        opt: str = "",
        filename: str = "",
        ext: str = "",
        dir_: str = "",
        filetype: str = "",
        fileformat: int | str = "",
        wrio: str = "",
        addional_command_arg: str = "",
        **kwargs,
    ):
        r"""Specifies options for the view factor file and calculates view factors.

        Mechanical APDL Command: `VFOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFOPT.html>`_

        Parameters
        ----------
        opt : str
            View factor option:

            * ``NEW`` - Calculate view factors, store them in the database, and write them to a file. This is an
              action option that is executed immediately when the command is issued.

            * ``OFF`` - Do not recalculate or read view factors if they already exist in the database; otherwise
              calculate them at the next :ref:`solve` command. Remaining arguments are ignored. This option is the
              default.

            * ``READ`` - If the command is issued in the solution processor ( :ref:`slashsolu` ), this option
              reads view factors from the specified binary file when the next :ref:`solve` command is issued.
              ``FileType`` must be set to BINA (binary). For subsequent :ref:`solve` commands, the program
              switches back to the default option (OFF).

              If the command is issued in the radiation processor ( :ref:`aux12` ), this option immediately reads
              view factors from the specified binary file. ``FileType`` must be set to BINA (binary). The program
              switches back to the default option (OFF) after reading the view factors.

            * ``NONE`` - Do not write view factors to a file when the next :ref:`solve` command is issued.
              Remaining arguments are ignored.

        filename : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFOPT.html>`_ for further
            information.

        ext : str
            Filename extension for view factor matrix. Default = :file:`vf`.

        dir_ : str
            Directory path for view factor matrix. If you do not specify a directory path, it will default
            to your working directory.

        filetype : str
            View factor file type:

            * ``BINA`` - Binary (default).

            * ``ASCI`` - ASCII.

        fileformat : int or str
            Format for the specified ``Filetype`` :

            Binary files ( ``Filetype`` = BINA):

            * ``0`` - No compression. (View factor file size may be very large.)

            * ``1`` - Zeroes are compressed out. (Useful for large models to reduce the view factor file size.)

            ASCII files ( ``Filetype`` = ASCI):

            * ``0`` - 10F7.4 (low precision, lower accuracy).

            * ``1`` - 7F11.8 (high precision, higher accuracy).

        wrio : str
            Write only the view factors of independent facets for symmetric models. This option is valid when
            view factor condensation is enabled ( :ref:`vfco`,,,1 or :ref:`vfco`,,,2) and further increases
            efficiency by reducing read/write time; for more information, see :ref:`VFOPT_VFCondensation` below.

            * ``ON`` - Writes only the independent view factors when view factor condensation has been enabled,
              providing additional efficiency gains. After view factors are computed and written to a file,
              ``WRIO`` is automatically reset to OFF.

            * ``OFF`` - Turns off option to write only the independent view factors (default).

        addional_command_arg : str
            Additional arguments can be passed to the initial command. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFOPT.html>`_ for further
            information.

        Notes
        -----

        .. _VFOPT_notes:

        The :ref:`vfopt` command allows you to deactivate the view factor computation ( ``Opt`` = OFF) if
        the view factors already exist in the database. The default behavior is OFF upon encountering the
        second and subsequent :ref:`solve` commands in the solution processor.

        When ``Opt`` = READ, only a previously calculated view factor binary file is valid. View factors are
        read only and are not written after they are read in. Do not issue :ref:`vfopt`,OFF or
        :ref:`vfopt`,NONE until after the next :ref:`solve` command is executed.

        If you want to read in view factors after restarting a radiation analysis, issue :ref:`vfopt`,READ
        after :ref:`antype`,,REST.

        For 3D analyses, two options are available for calculating view factors when running a distributed-
        memory parallel solution :

        * Issue a :ref:`solve` command -- View factors are calculated in parallel mode if no view factors
          were previously calculated.

        * Issue a :ref:`vfopt`,NEW command -- View factors are calculated in serial mode.

        For 2D analyses, view factors are calculated in serial mode.

        .. _VFOPT_VFCondensation:

        Considerations for Symmetric Models Using View Factor Condensation
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        For symmetric models using view factor condensation ( :ref:`vfco`,,,1 or :ref:`vfco`,,,2),
        read/write time can be reduced by writing only the independent view factors since they are the only
        non-zero values in the view factor matrix as described in.

        When view factor condensation is turned off ( :ref:`vfco`,,,0), the full matrix is written to the
        view factor file when :ref:`vfopt`,NEW is issued:

        :math:`equation not available`  where the view factor matrix is decomposed, and the subscripts,
        :math:`equation not available`  and  :math:`equation not available`, denote independent and
        dependent. (See  for details.)

        When view factor condensation is turned on ( :ref:`vfco`,,,1 or :ref:`vfco`,,,2), use ``WRIO`` to
        control what is written to the view factor file:

        * When :ref:`vfopt`,NEW,,,,,,OFF is issued, the lumped matrix and zeros are written: :math:`equation
          not available`  (For the definition of  **F**  :sup:`L`, see.)

        * When :ref:`vfopt`,NEW,,,,,,ON is issued, only the lumped matrix is written: :math:`equation not
          available`.

        **Example Usage**

        .. _VFOPT_example:

        2D Radiation Analysis Using the Radiosity Method with Decimation and Symmetry

        `3D Open Enclosure with Symmetry: Radiation Analysis with Condensed View Factor Calculation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/the_example_rad_condensedVF.html#>`_
        """
        command = f"VFOPT,{opt},{filename},{ext},{dir_},{filetype},{fileformat},{wrio},{addional_command_arg}"
        return self.run(command, **kwargs)
