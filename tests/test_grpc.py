"""gRPC service specific tests"""
import os

import pytest

from ansys.mapdl.core import examples
from ansys.mapdl.core.launcher import get_start_instance

PATH = os.path.dirname(os.path.abspath(__file__))

# skip entire module unless HAS_GRPC installed or connecting to server
pytestmark = pytest.mark.skip_grpc

skip_launch_mapdl = pytest.mark.skipif(get_start_instance(),
                                       reason="Must be able to launch MAPDL locally")


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


@skip_launch_mapdl  # need to be able to start/stop an instance of MAPDL
def test_grpc_custom_ip():
    from ansys.mapdl.core import launch_mapdl
    
    ip='127.0.0.2'
    mapdl = launch_mapdl(ip=ip)

    # Check the ip
    # print(mapdl._ip)

    # Check it also in the output file.
    # print(mapdl.directory)

    output_file = mapdl._download_as_raw('.__tmp__.out')
    output = output_file.decode().splitlines()

    # Catching the line where the IP of the gRPC server is specified.
    for each_line in output:
        if 'Server listening on' in each_line: 
            line = each_line
            print(each_line)

    mapdl.exit()

    assert ip in line


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
