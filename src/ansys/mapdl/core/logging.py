# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Logging module.

This module supplies a general framework for logging in PyMAPDL.  This module is
built upon `logging <https://docs.python.org/3/library/logging.html>`_ library
and it does not intend to replace it rather provide a way to interact between
``logging`` and PyMAPDL.

The loggers used in the module include the name of the instance which
is intended to be unique.  This name is printed in all the active
outputs and it is used to track the different MAPDL instances.


How to use
==========

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
   LOG.std_out_handler.setLevel("DEBUG")  # If present.


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
Every time an instance of :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` is
created, a logger is created and stored in two places:

* ``MapdlBase._log``. For backward compatibility.
* ``LOG._instances``. This field is a ``weakref.WeakValueDictionary`` where the
  key is the name of the created logger. Entries are removed automatically
  once nothing but the instance itself keeps its logger alive (see
  *Resource cleanup* below), so this registry never grows without bound over
  the life of a process.

Internally, each instance logger is a true child of ``pymapdl_global`` in the
standard ``logging`` hierarchy (its ``logging.Logger.name`` looks like
``pymapdl_global.GRPC_127_0_0_1_50056``, with dots in the instance name
sanitized to underscores so they don't fragment the hierarchy). Unlike a
regular child logger, it does **not** propagate records up to
``pymapdl_global`` (``propagate=False``); instead, it has an internal
:class:`GlobalForwardingHandler` that looks up ``pymapdl_global``'s *current*
handlers live, at emit time, and forwards each record to them exactly once.
This gives you a unified sink with no duplicate log lines, and it also means
handlers added to ``LOG`` *after* an instance logger already exists (for
example, a later call to ``LOG.log_to_file(...)``) still reach that instance
retroactively.

Unless you explicitly set a level on an instance logger, its level stays at
``NOTSET`` so it cascades from ``pymapdl_global`` via
``logging.Logger.getEffectiveLevel()``: calling ``LOG.setLevel(...)`` after
instances already exist changes their effective level too, with no extra
bookkeeping needed. You can still override a specific instance's own level
(:func:`logger.Logging.setLevel <PymapdlCustomAdapter.setLevel>`) or attach an
extra, instance-only handler (:func:`log_to_file()
<PymapdlCustomAdapter.log_to_file>`, :func:`log_to_stdout()
<PymapdlCustomAdapter.log_to_stdout>`) without affecting any other instance.

You can use this logger like this:

.. code:: pycon
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> mapdl._log.info("This is a useful message")

    INFO - GRPC_127.0.0.1:50056 -  <ipython-input-19-f09bb2d8785c> - <module> - This is a useful message


Child (subsystem) logger
~~~~~~~~~~~~~~~~~~~~~~~~
Not every logger needs to represent a single MAPDL instance. Internal
subsystems that span (or outlive) individual instances, for example a
:class:`MapdlPool <ansys.mapdl.core.pool.MapdlPool>` or the launcher/
connection layer, can use :func:`LOG.add_child_logger()
<Logger.add_child_logger>` to get their own named logger without the
per-instance :class:`PymapdlCustomAdapter` context.

.. code:: pycon

    >>> from ansys.mapdl.core import LOG
    >>> pool_logger = LOG.add_child_logger("pool")
    >>> pool_logger.info("Pool started with 4 workers.")

    INFO -  -  <ipython-input-1-...> - <module> - Pool started with 4 workers.

Like an instance logger, a child logger is a true child of
``pymapdl_global`` in the standard ``logging`` hierarchy and forwards
records to ``pymapdl_global``'s handlers at emit time via a
:class:`GlobalForwardingHandler`, so it shares the same file/stdout sinks
and, unless a ``level`` is passed explicitly, cascades ``LOG.setLevel(...)``
changes the same way an instance logger does. Requesting the same
``logger_name`` again returns the already-registered logger instead of
creating a duplicate.

Resource cleanup
~~~~~~~~~~~~~~~~
Calling :func:`mapdl.exit() <ansys.mapdl.core.mapdl.MapdlBase.exit>` eagerly
closes any handler this instance owns exclusively (for example, its own file
handler) and immediately deregisters its logger from both ``LOG._instances``
and Python's own, otherwise-permanent ``logging.Logger.manager.loggerDict``.

If an instance is never explicitly exited (dropped by a fixture, an exception
during setup, and so on), a :func:`weakref.finalize` callback attached to its
logger performs the same cleanup once the instance (and its logger adapter)
are actually garbage collected, so long-running processes that create many
short-lived instances do not leak loggers, handlers, or file descriptors.
:func:`add_child_logger() <Logger.add_child_logger>`'s cleanup, used for
subsystem-level loggers rather than per-``Mapdl``-instance ones, is
best-effort: because stdlib's own ``loggerDict`` holds a strong reference to
every ``logging.Logger`` it creates, a bare child logger without an owning
wrapper object may not become collectible on its own.


Other loggers
~~~~~~~~~~~~~
You can create your own loggers using python ``logging`` library as
you would do in any other script.  There shall no be conflicts between
these loggers.
"""

from datetime import datetime
import logging
import sys
import threading
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Type,
    Union,
    cast,
)
import weakref

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl import MapdlBase

# Guards mutations of ``Logger._instances`` and deletions from
# ``logging.Logger.manager.loggerDict``. Both ``Logger`` and
# ``weakref.finalize`` callbacks can run concurrently (for example, a
# ``MapdlPool`` worker thread creating an instance logger while another
# thread's instance is being garbage collected).
#
# Must be reentrant: replacing an entry in ``Logger._instances`` (a
# ``weakref.WeakValueDictionary``) can drop the last strong reference to the
# previous value stored under that key, which triggers its
# ``weakref.finalize`` callback (``_finalize_child_logger``) synchronously,
# on the same thread, before the assignment call returns. That callback also
# acquires this lock, so a plain, non-reentrant ``threading.Lock`` would
# self-deadlock in that scenario.
_registry_lock = threading.RLock()

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

LOG_LEVEL_STRING_TYPE = Literal["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"]
LOG_LEVEL_TYPE = Union[LOG_LEVEL_STRING_TYPE, int]

string_to_loglevel: Dict[LOG_LEVEL_STRING_TYPE, int] = {
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

    file_handler: Optional[logging.FileHandler] = None
    std_out_handler: Optional[logging.StreamHandler] = None
    # Key under which this adapter is stored in ``Logger._instances``. Set by
    # ``Logger.add_instance_logger`` so that eager, explicit cleanup (see
    # ``MapdlBase._cleanup_loggers``) can deregister the exact same entry
    # that the weakref-based safety net (``_finalize_child_logger``) would
    # otherwise only clean up once this adapter is garbage collected.
    name_key: Optional[str] = None
    # The ``weakref.finalize`` object registered against this adapter (see
    # ``Logger._add_mapdl_instance_logger``). Eager cleanup paths must
    # invoke *this exact* finalizer (which both runs its callback and marks
    # itself dead) rather than calling ``_finalize_child_logger`` directly:
    # doing so guarantees the callback can never fire a second time later,
    # from garbage collection, against a *different* logger that happens to
    # have reused the same dotted name in the meantime.
    _finalizer: Optional["weakref.finalize"] = None
    # Set by ``ansys.mapdl.core.misc.supress_logging`` while it temporarily
    # raises this adapter's underlying logger to ``CRITICAL`` to silence an
    # internal call's own verbose logging. Records the level that was in
    # effect just *before* that temporary override, so other code that
    # needs to know the user's actual requested debug level (for example
    # ``_MapdlCore._non_interactive.__enter__``, which decides whether to
    # emit an APDL comment based on whether debug logging is enabled) can
    # see through the suppression window instead of reading the
    # momentarily-overridden ``CRITICAL`` level. ``None`` when no
    # suppression is currently in progress.
    _suppressed_from_level: Optional[int] = None

    def __init__(self, logger: logging.Logger, extra: Optional["MapdlBase"] = None):
        self.logger = logger
        if extra is not None:
            self.extra = weakref.proxy(extra)  # type: ignore[assignment]
        else:
            self.extra = None
        self.file_handler = logger.file_handler  # type: ignore[attr-defined]
        self.std_out_handler = logger.std_out_handler  # type: ignore[attr-defined]

    def process(self, msg: str, kwargs: MutableMapping[str, Dict[str, str]]):
        kwargs["extra"] = {}
        # This are the extra parameters sent to log
        if self.extra is not None:
            kwargs["extra"]["instance_name"] = self.extra.name  # type: ignore[union-attr,attr-defined]
        return msg, kwargs

    @property
    def level(self) -> int:
        """Current logging level explicitly set on the underlying logger.

        Unlike a plain attribute snapshotted at some point in time, this
        always reflects the live value of ``self.logger.level``. In
        particular, when the instance logger itself has no explicit level
        set (that is, it is left at ``logging.NOTSET`` so it cascades from
        ``pymapdl_global`` via ``getEffectiveLevel()``), this returns
        ``logging.NOTSET`` (``0``) rather than the resolved effective level.
        This is what keeps callers like
        :func:`ansys.mapdl.core.misc.supress_logging` (which reads this
        value to later restore it through :func:`setLevel`) from
        accidentally pinning a cascading instance to a fixed numeric level:
        restoring ``logging.NOTSET`` puts it back into cascading mode
        instead. It is never ``None``, which keeps ``setLevel`` calls safe.
        """
        return self.logger.level

    def log_to_file(
        self, filename: str = FILE_NAME, level: LOG_LEVEL_TYPE = LOG_LEVEL
    ) -> None:
        """Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default FILE_NAME
        level : str or int, optional
            Level of logging. E.x. 'DEBUG'. By default LOG_LEVEL
        """

        addfile_handler(self.logger, filename=filename, level=level, write_headers=True)
        self.file_handler = self.logger.file_handler

    def log_to_stdout(self, level: LOG_LEVEL_TYPE = LOG_LEVEL) -> None:
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str or int, optional
            Level of logging record. By default LOG_LEVEL
        """
        if self.std_out_handler:
            raise Exception("Stdout logger already defined.")

        add_stdout_handler(self.logger, level=level)
        self.std_out_handler = self.logger.std_out_handler

    def setLevel(self, level: Union[int, str] = "DEBUG"):
        """Change the log level of the object and the attached handlers."""
        if isinstance(level, str):
            level = string_to_loglevel[cast(LOG_LEVEL_STRING_TYPE, level.upper())]
        self.logger.setLevel(level)
        for each_handler in self.logger.handlers:
            each_handler.setLevel(level)


class PymapdlPercentStyle(logging.PercentStyle):
    def __init__(self, fmt, *, defaults=None):
        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def _format(self, record) -> str:
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
        fmt: str = STDOUT_MSG_FORMAT,
        datefmt: Optional[str] = None,
        style: Literal["%", "{", "$"] = "%",
        validate: bool = True,
        defaults: Optional[Mapping[str, Any]] = None,
    ):
        if sys.version_info[1] < 8:
            super().__init__(fmt, datefmt, style)
        else:
            # 3.8: The validate parameter was added
            super().__init__(fmt, datefmt, style, validate)
        self._style = PymapdlPercentStyle(fmt, defaults=defaults)  # overwriting


class InstanceFilter(logging.Filter):
    """Ensures that instance_name record always exists."""

    def filter(self, record: logging.LogRecord):
        if not hasattr(record, "instance_name") and hasattr(record, "name"):
            record.instance_name = record.name
        elif not hasattr(record, "instance_name"):  # pragma: no cover
            record.instance_name = ""
        return True


def _sanitize_logger_segment(name: str) -> str:
    """Make ``name`` safe to use as a single ``logging`` hierarchy segment.

    ``Mapdl`` instance names often embed literal dots, for example
    ``GRPC_127.0.0.1:50052`` (the IP address). Since ``logging`` treats
    every ``.`` in a logger name as an additional hierarchy level,
    concatenating such a name verbatim as a child of ``pymapdl_global``
    would silently create a chain of extra ``PlaceHolder`` entries in
    ``logging.Logger.manager.loggerDict`` (one per dot) instead of a single,
    real, direct child logger. Replacing dots keeps each instance/child
    logger exactly one level below ``pymapdl_global``. This only affects the
    underlying ``logging.Logger`` name used for registry/hierarchy purposes;
    the human-readable instance name shown in log messages
    (``instance_name``) is unaffected, since it comes from the ``Mapdl``
    instance's own ``name`` property, not from the logger's name.
    """
    return name.replace(".", "_")


def _finalize_child_logger(
    full_name: str,
    name_key: str,
    registry: "weakref.WeakValueDictionary[str, Any]",
) -> None:
    """Release a child logger's own handlers and its stdlib registry entry.

    Registered via ``weakref.finalize`` against the object stored in
    ``Logger._instances`` (a ``PymapdlCustomAdapter`` for instance loggers).
    This runs once nothing else references that object anymore — typically
    once the owning ``Mapdl`` instance itself is garbage collected — and is
    the safety net for instances that are never explicitly cleaned up via
    ``Mapdl.exit()`` / ``_cleanup_loggers``.

    Deliberately takes no reference to ``self`` (the ``Logger``/``LOG``
    singleton): only plain data (names) and the registry mapping itself are
    captured, so this callback cannot resurrect or keep alive anything
    beyond the process-wide ``logging`` state it is meant to clean up.

    Only handlers this instance is known to own exclusively (its own
    ``file_handler``/``std_out_handler``, tracked on the ``logging.Logger``
    object by :func:`addfile_handler`/:func:`add_stdout_handler`) are
    ``close()``-d. Any other handler found on the child (for example one a
    caller attached manually, possibly shared with another logger) is only
    detached via ``removeHandler``, never closed, so a shared stream is not
    pulled out from under whoever else still uses it.
    """
    with _registry_lock:
        manager = logging.Logger.manager
        child = manager.loggerDict.get(full_name)
        if isinstance(child, logging.Logger):
            owned_handlers = {
                handler
                for handler in (
                    getattr(child, "file_handler", None),
                    getattr(child, "std_out_handler", None),
                )
                if handler is not None
            }
            for handler in list(child.handlers):
                if handler in owned_handlers:
                    try:
                        handler.close()
                    except (OSError, ValueError):  # pragma: no cover
                        # Stream already closed/detached concurrently; safe to ignore.
                        pass
                child.removeHandler(handler)
            manager.loggerDict.pop(full_name, None)
        registry.pop(name_key, None)


class GlobalForwardingHandler(logging.Handler):
    """Forwards records to whichever handlers ``pymapdl_global`` currently owns.

    Every instance/child logger is a real ``logging`` child of
    ``pymapdl_global`` (for example ``pymapdl_global.GRPC_127_0_0_1:50052`` —
    see :func:`_sanitize_logger_segment` for why dots in the instance name
    are replaced), but with ``propagate`` disabled: instead of letting
    ``logging`` bubble records up (which would also require each child to
    carry copies of the global handlers, and thus would emit every record
    twice — once through its own copy, once through propagation), a single
    instance of this handler is attached directly to the child logger. It
    looks up ``pymapdl_global``'s handlers *live*, at emit time, rather than
    once at creation time. This means:

    * A record is only ever emitted once per target handler.
    * Handlers added to ``pymapdl_global`` after a child logger already
      exists (for example, calling :meth:`Logger.log_to_file` later) still
      reach every existing instance/child logger.
    * Closing or removing a specific instance's own handlers never touches
      ``pymapdl_global``'s handlers, because none are shared/copied.

    A record only reaches :meth:`emit` once it has already passed the
    originating child logger's own effective-level gate (whether that is an
    explicit per-instance override or one cascaded from ``pymapdl_global``).
    Records are therefore forwarded to every reachable handler
    unconditionally, deliberately *not* re-checking each handler's own
    configured ``level``: doing so would silently drop records from
    instances explicitly configured to be more verbose than
    ``pymapdl_global``'s own handlers (for example
    ``launch_mapdl(loglevel="DEBUG")`` while the global stdout handler stays
    at its default ``ERROR``), defeating that per-instance override.

    Handlers are gathered by walking ``pymapdl_global`` and then its
    ``parent`` chain for as long as each logger's own ``propagate`` is
    ``True`` (mirroring ``logging.Logger.callHandlers``), so ancestor
    handlers -- including the root logger's, such as ``pytest``'s
    ``caplog`` handler -- also receive the record, not just
    ``pymapdl_global``'s own direct handlers.
    """

    def __init__(self, global_logger: logging.Logger):
        super().__init__()
        self._global_logger_ref = weakref.ref(global_logger)
        # Gives ``fake_record()``-style tests (which format using the first
        # handler on an instance logger) a usable, PyMAPDL-formatted output,
        # since this handler is always the first one attached to a freshly
        # created instance/child logger.
        self.setFormatter(PymapdlFormatter())

    def emit(self, record: logging.LogRecord) -> None:
        global_logger = self._global_logger_ref()
        if global_logger is None:  # pragma: no cover
            return
        logger: Optional[logging.Logger] = global_logger
        while logger is not None:
            for handler in logger.handlers:
                if handler is self:  # pragma: no cover
                    continue
                try:
                    handler.handle(record)
                except Exception:  # pragma: no cover
                    self.handleError(record)
            if not logger.propagate:
                break
            logger = logger.parent


class Logger:
    """Logger used for each PyMAPDL session.

    This class allows you to add handlers to the logger to output to a file or
    standard output.

    Parameters
    ----------
    level : int, optional
        Logging level to filter the message severity allowed in the logger.
        The default is ``logging.DEBUG``.
    to_file : bool, optional
        Write log messages to a file. The default is ``False``.
    to_stdout : bool, optional
        Write log messages into the standard output. The default is
        ``True``.
    filename : str, optional
        Name of the file where log messages are written to.
        The default is ``FILE_NAME``.

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

    file_handler: Optional[logging.FileHandler] = None
    std_out_handler: Optional[logging.StreamHandler] = None
    _level = logging.DEBUG
    # A ``WeakValueDictionary`` so that instance/child loggers (or the
    # ``PymapdlCustomAdapter`` wrapping them) are automatically dropped from
    # this registry once nothing else references them (typically once the
    # owning ``Mapdl`` instance itself is garbage collected). This is the
    # safety net for instances that are never explicitly ``exit()``-ed; see
    # ``_register_finalizer`` for the accompanying cleanup of the
    # process-wide ``logging.Logger.manager.loggerDict`` entry and any
    # handlers still open on the child logger.
    _instances: "weakref.WeakValueDictionary[str, Any]" = weakref.WeakValueDictionary()

    def __init__(
        self,
        level: LOG_LEVEL_TYPE = logging.DEBUG,
        to_file: bool = False,
        to_stdout: bool = True,
        filename: str = FILE_NAME,
        catch_all_exceptions: bool = False,
    ):
        """Customized logger class for PyMAPDL.

        Parameters
        ----------
        level : str or int, optional
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
        self.logger: logging.Logger = logging.getLogger("pymapdl_global")
        self.logger.addFilter(InstanceFilter())
        if isinstance(level, str):
            level = cast(LOG_LEVEL_STRING_TYPE, level.upper())

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

        if to_file:
            # We record to file
            self.log_to_file(filename=filename, level=level)

        if to_stdout:
            self.log_to_stdout(level=level)

        # Using logger to record unhandled exceptions
        if catch_all_exceptions:
            self.add_handling_uncaught_expections(self.logger)

    def log_to_file(
        self, filename: str = FILE_NAME, level: LOG_LEVEL_TYPE = LOG_LEVEL
    ) -> None:
        """Add file handler to logger.

        Parameters
        ----------
        filename : str, optional
            Name of the file where the logs are recorded. By default
            ``'pymapdl.log'``.
        level : str or int, optional
            Level of logging. By default ``'DEBUG'``.

        Examples
        --------
        Write to ``pymapdl.log`` in the current working directory.

        >>> from ansys.mapdl.core import LOG
        >>> import os
        >>> file_path = os.path.join(os.getcwd(), 'pymapdl.log')
        >>> LOG.log_to_file(file_path)
        """

        addfile_handler(self, filename=filename, level=level, write_headers=True)

    def log_to_stdout(self, level: LOG_LEVEL_TYPE = LOG_LEVEL):
        """Add standard output handler to the logger.

        Parameters
        ----------
        level : str or int, optional
            Level of logging record. By default  ``'DEBUG'``.
        """

        add_stdout_handler(self, level=level)

    def setLevel(self, level: LOG_LEVEL_TYPE = "DEBUG"):
        """Change the log level of the object and the attached handlers."""
        if isinstance(level, str):
            level = string_to_loglevel[cast(LOG_LEVEL_STRING_TYPE, level.upper())]
        self.logger.setLevel(level)
        for each_handler in self.logger.handlers:
            each_handler.setLevel(level)
        self._level = level

    def _make_child_logger(
        self, logger_name: str, level: Optional[LOG_LEVEL_TYPE]
    ) -> logging.Logger:
        """Create (or fetch) a real ``logging`` child of ``pymapdl_global``.

        Unlike the previous implementation, the child does **not** carry
        copies of ``pymapdl_global``'s handlers. Instead, a single
        :class:`GlobalForwardingHandler` is attached, which looks up
        ``pymapdl_global``'s handlers live, at emit time (see that class's
        docstring for why this avoids the double-emission bug that copying
        handlers together with a real, ``propagate=True`` hierarchy used to
        cause). ``propagate`` is disabled here so ``logging`` itself never
        delivers a record to ``pymapdl_global``'s handlers a second time.
        """
        full_name = f"{self.logger.name}.{_sanitize_logger_segment(logger_name)}"
        logger = logging.getLogger(full_name)
        logger.std_out_handler = None  # type: ignore[attr-defined]
        logger.file_handler = None  # type: ignore[attr-defined]
        logger.propagate = False

        if not any(isinstance(h, GlobalForwardingHandler) for h in logger.handlers):
            logger.addHandler(GlobalForwardingHandler(self.logger))

        if level:
            if isinstance(level, str):
                level = string_to_loglevel[cast(LOG_LEVEL_STRING_TYPE, level.upper())]
            logger.setLevel(level)
        else:
            # Leave at NOTSET: ``getEffectiveLevel()`` then cascades from
            # ``pymapdl_global`` through the real hierarchy, so changing
            # ``LOG.setLevel()`` later transparently affects this logger,
            # as long as no explicit level was requested for it.
            logger.setLevel(logging.NOTSET)

        return logger

    def add_child_logger(
        self, logger_name: str, level: Optional[LOG_LEVEL_TYPE] = None
    ):
        """Add a child logger to the main logger.

        Use this for subsystem-level loggers (for example a connection pool
        or the launcher) that are not tied to a single MAPDL instance. This
        logger is more general than an instance logger, which is designed to
        track the state of the MAPDL instances and is created with
        :func:`add_instance_logger`.

        The returned logger is a true child of ``pymapdl_global`` in the
        standard ``logging`` hierarchy: it forwards records to
        ``pymapdl_global``'s handlers at emit time, so it shares the same
        sinks (file, standard output). Unless ``level`` is given explicitly,
        the child logger's level stays at ``NOTSET`` so it cascades from
        ``pymapdl_global``, meaning a later ``LOG.setLevel(...)`` call also
        changes its effective level. Requesting the same ``logger_name``
        again returns the already-registered logger instead of creating a
        duplicate.

        Parameters
        ----------
        logger_name : str
            Name of the logger.
        level : str or int, optional
            Level of logging. If not given, the level cascades from the
            main logger.

        Returns
        -------
        logging.logger
            Logger class.

        Examples
        --------
        >>> from ansys.mapdl.core import LOG
        >>> pool_logger = LOG.add_child_logger("pool")
        >>> pool_logger.info("Pool started with 4 workers.")
        """
        with _registry_lock:
            name = self.logger.name + "." + logger_name
            existing = self._instances.get(name)
            if existing is not None:
                # Re-requesting the same ``logger_name`` returns the same,
                # already-registered logger instead of creating a second,
                # redundant registry entry/finalizer for it.
                return existing

            # ``logger_name`` values that differ before sanitization (see
            # :func:`_sanitize_logger_segment`) can still collide once dots
            # are replaced, for example ``"a.b"`` and ``"a_b"``. Resolve
            # such collisions the same way ``add_instance_logger`` does, so
            # the second caller gets its own, distinct logger rather than
            # silently aliasing the first one's.
            count_ = 0
            new_logger_name = logger_name
            full_name = (
                f"{self.logger.name}.{_sanitize_logger_segment(new_logger_name)}"
            )
            while full_name in logging.Logger.manager.loggerDict:
                count_ += 1
                new_logger_name = f"{logger_name}_{count_}"
                full_name = (
                    f"{self.logger.name}.{_sanitize_logger_segment(new_logger_name)}"
                )

            child_logger = self._make_child_logger(new_logger_name, level)
            self._instances[name] = child_logger

        weakref.finalize(
            child_logger,
            _finalize_child_logger,
            child_logger.name,
            name,
            self._instances,
        )
        return child_logger

    def _add_mapdl_instance_logger(
        self,
        name: Optional[str],
        mapdl_instance: "MapdlBase",
        level: Optional[LOG_LEVEL_TYPE],
    ) -> logging.Logger:
        if isinstance(name, str):
            logger_name = name
        elif not name:  # pragma: no cover
            logger_name = "NO_NAMED_YET"
        else:
            raise ValueError("You can only input 'str' classes to this method.")

        child_logger = self._make_child_logger(logger_name, level)
        instance_logger = PymapdlCustomAdapter(child_logger, mapdl_instance)

        # Safety net: if this instance logger is never explicitly cleaned up
        # (via ``Mapdl.exit()`` / ``_cleanup_loggers``), release its handlers
        # and deregister it from ``logging.Logger.manager.loggerDict`` once
        # nothing but ``_instances`` and the owning ``Mapdl`` instance
        # reference it, i.e. once it is garbage collected.
        #
        # The finalizer object itself is stashed on the adapter so eager
        # cleanup (``MapdlBase._cleanup_loggers``) can call it directly. A
        # ``weakref.finalize`` object can only ever run its callback once:
        # invoking it here (instead of calling ``_finalize_child_logger``
        # separately) atomically performs the cleanup *and* permanently
        # disarms the later, GC-triggered call, so it cannot fire again
        # against a different, unrelated logger that later reuses the same
        # dotted name.
        instance_logger._finalizer = weakref.finalize(
            instance_logger,
            _finalize_child_logger,
            child_logger.name,
            name if isinstance(name, str) else logger_name,
            self._instances,
        )
        return instance_logger

    def add_instance_logger(
        self,
        name: str,
        mapdl_instance: "MapdlBase",
        level: Optional[LOG_LEVEL_TYPE] = None,
    ) -> logging.Logger:
        """Create a logger for a MAPDL instance.

        The MAPDL instance logger is a logger with an adapter which add the
        contextual information such as MAPDL instance name. This logger is
        returned and you can use it to log events as a normal logger. It is also
        stored in the ``_instances`` field.

        Parameters
        ----------
        name : str
            Name for the new logger
        mapdl_instance : ansys.mapdl.core.mapdl.MapdlBase
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
        with _registry_lock:
            count_ = 0
            new_name = name
            full_name = f"{self.logger.name}.{_sanitize_logger_segment(new_name)}"
            while full_name in logging.Logger.manager.loggerDict:
                count_ += 1
                new_name = name + "_" + str(count_)
                full_name = f"{self.logger.name}.{_sanitize_logger_segment(new_name)}"

            instance_logger = self._add_mapdl_instance_logger(
                new_name, mapdl_instance, level
            )
            # Tracked so that ``MapdlBase._cleanup_loggers`` can eagerly
            # deregister this exact entry (rather than waiting for GC) once
            # the instance is explicitly ``exit()``-ed.
            instance_logger.name_key = new_name  # type: ignore[attr-defined]
            self._instances[new_name] = instance_logger
        return self._instances[new_name]

    def __getitem__(self, key: str):
        if key in self._instances.keys():
            return self._instances[key]
        else:
            raise KeyError(f"There is no instances with name {key}")

    def add_handling_uncaught_expections(self, logger: logging.Logger):
        """This just redirect the output of an exception to the logger."""

        def handle_exception(
            exc_type: Type[BaseException],
            exc_value: BaseException,
            exc_traceback: Optional[TracebackType],
        ):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.critical(
                "Uncaught exception",
                exc_info=(exc_type, exc_value, exc_traceback),
            )

        sys.excepthook = handle_exception


def addfile_handler(
    logger: Union[Logger, logging.Logger],
    filename: str = FILE_NAME,
    level: LOG_LEVEL_TYPE = LOG_LEVEL,
    write_headers: bool = False,
):
    """Add a file handler to the input.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger where to add the file handler.
    filename : str, optional
        Name of the output file. By default FILE_NAME
    level : str or int, optional
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
        logger.file_handler = file_handler  # type: ignore[attr-defined]
        logger.addHandler(file_handler)

    if write_headers and file_handler.stream is not None:
        file_handler.stream.write(NEW_SESSION_HEADER)
        file_handler.stream.write(DEFAULT_FILE_HEADER)

    return logger


def add_stdout_handler(
    logger: Union[Logger, logging.Logger],
    level: LOG_LEVEL_TYPE = LOG_LEVEL,
    write_headers: bool = False,
):
    """Add a file handler to the logger.

    Parameters
    ----------
    logger : logging.Logger or logging.Logger
        Logger where to add the file handler.
    level : str or int, optional
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
