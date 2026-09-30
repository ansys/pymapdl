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

"""Package-wide constants used by PyMAPDL core modules.

This module contains fixed configuration, lookup tables, regular expressions,
and message templates. Runtime state, type aliases, and service objects remain
in their owning modules.
"""

from datetime import datetime
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from platformdirs import user_data_dir
import psutil

# Package initialization and supported versions.
VERSION_MAP: Dict[Tuple[int, int, int], str] = {
    (0, 0, 0): "2020R2",
    (0, 3, 0): "2021R1",
    (0, 4, 0): "2021R2",
    (0, 4, 1): "2021R2",
    (0, 5, 0): "2022R1",
    (0, 5, 1): "2022R2",
}
MINIMUM_PYTHON_VERSION: Tuple[int, int] = (3, 10)
USER_DATA_PATH: str = user_data_dir(appname="ansys_mapdl_core", appauthor="Ansys")
EXAMPLES_PATH: str = os.path.join(USER_DATA_PATH, "examples")

SUPPORTED_ANSYS_VERSIONS: Dict[int, str] = {
    271: "2027R1",
    261: "2026R1",
    252: "2025R2",
    251: "2025R1",
    242: "2024R2",
    241: "2024R1",
    232: "2023R2",
    231: "2023R1",
    222: "2022R2",
    221: "2022R1",
    212: "2021R2",
    211: "2021R1",
    202: "2020R2",
    201: "2020R1",
    195: "19.5",
    194: "19.4",
    193: "19.3",
    192: "19.2",
    191: "19.1",
}

# Command parsing and output conversion.
REG_LETTERS: re.Pattern[str] = re.compile(r"[a-df-zA-DF-Z]+")
REG_FLOAT_INT: re.Pattern[str] = re.compile(
    r"[+-]?[0-9]*[.]?[0-9]*[Ee]?[+-]?[0-9]+|\s[0-9]+\s"
)
BC_REGREP: re.Pattern[str] = re.compile(
    r"^\s*([0-9]+)\s*([A-Za-z]+)"
    r"(\s+(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)"
    r"(?:\s+(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+))*)$"
)
MSG_NOT_PANDAS: str = """'Pandas' is not installed or could not be found.
Hence this command is not applicable.

You can install it using:
pip install pandas
"""
MSG_BCLISTINGOUTPUT_TO_ARRAY: str = """This command has strings values in some of its columns (such 'UX', 'FX', 'UY', 'TEMP', etc),
so it cannot be converted to Numpy Array.

Please use 'to_list' or 'to_dataframe' instead."""
GROUP_DATA_START: List[str] = ["NODE", "ELEM"]
CMD_RESULT_LISTING: List[str] = [
    "NLIN",
    "PRCI",
    "PRDI",
    "PREF",
    "PREN",
    "PRER",
    "PRES",
    "PRET",
    "PRGS",
    "PRIN",
    "PRIT",
    "PRJS",
    "PRNL",
    "PRNM",
    "PRNS",
    "PROR",
    "PRPA",
    "PRRF",
    "PRRS",
    "PRSE",
    "PRSS",
    "PRST",
    "PRVE",
    "PRXF",
    "SWLI",
]
CMD_BC_LISTING: List[str] = [
    "DKLI",
    "DLLI",
    "DALI",
    "DLIS",
    "FKLI",
    "FLIS",
    "SFLL",
    "BFKL",
    "BFLL",
    "BFAL",
]
COLNAMES_BC_LISTING: Dict[str, List[str]] = {
    "DKLI": ["KEYPOINT", "LABEL", "REAL", "IMAG", "EXP KEY"],
    "DLLI": ["LINE", "LABEL", "REAL", "IMAG", "NAREA"],
    "DALI": ["AREA", "LABEL", "REAL", "IMAG"],
    "DLIS": ["NODE", "LABEL", "REAL", "IMAG"],
    "FKLI": ["KEYPOINT", "LABEL", "REAL", "IMAG"],
    "FLIS": ["NODE", "LABEL", "REAL", "IMAG"],
    "SFLL": ["LINE", "LABEL", "VALI", "VALJ", "VAL2I", "VAL2J"],
    "BFKL": ["KEYPOINT", "LABEL", "VALUE"],
    "BFLL": ["LINE", "LABEL", "VALUE"],
    "BFAL": ["AREA", "LABEL", "VALUE"],
}
CMD_ENTITY_LISTING: List[str] = ["NLIS"]
CMD_LISTING: List[str] = CMD_ENTITY_LISTING + CMD_RESULT_LISTING
CMD_DOCSTRING_INJECTION: str = r"""
Returns
-------

str
    Str object with the command console output.

    This object also has the extra methods:
    :meth:`to_list() <ansys.mapdl.core.commands.CommandListingOutput.to_list>`,
    :meth:`to_array() <ansys.mapdl.core.commands.CommandListingOutput.to_array>` (only on listing commands) and
    :meth:`to_dataframe() <ansys.mapdl.core.commands.CommandListingOutput.to_dataframe>` (only if Pandas is installed).
    |bl|
    **NOTE**: If you use these methods, you might
    obtain a lower precision than using :class:`Mesh <ansys.mapdl.core.mesh_grpc.MeshGrpc>` methods.
    |bl|
    For more information visit :ref:`user_guide_postprocessing`.
"""
XSEL_DOCSTRING_INJECTION: str = r"""
Returns
-------

np.ndarray
    Numpy array with the ids of the selected entities.

    For more information visit :ref:`user_guide_postprocessing`.
"""
CMD_XSEL: List[str] = [
    "NSEL",
    "ESEL",
    "KSEL",
    "LSEL",
    "ASEL",
    "VSEL",
    "ESLN",
    "NSLE",
]

