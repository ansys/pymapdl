"""
Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
SPDX-License-Identifier: MIT

MIT License

Copyright (c) 2024 ANSYS, Inc. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class ArtificiallyMatchedLayers:
    def pmlopt(
        self,
        esys="",
        lab="",
        xminus="",
        xplus="",
        yminus="",
        yplus="",
        zminus="",
        zplus="",
        **kwargs,
    ):
        """Defines perfectly matched layers (PMLs) for acoustic and structural

        APDL Command: PMLOPT
        analyses.

        Parameters
        ----------
        esys
            Element coordinate system number. ESYS may be 0 (global Cartesian)
            or any previously defined local Cartesian coordinate system number
            (>10). Defaults to 0.

        lab
            Label defining the number of dimensions:

            ONE - A one-dimensional PML region.

            THREE - A three-dimensional PML region (default).

        xminus
            For harmonic analysis, normal reflection coefficient in negative X
            direction of ESYS. Defaults to 1.E−3 (equivalent to -60 dB) for a
            harmonic analysis and 30 for a static structural analysis.

        xplus
            For harmonic analysis, normal reflection coefficient in positive X
            direction of ESYS. Defaults to 1.E−3 (equivalent to -60 dB) for a
            harmonic analysis and 30 for a static structural analysis.

        yminus
            For harmonic analysis, normal reflection coefficient in negative Y
            direction of ESYS. Defaults to 1.E−3 (equivalent to -60 dB) for a
            harmonic analysis and 30 for a static structural analysis.

        yplus
            For harmonic analysis, normal reflection coefficient in positive Y
            direction of ESYS. Defaults to 1.E−3 (equivalent to -60 dB) for a
            harmonic analysis and 30 for a static structural analysis.

        zminus
            For harmonic analysis, normal reflection coefficient in negative Z
            direction of ESYS. Defaults to 1.E−3 (equivalent to -60 dB) for a
            harmonic analysis and 30 for a static structural analysis.

        zplus
            For harmonic analysis, normal reflection coefficient in positive Z
            direction of ESYS. Defaults to 1.E−3 (equivalent to -60 dB) for a
            harmonic analysis and 30 for a static structural analysis.

        Notes
        -----
        PMLOPT defines perfectly matched layers (PML) for acoustic or
        structural analyses. Each PML region must have a uniquely defined
        element coordinate system. Normal reflection coefficient values for a
        harmonic analysis must be less than 1.

        Issue PMLOPT,STAT to list the current normal reflection coefficient or
        attenuation factor settings for a PML region. Issue PMLOPT,CLEAR to
        clear all normal reflection coefficient settings and restore them to
        the defaults. Issue PMLOPT,ESYS,CLEAR to clear all normal reflection
        coefficient settings for this element coordinate system and restore
        them to the defaults.
        """
        command = (
            f"PMLOPT,{esys},{lab},{xminus},{xplus},{yminus},{yplus},{zminus},{zplus}"
        )
        return self.run(command, **kwargs)

    def pmlsize(
        self, freqb="", freqe="", dmin="", dmax="", thick="", angle="", **kwargs
    ):
        """Determines number of PML layers.

        APDL Command: PMLSIZE

        Parameters
        ----------
        freqb
            Minimum operating frequency

        freqe
            Maximum operating frequency

        dmin
            Minimum distance from radiation source to PML interface.

        dmax
            Maximum distance from radiation source to PML interface.

        thick
            Thickness of PML region. Defaults to 0.

        angle
            Incident angle of wave to the PML interface. Defaults to 0.

        Notes
        -----
        PMLSIZE determines the number of PML layers for acceptable numerical
        accuracy.

        PMLSIZE must be issued before any meshing commands. If the thickness of
        the PML region is known, it determines an element edge length (h) and
        issues ESIZE,h.  If the thickness of the PML region is unknown, it
        determines the number of layers (n) and issues ESIZE,,n.
        """
        command = f"PMLSIZE,{freqb},{freqe},{dmin},{dmax},{thick},{angle}"
        return self.run(command, **kwargs)
