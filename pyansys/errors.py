LOCKFILE_MSG = """
Another ANSYS job with the same job name is already running in this
directory, or the lock file has not been deleted from an abnormally
terminated ANSYS run.

Disable this check by passing ``override=True``

"""

EMAILME = """
The ANSYS gRPC interface currently requires the closed source python
module ``ansys.mapdl`` to open a connection to the gRPC server.
Please contact Alex Kaszynski at alexander.kaszynski@ansys.com to
request access to the code repository.
"""

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


class PrivateModuleImportError(ImportError):
    """Raised when attempting to import a closed source module"""

    def __init__(self, msg=EMAILME):
        ImportError.__init__(self, msg)
