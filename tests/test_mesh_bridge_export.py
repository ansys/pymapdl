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

"""Offline tests of ``Mapdl.export_mesh`` and ``MeshGrpc.export`` round trips."""

from contextlib import nullcontext
import shutil
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

from ansys.mapdl.reader import Archive
import numpy as np
import pytest

pv = pytest.importorskip("pyvista")

from ansys.mapdl.core.mapdl_console import MapdlConsole
from test_mesh_bridge_grid import (
    HEX_CORNERS,
    HEX_EDGES,
    TET_CORNERS,
    TET_EDGES,
    _component_mapdl,
    _FakeMapdl,
    _quadratic_points,
)
from test_mesh_bridge_load import _CDWRITE_26_1, _ArchiveMapdl


def _two_tet_points():
    return np.vstack(
        [_quadratic_points(TET_CORNERS, TET_EDGES, shift=2.0 * eid) for eid in (1, 2)]
    )


def test_export_cdb_round_trips_whole_model_with_unselected_components(tmp_path):
    mapdl = _component_mapdl()

    path = mapdl.export_mesh(tmp_path / "model.CDB")

    assert path == (tmp_path / "model.CDB").resolve()
    mesh = _ArchiveMapdl().load_mesh(path)
    np.testing.assert_array_equal(mesh.nnum, np.arange(1, 21))
    np.testing.assert_allclose(mesh.nodes, _two_tet_points(), atol=1e-12)
    np.testing.assert_array_equal(mesh.enum, [1, 2])
    np.testing.assert_array_equal(mesh.section, [1, 3])
    np.testing.assert_array_equal(mesh.element_coord_system(), [0, 11])
    np.testing.assert_array_equal(mesh.ekey, [[1, 187]])
    assert [e[10:].tolist() for e in mesh.elem] == [
        list(range(1, 11)),
        list(range(11, 21)),
    ]
    assert mesh.node_components["LEFT"].tolist() == [1, 2, 3]
    assert mesh.element_components["SECOND"].tolist() == [2]


def test_export_restores_caller_selection(tmp_path):
    mapdl = _component_mapdl()
    before = (set(mapdl.nsel_ids), set(mapdl.esel_ids), set(mapdl.cmsel_names))
    assert mapdl.mesh.nnum.tolist() == [11]  # warm the selection-bound cache

    mapdl.export_mesh(tmp_path / "model.cdb")

    assert (mapdl.nsel_ids, mapdl.esel_ids, mapdl.cmsel_names) == before
    assert set(mapdl.model_components) == {"LEFT", "SECOND"}
    assert mapdl.mesh.nnum.tolist() == [11]
    assert mapdl.mesh.enum.tolist() == [2]
    assert "__" not in (tmp_path / "model.cdb").read_text()


def test_export_selected_only_writes_active_selection(tmp_path):
    mapdl = _component_mapdl()
    mapdl.nsle("S")

    mesh = _ArchiveMapdl().load_mesh(
        mapdl.export_mesh(tmp_path / "model.cdb", selected_only=True)
    )

    np.testing.assert_array_equal(mesh.nnum, np.arange(11, 21))
    np.testing.assert_array_equal(mesh.enum, [2])
    assert mesh.node_components == {}
    assert mesh.element_components["SECOND"].tolist() == [2]
    assert mapdl.nsel_ids == set(range(11, 21))


def test_export_selected_only_rejects_elements_using_unselected_nodes(tmp_path):
    mapdl = _component_mapdl()

    with pytest.raises(ValueError, match="use unselected nodes"):
        mapdl.export_mesh(tmp_path / "model.cdb", selected_only=True)
    assert not (tmp_path / "model.cdb").exists()


def _hex_and_beam_mapdl():
    """Hex20 missing two midside nodes, and a BEAM189 with an orientation node."""
    points = _quadratic_points(HEX_CORNERS, HEX_EDGES)
    nodes = {i + 1: tuple(xyz) for i, xyz in enumerate(points) if i not in (8, 9)}
    nodes.update({30: (3, 0, 0), 31: (4, 0, 0), 32: (3.5, 0, 0), 33: (3, 1, 0)})
    hex_nodes = [i if i not in (9, 10) else 0 for i in range(1, 21)]
    elements = {
        1: dict(mat=2, type=1, real=3, secnum=4, esys=0, nodes=hex_nodes),
        5: dict(mat=1, type=2, real=1, secnum=7, esys=0, nodes=[30, 31, 32, 33]),
    }
    etypes = {1: (186, {2: 1}), 2: (189, {})}
    components = {"BEAM": ("ELEM", [5]), "ENDS": ("NODE", [1, 31])}
    return _FakeMapdl(nodes, elements, etypes, components)


