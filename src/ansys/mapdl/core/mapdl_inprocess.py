# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

from typing import Optional, Protocol

from ansys.mapdl.core.mapdl import MapdlBase


class _Backend(Protocol):
    def run_command(self) -> str: ...


class MapdlInProcess(MapdlBase):
    def __init__(self, backend: _Backend):
        super().__init__(
            loglevel="WARNING", use_vtk=False, log_apdl=None, print_com=False
        )
        self._backend = backend
        self._cleanup: bool = True
        self._name: str = "MapdlInProcess"
        self._session_id: Optional[str] = None
        self._mute: bool = False

    def _run(self, command: str, verbose: bool = False, mute: bool = False) -> str:
        if not command.strip():
            raise ValueError("Empty commands not allowed")

        if len(command) > 639:
            raise ValueError("Maximum command length mut be less than 640 characters")

        return self._backend.run_command(command, verbose, mute).strip()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name) -> None:
        self._name = name

    def _check_session_id(self) -> None:
        pass

    def __repr__(self):
        info = super().__repr__()
        return info
