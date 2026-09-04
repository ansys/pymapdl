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

"""Unit tests for the ``get_default_ansys*`` backward-compatibility helpers."""

from unittest.mock import Mock, patch

from ansys.mapdl.core.launcher import (
    get_default_ansys,
    get_default_ansys_path,
    get_default_ansys_version,
)


def test_get_default_ansys():
    with patch("ansys.tools.common.path.find_mapdl") as mock_find_mapdl:
        mock_find_mapdl.return_value = ("/usr/ansys_inc/v211/ansys/bin/ansys211", 21.1)
        assert get_default_ansys() == ("/usr/ansys_inc/v211/ansys/bin/ansys211", 21.1)
        mock_find_mapdl.assert_called_once()


def test_get_default_ansys_path():
    with patch(
        "ansys.mapdl.core.launcher.get_default_ansys",
        Mock(return_value=("/usr/ansys_inc/v211/ansys/bin/ansys211", 21.1)),
    ):
        assert get_default_ansys_path() == "/usr/ansys_inc/v211/ansys/bin/ansys211"


def test_get_default_ansys_version():
    with patch(
        "ansys.mapdl.core.launcher.get_default_ansys",
        Mock(return_value=("/usr/ansys_inc/v211/ansys/bin/ansys211", 21.1)),
    ):
        assert get_default_ansys_version() == 21.1