def test_export_cdb_keeps_raw_element_records(tmp_path):
    mapdl = _hex_and_beam_mapdl()

    mesh = Archive(mapdl.export_mesh(tmp_path / "model.cdb"), parse_vtk=False)

    np.testing.assert_array_equal(mesh.ekey, [[1, 186], [2, 189]])
    assert mesh.key_option == {1: [[2, 1]]}
    np.testing.assert_array_equal(
        mesh.nnum, [*range(1, 9), *range(11, 21), 30, 31, 32, 33]
    )
    np.testing.assert_array_equal(mesh.enum, [1, 5])
    assert mesh.elem[0][:5].tolist() == [2, 1, 3, 4, 0]
    assert mesh.elem[0][10:].tolist() == [*range(1, 9), 0, 0, *range(11, 21)]
    assert mesh.elem[1][10:].tolist() == [30, 31, 32, 33]
    np.testing.assert_array_equal(mesh.section, [4, 7])
    assert mesh.element_components["BEAM"].tolist() == [5]
    assert mesh.node_components["ENDS"].tolist() == [1, 31]


def test_export_vtu_round_trips_through_load_mesh(tmp_path):
    mapdl = _component_mapdl()

    path = mapdl.export_mesh(tmp_path / "model.vtu")

    grid = pv.read(path)
    assert grid.celltypes.tolist() == [pv.CellType.QUADRATIC_TETRA] * 2
    assert np.flatnonzero(grid.point_data["LEFT"]).tolist() == [0, 1, 2]
    assert grid.cell_data["SECOND"].tolist() == [0, 1]
    assert grid.cell_data["ansys_esys"].tolist() == [0, 11]
    mesh = _ArchiveMapdl().load_mesh(path)
    np.testing.assert_array_equal(mesh.nnum, np.arange(1, 21))
    np.testing.assert_allclose(mesh.nodes, _two_tet_points(), atol=1e-12)
    np.testing.assert_array_equal(mesh.ekey, [[1, 187]])
    np.testing.assert_array_equal(mesh.section, [1, 3])
    assert mesh.node_components["LEFT"].tolist() == [1, 2, 3]
    assert mesh.element_components["SECOND"].tolist() == [2]


def test_export_legacy_vtk_as_ascii(tmp_path):
    mapdl = _component_mapdl()

    path = mapdl.export_mesh(tmp_path / "model.vtk", binary=False)

    assert "ASCII" in path.read_text().splitlines()[:3]
    assert pv.read(path).n_cells == 2


def _fake_meshio(monkeypatch):
    written = []
    meshio = SimpleNamespace(
        Mesh=lambda points, cells, **kwargs: SimpleNamespace(
            points=points, cells=cells, **kwargs
        ),
        write=lambda path, mesh: written.append((path, mesh)),
    )
    monkeypatch.setitem(sys.modules, "meshio", meshio)
    return written


def test_export_other_formats_with_meshio(tmp_path, monkeypatch):
    written = _fake_meshio(monkeypatch)
    mapdl = _hex_and_beam_mapdl()

    path = mapdl.export_mesh(tmp_path / "model.msh")

    [(target, mesh)] = written
    assert target == str(tmp_path / "model.msh")
    assert path == (tmp_path / "model.msh").resolve()
    assert [(kind, np.shape(cells)) for kind, cells in mesh.cells] == [
        ("hexahedron20", (1, 20)),
        ("line3", (1, 3)),
    ]
    np.testing.assert_allclose(
        mesh.points[mesh.cells[1][1][0]], [[3, 0, 0], [4, 0, 0], [3.5, 0, 0]]
    )
    np.testing.assert_allclose(
        mesh.points[mesh.point_sets["ENDS"]], [[0, 0, 0], [4, 0, 0]]
    )
    assert [ids.tolist() for ids in mesh.cell_sets["BEAM"]] == [[], [0]]
    data = {key: [v.tolist() for v in values] for key, values in mesh.cell_data.items()}
    assert data["ansys_elem_num"] == [[1], [5]]
    assert data["ansys_material_type"] == [[2], [1]]
    assert data["ansys_real_constant"] == [[3], [1]]
    assert data["ansys_secnum"] == [[4], [7]]
    assert data["ansys_esys"] == [[0], [0]]
    assert data["ansys_etype"] == [[1], [2]]
    assert data["ansys_elem_type_num"] == [[186], [189]]


def test_export_meshio_force_linear_writes_corner_nodes_only(tmp_path, monkeypatch):
    written = _fake_meshio(monkeypatch)

    _component_mapdl().export_mesh(tmp_path / "model.med", force_linear=True)

    [(_, mesh)] = written
    [(kind, cells)] = mesh.cells
    assert kind == "tetra"
    np.testing.assert_allclose(mesh.points[cells[1]], _two_tet_points()[10:14])


def test_export_other_formats_requires_meshio(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "meshio", None)

    with pytest.raises(
        ImportError, match="Exporting '.xdmf' meshes requires the optional 'meshio'"
    ):
        _component_mapdl().export_mesh(tmp_path / "model.XDMF")


