"""Small or misc tests that don't fit in other test modules"""
import inspect
import os

import numpy as np
import pytest
from pyvista.plotting import system_supports_plotting

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_start_instance,
    get_ansys_bin,
    last_created,
    load_file,
    no_return,
    requires_package,
    run_as_prep7,
)


def test_report():
    report = pymapdl.Report(gpu=system_supports_plotting())
    assert "PyAnsys Software and Environment Report" in str(report)


@pytest.mark.parametrize(
    "ip",
    [
        "localhost",
        "LOCALhost",
        "192.1.1.1",
        "127.0.0.01",
        pytest.param("asdf", marks=pytest.mark.xfail),
        pytest.param("300.2.2.2", marks=pytest.mark.xfail),
    ],
)
def test_check_valid_ip(ip):
    check_valid_ip(ip)


@pytest.mark.parametrize(
    "port",
    [
        5000,
        50053,
        10000,
        pytest.param("asdf", marks=pytest.mark.xfail),
        pytest.param("2323", marks=pytest.mark.xfail),
        pytest.param(1, marks=pytest.mark.xfail),
        pytest.param(1e9, marks=pytest.mark.xfail),
    ],
)
def test_check_valid_port(port):
    check_valid_port(port)


@pytest.mark.parametrize(
    "start_instance",
    [
        "true",
        "TRue",
        "False",
        True,
        False,
        pytest.param("asdf", marks=pytest.mark.xfail),
        pytest.param("2323", marks=pytest.mark.xfail),
        pytest.param(1, marks=pytest.mark.xfail),
        pytest.param(1e9, marks=pytest.mark.xfail),
    ],
)
def test_check_valid_start_instance(start_instance):
    check_valid_start_instance(start_instance)


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


def test_get_ansys_bin(mapdl):
    rver = mapdl.__str__().splitlines()[1].split(":")[1].strip().replace(".", "")
    assert isinstance(get_ansys_bin(rver), str)


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

    assert not info.stitles
    stitles = ["asfd", "qwer", "zxcv", "jkl"]
    info.stitles = "\n".join(stitles)

    assert stitles == info.stitles

    stitles = stitles[::-1]

    info.stitles = stitles
    assert stitles == info.stitles

    info.stitles = None
    assert not info.stitles


@pytest.mark.parametrize("file_", ["dummy.dumdum", "dumdum.dummy"])
def test_load_file_local(mapdl, tmpdir, file_):
    """Checking 'load_file' function.

    In CICD it seems we cannot write to the root folder '/'.
    Hence we cannot really test the files are being uploaded.
    So the assert in the '/' directory are commented.
    """
    old_state = mapdl._local
    mapdl._local = True

    if file_ == "dumdum.dummy":
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
    if mapdl.directory != "/":
        assert not os.path.exists(os.path.join(mapdl.directory, file_))

    load_file(mapdl, file_path)

    # File is in both, the python working directory and MAPDL directory
    assert os.path.exists(file_path)

    if mapdl.directory != "/":
        assert os.path.exists(os.path.join(mapdl.directory, file_))

        with pytest.warns(UserWarning, match=f"The file '{file_}' is present in both,"):
            load_file(mapdl, file_path)

        with open(os.path.join(mapdl.directory, file_), "r") as fid:
            assert "empty" in fid.read()

    # checking the overwriting with local
    # Changing local file first
    with open(file_path, "w") as fid:
        fid.write("not that empty")

    load_file(mapdl, file_path, priority_mapdl_file=False)

    if mapdl.directory != "/":
        with open(os.path.join(mapdl.directory, file_), "r") as fid:
            assert "not that empty" in fid.read()

    # File is in the MAPDL working directory
    os.remove(file_path)  # removing local file

    assert not os.path.exists(file_path)

    if mapdl.directory != "/":
        assert os.path.exists(os.path.join(mapdl.directory, file_))

        load_file(mapdl, file_path)

    mapdl._local = old_state
    if mapdl.directory != "/":
        os.remove(os.path.join(mapdl.directory, file_))


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
    _rep_str = rep_str.replace("Package not found", "", 1)
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
