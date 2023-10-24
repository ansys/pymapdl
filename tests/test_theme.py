import pytest

from conftest import TESTING_MINIMAL

if TESTING_MINIMAL:
    pytest.skip(allow_module_level=True)

from ansys.mapdl.core.theme import MapdlTheme, _apply_default_theme


def test_load_theme():
    MapdlTheme()


def test_apply_default_theme():
    _apply_default_theme()
