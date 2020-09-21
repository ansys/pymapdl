LOCKFILE_MSG = """
Another ANSYS job with the same job name is already running in this
directory, or the lock file has not been deleted from an abnormally
terminated ANSYS run.

Disable this check by passing ``override=True``

"""

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
