import pytest

from conftest import has_dependency

if not has_dependency("pyvista"):
    pytest.skip(allow_module_level=True)

from ansys.mapdl.core.theme import MapdlTheme, _apply_default_theme


def test_load_theme():
    MapdlTheme()


def test_apply_default_theme():
    _apply_default_theme()
