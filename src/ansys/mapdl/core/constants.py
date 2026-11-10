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

"""Constants shared across PyMAPDL core modules."""

import os
from typing import Dict, Optional

import numpy as np
from platformdirs import user_data_dir

USER_DATA_PATH: str = user_data_dir(appname="ansys_mapdl_core", appauthor="Ansys")

# In descending order.
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

DEFAULT_CHUNKSIZE: int = 256 * 1024  # 256 kB
ANSYS_VALUE_TYPE: Dict[int, Optional[np.typing.DTypeLike]] = {
    0: None,  # UNKNOWN
    1: np.int32,  # INTEGER
    2: np.int64,  # HYPER
    3: np.int16,  # SHORT
    4: np.float32,  # FLOAT
    5: np.float64,  # DOUBLE
    6: np.complex64,  # FCPLX
    7: np.complex128,  # DCPLX
    8: np.char,
}

LOCALHOST = "127.0.0.1"
MAPDL_DEFAULT_PORT = 50052
MAX_PARAM_CHARS = 32
MAX_MESSAGE_LENGTH = int(os.environ.get("PYMAPDL_MAX_MESSAGE_LENGTH", 256 * 1024**2))
