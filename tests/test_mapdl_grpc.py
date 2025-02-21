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

from unittest.mock import MagicMock, patch

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import pytest

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc, MapdlRuntimeError


@pytest.fixture
def mapdl_grpc():
    mapdl = MapdlGrpc()
    mapdl._stub = MagicMock()
    mapdl._log = MagicMock()
    mapdl._get_lock = False
    return mapdl


def test_get_float(mapdl_grpc):
    response = pb_types.GetResponse(type=1, dval=123.456)
    mapdl_grpc._stub.Get.return_value = response

    result = mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)
    assert result == 123.456


def test_get_string(mapdl_grpc):
    response = pb_types.GetResponse(type=2, sval="test_string")
    mapdl_grpc._stub.Get.return_value = response

    result = mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)
    assert result == "test_string"


def test_get_fallback(mapdl_grpc):
    response = pb_types.GetResponse(type=0)
    mapdl_grpc._stub.Get.return_value = response
    mapdl_grpc.run = MagicMock(return_value="VALUE= 789.012")

    result = mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)
    assert result == 789.012


def test_get_fallback_string(mapdl_grpc):
    response = pb_types.GetResponse(type=0)
    mapdl_grpc._stub.Get.return_value = response
    mapdl_grpc.run = MagicMock(return_value="VALUE= test_value")

    result = mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)
    assert result == "test_value"


def test_get_lock(mapdl_grpc):
    mapdl_grpc._get_lock = True

    with patch("time.sleep", return_value=None):
        with pytest.raises(MapdlRuntimeError):
            mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)


def test_get_invalid_response_type(mapdl_grpc):
    response = pb_types.GetResponse(type=3)
    mapdl_grpc._stub.Get.return_value = response

    with pytest.raises(MapdlRuntimeError):
        mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)


def test_get_non_interactive_mode(mapdl_grpc):
    mapdl_grpc._store_commands = True

    with pytest.raises(MapdlRuntimeError):
        mapdl_grpc._get(entity="NODE", entnum="1", item1="U", it1num=1)
