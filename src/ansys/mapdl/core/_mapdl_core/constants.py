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
import re
from typing import Literal, TypeAlias

MAX_PARAM_CHARS = 32


SESSION_ID_NAME = "__PYMAPDL_SESSION_ID__"


DEBUG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


VALID_DEVICES = ["PNG", "TIFF", "VRML", "TERM", "CLOSE"]


VALID_DEVICES_LITERAL: TypeAlias = Literal["PNG", "TIFF", "VRML", "TERM", "CLOSE"]


VALID_FILE_TYPE_FOR_PLOT = VALID_DEVICES.copy()
VALID_FILE_TYPE_FOR_PLOT.remove("CLOSE")


VALID_FILE_TYPE_FOR_PLOT_LITERAL: TypeAlias = Literal["PNG", "TIFF", "VRML", "TERM"]


_PERMITTED_ERRORS = [
    r"(\*\*\* ERROR \*\*\*).*(?:[\r\n]+.*)+highly distorted.",
    r"(\*\*\* ERROR \*\*\*).*[\r\n]+.*is turning inside out.",
    r"(\*\*\* ERROR \*\*\*).*[\r\n]+.*The distributed memory parallel solution does not support KRYLOV method",
]


_TMP_COMP = {
    "KP": "cmp_kp",
    "LINE": "cmp_line",
    "AREA": "cmp_area",
    "VOLU": "cmp_volu",
    "NODE": "cmp_node",
    "ELEM": "cmp_elem",
}


ENTITIES_TO_SELECTION_MAPPING = {
    "KP": "ksel",
    "LINE": "lsel",
    "AREA": "asel",
    "VOLU": "vsel",
    "NODE": "nsel",
    "ELEM": "esel",
}


PNG_IS_WRITTEN_TO_FILE = re.compile(
    "WRITTEN TO FILE"
)  # getting the file name is buggy.


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


PLOT_COMMANDS = [
    "APLO",
    "EPLO",
    "KPLO",
    "LPLO",
    "NPLO",
    "PLES",
    "PLNS",
    "PLVA",
    "PSDG",
    "SECP",
    "SPGR",
    "TBPL",
    "VPLO",
]


MAX_COMMAND_LENGTH = 600  # actual is 640, but seems to fail above 620


VALID_SELECTION_TYPE_TP = Literal["S", "R", "A", "U"]


VALID_SELECTION_ENTITY_TP = Literal["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE"]


GUI_FONT_SIZE = 15


LOG_APDL_DEFAULT_FILE_NAME = "apdl.log"


_ALLOWED_START_PARM = [
    "additional_switches",
    "check_parameter_names",
    "env_vars",
    "exec_file",
    "finish_job_on_exit",
    "hostname",
    "ip",
    "jobid",
    "jobname",
    "launch_on_hpc",
    "launched",
    "mode",
    "nproc",
    "override",
    "port",
    "print_com",
    "process",
    "ram",
    "run_location",
    "start_instance",
    "start_timeout",
    "timeout",
    "use_reader_backend",
    # Transport-related parameters
    "transport_mode",
    "uds_dir",
    "certs_dir",
]


class STATUS(str, Enum):
    EXITED = "exited"
    EXITING = "exiting"
    RUNNING = "running"
