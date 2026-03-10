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

from ansys.mapdl.core._commands import CommandsBase, parse


class ElementType(CommandsBase):

    def dof(
        self,
        lab1: str = "",
        lab2: str = "",
        lab3: str = "",
        lab4: str = "",
        lab5: str = "",
        lab6: str = "",
        lab7: str = "",
        lab8: str = "",
        lab9: str = "",
        lab10: str = "",
        **kwargs,
    ):
        r"""Adds degrees of freedom to the current DOF set.

        Mechanical APDL Command: `DOF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_DOF.html>`_

        **Command default:**

        .. _DOF_default:

        Use degree of freedom set determined from element types.

        Parameters
        ----------
        lab1 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab2 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab3 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab4 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab5 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab6 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab7 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab8 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab9 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        lab10 : str
            Valid labels are: UX, UY, UZ (structural displacements); ROTX, ROTY, ROTZ (structural
            rotations); TEMP, TBOT, TE2, TE3,..., TTOP (temperatures); PRES (pressure); VOLT (voltage); MAG
            (magnetic scalar potential); AZ (magnetic vector potential); CURR (current); EMF (electromotive
            force drop); CONC (concentration); DELETE.

        Notes
        -----

        .. _DOF_notes:

        The degree of freedom (DOF) set for the model is determined from all element types defined. This
        command may be used to add to the current set. The ALL label may be used on some commands to
        represent all labels of the current degree of freedom set for the model. Issue the :ref:`dof`
        command with no arguments to list the current set. Use the DELETE label to delete any previously
        added DOFs and return to the default DOF set.

        **Product Restrictions**

        .. _DOFprodRest:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"DOF,{lab1},{lab2},{lab3},{lab4},{lab5},{lab6},{lab7},{lab8},{lab9},{lab10}"
        return self.run(command, **kwargs)

    def et(
        self,
        itype: str = "",
        ename: str = "",
        kop1: str = "",
        kop2: str = "",
        kop3: str = "",
        kop4: str = "",
        kop5: str = "",
        kop6: str = "",
        inopr: str = "",
        **kwargs,
    ):
        r"""Defines a local element type from the element library.

        Mechanical APDL Command: `ET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ET.html>`_

        Parameters
        ----------
        itype : str
            An arbitrary local element-type number. Defaults to 1 + current maximum.

        ename : str
            A full element name (such as

            .. code:: apdl

               pipe288

            ) or element number only (such as

            .. code:: apdl

               288

            ), as given in the `element library
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_USER300.html>`_.

        kop1 : str
            KEYOPT values (1 through 6) as desired for the specified element.

        kop2 : str
            KEYOPT values (1 through 6) as desired for the specified element.

        kop3 : str
            KEYOPT values (1 through 6) as desired for the specified element.

        kop4 : str
            KEYOPT values (1 through 6) as desired for the specified element.

        kop5 : str
            KEYOPT values (1 through 6) as desired for the specified element.

        kop6 : str
            KEYOPT values (1 through 6) as desired for the specified element.

        inopr : str
            Specify 1 to suppress all element-solution printout for this element type.

        Notes
        -----
        The ET command selects an element type from the element
        library and establishes it as a local element type for the
        current model.  Information derived from the element type is
        used for subsequent commands, so the ET command(s) should be
        issued early. (The Element Reference describes the available
        elements.)

        A special option, ``ename=0``, permits the specified element
        type to be ignored during solution without actually removing
        the element from the model. Ename may be set to zero only
        after the element type has been previously defined with a
        nonzero Ename.  The preferred method of ignoring elements is
        to use the select commands (such as ESEL).

        KOPn are element option keys. These keys (referred to as
        KEYOPT(n)) are used to turn on certain element options for
        this element. These options are listed under "KEYOPT" in the
        input table for each element type in the Element Reference.
        KEYOPT values include stiffness formulation options, printout
        controls, and various other element options. If KEYOPT(7) or
        greater is needed, input their values with the KEYOPT command.

        The ET command only defines an element type local to your
        model (from the types in the element library). The TYPE or
        similar [KATT, LATT, AATT, or VATT] command must be used to
        point to the desired local element type before meshing.

        To activate the ANSYS program's LS-DYNA explicit dynamic
        analysis capability, use the ET command
        to choose an element that works only with LS-DYNA (such as
        SHELL163).

        Examples
        --------
        Define an element type.  Allow MAPDL to pick your the element
        type.

        >>> etype_num = mapdl.et('', 'SURF154')
        >>> etype_num
        1

        Define an element type while specifying the element type
        number.

        >>> etype_num = mapdl.et(2, 'SOLID186')
        >>> etype_num
        2
        """
        command = (
            f"ET,{itype},{ename},{kop1},{kop2},{kop3},{kop4},{kop5},{kop6},{inopr}"
        )
        return parse.parse_et(self.run(command, **kwargs))

    def etchg(self, cnv: str = "", **kwargs):
        r"""Changes element types to their corresponding types.

        Mechanical APDL Command: `ETCHG <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ETCHG.html>`_

        Parameters
        ----------
        cnv : str
            Converts the element types to the corresponding type. Valid labels are:

            * ``TTS`` - Thermal to Structural

            * ``STT`` - Structural to Thermal

            * ``MTT`` - Magnetic to Thermal

            * ``FTS`` - Fluid to Structural

            * ``ETS`` - Electrostatic to Structural

            * ``ETT`` - Electrical to Thermal

        Notes
        -----

        .. _ETCHG_notes:

        Changes the currently defined element types to their corresponding types. Elements without a
        companion element (listed above) are not switched and should be switched with the :ref:`et` command
        to an appropriate element type or to a null element. The KEYOPT values for the switched element
        types are reset to zero or to their default values. You must check these values to see if they are
        still meaningful. Additionally, if ``Cnv`` = ETI, ITE, or TTE, all real constants are set to zero.

        If ``Cnv`` = ITE, you will need to choose a material model that corresponds to your previously-
        defined material properties. If working interactively, the application prompts you to do so.

        .. _ETCHG_extranote1:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.
        """
        command = f"ETCHG,{cnv}"
        return self.run(command, **kwargs)

    def etcontrol(self, eltech: str = "", eldegene: str = "", **kwargs):
        r"""Control the element technologies used in element formulation (for applicable elements).

        Mechanical APDL Command: `ETCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ETCONTROL.html>`_

        Parameters
        ----------
        eltech : str
            Element technology control:

            * ``SUGGESTION`` - The program offers a suggestion for the best element technology before solving.
              If necessary, mixed u-P (KEYOPT(6)) is also included and reset. This behavior is the default.

            * ``SET`` - The program informs you of the best settings and resets any applicable KEYOPT settings
              automatically. This action overrides any previous manual settings.

            * ``OFF`` - Deactivates automatic selection of element technology. No suggestions are issued, and no
              automatic resetting occurs.

        eldegene : str
            Element degenerated shape control:

            * ``ON`` - If element shapes are degenerated, the degenerated shape function is employed and
              enhanced strain, simplified enhanced strain, and B-bar formulations are turned off (default).

            * ``OFF`` - If element shapes are degenerated, regular shape functions are still used, and the
              specified element technologies (for example, enhanced strain, B-bar, uniform reduced integration)
              are still used.

        Notes
        -----

        .. _ETCONTROL_notes:

        This command is valid for elements ``SHELL181``, ``PLANE182``, ``PLANE183``, ``SOLID185``,
        ``SOLID186``, ``SOLID187``, ``BEAM188``, ``BEAM189``, ``SHELL208``, ``SHELL209``, ``PLANE222``,
        ``PLANE223``, ``SOLID225``, ``SOLID226``, ``SOLID227``, ``REINF264``, ``SOLID272``, ``SOLID273``,
        ``SHELL281``, ``SOLID285``, ``PIPE288``, ``PIPE289``, ``ELBOW290``.

        For more information, see `Automatic Selection of Element Technologies and Formulations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_AutoSelectElems.html#EL2recCriteriaNonLin-3>`_
        """
        command = f"ETCONTROL,{eltech},{eldegene}"
        return self.run(command, **kwargs)

    def etdele(self, ityp1: str = "", ityp2: str = "", inc: str = "", **kwargs):
        r"""Deletes element types.

        Mechanical APDL Command: `ETDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ETDELE.html>`_

        Parameters
        ----------
        ityp1 : str
            Deletes element types from ``ITYP1`` to ``ITYP2`` (defaults to ``ITYP1`` ) in steps of ``INC``
            (defaults to 1). If ``ITYP1`` = ALL, ``ITYP2`` and ``INC`` are ignored and all element types are
            deleted. Element types are defined with the :ref:`et` command.

        ityp2 : str
            Deletes element types from ``ITYP1`` to ``ITYP2`` (defaults to ``ITYP1`` ) in steps of ``INC``
            (defaults to 1). If ``ITYP1`` = ALL, ``ITYP2`` and ``INC`` are ignored and all element types are
            deleted. Element types are defined with the :ref:`et` command.

        inc : str
            Deletes element types from ``ITYP1`` to ``ITYP2`` (defaults to ``ITYP1`` ) in steps of ``INC``
            (defaults to 1). If ``ITYP1`` = ALL, ``ITYP2`` and ``INC`` are ignored and all element types are
            deleted. Element types are defined with the :ref:`et` command.
        """
        command = f"ETDELE,{ityp1},{ityp2},{inc}"
        return self.run(command, **kwargs)

    def etlist(self, ityp1: str = "", ityp2: str = "", inc: str = "", **kwargs):
        r"""Lists currently defined element types.

        Mechanical APDL Command: `ETLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ETLIST.html>`_

        Parameters
        ----------
        ityp1 : str
            Lists element types from ``ITYP1`` to ``ITYP2`` (defaults to ``ITYP1`` ) in steps of ``INC``
            (defaults to 1). If ``ITYP1`` = ALL (default), ``ITYP2`` and ``INC`` are ignored and all element
            types are listed.

        ityp2 : str
            Lists element types from ``ITYP1`` to ``ITYP2`` (defaults to ``ITYP1`` ) in steps of ``INC``
            (defaults to 1). If ``ITYP1`` = ALL (default), ``ITYP2`` and ``INC`` are ignored and all element
            types are listed.

        inc : str
            Lists element types from ``ITYP1`` to ``ITYP2`` (defaults to ``ITYP1`` ) in steps of ``INC``
            (defaults to 1). If ``ITYP1`` = ALL (default), ``ITYP2`` and ``INC`` are ignored and all element
            types are listed.

        Notes
        -----

        .. _ETLIST_notes:

        This command is valid in any processor.
        """
        command = f"ETLIST,{ityp1},{ityp2},{inc}"
        return self.run(command, **kwargs)

    def keyopt(self, itype: str = "", knum: str = "", value: str = "", **kwargs):
        r"""Sets element key options.

        Mechanical APDL Command: `KEYOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KEYOPT.html>`_

        Parameters
        ----------
        itype : str
            Element type number as defined on the :ref:`et` command.

            The following labels are valid input for contact elements:

            * ``CONT`` - Set element key options for all contact element types, ``CONTA172``, ``CONTA174``,
              ``CONTA175``, and ``CONTA177``.

            * ``TARG`` - Set element key options for all target element types, ``TARGE169`` and ``TARGE170``.

            * ``GCN`` - Set element key options for all contact element types used in a `general contact
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_
              definition (that is, all contact elements having a real constant set number = 0).

            See `Notes
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_KEYOPT.html#refsect2_ibn_np5_xv>`_
            Notes for additional ``ITYPE`` input specific to general contact.

        knum : str
            Number of the KEYOPT to be defined (KEYOPT( ``KNUM`` )).

        value : str
            Value of this KEYOPT.

        Notes
        -----

        .. _KEYOPT_notes:

        The :ref:`keyopt` command is an alternative method for inputting element key option (KEYOPT) values
        via the :ref:`et` command. (Issue the :ref:`et` command first to define ``ITYPE`` ).

        The :ref:`keyopt` command is required for inputting key options numbered higher than six (that is, >
        KEYOPT(6)).

        .. _refsect2_kpb_rp5_xv:

        If :ref:`etcontrol`,SET is enabled, key options that you specify via the :ref:`keyopt` command might
        be overridden for many structural elements. For more information, see `Automatic Selection of
        Element Technologies and Formulations
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_AutoSelectElems.html#EL2recCriteriaNonLin-3>`_

        .. _refsect2_ibn_np5_xv:

        Specify ``ITYPE`` = GCN to set element key options for all contact element types used in a `general
        contact <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_
        definition. You can selectively set element key options for multiple contact element types in a
        general contact definition by setting ``ITYPE`` to a valid label (ALL_EDGE, ALL_FACE, ALL_VERT,
        ALL_TOP, or ALL_BOT) or by inputting a node component name with or without a component name
        extension (_EDGE, _FACE, _VERT, _TOP, or _BOT). For more information, see `Defining Non-Default
        Contact Settings
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_nondefset.html#>`_
        """
        command = f"KEYOPT,{itype},{knum},{value}"
        return self.run(command, **kwargs)

    def nsvr(self, itype: str = "", nstv: str = "", **kwargs):
        r"""Defines the number of variables for user-programmable element options.

        Mechanical APDL Command: `NSVR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NSVR.html>`_

        Parameters
        ----------
        itype : str
            Element type number as defined on the :ref:`et` command.

        nstv : str
            Number of extra state variables to save (must be no more than 840).

        Notes
        -----

        .. _NSVR_notes:

        Defines the number of extra variables that need to be saved for user-programmable (system-dependent)
        element options, for example, material laws through user subroutine USERPL. ``ITYPE`` must first be
        defined with the :ref:`et` command.
        """
        command = f"NSVR,{itype},{nstv}"
        return self.run(command, **kwargs)
