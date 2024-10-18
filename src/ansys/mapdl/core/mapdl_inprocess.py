# Copyright (C) 2016 - 2024 ANSYS, Inc. and/or its affiliates.
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

from typing import Protocol

from ansys.mapdl.core.mapdl import MapdlBase


class _Backend(Protocol):
    def run_command(self, command: str, verbose: bool, mute: bool) -> str: ...

    def input_file(
        self,
        filename: str,
        extension: str,
        directory: str,
        line: int,
        log: int,
        mute: bool,
    ) -> str: ...

    def exit(self) -> None: ...


class MapdlInProcess(MapdlBase):
    def __init__(self, in_process_backend: _Backend):
        super().__init__(
            loglevel="WARNING", use_vtk=False, log_apdl=None, print_com=False
        )
        self._in_process_backend = in_process_backend
        self._cleanup: bool = True

    def _run(self, command: str, verbose: bool = False, mute: bool = False) -> str:
        if not command.strip():
            raise ValueError("Empty commands not allowed")

        if len(command) > 639:
            raise ValueError("Maximum command length mut be less than 640 characters")

        return self._in_process_backend.run_command(command, verbose, mute).strip()

    def input(
        self,
        fname: str = "",
        ext: str = "",
        dir_: str = "",
        line: str = "",
        log: str = "",
        mute: bool = False,
        **_,
    ):
        return self._in_process_backend.input_file(
            fname, ext, dir_, int(line or 0), int(log or 0), mute
        )

    def exit(self) -> None:
        self._in_process_backend.exit()

    @MapdlBase.name.getter
    def name(self) -> str:
        return "MapdlInProcess"
