# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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
import inspect
import os
import pathlib

import numpy as np
import pytest

from conftest import has_dependency, requires

if has_dependency("pyvista"):
    from pyvista.plotting import system_supports_plotting

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_routine,
    create_temp_dir,
    last_created,
    load_file,
    no_return,
    requires_package,
    run_as_prep7,
)


@requires("pyvista")
def test_report():
    report = pymapdl.Report(
        additional=["matplotlib", "pyvista", "pyiges", "tqdm"],
        gpu=system_supports_plotting(),
    )
    assert "PyAnsys Software and Environment Report" in str(report)

    # Check that when adding additional (repeated) packages, they appear only once
    assert str(report).count("pyvista") == 1


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

    @run_as_prep7
    def fun(
        mapdl,
    ):  # This function is for mapdl methods, hence we have to pass the MAPDL instance somehow.
        mapdl.k("", 1, 1, 1)

    fun(mapdl)
    assert "POST1" in mapdl.parameters.routine
    last_keypoint = np.array(mapdl.klist().splitlines()[-1].split(), dtype=float)[0:4]
    assert np.allclose(last_keypoint, np.array([1, 1, 1, 1]))


def test_no_return(mapdl, cleared):
    mapdl.prep7()

    @no_return
    def fun(
        mapdl,
    ):  # This function is for mapdl methods, hence we have to pass the MAPDL instance somehow.
        mapdl.k("", 1, 1, 1)

    assert fun(mapdl) is None
    last_keypoint = np.array(mapdl.klist().splitlines()[-1].split(), dtype=float)[0:4]
    assert np.allclose(last_keypoint, np.array([1, 1, 1, 1]))


def test_mapdl_info(mapdl, capfd):
    info = mapdl.info
    for attr, value in inspect.getmembers(info):
        if not attr.startswith("_") and attr not in ["title", "stitles"]:
            assert isinstance(value, str)

            with pytest.raises(AttributeError):
                setattr(info, attr, "any_value")

    assert "PyMAPDL" in mapdl.info.__repr__()
    out = info.__str__()

    assert "ansys" in out.lower()
    assert "Product" in out
    assert "MAPDL Version" in out
    assert "UPDATE" in out


def test_info_title(mapdl):
    title = "this is my title"
    mapdl.info.title = title
    assert title == mapdl.info.title


def test_info_stitle(mapdl):
    info = mapdl.info

    assert all([not each for each in info.stitles])
    stitles = ["asfd", "qwer", "zxcv", "jkl"]
    info.stitles = "\n".join(stitles)

    assert stitles == info.stitles

    stitles = stitles[::-1]

    info.stitles = stitles
    assert stitles == info.stitles

    info.stitles = None
    assert all([not each for each in info.stitles])


@pytest.mark.parametrize("file_", ["dummy.dumdum", "dumdum.dummy"])
def test_load_file_local(mapdl, tmpdir, file_):
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


def test_plain_report():
    from ansys.mapdl.core.misc import Plain_Report

    core = ["numpy", "ansys.mapdl.reader"]
    optional = ["pyvista", "tqdm"]
    additional = ["scipy", "ger"]

    report = Plain_Report(core=core, optional=optional, additional=additional, gpu=True)
    rep_str = report.__repr__()

    for each in core + optional + additional:
        assert each in rep_str

    # There should be only one package not found ("ger")
    assert "Package not found" in rep_str
    not_found_packages = 1

    # Plus the not additional packages
    if not has_dependency("pyvista"):
        not_found_packages += 1
    if not has_dependency("tqdm"):
        not_found_packages += 1
    if not has_dependency("ansys.mapdl.reader"):
        not_found_packages += 1
    if not has_dependency("scipy"):
        not_found_packages += 1
    if not has_dependency("pexpect"):
        not_found_packages += 1

    _rep_str = rep_str.replace("Package not found", "", not_found_packages)
    assert "Package not found" not in _rep_str

    assert "\n" in rep_str
    assert len(rep_str.splitlines()) > 3

    assert "Core packages" in rep_str
    assert "Optional packages" in rep_str
    assert "Additional packages" in rep_str

    # Plain report should not represent GPU details evenif asked for
    assert "GPU Details" not in rep_str


def test_plain_report_no_options():
    from ansys.mapdl.core.misc import Plain_Report

    core = ["numpy", "ansys.mapdl.reader"]

    report = Plain_Report(core=core)
    rep_str = report.__repr__()

    for each in core:
        assert each in rep_str

    assert "\n" in rep_str
    assert len(rep_str.splitlines()) > 3

    assert "Core packages" in rep_str
    assert "Optional packages" not in rep_str
    assert "Additional packages" not in rep_str


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


def test_check_valid_routine():
    assert check_valid_routine("prep7")
    assert check_valid_routine("PREP7")
    assert check_valid_routine("begin level")
    with pytest.raises(ValueError, match="Invalid routine"):
        check_valid_routine("invalid")


@requires("local")
def test_create_temp_dir():

    path = create_temp_dir()

    path = pathlib.Path(path)
    parent = path.parent
    dir_ = path.parts[-1]

    assert str(path) != create_temp_dir(parent, dir)
