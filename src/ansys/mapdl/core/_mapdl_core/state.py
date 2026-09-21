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


"""The state MAPDL core responsibility mixin."""

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


class _CoreStateMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

    def _after_run(self, _command: str) -> None:
        pass

    @property
    def allow_ignore(self):
        """Invalid commands will be ignored rather than exceptions

        A command executed in the wrong processor will raise an
        exception when ``allow_ignore=False``.  This is the default
        behavior.

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.k(1, 0, 0, 0)
        Exception:  K is not a recognized POST1 command, abbreviation, or macro.

        Ignore these messages by setting allow_ignore=True

        >>> mapdl.allow_ignore = True
        2020-06-08 21:39:58,094 [INFO] : K is not a
        recognized POST1 command, abbreviation, or macro.  This
        command will be ignored.

        *** WARNING *** CP = 0.372 TIME= 21:39:58
        K is not a recognized POST1 command, abbreviation, or macro.
        This command will be ignored.
        """
        warn(
            "'allow_ignore' is being deprecated and will be removed in a future release. "
            "Use ``mapdl.ignore_errors`` instead.",
            DeprecationWarning,
        )
        return self._ignore_errors

    @allow_ignore.setter
    def allow_ignore(self, value):
        """Set allow ignore"""
        warn(
            "'allow_ignore' is being deprecated and will be removed in a future release. "
            "Use ``mapdl.ignore_errors`` instead.",
            DeprecationWarning,
        )
        self._ignore_errors = bool(value)

    def _before_run(self, _command: str) -> None:
        pass

    @property
    def check_status(self) -> STATUS:
        """Return MAPDL status.
        * 'exited' if MAPDL is exited
        * 'exiting' if MAPDL is exiting
        * Otherwise returns 'running'.
        """
        if self.exited:
            return STATUS.EXITED
        elif self.exiting:
            return STATUS.EXITING
        else:
            return STATUS.RUNNING

    @property
    def connection(self):
        """Return the type of connection to the instance, namely: grpc, corba or console."""
        return self._mode

    @property
    def exited(self):
        """Return true if the MAPDL session exited"""
        return self._exited

    @property
    def _exited(self):
        return self._MapdlCore__exited

    @_exited.setter
    def _exited(self, value):
        self._MapdlCore__exited = value

    @property
    def ignore_errors(self) -> bool:
        """Invalid commands will be ignored rather than exceptions

        Normally, any string containing "*** ERROR ***" from MAPDL
        will trigger a ``MapdlRuntimeError``.  Set this to ``True`` to
        ignore these errors.

        For example, a command executed in the wrong processor will
        raise an exception when ``ignore_errors=False``.
        This is the default behavior.

        Examples
        --------
        >>> mapdl.post1()
        >>> mapdl.k(1, 0, 0, 0)
        Exception:  K is not a recognized POST1 command, abbreviation, or macro.

        Ignore these messages by setting ignore_errors=True

        >>> mapdl.ignore_errors = True
        2020-06-08 21:39:58,094 [INFO] : K is not a
        recognized POST1 command, abbreviation, or macro.  This
        command will be ignored.

        *** WARNING *** CP = 0.372 TIME= 21:39:58
        K is not a recognized POST1 command, abbreviation, or macro.
        This command will be ignored.
        """
        return self._ignore_errors

    @ignore_errors.setter
    def ignore_errors(self, value):
        self._ignore_errors = bool(value)

    @property
    def is_console(self):
        """Return true if using console to connect to the MAPDL instance."""
        return self._mode == "console"

    @property
    def is_corba(self):
        """Return true if using corba to connect to the MAPDL instance."""
        return self._mode == "corba"

    @property
    def is_grpc(self):
        """Return true if using grpc to connect to the MAPDL instance."""
        return self._mode == "grpc"

    @property
    def is_local(self):
        """Check if the instance is running locally or remotely."""
        return self._local

    @property
    def jobname(self) -> str:
        """
        MAPDL job name.

        This is requested from the active mapdl instance.
        """
        try:
            self._jobname = self.inquire("", "JOBNAME")
        except Exception as e:
            logger.warning(f"Failed to get the jobname due to the following error: {e}")
        return self._jobname

    @jobname.setter
    def jobname(self, new_jobname: str):
        """Set the jobname"""
        self.finish(mute=True)
        self.filname(new_jobname)
        self._jobname = new_jobname

    @property
    def on_docker(self):
        """Check if MAPDL is running on docker."""
        if self._on_docker is None:
            self._on_docker = self._check_on_docker()
        return self._on_docker

    @property
    def last_response(self):
        """Returns the last response from MAPDL.

        Examples
        --------
        >>> mapdl.last_response
        'KEYPOINT      1   X,Y,Z=   1.00000       1.00000       1.00000'
        """
        return self._response

    @property
    def launched(self):
        """Check if the MAPDL instance has been launched by PyMAPDL."""
        return self._launched

    @property
    def check_parameter_names(self):
        """Whether check if the name which is given to the parameter is allowed or not"""
        return self._check_parameter_names

    @check_parameter_names.setter
    def check_parameter_names(self, value: bool):
        """Whether check if the name which is given to the parameter is allowed or not"""
        self._check_parameter_names = value

    @property
    def logger(self) -> logging.Logger:
        """MAPDL Python-based logger"""
        return self._log

    @property
    def name(self) -> str:
        raise NotImplementedError("Implemented by child classes.")

    @name.setter
    def name(self, name) -> None:
        raise AttributeError("The name of an instance cannot be changed.")

    @property
    def platform(self):
        """Return the platform where MAPDL is running."""
        if self._platform is None:
            self._check_mapdl_os()
        return self._platform

    @property
    def print_com(self):
        """Whether to print or not to the console the
        :meth:`mapdl.com ("/COM") <ansys.mapdl.core.Mapdl.com>` calls.
        """
        return self._print_com

    @print_com.setter
    def print_com(self, value):
        if isinstance(value, bool):
            status = "activated" if value else "deactivated"
            self._log.debug(f"The print of '/COM' commands has been {status}.")
            self._print_com = value
        else:
            raise ValueError(
                f"The property ``print_com`` only allows booleans, but type {type(value)} was supplied."
            )

    @property
    def version(self) -> float:
        """
        MAPDL build version.

        Examples
        --------
        >>> mapdl.version
        20.2
        """
        if not self._version:  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
            self._version = self.parameters.revision
        return self._version

    @property
    def _distributed(self):
        """MAPDL is running in distributed mode."""
        return "-smp" not in self._start_parm.get("additional_switches", "")

    @property
    def _has_matplotlib(self):
        try:
            import matplotlib  # noqa: F401

            return True
        except ModuleNotFoundError:
            return False

    @property
    def _lockfile(self):
        """Lockfile path"""
        path = self.directory
        if path is not None:
            return path / f"{self.jobname}.lock"

    @property
    def _png_mode(self):
        """Returns True when MAPDL is set to write plots as png to file."""
        with self.force_output:
            return "PNG" in self.show(mute=False)
