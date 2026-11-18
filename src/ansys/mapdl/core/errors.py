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

"""PyMAPDL specific errors"""

from enum import Enum
from functools import cache, wraps
import os
import pathlib
import re
import signal
import sys
import threading
from time import sleep
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

import grpc

from ansys.mapdl.core import LOG as logger

SIGINT_TRACKER: List[bool] = []

# 'signal.SIGKILL' does not exist on Windows. Its value is 9 on every POSIX platform.
# On Windows the fallback only avoids an AttributeError: the return code of a
# process is never negative there, so the exit signal is always None and this
# value is never matched. 'None' is not used as the fallback because then
# 'exit_signal == _SIGKILL' would be true when the exit signal is unknown.
_SIGKILL: int = getattr(signal, "SIGKILL", 9)

# Configuration of 'protect_grpc' wrapper
N_ATTEMPTS = 5
INITIAL_BACKOFF = 0.1
MULTIPLIER_BACKOFF = 2

# How much of the MAPDL error file is shown when the MAPDL process dies. The file
# can grow to tens of megabytes, so only its end is read.
ERROR_FILE_TAIL_BYTES = 4096
ERROR_FILE_TAIL_LINES = 20
# In distributed mode, at most this many 'JOBNAMEx.err' files (x > 0) are shown.
ERROR_FILE_MAX_WORKER_FILES = 3
# Headers of the messages that make a 'JOBNAMEx.err' file (x > 0) worth showing.
ERROR_FILE_HEADERS = ("*** FATAL ***", "*** ERROR ***")


LOCKFILE_MSG: str = """
Another ANSYS job with the same job name is already running in this
directory, or the lock file has not been deleted from an abnormally
terminated ANSYS run.

Disable this check by passing ``override=True``
"""


TYPE_MSG: str = (
    "Invalid datatype.  Must be one of the following:\n"
    + "np.int32, np.int64, or np.double"
)


@cache
def terminal_support_color() -> bool:
    """Check if the terminal supports color output."""
    # This is a simple check, you can expand it based on your requirements
    return sys.stdout.isatty()


class bcolors(Enum):
    NOTES = "\033[92m"  # Green
    WARNINGS = "\033[93m"  # Yellow
    ERRORS = "\033[91m"  # Red
    INFO = "\033[94m"  # Blue

    # ANSI escape sequences for colors
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def color_text(text: str, color: str, bold: bool = False) -> str:
    """Color the text if terminal supports color."""
    bold_ = bcolors.BOLD.value if bold else ""

    if terminal_support_color():
        return f"{bcolors[color].value}{bold_}{text}{bcolors.ENDC.value}"
    return text


## Abraham class
class MapdlException(Exception):
    """MAPDL general exception"""

    def __init__(self, msg: str = "", notes: str = ""):

        if msg:
            msg_lines = msg.splitlines()

            # If there are multiple lines, color the first line
            msg_lines_ = [color_text(msg_lines[0], "ERRORS", True)]
            msg_lines_.extend(msg_lines[1:])

            msg = "\n".join(msg_lines_)

        self.msg = msg
        self.notes = notes

        super().__init__(msg)

    def __str__(self):
        """Return the string representation of the exception."""
        msg = self.msg
        if self.notes:
            msg += f"\n{color_text('NOTES:', 'NOTES')} {self.notes}"
        return msg


## Main subclasses
class MapdlValueError(MapdlException, ValueError):
    """MAPDL Value error"""

    pass


class MapdlFileNotFoundError(MapdlException, FileNotFoundError):
    """Error when file is not found"""

    pass


class MapdlRuntimeError(MapdlException, RuntimeError):
    """Raised when MAPDL passes an error"""

    pass


## Inheritated
class ANSYSDataTypeError(MapdlValueError):
    """Raised when and invalid data type is sent to APDLMath"""

    def __init__(self, msg=TYPE_MSG, notes: str = ""):
        super().__init__(msg=msg, notes=notes)


class VersionError(MapdlValueError):
    """Raised when MAPDL is the wrong version"""

    def __init__(self, msg="Invalid MAPDL version", notes: str = ""):
        super().__init__(msg=msg, notes=notes)


class NoDistributedFiles(MapdlFileNotFoundError):
    """Unable to find any distributed result files"""

    def __init__(
        self, msg="Unable to find any distributed result files", notes: str = ""
    ):
        super().__init__(msg=msg, notes=notes)


