# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Test the plugin implementation"""

from unittest.mock import MagicMock
import warnings
import weakref

import pytest

from ansys.mapdl.core import Mapdl
from ansys.mapdl.core.errors import PluginError, PluginLoadError, PluginUnloadError
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from ansys.mapdl.core.plugin import ansPlugin
from conftest import requires

pytestmark = pytest.mark.random_order(disabled=True)

TEST_PLUGIN = "PluginDPF"


# ============================================================
# Integration tests — require a live MAPDL ≥ 25.2 via gRPC
# ============================================================


@pytest.fixture(scope="class")
def plugins(mapdl: Mapdl) -> ansPlugin:
    if mapdl.version < 25.2:
        pytest.skip("Plugin support requires MAPDL ≥ 25.2")
    return mapdl.plugins


@requires("grpc")
class TestPluginIntegration:
    """Full plugin lifecycle tests against a live MAPDL instance."""

    def test_load(self, plugins):
        """Loading a plugin returns a non-empty response."""
        response = plugins.load(TEST_PLUGIN)
        assert response is not None and response != ""

    @pytest.mark.xfail(reason="*PLUG,LIST output not yet captured by PyMAPDL")
    def test_list_after_load(self, plugins):
        """Loaded plugin appears in list()."""
        plugins.load(TEST_PLUGIN)
        try:
            assert TEST_PLUGIN in plugins.list()
        finally:
            plugins.unload(TEST_PLUGIN)

    def test_full_cycle(self, plugins):
        """Full cycle: load → commands injected → list → unload → commands removed."""
        response = plugins.load(TEST_PLUGIN)

        # Commands parsed from load response are injected on the MAPDL instance
        commands = plugins._parse_commands(response)
        assert isinstance(commands, list)
        assert len(commands) > 0, "At least one command should be injected on load"
        assert all(hasattr(plugins._mapdl, cmd) for cmd in commands)

        # After unload, injected commands are removed
        plugins.unload(TEST_PLUGIN)
        assert all(not hasattr(plugins._mapdl, cmd) for cmd in commands)

    def test_unload_already_unloaded(self, plugins):
        """Unloading a plugin that is not loaded returns an empty string."""
        plugins.load(TEST_PLUGIN)
        plugins.unload(TEST_PLUGIN)
        assert plugins.unload(TEST_PLUGIN) == ""

    def test_str_shows_loaded_plugin(self, plugins):
        """__str__ lists the plugin after it is loaded."""
        plugins.load(TEST_PLUGIN)
        try:
            assert TEST_PLUGIN in str(plugins)
        finally:
            plugins.unload(TEST_PLUGIN)


# ============================================================
# Unit fixtures — no MAPDL instance required
# ============================================================


@pytest.fixture()
def mock_mapdl():
    """Create a mock MapdlGrpc instance with proper hasattr/setattr/delattr behaviour."""
    mock = MagicMock(spec=MapdlGrpc)
    mock._log = MagicMock()
    return mock


@pytest.fixture()
def mock_plugins(mock_mapdl):
    """Create an ansPlugin bypassing the isinstance check in __init__."""
    plugin = object.__new__(ansPlugin)
    plugin._mapdl_weakref = weakref.ref(mock_mapdl)
    plugin._plugins = {}
    return plugin


# ============================================================
# Unit tests
# ============================================================


def test_parse_commands_empty_response(mock_plugins):
    assert mock_plugins._parse_commands("") == []


def test_parse_commands_malformed_response(mock_plugins):
    result = mock_plugins._parse_commands("This is not a valid command list")
    assert result == []


def test_parse_commands_valid_response(mock_plugins):
    response = (
        "New command [MYCOMMAND] registered\nNew command [ANOTHERCOMMAND] registered"
    )
    result = mock_plugins._parse_commands(response)
    assert result == ["MYCOMMAND", "ANOTHERCOMMAND"]


def test_set_commands_warns_on_existing(mock_plugins, mock_mapdl):
    """_set_commands warns when the (transformed) attribute already exists."""
    mock_mapdl.EXISTING_CMD = "something"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        mock_plugins._set_commands(["EXISTING_CMD"], plugin_name="TestPlugin")
    assert len(w) == 1
    assert "already exists" in str(w[0].message)


def test_set_commands_creates_callable(mock_plugins, mock_mapdl):
    """_set_commands sets a callable attribute on the MAPDL instance."""
    mock_plugins._set_commands(["NEW_CMD"], plugin_name="TestPlugin")
    assert hasattr(mock_mapdl, "NEW_CMD")
    assert callable(getattr(mock_mapdl, "NEW_CMD"))


def test_set_commands_name_transformation(mock_plugins, mock_mapdl):
    """Commands with * and / are transformed to star/slash prefixes."""
    mock_plugins._set_commands(["*STARCOMMAND"], plugin_name="TestPlugin")
    assert hasattr(mock_mapdl, "starSTARCOMMAND")


def test_deleter_commands_nonexistent(mock_plugins, mock_mapdl):
    """Deleting a non-existent command does not raise."""
    mock_plugins._deleter_commands(["NONEXISTENT_CMD"], plugin_name="TestPlugin")


def test_deleter_commands_applies_transformation(mock_plugins, mock_mapdl):
    """_deleter_commands applies the same *->star transformation as _set_commands."""
    mock_plugins._set_commands(["*TESTCMD"], plugin_name="TestPlugin")
    assert hasattr(mock_mapdl, "starTESTCMD")

    mock_plugins._deleter_commands(["*TESTCMD"], plugin_name="TestPlugin")
    assert not hasattr(mock_mapdl, "starTESTCMD")


def test_load_raises_on_error(mock_plugins, mock_mapdl):
    """load() raises PluginLoadError when MAPDL returns an error response."""
    mock_mapdl.run.return_value = "ERROR: plugin not found"
    with pytest.raises(PluginLoadError):
        mock_plugins.load("BadPlugin")


def test_unload_raises_on_error(mock_plugins, mock_mapdl):
    """unload() raises PluginUnloadError when MAPDL returns an error response."""
    mock_mapdl.run.return_value = "ERROR: plugin not loaded"
    with pytest.raises(PluginUnloadError):
        mock_plugins.unload("BadPlugin")


def test_list_raises_on_error(mock_plugins, mock_mapdl):
    """list() raises PluginError when MAPDL returns an error response."""
    mock_mapdl.run.return_value = "ERROR: cannot list plugins"
    with pytest.raises(PluginError):
        mock_plugins.list()


def test_str_representation(mock_plugins):
    """__str__ includes the 'MAPDL Plugins' header."""
    assert "MAPDL Plugins" in str(mock_plugins)
