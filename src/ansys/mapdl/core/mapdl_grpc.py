"""gRPC specific class and methods for the MAPDL gRPC client """

import fnmatch
from functools import wraps
import glob
import io
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import threading
import time
from typing import Optional
import warnings
from warnings import warn
import weakref

from ansys.tools.versioning.utils import version_string_as_tuple
import grpc
from grpc._channel import _InactiveRpcError, _MultiThreadedRendezvous
import numpy as np
import psutil

MSG_IMPORT = """There was a problem importing the ANSYS MAPDL API module `ansys-api-mapdl`.
Please make sure you have the latest updated version using:

'pip install ansys-api-mapdl' or 'pip install --upgrade ansys-api-mapdl'

If this does not solve it, please reinstall 'ansys.mapdl.core'
or contact Technical Support at 'https://github.com/pyansys/pymapdl'."""


try:
    from ansys.api.mapdl.v0 import ansys_kernel_pb2 as anskernel
    from ansys.api.mapdl.v0 import mapdl_pb2 as pb_types
    from ansys.api.mapdl.v0 import mapdl_pb2_grpc as mapdl_grpc
except ImportError:  # pragma: no cover
    raise ImportError(MSG_IMPORT)

from ansys.mapdl.core import _LOCAL_PORTS, __version__
from ansys.mapdl.core.common_grpc import (
    ANSYS_VALUE_TYPE,
    DEFAULT_CHUNKSIZE,
    DEFAULT_FILE_CHUNK_SIZE,
    parse_chunks,
)
from ansys.mapdl.core.errors import (
    MapdlConnectionError,
    MapdlExitedError,
    MapdlRuntimeError,
    protect_grpc,
)
from ansys.mapdl.core.mapdl import _MapdlCore
from ansys.mapdl.core.mapdl_types import MapdlInt
from ansys.mapdl.core.misc import (
    check_valid_ip,
    last_created,
    random_string,
    requires_package,
    run_as_prep7,
    supress_logging,
)

# Checking if tqdm is installed.
# If it is, the default value for progress_bar is true.
try:
    from tqdm import tqdm

    _HAS_TQDM = True
except ModuleNotFoundError:  # pragma: no cover
    _HAS_TQDM = False

TMP_VAR = "__tmpvar__"
VOID_REQUEST = anskernel.EmptyRequest()

# Default 256 MB message length
MAX_MESSAGE_LENGTH = int(os.environ.get("PYMAPDL_MAX_MESSAGE_LENGTH", 256 * 1024**2))

VAR_IR = 9  # Default variable number for automatic variable retrieving (/post26)


def chunk_raw(raw, save_as):
    with io.BytesIO(raw) as f:
        while True:
            piece = f.read(DEFAULT_FILE_CHUNK_SIZE)
            length = len(piece)
            if length == 0:
                return
            yield pb_types.UploadFileRequest(
                file_name=os.path.basename(save_as),
                chunk=anskernel.Chunk(payload=piece, size=length),
            )


