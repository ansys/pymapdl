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

"""Non-interactive command context manager."""

import logging
import weakref

from ansys.mapdl.core._mapdl_core import _CoreMixinBase


class _NonInteractiveContext:
    """Allow commands that must run non-interactively."""

    def __init__(self, parent):
        self._parent = weakref.ref(parent)

    def __enter__(self):
        parent = self._parent()
        parent._log.debug("Entering in non-interactive mode")
        if parent.logger.logger.level <= logging.DEBUG:
            parent.com("Entering in non_interactive mode")
        parent._store_commands = True

    def __exit__(self, *args):
        parent = self._parent()
        parent._store_commands = False

        if args[0] is not None:
            parent._log.debug(
                "An exception was found in the `non_interactive` environment. "
                "Hence the commands are not flushed and are discarded."
            )
            parent._stored_commands = []
            return None

        parent._log.debug("Exiting non-interactive mode")
        parent._flush_stored()


class _NonInteractiveMixin(_CoreMixinBase):
    """Expose the ``non_interactive`` context."""

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