# Common gRPC data conversion.
DEFAULT_CHUNKSIZE: int = 256 * 1024
DEFAULT_FILE_CHUNK_SIZE: int = 1024 * 1024
ANSYS_VALUE_TYPE: Dict[int, Optional[np.typing.DTypeLike]] = {
    0: None,
    1: np.int32,
    2: np.int64,
    3: np.int16,
    4: np.float32,
    5: np.float64,
    6: np.complex64,
    7: np.complex128,
    8: np.char,
}
VGET_ENTITY_TYPES: List[str] = [
    "NODE",
    "ELEM",
    "KP",
    "LINE",
    "AREA",
    "VOLU",
    "CDSY",
    "RCON",
    "TLAB",
]
COMMON_GRPC_STRESS_TYPES: List[str] = [
    "X",
    "Y",
    "Z",
    "XY",
    "YZ",
    "XZ",
    "1",
    "2",
    "3",
    "INT",
    "EQV",
]
COMMON_GRPC_COMP_TYPE: List[str] = ["X", "Y", "Z", "SUM"]
VGET_NODE_ENTITY_TYPES: Dict[str, List[str]] = {
    "U": ["X", "Y", "Z"],
    "S": COMMON_GRPC_STRESS_TYPES,
    "EPTO": COMMON_GRPC_STRESS_TYPES,
    "EPEL": COMMON_GRPC_STRESS_TYPES,
    "EPPL": COMMON_GRPC_STRESS_TYPES,
    "EPCR": COMMON_GRPC_STRESS_TYPES,
    "EPTH": COMMON_GRPC_STRESS_TYPES,
    "EPDI": COMMON_GRPC_STRESS_TYPES,
    "EPSW": [""],
    "NL": ["SEPL", "SRAT", "HPRES", "EPEQ", "PSV", "PLWK"],
    "HS": ["X", "Y", "Z"],
    "BFE": ["TEMP"],
    "TG": COMMON_GRPC_COMP_TYPE,
    "TF": COMMON_GRPC_COMP_TYPE,
    "PG": COMMON_GRPC_COMP_TYPE,
    "EF": COMMON_GRPC_COMP_TYPE,
    "D": COMMON_GRPC_COMP_TYPE,
    "H": COMMON_GRPC_COMP_TYPE,
    "B": COMMON_GRPC_COMP_TYPE,
    "FMAG": COMMON_GRPC_COMP_TYPE,
    "NLIST": [""],
}

