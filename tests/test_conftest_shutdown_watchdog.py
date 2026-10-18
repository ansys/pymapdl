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
"""Tests for the ``pytest_unconfigure`` shutdown watchdog in ``conftest.py``.

The watchdog must stay opt-in: ``pytest_unconfigure`` also runs whenever a
plain, in-process ``pytest.main()`` call returns, which is not interpreter
shutdown, so arming it unconditionally would eventually ``_exit()`` an
otherwise healthy, still-running caller.
"""

import os
from unittest.mock import MagicMock, patch

import conftest


class TestShutdownWatchdogOptIn:
    def test_does_not_arm_when_env_var_is_unset(self):
        """Without an explicit 'PYMAPDL_SHUTDOWN_TIMEOUT', the watchdog must
        not be armed, since 'pytest_unconfigure' also fires after a plain,
        in-process 'pytest.main()' call that is not interpreter shutdown."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PYMAPDL_SHUTDOWN_TIMEOUT", None)
            with patch.object(
                conftest.faulthandler, "dump_traceback_later"
            ) as mock_arm:
                conftest.pytest_unconfigure(MagicMock())

        mock_arm.assert_not_called()

    def test_does_not_arm_when_env_var_is_zero(self):
        with patch.dict(os.environ, {"PYMAPDL_SHUTDOWN_TIMEOUT": "0"}):
            with patch.object(
                conftest.faulthandler, "dump_traceback_later"
            ) as mock_arm:
                conftest.pytest_unconfigure(MagicMock())

        mock_arm.assert_not_called()

    def test_arms_with_explicit_positive_timeout(self):
        """CI workflows set 'PYMAPDL_SHUTDOWN_TIMEOUT' explicitly, so the
        watchdog must still arm in that case."""
        with patch.dict(os.environ, {"PYMAPDL_SHUTDOWN_TIMEOUT": "12"}):
            with (
                patch.object(conftest.faulthandler, "dump_traceback_later") as mock_arm,
                patch.object(conftest.faulthandler, "enable"),
            ):
                conftest.pytest_unconfigure(MagicMock())

        mock_arm.assert_called_once()
        args, kwargs = mock_arm.call_args
        assert args[0] == 12.0
        assert kwargs.get("exit") is True
