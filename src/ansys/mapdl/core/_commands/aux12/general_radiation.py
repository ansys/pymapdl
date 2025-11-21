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

from ansys.mapdl.core._commands import CommandsBase


class GeneralRadiation(CommandsBase):

    def aux12(self, **kwargs):
        r"""Enters the radiation processor.

        Mechanical APDL Command: `/AUX12 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_AUX12.html>`_

        Notes
        -----

        .. _s-AUX12_notes:

        Enters the radiation processor (auxiliary processor AUX12). This processor supports the Radiation
        Matrix and the Radiosity Solver methods.

        This command is valid only at the Begin Level.
        """
        command = "/AUX12"
        return self.run(command, **kwargs)

    def stef(self, value: str = "", **kwargs):
        r"""Specifies Stefan-Boltzmann radiation constant.

        Mechanical APDL Command: `STEF <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_STEF.html>`_

        Parameters
        ----------
        value : str
            Stefan-Boltzmann constant (defaults to 0.119E-10 Btu/hr/in :sup:`2` / °R :sup:`4` ).

        Notes
        -----

        .. _STEF_notes:

        You can use this command in the general preprocessor (PREP7) and in the Solution processor to
        specify the Stefan-Boltzmann constant in analyses using the radiation matrix method or the radiosity
        solver to model radiation.
        """
        command = f"STEF,{value}"
        return self.run(command, **kwargs)
