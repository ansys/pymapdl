# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""MAPDL command-wide context facade methods."""

from ansys.mapdl.core.errors import MapdlRuntimeError

from ansys.mapdl.core._mapdl_core import _CoreMixinBase
from .chain_commands import _ChainCommandsContext
from .force_output import _ForceOutputContext
from .muted import _MutedContext
from .non_interactive import _NonInteractiveContext
from .run_as_routine import (
    _RunAsRoutineContext,
    _cache_routine,
    _enter_routine,
    _resume_routine,
)


class _CoreCommandContextMixin(_CoreMixinBase):
    """Expose command-wide contexts while implementations remain composed."""
    @property
    def chain_commands(self):
        """Chain several mapdl commands.

        Commands can be separated with ``"$"`` in MAPDL rather than
        with a line break, so you could send multiple commands to
        MAPDL with:

        ``mapdl.run("/PREP7$K,1,1,2,3")``

        This method is merely a convenience context manager to allow
        for easy chaining of PyMAPDL commands to speed up sending
        commands to MAPDL.

        View the response from MAPDL with :attr:`Mapdl.last_response`.

        Notes
        -----
        Distributed Ansys cannot properly handle condensed data input
        and chained commands are not permitted in distributed ansys.

        Examples
        --------
        >>> with mapdl.chain_commands:
            mapdl.prep7()
            mapdl.k(1, 1, 2, 3)
        """
        if self._distributed:
            raise MapdlRuntimeError(
                "Chained commands are not permitted in distributed ansys."
            )
        return _ChainCommandsContext(self)

    @property
    def force_output(self):
        """Force text output globally by turning the ``Mapdl.mute`` attribute to False
        and activating text output (``/GOPR``)

        You can still do changes to those inside this context.
        """
        return _ForceOutputContext(self)

    @property
    def non_interactive(self):
        """Non-interactive context manager.

        Allow to execute code without user interaction or waiting
        between PyMAPDL responses.
        It can also be used to execute some commands which are not
        supported in interactive mode. For a complete list of commands
        visit :ref:`ref_unsupported_interactive_commands`.

        View the last response with :attr:`Mapdl.last_response` method.

        Notes
        -----
        All the commands executed inside this context manager are not
        executed until the context manager exits which then execute them
        all at once in the MAPDL instance.

        This command uses :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>`
        method.

        Examples
        --------
        Use the non-interactive context manager for the VWRITE (
        :func:`Mapdl.vwrite() <ansys.mapdl.core.Mapdl.vwrite>`)
        command.

        >>> with mapdl.non_interactive:
        ...    mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        ...    mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")
        >>> mapdl.last_response
        """
        return _NonInteractiveContext(self)

    @property
    def muted(self):
        """Context manager that suppress all output from MAPDL

        Use the `muted` context manager to suppress all the output. Similar to
        setting `mapdl.mute = True` but only for the context manager.

        Examples
        --------
        >>> with mapdl.muted:
        ...    mapdl.run("/SOLU") # This call is muted
        """
        return _MutedContext(self)

    def run_as_routine(self, routine):
        """Run commands at a routine and then revert to the prior routine.

        Parameters
        ----------
        routine : str
            A MAPDL routine. For example, ``"PREP7"`` or ``"POST1"``.

        Examples
        --------
        Enter ``PREP7`` and run ``numvar``, which requires ``POST26``, and
        revert to the prior routine.

        >>> mapdl.prep7()
        >>> mapdl.parameters.routine
        'PREP7'
        >>> with mapdl.run_as_routine('POST26'):
        ...     mapdl.numvar(200)
        >>> mapdl.parameters.routine
        'PREP7'
        """
        return _RunAsRoutineContext(self, routine)

    def _enter_routine(self, routine):
        return _enter_routine(self, routine)

    def _cache_routine(self):
        return _cache_routine(self)

    def _resume_routine(self):
        return _resume_routine(self)
