""""Testing of log module"""
from ansys.mapdl.core import logging
import logging as deflogging  # Default logging
from ansys.mapdl.core import LOG  # Global logger

from conftest import HAS_GRPC

import re
import pytest
import os

## Notes
# Use the next fixtures for:
# - capfd: for testing console printing.
# - caplog: for testing logging printing.

LOG_LEVELS =  {'CRITICAL': 50,
'ERROR': 40,
'WARNING': 30,
'INFO': 20,
'DEBUG': 10}


def fake_record(logger, msg ='This is a message', instance_name='172.1.1.1:52000', handler_index=0, name_logger=None, level=deflogging.DEBUG, filename='fn', lno=0, args=(), exc_info=None, extra={}):
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

    if 'instance_name' not in extra.keys():
        extra['instance_name'] = instance_name

    record = logger.makeRecord(name_logger, level, filename, lno, msg, args=args, exc_info=exc_info, extra=extra, sinfo=sinfo)
    handler = logger.handlers[handler_index]
    return handler.format(record)


def test_stdout_reading(capfd):
    print('This is a test')

    out, err = capfd.readouterr()
    assert out == "This is a test\n"


def test_only_logger(caplog):
    log_a = deflogging.getLogger('test')
    log_a.setLevel('DEBUG')

    log_a.debug('This is another test')
    assert 'This is another test' in caplog.text


def test_global_logger_exist():
    assert isinstance(LOG._global, deflogging.Logger)
    assert LOG._global.name == '_Global_'


def test_global_logger_has_handlers():
    assert hasattr(LOG, '_file_handler')
    assert hasattr(LOG, '_std_out_handler')
    assert LOG._global.hasHandlers
    assert LOG._file_handler or LOG._std_out_handler  # at least a handler is not empty


def test_global_logger_logging(caplog):
    for each_log_name, each_log_number in LOG_LEVELS.items():
        msg = f'This is an {each_log_name} message.'
        LOG._global.log(each_log_number, msg)
        # Make sure we are using the right logger, the right level and message.
        assert caplog.record_tuples[-1] == ("_Global_", each_log_number, msg)

def test_global_logger_debug_mode():
    assert deflogging.DEBUG == LOG._global.level

def test_global_logger_exception_handling(caplog):
    exc = 'Unexpected exception'
    with pytest.raises(Exception):
        raise Exception(exc)
        assert exc in caplog.text


def test_global_logger_debug_levels(caplog):
    """Testing for all the possible logging level that the output is recorded properly for each type of msg."""
    for each_level in [deflogging.DEBUG, deflogging.INFO, deflogging.WARN, deflogging.ERROR, deflogging.CRITICAL]:
        with caplog.at_level(each_level, LOG._global.name):  # changing root logger level:
            for each_log_name, each_log_number in LOG_LEVELS.items():
                msg = f'This is an {each_log_name} message.'
                LOG._global.log(each_log_number, msg)
                # Make sure we are using the right logger, the right level and message.
                if each_log_number >= each_level:
                    assert caplog.record_tuples[-1] == ("_Global_", each_log_number, msg)
                else:
                    assert caplog.record_tuples[-1] != ("_Global_", each_log_number, msg)


@pytest.mark.skipif(not HAS_GRPC, reason="Requires GRPC")
def test_global_logger_format():
    # Since we cannot read the format of our logger, because pytest just dont show the console output or
    # if it does, it formats the logger with its own formatter, we are going to check the logger handlers
    # and output by faking a record.
    # This method is not super robust, since we are input fake data to ``logging.makeRecord``.
    # There are things such as filename or class that we cannot evaluate without going
    # into the code.

    assert 'instance' in logging.FILE_MSG_FORMAT
    assert 'instance' in logging.STDOUT_MSG_FORMAT

    log = fake_record(LOG._global, msg ='This is a message', level=deflogging.DEBUG, extra={'instance_name': '172.1.1.1'})
    assert re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', log)
    assert 'DEBUG' in log
    assert 'This is a message' in log


@pytest.mark.skipif(not HAS_GRPC, reason="Requires GRPC")
def test_instance_logger_format(mapdl):
    # Since we cannot read the format of our logger, because pytest just dont show the console output or
    # if it does, it formats the logger with its own formatter, we are going to check the logger handlers
    # and output by faking a record.
    # This method is not super robust, since we are input fake data to ``logging.makeRecord``.
    # There are things such as filename or class that we cannot evaluate without going
    # into the code.

    log = fake_record(mapdl._log.logger, msg ='This is a message', level=deflogging.DEBUG, extra={'instance_name': '172.1.1.1'})
    assert re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', log)
    assert 'DEBUG' in log
    assert 'This is a message' in log

def test_global_methods(caplog):
    msg = f'This is a debug message'
    LOG.debug(msg)
    assert msg in caplog.text

    msg = f'This is an info message'
    LOG.info(msg)
    assert msg in caplog.text

    msg = f'This is a warning message'
    LOG.warning(msg)
    assert msg in caplog.text

    msg = f'This is an error message'
    LOG.error(msg)
    assert msg in caplog.text

    msg = f'This is a critical message'
    LOG.critical(msg)
    assert msg in caplog.text

    msg = f'This is a 30 message using "log"'
    LOG.log(30, msg)
    assert msg in caplog.text


def test_add_file_handler(tmpdir):
    n_handlers = len(LOG._global.handlers)
    LOG.add_file_handler('file.log')
    assert len(LOG._global.handlers) == n_handlers + 1
    assert LOG._file_handler == LOG._global.handlers[-1]
    assert isinstance(LOG._file_handler, deflogging.FileHandler)

def test_log_to_file(tmpdir):
    # Checking there is actually a file handler.
    if not LOG._file_handler:
        LOG.add_file_handler('file.log')

    LOG.debug('This is a debug log')

    with open('file.log', 'r') as fid:
        text = ''.join(fid.readlines())

    assert 'This is a debug log' in text

def test_instance_log_to_file(mapdl, tmpdir):
    file_path = os.path.join(tmpdir, 'instance.log')
    file_msg = 'This is a debug message'
    if not mapdl._log._file_handler:
        mapdl._log.add_file_handler(file_path)

    mapdl._log.debug(file_msg)

    with open(file_path, 'r') as fid:
        text = ''.join(fid.readlines())

    assert file_msg in text
    assert 'DEBUG' in text
