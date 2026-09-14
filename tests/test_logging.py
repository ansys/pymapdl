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

""" "Testing of log module"""

import gc
import io
import logging as deflogging  # Default logging
import os
import re
from unittest.mock import Mock

import pytest

from ansys.mapdl.core import LOG  # Global logger
from ansys.mapdl.core import logging
from conftest import requires

## Notes
# Use the next fixtures for:
# - capfd: for testing console printing.
# - caplog: for testing logging printing.

LOG_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
}


def fake_record(
    logger,
    msg="This is a message",
    instance_name="172.1.1.1:52000",
    handler_index=0,
    name_logger=None,
    level=deflogging.DEBUG,
    filename="fn",
    lno=0,
    args=(),
    exc_info=None,
    extra={},
):
    """
    Function to fake log records using the format from the logger handler.

    Parameters
    ----------
    logger : logging.Logger
        A logger object with at least a handler.
    msg : str, optional
        Message to include in the log record. By default 'This is a message'
    instance_name : str, optional
        Name of the instance. By default '172.1.1.1:52000'
    handler_index : int, optional
        Index of the selected handler in case you want to test a handler different than
        the first one. By default 0
    level : int, optional
        Logging level, by default deflogging.DEBUG
    filename : str, optional
        Name of the file name. [FAKE]. By default 'fn'
    lno : int, optional
        Line where the fake log is recorded [FAKE]. By default 0
    args : tuple, optional
        Other arguments. By default ()
    exc_info : [type], optional
        Exception information. By default None
    extra : dict, optional
        Extra arguments, one of them should be 'instance_name'. By default {}

    Returns
    -------
    [type]
        [description]
    """
    sinfo = None
    if not name_logger:
        name_logger = logger.name

    if "instance_name" not in extra.keys():
        extra["instance_name"] = instance_name

    record = logger.makeRecord(
        name_logger,
        level,
        filename,
        lno,
        msg,
        args=args,
        exc_info=exc_info,
        extra=extra,
        sinfo=sinfo,
    )
    handler = logger.handlers[handler_index]
    return handler.format(record)


def test_stdout_reading(capfd):
    print("This is a test")

    out, err = capfd.readouterr()
    assert out == "This is a test\n"


def test_only_logger(caplog):
    log_a = deflogging.getLogger("test")
    log_a.setLevel("DEBUG")

    log_a.debug("This is another test")
    assert "This is another test" in caplog.text


def test_global_logger_exist():
    assert isinstance(LOG.logger, deflogging.Logger)
    assert LOG.logger.name == "pymapdl_global"


def test_global_logger_has_handlers():
    assert hasattr(LOG, "file_handler")
    assert hasattr(LOG, "std_out_handler")
    assert LOG.logger.hasHandlers
    assert LOG.file_handler or LOG.std_out_handler  # at least a handler is not empty


def test_global_logger_logging(caplog):
    LOG.logger.setLevel("DEBUG")
    LOG.std_out_handler.setLevel("DEBUG")
    for each_log_name, each_log_number in LOG_LEVELS.items():
        msg = f"This is an {each_log_name} message."
        LOG.logger.log(each_log_number, msg)
        # Make sure we are using the right logger, the right level and message.
        assert caplog.record_tuples[-1] == (
            "pymapdl_global",
            each_log_number,
            msg,
        )


def test_global_logger_debug_mode():
    assert isinstance(LOG.logger.level, int)


def test_global_logger_exception_handling(caplog):
    exc = "Unexpected exception"
    with pytest.raises(Exception):
        raise Exception(exc)
        assert exc in caplog.text


