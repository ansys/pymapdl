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

"""Shared offline test double for Mechanical APDL 2026 R1 command wrappers."""

import importlib.util
import logging
from pathlib import Path
import sys
from unittest.mock import MagicMock

import pytest

from ansys.mapdl.core.mapdl_extended import _MapdlExtended

# Re-export root tests/conftest.py symbols so default pytest prepend import mode
# resolves ``from conftest import ...`` without re-executing root conftest.py.
_ROOT_CONFTEST = (Path(__file__).resolve().parent.parent / "conftest.py").resolve()
_mod = next(
    (
        m
        for m in list(sys.modules.values())
        if getattr(m, "__file__", None) and Path(m.__file__).resolve() == _ROOT_CONFTEST
    ),
    None,
)
if _mod is None:
    _spec = importlib.util.spec_from_file_location(
        "root_tests_conftest", _ROOT_CONFTEST
    )
    assert _spec is not None and _spec.loader is not None
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules["root_tests_conftest"] = _mod
    _spec.loader.exec_module(_mod)

NullContext = _mod.NullContext
TestClass = _mod.TestClass
has_dependency = _mod.has_dependency
requires = _mod.requires
ON_LOCAL = _mod.ON_LOCAL


class FakeMapdl(_MapdlExtended):
    """Lightweight offline ``Mapdl`` double inheriting the full command MRO.

    Bypasses ``_MapdlCore.__init__`` (no live or gRPC connection required) and
    records every ``(command, kwargs)`` pair passed to ``run()``.
    """

    def __init__(self) -> None:
        self._do_loop_level = 0
        self._store_commands = False
        self._stored_commands: list[str] = []
        self.sent_commands: list[str] = []
        self.calls: list[tuple[str, dict]] = []
        self._log = MagicMock()
        self._log.logger.level = logging.WARNING

    def run(self, command: str, **kwargs):
        if self._store_commands:
            self._stored_commands.append(command)
            return None
        self.sent_commands.append(command)
        self.calls.append((command, kwargs))
        return f"OUT:{command}"


@pytest.fixture
def fake_mapdl() -> FakeMapdl:
    """Return a fresh offline ``FakeMapdl`` instance."""
    return FakeMapdl()
