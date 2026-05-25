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

import re
from warnings import warn
import weakref

from ansys.mapdl.core import Mapdl
from ansys.mapdl.core.errors import PluginError, PluginLoadError, PluginUnloadError
from ansys.mapdl.core.logging import Logger


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
    """
    ANSYS MAPDL Plugin Manager.

    Examples
    --------
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> plugins = mapdl.plugins

    Load a plugin in the MAPDL Session
    """

    def __init__(self, mapdl: Mapdl):
        """Initialize the class."""
        from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using an 'MapdlGrpc' object")

        self._mapdl_weakref = weakref.ref(mapdl)
        self._filename = None
        self._open = False
        self._plugins: dict[str, str] = {}

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
            for name, feature in self._plugins.items():
                lines.append(f"{name:<28} : {feature}")
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
        self._plugins[plugin_name] = feature
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
        self._plugins.pop(plugin_name, None)

        commands = self._parse_commands(response)
        self._deleter_commands(commands, plugin_name=plugin_name)

        return response

    def list(self) -> list[str]:
        """
        Lists all currently loaded plugins in MAPDL.

        Returns
        -------
        list
            A list of loaded plugin names.

        Raises
        ------
        RuntimeError
            If the plugin list cannot be retrieved.
        """

        command = "*PLUG,LIST"
        response = self._mapdl.run(command) or ""
        if response and "error" in response.lower():
            raise PluginError("Failed to retrieve the list of loaded plugins.")

        plugin_names = []
        for line in response.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            # Skip separator/header lines and informational messages
            if (
                re.match(r"^[-=*]+$", line)
                or "plugin" in line.lower()
                or "loaded" in line.lower()
            ):
                continue
            match = re.match(r"^(\S+)", line)
            if match:
                plugin_names.append(match.group(1))
        return plugin_names
