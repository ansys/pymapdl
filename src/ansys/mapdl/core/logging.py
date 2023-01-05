"""Logging module.

This module supplies a general framework for logging in Pymapdl.  This module is
built upon `logging <https://docs.python.org/3/library/logging.html>`_ library
and it does not intend to replace it rather provide a way to interact between
``logging`` and PyMAPDL.

The loggers used in the module include the name of the instance which
is intended to be unique.  This name is printed in all the active
outputs and it is used to track the different MAPDL instances.


Usage
-----

Global logger
~~~~~~~~~~~~~
There is a global logger named ``pymapdl_global`` which is created at
``ansys.mapdl.core.__init__``.  If you want to use this global logger,
you must call at the top of your module:

.. code:: python

   from ansys.mapdl.core import LOG

You could also rename it to avoid conflicts with other loggers (if any):

.. code:: python

   from ansys.mapdl.core import LOG as logger


It should be noticed that the default logging level of ``LOG`` is ``ERROR``.
To change this and output lower level messages you can use the next snippet:

.. code:: python

   LOG.logger.setLevel("DEBUG")
   LOG.file_handler.setLevel("DEBUG")  # If present.
   LOG.stdout_handler.setLevel("DEBUG")  # If present.


Alternatively:

.. code:: python

   LOG.setLevel("DEBUG")

This way ensures all the handlers are set to the input log level.

By default, this logger does not log to a file. If you wish to do so,
you can add a file handler using:

.. code:: python

   import os

   file_path = os.path.join(os.getcwd(), "pymapdl.log")
   LOG.log_to_file(file_path)

This sets the logger to be redirected also to that file.  If you wish
to change the characteristics of this global logger from the beginning
of the execution, you must edit the file ``__init__`` in the directory
``ansys.mapdl.core``.

To log using this logger, just call the desired method as a normal logger.

.. code:: pycon

    >>> import logging
    >>> from ansys.mapdl.core.logging import Logger
    >>> LOG = Logger(level=logging.DEBUG, to_file=False, to_stdout=True)
    >>> LOG.debug("This is LOG debug message.")

    DEBUG -  -  <ipython-input-24-80df150fe31f> - <module> - This is LOG debug message.


Instance Logger
~~~~~~~~~~~~~~~
Every time an instance of :class:`Mapdl <ansys.mapdl.core.mapdl._MapdlCore>` is
created, a logger is created and stored in two places:

* ``_MapdlCore._log``. For backward compatibility.
* ``LOG._instances``. This field is a ``dict`` where the key is the name of the
  created logger.

These instance loggers inheritate the ``pymapdl_global`` output handlers and
logging level unless otherwise specified.  The way this logger works is very
similar to the global logger.  You can add a file handler if you wish using
:func:`log_to_file() <PymapdlCustomAdapter.log_to_file>` or change the log level
using :func:`logger.Logging.setLevel`.

You can use this logger like this:

.. code:: pycon
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info("This is a useful message")

    INFO - GRPC_127.0.0.1:50056 -  <ipython-input-19-f09bb2d8785c> - <module> - This is a useful message



Other loggers
~~~~~~~~~~~~~
You can create your own loggers using python ``logging`` library as
you would do in any other script.  There shall no be conflicts between
these loggers.

"""

from copy import copy
from datetime import datetime
import logging
import sys
import weakref

## Default configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = "pymapdl.log"

# For convenience
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

## Formatting

STDOUT_MSG_FORMAT = (
    "%(levelname)s - %(instance_name)s -  %(module)s - %(funcName)s - %(message)s"
)

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
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARN": WARN,
    "WARNING": WARN,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}


