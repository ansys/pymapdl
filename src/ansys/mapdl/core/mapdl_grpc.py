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

"""A gRPC specific class and methods for the MAPDL gRPC client"""

import os
from pathlib import Path

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
import subprocess  # nosec B404
import threading
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Union,
)
from warnings import warn

import grpc

MSG_IMPORT = """There was a problem importing the ANSYS MAPDL API module `ansys-api-mapdl`.
Please make sure you have the latest updated version using:

'pip install ansys-api-mapdl' or 'pip install --upgrade ansys-api-mapdl'

If this does not solve it, please reinstall 'ansys.mapdl.core'
or contact Technical Support at 'https://github.com/ansys/pymapdl'."""

try:
    from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
    from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
except ImportError:  # pragma: no cover
    raise ImportError(MSG_IMPORT)

from ansys.mapdl.core import __version__
from ansys.mapdl.core._mapdl_grpc.connection import _GrpcConnectionMixin
from ansys.mapdl.core._mapdl_grpc.files import _GrpcFileMixin
from ansys.mapdl.core._mapdl_grpc.health import _GrpcHealthMixin
from ansys.mapdl.core._mapdl_grpc.input import _GrpcInputMixin
from ansys.mapdl.core._mapdl_grpc.lifecycle import _GrpcLifecycleMixin
from ansys.mapdl.core._mapdl_grpc.post26 import VAR_IR, _GrpcPost26Mixin
from ansys.mapdl.core._mapdl_grpc.processes import _drain_queue, _GrpcProcessMixin
from ansys.mapdl.core._mapdl_grpc.queries import _GrpcQueryMixin
from ansys.mapdl.core._mapdl_grpc.transport import (
    DEFAULT_GRPC_OPTIONS,
    KEEPALIVE_TIME_MS,
    SERVICE_DEFAULT_CONFIG,
    VOID_REQUEST,
    chunk_raw,
    get_file_chunks,
    save_chunks_to_file,
)
from ansys.mapdl.core.common_grpc import DEFAULT_FILE_CHUNK_SIZE
from ansys.mapdl.core.constants import (
    MAPDL_DEFAULT_PORT,
    MAX_MESSAGE_LENGTH,
)
from ansys.mapdl.core.errors import (
    MapdlConnectionError,
    MapdlExitedError,
    MapdlRuntimeError,
    protect_grpc,
)
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.mapdl_types import MapdlInt
from ansys.mapdl.core.misc import (
    check_valid_ip,
    get_ip_hostname,
    random_string,
    supress_logging,
)

if TYPE_CHECKING:  # pragma: no cover
    from queue import Queue

    from ansys.platform.instancemanagement import Instance as PIM_Instance

    from ansys.mapdl.core.database import MapdlDb


# Names re-exported for backward compatibility with code that imported them
# from this module before the responsibility split.
__all__ = [
    "_drain_queue",
    "chunk_raw",
    "DEFAULT_FILE_CHUNK_SIZE",
    "DEFAULT_GRPC_OPTIONS",
    "get_file_chunks",
    "KEEPALIVE_TIME_MS",
    "MapdlGrpc",
    "MAX_MESSAGE_LENGTH",
    "save_chunks_to_file",
    "SERVICE_DEFAULT_CONFIG",
    "VAR_IR",
    "VOID_REQUEST",
]


DEFAULT_TIME_STEP_STREAM = None
DEFAULT_TIME_STEP_STREAM_NT = 500
DEFAULT_TIME_STEP_STREAM_POSIX = 100


def get_start_instance(
    start_instance=None, ip=None, **kwargs
) -> bool:  # numpydoc ignore=RT01
    """Wraps resolve_start_instance to avoid circular imports."""
    from ansys.mapdl.core.launcher.config import resolve_start_instance

    return resolve_start_instance(start_instance, ip)