class MapdlInvalidRoutineError(MapdlRuntimeError):
    """Raised when MAPDL is in the wrong routine"""

    pass


class MapdlCommandBlockedError(MapdlRuntimeError):
    """Raised when a command matches an entry in ``blocked_commands``."""


class MapdlCommandIgnoredError(MapdlRuntimeError):
    """Raised when MAPDL ignores a command."""

    pass


class MapdlDoLoopLimitError(MapdlRuntimeError):
    """Raised when too many ``*DO``/``*DOWHILE`` loops are nested.

    MAPDL only supports a limited number of nested do-loops. See
    :attr:`Mapdl.do() <ansys.mapdl.core.Mapdl.do>` and
    :attr:`Mapdl.dowhile() <ansys.mapdl.core.Mapdl.dowhile>`.
    """

    def __init__(
        self,
        msg: str = "Exceeded the maximum number of nested MAPDL do-loops.",
        notes: str = "",
    ):
        super().__init__(msg=msg, notes=notes)


class MapdlExitedError(MapdlRuntimeError):
    """Raised when MAPDL has exited"""

    def __init__(self, msg="MAPDL has exited", notes: str = ""):
        super().__init__(msg=msg, notes=notes)


class NotEnoughResources(MapdlExitedError):
    """Raised when MAPDL has exited"""

    def __init__(
        self,
        msg: str = "MAPDL has exited because there is not enough resources ({resource})",
        notes: str = "",
        resource: str = "CPUs",
    ):
        super().__init__(msg=msg.format(resource=resource), notes=notes)


class LockFileException(MapdlRuntimeError):
    """Error message when the lockfile has not been removed"""

    def __init__(self, msg=LOCKFILE_MSG, notes: str = ""):
        super().__init__(msg=msg, notes=notes)


class MapdlDidNotStart(MapdlRuntimeError):
    """Error when the MAPDL process does not start"""

    def __init__(
        self,
        msg: str = "MAPDL failed to start",
        notes: str = "",
        stdout: str = "",
        stderr: str = "",
    ):
        super().__init__(msg=msg, notes=notes)
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        """Return the string representation of the exception."""
        msg = self.msg

        if self.stdout:
            msg += (
                f"\n{color_text('Terminal output (STDOUT):', 'INFO')}\n {self.stdout}"
            )

        if self.stderr:
            msg += f"\n{color_text('Terminal error output (STDERR):', 'INFO')}\n {self.stderr}"

        if self.notes:
            msg += f"\n{color_text('NOTES:', 'NOTES')} {self.notes}"

        return msg


class PortAlreadyInUse(MapdlDidNotStart):
    """Error when the port is already occupied"""

    def __init__(
        self, port: int = 50052, msg: str = "The port {port} is already being used."
    ):
        super().__init__(msg.format(port=port))


class PortAlreadyInUseByAnMAPDLInstance(PortAlreadyInUse):
    """Error when the port is already occupied"""

    def __init__(
        self,
        port: int = 50052,
        msg: str = "The port {port} is already used by an MAPDL instance.",
    ):
        super().__init__(port=port, msg=msg)


class MapdlConnectionError(MapdlRuntimeError):
    """Provides the error when connecting to the MAPDL instance fails."""

    pass


class LicenseServerConnectionError(MapdlDidNotStart):
    """Provides the error when the license server is not available."""

    pass


class NotAvailableLicenses(MapdlDidNotStart):
    """Provides the error when the license server is not available."""

    def __init__(self, msg=""):
        super().__init__(msg)


class IncorrectWorkingDirectory(OSError, MapdlRuntimeError):
    """Raised when the MAPDL working directory does not exist."""

    # The working directory specified (wrong_path) is not a directory.
    pass


class DifferentSessionConnectionError(MapdlRuntimeError):
    """Provides the error when connecting to the MAPDL instance fails."""

    pass


class DeprecationError(MapdlRuntimeError):
    """Provides the error for deprecated commands, classes, interfaces, etc"""

    pass


class MapdlError(MapdlException):
    """General MAPDL Error"""

    pass


class MapdlWarning(MapdlException):
    """General MAPDL warning"""

    pass


class MapdlNote(MapdlException):
    """General MAPDL note"""

    pass


class MapdlInfo(MapdlException):
    """General MAPDL info message"""

    pass


