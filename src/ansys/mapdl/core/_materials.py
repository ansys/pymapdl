# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Read-only snapshot of the Materials defined in a MAPDL session."""

from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np

from ansys.mapdl.core.misc import random_string


def _read_only(values: List[float]) -> np.ndarray:
    array = np.array(values, dtype=float)
    array.flags.writeable = False
    return array


@dataclass(frozen=True)
class PropertyTable:
    """Temperature table of one Material Property.

    A constant set with ``MP`` is a one-point table at temperature ``0.0``.

    Parameters
    ----------
    temperatures : numpy.ndarray
        Read-only temperatures, at least one.
    values : numpy.ndarray
        Read-only values, one for each temperature.

    Examples
    --------
    >>> ex = mapdl.materials[1].properties["EX"]
    >>> ex.temperatures, ex.values
    (array([ 20., 100.]), array([2.1e+11, 2.0e+11]))
    """

    temperatures: np.ndarray
    values: np.ndarray


@dataclass(frozen=True)
class Material:
    """Snapshot of one Material.

    Parameters
    ----------
    id : int
        Material ID.
    properties : dict[str, PropertyTable]
        Material Properties keyed by their ``MP`` label, such as ``"EX"``.

    Examples
    --------
    >>> material = mapdl.materials[1]
    >>> material.id, list(material.properties)
    (1, ['EX', 'PRXY'])
    """

    id: int
    properties: Dict[str, PropertyTable]


_IGNORED_COMMANDS = {"", "/COM", "/NOP", "/GO"}


class _CdwriteMatParser:
    """Accumulate the lines of one ``CDWRITE,MAT`` file into Materials."""

    def __init__(self) -> None:
        self._temperatures: List[float] = []
        self._properties: Dict[Tuple[int, str], Dict[int, Tuple[float, float]]] = {}
        self._handlers = {"MPTE": self._mptemp, "MPDA": self._mpdata}

    def feed(self, line: str) -> None:
        fields = [field.strip() for field in line.split(",")]
        command = fields[0][:4].upper()
        if command in _IGNORED_COMMANDS:
            return
        handler = self._handlers.get(command)
        if handler is None:
            raise ValueError(f"Unknown line in CDWRITE,MAT output: {line!r}")
        handler(fields)

    def _mptemp(self, fields: List[str]) -> None:
        start = int(fields[3])
        if start == 1:
            self._temperatures = []
        self._temperatures[start - 1 :] = [float(f) for f in fields[4:] if f]

    def _mpdata(self, fields: List[str]) -> None:
        table = self._properties.setdefault((int(fields[4]), fields[3].upper()), {})
        values = [float(f) for f in fields[6:] if f]
        for slot, value in enumerate(values, int(fields[5]) - 1):
            table[slot] = (self._temperatures[slot], value)

    def materials(self) -> Dict[int, Material]:
        properties: Dict[int, Dict[str, PropertyTable]] = {}
        for (mat_id, label), table in self._properties.items():
            temperatures, values = zip(*(table[slot] for slot in sorted(table)))
            properties.setdefault(mat_id, {})[label] = PropertyTable(
                _read_only(list(temperatures)), _read_only(list(values))
            )
        return {
            mat_id: Material(mat_id, properties[mat_id])
            for mat_id in sorted(properties)
        }


def _parse_cdwrite_mat(text: str) -> Dict[int, Material]:
    """Parse ``CDWRITE,MAT`` file text into ``{id: Material}``."""
    parser = _CdwriteMatParser()
    for line in text.splitlines():
        parser.feed(line)
    return parser.materials()


class MaterialsSnapshot(Mapping[int, Material]):
    """Read-only mapping of every Material in the session, keyed by material ID.

    Each access to ``mapdl.materials`` reads MAPDL once and returns a new
    snapshot. A snapshot does not change when MAPDL changes later.

    Parameters
    ----------
    materials : dict[int, Material]
        Materials keyed by material ID.

    Examples
    --------
    >>> materials = mapdl.materials
    >>> list(materials), 1 in materials, len(materials)
    ([1, 4], True, 2)
    >>> materials[1].properties["EX"].values
    array([2.1e+11, 2.0e+11])
    """

    def __init__(self, materials: Dict[int, Material]) -> None:
        self._materials = materials

    def __getitem__(self, mat_id: int) -> Material:
        return self._materials[mat_id]

    def __iter__(self) -> Iterator[int]:
        return iter(self._materials)

    def __len__(self) -> int:
        return len(self._materials)

    def __repr__(self) -> str:
        return f"MaterialsSnapshot(ids={list(self._materials)})"


def _read_materials(mapdl: Any) -> MaterialsSnapshot:
    """Write ``CDWRITE,MAT`` to a unique server file, read it, and delete it."""
    fname = f"_materials_{random_string()}"
    try:
        mapdl.cdwrite("MAT", fname, "cdb", mute=True)
        text = mapdl._download_as_raw(f"{fname}.cdb").decode()
    finally:
        mapdl.slashdelete(fname, "cdb", mute=True)
    return MaterialsSnapshot(_parse_cdwrite_mat(text))
