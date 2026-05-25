# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#

"""Launcher tests package."""

from pathlib import Path
import sys

# Add the parent directory to sys.path for imports
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from conftest import ON_LOCAL
