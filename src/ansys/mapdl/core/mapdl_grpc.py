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

import fnmatch
from functools import wraps
import glob
import os
from pathlib import Path, PurePath, PurePosixPath
import re
import shutil

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
import subprocess  # nosec B404
import tempfile
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
    Tuple,
    Union,
)
from warnings import warn

import grpc
import numpy as np
from numpy.typing import NDArray

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

from ansys.mapdl.core import _HAS_TQDM, __version__
from ansys.mapdl.core._mapdl_grpc.connection import _GrpcConnectionMixin
from ansys.mapdl.core._mapdl_grpc.health import _GrpcHealthMixin
from ansys.mapdl.core._mapdl_grpc.lifecycle import _GrpcLifecycleMixin
from ansys.mapdl.core._mapdl_grpc.processes import _drain_queue, _GrpcProcessMixin
from ansys.mapdl.core._mapdl_grpc.transport import (
    DEFAULT_GRPC_OPTIONS,
    KEEPALIVE_TIME_MS,
    SERVICE_DEFAULT_CONFIG,
    VOID_REQUEST,
    chunk_raw,
    get_file_chunks,
    save_chunks_to_file,
)
from ansys.mapdl.core.common_grpc import DEFAULT_FILE_CHUNK_SIZE, parse_chunks
from ansys.mapdl.core.constants import (
    ANSYS_VALUE_TYPE,
    DEFAULT_CHUNKSIZE,
    MAPDL_DEFAULT_PORT,
    MAX_MESSAGE_LENGTH,
)
from ansys.mapdl.core.errors import (
    MapdlConnectionError,
    MapdlError,
    MapdlExitedError,
    MapdlRuntimeError,
    protect_grpc,
)
from ansys.mapdl.core.lazy_array import LazyArray
from ansys.mapdl.core.mapdl import MapdlBase
from ansys.mapdl.core.mapdl_core import MAX_PARAM_CHARS
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat, MapdlInt
from ansys.mapdl.core.misc import (
    check_valid_ip,
    get_ip_hostname,
    last_created,
    random_string,
    run_as,
    supress_logging,
)

if TYPE_CHECKING:  # pragma: no cover
    from queue import Queue

    from ansys.platform.instancemanagement import Instance as PIM_Instance

    from ansys.mapdl.core.database import MapdlDb
    from ansys.mapdl.core.xpl import ansXpl