class MapdlVersionError(MapdlException):
    """Incompatible MAPDL version"""

    pass


class EmptyRecordError(MapdlRuntimeError):
    """Raised when a record is empty"""

    pass


class ComponentNoData(MapdlException):
    """Raised when the component has no data"""

    pass


class ComponentIsNotSelected(MapdlException):
    """Raised when the component is not selected"""

    pass


class ComponentDoesNotExits(MapdlException):
    """Raised when the component does not exist"""

    pass


class CommandDeprecated(DeprecationError):
    """Raised when a command is deprecated"""

    pass


class MapdlgRPCError(MapdlRuntimeError):
    """Raised when gRPC issues are found"""

    pass


class IncorrectMPIConfigurationError(MapdlDidNotStart):
    """Raised when the MPI configuration is incorrect"""

    def __init__(self, msg=""):
        super().__init__(msg)


class PluginError(MapdlRuntimeError):
    """Raised when a plugin fails"""

    def __init__(self, msg=""):
        super().__init__(msg)


class PluginLoadError(PluginError):
    """Raised when a plugin fails to load"""

    def __init__(self, msg=""):
        super().__init__(msg)


class PluginUnloadError(PluginError):
    """Raised when a plugin fails to unload"""

    def __init__(self, msg=""):
        super().__init__(msg)


# handler for protect_grpc
def handler(sig, frame):  # pragma: no cover
    """Pass signal to custom interrupt handler."""
    logger.info(
        "KeyboardInterrupt received.  Waiting until MAPDL " "execution finishes"
    )
    SIGINT_TRACKER.append(True)


def protect_grpc(func: Callable) -> Callable:
    """Capture gRPC exceptions and return a more succinct error message

    Capture KeyboardInterrupt to avoid segfaulting MAPDL.
    Responses exceeding the configured message size are not retried.

    This works some of the time, but not all the time.  For some
    reason gRPC still captures SIGINT.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Capture gRPC exceptions and KeyboardInterrupt"""

        # capture KeyboardInterrupt
        old_handler = None
        if threading.current_thread().__class__.__name__ == "_MainThread":
            if threading.current_thread().is_alive():
                old_handler = signal.signal(signal.SIGINT, handler)

        # Capture gRPC exceptions
        n_attempts = kwargs.get("n_attempts", N_ATTEMPTS)
        initial_backoff = kwargs.get("initial_backoff", INITIAL_BACKOFF)
        multiplier_backoff = kwargs.get("multiplier_backoff", MULTIPLIER_BACKOFF)

        i_attemps = 0

        while True:
            try:
                out = func(*args, **kwargs)

                # Exit while-loop if success
                break

            except ValueError as error:
                if "Cannot invoke RPC on closed channel" not in str(error):
                    raise

                mapdl = retrieve_mapdl_from_args(args)
                mapdl._log.debug("RPC invoked on a closed channel: MAPDL has exited.")
                mapdl._exited = True
                raise MapdlExitedError(
                    "MAPDL has exited: cannot invoke RPC on a closed channel."
                ) from error

            except grpc.FutureCancelledError as error:
                # Raised by 'MapdlGrpc._watched_call' cancelling the in-flight
                # call once the channel connectivity callback confirms the
                # transport is dead ('TRANSIENT_FAILURE'/'SHUTDOWN'), rather
                # than letting the call hang indefinitely.
                mapdl = retrieve_mapdl_from_args(args)
                channel_state = getattr(mapdl, "channel_state", None)
                mapdl._log.debug(
                    "The in-flight gRPC call was cancelled because the "
                    f"channel became '{channel_state}'."
                )
                msg = (
                    "The in-flight gRPC call was cancelled because the channel "
                    f"connectivity became '{channel_state}'. MAPDL might have died "
                    "or stopped answering."
                )
                # If MAPDL died, the reason is often only in its error file.
                error_file_tail = _get_error_file_tail(mapdl)
                if error_file_tail:
                    msg = f"{msg}\n{error_file_tail}"
                raise MapdlConnectionError(msg) from error

            except grpc.RpcError as error:
                mapdl = retrieve_mapdl_from_args(args)

                mapdl._log.debug(
                    f"A gRPC error has been detected: {error.code()}: {error.details()}"
                )

                # A response-size limit cannot be repaired by replaying the command.
                if error.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                    if "Received message larger than max" in error.details():
                        # Some gRPC versions wrap the message as
                        # "Stream removed (CLIENT: Received message larger
                        # than max (<received> vs. <limit>))", so the
                        # received size is matched with a regex instead of
                        # blindly splitting on "(".
                        match = re.search(r"\((\d+)\s*vs\.?\s*\d+\)", error.details())
                        if match:
                            lim_ = int(match.group(1))
                        else:
                            lim_ = int(512 * 1024**2)

                        raise MapdlgRPCError(
                            f"RESOURCE_EXHAUSTED: {error.details()}. "
                            "You can try to increase the gRPC message length size using 'PYMAPDL_MAX_MESSAGE_LENGTH'"
                            " environment variable. For instance:\n\n"
                            f"$ export PYMAPDL_MAX_MESSAGE_LENGTH={lim_}"
                        )

                # A method the server refuses is not repaired by replaying the call,
                # and MAPDL is still alive (commands keep working), so don't mark it exited.
                if error.code() == grpc.StatusCode.UNIMPLEMENTED:
                    raise MapdlgRPCError(
                        f"UNIMPLEMENTED: '{func.__name__}' was refused by the MAPDL server."
                    )

                if not mapdl.exited:
                    i_attemps += 1
                    if i_attemps <= n_attempts:

                        wait = (
                            initial_backoff * multiplier_backoff**i_attemps
                        )  # Exponential backoff

                        # reconnect
                        mapdl._log.debug(
                            f"Re-connection attempt {i_attemps} after waiting {wait:0.3f} seconds"
                        )

                        if not mapdl.is_alive:
                            connected = mapdl._connect(timeout=wait)
                        else:
                            sleep(wait)

                        # Retry again
                        continue

                # Custom errors
                reason = ""
                suggestion = ""

                # Every try to reconnecto to MAPDL failed
                # So let's avoid execution from now on.
                # The above exception should not break the channel.
                mapdl._exited = True

                if error.code() == grpc.StatusCode.UNAVAILABLE:
                    # Very likely the MAPDL server has died.
                    suggestion = _build_unavailable_suggestion(mapdl)

                # Generic error
                handle_generic_grpc_error(error, func, args, kwargs, reason, suggestion)

        # No exceptions
        if threading.current_thread().__class__.__name__ == "_MainThread":
            received_interrupt = bool(SIGINT_TRACKER)

            # always clear and revert to old handler
            SIGINT_TRACKER.clear()
            if old_handler:
                signal.signal(signal.SIGINT, old_handler)

            if received_interrupt:  # pragma: no cover
                raise KeyboardInterrupt("Interrupted during MAPDL execution")

        return out

    return wrapper


