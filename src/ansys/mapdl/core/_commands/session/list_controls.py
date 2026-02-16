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


class ListControls(CommandsBase):

    def com(self, comment: str = "", **kwargs):
        r"""Places a comment in the output.

        Mechanical APDL Command: `/COM <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_COM.html>`_

        Parameters
        ----------
        comment : str
            Comment string, up to 75 characters.

        Notes
        -----

        .. _s-COM_notes:

        The output from this command consists of the comment string. This command is similar to ``C***``
        except that the comment produced by ``C***`` is more easily identified in the output. Parameter
        substitution within the comment occurs for every valid expression delimited by percent (%) signs.
        Enclosing such an expression in single quotes prevents parameter substitution.

        Another way to include a comment is to precede it with a ! character (on the same line). The ! may
        be placed anywhere on the line, and any input following it is ignored as a comment. No output is
        produced by such a comment, but the comment line is included on the log file. This is a convenient
        way to annotate the log file.

        This command is valid anywhere.
        """
        command = f"/COM,{comment}"
        return self.run(command, **kwargs)

    def golist(self, **kwargs):
        r"""Reactivates the suppressed data input listing.

        Mechanical APDL Command: `/GOLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GOLIST.html>`_

        Notes
        -----

        .. _s-GOLIST_notes:

        Reactivates printout of the data input listing suppressed with :ref:`nolist`.

        This command is valid in any processor, but only within a batch run ( ``/BATCH`` ).
        """
        command = "/GOLIST"
        return self.run(command, **kwargs)

    def gopr(self, **kwargs):
        r"""Reactivates suppressed printout.

        Mechanical APDL Command: `/GOPR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GOPR.html>`_

        Notes
        -----

        .. _s-GOPR_notes:

        Reactivates printout suppressed with the :ref:`nopr` command. The :ref:`slashgo` command has the
        same function except that it does not produce a command response from the program.

        This command is valid in any processor.
        """
        command = "/GOPR"
        return self.run(command, **kwargs)

    def nolist(self, **kwargs):
        r"""Suppresses the data input listing.

        Mechanical APDL Command: `/NOLIST <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NOLIST.html>`_

        Notes
        -----

        .. _s-NOLIST_notes:

        Printout is suppressed until a :ref:`golist` command is read or the end of the listing is
        encountered.

        This command is valid in any processor, but only within a batch run ( ``/BATCH`` ).
        """
        command = "/NOLIST"
        return self.run(command, **kwargs)

    def nopr(self, **kwargs):
        r"""Suppresses the expanded interpreted input data listing.

        Mechanical APDL Command: `/NOPR <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_NOPR.html>`_

        .. warning::

            PyMAPDL uses the console output to parse and retrieve information from the MAPDL
            instance. Hence, it is strongly advised to **NOT** use this command unless you really
            know what you are doing. In case of an accidental ``NOPR`` activation, you can run
            `mapdl.gopr()` to reactivate console output.

        Notes
        -----

        .. _s-NOPR_notes:

        Suppresses printout of interpreted input data, including information labeled as "Notes." When this
        printout is not suppressed, the data input to the analysis is echoed to the output file in an
        expanded format. Printout is suppressed until a :ref:`gopr` or :ref:`slashgo` command is read.

        Use of :ref:`nopr` is not recommended when the graphical user interface (GUI) is active. The GUI
        sometimes issues "hidden" :ref:`nopr` and :ref:`gopr` command sequences, which will countermand
        user-issued :ref:`nopr` commands, thus making the use of :ref:`nopr` in the GUI environment
        unpredictable.

        This command is valid in any processor.
        """
        command = "/NOPR"
        return self.run(command, **kwargs)

    def slashgo(self, **kwargs):
        r"""Reactivates suppressed printout.

        Mechanical APDL Command: `/GO <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_GO.html>`_

        Notes
        -----

        .. _s-GO_notes:

        Reactivates printout suppressed with the :ref:`nopr` command without producing any output. The
        :ref:`gopr` command has the same function except that it also produces a command response from the
        program.

        This command is valid in any processor.
        """
        command = "/GO"
        return self.run(command, **kwargs)
