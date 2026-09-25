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

"""No-MAPDL regression tests for the ``mapdl_core`` and ``mapdl_extended`` facades."""

from inspect import getattr_static, getmembers, isfunction
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from ansys.mapdl.core import commands, mapdl_core, mapdl_extended
from ansys.mapdl.core._mapdl_core import execution as core_execution
from ansys.mapdl.core._mapdl_core.constants import (
    MAX_PARAM_CHARS as PRIVATE_MAX_PARAM_CHARS,
)
from ansys.mapdl.core._mapdl_core.constants import (
    SESSION_ID_NAME as PRIVATE_SESSION_ID_NAME,
)
from ansys.mapdl.core._mapdl_core.constants import STATUS as PRIVATE_STATUS
from ansys.mapdl.core._mapdl_core.constants import _TMP_COMP as PRIVATE_TMP_COMP
from ansys.mapdl.core._mapdl_extended.contexts import (
    MAX_DO_LOOP_LEVEL as PRIVATE_MAX_DO_LOOP_LEVEL,
)
from ansys.mapdl.core._mapdl_extended.contexts import TMP_VAR as PRIVATE_TMP_VAR
from ansys.mapdl.core.errors import CommandDeprecated
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.mapdl_core import (
    _TMP_COMP,
    MAX_PARAM_CHARS,
    SESSION_ID_NAME,
    STATUS,
    _MapdlCore,
    parse_to_short_cmd,
)
from ansys.mapdl.core.mapdl_extended import (
    TMP_VAR,
    _MapdlCommandExtended,
    _MapdlExtended,
)


def test_facade_symbols_and_helpers_are_reexported():
    """The original module-level compatibility surface remains available."""
    assert mapdl_core.MAX_PARAM_CHARS == PRIVATE_MAX_PARAM_CHARS == MAX_PARAM_CHARS
    assert mapdl_core.SESSION_ID_NAME == PRIVATE_SESSION_ID_NAME == SESSION_ID_NAME
    assert mapdl_core.STATUS is PRIVATE_STATUS is STATUS
    assert mapdl_core._TMP_COMP is PRIVATE_TMP_COMP is _TMP_COMP
    assert mapdl_extended.TMP_VAR == PRIVATE_TMP_VAR == TMP_VAR
    assert mapdl_extended.MAX_DO_LOOP_LEVEL == PRIVATE_MAX_DO_LOOP_LEVEL
    assert parse_to_short_cmd is core_execution.parse_to_short_cmd
    assert parse_to_short_cmd("VPLOT,ALL") == "VPLO"


def test_public_class_identity_and_module_paths_are_preserved():
    """The three compatibility classes retain their names and modules."""
    assert _MapdlCore.__name__ == "_MapdlCore"
    assert _MapdlCore.__module__ == "ansys.mapdl.core.mapdl_core"
    assert _MapdlCommandExtended.__name__ == "_MapdlCommandExtended"
    assert _MapdlCommandExtended.__module__ == "ansys.mapdl.core.mapdl_extended"
    assert _MapdlExtended.__name__ == "_MapdlExtended"
    assert _MapdlExtended.__module__ == "ansys.mapdl.core.mapdl_extended"


def test_private_mixins_are_static_and_have_expected_relative_mro():
    """Private mixins appear in the intended hierarchy without exact-MRO coupling."""
    core_mixins = (
        mapdl_core._CoreStateMixin,
        mapdl_core._CoreExecutionMixin,
    )
    extended_mixins = (mapdl_extended._ExtendedContextMixin,)

    core_mro = _MapdlCore.__mro__
    command_mro = _MapdlCommandExtended.__mro__
    extended_mro = _MapdlExtended.__mro__

    assert core_mro.index(_MapdlCore) < core_mro.index(commands.Commands)
    assert command_mro.index(_MapdlCommandExtended) < command_mro.index(_MapdlCore)
    assert extended_mro.index(_MapdlExtended) < extended_mro.index(
        _MapdlCommandExtended
    )
    assert issubclass(MapdlBase, _MapdlExtended)
    assert MapdlBase.__mro__.index(_MapdlExtended) < MapdlBase.__mro__.index(
        _MapdlCommandExtended
    )
    for mixin in core_mixins + extended_mixins:
        assert mixin.__module__.startswith("ansys.mapdl.core._mapdl_")
        assert "__init__" not in mixin.__dict__


def test_lightweight_construction_does_not_start_mapdl():
    """The compatibility classes can be constructed with the core initializer mocked."""
    with patch.object(_MapdlCore, "__init__", return_value=None):
        core = _MapdlCore()
        command_extended = _MapdlCommandExtended()
        extended = _MapdlExtended()

    assert isinstance(core, _MapdlCore)
    assert isinstance(command_extended, _MapdlCommandExtended)
    assert isinstance(extended, _MapdlExtended)
    assert command_extended._do_loop_level == 0
    assert extended._do_loop_level == 0


