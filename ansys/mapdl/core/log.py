import logging
from datetime import datetime
import sys

from ansys.mapdl.core.mapdl import _MapdlCore

## General configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = 'pyansys.log'

## Single configuration #79
STDOUT_MSG_FORMAT = '| %(levelname)-11s | %(module)-15s | %(funcName)-25s | %(message)s'
FILE_MSG_FORMAT = '| %(asctime)-15s | %(levelname)-12s | %(module)-15s | %(funcName)-25s | %(message)s'
DEFAULT_FILE_HEADER = """
| Date Time               | Level name   | Module          | Function                  | Message
|-------------------------|--------------|-----------------|---------------------------|---------------------------
"""
DEFAULT_STDOUT_HEADER = """
| Level name  | Module          | Function                  | Message
|-------------|-----------------|---------------------------|---------------------------
"""

## Pool configuration
STDOUT_MSG_POOL_FORMAT = '| %(levelname)-12s | %(threadName)-15s | %(module)-15s | %(funcName)-25s | %(message)s'
FILE_MSG_POOL_FORMAT = '| %(asctime)-15s | %(levelname)-12s | %(threadName)-15s | %(module)-15s | %(funcName)-25s | %(message)s'
DEFAULT_FILE_HEADER_POOL = """
| Date Time               | Level name   | Thread          | Module          | Function                  | Message
|-------------------------|--------------|-----------------|-----------------|---------------------------|---------------------------
"""
DEFAULT_STDOUT_HEADER_POOL = """
| Level name   | Thread          | Module          | Function                  | Message
|--------------|-----------------|-----------------|---------------------------|---------------------------
"""

NEW_SESSION_HEADER = f"""\n=====================================================================================================================================
========================                      NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}                             ========================
====================================================================================================================================="""

#changing the log record.
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.custom_attribute = 0xdecafbad
    return record

logging.setLogRecordFactory(record_factory)

class PyansysLogger():
    """Logger used for each Pyansys logger.
    This class allows you to add handler to a file or standard output.
    Parameters
    ----------
    level : int, optional
        Logging level to filter the message severity allowed in the logger.
        The default is ``logging.DEBUG``.
    filename : str, optional
        Name of the file where log messages can be written to.
        The default is ``None``.
    to_stdout : bool, optional
        Write log message into the standard output. The default is ``False``.
    """

    _file_handler = None
    _std_out_handler = None 
    _level = logging.DEBUG
    _instances = {}

    def __init__(self, level=_level, to_file=False, to_stdout=True, filename=FILE_NAME):

        self._global = logging.getLogger('_Global_')
        self._global.level = level

        self.debug    = self._global.debug
        self.info     = self._global.info
        self.warning  = self._global.warning
        self.error    = self._global.error
        self.critical = self._global.critical

        if to_file or filename != FILE_NAME:
            # We record to file
            self._file_handler = logging.FileHandler(filename)
            self._file_handler.setLevel(level)
            self._file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
            self._global.addHandler(self._file_handler)

            self._file_handler.stream.write(NEW_SESSION_HEADER)
            self._file_handler.stream.write(DEFAULT_FILE_HEADER)

        if to_stdout:
            self._std_out_handler = logging.StreamHandler()
            self._std_out_handler.setLevel(level)
            self._std_out_handler.setFormatter(logging.Formatter(STDOUT_MSG_FORMAT))
            self._global.addHandler(self._std_out_handler)

            self._std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

        self.add_handling_uncaught_expections(self._global) # Using logger to record unhandled exceptions

    def _add_instance(self, obj):
        if isinstance(obj, str):
            self._instances[obj] = self._global.getChild(obj)
        elif issubclass(obj, _MapdlCore):
            self._instances[obj._name] = self._global.getChild(obj._name)
        else:
            raise Exception("You can only add 'str' or 'MAPDL' classes to this method.")
        return self._instances[obj]

    def __getitem__(self, key):
        if key in self._instances.keys():
            return self._instances[key]
        else:
            raise KeyError(f"There is no instances with name {key}")

    def add_handling_uncaught_expections(self, logger):
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.excepthook = handle_exception
