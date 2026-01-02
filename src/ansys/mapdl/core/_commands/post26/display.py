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


class Display(CommandsBase):

    def keep(self, key: str = "", **kwargs):
        r"""Stores POST26 definitions and data during active session.

        Mechanical APDL Command: `KEEP <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_KEEP.html>`_

        Parameters
        ----------
        key : str
            State or value

            * ``On or 1`` - Allows you to exit and reenter :ref:`post26` without losing your current time
              history variable information. Keeps a cache of the :ref:`post26` variable information including the
              active file name ( :ref:`file` ), variable definitions ( :ref:`nsol`, :ref:`esol`, :ref:`rforce`,
              and :ref:`solu` ) and stored variable data in memory for the current Mechanical APDL session.

            * ``Off or 0`` - :ref:`post26` variable information is deleted when you exit :ref:`post26`.

        Notes
        -----

        .. _KEEP_notes:

        Your variable information is saved in memory only for the current active Mechanical APDL session. It
        is
        deleted when you exit Mechanical APDL. This information is also deleted when you issue :ref:`clear`,
        :ref:`resume`, :ref:`solve`, or :ref:`reset`.

        When you reenter :ref:`post26` all time history variable data is available for use. When you issue
        :ref:`store`, NEW, variable definitions created by math operations such as :ref:`add` or :ref:`prod`
        will not be restored. However, variables defined with :ref:`nsol`, :ref:`esol`, :ref:`rforce`, and
        :ref:`solu`  will be restored. Only the last active results file name is kept in memory (
        :ref:`file` ).

        Commands such as :ref:`layerp26`, :ref:`shell`, and :ref:`force` that specify the location or a
        component of data to be stored will retain the setting at the time of exiting :ref:`post26`.
        """
        command = f"KEEP,{key}"
        return self.run(command, **kwargs)

    def plcplx(self, key: int | str = "", **kwargs):
        r"""Specifies the part of a complex variable to display.

        Mechanical APDL Command: `PLCPLX <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLCPLX.html>`_

        Parameters
        ----------
        key : int or str
            Complex variable part:

            * ``0`` - Amplitude.

            * ``1`` - Phase angle.

            * ``2`` - Real part.

            * ``3`` - Imaginary part.

        Notes
        -----

        .. _PLCPLX_notes:

        Used only with harmonic analyses ( :ref:`antype`,HARMIC).

        All results data are stored in the form of real and imaginary components and converted to amplitude
        and/or phase angle as specified via the :ref:`plcplx` command. The conversion is not valid for
        derived results (such as principal stress/strain, equivalent stress/strain and USUM).
        """
        command = f"PLCPLX,{key}"
        return self.run(command, **kwargs)

    def pltime(self, tmin: str = "", tmax: str = "", **kwargs):
        r"""Defines the time range for which data are to be displayed.

        Mechanical APDL Command: `PLTIME <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLTIME.html>`_

        **Command default:**

        .. _PLTIME_default:

        Use the previously defined range ( :ref:`timerange` ).

        Parameters
        ----------
        tmin : str
            Minimum time (defaults to the first point stored).

        tmax : str
            Maximum time (defaults to the last point stored).

        Notes
        -----

        .. _PLTIME_notes:

        Defines the time (or frequency) range (within the range stored) for which data are to be displayed.
        Time is always displayed in the Z-axis direction for 3D graph displays. If XVAR = 1, time is also
        displayed in the X-axis direction and this control also sets the abscissa scale range.
        """
        command = f"PLTIME,{tmin},{tmax}"
        return self.run(command, **kwargs)

    def plvar(
        self,
        nvar1: str = "",
        nvar2: str = "",
        nvar3: str = "",
        nvar4: str = "",
        nvar5: str = "",
        nvar6: str = "",
        nvar7: str = "",
        nvar8: str = "",
        nvar9: str = "",
        nvar10: str = "",
        **kwargs,
    ):
        r"""Displays up to ten variables in the form of a graph.

        Mechanical APDL Command: `PLVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PLVAR.html>`_

        Parameters
        ----------
        nvar1 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar2 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar3 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar4 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar5 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar6 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar7 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar8 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar9 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        nvar10 : str
            Variables to be displayed, defined either by the reference number or a unique thirty-two
            character name. If duplicate names are used the command will plot the data for the lowest-
            numbered variable with that name.

        Notes
        -----

        .. _PLVAR_notes:

        Variables are displayed vs. variable ``N`` on the :ref:`xvar` command. The string value will be a
        predefined, unique name. For complex variables, the amplitude is displayed by default (
        :ref:`plcplx` ). Each :ref:`plvar` command produces a new frame. See the :ref:`grtyp` command for
        displaying multiple variables in a single frame with separate Y-axes.
        """
        command = f"PLVAR,{nvar1},{nvar2},{nvar3},{nvar4},{nvar5},{nvar6},{nvar7},{nvar8},{nvar9},{nvar10}"
        return self.run(command, **kwargs)

    def spread(self, value: str = "", **kwargs):
        r"""Turns on a dashed tolerance curve for the subsequent curve plots.

        Mechanical APDL Command: `SPREAD <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SPREAD.html>`_

        Parameters
        ----------
        value : str
            Amount of tolerance. For example, 0.1 is ± 10%.
        """
        command = f"SPREAD,{value}"
        return self.run(command, **kwargs)

    def xvar(self, n: int | str = "", **kwargs):
        r"""Specifies the X variable to be displayed.

        Mechanical APDL Command: `XVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_XVAR.html>`_

        Parameters
        ----------
        n : int or str
            X variable number:

            * ``0 or 1`` - Display :ref:`plvar` values vs. time (or frequency).

            * ``n`` - Display :ref:`plvar` values vs. variable ``n`` (2 to ``NV`` ( :ref:`numvar` )).

            * ``1`` - Interchange time and :ref:`plvar` variable numbers with time as the curve parameter.
              :ref:`plvar` variable numbers are displayed uniformly spaced along X-axis from position 1 to 10.

        Notes
        -----

        .. _XVAR_notes:

        Defines the X variable (displayed along the abscissa) against which the Y variable(s) ( :ref:`plvar`
        ) are to be displayed.
        """
        command = f"XVAR,{n}"
        return self.run(command, **kwargs)
