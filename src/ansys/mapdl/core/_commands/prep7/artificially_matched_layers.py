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


class ArtificiallyMatchedLayers(CommandsBase):

    def pmlopt(
        self,
        psys: str = "",
        lab: str = "",
        xminus: str = "",
        xplus: str = "",
        yminus: str = "",
        yplus: str = "",
        zminus: str = "",
        zplus: str = "",
        woptxm: str = "",
        woptxp: str = "",
        woptym: str = "",
        woptyp: str = "",
        woptzm: str = "",
        woptzp: str = "",
        **kwargs,
    ):
        r"""Defines perfectly matched layers (PMLs) or irregular perfectly matched layers (IPML).

        Mechanical APDL Command: `PMLOPT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PMLOPT.html>`_

        Parameters
        ----------
        psys : str
            PML element coordinate system number. ``PSYS`` may be 0 (global Cartesian) or any previously
            defined local Cartesian coordinate system number (>10). Defaults to 0. (Not used for IPML.)

        lab : str
            Label defining the number of dimensions (not used for IPML) :

            * ``ONE`` - A one-dimensional PML region.

            * ``THREE`` - A three-dimensional PML region (default).

        xminus : str
            For PML, normal reflection coefficient (harmonic analysis) or attenuation factor (static
            structural analysis) in negative X direction of ``PSYS``. Defaults to 1.E-3 (equivalent to -60
            dB) for ``WOptXm`` = PROP or HYBR, 30 for ``WOptXm`` = EVAN, and 40 for ``WOptXm`` = MAXP.

        xplus : str
            Normal reflection coefficient (harmonic analysis) or attenuation factor (static structural
            analysis) in positive X direction of ``PSYS``. Defaults to 1.E-3 (equivalent to -60 dB) for
            ``WOptXp`` = PROP or HYBR, 30 for ``WOptXp`` = EVAN, and 40 for ``WOptXp`` = MAXP. (Not used for
            IPML.)

        yminus : str
            Normal reflection coefficient (harmonic analysis) or attenuation factor (static structural
            analysis) in negative Y direction of ``PSYS``. Defaults to 1.E-3 (equivalent to -60 dB) for
            ``WOptYm`` = PROP or HYBR, 30 for ``WOptYm`` = EVAN, and 40 for ``WOptYm`` = MAXP. (Not used for
            IPML.)

        yplus : str
            Normal reflection coefficient (harmonic analysis) or attenuation factor (static structural
            analysis) in positive Y direction of ``PSYS``. Defaults to 1.E-3 (equivalent to -60 dB) for
            ``WOptYp`` = PROP or HYBR, 30 for ``WOptYp`` = EVAN, and 40 for ``WOptYp`` = MAXP. (Not used for
            IPML.)

        zminus : str
            Normal reflection coefficient (harmonic analysis) or attenuation factor (static structural
            analysis) in negative Z direction of ``PSYS``. Defaults to 1.E-3 (equivalent to -60 dB) for
            ``WOptZm`` = PROP or HYBR, 30 for ``WOptZm`` = EVAN, and 40 for ``WOptZm`` = MAXP. (Not used for
            IPML.)

        zplus : str
            Normal reflection coefficient (harmonic analysis) or attenuation factor (static structural
            analysis) in positive Z direction of ``PSYS``. Defaults to 1.E-3 (equivalent to -60 dB) for
            ``WOptZp`` = PROP or HYBR, 30 for ``WOptZp`` = EVAN, and 40 for ``WOptZp`` = MAXP. (Not used for
            IPML.)

        woptxm : str
            Type of attenuated wave in the PML region in each direction:

            * ``PROP`` - Only the propagating wave is attenuated. The PML parameter is set to s = 1-jβ in
              harmonic analyses and acoustic transient analyses.

            * ``EVAN`` - Only the evanescent field is attenuated. The PML parameter is set to s = α ( α > 1) in
              static analyses.

            * ``HYBR`` - Both the propagating wave and the evanescent wave are attenuated (default). The PML
              parameter is set to s = α -jβ ( α > 1). The program sets the coefficient α values in terms of the
              normal reflection coefficients in harmonic analyses.

            * ``MAXP`` - The maximum attenuation coefficient for frequency-independent PML parameter in harmonic
              analyses, acoustic modal analyses, and acoustic transient analyses.

        woptxp : str
            Type of attenuated wave in the PML region in each direction:

            * ``PROP`` - Only the propagating wave is attenuated. The PML parameter is set to s = 1-jβ in
              harmonic analyses and acoustic transient analyses.

            * ``EVAN`` - Only the evanescent field is attenuated. The PML parameter is set to s = α ( α > 1) in
              static analyses.

            * ``HYBR`` - Both the propagating wave and the evanescent wave are attenuated (default). The PML
              parameter is set to s = α -jβ ( α > 1). The program sets the coefficient α values in terms of the
              normal reflection coefficients in harmonic analyses.

            * ``MAXP`` - The maximum attenuation coefficient for frequency-independent PML parameter in harmonic
              analyses, acoustic modal analyses, and acoustic transient analyses.

        woptym : str
            Type of attenuated wave in the PML region in each direction:

            * ``PROP`` - Only the propagating wave is attenuated. The PML parameter is set to s = 1-jβ in
              harmonic analyses and acoustic transient analyses.

            * ``EVAN`` - Only the evanescent field is attenuated. The PML parameter is set to s = α ( α > 1) in
              static analyses.

            * ``HYBR`` - Both the propagating wave and the evanescent wave are attenuated (default). The PML
              parameter is set to s = α -jβ ( α > 1). The program sets the coefficient α values in terms of the
              normal reflection coefficients in harmonic analyses.

            * ``MAXP`` - The maximum attenuation coefficient for frequency-independent PML parameter in harmonic
              analyses, acoustic modal analyses, and acoustic transient analyses.

        woptyp : str
            Type of attenuated wave in the PML region in each direction:

            * ``PROP`` - Only the propagating wave is attenuated. The PML parameter is set to s = 1-jβ in
              harmonic analyses and acoustic transient analyses.

            * ``EVAN`` - Only the evanescent field is attenuated. The PML parameter is set to s = α ( α > 1) in
              static analyses.

            * ``HYBR`` - Both the propagating wave and the evanescent wave are attenuated (default). The PML
              parameter is set to s = α -jβ ( α > 1). The program sets the coefficient α values in terms of the
              normal reflection coefficients in harmonic analyses.

            * ``MAXP`` - The maximum attenuation coefficient for frequency-independent PML parameter in harmonic
              analyses, acoustic modal analyses, and acoustic transient analyses.

        woptzm : str
            Type of attenuated wave in the PML region in each direction:

            * ``PROP`` - Only the propagating wave is attenuated. The PML parameter is set to s = 1-jβ in
              harmonic analyses and acoustic transient analyses.

            * ``EVAN`` - Only the evanescent field is attenuated. The PML parameter is set to s = α ( α > 1) in
              static analyses.

            * ``HYBR`` - Both the propagating wave and the evanescent wave are attenuated (default). The PML
              parameter is set to s = α -jβ ( α > 1). The program sets the coefficient α values in terms of the
              normal reflection coefficients in harmonic analyses.

            * ``MAXP`` - The maximum attenuation coefficient for frequency-independent PML parameter in harmonic
              analyses, acoustic modal analyses, and acoustic transient analyses.

        woptzp : str
            Type of attenuated wave in the PML region in each direction:

            * ``PROP`` - Only the propagating wave is attenuated. The PML parameter is set to s = 1-jβ in
              harmonic analyses and acoustic transient analyses.

            * ``EVAN`` - Only the evanescent field is attenuated. The PML parameter is set to s = α ( α > 1) in
              static analyses.

            * ``HYBR`` - Both the propagating wave and the evanescent wave are attenuated (default). The PML
              parameter is set to s = α -jβ ( α > 1). The program sets the coefficient α values in terms of the
              normal reflection coefficients in harmonic analyses.

            * ``MAXP`` - The maximum attenuation coefficient for frequency-independent PML parameter in harmonic
              analyses, acoustic modal analyses, and acoustic transient analyses.

        Notes
        -----

        .. _PMLOPT_notes:

        The :ref:`pmlopt` command can be used to define perfectly matched layers (PML). The following
        element types support perfectly matched layers:

        * Acoustic elements: ``FLUID30``, ``FLUID220``, and ``FLUID221`` (KEYOPT(4) > 0) in a modal,
          harmonic, or transient acoustic analysis.

        * Piezoelectric coupled-field elements: ``PLANE222``, ``PLANE223``, ``SOLID225``, ``SOLID226``, and
          ``SOLID227`` (KEYOPT(15) = 1) in a harmonic piezoelectric analysis. For the lower order elements (
          ``PLANE222`` and ``SOLID225`` ), PML is only supported with the B-bar method.

        * Structural elements: ``PLANE182``, ``PLANE183``, ``SOLID185``, ``SOLID186``, and ``SOLID187``
          (KEYOPT(15) = 1) in a linear static or harmonic structural analysis. For the lower order elements
          ( ``PLANE182`` and ``SOLID185`` ), PML is only supported with the B-bar method.

        Each PML region must have a uniquely defined PML element coordinate system ( :ref:`psys` ). Normal
        reflection coefficient values for a harmonic analysis must be less than 1.

        The :ref:`pmlopt` command can also be used to define irregular perfectly matched layers (IPML) for
        acoustic analyses. Normal reflection coefficient values for a harmonic analysis must be less than 1.

        Issue :ref:`pmlopt`,STAT to list the current normal reflection coefficient or attenuation factor
        settings for a PML or IPML region. Issue :ref:`pmlopt`,CLEAR to clear all normal reflection
        coefficient settings and restore them to the defaults.

        Issue :ref:`pmlopt`,PSYS,CLEAR to clear all normal reflection coefficient settings for the specified
        PML element coordinate system and restore them to the defaults.

        For modal analysis, use one buffer element between the PML and the resonant structure to avoid the
        spurious modes. The mode patterns should be evaluated graphically.

        See `Artificially Matched Layers
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_artificial.html#acous_aml>`_
        """
        command = f"PMLOPT,{psys},{lab},{xminus},{xplus},{yminus},{yplus},{zminus},{zplus},{woptxm},{woptxp},{woptym},{woptyp},{woptzm},{woptzp}"
        return self.run(command, **kwargs)

    def pmlsize(
        self,
        freqb: str = "",
        freqe: str = "",
        dmin: str = "",
        dmax: str = "",
        thick: str = "",
        angle: str = "",
        wavespeed: str = "",
        **kwargs,
    ):
        r"""Determines number of PML or IPML layers.

        Mechanical APDL Command: `PMLSIZE <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PMLSIZE.html>`_

        Parameters
        ----------
        freqb : str
            Minimum operating frequency (no default).

        freqe : str
            Maximum operating frequency (defaults to ``FREQB`` ).

        dmin : str
            Minimum distance from the radiation source to the PML or IPML interface (no default).

        dmax : str
            Maximum distance from the radiation source to the PML or IPML interface (defaults to ``DMIN`` ).

        thick : str
            Thickness of the PML or IPML region (defaults to 0).

        angle : str
            Incident angle of wave to the PML or IPML interface (defaults to 0).

        wavespeed : str
            Wave speed in PML or IPML medium (defaults to 343.24 m/s).

        Notes
        -----
        :ref:`pmlsize` determines the number of PML or IPML layers for acceptable numerical accuracy.

        :ref:`pmlsize` must be issued before any meshing commands. If the thickness of the PML or IPML
        region is known, it determines an element edge length (h) and issues :ref:`esize`,h. If the
        thickness of the PML or IPML region is unknown, it determines the number of layers (n) and issues
        :ref:`esize`,,n.

        See `Artificially Matched Layers
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_acous/acous_artificial.html#acous_aml>`_
        """
        command = f"PMLSIZE,{freqb},{freqe},{dmin},{dmax},{thick},{angle},{wavespeed}"
        return self.run(command, **kwargs)

    def psys(self, kcn: int | str = "", **kwargs):
        r"""Sets the PML element coordinate system attribute pointer.

        Mechanical APDL Command: `PSYS <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PSYS.html>`_

        **Command default:**

        .. _PSYS_default:

        The PML element coordinate system orientation defaults to the global Cartesian system.

        Parameters
        ----------
        kcn : int or str
            Coordinate system number:

            * ``0`` - Use the global Cartesian coordinate system as the PML element coordinate system (default).

            * ``N`` - Set the PML element coordinate system orientation based on a local Cartesian coordinate
              system N (where N must be greater than 10) defined by the :ref:`local` or :ref:`cs` command (for
              example: :ref:`local`,11,0).

        Notes
        -----

        .. _PSYS_notes:

        This command identifies the local coordinate system used to define the PML (perfectly matched
        layers) coordinate system of subsequently defined PML elements. It is only applicable to volume
        elements that support PML. The use of PML coordinate systems is similar to element coordinate
        systems, as discussed in `Understanding the Element Coordinate System
        <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en/ans_elem/Hlp_E_CH2_3.html#elemESYSchange>`_
        ``KCN`` ) defined using the :ref:`local` (or similar) command.
        """
        command = f"PSYS,{kcn}"
        return self.run(command, **kwargs)
