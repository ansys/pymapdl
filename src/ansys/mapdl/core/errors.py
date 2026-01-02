# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""PyMAPDL specific errors"""
from enum import Enum
from functools import cache, wraps
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

# Configuration of 'protect_grpc' wrapper
N_ATTEMPTS = 5
INITIAL_BACKOFF = 0.1
MULTIPLIER_BACKOFF = 2


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


class MapdlCommandIgnoredError(MapdlRuntimeError):
    """Raised when MAPDL ignores a command."""

    pass


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

            except grpc.RpcError as error:
                mapdl = retrieve_mapdl_from_args(args)

                mapdl._log.debug("A gRPC error has been detected.")

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

                if error.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
                    if "Received message larger than max" in error.details():
                        try:
                            lim_ = int(error.details().split("(")[1].split("vs")[0])
                        except IndexError:
                            lim_ = int(512 * 1024**2)

                        raise MapdlgRPCError(
                            f"RESOURCE_EXHAUSTED: {error.details()}. "
                            "You can try to increase the gRPC message length size using 'PYMAPDL_MAX_MESSAGE_LENGTH'"
                            " environment variable. For instance:\n\n"
                            f"$ export PYMAPDL_MAX_MESSAGE_LENGTH={lim_}"
                        )

                # Every try to reconnecto to MAPDL failed
                # So let's avoid execution from now on.
                # The above exception should not break the channel.
                mapdl._exited = True

                if error.code() == grpc.StatusCode.UNAVAILABLE:
                    # Very likely the MAPDL server has died.
                    suggestion = (
                        "  MAPDL *might* have died because it executed a not-allowed command or ran out of memory.\n"
                        "  Check the MAPDL command output for more details.\n"
                        "  Open an issue on GitHub if you need assistance: "
                        "https://github.com/ansys/pymapdl/issues"
                    )

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
