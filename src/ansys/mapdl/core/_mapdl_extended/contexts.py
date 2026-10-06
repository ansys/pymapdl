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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""APDL loop contexts used by the extended MAPDL facade."""

import weakref

from ansys.mapdl.core.errors import MapdlDoLoopLimitError

MAX_DO_LOOP_LEVEL = 20


class _DoLoopContext:
    """Open and close an APDL ``*DO`` or ``*DOWHILE`` loop."""

    def __init__(self, parent, command: str, **kwargs):
        self._parent = weakref.ref(parent)
        self._command = command
        self._kwargs = kwargs
        self._non_interactive_cm = None
        self._stored_commands_len = 0

    def __enter__(self):
        mapdl = self._parent()
        if mapdl._do_loop_level >= MAX_DO_LOOP_LEVEL:
            raise MapdlDoLoopLimitError(
                "Cannot open another APDL do-loop: MAPDL only supports "
                f"{MAX_DO_LOOP_LEVEL} levels of nested '*DO'/'*DOWHILE' "
                "loops. Reduce the number of nested 'mapdl.do' or "
                "'mapdl.dowhile' context managers."
            )

        mapdl._do_loop_level += 1
        mapdl._log.debug(
            f"Entering do-loop level {mapdl._do_loop_level}: {self._command}"
        )

        if not mapdl._store_commands:
            self._non_interactive_cm = mapdl.non_interactive
            self._non_interactive_cm.__enter__()

        self._stored_commands_len = len(mapdl._stored_commands)
        mapdl.run(self._command, **self._kwargs)
        return self

    def __exit__(self, *args):
        mapdl = self._parent()
        mapdl._do_loop_level -= 1
        mapdl._log.debug(f"Exiting do-loop level {mapdl._do_loop_level + 1}")

        try:
            if args[0] is None:
                mapdl.run("*ENDDO")
            else:
                mapdl._stored_commands = mapdl._stored_commands[
                    : self._stored_commands_len
                ]
        finally:
            if self._non_interactive_cm is not None:
                self._non_interactive_cm.__exit__(*args)
