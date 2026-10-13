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

"""Logging responsibilities for the MAPDL core facade."""

import logging
from pathlib import Path
from typing import Literal, Union

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import LOG as logger
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import run_as, supress_logging

from . import _CoreMixinBase

DEBUG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_APDL_DEFAULT_FILE_NAME = "apdl.log"


def setup_logger(loglevel="INFO", log_file=True, mapdl_instance=None):
    """Return the shared logger configured for a MAPDL instance."""
    if hasattr(setup_logger, "log"):
        return setup_logger.log
    setup_logger.log = logger.add_instance_logger("MAPDL", mapdl_instance)
    return setup_logger.log


class _CoreLoggingMixin(_CoreMixinBase):
    """Static responsibility mixin for MAPDL logging APIs."""

    @property
    def logger(self) -> logging.Logger:
        """MAPDL Python-based logger."""
        return self._log

    def set_log_level(self, loglevel: DEBUG_LEVELS) -> None:
        """Set the MAPDL Python logger level."""
        if isinstance(loglevel, str):
            loglevel = loglevel.upper()  # type: ignore[assignment]
        setup_logger(loglevel=loglevel)

    def _set_log_level(self, level):
        """Alias for :meth:`set_log_level`."""
        self.set_log_level(level)

    def open_apdl_log(
        self,
        filename: Union[str, Path],
        mode: Literal["w", "a", "x"] = "w",
    ) -> None:
        """Start writing APDL commands to an input file."""
        if self._apdl_log is not None:
            raise MapdlRuntimeError("APDL command logging already enabled")
        self._log.debug("Opening ANSYS log file at %s", filename)
        if mode not in ["w", "a", "x"]:
            raise ValueError(
                "File mode should either be write, append, or exclusive"
                " creation ('w', 'a', or 'x')."
            )
        self._apdl_log = open(filename, mode=mode, buffering=1)
        if self._apdl_log is None:
            raise MapdlRuntimeError("Failed to open APDL log file.")
        self._apdl_log.write(
            f"! APDL log script generated using PyMAPDL (ansys.mapdl.core {pymapdl.__version__})\n"
        )

    def _close_apdl_log(self):
        """Close the APDL log."""
        if self._apdl_log is not None:
            self._apdl_log.close()
        self._apdl_log = None

    def add_file_handler(self, filepath, append=False, level="DEBUG"):
        """Add a file handler to the MAPDL Python logger."""
        mode = "a" if append else "w"
        self._log_filehandler = logging.FileHandler(filepath, mode=mode)
        formatstr = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        self._log_filehandler.setFormatter(logging.Formatter(formatstr))
        if isinstance(level, str):
            level = level.upper()
        self._log_filehandler.setLevel(level)
        self._log.logger.addHandler(self._log_filehandler)
        self._log.info("Added file handler at %s", filepath)

    def remove_file_handler(self):
        """Remove the file handler from the MAPDL Python logger."""
        self._log.removeHandler(self._log_filehandler)
        self._log.info("Removed file handler")

    def _cleanup_loggers(self):
        """Clean up the instance logger and its handlers."""
        log = self._log
        log.setLevel(logging.CRITICAL + 1)
        if log.hasHandlers():
            for handler in log.logger.handlers:
                if handler.stream and not handler.stream.closed:
                    log.logger.removeHandler(handler)
        if log.file_handler:
            log.file_handler.close()
            log.file_handler = None
        if log.std_out_handler:
            log.std_out_handler.close()
            log.std_out_handler = None
