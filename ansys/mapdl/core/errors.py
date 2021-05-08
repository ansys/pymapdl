"""pymapdl specific errors"""
import logging
import threading
import signal
from functools import wraps

from grpc._channel import _InactiveRpcError, _MultiThreadedRendezvous

SIGINT_TRACKER = []

logger = logging.getLogger(__name__)


LOCKFILE_MSG = """
Another ANSYS job with the same job name is already running in this
directory, or the lock file has not been deleted from an abnormally
terminated ANSYS run.

Disable this check by passing ``override=True``

"""


TYPE_MSG = 'Invalid datatype.  Must be one of the following:\n' +\
    'np.int32, np.int64, or np.double'


class ANSYSDataTypeError(ValueError):
    """Raised when and invalid data type is sent to APDLMath"""

    def __init__(self, msg=TYPE_MSG):
        ValueError.__init__(self, msg)


class VersionError(ValueError):
    """Raised when MAPDL is the wrong version"""

    def __init__(self, msg='Invalid MAPDL version'):
        ValueError.__init__(self, msg)


class NoDistributedFiles(FileNotFoundError):
    """Unable to find any distributed result files """

    def __init__(self, msg='Unable to find any distributed result files'):
        FileNotFoundError.__init__(self, msg)


class MapdlRuntimeError(RuntimeError):
    """Raised when MAPDL passes an error"""
    pass


class MapdlInvalidRoutineError(RuntimeError):
    """Raised when MAPDL is in the wrong routine"""
    def __init__(self, msg=''):
        RuntimeError.__init__(self, msg)


class MapdlExitedError(RuntimeError):
    """Raised when MAPDL has exited"""

    def __init__(self, msg='MAPDL has exited'):
        RuntimeError.__init__(self, msg)


class LockFileException(RuntimeError):
    """Error message when the lockfile has not been removed"""
    def __init__(self, msg=LOCKFILE_MSG):
        RuntimeError.__init__(self, msg)


# handler for protect_grpc
def handler(sig, frame):  # pragma: no cover
    """Pass signal to custom interrupt handler."""
    logger.info('KeyboardInterrupt received.  Waiting until MAPDL '
                'execution finishes')
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
        if threading.current_thread().__class__.__name__ == '_MainThread':
            if threading.current_thread().is_alive():
                old_handler = signal.signal(signal.SIGINT, handler)

        # Capture gRPC exceptions
        try:
            out = func(*args, **kwargs)
        except (_InactiveRpcError, _MultiThreadedRendezvous) as error:
            # can't use isinstance here due to circular imports
            try:
                class_name = args[0].__class__.__name__
            except:
                class_name = ''

            if class_name == 'MapdlGrpc':
                mapdl = args[0]
            elif hasattr(args[0], '_mapdl'):
                mapdl = args[0]._mapdl

            # Must close unfinished processes
            mapdl._close_process()
            raise MapdlExitedError('MAPDL server connection terminated') from None

        if threading.current_thread().__class__.__name__ == '_MainThread':
            received_interrupt = bool(SIGINT_TRACKER)

            # always clear and revert to old handler
            SIGINT_TRACKER.clear()
            if old_handler:
                signal.signal(signal.SIGINT, old_handler)

            if received_interrupt:  # pragma: no cover
                raise KeyboardInterrupt('Interrupted during MAPDL execution')

        return out

    return wrapper
