# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Types for the MAPDL reader module."""

from typing import Any, Iterable, Literal, ParamSpec, TypeAlias, Union

import ansys.dpf.core as dpf
import numpy as np

## Types
Rnum: TypeAlias = Union[int, float, Iterable[int], Iterable[float], None]
Ids: TypeAlias = Union[int, Iterable[int], None]
Locations: TypeAlias = Literal["Nodal", "Elemental"]

Entities: TypeAlias = str | int | Iterable[str | int] | None
EntityType: TypeAlias = Literal["Nodal", "Elemental", "ElementalNodal"]

ResultField: TypeAlias = str  # To be defined later.. Eg "displacement" etc...
SolutionType: TypeAlias = str
ComponentsDirections: TypeAlias = Literal["X", "Y", "Z", "XY", "YZ", "XZ"]

Nodes: TypeAlias = str | int | Iterable[int | str] | None
Elements: TypeAlias = str | int | Iterable[int | str] | None
MAPDLComponents: TypeAlias = str | Iterable[int | str] | None

ReturnData: TypeAlias = Union[
    tuple[
        np.ndarray[Any, np.dtype[np.floating[Any]]],
        np.ndarray[Any, np.dtype[np.floating[Any]]],
    ],
    dpf.Field,
]

Kwargs: TypeAlias = dict[Any, Any]
P = ParamSpec("P")
