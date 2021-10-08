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

    def __init__(self, logger, extra=None):
        self.logger = logger
        self.extra = extra

    def process(self, msg, kwargs):
        kwargs['extra'] = {}
        # This are the extra parameters sent to log
        kwargs['extra']['instance_name'] = self.extra['name'] # here self.extra is the argument pass to the ``PyAnsys
        return msg, kwargs


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
        return STDOUT_MSG_FORMAT % values


class PyAnsysFormatter(logging.Formatter):
    """Customized ``Formatter`` class used to overwrite the defaults format styles."""

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
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
    level = None # TODO: TO REMOVE

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
        self._global.level = level

        # Writting logging methods.
        self.debug    = self._global.debug
        self.info     = self._global.info
        self.warning  = self._global.warning
        self.error    = self._global.error
        self.critical = self._global.critical

        if to_file or filename != FILE_NAME:
            # We record to file
            self.log_to_file(filename=filename, level=level)

        if to_stdout:
            self.log_to_stdout(level=level)

        self.add_handling_uncaught_expections(self._global) # Using logger to record unhandled exceptions

    def log_to_file(self, filename=FILE_NAME, level=LOG_LEVEL):
        self._file_handler = logging.FileHandler(filename)
        self._file_handler.setLevel(level)
        self._file_handler.setFormatter(logging.Formatter(FILE_MSG_FORMAT))
        self._global.addHandler(self._file_handler)

        # Writting headers
        self._file_handler.stream.write(NEW_SESSION_HEADER)
        self._file_handler.stream.write(DEFAULT_FILE_HEADER)

    def log_to_stdout(self, level=LOG_LEVEL):
        self._std_out_handler = logging.StreamHandler()
        self._std_out_handler.setLevel(level)
        self._std_out_handler.setFormatter(PyAnsysFormatter(STDOUT_MSG_FORMAT))
        self._global.addHandler(self._std_out_handler)

        # Writting the header
        self._std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

    def _add_instance(self, obj):
        self.is_adapter = False  # Probably I could use isinstance to check this is an adaptor class. But just in case.

        if isinstance(obj, str):
            self._instances[obj] = self._global.getChild(obj)
        else:
            raise Exception("You can only input 'str' classes to this method.")
        return self._instances[obj]

    def _add_MAPD_instance_logger(self, name, MAPDL_instance):
        self.is_adapter = True

        if isinstance(name, str):
            self._instances[name] = PyansysCustomAdapter(self._global.getChild(name), MAPDL_instance)
        elif isinstance(name, None):
            self._instances[name] = PyansysCustomAdapter(self._global.getChild("NO_NAME_YET"), MAPDL_instance)
        else:
            raise Exception("You can only input 'str' classes to this method.")
        self._instances[name].level = None
        return self._instances[name]

    def add_child_logger(self, name):
        """
        Add a child logger to the main logger. This logger is more general than
        an instance logger which is designed to track the state of the MAPDL instances.

        Parameters
        ----------
        name : str
            Name of the logger.

        Returns
        -------
        logging.logger
            Logger class.
        """
        return self.add_child_logger()

    def add_instance_logger(self, name, MAPDL_instance):
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
        return self._add_MAPD_instance_logger(name, MAPDL_instance)

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
            logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        sys.excepthook = handle_exception
