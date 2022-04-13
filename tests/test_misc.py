"""Small or misc tests that don't fit in other test modules"""
import numpy as np
import pytest
from pyvista.plotting import system_supports_plotting

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_start_instance,
    last_created,
    run_as_prep7,
)


def test_report():
    report = pymapdl.Report(gpu=system_supports_plotting())
    assert "PyMAPDL Software and Environment Report" in str(report)


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
