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

from ansys.mapdl.core._commands import CommandsBase


class Controls(CommandsBase):

    def avprin(self, key: int | str = "", effnu: str = "", **kwargs):
        r"""Specifies how principal and vector sums are to be calculated.

        Mechanical APDL Command: `AVPRIN <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AVPRIN.html>`_

        **Command default:**

        .. _AVPRIN_default:

        Average components at common node before principal or vector sum calculation except for the von
        Mises equivalent strain (EQV), see below.

        Parameters
        ----------
        key : int or str
            Averaging key:

            * ``0`` - Average the component values from the elements at a common node, then calculate the
              principal or vector sum from the averaged components (default).

            * ``1`` - Calculate the principal or vector sum values on a per element basis, then average these
              values from the elements at a common node.

        effnu : str
            Effective Poisson's ratio used for computing the von Mises equivalent strain (EQV). This command
            option is intended for use with line elements or in load case operations ( :ref:`lcoper` ); the
            program automatically selects the most appropriate effective Poisson's ratio, as discussed
            below.

        Notes
        -----

        .. _AVPRIN_notes:

        Selects the method of combining components for certain derived nodal results when two or more
        elements connect to a common node. The methods apply to the calculations of derived nodal principal
        stresses, principal strains, and vector sums for selects, sorts, and output ( :ref:`nsel`,
        :ref:`nsort`, :ref:`prnsol`, :ref:`plnsol`, etc.). The calculation of these nodal results excludes
        beam and pipe elements.

        This command also defines the effective Poisson's ratio ( ``EFFNU`` ) used for equivalent strain
        calculations. If you use ``EFFNU``, the default effective Poisson's ratios shown below will be
        overridden for all elements by the ``EFFNU`` value. To return to the default settings, issue the
        :ref:`reset` command. The default value for ``EFFNU`` is:

        * Poisson's ratio as defined on the :ref:`mp` commands for EPEL and EPTH

        * 0.5 for EPPL and EPCR

        * 0.5 if the referenced material is hyperelastic

        * 0.0 for line elements (includes beam, link, and pipe elements, as well as discrete elements),
          `cyclic symmetry analysis
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/cycsym_example.html>`_, mode
          superposition analyses (with ``MSUPkey`` = YES on the :ref:`mxpand` command), and load case
          operations ( :ref:`lcoper` ).

        * For multistage analysis, a value of ``EFFNU`` must always be specified.

        If ``EFFNU`` is specified, the calculation of von Mises equivalent strain (EQV) is performed
        according to the ``KEY`` setting. However, if ``EFFNU`` is not specified, or if the :ref:`avprin`
        command is not issued, the von Mises equivalent strain is calculated using the average of the
        equivalent strains from the elements at a common node (behavior of ``KEY`` =1) irrespective of the
        value of the averaging KEY.

        For a random vibration (PSD) analysis (for more details, see `Review the Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/Hlp_G_STR6_8.html#strcovtlm61199>`_

        * Issuing either :ref:`avprin`,0 or :ref:`avprin`,1 calculates the principal stresses using the
          appropriate averaging method. They are then used to determine SEQV. The output will have non-zero
          values for the principal stresses.

        * If :ref:`avprin` is not issued, the Segalman-Fulcher method is used to calculate SEQV. This method
          does not calculate principal stresses, but directly calculates SEQV from the component stresses;
          therefore, the output will have zero values for the principal stresses.

        This command is also valid in POST26, where applicable.

        See `Combined Stresses and Strains
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_str4.html#strucfailure>`_
        """
        command = f"AVPRIN,{key},{effnu}"
        return self.run(command, **kwargs)

    def avres(self, key: int | str = "", opt: str = "", **kwargs):
        r"""Specifies how results data will be averaged when PowerGraphics is enabled.

        Mechanical APDL Command: `AVRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AVRES.html>`_

        Parameters
        ----------
        key : int or str
            Averaging key.

            * ``1`` - Average results at all common subgrid locations.

            * ``2`` - Average results at all common subgrid locations except where material type ( :ref:`mat` )
              discontinuities exist. (Default.)

            * ``3`` - Average results at all common subgrid locations except where real constant ( :ref:`real` )
              discontinuities exist.

            * ``4`` - Average results at all common subgrid locations except where material type ( :ref:`mat` )
              or real constant ( :ref:`real` ) discontinuities exist.

        opt : str
            Option to determine how results data are averaged.

            * ``(blank)`` - Average surface results data using only the exterior element faces (default).

            * ``FULL`` - Average surface results data using the exterior face and interior element data.

        Notes
        -----

        .. _AVRES_notes:

        The :ref:`avres` command specifies how results data will be averaged at subgrid locations that are
        common to 2 or more elements. The command is valid only when PowerGraphics is enabled (via the
        :ref:`graphics`,POWER command).

        With PowerGraphics active ( :ref:`graphics`,POWER), the averaging scheme for surface data with
        interior element data included ( :ref:`avres`,,FULL) and multiple facets per edge ( :ref:`efacet`
        ,2 or :ref:`efacet`,4) will yield differing minimum and maximum contour values depending on the
        Z-Buffering options ( :ref:`slashtype`,,6 or :ref:`slashtype`,,7). When the Section data is not
        included in the averaging schemes ( :ref:`slashtype`,,7), the resulting absolute value for the
        midside node is significantly smaller.

        PowerGraphics does not average your stresses across discontinuous surfaces. The normals for various
        planes and facets are compared to a tolerance to determine continuity. The ``ANGLE`` value you
        specify in the :ref:`edge` command is the tolerance for classifying surfaces as continuous or
        "coplanar."

        The command affects nodal solution contour plots ( :ref:`plnsol` ), nodal solution printout (
        :ref:`prnsol` ), and subgrid solution results accessed through the Query Results function (under
        General Postprocessing) in the GUI.

        The command has no effect on the nodal degree of freedom solution values (UX, UY, UZ, TEMP, etc.).

        For cyclic symmetry mode-superposition harmonic solutions, :ref:`avres`,,FULL is not supported.
        Additionally, averaging does not occur across discontinuous surfaces, and the ``ANGLE`` value on the
        :ref:`edge` command has no effect.

        The section-based ( :ref:`mat` ) discontinuity in shells is accommodated via :ref:`eshape`.

        The command is also available in :ref:`slashsolu`.
        """
        command = f"AVRES,{key},{opt}"
        return self.run(command, **kwargs)

    def efacet(self, num: int | str = "", **kwargs):
        r"""Specifies the number of facets per element edge for PowerGraphics displays.

        Mechanical APDL Command: `/EFACET <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EFACET.html>`_

        **Command default:**

        .. _s-EFACET_default:

        As stated above.

        Parameters
        ----------
        num : int or str
            Number of facets per element edge for element plots.

            * ``1`` - Use 1 facet per edge (default for h-elements).

            * ``2`` - Use 2 facets per edge.

            * ``4`` - Use 4 facets per edge.

        Notes
        -----

        .. _s-EFACET_notes:

        :ref:`efacet` is valid only when PowerGraphics is enabled ( :ref:`graphics`,POWER), except that it
        can be used in FULL graphics mode for element ``CONTA174``. (See the :ref:`graphics` command and
        element ``CONTA174`` in the `Element Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_BIBLIO.html>`_ for more
        information.) The :ref:`efacet` command is only
        applicable to element type displays.

        :ref:`efacet` controls the fineness of the subgrid that is used for element plots. The element is
        subdivided into smaller portions called facets. Facets are piecewise linear surface approximations
        of the actual element face. In their most general form, facets are warped planes in 3D space. A
        greater number of facets will result in a smoother representation of the element surface for element
        plots. :ref:`efacet` may affect results averaging. See `Contour Displays
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS5_3.html#>`_ in the
        `Basic Analysis Guide
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_bas/Hlp_G_BAS19.html>`_ for more
        information.

        For midside node elements, use ``NUM`` = 2; if ``NUM`` = 1, no midside node information is output.
        For non-midside node elements, ``NUM`` should be set to 1. See the :ref:`plnsol` and :ref:`prnsol`
        commands for more information.

        With PowerGraphics active ( :ref:`graphics`,POWER), the averaging scheme for surface data with
        interior element data included ( :ref:`avres`,,FULL) and multiple facets per edge ( :ref:`efacet`
        ,2 or :ref:`efacet`,4) will yield differing minimum and maximum contour values depending on the
        Z-Buffering options ( :ref:`slashtype`,,6 or :ref:`slashtype`,,7). When the Section data is not
        included in the averaging schemes ( :ref:`slashtype`,,7), the resulting absolute value for the
        midside node is significantly smaller.

        For cyclic symmetry mode-superposition harmonic solutions, only ``NUM`` = 1 is supported in
        postprocessing.

        .. warning::

            If you specify /EFACET,1, PowerGraphics does not plot midside nodes. You must use /EFACET,2 to
            make the nodes visible.

        This command is valid in any processor.
        """
        command = f"/EFACET,{num}"
        return self.run(command, **kwargs)

    def ernorm(self, key: str = "", **kwargs):
        r"""Controls error estimation calculations.

        Mechanical APDL Command: `ERNORM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_ERNORM.html>`_

        **Command default:**

        .. _ERNORM_default:

        Error estimation calculations are performed by default unless PowerGraphics is enabled (
        :ref:`graphics`,POWER).

        Parameters
        ----------
        key : str
            Control key:

            * ``ON`` - Perform error estimation (default). This option is not valid for PowerGraphics.

            * ``OFF`` - Do not perform error estimation.

        Notes
        -----

        .. _ERNORM_notes:

        Especially for thermal analyses, program speed increases if error estimation is suppressed.
        Therefore, it might be desirable to use error estimation only when needed. The value of the
        :ref:`ernorm` key is not saved on :file:`file.db`. Consequently, you need to reissue the
        :ref:`ernorm` key after a :ref:`resume` if you wish to deactivate error estimation again.
        """
        command = f"ERNORM,{key}"
        return self.run(command, **kwargs)

    def force(self, lab: str = "", **kwargs):
        r"""Selects the element nodal force type for output.

        Mechanical APDL Command: `FORCE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FORCE.html>`_

        Parameters
        ----------
        lab : str
            Type of force to be associated with the force items:

            * ``TOTAL`` - Total forces (static, damping, and inertia).

            * ``STATIC`` - Static forces.

            * ``DAMP`` - Damping forces.

            * ``INERT`` - Inertia forces.

        Notes
        -----

        .. _FORCE_notes:

        :ref:`force` selects the element nodal force type for output with the POST1 :ref:`presol`,
        :ref:`plesol`, :ref:`prrfor`, :ref:`nforce`, :ref:`fsum`, etc. commands, the POST26 :ref:`esol`
        command, and reaction force plotting ( :ref:`pbc` ). For example, :ref:`force`,STATIC causes item F
        of the :ref:`presol` command to be the static forces for the elements processed. Element member
        forces (such as those available for beams and shells and processed by Item and Sequence number) are
        not affected by this command. The SMISC records extract the static force.

        In a non-spectrum analysis that includes either contact or pretension elements in the model, the
        :ref:`prrsol` command is valid with the :ref:`force` command. Otherwise, the :ref:`prrsol` command
        is not valid with :ref:`force`. Use the :ref:`prrfor` command, which provides the same functionality
        as :ref:`prrsol`, instead.

        Use the :ref:`force` command prior to any load case operations ( :ref:`lcoper` ) to insure the
        correct element nodal force combinations.

        In POST26, the :ref:`esol` data stored is based on the active :ref:`force` specification at the time
        the data is stored. To store data at various specifications (for example, static and inertia
        forces), issue a :ref:`store` command before each new specification.

        The :ref:`force` command cannot be used to extract static, damping, and inertial forces for
        ``MPC184`` joint elements.

        To retrieve the different force types, use the :ref:`get` command with ``Entity`` =ELEM and
        ``Item1`` =EFOR.

        The :ref:`force` command is not supported in a spectrum analysis. You can specify the force type
        directly on the combination method commands ( ``ForceType`` on the :ref:`psdcom`, :ref:`srss`,
        :ref:`cqc`, etc. commands).

        The :ref:`force` command is not supported in a modal analysis.
        """
        command = f"FORCE,{lab}"
        return self.run(command, **kwargs)

    def inres(
        self,
        item1: str = "",
        item2: str = "",
        item3: str = "",
        item4: str = "",
        item5: str = "",
        item6: str = "",
        item7: str = "",
        item8: str = "",
        **kwargs,
    ):
        r"""Identifies the data to be retrieved from the results file.

        Mechanical APDL Command: `INRES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_INRES.html>`_

        Parameters
        ----------
        item1 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item2 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item3 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item4 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item5 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item6 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item7 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        item8 : str
            Data to be read into the database from the results file. May consist of any of the following labels:

            * ``ALL`` - All solution items (default).

            * ``BASIC`` - NSOL, RSOL, NLOAD, STRS, FGRAD, and FFLUX items.

            * ``NSOL`` - Nodal DOF solution.

            * ``RSOL`` - Nodal reaction loads.

            * ``ESOL`` - Element solution items (includes all of the following):

              * ``NLOAD`` - Element nodal loads.

              * ``STRS`` - Element nodal stresses.

              * ``EPEL`` - Element elastic strains.

              * ``EPTH`` - Element thermal, initial, and swelling strains.

              * ``EPPL`` - Element plastic strains.

              * ``EPCR`` - Element creep strains.

              * ``FGRAD`` - Element nodal gradients.

              * ``FFLUX`` - Element nodal fluxes.

              * ``MISC`` - Element miscellaneous data (SMISC and NMISC).

            * ``NAR`` - `Nodal-averaged result
              <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
              items (includes all of the following):

              * ``NDST`` - Nodal-averaged stresses.

              * ``NDEL`` - Nodal-averaged elastic strains.

              * ``NDPL`` - Nodal-averaged plastic strains.

              * ``NDCR`` - Nodal-averaged creep strains.

              * ``NDTH`` - Nodal-averaged thermal and swelling strains.

        Notes
        -----

        .. _INRES_notes:

        Identifies the type of data to be retrieved from the results file for placement into the database
        through commands such as :ref:`set`, :ref:`subset`, and :ref:`append`. :ref:`inres` is a companion
        command to the :ref:`outres` command controlling data written to the database and the results file.
        Since the :ref:`inres` command can only flag data that has already been written to the results file,
        care should be taken when using the :ref:`outres` command to include all data you wish to retrieve
        for postprocessing later on.

        The ``Item`` = ALL option includes all NAR items. For more information, see `Nodal-Averaged Results
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_2.html#nodeavepost>`_
        """
        command = (
            f"INRES,{item1},{item2},{item3},{item4},{item5},{item6},{item7},{item8}"
        )
        return self.run(command, **kwargs)

    def layer(self, num: str = "", **kwargs):
        r"""Specifies the element layer for which data are to be processed.

        Mechanical APDL Command: `LAYER <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LAYER.html>`_

        Parameters
        ----------
        num : str
            Layer-processing mode:

            * ``N`` - The layer number to process. The default value is 0.

            * ``FCMAX`` - Processes the layer with the largest failure criteria.

        Notes
        -----

        .. _LAYER_notes:

        Specifies the element layer for which results data are to be listed, plotted, or otherwise
        processed.

        Applies to stress and strain data for layered elements ``SHELL181``, ``SHELL281``, ``ELBOW290``,
        ``SOLID185``, ``SOLID186``, ``SOLSH190``, ``SHELL208``, ``SHELL209``, ``REINF264``, and ``REINF265``
        ; heat flux and heat gradient for ``SHELL131`` and ``SHELL132``.

        For `reinforcing
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_str/str_compreinfdirectemb.html>`_
        elements, ``N`` is a given reinforcing member (individual reinforcing). Specifying ``N`` = 0
        (default) or ``N`` = 1 selects the first reinforcing member.

        The :ref:`shell` command can then be used (with shell elements) to specify a location (TOP, MID,
        BOT) within the layer for output. (The :ref:`shell` command does not apply to thermal shell elements
        ``SHELL131`` and ``SHELL132``.) Transverse shear stresses for MID are linearly averaged from TOP and
        BOT, and do not reflect a parabolic distribution. Setting KEYOPT(8) = 2 for ``SHELL181``,
        ``SHELL281``, ``SHELL208``, ``SHELL209``, and ``ELBOW290`` writes the mid-surface values directly to
        the results file and yields more accurate values than linear averaging.

        Because energy is a per-element quantity, you cannot use this command for energy output.

        When using the :ref:`layer` command with ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLSH190``,
        ``SHELL208``, ``SHELL209``, ``SHELL281``, and ``ELBOW290``, KEYOPT(8) must be set to 1 (or 2 for
        ``SHELL181``, ``SHELL281``, ``ELBOW290``, ``SHELL208``, and ``SHELL209`` ) in order to store results
        for all layers.

        When ``NUM`` = FCMAX, you must provide the failure criterion input. If specifying input via the
        :ref:`fc` command, all structural elements are processed. For more information, see the
        documentation for the :ref:`fc` command.

        Use this command with :ref:`rsys`,LSYS to display results in the layer coordinate system for a
        particular layer.
        """
        command = f"LAYER,{num}"
        return self.run(command, **kwargs)

    def rsys(self, kcn: int | str = "", **kwargs):
        r"""Activates a coordinate system for printout or display of element and nodal results.

        Mechanical APDL Command: `RSYS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_RSYS.html>`_

        Parameters
        ----------
        kcn : int or str
            The coordinate system to use for results output:

            * ``0`` - Global Cartesian coordinate system (default, except for spectrum analyses).

            * ``1`` - Global cylindrical coordinate system in Z.

            * ``2`` - Global spherical coordinate system.

            * ``5`` - Global cylindrical coordinate system in Y.

            * ``6`` - Global cylindrical coordinate system in X.

            * ``> 10`` - Any existing local coordinate system.

            * ``SOLU`` - Solution coordinate systems.

            * ``LSYS`` - Layer coordinate system (default for spectrum analysis).

        Notes
        -----

        .. _RSYS_notes:

        The :ref:`rsys` command activates a coordinate system for printing or displaying element results
        data such as stresses and heat fluxes, and nodal results data such as degrees of freedom and
        reactions.

        Mechanical APDL rotates the results data to the specified coordinate system during printout,
        display, or
        element table operations (such as :ref:`prnsol`, :ref:`presol`, :ref:`plnsol`, and :ref:`etable` ).

        You can define coordinate systems with various Mechanical APDL commands such as :ref:`local`,
        :ref:`cs`,
        :ref:`clocal`, and :ref:`cskp`.

        The :ref:`rsys` command has no effect on beam or pipe stresses, which Mechanical APDL displays (via
        :ref:`eshape`,1 and PowerGraphics) in the element coordinate system.

        Element results such as stresses and heat fluxes are in the element coordinate systems when ``KCN``
        = SOLU. Nodal requests for element results (for example, :ref:`prnsol`,S,COMP) average the element
        values at the common node; that is, the orientation of the node is not a factor in the output of
        element quantities.

        For nearly all solid elements, the default element coordinate systems are parallel to the global
        Cartesian coordinate system.

        For shell elements and the remaining solid elements, the default element coordinate system can
        differ from element to element.

        For layered shell and layered solid elements, Mechanical APDL initially selects the element
        coordinate
        system when ``KCN`` = SOLU. You can then select the layer coordinate system via the :ref:`layer`
        command.

        Nodal results such as degrees of freedom and reactions can be properly rotated only if the resulting
        component set is consistent with the degree-of-freedom set at the node. The degree-of-freedom set at
        a node is determined by the elements attached to the node.

        Example: If a node does not have a UZ degree of freedom during solution, any Z component resulting
        from a rotation does not print or display in POST1. Results at nodes with a single degree-of-freedom
        (UY only, for example) should therefore not be rotated; that is, they should be viewed only in the
        nodal coordinate system or a system parallel to the nodal system. (The default global Cartesian
        system cannot be parallel to the nodal system.)

        Results at nodes with a 2D degree-of-freedom set (UX and UY, for example) should not be rotated out
        of the 2D plane.

        When ``KCN`` > 10, and the specified system is subsequently redefined, reissue the :ref:`rsys`
        command for results to be rotated into the redefined system.

        For element quantities, solution coordinate systems are the element coordinate system for each
        element. For nodal quantities, they are the nodal coordinate systems.

        If an element or nodal coordinate system is not defined, Mechanical APDL uses the global Cartesian
        coordinate system.

        If you issue a :ref:`layer`, ``N`` command (where ``N`` refers to a layer number), the results
        appear in the layer coordinate system. (SOLU is the default for spectrum analyses.)

        The default coordinate system for certain elements, notably shells, is not global Cartesian and is
        frequently not aligned at adjacent elements. Avoid setting ``KCN`` = SOLU with such elements, as it
        can make nodal averaging of component element results (such as SX, SY, SZ, SXY, SYZ, and SXZ)
        invalid.

        When post-processing expanded nodal results in a cyclic symmetry analysis ( :ref:`cycexpand` ), use
        of :ref:`rsys`,SOLU is recommended so that the appropriate cyclic nodal coordinate system is used
        (see :ref:`cyclic` command). For any other coordinate system (for example, :ref:`rsys`,1), cyclic
        rotation is not carried out, and nodal results at all sectors are expressed in the specified
        coordinate system ( ``KCN`` ). See `Result Coordinate System
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_cycsym/advcycpost.html#advcycrescosys>`_

        For layered shell and solid elements, the results appear in their respective layer coordinate
        systems. For a specific layer of interest, issue a :ref:`layer`, ``N`` command (where ``N`` refers
        to a layer number).

        If a model has both nonlayered and layered elements, you can use :ref:`rsys`,SOLU and :ref:`rsys`
        ,LSYS simultaneously (with :ref:`rsys`,SOLU applicable to nonlayered elements and :ref:`rsys`,LSYS
        applicable to layered elements).

        To reverse effects of the LSYS option, issue an :ref:`rsys`,0 command.

        LSYS is the default for spectrum analysis.

        Mechanical APDL plots :ref:`plvect` vector arrow displays (such temperature, velocity, and force) in
        the
        global Cartesian coordinate system ( :ref:`rsys` = 0). Subsequent operations revert to your original
        coordinate system.

        When using solution coordinate systems for results output ( :ref:`rsys`,SOLU), the deformed or
        displaced shape in a POST1 contour display can be unexpected (although the contours are displayed in
        the expected colors). The program does not rotate displacement values (Ux,Uy,Uz) to global; instead,
        the displacements (stored locally) are added directly to the global coordinates (X,Y,Z). For
        example, if in PREP7 the nodes are rotated 90 degrees about the z axis and the global Uy
        displacements are relatively large, the Ux values will be large, causing the model to display a
        large deformation in the global X direction.

        If large deflection is active ( :ref:`nlgeom`,ON), Mechanical APDL rotates the element component
        result
        directions by the amount of rigid body rotation.

        Mechanical APDL displays the element component results in the initial global coordinate system for
        the
        following elements: ``SHELL181``, ``SHELL281``, ``ELBOW290``, ``PLANE182``, ``PLANE183``,
        ``SOLID185``, ``SOLID186``, ``SOLID187``, ``SOLID272``, ``SOLID273``, ``SOLID285``, ``SOLSH190``,
        ``SHELL208``, and ``SHELL209``.

        All other element result transformations, therefore, are also relative to the initial global system.

        Nodal degree-of-freedom results are based on the initial geometry.

        For all other element types, component results displayed in the co-rotated coordinate system include
        the element rigid body rotation from the initial global coordinate system, and all other element
        result transformations are relative to the rotated global system.
        """
        command = f"RSYS,{kcn}"
        return self.run(command, **kwargs)

    def shell(self, loc: str = "", **kwargs):
        r"""Selects a shell element or shell layer location for results output.

        Mechanical APDL Command: `SHELL <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SHELL.html>`_

        Parameters
        ----------
        loc : str
            Location within shell element (or layer) to obtain stress results:

            * ``TOP`` - Top of shell element (or layer) (default).

            * ``MID`` - Middle of shell element (or layer). The default method averages the TOP and BOT values
              to obtain a mid value. Setting KEYOPT(8) = 2 for ``SHELL181``, ``SHELL208``, ``SHELL209``,
              ``SHELL281``, and ``ELBOW290`` uses MID results obtained directly from the results file.

            * ``BOT`` - Bottom of shell element (or layer).

        Notes
        -----

        .. _SHELL_notes:

        Selects the location within a shell element (or a shell layer) for results output (nodal stresses,
        strains, etc.). Applies to POST1 selects, sorts, and output ( :ref:`nsel`, :ref:`nsort`,
        :ref:`prnsol`, :ref:`plnsol`, :ref:`prpath`, :ref:`plpath`, etc.), and is used for storage with the
        POST26 :ref:`esol` command. For example, :ref:`shell`,TOP causes item S of the POST1 :ref:`prnsol`
        command or the POST26 :ref:`esol` command to be the stresses at the top of the shell elements. For
        layered shell elements, use the :ref:`layer` (POST1) or :ref:`layerp26` (POST26) command to select
        the layer. The :ref:`shell` command does not apply to the layered thermal shell elements,
        ``SHELL131`` and ``SHELL132``.

        For PowerGraphics ( :ref:`graphics`,POWER), the :ref:`shell`,MID command affects both the printed
        output and the displayed results, while the :ref:`shell` (TOP or BOT) command prints and displays
        both the top and bottom layers simultaneously. Note that :ref:`cycexpand`,ON automatically turns on
        PowerGraphics; however, for cyclic mode-superposition harmonic postprocessing ( :ref:`cycfiles` ),
        the :ref:`shell` command prints and displays only the requested layer.

        In POST26, the :ref:`esol` data stored is based on the active :ref:`shell` specification at the time
        the data is stored. To store data at various specifications (for example, stresses at the top and
        bottom locations), issue a :ref:`store` command before each new specification.
        """
        command = f"SHELL,{loc}"
        return self.run(command, **kwargs)
