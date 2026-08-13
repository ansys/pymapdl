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

import gc
from unittest.mock import MagicMock, Mock, patch
import weakref

from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import pytest

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc, MapdlRuntimeError


def _make_mock_mapdl():
    """Return a MagicMock that carries the real instance attributes needed by
    :meth:`MapdlGrpc._close_grpc_channel`.

    Calling ``MapdlGrpc.<method>(mock, ...)`` runs the real method body with
    the mock as ``self``.
    """
    m = MagicMock(spec=MapdlGrpc)
    m._log = MagicMock()
    m._channel = None
    m._connectivity_callback = None
    return m


def test_get_float(mapdl):
    response = pb_types.GetResponse(type=1, dval=123.456)

    with patch.object(mapdl, "_stub", autospec=True) as mock_stub:
        mock_stub.Get.return_value = response
        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == 123.456


def test_get_string(mapdl):
    response = pb_types.GetResponse(type=2, sval="test_string")

    with patch.object(mapdl, "_stub", autospec=True) as mock_stub:
        mock_stub.Get.return_value = response
        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == "test_string"


def test_get_fallback(mapdl):
    response = pb_types.GetResponse(type=0)

    with (
        patch.object(mapdl, "_stub", autospec=True) as mock_stub,
        patch.object(mapdl, "run") as mock_run,
    ):

        mock_run.return_value = "VALUE= 789.012"
        mock_stub.Get.return_value = response

        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == 789.012


def test_get_fallback_string(mapdl):
    response = pb_types.GetResponse(type=0)

    with (
        patch.object(mapdl, "_stub", autospec=True) as mock_stub,
        patch.object(mapdl, "run") as mock_run,
    ):

        mock_run.return_value = "VALUE= test_value"
        mock_stub.Get.return_value = response

        result = mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)
        assert result == "test_value"


def test_get_lock(mapdl):
    mapdl._get_lock = True

    with pytest.raises(MapdlRuntimeError):
        mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1, timeout=0.5)

    mapdl._get_lock = False


def test_get_invalid_response_type(mapdl):
    response = pb_types.GetResponse(type=3)

    with patch.object(mapdl, "_stub", autospec=True) as mock_stub:
        mock_stub.Get.return_value = response

        with pytest.raises(MapdlRuntimeError):
            mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)


def test_get_non_interactive_mode(mapdl):
    mapdl._store_commands = True

    with pytest.raises(MapdlRuntimeError):
        mapdl._get(entity="NODE", entnum="1", item1="U", it1num=1)

    # reset
    mapdl._store_commands = False


class TestCloseGrpcChannel:
    """Tests for MapdlGrpc._close_grpc_channel."""

    def test_closes_channel_and_nulls_reference(self):
        """The channel's close() is called and _channel is set to None."""
        mock = _make_mock_mapdl()
        channel = Mock()
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock)

        channel.close.assert_called_once()
        assert mock._channel is None

    def test_noop_when_channel_is_none(self):
        """No error when _channel is already None."""
        mock = _make_mock_mapdl()
        mock._channel = None

        MapdlGrpc._close_grpc_channel(mock)  # must not raise

    def test_idempotent_second_call(self):
        """Calling twice is safe — second call is a no-op."""
        mock = _make_mock_mapdl()
        channel = Mock()
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock)
        MapdlGrpc._close_grpc_channel(mock)

        channel.close.assert_called_once()

    def test_exception_on_close_is_logged_not_raised(self):
        """An exception from channel.close() is logged, not re-raised."""
        mock = _make_mock_mapdl()
        channel = Mock()
        channel.close.side_effect = RuntimeError("channel already gone")
        mock._channel = channel

        MapdlGrpc._close_grpc_channel(mock)  # must not raise

        mock._log.debug.assert_called()
        assert mock._channel is None

    def test_unsubscribes_callback_before_closing(self):
        """The connectivity callback is removed before the channel is closed."""
        mock = _make_mock_mapdl()
        channel = Mock()
        callback = lambda connectivity: None  # noqa: E731
        mock._channel = channel
        mock._connectivity_callback = callback

        MapdlGrpc._close_grpc_channel(mock)

        channel.unsubscribe.assert_called_once_with(callback)
        channel.close.assert_called_once()
        assert mock._connectivity_callback is None

    def test_unsubscribe_failure_does_not_prevent_close(self):
        """A failing unsubscribe() is logged and close() still runs."""
        mock = _make_mock_mapdl()
        channel = Mock()
        channel.unsubscribe.side_effect = RuntimeError("not subscribed")
        mock._channel = channel
        mock._connectivity_callback = lambda connectivity: None  # noqa: E731

        MapdlGrpc._close_grpc_channel(mock)  # must not raise

        channel.close.assert_called_once()


class TestConnectivityCallbackDoesNotLeakInstance:
    """The gRPC poll thread must not keep the MapdlGrpc instance alive.

    The callback registered by ``_subscribe_to_channel`` is held by gRPC for as
    long as the subscription lasts.  A strong reference to ``self`` there makes
    the instance uncollectable, so ``__del__`` never runs and the channel is
    never closed.
    """

    def test_callback_holds_only_a_weak_reference(self):
        """The instance is garbage-collected even while the callback lives on."""

        class _Dummy:
            """Minimal stand-in exposing what _subscribe_to_channel touches."""

            def __init__(self, channel):
                self._log = MagicMock()
                self._channel = channel
                self._channel_state = None
                self._connectivity_callback = None

            _subscribe_to_channel = MapdlGrpc._subscribe_to_channel

        channel = Mock()
        dummy = _Dummy(channel)
        dummy._subscribe_to_channel()

        # gRPC keeps the callback alive; emulate that.
        callback = channel.subscribe.call_args[0][0]
        ref = weakref.ref(dummy)

        del dummy
        gc.collect()

        assert ref() is None, "the connectivity callback leaked the instance"

        # A callback firing after collection must not raise.
        callback("READY")

    def test_callback_updates_state_while_instance_is_alive(self):
        """The weak reference still forwards updates for a live instance."""

        class _Dummy:
            def __init__(self, channel):
                self._log = MagicMock()
                self._channel = channel
                self._channel_state = None
                self._connectivity_callback = None

            _subscribe_to_channel = MapdlGrpc._subscribe_to_channel

        channel = Mock()
        dummy = _Dummy(channel)
        dummy._subscribe_to_channel()

        callback = channel.subscribe.call_args[0][0]
        callback("READY")

        assert dummy._channel_state == "READY"
        assert dummy._connectivity_callback is callback
