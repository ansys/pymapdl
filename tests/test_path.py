import pytest


def test_path_without_spaces(mapdl, path_tests):
    resp = mapdl.cwd(path_tests.path_without_spaces)
    assert 'WARNING' not in resp


def test_path_with_spaces(mapdl, path_tests):
    resp = mapdl.cwd(path_tests.path_with_spaces)
    assert 'WARNING' not in resp


def test_path_with_single_quote(mapdl, path_tests):
    with pytest.raises(RuntimeError):
        resp = mapdl.cwd(path_tests.path_with_single_quote)
        assert 'WARNING' not in resp
