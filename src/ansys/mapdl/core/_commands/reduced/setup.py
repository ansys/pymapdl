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


class Setup:
    def rmresume(self, fname="", ext="", **kwargs):
        """Resumes ROM data from a file.

        APDL Command: RMRESUME

        Parameters
        ----------
        fname
            Name and directory path of the ROM database file (248 character
            maximum). Default to Jobname.

        ext
            Extension of the ROM database file. Default to .rom.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        command = f"RMRESUME,{fname},{ext}"
        return self.run(command, **kwargs)

    def rmsave(self, fname="", ext="", **kwargs):
        """Saves ROM data to file.

        APDL Command: RMSAVE

        Parameters
        ----------
        fname
            Name and directory path of the ROM database file. Default to
            Jobname.

        ext
            Extension of the ROM database file. Default to .rom.

        Notes
        -----
        Distributed ANSYS Restriction: This command is not supported in
        Distributed ANSYS.
        """
        return self.run(f"RMSAVE,{fname},{ext}", **kwargs)
