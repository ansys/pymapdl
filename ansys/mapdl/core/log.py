import logging
from datetime import datetime
import sys

## General configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = 'pyansys.log'

## Single configuration
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
    _is_pool = False
    _level = logging.DEBUG

    def __init__(self, level=_level, filename=FILE_NAME, to_stdout=True):

        self._global = logging.getLogger('_Global_')

        if not self._global.handlers:
            self._global.level = level
            self._global._is_pool = self._is_pool
            self.add_handling_uncaught_expections(self._global) # Using logger to record unhandled exceptions

            if filename:
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

        else:
            self._level = self._global.level
            self._is_pool = self._global._is_pool
            self._file_handler = self._global.handlers[0]
            self._std_out_handler = self._global.handlers[1]

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, newlevel):
        if not isinstance(newlevel, int) and newlevel > 100 and newlevel < 0:
            raise Exception("The log level must be an integer and being between 0 and 100.")

        self._level = newlevel
        self._global.level = newlevel
        self._std_out_handler.setLevel(newlevel)
        self._file_handler.setLevel(newlevel)

    @property
    def is_pool(self):
        return self._is_pool

    @is_pool.setter
    def is_pool(self, newbool):
        if not isinstance(newbool, bool):
            raise Exception("'is_pool' arguments can be only booleans.")

        if newbool:
            self.debug("Switching to 'multiple thread' style logging.")
            if self._file_handler:
                self._file_handler.setFormatter(logging.Formatter(FILE_MSG_POOL_FORMAT))
                self._file_handler.stream.write(DEFAULT_FILE_HEADER_POOL)

            if self._std_out_handler:
                self._std_out_handler.setFormatter(logging.Formatter(STDOUT_MSG_POOL_FORMAT))
                self._std_out_handler.stream.write(DEFAULT_STDOUT_HEADER_POOL)
        else:
            if self._is_pool:
                self.debug("Switching back to 'single thread' style logging.")

            if self._file_handler:
                self._file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
                self._file_handler.stream.write(DEFAULT_FILE_HEADER)
            if self._std_out_handler:
                self._std_out_handler.setFormatter(logging.Formatter(STDOUT_MSG_FORMAT))
                self._std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

        self._is_pool = newbool
        self._global._is_pool = newbool

    def debug(self, *args, **kwargs):
        return self._global.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self._global.info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        return self._global.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        return self._global.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        return self._global.critical(*args, **kwargs)

    def add_handling_uncaught_expections(self, logger):

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.excepthook = handle_exception
