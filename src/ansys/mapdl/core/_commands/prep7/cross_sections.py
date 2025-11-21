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


class CrossSections:

    def bsax(self, val1: str = "", val2: str = "", t: str = "", **kwargs):
        r"""Specifies the axial strain and axial force relationship for beam sections.

        Mechanical APDL Command: `BSAX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSAX.html>`_

        Parameters
        ----------
        val1 : str
            Axial strain component ( :math:`equation not available` ).

        val2 : str
            Axial force component ( :math:`equation not available` ).

        t : str
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ :

        .. math::

            equation not available

        The :ref:`bsax` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the relationship of axial strain and axial force for a beam section. The section data
        defined is associated with the section most recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`, :ref:`bsmd`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        .
        """
        command = f"BSAX,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bsm1(self, val1: str = "", val2: str = "", t: str = "", **kwargs):
        r"""Specifies the bending curvature and moment relationship in plane XZ for beam sections.

        Mechanical APDL Command: `BSM1 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSM1.html>`_

        Parameters
        ----------
        val1 : str
            Curvature component ( :math:`equation not available` ).

        val2 : str
            Bending moment component ( :math:`equation not available` ).

        t : str
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ :

        .. math::

            equation not available

        The :ref:`bsm1` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the bending curvature and moment for plane XZ of a beam section. The section data defined
        is associated with the section most recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`bsax`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`, :ref:`bsmd`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        .
        """
        command = f"BSM1,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bsm2(self, val1: str = "", val2: str = "", t: str = "", **kwargs):
        r"""Specifies the bending curvature and moment relationship in plane XY for beam sections.

        Mechanical APDL Command: `BSM2 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSM2.html>`_

        Parameters
        ----------
        val1 : str
            Curvature component ( :math:`equation not available` ).

        val2 : str
            Bending moment component ( :math:`equation not available` ).

        t : str
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ :

        .. math::

            equation not available

        The :ref:`bsm2` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the bending curvature and moment relationship for plane XY of a beam section. The section
        data defined is associated with the section most recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`bsax`, :ref:`bsm1`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`, :ref:`bsmd`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        .
        """
        command = f"BSM2,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bsmd(self, dens: str = "", t: str = "", **kwargs):
        r"""Specifies mass per unit length for a nonlinear general beam section.

        Mechanical APDL Command: `BSMD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSMD.html>`_

        Parameters
        ----------
        dens : str
            Mass density.

        t : str
            Temperature.

        Notes
        -----
        The :ref:`bsmd` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the mass density (assuming a unit area) for a beam section. The value specified is
        associated with the section most recently defined (via the :ref:`sectype` command).

        Related commands are :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        """
        command = f"BSMD,{dens},{t}"
        return self.run(command, **kwargs)

    def bss1(self, val1: str = "", val2: str = "", t: str = "", **kwargs):
        r"""Specifies the transverse shear strain and force relationship in plane XZ for beam sections.

        Mechanical APDL Command: `BSS1 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSS1.html>`_

        Parameters
        ----------
        val1 : str
            Transverse shear strain component ( :math:`equation not available` ).

        val2 : str
            Transverse shear force component ( :math:`equation not available` ).

        t : str
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ :

        .. math::

            equation not available

        The :ref:`bss1` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the transverse shear strain and transverse shear force relationship for plane XZ of a beam
        section. The section data defined is associated with the section most recently defined (via the
        :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss2`, :ref:`bsmd`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        .
        """
        command = f"BSS1,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bss2(self, val1: str = "", val2: str = "", t: str = "", **kwargs):
        r"""Specifies the transverse shear strain and force relationship in plane XY for beam sections.

        Mechanical APDL Command: `BSS2 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSS2.html>`_

        Parameters
        ----------
        val1 : str
            Transverse shear strain component ( :math:`equation not available` ).

        val2 : str
            Transverse shear force component ( :math:`equation not available` ).

        t : str
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ :

        .. math::

            equation not available

        The :ref:`bss1` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the transverse shear strain and transverse shear force relationship for plane XY of a beam
        section. The section data defined is associated with the section most recently defined (via the
        :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bsmd`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        .
        """
        command = f"BSS2,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def bste(self, alpha: str = "", t: str = "", **kwargs):
        r"""Specifies a thermal expansion coefficient for a nonlinear general beam section.

        Mechanical APDL Command: `BSTE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSTE.html>`_

        Parameters
        ----------
        alpha : str
            Coefficient of thermal expansion for the cross section.

        t : str
            Temperature.

        Notes
        -----
        The :ref:`bste` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies a thermal expansion coefficient for a beam section. The value specified is associated with
        the section most recently defined (via the :ref:`sectype` command).

        Related commands are :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`, :ref:`bss2`,
        and :ref:`bsmd`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        """
        command = f"BSTE,{alpha},{t}"
        return self.run(command, **kwargs)

    def bstq(self, val1: str = "", val2: str = "", t: str = "", **kwargs):
        r"""Specifies the cross section twist and torque relationship for beam sections.

        Mechanical APDL Command: `BSTQ <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_BSTQ.html>`_

        Parameters
        ----------
        val1 : str
            Twist component ( :math:`equation not available` ).

        val2 : str
            Torque component ( :math:`equation not available` ).

        t : str
            Temperature.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ :

        .. math::

            equation not available

        The :ref:`bstq` command, one of several `nonlinear general beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbsstrain>`_,
        specifies the cross section twist and torque relationship for a beam section. The section data
        defined is associated with the section most recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bss1`, :ref:`bss2`, :ref:`bsmd`,
        and :ref:`bste`.

        For complete information, see `Using Nonlinear General Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
        .
        """
        command = f"BSTQ,{val1},{val2},{t}"
        return self.run(command, **kwargs)

    def cbmd(
        self,
        row: str = "",
        c_r__r: str = "",
        c_r__rplus1: str = "",
        c_r__rplus2: str = "",
        c_r__rplus3: str = "",
        c_r__rplus4: str = "",
        c_r__rplus5: str = "",
        **kwargs,
    ):
        r"""Specifies preintegrated section mass matrix for composite-beam sections.

        Mechanical APDL Command: `CBMD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CBMD.html>`_

        Parameters
        ----------
        row : str
            Row number of the matrix.

        c_r__r : str
            Upper triangle of the cross-section mass matrix **[C]**.

        c_r__rplus1 : str
            Upper triangle of the cross-section mass matrix **[C]**.

        c_r__rplus2 : str
            Upper triangle of the cross-section mass matrix **[C]**.

        c_r__rplus3 : str
            Upper triangle of the cross-section mass matrix **[C]**.

        c_r__rplus4 : str
            Upper triangle of the cross-section mass matrix **[C]**.

        c_r__rplus5 : str
            Upper triangle of the cross-section mass matrix **[C]**.

        Notes
        -----
        With a unit beam length, the section mass matrix relates the resultant forces and torques to
        accelerations and angular accelerations as follows (applicable to the local element coordinate
        system):

        .. math::

            equation not available

        The :ref:`cbmd` command, one of several `composite beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_,
        specifies the section mass matrix (submatrix [ **C** ] data) for a composite beam section.
        The section data defined is associated with the section most
        recently defined ( :ref:`sectype` ) at the specified temperature ( :ref:`cbtmp` ).

        Unspecified values default to zero.

        Related commands are :ref:`cbtmp`, :ref:`cbte`, and :ref:`cbmx`.

        For complete information, see `Using Preintegrated Composite Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_
        """
        command = f"CBMD,{row},{c_r__r},{c_r__rplus1},{c_r__rplus2},{c_r__rplus3},{c_r__rplus4},{c_r__rplus5}"
        return self.run(command, **kwargs)

    def cbmx(
        self,
        row: str = "",
        s_r__r: str = "",
        s_r__rplus1: str = "",
        s_r__rplus2: str = "",
        s_r__rplus3: str = "",
        s_r__rplus4: str = "",
        s_r__rplus5: str = "",
        s_r__rplus6: str = "",
        **kwargs,
    ):
        r"""Specifies preintegrated cross-section stiffness for composite beam sections.

        Mechanical APDL Command: `CBMX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CBMX.html>`_

        Parameters
        ----------
        row : str
            Row number of the matrix.

        s_r__r : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        s_r__rplus1 : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        s_r__rplus2 : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        s_r__rplus3 : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        s_r__rplus4 : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        s_r__rplus5 : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        s_r__rplus6 : str
            Upper triangle of the cross-section stiffness matrix **[S]**.

        Notes
        -----
        The behavior of beam elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_ :

        .. math::

            equation not available

        The :ref:`cbmx` command, one of several `composite beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_,
        specifies the cross-section stiffness matrix (submatrix [ **S** ] data) for a composite beam
        section. The section data defined is associated with the section most
        recently defined ( :ref:`sectype` ) at the specified temperature ( :ref:`cbtmp` ).

        Unspecified values default to zero.

        Related commands are :ref:`cbtmp`, :ref:`cbte`, and :ref:`cbmd`.

        For complete information, see `Using Preintegrated Composite Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_
        """
        command = f"CBMX,{row},{s_r__r},{s_r__rplus1},{s_r__rplus2},{s_r__rplus3},{s_r__rplus4},{s_r__rplus5},{s_r__rplus6}"
        return self.run(command, **kwargs)

    def cbte(self, alpha: str = "", **kwargs):
        r"""Specifies a thermal expansion coefficient for a composite beam section.

        Mechanical APDL Command: `CBTE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CBTE.html>`_

        Parameters
        ----------
        alpha : str
            Coefficient of thermal expansion for the cross section.

        Notes
        -----
        The :ref:`cbte` command, one of several `composite beam section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_,
        specifies a thermal expansion coefficient for a beam section. The value specified is associated with
        the section most recently defined ( :ref:`sectype` ) at the specified temperature ( :ref:`cbtmp`
        ).

        Unspecified values default to zero.

        Related commands are :ref:`cbtmp`, :ref:`cbmx`, and :ref:`cbmd`.

        For complete information, see `Using Preintegrated Composite Beam Sections
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_
        """
        command = f"CBTE,{alpha}"
        return self.run(command, **kwargs)

    def sdelete(
        self,
        sfirst: str = "",
        slast: str = "",
        sinc: str = "",
        knoclean: int | str = "",
        lchk: str = "",
        **kwargs,
    ):
        r"""Deletes sections from the database.

        Mechanical APDL Command: `SDELETE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SDELETE.html>`_

        Parameters
        ----------
        sfirst : str
            First section ID to be deleted; defaults to first available section in the database.

        slast : str
            Last section ID to be deleted; defaults to last available section in the database.

        sinc : str
            Increment of the section ID; defaults to 1.

        knoclean : int or str
            Pretension element cleanup key (pretension sections only).

            * ``0`` - Perform cleanup of ``PRETS179`` pretension elements (delete pretension elements and
              reconnect elements split during :ref:`psmesh` ).

            * ``1`` - Do not perform cleanup.

        lchk : str
            Specifies the level of element-associativity checking:

            * ``NOCHECK`` - No element-associativity check occurs. This option is the default.

            * ``WARN`` - When a section, material, or real constant is associated with an element, the program
              issues a message warning that the necessary entity has been deleted.

            * ``CHECK`` - The command terminates, and no section, material, or real constant is deleted if it is
              associated with an element.

        Notes
        -----

        .. _SDELETE_notes:

        Deletes one or more specified sections and their associated data from the Mechanical APDL database.
        """
        command = f"SDELETE,{sfirst},{slast},{sinc},{knoclean},{lchk}"
        return self.run(command, **kwargs)

    def seccontrol(
        self,
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        val10: str = "",
        val11: str = "",
        val12: str = "",
        val13: str = "",
        **kwargs,
    ):
        r"""Supplements or overrides default section properties.

        Mechanical APDL Command: `SECCONTROL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECCONTROL.html>`_

        Parameters
        ----------
        val1 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val2 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val3 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val4 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val5 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val6 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val7 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val8 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val9 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val10 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val11 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val12 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        val13 : str
            Values, such as the length of a side or the numbers of cells along the width, that describe the
            geometry of a section. See the :ref:`SECCONTROL_notes` section of this command description for
            details about these values for the various section types.

        Notes
        -----

        .. _SECCONTROL_notes:

        The :ref:`seccontrol` command is divided into these operation types: :ref:`Beams,
        <SECCONTROL_beams>` :ref:`Links, <SECCONTROL_links>` :ref:`Pipes, <SECCONTROL_pipes>` :ref:`Shells,
        and <SECCONTROL_shells>` :ref:`Reinforcings. <SECCONTROL_reinfs>`

        Values are associated with the most recently issued :ref:`sectype` command. The data required is
        determined by the section type and is different for each type.

        :ref:`seccontrol` overrides the program-calculated transverse-shear stiffness.

        The command does not apply to thermal shell elements ``SHELL131`` and ``SHELL132`` or thermal solid
        elements ``SOLID278`` and ``SOLID279``.

        **Beams**

        .. _SECCONTROL_beams:

        Type: BEAM
        ^^^^^^^^^^

        * Data to provide in the value fields ( ``VAL1`` through ``VAL4`` ):

        * ``TXZ`` - User transverse shear stiffness.
        .. flat-table ::

        * -- - Unused field.

        * ``TXY`` - User transverse shear stiffness.
        * ``ADDMAS`` - Added mass per unit length.

        **Links**

        .. _SECCONTROL_links:

        Type: LINK
        ^^^^^^^^^^

        * Data to provide in the value fields ( ``VAL1``, ``VAL2``, ``VAL3``, ``VAL4``, ``VAL5``, ``VAL6``
          ):

        * ``ADDMAS`` - Added mass per unit length.
        * ``TENSKEY`` - Flag specifying tension and compression, tension only, or compression only (not
          valid for ``CABLE280`` :
        * 0 - Tension and compression (default).
        * 1 - Tension only.
        .. flat-table ::

        * -1 - Compression only.

        * ``CV1``, ``CV2`` - `Damping coefficients
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_LINK180.html#eqe20b311a-4d50-4c25-a2a3-ce500a7b0382>`_.
        * ``CV3`` - Compressive stiffness scaling factor (for ``CABLE280`` only). The ratio between
          compressive stiffness and tensile stiffness. Default - 1.0e-5. Maximum - 1.0.
        * ``CV4`` - Viscous regularization factor (for ``CABLE280`` only). Default - 0.05. Maximum - 1.0.

        **Pipes**

        .. _SECCONTROL_pipes:

        Type: PIPE
        ^^^^^^^^^^

        * Data to provide in the value field ( ``VAL1`` ):

        * ``ADDMAS`` - Added mass per unit length. Use this value to account for extra hardware only.

        * **Notes**
        * Other masses are handled as follows:

        * The mass of the internal fluid is accounted for by ``M`` :sub:`int` on the :ref:`secdata` command.

        * The mass of the outer covering (insulation) is accounted for by ``M`` :sub:`ins` on the
          :ref:`secdata` command.

        * The mass of the external fluid is accounted for by ``MATOC`` on the :ref:`ocdata` command.

        **Shells**

        .. _SECCONTROL_shells:

        Type: SHELL
        ^^^^^^^^^^^

        * Data to provide in the value fields ( ``VAL1`` through ``VAL8`` ):

        * ``E`` 11 - User transverse-shear stiffness.
        * ``E`` 22 - User transverse-shear stiffness.
        * ``E`` 12 - User transverse-shear stiffness.
        * ``ADDMAS`` - Added mass-per-unit area.
        * ``HMEMSCF`` - Hourglass-control membrane-scale factor.
        * ``HBENSCF`` - Hourglass-control bending-scale factor.
        * ``DRLSTIF`` - Drill-stiffness scale factor.
        * ``BENSTIF`` - Bending-stiffness scale factor ( ``SHELL181`` and ``SHELL281`` ).

        **Reinforcing**

        .. _SECCONTROL_reinfs:

        Type: REINF
        ^^^^^^^^^^^

        * Data to provide in the value fields ( ``VAL1``, ``VAL2``, ``VAL3`` ):

        * ``TENSKEY`` - Flag specifying tension-and-compression, tension-only, or compression-only
          reinforcing behavior (valid for structural reinforcing analysis):
        * 0 - Tension and compression (default).
        * 1 - Tension only.
        .. flat-table ::

        * -1 - Compression only.
        * -------------


        * ``REMBASE`` - Flag specifying how base-element material is handled:
        * 0 - Retain base-element material in the space occupied by the reinforcing fibers (default).
        * 1 - Remove base-element material in the space occupied by the reinforcing fibers.
        .. flat-table ::

        * -------------


        * ``STSSTATE`` - Flag specifying the reinforcing stress state or heat flow:
        * For smeared reinforcing:
        * 0 - Uniaxial-stress state (for structural reinforcing analysis) or uniaxial heat flow (for thermal
          reinforcing analysis). Only ``kxx`` is required. (Default.)
        * 1 - Plane-stress state (for structural reinforcing analysis) or anisotropic heat flow (for thermal
          reinforcing analysis). Both kxx and kyy are specified.
        * 2 - Plane-stress state with transverse shear stiffness. Valid for 3D smeared structural
          reinforcing analysis.
        * 3 - Plane-stress state with transverse shear stiffness and bending stiffness. Valid for 3D smeared
          structural reinforcing analysis with solid base elements.
        * For discrete reinforcing:
        * 0 - Uniaxial stiffness, or uniaxial heat flow for thermal reinforcing analysis. (Default.)
        * 1 - Uniaxial, bending, and torsional stiffness with square cross section. Valid for 3D structural
          reinforcing analysis with solid base elements.

        * **Notes**
        * ``REMBASE`` = 1 typically leads to more accurate models. (The base material must support 1D stress
          states.) For structural-reinforcing analysis, the base-element material consists of mass,
          stiffness, and body force. For thermal-reinforcing analysis, the base-element material consists of
          damping, conduction, and heat generation, and the base-element surface loads (convection and heat
          flux) are not subtracted. This option is not valid when the base-element material is anisotropic.
        * For smeared reinforcing with ``STSSTATE`` = 0, the equivalent thickness h of the smeared
          reinforcing layer is determined by h = ``A`` / ``S``, where ``A`` is the cross-section area of a
          single fiber and ``S`` is the distance between two adjacent fibers. (See :ref:`secdata`.)
        * ``STSSTATE`` = 1 to 3 is suitable for homogenous reinforcing layers (membrane) and applies to
          smeared reinforcing only ( :ref:`sectype`,,REINF,SMEAR). For smeared reinforcing with ``STSSTATE``
          = 1 to 3, discrete reinforcing with ``STSSTATE`` = 1, ``TENSKEY`` is ignored, and the default
          tension and compression behaviors apply to the reinforcing layers; also, the cross-section area
          input ``A`` is the thickness of the reinforcing layers and the distance input ``S`` is ignored.
          (See :ref:`secdata` and `REINF265 Structural/Thermal Input Data
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_REINF265.html#reinf265inpsummary>`_
        * For discrete reinforcing with ``STSSTATE`` = 1 or smeared reinforcing with ``STSSTATE`` = 3,
          bending or torsional reinforcing stiffness may not be captured adequately when using reinforcing
          with overly refined high-order base tetrahedral elements ( ``SOLID187`` or degenerated
          ``SOLID186`` ) and the stiffness ratio between reinforcing and base elements is excessive (>
          100x).
        * Specified ``TENSKEY``, ``REMBASE`` and ``STSSTATE`` values apply to all fibers defined in the
          current section.
        * For more information, see `Element Embedding
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        """
        command = f"SECCONTROL,{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12},{val13}"
        return self.run(command, **kwargs)

    def secdata(
        self,
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        val7: str = "",
        val8: str = "",
        val9: str = "",
        val10: str = "",
        val11: str = "",
        val12: str = "",
        **kwargs,
    ):
        r"""Describes the geometry of a section.

        Mechanical APDL Command: `SECDATA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECDATA.html>`_

        Parameters
        ----------
        val1 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val2 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val3 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val4 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val5 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val6 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val7 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val8 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val9 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val10 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val11 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        val12 : str
            Values, such as thickness or the length of a side or the numbers of cells along the width, that
            describe the geometry of a section. The terms ``VAL1``, ``VAL2``, etc. are specialized for each
            type of cross-section.

        Notes
        -----

        .. _SECDATA_notes:

        The :ref:`secdata` command defines the data describing the geometry of a section. The command is
        divided into these section types: `Beams
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SECDATA.html#SECDATA.fig.11>`_
        Beams, :ref:`Contact, <SECDATA_contact>` :ref:`General Axisymmetric, <SECDATA_axisy>` :ref:`Joints,
        <SECDATA_joints>` :ref:`Links, <SECDATA_links>` `Pipes
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SECDATA.html#eq148b7566-f562-4fe0-8ce3-f61c6b455f70>`_
        Pipes, :ref:`Pretension, <SECDATA_pretension>` :ref:`Reinforcing, <SECDATA_reinforcement>`
        :ref:`Shells, <SECDATA_shells>` :ref:`Supports, and <SECDATA_supports>` :ref:`Taper.
        <SECDATA_taper>`

        The data input on the :ref:`secdata` command is interpreted based on the most recently issued
        :ref:`sectype` command. The data required is determined by the section type and subtype, and is
        different for each one.

        .. _SECDATA_beams:

        Type: BEAM
        ^^^^^^^^^^

        Beam sections are referenced by ``BEAM188`` and ``BEAM189`` elements. Not all :ref:`secoffset`
        location values are valid for each subtype.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        .. _SECDATA_contact:

        Type: CONTACT
        ^^^^^^^^^^^^^

        Geometry Correction Contact sections for geometry correction ( ``Subtype`` = CIRCLE, SPHERE, or
        CYLINDER) are referenced
        by the following elements: ``TARGE169``, ``TARGE170``, ``CONTA172``, and ``CONTA174``. This geometry
        correction applies to cases where the original meshes of contact elements or target elements are
        located on a portion of a circular, spherical, or revolute surface.

        **Type: CONTACT, Subtype: CIRCLE**

        * Data to provide in the value fields for ``Subtype`` = CIRCLE:
        * ``X0``, ``Y0`` (circle center location in Global Cartesian coordinates - XY plane)

        **Type: CONTACT, Subtype: SPHERE**

        * Data to provide in the value fields for ``Subtype`` = SPHERE:
        * ``X0``, ``Y0``, ``Z0`` (sphere center location in Global Cartesian coordinates)

        **Type: CONTACT, Subtype: CYLINDER**

        * Data to provide in the value fields for ``Subtype`` = CYLINDER:
        * ``X1``, ``Y1``, ``Z1``, ``X2``, ``Y2``, ``Z2`` (two ends of cylindrical axis in Global Cartesian
          coordinates)

        User-Defined Contact Surface Normal The contact section for a user-defined contact surface normal (
        ``Subtype`` = NORMAL) is referenced
        by the following elements: ``CONTA172``, ``CONTA174``, and ``CONTA175``. This geometry correction is
        used to define a `shift direction for interference fit
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctecgeomcor.html#>`_ solutions.

        **Type: CONTACT, Subtype: NORMAL**

        * Data to provide in the value fields for ``Subtype`` = NORMAL:
        * ``CSYS``, ``NX``, ``NY``, ``NZ``
        * where:
        * ``CSYS`` = Local coordinate system number (defaults to global Cartesian).
        * ``NX``, ``NY``, ``NZ`` = Direction cosines with respect to ``CSYS.``

        Radius values associated with contact or target elements The radius contact section ( ``Subtype`` =
        RADIUS) is referenced by contact or target elements in a general contact definition under the
        following circumstances:

        * **Equivalent 3D contact radius for beam-to-beam contact** - The contact section for a user-defined
          equivalent contact radius ( ``Subtype`` = RADIUS) is referenced by the element type ``CONTA177``
          within a general contact definition. 3D beam-to-beam contact (or edge-to-edge contact) modeled by
          this line contact element assumes that its surface is a cylindrical surface.

        * **Radius (or radii) of rigid target segments** - The contact section for rigid target segment
          radii is referenced by target elements ``TARGE169`` (circle segment type) and ``TARGE170`` (line,
          parabola, cylinder, sphere, or cone segment type) in a general contact definition.

        **Type: CONTACT, Subtype: RADIUS**

        * Data to provide in the value fields for ``Subtype`` = RADIUS if the section is used as an
          equivalent contact radius for 3D beam-to-beam contact:
        * ``VAL1`` = Equivalent radius - outer radius
        * ``VAL2`` = Equivalent radius - inner radius (internal beam-to-beam contact)
        * ``VAL3`` : Set to 1 for internal beam-to-beam contact. Defaults to external beam-to-beam contact.

        * Data to provide in the value fields for ``Subtype`` = RADIUS if the section is used for 2D or 3D
          rigid target segments:
        * ``VAL1`` = First radius of the target segment (used for circle, line, parabola, cylinder, sphere,
          and cone segment types)
        * ``VAL2`` = Second radius of the target segment (used only for the cone segment type)

        Simplified Bolt Thread Modeling The contact section for bolt-thread modeling ( ``Subtype`` = BOLT)
        is referenced by the following
        elements: ``CONTA172``, ``CONTA174``, and ``CONTA175``. It applies to cases where the original
        meshes of contact elements are located on a portion of a bolt-thread surface. This feature allows
        you to include the behavior of bolt threads without having to add the geometric detail of the
        threads. Calculations are performed internally to approximate the behavior of the bolt-thread
        connections.

        **Type: CONTACT, Subtype: BOLT**

        * Data to provide in the value fields for ``Subtype`` = BOLT:
        * ``D`` m, ``P``, ``ALPHA``, ``N``, ``X1``, ``Y1``, ``Z1``, ``X2``, ``Y2``, ``Z2``
        * where:
        * ``D`` m = Pitch diameter, d :sub:`m`.
        * ``P`` = Pitch distance, p.
        * ``ALPHA`` = Half-thread angle, α (defaults to 30 degrees).
        * ``N`` = Number of starts (defaults to 1).
        * ``X1``, ``Y1``, ``Z1``, ``X2``, ``Y2``, ``Z2`` = Two end points of the bolt axis in global
          Cartesian coordinates.

        .. _SECDATA_axisy:

        Type: AXIS
        ^^^^^^^^^^

        General axisymmetric sections are referenced by the ``SURF159``, ``SOLID272``, and ``SOLID273``
        elements. Use this command to locate the axisymmetric axis.

        * Data to provide in the value fields:
        * **Pattern 1 (two points):**
        * 1, ``X1``, ``Y1``, ``Z1``, ``X2``, ``Y2``, ``Z2``
        * where ``X1``, ``Y1``, ``Z1``, ``X2``, ``Y2``, ``Z2`` are global Cartesian coordinates.
        * **Pattern 2 (coordinate system number plus axis [1 = x, 2 = y, 3 = z] ):**
        * 2, ``csys``, ``axis``
        * where ``csys`` is a Cartesian coordinate system.
        * **Pattern 3 (origin plus direction):**
        * 3, ``XO``, ``YO``, ``ZO``, ``xdir``, ``ydir``, ``zdir``
        * where ``XO``, ``YO``, ``ZO``  ``are global Cartesian coordinates and xdir``, ``ydir``, and
          ``zdir`` are direction cosines.

        .. _SECDATA_joints:

        Type: JOINT
        ^^^^^^^^^^^

        Joint sections are referenced by ``MPC184`` joint elements.

        * Data to provide in the value fields:
        * ``length1``, ``length2``, ``length3``, ``angle1``, ``angle2``, ``angle3``
        * where:
        * ``length1-3`` = Reference lengths used in the constitutive calculations.
        * ``angle1-3`` = Reference angles used in the constitutive calculations.

        The following table shows the lengths and angles to be specified for different kinds of joints.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The reference length and angle specifications correspond to the free relative degrees of freedom in
        a joint element for which constitutive calculations are performed. These values are used when
        stiffness and/or damping are specified for the joint elements.

        If the reference lengths and angles are not specified, they are calculated from the default or
        starting configuration for the element.

        See ``MPC184`` or the individual joint element descriptions for more information on joint element
        constitutive calculations.

        .. _SECDATA_links:

        Type: LINK
        ^^^^^^^^^^

        Link sections are referenced by the ``LINK33``, ``LINK180`` and ``CABLE280`` elements.

        * Data to provide in the value fields:
        * ``VAL1`` = Area

        .. _SECDATA_pipes:

        Type: PIPE
        ^^^^^^^^^^

        Pipe sections are referenced by the ``PIPE288``, ``PIPE289``, and ``ELBOW290`` elements.

        * Data to provide in the value fields:
        * ``D``  :sub:`o`, ``T``  :sub:`w`, ``N``  :sub:`c`, ``S``  :sub:`s`, ``N``  :sub:`t`, ``M``
          :sub:`int`, ``M``  :sub:`ins`, ``T``  :sub:`ins`
        * where:
        * ``D``  :sub:`o` = Outside diameter of pipe. Use a constant value for a circular pipe and an array
          for a noncircular pipe. (Noncircular pipe sections are referenced by the ``ELBOW290`` element
          only. See `Defining a Noncircular Pipe
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR15_4.html#eq250dbbf7-3095-46cc-b4f3-1beb47c75a9c>`_
        * ``T``  :sub:`w` = Wall thickness. Default = ``D`` o / 2, or “solid” pipe. ("Solid" pipe is not
          applicable to ``ELBOW290`` ; for that element, a thickness less than ``D`` o / 4 is recommended.)
        * ``N``  :sub:`c` = Number of cells around the circumference (8 :math:`equation not available`
          ``N``  :sub:`c`  :math:`equation not available`  120, where a greater value improves accuracy
          slightly; default =      8).
        * ``S``  :sub:`s` = Section number of the shell representing the pipe wall. Valid with ``ELBOW290``
          only. (Total thickness of the section is scaled to ``T``  :sub:`w`. The program considers the
          innermost layer inside of the pipe to be the first layer.)
        * ``N``  :sub:`t` = Number of cells through the pipe wall. Valid values are 1 (default), 3, 5, 7,
          and 9. Cells are graded such that they are thinner on the inner and outer surfaces. Valid with
          ``PIPE288`` and ``PIPE289`` only.
        * ``M``  :sub:`int` = Material number of fluid inside of the pipe. The default value is 0 (no
          fluid). This value is used to input the density of the internal fluid. The fluid inside the pipe
          element is ignored unless the free surface in a global X-Y plane is added as face 3 ( :ref:`sfe` )
          and is high enough to include at least one end node of the element.
        * ``M``  :sub:`ins` = Material number of material external to the pipe (such as insulation or
          armoring). The default value is 0 (no external material). This value is used to input the density
          of the external material. (External material adds mass and increases hydraulic diameter, but does
          not add to stiffness.)
        * ``T``  :sub:`ins` = Thickness of material external to the pipe, such as insulation. The default
          value is 0 (no external material).

        The accuracy of the ovalization value (OVAL) output by ``ELBOW290`` ( `Structural Elbow
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_ELBOW290.html#elem290coordsys>`_
        form only) improves as the specified number of cells around the circumference ( ``N`` :sub:`c` ) is
        increased.

        External material ( ``M`` :sub:`ins` ) adds mass and increases hydraulic diameter, but does not add
        to stiffness.

        .. figure:: ../../../images/_commands/gSECD_pipe.svg

        .. _SECDATA_pretension:

        Type: PRETENSION
        ^^^^^^^^^^^^^^^^

        Pretension sections are referenced by the ``PRETS179`` element.

        * Data to provide in the value fields:
        * ``node``, ``nx``, ``ny``, ``nz``
        * where:
        * ``node`` = Pretension node number.
        * ``nx`` = Orientation in global Cartesian x direction.
        * ``ny`` = Orientation in global Cartesian y direction.
        * ``nz`` = Orientation in global Cartesian z direction.

        The following usage is typical:

        * SECTYPE, 1, PRETENSION
        * SECDATA, 13184, 0.000, 0.000, 1.000
        * SECMODIF, 1, NAME, example
        * SLOAD, 1, PL01, TINY, FORC, 100.00, 1, 2

        The ``PRETENSION`` section options of :ref:`sectype` and :ref:`secdata` are documented mainly to aid
        in the understanding of data written by :ref:`cdwrite`. Ansys, Inc. recommends that you
        generate pretension sections using :ref:`psmesh`.

        .. _SECDATA_reinforcement:

        Type: REINF
        ^^^^^^^^^^^

        Each :ref:`secdata` command defines the material, geometry, and orientation (if Subtype = SMEAR) of
        one reinforcing member (discrete fiber or smeared surface) in the section. The reinforcing section
        can be referenced by reinforcing elements ( ``REINF263``, ``REINF264``, and ``REINF265`` ), or
        ``MESH200`` elements when used for temporarily representing reinforcing members. Only one
        :ref:`secdata` command is allowed per section when referenced by ``MESH200`` elements. For more
        information, see `Element Embedding
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_

        - - - - - - - - - - - - - - - - - - - - -

        **Type: REINF, Subtype: DISCRETE**

        Defines discrete reinforcing fibers with arbitrary orientations. For the MESH input pattern,
        reinforcing section data is referenced by ``MESH200`` elements. For other patterns, issue separate
        :ref:`secdata` commands to define each reinforcing fiber.

        * Data to provide in the value fields:
        * ``MAT, A, PATT, V1, V2, V3, V4, V5``
        * ``MAT`` = Material ID for the fiber. (See ``REINF264`` for valid material models.) When the
          reinforcing section is referenced by a ``MESH200`` element, the default is the ``MESH200`` element
          material ID ( :ref:`mat` ). When the section is referenced by reinforcing elements, the material
          ID is required for all fibers, and no default for this value is available.
        * ``A`` = Cross-section area of the reinforcing fiber.
        * ``PATT`` = Input pattern code (described below) indicating how the location of this fiber is
          defined. Available input patterns are MESH (when the section is referenced by a ``MESH200``
          element), and LAYN, EDGO, and BEAM (when the section is referenced by a reinforcing element).
        * ``V1, V2, V3, V4, V5`` = Values to define the location of the reinforcing fiber (depending on the
          ``PATT`` pattern code used), as shown:

        **PATT: MESH**

        **Description:** The locations of reinforcing fibers are defined directly via ``MESH200`` element
        connectivity.

        **Required input:**None.

        **PATT: LAYN**

        **Description:** The discrete reinforcing fiber is placed in the middle of a layer in a layered base
        element. The
        orientation of the fiber within the layer is adjustable via offsets with respect to a specified
        element edge.

        **Required input:**

        * ``V1`` (or ``N`` ) -- The number of the layer in the base element on which to apply the
          reinforcing fiber. The default value is 1.
        * ``V2`` (or ``e`` ) -- The number to indicate the element edge to which the offsets are measured.
          The default value is 1.
        * ``V3`` and ``V4`` (or ``Y1`` and ``Y2`` ) -- The normalized distances from the fiber to the two
          ends of the specified element edge. Valid values for ``Y1`` and ``Y2`` are 0.0 through 1.0. The
          default value of ``Y1`` is 0.5. The default value of ``Y2`` is ``Y1``.

        When applied to 8-node or 20-node layered solid elements:

        .. figure:: ../../../images/_commands/gSECD18.svg

        .. figure:: ../../../images/_commands/gSECD19.svg

        When applied to 4-node or 8-node layered shell elements:

        .. figure:: ../../../images/_commands/gSECD20.svg

        .. figure:: ../../../images/_commands/gSECD21.svg

        **PATT: EDGO**

        **Description:** The orientation of the discrete reinforcing fiber is similar to one of the
        specified element edges.
        The fiber orientation can be further adjusted via offsets with respect to the specified element
        edge.

        **Required input:**

        * ``V1`` (or ``O`` ) -- The number to indicate the element edge to which the offsets are measured.
          The default value is 1.
        * ``V2`` and ``V3`` (or ``Y1`` and ``Z1`` ) -- The normalized distances from the fiber to the first
          end of the specified element edge. Valid values for ``Y1`` and ``Z1`` are 0.0 through 1.0. The
          default value for ``Y1`` and ``Z1`` is 0.5.
        * ``V4`` and ``V5`` (or ``Y2`` and ``Z2`` ) - The normalized distances from the fiber to the second
          end of the specified element edge. Value values for ``Y2`` and ``Z2`` are 0.0 through 1.0. The
          default value for ``Y2`` is ``Y1``, and the default value for ``Z2`` is ``Z1``.

        If the base element is a beam or link, the program ignores values ``V2`` through ``V5`` and instead
        places the reinforcing in the center of the beam or link.

        When applied to 8-node or 20-node solid elements:

        .. figure:: ../../../images/_commands/gSECD22.svg

        .. figure:: ../../../images/_commands/gSECD22b.svg

        .. figure:: ../../../images/_commands/gSECD22c.svg

        When applied to tetrahedral elements:

          This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        When applied to 3D shell elements:

        .. figure:: ../../../images/_commands/gSECD28.svg

        .. figure:: ../../../images/_commands/gSECD29.svg

        When applied to beam or link elements:

        .. figure:: ../../../images/_commands/gSECD30.svg

        **PATT: BEAM**

        **Description:** Use this specialized input pattern for defining reinforcing in regular constant and
        tapered beams.

        **Required input:**

        * ``V1`` and ``V2`` (or ``Y1`` and ``Z1`` ) -- Y and Z offsets with respect to the section origin in
          the first beam section referenced by the base beam element. The default value for Y1 and Z1 is
          0.0.
        * ``V3`` and ``V4`` (or ``Y2`` and ``Z2`` ) -- Y and Z offsets with respect to the section origin in
          the second beam section referenced by the base beam element. The default value for ``Y2`` is
          ``Y1``, and the default value for ``Z2`` is ``Z1``. (Because ``V3`` and ``V4`` values apply only
          to tapered beams, the program ignores them if the base beam has a constant section.)

        .. figure:: ../../../images/_commands/gSECD31.svg

        - - - - - - - - - - - - - - - - - - - - -

        **Type: REINF, Subtype: SMEAR**

        Suitable for layers of reinforcing fibers with uniform cross-section area and spacing. Each
        :ref:`secdata` command defines the one reinforcing layer in the section. When referenced by a
        ``MESH200`` element, only one :ref:`secdata` command per section is allowed. When referenced by
        reinforcing elements ( ``REINF263`` and ``REINF265`` ), this limitation does not apply.

        * Data to provide in the value fields:
        * ``MAT, A, S, KCN, THETA, PATT, V1, V2, V3, V4, V5``
        * where:
        * ``MAT`` = Material ID for layer. (See ``REINF263`` or ``REINF265`` for available material models.)
          When the section is referenced by a ``MESH200`` element, the default is the ``MESH200`` element
          material ID ( :ref:`mat` ). When the section is referenced by reinforcing elements, the material
          ID is required for all fibers, and no default for this value is available.
        * ``A`` = Cross-section area of a single reinforcing fiber ( or the thickness of the reinforcing
          layer for homogeneous reinforcing membranes).
        * ``S`` = Distance between two adjacent reinforcing fibers (ignored for homogeneous reinforcing
          membranes).
        * **Note:** If the section is used to model the reinforcing layers with a uniaxial stress state (
          :ref:`seccontrol`,,,0), the equivalent thickness h of the reinforcing layer is determined by h =
          ``A`` / ``S``, where ``A`` is the cross-section area of a single fiber and ``S`` is the distance
          between two adjacent fibers. If the section is used to model homogeneous reinforcing membranes (
          :ref:`seccontrol`,,,1), the cross-section area input ``A`` is the thickness of the reinforcing
          layer and the distance input ``S`` is ignored.
        * ``KCN`` = Local coordinate system reference number for this layer. (See :ref:`local` for more
          information.) When the section is referenced by a ``MESH200`` element, the default ``KCN`` value
          is the ``MESH200`` element coordinate system ID ( :ref:`esys` ). For the 2D smeared reinforcing
          element ``REINF263``, ``KCN`` input is not required. When ``KCN`` is not specified, the program
          uses a default layer coordinate system (described in ``REINF263`` and ``REINF265`` ).
        * ``THETA`` = Angle (in degrees) of the final layer coordinate system with respect to the default
          layer system or the layer system specified in the ``KCN`` field. This value is ignored for
          ``REINF263`` when that element is embedded in 2D plane strain or plane stress base elements.
        * ``PATT`` = Input pattern code (described below) indicating how the location of this fiber is
          defined. Available input patterns are MESH (when the section is referenced by a ``MESH200``
          element), and LAYN, EDGO, and BEAM (when the section is referenced by a reinforcing element).
        * ``V1, V2, V3, V4, V5`` = Values to define the location of the reinforcing layer, as shown:

        **PATT: MESH**

        **Description:** The locations of reinforcing fibers are defined directly via ``MESH200`` element
        connectivity.

        **Required input:**None.

        **PATT: LAYN**

        **Description:** The smeared reinforcing layer is placed in the middle of a layer in a layered base
        element.

        **Required input:**``V1`` (or ``n`` ) -- The number of the layer in the base element on which to apply the reinforcing layer. The default value is 1.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        **PATT: EDGO**

        **Description:** This pattern applies only to 2D smeared reinforcing element ``REINF263``. The
        smeared reinforcing layer is represented by a line in 2D. The orientation of the 2D smeared
        reinforcing layer is similar to one of the specified element edges. The fiber orientation can be
        further adjusted via offsets with respect to the specified element edge.

        **Required input:**

        * ``V1`` (or ``O`` ) -- The number to indicate the element edge to which the offsets are measured.
          The default value is 1.
        * ``V2`` (or ``Y1`` ) -- The normalized distances from the reinforcing layer to the first end of the
          specified element edge. Valid values for Y1 are 0.0 through 1.0. The default value for ``Y1`` is
          0.5. ``V3`` (or ``Z1`` ) input is ignored.
        * ``V4`` (or ``Y2`` ) -- The normalized distances from the reinforcing layer to the second end of
          the specified element edge. Valid value values for ``Y2`` are 0.0 through 1.0. The default value
          for ``Y2`` is ``Y1``. ``V4`` (or ``Y2`` ) is ignored for axisymmetric shell elements. ``V5`` (or
          ``Z2``` ) input is ignored.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        **PATT: ELEF**

        **Description:** The smeared reinforcing layer is oriented parallel to one of three adjacent element
        faces. (This
        pattern does not apply to 2D smeared reinforcing element ``REINF263``.)

        **Required input:**

        * ``V1`` (or ``F`` ) -- The number to indicate the base element face. The default value is 1.
        * ``V2`` (or ``d1`` ) -- The normalized distance from the layer to the specified base element face.
          Valid values for ``d1`` are 0.0 through 1.0. The default value is 0.5.
        * ``V3`` (or ``d2`` ) -- The normalized distance from corners JJ and KK of the layer to the
          specified base element face (applicable to 8-node or 20-node solid elements only). Valid values
          for ``d2`` are 0.0 through 1.0. The default value is ``d1``.

        When applied to 8-node or 20-node solid elements:

          This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        When applied to tetrahedral elements:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        When applied to 3D shell elements:

        .. figure:: ../../../images/_commands/gSECD16.svg

        .. _SECDATA_shells:

        Type: SHELL
        ^^^^^^^^^^^

        Shell sections are referenced by the ``SHELL131``, ``SHELL132``, ``SHELL181``, ``SOLID185`` Layered
        Solid, ``SOLID186`` Layered Solid, ``SOLSH190``, ``SHELL208``, ``SHELL209``, ``SOLID278`` Layered
        Solid, ``SOLID279`` Layered Solid, and ``SHELL281`` elements.

        * Data to provide in the value fields:
        * ``TK``, ``MAT``, ``THETA``, ``NUMPT``, ``LayerName``
        * where:
        * ``TK`` = Thickness of shell layer. Zero thickness (not valid for ``SHELL131`` and ``SHELL132`` )
          indicates a dropped layer. The sum of all layer thicknesses must be greater than zero. The total
          thickness can be tapered via the :ref:`secfunction` command.
        * ``MAT`` = Material ID for layer (any current-technology material model is available for
          ``SHELL181``, ``SOLID185`` Layered Solid, ``SOLID186`` Layered Solid, ``SOLSH190``, ``SHELL208``,
          ``SHELL209``, ``SOLID278`` Layered Solid and ``SOLID279`` Layered Solid [including `UserMat
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_prog/Z7K4r1e5lcd.html#>`_ ], and
          ``SHELL281`` ). ``MAT`` is required for a composite (multi-layered) laminate. For a homogeneous
          (single-layered) shell, the default is the `element material attribute
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_mod/Hlp_G_MOD7_2.html#ad77wq1a7lcd>`_.
          You can also address multiple reference temperatures ( :ref:`tref` and/or :ref:`mp`,REFT).

        * ``THETA`` = Angle (in degrees) of layer element coordinate system with respect to element
          coordinate system (ESYS).
        * ``NUMPT`` = Number of integration points in layer. The user interface offers 1, 3 (default), 5, 7,
          or 9 points; however, you can specify a higher number on the :ref:`secdata` command. The
          integration rule used is Simpson's Rule. ( ``NUMPT`` is not used by ``SHELL131`` and
          ``SHELL132``.)

        .. _SECDATA_supports:

        Type: SUPPORT
        ^^^^^^^^^^^^^

        Support sections are referenced by ``SOLID185`` and ``SOLID186`` elements.

        **Type: SUPPORT, Subtype: BLOCK**

        * Data to provide in the value fields for ``Subtype`` = BLOCK:
        * ``T``, ``L``
        * where:
        * ``T`` = Thickness of the block wall.
        * ``L`` = Spacing distance of the block walls.

        **Type: SUPPORT, Subtype: ASEC**

        * Data to provide in the value fields for ``Subtype`` = ASEC:

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        * The multiplication factors are homogenization factors, and in each direction reflect the ratio of
          the support area projected onto the area of a fully solid support.
        * Values default to 1.0.
        * Y and Z values default to X values.
        * GXY value defaults to EX value, GYZ to EY, and GXZ to EZ.

        .. _SECDATA_taper:

        Type: TAPER
        ^^^^^^^^^^^

        Tapered sections are referenced by ``BEAM188``, ``BEAM189`` and ``ELBOW290`` elements. After
        specifying the tapered section type ( :ref:`sectype`,,TAPER), issue separate :ref:`secdata` commands
        to define each end of the tapered beam or pipe.

        * Data to provide in the value fields:
        * ``Sec_IDn``, ``XLOC``, ``YLOC``, ``ZLOC``

        * where:
        * ``Sec_IDn`` = Previously defined beam or pipe section at ends 1 and 2.
        * ``XLOC``, ``YLOC``, ``ZLOC`` = The location of Sec_ID n in the global Cartesian coordinate system.

        For more information about tapered beams and pipes, including assumptions and example command input,
        see `Defining a Tapered Beam or Pipe
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR15_4.html#>`_

        """
        command = f"SECDATA,{val1},{val2},{val3},{val4},{val5},{val6},{val7},{val8},{val9},{val10},{val11},{val12}"
        return self.run(command, **kwargs)

    def secfunction(self, table: str = "", pattern: str = "", **kwargs):
        r"""Specifies shell section thickness as a tabular function.

        Mechanical APDL Command: `SECFUNCTION <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECFUNCTION.html>`_

        Parameters
        ----------
        table : str
            Name of table parameter or array parameter for specifying thickness.

        pattern : str
            Interpretation pattern for array parameters.

        Notes
        -----

        .. _SECFUNCTION_notes:

        The :ref:`secfunction` command is associated with the section most recently defined via the
        :ref:`sectype` command.

        A table parameter can define tabular thickness as a function of coordinates. Alternatively, you can
        use an array parameter (indexed by node number) that expresses the function to be mapped. (See
        ``PATTERN`` of NOD2 for array content.) Enclose the table or array name in percent signs (%) (
        :ref:`secfunction`,``tablename``).

        Issue the :ref:`dim` command to define a table or array.

        The table or array defines the total shell thickness at any point in space. In multilayered
        sections, the total thickness and each layer thickness are scaled accordingly.

        The `Function Tool
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BASFUNCGRAPH.html>`_ is a
        convenient way to define your thickness tables.

        Refer to the :ref:`dim` command for interpreting a table in a local coordinate system.

        When ``PATTERN`` = NODE, ``TABLE`` should be a 1D array parameter (indexed by node number) that
        expresses the function to be mapped.

        When ``PATTERN`` = NOD2, ``TABLE`` should be a 2D array parameter (where column 1 contains node
        numbers and column 2 contains the corresponding thicknesses) that expresses the function to be
        mapped.

        Specify ``PATTERN`` when ``TABLE`` is an array parameter only (and not when it is a table parameter
        or a single value).
        """
        command = f"SECFUNCTION,{table},{pattern}"
        return self.run(command, **kwargs)

    def secjoint(
        self,
        kywrd: str = "",
        val1: str = "",
        val2: str = "",
        val3: str = "",
        val4: str = "",
        val5: str = "",
        val6: str = "",
        **kwargs,
    ):
        r"""Defines local coordinate systems at joint element nodes and other data for joint elements.

        Mechanical APDL Command: `SECJOINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECJOINT.html>`_

        Parameters
        ----------
        kywrd : str
            Keyword that indicates the type of joint element data being defined.

            * ``LSYS or blank`` - Define local coordinate systems at the nodes that form the ``MPC184`` joint
              element.

            * ``RDOF`` - Define the relative degrees of freedom to be fixed for an ``MPC184-General`` joint
              element.

            * ``PITC`` - Define the pitch of an ``MPC184-Screw`` joint element.

            * ``FRIC`` - Define the geometric quantities required for Coulomb frictional behavior in the
              ``MPC184-Revolute``, ``MPC184-Slot``, ``MPC184-Translational``, or ``MPC184-Spherical`` joint
              element.

            * ``PNLT`` - Define the penalty factors for the penalty-based joint element formulation.

        val1 : str
            The meaning of ``Val1`` through ``Val6`` changes, depending on the value of ``Kywrd``.

            If ``Kywrd`` = LSYS (or blank), ``Val1`` and ``Val2`` are Identifiers of the local coordinate
            systems at nodes I and J, respectively, of the joint element. ``Val3`` through ``Val6`` are not
            used.

            If ``Kywrd`` = RDOF, ``Val1`` through ``Val6`` are the relative degrees of freedom to be fixed for a
            general joint element. Input 1 for UX, 2 for UY, 3 for UZ, 4 for ROTX, 5 for ROTY, and 6 for ROTZ.
            You may input the DOFs in any order.

            If ``Kywrd`` = PITC, ``Val1`` is the pitch of the screw joint element; pitch is defined as the ratio
            of relative axial displacement (length units) to relative rotation (in radians). ``Val2`` through
            ``Val6`` are not used.

            If ``Kywrd`` = FRIC, ``Val1`` through ``Val3`` are defined as follows.

            * **For Revolute Joint:**
            * ``Val1`` = outer radius
            * ``Val2`` = inner radius
            * ``Val3`` = effective length
            * **For Translational Joint:**
            * ``Val1`` = effective length
            * ``Val2`` = effective radius
            * **For Spherical Joint:**
            * ``Val1`` = effective radius

            If ``Kywrd`` = PNLT, ``Val1`` and ``Val2`` are defined as follows, and ``Val3`` through ``Val6`` are not used.

            * ``Val1`` - Constraint type:

              * DISP - Displacement-based constraint
              * ROT - Rotation-based constraint

            * ``Val2`` - Scaling factor (input a positive number) or penalty factor (input a negative number) used with the
              penalty-based joint element formulation:

              * Positive number - the number is used as a scaling factor to scale the internally calculated
                penalty values.
              * Negative number - the absolute value of the number is used as the penalty factor in calculations.

        val2 : str
            The meaning of ``Val1`` through ``Val6`` changes, depending on the value of ``Kywrd``.

            If ``Kywrd`` = LSYS (or blank), ``Val1`` and ``Val2`` are Identifiers of the local coordinate
            systems at nodes I and J, respectively, of the joint element. ``Val3`` through ``Val6`` are not
            used.

            If ``Kywrd`` = RDOF, ``Val1`` through ``Val6`` are the relative degrees of freedom to be fixed for a
            general joint element. Input 1 for UX, 2 for UY, 3 for UZ, 4 for ROTX, 5 for ROTY, and 6 for ROTZ.
            You may input the DOFs in any order.

            If ``Kywrd`` = PITC, ``Val1`` is the pitch of the screw joint element; pitch is defined as the ratio
            of relative axial displacement (length units) to relative rotation (in radians). ``Val2`` through
            ``Val6`` are not used.

            If ``Kywrd`` = FRIC, ``Val1`` through ``Val3`` are defined as follows.

            * **For Revolute Joint:**
            * ``Val1`` = outer radius
            * ``Val2`` = inner radius
            * ``Val3`` = effective length
            * **For Translational Joint:**
            * ``Val1`` = effective length
            * ``Val2`` = effective radius
            * **For Spherical Joint:**
            * ``Val1`` = effective radius

            If ``Kywrd`` = PNLT, ``Val1`` and ``Val2`` are defined as follows, and ``Val3`` through ``Val6`` are not used.

            * ``Val1`` - Constraint type:

              * DISP - Displacement-based constraint
              * ROT - Rotation-based constraint

            * ``Val2`` - Scaling factor (input a positive number) or penalty factor (input a negative number) used with the
              penalty-based joint element formulation:

              * Positive number - the number is used as a scaling factor to scale the internally calculated
                penalty values.
              * Negative number - the absolute value of the number is used as the penalty factor in calculations.

        val3 : str
            The meaning of ``Val1`` through ``Val6`` changes, depending on the value of ``Kywrd``.

            If ``Kywrd`` = LSYS (or blank), ``Val1`` and ``Val2`` are Identifiers of the local coordinate
            systems at nodes I and J, respectively, of the joint element. ``Val3`` through ``Val6`` are not
            used.

            If ``Kywrd`` = RDOF, ``Val1`` through ``Val6`` are the relative degrees of freedom to be fixed for a
            general joint element. Input 1 for UX, 2 for UY, 3 for UZ, 4 for ROTX, 5 for ROTY, and 6 for ROTZ.
            You may input the DOFs in any order.

            If ``Kywrd`` = PITC, ``Val1`` is the pitch of the screw joint element; pitch is defined as the ratio
            of relative axial displacement (length units) to relative rotation (in radians). ``Val2`` through
            ``Val6`` are not used.

            If ``Kywrd`` = FRIC, ``Val1`` through ``Val3`` are defined as follows.

            * **For Revolute Joint:**
            * ``Val1`` = outer radius
            * ``Val2`` = inner radius
            * ``Val3`` = effective length
            * **For Translational Joint:**
            * ``Val1`` = effective length
            * ``Val2`` = effective radius
            * **For Spherical Joint:**
            * ``Val1`` = effective radius

            If ``Kywrd`` = PNLT, ``Val1`` and ``Val2`` are defined as follows, and ``Val3`` through ``Val6`` are not used.

            * ``Val1`` - Constraint type:

              * DISP - Displacement-based constraint
              * ROT - Rotation-based constraint

            * ``Val2`` - Scaling factor (input a positive number) or penalty factor (input a negative number) used with the
              penalty-based joint element formulation:

              * Positive number - the number is used as a scaling factor to scale the internally calculated
                penalty values.
              * Negative number - the absolute value of the number is used as the penalty factor in calculations.

        val4 : str
            The meaning of ``Val1`` through ``Val6`` changes, depending on the value of ``Kywrd``.

            If ``Kywrd`` = LSYS (or blank), ``Val1`` and ``Val2`` are Identifiers of the local coordinate
            systems at nodes I and J, respectively, of the joint element. ``Val3`` through ``Val6`` are not
            used.

            If ``Kywrd`` = RDOF, ``Val1`` through ``Val6`` are the relative degrees of freedom to be fixed for a
            general joint element. Input 1 for UX, 2 for UY, 3 for UZ, 4 for ROTX, 5 for ROTY, and 6 for ROTZ.
            You may input the DOFs in any order.

            If ``Kywrd`` = PITC, ``Val1`` is the pitch of the screw joint element; pitch is defined as the ratio
            of relative axial displacement (length units) to relative rotation (in radians). ``Val2`` through
            ``Val6`` are not used.

            If ``Kywrd`` = FRIC, ``Val1`` through ``Val3`` are defined as follows.

            * **For Revolute Joint:**
            * ``Val1`` = outer radius
            * ``Val2`` = inner radius
            * ``Val3`` = effective length
            * **For Translational Joint:**
            * ``Val1`` = effective length
            * ``Val2`` = effective radius
            * **For Spherical Joint:**
            * ``Val1`` = effective radius

            If ``Kywrd`` = PNLT, ``Val1`` and ``Val2`` are defined as follows, and ``Val3`` through ``Val6`` are not used.

            * ``Val1`` - Constraint type:

              * DISP - Displacement-based constraint
              * ROT - Rotation-based constraint

            * ``Val2`` - Scaling factor (input a positive number) or penalty factor (input a negative number) used with the
              penalty-based joint element formulation:

              * Positive number - the number is used as a scaling factor to scale the internally calculated
                penalty values.
              * Negative number - the absolute value of the number is used as the penalty factor in calculations.

        val5 : str
            The meaning of ``Val1`` through ``Val6`` changes, depending on the value of ``Kywrd``.

            If ``Kywrd`` = LSYS (or blank), ``Val1`` and ``Val2`` are Identifiers of the local coordinate
            systems at nodes I and J, respectively, of the joint element. ``Val3`` through ``Val6`` are not
            used.

            If ``Kywrd`` = RDOF, ``Val1`` through ``Val6`` are the relative degrees of freedom to be fixed for a
            general joint element. Input 1 for UX, 2 for UY, 3 for UZ, 4 for ROTX, 5 for ROTY, and 6 for ROTZ.
            You may input the DOFs in any order.

            If ``Kywrd`` = PITC, ``Val1`` is the pitch of the screw joint element; pitch is defined as the ratio
            of relative axial displacement (length units) to relative rotation (in radians). ``Val2`` through
            ``Val6`` are not used.

            If ``Kywrd`` = FRIC, ``Val1`` through ``Val3`` are defined as follows.

            * **For Revolute Joint:**
            * ``Val1`` = outer radius
            * ``Val2`` = inner radius
            * ``Val3`` = effective length
            * **For Translational Joint:**
            * ``Val1`` = effective length
            * ``Val2`` = effective radius
            * **For Spherical Joint:**
            * ``Val1`` = effective radius

            If ``Kywrd`` = PNLT, ``Val1`` and ``Val2`` are defined as follows, and ``Val3`` through ``Val6`` are not used.

            * ``Val1`` - Constraint type:

              * DISP - Displacement-based constraint
              * ROT - Rotation-based constraint

            * ``Val2`` - Scaling factor (input a positive number) or penalty factor (input a negative number) used with the
              penalty-based joint element formulation:

              * Positive number - the number is used as a scaling factor to scale the internally calculated
                penalty values.
              * Negative number - the absolute value of the number is used as the penalty factor in calculations.

        val6 : str
            The meaning of ``Val1`` through ``Val6`` changes, depending on the value of ``Kywrd``.

            If ``Kywrd`` = LSYS (or blank), ``Val1`` and ``Val2`` are Identifiers of the local coordinate
            systems at nodes I and J, respectively, of the joint element. ``Val3`` through ``Val6`` are not
            used.

            If ``Kywrd`` = RDOF, ``Val1`` through ``Val6`` are the relative degrees of freedom to be fixed for a
            general joint element. Input 1 for UX, 2 for UY, 3 for UZ, 4 for ROTX, 5 for ROTY, and 6 for ROTZ.
            You may input the DOFs in any order.

            If ``Kywrd`` = PITC, ``Val1`` is the pitch of the screw joint element; pitch is defined as the ratio
            of relative axial displacement (length units) to relative rotation (in radians). ``Val2`` through
            ``Val6`` are not used.

            If ``Kywrd`` = FRIC, ``Val1`` through ``Val3`` are defined as follows.

            * **For Revolute Joint:**
            * ``Val1`` = outer radius
            * ``Val2`` = inner radius
            * ``Val3`` = effective length
            * **For Translational Joint:**
            * ``Val1`` = effective length
            * ``Val2`` = effective radius
            * **For Spherical Joint:**
            * ``Val1`` = effective radius

            If ``Kywrd`` = PNLT, ``Val1`` and ``Val2`` are defined as follows, and ``Val3`` through ``Val6`` are not used.

            * ``Val1`` - Constraint type:

              * DISP - Displacement-based constraint
              * ROT - Rotation-based constraint

            * ``Val2`` - Scaling factor (input a positive number) or penalty factor (input a negative number) used with the
              penalty-based joint element formulation:

              * Positive number - the number is used as a scaling factor to scale the internally calculated
                penalty values.
              * Negative number - the absolute value of the number is used as the penalty factor in calculations.

        Notes
        -----

        .. _SECJOINT_notes:

        Use this command to define additional section data for ``MPC184`` joint elements. To overwrite the
        current values, issue another :ref:`secjoint` command with the same ``Kywrd`` value. The data input
        on this command is interpreted based on the most recently issued :ref:`sectype` command.

        The command :ref:`secjoint`,PNLT is only applicable to penalty-based joints (KEYOPT(2) = 1 on most
        joint elements). The default penalty factor (common to all constraints of the joint element) is of
        the order of 10\2E:sub:`avg`, where E:sub:`avg` is the average Young``s modulus of the elements
        attached to the joint element or deduced from the connections to other elements. The default value
        may be overridden by specifying user-defined penalty factors via :ref:`secjoint`,PNLT. The choice of
        penalty factors can affect the constraint satisfaction as well as overall solution convergence.
        """
        command = f"SECJOINT,{kywrd},{val1},{val2},{val3},{val4},{val5},{val6}"
        return self.run(command, **kwargs)

    def seclib(self, option: str = "", path: str = "", **kwargs):
        r"""Sets the default section library path for the :ref:`secread` command.

        Mechanical APDL Command: `/SECLIB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLIB.html>`_

        Parameters
        ----------
        option : str

            * ``READ`` - Sets the read path (default).

            * ``STATUS`` - Reports the current section library path setting to the :file:`Jobname.LOG` file.

        path : str
            Defines the directory path from which to read section library files.

        Notes
        -----

        .. _s-SECLIB_notes:

        When the :ref:`secread` command is issued without a directory path, the command searches for a
        section library in the following order:

        * The user's home directory

        * The current working directory

        * The path specified by the :ref:`seclib` command

        """
        command = f"/SECLIB,{option},{path}"
        return self.run(command, **kwargs)

    def seclock(
        self,
        dof0: str = "",
        minvalue0: str = "",
        maxvalue0: str = "",
        dof1: str = "",
        minvalue1: str = "",
        maxvalue1: str = "",
        dof2: str = "",
        minvalue2: str = "",
        maxvalue2: str = "",
        addional_command_arg: str = "",
        **kwargs,
    ):
        r"""Specifies locks on the components of relative motion in a joint element.

        Mechanical APDL Command: `SECLOCK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_

        Parameters
        ----------
        dof0 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        minvalue0 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        maxvalue0 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        dof1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        minvalue1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        maxvalue1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        dof2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        minvalue2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        maxvalue2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        addional_command_arg : str
            Additional arguments can be passed to the initial command. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECLOCK.html>`_ for
            further information.

        Notes
        -----

        .. _SECLOCK_notes:

        Specify up to three DOFs to be locked. Locks are activated when the limit values are reached, and
        further motion in that DOF is frozen. If necessary, you may repeat the command.
        """
        command = f"SECLOCK,{dof0},{minvalue0},{maxvalue0},{dof1},{minvalue1},{maxvalue1},{dof2},{minvalue2},{maxvalue2},{addional_command_arg}"
        return self.run(command, **kwargs)

    def secmodif(
        self, secid: str = "", kywrd: str = "", addional_command_arg: str = "", **kwargs
    ):
        r"""Modifies a pretension section

        Mechanical APDL Command: `SECMODIF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECMODIF.html>`_

        Parameters
        ----------
        secid : str
            Unique section number. This number must already be assigned to a section.

        kywrd : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECMODIF.html>`_ for
            further information.

        addional_command_arg : str
            Additional arguments can be passed to the initial command. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECMODIF.html>`_ for
            further information.

        Notes
        -----

        .. warning::

           This function contains specificities regarding the argument definitions.
           Please refer to the `command documentation <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECMODIF.html>`_
           for further explanations.

        .. _SECMODIF_notes:

        The :ref:`secmodif` command either modifies the normal for a specified pretension section, or
        changes the name of the specified pretension surface.
        """
        command = f"SECMODIF,{secid},{kywrd},{addional_command_arg}"
        return self.run(command, **kwargs)

    def secnum(self, secid: str = "", **kwargs):
        r"""Sets the element section attribute pointer.

        Mechanical APDL Command: `SECNUM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECNUM.html>`_

        Parameters
        ----------
        secid : str
            Defines the section ID number to be assigned to the subsequently-defined elements. Defaults to
            1. See :ref:`sectype` for more information about the section ID number.
        """
        command = f"SECNUM,{secid}"
        return self.run(command, **kwargs)

    def secoffset(
        self,
        location: str = "",
        offset1: str = "",
        offset2: str = "",
        cg_y: str = "",
        cg_z: str = "",
        sh_y: str = "",
        sh_z: str = "",
        **kwargs,
    ):
        r"""Defines the section offset for cross sections.

        Mechanical APDL Command: `SECOFFSET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECOFFSET.html>`_

        Parameters
        ----------
        location : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        offset1 : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        offset2 : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        cg_y : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        cg_z : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        sh_y : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        sh_z : str
            The location of the nodes in the section. All are dependent on the type. See the
            :ref:`SECOFFSET_notes` section for information about the values for the various section types.

        Notes
        -----

        .. _SECOFFSET_notes:

        The :ref:`secoffset` command is divided into four types: `Beams
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SECOFFSET.html#SECOFFSET.fig.1>`_
        Beams, :ref:`Pipes, <SECOFFSET_pipes>` :ref:`Shells, and <SECOFFSET_shells>` :ref:`Preintegrated
        General Shells. <SECOFFSET_preintshells>`

        The offsets defined by the :ref:`secoffset` command are associated with the section most recently
        defined using the :ref:`sectype` command. Not all :ref:`secoffset` location values are valid for
        each subtype.

        For the thermal shell elements, ``SHELL131`` and ``SHELL132``, the node offset specified by
        :ref:`secoffset` is used in thermal contact analyses. Otherwise, the :ref:`secoffset` command has no
        effect on the solution for these elements and is used only for visualization purposes.

        This command is not valid with thermal solid elements ``SOLID278`` and ``SOLID279``.

        For beam elements ``BEAM188`` / ``BEAM189`` and pipe elements ``PIPE288`` / ``PIPE289`` in the XY
        plane, an offset is not allowed if it causes the elements to be nonsymmetric about the XY plane.

        **Beams**

        .. _SECOFFSET_beams:

        Type: BEAM
        ^^^^^^^^^^

        Argument data to provide:

        ``Location``, ``OFFSETY``, ``OFFSETZ``, ``CG-Y``, ``CG-Z``, ``SH-Y``, ``SH-Z``

        * ``Location`` -

          * ``CENT`` - Beam node will be offset to centroid (default).

          * ``SHRC`` - Beam node will be offset to shear center.

          * ``ORIGIN`` - Beam node will be offset to origin of the cross section.

          * ``USER`` - Beam node will be offset to the location specified by ``OFFSETY`` and ``OFFSETZ``.

        * ``OFFSETY, OFFSETZ`` - Values that locate the node with respect to the default origin of the
          cross section when the ``Location`` argument is set to USER. Valid only when USER is set.

          The following figure illustrates the offsets for a channel cross section, and shows the relative
          locations of SHRC and CENT.

          .. figure:: ../../../images/_commands/gSECO1.svg

             Offsets for a CHAN Section Subtype

        * ``CG-Y, CG-Z, SH-Y, SH-Z`` - Override the program-calculated centroid and shear centroid
          locations.

          This option should only be used by advanced users modeling composite cross sections.

        **Pipes**

        .. _SECOFFSET_pipes:

        Type: PIPE
        ^^^^^^^^^^

        Argument data to provide:

        ``OFFSETY``, ``OFFSETZ``

        * ``OFFSETY, OFFSETZ`` - Values that locate the node with respect to the center of the pipe.

        **Shells**

        .. _SECOFFSET_shells:

        Type: SHELL
        ^^^^^^^^^^^

        Argument data to provide:

        ``Location``, ``OFFSET``

        * ``Location`` -

          * ``TOP`` - Shell node will be offset to top of the section.

          * ``MID`` - Shell node will be offset to midplane of the section (default).

          * ``BOT`` - Shell node will be offset to bottom of the section.

          * ``USER`` - Shell node will be offset to the location specified by ``OFFSET``.

        * ``OFFSET`` - Value that locates the node with respect to the default origin (midplane) of the
          section. Valid only when ``Location`` = USER.

          The offset alters only the reference surface of the shell elements (that is, where the nodes are
          located). It does not change the physical dimensions of the shell itself; the volume and mass remain
          constant when an offset is specified.

        **Preintegrated General Shells**

        .. _SECOFFSET_preintshells:

        Type: GENS
        ^^^^^^^^^^

        Argument data to provide:

        ``Location``, ``OFFSET``

        * ``Location`` -

          * ``MID`` - Shell node will be offset to midplane of the section (default).

          * ``USER`` - Shell node will be offset to the location specified by ``OFFSET``.

        * ``OFFSET`` - Value that locates the node with respect to the default origin (midplane) of the
          section. Valid only when ``Location`` = USER.

          The offset alters only the reference surface of the shell elements (that is, where the nodes are
          located).
        """
        command = (
            f"SECOFFSET,{location},{offset1},{offset2},{cg_y},{cg_z},{sh_y},{sh_z}"
        )
        return self.run(command, **kwargs)

    def secplot(
        self, secid: str = "", val1: str = "", val2: str = "", val3: str = "", **kwargs
    ):
        r"""Plots the geometry of a beam, pipe, shell, or reinforcing section to scale.

        Mechanical APDL Command: `SECPLOT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECPLOT.html>`_

        Parameters
        ----------
        secid : str
            The section ID number (as defined via the :ref:`sectype` command).

        val1 : str
            Values that control the information to be plotted. See the :ref:`SECPLOT_notes` section of this
            command description for more information. For clarity, the labels ``VAL1``, ``VAL2``, and
            ``VAL3`` are renamed according to the section type.

        val2 : str
            Values that control the information to be plotted. See the :ref:`SECPLOT_notes` section of this
            command description for more information. For clarity, the labels ``VAL1``, ``VAL2``, and
            ``VAL3`` are renamed according to the section type.

        val3 : str
            Values that control the information to be plotted. See the :ref:`SECPLOT_notes` section of this
            command description for more information. For clarity, the labels ``VAL1``, ``VAL2``, and
            ``VAL3`` are renamed according to the section type.

        Notes
        -----

        .. _SECPLOT_notes:

        :ref:`secplot` is valid for :ref:`SECPLOT_beams`, :ref:`SECPLOT_shells`, and :ref:`SECPLOT_reinf`
        only. The command is not valid for ``ELBOW290``.

        :ref:`secplot` cannot display the plot of an ASEC (arbitrary section) subtype.

        .. _SECPLOT_beams:

        Plots the geometry of the beam or pipe section to scale depicting the centroid, shear center, and
        origin. :ref:`secplot` also lists various section properties such as ``Iyy``, ``Iyz``, and ``Izz``.

        Data to be supplied in the value fields:

        * ``MESHKEY`` - Beam or pipe section mesh display options:

          * ``0`` - Display section outline only.

          * ``1`` - Display beam or pipe section mesh.

          * ``2`` - Display the section mesh with node numbers.

          * ``3`` - Display the section mesh with cell numbers.

          * ``4`` - Display the section mesh with material numbers and colors.

          * ``5`` - Display the section mesh with material colors only.

          * ``6`` - Display the section mesh with the RST node numbers. RST nodes are section corner nodes
            where results are available. This is applicable when the averaged results format (KEYOPT(15) = 0 for
            ``BEAM188``, ``BEAM189``, ``PIPE288``, and ``PIPE289`` ) is used.

          * ``7`` - Display the section mesh with the RST cell numbers. RST cells are section cells where
            results are available. This is applicable when the non-averaged results format (KEYOPT(15) = 1 for
            ``BEAM188``, ``BEAM189``, ``PIPE288``, and ``PIPE289`` ) is used.

          Options 2 through 6 do not depict centroid and shear center, nor do they list section properties.

        Following is a sample section plot for the beam section type:

        .. figure:: ../../../images/_commands/gSECP1.jpg

        .. _SECPLOT_shells:

        Plots the layer arrangement of the shell section showing the layer material and orientation.

        Data to be supplied in the value fields:

        * ``LAYR1, LAYR2`` - The range of layer numbers to be displayed. If ``LAYR1`` is greater than
          ``LAYR2``, a reversed order display is produced. Up to 20 layers may be displayed at the same time.
          ``LAYR1`` defaults to 1. ``LAYR2`` defaults to ``LAYR1`` if ``LAYR1`` is input or to the number of
          layers (or to 19+ ``LAYR1``, if smaller) if ``LAYR1`` is not input.

        Following is a sample section plot for the shell section type:

        .. figure:: ../../../images/_commands/gsecplotshell.jpg

        .. _SECPLOT_reinf:

        Plots the arrangement of a :ref:`reinforcing section within the base element.
        <SECDATA_reinforcement>`

        Data to be supplied in the value fields:

        * ``REINF1, REINF2, OVERLAY`` - ``REINF1, REINF2`` -- The numerical range of reinforcings to be
        displayed. The default ``REINF1``
          value is 1. The default ``REINF2`` value is the number of reinforcings.

          ``OVERLAY`` -- The section ID of the base element within which to display the reinforcing section. The section appears translucent and the reinforcing section is solid. Valid values are:

          * SOLID -- Display a translucent solid block over the reinforcing section

          * ``SECID`` -- A number corresponding to a specific section ID of the base element.

          If no ``OVERLAY`` value is specified, the program displays the reinforcing section only.

        Following is a sample section plot for the reinforcing section type:

        .. figure:: ../../../images/_commands/gSECP.fig.3.jpg

        For more information about reinforcing, see the documentation for the :ref:`secdata` command, and
        the ``REINF264`` and ``REINF265`` elements.
        """
        command = f"SECPLOT,{secid},{val1},{val2},{val3}"
        return self.run(command, **kwargs)

    def secread(self, fname: str = "", ext: str = "", option: str = "", **kwargs):
        r"""Reads a custom section library or a user-defined section mesh into Mechanical APDL.

        Mechanical APDL Command: `SECREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECREAD.html>`_

        Parameters
        ----------
        fname : str
            Section library file name and directory path containing the section library file (248 characters
            maximum, including directory). If you do not specify a directory path, it will default to your
            working directory and you can use all 248 characters for the file name.

            When the :ref:`secread` command is given without a directory path, the command searches for a section library in the following order:

            * The user's home directory

            * The current working directory

            * The path specified by the :ref:`seclib` command

            The file name defaults to :file:`Jobname` if ``Fname`` is left blank.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to SECT if ``Ext`` is left
            blank.

        option : str

            * ``LIBRARY`` - Reads in a library of sections and their associated section data values; the
              default. A section library may be created by editing the section-defining portions of the
              :file:`Jobname.LOG` file and saving it with a :file:`.SECT` suffix.

            * ``MESH`` - Reads in a user mesh section file containing the cell connectivity, cell flags, and
              nodal coordinates for the current beam section of subtype MESH as defined by :ref:`sectype`. See the
              :ref:`SECREAD_notes` section of this command description for details about user mesh section files.
              :ref:`secwrite` builds mesh files based on 2D models you create.

        Notes
        -----

        .. _SECREAD_notes:

        The :ref:`secread` command operates on the section specified via the most recently issued
        **SECTYPE** command. Issue a separate :ref:`secread` command for each section ID that you want to
        read in.

        .. _SECREAD_extranote1:

        Here are excerpts from a sample user section mesh file for a section with 75 nodes, 13 cells, and 9
        nodes per cell for a two-hole box section. Illustrations of the two-hole box section and the cell
        mesh for it appear later in this command description.

        This command contains some tables and extra information which can be inspected in the original
        documentation pointed above.

        The mesh file is divided into three sections: the First Line, the Cells Section, and the Nodes
        Section. Here are brief descriptions of the contents of each.

        **First Line:** The First Line defines the number of nodes and the number of cells for the mesh.

        **Cells Section:** The Cells Section contains as many lines as there are cells. In this example,
        there are thirteen
        cells, so there are thirteen lines in this section. In each line, the number "1" that follows the
        cell connectivity information is the material number.

        Cell nodal connectivity must be given in a counterclockwise direction, with the center node being
        the ninth node. For details, see :ref:`secread_fig_2`.

        **Nodes Section:** The Nodes Section contains as many lines as there are nodes. In this example,
        there are 75 nodes, so
        there are a total of 75 lines in this section. Each node line contains the node's boundary flag, the
        Y coordinate of the node, and the Z coordinate of the node. Currently, all node boundary flags
        appear as 0s in a cell mesh file (as illustrated in :ref:`secread_fig_1` ). Since all node boundary
        flags are 0, :ref:`secread` ignores them when it reads a cell mesh file into Mechanical APDL.

        There cannot be any gaps in the node numbering of a cell mesh. The nodes in a cell mesh must be
        numbered consecutively, with the first node having a node number of 1, and the last node having a
        node number that is equal to the maximum number of nodes in the cell mesh.

        .. figure:: ../../../images/_commands/gSECR2.svg

           Two-hole Box Section

        .. figure:: ../../../images/_commands/gSECR3.svg

           Cell Mesh for the Two-hole Box Section
        """
        command = f"SECREAD,{fname},{ext},,{option}"
        return self.run(command, **kwargs)

    def secstop(
        self,
        dof0: str = "",
        minvalue0: str = "",
        maxvalue0: str = "",
        dof1: str = "",
        minvalue1: str = "",
        maxvalue1: str = "",
        dof2: str = "",
        minvalue2: str = "",
        maxvalue2: str = "",
        addional_command_arg: str = "",
        **kwargs,
    ):
        r"""Specifies stops on the components of relative motion in a joint element.

        Mechanical APDL Command: `SECSTOP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_

        Parameters
        ----------
        dof0 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        minvalue0 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        maxvalue0 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        dof1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        minvalue1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        maxvalue1 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        dof2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        minvalue2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        maxvalue2 : str
            The description of the argument is missing in the Python function. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        addional_command_arg : str
            Additional arguments can be passed to the initial command. Please, refer to the `command
            documentation
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECSTOP.html>`_ for
            further information.

        Notes
        -----

        .. _SECSTOP_notes:

        Stops restrict motion in a DOF; motion beyond the MINVALUE or MAXVALUE is prevented (motion away
        from a limit is allowed). You can specify up to three stops. If necessary, you can repeat the
        command.
        """
        command = f"SECSTOP,{dof0},{minvalue0},{maxvalue0},{dof1},{minvalue1},{maxvalue1},{dof2},{minvalue2},{maxvalue2},{addional_command_arg}"
        return self.run(command, **kwargs)

    def sectype(
        self,
        secid: str = "",
        type_: str = "",
        subtype: str = "",
        name: str = "",
        refinekey: str = "",
        **kwargs,
    ):
        r"""Associates section type information with a section ID number.

        Mechanical APDL Command: `SECTYPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECTYPE.html>`_

        Parameters
        ----------
        secid : str
            Section identification number. If ``SECID`` is blank or zero, the ``SECID`` number is
            incremented by one from the highest section ID number currently defined in the database. (See
            `Notes
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cmd/Hlp_C_SECTYPE.html#SECTYPE.prodres>`_
            Notes for ``SECID`` input specific to general contact.)

        type_ : str

            * ``AXIS`` - Define the axis for a general axisymmetric section.

            * ``BEAM`` - Defines a beam section. This option has a ``Subtype``.

            * ``COMB`` - Defines a composite (temperature-dependent) beam section. This option has a
              ``Subtype``.

            * ``CONTACT`` - Defines a contact section. This option has a ``Subtype``.

            * ``GENB`` - Defines a nonlinear general (temperature-dependent) beam section. This option has a
              ``Subtype``.

            * ``GENS`` - Defines a preintegrated general (temperature-dependent) shell section.

            * ``JOINT`` - Defines a joint section. This option has a ``Subtype``.

            * ``LINK`` - Defines a link section.

            * ``PIPE`` - Defines a pipe section.

            * ``PRETENSION`` - Defines a pretension section.

            * ``REINF`` - Defines a reinforcing section. This option has a ``Subtype``.

            * ``SHELL`` - Defines a shell section.

            * ``SUPPORT`` - Additive manufacturing support. This option has a ``Subtype``.

            * ``TAPER`` - Defines a tapered beam or pipe section. The sections at the end points must be
              topologically identical.

        subtype : str
            When ``Type`` = BEAM, the possible beam sections that can be defined for ``Subtype`` are:  This
            command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

            The following figure shows the shape of each cross section subtype:

            .. figure:: ../../../images/_commands/gSECT1.svg

            When ``Type`` = COMB, the only possible `composite-beam section
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_
            that can be defined for ``Subtype`` is:  This command contains some tables and extra information
            which can be inspected in the original documentation pointed above.

            When ``Type`` = CONTACT, the possible contact sections that can be defined for ``Subtype`` are:
            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

            When ``Type`` = GENB, the possible `nonlinear general beam sections
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_
            that can be defined for ``Subtype`` are:  This command contains some tables and extra
            information which can be inspected in the original documentation pointed above.

            When ``Type`` = JOINT, the possible joint sections that can be defined for ``Subtype`` are:
            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

            When ``Type`` = REINF, the possible reinforcing sections that can be defined for ``Subtype``
            are: This command contains some tables and extra information which can be inspected in the
            original documentation pointed above.

            When ``Type`` = SUPPORT, the possible support sections that can be defined for ``Subtype`` are:
            This command contains some tables and extra information which can be inspected in the original
            documentation pointed above.

        name : str
            An eight-character name for the section. ``Name`` can be a string such as "W36X210" or "HP13X73"
            for beam sections. Section name can consist of letters and numbers, but cannot contain
            punctuation, special characters, or spaces.

        refinekey : str
            Sets mesh refinement level for thin-walled beam sections. Valid values are 0 (the default - no
            mesh refinement) through 5 (high level of mesh refinement). This value has meaning only when
            ``Type`` = BEAM.

        Notes
        -----

        .. _SECTYPE_notes:

        :ref:`sectype` sets the section ID number, section type, and subtype for a section. A previously-
        defined section with the same identification number will be redefined. The geometry data describing
        this section type is defined by a subsequent :ref:`secdata` command. Define the offsets (if
        applicable) by a subsequent :ref:`secoffset` command. The :ref:`slist` command lists the section
        properties, and the :ref:`secplot` command displays the section to scale. The :ref:`secnum` command
        assigns the section ID number to any subsequently-defined elements.

        When defining a section for contact elements ( ``Type`` = CONTACT) that are used in a `general
        contact <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_toolsgencont.html>`_
        definition, a section number representing a general contact surface can be specified. Alternatively,
        you may define a subset of a region by inputting a valid label for ``SECID`` (ALL_EDGE, ALL_FACE,
        ALL_VERT, ALL_TOP,or ALL_BOT), or by inputting a node component name with or without a component
        name extension (_EDGE, _FACE, _VERT, _TOP, or _BOT). For more information, see in the `Contact
        Technology Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_ctec/ctec_flpressexamp.html>`_.

        For a beam section ( ``Type`` = BEAM), a subsequent :ref:`secdata` command builds a numeric model
        using a nine-node cell for determining the properties ( ``Ixx``, ``Iyy``, etc.) of the section and
        for the solution to the Poisson's equation for torsional behavior. See `Beam Analysis and Cross
        Sections <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR15_6.html>`_ in
        the `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_ for
        examples using the section commands.

        For a `nonlinear general beam section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STRNGBS.html#strngbscons>`_ (
        ``Type`` = GENB), the ``Subtype`` and ``REFINEKEY`` options do not apply. Subsequent commands are
        necessary to define the section: :ref:`bsax`, :ref:`bsm1`, :ref:`bsm2`, :ref:`bstq`, :ref:`bss1`,
        :ref:`bss2`, :ref:`bsmd`, and :ref:`bste` are available. All other section commands are ignored for
        this section type.

        For a `preintegrated composite-beam section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PREBEAMSECT_5.html#>`_ (
        ``Type`` = COMB), the ``REFINEKEY`` options do not apply. Subsequent commands are necessary to
        define the section: :ref:`cbtmp`, :ref:`cbmx`, :ref:`cbmd`, and :ref:`cbte` are available. All other
        section commands are ignored for this section type.

        For a `tapered beam or pipe section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR15_4.html#>`_ ( ``Type`` =
        TAPER), two subsequent :ref:`secdata` commands are required (one for each end section). Section ends
        must be topologically identical (same ``Subtype``, number of cells and material IDs). For a tapered
        pipe section, end sections must have the same number of cells around the circumference and along the
        pipe wall, and the same shell section ID for a composite pipe wall.

        For a `preintegrated general shell section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        ( ``Type`` = GENS), the ``Subtype`` and ``REFINEKEY`` options do not apply. Subsequent commands are
        necessary to define the section: :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`,
        :ref:`ssbt`, and :ref:`sspm` are available. All other section commands are ignored for this section
        type.

        The PRETENSION section options of the :ref:`sectype` and :ref:`secdata` commands are documented
        primarily to aid your understanding of the data written by the :ref:`cdwrite` command.
        Ansys, Inc. recommends that you generate pretension sections via the :ref:`psmesh` command.

        For a reinforcing section ( ``Type`` = REINF), each subsequent :ref:`secdata` command defines the
        material, geometry, and orientation of one discrete reinforcing fiber ( ``Subtype`` = DISC) or one
        smeared reinforcing surface ( ``Subtype`` = SMEAR). When referenced by a ``MESH200`` element, only
        one :ref:`secdata` command is valid.

        A subsequent :ref:`secdata` command defines the geometry data describing this section type.

        To display elements with shapes determined from the section definition, issue the :ref:`eshape`
        command.

        .. _SECTYPE_prodres:

        Ansys Mechanical Pro :ref:`sectype`,COMB is not valid.
        """
        command = f"SECTYPE,{secid},{type_},{subtype},{name},{refinekey}"
        return self.run(command, **kwargs)

    def secwrite(self, fname: str = "", ext: str = "", elem_type: str = "", **kwargs):
        r"""Creates an ASCII file containing user mesh section information.

        Mechanical APDL Command: `SECWRITE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SECWRITE.html>`_

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the characters needed for the
            directory path). An unspecified directory path defaults to the working directory; in this case,
            you can use all 248 characters for the file name. The file name defaults to :file:`Jobname` if
            ``Fname`` is left blank.

        ext : str
            Filename extension (eight-character maximum). The extension defaults to SECT if ``Ext`` is left
            blank.

        elem_type : str
            Element type attribute pointer ( :ref:`et` ) for the elements that are part of the section. See
            :ref:`secread` for a detailed description.

        Notes
        -----

        .. _SECWRITE_notes:

        Before creating a user mesh file, first create a model using 2D meshing. Use ``PLANE183`` or
        ``MESH200`` with KEYOPT(1) = 7 (quadrilateral with 8 nodes option) to model the cells.
        :ref:`secwrite` creates an ASCII file that contains information about the nodes and cells that
        describe a beam section. For detailed information on how to create a user mesh file, see `Creating
        Custom Cross Sections with a User-defined Mesh
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR15_4.html#>`_ in the
        `Structural Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_enercalc_app.html>`_.
        """
        command = f"SECWRITE,{fname},{ext},,{elem_type}"
        return self.run(command, **kwargs)

    def sflex(
        self,
        ffax: str = "",
        ffby: str = "",
        ffbz: str = "",
        ffto: str = "",
        fftsy: str = "",
        fftsz: str = "",
        **kwargs,
    ):
        r"""Sets flexibility factors for the currently defined pipe element section.

        Mechanical APDL Command: `SFLEX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFLEX.html>`_

        Parameters
        ----------
        ffax : str
            Factor to increase axial flexibility. The default value is 1.0.

        ffby : str
            Factor to increase bending flexibility about element y axis (bending in the element x-z plane).
            The default value is 1.0.

        ffbz : str
            Factor to increase bending flexibility about element z axis (bending in the element x-y plane).
            The default value is ``FFBY``.

        ffto : str
            Factor to increase torsional flexibility. The default value is 1.0.

        fftsy : str
            Factor to increase transverse shear flexibility in the element x-z plane. The default value is
            1.0.

        fftsz : str
            Factor to increase transverse shear flexibility in the element x-y plane. The default value is
            ``FFTSY``.

        Notes
        -----

        .. _SFLEX_notes:

        The :ref:`sflex` command sets section-flexibility factors for sections used by pipe elements.

        To increase stiffness, use a flexibility factor of less than 1.0.

        The ``FFBY`` and ``FFTSY`` arguments affect motion in the element x-z plane, and the ``FFBZ`` and
        ``FFTSZ`` arguments affect motion in the element x-y plane. For stout pipe structures with low
        slenderness ratios, set both FFBY and FFTSY--and/or both FFBZ and FFTSZ (the related bending and
        transverse shear factors)--to the same value to obtain the expected flexibility effect.

        When issued, the :ref:`sflex` command applies to the pipe section most recently defined via the
        :ref:`sectype` command.

        :ref:`sflex` is valid only for linear material properties and small strain analyses. The command
        does not support offsets, temperature loading, or initial state loading. While the resulting
        displacements and reactions are valid, the stresses may not be valid.
        """
        command = f"SFLEX,{ffax},{ffby},{ffbz},{ffto},{fftsy},{fftsz}"
        return self.run(command, **kwargs)

    def slist(
        self,
        sfirst: str = "",
        slast: str = "",
        sinc: str = "",
        details: str = "",
        type_: str = "",
        **kwargs,
    ):
        r"""Summarizes the section properties for all defined sections in the current session.

        Mechanical APDL Command: `SLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SLIST.html>`_

        Parameters
        ----------
        sfirst : str
            First section ID to be summarized. Default = First available section in the database.

        slast : str
            Last section ID to be summarized. Default = Last available section in the database.

        sinc : str
            Increment of the section ID. Default = 1.

        details : str
            Determines the content of the summarized information for beam, pipe, shell, and reinforcing
            sections.

            * ``BRIEF`` - For beams, lists only the section integrated properties (such as Area, Iyy, and Iyz ).
              This option is the default.

              For `reinforcing
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_,
              lists only the input reinforcing properties (such as material, cross-section area, fiber spacing,
              and input fiber location parameters).

            * ``FULL`` - For beams, lists the section integrated properties, as well as the section nodal
              coordinates, section cell connectivity information, and section cell integration point coordinates.
              For shells, the section stiffness (membrane, bending, membrane-bending coupling and transverse
              shear) are printed.

              The shell section stiffness listed considers elastic behavior of materials at reference temperature
              only. The elements that use the section data may alter the transverse shear stiffness based on
              slenderness considerations (in addition to the shear correction factors shown).

              Section stiffness terms listed via the FULL option do not include section offsets. The program
              accounts for section offsets during the solution phase of the analysis.

              For predefined reinforcing sections used by the standard method, lists the complete information of
              reinforcing fibers or surfaces (including material ID, cross-section area, fiber spacing,
              orientation, and locations in natural coordinates). For predefined section reinforcing used by the
              mesh-independent method, lists section properties to generate the fibers or surfaces (including
              material ID, cross-section area, fiber spacing, and orientation) For reinforcing sections generated
              ( :ref:`ereinf` ) via the mesh-independent method, lists element ID, material ID, and locations in
              natural coordinates.

            * ``GROUP`` - If a section calls other sections, this option lists those sections too.

        type_ : str
            The section type. Valid arguments are ALL (default) or any valid section type ( :ref:`sectype`
            ).

        Notes
        -----

        .. _SLIST_notes:

        By default, the command lists information about all sections. You can limit the output to specific
        section types via the ``Type`` key.

        When ocean loading is present, the command lists beam section properties used by ocean loading.

        .. _SLIST_extranote1:

        Following is example output from the :ref:`slist`,,,,BRIEF command for a rectangular beam section
        subtype ( :ref:`sectype`,,BEAM,RECT):

        .. code:: apdl

           LIST SECTION ID SETS     1 TO     1 BY     1

             SECTION ID NUMBER:         1
             BEAM SECTION TYPE:     Rectangle
             BEAM SECTION NAME IS:
             BEAM SECTION DATA SUMMARY:
              Area                 =  6.0000
              Iyy                  =  4.5000
              Iyz                  = 0.11281E-15
              Izz                  =  2.0000
              Warping Constant     = 0.23299
              Torsion Constant     =  4.7330
              Center of Gravity Y  =-0.30973E-16
              Center of Gravity Z  = 0.15376E-15
              Shear Center Y       =-0.22957E-13
              Shear Center Z       = 0.31281E-13

              Beam Section is offset to CENTROID of cross section
        """
        command = f"SLIST,{sfirst},{slast},{sinc},{details},{type_}"
        return self.run(command, **kwargs)

    def sload(
        self,
        secid: str = "",
        plnlab: str = "",
        kinit: str = "",
        kfd: str = "",
        fdvalue: str = "",
        lsload: str = "",
        lslock: str = "",
        **kwargs,
    ):
        r"""Loads a pretension section.

        Mechanical APDL Command: `SLOAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SLOAD.html>`_

        **Command default:**

        .. _SLOAD_default:

        The default pretension load value ``FDVALUE`` is zero (no load). A positive value puts the
        pretension elements in tension.

        No default exists for the ``LSLOAD`` applied load step value. You must specify the load step in
        which to apply the ``FDVALUE``.

        No default exists for the ``LSLOCK`` locked load step value. You must specify the load step in which
        to lock the ``FDVALUE``.

        Parameters
        ----------
        secid : str
            Unique section number. The number must already be assigned to a pretension section.

        plnlab : str
            Label representing the pretension load sequence number in the format "PL ``nn`` " where ``nn``
            is an integer from 1 through 99 (for example, PL01 through PL99).

            Specify a value of DELETE to delete all loads on the specified pretension section ( ``SECID`` ).
            In this case, the command ignores any other argument values.

        kinit : str
            Initial action key for pretension load PL01. (This field is omitted for PL02 and up.) Three
            scenarios are possible:

            * ``LOCK`` - Constrains (connects) the cutting plane on the pretension section. This value is the
              default.

            * ``SLID`` - Unconstrains (disconnects) the cutting plane on the pretension section.

            * ``TINY`` - Applies a very small pretension load (0.1% of ``FDVALUE`` ) before the desired load is
              established. The small load prevents convergence problems which can occur when the desired load is
              not established in the first load step. This value is valid only if ``KFD`` = FORC.

        kfd : str
            Force/Displacement key. Specifies whether ``FDVALUE`` is a force or a displacement:

            * ``FORC`` - Apply a force on the specified pretension section. This value is the default.

            * ``DISP`` - Apply a displacement (adjustment) on the specified pretension section.

        fdvalue : str
            Pretension load value. If ``KFD`` = FORC, this value is a pretension force. If ``KFD`` = DISP,
            this value is a pretension displacement (adjustment).

        lsload : str
            Load step in which to apply the ``FDVALUE``.

        lslock : str
            The load step in which the displacement value resulting from the pretension force is locked.
            This value is valid only if ``KFD`` = FORC.

        Notes
        -----

        .. _SLOAD_notes:

        The :ref:`sload` command applies pretension loads to specified pretension sections ( ``PRETS179``
        -based) created via the :ref:`psmesh` command. A pretension load is ramp-applied ( :ref:`kbc` = 0)
        if it is a force ( ``KFD`` = FORC), and step-applied ( :ref:`kbc` = 1) if it is a displacement (
        ``KFD`` = DISP).

        You can lock the load value at a specified load step. When locked, the load changes from a force to
        a displacement, and the program applies the load as a constant displacement in all future load
        steps. Locking is useful when applying additional loadings. The additional loadings alter the effect
        of the initial load value, but because locking transforms the load into a displacement, it preserves
        the initial load's effect.

        In modal and harmonic analyses, any pretension load (force, displacement, or locked) is ignored and
        no load is produced.

        The :ref:`sload` command is not valid for ``MPC184`` -based preload sections created with
        :ref:`psmesh`.

          **Example: Applying a Load**

          The following command shows how to establish loads on a pretension section:

          .. code:: apdl

             SLOAD,1,PL01,TINY,FORC,5000,2,3

          In this example, the load is applied to pretension section

          .. code:: apdl

             1

         , and the sequence begins with the initial action key, ``KINIT``, set to ``TINY``. A small
          stabilization load (5 = 0.10% of 5000) is applied in the first load step, as the actual pretension
          force is not applied until the second load step. The next four fields set the actual load: the
          ``KFD`` value ``FORC`` specifies the type of load, ``FDVALUE`` defines the pretension load value (
          ``5000`` ), ``LSLOAD`` specifies the load step in which the force is applied ( ``2`` ), and the
          ``LSLOCK`` field specifies the load step in which the force is locked ( ``3`` ). Additional sets of
          four fields can be used to define additional loads.

          **Example: Editing an Existing Load**

          You can use the :ref:`sload` command to edit (overwrite) existing loads on a pretension section.
          This example changes the load on pretension section 1 (set above) to 6000:

          .. code:: apdl

             SLOAD,1,PL01,,,6000,2,3

          Unspecified values (blank fields), as shown in this example, remain unchanged from prior settings.
          If no prior specifications exist, then default values ( ``KINIT`` = LOCK and ``KFD`` = FORC) apply.

          **Example: Deleting All Loads**

          The command can also delete all loads on a specified pretension section, as shown here:

          .. code:: apdl

             SLOAD,1,DELETE

          **Example: Locking a Pretension Element**

          For a prestressed modal analysis, this command locks the pretension element:

          .. code:: apdl

             SLOAD,1,PL01,LOCK,DISP,0,1,2

        **Multiple Loadings**
        The :ref:`sload` command allows you to apply multiple loadings. You can add up to 15 loadings (PL01
        through PL15), or delete loadings, for any given pretension section(s).

          **Example: Applying Multiple Loadings**

          The following :ref:`sload` commands, issued in the order shown, establish a pretension load sequence
          in pretension section 2 with a force of 25 in load step (LS) 2, locked in LS 3-6, a force of 50 in
          LS 7, locked in LS 8-11, a force of 75 in LS 12, locked in LS 13 and beyond:

          .. code:: apdl

             SLOAD,2,PL01,LOCK,FORC,25,2,3

          .. code:: apdl

             SLOAD,2,PL02,,FORC,50,7,8

          .. code:: apdl

             SLOAD,2,PL03,,FORC,75,12,13

          At the same time, you can issue SLOAD commands to apply loads on other pretension sections. For
          example, in addition to the commands listed above, you could issue the following command to apply a
          load on pretension section 3:

          .. code:: apdl

             SLOAD,3,PL01,LOCK,FORC,25,3,4

        Any addition or deletion of a loading applies to the selected sections only. Mechanical APDL does
        not apply
        or delete a load until you click the Apply or OK button.

        After you have successfully solved for a specified ``LSLOAD`` (GUI field Apply at LS ) and
        eventually ``LSLOCK`` (GUI field Lock at LS ) value, you cannot modify that loading's settings
        during subsequent steps of the analysis. Similarly, you cannot delete loadings that you have already
        partially or completely solved.

        You can select more than one pretension section at a time in order to specify identical loadings on
        them. Before you completely solve a given loading, any combination of pretension sections is valid.
        The following limitations apply:

        * After you have completely solved one or more loadings, Mechanical APDL allows multiple selection
        of only
          those pretension sections having

        .. flat-table ::

        * -- the same number of defined loadings, and * -- the identical loading number from the most recent

          completely solved loading.

        * A multiple selection meeting the necessary criteria retains the settings that are identical for
          all selected pretension sections and leaves all other fields blank.
        """
        command = f"SLOAD,{secid},{plnlab},{kinit},{kfd},{fdvalue},{lsload},{lslock}"
        return self.run(command, **kwargs)

    def ssbt(
        self, bt11: str = "", bt22: str = "", bt12: str = "", t: str = "", **kwargs
    ):
        r"""Specifies preintegrated bending thermal effects for shell sections.

        Mechanical APDL Command: `SSBT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSBT.html>`_

        Parameters
        ----------
        bt11 : str
            Bending thermal effects component [ **B**  :sup:`T` ].

        bt22 : str
            Bending thermal effects component [ **B**  :sup:`T` ].

        bt12 : str
            Bending thermal effects component [ **B**  :sup:`T` ].

        t : str
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        :

        .. math::

            equation not available

        The :ref:`ssbt` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_,
        specifies the bending thermal effects quantity (submatrix [ **B**  :sup:`T` ] data) for a
        preintegrated shell section. The section data defined is associated with the section most recently
        defined (via the :ref:`sectype` command).

        The [ **B**  :sup:`T` ] quantity represents bending stress resultants caused by a unit raise in
        temperature on a fully constrained model. For a layered composite shell, it is usually necessary to
        specify both the [ **B**  :sup:`T` ] and [ **M**  :sup:`T` ] quantities (by issuing the :ref:`ssbt`
        and :ref:`ssmt` commands, respectively).

        Unspecified values default to zero.

        Related commands are :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`, and
        :ref:`sspm`.

        If you are using the ``SHELL181`` or ``SHELL281`` element's Membrane option (KEYOPT(1) = 1), it is
        not necessary to issue this command.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        """
        command = f"SSBT,{bt11},{bt22},{bt12},{t}"
        return self.run(command, **kwargs)

    def ssmt(
        self, mt11: str = "", mt22: str = "", mt12: str = "", t: str = "", **kwargs
    ):
        r"""Specifies preintegrated membrane thermal effects for shell sections.

        Mechanical APDL Command: `SSMT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSMT.html>`_

        Parameters
        ----------
        mt11 : str
            Membrane thermal effects component [ **M**  :sup:`T` ].

        mt22 : str
            Membrane thermal effects component [ **M**  :sup:`T` ].

        mt12 : str
            Membrane thermal effects component [ **M**  :sup:`T` ].

        t : str
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        :

        .. math::

            equation not available

        The :ref:`ssmt` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_,
        specifies the membrane thermal effects quantity (submatrix [ **M**  :sup:`T` ] data) for a
        preintegrated shell section. The section data defined is associated with the section most recently
        defined (via the :ref:`sectype` command).

        The [ **M**  :sup:`T` ] quantity represents membrane stress resultants caused by a unit raise in
        temperature on a fully constrained model. For a layered composite shell, it is usually necessary to
        specify both the [ **M**  :sup:`T` ] and [ **B**  :sup:`T` ] quantities (by issuing the :ref:`ssmt`
        and :ref:`ssbt` commands, respectively).

        Unspecified values default to zero.

        Related commands are :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssbt`, and
        :ref:`sspm`.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        """
        command = f"SSMT,{mt11},{mt22},{mt12},{t}"
        return self.run(command, **kwargs)

    def sspa(
        self,
        a11: str = "",
        a21: str = "",
        a31: str = "",
        a22: str = "",
        a32: str = "",
        a33: str = "",
        t: str = "",
        **kwargs,
    ):
        r"""Specifies a preintegrated membrane stiffness for shell sections.

        Mechanical APDL Command: `SSPA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSPA.html>`_

        Parameters
        ----------
        a11 : str
            Membrane stiffness component (symmetric lower part of submatrix [ **A** ]).

        a21 : str
            Membrane stiffness component (symmetric lower part of submatrix [ **A** ]).

        a31 : str
            Membrane stiffness component (symmetric lower part of submatrix [ **A** ]).

        a22 : str
            Membrane stiffness component (symmetric lower part of submatrix [ **A** ]).

        a32 : str
            Membrane stiffness component (symmetric lower part of submatrix [ **A** ]).

        a33 : str
            Membrane stiffness component (symmetric lower part of submatrix [ **A** ]).

        t : str
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        :

        .. math::

            equation not available

        The :ref:`sspa` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_,
        specifies the membrane stiffness quantity (submatrix [ **A** ]) for a preintegrated shell
        section. The section data defined is associated with the section most
        recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`, :ref:`ssbt`, and
        :ref:`sspm`.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        """
        command = f"SSPA,{a11},{a21},{a31},{a22},{a32},{a33},{t}"
        return self.run(command, **kwargs)

    def sspb(
        self,
        b11: str = "",
        b21: str = "",
        b31: str = "",
        b22: str = "",
        b32: str = "",
        b33: str = "",
        t: str = "",
        b12: str = "",
        b13: str = "",
        b23: str = "",
        **kwargs,
    ):
        r"""Specifies a preintegrated coupling stiffness for shell sections.

        Mechanical APDL Command: `SSPB <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSPB.html>`_

        Parameters
        ----------
        b11 : str
            Coupling stiffness component (symmetric lower part of submatrix [ **B** ]).

        b21 : str
            Coupling stiffness component (symmetric lower part of submatrix [ **B** ]).

        b31 : str
            Coupling stiffness component (symmetric lower part of submatrix [ **B** ]).

        b22 : str
            Coupling stiffness component (symmetric lower part of submatrix [ **B** ]).

        b32 : str
            Coupling stiffness component (symmetric lower part of submatrix [ **B** ]).

        b33 : str
            Coupling stiffness component (symmetric lower part of submatrix [ **B** ]).

        t : str
            Temperature.

        b12 : str
            Upper part of submatrix [ **B** ]

        b13 : str
            Upper part of submatrix [ **B** ]

        b23 : str
            Upper part of submatrix [ **B** ]

        Notes
        -----
        The behavior of shell elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        :

        .. math::

            equation not available

        If the coefficients ``B`` 12, ``B`` 13, ``B`` 23 are undefined, the program uses a symmetric form of
        submatrix [ **B** ]. If any one of the coefficients ``B`` 12, ``B`` 13, ``B`` 23 is nonzero, the
        program considers submatrix [ **B** ] to be unsymmetric.

        The :ref:`sspb` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_,
        specifies the coupling stiffness quantity (submatrix [ **B** ] data) for a preintegrated shell
        section. The section data defined is associated with the section
        most recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`sspa`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`, :ref:`ssbt`, and
        :ref:`sspm`.

        If you are using the ``SHELL181`` or ``SHELL281`` element's Membrane option (KEYOPT(1) = 1), it is
        not necessary to issue this command.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        """
        command = f"SSPB,{b11},{b21},{b31},{b22},{b32},{b33},{t},{b12},{b13},{b23}"
        return self.run(command, **kwargs)

    def sspd(
        self,
        d11: str = "",
        d21: str = "",
        d31: str = "",
        d22: str = "",
        d32: str = "",
        d33: str = "",
        t: str = "",
        **kwargs,
    ):
        r"""Specifies a preintegrated bending stiffness for shell sections.

        Mechanical APDL Command: `SSPD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSPD.html>`_

        Parameters
        ----------
        d11 : str
            Bending stiffness component (symmetric lower part of submatrix [ **D** ]).

        d21 : str
            Bending stiffness component (symmetric lower part of submatrix [ **D** ]).

        d31 : str
            Bending stiffness component (symmetric lower part of submatrix [ **D** ]).

        d22 : str
            Bending stiffness component (symmetric lower part of submatrix [ **D** ]).

        d32 : str
            Bending stiffness component (symmetric lower part of submatrix [ **D** ]).

        d33 : str
            Bending stiffness component (symmetric lower part of submatrix [ **D** ]).

        t : str
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        :

        .. math::

            equation not available

        The :ref:`sspd` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_
        , specifies the bending stiffness quantity (submatrix [ **D** ] data) for a preintegrated
        shell section. The section data defined is associated with the section
        most recently defined (via the :ref:`sectype` command).

        Unspecified commands default to zero.

        Related commands are :ref:`sspa`, :ref:`sspb`, :ref:`sspe`, :ref:`ssmt`, :ref:`ssbt`, and
        :ref:`sspm`.

        If you are using the ``SHELL181`` or ``SHELL281`` element's Membrane option (KEYOPT(1) = 1), it is
        not necessary to issue this command.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        """
        command = f"SSPD,{d11},{d21},{d31},{d22},{d32},{d33},{t}"
        return self.run(command, **kwargs)

    def sspe(self, e11: str = "", e21: str = "", e22: str = "", t: str = "", **kwargs):
        r"""Specifies a preintegrated transverse shear stiffness for shell sections.

        Mechanical APDL Command: `SSPE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSPE.html>`_

        Parameters
        ----------
        e11 : str
            Transverse shear stiffness component (symmetric lower part of submatrix [ **E** ]).

        e21 : str
            Transverse shear stiffness component (symmetric lower part of submatrix [ **E** ]).

        e22 : str
            Transverse shear stiffness component (symmetric lower part of submatrix [ **E** ]).

        t : str
            Temperature.

        Notes
        -----
        The behavior of shell elements is governed by the generalized-stress/generalized-strain relationship
        of the `form
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        :

        .. math::

            equation not available

        The :ref:`sspe` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_,
        specifies the transverse shear stiffness quantity (submatrix [ **E** ] data) for a preintegrated
        shell section. The section data defined is associated with the section
        most recently defined (via the :ref:`sectype` command).

        Unspecified values default to zero.

        Related commands are :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`ssmt`, :ref:`ssbt`, and
        :ref:`sspm`.

        If you are using the ``SHELL181`` or ``SHELL281`` element's Membrane option (KEYOPT(1) = 1), it is
        not necessary to issue this command.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        .
        """
        command = f"SSPE,{e11},{e21},{e22},{t}"
        return self.run(command, **kwargs)

    def sspm(self, dens: str = "", t: str = "", **kwargs):
        r"""Specifies mass density for a preintegrated shell section.

        Mechanical APDL Command: `SSPM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SSPM.html>`_

        Parameters
        ----------
        dens : str

        t : str
            Temperature.

        Notes
        -----
        The :ref:`sspm` command, one of several `preintegrated shell section commands
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#membraneoptionnote>`_,
        specifies the mass density (assuming a unit thickness) for a preintegrated shell section. The value
        specified is associated with the section most recently defined (via the :ref:`sectype` command).

        Related commands are :ref:`sspa`, :ref:`sspb`, :ref:`sspd`, :ref:`sspe`, :ref:`ssmt`, and
        :ref:`ssbt`.

        For complete information, see `Creating a Preintegrated General Shell Section
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_PRESHELL_5.html#strpreshcons>`_
        """
        command = f"SSPM,{dens},{t}"
        return self.run(command, **kwargs)