def test_exited_state_uses_the_core_initializer_backing_attribute():
    """Relocating the accessor preserves the core class's private state name."""
    instance = object.__new__(_MapdlCore)
    instance._MapdlCore__exited = False

    assert instance.exited is False
    instance._exited = True
    assert instance.exited is True


def test_generated_commands_are_available_and_dispatch_at_each_public_level():
    """Generated command descriptors remain inherited through every facade class."""
    for cls in (_MapdlCore, _MapdlCommandExtended, _MapdlExtended):
        assert getattr_static(cls, "allsel") is not None
        assert getattr_static(cls, "finish") is not None

    instance = object.__new__(_MapdlExtended)
    instance.run = Mock(return_value="response")

    assert instance.allsel("ALL") == "response"
    instance.run.assert_called_once_with("ALLSEL,ALL,", **{})


@pytest.mark.parametrize(
    ("name", "mixin", "wraps_core"),
    [
        ("file", mapdl_extended._ExtendedFileCommandsMixin, True),
        ("vsel", mapdl_extended._ExtendedSelectionCommandsMixin, True),
        ("kplot", mapdl_extended._ExtendedPlottingCommandsMixin, False),
        ("dim", mapdl_extended._ExtendedParameterCommandsMixin, True),
        ("edasmp", mapdl_extended._ExtendedExplicitCommandsMixin, True),
        ("catiain", mapdl_extended._ExtendedImportCommandsMixin, True),
        ("a", mapdl_extended._ExtendedParsedCommandsMixin, True),
    ],
)
def test_extended_wrapper_precedence_and_metadata_are_preserved(
    name, mixin, wraps_core
):
    """Extended command wrappers retain their owning mixin and core metadata."""
    extended_method = getattr_static(_MapdlCommandExtended, name)
    core_method = getattr_static(_MapdlCore, name)

    assert extended_method is getattr_static(mixin, name)
    assert extended_method is not core_method
    assert extended_method.__name__ == name
    if wraps_core:
        assert extended_method.__wrapped__ is core_method


def test_parameter_and_explicit_wrappers_preserve_pre_dispatch_validation():
    """Moved wrappers retain validation that occurs before MAPDL dispatch."""
    instance = object.__new__(_MapdlExtended)
    instance._check_parameter_name = Mock()
    instance._version = 19.1

    with pytest.raises(ValueError, match="Parenthesis are not allowed"):
        instance.dim("invalid(")
    instance._check_parameter_name.assert_called_once_with("invalid(")

    with pytest.raises(CommandDeprecated, match="edasmp"):
        instance.edasmp()


def test_extended_value_patch_target_remains_on_public_facade():
    """Patching the historical ``_MapdlExtended.get_value`` target still works."""
    instance = object.__new__(_MapdlExtended)

    with patch(
        "ansys.mapdl.core.mapdl_extended._MapdlExtended.get_value", return_value=42
    ):
        assert instance.get_value("NODE", "1", "LOC", "X") == 42


def test_no_duplicate_public_callables_among_sibling_mixins():
    """Each responsibility mixin owns a public callable name only once."""
    sibling_groups = (
        (
            mapdl_core._CoreStateMixin,
            mapdl_core._CoreServicesMixin,
            mapdl_core._CoreContextMixin,
            mapdl_core._CoreFileMixin,
            mapdl_core._CorePlottingMixin,
            mapdl_core._CoreSelectionMixin,
            mapdl_core._CoreExecutionMixin,
        ),
        (
            mapdl_extended._ExtendedFileCommandsMixin,
            mapdl_extended._ExtendedSelectionCommandsMixin,
            mapdl_extended._ExtendedPlottingCommandsMixin,
            mapdl_extended._ExtendedParameterCommandsMixin,
            mapdl_extended._ExtendedExplicitCommandsMixin,
            mapdl_extended._ExtendedImportCommandsMixin,
            mapdl_extended._ExtendedParsedCommandsMixin,
        ),
        (
            mapdl_extended._ExtendedArrayMixin,
            mapdl_extended._ExtendedAnalysisMixin,
            mapdl_extended._ExtendedValueMixin,
            mapdl_extended._ExtendedContextMixin,
        ),
    )

    for siblings in sibling_groups:
        owners = {}
        for sibling in siblings:
            for name, value in getmembers(sibling, isfunction):
                if not name.startswith("_"):
                    owners.setdefault(name, []).append(sibling.__name__)
        duplicates = {
            name: mixins for name, mixins in owners.items() if len(mixins) > 1
        }
        assert not duplicates


def test_no_obsolete_extended_plotting_module():
    """High-level graphics backend selection remains on the extended facade."""
    plotting_module = (
        Path(mapdl_extended.__file__).parent / "_mapdl_extended" / "plotting.py"
    )
    assert not plotting_module.exists()
    assert "set_graphics_backend" in _MapdlExtended.__dict__