@pytest.mark.parametrize("name", ["model.cdb", "model.vtu", "model.msh"])
def test_export_rejects_empty_mesh(tmp_path, monkeypatch, name):
    _fake_meshio(monkeypatch)

    with pytest.raises(ValueError, match="The mesh is empty"):
        _FakeMapdl().export_mesh(tmp_path / name)
    assert not (tmp_path / name).exists()


def test_export_force_linear_writes_linear_cells(tmp_path):
    mapdl = _component_mapdl()

    grid = pv.read(mapdl.export_mesh(tmp_path / "model.vtu", force_linear=True))
    mesh = Archive(mapdl.export_mesh(tmp_path / "model.cdb", force_linear=True))

    assert grid.celltypes.tolist() == [pv.CellType.TETRA] * 2
    np.testing.assert_array_equal(mesh.ekey, [[1, 185]])
    assert mesh.elem[1][10:].tolist() == [11, 12, 13, 13, 14, 14, 14, 14]
    np.testing.assert_array_equal(mesh.enum, [1, 2])
    np.testing.assert_array_equal(mesh.section, [1, 3])
    np.testing.assert_array_equal(mesh.element_coord_system(), [0, 11])
    assert mesh.node_components["LEFT"].tolist() == [1, 2, 3]
    assert mesh.element_components["SECOND"].tolist() == [2]


def test_export_skips_components_on_request(tmp_path):
    mapdl = _component_mapdl()

    mesh = Archive(mapdl.export_mesh(tmp_path / "model.cdb", include_components=False))
    grid = pv.read(mapdl.export_mesh(tmp_path / "model.vtu", include_components=False))

    assert mesh.node_components == {} and mesh.element_components == {}
    assert "LEFT" not in grid.point_data and "SECOND" not in grid.cell_data


def test_mesh_export_delegates_to_export_mesh(tmp_path):
    mapdl = _component_mapdl()
    calls = []
    mapdl.export_mesh = lambda *args, **kwargs: calls.append((args, kwargs)) or "out"

    out = mapdl.mesh.export(tmp_path / "m.vtu", selected_only=True, binary=False)

    assert out == "out"
    assert calls == [
        (
            (tmp_path / "m.vtu",),
            dict(
                include_components=True,
                selected_only=True,
                force_linear=False,
                binary=False,
            ),
        )
    ]


class _ConsoleMapdl(MapdlConsole):
    """Console session whose ``CDWRITE`` writes a MAPDL 2026 R1 ``CDWRITE,DB`` file."""

    def __init__(self, directory):
        self._log = MagicMock(level="CRITICAL")
        self._archive_cache = None
        self._path = directory
        self.commands = []

    def __del__(self):
        pass

    @property
    def directory(self):
        return self._path

    @property
    def save_selection(self):
        self.commands.append("SAVE_SELECTION")
        return nullcontext()

    def run(self, command, write_to_log=True, mute=None, **kwargs):
        self._reset_cache()
        self.commands.append(command.split(",")[0].upper())
        if command.upper().startswith("CDWRITE"):
            shutil.copy(_CDWRITE_26_1, command.split("'")[1])
        return ""


def test_export_archive_backed_console_mesh(tmp_path):
    mapdl = _ConsoleMapdl(tmp_path)

    cdb = Archive(mapdl.export_mesh(tmp_path / "model.cdb"), parse_vtk=False)
    grid = pv.read(mapdl.export_mesh(tmp_path / "model.vtu"))

    assert mapdl.commands[:3] == ["SAVE_SELECTION", "ALLSEL", "CMSEL"]
    np.testing.assert_array_equal(cdb.ekey, [[1, 186], [3, 181]])
    assert cdb.key_option == {1: [[2, 1]], 3: [[3, 2], [8, 2]]}
    np.testing.assert_array_equal(cdb.nnum, np.arange(1, 33))
    np.testing.assert_array_equal(cdb.enum, [1, 2, 3])
    assert cdb.elem[2][10:].tolist() == [4, 19, 15, 8]
    assert cdb.node_components["FIXED"].tolist() == [1, 2, 3, 14, 21, 25, 27, 31]
    assert cdb.element_components["SKIN"].tolist() == [3]
    assert "__" not in (tmp_path / "model.cdb").read_text()
    assert grid.celltypes.tolist() == [
        pv.CellType.QUADRATIC_HEXAHEDRON,
        pv.CellType.QUADRATIC_HEXAHEDRON,
        pv.CellType.QUAD,
    ]
    assert grid.cell_data["ansys_esys"].tolist() == [0, 0, 0]
    assert grid.cell_data["SKIN"].tolist() == [0, 0, 1]
    assert grid.point_data["FIXED"].sum() == 8
