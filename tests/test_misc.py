"""Small or misc tests that don't fit in other test modules"""
import pytest
from pyvista.plotting import system_supports_plotting

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core.misc import (
    check_valid_ip,
    check_valid_port,
    check_valid_start_instance,
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


def test_plain_report():
    from ansys.mapdl.core.misc import Plain_Report

    core = ["numpy", "ansys.mapdl.reader"]
    optional = ["pyvista", "tqdm"]
    additional = ["scipy", "ger"]

    report = Plain_Report(core=core, optional=optional, additional=additional)
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
