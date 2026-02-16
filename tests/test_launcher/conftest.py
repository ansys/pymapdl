# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Conftest for launcher tests.

This module provides test configuration specific to launcher tests.
Launcher tests don't need a running MAPDL instance, so we disable
the global autouse fixture that launches MAPDL.
"""

import pytest

from ansys.mapdl.core.helpers import is_installed as has_dependency


@pytest.fixture(autouse=False)
def run_before_and_after_tests(request: pytest.FixtureRequest):
    """Override the global autouse fixture to disable MAPDL launching for launcher tests."""
    yield


def requires_dependency(dependency: str):
    """Skip a test if a dependency is not installed."""
    if not has_dependency(dependency):
        return pytest.mark.skip(reason=f"{dependency} not installed")
    return lambda x: x


def requires(requirement: str):
    """Check requirements and return appropriate skip marker or function wrapper."""
    requirement = requirement.lower()
    if "ansys-tools-common" == requirement:
        return requires_dependency("ansys-tools-common")
    else:
        return requires_dependency(requirement)