class PymapdlCustomAdapter(logging.LoggerAdapter):
    """This is key to keep the reference to the MAPDL instance name dynamic.

    If we use the standard approach which is supplying ``extra`` input
    to the logger, we would need to keep inputting MAPDL instances
    every time we do a log.

    Using adapters we just need to specify the MAPDL instance we refer
    to once.
    """

    level = None  # This is maintained for compatibility with ``supress_logging``, but it does nothing.
    file_handler = None
    stdout_handler = None

    def __init__(self, logger, extra=None):
        self.logger = logger
        if extra is not None:
            self.extra = weakref.proxy(extra)
        else:
            self.extra = None
        self.file_handler = logger.file_handler
        self.std_out_handler = logger.std_out_handler

    def process(self, msg, kwargs):
        kwargs["extra"] = {}
        # This are the extra parameters sent to log
        kwargs["extra"][
            "instance_name"
        ] = self.extra.name  # here self.extra is the argument pass to the log records.
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

        self.logger = addfile_handler(
            self.logger, filename=filename, level=level, write_headers=True
        )
        self.file_handler = self.logger.file_handler

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default LOG_LEVEL
        """
        if self.std_out_handler:
            raise Exception("Stdout logger already defined.")

        self.logger = add_stdout_handler(self.logger, level=level)
        self.std_out_handler = self.logger.std_out_handler

    def setLevel(self, level="DEBUG"):
        """Change the log level of the object and the attached handlers."""
        if isinstance(level, str):
            level = string_to_loglevel[level.upper()]
        self.logger.setLevel(level)
        for each_handler in self.logger.handlers:
            each_handler.setLevel(level)
        self.level = level


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

        # For the case of logging exceptions to the logger.
        values.setdefault("instance_name", "")

        return STDOUT_MSG_FORMAT % values


class PymapdlFormatter(logging.Formatter):
    """Customized ``Formatter`` class used to overwrite the defaults format styles."""

    def __init__(
        self,
        fmt=STDOUT_MSG_FORMAT,
        datefmt=None,
        style="%",
        validate=True,
        defaults=None,
    ):
        if sys.version_info[1] < 8:
            super().__init__(fmt, datefmt, style)
        else:
            # 3.8: The validate parameter was added
            super().__init__(fmt, datefmt, style, validate)
        self._style = PymapdlPercentStyle(fmt, defaults=defaults)  # overwriting


class InstanceFilter(logging.Filter):
    """Ensures that instance_name record always exists."""

    def filter(self, record):
        if not hasattr(record, "instance_name") and hasattr(record, "name"):
            record.instance_name = record.name
        elif not hasattr(record, "instance_name"):  # pragma: no cover
            record.instance_name = ""
        return True


class Logger:
    """Logger used for each Pymapdl session.

    This class allows you to add handlers to the logger to output to a file or
    standard output.

    Parameters
    ----------
    level : int, optional
        Logging level to filter the message severity allowed in the logger.
        The default is ``logging.DEBUG``.
    to_filet : bool, optional
        Write log messages to a file. The default is ``False``.
    to_stdout : bool, optional
        Write log messages into the standard output. The default is
        ``True``.
    filename : str, optional
        Name of the file where log messages are written to.
        The default is ``None``.

    Examples
    --------
    Demonstrate logger usage from an instance mapdl. This is automatically
    created when creating an Mapdl instance.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl(loglevel='DEBUG')
    >>> mapdl._log.info('This is a useful message')
    INFO -  -  <ipython-input-24-80df150fe31f> - <module> - This is LOG debug message.

    Import the global pymapdl logger and add a file output handler.

    >>> import os
    >>> from ansys.mapdl.core import LOG
    >>> file_path = os.path.join(os.getcwd(), 'pymapdl.log')
    >>> LOG.log_to_file(file_path)

    """

    file_handler = None
    std_out_handler = None
    _level = logging.DEBUG
    _instances = {}

    def __init__(
        self,
        level=logging.DEBUG,
        to_file=False,
        to_stdout=True,
        filename=FILE_NAME,
    ):
        """Customized logger class for Pymapdl.

        Parameters
        ----------
        level : str, optional
            Level of logging as defined in the package ``logging``. By default 'DEBUG'.
        to_file : bool, optional
            To record the logs in a file, by default ``False``.
        to_stdout : bool, optional
            To output the logs to the standard output, which is the
            command line. By default ``True``.
        filename : str, optional
            Name of the output file. By default ``pymapdl.log``.
        """

        # create default main logger
        self.logger = logging.getLogger("pymapdl_global")
        self.logger.addFilter(InstanceFilter())
        if isinstance(level, str):
            level = level.upper()

        self.logger.setLevel(level)
        self.logger.propagate = True
        self.level = self.logger.level  # TODO: TO REMOVE

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

        # Using logger to record unhandled exceptions
        self.add_handling_uncaught_expections(self.logger)

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default
            ``'pymapdl.log'``.
        level : str, optional
            Level of logging. By default ``'DEBUG'``.

        Examples
        --------
        Write to ``pymapdl.log`` in the current working directory.

        >>> from ansys.mapdl.core import LOG
        >>> import os
        >>> file_path = os.path.join(os.getcwd(), 'pymapdl.log')
        >>> LOG.log_to_file(file_path)

        """

        self = addfile_handler(self, filename=filename, level=level, write_headers=True)

    def log_to_stdout(self, level=LOG_LEVEL):
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default  ``'DEBUG'``.
        """

        self = add_stdout_handler(self, level=level)

    def setLevel(self, level="DEBUG"):
        """Change the log level of the object and the attached handlers."""
        if isinstance(level, str):
            level = string_to_loglevel[level.upper()]
        self.logger.setLevel(level)
        for each_handler in self.logger.handlers:
            each_handler.setLevel(level)
        self._level = level

    def _make_child_logger(self, sufix, level):
        """Create a child logger.

        Uses ``getChild`` or copying attributes between ``pymapdl_global``
        logger and the new one.
        """
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
                    # The logger handlers are copied and changed the loglevel is
                    # the specified log level is lower than the one of the
                    # global.
                    if isinstance(level, str):
                        new_loglevel = string_to_loglevel[level.upper()]
                    elif isinstance(level, (int, float)):  # pragma: no cover
                        new_loglevel = level

                    if each_handler.level > new_loglevel:
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
        """Add a child logger to the main logger.

        This logger is more general than an instance logger which is designed to
        track the state of the MAPDL instances.

        If the logging level is in the arguments, a new logger with a reference
        to the ``_global`` logger handlers is created instead of a child.

        Parameters
        ----------
        sufix : str
            Name of the logger.
        level : str, optional
            Level of logging

        Returns
        -------
        logging.logger
            Logger class.
        """
        name = self.logger.name + "." + sufix
        self._instances[name] = self._make_child_logger(self, name, level)
        return self._instances[name]

    def _add_mapdl_instance_logger(self, name, mapdl_instance, level):
        if isinstance(name, str):
            instance_logger = PymapdlCustomAdapter(
                self._make_child_logger(name, level), mapdl_instance
            )
        elif not name:  # pragma: no cover
            instance_logger = PymapdlCustomAdapter(
                self._make_child_logger("NO_NAMED_YET", level), mapdl_instance
            )
        else:
            raise ValueError("You can only input 'str' classes to this method.")

        return instance_logger

    def add_instance_logger(self, name, mapdl_instance, level=None):
        """Create a logger for a MAPDL instance.

        The MAPDL instance logger is a logger with an adapter which add the
        contextual information such as MAPDL instance name. This logger is
        returned and you can use it to log events as a normal logger. It is also
        stored in the ``_instances`` field.

        Parameters
        ----------
        name : str
            Name for the new logger
        mapdl_instance : ansys.mapdl.core.mapdl._MapdlCore
            Mapdl instance object. This should contain the attribute ``name``.

        Returns
        -------
        ansys.mapdl.core.logging.PymapdlCustomAdapter
            Logger adapter customized to add MAPDL information to the
            logs.  You can use this class to log events in the same
            way you would with the logger class.

        Raises
        ------
        Exception
            You can only input strings as ``name`` to this method.
        """
        count_ = 0
        new_name = name
        while new_name in logging.root.manager.__dict__.keys():
            count_ += 1
            new_name = name + "_" + str(count_)

        self._instances[new_name] = self._add_mapdl_instance_logger(
            new_name, mapdl_instance, level
        )
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
            logger.critical(
                "Uncaught exception",
                exc_info=(exc_type, exc_value, exc_traceback),
            )

        sys.excepthook = handle_exception


def addfile_handler(logger, filename=FILE_NAME, level=LOG_LEVEL, write_headers=False):
    """Add a file handler to the input.

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
        logger.file_handler = file_handler
        logger.addHandler(file_handler)

    if write_headers:
        file_handler.stream.write(NEW_SESSION_HEADER)
        file_handler.stream.write(DEFAULT_FILE_HEADER)

    return logger


def add_stdout_handler(logger, level=LOG_LEVEL, write_headers=False):
    """Add a file handler to the logger.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger where to add the file handler.
    level : str, optional
        Level of log recording. By default ``logging.DEBUG``.
    write_headers : bool, optional
        Record the headers to the file. By default ``False``.

    Returns
    -------
    logger
        The logger or Logger object.
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
