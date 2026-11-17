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

"""Channel creation, transport configuration and connection attempts."""

import os
from pathlib import Path
import threading
import time
from typing import Optional
from warnings import warn
import weakref

from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
from ansys.tools.common.versioning import version_string_as_tuple
import grpc

from ansys.mapdl.core.errors import (
    MapdlConnectionError,
    MapdlDidNotStart,
    MapdlRuntimeError,
)

from . import _GrpcMixinBase


class _GrpcConnectionMixin(_GrpcMixinBase):
    """Channel creation, transport configuration and connection attempts."""

    _channel: "grpc.Channel | None"
    _server_version_cache: tuple[int, int, int] | None
    certs_dir: Path | None
    transport_mode: str | None

    def _configure_transport(self, *, ip: str, port: int) -> None:
        """Configure transport-related defaults, validate mode, and resolve UDS conflicts.

        This centralizes duplicated logic from the constructor and can be
        safely called before or after `super().__init__()`; it expects that
        when called after `super().__init__()` the attributes `self._port`
        and `self._log` are available.
        """
        # Determine transport mode if not provided
        if self.transport_mode is None:
            self.transport_mode = os.environ.get(
                "PYMAPDL_GRPC_TRANSPORT"
            ) or os.environ.get("ANSYS_MAPDL_GRPC_TRANSPORT")
            if self.transport_mode is None:
                import platform

                if platform.system() == "Linux":
                    self.transport_mode = "uds"
                elif platform.system() == "Windows":
                    self.transport_mode = "wnua"
                else:
                    warn("Unknown platform, defaulting to 'insecure' transport mode.")
                    self.transport_mode = "insecure"

        # Configure transport-specific settings
        if self.transport_mode == "uds":
            if os.name == "nt":
                raise ValueError("UDS transport mode is not supported on Windows.")
            self.configure_uds(port=port)

        elif self.transport_mode == "wnua":
            if os.name != "nt":
                raise ValueError("WNUA transport mode is only supported on Windows.")
            self.configure_wnua()

        elif self.transport_mode == "insecure":
            self.configure_insecure()

        elif self.transport_mode == "mtls":
            self.configure_mtls()

        # Validate transport mode compatibility using external helper
        try:
            from ansys.tools.common.cyberchannel import verify_transport_mode

            verify_transport_mode(self.transport_mode)
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "ansys.tools.common is required for transport verification. "
                "Install ansys-tools-common or set transport_mode to 'insecure'."
            )

        # Transport compatibility checks for remote IPs. Allow loopback/local
        # addresses (e.g., 127.0.0.1) to use local-only transports.
        self._check_remote(ip)

        if self.transport_mode == "wnua":
            msg = f"Using WNUA transport on {ip}:{self._port}"
        elif self.transport_mode == "uds":
            msg = f"Using UDS transport with socket ID '{self.port}' in directory '{self.uds_dir}'"
        elif self.transport_mode == "mtls":
            msg = f"Using mTLS transport with certificates in '{self.certs_dir}'"
        else:
            msg = f"Using insecure transport on {ip}:{self._port}"

        if hasattr(self, "_log"):
            self._log.info(msg)

    def _check_remote(self, ip: Optional[str]) -> None:
        """Check if the connection is remote and validate transport mode compatibility."""
        is_remote = True
        if ip is None:
            is_remote = False
        else:
            try:
                import ipaddress

                is_remote = not ipaddress.ip_address(str(ip)).is_loopback
            except Exception:
                # If ip cannot be parsed, conservatively treat as not remote
                is_remote = False

        if is_remote and self.transport_mode in ["wnua", "uds"]:
            raise ValueError(
                f"Transport mode '{self.transport_mode}' does not support remote connections. "
                "For remote connections, use 'mtls' or 'insecure' (discouraged)."
            )

    def configure_uds(self, port: int) -> None:
        """Configure UDS transport-specific settings.

        MAPDL derives the socket identifier from the port number automatically,
        naming its socket ``mapdl-{PORT}.sock`` inside the directory set via the
        ``ANSYS_MAPDL_UDS_PATH`` environment variable.
        """
        pass

    def configure_insecure(self) -> None:
        """Configure insecure transport-specific settings."""
        # No specific configuration needed for insecure transport
        pass

    def configure_wnua(self) -> None:
        """Configure WNUA transport-specific settings."""
        # No specific configuration needed for WNUA transport
        pass

    def configure_mtls(self) -> None:
        """Configure mTLS transport-specific settings.

        Resolves the certificates directory (from the configured value, the
        ANSYS_GRPC_CERTIFICATES environment variable, or ./certs). If the
        certs_dir was explicitly provided by the caller, ensure it exists and
        contains the required client certificate files. When certs_dir is None
        we only set the resolved path (env var or ./certs) and do not raise if
        the directory is absent; this matches historical behavior relied on by
        the test-suite and callers that defer validation later.
        """
        # Track whether caller provided certs_dir
        provided = self.certs_dir is not None

        # Resolve certs_dir if not provided
        if not provided:
            self.certs_dir = Path(
                os.environ.get(
                    "ANSYS_GRPC_CERTIFICATES", os.path.join(os.getcwd(), "certs")
                )
            )
        else:
            # Accept string or Path
            # Ensure a str is passed to Path to satisfy type checkers
            self.certs_dir = Path(str(self.certs_dir))

        # If caller provided certs_dir, ensure it exists and is a directory
        if provided and (not self.certs_dir.exists() or not self.certs_dir.is_dir()):
            raise FileNotFoundError(
                f"mTLS certificate directory not found: '{self.certs_dir}'. "
                "Provide a valid certs_dir or set ANSYS_GRPC_CERTIFICATES environment variable."
            )

        # If the directory exists (whether provided or resolved), validate required files
        if self.certs_dir.exists() and self.certs_dir.is_dir():
            required_client_files = ["client.crt", "client.key", "ca.crt"]
            missing = [
                f for f in required_client_files if not (self.certs_dir / f).is_file()
            ]
            if missing:
                raise FileNotFoundError(
                    f"mTLS certificate directory '{self.certs_dir}' is missing files: {missing}. "
                    "Ensure 'client.crt', 'client.key', and 'ca.crt' are present."
                )

    def _ensure_channel(self) -> None:
        """Rebuild the gRPC channel if it has been closed.

        A closed gRPC channel cannot be reopened, so after
        :meth:`_close_grpc_channel` (or :meth:`_disconnect_but_leave_mapdl_running`)
        has run, ``self._channel`` is ``None``. This rebuilds it via
        :meth:`_create_channel` and re-subscribes with
        :meth:`_subscribe_to_channel`, so that :meth:`reconnect_to_mapdl` can
        resume driving the same MAPDL session.

        Raises
        ------
        MapdlRuntimeError
            If the IP address or port of the instance is unknown, since both
            are required to rebuild the channel.

        Returns
        -------
        None
        """
        if self._channel is not None:
            return

        if self._ip is None or self._port is None:
            raise MapdlRuntimeError(
                "Cannot rebuild the gRPC channel: the IP address or port of "
                "this MAPDL instance is unknown."
            )

        self._log.debug("Rebuilding gRPC channel to %s:%s", self._ip, self._port)
        self._channel = self._create_channel(self._ip, self._port)
        self._subscribe_to_channel()

    def _connect_to_mapdl(self, timeout: int):
        """(Re)connect to an existing MAPDL instance"""
        self._ensure_channel()

        try:
            self._multi_connect(timeout=timeout)
        except MapdlConnectionError as err:  # pragma: no cover
            self._post_mortem_checks()
            self._log.debug(
                "The error wasn't caught by the post-mortem checks.\nThe stdout is printed now:"
            )
            self._log.debug(self._stdout)
            raise err  # Raise original error if we couldn't catch it in post-mortem analysis
        else:
            self._log.debug("Connection established")

    def reconnect_to_mapdl(self, timeout: Optional[int] = None):
        """Reconnect to an already instantiated MAPDL instance.

        Re-establish an stopped or crashed gRPC connection with an already alive
        MAPDL instance. This function does not relaunch the MAPDL instance.

        Notes
        -----
        If the gRPC channel was previously closed (for example after
        :meth:`exit` released the client side while leaving MAPDL running),
        the channel is rebuilt and re-subscribed automatically.

        Parameters
        ----------
        timeout : int, optional
            Timeout before raising an exception, by default None
        """

        if timeout is None:
            timeout = self._timeout

        self._connect_to_mapdl(timeout)
        self._exited = False  # Reset the exited state

    def _create_channel(self, ip: str, port: int) -> grpc.Channel:
        """Create a gRPC channel using the specified transport mode.

        Parameters
        ----------
        ip : str
            The IP address of the gRPC server.

        port : int
            The port number of the gRPC server.

        Returns
        -------
        grpc.Channel
            The created gRPC channel.
        """
        from ansys.tools.common.cyberchannel import create_channel

        # open the channel
        channel_str = f"{ip}:{port}"
        self._log.debug(f"Opening channel at {channel_str}")
        return create_channel(
            transport_mode=self.transport_mode,
            host=ip,
            port=port,
            uds_service="mapdl",
            uds_id=port,
            uds_dir=self.uds_dir,
            certs_dir=self.certs_dir,
            grpc_options=self.grpc_options,
        )

    def _subscribe_to_channel(self):
        """Subscribe to channel status and store the value in 'mapdl._channel_state'"""

        # A weak reference is used so that the gRPC ``_poll_connectivity``
        # daemon thread, which keeps the callback alive for as long as the
        # subscription lasts, does not keep this instance alive too.  A strong
        # reference here creates an uncollectable cycle
        # (thread -> state -> callback -> mapdl -> channel -> state) that
        # prevents ``__del__`` from ever running, leaking both the instance and
        # the polling thread.
        self_ref = weakref.ref(self)

        # States in which the transport is confirmed unusable: a call blocked
        # on a connection that has reached one of these will never complete on
        # its own.
        dead_states = (
            grpc.ChannelConnectivity.TRANSIENT_FAILURE,
            grpc.ChannelConnectivity.SHUTDOWN,
        )

        # Callback function to monitor state changes
        def connectivity_callback(connectivity):
            mapdl = self_ref()
            if mapdl is None:
                return
            mapdl._log.debug(f"Channel connectivity changed to: {connectivity}")
            mapdl._channel_state = connectivity

            if connectivity in dead_states:
                mapdl._cancel_call_if_pending(connectivity)

        # Keep a handle so the callback can be unsubscribed on teardown
        self._connectivity_callback = connectivity_callback

        # Subscribe to channel state changes
        self._channel.subscribe(connectivity_callback, try_to_connect=True)

    def _multi_connect(self, n_attempts=5, timeout=15):
        """Try to connect over a series of attempts to the channel.

        A background monitoring thread runs in parallel with connection
        attempts and checks whether the local MAPDL process is still alive
        every 0.5 s.  When process death is detected the thread sets
        ``monitor_stop_event``, which causes the in-progress ``_connect()``
        call to abort within 10 ms, so the worst-case wait is reduced from
        the full ``attempt_timeout`` to ~0.5 s.

        Parameters
        ----------
        n_attempts : int, optional
            Number of connection attempts.
        timeout : float, optional
            Total timeout in seconds.
        """
        connected = False
        attempt_timeout = int(timeout / n_attempts)

        # Shared state between the main thread and the monitor thread.
        monitor_stop_event = threading.Event()
        monitor_exception: dict = {"error": None}

        def monitor_mapdl_alive() -> None:
            """Background thread: poll MAPDL process liveness every 0.5 s.

            Only active for local launches where both ``_mapdl_process`` and
            ``_path`` are set.  Uses direct process-status checks rather than
            PID existence to avoid PID-reuse false-positives on Windows.
            Supports both ``subprocess.Popen`` and ``psutil.Process`` handles.
            """
            try:
                while not monitor_stop_event.is_set():
                    if self._local and self._mapdl_process and self._path:
                        try:
                            process_alive = self._check_process_handle(
                                self._mapdl_process
                            )

                            if not process_alive:
                                # On Windows a terminal process can spawn MAPDL
                                # and then exit; try to discover the real
                                # MAPDL process before declaring death.
                                procs = self._find_live_mapdl_processes()
                                if not procs:
                                    raise MapdlDidNotStart("MAPDL process has died.")
                                # Cache discovered PIDs without overwriting the
                                # original process handle (it may be a terminal).
                                self._pids = [int(p.pid) for p in procs]

                        except Exception as exc:
                            monitor_exception["error"] = exc
                            monitor_stop_event.set()
                            break

                    monitor_stop_event.wait(0.5)

            except Exception as exc:
                self._log.debug("Monitor thread encountered error: %s", exc)
                monitor_exception["error"] = exc
                monitor_stop_event.set()

        # Only start monitoring for local instances with a process handle and path.
        monitor_thread = None
        if self._local and self._mapdl_process and self._path:
            monitor_thread = threading.Thread(target=monitor_mapdl_alive, daemon=True)
            monitor_thread.start()
            self._log.debug("Started MAPDL monitoring thread")

        try:
            max_time = time.time() + timeout
            i = 1
            while time.time() < max_time and i <= n_attempts:
                # Propagate any exception raised by the monitor thread.
                if monitor_exception["error"] is not None:
                    self._log.debug(
                        "Monitor detected MAPDL process issue, "
                        "stopping connection attempts"
                    )
                    raise monitor_exception["error"]

                self._log.debug("Connection attempt %d", i)
                connected = self._connect(
                    timeout=attempt_timeout, stop_event=monitor_stop_event
                )
                i += 1
                if connected:
                    self._log.debug("Connected")
                    break

            else:
                # Exhausted attempts / timeout — build an informative message.
                msg = (
                    f"Unable to connect to MAPDL gRPC instance at "
                    f"{self._channel_str}.\nReached either maximum amount of "
                    f"connection attempts ({n_attempts}) or timeout ({timeout} s)."
                )

                alive = self._is_alive_subprocess()
                if alive:
                    pid = getattr(self._mapdl_process, "pid", "'Not found'")
                    raise MapdlConnectionError(
                        msg + f" The MAPDL process seems to be alive (PID: {pid})"
                        " but PyMAPDL cannot connect to it."
                    )

                # Double-check using cached _pids.
                cached_proc = self._find_processes_from_cached_pids()
                cached_pid = cached_proc[0].pid if cached_proc else None

                if cached_pid is not None:
                    raise MapdlConnectionError(
                        msg
                        + f" The MAPDL process seems to be alive (PID: {cached_pid})"
                        " but PyMAPDL cannot connect to it."
                    )
                else:
                    pid_msg = ""
                    if self._mapdl_process is not None:
                        pid = getattr(self._mapdl_process, "pid", "'Not found'")
                        pid_msg = f" PID: {pid}"
                    raise MapdlConnectionError(
                        msg + f" The MAPDL process has died{pid_msg}."
                    )

            # Raise any deferred monitor exception (e.g. when the loop broke
            # early because check_process_is_alive failed inline).
            if monitor_exception["error"] is not None:
                raise monitor_exception["error"]

        finally:
            monitor_stop_event.set()
            if monitor_thread is not None:
                monitor_thread.join(timeout=1.0)
                self._log.debug("Stopped MAPDL monitoring thread")

            self._exited = False

    @property
    def _channel_str(self) -> str:
        """Returns the target string.

        Notes
        -----
        Generally of the form of "ip:port", like "127.0.0.1:50052".

        Returns
        -------
        str
            The target string.
        """
        channel = self._channel
        while channel is not None:
            # When creating interceptors, channels have a nested "_channel" member
            # containing the intercepted channel.
            # Only the actual channel contains the "target" member describing the address
            if hasattr(channel, "target"):
                return channel.target().decode()
            channel = getattr(channel, "_channel", None)
        # This method is relying on grpc channel's private attributes, fallback in case
        # it does not exist
        return "unknown"  #  pragma: no cover Unreachable in the current gRPC version

    def _connect(
        self, timeout: int = 5, stop_event: Optional[threading.Event] = None
    ) -> bool:
        """Establish a gRPC channel to a remote or local MAPDL instance.

        Parameters
        ----------
        timeout : float
            Time in seconds to wait until the connection has been established.
        stop_event : threading.Event, optional
            When provided, the connection attempt will abort immediately if the
            event becomes set (e.g. signalled by a monitor thread that detected
            MAPDL process death).  Returns ``False`` in that case.

        Returns
        -------
        bool
            True if the connection was established successfully, False otherwise.
        """
        self._state = grpc.channel_ready_future(self._channel)
        self._stub = mapdl_grpc.MapdlServiceStub(self._channel)

        # verify connection
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            if stop_event is not None and stop_event.is_set():
                return False  # Monitor signalled process death — bail immediately
            time.sleep(0.01)

        if not self._state._matured:  # pragma: no cover
            return False
        self._log.debug("Established connection to MAPDL gRPC")

        return True

    @property
    def _server_version(self) -> tuple[int, int, int]:
        """Return the server version.

        Returns
        -------
        tuple
            The server version as a tuple of (major, minor, patch).

        Examples
        --------
        >>> mapdl._server_version
        (0, 3, 0)

        Uses cached ``_server_version_cache`` to avoid unnecessary communication.
        """
        # check cache
        if self._server_version_cache is None:
            self._server_version_cache = self._get_server_version()
        return self._server_version_cache

    def _get_server_version(self) -> tuple[int, int, int]:
        """Request version from gRPC server.

        Notes
        -----
        Generally tied to the release version unless on a development release.

        2020R2 --> 0.0.0 (or any unknown version)
        2021R1 --> 0.3.0
        2021R2 --> 0.4.0
        2022R1 --> 0.X.X

        Returns
        -------
        tuple
            The server version as a tuple of (major, minor, patch).
        """
        sver = (0, 0, 0)
        verstr = self._ctrl("VERSION")
        if verstr:
            sver = version_string_as_tuple(verstr)
        return sver

    def _verify_local(self):
        """Check if Python is local to the MAPDL instance."""
        # Verify if python has assess to the MAPDL directory.
        if self._local:
            directory = self.directory

            if self._jobname is None:
                jobname = self.jobname
            else:
                jobname = self._jobname

            lockfile = directory / (jobname + ".err")
            lockfile0 = directory / (jobname + "0.err")

            if os.path.isfile(lockfile):
                return
            if os.path.isfile(lockfile0):
                return
            self._local = False
