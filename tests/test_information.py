# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

"""Test the information module"""

import inspect

import pytest


def test_mapdl_info(mapdl, cleared, capfd):
    info = mapdl.info
    for attr, value in inspect.getmembers(info):
        if not attr.startswith("_") and attr not in ["title", "stitles"]:
            assert isinstance(value, str)

            with pytest.raises(AttributeError):
                setattr(info, attr, "any_value")

    assert "PyMAPDL" in mapdl.info.__repr__()
    out = info.__str__()

    assert "ansys" in out.lower()
    assert "Product" in out
    assert "MAPDL Version" in out
    assert "UPDATE" in out


def test_info_title(mapdl, cleared):
    title = "this is my title"
    mapdl.info.title = title
    assert title == mapdl.info.title


def test_info_stitle(mapdl, cleared):
    info = mapdl.info

    assert all([not each for each in info.stitles])
    stitles = ["asfd", "qwer", "zxcv", "jkl"]
    info.stitles = "\n".join(stitles)

    assert stitles == info.stitles

    stitles = stitles[::-1]

    info.stitles = stitles
    assert stitles == info.stitles

    info.stitles = None
    assert all([not each for each in info.stitles])
