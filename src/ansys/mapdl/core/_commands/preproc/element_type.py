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

"""
These PREP7 commands define the type of elements to be used in the model.
"""
from typing import Optional, Union

from ansys.mapdl.core._commands import parse
from ansys.mapdl.core.mapdl_types import MapdlInt


class ElementType:
    def dof(
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
        lab10="",
        **kwargs,
    ):
        """Adds degrees of freedom to the current DOF set.

        APDL Command: DOF

        Parameters
        ----------
        lab1, lab2, lab3, . . . , lab10
            Valid labels are: UX, UY, UZ (structural displacements); ROTX,
            ROTY, ROTZ (structural rotations); TEMP, TBOT, TE2, TE3, . . .,
            TTOP (temperatures);  PRES (pressure);  VOLT (voltage); MAG
            (magnetic scalar potential);  AX, AY, AZ (magnetic vector
            potentials);  CURR (current);  EMF (electromotive force drop); CONC
            (concentration); DELETE.

        Notes
        -----
        The degree of freedom (DOF) set for the model is determined from all
        element types defined. This command may be used to add to the current
        set.  The ALL label may be used on some commands to represent all
        labels of the current degree of freedom set for the model.  Issue the
        DOF command with no arguments to list the current set.  Use the DELETE
        label to delete any previously added DOFs and return to the default DOF
        set.
        """
        command = "DOF,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
            str(lab1),
            str(lab2),
            str(lab3),
            str(lab4),
            str(lab5),
            str(lab6),
            str(lab7),
            str(lab8),
            str(lab9),
            str(lab10),
        )
        return self.run(command, **kwargs)

    def elbow(
        self,
        transkey="",
        tol="",
        dof="",
        cons1="",
        cons2="",
        cons3="",
        cons4="",
        **kwargs,
    ):
        """APDL Command: ELBOW

        Specifies degrees of freedom to be coupled for end release and applies
        section constraints to elbow elements.

        Parameters
        ----------
        transkey
            Pipe-to-elbow transition flag:

            OFF - Do not automatically transition pipes to elbows. (This behavior is the
                  default.)

            ON - Automatically convert straight PIPE289 elements to ELBOW290 elements where it
                 is beneficial. The program converts elements in transition
                 regions where curved ELBOW290 elements are connected to
                 straight PIPE289 elements.

        tol
            Angle tolerance (in degrees) between adjacent ELBOW290 elements.
            The default value is 20. A value of -1 specifies all selected
            ELBOW290 elements.

        dof
            Degrees of freedom to couple:

            ALL - Couple all nodal degrees of freedom (UX, UY, UZ, ROTX, ROTY, and ROTZ). This
                  behavior is the default.

            BALL - Create ball joints (equivalent to releasing ROTX, ROTY, and ROTZ).

        cons1, cons2, cons3, cons4
            Section degrees of freedoms to constrain. If Cons1 through Cons4
            are unspecified, no section constraints are applied:

            SECT  - All section deformation

            SE - Section radial expansion

            SO - Section ovalization

            SW - Section warping

            SRA - Local shell normal rotation about cylindrical axis t2

            SRT - Local shell normal rotation about cylindrical axis t1

        Notes
        -----
        The ELBOW command specifies end releases and section constraints for
        ELBOW290 elements and converts straight PIPE289 elements to ELBOW290
        elements.

        Curved PIPE289 elements are not converted to ELBOW290 elements.

        ELBOW290 elements are generated only if there are existing ELBOW290
        elements in the curved areas.

        The command works on currently selected nodes and elements. It creates
        end releases on any two connected elbow elements whose angle at
        connection exceeds the specified tolerance. From within the GUI, the
        Picked node option generates an end release and section constraints at
        the selected node regardless of the angle of connection (that is, the
        angle tolerance [TOL ] is set to -1).

        Elbow and pipe elements must share the same section ID in order for the
        pipe-to-elbow transition to occur.

        To list the elements altered by the ELBOW command, issue an ELIST
        command.

        To list the coupled sets generated by the ELBOW command, issue a CPLIST
        command.

        To list the section constraints generated by the ELBOW command, issue a
        DLIST command.
        """
        command = "ELBOW,%s,%s,%s,%s,%s,%s,%s" % (
            str(transkey),
            str(tol),
            str(dof),
            str(cons1),
            str(cons2),
            str(cons3),
            str(cons4),
        )
        return self.run(command, **kwargs)

    def et(
        self,
        itype: MapdlInt = "",
        ename: Union[str, int] = "",
        kop1: MapdlInt = "",
        kop2: MapdlInt = "",
        kop3: MapdlInt = "",
        kop4: MapdlInt = "",
        kop5: MapdlInt = "",
        kop6: MapdlInt = "",
        inopr: MapdlInt = "",
        **kwargs,
    ) -> Optional[int]:
        """Define a local element type from the element library.

        APDL Command: ET

        Parameters
        ----------
        itype
            Arbitrary local element type number. Defaults to 1 +
            current maximum.

        ename
            Element name (or number) as given in the element library
            in Chapter 4 of the Element Reference. The name consists
            of a category prefix and a unique number, such as PIPE288.
            The category prefix of the name (PIPE for the example) may
            be omitted but is displayed upon output for clarity. If
            ``ename=0``, the element is defined as a null element.

        kop1, kop2, kop3, kop4, kop5, kop6
            KEYOPT values (1 through 6) for this element, as described
            in the Element Reference.

        inopr
            If 1, suppress all element solution printout for this
            element type.

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

    def etchg(self, cnv: str = "", **kwargs) -> Optional[str]:
        """Changes element types to their corresponding types.

        APDL Command: ETCHG

        Parameters
        ----------
        cnv
            Converts the element types to the corresponding type.
            Valid labels
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
        Changes the currently defined element types to their
        corresponding types.  Elements without a companion element
        (listed above) are not switched and should be switched with
        the ET command to an appropriate element type or to a null
        element. The KEYOPT values for the switched element types are
        reset to zero or to their default values. You must
        check these values to see if they are still meaningful.
        Additionally, if Cnv = ETI, ITE, or TTE, all real constants
        are set to zero.

        If Cnv = ITE, you will need to choose a material model that
        corresponds to your previously-defined material properties.
        If working interactively, you will be prompted to do so.
        """
        command = f"ETCHG,{cnv}"
        return self.run(command, **kwargs)

    def etcontrol(
        self, eltech: str = "", eldegene: str = "", **kwargs
    ) -> Optional[str]:
        """Control the element technologies used in element
        formulation (for applicable elements).

        APDL Command: ETCONTROL

        Parameters
        ----------
        eltech
            Element technology control.  One of the following:

            - ``"SUGGESTION"`` : The program offers a suggestion for the
              best element technology before solving.  If necessary,
              mixed u-P (KEYOPT(6)) is also included and reset. This
              behavior is the default.

            - ``"SET"`` : The program informs you of the best settings
              and resets any applicable KEYOPT settings
              automatically. This action overrides any previous manual
              settings.

            - ``"OFF"`` : Deactivates automatic selection of element
              technology. No suggestions are issued, and no
              automatic resetting occurs.

        eldegene
            Element degenerated shape control.  One of the following:

            - ``"ON"`` - If element shapes are degenerated, the
              degenerated shape function is employed and enhanced
              strain, simplified enhanced strain, and B-bar formulations
              are turned off (default).

            - ``"OFF"`` - If element shapes are degenerated, regular
              shape functions are still used, and the specified element
              technologies (e.g., enhanced strain, B-bar, uniform
              reduced integration) are still used.

        Notes
        -----
        The command default is ``mapdl.etcontrol('SUGGESTION', 'ON')``

        This command is valid for elements SHELL181, PLANE182,
        PLANE183, SOLID185, SOLID186, SOLID187, BEAM188, BEAM189,
        SHELL208, SHELL209, PLANE223, SOLID226, SOLID227, REINF264,
        SOLID272, SOLID273, SHELL281, SOLID285, PIPE288, PIPE289,
        ELBOW290.

        For more information, see Automatic Selection of Element
        Technologies and Formulations in the Element Reference.

        Examples
        --------
        Enable element tech control and degenerated shape control.

        >>> mapdl.et(1, 'SOLID186')
        >>> output = mapdl.etcontrol(eltech='SET', eldegene='ON')
        >>> print(output)
        ELEMENT TECHNOLOGY CONTROL PARAMETER FOR APPLICABLE ELEMENTS = SET.
         DEGENERATED ELEMENT SHAPE CONTROL PARAMETER FOR APPLICABLE ELEMENTS = ON.

        """
        return self.run(f"ETCONTROL,{eltech},{eldegene}", **kwargs)

    def etdele(
        self,
        ityp1: Union[str, int] = "",
        ityp2: MapdlInt = "",
        inc: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """APDL Command: ETDELE

        Deletes element types.

        Parameters
        ----------
        ityp1, ityp2, inc
            Deletes element types from ``ityp1`` to ``ityp2``
            (defaults to ``ityp1``) in steps of ``inc`` (defaults to
            1). If ``ityp1='ALL'``, ``ityp2`` and ``inc`` are ignored
            and all element types are deleted.  Element types are
            defined with the ``et`` command.

        Examples
        --------
        Create and delete an element type.

        >>> mapdl.et(1, 'SOLID186')
        >>> mapdl.etdele(1)

        """
        command = f"ETDELE,{ityp1},{ityp2},{inc}"
        return self.run(command, **kwargs)

    def etlist(
        self,
        ityp1: MapdlInt = "",
        ityp2: MapdlInt = "",
        inc: MapdlInt = "",
        **kwargs,
    ) -> Optional[str]:
        """Lists currently defined element types.

        APDL Command: ETLIST

        Parameters
        ----------
        ityp1, ityp2, inc
            Lists element types from ITYP1 to ITYP2 (defaults to
            ITYP1) in steps of INC (defaults to 1). If ITYP1 = ALL (
            default), ITYP2 and INC are ignored and all element types
            are listed.

        Notes
        -----
        This command is valid in any processor.
        """
        command = f"ETLIST,{ityp1},{ityp2},{inc}"
        return self.run(command, **kwargs)

    def keyopt(self, itype="", knum="", value="", **kwargs):
        """APDL Command: KEYOPT

        Sets element key options.

        Parameters
        ----------
        itype
            Element type number as defined on the ET command. The label GCN is
            also valid input for general contact elements (see Notes).

        knum
            Number of the KEYOPT to be defined (KEYOPT(KNUM)).

        value
            Value of this KEYOPT.

        Notes
        -----
        Alternative to inputting KEYOPT values on ET command.  Must be used if
        KEYOPT(7) or greater values are to be input. ITYPE must first be
        defined with the ET command.

        Specify ITYPE = GCN to set element key options for all contact elements
        types used in any existing general contact definitions (that is,
        contact elements having a real constant set number = 0).
        """
        command = "KEYOPT,%s,%s,%s" % (str(itype), str(knum), str(value))
        return self.run(command, **kwargs)

    def nsvr(self, itype="", nstv="", **kwargs):
        """APDL Command: NSVR

        Defines the number of variables for user-programmable element options.

        Parameters
        ----------
        itype
            Element type number as defined on the ET command.

        nstv
            Number of extra state variables to save (must be no more than 840).

        Notes
        -----
        Defines the number of extra variables that need to be saved for user-
        programmable (system-dependent) element options, e.g., material laws
        through user subroutine USERPL.  ITYPE must first be defined with the
        ET command.
        """
        command = "NSVR,%s,%s" % (str(itype), str(nstv))
        return self.run(command, **kwargs)
