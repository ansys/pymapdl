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

"""These commands may be run by PyMAPDL, but are not supported from a
user-context.

"""


class _Hidden:
    def _batch(self, lab="", **kwargs):
        """APDL Command: /BATCH

        Sets the program mode to "batch."

        Parameters
        ----------
        lab
            Specifies listing mode during a batch run:

            LIST
                The batch output will include a listing of the input file.

            (blank)
                Suppress input data listing.

        Notes
        -----
        Sets the program mode to "batch" when included as the first line on an
        input file of ANSYS commands.  For convenience, this command is
        automatically recorded on the log file (Jobname.LOG) at the beginning
        of an interactive ANSYS session so that the log file can be reused
        later for batch input.

        Caution:: : This command  should not be entered directly in an
        interactive ANSYS session since all subsequent keyboard input is simply
        copied to a file, without further processing or prompts from the
        program (use the "system break" to exit the ANSYS program if this
        occurs).

        The recommended method for choosing batch mode, rather than using the
        /BATCH command, is to select the Batch simulation environment from the
        ANSYS Product Launcher  task in the ANSYS launcher, or the batch mode
        entry option on the ANSYS execution command when entering the program.

        This command is valid only at the Begin Level.
        """
        command = "/BATCH,%s" % (str(lab))
        return self.run(command, **kwargs)

    def _output(self, fname="", ext="", loc="", **kwargs):
        """Redirects text output to a file or to the screen.

        APDL Command: /OUTPUT

        Parameters
        ----------
        fname
            Filename and directory path (248 character maximum, including
            directory) to which text output will be redirected (defaults to
            Jobname if Ext is specified).  For interactive runs, Fname = TERM
            (or blank) redirects output to the screen.  For batch runs, Fname =
            blank (with all remaining command arguments blank) redirects output
            to the  default system output file.

        ext
            Filename extension (eight-character maximum).

        loc
            Location within a file to which output will be written:

            (blank)
                Output is written starting at the top of the file (default).

            APPEND
                Output is appended to the existing file.

        Notes
        -----
        Text output includes responses to every command and GUI
        function, notes, warnings, errors, and other informational
        messages.  Upon execution of /OUTPUT,Fname, Ext, ..., all
        subsequent text output is redirected to the file Fname.Ext.
        To redirect output back to the default location, issue /OUTPUT
        (no arguments).

        This command is valid in any processor.
        """
        if loc:
            return self.run(f"/OUTPUT,{fname},{ext},,{loc}", **kwargs)
        else:
            return self.run(f"/OUTPUT,{fname},{ext}", **kwargs)
