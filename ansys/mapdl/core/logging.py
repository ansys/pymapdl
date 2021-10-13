"""
# ``log`` module

## Objective
This module intends to create a general framework for logging in Pymapdl.
This module is built upon ``logging`` library and it does NOT intend to replace it rather provide a way to interact between ``logging`` and ``Pymapdl``.

The loggers used in the module include the name of the instance which is intended to be unique.
This name is printed in all the active outputs and it is used to track the different MAPDL instances.


## Usage

### Global logger
There is a global logger named ``pymapdl_global`` which is created at ``ansys.mapdl.core.__init__``.
If you want to use this global logger, you must call at the top of your module:

.. code::
    from ansys.mapdl.core import LOG

You could also rename it to avoid conflicts with other loggers (if any):

.. code::
    from ansys.mapdl.core import LOG as logger


To log using this logger, just call the desired method as a normal logger.

.. code::
    >>> import logging
    >>> from ansys.mapdl.core.logging import Logger
    >>> LOG = Logger(level=logging.DEBUG, to_file=False, to_stdout=True)
    >>> LOG.debug('This is LOG debug message.')

       | Level    | Instance        | Module           | Function             | Message
    |----------|-----------------|------------------|----------------------|--------------------------------------------------------
    | DEBUG    |                 |  __init__        | <module>             | This is LOG debug message.


By default, ``pymapdl_global`` does not output to file or stdout. You should activate it from ``__init__``.


### Instance logger
Every time that the class ``_MapdlCore`` is instantiated, a logger is created and stored in two places:

* ``_MapdlCore._log``. For backward compatibility.
* ``LOG._instances``. This field is a ``dict`` where the key is the name of the created logger.

These instance loggers inheritate the ``pymapdl_global`` output handlers and logging level unless otherwise specified.

You can use this logger like this:

.. code:: python
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info('This is an useful message')

    | Level    | Instance        | Module           | Function             | Message
    |----------|-----------------|------------------|----------------------|--------------------------------------------------------
    | INFO     | 127.0.0.1:50052 |  test            | <module>             | This is an useful message



### Other loggers
You can create your own loggers using python ``logging`` library as you would do in any other script.
There shall no be conflicts between these loggers.


## Notes


## To-Do's

* [] Make sure the logging level is changed when instance is created.

"""

import logging
from datetime import datetime
import sys
from copy import copy

## Default configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = 'Pymapdl.log'

# For convenience
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

## Formatting

STDOUT_MSG_FORMAT = '%(levelname)s - %(instance_name)s -  %(module)s - %(funcName)s - %(message)s'
FILE_MSG_FORMAT = STDOUT_MSG_FORMAT

DEFAULT_STDOUT_HEADER = """
LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER

NEW_SESSION_HEADER = f"""
===============================================================================
       NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
