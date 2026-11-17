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

"""Liveness checks, in-flight call tracking and control requests."""

from contextlib import contextmanager
from typing import Optional

from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
import grpc
from grpc._channel import _InactiveRpcError, _MultiThreadedRendezvous

from ansys.mapdl.core.errors import (
    MapdlConnectionError,
    protect_grpc,
)

from . import _GrpcMixinBase


class _GrpcHealthMixin(_GrpcMixinBase):
    """Liveness checks, in-flight call tracking and control requests."""

    def _track_call(self, call: grpc.Future) -> None:
        """Record ``call`` as the in-flight gRPC call.

        Parameters
        ----------
        call : grpc.Future
            The gRPC call (or streaming response) to track.
        """
        with self._current_call_lock:
            self._current_call = call

    def _untrack_call(self, call: grpc.Future) -> None:
        """Stop tracking ``call``, unless it was already replaced.

        Only clears ``_current_call`` when it is still ``call``, so a newer
        call tracked by a concurrent invocation is never clobbered by an
        older one finishing later. The check and the clear happen under the
        same lock acquisition so they behave as a single, uninterruptible
        operation instead of two separate ones a second thread could step
        between.

        Parameters
        ----------
        call : grpc.Future
            The gRPC call (or streaming response) to stop tracking.
        """
        with self._current_call_lock:
            if self._current_call is call:
                self._current_call = None

    def _cancel_call_if_pending(self, connectivity: "grpc.ChannelConnectivity") -> None:
        """Cancel the tracked in-flight call if it is still running.

        Called from the channel connectivity callback once the transport is
        confirmed dead, so a call blocked on it does not hang until MAPDL
        eventually answers or the OS notices the broken connection.

        Parameters
        ----------
        connectivity : grpc.ChannelConnectivity
            The connectivity state that triggered the cancellation, used only
            for the debug log message.
        """
        with self._current_call_lock:
            call = self._current_call
        if call is not None and not call.done():
            self._log.debug(
                "Cancelling the in-flight gRPC call: the channel "
                f"became '{connectivity.name}'. MAPDL might have "
                "died or stopped answering."
            )
            call.cancel()

    @contextmanager
    def _watched_call(self, call: grpc.Future):
        """Track ``call`` as the in-flight gRPC call.

        While ``call`` is tracked, the channel connectivity callback (see
        :meth:`_subscribe_to_channel`) cancels it as soon as the channel is
        confirmed dead (``TRANSIENT_FAILURE`` or ``SHUTDOWN``), instead of
        letting it block until MAPDL eventually answers or the OS notices the
        broken connection. This does not bound how long ``call`` may run while
        the channel stays healthy, so long-running commands such as ``SOLVE``
        are unaffected.

        Parameters
        ----------
        call : grpc.Future
            The in-flight gRPC call (or streaming response) to track. Must
            support ``cancel()`` and ``done()``.

        Yields
        ------
        grpc.Future
            The same ``call`` passed in, for convenience.
        """
        self._track_call(call)
        try:
            yield call
        finally:
            self._untrack_call(call)

    @property
    def channel_state(self) -> str:
        """Returns the gRPC channel state.

        Notes
        -----
        The possible values are:

        - 0 - 'IDLE'
        - 1 - 'CONNECTING'
        - 2 - 'READY'
        - 3 - 'TRANSIENT_FAILURE'
        - 4 - 'SHUTDOWN'

        Returns
        -------
        str
            The current state of the gRPC channel as a string.
        """
        return self._channel_state.name

    def wait_until_healthy(self, timeout: float = 30.0) -> None:
        """Wait for the gRPC channel to become healthy.

        This method waits for the channel to reach the 'READY' state,
        indicating that the connection is healthy and ready for use.
        It supports configurable timeout and handles different transport modes.

        Parameters
        ----------
        timeout : float, optional
            Maximum time in seconds to wait for the channel to become healthy.
            Default is 30.0 seconds.

        Raises
        ------
        MapdlConnectionError
            If the channel does not become healthy within the specified timeout.

        Examples
        --------
        >>> mapdl.wait_until_healthy(timeout=10.0)
        """
        import concurrent.futures

        # Use the public API to wait for channel readiness.
        state_future = grpc.channel_ready_future(self._channel)
        try:
            state_future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            current_state = self.channel_state
            raise MapdlConnectionError(
                f"Channel did not become healthy within {timeout} seconds. "
                f"Current state: {current_state}"
            )

        self._log.debug("Channel is healthy and ready for use.")

    @property
    def is_alive(self) -> bool:
        """True when there is an active connect to the gRPC server.

        Returns
        -------
        bool
            True if the MAPDL instance is alive, False otherwise.
        """
        if self.channel_state not in ["IDLE", "READY", None]:
            self._log.debug(
                "MAPDL instance is not alive because the channel is not 'IDLE' o 'READY'."
            )
            return False

        if self._exited:
            self._log.debug("MAPDL instance is not alive because it is exited.")
            return False

        if self.busy:
            self._log.debug("MAPDL instance is alive because it is busy.")
            return True

        if self._exiting:
            # It should be exiting so we should not issue gRPC calls
            self._log.debug("MAPDL instance is expected to be exiting")
            return False

        if self._stub is None:
            self._log.debug("MAPDL instance is not alive because it is not connected.")
            return False

        try:
            # Not '_ctrl': 'protect_grpc' calls 'is_alive' while retrying, so a
            # retried probe would recurse until 'RecursionError'.
            check = bool(self._ctrl_raw("VERSION"))
            if check:
                self._log.debug(
                    "MAPDL instance is alive because version was retrieved."
                )
            else:
                self._log.debug(
                    "MAPDL instance is not alive because version was not retrieved. Maybe output is muted?."
                )
            return check

        except grpc.RpcError as error:
            if self._exited:
                return False
            # MAPDL on v25.2 can answer 'Ctrl' with UNIMPLEMENTED on a new channel -> so a failed version check isn't proof that MAPDL is not alive.
            if error.code() == grpc.StatusCode.UNIMPLEMENTED:
                try:
                    self._connected_stub.SendCommand(
                        pb_types.CmdRequest(command="/COM"), timeout=1.0
                    )
                except Exception as cmd_error:
                    self._log.debug(
                        f"MAPDL instance is not alive because '/COM' also failed with:\n{cmd_error}"
                    )
                    return False
                self._log.debug(
                    "MAPDL instance is alive because '/COM' succeeded after 'Ctrl' returned UNIMPLEMENTED."
                )
                return True
            self._log.debug(
                f"MAPDL instance is not alive because retrieving version failed with:\n{error}"
            )
            return False
        except Exception as error:
            if self._exited:
                return False
            self._log.debug(
                f"MAPDL instance is not alive because retrieving version failed with:\n{error}"
            )
            return False

    @protect_grpc
    def _ctrl(
        self, cmd: str, opt1: str = "", timeout: Optional[float] = 1.0
    ):  # numpydoc ignore=RT01
        """Issue control command to the MAPDL server, with gRPC error handling.

        See :meth:`_ctrl_raw` for the available commands.

        Parameters
        ----------
        cmd : str
            Control command to send.
        opt1 : str, optional
            Option accompanying ``cmd``. The default is ``""``.
        timeout : float, optional
            Maximum time in seconds to wait for the server to respond.
            The default is ``1.0``. Use ``None`` to wait indefinitely.

        Returns
        -------
        str or None
            The server response, if any.
        """
        return self._ctrl_raw(cmd, opt1, timeout)

    def _ctrl_raw(
        self, cmd: str, opt1: str = "", timeout: Optional[float] = 1.0
    ):  # numpydoc ignore=RT01
        """Issue control command to the MAPDL server, without retries.

        Unlike :meth:`_ctrl`, gRPC errors are raised as is and MAPDL is never
        marked as exited, so this is safe to call from ``is_alive``.

        Available commands:

        - ``EXIT``
            Calls exit(0) on the server.

        - ``set_verb``
            Enables verbose mode on the server.
            In this case, the verbosity level is set using ``opt1`` argument.

        - ``VERSION``
            Returns version string in of the server in the form
            "MAJOR.MINOR.PATCH".  E.g. "0.3.0".  Known versions
            include:

            2020R2 - "0.3.0"
            2021R1 - "0.3.0"
            2021R2 - "0.4.0"

        Unavailable/Flaky:

        - ``time_stats``
            Prints a table for time stats on the server.
            This command appears to be disabled/broken.

        - ``mem-stats``
            To be added

        Parameters
        ----------
        cmd : str
            Control command to send. See the commands documented above.
        opt1 : str, optional
            Option accompanying ``cmd``. The default is ``""``.
        timeout : float, optional
            Maximum time in seconds to wait for the server to respond before
            raising a gRPC deadline-exceeded error. The default is ``1.0``.
            Use ``None`` to wait indefinitely. Bounding this call prevents an
            unresponsive or already-dead server (for example, one whose
            process was just killed during teardown) from hanging the caller
            forever, since the underlying gRPC channel does not detect a
            severed local connection on its own.

        Returns
        -------
        str or None
            The server response, if any.
        """
        self._log.debug(f'Issuing CtrlRequest "{cmd}" with option "{opt1}".')
        request = anskernel.CtrlRequest(ctrl=str(cmd), opt1=str(opt1))

        # handle socket closing upon exit
        if cmd.lower() == "exit":
            try:
                # this always returns an error as the connection is closed
                self._connected_stub.Ctrl(request, timeout=timeout)
            except (_InactiveRpcError, _MultiThreadedRendezvous):
                pass
            return

        resp = self._connected_stub.Ctrl(request, timeout=timeout)

        if hasattr(resp, "response"):
            return resp.response
