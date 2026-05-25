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

"""Contains the ansPlugin class."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import List
from warnings import warn
import weakref

from ansys.mapdl.core import Mapdl
from ansys.mapdl.core.errors import PluginError, PluginLoadError, PluginUnloadError
from ansys.mapdl.core.logging import Logger


@dataclass
class _PluginInfo:
    """Internal record for a loaded plugin.

    Parameters
    ----------
    feature : str
        Feature string passed to ``*PLUG,LOAD``.
    commands : list[str]
        Transformed attribute names (``*`` → ``star``, ``/`` → ``slash``)
        that were injected on the MAPDL instance when the plugin was loaded.
    """

    feature: str
    commands: list[str] = field(default_factory=list)


def _make_command(mapdl_instance: Mapdl, plugin_name: str, command_name: str):
    """Create a bound command function for a plugin command.

    Parameters
    ----------
    mapdl_instance : Mapdl
        The MAPDL instance to run the command on.
    plugin_name : str
        Name of the plugin that registered the command.
    command_name : str
        The MAPDL command string to run.

    Returns
    -------
    callable
        A zero-argument function (aside from ``*args``/``**kwargs``) that
        forwards its arguments to ``mapdl_instance.run``.
    """

    def command(*args, **kwargs):
        return mapdl_instance.run(command_name, *args, **kwargs)

    command.__doc__ = (
        f"Command from plugin {plugin_name}: {command_name}.\n"
        "Use this plugin documentation to understand the command and its parameters.\n\n"
        "Automatically generated docstring by ansPlugin."
    )
    command.__name__ = command_name
    return command


class ansPlugin:
    """MAPDL plugin manager.

    Provides an interface for loading, inspecting, and unloading MAPDL
    plugins at runtime. Access it through the ``plugins`` property on a
    :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` instance.

    .. note::
       Plugin support requires MAPDL 25.2 or later. Plugin tracking is
       session-scoped: if the Python process reconnects to an
       already-running MAPDL instance, ``list()`` returns an empty list
       until the server-side ``*PLUG,LIST`` response is available.

    Examples
    --------
    Create a MAPDL instance and access the plugin manager.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> plugins = mapdl.plugins

    Load a plugin and inspect the commands it registers.

    >>> plugins.load("my_plugin", feature="advanced")
    >>> plugins.list()
    ['my_plugin']
    >>> plugins.commands("my_plugin")
    ['my_command', 'another_command']

    Print a summary table of all loaded plugins.

    >>> print(plugins)
    MAPDL Plugins
    ----------------
    my_plugin                    : advanced  [2 commands]

    Unload the plugin and confirm it is no longer listed.

    >>> plugins.unload("my_plugin")
    >>> plugins.list()
    []
    """

    def __init__(self, mapdl: Mapdl):
        """Initialize the class."""
        from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using an 'MapdlGrpc' object")

        self._mapdl_weakref = weakref.ref(mapdl)
        self._filename = None
        self._open = False
        self._plugins: dict[str, _PluginInfo] = {}

    @property
    def _mapdl(self) -> Mapdl:
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    @property
    def _log(self) -> Logger:
        """Return the logger from the MAPDL instance."""
        return self._mapdl._log

    def __str__(self) -> str:
        """Return a human-readable summary of loaded plugins."""
        lines = ["MAPDL Plugins", "-" * 16]
        if not self._plugins:
            lines.append("  (no plugins loaded)")
        else:
            for name, info in self._plugins.items():
                n_cmds = len(info.commands)
                cmd_label = f"{n_cmds} command{'s' if n_cmds != 1 else ''}"
                lines.append(
                    f"{name:<28} : {info.feature or '(default)'}  [{cmd_label}]"
                )
        return "\n".join(lines)

    def __repr__(self) -> str:
        """Return the same string representation as ``__str__``."""
        return self.__str__()

    def _parse_commands(self, response: str) -> list[str]:
        """
        Parse the response string to extract commands.

        Parameters
        ----------
        response : str
            The response string containing commands.

        Returns
        -------
        list[str]
            A list of commands extracted from the response.
        """
        return re.findall(r"New command \[(.*)\] registered", response)

    def _set_commands(self, commands: list[str], plugin_name: str = "NOT_SET") -> None:
        """
        Set commands to be executed.

        Parameters
        ----------
        commands : list[str]
            List of commands to be set.
        """
        if not commands:
            return

        mapdl = self._mapdl

        for each_command in commands:
            each_command = each_command.replace("*", "star").replace("/", "slash")

            if hasattr(mapdl, each_command):
                # We are allowing to overwrite existing commands
                warn(f"Command '{each_command}' already exists in the MAPDL instance.")

            setattr(
                mapdl, each_command, _make_command(mapdl, plugin_name, each_command)
            )
            if plugin_name in self._plugins:
                self._plugins[plugin_name].commands.append(each_command)
            self._log.info(
                f"Command '{each_command}' from plugin '{plugin_name}' set successfully."
            )

    def _deleter_commands(
        self, commands: list[str], plugin_name: str = "NOT_SET"
    ) -> None:
        """
        Delete commands from the MAPDL instance.

        Parameters
        ----------
        commands : list[str]
            List of commands to be deleted.
        """
        if not commands:
            return

        mapdl = self._mapdl

        for each_command in commands:
            each_command = each_command.replace("*", "star").replace("/", "slash")
            if hasattr(mapdl, each_command):
                delattr(mapdl, each_command)
                if plugin_name in self._plugins:
                    self._plugins[plugin_name].commands = [
                        c
                        for c in self._plugins[plugin_name].commands
                        if c != each_command
                    ]
                self._log.info(
                    f"Command '{each_command}' from '{plugin_name}' deleted successfully."
                )

    def _load_commands(self, response: str, plugin_name: str) -> None:
        """
        Load commands from the response string.

        Parameters
        ----------
        response : str
            The response string containing commands to be loaded.
        """
        if not response:
            return

        commands = self._parse_commands(response)
        if not commands:
            self._log.warning("No commands found in the response.")
            return
        self._set_commands(commands, plugin_name=plugin_name)

    def load(self, plugin_name: str, feature: str = "") -> str:
        """
        Loads a plugin into MAPDL.

        Parameters
        ----------
        plugin_name : str
            Name of the plugin to load.
        feature : str
            Feature or module to activate in the plugin.

        Raises
        ------
        PluginLoadError
            If the plugin fails to load.
        """

        command = f"*PLUG,LOAD,{plugin_name},{feature}"
        response = self._mapdl.run(command)
        if "error" in response.lower():
            raise PluginLoadError(
                f"Failed to load plugin '{plugin_name}' with feature '{feature}'."
            )
        self._log.info(
            f"Plugin '{plugin_name}' with feature '{feature}' loaded successfully."
        )
        self._plugins[plugin_name] = _PluginInfo(feature=feature)
        self._load_commands(response, plugin_name=plugin_name)
        return response

    def unload(self, plugin_name: str) -> str:
        """
        Unloads a plugin from MAPDL.

        Parameters
        ----------
        plugin_name : str
            Name of the plugin to unload.

        Raises
        ------
        PluginUnloadError
            If the plugin fails to unload.
        """

        command = f"*PLUG,UNLOAD,{plugin_name}"
        response = self._mapdl.run(command)

        if not response:
            return ""

        if "error" in response.lower():
            raise PluginUnloadError(f"Failed to unload plugin '{plugin_name}'.")

        self._log.info(f"Plugin '{plugin_name}' unloaded successfully.")

        # Use the internally tracked command list for cleanup — the unload
        # response uses a different pattern ("command [...] removed") than the
        # load response ("New command [...] registered"), so _parse_commands
        # would not find anything here.
        if plugin_name in self._plugins:
            tracked = list(self._plugins[plugin_name].commands)
            self._plugins.pop(plugin_name, None)
            self._deleter_commands(tracked, plugin_name=plugin_name)
        else:
            self._plugins.pop(plugin_name, None)

        return response

    def list(self) -> list[str]:
        """List all currently loaded plugins.

        Attempts to query MAPDL via ``*PLUG,LIST``. Falls back to the
        internal tracking state when the server returns no output (which is
        the case for MAPDL releases prior to the server-side fix).

        .. note::
           Internal tracking is session-scoped. If the Python process
           reconnects to an already-running MAPDL instance that has plugins
           loaded, this method will return an empty list until
           server-side ``*PLUG,LIST`` parsing is available.

        Returns
        -------
        list[str]
            Names of the loaded plugins.

        Raises
        ------
        PluginError
            If MAPDL explicitly reports an error retrieving the plugin list.
        """
        response = self._mapdl.run("*PLUG,LIST") or ""
        if response and "error" in response.lower():
            raise PluginError("Failed to retrieve the list of loaded plugins.")

        # Try to extract names from the server response
        server_names = []
        for line in response.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Skip separator lines and MAPDL informational lines
            # (e.g. "*PLUG command : Open The lib..." or " : continuation...")
            if re.match(r"^[-=*]+$", line) or re.match(
                r"(\*PLUG\s+command|\s*:|\s*>>)", line, re.IGNORECASE
            ):
                continue
            match = re.match(r"^(\S+)", line)
            if match:
                server_names.append(match.group(1))

        if server_names:
            return server_names

        # Fall back to internal state when server returns nothing
        return list(self._plugins.keys())

    def commands(self, plugin_name: str) -> List[str]:
        """Return the attribute names registered by a plugin.

        These are the command names (after ``*`` → ``star`` / ``/`` →
        ``slash`` transformation) that were injected as attributes on the
        MAPDL instance when *plugin_name* was loaded.

        Parameters
        ----------
        plugin_name : str
            Name of the plugin whose commands are requested.

        Returns
        -------
        list[str]
            Attribute names registered by the plugin.

        Raises
        ------
        KeyError
            If *plugin_name* is not currently tracked as loaded.
        """
        if plugin_name not in self._plugins:
            raise KeyError(
                f"Plugin '{plugin_name}' is not loaded. "
                f"Loaded plugins: {list(self._plugins.keys())}"
            )
        return list(self._plugins[plugin_name].commands)
