# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
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
from ansys.mapdl.core.errors import (
    PluginError,
    PluginLoadError,
    PluginUnloadError,
)
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

    def test_list_after_load(self, plugins):
        """Loaded plugin appears in list() (via internal state fallback)."""
        plugins.load(TEST_PLUGIN)
        try:
            assert TEST_PLUGIN in plugins.list()
        finally:
            plugins.unload(TEST_PLUGIN)

    def test_full_cycle(self, plugins):
        """Full cycle: load → commands injected → list → unload → commands removed."""
        plugins.load(TEST_PLUGIN)

        # Injected command attribute names are tracked internally
        injected = plugins.commands(TEST_PLUGIN)
        assert len(injected) > 0, "At least one command should be injected on load"
        assert all(hasattr(plugins._mapdl, cmd) for cmd in injected)

        # Plugin appears in list() via internal tracking
        assert TEST_PLUGIN in plugins.list()

        # After unload, injected attributes are removed and plugin no longer listed
        plugins.unload(TEST_PLUGIN)
        assert all(not hasattr(plugins._mapdl, cmd) for cmd in injected)
        assert TEST_PLUGIN not in plugins.list()

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


# ============================================================
# Unit tests — internal tracking
# ============================================================


def test_list_fallback_to_internal_state(mock_plugins, mock_mapdl):
    """list() returns internally tracked names when server returns nothing."""
    from ansys.mapdl.core.plugin import _PluginInfo

    mock_plugins._plugins["PluginDPF"] = _PluginInfo(feature="")
    mock_mapdl.run.return_value = ""
    assert mock_plugins.list() == ["PluginDPF"]


def test_list_prefers_server_response(mock_plugins, mock_mapdl):
    """list() uses server response when it contains parseable plugin names."""
    from ansys.mapdl.core.plugin import _PluginInfo

    mock_plugins._plugins["PluginDPF"] = _PluginInfo(feature="")
    # A response that looks like a real *PLUG,LIST table line (no filtered keywords)
    mock_mapdl.run.return_value = "DPFServer   active"
    result = mock_plugins.list()
    assert "DPFServer" in result
    assert "PluginDPF" not in result


def test_commands_returns_registered_commands(mock_plugins, mock_mapdl):
    """commands() returns the list of attribute names injected by the plugin."""
    mock_plugins._set_commands(["CMD1", "CMD2"], plugin_name="TestPlugin")
    # _set_commands only records when plugin_name is already in _plugins
    from ansys.mapdl.core.plugin import _PluginInfo

    mock_plugins._plugins["TestPlugin"] = _PluginInfo(
        feature="", commands=["CMD1", "CMD2"]
    )
    assert mock_plugins.commands("TestPlugin") == ["CMD1", "CMD2"]


def test_commands_raises_for_unknown_plugin(mock_plugins):
    """commands() raises KeyError for a plugin that is not loaded."""
    with pytest.raises(KeyError, match="Unknown"):
        mock_plugins.commands("Unknown")


def test_commands_updated_after_load(mock_plugins, mock_mapdl):
    """After load(), _plugins records the injected command names."""
    from ansys.mapdl.core.plugin import _PluginInfo

    response = "New command [MYCMD] registered"
    mock_mapdl.run.return_value = response
    # Seed _plugins so _set_commands can append to it
    mock_plugins._plugins["TestPlugin"] = _PluginInfo(feature="")
    mock_plugins._load_commands(response, plugin_name="TestPlugin")
    assert "MYCMD" in mock_plugins.commands("TestPlugin")


def test_commands_cleared_after_deleter(mock_plugins, mock_mapdl):
    """After _deleter_commands, removed commands no longer appear in commands()."""
    from ansys.mapdl.core.plugin import _PluginInfo

    mock_plugins._plugins["TestPlugin"] = _PluginInfo(feature="", commands=["CMD1"])
    mock_mapdl.CMD1 = "something"  # make hasattr return True
    mock_plugins._deleter_commands(["CMD1"], plugin_name="TestPlugin")
    assert mock_plugins.commands("TestPlugin") == []


def test_str_shows_command_count(mock_plugins):
    """__str__ shows the number of commands for each loaded plugin."""
    from ansys.mapdl.core.plugin import _PluginInfo

    mock_plugins._plugins["PluginDPF"] = _PluginInfo(
        feature="", commands=["CMD1", "CMD2"]
    )
    output = str(mock_plugins)
    assert "2 commands" in output
    assert "PluginDPF" in output
