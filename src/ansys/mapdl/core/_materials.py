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

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

import numpy as np

from ansys.mapdl.core import _HAS_PANDAS
from ansys.mapdl.core.commands import MSG_NOT_PANDAS
from ansys.mapdl.core.misc import random_string

if TYPE_CHECKING:
    import pandas


def _read_only(values: Sequence[Any]) -> np.ndarray:
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
class DataTable:
    """Raw content of one Data Table, without interpretation.

    A Data Table fills either ``constants`` or ``points``; the other list is
    empty.

    Parameters
    ----------
    label : str
        Data Table label as MAPDL writes it, such as ``"BISO"``.
    tbopt : str
        Data Table option as written, or ``""`` when not set.
    temperatures : numpy.ndarray
        Read-only temperatures. A table defined without ``TBTEMP`` is at
        temperature ``0.0``.
    constants : list[numpy.ndarray]
        Read-only constants, one array for each temperature.
    points : list[numpy.ndarray]
        Read-only ``(n, 2)`` points, one array for each temperature.
    fields : dict[str, numpy.ndarray]
        Read-only field values other than temperature, aligned with
        ``temperatures``. Empty for Data Tables without fields.

    Examples
    --------
    >>> biso = mapdl.materials[1].tables[0]
    >>> biso.label, biso.temperatures, biso.constants[0]
    ('BISO', array([ 20., 200.]), array([2.5e+08, 2.0e+09]))
    """

    label: str
    tbopt: str
    temperatures: np.ndarray
    constants: List[np.ndarray]
    points: List[np.ndarray]
    fields: Dict[str, np.ndarray]


@dataclass(frozen=True)
class Material:
    """Snapshot of one Material.

    Parameters
    ----------
    id : int
        Material ID.
    properties : dict[str, PropertyTable]
        Material Properties keyed by their ``MP`` label, such as ``"EX"``.
    tables : list[DataTable]
        Data Tables in the order MAPDL writes them.

    Examples
    --------
    >>> material = mapdl.materials[1]
    >>> material.id, list(material.properties), [t.label for t in material.tables]
    (1, ['EX', 'PRXY'], ['BISO'])
    """

    id: int
    properties: Dict[str, PropertyTable]
    tables: List[DataTable]


_IGNORED_COMMANDS = {"", "/COM", "/NOP", "/GO"}


class _DataTableBuilder:
    """Collect the lines of one legacy-format Data Table."""

    def __init__(self, fields: List[str]) -> None:
        self.label = fields[1]
        self.mat_id = int(fields[2])
        self.ntemp = int(fields[3])
        self.tbopt = fields[5] if len(fields) > 5 else ""
        self.temperatures: List[float] = []
        self.constants: List[Dict[int, float]] = []
        self.points: List[List[Tuple[float, float]]] = []

    def build(self) -> DataTable:
        if len(self.temperatures) != self.ntemp:
            raise ValueError(
                f"Data Table {self.label} of Material {self.mat_id}: TB header "
                f"gives {self.ntemp} temperatures, CDWRITE,MAT output has "
                f"{len(self.temperatures)}."
            )
        constants = []
        for slots in self.constants:
            values = np.zeros(max(slots, default=-1) + 1)
            values[list(slots)] = list(slots.values())
            constants.append(_read_only(values))
        points = [_read_only(rows).reshape(-1, 2) for rows in self.points]
        return DataTable(
            self.label,
            self.tbopt,
            _read_only(self.temperatures),
            constants if any(self.constants) else [],
            points if any(self.points) else [],
            {},
        )


