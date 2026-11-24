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
import os
from pathlib import Path
import re
import tempfile
from typing import Any

import numpy as np
from numpy.typing import NDArray
import pyvista as pv
from pyvista import CellType

from ansys.mapdl.core.mesh.mesh import _pack_keyopt_array

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

_LAYOUT_DIMENSIONS = {
    "point": 0,
    "line": 1,
    "line3": 1,
    "shell": 2,
    "shell8": 2,
    "brick": 3,
    "brick20": 3,
    "tet10": 3,
}
_CELL_DIMENSIONS = {
    celltype: _LAYOUT_DIMENSIONS[layout]
    for layout, cells in _LAYOUTS.items()
    for celltype in cells
}
_CELL_POINTS = {
    celltype: max(slots) + 1
    for cells in _LAYOUTS.values()
    for celltype, slots in cells.items()
}
# Raw element node counts that identify one cell shape, and those that need ``etype``.
_RAW_CELL_TYPES = {
    1: CellType.VERTEX,
    2: CellType.LINE,
    5: CellType.PYRAMID,
    10: CellType.QUADRATIC_TETRA,
    13: CellType.QUADRATIC_PYRAMID,
    15: CellType.QUADRATIC_WEDGE,
    20: CellType.QUADRATIC_HEXAHEDRON,
}
_AMBIGUOUS_SIZES = {
    3: "QUADRATIC_EDGE or TRIANGLE",
    4: "QUAD or TETRA",
    6: "QUADRATIC_TRIANGLE or WEDGE",
    8: "QUADRATIC_QUAD or HEXAHEDRON",
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
    "voxel": CellType.VOXEL,
    "pixel": CellType.PIXEL,
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
# ``meshio`` readers store metadata such as ``gmsh:bounding_entities`` as sets.
_MESHIO_METADATA = ("gmsh:", "medit:", "ansys:")


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


def _stored_etypes(
    grid: pv.UnstructuredGrid,
) -> tuple[NDArray[np.int64], NDArray[np.int64]] | None:
    """Return valid ``ansys_etype`` and ``ansys_elem_type_num`` cell arrays, if any."""
    arrays = [grid.cell_data.get(key) for key in ("ansys_etype", "ansys_elem_type_num")]
    for arr in arrays:
        if (
            arr is None
            or np.shape(arr) != (grid.n_cells,)
            or not np.array_equal(arr, np.round(arr))
            or (np.asarray(arr) <= 0).any()
        ):
            return None
    return np.asarray(arrays[0], np.int64), np.asarray(arrays[1], np.int64)


def _id_argument(values: Any, count: int, name: str) -> NDArray[np.int64]:
    arr = np.asarray(values)
    if (
        arr.shape != (count,)
        or not np.issubdtype(arr.dtype, np.integer)
        or (arr <= 0).any()
        or np.unique(arr).size != count
    ):
        raise ValueError(f"`{name}` must contain {count} unique positive integers.")
    return arr.astype(np.int64)


def _kept(value: Any, keep: NDArray[np.bool_]) -> Any:
    """Slice a per-cell argument given for every input cell down to the kept cells."""
    if value is None or np.ndim(value) != 1 or len(value) != keep.size:
        return value
    return np.asarray(value)[keep]


def _vtk_cells(sizes: NDArray[np.int64], connectivity: Any) -> NDArray[np.int64]:
    """Return the legacy VTK cell array ``[n0, p..., n1, p..., ...]``."""
    return np.insert(
        np.asarray(connectivity, np.int64), np.cumsum(sizes) - sizes, sizes
    )


def _cell_sizes(grid: pv.UnstructuredGrid) -> NDArray[np.int64]:
    return np.diff(pv.convert_array(grid.GetCells().GetOffsetsArray())).astype(np.int64)


def _drop_boundary_cells(
    grid: pv.UnstructuredGrid,
    etype: Any,
    keep_boundary_elements: bool,
    include_components: bool,
) -> tuple[pv.UnstructuredGrid, NDArray[np.bool_]]:
    """Drop lower-dimensional cells, turning their cell masks into point masks."""
    celltypes = np.asarray(grid.celltypes, np.int64)
    unique, inverse = np.unique(celltypes, return_inverse=True)
    # Unsupported cell types count as 3D so that their validation error still surfaces.
    dims = np.array([_CELL_DIMENSIONS.get(c, 3) for c in unique.tolist()])[inverse]
    keep = dims == dims.max(initial=0)
    if keep_boundary_elements or (etype is None and _stored_etypes(grid) is not None):
        keep[:] = True
    elif isinstance(etype, Mapping):
        keep |= np.isin(celltypes, [_cell_type(key) for key in etype])
    if keep.all():
        return grid, keep

    sizes = _cell_sizes(grid)
    connectivity = np.asarray(grid.cell_connectivity, np.int64)
    # Copy VTK-backed arrays: sharing them between datasets corrupts the heap.
    kept = pv.UnstructuredGrid(
        _vtk_cells(sizes[keep], connectivity[np.repeat(keep, sizes)]),
        celltypes[keep],
        np.array(grid.points),
    )
    for key in grid.point_data.keys():
        kept.point_data[key] = np.array(grid.point_data[key])
    for key in grid.field_data.keys():
        kept.field_data[key] = np.array(grid.field_data[key])
    for key in grid.cell_data.keys():
        arr = np.asarray(grid.cell_data[key])
        is_group = include_components and _is_mask(arr)
        dropped = arr.astype(bool) & ~keep if is_group else None
        if _INTERNAL_ARRAY.fullmatch(key) or dropped is None or not dropped.any():
            kept.cell_data[key] = arr[keep]
            continue
        if (arr.astype(bool) & keep).any():
            raise ValueError(
                f"Mesh Component {key!r} contains both elements and lower-dimensional "
                "boundary cells, which become a NODE component; Mechanical APDL shares "
                "one component namespace. Pass `keep_boundary_elements=True` or split "
                "the group."
            )
        points = np.zeros(grid.n_points, bool)
        points[connectivity[np.repeat(dropped, sizes)]] = True
        if key in kept.point_data:
            points |= np.asarray(kept.point_data[key]).astype(bool)
        kept.point_data[key] = points
    return kept, keep


def _coordinates(points: Any) -> NDArray[np.float64]:
    """Return a copy of ``(N, 2)`` or ``(N, 3)`` coordinates as ``(N, 3)``."""
    coords = np.array(points, np.float64)
    if coords.ndim != 2 or coords.shape[1] not in (2, 3):
        raise ValueError(
            f"Node coordinates must have shape (N, 2) or (N, 3), not {coords.shape}."
        )
    if coords.shape[1] == 2:
        return np.column_stack([coords, np.zeros(len(coords))])
    return coords


def _grid_from_meshio(mesh: Any) -> pv.UnstructuredGrid:
    """Convert a duck-typed ``meshio.Mesh`` without modifying it."""
    celltypes, dims, sizes, connectivity = [], [], [], []
    block_cells: list[NDArray[np.int64]] = []
    type_blocks: dict[str, list[NDArray[np.int64]]] = {}
    for block in mesh.cells:
        if block.type not in _MESHIO_CELL_TYPES:
            raise ValueError(f"Unsupported meshio cell type {block.type!r}.")
        data = np.asarray(block.data, np.int64)
        start = sum(cells.size for cells in block_cells)
        block_cells.append(np.arange(start, start + len(data)))
        type_blocks.setdefault(block.type, []).append(block_cells[-1])
        celltypes.append(np.full(len(data), _MESHIO_CELL_TYPES[block.type]))
        dims.append(
            np.full(len(data), _CELL_DIMENSIONS[_MESHIO_CELL_TYPES[block.type]])
        )
        sizes.append(np.full(len(data), data.shape[1]))
        connectivity.append(data.ravel())
    if not block_cells:
        raise ValueError("The meshio mesh has no cells.")
    type_cells = {kind: np.concatenate(blocks) for kind, blocks in type_blocks.items()}

    def by_cell(per_block: Any) -> list[tuple[NDArray[np.int64], NDArray[Any]]]:
        """Pair block-aligned or cell-type-keyed values with their global cell indices."""
        if isinstance(per_block, Mapping):
            pairs = [(type_cells[kind], v) for kind, v in per_block.items()]
        else:
            pairs = list(zip(block_cells, per_block))
        return [(cells, np.ravel(v)) for cells, v in pairs if v is not None]

    grid = pv.UnstructuredGrid(
        _vtk_cells(np.concatenate(sizes), np.concatenate(connectivity)),
        np.concatenate(celltypes),
        _coordinates(mesh.points),
    )
    for name, indices in (getattr(mesh, "point_sets", None) or {}).items():
        if str(name).startswith(_MESHIO_METADATA):
            continue
        points = np.zeros(grid.n_points, bool)
        points[np.asarray(indices, np.int64)] = True
        grid.point_data[str(name)] = points

    masks: dict[str, NDArray[np.bool_]] = {}
    for name, per_block in (getattr(mesh, "cell_sets", None) or {}).items():
        if str(name).startswith(_MESHIO_METADATA):
            continue
        for cells, local in by_cell(per_block):
            masks.setdefault(str(name), np.zeros(grid.n_cells, bool))[
                cells[local.astype(np.int64)]
            ] = True
    tags = (getattr(mesh, "cell_data", None) or {}).get("gmsh:physical")
    if tags is None:
        tags = (getattr(mesh, "cell_data_dict", None) or {}).get("gmsh:physical")
    if tags is not None:
        physical = np.zeros(grid.n_cells, np.int64)
        for cells, local in by_cell(tags):
            physical[cells] = local
        cell_dims = np.concatenate(dims)
        for name, value in (getattr(mesh, "field_data", None) or {}).items():
            tag_dim = np.ravel(value)
            if tag_dim.size == 2:
                group = (physical == tag_dim[0]) & (cell_dims == tag_dim[1])
                masks[str(name)] = masks.get(str(name), group) | group
    for name, mask in masks.items():
        grid.cell_data[name] = mask
    return grid


def _raw_cell_type(
    size: int, etype: Any, existing_etypes: Mapping[int, int]
) -> CellType:
    """Return the cell type of raw ``size``-node elements, using ``etype`` if ambiguous."""
    if size in _RAW_CELL_TYPES:
        return _RAW_CELL_TYPES[size]
    if size not in _AMBIGUOUS_SIZES:
        raise ValueError(f"{size}-node elements are not supported.")
    if etype is None:
        raise ValueError(
            f"{size}-node elements are ambiguous ({_AMBIGUOUS_SIZES[size]}); "
            "pass `etype` to choose the element type."
        )
    if isinstance(etype, Mapping):
        candidates = list(dict.fromkeys(_cell_type(key) for key in etype))
    else:
        number = existing_etypes[int(etype)] if _is_int(etype) else etype
        candidates = list(_LAYOUTS[_ELEMENTS[_element_number(number)][1]])
    matches = [c for c in candidates if _CELL_POINTS.get(c) == size]
    if not matches:
        raise ValueError(
            f"Element type {etype!r} does not support {size}-node elements."
        )
    return matches[0]


def _grid_from_arrays(
    nodes: Any, elements: Any, etype: Any, existing_etypes: Mapping[int, int]
) -> pv.UnstructuredGrid:
    """Build a grid from coordinates and 0-based element node indices."""
    points = _coordinates(nodes)
    if isinstance(elements, np.ndarray) and elements.ndim == 2:
        sizes = np.full(len(elements), elements.shape[1], np.int64)
        connectivity = elements.ravel()
    else:
        cells = [np.asarray(cell) for cell in elements]
        if any(cell.ndim != 1 for cell in cells):
            raise ValueError(
                "`elements` must be a 2D array or a sequence of 1D node index arrays."
            )
        sizes = np.array([cell.size for cell in cells], np.int64)
        connectivity = np.concatenate(cells) if cells else np.empty(0, np.int64)
    if not sizes.size:
        raise ValueError("`elements` must contain at least one element.")
    if (sizes == 0).any():
        raise ValueError("Every element must be a non-empty sequence of node indices.")
    if not np.issubdtype(connectivity.dtype, np.integer):
        raise ValueError("Element node indices must be integers.")

    owner = np.repeat(np.arange(sizes.size), sizes)
    outside = (connectivity < 0) | (connectivity >= len(points))
    if outside.any():
        raise ValueError(
            f"Element {owner[outside][0]} references node indices outside "
            f"[0, {len(points)})."
        )
    order = np.lexsort((connectivity, owner))
    repeated = (np.diff(connectivity[order]) == 0) & (np.diff(owner[order]) == 0)
    if repeated.any():
        raise ValueError(
            f"Element {owner[order][1:][repeated][0]} repeats node indices."
        )

    unique, inverse = np.unique(sizes, return_inverse=True)
    celltypes = np.array(
        [_raw_cell_type(int(size), etype, existing_etypes) for size in unique]
    )[inverse]
    return pv.UnstructuredGrid(_vtk_cells(sizes, connectivity), celltypes, points)


def _expand_etblock(text: str) -> str:
    """Rewrite ``ETBLOCK`` rows, which ``Archive`` cannot parse, as ``ET`` and ``KEYOPT``."""
    lines = iter(text.splitlines())
    out = []
    for line in lines:
        if not line.upper().startswith("ETBLOCK"):
            out.append(line)
            continue
        next(lines)  # Format line.
        for row in lines:
            fields = [int(field) for field in row.split()]
            if fields[0] == -1:
                break
            et_id, number, *keyopts = fields
            out.append(f"ET,{et_id},{number}")
            out.extend(
                f"KEYOPT,{et_id},{knum},{value}"
                for knum, value in enumerate(keyopts[:18], 1)
                if value
            )
    return "\n".join(out) + "\n"


def _grid_from_cdb(path: Path, passthrough: bool) -> pv.UnstructuredGrid | Path:
    """Read a ``.cdb`` file with its metadata, or return ``path`` to ``CDREAD`` it as is."""
    from ansys.mapdl.reader import Archive

    with tempfile.TemporaryDirectory() as tmpdir:
        clean = Path(tmpdir) / "mesh.cdb"
        clean.write_text(
            _expand_etblock(path.read_text(encoding="latin-1")),
            encoding="latin-1",
            newline="\n",
        )
        archive = Archive(clean, force_linear=False)
    numbers = set(np.asarray(archive.ekey, np.int64).reshape(-1, 2)[:, 1].tolist())
    if passthrough and not numbers <= _ELEMENTS.keys():
        return path
    for number in sorted(numbers):
        _element_number(number)
    grid = archive.grid
    grid.cell_data["ansys_secnum"] = archive.section
    grid.cell_data["ansys_esys"] = archive.element_coord_system()
    keyopts = _pack_keyopt_array(archive.key_option)
    if keyopts.size:
        grid.field_data["ansys_keyopt"] = keyopts
    return grid


def _require_meshio(action: str, suffix: str) -> Any:
    try:
        import meshio
    except ImportError as err:
        raise ImportError(
            f"{action} '{suffix}' meshes requires the optional 'meshio' package. "
            "Install it with `pip install meshio`."
        ) from err
    return meshio


def _read_mesh_file(path: Path, passthrough: bool) -> Any:
    """Read a mesh file into a PyVista dataset, a ``meshio.Mesh``, or a passthrough path."""
    if not path.is_file():
        raise FileNotFoundError(f"Mesh file '{path}' does not exist.")
    suffix = path.suffix.lower()
    if suffix in (".cdb", ".inp"):
        return _grid_from_cdb(path, passthrough)
    if suffix in (".vtk", ".vtu", ".vtp", ".pvtu"):
        return pv.read(path)
    return _require_meshio("Reading", suffix).read(path)


def _as_grid(
    mesh: Any, etype: Any, existing_etypes: Mapping[int, int], passthrough: bool
) -> pv.UnstructuredGrid | Path:
    """Convert a ``load_mesh`` input into a grid, or a ``.cdb`` path to read as is."""
    if isinstance(mesh, (str, os.PathLike)):
        mesh = _read_mesh_file(Path(mesh), passthrough)
    if isinstance(mesh, (pv.UnstructuredGrid, Path)):
        return mesh
    if isinstance(mesh, pv.DataSet):
        return mesh.cast_to_unstructured_grid()
    if isinstance(mesh, tuple) and len(mesh) == 2:
        return _grid_from_arrays(*mesh, etype, existing_etypes)
    if hasattr(mesh, "points") and hasattr(mesh, "cells"):
        return _grid_from_meshio(mesh)
    raise TypeError(
        "`mesh` must be a PyVista dataset, a meshio.Mesh, a (nodes, elements) "
        f"tuple, or a mesh file path, not {type(mesh).__name__}."
    )


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
    stored = _stored_etypes(grid) if etype is None else None
    keyopts: dict[int, dict[int, int]] = {}

    if stored is not None:
        stored_ids, stored_nums = stored
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
        for et_id in np.unique(etype_ids).tolist():
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
        # ``linear_copy()`` keeps the midside point IDs after the corner ones.
        if (offsets[idx + 1] - offsets[idx] < perm.max() + 1).any():
            raise ValueError(
                f"{CellType(int(celltype)).name} cells must have at least {perm.max() + 1} points."
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
    keep_boundary_elements: bool = False,
    sanitize_names: bool = False,
    node_ids: Any = None,
    elem_ids: Any = None,
) -> _MeshData:
    """Normalize a PyVista unstructured grid into a Mesh Archive representation."""
    grid, keep = _drop_boundary_cells(
        grid, etype, keep_boundary_elements, include_components
    )
    mat, real, secnum, esys, elem_ids = (
        _kept(value, keep) for value in (mat, real, secnum, esys, elem_ids)
    )
    if node_ids is not None:
        point_ids = _id_argument(node_ids, grid.n_points, "node_ids")
    else:
        point_ids = _valid_ids(
            grid.point_data.get("ansys_node_num"), allow_synthetic=True
        )
        if point_ids is None:
            point_ids = np.arange(1, grid.n_points + 1, dtype=np.int64)
    if elem_ids is not None:
        elem_ids = _id_argument(elem_ids, grid.n_cells, "elem_ids")
    else:
        elem_ids = _valid_ids(
            grid.cell_data.get("ansys_elem_num"), allow_synthetic=False
        )
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


def _mesh_components(mesh: Any) -> dict[str, tuple[str, NDArray[np.int64]]]:
    """Return the NODE and ELEM Mesh Components of a ``MeshGrpc`` or ``Archive`` mesh."""
    components = {}
    for kind, items in (
        ("NODE", mesh.node_components),
        ("ELEM", mesh.element_components),
    ):
        for name, ids in items.items():
            # Hidden ``_`` names include temporaries such as the ``save_selection`` ones.
            if not name.startswith("_"):
                components[name] = (kind, np.asarray(ids, np.int64))
    return components


def _add_component_masks(grid: pv.UnstructuredGrid, mesh: Any) -> None:
    """Add one boolean mask per NODE and ELEM Mesh Component of ``mesh`` to ``grid``."""
    for name, (kind, ids) in _mesh_components(mesh).items():
        if kind == "NODE":
            grid.point_data[name] = np.isin(grid.point_data["ansys_node_num"], ids)
        else:
            grid.cell_data[name] = np.isin(grid.cell_data["ansys_elem_num"], ids)


def _mesh_grid(
    mesh: Any, include_components: bool, force_linear: bool
) -> pv.UnstructuredGrid:
    """Convert the selected part of a ``MeshGrpc`` or ``Archive`` mesh into a grid."""
    if hasattr(mesh, "to_pyvista"):
        grid = mesh.to_pyvista(
            include_components=include_components,
            selected_only=True,
            force_linear=force_linear,
        )
    else:
        from ansys.mapdl.core.mesh.mesh import _parse_vtk

        grid = _parse_vtk(mesh, force_linear=force_linear)
        if include_components and grid.n_points:
            _add_component_masks(grid, mesh)
    if not grid.n_cells:
        raise ValueError("The mesh is empty, hence no file has been written.")
    return grid


def _write_meshio(grid: pv.UnstructuredGrid, path: Path) -> None:
    """Write ``grid`` with ``meshio``, as point sets, cell sets, and ``ansys_*`` cell data."""
    meshio = _require_meshio("Exporting", path.suffix.lower())
    names = {celltype: name for name, celltype in _MESHIO_CELL_TYPES.items()}
    celltypes = np.asarray(grid.celltypes)
    offsets = pv.convert_array(grid.GetCells().GetOffsetsArray()).astype(np.int64)
    connectivity = np.asarray(grid.cell_connectivity, np.int64)
    _, first = np.unique(celltypes, return_index=True)
    blocks, cells = [], []
    for celltype in celltypes[np.sort(first)]:
        if celltype not in names:
            raise ValueError(
                f"{CellType(celltype).name} cells cannot be exported with meshio."
            )
        idx = np.flatnonzero(celltypes == celltype)
        size = _CELL_POINTS[celltype]  # ``linear_copy()`` cells keep extra point IDs.
        blocks.append(idx)
        cells.append(
            (names[celltype], connectivity[offsets[idx][:, None] + np.arange(size)])
        )

    point_sets, cell_sets, cell_data = {}, {}, {}
    for key in grid.point_data.keys():
        arr = np.asarray(grid.point_data[key])
        if not _INTERNAL_ARRAY.fullmatch(key) and _is_mask(arr):
            point_sets[key] = np.flatnonzero(arr)
    for key in grid.cell_data.keys():
        arr = np.asarray(grid.cell_data[key])
        if key.startswith("ansys_"):
            cell_data[key] = [arr[idx] for idx in blocks]
        elif not _INTERNAL_ARRAY.fullmatch(key) and _is_mask(arr):
            cell_sets[key] = [np.flatnonzero(arr[idx]) for idx in blocks]
    mesh = meshio.Mesh(
        np.asarray(grid.points, np.float64),
        cells,
        point_sets=point_sets,
        cell_sets=cell_sets,
        cell_data=cell_data,
    )
    meshio.write(str(path), mesh)


def _mesh_data_from_mesh(mesh: Any, include_components: bool) -> _MeshData:
    """Normalize the raw records of a ``MeshGrpc`` or ``Archive`` mesh losslessly."""
    records = [np.asarray(record, np.int64) for record in mesh.elem]
    if not records:
        raise ValueError("The mesh is empty, hence no file has been written.")
    header = np.array([record[:10] for record in records])
    # Trailing omitted (``0``) node slots are dropped, as ``CDWRITE`` does.
    cell_nodes = [np.trim_zeros(record[10:], "b") for record in records]
    nnodes = np.array([ids.size for ids in cell_nodes], np.int64)
    if nnodes.max() > 20:
        raise ValueError("Elements with more than 20 nodes cannot be exported.")
    connectivity = np.zeros((len(records), 20), np.int64)
    for row, ids in zip(connectivity, cell_nodes):
        row[: ids.size] = ids

    node_ids = np.asarray(mesh.nnum, np.int64)
    if not np.isin(connectivity[connectivity > 0], node_ids).all():
        raise ValueError(
            "The selected elements use unselected nodes. Select them with "
            "`mapdl.nsle('A')` or pass `selected_only=False`."
        )
    elem_ids = header[:, 8]
    angles = getattr(mesh, "node_angles", None)
    if angles is not None and (
        np.shape(angles) != (node_ids.size, 3) or not np.any(angles)
    ):
        angles = None

    components = {}
    if include_components:
        for name, (kind, ids) in _mesh_components(mesh).items():
            ids = np.intersect1d(ids, node_ids if kind == "NODE" else elem_ids)
            if ids.size:
                components[name] = (kind, ids)
    return _MeshData(
        node_ids=node_ids,
        nodes=np.asarray(mesh.nodes, np.float64).reshape(-1, 3),
        node_angles=angles,
        elem_ids=elem_ids,
        etype_ids=header[:, 1],
        mat_ids=header[:, 0],
        real_ids=header[:, 2],
        sec_ids=header[:, 3],
        esys_ids=header[:, 4],
        connectivity=connectivity,
        nnodes=nnodes,
        et_defs={int(et_id): int(number) for et_id, number in mesh.ekey},
        keyopts={
            int(et_id): {int(knum): int(value) for knum, value in options}
            for et_id, options in mesh.key_option.items()
        },
        components=components,
    )


def _compress_ids(ids: NDArray[np.int64]) -> NDArray[np.int64]:
    """Encode sorted IDs as CMBLOCK items, writing contiguous runs as ``a, -b``."""
    ids = np.unique(ids)
    breaks = np.flatnonzero(np.diff(ids) != 1) + 1
    starts = ids[np.r_[0, breaks]]
    ends = ids[np.r_[breaks - 1, ids.size - 1]]
    keep = np.column_stack([np.ones_like(starts, bool), ends != starts]).ravel()
    return np.column_stack([starts, -ends]).ravel()[keep]


def _write_mesh_archive(data: _MeshData, path: str | Path) -> None:
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
