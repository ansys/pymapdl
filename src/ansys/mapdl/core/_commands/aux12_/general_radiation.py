# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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


class GeneralRadiation:
    def stef(self, value="", **kwargs):
        """Specifies Stefan-Boltzmann radiation constant.

        APDL Command: STEF

        Parameters
        ----------
        value
            Stefan-Boltzmann constant (defaults to 0.119E-10 Btu/hr/in2/ °R4).

        Notes
        -----
        You can use this command in the general preprocessor (PREP7) and in the
        Solution processor to specify the Stefan-Boltzmann constant in analyses
        using the radiation matrix method or the radiosity solver to model
        radiation.
        """
        command = f"STEF,{value}"
        return self.run(command, **kwargs)

    def toffst(self, value="", **kwargs):
        """Specifies the temperature offset from absolute zero to zero.

        APDL Command: TOFFST

        Parameters
        ----------
        value
            Degrees between absolute zero and zero of temperature system used
            (should be positive).

        Notes
        -----
        Specifies the difference (in degrees) between absolute zero and the
        zero of the temperature system used.  Absolute temperature values are
        required in evaluating certain expressions, such as for creep,
        swelling, radiation heat transfer, MASS71, etc.  (The offset
        temperature is not used in evaluating emissivity.) Examples are 460°
        for the Fahrenheit system and 273° for the Celsius system.  The offset
        temperature is internally included in the element calculations and does
        not affect the temperature input or output.  If used in SOLUTION, this
        command is valid only within the first load step.

        This command is also valid in PREP7.
        """
        command = f"TOFFST,{value}"
        return self.run(command, **kwargs)