class _CdwriteMatParser:
    """Accumulate the lines of one ``CDWRITE,MAT`` file into Materials."""

    def __init__(self) -> None:
        self._temperatures: List[float] = []
        self._properties: Dict[Tuple[int, str], Dict[int, Tuple[float, float]]] = {}
        self._tables: List[_DataTableBuilder] = []
        self._handlers = {
            "MPTE": self._mptemp,
            "MPDA": self._mpdata,
            "TB": self._tb,
            "TBTE": self._tbtemp,
            "TBDA": self._tbdata,
            "TBPT": self._tbpt,
        }

    def feed(self, line: str) -> None:
        fields = [field.strip() for field in line.split(",")]
        command = fields[0][:4].upper()
        if command in _IGNORED_COMMANDS:
            return
        handler = self._handlers.get(command)
        if handler is None or not handler(fields):
            raise ValueError(f"Unknown line in CDWRITE,MAT output: {line!r}")

    def _mptemp(self, fields: List[str]) -> bool:
        start = int(fields[3])
        if start == 1:
            self._temperatures = []
        self._temperatures[start - 1 :] = [float(f) for f in fields[4:] if f]
        return True

    def _mpdata(self, fields: List[str]) -> bool:
        table = self._properties.setdefault((int(fields[4]), fields[3].upper()), {})
        values = [float(f) for f in fields[6:] if f]
        for slot, value in enumerate(values, int(fields[5]) - 1):
            table[slot] = (self._temperatures[slot], value)
        return True

    def _tb(self, fields: List[str]) -> bool:
        self._tables.append(_DataTableBuilder(fields))
        return True

    def _current_table(self) -> _DataTableBuilder | None:
        if not self._tables:
            return None
        table = self._tables[-1]
        if not table.temperatures:
            self._start_temperature(table, 0.0)
        return table

    @staticmethod
    def _start_temperature(table: _DataTableBuilder, temperature: float) -> None:
        table.temperatures.append(temperature)
        table.constants.append({})
        table.points.append([])

    def _tbtemp(self, fields: List[str]) -> bool:
        if not self._tables:
            return False
        self._start_temperature(self._tables[-1], float(fields[1]))
        return True

    def _tbdata(self, fields: List[str]) -> bool:
        table = self._current_table()
        if table is None or fields[0].upper() == "TBDATA":
            return False
        values = [float(f) for f in fields[2:] if f]
        table.constants[-1].update(enumerate(values, int(fields[1]) - 1))
        return True

    def _tbpt(self, fields: List[str]) -> bool:
        table = self._current_table()
        if table is None or fields[1]:
            return False
        table.points[-1].append((float(fields[2]), float(fields[3])))
        return True

    def materials(self) -> Dict[int, Material]:
        properties: Dict[int, Dict[str, PropertyTable]] = {}
        for (mat_id, label), table in self._properties.items():
            temperatures, values = zip(*(table[slot] for slot in sorted(table)))
            properties.setdefault(mat_id, {})[label] = PropertyTable(
                _read_only(list(temperatures)), _read_only(list(values))
            )
        tables: Dict[int, List[DataTable]] = {}
        for builder in self._tables:
            tables.setdefault(builder.mat_id, []).append(builder.build())
        return {
            mat_id: Material(mat_id, properties.get(mat_id, {}), tables.get(mat_id, []))
            for mat_id in sorted(properties.keys() | tables.keys())
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

    def to_dataframe(self) -> "pandas.DataFrame":
        """Return the Material Properties as a long-format pandas DataFrame.

        The DataFrame has one row per temperature point of every Material
        Property. Data Tables are not included because their shapes vary.

        Returns
        -------
        pandas.DataFrame
            Columns ``material``, ``label``, ``temperature`` and ``value``.

        Raises
        ------
        ModuleNotFoundError
            If pandas is not installed.

        Examples
        --------
        >>> df = mapdl.materials.to_dataframe()
        >>> df[df.label == "EX"].pivot(
        ...     index="temperature", columns="material", values="value"
        ... )
        """
        if not _HAS_PANDAS:
            raise ModuleNotFoundError(MSG_NOT_PANDAS)
        import pandas

        rows = [
            (material.id, label, temperature, value)
            for material in self._materials.values()
            for label, table in material.properties.items()
            for temperature, value in zip(table.temperatures, table.values)
        ]
        return pandas.DataFrame(
            rows, columns=["material", "label", "temperature", "value"]
        )


def _read_materials(mapdl: Any) -> MaterialsSnapshot:
    """Write ``CDWRITE,MAT`` to a unique server file, read it, and delete it."""
    fname = f"_materials_{random_string()}"
    try:
        mapdl.cdwrite("MAT", fname, "cdb", mute=True)
        text = mapdl._download_as_raw(f"{fname}.cdb").decode()
    finally:
        mapdl.slashdelete(fname, "cdb", mute=True)
    return MaterialsSnapshot(_parse_cdwrite_mat(text))