def _build_unavailable_suggestion(mapdl: "MapdlGrpc") -> str:
    """Build the user-facing suggestion for a ``UNAVAILABLE`` gRPC error.

    Parameters
    ----------
    mapdl : MapdlGrpc
        The MAPDL instance whose underlying process just became unreachable.

    Returns
    -------
    str
        A suggestion message. When the locally tracked MAPDL subprocess was
        terminated by ``SIGKILL``, the message calls that out explicitly and
        points to the OS Out-Of-Memory (OOM) killer as the most common cause.
        Otherwise, it falls back to the generic "might have died" message.

    Notes
    -----
    The exit signal can only be retrieved when PyMAPDL is the parent process
    of the local MAPDL subprocess (see
    :meth:`MapdlGrpc._get_process_exit_signal
    <ansys.mapdl.core.mapdl_grpc.MapdlGrpc._get_process_exit_signal>`). For
    remote or previously-running instances, this falls back to the generic
    message.
    """
    exit_signal = None
    get_exit_signal = getattr(mapdl, "_get_process_exit_signal", None)
    if callable(get_exit_signal):
        exit_signal = get_exit_signal()

    if exit_signal == _SIGKILL:
        return (
            "  MAPDL process was terminated with SIGKILL (signal 9).\n"
            "  This is commonly caused by the operating system's Out-Of-Memory (OOM) killer forcibly terminating the process,\n"
            "  but it can also happen if MAPDL was killed manually or by a job scheduler/resource limit.\n"
            "  Check 'dmesg' / 'journalctl -k' (Linux) or your job scheduler logs for confirmation, and consider reducing\n"
            "  model size, increasing available memory, or requesting more memory from your job scheduler.\n"
            "  Open an issue on GitHub if you need assistance: "
            "https://github.com/ansys/pymapdl/issues"
        )

    if exit_signal is not None:
        try:
            signal_name = signal.Signals(exit_signal).name
        except ValueError:
            signal_name = str(exit_signal)
        return (
            f"  MAPDL process was terminated by signal {exit_signal} ({signal_name}).\n"
            "  Check the MAPDL command output or system logs for more details.\n"
            "  Open an issue on GitHub if you need assistance: "
            "https://github.com/ansys/pymapdl/issues"
        )

    return (
        "  MAPDL *might* have died because it executed a not-allowed command or ran out of memory.\n"
        "  Check the MAPDL command output for more details.\n"
        "  Open an issue on GitHub if you need assistance: "
        "https://github.com/ansys/pymapdl/issues"
    )


