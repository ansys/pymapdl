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


class ProcessorEntry(CommandsBase):

    def finish(self, **kwargs):
        r"""Exits normally from a processor.

        Mechanical APDL Command: `FINISH <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_FINISH.html>`_

        Notes
        -----

        .. _FINISH_notes:

        This command exits any of the Mechanical APDL processors.

        When exiting the Mechanical APDL processors, data remains intact in the database, but the database
        is not
        automatically written to a file. (Issue :ref:`save` to write the database to a file.)

        If exiting POST1 or POST26:

        * POST1: Data in the database remains intact (including the POST1 element table data, the path table
          data, the fatigue table data, and the load case pointers).

        * POST26: Data in the database remains intact, except that POST26 variables are erased and
          specification commands (such as :ref:`file`, :ref:`prtime`, and :ref:`nprint` ) are reset. Issue
          :ref:`quit` to exit the processor and bypass these exceptions.

        See :ref:`quit` for an alternate processor exit command.

        This command is valid in any processor. This command is not valid at the Begin level.
        """
        command = "FINISH"
        return self.run(command, **kwargs)

    def post1(self, **kwargs):
        r"""Enters the database results postprocessor.

        Mechanical APDL Command: `/POST1 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_POST1.html>`_

        Notes
        -----

        .. _s-POST1_notes:

        Enters the general database results postprocessor (POST1). All load symbols ( :ref:`pbc`,
        :ref:`psf`, or :ref:`pbf` ) are automatically turned off with this command.

        This command is valid only at the Begin Level.
        """
        command = "/POST1"
        return self.run(command, **kwargs)

    def post26(self, **kwargs):
        r"""Enters the time-history results postprocessor.

        Mechanical APDL Command: `/POST26 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_POST26.html>`_

        Notes
        -----

        .. _s-POST26_notes:

        Enters the time-history results postprocessor (POST26).

        This command is valid only at the Begin Level.
        """
        command = "/POST26"
        return self.run(command, **kwargs)

    def prep7(self, **kwargs):
        r"""Enters the model creation preprocessor.

        Mechanical APDL Command: `/PREP7 <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_PREP7.html>`_

        Notes
        -----

        .. _s-PREP7_notes:

        Enters the general input data preprocessor (PREP7).

        This command is valid only at the Begin Level.
        """
        command = "/PREP7"
        return self.run(command, **kwargs)

    def quit(self, **kwargs):
        r"""Exits a processor.

        Mechanical APDL Command: `/QUIT <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_QUIT.html>`_

        Notes
        -----

        .. _s-QUIT_notes:

        This is an alternative to the :ref:`finish` command. If any cleanup or file writing is normally done
        by the :ref:`finish` command, it is bypassed if the :ref:`quit` command is used instead. A new
        processor may be entered after this command. See the ``/EXIT`` command to terminate the run.

        This command is valid in any processor. This command is not valid at the Begin level.
        """
        command = "/QUIT"
        return self.run(command, **kwargs)

    def slashsolu(self, **kwargs):
        r"""Enters the solution processor.

        Mechanical APDL Command: `/SOLU <https://ansyshelp.ansys.com/Views/Secured/corp/v232/en//ans_cmd/Hlp_C_SOLU_sl.html>`_

        Notes
        -----

        .. _s-SOLU_notes:

        This command is valid only at the Begin Level.
        """
        command = "/SOLU"
        return self.run(command, **kwargs)
