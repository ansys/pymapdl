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


class MagneticsCalculations:

    def curr2d(self, **kwargs):
        r"""Calculates current flow in a 2D conductor.

        Mechanical APDL Command: `CURR2D <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CURR2D.html>`_

        Notes
        -----

        .. _CURR2D_notes:

        :ref:`curr2d` invokes a macro which calculates the total current flowing in a conducting body for a
        2D planar or axisymmetric magnetic field analysis. The currents may be applied source currents or
        induced currents (eddy currents). The elements of the conducting region must be selected before this
        command is issued. The total current calculated by the macro is stored in the parameter TCURR. Also,
        the total current and total current density are stored on a per-element basis in the element table (
        :ref:`etable` ) with the labels TCURR and JT, respectively. Use the :ref:`pletab` and :ref:`pretab`
        commands to plot and list the element table items.
        """
        command = "CURR2D"
        return self.run(command, **kwargs)

    def emagerr(self, **kwargs):
        r"""Calculates the relative error in an electrostatic or electromagnetic field analysis.

        Mechanical APDL Command: `EMAGERR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMAGERR.html>`_

        Notes
        -----

        .. _EMAGERR_notes:

        The relative error is an approximation of the mesh discretization error associated with a solution.
        It is based on the discrepancy between the unaveraged, element-nodal field values and the averaged,
        nodal field values. The calculation is valid within a material boundary and does not consider the
        error in continuity of fields across dissimilar materials.

        For electrostatics, the field values evaluated are the electric field strength (EFSUM) and the
        electric flux density (DSUM). A relative error norm of each is calculated on a per-element basis and
        stored in the element table ( :ref:`etable` ) with the labels EF_ERR and D_ERR. Normalized error
        values EFN_ERR and DN_ERR are also calculated and stored in the element table. Corresponding
        quantities for electromagnetics are H_ERR, B_ERR, HN_ERR, and BN_ERR, which are calculated from the
        magnetic field intensity (HSUM) and the magnetic flux density (BSUM). The normalized error value is
        the relative error norm value divided by the peak element-nodal field value for the currently
        selected elements.

        Use the :ref:`pletab` and :ref:`pretab` commands to plot and list the error norms and normalized
        error values.
        """
        command = "EMAGERR"
        return self.run(command, **kwargs)

    def emf(self, **kwargs):
        r"""Calculates the electromotive force (emf), or voltage drop along a predefined path.

        Mechanical APDL Command: `EMF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMF.html>`_

        Notes
        -----

        .. _EMF_notes:

        :ref:`emf` invokes a Mechanical APDL macro which calculates the electromotive force (emf), or
        voltage drop
        along a predefined path (specified with the :ref:`path` command). It is valid for both 2D and 3D
        electric field analysis. The calculated emf value is stored in the parameter EMF.

        You must define a line path (via the :ref:`path` command) before issuing the :ref:`emf` command
        macro. The macro uses calculated values of the electric field (EF), and uses path operations for the
        calculations. All path items are cleared when the macro finishes executing.

        The :ref:`emf` macro sets the "ACCURATE" mapping method and "MAT" discontinuity option on the
        :ref:`pmap` command. The program retains these settings after executing the macro.
        """
        command = "EMF"
        return self.run(command, **kwargs)

    def emft(self, **kwargs):
        r"""Summarizes electromagnetic forces and torques.

        Mechanical APDL Command: `EMFT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EMFT.html>`_

        Notes
        -----
        Use this command to summarize electromagnetic force and torque in both static electric and magnetic
        problems. To use this command, select the nodes in the region of interest and make sure that all
        elements are selected. If :ref:`rsys` = 0, the force is reported in the global Cartesian coordinate
        system. If :ref:`rsys` ≠ 0, force is reported in the specified coordinate system. However, for
        torque, if :ref:`rsys` ≠ 0, this command will account for the shift and rotation as specified by
        :ref:`rsys`, but will report only the Cartesian components.

        Forces are stored as items _FXSUM, _FYSUM, _FZSUM, and _FSSUM. Torque is stored as items _TXSUM,
        _TYSUM, _TZSUM, and _TSSUM.

        This command is valid only with ``PLANE121``, ``SOLID122``, ``SOLID123``, ``PLANE222``,
        ``PLANE223``, ``SOLID225``, ``SOLID226``, ``SOLID227``, ``PLANE233``, ``SOLID236`` and ``SOLID237``
        elements.
        """
        command = "EMFT"
        return self.run(command, **kwargs)

    def fluxv(self, **kwargs):
        r"""Calculates the flux passing through a closed contour.

        Mechanical APDL Command: `FLUXV <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FLUXV.html>`_

        Notes
        -----

        .. _FLUXV_notes:

        :ref:`fluxv` invokes a Mechanical APDL macro which calculates the flux passing through a closed
        contour
        (path) predefined by :ref:`path`.

        The calculated flux is stored in the parameter FLUX.

        In a 2D analysis, at least two nodes must be defined on the path. In 3D, a path of nodes describing
        a closed contour must be specified (that is, the first and last node in the path specification must
        be the same).

        A counterclockwise ordering of nodes on the :ref:`ppath` command gives the correct sign on flux.

        Path operations are used for the calculations, and all path items are cleared upon completion.

        This macro is available for vector potential formulations only.
        """
        command = "FLUXV"
        return self.run(command, **kwargs)

    def mmf(self, **kwargs):
        r"""Calculates the magnetomotive force along a path.

        Mechanical APDL Command: `MMF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_MMF.html>`_

        Notes
        -----

        .. _MMF_notes:

        :ref:`mmf` invokes a Mechanical APDL macro which calculates the magnetomotive force (mmf) along a
        predefined path ( :ref:`path` ). It is valid for both 2D and 3D magnetic field analyses. The
        calculated mmf value is stored in the parameter MMF.

        A closed path ( :ref:`path` ), passing through the magnetic circuit for which mmf is to be
        calculated, must be defined before this command is issued. A counterclockwise ordering of points on
        the :ref:`ppath` command will yield the correct sign on the mmf. The mmf is based on Ampere's Law.
        The macro makes use of calculated values of field intensity (H), and uses path operations for the
        calculations. All path items are cleared upon completion. The :ref:`mmf` macro sets the "ACCURATE"
        mapping method and "MAT" discontinuity option of the :ref:`pmap` command.
        """
        command = "MMF"
        return self.run(command, **kwargs)

    def plf2d(
        self,
        ncont: str = "",
        olay: int | str = "",
        anum: str = "",
        win: str = "",
        **kwargs,
    ):
        r"""Generates a contour line plot of equipotentials.

        Mechanical APDL Command: `PLF2D <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLF2D.html>`_

        Parameters
        ----------
        ncont : str
            Number of contour lines to display. Issue in multiples of 9 (that is, 9, 18, 27, etc.). Default
            is 27 contour lines.

        olay : int or str
            Overlay:

            * ``0`` - Overlay edge outlines by material number.

            * ``1`` - Overlay edge outlines by real constant number.

        anum : str
            Highest material or real constant attribute number. Command will cycle through ``ANUM`` element
            display overlays. Defaults to 10.

        win : str
            Window number to which command applies. Defaults to 1.

        Notes
        -----

        .. _PLF2D_notes:

        :ref:`plf2d` invokes a Mechanical APDL macro which plots equipotentials of the degree of freedom AZ.
        The
        equipotential lines are parallel to flux lines and thus give a good representation of flux patterns.

        In the axisymmetric case, the display is actually r * AZ where r is the node radius.

        The macro overlays ( ``OLAY`` ) edge outlines by material number or real constant number ( ``ANUM``
        ) and enables you to control the number of contour lines to display ( ``NCONT`` ).
        """
        command = f"PLF2D,{ncont},{olay},{anum},{win}"
        return self.run(command, **kwargs)

    def powerh(self, **kwargs):
        r"""Calculates the rms power loss in a conductor or lossy dielectric.

        Mechanical APDL Command: `POWERH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_POWERH.html>`_

        Notes
        -----

        .. _POWERH_notes:

        :ref:`powerh` invokes a Mechanical APDL macro which calculates the time-averaged (rms) power loss in
        a
        conductor or lossy dielectric material from a harmonic analysis. The power loss is stored in the
        parameter PAVG.

        Conductor losses include solid conductors and surface conductors approximated by impedance or
        shielding boundary conditions. The power-loss  density for solid conductors or dielectrics is
        stored in the element table with the label PLOSSD and may be listed ( :ref:`pretab` ) or displayed (
        :ref:`pletab` ). PLOSSD does not include surface losses.

        The elements of the conducting region must be selected before this command is issued.

        :ref:`powerh` is valid for 2D and 3D analyses.
        """
        command = "POWERH"
        return self.run(command, **kwargs)

    def senergy(self, opt: int | str = "", antype: int | str = "", **kwargs):
        r"""Determines the stored magnetic energy or co-energy.

        Mechanical APDL Command: `SENERGY <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SENERGY.html>`_

        Parameters
        ----------
        opt : int or str
            Item to be calculated:

            * ``0`` - Stored magnetic energy.

            * ``1`` - Stored magnetic co-energy.

        antype : int or str
            Analysis type:

            * ``0`` - Static or transient.

            * ``1`` - Harmonic.

        Notes
        -----

        .. _SENERGY_notes:

        :ref:`senergy` invokes a Mechanical APDL macro which calculates the stored magnetic energy or co-
        energy for
        all selected elements. (For a harmonic analysis, the macro calculates a time-averaged (rms) stored
        energy.)

        A summary table listing the energy by material number is generated. The energy density is also
        calculated and stored on a per-element basis in the element table ( :ref:`etable` ) with the label
        MG_ENG (energy density) or MG_COENG (co-energy density). The macro erases all other items in the
        element table and retains only the energy density or co-energy density.

        Issue :ref:`pletab` and :ref:`pretab` to plot and list the energy density.

        The macro is valid for static and low-frequency magnetic field formulations.

        The macro will not calculate stored energy and co-energy for the following cases:

        * Orthotropic nonlinear permanent magnets.

        * Orthotropic nonlinear permeable materials.

        * Temperature dependent materials.

        :ref:`senergy` is restricted to MKSA units.
        """
        command = f"SENERGY,{opt},{antype}"
        return self.run(command, **kwargs)
