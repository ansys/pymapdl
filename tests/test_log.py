""""Testing of log module"""
from ansys.mapdl.core.log import FILE_NAME

def find_string_in_log(string):
    with(open(FILE_NAME, 'r')) as fid:
        text = ''.join(fid.readlines())
    return string in text


def test_log_info(mapdl):
    string = 'This is an info log'
    mapdl._log.info('This is an info log')
    assert find_string_in_log(string)
