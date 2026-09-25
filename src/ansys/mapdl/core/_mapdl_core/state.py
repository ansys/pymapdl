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

import logging

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from typing import TYPE_CHECKING
from warnings import warn

from ansys.mapdl.core import _HAS_DPF
from ansys.mapdl.core import LOG as logger

if TYPE_CHECKING:  # pragma: no cover
    if _HAS_DPF:
        pass


from . import _CoreMixinBase
from .constants import STATUS


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
            __import__("matplotlib")

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
