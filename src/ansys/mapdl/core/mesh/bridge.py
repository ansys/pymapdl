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

"""Internal normalized mesh representation and pure-NumPy Mesh Archive writer."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import numpy as np
from numpy.typing import NDArray
import pyvista as pv
from pyvista import CellType

# VTK point index written to each Mechanical APDL EBLOCK node slot, per layout.
_LAYOUTS: dict[str, dict[CellType, tuple[int, ...]]] = {
    "point": {CellType.VERTEX: (0,)},
    "line": {CellType.LINE: (0, 1)},
    "line3": {CellType.QUADRATIC_EDGE: (0, 1, 2)},
    "shell": {
        CellType.QUAD: (0, 1, 2, 3),
        CellType.PIXEL: (0, 1, 3, 2),
        CellType.TRIANGLE: (0, 1, 2, 2),
    },
    "shell8": {
        CellType.QUADRATIC_QUAD: tuple(range(8)),
        CellType.QUADRATIC_TRIANGLE: (0, 1, 2, 2, 3, 4, 2, 5),
    },
    "brick": {
        CellType.HEXAHEDRON: tuple(range(8)),
        CellType.VOXEL: (0, 1, 3, 2, 4, 5, 7, 6),
        CellType.TETRA: (0, 1, 2, 2, 3, 3, 3, 3),
        CellType.PYRAMID: (0, 1, 2, 3, 4, 4, 4, 4),
        # Reversed base keeps a positive Jacobian in Mechanical APDL.
        CellType.WEDGE: (2, 1, 0, 0, 5, 4, 3, 3),
    },
    "brick20": {
        CellType.QUADRATIC_HEXAHEDRON: tuple(range(20)),
        CellType.QUADRATIC_TETRA: (
            0,
            1,
            2,
            2,
            3,
            3,
            3,
            3,
            4,
            5,
            2,
            6,
            3,
            3,
            3,
            3,
            7,
            8,
            9,
            9,
        ),
        CellType.QUADRATIC_PYRAMID: (
            0,
            1,
            2,
            3,
            4,
            4,
            4,
            4,
            5,
            6,
            7,
            8,
            4,
            4,
            4,
            4,
            9,
            10,
            11,
            12,
        ),
        CellType.QUADRATIC_WEDGE: (
            2,
            1,
            0,
            0,
            5,
            4,
            3,
            3,
            7,
            6,
            0,
            8,
            10,
            9,
            3,
            11,
            14,
            13,
            12,
            12,
        ),
    },
    "tet10": {CellType.QUADRATIC_TETRA: tuple(range(10))},
}

# Leading EBLOCK slots that hold corner nodes and therefore can never be omitted (0).
_CORNER_SLOTS = {
    "point": 1,
    "line": 2,
    "line3": 2,
    "shell": 4,
    "shell8": 4,
    "brick": 8,
    "brick20": 8,
    "tet10": 4,
}

_ELEMENTS: dict[int, tuple[str, str]] = {
    21: ("MASS21", "point"),
    14: ("COMBIN14", "line"),
    180: ("LINK180", "line"),
    188: ("BEAM188", "line"),
    288: ("PIPE288", "line"),
    189: ("BEAM189", "line3"),
    289: ("PIPE289", "line3"),
    55: ("PLANE55", "shell"),
    131: ("SHELL131", "shell"),
    154: ("SURF154", "shell"),
    181: ("SHELL181", "shell"),
    182: ("PLANE182", "shell"),
    77: ("PLANE77", "shell8"),
    132: ("SHELL132", "shell8"),
    183: ("PLANE183", "shell8"),
    223: ("PLANE223", "shell8"),
    281: ("SHELL281", "shell8"),
    70: ("SOLID70", "brick"),
    185: ("SOLID185", "brick"),
    278: ("SOLID278", "brick"),
    90: ("SOLID90", "brick20"),
    186: ("SOLID186", "brick20"),
    226: ("SOLID226", "brick20"),
    279: ("SOLID279", "brick20"),
    87: ("SOLID87", "tet10"),
    187: ("SOLID187", "tet10"),
    227: ("SOLID227", "tet10"),
}

_DEFAULT_ELEMENTS: dict[CellType, int] = {
    CellType.VERTEX: 21,
    CellType.LINE: 188,
    CellType.QUADRATIC_EDGE: 189,
    CellType.TRIANGLE: 181,
    CellType.QUAD: 181,
    CellType.PIXEL: 181,
    CellType.QUADRATIC_TRIANGLE: 281,
    CellType.QUADRATIC_QUAD: 281,
    CellType.TETRA: 185,
    CellType.PYRAMID: 185,
    CellType.WEDGE: 185,
    CellType.HEXAHEDRON: 185,
    CellType.VOXEL: 185,
    CellType.QUADRATIC_PYRAMID: 186,
    CellType.QUADRATIC_WEDGE: 186,
    CellType.QUADRATIC_HEXAHEDRON: 186,
    CellType.QUADRATIC_TETRA: 187,
}

_MESHIO_CELL_TYPES: dict[str, CellType] = {
    "vertex": CellType.VERTEX,
    "line": CellType.LINE,
    "line3": CellType.QUADRATIC_EDGE,
    "triangle": CellType.TRIANGLE,
    "triangle6": CellType.QUADRATIC_TRIANGLE,
    "quad": CellType.QUAD,
    "quad8": CellType.QUADRATIC_QUAD,
    "tetra": CellType.TETRA,
    "tetra10": CellType.QUADRATIC_TETRA,
    "pyramid": CellType.PYRAMID,
    "pyramid13": CellType.QUADRATIC_PYRAMID,
    "wedge": CellType.WEDGE,
    "wedge15": CellType.QUADRATIC_WEDGE,
    "hexahedron": CellType.HEXAHEDRON,
    "hexahedron20": CellType.QUADRATIC_HEXAHEDRON,
}

_COMPONENT_KINDS = {
    "NODE": "NODE",
    "NODES": "NODE",
    "ELEM": "ELEM",
    "ELEMS": "ELEM",
    "ELEMENT": "ELEM",
    "ELEMENTS": "ELEM",
}
# Names starting with ``_`` are hidden from ``CMLIST`` and ``mapdl.components``.
_COMPONENT_NAME = re.compile(r"[A-Z][A-Z0-9_]{0,31}")
_INTERNAL_ARRAY = re.compile(r"origid|vtkorigid|vtk.*|ansys_.*", re.IGNORECASE)


@dataclass(slots=True)
class _MeshData:
    """Normalized mesh ready to serialize as a Mesh Archive."""

    node_ids: NDArray[np.int64]
    nodes: NDArray[np.float64]
    node_angles: NDArray[np.float64] | None
    elem_ids: NDArray[np.int64]
    etype_ids: NDArray[np.int64]
    mat_ids: NDArray[np.int64]
    real_ids: NDArray[np.int64]
    sec_ids: NDArray[np.int64]
    esys_ids: NDArray[np.int64]
    connectivity: NDArray[np.int64]  # (M, 20) MAPDL node IDs, 0 = omitted/unused slot
    nnodes: NDArray[np.int64]
    et_defs: dict[int, int]
    keyopts: dict[int, dict[int, int]]
    components: dict[str, tuple[str, NDArray[np.int64]]]


def _existing_etype_ids(etype: Any) -> set[int]:
    """Return the pre-defined ET IDs referenced by an ``etype`` argument."""
    values = etype.values() if isinstance(etype, Mapping) else [etype]
    return {int(v) for v in values if _is_int(v)}


def _is_int(value: Any) -> bool:
    return isinstance(value, (int, np.integer)) and not isinstance(value, bool)


def _element_number(etype: Any) -> int:
    match = re.fullmatch(r"([A-Z]*)(\d+)", str(etype).strip().upper())
    number = int(match.group(2)) if match else 0
    if number not in _ELEMENTS or (
        match and match.group(1) and _ELEMENTS[number][0] != match.group(0)
    ):
        supported = ", ".join(name for name, _ in sorted(_ELEMENTS.values()))
        raise ValueError(
            f"Unsupported element type {etype!r}. Supported element types: {supported}."
        )
    return number


def _cell_type(key: Any) -> CellType:
    if isinstance(key, str):
        name = key.strip()
        if name.lower() in _MESHIO_CELL_TYPES:
            return _MESHIO_CELL_TYPES[name.lower()]
        if name.upper() in CellType.__members__:
            return CellType[name.upper()]
        raise ValueError(f"Unknown cell type key {key!r} in `etype` mapping.")
    return CellType(int(key))


def _check_compatible(number: int, celltype: int) -> None:
    if number not in _ELEMENTS:
        _element_number(number)
    name, layout = _ELEMENTS[number]
    if celltype not in _LAYOUTS[layout]:
        supported = ", ".join(c.name for c in _LAYOUTS[layout])
        raise ValueError(
            f"Element type {name} cannot represent {CellType(celltype).name} cells; "
            f"it supports {supported} cells."
        )


def _valid_ids(values: Any, allow_synthetic: bool) -> NDArray[np.int64] | None:
    """Return integral, positive, unique IDs (``-1`` mapped to ``0`` when allowed)."""
    if values is None:
        return None
    arr = np.asarray(values)
    if arr.ndim != 1 or not np.array_equal(arr, np.round(arr)):
        return None
    ids = arr.astype(np.int64)
    real = ids[ids != -1] if allow_synthetic else ids
    if (real <= 0).any() or np.unique(real).size != real.size:
        return None
    return np.where(ids == -1, 0, ids)


def _cell_attribute(
    grid: pv.UnstructuredGrid,
    value: Any,
    key: str,
    name: str,
    minimum: int,
    default: int,
) -> NDArray[np.int64]:
    n_cells = grid.n_cells
    if value is None:
        stored = grid.cell_data.get(key)
        if stored is not None:
            stored = np.asarray(stored)
            if (
                stored.ndim == 1
                and np.array_equal(stored, np.round(stored))
                and (stored >= minimum).all()
            ):
                return stored.astype(np.int64)
        return np.full(n_cells, default, np.int64)

    arr = np.asarray(value)
    if (
        not np.issubdtype(arr.dtype, np.integer)
        or arr.ndim > 1
        or (arr.ndim == 1 and arr.size != n_cells)
    ):
        raise ValueError(
            f"`{name}` must be an integer or a sequence of {n_cells} integers "
            "(one per element)."
        )
    if (arr < minimum).any():
        raise ValueError(f"`{name}` values must be greater than or equal to {minimum}.")
    return np.broadcast_to(arr, (n_cells,)).astype(np.int64)


def _resolve_element_types(
    grid: pv.UnstructuredGrid,
    etype: Any,
    existing_etypes: Mapping[int, int],
    et_offset: int,
    keyopt: Mapping[int, int] | None,
) -> tuple[
    NDArray[np.int64], NDArray[np.int64], dict[int, int], dict[int, dict[int, int]]
]:
    """Return per-cell ET IDs, element numbers, new ET definitions, and their KEYOPTs."""
    celltypes = np.asarray(grid.celltypes, np.int64)
    stored_ids = _valid_ids(grid.cell_data.get("ansys_etype"), allow_synthetic=False)
    stored_nums = _valid_ids(
        grid.cell_data.get("ansys_elem_type_num"), allow_synthetic=False
    )
    keyopts: dict[int, dict[int, int]] = {}

    if etype is None and stored_ids is not None and stored_nums is not None:
        pairs = np.unique(np.column_stack([stored_ids, stored_nums]), axis=0)
        if np.unique(pairs[:, 0]).size != len(pairs):
            raise ValueError("`ansys_etype` maps one ET ID to several element types.")
        etype_ids = stored_ids + et_offset
        numbers = stored_nums
        et_defs = {int(i) + et_offset: int(n) for i, n in pairs}
        rows = grid.field_data.get("ansys_keyopt")
        for et_id, knum, val in np.asarray(
            rows if rows is not None else [], np.int64
        ).reshape(-1, 3):
            if et_id + et_offset in et_defs:
                keyopts.setdefault(int(et_id) + et_offset, {})[int(knum)] = int(val)
    else:
        etype_ids = np.empty(celltypes.size, np.int64)
        numbers = np.empty(celltypes.size, np.int64)
        new_ids: dict[int, int] = {}
        _, first = np.unique(celltypes, return_index=True)
        for celltype in celltypes[np.sort(first)]:
            if celltype not in _DEFAULT_ELEMENTS:
                raise ValueError(
                    f"Unsupported VTK cell type {CellType(celltype).name} for a Mesh Archive."
                )
            target = etype
            if isinstance(etype, Mapping):
                target = next(
                    (v for k, v in etype.items() if _cell_type(k) == celltype), None
                )
            if _is_int(target):
                et_id = int(target)
                number = existing_etypes[et_id]
            else:
                number = (
                    _DEFAULT_ELEMENTS[celltype]
                    if target is None
                    else _element_number(target)
                )
                et_id = new_ids.setdefault(number, et_offset + len(new_ids) + 1)
            mask = celltypes == celltype
            etype_ids[mask] = et_id
            numbers[mask] = number
        et_defs = {et_id: number for number, et_id in new_ids.items()}

    for celltype, number in np.unique(np.column_stack([celltypes, numbers]), axis=0):
        _check_compatible(int(number), int(celltype))

    for knum, val in (keyopt or {}).items():
        if not (_is_int(knum) and 1 <= knum <= 18 and _is_int(val)):
            raise ValueError(
                "`keyopt` must map KEYOPT numbers (1 to 18) to integer values."
            )
        for et_id in et_defs:
            keyopts.setdefault(et_id, {})[int(knum)] = int(val)
    return etype_ids, numbers, et_defs, keyopts


def _connectivity(
    grid: pv.UnstructuredGrid, numbers: NDArray[np.int64], point_ids: NDArray[np.int64]
) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    celltypes = np.asarray(grid.celltypes, np.int64)
    offsets = pv.convert_array(grid.GetCells().GetOffsetsArray()).astype(np.int64)
    cell_points = np.asarray(grid.cell_connectivity, np.int64)
    connectivity = np.zeros((grid.n_cells, 20), np.int64)
    nnodes = np.zeros(grid.n_cells, np.int64)
    for celltype, number in np.unique(np.column_stack([celltypes, numbers]), axis=0):
        layout = _ELEMENTS[int(number)][1]
        perm = np.array(_LAYOUTS[layout][CellType(int(celltype))])
        idx = np.flatnonzero((celltypes == celltype) & (numbers == number))
        if (offsets[idx + 1] - offsets[idx] != perm.max() + 1).any():
            raise ValueError(
                f"{CellType(int(celltype)).name} cells must have {perm.max() + 1} points."
            )
        connectivity[idx, : perm.size] = point_ids[
            cell_points[offsets[idx][:, None] + perm]
        ]
        nnodes[idx] = perm.size
        if (connectivity[idx, : _CORNER_SLOTS[layout]] == 0).any():
            raise ValueError(
                "Points with `ansys_node_num == -1` may only be used as omitted midside nodes."
            )
    return connectivity, nnodes


def _component_name(name: Any, sanitize: bool) -> str:
    clean = str(name).strip().upper()
    if sanitize:
        clean = re.sub(r"[^A-Z0-9_]+", "_", clean)
        if not clean[:1].isalpha():
            clean = f"C_{clean}"
        clean = clean[:32]
    if not _COMPONENT_NAME.fullmatch(clean):
        raise ValueError(
            f"Invalid Mesh Component name {name!r}: names must start with a letter, "
            "contain only letters, digits, or underscores, and have at most 32 "
            "characters. Pass `sanitize_names=True` to clean names automatically."
        )
    return clean


def _is_mask(arr: NDArray[Any]) -> bool:
    return arr.ndim == 1 and (
        arr.dtype == np.bool_ or (arr.dtype == np.uint8 and arr.max(initial=0) <= 1)
    )


def _component_ids(
    kind: str, values: Any, ids: NDArray[np.int64], name: Any
) -> NDArray[np.int64]:
    arr = np.asarray(values)
    if arr.dtype == np.bool_:
        if arr.shape != ids.shape:
            raise ValueError(
                f"Boolean mask for Mesh Component {name!r} must have {ids.size} entries."
            )
        selected = ids[arr]
        return selected[selected > 0]
    if arr.ndim != 1 or (arr.size and not np.issubdtype(arr.dtype, np.integer)):
        raise ValueError(
            f"Mesh Component {name!r} must be a 1D sequence of {kind} IDs or a boolean mask."
        )
    missing = np.setdiff1d(arr, ids[ids > 0])
    if missing.size:
        raise ValueError(
            f"Mesh Component {name!r} references {kind} IDs not in the mesh: {missing[:10].tolist()}."
        )
    return np.unique(arr.astype(np.int64))


def _collect_components(
    grid: pv.UnstructuredGrid,
    point_ids: NDArray[np.int64],
    elem_ids: NDArray[np.int64],
    components: Mapping[str, Any] | None,
    include_components: bool,
    sanitize_names: bool,
) -> dict[str, tuple[str, NDArray[np.int64]]]:
    sources: list[tuple[str, Any, str, Any]] = []
    if include_components:
        for data, kind in ((grid.point_data, "NODE"), (grid.cell_data, "ELEM")):
            for key in data.keys():
                arr = np.asarray(data[key])
                if not _INTERNAL_ARRAY.fullmatch(key) and _is_mask(arr):
                    sources.append(("embedded", key, kind, arr.astype(np.bool_)))
    for key, value in (components or {}).items():
        kind, ids = "NODE", value
        if isinstance(value, tuple) and len(value) == 2 and isinstance(value[0], str):
            kind = _COMPONENT_KINDS.get(value[0].strip().upper(), "")
            ids = value[1]
            if not kind:
                raise ValueError(
                    f"Mesh Component {key!r} type must be 'NODE' or 'ELEM', not {value[0]!r}."
                )
        sources.append(("explicit", key, kind, ids))

    result: dict[str, tuple[str, NDArray[np.int64]]] = {}
    origin: dict[str, tuple[str, Any]] = {}
    for source, key, kind, values in sources:
        name = _component_name(key, sanitize_names)
        if name in result:
            if result[name][0] != kind:
                raise ValueError(
                    f"Mesh Component name {name!r} is used for both NODE and ELEM "
                    "components; Mechanical APDL shares one component namespace."
                )
            if origin[name][0] == source:
                raise ValueError(
                    f"Mesh Component names {origin[name][1]!r} and {key!r} both map to {name!r}."
                )
        ids = _component_ids(
            kind, values, point_ids if kind == "NODE" else elem_ids, key
        )
        result[name] = (kind, ids)
        origin[name] = (source, key)
    return {name: comp for name, comp in result.items() if comp[1].size}


def _mesh_data_from_grid(
    grid: pv.UnstructuredGrid,
    *,
    etype: Any = None,
    existing_etypes: Mapping[int, int] | None = None,
    et_offset: int = 0,
    mat: Any = None,
    real: Any = None,
    secnum: Any = None,
    esys: Any = None,
    keyopt: Mapping[int, int] | None = None,
    components: Mapping[str, Any] | None = None,
    include_components: bool = True,
    sanitize_names: bool = False,
) -> _MeshData:
    """Normalize a PyVista unstructured grid into a Mesh Archive representation."""
    point_ids = _valid_ids(grid.point_data.get("ansys_node_num"), allow_synthetic=True)
    if point_ids is None:
        point_ids = np.arange(1, grid.n_points + 1, dtype=np.int64)
    elem_ids = _valid_ids(grid.cell_data.get("ansys_elem_num"), allow_synthetic=False)
    if elem_ids is None:
        elem_ids = np.arange(1, grid.n_cells + 1, dtype=np.int64)

    etype_ids, numbers, et_defs, keyopts = _resolve_element_types(
        grid, etype, existing_etypes or {}, et_offset, keyopt
    )
    connectivity, nnodes = _connectivity(grid, numbers, point_ids)

    real_points = point_ids > 0
    angles = grid.point_data.get("angles")
    node_angles = None
    if angles is not None and np.shape(angles) == (grid.n_points, 3) and np.any(angles):
        node_angles = np.asarray(angles, np.float64)[real_points]

    return _MeshData(
        node_ids=point_ids[real_points],
        nodes=np.asarray(grid.points, np.float64)[real_points],
        node_angles=node_angles,
        elem_ids=elem_ids,
        etype_ids=etype_ids,
        mat_ids=_cell_attribute(grid, mat, "ansys_material_type", "mat", 1, 1),
        real_ids=_cell_attribute(grid, real, "ansys_real_constant", "real", 1, 1),
        sec_ids=_cell_attribute(grid, secnum, "ansys_secnum", "secnum", 1, 1),
        esys_ids=_cell_attribute(grid, esys, "ansys_esys", "esys", 0, 0),
        connectivity=connectivity,
        nnodes=nnodes,
        et_defs=et_defs,
        keyopts=keyopts,
        components=_collect_components(
            grid, point_ids, elem_ids, components, include_components, sanitize_names
        ),
    )


def _offset_ids(data: _MeshData, node_offset: int, elem_offset: int) -> None:
    """Shift node and element IDs, connectivity, and Mesh Components in place."""
    data.node_ids += node_offset
    data.connectivity[data.connectivity > 0] += node_offset
    data.elem_ids += elem_offset
    data.components = {
        name: (kind, ids + (node_offset if kind == "NODE" else elem_offset))
        for name, (kind, ids) in data.components.items()
    }


def _compress_ids(ids: NDArray[np.int64]) -> NDArray[np.int64]:
    """Encode sorted IDs as CMBLOCK items, writing contiguous runs as ``a, -b``."""
    ids = np.unique(ids)
    breaks = np.flatnonzero(np.diff(ids) != 1) + 1
    starts = ids[np.r_[0, breaks]]
    ends = ids[np.r_[breaks - 1, ids.size - 1]]
    keep = np.column_stack([np.ones_like(starts, bool), ends != starts]).ravel()
    return np.column_stack([starts, -ends]).ravel()[keep]


def write_mesh_archive(data: _MeshData, path: str | Path) -> None:
    """Write ``data`` as a Mesh Archive readable by ``CDREAD,DB``."""
    largest = max(data.node_ids.max(initial=0), data.elem_ids.max(initial=0))
    width = max(10, len(str(largest)) + 1)
    int_fmt = f"%{width}d"
    # LF endings on every platform: remote Linux MAPDL and the archive reader expect them.
    with open(path, "w", newline="\n") as fid:
        fid.write("/PREP7\n")
        for et_id, number in data.et_defs.items():
            fid.write(f"ET,{et_id},{number}\n")
        for et_id, options in data.keyopts.items():
            for knum, value in options.items():
                fid.write(f"KEYOPT,{et_id},{knum},{value}\n")

        if data.node_ids.size:
            order = np.argsort(data.node_ids)
            columns = [data.nodes[order]]
            if data.node_angles is not None:
                columns.append(data.node_angles[order])
            values = np.column_stack(
                [data.node_ids[order], np.zeros((order.size, 2)), *columns]
            )
            n_float = values.shape[1] - 3
            fid.write(
                f"NBLOCK,6,SOLID,{data.node_ids.max()},{data.node_ids.size}\n"
                f"(3i{width},6e21.13e3)\n"
            )
            np.savetxt(
                fid, values, fmt=[int_fmt] * 3 + ["%21.13E"] * n_float, delimiter=""
            )
            fid.write(f"N,R5.3,LOC,{-1:{width}d},\n")

        if data.elem_ids.size:
            zeros = np.zeros_like(data.elem_ids)
            records = np.column_stack(
                [
                    data.mat_ids,
                    data.etype_ids,
                    data.real_ids,
                    data.sec_ids,
                    data.esys_ids,
                    zeros,
                    zeros,
                    zeros,
                    data.nnodes,
                    zeros,
                    data.elem_ids,
                    data.connectivity,
                ]
            )
            fid.write(
                f"EBLOCK,19,SOLID,{data.elem_ids.max()},{data.elem_ids.size}\n(19i{width})\n"
            )
            formats = {
                n: int_fmt * min(11 + n, 19)
                + "\n"
                + (int_fmt * (n - 8) + "\n" if n > 8 else "")
                for n in np.unique(data.nnodes).tolist()
            }
            for record, n in zip(records.tolist(), data.nnodes.tolist()):
                fid.write(formats[n] % tuple(record[: 11 + n]))
            fid.write(f"{-1:{width}d}\n")

        for name, (kind, ids) in data.components.items():
            items = _compress_ids(ids).tolist()
            fid.write(f"CMBLOCK,{name},{kind},{len(items)}\n(8i{width})\n")
            for start in range(0, len(items), 8):
                line = items[start : start + 8]
                fid.write(int_fmt * len(line) % tuple(line) + "\n")
