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


class Listing:

    def extrem(self, nvar1: str = "", nvar2: str = "", ninc: str = "", **kwargs):
        r"""Lists the extreme values for variables.

        Mechanical APDL Command: `EXTREM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_EXTREM.html>`_

        Parameters
        ----------
        nvar1 : str
            List extremes for variables ``NVAR1`` through ``NVAR2`` in steps of ``NINC``. Variable range
            defaults to its maximum. ``NINC`` defaults to 1.

        nvar2 : str
            List extremes for variables ``NVAR1`` through ``NVAR2`` in steps of ``NINC``. Variable range
            defaults to its maximum. ``NINC`` defaults to 1.

        ninc : str
            List extremes for variables ``NVAR1`` through ``NVAR2`` in steps of ``NINC``. Variable range
            defaults to its maximum. ``NINC`` defaults to 1.

        Notes
        -----

        .. _EXTREM_notes:

        Lists the extreme values (and the corresponding times) for stored and calculated variables. Extremes
        for stored variables are automatically listed as they are stored. Only the real part of a complex
        number is used. Extreme values may also be assigned to parameters ( :ref:`get` ).
        """
        command = f"EXTREM,{nvar1},{nvar2},{ninc}"
        return self.run(command, **kwargs)

    def lines(self, n: str = "", **kwargs):
        r"""Specifies the length of a printed page.

        Mechanical APDL Command: `LINES <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LINES.html>`_

        Parameters
        ----------
        n : str
            Number of lines per page (defaults to 20). (Minimum allowed = 11).

        Notes
        -----

        .. _LINES_notes:

        Specifies the length of a printed page (for use in reports, etc.).
        """
        command = f"LINES,{n}"
        return self.run(command, **kwargs)

    def nprint(self, n: str = "", **kwargs):
        r"""Defines which time points stored are to be listed.

        Mechanical APDL Command: `NPRINT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NPRINT.html>`_

        Parameters
        ----------
        n : str
            List data associated with every ``N`` time (or frequency) point(s), beginning with the first
            point stored (defaults to 1).

        Notes
        -----

        .. _NPRINT_notes:

        Defines which time (or frequency) points within the range stored are to be listed.
        """
        command = f"NPRINT,{n}"
        return self.run(command, **kwargs)

    def prcplx(self, key: int | str = "", **kwargs):
        r"""Defines the output form for complex variables.

        Mechanical APDL Command: `PRCPLX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRCPLX.html>`_

        Parameters
        ----------
        key : int or str
            Output form key:

            * ``0`` - Real and imaginary parts.

            * ``1`` - Amplitude and phase angle. Stored real and imaginary data are converted to amplitude and
              phase angle upon output. Data remain stored as real and imaginary parts.

        Notes
        -----

        .. _PRCPLX_notes:

        Defines the output form for complex variables. Used only with harmonic analyses (
        :ref:`antype`,HARMIC).

        All results data are stored in the form of real and imaginary components and converted to amplitude
        and/or phase angle as specified via the :ref:`prcplx` command. The conversion is not valid for
        derived results (such as principal stress/strain, equivalent stress/strain and USUM).
        """
        command = f"PRCPLX,{key}"
        return self.run(command, **kwargs)

    def prtime(self, tmin: str = "", tmax: str = "", **kwargs):
        r"""Defines the time range for which data are to be listed.

        Mechanical APDL Command: `PRTIME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRTIME.html>`_

        **Command default:**

        .. _PRTIME_default:

        Use the previously defined range ( :ref:`timerange` ).

        Parameters
        ----------
        tmin : str
            Minimum time (defaults to the first point stored).

        tmax : str
            Maximum time (defaults to the last point stored).

        Notes
        -----

        .. _PRTIME_notes:

        Defines the time (or frequency) range (within the range stored) for which data are to be listed.
        """
        command = f"PRTIME,{tmin},{tmax}"
        return self.run(command, **kwargs)

    def prvar(
        self,
        nvar1: str = "",
        nvar2: str = "",
        nvar3: str = "",
        nvar4: str = "",
        nvar5: str = "",
        nvar6: str = "",
        **kwargs,
    ):
        r"""Lists variables vs. time (or frequency).

        Mechanical APDL Command: `PRVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PRVAR.html>`_

        Parameters
        ----------
        nvar1 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will print the data for the lowest-
            numbered variable with that name.

        nvar2 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will print the data for the lowest-
            numbered variable with that name.

        nvar3 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will print the data for the lowest-
            numbered variable with that name.

        nvar4 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will print the data for the lowest-
            numbered variable with that name.

        nvar5 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will print the data for the lowest-
            numbered variable with that name.

        nvar6 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will print the data for the lowest-
            numbered variable with that name.

        Notes
        -----

        .. _PRVAR_notes:

        Lists variables vs. time (or frequency). Up to six variables may be listed across the line. Time
        column output format can be changed using the :ref:`format` command arguments ``Ftype``, ``NWIDTH``,
        and ``DSIGNF``.
        """
        command = f"PRVAR,{nvar1},{nvar2},{nvar3},{nvar4},{nvar5},{nvar6}"
        return self.run(command, **kwargs)
