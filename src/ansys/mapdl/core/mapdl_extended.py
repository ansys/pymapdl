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

from functools import wraps  # noqa: F401
import os  # noqa: F401
import pathlib  # noqa: F401
import re  # noqa: F401
import shutil  # noqa: F401
import tempfile  # noqa: F401
from typing import Union  # noqa: F401
import warnings  # noqa: F401
import weakref  # noqa: F401

import numpy as np  # noqa: F401
from numpy.typing import DTypeLike, NDArray  # noqa: F401

from ansys.mapdl.core import LOG as logger  # noqa: F401
from ansys.mapdl.core import parse  # noqa: F401
from ansys.mapdl.core._mapdl_extended.analysis import (
    _ExtendedAnalysisMixin,
)
from ansys.mapdl.core._mapdl_extended.arrays import _ExtendedArrayMixin
from ansys.mapdl.core._mapdl_extended.contexts import (
    _ExtendedContextMixin,
)
from ansys.mapdl.core._mapdl_extended.contexts import MAX_DO_LOOP_LEVEL  # noqa: F401
from ansys.mapdl.core._mapdl_extended.contexts import TMP_VAR  # noqa: F401
from ansys.mapdl.core._mapdl_extended.explicit_commands import (
    _ExtendedExplicitCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.file_commands import (
    _ExtendedFileCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.import_commands import (
    _ExtendedImportCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.parameter_commands import (
    _ExtendedParameterCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.parsed_commands import (
    _ExtendedParsedCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.plotting_commands import (
    _ExtendedPlottingCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.selection_commands import (
    _ExtendedSelectionCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.values import _ExtendedValueMixin
from ansys.mapdl.core.commands import CommandListingOutput, CommandOutput  # noqa: F401
from ansys.mapdl.core.errors import (  # noqa: F401
    CommandDeprecated,
    ComponentDoesNotExits,
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlDoLoopLimitError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_core import _MapdlCore  # noqa: F401
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat  # noqa: F401
from ansys.mapdl.core.misc import (  # noqa: F401
    allow_iterables_vmin,
    allow_pickable_entities,
    check_deprecated_vtk_kwargs,
    random_string,
    requires_graphics,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401


class _MapdlCommandExtended(
    _ExtendedFileCommandsMixin,
    _ExtendedSelectionCommandsMixin,
    _ExtendedPlottingCommandsMixin,
    _ExtendedParameterCommandsMixin,
    _ExtendedExplicitCommandsMixin,
    _ExtendedImportCommandsMixin,
    _ExtendedParsedCommandsMixin,
    _MapdlCore,
):
    """Class that extended MAPDL capabilities by wrapping or overwriting commands"""

    def __init__(self, *args, **kwargs):
        """Initialize the MAPDL command extended class.

        Parameters
        ----------
        *args : list
            Positional arguments to pass to the base class.

        **kwargs : dict
            Keyword arguments to pass to the base class.
        """
        super().__init__(*args, **kwargs)
        self._graphics_backend = GraphicsBackend.PYVISTA
        # Number of currently nested ``*DO``/``*DOWHILE`` loops opened
        # through :meth:`do` or :meth:`dowhile`.
        self._do_loop_level: int = 0

    @wraps(_MapdlCore.nrm)
    def nrm(self, name="", normtype="", parr="", normalize="", **kwargs):
        """Wraps *NRM"""
        if not parr:
            parr = "__temp_par__"
        super().nrm(
            name=name, normtype=normtype, parr=parr, normalize=normalize, **kwargs
        )
        return self.parameters[parr]

    @wraps(_MapdlCore.com)
    def com(self, comment="", **kwargs):
        """Wraps /COM"""
        if self.print_com and not self.mute and not kwargs.get("mute", False):
            print("/COM,%s" % (str(comment)))

        return super().com(comment=comment, **kwargs)

    @wraps(_MapdlCore.lssolve)
    def lssolve(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """Wraps LSSOLVE"""
        with self.non_interactive:
            super().lssolve(lsmin=lsmin, lsmax=lsmax, lsinc=lsinc, **kwargs)
        return self.last_response


class _MapdlExtended(
    _ExtendedArrayMixin,
    _ExtendedAnalysisMixin,
    _ExtendedValueMixin,
    _ExtendedContextMixin,
    _MapdlCommandExtended,
):
    def set_graphics_backend(self, backend: GraphicsBackend):
        """Set the graphics backend to use for plotting."""
        self._graphics_backend = backend
