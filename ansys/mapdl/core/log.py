import logging
from datetime import datetime
import sys

## General configuration
LOG_LEVEL = logging.DEBUG
FILE_NAME = 'pyansys.log'

STDOUT_MSG_FORMAT = '| %(levelname)-8s | %(instance_name)-15s |  %(module)-15s | %(funcName)-25s | %(message)s'
FILE_MSG_FORMAT = STDOUT_MSG_FORMAT

DEFAULT_STDOUT_HEADER = """
| Level    | Instance        | Module           | Function                  | Message
|----------|-----------------|------------------|---------------------------|---------------------------
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER

NEW_SESSION_HEADER = f"""\n=====================================================================================================================================
========================                      NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}                             ========================
====================================================================================================================================="""


class CustomAdapter(logging.LoggerAdapter):
    """
    This is key to keep the reference to the MAPDL instance name dynamic.
    """

    def __init__(self, logger, extra=None):
        self.logger = logger
        self.extra = extra

    def process(self, msg, kwargs):
        kwargs['extra'] = {}
        # This are the extra parameters sent to log
        kwargs['extra']['instance_name'] = self.extra['name']
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
        # change the record.__dict__
        return STDOUT_MSG_FORMAT % values


class PyAnsysFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
        super().__init__(fmt = fmt, datefmt = datefmt, style = style, validate = validate) # TODO: to fix `, **defaults)`
        self._style = PyAnsysPercentStyle(fmt)# , defaults) #overwritting


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
    level = None # TODO: TO REMOVE

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
            # self._std_out_handler.setFormatter(logging.Formatter(STDOUT_MSG_FORMAT))
            self._std_out_handler.setFormatter(PyAnsysFormatter(STDOUT_MSG_FORMAT))
            self._global.addHandler(self._std_out_handler)

            self._std_out_handler.stream.write(DEFAULT_STDOUT_HEADER)

        self.add_handling_uncaught_expections(self._global) # Using logger to record unhandled exceptions

    def _add_instance(self, obj):
        if isinstance(obj, str):
            self._instances[obj] = self._global.getChild(obj)
        else:
            raise Exception("You can only input 'str' classes to this method.")
        return self._instances[obj]

    def _add_MAPD_instance_logger(self, name, MAPDL_instance):
        if isinstance(name, str):
            self._instances[name] = CustomAdapter(self._global.getChild(name), MAPDL_instance)
        elif isinstance(name, None):
            self._instances[name] = CustomAdapter(self._global.getChild("NO_NAME_YET"), MAPDL_instance)
        else:
            raise Exception("You can only input 'str' classes to this method.")
        self._instances[name].level = None
        return self._instances[name]

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
