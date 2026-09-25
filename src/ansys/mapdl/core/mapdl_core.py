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

"""Module to control interaction with MAPDL through Python"""

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
    from ansys.mapdl.core.mapdl_geometry import (  # noqa: F401
        Geometry,
        LegacyGeometry,
    )
    from ansys.mapdl.core.parameters import Parameters  # noqa: F401
    from ansys.mapdl.core.plugin import ansPlugin  # noqa: F401
    from ansys.mapdl.core.solution import Solution  # noqa: F401
    from ansys.mapdl.core.xpl import ansXpl  # noqa: F401

    if _HAS_DPF:
        from ansys.mapdl.core.reader import DPFResult  # noqa: F401

from ansys.mapdl.core._mapdl_core.constants import (  # noqa: F401
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
from ansys.mapdl.core._mapdl_core.contexts import _CoreContextMixin
from ansys.mapdl.core._mapdl_core.execution import (
    _CoreExecutionMixin,
)
from ansys.mapdl.core._mapdl_core.execution import parse_to_short_cmd  # noqa: F401
from ansys.mapdl.core._mapdl_core.execution import setup_logger  # noqa: F401
from ansys.mapdl.core._mapdl_core.files import _CoreFileMixin
from ansys.mapdl.core._mapdl_core.plotting import _CorePlottingMixin
from ansys.mapdl.core._mapdl_core.selection import _CoreSelectionMixin
from ansys.mapdl.core._mapdl_core.services import _CoreServicesMixin
from ansys.mapdl.core._mapdl_core.state import _CoreStateMixin
from ansys.mapdl.core.post import PostProcessing  # noqa: F401


def _sanitize_start_parm(start_parm):
    for each_key in start_parm:
        if each_key not in _ALLOWED_START_PARM:
            raise ValueError(f"The argument '{each_key}' is not recognaised.")


class _MapdlCore(
    _CoreStateMixin,
    _CoreServicesMixin,
    _CoreContextMixin,
    _CoreFileMixin,
    _CorePlottingMixin,
    _CoreSelectionMixin,
    _CoreExecutionMixin,
    Commands,
):
    """Contains methods in common between all Mapdl subclasses"""

    @check_deprecated_vtk_kwargs
    def __init__(
        self,
        loglevel: DEBUG_LEVELS = "DEBUG",
        graphics_backend: Optional[GraphicsBackend] = None,
        log_apdl: Optional[str] = None,
        log_file: Union[bool, str] = False,
        local: bool = True,
        print_com: bool = False,
        file_type_for_plots: VALID_FILE_TYPE_FOR_PLOT_LITERAL = "PNG",
        **start_parm: dict[str, Any],
    ):
        """Initialize connection with MAPDL."""
        self._show_matplotlib_figures = True  # for testing
        self._query = None
        self.__exited: bool = False
        self._ignore_errors: bool = False
        self._apdl_log: Optional[TextIO] = None
        self._store_commands: bool = False
        self._stored_commands: list[str] = []
        self._response = None
        self._mode = start_parm.get("mode", None)
        self._mapdl_process = None
        self._launched: bool = start_parm.get("launched", False)  # type: ignore[assignment]
        self._stderr = None
        self._archive_cache = None  # type: ignore[var-annotated]
        self._remove_tmp: bool = False
        self._stdout = None
        self._file_type_for_plots = file_type_for_plots
        self._default_file_type_for_plots: VALID_FILE_TYPE_FOR_PLOT_LITERAL = (
            file_type_for_plots
        )
        self._version = None  # cached version
        self._mute = False
        self._save_selection_obj = None
        self._use_reader_backend: bool = start_parm.pop("use_reader_backend", True)  # type: ignore[assignment]

        if _HAS_VISUALIZER:
            if graphics_backend is not None:  # pragma: no cover
                self._graphics_backend = graphics_backend
            else:
                self._graphics_backend = GraphicsBackend.PYVISTA
        else:  # pragma: no cover
            if graphics_backend:
                raise ModuleNotFoundError(
                    "Graphic libraries are required to use this class.\n"
                    "You can install this using `pip install ansys-mapdl-core[graphics]`."
                )

        self._log_filehandler = None
        self._local: bool = local
        self._cleanup: bool = True
        self._vget_arr_counter = 0
        self._cached_routine = None
        self._geometry = None
        self.legacy_geometry: bool = False
        self._math = None
        self._krylov = None
        self._on_docker = None
        self._platform = None
        self._print_com: bool = print_com  # print the command /COM input.

        # Start_parameters
        _sanitize_start_parm(start_parm)
        self._start_parm: Dict[str, Any] = start_parm
        self._jobname: str = start_parm.get("jobname", "file")  # type: ignore[assignment]
        self._path: str | pathlib.PurePath | None = (
            None  # start_parm.get("run_location", None)
        )
        self._check_parameter_names: bool = start_parm.get(
            "check_parameter_names", True
        )  # type: ignore[assignment]

        # Setting up loggers
        self._log: logger = logger.add_instance_logger(
            self.name, self, level=loglevel
        )  # instance logger
        # adding a file handler to the logger
        if log_file:
            if not isinstance(log_file, str):
                log_file = "instance.log"
            self._log.log_to_file(filename=log_file, level=loglevel)

        self._log.debug("Logging set to %s", loglevel)

        # Modules
        from ansys.mapdl.core.parameters import Parameters

        self._parameters: Parameters = Parameters(self)

        from ansys.mapdl.core.solution import Solution

        self._solution: Solution = Solution(self)

        self._xpl: Optional[ansXpl] = None  # Initialized in mapdl_grpc

        self._plugin: Optional[ansPlugin] = None  # Initialized in mapdl_grpc

        from ansys.mapdl.core.component import ComponentManager

        self._componentmanager: ComponentManager = ComponentManager(self)

        if isinstance(log_apdl, bool) and log_apdl:
            log_apdl = LOG_APDL_DEFAULT_FILE_NAME

        if log_apdl:
            self.open_apdl_log(log_apdl, mode="w")

        # Empty object that will store the `PostProcessing` object
        self._post_object = None

        # Wrapping listing functions for "to_array" methods
        self._wrap_listing_functions()

        # Wrapping XSEL commands to return ids.
        self._xsel_mapdl_output = False
        self._wrap_xsel_commands()

        self._info = Information(self)

        # DPF
        self._dpf_result: "DPFResult | None" = None