def retrieve_mapdl_from_args(args: tuple[Any, ...]) -> "MapdlGrpc":
    # can't use isinstance here due to circular imports
    try:
        class_name = args[0].__class__.__name__
    except (IndexError, AttributeError):
        class_name = ""

    if class_name == "MapdlGrpc":
        mapdl = args[0]
    elif hasattr(args[0], "_mapdl"):
        mapdl = args[0]._mapdl
    else:
        raise TypeError(
            "The first argument must be a MapdlGrpc instance or an object with a '_mapdl' attribute."
        )

    return mapdl


def _read_error_file_tail(
    path: pathlib.Path, max_bytes: int, max_lines: int
) -> List[str]:
    """Return the last non-empty lines of an error file, or an empty list if it cannot be read."""
    try:
        with open(path, "rb") as fid:
            fid.seek(0, os.SEEK_END)
            size = fid.tell()
            fid.seek(max(0, size - max_bytes))
            content = fid.read()
    except OSError:
        return []

    lines = content.decode("latin-1").splitlines()
    if size > max_bytes and lines:
        lines = lines[1:]  # The first line is probably incomplete.
    return [line.rstrip() for line in lines if line.strip()][-max_lines:]


def _get_error_file_tail(
    mapdl: "MapdlGrpc",
    max_bytes: int = ERROR_FILE_TAIL_BYTES,
    max_lines: int = ERROR_FILE_TAIL_LINES,
    max_worker_files: int = ERROR_FILE_MAX_WORKER_FILES,
) -> str:
    """Return the last lines of the MAPDL error files of a local instance.

    When the MAPDL process dies, the reason is often written only to its error
    file, for example a license limit exceeded while meshing. This function
    reads the end of that file so the reason can be added to the exception
    message.

    The main error file is ``JOBNAME.err``, or ``JOBNAME0.err`` in distributed
    mode (the most recent one if both exist). In distributed mode, each process
    also writes its own ``JOBNAMEx.err`` file, where ``x`` is the process
    number, and an error in one of them might not reach ``JOBNAME0.err``.
    Those files are shown too, but only if their end contains an error or a
    fatal error. Files with a fatal error are shown first.

    Only cached attributes of the instance are used, because the MAPDL process
    cannot be queried once it has died.

    Parameters
    ----------
    mapdl : MapdlGrpc
        MAPDL instance whose process has died.
    max_bytes : int, default: 4096
        Number of bytes read from the end of each error file.
    max_lines : int, default: 20
        Maximum number of non-empty lines shown from each error file.
    max_worker_files : int, default: 3
        Maximum number of ``JOBNAMEx.err`` files (``x`` > 0) shown. The names of
        the remaining files with errors are listed.

    Returns
    -------
    str
        A message with the last lines of the error files, or an empty string
        if the instance is remote or no error file can be read.

    Examples
    --------
    >>> from ansys.mapdl.core.errors import _get_error_file_tail
    >>> print(_get_error_file_tail(mapdl))
    Last lines of the MAPDL error file 'C:/work/file.err':
      *** FATAL ***
      ...
    """
    if not getattr(mapdl, "_local", False):
        return ""

    directory = getattr(mapdl, "_path", None)
    if not directory:
        start_parm = getattr(mapdl, "_start_parm", None) or {}
        directory = start_parm.get("run_location")
    if not directory:
        return ""

    jobname = getattr(mapdl, "_jobname", None) or "file"
    pattern = re.compile(rf"{re.escape(jobname)}(\d*)\.err")
    main_files: List[pathlib.Path] = []
    worker_files: List[Tuple[int, pathlib.Path]] = []
    try:
        for path in pathlib.Path(str(directory)).iterdir():
            match = pattern.fullmatch(path.name)
            if not match or not path.is_file():
                continue
            rank = int(match.group(1) or 0)
            if rank == 0:
                main_files.append(path)
            else:
                worker_files.append((rank, path))
        # 'JOBNAME.err' and 'JOBNAME0.err' can both exist; the most recent one is the relevant one.
        main_file = max(main_files, key=lambda path: path.stat().st_mtime, default=None)
    except OSError:
        return ""

    sections = []
    if main_file is not None:
        lines = _read_error_file_tail(main_file, max_bytes, max_lines)
        if lines:
            sections.append((main_file, lines))

    failed_workers = []
    for rank, path in worker_files:
        lines = _read_error_file_tail(path, max_bytes, max_lines)
        has_fatal = any("*** FATAL ***" in line for line in lines)
        if has_fatal or any(
            header in line for line in lines for header in ERROR_FILE_HEADERS
        ):
            failed_workers.append((not has_fatal, rank, path, lines))
    # Fatal errors first, then by process number.
    failed_workers.sort(key=lambda item: item[:2])
    sections.extend(
        (path, lines) for _, _, path, lines in failed_workers[:max_worker_files]
    )

    message = ""
    for path, lines in sections:
        body = "\n".join(f"  {line}" for line in lines)
        message += f"Last lines of the MAPDL error file '{path.as_posix()}':\n{body}\n"

    not_shown = [path.name for _, _, path, _ in failed_workers[max_worker_files:]]
    if not_shown:
        message += "Other MAPDL error files with errors: " + ", ".join(not_shown) + "\n"
    return message


