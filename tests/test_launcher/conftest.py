# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Conftest for launcher tests.

This module provides test configuration specific to launcher tests.
Launcher tests don't need a running MAPDL instance, so we disable
the global autouse fixture that launches MAPDL.
"""

from pathlib import Path
import sys

import pytest

# Add parent tests directory to path to enable imports from parent conftest
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

# Re-export symbols from parent conftest for "from conftest import" statements
# This is necessary because Python's import system will find this conftest first
from conftest import VALID_PORTS, requires  # noqa: F401


@pytest.fixture(autouse=True, scope="function")
def run_before_and_after_tests(request: pytest.FixtureRequest):
    """Override the global autouse fixture to disable MAPDL launching for launcher tests."""
    yield