# Component handling.
VALID_ENTITIES: List[str] = [
    "NODE",
    "NODES",
    "ELEM",
    "ELEMS",
    "ELEMENTS",
    "VOLU",
    "AREA",
    "LINE",
    "KP",
]
SELECTOR_FUNCTION: List[str] = [
    "NSEL",
    "NSEL",
    "ESEL",
    "ESEL",
    "ESEL",
    "VSEL",
    "ASEL",
    "LSEL",
    "KSEL",
]
ENTITIES_MAPPING: Dict[str, str] = dict(zip(VALID_ENTITIES, SELECTOR_FUNCTION))
WARNING_ENTITY: str = (
    "Assuming a {default_entity} selection.\n"
    "It is recommended you use the following notation to avoid this warning:\n"
    ">>> mapdl.components['{key}'] = '{default_entity}', {value}\n"
    "Alternatively, you disable this warning using:\n"
    ">>> mapdl.components.default_entity_warning=False"
)

# APDL converter defaults and command mappings.
FORMAT_OPTIONS: Dict[str, Any] = {
    "select": "W191,W291,W293,W391,E115,E117,E122,E124,E125,E225,E231,E301,E303,F401,F403",
    "max-line-length": 100,
}
LOGLEVEL_DEFAULT: str = "WARNING"
AUTO_EXIT_DEFAULT: bool = True
LINE_ENDING_DEFAULT: Optional[str] = None
EXEC_FILE_DEFAULT: Optional[str] = None
MACROS_AS_FUNCTIONS_DEFAULT: bool = True
USE_FUNCTION_NAMES_DEFAULT: bool = True
SHOW_LOG_DEFAULT: bool = False
ADD_IMPORTS_DEFAULT: bool = True
COMMENT_SOLVE_DEFAULT: bool = False
CLEANUP_OUTPUT_DEFAULT: bool = True
HEADER_DEFAULT: bool = True
PRINT_COM_DEFAULT: bool = True
ONLY_COMMANDS_DEFAULT: bool = False
GRAPHICS_BACKEND_DEFAULT = None
CLEAR_AT_START_DEFAULT: bool = False
CHECK_PARAMETER_NAMES_DEFAULT: bool = True
COMMANDS_WITH_EMPTY_ARGS: Dict[str, Tuple[Any, ...]] = {
    "/CMA": (),
    "/NER": (),
    "/PBF": (),
    "/PMO": (),
    "ADD": (),
    "ANTY": (),
    "ASBL": (),
    "ATAN": (),
    "BCSO": (),
    "CDRE": (),
    "CLOG": (),
    "CONJ": (),
    "CORI": (),
    "DERI": (),
    "DSPO": (),
    "ENER": (),
    "ENSY": (),
    "EQSL": (),
    "ESYM": (),
    "EXP": (),
    "EXPA": (),
    "FCLI": (),
    "FILE": (),
    "FLUR": (),
    "GMAT": (),
    "IMAG": (),
    "INT1": (),
    "LARG": (),
    "LATT": (),
    "MAP": (),
    "MORP": (),
    "MPCO": (),
    "NLOG": (),
    "PLMA": (),
    "PRED": (),
    "PROD": (),
    "QRDO": (),
    "QUOT": (),
    "RACE": (),
    "RDEC": (),
    "REAL": (),
    "REME": (),
    "RPSD": (),
    "SECR": (),
    "SECW": (),
    "SESY": (),
    "SETF": (),
    "SETR": (),
    "SMAL": (),
    "SNOP": (),
    "SQRT": (),
    "SURE": (),
    "THOP": (),
    "TINT": (),
    "XFDA": (),
}
COMMANDS_TO_NOT_BE_CONVERTED: List[str] = ["CMPL"]
FORCED_MAPPING: Dict[str, str] = {"SECT": "sectype"}

