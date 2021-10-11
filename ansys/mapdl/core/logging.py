"""


"""

import logging
from datetime import datetime
import sys

## Default configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = 'pyansys.log'


## Formatting

STDOUT_MSG_FORMAT = '| %(levelname)-8s | %(instance_name)-15s |  %(module)-15s | %(funcName)-20s | %(message)s'
FILE_MSG_FORMAT = STDOUT_MSG_FORMAT

DEFAULT_STDOUT_HEADER = """
| Level    | Instance        | Module           | Function             | Message
|----------|-----------------|------------------|----------------------|--------------------------------------------------------
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER

NEW_SESSION_HEADER = f"""\n=====================================================================================================================================
========================                      NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}                             ========================
====================================================================================================================================="""


## Code

class PyansysCustomAdapter(logging.LoggerAdapter):
    """
    This is key to keep the reference to the MAPDL instance name dynamic.
    If we use the standard approach which is supplying ``extra`` input to the logger, we
    would need to keep inputting MAPDL instances everytime we do a log.

    Using adapters we just need to especify the MAPDL instance we refer to once.
    """

    level = None  # This is maintained for compatibility with ``supress_logging``, but it does nothing.
    _file_handler = None
    _stdout_handler = None

    def __init__(self, logger, extra=None):
        self.logger = logger
        self.extra = extra
        self._file_handler = logger._file_handler
        self._std_out_handler = logger._std_out_handler

    def process(self, msg, kwargs):
        kwargs['extra'] = {}
        # This are the extra parameters sent to log
        kwargs['extra']['instance_name'] = self.extra['name'] # here self.extra is the argument pass to the ``PyAnsys
        return msg, kwargs

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """
        Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default FILE_NAME
        level : str, optional
            Level of logging. E.x. 'DEBUG'. By default LOG_LEVEL
        """

        self.logger = add_file_handler(self.logger, filename=filename, level=level, write_headers=True)
        self._file_handler = self.logger._file_handler

    def log_to_stdout(self, level=LOG_LEVEL):
        """
        Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default LOG_LEVEL
        """

        self.logger = add_stdout_handler(self.logger, level=level)
        self._std_out_handler = self.logger._std_out_handler

    ## Copy functions
    add_stdout_handler = log_to_stdout
    add_file_handler = log_to_file


class PyAnsysPercentStyle(logging.PercentStyle):

    def __init__(self, fmt, *, defaults=None):
        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def _format(self, record):
        if defaults := self._defaults:
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


class PyAnsysFormatter(logging.Formatter):
    """Customized ``Formatter`` class used to overwrite the defaults format styles."""

    def __init__(self, fmt=STDOUT_MSG_FORMAT, datefmt=None, style='%', validate=True, *, defaults=None):
        super().__init__(fmt, datefmt, style, validate)
        self._style = PyAnsysPercentStyle(fmt, defaults=defaults)  # overwritting


class PyansysLogger():
    """Logger used for each Pyansys logger.
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

    _file_handler = None
    _std_out_handler = None
    _level = logging.DEBUG
    _instances = {}

    def __init__(self, level=logging.DEBUG, to_file=False, to_stdout=True, filename=FILE_NAME):
        """
        Customized logger class for PyAnsys.

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

        self._global = logging.getLogger('_Global_')  # Creating default main logger.
        self._global.setLevel(level)
        self._global.propagate = True
        self.level = self._global.level # TODO: TO REMOVE

        # Writting logging methods.
        self.debug    = self._global.debug
        self.info     = self._global.info
        self.warning  = self._global.warning
        self.error    = self._global.error
        self.critical = self._global.critical
        self.log      = self._global.log

        if to_file or filename != FILE_NAME:
            # We record to file
            self.log_to_file(filename=filename, level=level)

        if to_stdout:
            self.log_to_stdout(level=level)

        self.add_handling_uncaught_expections(self._global) # Using logger to record unhandled exceptions

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        """
        Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default FILE_NAME
        level : str, optional
            Level of logging. E.x. 'DEBUG'. By default LOG_LEVEL
        """

        self = add_file_handler(self, filename=filename, level=level, write_headers=True)

    def log_to_stdout(self, level=LOG_LEVEL):
        """
        Add standard output handler to the logger.

        Parameters
        ----------
        level : str, optional
            Level of logging record. By default LOG_LEVEL
        """

        self = add_stdout_handler(self, level=level)

    ## Copy functions
    add_stdout_handler = log_to_stdout
    add_file_handler = log_to_file

    def _make_child_logger(self, sufix, level):
        """Make a child logger, either using ``getChild`` or copying attributes between ``_global_``
        logger and the new one. """
        logger = logging.getLogger(sufix)
        logger._std_out_handler = None
        logger._file_handler = None

        if self._global.handlers:
            for each_handler in self._global.handlers:
                if each_handler == self._file_handler:
                    logger._file_handler = each_handler
                elif each_handler == self._std_out_handler:
                    logger._std_out_handler = each_handler
                logger.addHandler(each_handler)

        if level: # Child logger cannot have different logging level than the parents.
            logger.setLevel(level)
        else:
            logger.setLevel(self._global.level)
        logger.propagate = True
        return logger

    def add_child_logger(self, sufix, level=None):
        """
        Add a child logger to the main logger. This logger is more general than
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
        name = self._global.name + '.' + sufix
        self._instances[name] = self._make_child_logger(self, name, level)
        return self._instances[name]

    def _add_MAPDL_instance_logger(self, name, MAPDL_instance, level):
        if isinstance(name, str):
            instance_logger = PyansysCustomAdapter(self._make_child_logger(name, level), MAPDL_instance)
        elif isinstance(name, None):
            instance_logger = PyansysCustomAdapter(self._make_child_logger("NO_NAMED_YET", level), MAPDL_instance)
        else:
            raise Exception("You can only input 'str' classes to this method.")

        return instance_logger
        # return.level = None # TODO: To remove

    def add_instance_logger(self, name, MAPDL_instance, level=None):
        """
        Create a logger for a MAPDL instance.
        The MAPDL instance logger is a logger with an adapter which add the contextual
        information such as MAPDL instance name. This logger is returned and you can use
        it to log events as a normal logger. It is also stored in the ``_instances`` field.

        Parameters
        ----------
        name : str
            Name for the new logger
        MAPDL_instance : ansys.mapdl.core.mapdl._MapdlCore
            Mapdl instance object. This should contain the attribute ``name``.

        Returns
        -------
        ansys.mapdl.core.logging.PyansysCustomAdapter
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

        self._instances[new_name] = self._add_MAPDL_instance_logger(new_name, MAPDL_instance, level)
        return self._instances[new_name]

    def __getitem__(self, key):
        if key in self._instances.keys():
            return self._instances[key]
        else:
            raise KeyError(f"There is no instances with name {key}")

    def add_handling_uncaught_expections(self, logger):
        """This just redirect the ouput of an exception to the logger."""
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.excepthook = handle_exception


## Auxiliary functions

def add_file_handler(logger, filename=FILE_NAME, level=LOG_LEVEL, write_headers=False):
    """
    Add a file handler to the input.

    Parameters
    ----------
    logger : logging.Logger or logging.PyansysLogger
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
        Return the logger or PyansysLogger object.
    """

    _file_handler = logging.FileHandler(filename)
    _file_handler.setLevel(level)
    _file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))

    if isinstance(logger, PyansysLogger):
        logger._file_handler = _file_handler
        logger._global.addHandler(_file_handler)

    elif isinstance(logger, logging.Logger):
        logger.addHandler(_file_handler)

    if write_headers:
        _file_handler.stream.write(NEW_SESSION_HEADER)
        _file_handler.stream.write(DEFAULT_FILE_HEADER)

    return logger


def add_stdout_handler(logger, level=LOG_LEVEL, write_headers=True):
    """
    Add a file handler to the input.

    Parameters
    ----------
    logger : logging.Logger or logging.PyansysLogger
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
        Return the logger or PyansysLogger object.
    """

    _std_out_handler = logging.StreamHandler()
    _std_out_handler.setLevel(level)
    _std_out_handler.setFormatter(PyAnsysFormatter(STDOUT_MSG_FORMAT))

    if isinstance(logger, PyansysLogger):
        logger._std_out_handler = _std_out_handler
        logger._global.addHandler(_std_out_handler)

    elif isinstance(logger, logging.Logger):
        logger.addHandler(_std_out_handler)

    if write_headers:
        _std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    return logger