==============================================================================="""

string_to_loglevel = {
    'DEBUG': DEBUG,
    'INFO': INFO,
    'WARN': WARN,
    'ERROR': ERROR,
    'CRITICAL': CRITICAL,
}


class PymapdlCustomAdapter(logging.LoggerAdapter):
    """This is key to keep the reference to the MAPDL instance name dynamic.

    If we use the standard approach which is supplying ``extra`` input to the logger, we
    would need to keep inputting MAPDL instances every time we do a log.

    Using adapters we just need to specify the MAPDL instance we refer to once.
    """

    level = None  # This is maintained for compatibility with ``supress_logging``, but it does nothing.
    file_handler = None
    _stdout_handler = None

    def __init__(self, logger, extra=None):
        self.logger = logger
        self.extra = extra
        self.file_handler = logger.file_handler
        self.std_out_handler = logger.std_out_handler

    def process(self, msg, kwargs):
        kwargs['extra'] = {}
        # This are the extra parameters sent to log
        kwargs['extra']['instance_name'] = self.extra['name'] # here self.extra is the argument pass to the ``Pymapdl
        return msg, kwargs

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default FILE_NAME
        level : str, optional
            Level of logging. E.x. 'DEBUG'. By default LOG_LEVEL
        """

        self.logger = addfile_handler(self.logger, filename=filename, level=level, write_headers=True)
        self.file_handler = self.logger.file_handler

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default LOG_LEVEL
        """
        if self.std_out_handler:
            raise Exception('Stdout logger already defined.')

        self.logger = add_stdout_handler(self.logger, level=level)
        self.std_out_handler = self.logger.std_out_handler


class PymapdlPercentStyle(logging.PercentStyle):

    def __init__(self, fmt, *, defaults=None):
        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def _format(self, record):
        defaults = self._defaults
        if defaults:
            values = defaults | record.__dict__
        else:
            values = record.__dict__

        # We can do here any changes we want in record, for example adding a key.

        # We could create an if here if we want conditional formatting, and even
        # change the record.__dict__.
        # Since now we don't want to create conditional fields, it is fine to keep
        # the same MSG_FORMAT for all of them.
        if 'instance_name' not in values.keys():  # For the case of logging exceptions to the logger.
            values['instance_name'] = ''

        return STDOUT_MSG_FORMAT % values


class PymapdlFormatter(logging.Formatter):
    """Customized ``Formatter`` class used to overwrite the defaults format styles."""

    def __init__(self, fmt=STDOUT_MSG_FORMAT, datefmt=None, style='%', validate=True, *, defaults=None):
        super().__init__(fmt, datefmt, style, validate)
        self._style = PymapdlPercentStyle(fmt, defaults=defaults)  # overwriting


class Logger():
    """Logger used for each Pymapdl session.

    This class allows you to add handler to a file or standard output.

    Parameters
    ----------
    level : int, optional
        Logging level to filter the message severity allowed in the logger.
        The default is ``logging.DEBUG``.
    to_filet : bool, optional
        Write log messages to a file. The default is ``False``.
    to_stdout : bool, optional
        Write log messages into the standard output (terminal). The default is ``True``.
    filename : str, optional
        Name of the file where log messages are written to.
        The default is ``None``.
    """

    file_handler = None
    std_out_handler = None
    _level = logging.DEBUG
    _instances = {}

    def __init__(self, level=logging.DEBUG, to_file=False, to_stdout=True, filename=FILE_NAME):
        """Customized logger class for Pymapdl.

        Parameters
        ----------
        level : str, optional
            Level of logging as defined in the package ``logging``. By default _level.
        to_file : bool, optional
            To record the logs in a file, by default False
        to_stdout : bool, optional
            To output the logs to the standard output, which is the command line. By default True.
        filename : str, optional
            Name of the output file. By default FILE_NAME.
        """

        self.logger = logging.getLogger('pymapdl_global')  # Creating default main logger.
        self.logger.setLevel(level)
        self.logger.propagate = True
        self.level = self.logger.level # TODO: TO REMOVE

        # Writing logging methods.
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.log = self.logger.log

        if to_file or filename != FILE_NAME:
            # We record to file
            self.log_to_file(filename=filename, level=level)

        if to_stdout:
            self.log_to_stdout(level=level)

        self.add_handling_uncaught_expections(self.logger) # Using logger to record unhandled exceptions

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default FILE_NAME
        level : str, optional
            Level of logging. E.x. 'DEBUG'. By default LOG_LEVEL
        """

        self = addfile_handler(self, filename=filename, level=level, write_headers=True)

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default LOG_LEVEL
        """

        self = add_stdout_handler(self, level=level)

    def _make_child_logger(self, sufix, level):
        """Make a child logger, either using ``getChild`` or copying attributes between ``pymapdl_global``
        logger and the new one. """
        logger = logging.getLogger(sufix)
        logger.std_out_handler = None
        logger.file_handler = None

        if self.logger.hasHandlers:
            for each_handler in self.logger.handlers:
                new_handler = copy(each_handler)

                if each_handler == self.file_handler:
                    logger.file_handler = new_handler
                elif each_handler == self.std_out_handler:
                    logger.std_out_handler = new_handler

                if level:
                    # The logger handlers are copied and changed the loglevel is the specified log level
                    # is lower than the one of the global.
                    if each_handler.level > string_to_loglevel[level.upper()]:
                        new_handler.setLevel(level)

                logger.addHandler(new_handler)

        if level:
            if isinstance(level, str):
                level = string_to_loglevel[level.upper()]
            logger.setLevel(level)

        else:
            logger.setLevel(self.logger.level)

        logger.propagate = True
        return logger

    def add_child_logger(self, sufix, level=None):
        """Add a child logger to the main logger. This logger is more general than
        an instance logger which is designed to track the state of the MAPDL instances.

        If the logging level is in the arguments, a new logger with a reference to the ``_global`` logger handlers
        is created instead of a child.

        Parameters
        ----------
        sufix : str
            Name of the logger.
        level : str
            Level of logging

        Returns
        -------
        logging.logger
            Logger class.
        """
        name = self.logger.name + '.' + sufix
        self._instances[name] = self._make_child_logger(self, name, level)
        return self._instances[name]

    def _add_mapdl_instance_logger(self, name, mapdl_instance, level):
        if isinstance(name, str):
            instance_logger = PymapdlCustomAdapter(self._make_child_logger(name, level), mapdl_instance)
        elif isinstance(name, None):
            instance_logger = PymapdlCustomAdapter(self._make_child_logger("NO_NAMED_YET", level), mapdl_instance)
        else:
            raise ValueError("You can only input 'str' classes to this method.")

        return instance_logger
        # return.level = None # TODO: To remove

    def add_instance_logger(self, name, mapdl_instance, level=None):
        """Create a logger for a MAPDL instance.

        The MAPDL instance logger is a logger with an adapter which add the contextual
        information such as MAPDL instance name. This logger is returned and you can use
        it to log events as a normal logger. It is also stored in the ``_instances`` field.

        Parameters
        ----------
        name : str
            Name for the new logger
        mapdl_instance : ansys.mapdl.core.mapdl._MapdlCore
            Mapdl instance object. This should contain the attribute ``name``.

        Returns
        -------
        ansys.mapdl.core.logging.PymapdlCustomAdapter
            Logger adapter customized to add MAPDL information to the logs.
            You can use this class to log events in the same way you would with a logger
            class.

        Raises
        ------
        Exception
            You can only input strings as ``name`` to this method.
        """
        count_ = 0
        new_name = name
        while new_name in logging.root.manager.__dict__.keys():
            count_ += 1
            new_name = name + '_' + str(count_)

        self._instances[new_name] = self._add_mapdl_instance_logger(new_name, mapdl_instance, level)
        return self._instances[new_name]

    def __getitem__(self, key):
        if key in self._instances.keys():
            return self._instances[key]
        else:
            raise KeyError(f"There is no instances with name {key}")

    def add_handling_uncaught_expections(self, logger):
        """This just redirect the output of an exception to the logger."""
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.excepthook = handle_exception


## Auxiliary functions

def addfile_handler(logger, filename=FILE_NAME, level=LOG_LEVEL, write_headers=False):
    """
    Add a file handler to the input.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger where to add the file handler.
    filename : str, optional
        Name of the output file. By default FILE_NAME
    level : str, optional
        Level of log recording. By default LOG_LEVEL
    write_headers : bool, optional
        Record the headers to the file. By default False

    Returns
    -------
    logger
        Return the logger or Logger object.
    """

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))

    if isinstance(logger, Logger):
        logger.file_handler = file_handler
        logger.logger.addHandler(file_handler)

    elif isinstance(logger, logging.Logger):
        logger.addHandler(file_handler)

    if write_headers:
        file_handler.stream.write(NEW_SESSION_HEADER)
        file_handler.stream.write(DEFAULT_FILE_HEADER)

    return logger


def add_stdout_handler(logger, level=LOG_LEVEL, write_headers=True):
    """
    Add a file handler to the input.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger where to add the file handler.
    filename : str, optional
        Name of the output file. By default FILE_NAME
    level : str, optional
        Level of log recording. By default LOG_LEVEL
    write_headers : bool, optional
        Record the headers to the file. By default False

    Returns
    -------
    logger
        Return the logger or Logger object.
    """

    std_out_handler = logging.StreamHandler()
    std_out_handler.setLevel(level)
    std_out_handler.setFormatter(PymapdlFormatter(STDOUT_MSG_FORMAT))

    if isinstance(logger, Logger):
        logger.std_out_handler = std_out_handler
        logger.logger.addHandler(std_out_handler)

    elif isinstance(logger, logging.Logger):
        logger.addHandler(std_out_handler)

    if write_headers:
        std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    return logger
