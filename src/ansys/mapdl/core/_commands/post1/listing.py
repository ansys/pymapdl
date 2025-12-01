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

from ansys.mapdl.core._commands import CommandsBase


class Listing(CommandsBase):

    def format(
        self,
        ndigit: str = "",
        ftype: str = "",
        nwidth: str = "",
        dsignf: str = "",
        line: str = "",
        char_: str = "",
        exptype: str = "",
        **kwargs,
    ):
        r"""Specifies format controls for tables.

        Mechanical APDL Command: `/FORMAT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FORMAT.html>`_

        Parameters
        ----------
        ndigit : str
            Number of digits (3 to 32) in first table column (usually the node or element number). Initially
            defaults to 7.

        ftype : str
            FORTRAN format type:

            * ``G`` - G ``xx.yy`` (default)

            * ``F`` - F ``xx.yy``

            * ``E`` - E ``xx.yy``

            where ``xx`` and ``yy`` are described below.

        nwidth : str
            Total width (9 to 32) of the field ( ``xx`` in ``Ftype`` ). Default = 13.

        dsignf : str
            Number of digits after the decimal point ( ``yy`` in F or E format) or number of significant
            digits in G format. Range is 2 to ``xx`` -7 for ``Ftype`` = G or E; and 0 to ``xx`` -4 for
            ``Ftype`` = F. Default = 5.

        line : str
            Number of lines (11 minimum) per page. Default = ``ILINE`` or ``BLINE`` ( :ref:`page` ).

        char_ : str
            Number of characters (41 to 240, system-dependent) per line before wraparound. Default =
            ``ICHAR`` or ``BCHAR`` ( :ref:`page` ).

        exptype : str
            Number of digits for the exponent ( ``Ftype`` = G):

            * ``3`` - Three digits (default).

            * ``2`` - Two digits.

        Notes
        -----

        .. _s-FORMAT_notes:

        Specifies various format controls for tables printed with the POST1 :ref:`prnsol`, :ref:`presol`,
        :ref:`pretab`, :ref:`prrsol`, :ref:`prpath`, and :ref:`cyccalc` commands. A blank (or out-of-range)
        field on the command retains the current setting. Issue :ref:`format`,STAT to display the current
        settings. Issue :ref:`format`,DEFA to reestablish the initial default specifications.

        For the POST26 :ref:`prvar` command, the ``Ftype``, ``NWIDTH``, and ``DSIGNF`` fields control the
        time output format.

        When viewing integer output quantities, the floating point format may lead to incorrect output
        values for large integers. You should verify large integer output values via the :ref:`get` command
        whenever possible.

        This command is valid in any processor.
        """
        command = f"/FORMAT,{ndigit},{ftype},{nwidth},{dsignf},{line},{char_},{exptype}"
        return self.run(command, **kwargs)

    def header(
        self,
        header: str = "",
        stitle: str = "",
        idstmp: str = "",
        notes: str = "",
        colhed: str = "",
        minmax: str = "",
        **kwargs,
    ):
        r"""Sets page and table heading print controls.

        Mechanical APDL Command: `/HEADER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_HEADER.html>`_

        Parameters
        ----------
        header : str
            Mechanical APDL page header (system, date, time, version, copyright, title, etc.):

            * ``ON`` - Turns this item on (default for batch mode; not available for interactive mode).

            * ``OFF`` - Turns this item off.

            * ``(blank)`` - Retains the previous setting.

        stitle : str
            Subtitles (see :ref:`stitle` command): ON, OFF, or (blank) (see above).

        idstmp : str
            Load step information (step number, substep number, time value): ON, OFF, or (blank) (see
            above).

        notes : str
            Information relative to particular table listings: ON, OFF, or (blank) (see above).

        colhed : str
            Column header labels of table listings (currently only for single column tables): ON, OFF, or
            (blank) (see above).

        minmax : str
            Minimum/maximum information or totals after table listings: ON, OFF, or (blank) (see above).

        Notes
        -----

        .. _s-HEADER_notes:

        Sets specifications on or off for page and table heading print controls associated with the POST1
        :ref:`prnsol`, :ref:`presol`, :ref:`pretab`, :ref:`prrsol`, and :ref:`prpath` commands. If the
        printout caused a top-of-form (page eject to top of next page), the top-of-form is also suppressed
        with the printout. Issue :ref:`header`,STAT to display the current settings. Issue
        :ref:`header`,DEFA to reset the default specifications.

        This command is valid in any processor.
        """
        command = f"/HEADER,{header},{stitle},{idstmp},{notes},{colhed},{minmax}"
        return self.run(command, **kwargs)

    def irlist(self, **kwargs):
        r"""Prints inertia relief summary table.

        Mechanical APDL Command: `IRLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_IRLIST.html>`_

        Notes
        -----

        .. _IRLIST_notes:

        Prints the inertia relief summary data, including the mass summary table, the total load summary
        table, and the inertia relief summary table resulting from the inertia relief calculations. These
        calculations are performed in the solution phase ( :ref:`solve` ) as specified by the :ref:`irlf`
        or :ref:`airl`  command.

        Inertia relief output is stored in the database rather than in the results file (
        :file:`Jobname.RST` ). When you issue :ref:`irlist`  or :ref:`airl`, Mechanical APDL pulls the
        information
        from the database, which contains the inertia relief output from the most recent solution (
        :ref:`solve` ).

        This command is valid in any processor.
        """
        command = "IRLIST"
        return self.run(command, **kwargs)

    def page(
        self,
        iline: str = "",
        ichar: str = "",
        bline: str = "",
        bchar: str = "",
        comma: str = "",
        **kwargs,
    ):
        r"""Defines the printout and screen page size.

        Mechanical APDL Command: `/PAGE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PAGE.html>`_

        **Command default:**

        .. _s-PAGE_default:

        As defined by the items above.

        Parameters
        ----------
        iline : str
            Number of lines (11 minimum) per "page" or screen. Defaults to 24. Applies to interactive non-
            GUI to the screen output only.

        ichar : str
            Number of characters (41 to 132) per line before wraparound. Defaults to 80. Applies to
            interactive non-GUI to the screen output only.

        bline : str
            Number of lines (11 minimum) per page. Defaults to 56. Applies to batch mode ( ``/BATCH`` ),
            diverted ( :ref:`output` ), or interactive GUI ( :ref:`menu` ) output. If negative, no page
            headers are output.

        bchar : str
            Number of characters (41 to 240 (system dependent)) per line before wraparound. Defaults to 140.
            Applies to batch mode ( ``/BATCH`` ), diverted ( :ref:`output` ), or interactive GUI (
            :ref:`menu` ) output.

        comma : str
            Input 1 to specify comma-separated output for node ( :ref:`nlist` ) and element ( :ref:`elist` )
            output.

        Notes
        -----

        .. _s-PAGE_notes:

        Defines the printout page size for batch runs and the screen page size for interactive runs. Applies
        to the POST1 :ref:`prnsol`, :ref:`presol`, :ref:`pretab`, :ref:`prrsol`, and :ref:`prpath` commands.
        See the :ref:`header` command for additional controls (page ejects, headers, etc.) that affect the
        amount of printout. A blank (or out-of-range) value retains the previous setting. Issue :ref:`page`
        ,STAT to display the current settings. Issue :ref:`page`,DEFA to reset the default specifications.

        This command is valid in any processor.
        """
        command = f"/PAGE,{iline},{ichar},{bline},{bchar},{comma}"
        return self.run(command, **kwargs)

    def prerr(self, **kwargs):
        r"""Prints SEPC and TEPC.

        Mechanical APDL Command: `PRERR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRERR.html>`_

        Notes
        -----

        .. _PRERR_notes:

        Prints the percent error in structural energy norm (SEPC) and the thermal energy norm percent error
        (TEPC). Approximations of mesh discretization error associated with a solution are calculated for
        analyses having structural or thermal degrees of freedom.

        The structural approximation is based on the energy error (which is similar in concept to the strain
        energy) and represents the error associated with the discrepancy between the calculated stress field
        and the globally continuous stress field (see `POST1 - Error Approximation Technique
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_post7.html#errormagbased>`_ in
        the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_). This
        discrepancy is due to the assumption in the elements that only the
        displacements are continuous at the nodes. The stress field is calculated from the displacements and
        should also be continuous, but generally is not.

        Thermal analyses may use any solid and shell thermal element having only temperature degrees of
        freedom. The thermal approximation is based on the total heat flow dissipation and represents the
        error associated with the discrepancy between the calculated nodal thermal flux within an element
        and a continuous global thermal flux. This continuous thermal flux is calculated with the normal
        nodal averaging procedure.

        The volume (result label VOLU) is used to calculate the energy error per element (result label SERR
        for the structural energy error and TERR for the thermal energy error). These energy errors, along
        with the appropriate energy, are then used to calculate the percent error in energy norm (SEPC for
        structural and TEPC for thermal). These percentages can be listed by the :ref:`prerr` command,
        retrieved by the :ref:`get` command (with labels SEPC and TEPC) for further calculations, and shown
        on the displacement display ( :ref:`pldisp` ), as applicable.

        For structural analyses, the maximum absolute value of nodal stress variation of any stress
        component for any node of an element (result item SDSG) is also calculated. Similarly, for thermal
        gradient components, TDSG is calculated. Minimum and maximum result bounds considering the possible
        effect of discretization error will be shown on contour displays ( :ref:`plnsol` ). For shell
        elements, the top surface location is used to produce a meaningful percentage value. SERR, TERR,
        SEPC, TEPC, SDSG, and TDSG will be updated whenever the nodal stresses or fluxes are recalculated.

        If the energy error is a significant portion of the total energy, then the analysis should be
        repeated using a finer mesh to obtain a more accurate solution. The energy error is relative from
        problem to problem but will converge to a zero energy error as the mesh is refined.

        **The following element- and material-type limitations apply:**

        * Valid with most 2D solid, 3D solid, axisymmetric solid, or 3D shell elements.

        * The model should have only structural or thermal degrees of freedom.

        * The analysis must be linear (for both material and geometry).

        * Multi-material (for example, composite) elements are not valid.

        * Transition regions from one material to another are not valid (that is, the entire model should
          consist of one material).

        * Anisotropic materials ( :ref:`tb`,ANEL) are not considered.
        """
        command = "PRERR"
        return self.run(command, **kwargs)

    def priter(self, **kwargs):
        r"""Prints solution summary data.

        Mechanical APDL Command: `PRITER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRITER.html>`_

        Notes
        -----

        .. _PRITER_notes:

        Prints solution summary data (such as time step size, number of equilibrium iterations, convergence
        values, etc.) from a static or full transient analysis. All other analyses print zeros for the data.
        """
        command = "PRITER"
        return self.run(command, **kwargs)
