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


"""The contexts MAPDL core responsibility mixin."""

from enum import Enum  # noqa: F401
from functools import wraps  # noqa: F401
import glob  # noqa: F401
import logging  # noqa: F401
import os  # noqa: F401
import pathlib  # noqa: F401
import re  # noqa: F401
from shutil import copyfile, rmtree  # noqa: F401

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from subprocess import DEVNULL, call  # nosec B404  # noqa: F401
import tempfile  # noqa: F401
import time  # noqa: F401
from typing import (  # noqa: F401
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TextIO,
    Tuple,
    TypeAlias,
    Union,
)
from uuid import uuid4  # noqa: F401
from warnings import warn  # noqa: F401
import weakref  # noqa: F401

import numpy as np  # noqa: F401

from ansys.mapdl import core as pymapdl  # noqa: F401
from ansys.mapdl.core import LOG as logger  # noqa: F401
from ansys.mapdl.core import _HAS_DPF, _HAS_VISUALIZER  # noqa: F401
from ansys.mapdl.core.commands import (  # noqa: F401
    CMD_BC_LISTING,
    CMD_LISTING,
    CMD_XSEL,
    XSEL_DOCSTRING_INJECTION,
    BoundaryConditionsListingOutput,
    CommandListingOutput,
    Commands,
    StringWithLiteralRepr,
    inject_docs,
)
from ansys.mapdl.core.errors import (  # noqa: F401
    ComponentNoData,
    MapdlCommandIgnoredError,
    MapdlExitedError,
    MapdlFileNotFoundError,
    MapdlInvalidRoutineError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.information import Information  # noqa: F401
from ansys.mapdl.core.inline_functions import Query  # noqa: F401
from ansys.mapdl.core.mapdl_types import MapdlFloat  # noqa: F401
from ansys.mapdl.core.misc import (  # noqa: F401
    check_deprecated_vtk_kwargs,
    check_valid_routine,
    last_created,
    random_string,
    requires_graphics,
    requires_package,
    run_as,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.reader import Archive  # noqa: F401

    from ansys.mapdl.core.component import ComponentManager  # noqa: F401
    from ansys.mapdl.core.mapdl import MapdlBase  # noqa: F401
    from ansys.mapdl.core.mapdl_geometry import Geometry, LegacyGeometry  # noqa: F401
    from ansys.mapdl.core.parameters import Parameters  # noqa: F401
    from ansys.mapdl.core.plugin import ansPlugin  # noqa: F401
    from ansys.mapdl.core.solution import Solution  # noqa: F401
    from ansys.mapdl.core.xpl import ansXpl  # noqa: F401

    if _HAS_DPF:
        from ansys.mapdl.core.reader import DPFResult  # noqa: F401

from ansys.mapdl.core.post import PostProcessing  # noqa: F401

from . import _CoreMixinBase
from .constants import (  # noqa: F401
    _ALLOWED_START_PARM,
    _PERMITTED_ERRORS,
    _TMP_COMP,
    DEBUG_LEVELS,
    ENTITIES_TO_SELECTION_MAPPING,
    GUI_FONT_SIZE,
    INVAL_COMMANDS,
    INVAL_COMMANDS_SILENT,
    LOG_APDL_DEFAULT_FILE_NAME,
    MAX_COMMAND_LENGTH,
    MAX_PARAM_CHARS,
    PLOT_COMMANDS,
    PNG_IS_WRITTEN_TO_FILE,
    SESSION_ID_NAME,
    STATUS,
    VALID_DEVICES,
    VALID_DEVICES_LITERAL,
    VALID_FILE_TYPE_FOR_PLOT,
    VALID_FILE_TYPE_FOR_PLOT_LITERAL,
    VALID_SELECTION_ENTITY_TP,
    VALID_SELECTION_TYPE_TP,
    VWRITE_MWRITE_REPLACEMENT,
)


class _CoreContextMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

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
        return self._chain_commands(self)

    @property
    def force_output(self):
        """Force text output globally by turning the ``Mapdl.mute`` attribute to False
        and activating text output (``/GOPR``)

        You can still do changes to those inside this context.
        """
        return self._force_output(self)

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
        return self._non_interactive(self)

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
        return self._muted(self)

    def run_as_routine(self, routine):
        """
        Runs a command or commands at a routine and then revert to the prior routine.

        This can be useful to avoid constantly changing between routines.

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
        return self._RetainRoutine(self, routine)

    def _chain_stored(self):
        """Send a series of commands to MAPDL"""
        # there's to be an limit to 640 characters per command, so
        # when chaining commands they must be shorter than 640 (minus
        # some overhead).
        c = 0
        chained_commands = []
        chunk = []
        for command in self._stored_commands:
            len_command = len(command) + 1  # include sep var
            if len_command + c > MAX_COMMAND_LENGTH:
                chained_commands.append("$".join(chunk))
                chunk = [command]
                c = 0
            else:
                chunk.append(command)
                c += len_command

        # join the last
        chained_commands.append("$".join(chunk))
        self._stored_commands = []

        responses = [self._run(command) for command in chained_commands]
        self._response = "\n".join(responses)

    class _non_interactive:
        """Allows user to enter commands that need to run non-interactively."""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)

        def __enter__(self):
            self._parent()._log.debug("Entering in non-interactive mode")
            if self._parent().logger.logger.level <= logging.DEBUG:
                # only commenting if on debug mode
                self._parent().com("Entering in non_interactive mode")
            self._parent()._store_commands = True

        def __exit__(self, *args):
            self._parent()._store_commands = False

            if args[0] is not None:
                # An exception was raised, let's exit now without flushing.
                # Discard whatever was buffered so an incomplete (and
                # potentially invalid, for example a '*DO' missing its
                # '*ENDDO') block cannot leak into a later flush.
                self._parent()._log.debug(
                    "An exception was found in the `non_interactive` environment. "
                    "Hence the commands are not flushed and are discarded."
                )
                self._parent()._stored_commands = []
                return None
            else:
                # No exception so let's flush.
                self._parent()._log.debug("Exiting non-interactive mode")
                self._parent()._flush_stored()

    class _save_selection:
        """Save the selection and returns to it when exiting"""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)
            self.selection = []

        def __enter__(self):
            self._parent()._log.debug("Entering saving selection context")
            mapdl = self._parent()

            # Storing components
            selection = {
                "cmsel": mapdl.components._comp,
            }
            id_ = random_string(5)
            for each_type, each_name in _TMP_COMP.items():
                each_name = f"__{each_name}{id_}__"
                selection[each_type] = each_name
                mapdl.cm(
                    each_name, each_type, mute=True
                )  # to hide ComponentNoData error

            self.selection.append(selection)

        def __exit__(self, *args):
            self._parent()._log.debug("Exiting saving selection context")

            mapdl = self._parent()
            mapdl.allsel()
            mapdl.cmsel("None")

            selection = self.selection.pop()
            cmps = selection.pop("cmsel")

            if cmps:
                for each_name, each_value in cmps.items():
                    mapdl.cmsel("a", each_name, each_value, mute=True)

            for each_type, each_name in selection.items():
                mapdl.cmsel("a", each_name, each_type, mute=True)

                selfun = getattr(
                    mapdl, ENTITIES_TO_SELECTION_MAPPING[each_type.upper()]
                )
                selfun("s", vmin=each_name, mute=True)

                mapdl.cmdele(each_name, mute=True)

    class _chain_commands:
        """Store MAPDL commands and send one chained command."""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)

        def __enter__(self):
            self._parent()._log.debug("Entering chained command mode")
            self._parent()._store_commands = True

        def __exit__(self, *args):
            self._parent()._log.debug("Exiting chained command mode")
            self._parent()._chain_stored()
            self._parent()._store_commands = False

    class _RetainRoutine:
        """Store MAPDL's routine when entering and reverts it when exiting."""

        def __init__(self, parent, routine):
            self._parent = weakref.ref(parent)
            self._requested_routine = routine

        def __enter__(self):
            """Store the current routine and enter the requested routine."""
            self._parent()._cache_routine()
            self._parent()._log.debug(f"Caching routine {self._cached_routine}")

            if (
                self._requested_routine.lower().strip()
                != self._cached_routine.lower().strip()
            ):
                self._parent()._enter_routine(self._requested_routine)

        def __exit__(self, *args):
            """Restore the original routine."""
            self._parent()._log.debug(f"Restoring routine '{self._cached_routine}'")
            self._parent()._resume_routine()

        @property
        def _cached_routine(self):
            return self._parent()._cached_routine

    class _muted:
        def __init__(self, parent):
            self._parent = weakref.ref(parent)
            self.old_value = None

        def __enter__(self):
            self.old_value = self._parent().mute
            self._parent().mute = True

        def __exit__(self, *args):
            self._parent().mute = self.old_value
            self.old_value = None

    def _enter_routine(self, routine):
        # check the routine is valid since we're muting the output
        check_valid_routine(routine)

        if routine.lower() in ["begin level", "finish"]:
            self.finish(mute=True)
        else:
            if not routine.startswith("/"):
                routine = f"/{routine}"

            self.run(f"{routine}", mute=True)

    def _cache_routine(self):
        """Cache the current routine."""
        self._cached_routine = self.parameters.routine

    def _resume_routine(self):
        """Resume the cached routine."""
        if self._cached_routine is not None:
            self._enter_routine(self._cached_routine)
            self._cached_routine = None

    class _force_output:
        """Allows user to enter commands that need to run with forced text output."""

        def __init__(self, parent: "MapdlBase"):
            self._parent: "MapdlBase" = weakref.ref(parent)

        def __enter__(self):
            self._parent()._log.debug("Entering force-output mode")
            if self._parent().wrinqr(1) == 0:  # using wrinqr is more reliable than *get
                self._in_nopr = True
                self._parent()._run("/gopr")  # Going to PR mode
            else:
                self._in_nopr = False

            self._previous_mute, self._parent()._mute = self._parent()._mute, False

        def __exit__(self, *args):
            self._parent()._log.debug("Exiting force-output mode")
            if self._in_nopr:
                self._parent()._run("/nopr")
            self._parent()._mute = self._previous_mute
