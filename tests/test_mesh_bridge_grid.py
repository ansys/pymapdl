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

"""Offline tests of ``mapdl.mesh.grid`` and ``mapdl.mesh.to_pyvista`` over a fake MAPDL server."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import grpc
import numpy as np
import pytest

pv = pytest.importorskip("pyvista")

from ansys.mapdl.core.component import ComponentManager
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from ansys.mapdl.core.mesh_grpc import MeshGrpc

TET_CORNERS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
TET_EDGES = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
HEX_CORNERS = [
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 1),
    (0, 1, 1),
]
HEX_EDGES = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]


def _quadratic_points(corners, edges, shift=0.0):
    pts = np.array(corners, float) + [shift, 0.0, 0.0]
    return np.vstack([pts, [(pts[a] + pts[b]) / 2 for a, b in edges]])


class _Stream:
    """One-chunk gRPC response stream as consumed by ``parse_chunks``."""

    def __init__(self, array):
        self._chunks = [SimpleNamespace(payload=array.tobytes(), value_type=0)]
        if not array.size:
            self._chunks.clear()

    def is_active(self):
        return True

    def code(self):
        return grpc.StatusCode.OK

    def next(self):
        if not self._chunks:
            raise StopIteration
        return self._chunks.pop(0)

    def done(self):
        return not self._chunks

    def __iter__(self):
        return iter(self._chunks)


class _FakeMapdl(MapdlGrpc):
    """MAPDL server emulating node/element/component selection in memory."""

    path = ""  # MeshGrpc queries it on Windows; avoid a server round trip.

    def __init__(self, nodes=None, elements=None, etypes=None, components=None):
        self._log = MagicMock(level="CRITICAL")
        self._MapdlCore__exited = False
        self._save_selection_obj = None
        self._geometry = None
        self._store_commands = False
        self.commands = []

        self.model_nodes = nodes or {}
        self.model_elements = elements or {}
        self.model_etypes = etypes or {}
        self.model_components = {
            name: (kind, set(ids)) for name, (kind, ids) in (components or {}).items()
        }
        self.nsel_ids = set(self.model_nodes)
        self.esel_ids = set(self.model_elements)
        self.cmsel_names = set(self.model_components)

        self._stub = SimpleNamespace(
            Nodes=lambda request: _Stream(self._node_payload()),
            LoadElements=lambda request: _Stream(self._elem_payload()),
            LoadElementTypeDescription=lambda request: _Stream(self._etype_payload()),
        )
        self._componentmanager = ComponentManager(self)
        self._mesh_rep = MeshGrpc(self)

    def __del__(self):
        pass

    def _node_payload(self):
        coords = [self.model_nodes[i] for i in sorted(self.nsel_ids)]
        return np.asarray(coords, np.double).ravel()

    def _elem_payload(self):
        records = []
        for eid in sorted(self.esel_ids):
            elem = self.model_elements[eid]
            header = [elem["mat"], elem["type"], elem["real"], elem["secnum"]]
            header += [elem["esys"], 0, 0, 0, eid, 0]
            records.append(header + list(elem["nodes"]))
        offsets, start = [], len(records)
        for record in records:
            offsets.append(start)
            start += len(record)
        return np.array(offsets + sum(records, []), np.int32)

    def _etype_payload(self):
        records = []
        for et_id, (ansys_type, keyopts) in sorted(self.model_etypes.items()):
            keyopt = [0] * 18
            for knum, value in keyopts.items():
                keyopt[knum - 1] = value
            records.append([et_id, ansys_type, *keyopt])
        offsets, start = [], 1 + len(records)
        for record in records:
            offsets.append(start)
            start += len(record)
        return np.array([len(records), *offsets, *sum(records, [])], np.int32)

    def _entity_selection(self, entity):
        return {"NODE": self.nsel_ids, "ELEM": self.esel_ids}.get(entity, set())

    def _select(self, entity, type_, ids):
        current = self._entity_selection(entity)
        if type_ == "S":
            current.clear()
            current.update(ids)
        elif type_ == "A":
            current.update(ids)
        elif type_ == "U":
            current.difference_update(ids)

    def run(self, command, write_to_log=True, mute=None, **kwargs):
        self._reset_cache()
        self.commands.append(command)
        args = [arg.strip().upper() for arg in command.split(",")]
        args += [""] * 5
        cmd = args[0]
        if cmd == "ALLSEL":
            self.nsel_ids.update(self.model_nodes)
            self.esel_ids.update(self.model_elements)
        elif cmd == "CM":
            selected = set(self._entity_selection(args[2]))
            self.model_components[args[1]] = (args[2], selected)
            self.cmsel_names.add(args[1])
        elif cmd == "CMDELE":
            self.model_components.pop(args[1])
            self.cmsel_names.discard(args[1])
        elif cmd == "CMSEL":
            type_, name = args[1], args[2]
            if type_ == "ALL":
                self.cmsel_names.update(self.model_components)
            elif type_ == "NONE":
                self.cmsel_names.clear()
            else:
                kind, ids = self.model_components[name]
                self._select(kind, type_, ids)
                if type_ == "S":
                    self.cmsel_names.clear()
                if type_ == "U":
                    self.cmsel_names.discard(name)
                else:
                    self.cmsel_names.add(name)
        elif cmd in ("NSEL", "ESEL"):
            entity = "NODE" if cmd == "NSEL" else "ELEM"
            type_, item, vmin = args[1], args[2], args[4]
            if type_ == "ALL":
                self._select(entity, "S", self._all_ids(entity))
            elif type_ == "NONE":
                self._select(entity, "S", set())
            elif item == entity:
                self._select(entity, type_, {int(float(vmin))})
            elif not item and vmin in self.model_components:
                self._select(entity, type_, self.model_components[vmin][1])
        elif cmd == "NSLE":
            attached = {
                nid
                for eid in self.esel_ids
                for nid in self.model_elements[eid]["nodes"]
                if nid
            }
            self._select("NODE", args[1] or "S", attached)
        return ""

    def _all_ids(self, entity):
        return set(self.model_nodes if entity == "NODE" else self.model_elements)

    def get(self, par="__floatparameter__", entity="", entnum="", item1="", **kwargs):
        self._reset_cache()
        assert item1.upper() == "COUNT"
        return float(len(self._entity_selection(entity.upper())))

    def get_array(self, entity="", entnum="", item1="", **kwargs):
        self._reset_cache()
        ids = sorted(self._entity_selection(entity.upper())) or [0]
        return np.array(ids, float)

    def _parse_cmlist(self, cmlist=None):
        names = sorted(self.cmsel_names)
        return {name: self.model_components[name][0] for name in names}, {}

    def _parse_cmlist_indiv(self, cmname, cmtype, cmlist=None):
        return sorted(self.model_components[cmname.upper()][1])


def _single_element_mapdl(corners, edges, ansys_type):
    points = _quadratic_points(corners, edges)
    nodes = {i + 1: tuple(xyz) for i, xyz in enumerate(points)}
    element = dict(mat=1, type=1, real=1, secnum=1, esys=0, nodes=list(nodes))
    return _FakeMapdl(nodes, {1: element}, {1: (ansys_type, {})})


def _two_tet_mapdl(keyopts=None, components=None):
    nodes, elements = {}, {}
    for eid, (secnum, esys) in enumerate([(1, 0), (3, 11)], start=1):
        first = len(nodes) + 1
        points = _quadratic_points(TET_CORNERS, TET_EDGES, shift=2.0 * eid)
        nodes.update({first + i: tuple(xyz) for i, xyz in enumerate(points)})
        elements[eid] = dict(
            mat=1,
            type=1,
            real=1,
            secnum=secnum,
            esys=esys,
            nodes=list(range(first, first + 10)),
        )
    return _FakeMapdl(nodes, elements, {1: (187, keyopts or {})}, components)


@pytest.mark.parametrize(
    "corners,edges,ansys_type,celltype",
    [
        (TET_CORNERS, TET_EDGES, 187, pv.CellType.QUADRATIC_TETRA),
        (HEX_CORNERS, HEX_EDGES, 186, pv.CellType.QUADRATIC_HEXAHEDRON),
    ],
)
def test_grid_preserves_quadratic_cell_types(corners, edges, ansys_type, celltype):
    mapdl = _single_element_mapdl(corners, edges, ansys_type)

    grid = mapdl.mesh.grid

    assert grid.celltypes.tolist() == [celltype]
    assert grid.n_points == len(corners) + len(edges)


def test_grid_carries_section_esys_and_keyopt_metadata():
    mapdl = _two_tet_mapdl(keyopts={2: 1, 5: 3})

    grid = mapdl.mesh.grid

    assert grid.cell_data["ansys_secnum"].tolist() == [1, 3]
    assert grid.cell_data["ansys_esys"].tolist() == [0, 11]
    keyopt = grid.field_data["ansys_keyopt"]
    assert keyopt.dtype == np.int32
    assert keyopt.tolist() == [[1, 2, 1], [1, 5, 3]]


def test_grid_omits_keyopt_field_without_nonzero_key_options():
    mapdl = _two_tet_mapdl()
    assert "ansys_keyopt" not in mapdl.mesh.grid.field_data


def _component_mapdl():
    components = {"LEFT": ("NODE", [1, 2, 3]), "SECOND": ("ELEM", [2])}
    mapdl = _two_tet_mapdl(components=components)
    mapdl.cmsel("U", "LEFT")
    mapdl.allsel()
    mapdl.esel("S", "ELEM", "", 2)
    mapdl.nsel("S", "NODE", "", 11)
    return mapdl


def test_to_pyvista_exports_whole_model_with_unselected_components():
    mapdl = _component_mapdl()
    assert mapdl.mesh.enum.tolist() == [2]  # warm the selection-bound cache

    grid = mapdl.mesh.to_pyvista()

    assert grid.cell_data["ansys_elem_num"].tolist() == [1, 2]
    assert grid.point_data["ansys_node_num"].tolist() == list(range(1, 21))
    assert grid.celltypes.tolist() == [pv.CellType.QUADRATIC_TETRA] * 2
    left = grid.point_data["LEFT"]
    assert left.dtype == np.bool_
    assert np.flatnonzero(left).tolist() == [0, 1, 2]
    assert grid.cell_data["SECOND"].tolist() == [False, True]
    arrays = [*grid.point_data, *grid.cell_data]
    assert not [name for name in arrays if name.startswith("__")]


def test_to_pyvista_restores_caller_selection():
    mapdl = _component_mapdl()
    assert mapdl.mesh.nnum.tolist() == [11]  # warm the selection-bound cache

    mapdl.mesh.to_pyvista()

    assert mapdl.mesh.nnum.tolist() == [11]
    assert mapdl.mesh.enum.tolist() == [2]
    assert mapdl.mesh.node_components == {}
    assert list(mapdl.mesh.element_components) == ["SECOND"]
    assert set(mapdl.model_components) == {"LEFT", "SECOND"}


def test_to_pyvista_selected_only_exports_active_selection():
    mapdl = _component_mapdl()
    mapdl.nsle("S")

    grid = mapdl.mesh.to_pyvista(selected_only=True)

    assert grid.cell_data["ansys_elem_num"].tolist() == [2]
    assert grid.point_data["ansys_node_num"].tolist() == list(range(11, 21))
    assert "LEFT" not in grid.point_data
    assert grid.cell_data["SECOND"].tolist() == [True]
    assert mapdl.mesh.nnum.tolist() == list(range(11, 21))
    assert list(mapdl.mesh.element_components) == ["SECOND"]


def test_to_pyvista_force_linear_without_components():
    mapdl = _component_mapdl()

    grid = mapdl.mesh.to_pyvista(include_components=False, force_linear=True)

    assert grid.celltypes.tolist() == [pv.CellType.TETRA] * 2
    assert "LEFT" not in grid.point_data
    assert "SECOND" not in grid.cell_data


def test_to_pyvista_empty_model_returns_empty_grid():
    mapdl = _FakeMapdl()

    grid = mapdl.mesh.to_pyvista()

    assert isinstance(grid, pv.UnstructuredGrid)
    assert grid.n_points == 0
    assert grid.n_cells == 0
