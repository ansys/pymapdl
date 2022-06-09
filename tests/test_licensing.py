"""Test PyMAPDL license.py module."""

import os
import time
import types

import pytest

from ansys.mapdl.core import errors, launch_mapdl, licensing
from ansys.mapdl.core.launcher import check_valid_ansys, get_start_instance
from ansys.mapdl.core.misc import threaded

skip_launch_mapdl = pytest.mark.skipif(
    not get_start_instance() and check_valid_ansys(),
    reason="Must be able to launch MAPDL locally",
)


FAKE_CHECKOUT_SUCCESS = """
2021/09/17 14:08:19    INFO                Starting Licensing Client Proxy server.
2021/09/17 14:08:19    INFO                /usr/ansys_inc/v212/licensingclient/linx64/ansyscl -acl 3423788.77064 -nodaemon -log /home/USER/.ansys/ansyscl.HOST.3423788.77064.log
2021/09/17 14:08:19    INFO                Started ANSYSLI server.
2021/09/17 14:08:21    CLIENT_CONNECT                                                                                           1/1/1/1   3423788:FEAT_ANSYS:USER@HOST:linx64                         25:127.0.1.1
2021/09/17 14:08:21    NEW_CONNECTION      Connected to Licensing Client Proxy server: 55923@127.0.0.1.
2021/09/17 14:08:21    CHECKOUT            ansys                           21.2 (2021.0512)            1/1/1/30                 1/1/1/1   3423788:FEAT_ANSYS:USER@HOST:linx64                         25:127.0.1.1
2021/09/17 14:08:21    CHECKOUT            FEAT_ANSYS                      21.2 (2021.0512)             1/1/1/1                 1/1/1/1   3423788:FEAT_ANSYS:USER@HOST:linx64                         25:127.0.1.1
2021/09/17 14:08:21    SPLIT_CHECKOUT      HPC_PARALLEL                    21.2 (2021.0512)             2/2/2/4                 1/1/1/1   3423788:FEAT_ANSYS:USER@HOST:linx64                         25:127.0.1.1
2021/09/17 14:08:21    CHECKOUT            HPC_PARALLEL                    21.2 (2021.0512)             2/2/2/4                 1/1/1/1   3423788:FEAT_ANSYS:USER@HOST:linx64                         25:127.0.1.1
"""


# TEST-NET-3 (not quite a black hole, but set aside by RFC 5737)
test_net_3 = "203.0.113.0"

PATH = os.path.dirname(os.path.abspath(__file__))
SAMPLE_LOG_PATH = os.path.join(PATH, "test_files", "sample_lic_log.log")


@threaded
def write_log(path):
    """Write in a background process to a file"""
    time.sleep(0.01)
    with open(path, "w") as fid:
        for line in FAKE_CHECKOUT_SUCCESS.splitlines():
            fid.write(line + "\n")
            time.sleep(0.01)


try:
    LIC_INSTALLED = licensing.get_ansyslic_dir()
except:
    LIC_INSTALLED = None

skip_no_lic_bin = pytest.mark.skipif(
    not LIC_INSTALLED, reason="Requires local license utilities binaries"
)


@skip_no_lic_bin
def test_get_licdebug_path():
    ansyslic_dir = licensing.get_ansyslic_dir()
    if os.name == "nt":
        assert "Shared Files" in ansyslic_dir and "Licensing" in ansyslic_dir
    else:
        assert os.path.isdir(ansyslic_dir)
        assert "shared_files" in ansyslic_dir and "licensing" in ansyslic_dir


@skip_no_lic_bin
def test_checkout_license():
    output = licensing.checkout_license("meba")
    assert "ANSYS LICENSE MANAGER ERROR" not in output


@skip_no_lic_bin
def test_checkout_license_fail():
    output = licensing.checkout_license("meba", test_net_3, 1055)
    assert "CHECKOUT FAILED" in output


@skip_no_lic_bin
def test_check_mech_license_available():
    licensing.check_mech_license_available()


@skip_no_lic_bin
def test_check_mech_license_available_fail():
    with pytest.raises(errors.LicenseServerConnectionError):
        licensing.check_mech_license_available(test_net_3)


def test_get_licdebug_tail_timeout():
    with pytest.raises(TimeoutError):
        msg = licensing.get_licdebug_tail("does_not_exist", start_timeout=0.05)
        next(msg)


def test_get_licdebug_tail(tmpdir):
    tmp_file = tmpdir.join("tmplog.log")
    write_log(tmp_file)

    msg_iter = licensing.get_licdebug_tail(tmp_file, start_timeout=1)
    isinstance(msg_iter, types.GeneratorType)
    for line in msg_iter:
        if "CHECKOUT" in line:
            break

    assert "CHECKOUT" in line


@skip_launch_mapdl
@skip_no_lic_bin
def test_check_license_file_fail():
    with pytest.raises(TimeoutError):
        licensing.check_license_file(timeout=0.1)


@skip_no_lic_bin
def test_license_checker(tmpdir):
    # validate license checker (this will only checkout the license)
    checker = licensing.LicenseChecker()
    checker.start(license_file=False, checkout_license=True)
    assert checker.check() is False
    assert checker._license_checkout_success is None
    checker.wait()
    assert checker.check()


@skip_launch_mapdl
@skip_no_lic_bin
def test_check_license_file(tmpdir):
    timeout = 15
    checker = licensing.LicenseChecker(verbose=True, timeout=timeout)
    # start the license check in the background
    checker.start(checkout_license=False)

    try:
        mapdl = launch_mapdl(license_server_check=False, start_timeout=timeout)
        assert mapdl._local
        mapdl.exit()
    except IOError:  # MAPDL never started
        assert not checker._license_file_success
    else:
        assert checker._license_file_success