# Error handling.
N_ATTEMPTS = 5
INITIAL_BACKOFF = 0.1
MULTIPLIER_BACKOFF = 2
LOCKFILE_MSG: str = """
Another ANSYS job with the same job name is already running in this
directory, or the lock file has not been deleted from an abnormally
terminated ANSYS run.

Disable this check by passing ``override=True``
"""
TYPE_MSG: str = (
    "Invalid datatype.  Must be one of the following:\n"
    + "np.int32, np.int64, or np.double"
)

# Jupyter and Krylov limits.
MAX_CPU: int = 128
MAX_MEM: int = 256
RESIDUAL_ALGORITHM: List[str] = ["l-inf", "linf", "l-1", "l1", "l-2", "l2"]

# Licensing.
LOCALHOST = "127.0.0.1"
LIC_PATH_ENVAR = "ANSYSLIC_DIR"
LIC_FILE_ENVAR = "ANSYSLMD_LICENSE_FILE"
APP_NAME = "FEAT_ANSYS"
LIC_TO_CHECK = ["mech_1"]
LICENSES = {
    "ansys": "Ansys Mechanical Enterprise",
    "meba": "Ansys Mechanical Enterprise Solver",
    "mech_2": "Ansys Mechanical Premium",
    "mech_1": "Ansys Mechanical Pro",
    "preppost": "Mechanical Enterprise PrepPost",
}
ALLOWABLE_LICENSES = list(LICENSES)

# Logging configuration.
LOG_LEVEL = logging.DEBUG
FILE_NAME = "pymapdl.log"
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
STDOUT_MSG_FORMAT = (
    "%(levelname)s - %(instance_name)s -  %(module)s - %(funcName)s - %(message)s"
)
FILE_MSG_FORMAT = STDOUT_MSG_FORMAT
DEFAULT_STDOUT_HEADER = """
LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER
NEW_SESSION_HEADER = f"""
===============================================================================
       NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
===============================================================================
"""

# Core MAPDL behavior.
MAX_PARAM_CHARS = 32
SESSION_ID_NAME = "__PYMAPDL_SESSION_ID__"
VALID_DEVICES = ["PNG", "TIFF", "VRML", "TERM", "CLOSE"]
VALID_FILE_TYPE_FOR_PLOT = ["PNG", "TIFF", "VRML", "TERM"]
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
PNG_IS_WRITTEN_TO_FILE = re.compile("WRITTEN TO FILE")
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
MAX_COMMAND_LENGTH = 600
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
    "transport_mode",
    "uds_dir",
    "certs_dir",
]

# Extended command behavior and geometry.
TMP_VAR = "__tmpvar__"
MAX_DO_LOOP_LEVEL = 20
VALID_SELECTION_TYPE = ["S", "R", "A", "U"]
VALID_SELECTION_ENTYTY = ["VOLU", "AREA", "LINE", "KP", "ELEM", "NODE"]
FLST_LOOKUP = {
    "NODE": 1,
    "ELEM": 2,
    "KP": 3,
    "LINE": 4,
    "AREA": 5,
    "VOLU": 6,
    "TRACE": 7,
    "COORD": 8,
}
VALID_TYPE_MSG = """- 'S' : Select a new set (default)
- 'R' : Reselect a set from the current set.
- 'A' : Additionally select a set and extend the current set.
- 'U' : Unselect a set from the current set.
"""
VERSION_ERROR = """
In PyMAPDL 0.66.0 and later, the new geometry module does not allow calls on
``geometry.keypoints``, ``geometry.lines``, or ```geometry.areas``.

You can activate the old API like this:
>>> mapdl.legacy_geometry = True

For more information, see `Mesh and geometry <https://mapdl.docs.pyansys.com/version/stable/user_guide/mesh_geometry.html>`_.
"""

# MAPDL gRPC behavior.
MSG_IMPORT = """There was a problem importing the ANSYS MAPDL API module `ansys-api-mapdl`.
Please make sure you have the latest updated version using:

