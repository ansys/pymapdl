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

"""Compatibility facade composing the MAPDL command and convenience mixins."""

from ansys.mapdl.core._mapdl_extended.analysis import (
    _ExtendedAnalysisMixin,
)
from ansys.mapdl.core._mapdl_extended.apdl.matrix_operations import (
    _ExtendedMatrixCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.apdl.parameter_definition import (
    TMP_VAR,
    _ExtendedParameterCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.arrays import _ExtendedArrayMixin
from ansys.mapdl.core._mapdl_extended.aux15.iges import (
    _ExtendedImportCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.contexts import _ExtendedLoopContextMixin
from ansys.mapdl.core._mapdl_extended.database.components import _ExtendedComponentMixin
from ansys.mapdl.core._mapdl_extended.database.selecting import (
    _ExtendedSelectionCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.database.set_up import _ExtendedDatabaseSetupMixin
from ansys.mapdl.core._mapdl_extended.parsed_commands import (
    _ExtendedParsedCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.plotting_commands import (
    _ExtendedPlottingCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.post1.set_up import _ExtendedPostSetupMixin
from ansys.mapdl.core._mapdl_extended.prep7.explicit_dynamics import (
    _ExtendedExplicitCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.session.files import (
    _ExtendedFileCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.session.list_controls import (
    _ExtendedListControlsMixin,
)
from ansys.mapdl.core._mapdl_extended.solution.load_step_operations import (
    _ExtendedLoadStepCommandsMixin,
)
from ansys.mapdl.core._mapdl_extended.values import _ExtendedValueMixin
from ansys.mapdl.core.commands import CommandListingOutput, CommandOutput
from ansys.mapdl.core.contexts.loops import (
    MAX_DO_LOOP_LEVEL,
    _DoLoopContext,
)
from ansys.mapdl.core.errors import (
    CommandDeprecated,
    ComponentDoesNotExits,
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlDoLoopLimitError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.lazy_array import LazyArray
from ansys.mapdl.core.mapdl_core import _MapdlCore
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat
from ansys.mapdl.core.misc import (
    allow_iterables_vmin,
    allow_pickable_entities,
    check_deprecated_vtk_kwargs,
    requires_graphics,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend

# Names re-exported for backward compatibility with code that imported them
# from this module before the responsibility split.
__all__ = [
    "_MapdlCommandExtended",
    "_MapdlExtended",
    "_MapdlCore",
    "_DoLoopContext",
    "MAX_DO_LOOP_LEVEL",
    "TMP_VAR",
    "CommandDeprecated",
    "CommandListingOutput",
    "CommandOutput",
    "ComponentDoesNotExits",
    "GraphicsBackend",
    "IncorrectWorkingDirectory",
    "KwargDict",
    "LazyArray",
    "MapdlCommandIgnoredError",
    "MapdlDoLoopLimitError",
    "MapdlFloat",
    "MapdlRuntimeError",
    "allow_iterables_vmin",
    "allow_pickable_entities",
    "check_deprecated_vtk_kwargs",
    "requires_graphics",
    "supress_logging",
]


class _MapdlCommandExtended(
    _ExtendedFileCommandsMixin,
    _ExtendedSelectionCommandsMixin,
    _ExtendedPostSetupMixin,
    _ExtendedDatabaseSetupMixin,
    _ExtendedComponentMixin,
    _ExtendedPlottingCommandsMixin,
    _ExtendedParameterCommandsMixin,
    _ExtendedExplicitCommandsMixin,
    _ExtendedImportCommandsMixin,
    _ExtendedParsedCommandsMixin,
    _ExtendedMatrixCommandsMixin,
    _ExtendedListControlsMixin,
    _ExtendedLoadStepCommandsMixin,
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


class _MapdlExtended(
    _ExtendedArrayMixin,
    _ExtendedAnalysisMixin,
    _ExtendedValueMixin,
    _ExtendedLoopContextMixin,
    _MapdlCommandExtended,
):
    """Compose MAPDL command overrides and Python convenience methods."""
