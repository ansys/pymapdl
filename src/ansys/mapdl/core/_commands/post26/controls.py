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


class Controls:

    def cfact(
        self,
        rfacta: str = "",
        ifacta: str = "",
        rfactb: str = "",
        ifactb: str = "",
        rfactc: str = "",
        ifactc: str = "",
        **kwargs,
    ):
        r"""Defines complex scaling factors to be used with operations.

        Mechanical APDL Command: `CFACT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_CFACT.html>`_

        **Command default:**

        .. _CFACT_default:

        Use the real factors as described with the operation command.

        Parameters
        ----------
        rfacta : str
            Real portion of the complex scale factor used in place of ``FACTA``.

        ifacta : str
            Imaginary portion of the complex scale factor used in place of ``FACTA``.

        rfactb : str
            Real portion of the complex scale factor used in place of ``FACTB``.

        ifactb : str
            Imaginary portion of the complex scale factor used in place of ``FACTB``.

        rfactc : str
            Real portion of the complex scale factor used in place of ``FACTC``.

        ifactc : str
            Imaginary portion of the complex scale factor used in place of ``FACTC``.

        Notes
        -----

        .. _CFACT_notes:

        Defines complex scale factors to be used with the operations ( :ref:`add`, :ref:`prod`, etc.). If
        this command is supplied, these complex factors override any real factors ( ``FACTA``, ``FACTB``,
        ``FACTC`` ) supplied on the operation commands. Factors are typically involved in scaling a
        specified variable, such as in the term ``FACTA`` x ``IA`` of the :ref:`add` command to scale
        variable ``IA`` before the ADD operation.

        When the :ref:`cfact` command is active, defaults are as follows: 1) if the complex factor is not
        specified, but the variable upon which it acts (such as ``IA`` ) is specified, the factor defaults
        to 1.0+ i 0.0; 2) if the variable upon which the factor operates is not specified, but the factor is
        specified, the variable defaults to 1.0 so that the term in the operation becomes the complex factor
        itself; 3) if neither the factor nor the variable number is supplied, the term is omitted from the
        operation. Once the operation (such as the :ref:`add` command) has been processed, the :ref:`cfact`
        command becomes inactive and must be specified again if it is to be used.
        """
        command = f"CFACT,{rfacta},{ifacta},{rfactb},{ifactb},{rfactc},{ifactc}"
        return self.run(command, **kwargs)

    def layerp26(self, num: str = "", **kwargs):
        r"""Specifies the element layer for which data are to be stored.

        Mechanical APDL Command: `LAYERP26 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_LAYERP26.html>`_

        Parameters
        ----------
        num : str
            Layer-processing mode:

            * ``N`` - The layer number to process. The default value is 1.

        Notes
        -----

        .. _LAYERP26_notes:

        Defines the element layer for which results data are to be stored for postprocessing. Applies to
        stress and strain data for layered elements ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLSH190``,
        ``SHELL208``, ``SHELL209``, ``SHELL281``, ``REINF265``, and ``ELBOW290``.

        The :ref:`shell` command can be used (for shell elements) to specify a location (TOP, MID, BOT)
        within the layer for selection on the :ref:`esol` command. Transverse shear stresses for MID are
        linearly averaged from TOP and BOT, and do not reflect a parabolic distribution. Setting KEYOPT(8) =
        2 for ``SHELL181``, ``SHELL208``, ``SHELL209``, ``SHELL281``, and ``ELBOW290`` writes the mid-
        surface values directly to the results file and yields more accurate values than linear averaging.

        That this command cannot be used for energy output, as energy is a per-element quantity.

        When using the :ref:`layerp26` command with ``SHELL181``, ``SOLID185``, ``SOLID186``, ``SOLSH190``,
        ``SHELL208``, or ``SHELL209``, KEYOPT(8) must be set to 1 (or 2 for ``SHELL181``, ``SHELL208``,
        ``SHELL209``, ``SHELL281``, and ``ELBOW290`` ) in order to store results for all layers.

        In POST26, the :ref:`esol` data stored is based on the active :ref:`layerp26` specification at the
        time the data is stored. To store data at various specifications (for example, layers 2 and 5),
        issue a :ref:`store` command before each new specification.
        """
        command = f"LAYERP26,{num}"
        return self.run(command, **kwargs)

    def tvar(self, key: int | str = "", **kwargs):
        r"""Changes time to the cumulative iteration number.

        Mechanical APDL Command: `TVAR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_TVAR.html>`_

        Parameters
        ----------
        key : int or str
            Time key:

            * ``0`` - Time is used for the variable ``TIME``.

            * ``1`` - NCUMIT is used for the variable ``TIME``.

        Notes
        -----

        .. _TVAR_notes:

        Changes the meaning of the time variable to the cumulative iteration number (NCUMIT) variable. Data
        can be read from the file, printed, and displayed as a function of NCUMIT rather than time. All
        POST26 descriptions applying to TIME then apply to NCUMIT.
        """
        command = f"TVAR,{key}"
        return self.run(command, **kwargs)
