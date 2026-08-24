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

"""Constants shared by the CLI commands and their click-independent functions."""

from typing import Tuple

from ansys.mapdl.core.launcher import LOCALHOST as MAPDL_DEFAULT_IP  # noqa: F401
from ansys.mapdl.core.launcher import MAPDL_DEFAULT_PORT  # noqa: F401

DEFAULT_TIMEOUT = 10
"""Seconds to wait when connecting to a running MAPDL instance."""

SUPPORTED_ENVS: Tuple[str, ...] = ("claude", "copilot", "codex", "cursor")
"""AI coding environments a skill can be installed into."""

GLOBAL_UNSUPPORTED: Tuple[str, ...] = ("copilot",)
"""Environments that only support a local, per-project installation."""
