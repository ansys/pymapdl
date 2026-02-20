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


class SolidSurfaceLoads:

    def sfa(
        self,
        area: str = "",
        lkey: str = "",
        lab: str = "",
        value: str = "",
        value2: str = "",
        **kwargs,
    ):
        r"""Specifies surface loads on the selected areas.

        Mechanical APDL Command: `SFA <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFA.html>`_

        Parameters
        ----------
        area : str
            Area to which surface load applies. If ALL, apply load to all selected areas ( :ref:`asel` ). If
            ``Area`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component may be substituted for ``Area``.

        lkey : str
            Load key associated with surface load (defaults to 1). Load keys (1,2,3, etc.) are listed under
            "Surface Loads" in the input data table for each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_. ``LKEY``
            is ignored if the area is the face of a volume region meshed with volume elements.

        lab : str
            Valid surface load label. Load labels are listed under "Surface Loads" in the input table for
            each area type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.

             This command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sfa1:

            Thermal labels CONV and HFLUX are mutually exclusive.

            .. _sfa2:

            For an acoustic analysis, apply the fluid-structure interaction flag (Label = FSI) to only the
            ``FLUID129`` or ``FLUID130`` elements.

        value : str
            Surface load value or table name reference for specifying tabular boundary conditions.

            If ``Lab`` = CONV:

            * ``VALUE`` is typically the film coefficient and ``VALUE2`` (below) is typically the bulk
              temperature. If ``Lab`` = CONV and ``VALUE`` = - ``N``, the film coefficient may be a function of
              temperature and is determined from the HF property table for material ``N`` ( :ref:`mp` ). (See
              the :ref:`scopt` command for a way to override this option and use - ``N`` as the film
              coefficient.) The temperature used to evaluate the film coefficient is usually the average between
              the bulk and wall temperatures, but may be user-defined for some elements.
            * If :ref:`kbc`,0 has been issued for ramped loads, it affects only ``VALUE2``, :ref:`the bulk
              temperature, and the film coefficient specification is unaffected. <SFA_V2CONV>`
            *

            If ``Lab`` = RAD, ``VALUE`` is the surface emissivity.

            If ``Lab`` = PORT, ``VALUE`` is a port number representing a waveguide exterior port. The port
            number must be an integer between 1 and 50. For acoustic 2×2 transfer admittance matrix, the port
            number can be any positive integer. The smaller port number corresponds to the port 1 of the 2×2
            transfer admittance matrix and the greater port number corresponds to the port 2. If one port of the
            transfer admittance matrix is connecting to the acoustic-structural interaction interface, the port
            number corresponds to the port 2 of the transfer admittance matrix. A pair of ports of the 2×2
            transfer admittance matrix must be defined in the same element.

            If ``Lab`` = SHLD, ``VALUE`` is the surface normal velocity in harmonic analysis and the surface
            normal acceleration in transient analysis for acoustics.

            If ``Lab`` = IMPD, ``VALUE`` is resistance in (N)(s)/m :sup:`3` if ``VALUE`` > 0 and is conductance
            in mho if ``VALUE`` < 0 for acoustics. In acoustic transient analyses, ``VALUE2`` is not used.

            If ``Lab`` = RDSF, ``VALUE`` is the emissivity value; the following conditions apply: If ``VALUE``
            is between 0 and 1, apply a single value to the surface. If ``VALUE`` = - ``N``, the emissivity may
            be a function of the temperature, and is determined from the EMISS property table for material ``N``
            ( :ref:`mp` ). The material ``N`` does not need to correlate with the underlying solid thermal
            elements.

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL to CFX analysis, ``VALUE`` is not used.

            If ``Lab`` = ATTN, ``VALUE`` is the absorption coefficient of the surface.

        value2 : str
            Second surface load value (if any).

            If ``Lab`` = CONV:

            * ``VALUE2`` is typically the bulk temperature for thermal analyses.
            * If :ref:`kbc`,0 has been issued for ramped loads, the bulk temperature is ramped from the value
              defined by :ref:`tunif` to the value specified by ``VALUE2`` for the first loadstep. If
              :ref:`tabular boundary conditions are defined, the <SFA_tabBC>` :ref:`kbc` command is ignored and
              tabular values are used.
            * For acoustic analyses, VALUE2 is not used.

            If ``Lab`` = RAD ``VALUE2`` is ambient temperature.

            If ``Lab`` = SHLD, ``VALUE2`` is the phase angle of the normal surface velocity (defaults to zero)
            for harmonic response analyses while ``VALUE2`` is not used for transient analyses in acoustics.

            If ``Lab`` = IMPD, ``VALUE2`` is reactance in (N)(s)/m :sup:`3` if ``VALUE`` > 0 and is the product
            of susceptance and angular frequency if ``VALUE`` < 0 for acoustics.

            If ``Lab`` = RDSF, ``VALUE2`` is the enclosure number. Radiation will occur between surfaces flagged
            with the same enclosure numbers. If the enclosure is open, radiation will also occur to ambient. If
            ``VALUE2`` is negative, radiation direction is reversed and will occur inside the element for the
            flagged radiation surfaces.

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL to CFX analysis, ``VALUE2`` is the surface interface
            number (not available from within the GUI).

        Notes
        -----

        .. _SFA_notes:

        Surface loads may be transferred from areas to elements with the :ref:`sftran` or :ref:`sbctran`
        commands. See the :ref:`sfgrad` command for an alternate tapered load capability.

        Tabular boundary conditions Tabular boundary conditions ( ``VALUE`` = ``tabname`` and/or ``VALUE2``
        = ``tabname``) are available
        for the following surface load labels ( ``Lab`` ) only: PRES (real and/or imaginary components),
        CONV (film coefficient and/or bulk temperature) or HFLUX, and RAD (surface emissivity and ambient
        temperature). Use the :ref:`dim` command to define a table.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via the :ref:`lvscale` command.

        This command is also valid in PREP7.
        """
        command = f"SFA,{area},{lkey},{lab},{value},{value2}"
        return self.run(command, **kwargs)

    def sfadele(self, area: str = "", lkey: str = "", lab: str = "", **kwargs):
        r"""Deletes surface loads from areas.

        Mechanical APDL Command: `SFADELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFADELE.html>`_

        Parameters
        ----------
        area : str
            Area to which surface load deletion applies. If ALL, delete load from all selected areas (
            :ref:`asel` ). If ``AREA`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``AREA``.

        lkey : str
            Load key associated with surface load (defaults to 1). See the :ref:`sfa` command for details.

        lab : str
            Valid surface load label. If ALL, use all appropriate labels. See the :ref:`sfa` command for
            labels.

        Notes
        -----

        .. _SFADELE_notes:

        Deletes surface loads (and all corresponding finite element loads) from selected areas.

        This command is also valid in PREP7.
        """
        command = f"SFADELE,{area},{lkey},{lab}"
        return self.run(command, **kwargs)

    def sfalist(self, area: str = "", lab: str = "", **kwargs):
        r"""Lists the surface loads for the specified area.

        Mechanical APDL Command: `SFALIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFALIST.html>`_

        Parameters
        ----------
        area : str
            Area at which surface load is to be listed. If ALL (or blank), list for all selected areas (
            :ref:`asel` ). If ``AREA`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``AREA``.

        lab : str
            Valid surface load label. If ALL (or blank), use all appropriate labels. See the :ref:`sfa`
            command for labels.

        Notes
        -----

        .. _SFALIST_notes:

        This command is valid in any processor.
        """
        command = f"SFALIST,{area},{lab}"
        return self.run(command, **kwargs)

    def sfl(
        self,
        line: str = "",
        lab: str = "",
        vali: str = "",
        valj: str = "",
        val2i: str = "",
        val2j: str = "",
        **kwargs,
    ):
        r"""Specifies surface loads on lines of an area.

        Mechanical APDL Command: `SFL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFL.html>`_

        Parameters
        ----------
        line : str
            Line to which surface load applies. If ALL, apply load to all selected lines ( :ref:`lsel` ). If
            ``Line`` = P, graphical picking is enabled and all remaining command fields are ignored (valid
            only in the GUI). A component name may be substituted for ``Line``.

        lab : str
            Valid surface load label. Load labels are listed under "Surface Loads" in the input table for
            each element type in the `Element Reference
            <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_.  This
            command contains some tables and extra information which can be inspected in the original
            documentation pointed above... _sfl1:

            Thermal labels CONV and HFLUX are mutually exclusive.

            .. _sfl2:

            For an acoustic analysis, apply the fluid-structure interaction flag (Label = FSI) to only the
            ``FLUID129`` or ``FLUID130`` elements.

        vali : str
            Surface load values at the first keypoint ( ``VALI`` ) and at the second keypoint ( ``VALJ`` ) of
            the line, or table name for specifying tabular boundary conditions. If ``VALJ`` is blank, it
            defaults to ``VALI``. If ``VALJ`` is zero, a zero is used.

            If ``Lab`` = CONV:

            * ``VALI`` and ``VALJ`` are the film coefficients and ``VAL2I`` and ``VAL2J`` are the bulk
              temperatures.
            * To specify a table, enclose the table name in percent signs (%), e.g., ``tabname``. (Issue
              :ref:`dim` to define a table.)
            * If ``Lab`` = CONV and ``VALI`` = - ``N``, the film coefficient may be a function of temperature
              and is determined from the HF property table for material ``N`` ( :ref:`mp` ). (See :ref:`scopt`
              for a way to override this option and use - ``N`` as the film coefficient.)
            * If :ref:`kbc`,0 has been issued for ramped loads, it affects only the bulk temperatures, ``VAL2I``
              and ``VAL2J``, and the film coefficient specification, ``VALI`` and ``VALJ``, are unaffected.

            If ``Lab`` = RAD, ``VALI`` and ``VALJ`` values are surface emissivities and ``VAL2I`` and ``VAL2J``
            are ambient temperatures. The temperature used to evaluate the film coefficient is usually the
            average between the bulk and wall temperatures, but may be user-defined for some elements.

            If ``Lab`` = RDSF, ``VALI`` is the emissivity value. If ``VALI`` = ``-N``, the emissivity may be a
            function of the temperature and is determined from the EMISS property table for material ``N`` (
            :ref:`mp` ).

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL-to-CFX analysis, ``VALJ`` is the surface interface
            number (not available from within the GUI) and ``VALI`` is not used.

        valj : str
            Surface load values at the first keypoint ( ``VALI`` ) and at the second keypoint ( ``VALJ`` ) of
            the line, or table name for specifying tabular boundary conditions. If ``VALJ`` is blank, it
            defaults to ``VALI``. If ``VALJ`` is zero, a zero is used.

            If ``Lab`` = CONV:

            * ``VALI`` and ``VALJ`` are the film coefficients and ``VAL2I`` and ``VAL2J`` are the bulk
              temperatures.
            * To specify a table, enclose the table name in percent signs (%), e.g., ``tabname``. (Issue
              :ref:`dim` to define a table.)
            * If ``Lab`` = CONV and ``VALI`` = - ``N``, the film coefficient may be a function of temperature
              and is determined from the HF property table for material ``N`` ( :ref:`mp` ). (See :ref:`scopt`
              for a way to override this option and use - ``N`` as the film coefficient.)
            * If :ref:`kbc`,0 has been issued for ramped loads, it affects only the bulk temperatures, ``VAL2I``
              and ``VAL2J``, and the film coefficient specification, ``VALI`` and ``VALJ``, are unaffected.

            If ``Lab`` = RAD, ``VALI`` and ``VALJ`` values are surface emissivities and ``VAL2I`` and ``VAL2J``
            are ambient temperatures. The temperature used to evaluate the film coefficient is usually the
            average between the bulk and wall temperatures, but may be user-defined for some elements.

            If ``Lab`` = RDSF, ``VALI`` is the emissivity value. If ``VALI`` = ``-N``, the emissivity may be a
            function of the temperature and is determined from the EMISS property table for material ``N`` (
            :ref:`mp` ).

            If ``Lab`` = FSIN in a unidirectional Mechanical APDL-to-CFX analysis, ``VALJ`` is the surface interface
            number (not available from within the GUI) and ``VALI`` is not used.

        val2i : str
            Second surface load values (if any). If ``VAL2J`` is blank, it defaults to ``VAL2I``. If ``VAL2J``
            is zero, a zero is used. To specify a table ( ``Lab`` = CONV), enclose the table name in percent
            signs (%), for example, ``tabname``. Use the :ref:`dim` command to define a table.

            If ``Lab`` = CONV:

            * ``VAL2I`` and ``VAL2J`` are the bulk temperatures.
            * If :ref:`kbc`,0 has been issued for ramped loads, the bulk temperature is ramped from the value
              defined by :ref:`tunif` to the value specified by ``VALI`` and ``VALJ`` for the first loadstep. If
              tabular boundary conditions are defined, the :ref:`kbc` command is ignored and tabular values are
              used for the bulk temperatures.

            If ``Lab`` = RAD, ``VAL2I`` and ``VAL2J`` are the ambient temperatures.

            If ``Lab`` = RDSF, ``VAL2I`` is the enclosure number. Radiation will occur between surfaces flagged
            with the same enclosure numbers. If the enclosure is open, radiation will occur to the ambient.

            ``VAL2I`` and ``VAL2J`` are not used for other surface load labels.

        val2j : str
            Second surface load values (if any). If ``VAL2J`` is blank, it defaults to ``VAL2I``. If ``VAL2J``
            is zero, a zero is used. To specify a table ( ``Lab`` = CONV), enclose the table name in percent
            signs (%), for example, ``tabname``. Use the :ref:`dim` command to define a table.

            If ``Lab`` = CONV:

            * ``VAL2I`` and ``VAL2J`` are the bulk temperatures.
            * If :ref:`kbc`,0 has been issued for ramped loads, the bulk temperature is ramped from the value
              defined by :ref:`tunif` to the value specified by ``VALI`` and ``VALJ`` for the first loadstep. If
              tabular boundary conditions are defined, the :ref:`kbc` command is ignored and tabular values are
              used for the bulk temperatures.

            If ``Lab`` = RAD, ``VAL2I`` and ``VAL2J`` are the ambient temperatures.

            If ``Lab`` = RDSF, ``VAL2I`` is the enclosure number. Radiation will occur between surfaces flagged
            with the same enclosure numbers. If the enclosure is open, radiation will occur to the ambient.

            ``VAL2I`` and ``VAL2J`` are not used for other surface load labels.

        Notes
        -----

        .. _SFL_notes:

        Specifies surface loads on the selected lines of area regions. The lines represent either the edges
        of area elements or axisymmetric shell elements themselves. Surface loads may be transferred from
        lines to elements via :ref:`sftran` or :ref:`sbctran`. See :ref:`sfe` for a description of surface
        loads. Loads input on this command may be tapered. See :ref:`sfgrad` for an alternate tapered load
        capability.

        You can specify a table name only when using structural (PRES) and thermal (CONV [film coefficient
        and/or bulk temperature], HFLUX), and surface emissivity and ambient temperature (RAD) surface load
        labels. ``VALJ`` and ``VAL2J`` are ignored for tabular boundary conditions.

        In a mode-superposition harmonic or transient analysis, you must apply the load in the modal portion
        of the analysis. Mechanical APDL calculates a load vector and writes it to the :file:`MODE` file,
        which you
        can apply via :ref:`lvscale`.

        This command is also valid in PREP7.
        """
        command = f"SFL,{line},{lab},{vali},{valj},{val2i},{val2j}"
        return self.run(command, **kwargs)

    def sfldele(self, line: str = "", lab: str = "", **kwargs):
        r"""Deletes surface loads from lines.

        Mechanical APDL Command: `SFLDELE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFLDELE.html>`_

        Parameters
        ----------
        line : str
            Line to which surface load deletion applies. If ALL, delete load from all selected lines (
            :ref:`lsel` ). If ``LINE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``LINE``.

        lab : str
            Valid surface load label. If ALL, use all appropriate labels. See the :ref:`sfl` command for
            labels.

        Notes
        -----

        .. _SFLDELE_notes:

        Deletes surface loads (and all corresponding finite element loads) from selected lines.

        This command is also valid in PREP7.
        """
        command = f"SFLDELE,{line},{lab}"
        return self.run(command, **kwargs)

    def sfllist(self, line: str = "", lab: str = "", **kwargs):
        r"""Lists the surface loads for lines.

        Mechanical APDL Command: `SFLLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFLLIST.html>`_

        Parameters
        ----------
        line : str
            Line at which surface load is to be listed. If ALL (or blank), list for all selected lines (
            :ref:`lsel` ). If ``LINE`` = P, graphical picking is enabled and all remaining command fields
            are ignored (valid only in the GUI). A component name may be substituted for ``LINE``.

        lab : str
            Valid surface load label. If ALL (or blank), use all appropriate labels. See the :ref:`sfl`
            command for labels.

        Notes
        -----

        .. _SFLLIST_notes:

        Lists the surface loads for the specified line.

        This command is valid in any processor.
        """
        command = f"SFLLIST,{line},{lab}"
        return self.run(command, **kwargs)

    def sftran(self, **kwargs):
        r"""Transfer the solid model surface loads to the finite element model.

        Mechanical APDL Command: `SFTRAN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SFTRAN.html>`_

        Notes
        -----

        .. _SFTRAN_notes:

        Surface loads are transferred only from selected lines and areas to all selected elements. The
        :ref:`sftran` operation is also done if the :ref:`sbctran` command is issued or automatically done
        upon initiation of the solution calculations ( :ref:`solve` ).

        This command is also valid in PREP7.
        """
        command = "SFTRAN"
        return self.run(command, **kwargs)