def test_global_logger_debug_levels(caplog):
    """Testing for all the possible logging level that the output is recorded properly for each type of msg."""
    for each_level in [
        deflogging.DEBUG,
        deflogging.INFO,
        deflogging.WARN,
        deflogging.ERROR,
        deflogging.CRITICAL,
    ]:
        with caplog.at_level(
            each_level, LOG.logger.name
        ):  # changing root logger level:
            for each_log_name, each_log_number in LOG_LEVELS.items():
                msg = f"This is an {each_log_name} message."
                LOG.logger.log(each_log_number, msg)
                # Make sure we are using the right logger, the right level and message.
                if each_log_number >= each_level:
                    assert caplog.record_tuples[-1] == (
                        "pymapdl_global",
                        each_log_number,
                        msg,
                    )
                else:
                    assert caplog.record_tuples[-1] != (
                        "pymapdl_global",
                        each_log_number,
                        msg,
                    )


@requires("grpc")
def test_global_logger_format():
    # Since we cannot read the format of our logger, because pytest just dont show the console output or
    # if it does, it formats the logger with its own formatter, we are going to check the logger handlers
    # and output by faking a record.
    # This method is not super robust, since we are input fake data to ``logging.makeRecord``.
    # There are things such as filename or class that we cannot evaluate without going
    # into the code.

    assert "instance" in logging.FILE_MSG_FORMAT
    assert "instance" in logging.STDOUT_MSG_FORMAT

    log = fake_record(
        LOG.logger,
        msg="This is a message",
        level=deflogging.DEBUG,
        extra={"instance_name": "172.1.1.1"},
    )
    assert re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", log)
    assert "DEBUG" in log
    assert "This is a message" in log


@requires("grpc")
def test_instance_logger_format(mapdl, cleared, tmpdir):
    # Since we cannot read the format of our logger, because pytest just dont show the console output or
    # if it does, it formats the logger with its own formatter, we are going to check the logger handlers
    # and output by faking a record.
    # This method is not super robust, since we are input fake data to ``logging.makeRecord``.
    # There are things such as filename or class that we cannot evaluate without going
    # into the code.

    msg = "This is a message"
    logfile = os.path.join(tmpdir, "mylogfile.log")

    # Adding a log handler
    mapdl.logger.log_to_file(logfile, logging.DEBUG)

    # Faking a record
    log = fake_record(
        mapdl._log.logger,
        msg=msg,
        level=logging.DEBUG,
        extra={"instance_name": "172.1.1.1"},
    )
    assert re.findall(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}", log)
    assert "DEBUG" in log
    assert msg in log


def test_global_methods(caplog):
    LOG.logger.setLevel("DEBUG")
    LOG.std_out_handler.setLevel("DEBUG")

    msg = f"This is a debug message"
    LOG.debug(msg)
    assert msg in caplog.text

    msg = f"This is an info message"
    LOG.info(msg)
    assert msg in caplog.text

    msg = f"This is a warning message"
    LOG.warning(msg)
    assert msg in caplog.text

    msg = f"This is an error message"
    LOG.error(msg)
    assert msg in caplog.text

    msg = f"This is a critical message"
    LOG.critical(msg)
    assert msg in caplog.text

    msg = f'This is a 30 message using "log"'
    LOG.log(30, msg)
    assert msg in caplog.text