def handle_generic_grpc_error(
    error: grpc.RpcError,
    func: Callable[..., Any],
    args: Tuple[Any],
    kwargs: Dict[Any, Any],
    reason: str = "",
    suggestion: str = "",
):
    """Handle non-custom gRPC errors"""

    mapdl = retrieve_mapdl_from_args(args)

    # trying to get "cmd" argument:
    cmd = args[1] if len(args) >= 2 else ""
    cmd = kwargs.get("cmd", cmd)

    caller = func.__name__

    if cmd:
        msg_ = f"running:\n  {cmd}\ncalled by:\n  {caller}\n"
    else:
        msg_ = f"calling:{caller}\nwith the following arguments:\n  args: {args}\n  kwargs: {kwargs}"

    if reason:
        reason = f"Possible reason:\n{reason}\n"

    if suggestion:
        suggestion = f"Suggestions:\n{suggestion}\n"

    msg = (
        f"Error:\nMAPDL server connection terminated unexpectedly while {msg_}\n"
        f"{reason}"
        f"{suggestion}"
        "MAPDL instance:\n"
        f"  {mapdl._path}\n"
        f"  {mapdl.ip}:{mapdl.port}\n"
        "Error:\n"
        f"  {error.details()}\n"
        f"Full error:\n{error}"
    )

    # Generic error
    # Test if MAPDL is alive or not.
    if mapdl.is_alive:
        raise MapdlRuntimeError(msg)

    else:
        # The reason why MAPDL died is often only in its error file. Read it
        # before exiting, which might remove the working directory.
        error_file_tail = _get_error_file_tail(mapdl)
        if error_file_tail:
            msg = f"{msg}\n{error_file_tail}"

        # Making sure we do not keep executing gRPC calls.
        # Must close unfinished processes
        mapdl.exit()
        raise MapdlExitedError(msg)


def protect_from(
    exception, match: Optional[str] = None, condition: Optional[bool] = None
) -> Callable:
    """Protect the decorated method from raising an exception of
    of a given type.

    You can filter the exceptions by using 'match' and/or 'condition'. If both
    are given, **both** need to be fulfilled. If you only need one or the other,
    you can use multiple decorators.

    Parameters
    ----------
    exception : Exception
        Exception to catch.
    match : optional
        String against to match the exception, by default None
    condition : optional
        Condition that needs to be fulfil to catch the exception, by default None

    Returns
    -------
    Callable
        Decorated function

    Raises
    ------
    e
        The given exception if not caught by the internal try.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                return function(self, *args, **kwargs)
            except exception as e:
                if (match is None or match in str(e)) and (
                    condition is None or condition
                ):
                    pass
                # everything else raises
                else:
                    raise e

        return wrapper

    return decorator
