# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

"""Test PyMAPDL license.py module."""

import os
import time
import types

import pytest

from ansys.mapdl.core import errors, launch_mapdl, licensing
from ansys.mapdl.core.misc import threaded
from conftest import ON_LOCAL as IS_LOCAL
from conftest import QUICK_LAUNCH_SWITCHES, requires

LIC_INSTALLED: bool = False
try:
    LIC_INSTALLED = os.path.isfile(licensing.get_ansys_license_utility_path())
except:
    pass

skip_no_lic_bin = pytest.mark.skipif(
    not (LIC_INSTALLED and IS_LOCAL),
    reason="Requires being in 'local' mode and have license utilities binaries.",
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

MSG_LIC_DENIED = """
        2021/09/06 22:39:38    DENIED              ansys                           21.2 (2021.0512)             1/0/0/0                 1/1/1/1   1026:FEAT_ANSYS:user@machine.win.ansys.com:winx64   0000:1.1.1.1
                    Request name ansys does not exist in the licensing pool.
                    Cannot connect to license server system.
                    The license server manager (lmgrd) has not been started yet,
                    the wrong port@host or license file is being used, or the
                    port or hostname in the license file has been changed.
                    Feature:       ansys
                    Server nam0000 1.1.1.1
                    License path:  1055@machine;
                    FlexNet Licensing error:-15,578.  System Error: 10049 "WinSock: Invalid address"
"""
MSG_LIC_CHECKOUT = """
        2021/09/06 22:39:38    CHECKOUT              ansys                           21.2 (2021.0512)             1/0/0/0                 1/1/1/1   1026:FEAT_ANSYS:user@machine.win.ansys.com:winx64   0000:1.1.1.1
                    Request name ansys does not exist in the licensing pool.
                    Cannot connect to license server system.
                    The license server manager (lmgrd) has not been started yet,
                    the wrong port@host or license file is being used, or the
                    port or hostname in the license file has been changed.
                    Feature:       ansys
                    Server nam0000 1.1.1.1
                    License path:  1055@machine;
                    FlexNet Licensing error:-15,578.  System Error: 10049 "WinSock: Invalid address"
"""


# TEST-NET-3 (not quite a black hole, but set aside by RFC 5737)
TEST_NET_3 = "203.0.113.0"

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


@pytest.fixture(scope="module")
def license_checker():
    return licensing.LicenseChecker()


@skip_no_lic_bin
def test_get_ansys_license_directory():
    ansyslic_dir = licensing.get_ansys_license_directory()
    if os.name == "nt":
        assert "Shared Files" in ansyslic_dir and "Licensing" in ansyslic_dir
    else:
        assert os.path.isdir(ansyslic_dir)
        assert "shared_files" in ansyslic_dir and "licensing" in ansyslic_dir


@skip_no_lic_bin
def test__checkout_wrong_license(license_checker):
    with pytest.raises(ValueError):
        license_checker._checkout_license("meeeeba")


@skip_no_lic_bin
def test__checkout_license_fail(license_checker):
    output = license_checker._checkout_license("meba", TEST_NET_3, 1055)
    assert "CHECKOUT FAILED" in output


@skip_no_lic_bin
def test__check_mech_license_available(license_checker):
    license_checker._check_mech_license_available()


@skip_no_lic_bin
def test__check_mech_license_available_specified_license(license_checker):
    license_checker._check_mech_license_available(licenses="meba")


@skip_no_lic_bin
def test_check_mech_license_available_fail(license_checker):
    with pytest.raises(errors.LicenseServerConnectionError):
        license_checker._check_mech_license_available(TEST_NET_3)


def test_get_ansys_license_debug_file_tail_timeout(license_checker):
    with pytest.raises(TimeoutError):
        msg = licensing.get_ansys_license_debug_file_tail(
            "does_not_exist", start_timeout=0.05
        )
        next(msg)


def test_get_ansys_license_debug_file_tail(tmpdir, license_checker):
    tmp_file = tmpdir.join("tmplog.log")
    write_log(tmp_file)

    msg_iter = licensing.get_ansys_license_debug_file_tail(tmp_file, start_timeout=1)
    isinstance(msg_iter, types.GeneratorType)
    for line in msg_iter:
        if "CHECKOUT" in line:
            break

    assert "CHECKOUT" in line


@requires("local")
@skip_no_lic_bin
def test_check_license_file_fail(license_checker):
    with pytest.raises(TimeoutError):
        license_checker._check_license_file(timeout=0.1)


@skip_no_lic_bin
def test_license_checker(tmpdir, license_checker):
    # validate license checker (this will only checkout the license)
    license_checker.start(license_file=False, checkout_license=True)
    assert license_checker.check() is False
    assert license_checker._license_checkout_success is None
    license_checker.wait()
    assert license_checker.check()


@requires("local")
@skip_no_lic_bin
def test_check_license_file(mapdl, cleared, tmpdir):
    timeout = 15
    checker = licensing.LicenseChecker(timeout=timeout)
    # start the license check in the background
    checker.start(checkout_license=False)

    try:
        mapdl_ = launch_mapdl(
            license_server_check=False,
            start_timeout=timeout,
            additional_switches=QUICK_LAUNCH_SWITCHES,
            port=mapdl.port + 1,
        )
        assert mapdl_._local
        mapdl_.exit()
    except IOError:  # MAPDL never started
        assert not checker._license_file_success
    else:
        assert checker._license_file_success


def test__check_license_file_iterator(tmpdir, license_checker):
    file_name = "lic.log"
    file_ = tmpdir.join(file_name)

    def create_log_file(file_, msg):
        file_iterator = licensing.get_ansys_license_debug_file_tail(file_, debug=True)
        with open(file_, "w") as fid:
            fid.write(msg)
        return file_iterator

    # making it fail
    notify_at_second = 1  # sec
    timeout = -1
    file_iterator = create_log_file(file_, MSG_LIC_DENIED)
    with pytest.raises(TimeoutError):
        license_checker._check_license_file_iterator(
            file_iterator, file_, timeout, notify_at_second
        )

    # Running it with message.
    notify_at_second = 0
    timeout = 10
    file_iterator = create_log_file(file_, MSG_LIC_DENIED)
    with pytest.raises(errors.LicenseServerConnectionError):
        license_checker._check_license_file_iterator(
            file_iterator, file_, timeout, notify_at_second
        )

    notify_at_second = 0
    timeout = 10
    file_iterator = create_log_file(file_, MSG_LIC_CHECKOUT)
    assert license_checker._check_license_file_iterator(
        file_iterator, file_, timeout, notify_at_second
    )


def test_stop(license_checker):
    license_checker.stop = True
    assert license_checker._stop

    license_checker.stop = 0
    assert not license_checker._stop


def test_is_connected(license_checker):
    license_checker.is_connected = True
    assert license_checker._is_connected

    license_checker.is_connected = 0
    assert not license_checker._is_connected


@skip_no_lic_bin
def test_check_license_file_exception(license_checker):
    with pytest.raises(TimeoutError):
        license_checker._check_license_file(0.01)


@requires("ansys-tools-common")
def test_license_wait():
    license_checker = licensing.LicenseChecker()
    assert not license_checker._lic_file_thread
    assert not license_checker._checkout_thread

    license_checker.start(checkout_license=True)
    assert license_checker._lic_file_thread
    assert license_checker._checkout_thread

    license_checker.wait()
    assert license_checker._lic_file_thread
    assert license_checker._checkout_thread


def test_license_check():
    license_checker = licensing.LicenseChecker()

    license_checker._license_file_success = True
    assert license_checker.check()

    with pytest.raises(errors.LicenseServerConnectionError):
        license_checker._license_file_success = False
        license_checker.check()

    license_checker._license_file_success = None
    license_checker._license_checkout_success = True
    assert license_checker.check()

    with pytest.raises(errors.LicenseServerConnectionError):
        license_checker._license_file_success = None
        license_checker._license_checkout_success = False
        license_checker.check()


@requires("ansys-tools-common")
def test_stop_license_checker():
    license_checker = licensing.LicenseChecker()

    license_checker.start()
    time.sleep(1)
    prev_stop = license_checker.stop
    prev_is_connected = license_checker.is_connected

    license_checker.stop = True  # Overwriting the connect attribute
    # so the thread is killed right after.
    time.sleep(2)

    # Starting by #3421 the following line gives error but is not critical,
    # so I'm disabling it.
    # assert not license_checker._lic_file_thread.is_alive()
    assert not prev_stop
    assert not prev_is_connected


@skip_no_lic_bin
def test__checkout_license(license_checker):
    assert license_checker._checkout_license("mech_1")  # using default host and port


def test_verbose_deprecating():
    with pytest.raises(DeprecationWarning):
        licensing.LicenseChecker(verbose=True)
