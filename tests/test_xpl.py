"""Test xpl functionality"""
import numpy as np
import pytest

# skip entire module unless HAS_GRPC
pytestmark = pytest.mark.skip_grpc


@pytest.fixture(scope="function")
def xpl(mapdl, cube_solve):
    xpl = mapdl.xpl
    xpl.open("file.full")
    return xpl


def test_close(xpl):
    xpl.close()
    with pytest.raises(RuntimeError):
        xpl.list()


def test_xpl_str(xpl):
    assert "file.full" in str(xpl)


def test_read_int32(xpl):
    vec = xpl.read("MASS")
    arr = vec.asarray()
    assert arr.size
    assert arr.dtype == np.int32


def test_read_double(xpl):
    vec = xpl.read("DIAGK")
    arr = vec.asarray()
    assert arr.size
    assert arr.dtype == np.double


def test_save(xpl):
    xpl.save()
    with pytest.raises(RuntimeError):
        xpl.list()


# @pytest.mark.skipif(no_scheduler, reason='Cannot create instance outside of vnet')
def test_copy(mapdl, xpl):
    filename = "tmpfile.full"
    xpl.copy(filename)
    assert filename in mapdl.list_files()


def test_list(xpl):
    assert "::FULL::" in xpl.list(1)


def test_help(xpl):
    assert "SAVE" in xpl.help()


def test_step_where(xpl):
    xpl.step("MASS")
    assert "FULL::MASS" in xpl.where()

    with pytest.raises(RuntimeError):
        xpl.step("notarecord")


def test_info(xpl):
    assert "Record Size" in xpl.info("NGPH")


def test_print(xpl):
    assert "10" in xpl.print("MASS")


def test_json(xpl):
    json_out = xpl.json()
    assert json_out["name"] == "FULL"
    assert "children" in json_out


def test_up(xpl):
    xpl.step("MASS")
    xpl.up()
    assert "Current Location : FULL" in xpl.where()

    xpl.up("TOP")
    assert "Current Location : FULL" in xpl.where()


def test_goto(xpl):
    xpl.goto("MASS")
    assert "Current Location : FULL::MASS" in xpl.where()
