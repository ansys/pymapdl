# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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
from functools import wraps
import signal
import threading
from time import sleep
from typing import Callable, Optional

import grpc

from ansys.mapdl.core import LOG as logger

SIGINT_TRACKER = []


LOCKFILE_MSG = """
Another ANSYS job with the same job name is already running in this
directory, or the lock file has not been deleted from an abnormally
terminated ANSYS run.

Disable this check by passing ``override=True``

"""


TYPE_MSG = (
    "Invalid datatype.  Must be one of the following:\n"
    + "np.int32, np.int64, or np.double"
)


## Abraham class
class MapdlException(Exception):
    """MAPDL general exception"""

    def __init__(self, msg=""):
        super().__init__(msg)


## Main subclasses
class MapdlValueError(MapdlException, ValueError):
    """MAPDL Value error"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlFileNotFoundError(MapdlException, FileNotFoundError):
    """Error when file is not found"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlRuntimeError(MapdlException, RuntimeError):
    """Raised when MAPDL passes an error"""

    def __init__(self, msg=""):
        super().__init__(msg)


## Inheritated
class ANSYSDataTypeError(MapdlValueError):
    """Raised when and invalid data type is sent to APDLMath"""

    def __init__(self, msg=TYPE_MSG):
        super().__init__(msg)


class VersionError(MapdlValueError):
    """Raised when MAPDL is the wrong version"""

    def __init__(self, msg="Invalid MAPDL version"):
        super().__init__(msg)


class NoDistributedFiles(MapdlFileNotFoundError):
    """Unable to find any distributed result files"""

    def __init__(self, msg="Unable to find any distributed result files"):
        super().__init__(msg)


class MapdlInvalidRoutineError(MapdlRuntimeError):
    """Raised when MAPDL is in the wrong routine"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlCommandIgnoredError(MapdlRuntimeError):
    """Raised when MAPDL ignores a command."""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlExitedError(MapdlRuntimeError):
    """Raised when MAPDL has exited"""

    def __init__(self, msg="MAPDL has exited"):
        super().__init__(msg)


class NotEnoughResources(MapdlExitedError):
    """Raised when MAPDL has exited"""

    def __init__(
        self,
        msg="MAPDL has exited because there is not enough resources ({resource})",
        resource="CPUs",
    ):
        super().__init__(msg.format(resource=resource))


class LockFileException(MapdlRuntimeError):
    """Error message when the lockfile has not been removed"""

    def __init__(self, msg=LOCKFILE_MSG):
        super().__init__(msg)


class MapdlDidNotStart(MapdlRuntimeError):
    """Error when the MAPDL process does not start"""

    def __init__(self, msg=""):
        super().__init__(msg)


class PortAlreadyInUse(MapdlDidNotStart):
    """Error when the port is already occupied"""

    def __init__(self, port=50052, msg="The port {port} is already being used."):
        super().__init__(msg.format(port=port))


class PortAlreadyInUseByAnMAPDLInstance(PortAlreadyInUse):
    """Error when the port is already occupied"""

    def __init__(
        self, port=50052, msg="The port {port} is already used by an MAPDL instance."
    ):
        super().__init__(msg.format(port=port))


class MapdlConnectionError(MapdlRuntimeError):
    """Provides the error when connecting to the MAPDL instance fails."""

    def __init__(self, msg=""):
        super().__init__(msg)


class LicenseServerConnectionError(MapdlDidNotStart):
    """Provides the error when the license server is not available."""

    def __init__(self, msg=""):
        super().__init__(msg)


class IncorrectWorkingDirectory(OSError, MapdlRuntimeError):
    """Raised when the MAPDL working directory does not exist."""

    # The working directory specified (wrong_path) is not a directory.
    def __init__(self, msg=""):
        super().__init__(msg)


class DifferentSessionConnectionError(MapdlRuntimeError):
    """Provides the error when connecting to the MAPDL instance fails."""

    def __init__(self, msg=""):
        super().__init__(msg)


class DeprecationError(MapdlRuntimeError):
    """Provides the error for deprecated commands, classes, interfaces, etc"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlError(MapdlException):
    """General MAPDL Error"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlWarning(MapdlException):
    """General MAPDL warning"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlNote(MapdlException):
    """General MAPDL note"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlInfo(MapdlException):
    """General MAPDL info message"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlVersionError(MapdlException):
    """Incompatible MAPDL version"""

    def __init__(self, msg=""):
        super().__init__(msg)


class EmptyRecordError(MapdlRuntimeError):
    """Raised when a record is empty"""

    def __init__(self, msg=""):
        super().__init__(msg)


class ComponentNoData(MapdlException):
    """Raised when the component has no data"""

    def __init__(self, msg=""):
        super().__init__(msg)


class ComponentIsNotSelected(MapdlException):
    """Raised when the component is not selected"""

    def __init__(self, msg=""):
        super().__init__(msg)


class ComponentDoesNotExits(MapdlException):
    """Raised when the component does not exist"""

    def __init__(self, msg=""):
        super().__init__(msg)


class CommandDeprecated(DeprecationError):
    """Raised when a command is deprecated"""

    def __init__(self, msg=""):
        super().__init__(msg)


class MapdlgRPCError(MapdlRuntimeError):
    """Raised when gRPC issues are found"""

    def __init__(self, msg=""):
        super().__init__(msg)


# handler for protect_grpc
def handler(sig, frame):  # pragma: no cover
    """Pass signal to custom interrupt handler."""
    logger.info(
        "KeyboardInterrupt received.  Waiting until MAPDL " "execution finishes"
    )
    SIGINT_TRACKER.append(True)


def protect_grpc(func):
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
        n_attempts = 3
        initial_backoff = 0.05
        multiplier_backoff = 3

        i_attemps = 0

        while True:
            try:
                out = func(*args, **kwargs)

                # Exit while-loop if success
                break

            except grpc.RpcError as error:

                mapdl = retrieve_mapdl_from_args(args)
                mapdl._log.debug("A gRPC error has been detected.")

                i_attemps += 1
                if i_attemps <= n_attempts:

                    wait = (
                        initial_backoff * multiplier_backoff**i_attemps
                    )  # Exponential backoff
                    sleep(wait)

                    # reconnect
                    mapdl._log.debug(
                        f"Re-connection attempt {i_attemps} after waiting {wait:0.3f} seconds"
                    )

                    connected = mapdl._connect(timeout=wait)

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


def retrieve_mapdl_from_args(args):
    # can't use isinstance here due to circular imports
    try:
        class_name = args[0].__class__.__name__
    except (IndexError, AttributeError):
        class_name = ""

    if class_name == "MapdlGrpc":
        mapdl = args[0]
    elif hasattr(args[0], "_mapdl"):
        mapdl = args[0]._mapdl

    return mapdl


def handle_generic_grpc_error(error, func, args, kwargs, reason="", suggestion=""):
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
        mapdl._exited = True
        mapdl._exiting = True

        # Must close unfinished processes
        mapdl._close_process()
        mapdl._exiting = False
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
