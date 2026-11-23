# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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

from ansys.mapdl.core._commands import CommandsBase


class Radiosity(CommandsBase):

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
        stabilization: str = "",
        **kwargs,
    ):
        r"""Specifies Radiosity Solver options.

        Mechanical APDL Command: `RADOPT <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RADOPT.html>`_

        **Command default:**

        The Jacobi iterative solver (``SOLVER``\ = 2) is the default; it is only
        available for 3D models. If the analysis is 2D, the Gauss-Seidel
        iterative solver (``SOLVER``\ = 0) is used instead.

        Parameters
        ----------
        fluxtol : str
            Convergence tolerance for radiation flux. Defaults to 0.0001.
            This value is a relative tolerance.

        solver : int or str
            Choice of solver for radiosity calculation:

            * ``0`` - Gauss-Seidel iterative solver.

            * ``1`` - Direct solver.

            * ``2`` - Jacobi iterative solver (default).

        maxiter : str
            Maximum number of iterations for the iterative solvers
            (``SOLVER``\ = 0 or 2). Defaults to 1000.

        toler : str
            Convergence tolerance for the iterative solvers (``SOLVER``\ = 0
            or 2). Defaults to 0.1.

            If ``TOLER``\ ≥ 0, the value is interpreted as an absolute
            tolerance. If ``TOLER``\ < 0, it is interpreted as a relative
            tolerance.

        overrlex : str
            Over-relaxation factor applied to the iterative solvers
            (``SOLVER``\ = 0 or 2). Defaults to 0.1.

        maxfluxiter : int or str
            Maximum number of flux iterations to be performed according to
            the specified solver type:

            * ``0`` - If the FULL solver is specified (`THOPT
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_THOPT.html>`_,FULL),
              convergence criteria are monitored and iterations are
              performed until convergence occurs. If the QUASI solver is
              specified (`THOPT
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_THOPT.html>`_,QUASI),
              convergence criteria are ignored and one iteration is
              performed. This value is the default.

            * ``1, 2, 3, ...N`` - If the FULL solver is specified (`THOPT
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_THOPT.html>`_,FULL),
              convergence criteria are monitored and iterations are
              performed until convergence occurs, or until the specified
              number of iterations has been completed, whichever comes
              first. If the QUASI solver is specified (`THOPT
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_THOPT.html>`_,QUASI),
              convergence criteria are ignored and the specified number of
              iterations are completed.

            To view ``MAXFLUXITER``\ usage illustrations, see `Figure 3.5:
            FULL Solution Method When Radiosity Is Present
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#the_trans_fullmethfig>`_
            and `Figure 3.6: QUASI Solution Method When Radiosity Is Present
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#the_trans_quasimethfig>`_.

        conservation : int or str
            Key to account for the midside node temperature of underlying
            solid elements for radiosity calculations. Under normal
            circumstations using lower order elements, this option does not
            need to be activated. However, when using higher elements, you
            can improve energy conservation by setting ``CONSERVATION``\ =
            1.

            * ``0`` - Not active (default). The midside node temperatures
              are not accounted for in the radiosity calculations.

            * ``1`` - Active. The midside node temperatures are accounted
              for in the radiosity calculations.

              .. note::

                 **Note:**\ To work effectively, ``CONSERVATION``\
                 requires a one-to-one correspondance between the
                 surface elements and their underlying solid elements.
                 Therefore, it cannot be activated if the `RDEC
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RDEC.html>`_\
                 command was issued when generating `SURF251
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_
                 or `SURF252
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_
                 elements.

        stabilization : str
            Nonlinear stabilization options to improve convergence behavior.
            The temperature field is calculated in the Newton Raphson (NR)
            loop, and the radiation heat flux, Q, is calculated in the
            multipass loop (see following figure). Q is not applied directly
            to the underlying solid elements. It is converted to a
            convection boundary condition that is applied to the underlying
            solid with a film coefficient, H:sub:`rad`, and a bulk
            temperature, T:sub:`bulk`. This helps to stabilize the solution,
            which may otherwise diverge. Stabilization options are:

            * ``0`` - H:sub:`rad`\ and T:sub:`bulk`\ are constants that are
              calculated from the converged temperature from the previous
              pass, T:sup:`p-1`\ (default).

            * ``1`` - Additional stabilization due to a nonlinear
              H:sub:`rad`\ that depends on the changing temperature,
              T:sup:`P`, during convergence in the NR loop in the current
              pass. Use this to improve stabilization if you experience
              convergence difficulties.

            * ``2`` - Further stabilization if the emissivity is
              temperature-dependent. (Temperature-dependent emissivity can
              be specified using the `MP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_MP.html>`_\
              command or the `MPTEMP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_MPTEMP.html>`_\
              and `MPDATA
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_MPDATA.html>`_\
              commands.) Use this option for additional stabilization if you
              still experience convergence difficulties with
              ``STABILIZATION``\ = 1.

        Notes
        -----

        .. _RADOPT_notes:

        The radiation heat flux is linearized, resulting in robust convergence.

        The radiation flux norm for ``FLUXTOL``\ is expressed as:

        where i is the pass or iteration number and j is the surface facet for
        radiation.

        For a sufficiently small absolute tolerance value, relative tolerance
        converges in fewer iterations than absolute tolerance. For a
        sufficiently large absolute tolerance value, relative tolerance may
        cause convergence difficulties.

        For more information about ``FLUXTOL``\ and ``MAXFLUXITER``\ usage, see
        `Figure 3.5: FULL Solution Method When Radiosity Is Present
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#the_trans_fullmethfig>`_
        and `Figure 3.6: QUASI Solution Method When Radiosity Is Present
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#the_trans_quasimethfig>`_
        in the `*Thermal Analysis Guide*\
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_TheTOC.html>`_.

        In `Figure 3.5: FULL Solution Method When Radiosity Is Present
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#the_trans_fullmethfig>`_
        and `Figure 3.6: QUASI Solution Method When Radiosity Is Present
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#the_trans_quasimethfig>`_
        (under `Solving for Temperature and Radiosity
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/thermsolualgors.html#therm_fullquasirad>`_
        in the `*Thermal Analysis Guide*\
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_TheTOC.html>`_),
        refer to the K:sub:`Q`\ Q = F:sub:`Q`\ equation system via the iterative
        method.

        If ``TOLER``\ ≥ 0, the iterative solver (``SOLVER``\ = 0 or 2) is
        converged for maximum value over a different ``j``\ as shown:

        If ``TOLER``\ < 0, the iterative solver (``SOLVER``\ = 0 or 2) is
        converged for maximum value over a different ``j``\ as shown:

        where:

        * ``j``\ = number of radiation facets

        * ``k``\ = number of iterations (``k``\ = 1 to ``MAXITER``)

        The Jacobi iterative solver (``SOLVER``\ = 2) is the only solver choice
        that runs in a fully distributed parallel fashion. Therefore, it is
        typically the best choice for optimal performance when running in
        distributed-memory parallel mode. Since the Jacobi iterative solver is
        not available for 2D models, it is not possible to run 2D models in
        parallel processes.
        """
        command = f"RADOPT,,{fluxtol},{solver},{maxiter},{toler},{overrlex},,,,,{maxfluxiter},{conservation},{stabilization}"
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

              .. figure:: ../../../images/_commands/gRDEC.svg

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

    def rsurf(
        self,
        options: str = "",
        delopts: str = "",
        etnum: str = "",
        dkey: str = "",
        **kwargs,
    ):
        r"""Generates the radiosity surface elements and stores them in the database.

        Mechanical APDL Command: `RSURF <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_

        Parameters
        ----------
        options : str
            Command options:

            * ``CLEAR`` - Deletes radiosity surface elements and nodes. The
              set of elements and nodes to be deleted is defined by
              ``Delopts``. ``ETNUM``\ and ``DKEY``\ are ignored.

            * ``DEFINE`` - Creates the radiosity surface elements and nodes
              (default).

            * ``STAT`` - Shows the status/listing. Other command options are
              ignored.

        delopts : str
            Deletion options

            * ``ALL`` - Deletes all radiosity surface elements and nodes.

            * ``LAST`` - Deletes radiosity surface elements and nodes
              created by the last `RSURF
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
              command.

        etnum : str
            Element type number. Leave blank to indicate the next available
            number.

        dkey : str
            Enables or disables displacement degrees of freedom (DOFs) on
            the generated radiosity surface elements so that they deform
            with the underlying solid mesh if large-deflection effects are
            enabled (`NLGEOM
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_NLGEOM.html>`_,ON).
            Displacement DOFs are required to recalculate view factors at
            the substep level (`VFUP
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,ON).

            * ``0`` - Sets KEYOPT(1) = 0 on generated radiosity surface
              elements: Temperature (TEMP) is the only DOF (default).

            * ``1`` - Sets KEYOPT(1) = 1 on generated radiosity surface
              elements: DOFs include temperature (TEMP) and displacement (UX
              and UY for `SURF251
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_,
              UX, UY, and UZ for `SURF252
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_).

        Notes
        -----

        .. _RSURF_notes:

        This is an action command that generates the radiosity surface elements
        (`SURF251
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_,
        `SURF252
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_)
        based on the `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        and `RDEC
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RDEC.html>`_\
        parameters and stores them in the database. It works only on the faces
        of selected underlying elements that have RDSF flags on them and all
        corner nodes selected. You can issue multiple `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        commands to build the radiosity model. However, all `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        commands must be issued after issuing the `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        command, and after the model is complete (that is, after all meshing
        operations are complete).

        If you do issue multiple `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        commands for different regions, you must first mesh the different
        regions, and then generate the radiosity surface elements on each meshed
        region individually. Use `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_,,,ETNUM
        to assign a separate element type number to each region. This procedure
        allow you to identify the individual regions later in the multi-field
        analysis.

        If the underlying solid elements are higher order, the radiosity surface
        elements are always lower order (4- or 3-node in 3D or 2-node in 2D).
        Decimation will always occur before any symmetry operations.

        For 2D axisymmetric YR models, the newly-generated nodes can have only
        positive Y coordinates.

        The `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        command assigns real constant set number 1 to all `SURF251
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_
        and `SURF252
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_
        elements generated, irrespective of the current real constant set
        attribute pointer (`REAL
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_REAL.html>`_\
        command). If the generated elements require a real constant set other
        than number 1, you must manually change the set number for those
        elements by using the `EMODIF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_EMODIF.html>`_,,REAL
        command.

        If you have already issued `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        for a surface and you issue `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        again, the program creates a new set of radiosity surface elements and
        nodes over the existing set, resulting in an erroneous solution.

        Specifying ``DKEY``\ is equivalent to setting KEYOPT(1) on the radiosity
        surface elements (see the `SURF251
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_
        / `SURF252
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_
        element descriptions for details). To change the KEYOPT(1) setting on
        surface elements after they are generated, use the `KEYOPT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_KEYOPT.html>`_\
        command in PREP7.

        **Distributed-Memory Parallel (DMP) Restriction --**\ This command is
        not supported in a DMP solution.

        This is an action command (that creates or deletes surface meshes) and
        is serial in nature. Even if a DMP solution is running, the `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        command runs serially.
        """
        command = f"RSURF,{options},{delopts},{etnum},{dkey}"
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
        toler: str = "",
        **kwargs,
    ):
        r"""Defines symmetry, rotation, or extrusion parameters for the radiosity method.

        Mechanical APDL Command: `RSYMM <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_

        Parameters
        ----------
        option : str
            Command options:

            * ``CLEAR`` - Deletes all symmetry/extrusion definitions. Other
              command options are ignored.

            * ``DEFINE`` - Defines the symmetry/extrusion definition
              (default).

            * ``STAT`` - Shows the status/listing. Other command options are
              ignored.

            * ``COND`` - Activates or deactivates condensation for all
              defined radiation symmetries/extrusions, which reduces the
              size of the radiosity equation system (see `Figure 19: Usage
              Example: Option\ = COND
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#cmd_rsymm_fig1>`_).
              Default is off.

              .. note::

                 **Note:**\ Condensation via `RSYMM
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_,COND
                 is not recommended as the most efficient solution for
                 symmetric models. To best leverage model symmetry to
                 improve efficiency, use view factor condensation via
                 the `VFCO
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFCO.html>`_\
                 command, which condenses the view factor matrix in
                 addition to simplifying the radiosity equations (see
                 `Considerations for View Factor Condensation
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#RSYMM_VFCO_notes>`_
                 for details).

        cs : str
            Local coordinate system ((see command documentation for
            equation) 11) as defined using the `LOCAL
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_LOCAL.html>`_\
            or `CS
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_CS.html>`_\
            commands or the global coordinate system (0). For planar
            reflection, the coordinate system origin must be on the plane of
            symmetry (POS) and one of its axes must be normal to the POS.
            For cyclic reflection, the coordinate system origin must be
            coincident with the center of rotation (COR). Only Cartesian
            systems are valid.

        axis : str
            Axis label of the coordinate system (``CS``) that is normal to
            the POS for planar reflection, or label to indicate the type of
            extrusion. For cyclic reflection, this field must be blank, and
            it is assumed that the Z axis is aligned with the axis of
            rotation.

            * ``X, Y, or Z`` - Planar reflection. For 2D model planar
              reflections, valid labels are X or Y. For 3D model planar
              reflections, valid labels are X, Y, or Z.

            * ``ZEXT`` - Linear extrusion of a line element in the X-Y
              plane, in the Z direction, to create 4-noded `SURF252
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_
              elements. ``NSECT``\ indicates how many elements will be
              created. ``SVAL``\ is the starting Z value, and ``EVAL``\ is
              the ending Z value. ``CS``\ must be 0.

            * ``CEXT`` - Circumferential extrusion (theta direction) around
              the global Y-axis. A 2-noded line element in the X-Y plane is
              extruded to create 4-noded `SURF252
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_
              elements. ``NSECT``\ indicates how many elements will be
              created. ``SVAL``\ is the starting angle, and EVAL is the
              ending angle (in degrees). The angles are with respect to the
              global X-axis. ``CS``\ must be 0.

            * ``(blank)`` - Cyclic reflection.

        nsect : str
            Number of cyclic reflections to be done, or number of elements
            in the extrusion direction.

            For planar reflection, this field must be 0 or blank.

            For cyclic reflection, this field must be ≥ 1 or ≤ -1. Use a
            positive value if you want the sector angle to be computed
            automatically. Use a negative value if you want the sector angle
            to be computed manually. See `Notes
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#rsymm.notes>`_
            for details.

        condvalue : str
            Condensation key. Valid only when ``Option``\ = COND.

            * ``ON`` - Activates condensation in the radiosity solver for
              all defined radiation symmetries/extrusions.

            * ``OFF`` - Deactivates condensation in the radiosity solver for
              all defined radiation symmetries/extrusions (default).

        sval : str
            Starting and ending Z values (if ``Axis``\ = ZEXT) or angle
            values (if ``Axis``\ = CEXT) used for the extrusion. Not used
            for planar or cyclic reflection.

        eval_ : str
            Starting and ending Z values (if ``Axis``\ = ZEXT) or angle
            values (if ``Axis``\ = CEXT) used for the extrusion. Not used
            for planar or cyclic reflection.

        toler : str
            Tolerance dimension used when generating radiosity surface
            elements (`SURF251
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_/`SURF252
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_)
            for planar or cyclic reflection. Defaults to 1.E-7 for planar
            reflection and 1.E-5 for cyclic reflection. If ``TOLER``\ is
            blank or less than or equal to zero, the default tolerance value
            is used. If you encounter an warning stating that the planar (or
            cyclic) symmetry surface intersects the initial patch and the
            symmetric radiation surfaces are not created as expected,
            increase ``TOLER``\ to a positive number larger than the default
            value. Not used for extrusion (ZEXT and CEXT).

            .. note::

               **Note:**\ Increase ``TOLER``\ with caution to allow only
               small offsets. Too large an offset can cause view factor
               errors.

        Notes
        -----

        .. _RSYMM_notes:

        The `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        command is used to define the plane of symmetry (POS) for planar
        reflection or the center of rotation (COR) for cyclic reflection. It can
        also be used to set parameters for a linear or circumferential
        extrusion. The input provided on this command is used to generate
        radiosity surface elements (`SURF251
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_/`SURF252
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_)
        when the `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        command is issued.

        The `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        command must be issued before `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_,
        and it may be issued multiple times to have more than one planar/cyclic
        reflection or extrusion. The `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        command processes `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        commands in the order they are issued.

        For planar reflection, you must define a local coordinate system ((see
        command documentation for equation) 11) with its origin on the POS. One
        of its axes (``Axis``) must be aligned so that it is normal to the
        plane. If possible, use the existing global coordinate system (0). A
        small amount of offset is permissible in cases where the local
        coordinate system, ``CS``, slightly penetrates inside the surface of an
        element. Increasing the tolerance (``TOLER``) will allow the symmetry
        surfaces to be generated with a greater overlap. Planar reflected nodes
        can be created provided that the x-coordinates, x′, in the local system,
        ``CS``, of *all*\ reflected nodes satisfy the equation: x′ > -``TOLER``.
        Alternatively, y′ > -``TOLER``, or z′ > -``TOLER``, depending on which
        coordinate is designated as ``Axis``. See `Figure 12: Usage Example:
        Planar Reflection with TOLER\
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#cmd_rsymm_toler_planar>`_
        for an example of ``TOLER``\ usage.

        For cyclic reflection, ``NSECT``\ is used as follows:

        (see command documentation for equation)

        (see command documentation for equation)

        where θ:sub:`max`\ and θ:sub:`min`\ are computed internally based on the
        location of the RDSF (surface-to-surface radiation) flagged surfaces.
        See `Figure 13: Usage Example: Positive and Negative NSECT\ Values
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#cmd_rsymm_fig2>`_
        for an example of ``NSECT``\ usage.

        For cyclic reflection, you must define a local coordinate system ((see
        command documentation for equation) 11) with its origin coincident with
        the COR. Reflections occur about the local Z-axis in the
        counterclockwise direction. You must align the Z-axis properly. If
        possible, use the existing global coordinate system (0). A small amount
        of offset is permissible in cases where the local coordinate system is
        not coincident with the COR. Cyclically reflected nodes/elements can be
        created provided that the sector angle (in radians) in the local system,
        ``CS``, satisfies the equation: (see command documentation for equation)
        \*(``NSECT``\ +1)/2\*𝛑) - 1.0 < ``TOLER``. See `Figure 14: Usage
        Example: Cyclic Reflection with TOLER\
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#cmd_rsymm_toler_cyclic>`_
        for an example of ``TOLER``\ usage.

        For linear or circumferential extrusion (``Axis``\ = ZEXT or CEXT), you
        must ensure that the extruded area matches the area of the underlying
        element; otherwise, the results may not be correct. For example, in the
        case of `PLANE55
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_PLANE55.html>`_
        elements with a planar depth = 10, use ``Axis``\ = ZEXT and set
        ``SVAL``\ and ``EVAL``\ such that ``EVAL``\ - ``SVAL``\ = 10. Likewise,
        for axisymmetric `PLANE55
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_PLANE55.html>`_
        elements, use ``Axis``\ = CEXT and set ``SVAL``\ and ``EVAL``\ such that
        ``EVAL``\ - ``SVAL``\ = 360. You must also issue `V2DOPT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_V2DOPT.html>`_,1
        for the axisymmetric case. See `Figure 15: Usage Example: Extrusions
        with Axis\ = ZEXT and CEXT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html#cmd_rsymm_fig3>`_
        for extrusion examples.

        The ``Axis``\ = ZEXT and CEXT options are not valid for `SHELL131
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SHELL131.html>`_
        and `SHELL132
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SHELL132.html>`_
        elements.

        New surface elements generated by the `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        command inherit the properties of the original elements.

        For 2D axisymmetric models, `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        can be used only for symmetrization in the YR plane. It cannot be used
        for the theta direction. Use `V2DOPT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_V2DOPT.html>`_\
        in that case.

        For 2D axisymmetric YR models, the newly-generated nodes can have only
        positive X coordinates.

        *Figure 12: Usage Example: Planar Reflection with TOLER*

        *Figure 13: Usage Example: Positive and Negative NSECT Values*

        *Figure 14: Usage Example: Cyclic Reflection with TOLER*

        *Figure 15: Usage Example: Extrusions with Axis = ZEXT and CEXT*

        **Considerations for View Factor Condensation**

        View factor condensation via the `VFCO
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFCO.html>`_\
        command is the recommended method to improve solution efficiency for
        models with symmetry, which are defined with the `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        command.

        When the `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_\
        command is used, it implies that some radiation facets (`SURF251
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_
        or `SURF252
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_)
        created by the `RSURF
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
        command will be a reflection of others. By definition, radiation facets
        with an underlying solid element are independent facets. Dependent
        facets are copies of the independent facets having the same dimensions
        but at different locations. The following figures illustrate solid
        elements (grey) and independent (blue) and dependent (red) facets for
        models with different types of symmetry. View factor condensation
        improves efficiency by condensing the view factor matrix to calculate
        view factors only for independent facets (`View Factor Matrix for a
        Model with Symmetry
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_thry/thy_heat1.html#thry_heatflo_symm_view_factor>`_)
        and simplifying the radiosity equations to solve only for the
        independent radiosity flux (`Radiosity Equations Simplified for Models
        with Symmetry in the Theory Reference
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_thry/thy_heat5.html#thy_radiosity_simplified_symmetry>`_).
        For an illustrative example, see `Example of a 3D Open Enclosure with
        Symmetry: Radiation Analysis with Condensed View Factor Calculation in
        the Thermal Analysis Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/the_example_rad_condensedVF.html>`_.

        *Figure 16: Independent and Dependent Facets in a Model with Planar
        Symmetry Employing View Factor Condensation*

        *Figure 17: Independent and Dependent Facets in a Model with Cyclic
        Symmetry Employing View Factor Condensation*

        *Figure 18: Independent and Dependent Facets for a Model Built by
        Extrusions Employing View Factor Condensation*

        Although it is not the recommended method, the following figure
        illustrates condensation via `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_,COND.
        The efficiency gains by condensation via `RSYMM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSYMM.html>`_,COND
        are less than those obtained with view factor condensation via the `VFCO
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFCO.html>`_\
        command, which reduces the view factor matrix in addition to simplifying
        the radiosity equations, as described in `View Factor Matrix for a Model
        with Symmetry
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_thry/thy_heat1.html#thry_heatflo_symm_view_factor>`_
        and `Radiosity Equations Simplified for Models with Symmetry in the
        Theory Reference
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_thry/thy_heat5.html#thy_radiosity_simplified_symmetry>`_.

        *Figure 19: Usage Example: Option = COND*

        **Distributed-Memory Parallel (DMP) Restriction --**\ This command is
        not supported in a DMP solution.

        **Example Usage**

        `2D Radiation Analysis Using the Radiosity Method with Decimation and
        Symmetry
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_THE4_10.html#the_rad_rsymm_2Dradiosity_symmetry>`_

        `3D Open Enclosure with Symmetry: Radiation Analysis with Condensed View
        Factor Calculation
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/the_example_rad_condensedVF.html>`_
        """
        command = (
            f"RSYMM,{option},{cs},{axis},{nsect},{condvalue},{sval},{eval_},{toler}"
        )
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

    def vfdi(
        self,
        opt: str = "",
        enclosure: str = "",
        diagtype: str = "",
        realdata1: str = "",
        realdata2: str = "",
        **kwargs,
    ):
        r"""Specifies view factor diagnostic options.

        Mechanical APDL Command: `VFDI <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFDI.html>`_

        **Command default:**

        No diagnostic information is written.

        Parameters
        ----------
        opt : str
            Diagnostic option:

            * ``0`` - Do not write diagnostic information (default).

            * ``1`` - Write diagnostic information to the database file
              ``Jobname.db``.

            * ``2`` - Write diagnostic information to a separate view factor
              diagnosis file ``Jobname.vfd``.

            * ``3`` - Combine options 1 and 2 so that diagnostic information
              is written in both the ``Jobname.db``\ and the
              ``Jobname.vfd``\ files.

            * ``STAT`` - Print all specfied values for `VFDI
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFDI.html>`_\
              command arguments (``Opt``, ``ENCLOSURE``,
              ``DIAGTYPE``,``REALDATA1``, ``REALDATA2``)

        enclosure : str
            Specifies enclosure number to diagnose. (Enclosure number is set
            using the `SF
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SF.html>`_,
            `SFA
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SFA.html>`_,
            `SFE
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SFE.html>`_,
            or `SFL
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SFL.html>`_\
            command with ``LAB``\ = RDSF.)

            * ``0`` - Diagnose all enclosures (default).

            * ``>0`` - Enclosure number to diagnose.

        diagtype : str
            Specifies diagnostic type.

            * ``1`` - View factor sum diagnostic. Creates an element
              component to be written to ``Jobname.db``\ and/or
              ``Jobname.vfd``\ for rows that have a view factor sum equal to
              a value that is within the minimum and maximum view factor sum
              specified by ``REALDATA1``\ and ``REALDATA2``, respectively.
              If the sum is outside of this range, nothing is written. The
              element component name is "_ENCLOS_``n``\ ", where ``n``\ is
              the enclosure number.

        realdata1 : str
            For the view factor sum diagnostic (``DIAGTYPE``\ = 1), this
            specifies the minimum view factor sum (default = -0.01).

        realdata2 : str
            For the view factor sum diagnostic (``DIAGTYPE``\ = 1), this
            specifies the maximum view factor sum (default = 1.1).

        Notes
        -----

        .. _VFDI_notes:

        The `VFDI
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFDI.html>`_\
        command specifies a view factor diagnostic tool that is valid for
        radiation analyses using the `radiosity solver method
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_THE4_7.html>`_.
        It can be used to provide debugging information on the view factor
        matrix when you must restart an analysis after an unconverged solution.
        The command writes information to the ``Jobname.db``\ and/or
        ``Jobname.vfd``\ files in the working directory that help identify where
        view factors in a complex model may be causing a solution failure. For
        more information, see `Troubleshooting with View Factor Diagnostics in
        the Thermal Analysis Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_THE4_7.html#VFDiagnosis>`_.

        Issue `VFDI
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFDI.html>`_\
        to specify diagnostic information to be written the next time view
        factors are created and written to the database by a subsequent `VFOPT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFOPT.html>`_,NEW
        or `SOLVE
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SOLVE.html>`_\
        command.

        **Example Usage**

        `Using VFDI\ to Write View Factor Diagnostic Information in the Thermal
        Analysis Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_THE4_7.html#ans_the_rad_VFDIexample>`_
        """
        command = f"VFDI,{opt},{enclosure},{diagtype},{realdata1},{realdata2}"
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

    def vfup(
        self,
        action: str = "",
        opt: str = "",
        opt2: str = "",
        opt3: str = "",
        opt4: str = "",
        **kwargs,
    ):
        r"""Controls view factor updating at the substep level for a coupled-field radiation
        analysis that includes large-deflection effects.

        Mechanical APDL Command: `VFUP <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_

        **Command default:**

        Although the command is not required for solution, if you do not issue
        `VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,
        view factors are not updated at the substep level. Consequently, results
        of thermal radiation modeling may be inaccurate because they do not
        account for changes in the view factors of radiation surfaces as they
        deform or move.

        Parameters
        ----------
        action : str
            Action to be performed:

            * ``DEFINE`` - Define view factor updating parameters (default).

            * ``STAT`` - Print all specified values for `VFUP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_\
              command arguments.

            * ``DEFA`` - Resets all ``Opt``\ options to their default
              values. ``OPT2``, ``OPT3``, and ``OPT4``\ are ignored.

        opt : str
            Option to enable view factor updates at the substep level or
            specify updating criteria.

            * ``ON`` - Enable view factor updates according to the last
              criteria specified by the `VFUP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_\
              command. The default criteria is `VFUP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,,FRQU,1,0
              if you only issue `VFUP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,,ON
              without issuing another `VFUP
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_\
              command to choose between frequency-based (``Opt``\ = FRQU) or
              kinematic-based criteria (``Opt``\ = KNEX, KNIM, or KNI1).
              ``OPT2``, ``OPT3``, and ``OPT4``\ are ignored.

            * ``OFF`` - Do not update view factors at the substep level
              (default). ``OPT2``, ``OPT3``, and ``OPT4``\ are ignored.

            * ``FRQU`` - Key to specify a desired value for the substep
              frequency (``OPT2``) and the pass frequency (``OPT3``) at
              which view factors are updated. For guidelines on setting
              these values and example command usage, see `Controlling the
              frequency of view factor updates
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPfreq>`_.
              ``OPT4``\ is ignored.

            * ``KNEX`` - Key to specify kinematic-based view factor updating
              at the end of a substep. The program tests all radiation
              facets and updates view factors only if the relative change in
              facet spacing, area, or angle exceeds a threshold specified by
              ``OPT2``, ``OPT3``, and ``OPT4``. For details on how these
              values are calculated, see the table and figures below and
              `Kinematic-based algorithm
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
              in the notes. For guidelines on the timing of view factor
              updates, see `Controlling the frequency of view factor updates
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPfreq>`_.

            * ``KNIM`` - Key to specify kinematic-based view factor updating
              within the radiation multipass loop, after the Newton-Raphson
              (RP) loop has produced a converged coupled-field solution. The
              program tests all radiation facets and updates view factors
              only if the relative change in facet spacing, area, or angle
              exceeds a threshold specified by ``OPT2``, ``OPT3``, and
              ``OPT4``. For details on how these values are calculated, see
              the table and figures below and `Kinematic-based algorithm
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
              in the notes. For guidelines on the timing of view factor
              updates, see `Controlling the frequency of view factor updates
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPfreq>`_.

            * ``KNI1`` - Key to specify kinematic-based view factor updating
              within the first radiation multipass loop, after the
              Newton-Raphson (RP) loop has produced a converged
              coupled-field solution. The program tests all radiation facets
              and updates view factors only if the relative change in facet
              spacing, area, or angle exceeds a threshold specified by
              ``OPT2``, ``OPT3``, and ``OPT4``. For details on how these
              values are calculated, see the following table and figures and
              `Kinematic-based algorithm
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
              in the notes. For guidelines on the timing of view factor
              updates, see `Controlling the frequency of view factor updates
              <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPfreq>`_.

        opt2 : str
            Command argument ``OPT2``. Refer to the `VFUP command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_
            for option-specific definitions.

        opt3 : str
            Command argument ``OPT3``. Refer to the `VFUP command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_
            for option-specific definitions.

        opt4 : str
            Command argument ``OPT4``. Refer to the `VFUP command
            documentation
            <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_
            for option-specific definitions.

        Notes
        -----

        .. _VFUP_notes:

        .. list-table:: Table 254: Definitions of OPT2, OPT3, and OPT4 for different Opt labels
           :header-rows: 1

           * - ``Opt``\ label
             - ``OPT2``\
             - ``OPT3``\
             - ``OPT4``\
           * - FRQU (frequency-based updating)
             - Substep frequency for view factor updates. This value must
               be a positive integer (default = 1). If ``OPT2``\ = 3,
               view factors are updated every third substep.
             - Valid values are -1, 0, or a positive integer (default =
               0).If ``OPT3``\ = -1, view factors are updated only in the
               first pass of the multipass loop in the substeps that view
               factors are being updated (specified by ``OPT2``).If
               ``OPT3``\ = 0, view factors are not updated in the
               radiation multipass loop.If ``OPT3``\ is a positive
               integer, it specifies the pass frequency for view factor
               updates in the multipass loop.
             - Ignored
           * - If ``OPT3``\ = -1, view factors are updated only in the
               first pass of the multipass loop in the substeps that view
               factors are being updated (specified by ``OPT2``).
             - -
             - -
             - -
           * - If ``OPT3``\ = 0, view factors are not updated in the
               radiation multipass loop.
             - -
             - -
             - -
           * - If ``OPT3``\ is a positive integer, it specifies the pass
               frequency for view factor updates in the multipass loop.
             - -
             - -
             - -
           * - KNEX, KNIM, or KNI1 (kinematic-based updating)
             - Relative change in facet spacing threshold (default =
               0.05). Set ``OPT2``\ = 0 to ignore this threshold test.
             - Relative change in facet area threshold (default = 0.05).
               Set ``OPT3``\ = 0 to ignore this threshold test.
             - Relative change in facet angle threshold (default = 0.05).
               Set ``OPT4``\ = 0 to ignore this threshold test.
           * - 2-surface test: view factors update if (see command
               documentation for equation) ``OPT2``\
             - 2-surface test: view factors update if (see command
               documentation for equation) ``OPT3``\
             - 2-surface test: view factors update if (see command
               documentation for equation) ``OPT4``\ (see command
               documentation for equation) (see command documentation for
               equation)
             - -
           * - 1-surface test: view factors update if (see command
               documentation for equation) ``OPT2``\
             - 1-surface test: view factors update if (see command
               documentation for equation) ``OPT3``\
             - 1-surface test: view factors update if (see command
               documentation for equation) ``OPT4``\
             - -

        The following figure depicts the values used in kinematic-based tests to
        determine if thresholds are surpassed and view factors must be updated.
        There are two tests: a 2-surface test and a 1-surface test. The formulas
        for each of these tests are listed in the previous table, and the
        variables in these formulas are explained in the following figures. For
        a detailed description of the algorithm used to test all radiation
        surfaces and determine if thresholds are exceeded, see `Kinematic-based
        algorithm
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
        in the notes.

        *Figure 33: Definition of Values Used in 2-surface (A) and 1-surface (B)
        Kinematic-based Tests*

        RefLength in the denominator of the 1-surface facet spacing threshold
        test is a length scale representative of the radiation facet spacing for
        an enclosure. It is automatically calculated by putting a bounding box
        on the radiation facets and computing the diagonal of the bounding box.
        RefLength is dynamic and updates when view factors are updated. See the
        following figure for a depiction of how RefLength is computed.

        *Figure 34: Example Demonstrating How RefLength is Calculated*

        For details on how the kinematic-based thresholds are tested to
        determine if view factors are updated, see `Kinematic-based algorithm
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
        in the notes.

        Deformation and/or motion of radiating surfaces during an anlysis can
        cause inaccuracies in radiation calculations if the view factors are not
        updated to account for these changes. Issue `VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,ON
        to enable view factor updates at the substep level and improve
        simulation accuracy for an analysis that includes all of the following
        conditions:

        * Thermal radiation modeling using the `radiosity solver method
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/Hlp_G_THE4_7.html>`_.

        * Coupled-field elements (`PLANE222
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_PLANE222.html>`_,
          `PLANE223
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_PLANE223.html>`_,
          `SOLID225
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SOLID225.html>`_,
          `SOLID226
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SOLID226.html>`_,
          or `SOLID227
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SOLID227.html>`_)
          having at least structural and thermal degrees of freedom (DOFs).

        * Large-deflection effects (`NLGEOM
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_NLGEOM.html>`_,ON).

        Updates occur only if all of these conditions are met:

        * `VFUP
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,ON
          has been issued.

        * `NLGEOM
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_NLGEOM.html>`_,ON
          has been issued.

        * You have specified KEYOPT(1) = 1 for any surface elements (`SURF251
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF251.html>`_
          or `SURF252
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_SURF252.html>`_)
          that have been generated via the `RSURF
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RSURF.html>`_\
          command.

        When view factor updating is enabled (`VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,,ON),
        radiation facet areas are recalculated along with the view factors
        according to the specified criteria. To specify the updating criteria,
        you must re-issue the `VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_\
        command and choose one of the following:

        * frequency-based criteria (``Opt``\ = FRQU) to have updates occur at
          defined substep (``OPT2``) and pass (``OPT3``) frequencies, regardless
          of geometric changes to radiation facets,

          or

        * kinematic-based criteria (``Opt``\ = KNEX, KNIM, or KNI1) to have
          updates occur only if relative changes in facet spacing, areas, or
          angles exceed thresholds defined by ``OPT2``, ``OPT3``, and ``OPT4``,
          respectively.

        **Controlling the frequency of view factor updates**

        The full solution method (`THOPT
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_THOPT.html>`_,FULL)
        with radiosity has three nested loops, which occur for each load step:
        the substep (or time step) loop, the multipass loop, and the
        Newton-Raphson (NR) loop. Displacements and temperatures, in addition to
        any other DOFs that may be included in your coupled-field analysis, are
        computed in the NR loop. The view factors / radiation areas can be
        recalculated at different points during the solution, as depicted in
        `Figure 35: View Factor Update Timing
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPtiming>`_.
        There are three timing strategies, Explicit, Implicit, and Implicit-1,
        and the implications of each timing strategy are detailed in the
        following discussion.

        *Figure 35: View Factor Update Timing*

        As seen in the figure, implicit updates occur within the multipass loop,
        and updated view factors are used in the current substep. Instead,
        explicit updates occur at the end of the time step, and updated view
        factors are used in the next time step. An additional update occurs
        before entering the substep loop for a restart (`ANTYPE
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_ANTYPE.html>`_,,
        RESTART) or if you have imposed initial conditions on the displacements
        (`IC
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_IC.html>`_)
        as indicated.

        There is a trade-off between accuracy and computational cost as updating
        the view factors at the substep level improves accuracy but also
        increases the solution time. To control the timing of view factor
        updates and whether updates are based on geometric changes to the
        radiation facets due to kinematic motion or deformation during solution,
        you must choose one of these options:

        * ``Opt``\ = FRQU: Specify the substep (``OPT2``) and pass (``OPT3``)
          frequency at which view factor updates occur. Updates happen at the
          specified frequency, regardless of whether deformation or motion
          causes significant changes to the radiation facets.

        * ``Opt``\ = KNEX, KNIM, or KNI1: The view factors are updated only if
          changes in the radiation facets due to motion/deformation exceed a
          specified threshold (``OPT2``, ``OPT3``, or ``OPT4``). As shown in
          `Figure 35: View Factor Update Timing
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPtiming>`_
          and described in detail below, the difference between these
          kinematic-based update options is when the testing and updates occur.

        There are three timing strategies:

        * **Explicit**\ - View factors are updated at the end of a substep after
          a converged coupled-field solution is achieved, and the updated view
          factors are used in the next time step.

          For ``Opt``\ = FRQU - You chose the explicit strategy by setting
          ``OPT3``\ = 0, and the value specified for the substep frequency,
          ``OPT2``, determines which substeps include view factor updating. By
          default, ``OPT2``\ = 1, and view factors are updated at the end of
          every substep.

          .. list-table::

             * - For example, if you issue:
               - View factors are updated
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,FRQU,3,0
               - at the end of substeps 3,6,9,...

          For ``Opt``\ = KNEX - At the end of every substep, the facets are
          tested (see `Kinematic-based algorithm
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
          for details) and view factors updated only if one of the three
          kinematic-based thresholds (``OPT2``, ``OPT3``, ``OPT4``) are
          exceeded.

          .. list-table::

             * - For example, if you issue:
               - Radiation facets are tested and view factors are
                 updated
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,KNEX
               - at the end of every substep. Updates occur only if one
                 of three kinematic-based thresholds (facet spacing,
                 area, or angle) exceeds the default value of 0.05
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,KNEX,0.1,,0
               - at the end of every substep. Updates occur only if the
                 relative change in facet spacing threshold exceeds 0.1
                 or the relative change in facet area exceeds the
                 default value of 0.05.

          Explicit is the most stable timing strategy. If you have convergence
          difficulties, explicit updates are recommended. For an accurate
          solution, the substep size must be small. Explicit updates may lead
          to an energy imbalance in the radiosity solution since the view
          factor facet areas were calculated in the preceding time step. For
          further details, see the discussion related to `Figure 39: View
          Factor Updates and Reciprocity
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPrec>`_.

        * **Implicit**\ - View factors are updated within the radiation
          multipass loop, after the Newton-Raphson (RP) loop has produced a
          converged coupled-field solution, and are used in the current pass and
          substep.

          For ``Opt``\ = FRQU - The value of the pass frequency, ``OPT3``,
          determines which passes will update the view factors. To have
          implicit view factor updating, you must set ``OPT3``\ to something
          other than its default value of zero.

          .. list-table::

             * - For example, if you issue:
               - View factors are updated
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,FRQU,5,3
               - in passes 3,6,9,... for substeps 5,10,15...

          For ``Opt``\ = KNIM - The testing and view factor updating if a
          kinematic-based threshold is exceeded (see `Kinematic-based
          algorithm
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
          for details) occurs within the radiation multipass loop, after the
          Newton-Raphson (RP) loop has produced a converged coupled-field
          solution. Updated view factors are used in the current pass and
          substep.

          .. list-table::

             * - For example, if you issue:
               - Radiation facets are tested and view factors are
                 updated
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,KNIM
               - in every pass for every substep. Updates occur only if
                 one of three kinematic-based thresholds (facet
                 spacing, area, or angle) exceeds the default value of
                 0.05
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,KNIM,0.1,0,0.1
               - in every pass for every substep. Updates occur only if
                 the relative change in the facet spacing or angle
                 threshold exceeds 0.1.

          Implicit updates are useful when you have strong nonlinearities,
          strong structural-thermal coupling, or rapid changes in surface
          geometry. However, implicit updates can be computationally expensive
          as view factors are recalculated multiple times within a single
          substep. Also, Implicit updates of view factors can lead to
          instabilities and convergence difficulties.

        * **Implicit-1**\ - View factor updating occurs onlly in the first pass
          of the radiation multipass loop.

          For ``Opt``\ = FRQU - View factors are updated in the substeps
          prescribed by the value of the substep frequency, ``OPT2``, but they
          are updated only in the first pass of the radiation multipass loop.
          To have implicit-1 view factor updating, specify -1 for ``OPT3``.

          .. list-table::

             * - For example, if you issue:
               - View factors are updated
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,
                 DEFINE, FRQU, 5, -1
               - only in pass 1 for substeps 5,10,15...

          For ``Opt``\ = KNI1 - The facet testing and view-factor updating if
          a kinematic-based threshold is exceeded (see `Kinematic-based
          algorithm
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#VFUP_kinAlg>`_
          for details) occurs only within the first pass of the radiation
          multipass loop, after the Newton-Raphson (RP) loop has produced a
          converged coupled-field solution.

          .. list-table::

             * - For example, if you issue:
               - Radiation facets are tested and view factors are
                 updated
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,KNI1
               - in the first pass for every substep. Updates occur
                 only if one of three kinematic-based thresholds (facet
                 spacing, area, or angle) exceeds the default value of
                 0.05
             * - `VFUP
                 <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,KNI1,0.1,0,0
               - in the first pass for every substep. Updates occur
                 only if the relative change in the facet spacing
                 threshold exceeds 0.1.

          Use this timing strategy when the motion of bodies in your model is
          completely specified, as in rigid body motion (translation and
          rotation). It is most efficient and accurate to update the view
          factors in the first pass only when the NR loop achieves a converged
          structural solution in the first pass and the structural solution
          does not change for subsequent passes.

        **Kinematic-based algorithm**

        For ``Opt``\ = KNEX, KNIM, or KNI1, the kinematic-based criteria are
        used in the algorithm depicted below to test and update view factors.

        *Figure 36: Kinematic-based Algorithm*

        In most practical situations, S:sub:`2`\ will be found and the 2-surface
        test will be done. In some situations, when the facet only radiates to
        the environment, the 1-surface test is required. Two examples of when a
        1-surface test is encountered are shown in the following figure. For a
        2D square with four radiating surfaces around it, the 4x4 view factor
        matrix is zero, and only single surface tests will be done as the body
        translates (A in the figure). The second example (B) is two radiating
        surfaces, one fixed and one rotating. When the rotating surface reaches
        an 180 degree rotation, the view factor matrix becomes zero, and the
        1-surface test will be encountered.

        *Figure 37: Examples Scenarios that Require a 1-Surface Test*

        **Notes on kinematic-based and frequency-based updates**

        Kinematic-based updates (``Opt``\ = KNEX, KNIM, or KNI1) are sensitive
        to motion while frequency-based updates (``Opt``\ = FRQU) are not. For
        example, consider a 2 plate problem with total loadstep time = 100.
        Plate 1 is fixed and plate to moves only from time 10-20.
        Frequency-based updates will occur from time = 0 - 100, but
        kinematic-based updates will occur from time 10-20.

        If an enclosure is undergoing rigid-body translation or rotation, and
        there is no change to the radiation facets:

        * If you are using kinematic-based updates, view factors will not be
          updated if the 2-surface test is encountered. However, if a 1-surface
          surface is encountered, they will be updated.

        * If you are using frequency-based updates, view factors are updated at
          the prescribed frequency regardless of whether or not the radiation
          facets are moving.

        When you have no knowledge about body deformation prior to the
        simulation, kinematic-based updates are a good option since view factor
        updates will only be triggered if the geometry of the radiation surfaces
        move or deform significantly.

        For kinematic-based updating, when bodies are moving away from each
        other, updates occur less often. Vice-versa, when bodies move toward
        each other, updates occur more frequently.

        **Restrictions / limitations**

        **Enclosure status change and penetration must be avoided --**\
        Simulations using the `VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_\
        to update view factors at the substep level are invalid if an enclosure
        status changes or the surface of a radiating body penetrates the surface
        of another radiating body. `Figure 38: Examples of Radiation Problems
        that Undergo an Enclosure Status Change
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPencl>`_
        illustrates some examples of enclosure status changes that must be
        avoided. For example, if two radiating bodies in close proximity
        penetrate each other due to thermal expansion during the analysis, their
        view factors become zero, and results using the `VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_\
        command to update view factors are unpredictable and inaccurate. It is
        better to model bodies within close proximity using thermal contact
        radiation (contact and target elements: `CONTA172
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_CONTA172.html>`_,
        `CONTA174
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_CONTA174.html>`_,
        `CONTA175
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_CONTA175.html>`_,
        `CONTA178
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_CONTA178.html>`_,`TARGE169
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_TARGE169.html>`_,
        and `TARGE170
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_elem/Hlp_E_TARGE170.html>`_).

        You must also be careful to avoid an enclosure status change, for
        example if movement or deformation in the analysis causes an open
        enclosure to become closed or vice versa. If an enclosure is undergoing
        a status change in your analysis, split the load step into multiple load
        steps such that:

        * There is no status change in the individual load steps.

        * `VFSM
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFSM.html>`_\
          settings are appropriate for the enclosure status in individual load
          steps.

        *Figure 38: Examples of Radiation Problems that Undergo an Enclosure
        Status Change*

        **View factor Updates and Reciprocity --**\ For explicit updates, view
        factors are recalculated at the end of the substep and applied in the
        next substep. Consequently, they violate the reciprocity rule in the
        next substep as the radiating areas change since the view factors were
        calculated from the areas of the previous substep. This may lead to
        energy imbalance issues. The same problem exists if you specify a
        substep (``OPT2``) or pass (``OPT3``) frequency other than one. `Figure
        39: View Factor Updates and Reciprocity
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPrec>`_
        illustrates this issue for different updating strategies. Reciprocity /
        row sum properties are only satisfied in substeps where view factors are
        updated in every pass (``OPT3``\ = 1) provided you have used the `VFSM
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFSM.html>`_\
        command appropriately (see `View Factors in the Theory Reference
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_thry/thy_heat1.html#heaviewfact>`_).

        *Figure 39: View Factor Updates and Reciprocity*

        **Supported/restricted commands at the substep level with VFUP,DEFINE,ON**

        The following commands are not supported at the substep level:

        * `VFOPT
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFOPT.html>`_\

        * `THOPT
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_THOPT.html>`_,QUASI

        * `VFDI
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFDI.html>`_\

        The following commands may be used to query and print view factors or
        average view factors at the substep level:

        * View factor queries (`VFQUERY
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFQUERY.html>`_)
          are based on the last update.

        * Any `\*GET
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_GET.html>`_\
          command with ``Entity``\ = RAD is based on the last view factor
          update. To retrieve the latest average view factor, issue `\*GET
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_GET.html>`_,``Par``,RAD,0,VFAVG.

        * To print view factors to the output file at the substep level, issue
          `MPRINT
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_MPRINT.html>`_\
          before `SOLVE
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SOLVE.html>`_.

        The following radiation commands are valid at the substep level, and may
        be used with view factor updating enabled (`VFUP
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html>`_,DEFINE,ON):

        * `HEMIOPT
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_HEMIOPT.html>`_,
          `RADOPT
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_RADOPT.html>`_,
          `V2DOPT
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_V2DOPT.html>`_,
          `SPCTEMP
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SPCTEMP.html>`_,
          `SPCNOD
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_SPCNOD.html>`_,
          and `VFCO
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFCO.html>`_\

        * Settings on the `VFSM
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFSM.html>`_\
          command to adjust view factors (view factor smoothing) for different
          enclosures are valid for all substeps. However, if there is an
          enclosure status change during a load step, `VFSM
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFSM.html>`_\
          settings may become inappropriate and results inaccurate. See earlier
          discussion on inaccurate results if motion or deformation causes an
          enclosure status change (`Figure 38: Examples of Radiation Problems
          that Undergo an Enclosure Status Change
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFUP.html#ans_cmdVFUPencl>`_).
          To model a situation where deformation changes the enclosure status,
          you must solve the problem in multiple load steps and change `VFSM
          <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_cmd/Hlp_C_VFSM.html>`_\
          settings in each load step to accurately model the state of the
          enclosure.

        **Example Usage**

        `Example of a Structural-Thermal Analysis with Substep-Level View Factor
        Updating in the Thermal Analysis Guide
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_the/the_radExVFUP.html>`_

        `VM321 in the Ansys Mechanical APDL Verification Manual
        <https://ansyshelp.ansys.com/public/Views/Secured/corp/v261/en/ans_vm/Hlp_V_VM321.html>`_
        """
        command = f"VFUP,{action},{opt},{opt2},{opt3},{opt4}"
        return self.run(command, **kwargs)
