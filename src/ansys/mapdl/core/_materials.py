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
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

import numpy as np

from ansys.mapdl.core import _HAS_PANDAS
from ansys.mapdl.core.commands import MSG_NOT_PANDAS
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import random_string

if TYPE_CHECKING:
    import pandas

    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


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

    A Data Table fills either ``constants`` or ``points``; the other tuple is
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
    constants : tuple[numpy.ndarray, ...]
        Read-only constants, one array for each temperature. A constant slot
        that MAPDL does not write is ``nan``.
    points : tuple[numpy.ndarray, ...]
        Read-only ``(n, 2)`` points, one array for each temperature.
    fields : Mapping[str, numpy.ndarray]
        Read-only field values other than temperature, aligned with
        ``temperatures``. Empty for Data Tables without fields.
    options : Mapping[str, tuple[tuple[str, ...], ...]]
        Raw ``TBIN`` arguments keyed by option name, one inner tuple for each
        ``TBIN`` line of that option in file order, such as
        ``{"NORM": (("1",),)}``. Empty for legacy-format Data Tables.

    Examples
    --------
    >>> biso = mapdl.materials[1].tables[0]
    >>> biso.label, biso.temperatures, biso.constants[0]
    ('BISO', array([ 20., 200.]), array([2.5e+08, 2.0e+09]))
    """

    label: str
    tbopt: str
    temperatures: np.ndarray
    constants: Tuple[np.ndarray, ...]
    points: Tuple[np.ndarray, ...]
    fields: Mapping[str, np.ndarray]
    options: Mapping[str, Tuple[Tuple[str, ...], ...]]


@dataclass(frozen=True)
class Material:
    """Snapshot of one Material.

    Parameters
    ----------
    id : int
        Material ID.
    properties : Mapping[str, PropertyTable]
        Read-only Material Properties keyed by their ``MP`` label, such as
        ``"EX"``.
    tables : tuple[DataTable, ...]
        Data Tables in the order MAPDL writes them.

    Examples
    --------
    >>> material = mapdl.materials[1]
    >>> material.id, list(material.properties), [t.label for t in material.tables]
    (1, ['EX', 'PRXY'], ['BISO'])
    """

    id: int
    properties: Mapping[str, PropertyTable]
    tables: Tuple[DataTable, ...]


_IGNORED_COMMANDS = {"", "/COM", "/NOP", "/GO"}


class _DataTableBuilder:
    """Collect the lines of one Data Table, in either dialect."""

    def __init__(self, args: List[str]) -> None:
        self.label = args[1]
        self.mat_id = int(args[2])
        self.ntemp = int(args[3])
        self.tbopt = args[5] if len(args) > 5 else ""
        self.temperatures: List[float] = []
        self.constants: List[Dict[int, float]] = []
        self.points: List[List[Tuple[float, float]]] = []
        self.field_points: List[Dict[str, float]] = []
        self.options: Dict[str, List[Tuple[str, ...]]] = {}

    def start_point(self, temperature: float) -> None:
        self.temperatures.append(temperature)
        self.constants.append({})
        self.points.append([])

    def _current_point(self) -> None:
        if not self.temperatures:
            self.start_point(0.0)

    def add_field(self, name: str, value: float) -> None:
        if not self.field_points or name in self.field_points[-1]:
            self.start_point(0.0)
            self.field_points.append({})
        self.field_points[-1][name] = value
        if name.upper() == "TEMPS":
            self.temperatures[-1] = value

    def add_constants(self, start: int, values: List[float]) -> None:
        self._current_point()
        self.constants[-1].update(enumerate(values, start - 1))

    def add_point(self, x: float, y: float) -> None:
        self._current_point()
        self.points[-1].append((x, y))

    def add_option(self, name: str, args: Tuple[str, ...]) -> None:
        self.options.setdefault(name, []).append(args)

    def build(self) -> DataTable:
        if len(self.temperatures) != self.ntemp:
            unit = "field points" if self.field_points else "temperatures"
            raise ValueError(
                f"Data Table {self.label} of Material {self.mat_id}: TB header "
                f"gives {self.ntemp} {unit}, CDWRITE,MAT output has "
                f"{len(self.temperatures)}."
            )
        names = dict.fromkeys(
            name for row in self.field_points for name in row if name.upper() != "TEMPS"
        )
        constants = []
        for slots in self.constants:
            values = np.full(max(slots, default=-1) + 1, np.nan)
            values[list(slots)] = list(slots.values())
            constants.append(_read_only(values))
        points = [_read_only(rows).reshape(-1, 2) for rows in self.points]
        return DataTable(
            self.label,
            self.tbopt,
            _read_only(self.temperatures),
            tuple(constants) if any(self.constants) else (),
            tuple(points) if any(self.points) else (),
            MappingProxyType(
                {
                    name: _read_only([row[name] for row in self.field_points])
                    for name in names
                }
            ),
            MappingProxyType(
                {name: tuple(lines) for name, lines in self.options.items()}
            ),
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
            "TBFI": self._tbfield,
            "TBDA": self._tbdata,
            "TBPT": self._tbpt,
            "TBIN": self._tbin,
        }

    def feed(self, line: str) -> None:
        args = [arg.strip() for arg in line.split(",")]
        command = args[0][:4].upper()
        if command in _IGNORED_COMMANDS:
            return
        handler = self._handlers.get(command)
        if handler is None:
            raise ValueError(f"Unknown line in CDWRITE,MAT output: {line!r}")
        try:
            handler(args)
        except (ValueError, IndexError) as err:
            raise ValueError(f"Cannot parse CDWRITE,MAT line {line!r}: {err}") from err

    def _table(self) -> _DataTableBuilder:
        if not self._tables:
            raise ValueError("Data Table line without a preceding TB header.")
        return self._tables[-1]

    def _mptemp(self, args: List[str]) -> None:
        start = int(args[3])
        if start == 1:
            self._temperatures = []
        self._temperatures[start - 1 :] = [float(a) for a in args[4:] if a]

    def _mpdata(self, args: List[str]) -> None:
        table = self._properties.setdefault((int(args[4]), args[3].upper()), {})
        values = [float(a) for a in args[6:] if a]
        for slot, value in enumerate(values, int(args[5]) - 1):
            table[slot] = (self._temperatures[slot], value)

    def _tb(self, args: List[str]) -> None:
        self._tables.append(_DataTableBuilder(args))

    def _tbtemp(self, args: List[str]) -> None:
        self._table().start_point(float(args[1]))

    def _tbfield(self, args: List[str]) -> None:
        self._table().add_field(args[1], float(args[2]))

    def _tbdata(self, args: List[str]) -> None:
        self._table().add_constants(int(args[1]), [float(a) for a in args[2:] if a])

    def _tbpt(self, args: List[str]) -> None:
        table = self._table()
        if args[1].upper() not in ("", "DEFI"):
            raise ValueError(f"Unsupported TBPT option {args[1]!r}.")
        table.add_point(float(args[2]), float(args[3]))

    def _tbin(self, args: List[str]) -> None:
        self._table().add_option(args[1], tuple(args[2:]))

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
            mat_id: Material(
                mat_id,
                MappingProxyType(properties.get(mat_id, {})),
                tuple(tables.get(mat_id, ())),
            )
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
        >>> mapdl.materials.to_dataframe()
           material label  temperature         value
        0         1    EX         20.0  2.100000e+11
        1         1    EX        100.0  2.000000e+11
        2         1  PRXY          0.0  3.000000e-01
        3         4    EX          0.0  7.000000e+10
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


def _read_materials(mapdl: "MapdlGrpc") -> MaterialsSnapshot:
    """Write ``CDWRITE,MAT`` to a unique server file, read it, and delete it."""
    if not hasattr(mapdl, "_download_as_raw"):
        raise MapdlRuntimeError(
            "`mapdl.materials` needs a gRPC session to read the CDWRITE,MAT "
            "file back. It is not available in this session type."
        )
    if mapdl._store_commands:
        raise MapdlRuntimeError(
            "Cannot use `mapdl.materials` to retrieve materials when in "
            "`non_interactive` mode. "
            "Exit `non_interactive` mode before using this method."
        )
    fname = f"_materials_{random_string()}"
    try:
        mapdl.cdwrite("MAT", fname, "cdb", mute=True)
        text = mapdl._download_as_raw(f"{fname}.cdb").decode()
    finally:
        mapdl.slashdelete(fname, "cdb", mute=True)
    if not text:
        raise MapdlRuntimeError(
            f"MAPDL did not write the CDWRITE,MAT file '{fname}.cdb'. "
            "Check that the MAPDL working directory is writable."
        )
    return MaterialsSnapshot(_parse_cdwrite_mat(text))
