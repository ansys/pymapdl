# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

import pytest

pytestmark = pytest.mark.random_order(disabled=True)

from ansys.mapdl.core import Mapdl
from ansys.mapdl.core.plugin import ansPlugin

pytestmark = pytest.mark.random_order(disabled=True)

TEST_PLUGIN = "PluginDPF"


@pytest.fixture()
def plugins(mapdl: Mapdl) -> ansPlugin:
    if mapdl.version < 25.2:
        pytest.skip(
            "Plugin support is only for versions 25.2 and above",
            allow_module_level=True,
        )

    return mapdl.plugins


@pytest.fixture()
def dpf_load_response(plugins: ansPlugin) -> ansPlugin:
    response = plugins.load(TEST_PLUGIN)
    yield response
    plugins.unload(TEST_PLUGIN)


def test_plugin_load(plugins):
    assert plugins.load(TEST_PLUGIN) is not None


@pytest.mark.xfail(reason="Plugin unload not implemented in MAPDL yet")
def test_plugin_list(plugins, dpf_load_response):
    assert TEST_PLUGIN in plugins.list(), "Plugin should be loaded"


def test_plugin_unload(plugins):
    plugins.unload(TEST_PLUGIN)
    assert TEST_PLUGIN not in plugins.list(), "Plugin should be unloaded"


def test_parse_commands(plugins, dpf_load_response):
    commands = plugins._parse_commands(dpf_load_response)

    assert isinstance(commands, list), "Commands should be a list"
    assert len(commands) > 0, "Commands list should not be empty"
    assert "*DPF" in commands, "Expected command '*DPF' should be in the list"


def test_load_commands(plugins, dpf_load_response):
    commands = plugins._parse_commands(dpf_load_response)
    assert isinstance(commands, list), "Commands should be a list"
    assert len(commands) > 0, "Commands list should not be empty"

    for command in commands:
        assert hasattr(plugins._mapdl, command)


def test_deleter_commands(plugins, dpf_load_response):
    commands = plugins._parse_commands(dpf_load_response)
    assert isinstance(commands, list), "Commands should be a list"
    assert len(commands) > 0, "Commands list should not be empty"

    plugins._deleter_commands(commands, TEST_PLUGIN)

    for command in commands:
        assert not hasattr(
            plugins._mapdl, command
        ), f"Command {command} should be deleted"