def get_file_chunks(filename, progress_bar=False):
    """Serializes a file into chunks"""
    pbar = None
    if progress_bar:
        if not _HAS_TQDM:  # pragma: no cover
            raise ModuleNotFoundError(
                "To use the keyword argument 'progress_bar', you need to have "
                "installed the `tqdm` package. "
                "To avoid this message set `progress_bar=False`."
            )

        n_bytes = os.path.getsize(filename)

        base_name = os.path.basename(filename)
        pbar = tqdm(
            total=n_bytes,
            desc=f"Uploading {base_name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

    with open(filename, "rb") as f:
        while True:
            piece = f.read(DEFAULT_FILE_CHUNK_SIZE)
            length = len(piece)
            if length == 0:
                if pbar is not None:
                    pbar.close()
                return

            if pbar is not None:
                pbar.update(length)

            chunk = anskernel.Chunk(payload=piece, size=length)
            yield pb_types.UploadFileRequest(
                file_name=os.path.basename(filename), chunk=chunk
            )


def save_chunks_to_file(
    chunks, filename, progress_bar=False, file_size=None, target_name=""
):
    """Saves chunks to a local file

    Returns
    -------
    file_size : int
        File size saved in bytes.  ``0`` means no file was written.
    """
    pbar = None
    if progress_bar:
        if not _HAS_TQDM:  # pragma: no cover
            raise ModuleNotFoundError(
                f"To use the keyword argument 'progress_bar', you need to have installed the 'tqdm' package."
                "To avoid this message you can set 'progress_bar=False'."
            )

        pbar = tqdm(
            total=file_size,
            desc="Downloading %s" % target_name,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

    file_size = 0
    with open(filename, "wb") as f:
        for chunk in chunks:
            f.write(chunk.payload)
            payload_size = len(chunk.payload)
            file_size += payload_size
            if pbar is not None:
                pbar.update(payload_size)

    if pbar is not None:
        pbar.close()

    return file_size


class RepeatingTimer(threading.Timer):
    """Run a function repeately"""

    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class MapdlGrpc(_MapdlCore):
    """This class connects to a GRPC MAPDL server and allows commands
    to be passed to a persistent session.

    Parameters
    ----------
    ip : str, optional
        IP address to connect to the server.  The default is 'localhost'.

    port : int, optional
        Port to connect to the MAPDL server.  The default is ``50052``.

    timeout : float
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

    channel : grpc.Channel, optional
        gRPC channel to use for the connection. Can be used as an
        alternative to the ``ip`` and ``port`` parameters.

    remote_instance : ansys.platform.instancemanagement.Instance
        The corresponding remote instance when MAPDL is launched through
        PyPIM. This instance will be deleted when calling
        :func:`Mapdl.exit <ansys.mapdl.core.Mapdl.exit>`.

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
    _ip = None
    _port = None

    def __init__(
        self,
        ip=None,
        port=None,
        timeout=15,
        loglevel="WARNING",
        log_file=False,
        cleanup_on_exit=False,
        log_apdl=None,
        set_no_abort=True,
        remove_temp_files=None,
        remove_temp_dir_on_exit=False,
        print_com=False,
        channel=None,
        remote_instance=None,
        **start_parm,
    ):
        """Initialize connection to the mapdl server"""
        if remove_temp_files is not None:  # pragma: no cover
            warnings.warn(
                "The option ``remove_temp_files`` is being deprecated and it will be removed by PyMAPDL version 0.66.0.\n"
                "Please use ``remove_temp_dir_on_exit`` instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            remove_temp_dir_on_exit = remove_temp_files
            remove_temp_files = None

        self.__distributed = None
        self._remote_instance = remote_instance

        if channel is not None:
            if ip is not None or port is not None:
                raise ValueError(
                    "If `channel` is specified, neither `port` nor `ip` can be specified."
                )
        if ip is None:
            ip = "127.0.0.1"

        # port and ip are needed to setup the log
        self._port = port

        check_valid_ip(ip)
        self._ip = ip

        super().__init__(
            loglevel=loglevel,
            log_apdl=log_apdl,
            log_file=log_file,
            print_com=print_com,
            **start_parm,
        )
        self._mode = "grpc"

        # gRPC request specific locks as these gRPC request are not thread safe
        self._vget_lock = False
        self._get_lock = False

        self._prioritize_thermal = False
        self._locked = False  # being used within MapdlPool
        self._stub = None
        self._cleanup = cleanup_on_exit
        self.__remove_temp_dir_on_exit = remove_temp_dir_on_exit
        self._jobname = start_parm.get("jobname", "file")
        self._path = start_parm.get("run_location", None)
        self._busy = False  # used to check if running a command on the server
        self._local = ip in ["127.0.0.1", "127.0.1.1", "localhost"]
        if "local" in start_parm:  # pragma: no cover  # allow this to be overridden
            self._local = start_parm["local"]
        self._health_response_queue = None
        self._exiting = False
        self._exited = None
        self._mute = False
        self._db = None
        self.__server_version = None

        # saving for later use (for example open_gui)
        start_parm["ip"] = ip
        start_parm["port"] = port
        self._start_parm = start_parm

        if port is None:
            from ansys.mapdl.core.launcher import MAPDL_DEFAULT_PORT

            port = MAPDL_DEFAULT_PORT
        self._state = None
        self._stub = None
        self._timeout = timeout
        self._pids = []

        if channel is None:
            self._log.debug("Creating channel to %s:%s", ip, port)
            self._channel = self._create_channel(ip, port)
        else:
            self._log.debug("Using provided channel")
            self._channel = channel

        # connect and validate to the channel
        self._mapdl_process = start_parm.pop("process", None)

        # Queueing the stds
        if self._mapdl_process:
            self._create_process_stds_queue()

        try:
            self._multi_connect(timeout=timeout)
        except MapdlConnectionError as err:  # pragma: no cover
            self._post_mortem_checks()
            self._log.debug(
                "The error wasn't catch by the post-mortem checks.\nThe stdout is printed now:"
            )
            self._log.debug(self._stdout)

            raise err  # Raise original error if we couldn't catch it in post-mortem analysis
        else:
            self._log.debug("Connection established")

        # Avoiding muting when connecting to the session
        # It might trigger some errors later on if not.
        self._run("/gopr")

        # initialize mesh, post processing, and file explorer interfaces
        try:
            from ansys.mapdl.core.mesh_grpc import MeshGrpc

            self._mesh_rep = MeshGrpc(self)
        except ModuleNotFoundError:  # pragma: no cover
            self._mesh_rep = None

        # Run at connect
        self._run_at_connect()

        # HOUSEKEEPING:
        # Set to not abort after encountering errors.  Otherwise, many
        # failures in a row will cause MAPDL to exit without returning
        # anything useful.  Also avoids abort in batch mode if set.
        if set_no_abort:
            self._set_no_abort()

        # double check we have access to the local path if not
        # explicitly specified
        if "local" not in start_parm:
            self._verify_local()

        # only cache process IDs if launched locally
        if self._local and "exec_file" in start_parm:
            self._cache_pids()

    def _create_process_stds_queue(self, process=None):
        from ansys.mapdl.core.launcher import (
            _create_queue_for_std,  # Avoid circular import error
        )

        if not process:
            process = self._mapdl_process

        self._stdout_queue, self._stdout_thread = _create_queue_for_std(process.stdout)
        self._stderr_queue, self._stderr_thread = _create_queue_for_std(process.stderr)

    def _create_channel(self, ip, port):
        """Create an insecured grpc channel."""

        # open the channel
        channel_str = f"{ip}:{port}"
        self._log.debug("Opening insecure channel at %s", channel_str)
        return grpc.insecure_channel(
            channel_str,
            options=[
                ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
            ],
        )

    def _multi_connect(self, n_attempts=5, timeout=15):
        """Try to connect over a series of attempts to the channel.

        Parameters
        ----------
        n_attempts : int, optional
            Number of connection attempts.
        timeout : float, optional
            Total timeout.

        """
        # This prevents a single failed connection from blocking other attempts
        connected = False
        attempt_timeout = int(timeout / n_attempts)

        max_time = time.time() + timeout
        i = 0
        while time.time() < max_time and i <= n_attempts:
            self._log.debug("Connection attempt %d", i + 1)
            connected = self._connect(timeout=attempt_timeout)
            i += 1
            if connected:
                self._log.debug("Connected")
                break
        else:  # pragma: no cover
            # Check if mapdl process is alive
            msg = (
                f"Unable to connect to MAPDL gRPC instance at {self._channel_str}.\n"
                f"Reached either maximum amount of connection attempts ({n_attempts}) or timeout ({timeout} s)."
            )

            if self._mapdl_process is not None and psutil.pid_exists(
                self._mapdl_process.pid
            ):
                # Process is alive
                raise MapdlConnectionError(
                    msg
                    + f"The MAPDL process seems to be alive (PID: {self._mapdl_process.pid}) but PyMAPDL cannot connect to it."
                )
            else:
                pid_msg = (
                    f" PID: {self._mapdl_process.pid}"
                    if self._mapdl_process is not None
                    else ""
                )
                raise MapdlConnectionError(
                    msg + f"The MAPDL process has died{pid_msg}."
                )

        self._exited = False

    def _is_alive_subprocess(self):
        """Returns:
        * True if the PID is alive.
        * False if it is not.
        * None if there was no process
        """
        if self._mapdl_process:
            return psutil.pid_exists(self._mapdl_process.pid)

    @property
    def process_is_alive(self):
        return self._is_alive_subprocess()

    def _post_mortem_checks(self):
        """Check possible reasons for not having a successful connection."""
        # Check early exit
        process = self._mapdl_process
        if process is None or not self.is_grpc:
            return

        # check the stdout for any errors
        self._read_stds()

        self._check_stds()

    def _read_stds(self):
        """Read the stdout and stderr from the subprocess."""
        from ansys.mapdl.core.launcher import (
            _get_std_output,  # Avoid circular import error
        )

        if self._mapdl_process is None:
            return

        self._log.debug("Reading stdout")
        self._stdout = _get_std_output(self._stdout_queue)
        self._log.debug(f"Read stdout: {self._stdout[:20]}")

        self._log.debug("Reading stderr")
        self._stderr = _get_std_output(self._stderr_queue)
        self._log.debug(f"Read stderr: {self._stderr[:20]}")

    def _check_stds(self, stdout=None, stderr=None):
        """Check the stdout and stderr for any errors."""
        if stdout is None:
            stdout = self._stdout
        if stderr is None:
            stderr = self._stderr

        if not stderr:
            self._log.debug("MAPDL exited without stderr.")
        else:
            self._parse_stderr()

        if not stdout:
            self._log.debug("MAPDL exited without stdout.")
        else:
            self._parse_stdout()

    def _parse_stderr(self, stderr=None):
        """Parse the stderr for any errors."""
        if stderr is None:
            stderr = self._stderr
        errs = self._parse_std(stderr)
        if errs:
            self._log.debug("MAPDL exited with errors in stderr.")

            # Custom errors
            self._raise_custom_stds_errors(errs)

    def _parse_stdout(self, stdout=None):
        """Parse the stdout for any errors."""
        if stdout is None:
            stdout = self._stdout
        errs = self._parse_std(stdout)
        if errs:
            self._log.debug("MAPDL exited with errors in stdout.")

            # Custom errors
            self._raise_custom_stds_errors(errs)

    def _parse_std(self, std):
        # check for errors in stderr
        # split the stderr into groups
        if isinstance(std, list):
            std = "\n".join(std)
            std = std.replace("\n\n", "\n")
        groups = std.split("\r\n\r\n")
        errs = []

        for each in groups:
            if (
                "error" in each.lower()
                or "fatal" in each.lower()
                or "warning" in each.lower()
            ):
                errs.append(each)

        if errs:
            errs = "\r\n\r\n".join(errs)
            errs = errs.replace("\r\n", "\n")
        else:
            errs = ""
        return errs

    def _raise_custom_stds_errors(self, errs_message):
        """Custom errors for stdout and stderr."""
        if "Only one usage of each socket address" in errs_message:
            raise MapdlConnectionError(
                f"A process is already running on the specified port ({self._port}).\n"
                "Only one usage of each socket address (protocol/network address/port) is normally permitted.\n"
                f"\nFull error message:\n{errs_message.split('########',1)[0]}"
            )

        else:
            raise MapdlConnectionError(errs_message)

    @property
    def _channel_str(self):
        """Return the target string.

        Generally of the form of "ip:port", like "127.0.0.1:50052".

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

    def _verify_local(self):
        """Check if Python is local to the MAPDL instance."""
        # Verify if python has assess to the MAPDL directory.
        if self._local:
            directory = self.directory

            if self._jobname is None:
                jobname = self.jobname
            else:
                jobname = self._jobname

            lockfile = os.path.join(directory, jobname + ".err")
            lockfile0 = os.path.join(directory, jobname + "0.err")
            if os.path.isfile(lockfile):
                return
            if os.path.isfile(lockfile0):
                return
            self._local = False

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
        self._mute = value

    def __repr__(self):
        info = super().__repr__()
        return info

    def _connect(self, timeout=5, enable_health_check=False):
        """Establish a gRPC channel to a remote or local MAPDL instance.

        Parameters
        ----------
        timeout : float
            Time in seconds to wait until the connection has been established
        """
        self._state = grpc.channel_ready_future(self._channel)
        self._stub = mapdl_grpc.MapdlServiceStub(self._channel)

        # verify connection
        tstart = time.time()
        while ((time.time() - tstart) < timeout) and not self._state._matured:
            time.sleep(0.01)

        if not self._state._matured:  # pragma: no cover
            return False
        self._log.debug("Established connection to MAPDL gRPC")

        # keeps mapdl session alive
        self._timer = None
        if not self._local:
            self._initialised = threading.Event()
            self._t_trigger = time.time()
            self._t_delay = 30
            self._timer = threading.Thread(
                target=MapdlGrpc._threaded_heartbeat,
                args=(weakref.proxy(self),),
            )
            self._timer.daemon = True
            self._timer.start()

        # enable health check
        if enable_health_check:
            self._enable_health_check()

        return True

    @property
    def _server_version(self):
        """Return the server version.

        Examples
        --------
        >>> mapdl._server_version
        (0, 3, 0)

        Uses cached ``__server_version`` to avoid unnecessary communication.
        """
        # check cache
        if self.__server_version is None:
            self.__server_version = self._get_server_version()
        return self.__server_version

    def _get_server_version(self):
        """Request version from gRPC server.

        Generally tied to the release version unless on a development release.

        2020R2 --> 0.0.0 (or any unknown version)
        2021R1 --> 0.3.0
        2021R2 --> 0.4.0
        2022R1 --> 0.X.X

        """
        sver = (0, 0, 0)
        verstr = self._ctrl("VERSION")
        if verstr:
            sver = version_string_as_tuple(verstr)
        return sver

    def _enable_health_check(self):
        """Places the status of the health check in _health_response_queue"""
        # lazy imports here to speed up module load
        from grpc_health.v1 import health_pb2, health_pb2_grpc

        def _consume_responses(response_iterator, response_queue):
            try:
                for response in response_iterator:
                    response_queue.put(response)
                # NOTE: we're doing absolutely nothing with this as
                # this point since the server side health check
                # doesn't change state.
            except Exception as err:
                if self._exiting:
                    return
                self._exited = True
                raise MapdlExitedError("Lost connection with MAPDL server") from None

        # enable health check
        from queue import Queue

        request = health_pb2.HealthCheckRequest()
        self._health_stub = health_pb2_grpc.HealthStub(self._channel)
        rendezvous = self._health_stub.Watch(request)

        # health check feature implemented after 2020R2
        try:
            status = rendezvous.next()
        except Exception as err:
            if err.code().name != "UNIMPLEMENTED":
                raise err
            return

        if status.status != health_pb2.HealthCheckResponse.SERVING:
            raise MapdlRuntimeError(
                "Unable to enable health check and/or connect to" " the MAPDL server"
            )

        self._health_response_queue = Queue()

        # allow main process to exit by setting daemon to true
        thread = threading.Thread(
            target=_consume_responses,
            args=(rendezvous, self._health_response_queue),
            daemon=True,
        )
        thread.start()

    def _launch(self, start_parm, timeout=10):
        """Launch a local session of MAPDL in gRPC mode.

        This should only need to be used for legacy ``open_gui``
        """
        if not self._local:
            raise MapdlRuntimeError(
                "Can only launch the GUI with a local instance of MAPDL"
            )
        from ansys.mapdl.core.launcher import launch_grpc

        self._exited = False  # reset exit state
        port, directory, process = launch_grpc(**start_parm)
        self._connect(port)

        # may need to wait for viable connection in open_gui case
        tmax = time.time() + timeout
        success = False
        while time.time() < tmax:
            try:
                self.prep7()
                success = True
                break
            except:
                pass

        if not success:
            raise MapdlConnectionError("Unable to reconnect to MAPDL")

    @supress_logging
    def _set_no_abort(self):
        """Do not abort MAPDL."""
        self.nerr(abort=-1, mute=True)

    def _run_at_connect(self):
        """Run house-keeping commands when initially connecting to MAPDL."""
        # increase the number of variables allowed in POST26 to the maximum
        with self.run_as_routine("POST26"):
            self.numvar(200, mute=True)

    def _reset_cache(self):
        """Reset cached items."""
        if self._mesh_rep is not None:
            self._mesh_rep._reset_cache()

        if self._geometry is not None:
            self._geometry._reset_cache()

    @property
    @requires_package("pyvista")
    def _mesh(self):
        return self._mesh_rep

    def _run(self, cmd, verbose=False, mute=None):
        """Sens a command and return the response as a string.

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

        if self._exited:
            raise MapdlExitedError

        # don't allow empty commands
        if not cmd.strip():
            raise ValueError("Empty commands not allowed")

        if len(cmd) > 639:  # CMD_MAX_LENGTH
            raise ValueError("Maximum command length must be less than 640 characters")

        self._busy = True
        if verbose:
            response = self._send_command_stream(cmd, True)
        else:
            response = self._send_command(cmd, mute=mute)
        self._busy = False

        return response.strip()

    @property
    def busy(self):
        """True when MAPDL gRPC server is executing a command"""
        return self._busy

    @protect_grpc
    def _send_command(self, cmd, mute=False):
        """Send a MAPDL command and return the response as a string"""
        opt = ""
        if mute:
            opt = "MUTE"  # suppress any output

        request = pb_types.CmdRequest(command=cmd, opt=opt)
        # TODO: Capture keyboard exception and place this in a thread
        grpc_response = self._stub.SendCommand(request)

        resp = grpc_response.response
        if resp is not None:
            return resp.strip()
        return None

    @protect_grpc
    def _send_command_stream(self, cmd, verbose=False):
        """Send a command and expect a streaming response"""
        request = pb_types.CmdRequest(command=cmd)
        metadata = [("time_step_stream", "100")]
        stream = self._stub.SendCommandS(request, metadata=metadata)
        response = []
        for item in stream:
            cmdout = "\n".join(item.cmdout)
            if verbose:
                print(cmdout)
            response.append(cmdout.strip())

        return "".join(response)

    def _threaded_heartbeat(self):
        """To be called from a thread to verify mapdl instance is alive"""
        self._initialised.set()
        while True:
            if self._exited:
                break

            try:
                time.sleep(self._t_delay)
                if not self.is_alive:
                    break
            except ReferenceError:
                break
            except Exception:
                continue

    def exit(self, save=False, force=False):  # pragma: no cover
        """Exit MAPDL.

        Parameters
        ----------
        save : bool, optional
            Save the database on exit.  The default is ``False``.
        force : bool, optional
            Override any environment variables that may inhibit exiting MAPDL.

        Notes
        -----
        If ``PYMAPDL_START_INSTANCE`` is set to ``False`` (generally set in
        remote testing or documentation build), then this will be
        ignored. Override this behavior with ``force=True`` to always force
        exiting MAPDL regardless of your local environment.

        Examples
        --------
        >>> mapdl.exit()
        """
        # check if permitted to start (and hence exit) instances

        if self._exited is None:
            return  # Some edge cases the class object is not completely initialized but the __del__ method
            # is called when exiting python. So, early exit here instead an error in the following
            # self.directory command.
            # See issue #1796
        elif self._exited:
            # Already exited.
            return
        else:
            mapdl_path = self.directory

        if save:
            self._log.debug("Saving MAPDL database")
            self.save()

        if not force:
            # lazy import here to avoid circular import
            from ansys.mapdl.core.launcher import get_start_instance

            # ignore this method if PYMAPDL_START_INSTANCE=False
            if not get_start_instance():
                self._log.info("Ignoring exit due to PYMAPDL_START_INSTANCE=False")
                return
            # or building the gallery
            from ansys.mapdl import core as pymapdl

            if pymapdl.BUILDING_GALLERY:
                self._log.info("Ignoring exit due as BUILDING_GALLERY=True")
                return

        self._exiting = True
        self._log.debug("Exiting MAPDL")

        if self._local:
            self._cache_pids()  # Recache processes

            if os.name == "nt":
                self._kill_server()
            self._close_process()
            self._remove_lock_file(mapdl_path)
        else:
            self._kill_server()

        self._exited = True

        if self._remote_instance:
            # No cover: The CI is working with a single MAPDL instance
            self._remote_instance.delete()  # pragma: no cover

        self._remove_temp_dir_on_exit()

        if self._local and self._port in _LOCAL_PORTS:
            _LOCAL_PORTS.remove(self._port)

    def _remove_temp_dir_on_exit(self):
        """Removes the temporary directory created by the launcher.

        This only runs if the current working directory of MAPDL is within the
        user temporary directory.

        """
        if self.__remove_temp_dir_on_exit and self._local:  # pragma: no cover
            path = self.directory
            tmp_dir = tempfile.gettempdir()
            ans_temp_dir = os.path.join(tmp_dir, "ansys_")
            if path.startswith(ans_temp_dir):
                self._log.debug("Removing the MAPDL temporary directory %s", path)
                shutil.rmtree(path, ignore_errors=True)
            else:
                self._log.debug(
                    "MAPDL working directory is not in the temporary directory '%s'"
                    ", not removing the MAPDL working directory.",
                    tmp_dir,
                )

    def _kill_server(self):  # pragma: no cover
        """Call exit(0) on the server.

        Notes
        -----
        This only shuts down the mapdl server process and leaves the other
        processes orphaned. This is useful for killing a remote process but not
        a local process.

        """
        self._log.debug("Killing MAPDL server")
        self._ctrl("EXIT")

    def _kill_process(self):
        """Kill process stored in self._mapdl_process"""
        if self._mapdl_process is not None:
            self._log.debug("Killing process using subprocess.Popen.terminate")
            process = self._mapdl_process
            if process.poll() is not None:
                # process hasn't terminated
                process.kill()

    def _kill_child_processes(self, timeout=2):
        pids = self._pids.copy()
        pids.reverse()  # First pid is the parent, therefore start by the children (end)

        for pid in pids:
            self._kill_child_process(pid, timeout=timeout)

    def _kill_child_process(self, pid, timeout=2):
        """Kill an individual child process, given a pid."""
        try:
            self._log.debug(f"Killing MAPDL process: {pid}")
            t0 = time.time()
            while time.time() < t0 + timeout:
                if psutil.pid_exists(pid):
                    os.kill(pid, 9)
                    time.sleep(0.5)
                else:
                    self._log.debug(f"Process {pid} killed properly.")
                    break
            else:
                self._log.debug(
                    f"Process {pid} couldn't be killed in {timeout} seconds"
                )

        except OSError:
            self._log.debug(
                f"Failed attempt to kill process: The process with pid {pid} does not exist. Maybe it was already killed?"
            )

        finally:
            if not psutil.pid_exists(pid):
                self._pids.remove(pid)

    def _close_process(self, timeout=2):  # pragma: no cover
        """Close all MAPDL processes.

        Notes
        -----
        This is effectively the only way to completely close down MAPDL locally on
        linux. Just killing the server with ``_kill_server`` leaves orphaned
        processes making this method ineffective for a local instance of MAPDL.

        """
        if self._local:
            # killing server process
            self._kill_server()

            # killing main process (subprocess)
            self._kill_process()

            # Killing child processes
            self._kill_child_processes(timeout=timeout)

    def _cache_pids(self):
        """Store the process IDs used when launching MAPDL.

        These PIDs are stored in a "cleanup<GUID>.sh/bat" file and are the PIDs
        of the MAPDL process. Killing these kills all dependent MAPDL
        processes.

        """
        self._pids = []

        for filename in self.list_files():
            if "cleanup" in filename:  # Linux does not seem to generate this file?
                script = os.path.join(self.directory, filename)
                with open(script) as f:
                    raw = f.read()

                if os.name == "nt":
                    pids = re.findall(r"/pid (\d+)", raw)
                else:
                    pids = set(re.findall(r"-9 (\d+)", raw))
                self._pids = [int(pid) for pid in pids]

        if not self._pids:
            # For the cases where the cleanup file is not generated,
            # we relay on the process.
            parent_pid = self._mapdl_process.pid
            try:
                parent = psutil.Process(parent_pid)
            except psutil.NoSuchProcess:
                return
            children = parent.children(recursive=True)

            self._pids = [parent_pid] + [each.pid for each in children]

    def _remove_lock_file(self, mapdl_path=None):
        """Removes the lock file.

        Necessary to call this as a segfault of MAPDL or exit(0) will
        not remove the lock file.
        """
        self._log.debug("Removing lock file after exit.")
        if mapdl_path is None:  # pragma: no cover
            mapdl_path = self.directory
        if mapdl_path:
            for lockname in [self.jobname + ".lock", "file.lock"]:
                lock_file = os.path.join(mapdl_path, lockname)
                if os.path.isfile(lock_file):
                    try:
                        os.remove(lock_file)
                    except OSError:
                        pass

    def _run_cleanup_script(self):  # pragma: no cover
        """Run the APDL cleanup script.

        On distributed runs MAPDL creates a cleanup script to kill the
        processes created by the ANSYS spawner.  Normally this file is
        removed when APDL exits normally, but on a failure, it's
        necessary to manually close these PIDs.
        """
        # run cleanup script when local
        if self._local:
            for filename in self.list_files():
                if "cleanup" in filename:
                    script = os.path.join(self.directory, filename)
                    if not os.path.isfile(script):
                        return
                    if os.name != "nt":
                        script = ["/bin/bash", script]
                    process = subprocess.Popen(
                        script,
                        shell=False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                    # always communicate to allow process to run
                    output, err = process.communicate()
                    self._log.debug(
                        "Cleanup output:\n\n%s\n%s",
                        output.decode(),
                        err.decode(),
                    )

    def list_files(self, refresh_cache=True):
        """List the files in the working directory of MAPDL.

        Parameters
        ----------
        refresh_cache : bool, optional
            If local, refresh local cache by querying MAPDL for its
            current path.

        Returns
        -------
        list
            List of files in the working directory of MAPDL.

        Examples
        --------
        >>> files = mapdl.list_files()
        >>> for file in files: print(file)
        file.lock
        file0.bat
        file0.err
        file0.log
        file0.page
        file1.err
        file1.log
        file1.out
        file1.page
        """
        if self._local:  # simply return a python list of files
            if refresh_cache:
                local_path = self.directory
            else:
                local_path = self._directory
            if local_path:
                if os.path.isdir(local_path):
                    return os.listdir(local_path)
            return []

        elif self._exited:
            raise MapdlExitedError("Cannot list remote files since MAPDL has exited")

        # this will sometimes return 'LINUX x6', 'LIN', or 'L'
        if "L" in self.parameters.platform[:1]:
            cmd = "ls"
        else:
            cmd = "dir /b /a"

        files = self.sys(cmd).splitlines()
        if not files:
            warn("No files listed")
        return files

    @supress_logging
    def sys(self, cmd):
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
        # always redirect system output to a temporary file
        tmp_file = f"__tmp_sys_out_{random_string()}__"
        super().sys(f"{cmd} > {tmp_file}")
        if self._local:  # no need to download when local
            with open(os.path.join(self.directory, tmp_file)) as fobj:
                obj = fobj.read()
        else:
            obj = self._download_as_raw(tmp_file).decode()

        self.slashdelete(tmp_file)
        return obj

    def download_result(self, path=None, progress_bar=False, preference=None):
        """Download remote result files to a local directory

        Parameters
        ----------
        path : str, Path, optional
          Path where the files are downloaded, by default the current
          python path (``os.getcwd()``)

        progress_bar : bool, optional
          Show the progress bar or not, default to False.

        preference : str
          Preferred type for the result file, which is either ``rst`` or ``rth``.
          This parameter is only required when both files are present. The default is ```None``,
          in which case ``"rst"`` is used.

        Examples
        --------
        Download remote result files into the current working directory

        >>> import os
        >>> mapdl.download_result(os.getcwd())

        """
        if path is None:  # if not path seems to not work in same cases.
            path = os.getcwd()

        def _download(targets):
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

    @protect_grpc
    def _ctrl(self, cmd):
        """Issue control command to the mapdl server

        Available commands:

        - 'EXIT'
            Calls exit(0) on the server.

        - 'set_verb'
            Enables verbose mode on the server.

        - 'VERSION'
            Returns version string in of the server in the form
            "MAJOR.MINOR.PATCH".  E.g. "0.3.0".  Known versions
            include:

            2020R2 - "0.3.0"
            2021R1 - "0.3.0"
            2021R2 - "0.4.0"

        Unavailable/Flaky:

        - 'time_stats'
            Prints a table for time stats on the server.
            This command appears to be disabled/broken.

        - 'mem-stats'
            To be added

        """
        self._log.debug('Issuing CtrlRequest "%s"', cmd)
        request = anskernel.CtrlRequest(ctrl=cmd)

        # handle socket closing upon exit
        if cmd.lower() == "exit":
            try:
                # this always returns an error as the connection is closed
                self._stub.Ctrl(request)
            except (_InactiveRpcError, _MultiThreadedRendezvous):
                pass
            return

        resp = self._stub.Ctrl(request)
        if hasattr(resp, "response"):
            return resp.response

    @wraps(_MapdlCore.cdread)
    def cdread(self, option="", fname="", ext="", fnamei="", exti="", **kwargs):
        """Wraps CDREAD"""
        option = option.strip().upper()

        if option not in ["DB", "SOLID", "COMB"]:
            raise ValueError(
                f'Option "{option}" is not supported.  Please '
                "Input the geometry and mesh files separately "
                r'with "\INPUT" or ``mapdl.input``'
            )
        if option == "ALL":
            raise ValueError(
                f'Option "{option}" is not supported in gRPC mode.  Please '
                "Input the geometry and mesh files separately "
                r'with "\INPUT" or ``mapdl.input``'
            )

        kwargs.setdefault("verbose", False)
        kwargs.setdefault("progress_bar", False)
        kwargs.setdefault("orig_cmd", "CDREAD")
        kwargs.setdefault("cd_read_option", option.upper())

        fname = self._get_file_name(fname, ext, "cdb")
        fname = self._get_file_path(fname, kwargs["progress_bar"])

        self.input(fname, **kwargs)

    @wraps(_MapdlCore.tbft)
    def tbft(
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
        """Wraps ``_MapdlCore.tbft``."""
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

    @protect_grpc
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

        dir : str, optional
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
            dependent on verbosity.  The defaults are:

            - ``verbose=True``: ``time_step_stream=500``
            - ``verbose=False``: ``time_step_stream=50``

            These defaults will be ignored if ``time_step_stream`` is
            manually set.

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

        """
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
        # always check if file is present as the grpc and MAPDL errors
        # are unclear
        filename = self._get_file_path(fname, progress_bar)

        if time_step_stream is not None:
            if time_step_stream <= 0:
                raise ValueError("``time_step_stream`` must be greater than 0``")

        if verbose:
            if time_step_stream is None:
                time_step_stream = 500
            metadata = [
                ("time_step_stream", str(time_step_stream)),
                ("chunk_size", str(chunk_size)),
            ]

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

        # otherwise, not verbose
        if time_step_stream is None:
            time_step_stream = 50
        metadata = [
            ("time_step_stream", str(time_step_stream)),
            ("chunk_size", str(chunk_size)),
        ]

        # since we can't directly run /INPUT, we have to write a
        # temporary input file that tells MAPDL to read the input
        # file.
        id_ = random_string()
        tmp_name = f"_input_tmp_{id_}_.inp"
        tmp_out = f"_input_tmp_{id_}_.out"

        if "CDRE" in orig_cmd.upper():
            # Using CDREAD
            option = kwargs.get("cd_read_option", "COMB")
            tmp_dat = f"/OUT,{tmp_out}\n{orig_cmd},'{option}','{filename}'\n"
            delete_uploaded_files = False

        else:
            # Using default INPUT
            tmp_dat = f"/OUT,{tmp_out}\n{orig_cmd},'{filename}'\n"
            delete_uploaded_files = True

        if write_to_log and self._apdl_log is not None:
            if not self._apdl_log.closed:
                self._apdl_log.write(tmp_dat)

        # Escaping early if inside non_interactive context
        if self._store_commands:
            self._stored_commands.append(tmp_dat.splitlines()[1])
            return None

        if self._local:
            local_path = self.directory
            tmp_name_path = os.path.join(local_path, tmp_name)
            with open(tmp_name_path, "w") as f:
                f.write(tmp_dat)
        else:
            self._upload_raw(tmp_dat.encode(), tmp_name)

        request = pb_types.InputFileRequest(filename=tmp_name)

        # even though we don't care about the output, we still
        # need to check.  otherwise, since inputfile is
        # non-blocking, we could corrupt the service
        chunks = self._stub.InputFileS(request, metadata=metadata)
        _ = [chunk.cmdout for chunk in chunks]  # unstable

        # all output (unless redirected) has been written to a temp output
        if self._local:  # pragma: no cover
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

        return output

    def _get_file_path(self, fname, progress_bar=False):
        """Find files in the Python and MAPDL working directories.

        **The priority is for the Python directory.**

        Hence if the same file is in the Python directory and in the MAPDL directory,
        PyMAPDL will upload a copy from the Python directory to the MAPDL directory,
        overwriting the MAPDL directory copy.
        """

        if os.path.isdir(fname):
            raise ValueError(
                f"`fname` should be a full file path or name, not the directory '{fname}'."
            )

        fPath = pathlib.Path(fname)

        fpath = os.path.dirname(fname)
        fname = fPath.name
        fext = fPath.suffix

        # if there is no dirname, we are assuming the file is
        # in the python working directory.
        if not fpath:
            fpath = os.getcwd()

        ffullpath = os.path.join(fpath, fname)

        if os.path.exists(ffullpath) and self._local:
            return ffullpath

        if self._local:
            if os.path.isfile(fname):
                # And it exists
                filename = os.path.join(os.getcwd(), fname)
            elif fname in self.list_files():
                # It exists in the Mapdl working directory
                filename = os.path.join(self.directory, fname)
            else:
                # Finally
                raise FileNotFoundError(f"Unable to locate filename '{fname}'")

        else:  # Non-local
            # upload the file if it exists locally
            if os.path.isfile(ffullpath):
                self.upload(ffullpath, progress_bar=progress_bar)
                filename = fname

            elif fname in self.list_files():
                # It exists in the Mapdl working directory
                filename = fname

            else:
                raise FileNotFoundError(f"Unable to locate filename '{fname}'")

        return filename

    def _get_file_name(self, fname, ext=None, default_extension=None):
        """Get file name from fname and extension arguments.

        fname can be the full path.

        Parameters
        ----------
        fname : str
            File name (with our with extension). It can be a full path.

        ext : str, optional
            File extension. The default is None.

        default_extension : str
            Default filename extension. The default is None.
        """

        # the old behaviour is to supplied the name and the extension separately.
        # to make it easier let's going to allow names with extensions

        # Sanitizing ext
        while ext and ext[0] == ".":
            ext = ext[1:]

        if ext:
            fname = fname + "." + ext
        else:
            basename = os.path.basename(fname)

            if len(basename.split(".")) == 1:
                # there is no extension in the main name.
                if default_extension:
                    fname = fname + "." + default_extension

        return fname

    def _flush_stored(self):
        """Writes stored commands to an input file and runs the input
        file.  Used with non_interactive.
        """
        self._log.debug("Flushing stored commands")

        commands = "\n".join(self._stored_commands)
        if self._apdl_log:
            self._apdl_log.write(commands + "\n")

        self._log.debug(
            "Writing the following commands to a temporary " "apdl input file:\n%s",
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
        out = self.input(
            tmp_filename,
            write_to_log=False,
            verbose=False,
            chunk_size=DEFAULT_CHUNKSIZE,
            progress_bar=False,
        )
        # skip the first line as it simply states that it's reading an input file
        self._response = out[out.find("LINE=       0") + 13 :]
        self._log.info(self._response)

        if not self._ignore_errors:
            self._raise_errors(self._response)

        # try/except here because MAPDL might have not closed the temp file
        try:
            os.remove(tmp_filename)
        except:
            self._log.warning("Unable to remove temporary file %s", tmp_filename)

    @protect_grpc
    def _get(
        self, entity, entnum, item1, it1num, item2, it2num, item3, it3num, item4, it4num
    ):
        """Sends gRPC *Get request.

        .. warning::
           Not thread safe.  Uses ``_get_lock`` to ensure multiple
           request are not evaluated simultaneously.
        """
        if self._store_commands:
            raise MapdlRuntimeError(
                "Cannot use gRPC enabled ``GET`` when in non_interactive mode. "
                "Exit non_interactive mode before using this method."
            )

        cmd = f"{entity},{entnum},{item1},{it1num},{item2},{it2num},{item3}, {it3num}, {item4}, {it4num}"

        # not threadsafe; don't allow multiple get commands
        while self._get_lock:
            time.sleep(0.001)

        self._get_lock = True
        try:
            getresponse = self._stub.Get(pb_types.GetRequest(getcmd=cmd))
        finally:
            self._get_lock = False

        if getresponse.type == 0:
            self._log.debug(
                "The 'grpc' get method seems to have failed. Trying old implementation for more verbose output."
            )
            try:
                out = self.run("*GET,__temp__," + cmd)
            except MapdlRuntimeError:
                # Get can thrown some errors, in that case, they are caught in the default run method.
                raise
            else:
                # Here we catch the rest of the errors and warnings
                raise ValueError(out)

        if getresponse.type == 1:
            return getresponse.dval
        elif getresponse.type == 2:
            return getresponse.sval

        raise MapdlRuntimeError(
            f"Unsupported type {getresponse.type} response from MAPDL"
        )

    def download_project(self, extensions=None, target_dir=None, progress_bar=False):
        """Download all the project files located in the MAPDL working directory.

        Parameters
        ----------
        extensions : list[str], tuple[str], optional
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
            files = self.list_files()
            list_of_files = self.download(
                files, target_dir=target_dir, progress_bar=progress_bar
            )

        else:
            list_of_files = []
            for each_extension in extensions:
                list_of_files.extend(
                    self.download(
                        files=f"*.{each_extension}",
                        target_dir=target_dir,
                        progress_bar=progress_bar,
                    )
                )

        return list_of_files

    def download(
        self,
        files,
        target_dir=None,
        chunk_size=None,
        progress_bar=None,
        recursive=False,
    ):  # pragma: no cover
        """Download files from the gRPC instance workind directory

        .. warning:: This feature is only available for MAPDL 2021R1 or newer.

        Parameters
        ----------
        files : str or List[str] or Tuple(str)
            Name of the file on the server. File must be in the same
            directory as the mapdl instance. A list of string names or
            tuples of string names can also be used.
            List current files with :meth:`Mapdl.list_files <MapdlGrpc.list_files>`.

            Alternatively, you can also specify **glob expressions** to
            match file names. For example: `'file*'` to match every file whose
            name starts with `'file'`.

        target_dir : str, optional
            Path where the downloaded files will be located. The default is the current
            working directory.

        chunk_size : int, optional
            Chunk size in bytes.  Must be less than 4MB. The default is 256 kB.

        progress_bar : bool, optional
            Display a progress bar using ``tqdm`` when ``True``.
            Helpful for showing download progress.

        recursive : bool, optional
            Whether to use recursion when using glob pattern. The default is ``False``.

        Notes
        -----
        There are some considerations to keep in mind when using this command:

        * The glob pattern search does not search recursively in remote instances.
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

        Download every single file in the MAPDL workind directory:

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

        self_files = self.list_files()  # to avoid calling it too much

        if isinstance(files, str):
            if self._local:  # pragma: no cover
                # in local mode
                if os.path.exists(files):
                    # file exist
                    list_files = [files]
                elif "*" in files:
                    list_files = glob.glob(files, recursive=recursive)  # using filter
                    if not list_files:
                        raise ValueError(
                            f"The `'files'` parameter ({files}) didn't match any file using glob expressions in the local client."
                        )
                else:
                    raise ValueError(
                        f"The files parameter ('{files}') does not match any file or pattern."
                    )

            else:  # Remote or looking into MAPDL working directory
                if files in self_files:
                    list_files = [files]
                elif "*" in files:
                    # try filter on the list_files
                    if recursive:
                        warn(
                            "The 'recursive' keyword argument does not work with remote instances. So it is ignored."
                        )
                    list_files = fnmatch.filter(self_files, files)
                    if not list_files:
                        raise ValueError(
                            f"The `'files'` parameter ({files}) didn't match any file using glob expressions in the remote server."
                        )
                else:
                    raise ValueError(
                        f"The `'files'` parameter ('{files}') does not match any file or pattern."
                    )

        elif isinstance(files, (list, tuple)):
            if not all([isinstance(each, str) for each in files]):
                raise ValueError(
                    "The parameter `'files'` can be a list or tuple, but it should only contain strings."
                )
            list_files = files
        else:
            raise ValueError(
                f"The `file` parameter type ({type(files)}) is not supported."
                "Only strings, tuple of strings or list of strings are allowed."
            )

        if target_dir:
            try:
                os.mkdir(target_dir)
            except FileExistsError:
                pass
        else:
            target_dir = os.getcwd()

        for each_file in list_files:
            try:
                file_name = os.path.basename(
                    each_file
                )  # Getting only the name of the file.
                #  We try to avoid that when the full path is supplied, it will crash when trying
                # to do `os.path.join(target_dir"os.getcwd()", file_name "full filename path"`
                # This will produce the file structure to flat out, but it is find, because recursive
                # does not work in remote.
                self._download(
                    each_file,
                    out_file_name=os.path.join(target_dir, file_name),
                    chunk_size=chunk_size,
                    progress_bar=progress_bar,
                )
            except FileNotFoundError:
                # So far the grpc interface returns size of the file equal
                # zero, if the file does not exists or its size is zero,
                # but they are two different things!
                # In theory, since we are obtaining the files name from
                # `mapdl.list_files()` they do exist, so
                # if there is any error, it means their size is zero.
                pass  # this is not the best.

        return list_files

    @protect_grpc
    def _download(
        self,
        target_name,
        out_file_name=None,
        chunk_size=DEFAULT_CHUNKSIZE,
        progress_bar=False,
    ):
        """Download a file from the gRPC instance.

        Parameters
        ----------
        target_name : str
            Target file on the server.  File must be in the same
            directory as the mapdl instance.  List current files with
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
        chunks = self._stub.DownloadFile(request, metadata=metadata)
        file_size = save_chunks_to_file(
            chunks,
            out_file_name,
            progress_bar=progress_bar,
            target_name=target_name,
        )

        if not file_size:
            raise FileNotFoundError(f'File "{target_name}" is empty or does not exist.')

    @protect_grpc
    def upload(self, file_name, progress_bar=True):
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
        response = self._stub.UploadFile(chunks_generator)

        if not response.length:
            raise IOError("File failed to upload")
        return os.path.basename(file_name)

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
    ):
        """gRPC VGET request.

        Send a vget request, receive a bytes stream, and return it as
        a numpy array.

        Not thread safe as it uses a constant internal temporary
        parameter name.  This method uses _vget_lock to ensure
        multiple simultaneous request fail.

        Returns
        -------
        values : np.ndarray
            Numpy 1D array containing the requested *VGET item and entity.
        """
        if "parm" in kwargs:
            raise ValueError("Parameter name `parm` not supported with gRPC")

        while self._vget_lock:
            time.sleep(0.001)
        self._vget_lock = True

        cmd = f"{entity},{entnum},{item1},{it1num},{item2},{it2num},{kloop}"
        try:
            chunks = self._stub.VGet2(pb_types.GetRequest(getcmd=cmd))
            values = parse_chunks(chunks)
        finally:
            self._vget_lock = False
        return values

    def _screenshot_path(self):
        """Returns the local path of the MAPDL generated screenshot.

        If necessary, downloads the remotely rendered file.
        """
        if self._local:
            return super()._screenshot_path()

        all_filenames = self.list_files()
        filenames = []
        for filename in all_filenames:
            if ".png" == filename[-4:]:
                filenames.append(filename)
        filenames.sort()
        filename = os.path.basename(filenames[-1])

        temp_dir = tempfile.gettempdir()
        save_name = os.path.join(temp_dir, "tmp.png")
        self._download(filename, out_file_name=save_name)
        return save_name

    @protect_grpc
    def _download_as_raw(self, target_name):
        """Download a file from the gRPC instance as a binary
        string without saving it to disk.
        """
        request = pb_types.DownloadFileRequest(name=target_name)
        chunks = self._stub.DownloadFile(request)
        return b"".join([chunk.payload for chunk in chunks])

    @property
    def is_alive(self) -> bool:
        """True when there is an active connect to the gRPC server"""
        if self._exited:
            return False
        if self.busy:
            return True
        try:
            return bool(self.inquire("", "JOBNAME"))
        except:
            return False

    @property
    def xpl(self):
        """MAPDL file explorer

        Iteratively navigate through MAPDL files.

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
        return self._xpl

    @protect_grpc
    def scalar_param(self, pname):
        """Return a scalar parameter as a float.

        If parameter does not exist, returns ``None``.

        """
        request = pb_types.ParameterRequest(name=pname, array=False)
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
        """APDL math interface

        Returns
        -------
        :class:`MapdlMath <ansys.mapdl.core.math.MapdlMath>`

        Examples
        --------
        Get the stiffness matrix from MAPDL

        >>> mm = mapdl.math.stiff()
        >>> matrix = k.asarray()
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>

        Get the mass matrix from mapdl

        >>> mm = mapdl.math.stiff()
        >>> matrix = k.asarray()
        <60x60 sparse matrix of type '<class 'numpy.float64'>'
            with 1734 stored elements in Compressed Sparse Row format>
        """
        from ansys.mapdl.core.math import MapdlMath

        return MapdlMath(self)

    @property
    def krylov(self):
        """APDL krylov interface.

        For more information, see the :class:`KrylovSolver <ansys.mapdl.core.krylov.KrylovSolver>`

        Returns
        -------
        :class:`Krylov class <ansys.mapdl.core.krylov.KrylovSolver>`

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
    def _data_info(self, pname):
        """Returns the data type of a parameter

        APDLMATH vectors only.
        """
        request = pb_types.ParameterRequest(name=pname)
        return self._stub.GetDataInfo(request)

    @protect_grpc
    def _vec_data(self, pname):
        """Downloads vector data from a MAPDL MATH parameter"""
        dtype = ANSYS_VALUE_TYPE[self._data_info(pname).stype]
        request = pb_types.ParameterRequest(name=pname)
        chunks = self._stub.GetVecData(request)
        return parse_chunks(chunks, dtype)

    @protect_grpc
    def _mat_data(self, pname, raw=False):
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
    def locked(self):
        """Instance is in use within a pool"""
        return self._locked

    @locked.setter
    def locked(self, new_value):
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

        info = f"Product:             {product}\n"
        info += f"MAPDL Version:       {self.version}\n"
        info += f"ansys.mapdl Version: {__version__}\n"
        return info

    @supress_logging
    @run_as_prep7
    def _generate_iges(self):
        """Save IGES geometry representation to disk"""
        basename = "_tmp.iges"
        if self._local:
            filename = os.path.join(self.directory, basename)
            self.igesout(basename, att=1)
        else:
            self.igesout(basename, att=1)
            filename = os.path.join(tempfile.gettempdir(), basename)
            self._download(basename, filename, progress_bar=False)
        return filename

    @property
    def _distributed_result_file(self):
        """Path of the distributed result file"""
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

        rth_file = os.path.join(self.directory, rth_basename)
        rst_file = os.path.join(self.directory, rst_basename)

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
        """The thermal result object"""
        self._prioritize_thermal = True
        result = self.result
        self._prioritize_thermal = False
        return result

    def list_error_file(self):
        """Listing of errors written in JOBNAME.err"""
        files = self.list_files()
        jobname = self.jobname
        error_file = None
        for test_file in [f"{jobname}.err", f"{jobname}0.err"]:
            if test_file in files:
                error_file = test_file
                break

        if not error_file:
            return None

        if self.local:
            return open(os.path.join(self.directory, error_file)).read()
        elif self._exited:
            raise MapdlExitedError(
                "Cannot list error file when MAPDL Service has " "exited"
            )

        return self._download_as_raw(error_file).decode("latin-1")

    @wraps(_MapdlCore.igesin)
    def igesin(self, fname="", ext="", **kwargs):
        """Wrap the IGESIN command to handle the remote case."""

        fname = self._get_file_name(fname=fname, ext=ext)
        filename = self._get_file_path(fname, progress_bar=False)

        if " " in fname:
            # Bug in reading file paths with whitespaces.
            # https://github.com/pyansys/pymapdl/issues/1601

            msg_ = f"Applying \\IGESIN whitespace patch.\nSee #1601 issue in PyMAPDL repository.\nReading file {fname}"
            self.input_strings("\n".join([f"! {each}" for each in msg_.splitlines()]))
            self._log.debug(msg_)

            cmd = f"*dim,__iges_file__,string,248\n*set,__iges_file__(1), '{filename}'"
            self.input_strings(cmd)

            out = super().igesin(fname="__iges_file__(1)", **kwargs)
            self.run("__iges_file__ =")  # cleaning array.
            self.run("! Ending \\IGESIN whitespace patch.")
            return out
        else:
            return super().igesin(fname=filename, **kwargs)

    @wraps(_MapdlCore.cmatrix)
    def cmatrix(
        self,
        symfac="",
        condname="",
        numcond="",
        grndkey="",
        capname="",
        **kwargs,
    ):
        """Run CMATRIX in non-interactive mode and return the response
        from file.
        """

        # The CMATRIX command needs to run in non-interactive mode
        if not self._store_commands:
            with self.non_interactive:
                super().cmatrix(symfac, condname, numcond, grndkey, capname, **kwargs)
            self._response = self._download_as_raw("cmatrix.out").decode()
            return self._response

        # otherwise, simply run cmatrix as we're already in
        # non-interactive and there's no output to return
        super().cmatrix(symfac, condname, numcond, grndkey, capname, **kwargs)

    @property
    def name(self):
        """Instance unique identifier."""
        if not self._name:
            if self._ip or self._port:
                self._name = f"GRPC_{self._ip}:{self._port}"
            else:
                self._name = f"GRPC_instance_{id(self)}"
        return self._name

    @property
    def _distributed(self) -> bool:
        """MAPDL is running in distributed mode."""
        if self.__distributed is None:
            self.__distributed = self.parameters.numcpu > 1
        return self.__distributed

    @wraps(_MapdlCore.ndinqr)
    def ndinqr(self, node, key, **kwargs):
        """Wrap the ``ndinqr`` method to take advantage of the gRPC methods."""
        super().ndinqr(node, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.elmiqr)
    def elmiqr(self, ielem, key, **kwargs):
        """Wrap the ``elmiqr`` method to take advantage of the gRPC methods."""
        super().elmiqr(ielem, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.kpinqr)
    def kpinqr(self, knmi, key, **kwargs):
        """Wrap the ``kpinqr`` method to take advantage of the gRPC methods."""
        super().kpinqr(knmi, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.lsinqr)
    def lsinqr(self, line, key, **kwargs):
        """Wrap the ``lsinqr`` method to take advantage of the gRPC methods."""
        super().lsinqr(line, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.arinqr)
    def arinqr(self, anmi, key, **kwargs):
        """Wrap the ``arinqr`` method to take advantage of the gRPC methods."""
        super().arinqr(anmi, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.vlinqr)
    def vlinqr(self, vnmi, key, **kwargs):
        """Wrap the ``vlinqr`` method to take advantage of the gRPC methods."""
        super().vlinqr(vnmi, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.rlinqr)
    def rlinqr(self, nreal, key, **kwargs):
        """Wrap the ``rlinqr`` method to take advantage of the gRPC methods."""
        super().rlinqr(nreal, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.gapiqr)
    def gapiqr(self, ngap, key, **kwargs):
        """Wrap the ``gapiqr`` method to take advantage of the gRPC methods."""
        super().gapiqr(ngap, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.masiqr)
    def masiqr(self, node, key, **kwargs):
        """Wrap the ``masiqr`` method to take advantage of the gRPC methods."""
        super().masiqr(node, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.ceinqr)
    def ceinqr(self, nce, key, **kwargs):
        """Wrap the ``ceinqr`` method to take advantage of the gRPC methods."""
        super().ceinqr(nce, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.cpinqr)
    def cpinqr(self, ncp, key, **kwargs):
        """Wrap the ``cpinqr`` method to take advantage of the gRPC methods."""
        super().cpinqr(ncp, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.csyiqr)
    def csyiqr(self, ncsy, key, **kwargs):
        """Wrap the ``csyiqr`` method to take advantage of the gRPC methods."""
        super().csyiqr(ncsy, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.etyiqr)
    def etyiqr(self, itype, key, **kwargs):
        """Wrap the ``etyiqr`` method to take advantage of the gRPC methods."""
        super().etyiqr(itype, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.foriqr)
    def foriqr(self, node, key, **kwargs):
        """Wrap the ``foriqr`` method to take advantage of the gRPC methods."""
        super().foriqr(node, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.sectinqr)
    def sectinqr(self, nsect, key, **kwargs):
        """Wrap the ``sectinqr`` method to take advantage of the gRPC methods."""
        super().sectinqr(nsect, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.mpinqr)
    def mpinqr(self, mat, iprop, key, **kwargs):
        """Wrap the ``mpinqr`` method to take advantage of the gRPC methods."""
        super().mpinqr(mat, iprop, key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.dget)
    def dget(self, node, idf, kcmplx, **kwargs):
        """Wrap the ``dget`` method to take advantage of the gRPC methods."""
        super().dget(node, idf, kcmplx, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.fget)
    def fget(self, node, idf, kcmplx, **kwargs):
        """Wrap the ``fget`` method to take advantage of the gRPC methods."""
        super().fget(node, idf, kcmplx, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.erinqr)
    def erinqr(self, key, **kwargs):
        """Wrap the ``erinqr`` method to take advantage of the gRPC methods."""
        super().erinqr(key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.wrinqr)
    def wrinqr(self, key, **kwargs):
        """Wrap the ``wrinqr`` method to take advantage of the gRPC methods."""
        super().wrinqr(key, pname=TMP_VAR, mute=True, **kwargs)
        return self.scalar_param(TMP_VAR)

    @wraps(_MapdlCore.file)
    def file(self, fname="", ext="", **kwargs):
        """Wrap ``_MapdlCore.file`` to take advantage of the gRPC methods."""
        # always check if file is present as the grpc and MAPDL errors
        # are unclear
        fname = self._get_file_name(fname, ext, "cdb")
        fname = self._get_file_path(fname, kwargs.get("progress_bar", False))
        file_, ext_ = self._decompose_fname(fname)

        return self._file(file_, ext_, **kwargs)

    @wraps(_MapdlCore.vget)
    def vget(self, par="", ir="", tstrt="", kcplx="", **kwargs):
        """Wraps VGET"""
        super().vget(par=par, ir=ir, tstrt=tstrt, kcplx=kcplx, **kwargs)
        return self.parameters[par]

    def get_variable(self, ir, tstrt="", kcplx="", **kwargs):
        """
        Obtain the variable values.

        Parameters
        ----------
        ir : str, optional
            Reference number of the variable (1 to NV [NUMVAR]).

        tstrt : str, optional
            Time (or frequency) corresponding to start of IR data.  If between
            values, the nearer value is used. By default it is the first value.

        kcplx : str, optional
            Complex number key:

            * ``0`` - Use the real part of the IR data. Default.

            * ``1`` - Use the imaginary part of the IR data.

        Returns
        -------
        np.array
            Variable values as array.
        """
        par = "temp_var"
        variable = self.vget(par=par, ir=ir, tstrt=tstrt, kcplx=kcplx, **kwargs)
        del self.parameters[par]
        return variable

    @wraps(_MapdlCore.nsol)
    def nsol(
        self,
        nvar=VAR_IR,
        node="",
        item="",
        comp="",
        name="",
        sector="",
        **kwargs,
    ):
        """Wraps NSOL to return the variable as an array."""
        super().nsol(
            nvar=nvar,
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            kwargs=kwargs,
        )
        return self.vget("_temp", nvar)

    @wraps(_MapdlCore.esol)
    def esol(
        self,
        nvar: MapdlInt = VAR_IR,
        elem: MapdlInt = "",
        node: MapdlInt = "",
        item: str = "",
        comp: str = "",
        name: str = "",
        **kwargs,
    ) -> Optional[str]:
        """Wraps ESOL to return the variable as an array."""
        super().esol(
            nvar=nvar,
            elem=elem,
            node=node,
            item=item,
            comp=comp,
            name=name,
            kwargs=kwargs,
        )
        return self.vget("_temp", nvar)

    def get_nsol(self, node, item, comp, name="", sector="", **kwargs):
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
        np.array
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
            VAR_IR,
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            kwargs=kwargs,
        )

    def get_esol(
        self,
        elem,
        node,
        item,
        comp,
        name="",
        sector="",
        tstrt="",
        kcplx="",
        **kwargs,
    ):
        """Get ESOL data.

        /POST26 APDL Command: ESOL

        Parameters
        ----------
        elem : int
            Element for which data are to be stored.

        node : int
            Node number on this element for which data are to be
            stored. If blank, store the average element value (except
            for FMAG values, which are summed instead of averaged).

        item : str
            Label identifying the item. General item labels are shown
            in Table 134: ESOL - General Item and Component Labels
            below. Some items also require a component label.

        comp : str
            Component of the item (if required). General component
            labels are shown in Table 134: ESOL - General Item and
            Component Labels below.  If Comp is a sequence number (n),
            the NODE field will be ignored.

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
        np.array
            Variable values

        Notes
        -----
        By default, this command store temporally the variable on the
        variable number set by ``VAR_IR`` in the class MapdlGrpc.
        Therefore, any variable in that slot will be deleted when using
        this command.

        See Table: 134:: ESOL - General Item and Component Labels for
        a list of valid item and component labels for element (except
        line element) results.

        The ESOL command defines element results data to be stored
        from a results file (FILE). Not all items are valid for all
        elements. To see the available items for a given element,
        refer to the input and output summary tables in the
        documentation for that element.

        Two methods of data access are available via the ESOL
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
        for some elements via the SHELL, LAYERP26, and FORCE commands.

        For more information on the meaning of contact status and its
        possible values, see Reviewing Results in POST1 in the Contact
        Technology Guide.
        """
        self.esol(
            VAR_IR,
            elem=elem,
            node=node,
            item=item,
            comp=comp,
            name=name,
            sector=sector,
            kwargs=kwargs,
        )
        # Using get_variable because it deletes the intermediate parameter after using it.
        return self.get_variable(VAR_IR, tstrt=tstrt, kcplx=kcplx)
