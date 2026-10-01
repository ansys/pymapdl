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


"""Shared constants for the MAPDL core mixins."""

from enum import Enum
from typing import Literal

MAX_PARAM_CHARS = 32


SESSION_ID_NAME = "__PYMAPDL_SESSION_ID__"

_PERMITTED_ERRORS = [
    r"(\*\*\* ERROR \*\*\*).*(?:[\r\n]+.*)+highly distorted.",
    r"(\*\*\* ERROR \*\*\*).*[\r\n]+.*is turning inside out.",
    r"(\*\*\* ERROR \*\*\*).*[\r\n]+.*The distributed memory parallel solution does not support KRYLOV method",
]






VWRITE_MWRITE_REPLACEMENT = """
Cannot use *VWRITE/*MWRITE directly as a command in MAPDL
service mode.  Instead, run it as ``non_interactive``.

For example, in the *VWRITE case:

with self.non_interactive:
    self.vwrite('%s(1)' % parm_name)
    self.run('(F20.12)')
"""


INVAL_COMMANDS = {
    "*VWR": VWRITE_MWRITE_REPLACEMENT,
    "*MWR": VWRITE_MWRITE_REPLACEMENT,
    "*CFO": "Run CFOPEN as ``non_interactive``",
    "*CRE": "Create a function within python or run as non_interactive",
    "*END": "Create a function within python or run as non_interactive",
    "/EOF": "Unsupported command.  Use ``exit`` to stop the server.",
    "*ASK": "Unsupported command.  Use python ``input`` instead.",
    "*IF": "Use a python ``if`` or run as non_interactive",
    "CMAT": "Run `CMAT` as ``non_interactive``.",
    "*REP": "Run '*REPEAT' in ``non_interactive``.",
    "LSRE": "Run 'LSREAD' in ``non_interactive``.",
}


INVAL_COMMANDS_SILENT = {
    "/NOPR": "Suppressing console output is not recommended, use ``Mute`` parameter instead. This command is disabled in interactive mode."
}





VALID_SELECTION_TYPE_TP = Literal["S", "R", "A", "U"]


VALID_SELECTION_ENTITY_TP = Literal["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE"]


GUI_FONT_SIZE = 15




class STATUS(str, Enum):
    EXITED = "exited"
    EXITING = "exiting"
    RUNNING = "running"
