"""This module provides the tools for logging in PyAnsys"""

# The approach is to call ``Getlogger``` at the beginning of each module.
# Functions in several ways:
# * If ``GetLogger`` gets called before any other logger has been initialized, it will create
# the default logger which parameters are a constant in this module.
# * If ``GetLogger`` gets called after another logger has been created, there are two options:
#    * If we do not intend changes in the messages format, it will return a child logger with
# the default name. This child logger will redirect all the output to the main.
#    * If we do intend changes in the message format because maybe we want to account for
# different context, a new child logger is created with the same handlers as the parent and
# using the providen message format or the parent message format.
#
# In cases we want to change the format according to different contexts, for example when the
# module launcher is called by the pool module:
#
# >

import logging
import sys, os
import threading


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


def getLogger(name=None, file_msg=None, console_msg=None, fname=None, loglevel=LOG_LEVEL, record_uncaught_exceptions=True):

    default_file_header = DEFAULT_FILE_HEADER_POOL if name == POOL_LOGGER else DEFAULT_FILE_HEADER
    log_name = name.split('.')[-1]

    previous_loggers = logging.root.manager.__dict__['loggerDict']
    loggers = [each_logger for each_logger in previous_loggers.keys() if LAUNCHER_LOGGER in each_logger or POOL_LOGGER in each_logger]

    if loggers:
        # is not empty
        # parent_logger = list(previous_loggers.values())[-1]  #
        # logger = parent_logger.getChild(name)
        # hierarchy_len = [len(each.split('.')) for each in loggers]
        # logger_name = [value for index, value in enumerate(loggers) if hierarchy_len[index] == max(hierarchy_len)][0]
        # logger_name = loggers[]
        logger_name = logging.root.last_logger
        logger = previous_loggers[logger_name].getChild(log_name)
        logging.root.last_logger = logger.name

        if file_msg is None and console_msg is None and logger.parent.name != POOL_LOGGER:
            # We are not going to change the message output, hence we can reuse the whole logger.
            return logger

        def instance_but_not_subclass(obj, klass):
            return type(obj) is klass

        # There is a previous logger used
        # Since there is no easy way to modify the format at a given logger, we just create a new one (logger)
        # and pass the same file and stream handlers as the parent one, giving the option for change the format.
        first_logger = previous_loggers[logging.root.first_logger]
        fh = [each_handler for each_handler in first_logger.handlers if instance_but_not_subclass(
            each_handler, FileHandlerWithHeader)][0]
        ch = [each_handler for each_handler in first_logger.handlers if instance_but_not_subclass(
            each_handler, logging.StreamHandler)][0]

        if logger.parent.name == POOL_LOGGER:
            fh.setFormatter(logging.Formatter(
                file_msg or FILE_MSG_POOL_FORMAT))
            ch.setFormatter(logging.Formatter(
                console_msg or CONSOLE_MSG_POOL_FORMAT))

            # patch_threading_excepthook()

        else:
            fh.setFormatter(logging.Formatter(file_msg or fh.formatter._fmt))
            ch.setFormatter(logging.Formatter(
                console_msg or ch.formatter._fmt))

        logger.setLevel(logger.parent.level)
        logger.propagate = False  # This is important to avoid duplicated logs.

    else:
        # There is no parent logger, so we create it.
        logger = logging.getLogger(log_name)
        logging.root.last_logger = logger.name
        logging.root.first_logger = logger.name
        logger.setLevel(loglevel)
        ch = logging.StreamHandler()
        fh = FileHandlerWithHeader(
            fname or FILE_NAME, header=default_file_header)

        fh.setFormatter(logging.Formatter(file_msg or FILE_MSG_FORMAT))
        ch.setFormatter(logging.Formatter(console_msg or CONSOLE_MSG_FORMAT))
        logger.propagate = True  # Probably this is irrelevant.

    logger.addHandler(ch)
    logger.addHandler(fh)

    ## Using logger to record unhandled exceptions

    if record_uncaught_exceptions:
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        sys.excepthook = handle_exception

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

        if os.stat(self.stream.name).st_size < 2: # <0 should be alright.
            self.stream.write(self.header)
