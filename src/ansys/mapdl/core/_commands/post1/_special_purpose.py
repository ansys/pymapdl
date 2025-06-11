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


class SpecialPurpose:

    def kcalc(
        self,
        kplan: int | str = "",
        mat: str = "",
        kcsym: int | str = "",
        klocpr: int | str = "",
        **kwargs,
    ):
        r"""Calculates stress intensity factors in fracture mechanics analyses.

        Mechanical APDL Command: `KCALC <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KCALC.html>`_

        Parameters
        ----------
        kplan : int or str
            Key to indicate stress state for calculation of stress intensity factors:

            * ``0`` - Plane strain and axisymmetric condition (default).

            * ``1`` - Plane stress condition.

        mat : str
            Material number used in the extrapolation (defaults to 1).

        kcsym : int or str
            Symmetry key:

            * ``0 or 1`` - Half-crack model with symmetry boundary conditions ( :ref:`dsym` ]) in the crack-tip
              coordinate system. K II = K III = 0. Three nodes are required on the path.

            * ``2`` - Like 1 except with antisymmetric boundary conditions (K I = 0).

            * ``3`` - Full-crack model (both faces). Five nodes are required on the path (one at the tip and two
              on each face).

        klocpr : int or str
            Local displacements print key:

            * ``0`` - Do not print local crack-tip displacements.

            * ``1`` - Print local displacements used in the extrapolation technique.

        Notes
        -----

        .. _KCALC_notes:

        Calculates the stress intensity factors (K I, K II, and K III ) associated with homogeneous
        isotropic linear elastic fracture mechanics.

        A displacement extrapolation method is used in the calculation. (See `POST1 - Crack Analysis (KCALC)
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_arch/bob143.html#eq57266024-e263-4fd8-b9d4-5ff7d2c2411a>`_
        ``KPLAN`` = 1.

        The program uses minor Poisson's ratio ( :ref:`mp`,NUXY) for the stress intensity factor
        calculation.

        Issue the :ref:`path` and :ref:`ppath` commands to define a path with the crack face nodes (
        ``NODE1`` at the crack tip, ``NODE2`` and ``NODE3`` on one face, ``NODE4`` and ``NODE5`` on the
        other (optional) face).

        A crack-tip coordinate system, having x parallel to the crack face (and perpendicular to the crack
        front) and y perpendicular to the crack face, must be the active :ref:`rsys` and :ref:`csys` before
        :ref:`kcalc` is issued.

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"KCALC,{kplan},{mat},{kcsym},{klocpr}"
        return self.run(command, **kwargs)

    def plcrack(self, loc: int | str = "", num: int | str = "", **kwargs):
        r"""Displays cracking and crushing locations in `SOLID65
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_arch/Hlp_E_SOLID65.html#a5pNxq3a5mcm>`_
        elements.

        Mechanical APDL Command: `PLCRACK <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCRACK.html>`_

        Parameters
        ----------
        loc : int or str
            Location at which symbols are to be displayed:

            * ``0`` - Plot symbols at integration points (default).

            * ``1`` - Plot symbol at element centroids (averaged).

        num : int or str
            Crack to be displayed:

            * ``0`` - Plot all cracks (default).

            * ``1`` - Plot only the first crack.

            * ``2`` - Plot only the second crack.

            * ``3`` - Plot only the third crack.

        Notes
        -----

        .. _PLCRACK_notes:

        :ref:`plcrack` displays circles at locations of cracking or crushing in concrete elements. Cracking
        is shown with a circle outline in the plane of the crack, and crushing is shown with an octahedron
        outline. If the crack has opened and then closed, the circle outline will have an X through it. Each
        integration point can crack in up to three different planes. The first crack at an integration point
        is shown with a red circle outline, the second crack with a green outline, and the third crack with
        a blue outline.

        Symbols shown at the element centroid ( ``LOC`` = 1) are based on the status of all of the element's
        integration points. If any integration point in the element has crushed, the crushed (octahedron)
        symbol is shown at the centroid. If any integration point has cracked or cracked and closed, the
        cracked symbol is shown at the element centroid. If at least five integration points have cracked
        and closed, the cracked and closed symbol is shown at the element centroid. Finally, if more than
        one integration point has cracked, the circle outline at the element centroid shows the average
        orientation of all cracked planes for that element.

        Portions of this command are not supported by PowerGraphics ( :ref:`graphics`,POWER).

        .. warning::

            This command is archived in the latest version of the software.

        """
        command = f"PLCRACK,{loc},{num}"
        return self.run(command, **kwargs)
