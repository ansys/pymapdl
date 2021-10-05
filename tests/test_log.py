""""Testing of log module"""
from ansys.mapdl.core  import log

import re
import pytest


LOG_LEVELS =  {'CRITICAL': 50,
'ERROR': 40,
'WARNING': 30,
'INFO': 20,
'DEBUG': 10}


def get_logger_text(fname=log.FILE_NAME):
    with(open(fname, 'r')) as fid:
        return ''.join(fid.readlines())

def find_logmsg_in_logfile(prev_string='INFO', string='', text=None):
    if text is None:
        text = get_logger_text()
    if re.findall(f'^.*{prev_string}.*{string}.*$', text, re.MULTILINE):
        return True
    else:
        return False


def test_log_levels(mapdl):
    for each_log_name, each_log_number in LOG_LEVELS.items():
        string = f'This is an {each_log_name} log'
        mapdl._log.log(each_log_number, string)
        assert find_logmsg_in_logfile(each_log_name, string)


def test_log_nesting(mapdl):
    hierarchy = 'this.is.a.hierarchy.which.is.used.for.build.loggers'

    for each in hierarchy.split('.'):
        logger = log.getLogger(each)

    assert hierarchy in logger.name


# def test_log_different_loglevel(mapdl):
#     logger = log.getLogger(loglevel='ERROR')


def test_log_uncaught_exception(mapdl):
    exception_msg = 'Uncaught exception'
    with pytest.raises(Exception):
        raise Exception(exception_msg)
    assert find_logmsg_in_logfile('', exception_msg)


def test_log_change_in_file_msg(mapdl):
    logger = log.getLogger('test', file_msg='%(asctime)-15s | %(funcName)-25s | THIS IS A TEST %(message)s')
    logger.info('An useful info message')

    find_logmsg_in_logfile('THIS IS A TEST', 'An useful info message')