VAR_IR = 9  # Default variable number for automatic variable retrieving (/post26)


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

    def download_result(
        self,
        path: str | Path | None = None,
        progress_bar: bool = False,
        preference: Literal["rst", "rth"] | None = None,
    ) -> str:
        """Download remote result files to a local directory

        Parameters
        ----------
        path
            Path where the files are downloaded, by default the current
            python path (``os.getcwd()``)

        progress_bar
            Show the progress bar or not, default to False.

        preference
            Preferred type for the result file, which is either ``rst`` or ``rth``.
            This parameter is only required when both files are present. The default is ```None``,
            in which case ``"rst"`` is used.

        Returns
        -------
        list[str]
            List of downloaded files.

        Examples
        --------
        Download remote result files into the current working directory

        >>> import os
        >>> mapdl.download_result(os.getcwd())
        """
        if path is None:  # if not path seems to not work in same cases.
            path = os.getcwd()

        def _download(targets: List[str]) -> None:
            for target in targets:
                save_name = os.path.join(path, target)
                self._download(target, save_name, progress_bar=progress_bar)

        if preference:
            if preference not in ["rst", "rth"]:
                raise ValueError("``preference`` must be either 'rst' or 'rth'")

        # result file basename is the jobname
        jobname = self.jobname
        rth_basename = "%s.%s" % (jobname, "rth")
        rst_basename = "%s.%s" % (jobname, "rst")

        remote_files = self.list_files()
        result_file = None

        if self._prioritize_thermal and rth_basename in remote_files:
            result_file = rth_basename
        elif rst_basename in remote_files and rth_basename in remote_files:
            if preference == "rth":
                result_file = rth_basename
            else:
                result_file = rst_basename
        elif rst_basename in remote_files:
            result_file = rst_basename
        elif rth_basename in remote_files:
            result_file = rth_basename

        if result_file:  # found non-distributed result
            save_name = os.path.join(path, result_file)
            self._download(result_file, save_name, progress_bar=progress_bar)
            return save_name

        # otherwise, download all the distributed result files
        if jobname[-1].isnumeric():
            jobname += "_"

        rst_files = []
        rth_files = []
        for filename in remote_files:
            if "rst" in filename and jobname in filename:
                rst_files.append(filename)
            elif "rth" in filename and jobname in filename:
                rth_files.append(filename)

        if self._prioritize_thermal and rth_files:
            targets = rth_files
        else:
            if rst_files and rth_files:
                if preference is None:
                    raise ValueError(
                        "Found both structural and thermal results files."
                        "\nPlease specify which kind to download using:\n"
                        '``preference="rth"`` or ``preference="rst"``'
                    )
                if preference == "rst":
                    targets = rst_files
                elif preference == "rth":
                    targets = rth_files
            elif rst_files:
                preference = "rst"
                targets = rst_files
            elif rth_files:
                preference = "rth"
                targets = rth_files
            else:
                remote_files_str = "\n".join("\t%s" % item for item in remote_files)
                raise FileNotFoundError(
                    "Unable to locate any result file from the "
                    "following remote result files:\n\n" + remote_files_str
                )
        _download(targets)
        return os.path.join(path, jobname + "0." + preference)

    @wraps(MapdlBase.cdread)
    def cdread(
        self, option="", fname="", ext="", fnamei="", exti="", **kwargs
    ):  # numpydoc ignore=RT01
        """Wraps CDREAD"""
        option = option.strip().upper()

        if option not in ["ALL", "DB", "SOLID", "COMB"]:
            raise ValueError(
                f'Option "{option}" is not supported.  Please '
                "Input the geometry and mesh files separately "
                r'with "\INPUT" or ``mapdl.input``'
            )

        kwargs.setdefault("verbose", False)
        kwargs.setdefault("progress_bar", False)
        kwargs.setdefault("orig_cmd", "CDREAD")
        kwargs.setdefault("cd_read_option", option)

        cdb_fname = self._get_file_name(fname, ext, "cdb")
        cdb_fname = self._get_file_path(cdb_fname, kwargs["progress_bar"])

        if option == "ALL":
            # 'ALL' reads two archives: the command/database file resolved
            # above (``cdb_fname``), and a solid-model/IGES archive.  Per
            # CDREAD documented defaults, 'fnamei' defaults to the *original*
            # 'fname' argument (not the already-suffixed 'cdb_fname'), and
            # 'exti' defaults to 'iges' when omitted.
            iges_fname = self._get_file_name(fnamei or fname, exti, "iges")
            iges_fname = self._get_file_path(iges_fname, kwargs["progress_bar"])
            kwargs["fnamei"] = iges_fname

        return self.input(cdb_fname, **kwargs)

    @wraps(MapdlBase.tbft)
    def tbft(  # numpydoc ignore=RT01
        self,
        oper="",
        id_="",
        option1="",
        option2="",
        option3="",
        option4="",
        option5="",
        option6="",
        option7="",
        **kwargs,
    ):
        """Wraps ``MapdlBase.tbft``."""
        extra_info = ""
        if oper.lower() == "eadd":
            # Option 2 is a file and option 4 is the directory.
            # Option 3 is be extension
            option3 = option3.replace(".", "")
            fname = option2 if not option3 else option2 + "." + option3
            filename = os.path.join(option4, fname)

            fname = self._get_file_name(fname=option2, ext=option3)
            if option4:  # if directory is supplied
                fname = os.path.join(option4, fname)

            filename = self._get_file_path(fname, progress_bar=False)

            # since we upload the file, we dont need the full path: not in option2 nor option4.
            if not self._local:
                extra_info = f"PyMAPDL has upload the file {option2} to the MAPDL instance, hence the options for 'TBFT' command have changed."
                option2 = filename
                option3 = ""  # the extension is now included in filename
                option4 = ""

        if extra_info:
            self.com("")
            self._log.debug(extra_info)

        return super().tbft(
            oper,
            id_,
            option1,
            option2,
            option3,
            option4,
            option5,
            option6,
            option7,
            **kwargs,
        )

    def input(
        self,
        fname="",
        ext="",
        dir_="",
        line="",
        log="",
        *,
        verbose=False,
        progress_bar=False,
        time_step_stream=None,
        chunk_size=512,
        orig_cmd="/INP",
        write_to_log=True,
        **kwargs,
    ):
        """Stream a local input file to a remote mapdl instance.
        Stream the response back and deserialize the output.

        .. versionchanged:: 0.65
            From version 0.65 you can use the APDL commands arguments (``ext``, ``dir``, ``line``)
            in within this command.
            However, the gRPC implementation does *not* uses the APDL ``/INPUT`` command,
            rather the gRPC input method with the appropriate configuration to replicate
            ``/INPUT`` behaviour.

        Parameters
        ----------
        fname : str, optional
            MAPDL input file to stream to the MAPDL gRPC server.
            File name and directory path.
            An unspecified directory path defaults to the Python working
            directory; in this case, you can use all 248 characters for the file name.
            The file name defaults to the current ``Jobname`` if ``Ext`` is specified.

        ext : str, optional
            Filename extension (eight-character maximum).

        dir_ : str, optional
            Directory path. The default is the current working directory.

        line : int, optional
            A value indicating either a line number in the file from which to
            begin reading the input file. The first line is the zero line (Python
            convention).

            (blank), or 0
                Begins reading from the top of the file. Default.

            LINE_NUMBER
                Begins reading from the specified line number in the file.

        log : optional
            Not supported in the gRPC implementation.

        time_step_stream : int, optional
            Time to wait between streaming updates to send back chunks
            from the listener file.  Larger values mean more data per
            chunk and less chunks, but if the command is short, will
            wait until time_step_stream is finished leading to a long
            execution time.

            Due to stability issues, the default time_step_stream is
            dependent on the OS MAPDL is running on.  The defaults are:

            - Windows: ``time_step_stream=500``
            - Linux: ``time_step_stream=100``

            These defaults will be ignored if ``time_step_stream`` is
            manually set. See the *Examples* section to learn how to change
            the default value globally.

        orig_cmd : str, optional
            Original command. There are some cases, were input is
            used to send the file to the grpc server but then we want
            to run something different than ``/INPUT``, for example
            ``CDREAD``.

        Returns
        -------
        str
            Response from MAPDL.

        Notes
        -----
        This method does not use the APDL ``/INPUT`` command.
        However its usage is very similar to it. See *Examples* section.

        If you want to use ``/INPUT`` for some reason, although it is not
        recommended, you can write the desired input file, upload it using
        :func:`Mapdl.upload <ansys.mapdl.core.Mapdl.upload>`, and then use
        run command :func:`Mapdl.run('/INPUT,<FILE>,<EXT>) <ansys.mapdl.core.Mapdl.run>`.
        This does not avoid to use the gRPC input method, but it allows you to
        use the APDL ``/INPUT`` command from the generated input file.
        See *Examples* section for more information.

        Examples
        --------
        Load a simple ``"ds.dat"`` input file generated from Ansys
        Workbench.

        >>> output = mapdl.input('ds.dat')

        Load that same file while streaming the output in real-time.

        >>> output = mapdl.input('ds.dat', verbose=True)

        Use the default APDL ``/INPUT`` command:

        >>> with open('myinput.inp','w').write("/finish\\n/prep7\\n/com, my commands")
        >>> with open('inputtrigger.inp','w').write("/input,myinput,inp")
        >>> mapdl.upload("myinput.inp")
        Uploading myinput.inp: 100%|█████████████████████████████████████████████████| 26.0/26.0 [00:00<00:00, 5.86kB/s]
        'myinput.inp'
        >>> mapdl.upload("inputtrigger.inp")
        Uploading inputtrigger.inp: 100%|████████████████████████████████████████████| 32.0/32.0 [00:00<00:00, 8.92kB/s]
        'inputtrigger.inp'
        >>> with mapdl.non_interactive:
                mapdl.run("/input,inputtrigger,inp") # This inputs 'myinput.inp'

        You can also change them globably using:

        >>> from ansys.mapdl.core import mapdl_grpc
        >>> mapdl_grpc.DEFAULT_TIME_STEP_STREAM=100 # in milliseconds
        """
        self._check_blocked_commands(orig_cmd)
        return self._stream_input(
            fname,
            ext,
            dir_,
            line,
            log,
            verbose=verbose,
            progress_bar=progress_bar,
            time_step_stream=time_step_stream,
            chunk_size=chunk_size,
            orig_cmd=orig_cmd,
            write_to_log=write_to_log,
            **kwargs,
        )

    @protect_grpc
    def _stream_input(
        self,
        fname="",
        ext="",
        dir_="",
        line="",
        log="",
        *,
        verbose=False,
        progress_bar=False,
        time_step_stream=None,
        chunk_size=512,
        orig_cmd="/INP",
        write_to_log=True,
        **kwargs,
    ):
        # Checking compatibility
        # Checking the user is not reusing old api:
        #
        # fname,
        # verbose=False,
        # progress_bar=False,
        # time_step_stream=None,
        # chunk_size=512,
        # orig_cmd="/INP",
        # write_to_log=True,

        msg_compat = "\nThe 'mapdl.input' method API changed in v0.65. Please check the documentation for information about the new arguments."

        if log:
            raise ValueError(
                "'log' argument is not supported in the gRPC implementation."
            )

        if not isinstance(ext, (str)) and ext is not None:
            raise ValueError(
                "Only strings are allowed in 'ext' argument.\n" + msg_compat
            )

        if not isinstance(dir_, (str)) and dir_ is not None:
            raise ValueError(
                "Only strings are allowed in 'dir_' argument.\n" + msg_compat
            )

        # Getting arguments rights
        if not fname and ext:
            fname = self.jobname

        if not fname:
            raise ValueError("A file name must be supplied.")

        fname = self._get_file_name(fname=fname, ext=ext)

        if not dir_:
            self._log.debug(f"Using python working directory as 'dir_' value.")
            dir_ = os.getcwd()
        else:
            fname = os.path.join(dir_, fname)

        if not line:
            line = 0
        else:
            try:
                line = int(line)
            except ValueError:
                raise ValueError(
                    "Only integers are supported for 'line' argument. Labels are not supported on the gRPC implementation."
                )

        if line != 0:
            # Trimming file
            tmp_modified_file = os.path.join(
                tempfile.gettempdir(), os.path.basename(fname)
            )
            with open(tmp_modified_file, "w") as fid, open(fname, "r") as fid2:
                fid.writelines(fid2.readlines()[line:])

            fname = tmp_modified_file

        # Running method
        #
        is_cdread = "CDRE" in orig_cmd.upper()
        cd_read_option = kwargs.get("cd_read_option", "COMB").upper()
        is_cdread_all = is_cdread and cd_read_option == "ALL"

        if is_cdread:
            # CDREAD already uploads the file, and since the priority in
            # `_get_file_path` is for the files in the python working directory,
            # we skip that function here.
            self._log.debug(
                f"Avoid uploading the file {fname} because `CDREAD` should have upload it already."
            )
            filename = fname

        else:
            # Always check if file is present as the grpc and MAPDL errors
            # are unclear
            filename = self._get_file_path(fname, progress_bar)

        time_step_stream = self._get_time_step_stream(time_step_stream)

        metadata = [
            ("time_step_stream", str(time_step_stream)),
            ("chunk_size", str(chunk_size)),
        ]

        if verbose and not is_cdread_all:
            # For 'DB'/'SOLID'/'COMB', the archive itself is a valid sequence
            # of APDL commands, so it can be streamed and run directly.
            # 'ALL' cannot take this shortcut: it first needs the IGES
            # archive imported through '/AUX15' before the CDB file is read,
            # so it always goes through the multi-command driver file below.
            request = pb_types.InputFileRequest(filename=filename)
            strouts = self._stub.InputFileS(request, metadata=metadata)
            responses = []
            for strout in strouts:
                lines = strout.cmdout
                # print out input as it is being run
                print("\n".join(lines))
                responses.extend(lines)
            response = "\n".join(responses)
            return response.strip()

        ##
        # Otherwise, not verbose (or 'CDREAD,ALL', which always needs the
        # multi-command driver file below, even when 'verbose' is requested)

        # since we can't directly run /INPUT, we have to write a
        # temporary input file that tells MAPDL to read the input
        # file.
        id_ = random_string()
        tmp_name = f"_input_tmp_{id_}_.inp"
        tmp_out = f"_input_tmp_{id_}_.out"

        if is_cdread_all:
            # 'CDREAD,ALL' restores two archives: the solid-model geometry
            # and loads (IGES format) and the rest of the database (CDB
            # format).  MAPDL itself performs this as a sequence of
            # commands, so we replicate it explicitly here instead of
            # relying on 'CDREAD' to locate the second file, since the gRPC
            # implementation is the one responsible for uploading and
            # locating both archives:
            #   /AUX15            (enter the IGES file-transfer processor)
            #   IGESIN            (import the solid-model/loads archive)
            #   FINISH            (leave /AUX15)
            #   /INPUT            (read the CDB database archive)
            #   /PREP7            (CDREAD leaves the user in /PREP7)
            fnamei = kwargs.get("fnamei")
            if not fnamei:
                raise ValueError(
                    "The 'fnamei' argument (the IGES archive) must be "
                    "supplied when using 'CDREAD' with the 'ALL' option."
                )
            tmp_dat = (
                f"/OUT,{tmp_out}\n"
                "/AUX15\n"
                f"IGESIN,'{fnamei}'\n"
                "FINISH\n"
                f"/INPUT,'{filename}'\n"
                "/PREP7\n"
                "/RMTMP\n"
                "/OUT,"
            )
            delete_uploaded_files = False

        elif is_cdread:
            # Using CDREAD
            tmp_dat = (
                f"/OUT,{tmp_out}\n{orig_cmd},'{cd_read_option}','{filename}'\n/OUT,"
            )
            delete_uploaded_files = False

        else:
            # Using default INPUT
            tmp_dat = f"/OUT,{tmp_out}\n{orig_cmd},'{filename}'\n/OUT,"
            delete_uploaded_files = True

        if write_to_log and self._apdl_log is not None:
            if not self._apdl_log.closed:
                self._apdl_log.write(tmp_dat)

        # Escaping early if inside non_interactive context. The commands are
        # executed when the context exits, so there is no need to write or
        # upload a temporary input file.
        if self._store_commands:
            # Excludes the leading and trailing '/OUT' redirection lines,
            # keeping every command in between (a single one for 'DB',
            # 'SOLID', 'COMB', and plain '/INPUT'; several for 'ALL').
            self._stored_commands.extend(tmp_dat.splitlines()[1:-1])
            return None

        if self._local:
            local_path = self.directory
            tmp_name_path = os.path.join(local_path, tmp_name)
            with open(tmp_name_path, "w") as f:
                f.write(tmp_dat)
        else:
            self._upload_raw(tmp_dat.encode(), tmp_name)

        request = pb_types.InputFileRequest(filename=tmp_name, opt="MUTE")

        # even though we don't care about the output, we still
        # need to check.  otherwise, since inputfile is
        # non-blocking, we could corrupt the service
        chunks = self._stub.InputFileS(request, metadata=metadata)
        _ = [chunk.cmdout for chunk in chunks]  # unstable

        # all output (unless redirected) has been written to a temp output
        if self._local:
            tmp_out_path = os.path.join(local_path, tmp_out)
            with open(tmp_out_path) as f:
                output = f.read()

            # delete the files to avoid overwriting:
            try:
                os.remove(tmp_name_path)
            except OSError:
                pass

            try:
                os.remove(tmp_out_path)
            except OSError:
                pass

        # otherwise, read remote file
        else:
            output = self._download_as_raw(tmp_out).decode("latin-1")

            # Deleting the previous files
            self.slashdelete(tmp_name)
            self.slashdelete(tmp_out)
            if filename in self.list_files() and delete_uploaded_files:
                self.slashdelete(filename)

        if verbose:
            # 'CDREAD,ALL' redirects its output to a file (see 'tmp_dat'
            # above) instead of streaming it, so it cannot be printed line by
            # line as it runs. Print it once fully captured instead.
            print(output)

        return output

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

    def _flush_stored(self):
        """Writes stored commands to an input file and runs the input
        file.  Used with non_interactive.
        """
        if not self._stored_commands:
            self._log.debug("There is no commands to be flushed.")
            self._store_commands = False
            return

        self._log.debug("Flushing stored commands")

        commands = "\n".join(self._stored_commands)
        if self._apdl_log:
            self._apdl_log.write(commands + "\n")

        self._log.debug(
            "Writing the following commands to a temporary apdl input file:\n%s",
            commands,
        )

        # write to a temporary input file
        def build_rand_tmp():
            return os.path.join(tempfile.gettempdir(), f"tmp_{random_string()}.inp")

        # rare case of duplicated tmpfile (birthday problem)
        tmp_filename = build_rand_tmp()
        while os.path.isfile(tmp_filename):
            tmp_filename = build_rand_tmp()

        with open(tmp_filename, "w") as fid:
            fid.writelines(commands)

        self._store_commands = False
        self._stored_commands = []

        # run the stored commands
        # already checked by run() and input_strings() when stored
        out = self._stream_input(
            tmp_filename,
            write_to_log=False,
            verbose=False,
            chunk_size=DEFAULT_CHUNKSIZE,
            progress_bar=False,
        )
        # skip the first line as it simply states that it's reading an input file
        self._response = out[out.find("LINE=       0") + 13 :]
        response_ = "\n".join(self._response.splitlines()[:20])
        self._log.info(response_)

        if not self._ignore_errors:
            self._raise_errors(self._response)

        # try/except here because MAPDL might have not closed the temp file
        try:
            os.remove(tmp_filename)
        except:
            self._log.warning("Unable to remove temporary file %s", tmp_filename)

    @protect_grpc
    def _get(  # numpydoc ignore=RT01
        self,
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        item3: MapdlFloat = "",
        it3num: MapdlFloat = "",
        item4: MapdlFloat = "",
        it4num: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> Union[float, str]:
        """Sends gRPC *Get request.

        .. warning::
           Not thread safe.  Uses ``_get_lock`` to ensure multiple
           request are not evaluated simultaneously.
        """
        if self._session_id is not None:
            self._check_session_id()

        if self._store_commands:
            raise MapdlRuntimeError(
                "Cannot use `mapdl.get_value` when in `non_interactive` mode. "
                "Exit non_interactive mode before using this method.\n\n"
                "Alternatively you can use `mapdl.get` to specify the name of "
                "the MAPDL parameter where to store the retrieved value.\n"
            )

        cmd = f"{entity},{entnum},{item1},{it1num},{item2},{it2num},{item3}, {it3num}, {item4}, {it4num}"

        # not threadsafe; don't allow multiple get commands
        timeout_ = kwargs.pop("timeout", 2)
        timeout = time.time() + timeout_
        while self._get_lock:
            time.sleep(0.001)
            if time.time() > timeout:
                raise MapdlRuntimeError(
                    f"PyMAPDL couldn't obtain 'get_lock' in {timeout_} seconds "
                    "and PyMAPDL cannot issue multiple get commands simultaneously."
                )

        self._get_lock = True
        try:
            if self._stub is None:
                raise MapdlRuntimeError("MAPDL stub not initialized")
            response = self._stub.Get(pb_types.GetRequest(getcmd=cmd))
        finally:
            self._get_lock = False

        if response.type == 0:
            self._log.debug(
                "The 'grpc' get method seems to have failed. Trying old implementation for more verbose output."
            )

            response = self.run("*GET,__temp__," + cmd, mute=False)
            self._log.debug(f"Default *get output:\n{response}")

            if response:
                from ansys.mapdl.core.misc import is_float

                if "VALUE=" in response:
                    response = response.split("VALUE=")[1].strip()

                if is_float(response):
                    return float(response)
                else:
                    return response
            else:
                raise MapdlError(
                    f"Error when processing '*get' request output.\n{response}"
                )

        if response.type == 1:
            return response.dval
        elif response.type == 2:
            return response.sval

        raise MapdlRuntimeError(f"Unsupported type {response.type} response from MAPDL")

    def download_project(
        self,
        extensions: Optional[Union[str, List[str], Tuple[str]]] = None,
        target_dir: Optional[str] = None,
        progress_bar: bool = False,
    ) -> List[str]:
        """Download all the project files located in the MAPDL working directory.

        Parameters
        ----------
        extensions : List[str], Tuple[str], optional
            List of extensions to filter the files before downloading,
            by default None.

        target_dir : str, optional
            Path to downloaded the files will to. The default is ``None``.

        progress_bar : bool, optional
            Display a progress bar using
            ``tqdm`` when ``True``.  Helpful for showing download
            progress. The default is ``False``.

        Returns
        -------
        List[Str]
            List of downloaded files.
        """
        if not extensions:
            list_of_files = self.download(
                files="*", target_dir=target_dir, progress_bar=progress_bar
            )

        else:
            list_of_files = []
            for each_extension in extensions:
                list_of_files.extend(
                    self.download(
                        files="*",
                        target_dir=target_dir,
                        extension=each_extension,
                        progress_bar=progress_bar,
                    )
                )

        return list_of_files

    def download(
        self,
        files: str | list[str] | tuple[str, ...],
        target_dir: str | None = None,
        extension: str | None = None,
        chunk_size: int | None = None,
        progress_bar: bool | None = None,
        recursive: bool = False,
    ) -> list[str]:
        """Download files from the gRPC instance working directory

        .. warning:: This feature is only available for MAPDL 2021R1 or newer.

        Parameters
        ----------
        files
            Name of the file on the server. File must be in the same
            directory as the mapdl instance. A list of string names or
            tuples of string names can also be used.
            List current files with :meth:`Mapdl.list_files <MapdlGrpc.list_files>`.

            Alternatively, you can also specify **glob expressions** to
            match file names. For example: `'file*'` to match every file whose
            name starts with `'file'`.

        target_dir
            Path where the downloaded files will be located. The default is the current
            working directory.

        extension
            Filename with this extension will be considered. The default is None.

        chunk_size
            Chunk size in bytes.  Must be less than 4MB. The default is 256 kB.

        progress_bar
            Display a progress bar using ``tqdm`` when ``True``.
            Helpful for showing download progress.

        recursive
            Whether to use recursion when using glob pattern. The default is ``False``.

        Returns
        -------
        list[str]
            List of downloaded files.

        Notes
        -----
        There are some considerations to keep in mind when using this command:

        * The glob pattern search does not search recursively in remote instances.
        * You can download a specific file located in a subdirectory of the
          MAPDL working directory by giving its relative path, for example
          ``'subdir/file.rst'``.
        * In a remote instance, it is not possible to list or download files in different
          locations than the MAPDL working directory.
        * If you are in local and provide a file path, downloading files
          from a different folder is allowed.
          However it is not a recommended approach.

        Examples
        --------
        Download a single file:

        >>> mapdl.download('file.out')

        Download all the files starting with `'file'`:

        >>> mapdl.download('file*')

        Download every single file in the MAPDL working directory:

        >>> mapdl.download('*.*')

        Alternatively, you can download all the files using
        :func:`Mapdl.download_project <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download_project>` (recommended):

        >>> mapdl.download_project()
        """
        if chunk_size is None:
            chunk_size = DEFAULT_CHUNKSIZE

        if chunk_size > 4 * 1024 * 1024:  # 4MB
            raise ValueError(
                f"Chunk sizes bigger than 4 MB can generate unstable behaviour in PyMAPDL. "
                "Please decrease ``chunk_size`` value."
            )

        if target_dir:
            try:
                os.mkdir(os.path.abspath(target_dir))
            except FileExistsError:
                pass
        else:
            target_dir = os.getcwd()

        if self._local:
            return self._download_on_local(
                files, target_dir=target_dir, extension=extension, recursive=recursive
            )

        else:  # remote session
            if recursive:
                warn(
                    "The 'recursive' parameter is ignored if the session is non-local."
                )
            return self._download_from_remote(
                files,
                target_dir=target_dir,
                extension=extension,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )

    def _download_on_local(  # numpydoc ignore=RT01
        self,
        files: Union[str, List[str], Tuple[str, ...]],
        target_dir: str,
        extension: Optional[str] = None,
        recursive: bool = False,
    ) -> List[str]:
        """Download files when we are on a local session."""
        if isinstance(files, str):
            if not os.path.isdir(self.directory / files):
                list_files = self._validate_files(
                    files, extension=extension, recursive=recursive
                )
            else:
                list_files = [files]

        elif isinstance(files, PurePath):
            list_files = [str(files)]

        elif isinstance(files, (list, tuple)):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it should only contain strings."
                )
            list_files = []
            for each in files:
                list_files.extend(
                    self._validate_files(each, extension=extension, recursive=recursive)
                )

        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported. "
                "Only strings, tuple of strings or list of strings are allowed."
            )

        return_list_files: list[str] = []
        for file in list_files:
            # file is a complete path
            basename = os.path.basename(file)
            destination = os.path.join(target_dir, basename)
            if os.path.isfile(destination):
                os.remove(destination)
                # the file might have been already downloaded.
                warn(
                    f"The file {file} has been updated in the current working directory."
                )

            if os.path.isdir(self.directory / file):
                if recursive:  # only copy the directory if recursive is true.
                    shutil.copytree(
                        self.directory / file,
                        target_dir,
                        dirs_exist_ok=True,
                    )
                    return_list_files.extend(
                        glob.iglob(target_dir + "/**/*", recursive=recursive)
                    )

            else:
                return_list_files.append(destination)
                shutil.copy(
                    self.directory / file,
                    destination,
                )

        return return_list_files

    def _download_from_remote(  # numpydoc ignore=RT01
        self,
        files: Union[str, List[str], Tuple[str, ...]],
        target_dir: str,
        extension: Optional[str] = None,
        chunk_size: Optional[int] = None,
        progress_bar: Optional[bool] = None,
    ) -> List[str]:
        """Download files when we are connected to a remote session."""

        if isinstance(files, str):
            list_files = self._validate_files(files, extension=extension)

        elif isinstance(files, list):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it should only contain strings."
                )
            list_files = []
            for each in files:
                list_files.extend(self._validate_files(each, extension=extension))

        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported. "
                "Only strings, tuple of strings or list of strings are allowed."
            )

        for each_file in list_files:
            safe_relative_file = self._validate_remote_relative_path(each_file)
            out_file_name = os.path.join(target_dir, safe_relative_file)
            # 'each_file' might include subdirectories (relative to the
            # MAPDL working directory), which might not exist yet locally.
            os.makedirs(os.path.dirname(out_file_name) or ".", exist_ok=True)
            self._download(
                safe_relative_file,
                out_file_name=out_file_name,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )

        return list_files

    @staticmethod
    def _validate_remote_relative_path(path: str) -> str:
        """Validate a relative remote file path to keep downloads in target_dir."""
        normalized_path = os.path.normpath(path.replace("\\", "/"))
        normalized = PurePosixPath(normalized_path)

        if normalized.is_absolute():
            raise ValueError(
                f"Path '{path}' is invalid. Absolute paths are not allowed for remote downloads."
            )

        if ".." in normalized.parts:
            raise ValueError(
                f"Path '{path}' is invalid. Parent directory references are not allowed."
            )

        if normalized.parts and re.match(r"^[a-zA-Z]:$", normalized.parts[0]):
            raise ValueError(
                f"Path '{path}' is invalid. Drive-letter paths are not allowed for remote downloads."
            )

        if str(normalized) in [".", ""]:
            raise ValueError(f"Path '{path}' is invalid.")

        return str(normalized)

    def _validate_files(
        self, file: str, extension: Optional[str] = None, recursive: bool = True
    ) -> List[str]:
        if extension is not None:
            if not isinstance(extension, str):
                raise TypeError(f"The extension {extension} must be a string.")

            if not extension.startswith("."):
                extension = "." + extension

        else:
            extension = ""

        # A glob pattern (with '*', '?' or '[') requires listing the
        # directory content to filter against.
        is_glob = bool(re.search(r"[*?\[]", file))
        # A path with a directory component (for example
        # ``tmp_dir/file.rst``) points inside a subdirectory of the working
        # directory.
        has_subdir = bool(os.path.dirname(file))

        if self.is_local:
            # filtering with glob (accepting *)
            if not os.path.isabs(file):
                # Relative paths (including ones with subdirectories) are
                # resolved against the MAPDL working directory.
                file = str(self.directory / file)
            list_files = glob.glob(file + extension, recursive=recursive)

        elif is_glob or not has_subdir:
            # Either a glob pattern, or a plain filename in the top level of
            # the working directory: both can be validated against
            # ``list_files``.
            base_name = os.path.basename(file + extension)
            self_files = self.list_files()

            list_files = fnmatch.filter(self_files, base_name)

        else:
            # Literal file path inside a subdirectory of the working
            # directory. ``list_files`` only returns the top level of the
            # working directory, so it cannot be used to validate files in
            # subdirectories.
            file_to_check = self._validate_remote_relative_path(file + extension)
            list_files = (
                [file_to_check] if self.inquire("", "EXIST", file_to_check) else []
            )

        # filtering by extension
        list_files = [file for file in list_files if file.endswith(extension)]

        if len(list_files) == 0:
            raise FileNotFoundError(
                f"No file matching '{file}' in the MAPDL session can be found."
            )

        return list_files

    @protect_grpc
    def _download(
        self,
        target_name: str,
        out_file_name: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNKSIZE,
        progress_bar: bool = False,
    ) -> None:
        """Download a file from the gRPC instance.

        Parameters
        ----------
        target_name : str
            Target file on the server. File must be in the same
            directory as the mapdl instance. List current files with
            ``mapdl.list_files()``

        out_file_name : str, optional
            Save the filename as a different name other than the
            ``target_name``.

        chunk_size : int, optional
            Chunk size in bytes.  Must be less than 4MB.  The default is 256 kB.

        progress_bar : bool, optional
            Display a progress bar using ``tqdm`` when ``True``.
            Helpful for showing download progress. The default is
            ``False`` to avoid excessive command printout.

        Examples
        --------
        Download the remote result file "file.rst" as "my_result.rst"

        >>> mapdl.download('file.rst', 'my_result.rst')
        """

        if progress_bar and _HAS_TQDM:
            progress_bar = True

        if out_file_name is None:
            out_file_name = target_name

        request = pb_types.DownloadFileRequest(name=target_name)
        metadata = [
            ("time_step_stream", "200"),
            ("chunk_size", str(chunk_size)),
        ]
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        chunks = self._stub.DownloadFile(request, metadata=metadata)
        file_size = save_chunks_to_file(
            chunks,
            out_file_name,
            progress_bar=progress_bar,
            target_name=target_name,
        )

        if not file_size:
            if target_name not in self.list_files():
                warn(f'File "{target_name}" does not exist.')
            else:
                warn(f'File "{target_name}" is empty.')

    @protect_grpc
    def upload(self, file_name: str, progress_bar: bool = _HAS_TQDM) -> str:
        """Upload a file to the grpc instance

        file_name : str
            Local file to upload.

        progress_bar : bool, optional
            Whether to display a progress bar using ``tqdm``. The default is ``True``.
            This parameter is helpful for showing download progress.

        Returns
        -------
        str
            Base name of the file uploaded.  File can be accessed
            relative to the mapdl instance with this file name.

        Examples
        --------
        Upload "local_file.inp" while disabling the progress bar

        >>> mapdl.upload('local_file.inp', progress_bar=False)
        """
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Unable to locate filename {file_name}")
        self._log.debug(f"Uploading file '{file_name}' to the MAPDL instance.")

        chunks_generator = get_file_chunks(file_name, progress_bar=progress_bar)
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        response = self._stub.UploadFile(chunks_generator)

        if not response.length:
            raise IOError("File failed to upload")
        return os.path.basename(file_name)

    def _get_array_from_service(
        self,
        entity,
        entnum,
        item1,
        it1num,
        item2,
        it2num,
        kloop,
    ) -> NDArray[np.float64]:
        """Return an eager ``*VGET`` result through the gRPC service."""
        while self._vget_lock:
            time.sleep(0.001)
        self._vget_lock = True

        cmd = f"{entity},{entnum},{item1},{it1num},{item2},{it2num},{kloop}"
        try:
            if self._stub is None:
                raise MapdlRuntimeError("MAPDL stub not initialized")
            chunks = self._stub.VGet2(pb_types.GetRequest(getcmd=cmd))
            return parse_chunks(chunks)
        finally:
            self._vget_lock = False

    @protect_grpc
    def _get_array(
        self,
        entity="",
        entnum="",
        item1="",
        it1num="",
        item2="",
        it2num="",
        kloop="",
        **kwargs,
    ) -> Union[NDArray[np.float64], LazyArray]:
        """Populate a private MAPDL parameter and return it lazily.

        The ``*VGET`` command is issued immediately so the result reflects the
        selection at call time, even if the selection changes before the values
        are used. Only the download is deferred. On first use, the values are
        read with a binary ``*GET`` plus ``mwrite`` rather than by parsing
        ``*STATUS,PRM_`` output.
        """
        if "parm" in kwargs:
            raise ValueError("Parameter name `parm` not supported with gRPC")
        if str(item1).strip().upper() == "ETAB":
            return self._get_array_from_service(
                entity, entnum, item1, it1num, item2, it2num, kloop
            )
        parameter_name = self._new_lazy_array_parameter()
        try:
            output = self.starvget(
                parameter_name,
                entity,
                entnum,
                item1,
                it1num,
                item2,
                it2num,
                kloop,
                mute=False,
            )
        except Exception as error:
            try:
                self._delete_lazy_array_parameter(parameter_name)
            except Exception as cleanup_error:
                raise cleanup_error from error
            raise

        if "the dimension number 1 is 0" in output:
            self._delete_lazy_array_parameter(parameter_name)
            return np.empty(0)

        return LazyArray(
            self,
            parameter_name,
            cleanup=lambda: self._delete_lazy_array_parameter(parameter_name),
            fetch=lambda: self._read_owned_array_parameter(parameter_name),
            flatten=True,
        )

    def _screenshot_path(self):  # numpydoc ignore=RT01
        """Returns the local path of the MAPDL generated screenshot.

        If necessary, downloads the remotely rendered file.
        """
        if self._local:
            return super()._screenshot_path()

        jobname = self.jobname
        filenames = [
            filename
            for filename in self.list_files()
            if filename.endswith(".png") and filename.startswith(jobname)
        ]
        filenames.sort()
        filename = os.path.basename(filenames[-1])

        temp_dir = tempfile.gettempdir()
        save_name = os.path.join(temp_dir, "tmp.png")
        self._download(filename, out_file_name=save_name)
        return save_name

    @protect_grpc
    def _download_as_raw(self, target_name: str) -> str:  # numpydoc ignore=RT01
        """Download a file from the gRPC instance as a binary
        string without saving it to disk.
        """
        request = pb_types.DownloadFileRequest(name=target_name)
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        chunks = self._stub.DownloadFile(request)
        return b"".join([chunk.payload for chunk in chunks])

    @property
    def xpl(self) -> "ansXpl":
        """MAPDL file explorer

        Iteratively navigate through MAPDL files.

        Returns
        -------
        :class:`ansXpl <ansys.mapdl.core.xpl.ansXpl>`
            An instance of :class:`ansXpl <ansys.mapdl.core.xpl.ansXpl>`.

        Examples
        --------
        Read the MASS record from the "file.full" file

        >>> from ansys import Mapdl
        >>> mapdl = Mapdl()
        >>> xpl = mapdl.xpl
        >>> xpl.open('file.full')
        >>> vec = xpl.read('MASS')
        >>> vec.asarray()
        array([ 4,  7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52,
               55, 58,  1], dtype=int32)
        """
        if self._xpl is None:
            from ansys.mapdl.core.xpl import ansXpl

            self._xpl = ansXpl(self)
        return self._xpl

    @protect_grpc
    def scalar_param(self, pname: str) -> float:
        """Return a scalar parameter as a float.

        If parameter does not exist, returns ``None``.

        Returns
        -------
        float or None
            The value of the parameter as a float or ``None`` if the
            parameter does not exist.
        """
        request = pb_types.ParameterRequest(name=pname, array=False)
        if self._stub is None:
            raise MapdlRuntimeError("MAPDL stub not initialized")
        presponse = self._stub.GetParameter(request)
        if presponse.val:
            return float(presponse.val[0])

    @protect_grpc
    def _upload_raw(self, raw, save_as):  # consider private
        """Upload a binary string as a file"""
        chunks = chunk_raw(raw, save_as)
        response = self._stub.UploadFile(chunks)
        if response.length != len(raw):
            raise IOError("Raw Bytes failed to upload")

    # TODO: not fully tested/implemented
    @protect_grpc
    def Param(self, pname):
        presponse = self._stub.GetParameter(pb_types.ParameterRequest(name=pname))
        return presponse.val

    # TODO: not fully tested/implemented
    @protect_grpc
    def Var(self, num):
        presponse = self._stub.GetVariable(pb_types.VariableRequest(inum=num))
        return presponse.val

    @property
    def math(self):
        """Interface to launch PyAnsys Math from PyMAPDL.

         Returns
        -------
        :class:`MapdlMath <ansys.mapdl.core.math.MapdlMath>`
            MAPDL Math interface.

        Examples
        --------
        Get the stiffness matrix from MAPDL
        >>> mm = mapdl.math
        >>> k = mm.stiff()
        >>> k.asarray()
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>

        Get the mass matrix from MAPDL
        >>> mm = mapdl.math
        >>> m = mm.stiff()
        >>> m.asarray()
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>
        """
        if self._math is None:
            from ansys.math.core.math import AnsMath

            self._math = AnsMath(self)

        return self._math

    @property
    def krylov(self):
        """APDL krylov interface.

        For more information, see the :class:`KrylovSolver <ansys.mapdl.core.krylov.KrylovSolver>`

        Returns
        -------
        :class:`Krylov class <ansys.mapdl.core.krylov.KrylovSolver>`
            An instance of :class:`Krylov class <ansys.mapdl.core.krylov.KrylovSolver>`
        """
        if self._krylov is None:
            from ansys.mapdl.core.krylov import KrylovSolver

            self._krylov = KrylovSolver(self)

        return self._krylov

    @property
    def db(self):
        """
        MAPDL database interface.

        Returns
        -------
        :class:`MapdlDb <ansys.mapdl.core.database.MapdlDb>`
            MAPDL database interface.

        Examples
        --------
        Create a nodes instance.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> # create nodes...
        >>> nodes = mapdl.db.nodes
        >>> print(nodes)
        MAPDL Database Nodes
            Number of nodes:          270641
            Number of selected nodes: 270641
            Maximum node number:      270641

        >>> mapdl.nsel("NONE")
        >>> print(nodes)
        MAPDL Database Nodes
            Number of nodes:          270641
            Number of selected nodes: 0
            Maximum node number:      270641

        Return the selection status and the coordinates of node 22.

        >>> nodes = mapdl.db.nodes
        >>> sel, coord = nodes.coord(22)
        >>> coord
        (1.0, 0.5, 0.0, 0.0, 0.0, 0.0)
        """
        from ansys.mapdl.core.database import MapdlDb

        if self._db is None:
            self._db = MapdlDb(self)
            self._db.start()

        return self._db

    @protect_grpc
    def _data_info(self, pname):  # numpydoc ignore=RT01
        """Returns the data type of a parameter

        APDLMATH vectors only.
        """
        request = pb_types.ParameterRequest(name=pname)
        return self._stub.GetDataInfo(request)

    @protect_grpc
    def _vec_data(self, pname):  # numpydoc ignore=RT01
        """Downloads vector data from a MAPDL MATH parameter"""
        dtype = ANSYS_VALUE_TYPE[self._data_info(pname).stype]
        request = pb_types.ParameterRequest(name=pname)
        chunks = self._stub.GetVecData(request)
        return parse_chunks(chunks, dtype)

    @protect_grpc
    def _mat_data(self, pname, raw=False):  # numpydoc ignore=RT01
        """Downloads matrix data from a parameter and returns a scipy sparse array"""
        try:
            from scipy import sparse
        except ImportError:  # pragma: no cover
            raise ImportError("Install ``scipy`` to use this feature") from None

        minfo = self._data_info(pname)
        stype = ANSYS_VALUE_TYPE[minfo.stype]
        mtype = minfo.objtype
        shape = (minfo.size1, minfo.size2)

        if mtype == 2:  # dense
            request = pb_types.ParameterRequest(name=pname)
            chunks = self._stub.GetMatData(request)
            values = parse_chunks(chunks, stype)
            return np.transpose(np.reshape(values, shape[::-1]))
        elif mtype == 3:  # sparse
            indptr = self._vec_data(pname + "::ROWS")
            indices = self._vec_data(pname + "::COLS")
            vals = self._vec_data(pname + "::VALS")
            if raw:  # for debug
                return vals, indices, indptr, shape
            else:
                return sparse.csr_matrix(
                    (vals, indices, indptr), dtype=stype, shape=shape
                )

        raise ValueError(f'Invalid matrix type "{mtype}"')

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

    @supress_logging
    @run_as("PREP7")
    def _generate_iges(self):
        """Save IGES geometry representation to disk.

        Returns
        -------
        str
            The filename of the saved IGES representation.
        """
        basename = "_tmp.iges"
        if self._local:
            filename = self.directory / basename
            self.igesout(basename, att=1)
        else:
            self.igesout(basename, att=1)
            filename = os.path.join(tempfile.gettempdir(), basename)
            self._download(basename, filename, progress_bar=False)
        return filename

    @property
    def _distributed_result_file(self):  # numpydoc ignore=RT01
        """Path of the distributed result file."""
        if not self._distributed:
            return

        try:
            filename = self.inquire("", "RSTFILE")
            if not filename:
                filename = self.jobname
        except:
            filename = self.jobname

        # ansys decided that a jobname ended in a number needs a bonus "_"
        if filename[-1].isnumeric():
            filename += "_"

        rth_basename = "%s0.%s" % (filename, "rth")
        rst_basename = "%s0.%s" % (filename, "rst")

        rth_file = self.directory / rth_basename
        rst_file = self.directory / rst_basename

        if self._prioritize_thermal:
            if not os.path.isfile(rth_file):
                raise FileNotFoundError("Thermal Result not available")
            return rth_file

        if os.path.isfile(rth_file) and os.path.isfile(rst_file):
            return last_created([rth_file, rst_file])
        elif os.path.isfile(rth_file):
            return rth_file
        elif os.path.isfile(rst_file):
            return rst_file

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

    def list_error_file(self) -> str | None:
        """Listing of errors written in JOBNAME.err

        Returns
        -------
        str
            Contents of the error file or None if not found.
        """
        files = self.list_files()
        jobname = self.jobname
        error_file = None
        for test_file in [f"{jobname}.err", f"{jobname}0.err"]:
            if test_file in files:
                error_file = test_file
                break

        if not error_file:
            return None

        if self._local:
            return open(self.directory / error_file).read()
        elif self._exited:
            raise MapdlExitedError(
                "Cannot list error file when MAPDL Service has exited"
            )

        return self._download_as_raw(error_file).decode("latin-1")

    @wraps(MapdlBase.cmatrix)
    def cmatrix(  # numpydoc ignore=RT01
        self,
        symfac="",
        condname="",
        numcond="",
        grndkey="",
        capname="",
        **kwargs,
    ):
        """Run CMATRIX in non-interactive mode and return the response from file."""

        # The CMATRIX command needs to run in non-interactive mode
        if not self._store_commands:
            with self.non_interactive:
                super().cmatrix(symfac, condname, numcond, grndkey, capname, **kwargs)
            self._response = self._download_as_raw("cmatrix.out").decode()
            return self._response

        # otherwise, simply run cmatrix as we're already in
        # non-interactive and there's no output to return
        super().cmatrix(symfac, condname, numcond, grndkey, capname, **kwargs)

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

    def _new_lazy_array_parameter(self) -> str:
        """Reserve an unused, valid MAPDL parameter name for a lazy result."""
        prefix = self._lazy_array_prefix
        while True:
            self._lazy_array_counter += 1
            candidate = f"{prefix}{self._lazy_array_counter:016X}"
            if len(candidate) > MAX_PARAM_CHARS:  # pragma: no cover
                raise MapdlRuntimeError("Unable to generate a valid lazy-array name.")

            # Include parameters hidden by display settings while checking so
            # a user parameter cannot be overwritten.
            with self.parameters.full_parameters_output:
                if candidate not in self.parameters:
                    self._lazy_array_parameters.add(candidate)
                    return candidate

    def _delete_lazy_array_parameter(self, parameter_name: str) -> None:
        """Delete an owned lazy-result parameter and unregister it."""
        self.run(f"{parameter_name}=", mute=True)
        self._lazy_array_parameters.remove(parameter_name)

    def _cleanup_lazy_array_parameters(self) -> None:
        """Delete every unresolved lazy-result parameter."""
        for parameter_name in tuple(getattr(self, "_lazy_array_parameters", ())):
            self._delete_lazy_array_parameter(parameter_name)

    def _read_owned_array_parameter(self, parameter_name: str) -> NDArray[np.float64]:
        """Download an owned column-vector parameter without parsing ``*STATUS``.

        The row count is read with a binary ``*GET`` query and the values are
        streamed with ``mwrite``, so this avoids the version-fragile
        ``*STATUS,PRM_`` listing that
        :meth:`Parameters.__getitem__ <ansys.mapdl.core.parameters.Parameters.__getitem__>`
        performs to discover the array shape.

        The result keeps the ``(rows, 1)`` shape that ``Parameters`` returns for
        ``*VGET`` parameters, so ``get_variable`` results are unchanged.
        ``get_array`` flattens it through ``LazyArray(flatten=True)``.
        """
        rows = int(self.get_value("PARM", parameter_name, "DIM", 1))
        if rows == 0:
            return np.empty(0)
        return self.parameters._get_parameter_array(parameter_name, (rows, 1))

    @wraps(MapdlBase.vget)
    def vget(  # numpydoc ignore=RT01
        self,
        par: str = "",
        ir: MapdlInt = "",
        tstrt: MapdlFloat = "",
        kcplx: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Wraps VGET and returns its values eagerly."""
        super().vget(par=par, ir=ir, tstrt=tstrt, kcplx=kcplx, **kwargs)
        if self._store_commands:
            return None
        return self.parameters[par]

    def get_variable(
        self,
        ir: MapdlInt = "",
        tstrt: MapdlFloat = "",
        kcplx: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> LazyArray:
        """
        Obtain the POST26 time-history variable values lazily.

        This method uses the ``VGET`` command to copy a POST26 variable
        (for example, one created with
        :func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` or
        :func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`) into a private
        MAPDL array parameter. On gRPC connections, the returned
        :class:`LazyArray <ansys.mapdl.core.lazy_array.LazyArray>` downloads
        its values, and releases that private parameter, only when it is
        first used.

        Parameters
        ----------
        ir : int, optional
            Reference number of the variable (1 to NV [NUMVAR]). This is
            the same ``nvar`` reference number used when defining the
            variable, for example with
            :func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` or
            :func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`.

        tstrt : float, optional
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used. By default, retrieval starts at
            0.0.

        kcplx : int, optional
            Complex number key:

            * ``0`` - Use the real part of the IR data. Default.

            * ``1`` - Use the imaginary part of the IR data.

        Returns
        -------
        LazyArray
            Variable values downloaded from MAPDL when first used. Use
            :func:`numpy.asarray` or :meth:`LazyArray.resolve` to materialize
            the values explicitly.

        Examples
        --------
        Define a POST26 variable with
        :func:`Mapdl.nsol() <ansys.mapdl.core.Mapdl.nsol>` for the ``UX``
        displacement of node 1, and then retrieve its values with
        ``get_variable``.

        >>> mapdl.post26()
        >>> mapdl.nsol(2, 1, "U", "X")
        >>> np.asarray(mapdl.get_variable(2))
        array([0.        , 0.00108135, 0.00300901, ..., 0.03407310])

        The same works for element results defined with
        :func:`Mapdl.esol() <ansys.mapdl.core.Mapdl.esol>`, using
        ``tstrt`` to skip the initial time (or frequency) values.

        >>> mapdl.esol(3, 1, 1, "S", "Y")
        >>> np.asarray(mapdl.get_variable(3, tstrt=1.0))
        array([0.34632451, 0.36126732, ..., 0.38041256])
        """
        parameter_name = self._new_lazy_array_parameter()
        try:
            super().vget(
                par=parameter_name,
                ir=ir,
                tstrt=tstrt,
                kcplx=kcplx,
                **kwargs,
            )
        except Exception as error:
            try:
                self._delete_lazy_array_parameter(parameter_name)
            except Exception as cleanup_error:
                raise cleanup_error from error
            raise

        return LazyArray(
            self,
            parameter_name,
            cleanup=lambda: self._delete_lazy_array_parameter(parameter_name),
            fetch=lambda: self._read_owned_array_parameter(parameter_name),
        )

    @wraps(MapdlBase.nsol)
    def nsol(  # numpydoc ignore=RT01
        self,
        nvar: MapdlInt = VAR_IR,
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Wraps NSOL to return the variable as an array."""
        super().nsol(
            nvar=nvar,  # type: ignore[arg-type]
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            **kwargs,
        )
        return self.vget("_temp", nvar)  # type: ignore[arg-type]

    @wraps(MapdlBase.esol)
    def esol(  # numpydoc ignore=RT01
        self,
        nvar: MapdlInt = VAR_IR,
        elem: MapdlInt = "",
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Wraps ESOL to return the variable as an array."""
        super().esol(
            nvar=nvar,  # type: ignore[arg-type]
            elem=elem,
            node=node,
            item=item,
            comp=comp,
            name=name,
            **kwargs,
        )
        return self.vget("_temp", nvar)  # type: ignore[arg-type]

    @wraps(MapdlBase.rpsd)
    def rpsd(  # numpydoc ignore=RT01
        self,
        ir: str = "",
        ia: str = "",
        ib: str = "",
        itype: int | str = "",
        datum: int | str = "",
        name: str = "",
        signif: str = "",
        **kwargs,
    ) -> NDArray[np.float64]:
        """Wraps RPSD to return the variable as an array."""
        super().rpsd(
            ir=ir,
            ia=ia,
            ib=ib,
            itype=itype,
            datum=datum,
            name=name,
            signif=signif,
            **kwargs,
        )
        return self.vget("_temp", ir)  # type: ignore[arg-type]

    def get_nsol(
        self,
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """
        Get NSOL solutions

        Parameters
        ----------
        node : int
            Node for which data is to be stored.

        item : str
            Label identifying the item.  Valid item labels are shown in the
            table below. Some items also require a component label.

        comp : str
            Component of the item (if required).  Valid component labels are
            shown in the table below.

        name : str, optional
            Thirty-two character name identifying the item on printouts and
            displays.  The default is a label formed by concatenating the first
            four characters of the ``item`` and ``comp`` labels.

        sector : int, optional
            For a full harmonic cyclic symmetry solution, the sector number for
            which the results from NODE are to be stored.

        Returns
        -------
        numpy.ndarray
            Variable values

        Notes
        -----
        By default, this command store temporally the variable on the
        variable number set by ``VAR_IR`` in the class MapdlGrpc.
        Therefore, any variable in that slot will be deleted when using
        this command.

        Stores nodal degree of freedom and solution results in a variable. For
        more information, see Data Interpreted in the Nodal Coordinate System
        in the Modeling and Meshing Guide.

        For SECTOR>1, the result is in the nodal coordinate system of the base
        sector, and it is rotated to the expanded sector’s location. Refer to
        Using the /CYCEXPAND Command in the Cyclic Symmetry Analysis Guide for
        more information.

        For SHELL131 and SHELL132 elements with KEYOPT(3) = 0 or 1, use the
        labels TBOT, TE2, TE3, . . ., TTOP instead of TEMP.
        """
        return self.nsol(
            VAR_IR,  # type: ignore[arg-type]
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            **kwargs,
        )

    def get_esol(
        self,
        elem: MapdlInt = "",
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        sector: MapdlInt = "",
        tstrt: MapdlFloat = "",
        kcplx: MapdlInt = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Get ESOL data.

        /POST26 APDL Command: ESOL

        Parameters
        ----------
        elem : int
            Element for which data are to be stored.

        node : int
            Node number on this element for which data are to be
            stored. If blank, store the average element value (except
            for ``FMAG`` values, which are summed instead of averaged).

        item : str
            Label identifying the item. Some items also require a component label.

        comp : str
            Component of the item (if required). If Comp is a sequence number (n),
            the ``NODE`` field will be ignored.

        name : str, optional
            Thirty-two character name for identifying the item on the
            printout and displays.  The default is a label formed by
            concatenating the first four characters of the ``item`` and
            ``comp`` labels.

        tstrt : str, optional
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used. By default it is the first value.

        kcplx : str, optional
            Complex number key:

            * ``0`` - Use the real part of the IR data. Default.

            * ``1`` - Use the imaginary part of the IR data.

        Returns
        -------
        numpy.ndarray
            Variable values

        Notes
        -----
        By default, this command store temporally the variable on the
        variable number set by ``VAR_IR`` in the class
        :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>`
        Therefore, any variable in that slot will be deleted when using
        this command.

        The ``ESOL`` command defines element results data to be stored
        from a results file (``FILE``). Not all items are valid for all
        elements. To see the available items for a given element,
        refer to the input and output summary tables in the
        documentation for that element.

        Two methods of data access are available via the ``ESOL``
        command. You can access some simply by using a generic label
        (component name method), while others require a label and
        number (sequence number method).

        Use the component name method to access general element data
        (that is, element data generally available to most element
        types or groups of element types).

        The sequence number method is required for data that is not
        averaged (such as pressures at nodes and temperatures at
        integration points), or data that is not easily described in a
        generic fashion (such as all derived data for structural line
        elements and contact elements, all derived data for thermal
        line elements, and layer data for layered elements).

        Element results are in the element coordinate system, except
        for layered elements where results are in the layer coordinate
        system.  Element forces and moments are in the nodal
        coordinate system. Results are obtainable for an element at a
        specified node. Further location specifications can be made
        for some elements via the ``SHELL``, ``LAYERP26``, and ``FORCE`` commands.

        For more information on the meaning of contact status and its
        possible values, see Reviewing Results in ``POST1`` in the Contact
        Technology Guide.
        """
        self.esol(
            VAR_IR,  # type: ignore[arg-type]
            elem=elem,
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            **kwargs,
        )
        # Materialize the private result to preserve this method's ndarray API.
        return self.get_variable(VAR_IR, tstrt=tstrt, kcplx=kcplx).resolve()