'pip install ansys-api-mapdl' or 'pip install --upgrade ansys-api-mapdl'

If this does not solve it, please reinstall 'ansys.mapdl.core'
or contact Technical Support at 'https://github.com/ansys/pymapdl'."""
MAX_MESSAGE_LENGTH = int(os.environ.get("PYMAPDL_MAX_MESSAGE_LENGTH", 256 * 1024**2))
VAR_IR = 9
DEFAULT_TIME_STEP_STREAM = None
DEFAULT_TIME_STEP_STREAM_NT = 500
DEFAULT_TIME_STEP_STREAM_POSIX = 100
SERVICE_DEFAULT_CONFIG = {
    "methodConfig": [
        {
            "name": [{}],
            "retryPolicy": {
                "maxAttempts": 5,
                "initialBackoff": "0.01s",
                "maxBackoff": "3s",
                "backoffMultiplier": 3,
                "retryableStatusCodes": ["UNAVAILABLE", "RESOURCE_EXHAUSTED"],
            },
        }
    ]
}
PING_ABUSE_INTERVAL_S = 24
PING_ABUSE_PROBE_EVERY_N_PINGS = 3
PING_ABUSE_PROBE_INTERVAL_S = PING_ABUSE_INTERVAL_S * PING_ABUSE_PROBE_EVERY_N_PINGS
PING_ABUSE_PROBE_TIMEOUT_S = 5.0
DEFAULT_GRPC_OPTIONS = [
    ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
    ("grpc.service_config", json.dumps(SERVICE_DEFAULT_CONFIG)),
    ("grpc.keepalive_time_ms", PING_ABUSE_INTERVAL_S * 1000),
    ("grpc.keepalive_timeout_ms", 10_000),
    ("grpc.keepalive_permit_without_calls", 1),
    ("grpc.http2.min_time_between_pings_ms", PING_ABUSE_INTERVAL_S * 1000),
    ("grpc.http2.max_pings_without_data", 0),
]

# Mesh, parameter, parsing, postprocessing, and reporting data.
TMP_NODE_CM = "__NODE__"
ROUTINE_MAP = {
    0: "Begin level",
    17: "PREP7",
    21: "SOLUTION",
    31: "POST1",
    36: "POST26",
    52: "AUX2",
    53: "AUX3",
    62: "AUX12",
    65: "AUX15",
}
UNITS_MAP = {
    -1: "NONE",
    0: "USER",
    1: "SI",
    2: "CGS",
    3: "BFT",
    4: "BIN",
    5: "MKS",
    6: "MPA",
    7: "uMKS",
}
NUMERIC_CONST_PATTERN = r"""
[-+]? # optional sign
(?:
(?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
|
(?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
)
# followed by optional exponent part if desired
(?: [Ee] [+-]? \d+ ) ?
"""
NUM_PATTERN = re.compile(NUMERIC_CONST_PATTERN, re.VERBOSE)
COMPONENT_STRESS_TYPE = ["X", "Y", "Z", "XY", "YZ", "XZ"]
PRINCIPAL_TYPE = ["1", "2", "3"]
POST_STRESS_TYPES = ["X", "Y", "Z", "XY", "YZ", "XZ", "1", "2", "3", "INT", "EQV"]
POST_COMP_TYPE = ["X", "Y", "Z", "SUM"]
DISP_TYPE = ["X", "Y", "Z", "NORM", "ALL"]
ROT_TYPE = ["X", "Y", "Z", "ALL"]
ANSYS_ENV_VARS = [
    "PYMAPDL_START_INSTANCE",
    "PYMAPDL_PORT",
    "PYMAPDL_IP",
    "PYMAPDL_NPROC",
    "PYMAPDL_MAPDL_EXEC",
    "PYMAPDL_MAPDL_VERSION",
    "PYMAPDL_MAX_MESSAGE_LENGTH",
    "PYMAPDL_ON_SLURM",
    "ON_CI",
    "ON_LOCAL",
    "ON_REMOTE",
    "P_SCHEMA",
]
MYCTYPE = {
    np.int32: "I",
    np.int64: "L",
    np.single: "F",
    np.double: "D",
    np.complex64: "C",
    np.complex128: "Z",
}

# CLI constants.
CLI_DEFAULT_TIMEOUT = 10
SUPPORTED_ENVS: Tuple[str, ...] = ("claude", "copilot", "codex", "cursor")
GLOBAL_UNSUPPORTED: Tuple[str, ...] = ("copilot",)
STDIN_MARKER = "-"
NO_SOURCE_ERROR = (
    "Provide commands via positional COMMANDS, '-c CMD', '--file PATH', "
    "or stdin ('-')."
)
MULTIPLE_SOURCES_ERROR = (
    "Only one input source may be used at a time: "
    "positional COMMANDS, '-c CMD', '--file PATH', or stdin ('-')."
)
EMPTY_INPUT_ERROR = "No commands to run (input is empty)."
MISSING_RICH_RST_ERROR = (
    "The 'rich-rst' package is required to use the 'help' command.\n"
    "Install it via 'pip install rich-rst' and try again."
)
_KEY_WIDTH = 24
_MAPDL_CMD_RE = re.compile(r"Mechanical APDL Command: `(\\?\*?/?[^\s<`]+)")
_ANSYS_HELP_URL_RE = re.compile(r"ansyshelp\.ansys\.com")
_FIRST_SECTION_RE = re.compile(r"^\S[^\n]*\n-{3,}", re.MULTILINE)
_SPHINX_ROLE_WITH_TARGET_RE = re.compile(r":\w[\w.:-]*:`([^`<>]+)\s*<[^>]*>`")
_SPHINX_ROLE_SIMPLE_RE = re.compile(r":\w[\w.:-]*:`([^`]+)`")
_EXCLUDED_DIRECTORIES = ("evals", "workspace")
_INCOMPLETE_PLAN_ERROR = (
    "The installation plan is missing paths required by the {env!r} environment."
)

# Database and inline query constants.
MINIMUM_MAPDL_VERSION = "21.1"
FAILING_DATABASE_MAPDL = ["24.1", "24.2"]
DEFAULT_DB_PORT = 50055
QUERY_NAME = "__QUERY_PARM__"

# Launcher constants.
MAPDL_DEFAULT_PORT = 50052
LAUNCHER_DEFAULT_TIMEOUT = 45
_PROCESS_OK_STATUS = (
    psutil.STATUS_RUNNING,
    psutil.STATUS_SLEEPING,
    psutil.STATUS_DISK_SLEEP,
    psutil.STATUS_DEAD,
    psutil.STATUS_PARKED,
    psutil.STATUS_IDLE,
)
_TERMINATION_TIMEOUT = 5.0

# Mesh conversion constants.
MESH200_MAP = {
    0: 2,
    1: 2,
    2: 2,
    3: 2,
    4: 3,
    5: 3,
    6: 3,
    7: 3,
    8: 5,
    9: 5,
    10: 4,
    11: 4,
}
SHAPE_MAP = {
    0: "",
    1: "LINE",
    2: "PARA",
    3: "ARC ",
    4: "CARC",
    5: "",
    6: "TRIA",
    7: "QUAD",
    8: "TRI6",
    9: "QUA8",
    10: "POIN",
    11: "CIRC",
    12: "",
    13: "",
    14: "CYLI",
    15: "CONE",
    16: "SPHE",
    17: "",
    18: "",
    19: "PILO",
}
TARGE170_MAP = {
    "TRI": 3,
    "QUAD": 3,
    "CYLI": 0,
    "CONE": 0,
    "TRI6": 3,
    "SPHE": 0,
    "PILO": 1,
    "QUAD8": 3,
    "LINE": 2,
    "PARA": 2,
    "POINT": 1,
}

# Plotting constants.
POINT_SIZE = 10
BC_D = ["TEMP", "UX", "UY", "UZ", "VOLT"]
BC_F = ["HEAT", "FX", "FY", "FZ", "AMPS", "CHRG", "CSGZ"]
FIELDS = {
    "MECHANICAL": ["UX", "UY", "UZ", "FX", "FY", "FZ"],
    "THERMAL": ["TEMP", "HEAT"],
    "ELECTRICAL": ["VOLT", "CHRG", "AMPS"],
}
FIELDS_ORDERED_LABELS = FIELDS["MECHANICAL"] + FIELDS["THERMAL"] + FIELDS["ELECTRICAL"]
BCS = BC_D + BC_F
ALLOWED_TARGETS = ["NODES"]

# Reader constants.
COMPONENTS: List[str] = ["X", "Y", "Z", "XY", "YZ", "XZ"]
LOCATION_MAPPING: Dict[str, str] = {"NODE": "Nodal", "ELEM": "Elemental"}
MATERIAL_PROPERTIES: List[str] = [
    "EX",
    "EY",
    "EZ",
    "ALPX",
    "ALPY",
    "ALPZ",
    "REFT",
    "PRXY",
    "PRYZ",
    "PRX",
    "NUXY",
    "NUYZ",
    "NUXZ",
    "GXY",
    "GYZ",
    "GXZ",
    "DAMP",
    "MU",
    "DENS",
    "C",
    "ENTH",
    "KXX",
    "KYY",
    "KZZ",
    "HF",
    "EMIS",
    "QRATE",
    "VISC",
    "SONC",
    "RSVX",
    "RSVY",
    "RSVZ",
    "PERX",
    "PERY",
    "PERZ",
    "MURX",
    "MURY",
    "MURZ",
    "MGXX",
    "MGYY",
    "MGZZ",
    "XTEN",
    "XCMP",
    "YTEN",
    "YCMP",
    "ZTEN",
    "ZCMP",
    "XY",
    "YZ",
    "XZ",
    "XYCP",
    "YZCP",
    "XZCP",
    "XZIT",
    "XZIC",
    "YZIT",
    "YZIC",
]
NOT_AVAILABLE_METHOD = """The method '{method}' has not been ported to the new DPF-based Results backend.
If you still want to use it, you can switch to 'pymapdl-reader' backend using `mapdl.use_reader_backend = True`."""
NOT_AVAILABLE_ARGUMENT = """The argument '{argument}' in this function has not been ported to the new DPF-based Results backend.
If you still want to use it, you can switch to 'pymapdl-reader' backend using `mapdl.use_reader_backend = True`."""

# Legacy console protocol constants.
MAPDL_CONSOLE_READY_ITEMS = [
    rb"BEGIN:",
    rb"PREP7:",
    rb"SOLU_LS[0-9]+:",
    rb"POST1:",
    rb"POST26:",
    rb"RUNSTAT:",
    rb"AUX2:",
    rb"AUX3:",
    rb"AUX12:",
    rb"AUX15:",
    rb"YES,NO OR CONTINUOUS\)\=",
    rb"executed\?",
    rb"SHOULD INPUT PROCESSING BE SUSPENDED\?",
    rb"ANSYS Traceback",
    rb"eMPIChildJob",
    rb"ENTER FORMAT for",
]
CONTINUE_IDX = MAPDL_CONSOLE_READY_ITEMS.index(rb"YES,NO OR CONTINUOUS\)\=")
WARNING_IDX = MAPDL_CONSOLE_READY_ITEMS.index(rb"executed\?")
ERROR_IDX = MAPDL_CONSOLE_READY_ITEMS.index(rb"SHOULD INPUT PROCESSING BE SUSPENDED\?")
PROMPT_IDX = MAPDL_CONSOLE_READY_ITEMS.index(rb"ENTER FORMAT for")
MAPDL_CONSOLE_NITEMS = len(MAPDL_CONSOLE_READY_ITEMS)
MAPDL_CONSOLE_EXPECT_LIST = [re.compile(item) for item in MAPDL_CONSOLE_READY_ITEMS]
MAPDL_CONSOLE_IGNORED = re.compile(r"[\s\S]+".join(["WARNING", "command", "ignored"]))
