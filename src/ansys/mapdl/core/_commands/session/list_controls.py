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


class ListControls:
    def com(self, comment="", **kwargs):
        """Places a comment in the output.

        APDL Command: /COM

        Parameters
        ----------
        comment
            Comment string, up to 75 characters.

        Notes
        -----
        The output from this command consists of the comment string.  This
        command is similar to C*** except that the comment produced by C*** is
        more easily identified in the output. Parameter substitution within the
        comment occurs for every valid expression delimited by percent (%)
        signs. Enclosing such an expression in single quotes prevents parameter
        substitution.

        Another way to include a comment is to precede it with a ! character
        (on the same line).  The ! may be placed anywhere on the line, and any
        input following it is ignored as a comment.  No output is produced by
        such a comment, but the comment line is included on the log file.  This
        is a convenient way to annotate the log file.

        This command is valid anywhere.
        """
        command = f"/COM, {comment}"
        return self.run(command, **kwargs)

    def golist(self, **kwargs):
        """Reactivates the suppressed data input listing.

        APDL Command: /GOLIST

        Notes
        -----
        Reactivates printout of the data input listing suppressed with /NOLIST.

        This command is valid in any processor, but only within a batch run
        [/BATCH].
        """
        command = "/GOLIST,"
        return self.run(command, **kwargs)

    def gopr(self, **kwargs):
        """Reactivates suppressed printout.

        APDL Command: /GOPR

        Notes
        -----
        Reactivates printout suppressed with the /NOPR command.  The /GO
        command has the same function except that it does not produce a command
        response from the program.

        This command is valid in any processor.
        """
        command = "/GOPR,"
        return self.run(command, **kwargs)

    def nolist(self, **kwargs):
        """Suppresses the data input listing.

        APDL Command: /NOLIST

        Notes
        -----
        Printout is suppressed until a /GOLIST command is read or the end of
        the listing is encountered.

        This command is valid in any processor, but only within a batch run
        [/BATCH].
        """
        command = "/NOLIST,"
        return self.run(command, **kwargs)

    def nopr(self, **kwargs):
        """Suppresses the expanded interpreted input data listing.

        APDL Command: /NOPR

        Notes
        -----
        Suppresses printout of interpreted input data, including information
        labeled as "Notes."  When this printout is not suppressed, the data
        input to the analysis is echoed to the output file in an expanded
        format.  Printout is suppressed until a /GOPR or /GO command is read.

        Use of /NOPR is not recommended when the graphical user interface (GUI)
        is active.  The GUI sometimes issues "hidden" /NOPR and /GOPR command
        sequences, which will countermand user-issued /NOPR commands, thus
        making the use of /NOPR in the GUI environment unpredictable.

        This command is valid in any processor.
        """
        command = "/NOPR,"
        return self.run(command, **kwargs)
