"""gRPC service specific tests"""
import os

import pytest

from ansys.mapdl.core import examples

PATH = os.path.dirname(os.path.abspath(__file__))


def test_clear_nostart(mapdl):
    resp = mapdl._send_command('FINISH')
    resp = mapdl._send_command('/CLEAR, NOSTART')
    assert 'CLEAR ANSYS DATABASE AND RESTART' in resp


# NOTE: This command cannot be run repeately, otherwise we end up with
# to many levels of /INPUT.  2021R2 should have a fix for this
def test_clear(mapdl):
    resp = mapdl._send_command('FINISH')
    resp = mapdl._send_command('/CLEAR')
    assert 'CLEAR' in resp


def test_clear_multiple(mapdl):
    # simply should not fail.  See:
    # https://github.com/pyansys/pymapdl/issues/380
    for i in range(20):
        mapdl.run('/CLEAR')


def test_invalid_get(mapdl):
    with pytest.raises(ValueError):
        mapdl.get_value("ACTIVE", item1="SET", it1num='invalid')


def test_stream(mapdl):
    resp = mapdl._send_command_stream('/PREP7')
    assert 'PREP7' in resp


def test_basic_input_output(mapdl, tmpdir):
    mapdl.finish()
    mapdl.clear('NOSTART')
    filename = 'tmp2.inp'
    basic_inp = tmpdir.join(filename)
    with open(basic_inp, 'w') as f:
        f.write('FINISH\n')
        f.write('/PREP7\n')

    mapdl.upload(basic_inp)
    tmpfile = 'tmp.out'
    mapdl._send_command('/OUT, %s' % tmpfile, mute=True)
    mapdl._send_command('/INPUT, %s' % filename, mute=True)
    mapdl._send_command('/OUT, TERM', mute=True)
    mapdl.download(tmpfile)
    assert os.path.isfile(tmpfile)
    # input file won't actually run, but we want to see if the output switches


def test_upload_large(mapdl):
    mapdl.finish()
    mapdl.clear('NOSTART')

    file_name = examples.vmfiles['vm153']
    test_file = os.path.join(PATH, 'test_files', file_name)

    mapdl.upload(test_file)
    assert os.path.basename(file_name) in mapdl.list_files()


def test_upload_fail(mapdl):
    with pytest.raises(FileNotFoundError):
        mapdl.upload('thisisnotafile')


def test_input_empty(mapdl):
    resp = mapdl._send_command('/INPUT')
    assert 'INPUT FILE' in resp


def test_input_empty(mapdl):
    resp = mapdl._send_command('/INPUT, not_a_file')
    assert 'does not exist' in resp


def test_download_missing_file(mapdl, tmpdir):
    target = tmpdir.join('tmp')
    with pytest.raises(FileNotFoundError):
        mapdl.download('__notafile__', target)


# these tests take some time to run, and we might consider moving
# these to a functional testing module/directory outside of the tests
# directory.

def test_read_input_file_verbose(mapdl):
    test_file = examples.vmfiles['vm153']
    mapdl.finish()
    mapdl.clear()
    response = mapdl.input(test_file, verbose=True)
    assert '*****  ANSYS SOLUTION ROUTINE  *****' in response


test_files = ['full26.dat', 'static.dat']
@pytest.mark.parametrize('file_name', test_files)
def test_read_input_file(mapdl, file_name):
    test_file = os.path.join(PATH, 'test_files', file_name)
    mapdl.finish()
    mapdl.clear()
    response = mapdl.input(test_file)
    assert '*****  ANSYS SOLUTION ROUTINE  *****' in response