def test_log_to_file(tmpdir):
    """Testing writing to log file.

    Since the default loglevel of LOG is error, debug are not normally recorded to it.
    """
    file_path = os.path.join(tmpdir, "instance.log")
    file_msg_error = "This is a error message"
    file_msg_debug = "This is a debug message"

    # The LOG loglevel is changed in previous test,
    # hence making sure now it is the "default" one.
    LOG.logger.setLevel("ERROR")
    LOG.std_out_handler.setLevel("ERROR")

    if LOG.file_handler is None:
        old_logger = None
        LOG.log_to_file(file_path)
    else:
        # the logger has been already instantiated
        old_logger = LOG.file_handler.baseFilename
        LOG.log_to_file(file_path)

    LOG.error(file_msg_error)
    LOG.debug(file_msg_debug)

    with open(file_path, "r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_error in text
    assert file_msg_debug not in text
    assert "ERROR" in text
    assert "DEBUG" not in text

    LOG.logger.setLevel("DEBUG")
    for each_handler in LOG.logger.handlers:
        each_handler.setLevel("DEBUG")

    file_msg_debug = "This debug message should be recorded."
    LOG.debug(file_msg_debug)

    with open(file_path, "r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_debug in text

    if old_logger is not None:
        LOG.log_to_file(old_logger)


def test_log_instance_name(mapdl, cleared):
    # verify we can access via an instance name
    LOG[mapdl.name] == mapdl._log


def test_instance_log_to_file(mapdl, cleared, tmpdir):
    """Testing writing to log file.

    Since the default loglevel of LOG is error, debug are not normally recorded to it.
    """
    file_path = os.path.join(tmpdir, "instance.log")
    file_msg_error = "This is a error message"
    file_msg_debug = "This is a debug message"

    mapdl._log.log_to_file(file_path)
    mapdl._log.logger.setLevel("ERROR")
    for each_handler in mapdl._log.logger.handlers:
        each_handler.setLevel("ERROR")

    mapdl._log.error(file_msg_error)
    mapdl._log.debug(file_msg_debug)

    assert os.path.exists(file_path)

    with open(file_path, "r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_error in text
    assert file_msg_debug not in text
    assert "ERROR" in text
    assert "DEBUG" not in text

    mapdl._log.logger.setLevel("DEBUG")
    for each_handler in mapdl._log.logger.handlers:
        each_handler.setLevel("DEBUG")

    file_msg_debug = "This debug message should be recorded."
    mapdl._log.debug(file_msg_debug)

    with open(file_path, "r") as fid:
        text = "".join(fid.readlines())

    assert file_msg_debug in text


def test_lowercases():
    # test that all loggers are lowercase
    for each_loglevel in LOG_LEVELS.keys():
        LOG.setLevel(each_loglevel.lower())

        for each_logger in LOG._instances.values():
            each_logger.setLevel(each_loglevel.lower())


## Regression tests for the logging-module refactor (resource-leak fixes).
#
# These use lightweight ``unittest.mock.Mock`` stand-ins for ``Mapdl``
# instances (only a ``.name`` attribute is required by
# ``Logger.add_instance_logger``/``PymapdlCustomAdapter``) so no real MAPDL
# instance is needed.


def _make_fake_instance_logger(name, level=None):
    """Create an instance logger the same way ``_MapdlCore.__init__`` does."""
    fake_mapdl = Mock()
    fake_mapdl.name = name
    return fake_mapdl, LOG.add_instance_logger(name, fake_mapdl, level=level)


def test_instance_logger_is_real_child_of_global_logger():
    """Instance loggers must be true ``logging`` children of ``pymapdl_global``.

    This enables level cascading via ``getEffectiveLevel()`` while
    ``propagate`` stays disabled (see ``GlobalForwardingHandler``) so
    records are never delivered twice.
    """
    _, inst_log = _make_fake_instance_logger("172.30.30.1:50052")
    assert inst_log.logger.name.startswith(f"{LOG.logger.name}.")
    assert inst_log.logger.parent is LOG.logger
    assert inst_log.logger.propagate is False
    assert any(
        isinstance(h, logging.GlobalForwardingHandler) for h in inst_log.logger.handlers
    )


def test_instance_logger_uniqueness_check_deduplicates():
    """``add_instance_logger`` must detect real name collisions.

    Regression test for a bug where the uniqueness check inspected
    ``logging.root.manager.__dict__`` (the ``Manager`` object's own
    attributes) instead of ``logging.Logger.manager.loggerDict`` (the
    actual registered logger names), so it never triggered.
    """
    name = "172.30.30.2:50052"
    _, log_a = _make_fake_instance_logger(name)
    _, log_b = _make_fake_instance_logger(name)

    assert log_a.logger.name != log_b.logger.name
    assert log_b.logger.name.endswith("_1")


def test_no_duplicate_log_emission(caplog):
    """A record logged through an instance logger must reach a given
    ``pymapdl_global`` handler exactly once.

    Regression test for the double-emission bug: a real dotted hierarchy
    combined with ``propagate=True`` *and* copied handlers used to deliver
    every record twice (once via the instance's own handler copy, once via
    propagation to the parent's original handler).
    """
    buf = io.StringIO()
    handler = deflogging.StreamHandler(buf)
    handler.setLevel(deflogging.DEBUG)
    LOG.logger.addHandler(handler)
    previous_level = LOG.logger.level
    LOG.logger.setLevel(deflogging.DEBUG)
    try:
        _, inst_log = _make_fake_instance_logger("172.30.30.3:50052")
        inst_log.debug("no-duplicate-message")
        text = buf.getvalue()
        assert text.count("no-duplicate-message") == 1
    finally:
        LOG.logger.removeHandler(handler)
        LOG.logger.setLevel(previous_level)


def test_global_sink_reaches_existing_instances_retroactively():
    """Handlers added to ``LOG`` after an instance logger already exists
    must still receive that instance's records (unified, "live" sink)."""
    _, inst_log = _make_fake_instance_logger("172.30.30.4:50052")

    buf = io.StringIO()
    handler = deflogging.StreamHandler(buf)
    handler.setLevel(deflogging.DEBUG)
    LOG.logger.addHandler(handler)
    previous_level = LOG.logger.level
    LOG.logger.setLevel(deflogging.DEBUG)
    try:
        inst_log.debug("retroactive-message")
        assert "retroactive-message" in buf.getvalue()
    finally:
        LOG.logger.removeHandler(handler)
        LOG.logger.setLevel(previous_level)


def test_level_cascades_from_global_logger():
    """``LOG.setLevel()`` must cascade to instance loggers created without
    an explicit level of their own (left at ``NOTSET``)."""
    _, inst_log = _make_fake_instance_logger("172.30.30.5:50052", level=None)

    previous_level = LOG.logger.level
    try:
        LOG.logger.setLevel(deflogging.WARNING)
        assert inst_log.logger.getEffectiveLevel() == deflogging.WARNING

        LOG.logger.setLevel(deflogging.DEBUG)
        assert inst_log.logger.getEffectiveLevel() == deflogging.DEBUG
    finally:
        LOG.logger.setLevel(previous_level)


def test_instances_registry_and_loggerdict_shrink_after_gc():
    """``LOG._instances`` and ``logging.Logger.manager.loggerDict`` must not
    grow without bound for instances that are simply dereferenced (never
    explicitly ``exit()``-ed), which is the scenario behind the reported
    resource leak."""
    before_instances = len(LOG._instances)
    before_loggerdict = len(deflogging.Logger.manager.loggerDict)

    created = []
    full_names = []
    for i in range(25):
        _, inst_log = _make_fake_instance_logger(f"172.31.{i}.1:5005{i % 10}")
        created.append(inst_log)
        full_names.append(inst_log.logger.name)
    # Avoid leaving the loop variables bound to the last created instance,
    # which would otherwise keep exactly that one instance alive below.
    del _, inst_log

    assert len(LOG._instances) >= before_instances + 25
    assert len(deflogging.Logger.manager.loggerDict) >= before_loggerdict + 25

    # Drop the only strong references and force collection.
    del created
    gc.collect()

    assert len(LOG._instances) == before_instances
    assert len(deflogging.Logger.manager.loggerDict) == before_loggerdict
    for full_name in full_names:
        assert full_name not in deflogging.Logger.manager.loggerDict


def test_no_leaked_file_handles_after_many_create_destroy_cycles(tmp_path):
    """Instance loggers with their own file handler must not leak open file
    descriptors across many create/destroy cycles."""
    psutil = pytest.importorskip("psutil")
    if not hasattr(psutil.Process(), "num_fds"):
        pytest.skip("num_fds() is only available on Unix platforms")

    process = psutil.Process()
    before_fds = process.num_fds()

    for i in range(20):
        fake_mapdl, inst_log = _make_fake_instance_logger(f"172.32.{i}.1:50052")
        inst_log.log_to_file(str(tmp_path / f"instance_{i}.log"))
        inst_log.debug("some message")

        # Mirrors ``MapdlBase._cleanup_loggers``'s eager path.
        name_key = getattr(inst_log, "name_key", None)
        logging._finalize_child_logger(inst_log.logger.name, name_key, LOG._instances)

    gc.collect()
    after_fds = process.num_fds()
    assert after_fds <= before_fds + 2  # small slack for unrelated fd churn


def test_set_log_level_affects_multiple_instances_independently():
    """``_MapdlCore.set_log_level`` must set the level on the *calling*
    instance's own logger.

    Regression test for a bug where it delegated to a module-level
    ``setup_logger()`` helper that memoized a single logger process-wide
    (via a function attribute), so only the first call in the whole
    process ever had any effect.
    """
    from ansys.mapdl.core.mapdl_core import _MapdlCore

    fake_a, log_a = _make_fake_instance_logger("172.33.1.1:50052")
    fake_b, log_b = _make_fake_instance_logger("172.33.1.2:50052")
    fake_a._log = log_a
    fake_b._log = log_b

    _MapdlCore.set_log_level(fake_a, "DEBUG")
    _MapdlCore.set_log_level(fake_b, "ERROR")

    assert log_a.logger.level == deflogging.DEBUG
    assert log_b.logger.level == deflogging.ERROR


def test_setup_logger_is_deprecated_and_works_per_instance():
    """The legacy ``setup_logger`` helper is deprecated but still usable,
    and must no longer memoize a single logger process-wide."""
    from ansys.mapdl.core.mapdl_core import setup_logger

    fake_a = Mock()
    fake_a.name = "172.33.2.1:50052"
    fake_a._log = None
    fake_b = Mock()
    fake_b.name = "172.33.2.2:50052"
    fake_b._log = None

    with pytest.deprecated_call():
        log_a = setup_logger(loglevel="DEBUG", mapdl_instance=fake_a)
    with pytest.deprecated_call():
        log_b = setup_logger(loglevel="ERROR", mapdl_instance=fake_b)

    assert log_a is not log_b
    assert log_a.logger.level == deflogging.DEBUG
    assert log_b.logger.level == deflogging.ERROR


def test_instance_logger_level_is_never_none():
    """``PymapdlCustomAdapter.level`` must never be ``None``.

    Regression test for a crash surfaced once ``set_log_level`` was fixed to
    actually apply its argument:
    ``ansys.mapdl.core.misc.supress_logging`` reads ``mapdl._log.level``
    before a call, to restore it afterwards. Because the level used to be a
    static ``None`` class attribute until ``setLevel()`` was called
    explicitly, a fresh instance logger (left at ``NOTSET`` for cascading)
    would hand ``None`` back into ``setLevel``, raising
    ``TypeError: Level not an integer or a valid string: None``.
    """
    _, inst_log = _make_fake_instance_logger("172.34.1.1:50052", level=None)
    assert inst_log.level is not None
    assert isinstance(inst_log.level, int)

    # Must round-trip through setLevel without raising, mirroring
    # ``supress_logging``'s save/restore pattern.
    inst_log.setLevel(inst_log.level)


def test_supress_logging_restores_prior_level_without_crashing():
    """End-to-end regression test for the ``supress_logging`` decorator
    interacting with a freshly-created (``NOTSET``) instance logger."""
    from ansys.mapdl.core.mapdl import MapdlBase
    from ansys.mapdl.core.misc import supress_logging

    class _FakeMapdl(MapdlBase):
        def __init__(self, log):
            self._log = log

        def _set_log_level(self, level):
            self._log.setLevel(level)

    _, inst_log = _make_fake_instance_logger("172.34.2.1:50052", level=None)
    fake_mapdl = _FakeMapdl(inst_log)

    @supress_logging
    def fake_method(mapdl):
        assert mapdl._log.level == deflogging.CRITICAL
        return "ok"

    assert fake_method(fake_mapdl) == "ok"
