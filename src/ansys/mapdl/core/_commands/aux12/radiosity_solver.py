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


class RadiositySolver(CommandsBase):

    def vfco(self, action: str = "", encl: str = "", level: int | str = "", **kwargs):
        r"""Controls the use and level of view factor condensation for symmetric radiation.

        Mechanical APDL Command: `VFCO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFCO.html>`_

        Parameters
        ----------
        action : str
            Action to be performed:

            * ``DEFINE`` - Defines the level of view factor condensation (default).

            * ``CLEAR`` - Resets the level of view factor condensation to 0 for all enclosures. All subsequent
              arguments are ignored.

            * ``STATUS`` - Outputs the ``LEVEL`` of view factor condensation for each enclosure in the model.

        encl : str
            Previously defined enclosure number for the view factor adjustment.

        level : int or str
            Key that controls the level of condensation used in calculating the view factor matrix for models
            with symmetry. Efficiency gains increase with increasing values of ``LEVEL``.

            * ``0`` - View factor condensation is turned off (default). The view factor matrix is calculated for
              all facets, as described in.

            * ``1`` - View factor condensation is turned on. With condensation on, view factors for dependent
              facets are not calculated, which reduces solution time for models with symmetry. The view factor
              matrix is calculated only for independent facets as described in. This option achieves better
              efficiency than ``LEVEL`` = 0. Element NMISC data is written to the results file for both
              independent and dependent facets. :ref:`get`,,RAD,,NETHF, which also uses element fluxes, is based
              on independent and dependent facets.

            * ``2`` - This option achieves even more efficiency gains than ``LEVEL`` = 1, but it requires more
              memory and loses some information. Note that when ``LEVEL`` = 2 is used, dependent facets are
              unselected, and no element NMISC data is written to the results file for dependent facets. The same
              is true for :ref:`get`,,RAD,,NETHF, which also uses element fluxes and is based on independent
              facets only.

        Notes
        -----

        .. _VFCO_notes:

        If view factor condensation is turned on ( :ref:`vfco`, ``ENCL``,1 or :ref:`vfco`, ``ENCL``,2):

        * The dependent facets do not participate in the solution, and only the independent view factors are
          calculated as described in.

        * The problem is reduced to solving only for the independent radiosity flux as described in
          `Radiosity Equations Simplified for Models with Symmetry
          <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat5.html#eqd7803bd4-5251-4d80-bd90-e01d7fdcb8bb>`_

        * The :ref:`vfsm` command operates on the condensed view factor matrix.

        :ref:`vfco` must be issued before the view factors are computed by issuing either :ref:`vfopt`,NEW
        or :ref:`solve`.

        **Example Usage**
        `Example of a 3D Open Enclosure with Symmetry: Radiation Analysis with Condensed View Factor
        Calculation
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_the/the_example_rad_condensedVF.html#>`_
        """
        command = f"VFCO,{action},{encl},{level}"
        return self.run(command, **kwargs)

    def vfquery(self, srcelem: str = "", tarelem: str = "", **kwargs):
        r"""Queries and prints element Hemicube view factors and average view factor.

        Mechanical APDL Command: `VFQUERY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFQUERY.html>`_

        Parameters
        ----------
        srcelem : str
            Elements representing the source radiating surfaces used to query the view factor at the target
            element(s). If ``SRCELEM`` = P, graphical picking is enabled (valid only in the GUI). If
            ``SRCELEM`` = ALL, all selected elements will have their view factors queried. A component name
            may also be substituted for ``SRCELEM``. Selected elements must be flagged for surface to
            surface radiation in order to query view factors ( :ref:`sf`, :ref:`sfa`, or :ref:`sfe` with Lab
            = RDSF). The view factors must have been previously computed.

        tarelem : str
            Element for view factor query. If ``TARELEM`` = P, graphical picking is enabled (valid only in
            the GUI). If ``TARELEM`` = ALL, all selected elements will have their view factors queried. A
            component name may also be substituted for ``TARELEM``. Selected elements must be flagged for
            surface to surface radiation in order to query view factors ( :ref:`sf`, :ref:`sfa`, or
            :ref:`sfe` with Lab = RDSF). The view factors must have been previously computed.

        Notes
        -----

        .. _VFQUERY_notes:

        View factors for each target element will be printed.

        An average view factor for all target elements will be computed. (Use :ref:`get` to retrieve the
        average value).

        When resuming a database, issue the command :ref:`vfopt`,READ before issuing the :ref:`vfquery`
        command.
        """
        command = f"VFQUERY,{srcelem},{tarelem}"
        return self.run(command, **kwargs)

    def vfsm(
        self,
        action: str = "",
        encl: str = "",
        opt: int | str = "",
        maxiter: str = "",
        conv: str = "",
        **kwargs,
    ):
        r"""Adjusts view factor matrix to satisfy reciprocity and/or row sum properties.

        Mechanical APDL Command: `VFSM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_VFSM.html>`_

        Parameters
        ----------
        action : str
            Action to be performed:

            * ``DEFINE`` - Define a view factor summation (default)

            * ``CLEAR`` - Resets the scaling method to 0 for all enclosures. All subsequent arguments are
              ignored.

            * ``STATUS`` - Outputs the ``OPT`` value for each enclosure in the model.

        encl : str
            Previously defined enclosure number for the view factor adjustment.

        opt : int or str
            Option key:

            * ``0`` - The view factor matrix values are not adjusted (default).

            * ``1`` - The view factor matrix values are adjusted so that the row sum equals 1.0.

            * ``2`` - The view factor matrix values are adjusted so that the row sum equals 1.0 and the
              reciprocity relationship is satisfied.

            * ``3`` - The view factor matrix values are adjusted so that the reciprocity relationship is
              satisfied.

            * ``4`` - The view factor matrix values are adjusted so that the original row sum is maintained and
              the reciprocity relationship is satisfied.

        maxiter : str
            Maximum number of iterations to achieve convergence. Valid only when ``OPT`` = 2 or 4. Default
            is 100.

        conv : str
            Convergence value for row sum. Iterations will continue (up to ``MAXITER`` ) until the maximum
            residual over all the rows is less than this value. Valid only when ``OPT`` = 2 or 4. Default is
            1E-3.

        Notes
        -----

        .. _VFSM_notes:

        To have a good energy balance, it is important to satisfy both the row sum and reciprocity
        relationships. For more information, see `View Factors
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat1.html#eq28e43bc0-b07b-459a-87bc-d8cf1cf99906>`_
        in the `Mechanical APDL Theory Reference
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_biblio.html>`_.

        ``OPT`` = 1 and 2 are suitable for perfect enclosures. ``OPT`` = 1 is less expensive than ``OPT`` =
        2 because no iterations are involved. However, with ``OPT`` = 1, the reciprocity relationship is not
        satisfied.

        ``OPT`` = 3 and 4 are suitable for leaky enclosures. ``OPT`` = 3 is less expensive than ``OPT`` = 4
        because no iterations are involved. However, with ``OPT`` = 3, the original row sum is not
        maintained.

        The :ref:`vfsm` command must be used before :ref:`vfopt` is issued, or Solve is initiated.

        While the primary purpose of the :ref:`vfsm` command is to adjust the viewfactor matrix to satisfy
        reciprocity and rowsum properties, a side effect of this command is that the model could flip from
        being an imperfect to a perfect enclosure and the space node ignored if the rowsum becomes 1.0. The
        program's check for an imperfect enclosure is not based geometry, but rather on the value of the
        rowsum of all rows of the enclosure view factor matrix. A rowsum close to 1.0 is deemed a perfect
        enclosure; otherwise, it is an imperfect enclosure, which requires you to define a spacenode. It is
        important to be aware that the :ref:`vfsm` command can affect the `view factor
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_thry/thy_heat1.html#eq28e43bc0-b07b-459a-87bc-d8cf1cf99906>`_
        rowsum and potentially also whether the enclosure is treated as an imperfect or perfect enclosure.
        """
        command = f"VFSM,{action},{encl},{opt},{maxiter},{conv}"
        return self.run(command, **kwargs)
