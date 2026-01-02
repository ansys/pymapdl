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

"""Defines constants for the MAPDL reader."""


## Globals
COMPONENTS: list[str] = ["X", "Y", "Z", "XY", "YZ", "XZ"]

LOCATION_MAPPING: dict[str, str] = {
    "NODE": "Nodal",
    "ELEM": "Elemental",
}

MATERIAL_PROPERTIES: list[str] = [
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


NOT_AVAILABLE_METHOD: str = """The method '{method}' has not been ported to the new DPF-based Results backend.
If you still want to use it, you can switch to 'pymapdl-reader' backend using `mapdl.use_reader_backend = True`."""

NOT_AVAILABLE_ARGUMENT: str = """The argument '{argument}' in this function has not been ported to the new DPF-based Results backend.
If you still want to use it, you can switch to 'pymapdl-reader' backend using `mapdl.use_reader_backend = True`."""
