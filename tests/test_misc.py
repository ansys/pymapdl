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

"""Small or misc tests that don't fit in other test modules"""
import os
import pathlib

import numpy as np
import pytest

from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_routine,
    create_temp_dir,
    last_created,
    load_file,
    no_return,
    requires_package,
    run_as,
)
from conftest import requires


@pytest.mark.parametrize(
    "ip",
    [
        "localhost",
        "LOCALhost",
        "192.1.1.1",
        "127.0.0.01",
    ],
)
def test_check_valid_ip(ip):
    check_valid_ip(ip)


@pytest.mark.parametrize("ip", ["asdf", "300.2.2.2"])
def test_check_valid_ip_error(ip):
    with pytest.raises(OSError):
        check_valid_ip(ip)


@pytest.mark.parametrize(
    "port",
    [
        5000,
        50053,
        10000,
    ],
)
def test_check_valid_port(port):
    check_valid_port(port)


@pytest.mark.parametrize(
    "port",
    [
        "asdf",
        "2323",
        1,
        1e9,
    ],
)
def test_check_valid_port_error(port):
    with pytest.raises(ValueError):
        check_valid_port(port)


def test_creation_time(tmpdir):
    files_ = []
    for i in range(4):
        file_name = f"tmp_{i}.tmp"
        file_path = str(tmpdir.join(file_name))
        files_.append(file_path)

        with open(file_path, "w") as fid:
            fid.write("")

    assert last_created(files_) is not None


def test_run_as_prep7(mapdl, cleared):
    mapdl.post1()
    assert "POST1" in mapdl.parameters.routine

    @run_as("PREP7")
    def fun(
        mapdl,
    ):  # This function is for mapdl methods, hence we have to pass the MAPDL instance somehow.
        mapdl.k("", 1, 1, 1)

    fun(mapdl)
    assert "POST1" in mapdl.parameters.routine
    last_keypoint = np.array(mapdl.klist().splitlines()[-1].split(), dtype=float)[0:4]
    assert np.allclose(last_keypoint, np.array([1, 1, 1, 1]))


def test_no_return(mapdl, cleared):

    @no_return
    def fun(
        mapdl,
    ):  # This function is for mapdl methods, hence we have to pass the MAPDL instance somehow.
        mapdl.k("", 1, 1, 1)

    assert fun(mapdl) is None
    last_keypoint = np.array(mapdl.klist().splitlines()[-1].split(), dtype=float)[0:4]
    assert np.allclose(last_keypoint, np.array([1, 1, 1, 1]))


@pytest.mark.parametrize("file_", ["dummy.dumdum", "dumdum.dummy"])
def test_load_file_local(mapdl, cleared, tmpdir, file_):
    """Checking 'load_file' function.

    In CICD it seems we cannot write to the root folder '/'.
    Hence we cannot really test the files are being uploaded.
    """
    # first cleaning
    mapdl.slashdelete(file_)

    if file_ == "dumdum.dummy":
        # Upload from a different folder
        file_path = str(tmpdir.mkdir("tmpdir").join(file_))
    else:
        file_path = file_

    # remove the file in the rare case it's been left over from a failed run
    if os.path.isfile(file_path):
        os.remove(file_path)

    # When the file does not exist
    with pytest.raises(FileNotFoundError):
        load_file(mapdl, file_path)

    # File is in the python working directory
    with open(file_path, "w") as fid:
        fid.write("empty")

    assert os.path.exists(file_path)

    if mapdl.is_local:
        pth = os.path.join(mapdl.directory, file_)
        assert not os.path.exists(pth)
    else:
        assert file_ not in mapdl.list_files()

    load_file(mapdl, file_path)

    # File is in both, the python working directory and MAPDL directory
    assert os.path.exists(file_path)

    if mapdl.is_local:
        pth = os.path.join(mapdl.directory, file_)
        assert os.path.exists(pth)

        with open(os.path.join(mapdl.directory, file_), "r") as fid:
            assert "empty" in fid.read()

    else:
        assert file_ in mapdl.list_files()
        mapdl.download(file_)
        assert os.path.exists(file_)

        with open(os.path.join(file_), "r") as fid:
            assert "empty" in fid.read()

    with pytest.warns(UserWarning, match=f"The file '{file_}' is present in both,"):
        load_file(mapdl, file_path)

    # checking the overwriting with local
    # Changing local file first
    with open(file_path, "w") as fid:
        fid.write("not that empty")

    load_file(mapdl, file_path, priority_mapdl_file=False)

    if mapdl.is_local:
        file_name__ = os.path.join(mapdl.directory, file_)
        with open(file_name__, "r") as fid:
            assert "not that empty" in fid.read()
        os.remove(file_name__)
    else:
        mapdl.download(file_)
        with open(os.path.join(file_), "r") as fid:
            assert "empty" in fid.read()
        os.remove(file_)

    # File is in the MAPDL working directory
    try:
        os.remove(file_path)  # removing local file
    except FileNotFoundError:
        pass
    assert not os.path.exists(file_path)

    mapdl.slashdelete(file_)
    assert file_ not in mapdl.list_files()


def test_requires_package_decorator():
    class myClass:
        @requires_package("numpy")
        def myfun(self):
            return True

        @property
        @requires_package("numpy")
        def myfun2(self):
            return True

        @property
        @requires_package("nuuumpy")
        def myotherfun(self):
            return False

        @property
        @requires_package("nuuumpy", softerror=True)
        def myotherfun2(self):
            return False

    myclass = myClass()

    assert myclass.myfun()
    assert myclass.myfun2

    with pytest.raises(ModuleNotFoundError):
        assert myclass.myotherfun

    with pytest.warns(UserWarning):
        assert myclass.myotherfun2 is None


@pytest.mark.parametrize(
    "routine", ["prep7", "PREP7", "/PREP7", "begin level", "BEGIN LEVEL"]
)
def test_check_valid_routine(routine):
    assert check_valid_routine(routine)


@pytest.mark.parametrize("routine", ["invalid", "invalid routine", "prep78"])
def test_check_valid_routine_invalid(routine):
    with pytest.raises(ValueError, match="Invalid routine"):
        check_valid_routine(routine)


@requires("local")
def test_create_temp_dir():

    path = create_temp_dir()

    path = pathlib.Path(path)
    parent = path.parent
    dir_ = path.parts[-1]

    assert str(path) != create_temp_dir(parent, dir_)
