"""This module provides the tools for logging in PyAnsys"""

"""
# ``log`` module

## Objective
This module intends to create a general framework for logging in Pyansys.
This module is built upon ``logging`` library and it does NOT intend to replace it.
This module uses module logging, rather than log specific classes or functions.
This approach is simpler, since you do not need to carry around the logger.
However, for compatibility, the ``Mapdl._log`` has been redirected to the correspondent module logger.

## Usage

The approach is to call ``Getlogger``` at the beginning of each module we want to log.
This function works in several ways:

* If this is the first time that you call it, ``getLogger`` will create a new logger using the provided input or the default logger configuration.
* If ``getLogger`` has been called before, it will generate a child logger from the previously called logger.
    * If you only provide a name, the child logger will have no handlers and it will propagate its log to the parent one.
    * If ``file_msg`` and / or ``console_msg`` are provided in this call, the format of the child logger will be changed in the file stream and / or console stream.
    The parent handlers are copied into the child logger and the propagation from child to parent is disabled (See notes for further explanations).
    However, you can NOT change any other configuration of the logger.
    Attributes such as file name (``fname``), the log level (``loglevel``) or the options to record to file or console (``record_file`` and ``console_output``)
    cannot be changed at this step. This is to maintained the logging framework consistency.

This module detects automatically when the ``pool`` module is called for logging, and it adjust the log format in both cases, file and console streams.
The format is different for file and console output, being the file format a bit more detailed.

This module also write appropriate headers for the default file log handlers.

#### Default file header
.. code: :
    >> >
    Date Time               | Level name   | Module          | Function                  | Message
    ------------------------|--------------|-----------------|---------------------------|---------------------------


#### Default pool file header
.. code: :
    Date Time               | Level name   | Thread          | Module          | Function                  | Message
    ------------------------|--------------|-----------------|-----------------|---------------------------|---------------------------


## Output format

### Default console
.. code: :
    '%(levelname)-10s - %(module)-15s - %(funcName)s - %(message)s'


### Default file
.. code: :
    '%(asctime)-15s | %(levelname)-12s | %(module)-15s | %(funcName)-25s | %(message)s'


### Default pool console
.. code: :
    '%(levelname)-10s | %(threadName)-15s - %(module)-15s - %(funcName)s - %(message)s'


### Default pool file
.. code: :
    '%(asctime)-15s | %(levelname)-12s | %(threadName)-15s | %(module)-15s | %(funcName)-25s | %(message)s'


## Cases

### Log a module without changes in log format.
.. code-block: : python
    >> > from ansys.mapdl.core.log import getLogger
    >> > logger = getLogger(__name__)  # logger names as the module where it is imported.
    ...
    ...
    >> > logger.info('This is a useful message')
    INFO       |  test            - <module > - This is an useful message


### Log a module with changes in log format.
.. code-block: : python
    >> > from ansys.mapdl.core.log import getLogger
    >> > file_msg = '%(asctime)-15s | %(funcName)-25s | THIS IS A TEST %(message)s'
    >> > logger = getLogger(__name__, file_msg=file_msg)  # logger names as the module where it is imported.
    ...
    ...
    >> > logger.info('This is a useful message')
    INFO       |  test            - <module > - This is an useful message


## Notes

* To check if there is logger previously initialized by ``log`` module, we rely upon ``logging.root`` having or not the attribute ``last_logger``.
If this attribute does not exist, it is considered that ``getLogger`` hasn't been called and therefore, ``log`` hasn't been initialized previously.
* The ``propagate`` option is disabled when creating a child with different log format to avoid having the logs repeated from the same loggers since both loggers (child and parent) will share the handlers.
* This module check if ``pool`` module is called by checking the ``name`` parameter provided to ``getLogger``. If the string ``pool`` is found, it will be considered to be called from ``pool`` module.
* To log each thread, this module uses the flag ``% (threadName)s`` (more information on `LogRecord attributes < https: // docs.python.org/3/library/logging.html#logrecord-attributes/>`_) therefore, all the calls to ``Threading.Thread`` have been modified to include a thread name (``name``).
* For compatibility, the ``Mapdl._log`` has been redirected to the module logger, therefore you could do something like this in your script:
.. code: : python
    >> > from ansys.mapdl.core import launch_mapdl
    >> > mapdl = launch_mapdl()
    >> > mapdl._log.info('This is an useful message')
    INFO       | test            - <module > - This is an useful message  # Module is not defined since we are at ``__main__``

    ## Logic behind this module

    One of the objectives of this module was to provide a flexible tool to log in cases as different as being in a pool resource or running a single instance.
    Hence the format of the logs should be flexible and easy to change when logging in those cases but keeping the output streams.
    However, the ``logging`` module does not easy allow you to change this format once the logger has been created.
    Therefore the solution it is implemented here is to create a child logger which copies the handlers of the parent but it does set a different format.
    This way the output is still keep in place, but the format can be changed.
"""

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
