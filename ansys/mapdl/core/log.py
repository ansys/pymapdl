"""This module provides the tools for logging in PyAnsys"""

# The approach is to call ``Getlogger``` at the beginning of each module.
# Functions in several ways:
# * If ``GetLogger`` gets called before any other logger has been initialized, it will create
# the default logger which parameters are constants in this module.
# * If ``GetLogger`` gets called after another logger has been created, there are two options:
#    * If we do not intend changes in the messages format or the caller is not the pool library, 
#      it will return a child logger. This child logger will redirect all the output to the main.
#    * If we do intend changes in the message format because maybe we want to account for
# different context (for example when using the ``pool`` module), a new child logger is created
#  with the same handlers as the parent and using the providen message format or the parent message format.
# You can change both, the file message format or the console message format. 
# But you cannot change the present handlers or the file where the log is being written.

# In cases we want to change the format according to different contexts, for example when the
# module launcher is called by the pool module:

# >

import logging
import sys, os


## General configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = 'pyansys.log'

## Single configuration
LAUNCHER_LOGGER = 'launcher'
CONSOLE_MSG_FORMAT = '%(levelname)-10s - %(module)-15s - %(funcName)s - %(message)s'
FILE_MSG_FORMAT = '%(asctime)-15s | %(levelname)-12s | %(module)-15s | %(funcName)-25s | %(message)s'
DEFAULT_FILE_HEADER = """
Date Time               | Level name   | Module          | Function                  | Message
------------------------|--------------|-----------------|---------------------------|---------------------------
"""

## Pool configuration
POOL_LOGGER = 'pool'
CONSOLE_MSG_POOL_FORMAT = '%(levelname)-10s | %(threadName)-15s - %(module)-15s - %(funcName)s - %(message)s'
FILE_MSG_POOL_FORMAT = '%(asctime)-15s | %(levelname)-12s | %(threadName)-15s | %(module)-15s | %(funcName)-25s | %(message)s'
DEFAULT_FILE_HEADER_POOL = """
Date Time               | Level name   | Thread          | Module          | Function                  | Message
------------------------|--------------|-----------------|-----------------|---------------------------|---------------------------
"""


def getLogger(name=None, record_file=True, console_output=True, file_msg=None, console_msg=None, fname=FILE_NAME, loglevel=LOG_LEVEL, record_uncaught_exceptions=True):
    """"""
    log_last_name = name.split('.')[-1] 
    # if we are creating a logger for the pool class:
    default_file_header = DEFAULT_FILE_HEADER_POOL if POOL_LOGGER in name else DEFAULT_FILE_HEADER

    if not hasattr(logging.root, '_last_logger'):
        # There is no parent logger, so we create it.
        logger = logging.getLogger(log_last_name)
        logger = _configure_default_logger(logger, loglevel, record_file, console_output, file_msg, console_msg, fname, default_file_header)

    else:
        # there are previous loggers defined.
        logger = _get_logger_child(name, record_file, console_output, file_msg, console_msg) 

        # There is a previous logger used
        # Since there is no easy way to modify the format at a given logger, we just create a new one (logger)
        # and pass the same file and stream handlers as the parent one, giving the option for change the format.

        if POOL_LOGGER == logger.parent.name or POOL_LOGGER == log_last_name:
            # Adding header again.
            with open(fname, 'a') as fid:
                fid.write(DEFAULT_FILE_HEADER_POOL)

    ## Using logger to record unhandled exceptions
    if record_uncaught_exceptions:
        add_handling_uncaught_expections(logger)

    return logger


# Create a class that extends the FileHandler class from logging.FileHandler
class FileHandlerWithHeader(logging.FileHandler):

    # Pass the file name and header string to the constructor.
    def __init__(self, *args, **kwargs):
        # self._builtin_open = super()._builtin_open

        # Store the header information.
        self.header = kwargs.pop('header', DEFAULT_FILE_HEADER)

        # Call the parent __init__
        super().__init__(*args, **kwargs)

        # Checking if the file is empty
        if os.stat(self.stream.name).st_size < 2: # <0 should be alright too.
            self.stream.write(self.header)


def add_handling_uncaught_expections(logger):

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception


def _configure_default_logger(logger, loglevel, record_file, console_output, file_msg, console_msg, fname, default_file_header):
    # There is no parent logger, so we create it.
    logging.root._last_logger = logger.name
    logging.root._first_logger = logger.name

    logger.setLevel(loglevel)
    if record_file:
        fh = FileHandlerWithHeader(fname, header=default_file_header)
        fh.setFormatter(logging.Formatter(file_msg or FILE_MSG_FORMAT))
        logger.addHandler(fh)

    if console_output:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(console_msg or CONSOLE_MSG_FORMAT))
        logger.addHandler(ch)

    logger.propagate = True  # Probably this is irrelevant.


def get_logger_parent():
    logger_name = logging.root._last_logger
    return previous_loggers()[logger_name]


def _instance_but_not_subclass(obj, _class):
    return type(obj) is _class


def previous_loggers():
    return logging.root.manager.__dict__['loggerDict']


def _get_logger_child(name, record_file, console_output, file_msg, console_msg):
    # is not empty
    log_last_name = name.split('.')[-1]
    logger = get_logger_parent().getChild(log_last_name)
    logging.root._last_logger = logger.name # Updating

    # Case that we are logging on pool.
    if POOL_LOGGER == log_last_name or POOL_LOGGER == logger.parent.name:
        if file_msg is None:
            file_msg = FILE_MSG_POOL_FORMAT
        if console_msg is None:
            console_msg = CONSOLE_MSG_POOL_FORMAT

    if file_msg is None and console_msg is None:
        # We are not going to change the message output, hence we can reuse the whole logger.
        return logger

    # There is a previous defined logger
    # Since there is no easy way to modify the format at a given logger, we just create a new one (logger)
    # and pass the same file and stream handlers as the parent one, giving the option for change the format.

    return _configure_child_logger(logger, record_file, console_output, file_msg, console_msg) 


def _configure_child_logger(logger, record_file, console_output, file_msg, console_msg):
    first_logger = previous_loggers()[logging.root._first_logger]

    file_handlers = [each_handler for each_handler in first_logger.handlers if _instance_but_not_subclass(
        each_handler, FileHandlerWithHeader)]
    console_handlers = [each_handler for each_handler in first_logger.handlers if _instance_but_not_subclass(
        each_handler, logging.StreamHandler)]

    if file_handlers:
        fh = file_handlers[0]
        fh.setFormatter(logging.Formatter(file_msg or fh.formatter._fmt))

    if console_handlers:
        ch = console_handlers[0]
        ch.setFormatter(logging.Formatter(console_msg or ch.formatter._fmt))

    logger.setLevel(first_logger.level)
    logger.propagate = False  # This is important to avoid duplicated logs.
    if record_file:
        logger.addHandler(fh)
    if console_output:
        logger.addHandler(ch)
    return logger