class MapdlGrpc(
    # Mixins must precede MapdlBase: their super().<command>() calls
    # resolve to the generated commands through this order.
    _GrpcFileMixin,
    _GrpcInputMixin,
    _GrpcQueryMixin,
    _GrpcPost26Mixin,
    _GrpcConnectionMixin,
    _GrpcHealthMixin,
    _GrpcProcessMixin,
    _GrpcLifecycleMixin,
    MapdlBase,
):
    """This class connects to a GRPC MAPDL server and allows commands
    to be passed to a persistent session.

    Parameters
    ----------
    ip : str, optional
        IP address to connect to the server.  The default is 'localhost'.

    port : int, optional
        Port to connect to the MAPDL server.  The default is ``50052``.

    timeout : float, optional
        Maximum allowable time to connect to the MAPDL server.

    loglevel : str, optional
        Sets which messages are printed to the console.  Default
        'INFO' prints out all ANSYS messages, 'WARNING` prints only
        messages containing ANSYS warnings, and 'ERROR' prints only
        error messages.

    cleanup_on_exit : bool, optional
        Exit MAPDL when Python exits or when this instance is garbage
        collected.

    set_no_abort : bool, optional
        Sets MAPDL to not abort at the first error within /BATCH mode.
        The default is ``True``.

    remove_temp_dir : bool, optional
        When this parameter is ``True``, the MAPDL working directory will be
        deleted when MAPDL is exited provided that it is within the temporary
        user directory. The default is ``False``.

    log_file : bool, optional
        Copy the log to a file called `logs.log` located where the
        python script is executed. The default is ``True``.

    print_com : bool, optional
        Print the command ``/COM`` arguments to the standard output.
        The default is ``False``.

    disable_run_at_connect: bool, optional
        Whether to skip the connection-time setup: it sets the POST26 variable
        limit (``NUMVAR,200``), sets the ``/SHOW`` plot file type, and caches the
        working directory and the MAPDL version.
        The default is ``False``.

    channel : grpc.Channel, optional
        gRPC channel to use for the connection. This parameter can be
        used as an alternative to the ``ip`` and ``port`` parameters.

    remote_instance : ansys.platform.instancemanagement.Instance
        The corresponding remote instance when MAPDL is launched through
        PyPIM. This instance will be deleted when calling
        :func:`Mapdl.exit <ansys.mapdl.core.Mapdl.exit>`.

    transport_mode : str | None
        Transport mode selected, by default `None` and thus it will be selected
        for you based on the connection criteria. Options are: "insecure", "uds", "wnua", "mtls"

    uds_dir : Path | str | None
        Directory to use for Unix Domain Sockets (UDS) transport mode.
        By default `None` and thus it will use the "~/.conn" folder.

    certs_dir : Path | str | None
        Directory to use for TLS certificates.
        By default `None` and thus search for the "ANSYS_GRPC_CERTIFICATES" environment variable.
        If not found, it will use the "certs" folder assuming it is in the current working
        directory.


    Examples
    --------
    Connect to an instance of MAPDL already running on locally on the
    default port 50052.

    >>> from ansys.mapdl import core as pymapdl
    >>> mapdl = pymapdl.Mapdl()

    Connect to an instance of MAPDL running on the LAN on a default port.

    >>> mapdl = pymapdl.Mapdl('192.168.1.101')

    Connect to an instance of MAPDL running on the LAN on a non-default port.

    >>> mapdl = pymapdl.Mapdl('192.168.1.101', port=60001)

    If you wish to customize the channel, you can also directly connect
    directly to gRPC channels. For example, if you wanted to create an insecure
    channel with a maximum message length of 8 MB.

    >>> import grpc
    >>> channel = grpc.insecure_channel(
    ...     '127.0.0.1:50052',
    ...     options=[
    ...         ("grpc.max_receive_message_length", 8*1024**2),
    ...     ],
    ... )
    >>> mapdl = pymapdl.Mapdl(channel=channel)
    """

    # Required by `_name` method to be defined before __init__ be
    _ip: Optional[str] = None
    _port: Optional[int] = None
    _lazy_array_prefix = "PYMAPDL_LAZY_"

    def __init__(
        self,
        ip: Optional[str] = None,
        port: Optional[MapdlInt] = None,
        *,
        timeout: int = 15,
        loglevel: str = "WARNING",
        log_file: bool = False,
        cleanup_on_exit: bool = False,
        log_apdl: Optional[str] = None,
        set_no_abort: bool = True,
        remove_temp_dir_on_exit: bool = False,
        print_com: bool = False,
        disable_run_at_connect: bool = False,
        channel: Optional[grpc.Channel] = None,
        remote_instance: Optional["PIM_Instance"] = None,
        transport_mode: Optional[str] = None,
        uds_dir: Optional[Union[str, Path]] = None,
        certs_dir: Optional[Union[str, Path]] = None,
        **start_parm: dict[str, Any],
    ):
        """Initialize connection to the mapdl server"""
        self._name: Optional[str] = None
        self._session_id_: Optional[str] = None
        self._checking_session_id_: bool = False
        self._distributed_cache: Optional[bool] = None
        self._remote_instance: Optional["PIM_Instance"] = remote_instance
        self._strict_session_id_check: bool = (
            False  # bool to force to check the session id matches in client and server
        )

        self.transport_mode = transport_mode
        if uds_dir is not None:
            self.uds_dir: Path = Path(uds_dir)
        else:
            _env_uds = os.environ.get("ANSYS_MAPDL_UDS_PATH")
            self.uds_dir = (
                Path(_env_uds) if _env_uds else Path("~").expanduser() / ".conn"
            )

        self.certs_dir: Path | None = Path(certs_dir) if certs_dir is not None else None
        self.grpc_options = start_parm.pop("grpc_options", DEFAULT_GRPC_OPTIONS)
        # Transport configuration will be finalized after base init

        if channel is not None:
            if ip is not None or port is not None:
                raise ValueError(
                    "If `channel` is specified, neither `port` nor `ip` can be specified."
                )
        if ip is None:
            ip = start_parm.pop("ip", None) or "127.0.0.1"  # type: ignore[assignment]

        # setting hostname and ip
        ip, hostname = get_ip_hostname(ip)
        self._hostname: str = hostname

        check_valid_ip(ip)
        self._ip = ip  # type: ignore[misc]

        # port and ip are needed to setup the log
        if port is None:
            port = MAPDL_DEFAULT_PORT

        self._port: int = int(port)
        start_parm["port"] = self._port  # type: ignore[assignment]  # store for `open_gui`

        super().__init__(
            loglevel=loglevel,
            log_apdl=log_apdl,
            log_file=log_file,
            print_com=print_com,
            mode="grpc",
            **start_parm,
        )
        # Finalize transport specifics now that logging and port are set
        self._configure_transport(ip=ip, port=port)
        self._mode: Literal["grpc"] = "grpc"

        # gRPC request locks and lazy result bookkeeping.
        self._get_lock: bool = False
        self._vget_lock: bool = False
        self._lazy_array_counter: int = 0
        self._lazy_array_parameters: set[str] = set()

        self._prioritize_thermal: bool = False
        self._locked: bool = False  # being used within MapdlPool
        self._stub: Optional[mapdl_grpc.MapdlServiceStub] = None
        self._cleanup: bool = cleanup_on_exit
        self.remove_temp_dir_on_exit: bool = remove_temp_dir_on_exit
        self._jobname: str = start_parm.get("jobname", "file")  # type: ignore[assignment]
        self._path: Optional[str] = (
            None  # self._wrap_directory(start_parm.get("run_location"))
        )
        self._start_instance: Optional[str] = (
            start_parm.get("start_instance") or get_start_instance()  # type: ignore[assignment]
        )
        self._busy: bool = False  # used to check if running a command on the server
        self._local: bool = start_parm.get("local", True)  # type: ignore[assignment]
        self._xpl = None  # ansXpl instance, initialized on first access
        self._launched: bool = start_parm.get("launched", False)  # type: ignore[assignment]
        self._health_response_queue: Optional["Queue"] = None
        self._exiting: bool = False
        self._exited: Optional[bool] = None
        self._process_close_lock: threading.Lock = threading.Lock()
        self._db: Optional[MapdlDb] = None
        self._server_version_cache: Optional[tuple[int, int, int]] = None
        self._state: Optional[grpc.Future] = None
        self._timeout: int = timeout
        self._env_vars: Dict[str, str] = start_parm.get("env_vars", {})
        self._pids: List[Union[int, None]] = []
        self._channel_state: grpc.ChannelConnectivity = (
            grpc.ChannelConnectivity.CONNECTING
        )
        self._time_step_stream: Optional[int] = None
        self._connectivity_callback: Optional[Callable[[Any], None]] = None
        # Handle to the gRPC call currently in flight (if any), so a
        # connectivity-state watchdog can cancel it promptly when the
        # transport is confirmed dead, instead of waiting for it to time out
        # or hang forever. Guarded by '_current_call_lock' because it is
        # written from the calling thread and read/cancelled from the gRPC
        # connectivity callback thread.
        self._current_call: Optional[grpc.Future] = None
        self._current_call_lock: threading.Lock = threading.Lock()

        if channel is None:
            self._log.debug("Creating channel to %s:%s", ip, port)
            self._channel = self._create_channel(ip, port)  # type: ignore[misc]
        else:
            self._log.debug("Using provided channel")
            self._channel = channel  # type: ignore[misc]

        # Subscribe to channel for channel state updates
        self._subscribe_to_channel()

        # connect and validate to the channel
        self._mapdl_process: Optional[subprocess.Popen] = start_parm.pop(
            "process", None
        )  # type: ignore[assignment]

        # saving for later use (for example open_gui)
        self._start_parm: Dict[str, Any] = start_parm

        # Storing HPC related stuff
        self._jobid: int = start_parm.get("jobid")  # type: ignore[assignment]
        self._mapdl_on_hpc: bool = bool(self._jobid)
        self.finish_job_on_exit: bool = start_parm.get("finish_job_on_exit", True)  # type: ignore[assignment]

        # Queueing the stds
        if not self._mapdl_on_hpc and self._mapdl_process:
            self._create_process_stds_queue()

        self.reconnect_to_mapdl()

        # Avoiding muting when connecting to the session
        # It might trigger some errors later on if not.
        self._run("/gopr")

        # initialize mesh, post processing, and file explorer interfaces
        self._mesh_rep: Optional["MeshGrpc"] = None

        from ansys.mapdl.core.mesh_grpc import MeshGrpc

        self._mesh_rep = MeshGrpc(self)

        # Run at connect
        if not disable_run_at_connect:
            self._run_at_connect()

        # HOUSEKEEPING:
        # Set to not abort after encountering errors.  Otherwise, many
        # failures in a row will cause MAPDL to exit without returning
        # anything useful.  Also avoids abort in batch mode if set.
        if set_no_abort is None or set_no_abort:
            self._set_no_abort()

        # double check we have access to the local path if not
        # explicitly specified
        if "local" not in start_parm:
            self._verify_local()

        # only cache process IDs if launched locally
        if self._local and self._launched:
            self._cache_pids()

        self._create_session()

        # Caching platform.
        self._log.info(
            f"Connected to MAPDL server running at {self._hostname} on {self.ip}:{self.port} on {self.platform} OS"
        )

    def _after_run(self, command: str) -> None:
        if command[:4].upper() == "/CLE":
            # We have reset the database, so we need to create a new session id
            self._create_session()

    def _before_run(self, _command: str) -> None:
        if self._session_id is not None:
            self._check_session_id()
        else:
            # For some reason the session hasn't been created
            self._create_session()

    @property
    def mute(self):
        """Silence the response from all MAPDL functions unless
        explicitly set to ``True``.

        Returns
        -------
        bool
            Current state of the mute.

        Examples
        --------
        >>> mapdl.mute = True
        >>> mapdl.prep7()
        ''

        Temporarily override the instance setting this with
        ``mute=False``.  This is useful for methods that parse the
        MAPDL output like ``k``.

        >>> mapdl.k('', 1, 1, 1, mute=False)
        1
        """
        return self._mute

    @mute.setter
    def mute(self, value):
        self._log.debug(f"Mute value has been changed to '{value}'.")
        self._mute = value

    def __repr__(self):
        info = super().__repr__()
        return info

    def _launch(
        self, start_parm: dict[str, Any] | None = None, timeout: int | None = 10
    ):
        """Launch a local session of MAPDL in gRPC mode.

        This should only need to be used for legacy ``open_gui``
        """
        if not self._local:
            raise MapdlRuntimeError(
                "Can only launch the GUI with a local instance of MAPDL"
            )
        from ansys.mapdl.core.launcher.models import LaunchConfig, LaunchMode
        from ansys.mapdl.core.launcher.process import (
            _generate_launch_command,
            _start_subprocess,
        )

        self._exited = False  # reset exit state

        args = start_parm or self._start_parm
        config = LaunchConfig(
            exec_file=args["exec_file"],
            run_location=args["run_location"],
            jobname=args["jobname"],
            nproc=args["nproc"],
            ram=args.get("ram"),
            port=args["port"],
            ip=args.get("ip", "127.0.0.1"),
            mode=LaunchMode.GRPC,
            version=args.get("version"),
            start_instance=True,
            timeout=args.get("timeout", 60),
            cleanup_on_exit=args.get("cleanup_on_exit", True),
            clear_on_connect=args.get("clear_on_connect", True),
            override=args.get("override", False),
            remove_temp_dir_on_exit=args.get("remove_temp_dir_on_exit", False),
            set_no_abort=args.get("set_no_abort", True),
            additional_switches=args.get("additional_switches", ""),
            license_type=args.get("license_type"),
            launch_on_hpc=args.get("launch_on_hpc", False),
            running_on_hpc=args.get("running_on_hpc", False),
            scheduler_options=args.get("scheduler_options"),
            loglevel=args.get("loglevel", "WARNING"),
            log_apdl=args.get("log_apdl"),
            print_com=args.get("print_com", False),
            mapdl_output=args.get("mapdl_output"),
            transport_mode=args.get("transport_mode"),
            uds_dir=args.get("uds_dir"),
            certs_dir=args.get("certs_dir"),
        )
        cmd = _generate_launch_command(config)

        process = _start_subprocess(
            cmd=cmd,
            cwd=args["run_location"],
            env=self._env_vars or {},
            output_file=None,
        )

        self._connect()

        # may need to wait for viable connection in open_gui case
        timeout_value = timeout if timeout is not None else 10
        tmax = time.time() + timeout_value
        success = False
        while time.time() < tmax:
            try:
                self.prep7()
                success = True
                break
            except MapdlRuntimeError:
                time.sleep(1)
                warn("PyMAPDL is taking longer than expected to connect to the server.")

        if not success:
            raise MapdlConnectionError("Unable to reconnect to MAPDL")

        # Update process
        self._mapdl_process = process

    @supress_logging
    def _set_no_abort(self):
        """Do not abort MAPDL."""
        self._log.debug("Setting to no abort")
        self.run(
            "/NERR,,,-1", mute=True
        )  # ABORT argument is not surfaced in PyMAPDL because it is not documented in the manual

    def _run_at_connect(self):
        """Run house-keeping commands when initially connecting to MAPDL."""
        # increase the number of variables allowed in POST26 to the maximum
        with self.run_as_routine("POST26"):
            self.numvar(200, mute=True)

        # Caching directory
        self.directory

        self.show(self._file_type_for_plots)
        self.version  # Caching version
        self.file_type_for_plots  # Setting /show,png and caching it.

    def _reset_cache(self):
        """Reset cached items."""
        if self._mesh_rep is not None:
            self._mesh_rep._reset_cache()

        if self._geometry is not None:
            self._geometry._reset_cache()

    @property
    def _mesh(self):
        return self._mesh_rep

    def _run(self, cmd: str, verbose: bool = False, mute: Optional[bool] = None) -> str:
        """Send a command and return the response as a string.

        Parameters
        ----------
        cmd : str
            Valid MAPDL command.

        verbose : bool, optional
            Print the response of a command while it is being run.

        mute : bool, optional
            Whether output is to be sent from the gRPC server. The default
            is ``None``, in which case the global setting specified by
            ``mapdl.mute = <bool>`` is used, which is ``False`` by default.

        Returns
        -------
        str
            The response from the MAPDL server.

        Examples
        --------
        Run a basic command.

        >>> mapdl.run('/PREP7')

        Run a command and suppress its output.

        >>> mapdl.run('/PREP7', mute=True)

        Run a command and stream its output while it is being run.

        >>> mapdl.run('/PREP7', verbose=True)
        """
        if mute is None:
            mute = self._mute

        # Cheap, purely local liveness check: 'channel_state' reads the value
        # cached by the connectivity callback, whereas 'is_alive' would issue a
        # '_ctrl("VERSION")' round-trip on every single command. Only
        # 'SHUTDOWN' (channel closed) and 'TRANSIENT_FAILURE' (channel could
        # not connect) are treated as dead; 'CONNECTING' is a normal
        # transient and must not permanently mark the instance as exited.
        if self._channel is not None and self.channel_state in (
            "SHUTDOWN",
            "TRANSIENT_FAILURE",
        ):
            self._exited = True
            raise MapdlExitedError(
                f"Mapdl exited (gRPC channel is '{self.channel_state}') before running the command: {cmd}"
            )

        if self.exited:
            raise MapdlExitedError(
                f"The MAPDL instance has been exited before running the command: {cmd}"
            )

        # don't allow empty commands
        if not cmd.strip():
            raise ValueError("Empty commands not allowed")

        if len(cmd) > 639:  # CMD_MAX_LENGTH
            raise ValueError("Maximum command length must be less than 640 characters")

        self._busy = True
        try:
            if verbose:
                response = self._send_command_stream(cmd, True)
            else:
                response = self._send_command(cmd, mute=mute)
        finally:
            # '_busy' must be cleared even when the command raises, otherwise
            # 'is_alive' short-circuits on it forever and the liveness guard
            # above is permanently disabled.
            self._busy = False

        return response.strip()

    @property
    def busy(self) -> bool:
        """Check if the MAPDL gRPC server is busy executing a command.

        Returns
        -------
        bool
            Returns true if the MAPDL gRPC server is busy executing a command.
        """
        return self._busy

    @property
    def exiting(self) -> bool:
        """Check if the MAPDL instance is exiting.

        Returns
        -------
        bool
            Returns true if the MAPDL instance is exiting."""
        return self._exiting

    @property
    def port(self) -> int:
        """Returns the MAPDL gRPC instance port.

        Returns
        -------
        int
            Port number of the MAPDL gRPC instance.
        """
        return self._port

    @property
    def ip(self) -> str:
        """Return the MAPDL gRPC instance IP.

        Returns
        -------
        str
            IP address of the MAPDL gRPC instance.
        """
        return self._ip

    @property
    def hostname(self) -> str:
        """Return the hostname of the machine MAPDL is running in.

        Returns
        -------
        str
            Hostname of the machine MAPDL is running in
        """
        return self._hostname

    @property
    def jobid(self) -> int:
        """Returns the job id where the MAPDL is running in.

        This is only applicable if MAPDL is running on an HPC cluster.

        Returns
        -------
        int
            Returns the job id where the MAPDL is running in.
        """
        return self._jobid

    @property
    def mapdl_on_hpc(self) -> bool:
        """Check if MAPDL is running on an HPC cluster.

        Returns
        -------
        bool
            Returns :class:`True` if the MAPDL instance has been launched using
            an scheduler.
        """
        return self._mapdl_on_hpc

    @protect_grpc
    def _send_command(
        self, cmd: str, mute: bool = False
    ) -> Optional[str]:  # numpydoc ignore=RT01
        """Send a MAPDL command and return the response as a string"""
        opt = ""
        if mute:
            opt = "MUTE"  # suppress any output

        request = pb_types.CmdRequest(command=cmd, opt=opt)
        # TODO: Capture keyboard exception and place this in a thread
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        future = self._stub.SendCommand.future(request)
        with self._watched_call(future):
            grpc_response = future.result()

        resp = grpc_response.response
        if resp is not None:
            return resp.strip()
        return ""

    @protect_grpc
    def _send_command_stream(self, cmd, verbose=False) -> str:  # numpydoc ignore=RT01
        """Send a command and expect a streaming response"""
        request = pb_types.CmdRequest(command=cmd)
        time_step = self._get_time_step_stream()
        metadata = [("time_step_stream", str(time_step))]
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        stream = self._stub.SendCommandS(request, metadata=metadata)
        response = []
        with self._watched_call(stream):
            for item in stream:
                cmdout = "\n".join(item.cmdout)
                if verbose:
                    print(cmdout)
                response.append(cmdout.strip())

        return "".join(response)

    @supress_logging
    def sys(self, cmd: str, **kwargs) -> str:
        """Pass a command string to the operating system.

        APDL Command: /SYS

        Passes a command string to the operating system for execution
        (see the Operations Guide).  Typical strings are system
        commands such as list, copy, rename, etc.  Control returns to
        the ANSYS program after the system procedure is completed.
        ANSYS may not be aware of your specific user environment. For
        example, on Linux this command may not recognize aliases,
        depending on the hardware platform and user environment.

        Parameters
        ----------
        cmd : str
            Command string, up to 639 characters (including blanks,
            commas, etc.). The specified string is passed verbatim to
            the operating system, i.e., no parameter substitution is
            performed.

        Returns
        -------
        str
            Output from the command.

        Examples
        --------
        >>> mapdl.sys('ls')
        """
        return self._sys(cmd, check_blocked=True, **kwargs)

    @supress_logging
    def _sys(self, cmd: str, check_blocked: bool = False, **kwargs) -> str:
        """Run ``/SYS`` and return its output.

        PyMAPDL internals call this directly so that they keep working when
        ``/SYS`` is in ``blocked_commands``. Only ``sys()`` checks the block.
        """
        # always redirect system output to a temporary file
        tmp_file = f"__tmp_sys_out_{random_string()}__"
        if check_blocked:
            super().sys(f"{cmd} > {tmp_file}", **kwargs)
        else:
            self._run(f"/SYS,{cmd} > {tmp_file}")
        if self._local:  # no need to download when local
            with open(self.directory / tmp_file) as fobj:
                obj = fobj.read()
        else:
            obj = self._download_as_raw(tmp_file).decode()

        self.slashdelete(tmp_file)

        # Remove trailing newline character if present and only once
        return obj[:-1] if (len(obj) > 0 and obj[-1] == "\n") else obj

    def _get_time_step_stream(  # numpydoc ignore=RT01
        self, time_step: Optional[Union[int, float]] = None
    ) -> str:
        """Return the time step for checking if MAPDL is done writing the
        output to the file which later will be returned as response
        """
        if time_step is None:
            if DEFAULT_TIME_STEP_STREAM is not None:
                time_step = DEFAULT_TIME_STEP_STREAM
            elif self._time_step_stream is not None:
                time_step = self._time_step_stream
            else:
                if self.platform == "windows":
                    time_step = DEFAULT_TIME_STEP_STREAM_NT
                elif self.platform == "linux":
                    time_step = DEFAULT_TIME_STEP_STREAM_POSIX
                else:
                    raise ValueError(
                        f"The MAPDL platform ('{self.platform}') is not recognaised."
                    )

        else:
            if time_step <= 0:
                raise ValueError("``time_step`` argument must be greater than 0``")

        self.logger.debug(f"The time_step argument is set to: {time_step}")
        self._time_step_stream = time_step  # type: ignore[assignment]
        return time_step

    @property
    def locked(self) -> bool:
        """Instance is in use within a pool.

        Returns
        -------
        bool
            True if the instance is distributed, False otherwise.
        """
        return self._locked

    @locked.setter
    def locked(self, new_value: bool):
        self._locked = new_value

    @supress_logging
    def __str__(self):
        try:
            if self._exited:
                return "MAPDL exited"
            stats = self.slashstatus("PROD", mute=False)
        except:  # pragma: no cover
            return "MAPDL exited"

        st = stats.find("*** Products ***")
        en = stats.find("*** PrePro")
        product = "\n".join(stats[st:en].splitlines()[1:]).strip()

        info = "Mapdl\n"
        info += "-----\n"
        info += f"PyMAPDL Version:     {__version__}\n"
        info += "Interface:           grpc\n"
        info += f"Product:             {product}\n"
        info += f"MAPDL Version:       {self.version}\n"
        info += f"Running on:          {self.hostname}\n"
        info += f"                     ({self.ip})"
        return info

    @property
    def thermal_result(self):
        """The thermal result object.

        Returns
        -------
        :class:`MapdlResult <ansys.mapdl.core.result.MapdlResult>`
            The thermal result object.
        """
        self._prioritize_thermal = True
        result = self.result
        self._prioritize_thermal = False
        return result

    @MapdlBase.name.getter
    def name(self) -> str:
        """Instance unique identifier.

        Returns
        -------
        str
            Unique identifier for the instance. If not set, it will be
            generated based on the IP and port of the gRPC server.
        """
        if not self._name:
            if self._ip or self._port:
                self._name = f"GRPC_{self._ip}:{self._port}"
            else:
                self._name = f"GRPC_instance_{id(self)}"
        return self._name

    @property
    def _distributed(self) -> bool:  # numpydoc ignore=RT01
        """MAPDL is running in distributed mode."""
        if self._distributed_cache is None:
            self._distributed_cache = self.parameters.numcpu > 1
        return self._distributed_cache
