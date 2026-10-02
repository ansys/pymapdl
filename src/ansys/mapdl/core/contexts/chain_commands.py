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

"""Chained-command context manager."""

import weakref

MAX_COMMAND_LENGTH = 600  # actual is 640, but seems to fail above 620


class _ChainCommandsContext:
    """Store MAPDL commands and send one chained command."""

    def __init__(self, parent):
        self._parent = weakref.ref(parent)
        self._previous_store_commands = False
        self._stored_commands_len = 0

    def __enter__(self):
        parent = self._parent()
        parent._log.debug("Entering chained command mode")
        self._previous_store_commands = parent._store_commands
        self._stored_commands_len = len(parent._stored_commands)
        parent._store_commands = True

    def __exit__(self, *args):
        parent = self._parent()
        parent._log.debug("Exiting chained command mode")
        try:
            if args[0] is not None:
                parent._stored_commands = parent._stored_commands[
                    : self._stored_commands_len
                ]
            elif not self._previous_store_commands:
                self._send_stored(parent)
        finally:
            parent._store_commands = self._previous_store_commands

    @staticmethod
    def _send_stored(parent):
        """Send a series of commands to MAPDL."""
        size = 0
        chained_commands = []
        chunk = []
        for command in parent._stored_commands:
            command_size = len(command) + 1
            if command_size + size > MAX_COMMAND_LENGTH:
                chained_commands.append("$".join(chunk))
                chunk = [command]
                size = 0
            else:
                chunk.append(command)
                size += command_size

        chained_commands.append("$".join(chunk))
        parent._stored_commands = []

        responses = [parent._run(command) for command in chained_commands]
        parent._response = "\n".join(responses)
