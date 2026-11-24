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


"""Offline tests for ``Mapdl.load_mesh`` over an ``Archive``-backed MAPDL double."""

from pathlib import Path
from types import SimpleNamespace

from ansys.mapdl.reader import Archive
import numpy as np
import pytest
import pyvista as pv
from pyvista import CellType

from ansys.mapdl.core._mapdl_extended.mesh_bridge import _ExtendedMeshBridgeMixin
from ansys.mapdl.core.mapdl_console import MapdlConsole
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc


class _ArchiveMapdl(_ExtendedMeshBridgeMixin):
    """MAPDL double whose ``cdread`` parses the Mesh Archive with the real reader."""

    def __init__(self, node_max=0, elem_max=0, etypes=None, components=None):
        self.node_max = node_max
        self.elem_max = elem_max
        self.etypes = dict(etypes or {})
        self.components = dict(components or {})
        self.calls = []
        self.cdb = ""
        self.archive = None

    def get_value(self, entity, entnum, item1, it1num):
        assert (entnum, item1) == (0, "NUM")
        return float(
            {
                ("NODE", "MAXD"): self.node_max,
                ("ELEM", "MAXD"): self.elem_max,
                ("ETYP", "MAX"): max(self.etypes, default=0),
            }[(entity, it1num)]
        )

    def prep7(self, **kwargs):
        self.calls.append(("PREP7",))

    def allsel(self, **kwargs):
        self.calls.append(("ALLSEL",))

    def cmsel(self, type_, *args, **kwargs):
        self.calls.append(("CMSEL", type_))

    def cmdele(self, name, **kwargs):
        self.calls.append(("CMDELE", name))
        del self.components[name]

    def edele(self, iel1, **kwargs):
        self.calls.append(("EDELE", iel1))

    def ndele(self, node1, **kwargs):
        self.calls.append(("NDELE", node1))

    def cdread(self, option, fname):
        self.calls.append(("CDREAD", option))
        self.cdb = Path(fname).read_text()
        # Element types already in the database are visible to the reader too.
        database = Path(fname).with_name("database.cdb")
        predefined = "".join(f"ET,{i},{n}\n" for i, n in self.etypes.items())
        database.write_text(predefined + self.cdb, newline="\n")
        self.archive = Archive(database, force_linear=False)

    def _reset_cache(self):
        self.calls.append(("RESET",))

    @property
    def mesh(self):
        if self.archive is None:
            return SimpleNamespace(ekey=np.array(list(self.etypes.items())))
        return self.archive


def _single_cell(celltype, n_points, seed=0):
    points = np.random.default_rng(seed).random((n_points, 3))
    return pv.UnstructuredGrid(
        np.hstack([[n_points], np.arange(n_points)]), [celltype], points
    )


def _two_hexes():
    return pv.ImageData(dimensions=(3, 2, 2)).cast_to_unstructured_grid()


def _cell_nodes(mesh, index=0):
    return mesh.elem[index][10:].tolist()


def test_load_mesh_is_available_on_grpc_and_console_sessions():
    assert issubclass(MapdlGrpc, _ExtendedMeshBridgeMixin)
    assert issubclass(MapdlConsole, _ExtendedMeshBridgeMixin)


def test_load_mesh_hexahedron_round_trips_through_mesh_archive():
    grid = _single_cell(CellType.HEXAHEDRON, 8)
    mapdl = _ArchiveMapdl()

    mesh = mapdl.load_mesh(grid)

    assert mesh is mapdl.archive
    np.testing.assert_array_equal(mesh.nnum, np.arange(1, 9))
    np.testing.assert_allclose(mesh.nodes, grid.points, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(mesh.ekey, [[1, 185]])
    assert mesh.grid.celltypes.tolist() == [CellType.HEXAHEDRON]
    assert mapdl.calls[0] == ("PREP7",)
    assert ("CDREAD", "DB") in mapdl.calls
    assert mapdl.calls[-1] == ("RESET",)


@pytest.mark.parametrize(
    "celltype,n_points,etype,number,read_type,order",
    [
        (CellType.VERTEX, 1, None, 21, CellType.VERTEX, None),
        (CellType.LINE, 2, None, 188, CellType.LINE, None),
        (CellType.LINE, 2, "LINK180", 180, CellType.LINE, None),
        (CellType.QUADRATIC_EDGE, 3, None, 189, CellType.QUADRATIC_EDGE, None),
        (CellType.TRIANGLE, 3, None, 181, CellType.TRIANGLE, None),
        (CellType.TRIANGLE, 3, "PLANE182", 182, CellType.TRIANGLE, None),
        (CellType.QUAD, 4, None, 181, CellType.QUAD, None),
        (CellType.PIXEL, 4, None, 181, CellType.QUAD, [0, 1, 3, 2]),
        (CellType.QUADRATIC_TRIANGLE, 6, None, 281, CellType.QUADRATIC_TRIANGLE, None),
        (
            CellType.QUADRATIC_TRIANGLE,
            6,
            "PLANE183",
            183,
            CellType.QUADRATIC_TRIANGLE,
            None,
        ),
        (CellType.QUADRATIC_QUAD, 8, None, 281, CellType.QUADRATIC_QUAD, None),
        (CellType.TETRA, 4, None, 185, CellType.TETRA, None),
        (CellType.PYRAMID, 5, None, 185, CellType.PYRAMID, None),
        (CellType.WEDGE, 6, None, 185, CellType.WEDGE, None),
        (CellType.HEXAHEDRON, 8, "SOLID278", 278, CellType.HEXAHEDRON, None),
        (CellType.VOXEL, 8, None, 185, CellType.HEXAHEDRON, [0, 1, 3, 2, 4, 5, 7, 6]),
        (CellType.QUADRATIC_TETRA, 10, None, 187, CellType.QUADRATIC_TETRA, None),
        (CellType.QUADRATIC_TETRA, 10, "SOLID186", 186, CellType.QUADRATIC_TETRA, None),
        (CellType.QUADRATIC_PYRAMID, 13, None, 186, CellType.QUADRATIC_PYRAMID, None),
        (CellType.QUADRATIC_WEDGE, 15, None, 186, CellType.QUADRATIC_WEDGE, None),
        (
            CellType.QUADRATIC_HEXAHEDRON,
            20,
            "SOLID279",
            279,
            CellType.QUADRATIC_HEXAHEDRON,
            None,
        ),
    ],
)
def test_load_mesh_round_trips_every_topology(
    celltype, n_points, etype, number, read_type, order
):
    grid = _single_cell(celltype, n_points)

    mesh = _ArchiveMapdl().load_mesh(grid, etype=etype)

    np.testing.assert_array_equal(mesh.ekey, [[1, number]])
    read = mesh.grid
    assert read.celltypes.tolist() == [read_type]
    expected = grid.points[order if order is not None else slice(None)]
    np.testing.assert_allclose(
        read.points[read.cell_connectivity], expected, rtol=0, atol=1e-12
    )


@pytest.mark.parametrize("cell", [pv.examples.cells.Wedge, pv.examples.cells.Pyramid])
def test_load_mesh_keeps_positive_volume_of_degenerate_solids(cell):
    grid = cell()
    assert grid.volume > 0

    mesh = _ArchiveMapdl().load_mesh(grid)

    assert mesh.grid.volume == pytest.approx(grid.volume)


def test_load_mesh_casts_pyvista_datasets():
    mesh = _ArchiveMapdl().load_mesh(pv.Plane(i_resolution=2, j_resolution=1))

    np.testing.assert_array_equal(mesh.ekey, [[1, 181]])
    assert mesh.n_elem == 2


def test_load_mesh_rejects_non_pyvista_input():
    with pytest.raises(TypeError, match="PyVista dataset"):
        _ArchiveMapdl().load_mesh(np.zeros((3, 3)))


@pytest.mark.parametrize(
    "celltype,n_points,etype,match",
    [
        (CellType.HEXAHEDRON, 8, "SOLID187", "SOLID187 cannot represent HEXAHEDRON"),
        (CellType.TETRA, 4, "SHELL181", "SHELL181 cannot represent TETRA"),
        (
            CellType.QUADRATIC_TETRA,
            10,
            "SOLID185",
            "SOLID185 cannot represent QUADRATIC_TETRA",
        ),
        (
            CellType.QUADRATIC_EDGE,
            3,
            "LINK180",
            "LINK180 cannot represent QUADRATIC_EDGE",
        ),
        (CellType.HEXAHEDRON, 8, "SOLID181", "Unsupported element type 'SOLID181'"),
        (CellType.HEXAHEDRON, 8, "FOO", "Unsupported element type 'FOO'"),
        (CellType.POLY_VERTEX, 2, None, "Unsupported VTK cell type POLY_VERTEX"),
    ],
)
def test_load_mesh_rejects_incompatible_element_types_before_touching_mapdl(
    celltype, n_points, etype, match
):
    mapdl = _ArchiveMapdl()

    with pytest.raises(ValueError, match=match):
        mapdl.load_mesh(_single_cell(celltype, n_points), etype=etype)
    assert mapdl.calls == []


def test_load_mesh_accepts_element_number_strings():
    mesh = _ArchiveMapdl().load_mesh(
        _single_cell(CellType.QUADRATIC_TETRA, 10), etype="187"
    )

    np.testing.assert_array_equal(mesh.ekey, [[1, 187]])


def test_load_mesh_references_existing_element_type_id():
    mapdl = _ArchiveMapdl(etypes={4: 185})

    mesh = mapdl.load_mesh(_two_hexes(), etype=4)

    assert "\nET," not in mapdl.cdb
    np.testing.assert_array_equal(mesh.ekey, [[4, 185]])
    np.testing.assert_array_equal(mesh.et_id, [4, 4])


def test_load_mesh_rejects_undefined_element_type_id():
    mapdl = _ArchiveMapdl(etypes={1: 185})

    with pytest.raises(ValueError, match=r"Element type IDs \[3\] are not defined"):
        mapdl.load_mesh(_two_hexes(), etype=3)
    assert mapdl.calls == []


def test_load_mesh_rejects_existing_element_type_with_incompatible_topology():
    with pytest.raises(ValueError, match="SOLID187 cannot represent VOXEL"):
        _ArchiveMapdl(etypes={2: 187}).load_mesh(_two_hexes(), etype=2)


def test_load_mesh_maps_element_types_per_topology():
    tet10 = _single_cell(CellType.QUADRATIC_TETRA, 10)
    hexa = _single_cell(CellType.HEXAHEDRON, 8, seed=1)
    tri = _single_cell(CellType.TRIANGLE, 3, seed=2)
    grid = tet10.merge([hexa, tri], merge_points=False)
    mapdl = _ArchiveMapdl(etypes={7: 278})

    mesh = mapdl.load_mesh(grid, etype={"tetra10": "SOLID227", CellType.HEXAHEDRON: 7})

    assert sorted(map(tuple, mesh.ekey.tolist())) == [(7, 278), (8, 227), (9, 181)]
    np.testing.assert_array_equal(mesh.et_id, [8, 7, 9])


def test_load_mesh_new_element_type_ids_start_above_existing_ones():
    mesh = _ArchiveMapdl(etypes={1: 187}).load_mesh(_two_hexes(), etype="SOLID185")

    np.testing.assert_array_equal(mesh.et_id, [2, 2])


def test_load_mesh_reuses_element_type_metadata_on_grid():
    grid = _single_cell(CellType.QUADRATIC_HEXAHEDRON, 20)
    grid.cell_data["ansys_etype"] = [3]
    grid.cell_data["ansys_elem_type_num"] = [279]
    grid.field_data["ansys_keyopt"] = np.array([[3, 2, 1], [5, 1, 1]], np.int32)

    mesh = _ArchiveMapdl().load_mesh(grid)

    np.testing.assert_array_equal(mesh.ekey, [[3, 279]])
    assert mesh.key_option == {3: [[2, 1]]}


def test_load_mesh_round_trips_archive_grid_with_omitted_midside_nodes():
    grid = _single_cell(CellType.QUADRATIC_TETRA, 10)
    grid.point_data["ansys_node_num"] = np.array(
        [11, 12, 13, 14, 15, -1, 17, 18, 19, -1], np.float64
    )
    grid.point_data["fixed"] = np.ones(10, bool)
    mapdl = _ArchiveMapdl()

    mesh = mapdl.load_mesh(grid)

    np.testing.assert_array_equal(mesh.nnum, [11, 12, 13, 14, 15, 17, 18, 19])
    assert _cell_nodes(mesh) == [11, 12, 13, 14, 15, 0, 17, 18, 19, 0]
    np.testing.assert_array_equal(mesh.node_components["FIXED"], mesh.nnum)

    again = _ArchiveMapdl().load_mesh(mesh.grid)

    np.testing.assert_array_equal(again.nnum, mesh.nnum)
    assert _cell_nodes(again) == _cell_nodes(mesh)


def test_load_mesh_keeps_omitted_midside_zero_in_degenerate_brick_slots():
    grid = _single_cell(CellType.QUADRATIC_TETRA, 10)
    grid.point_data["ansys_node_num"] = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, -1.0])

    mesh = _ArchiveMapdl().load_mesh(grid, etype="SOLID186")

    assert _cell_nodes(mesh) == [
        1,
        2,
        3,
        3,
        4,
        4,
        4,
        4,
        5,
        6,
        3,
        7,
        4,
        4,
        4,
        4,
        8,
        9,
        0,
        0,
    ]


def test_load_mesh_rejects_omitted_corner_nodes():
    grid = _single_cell(CellType.QUADRATIC_TETRA, 10)
    grid.point_data["ansys_node_num"] = np.array([-1, 2, 3, 4, 5, 6, 7, 8, 9, 10.0])

    with pytest.raises(ValueError, match="omitted midside"):
        _ArchiveMapdl().load_mesh(grid)


def test_load_mesh_writes_wide_ids():
    grid = _single_cell(CellType.HEXAHEDRON, 8)
    grid.point_data["ansys_node_num"] = np.arange(1_000_000_000, 1_000_000_008)
    mapdl = _ArchiveMapdl()

    mesh = mapdl.load_mesh(grid)

    assert "(3i11,6e21.13e3)" in mapdl.cdb
    np.testing.assert_array_equal(mesh.nnum, grid.point_data["ansys_node_num"])


def test_load_mesh_assigns_scalar_and_per_element_attributes():
    mapdl = _ArchiveMapdl()

    mesh = mapdl.load_mesh(
        _two_hexes(),
        mat=7,
        real=[2, 3],
        secnum=4,
        esys=np.array([0, 11]),
        keyopt={2: 3},
    )

    np.testing.assert_array_equal(mesh.material_type, [7, 7])
    np.testing.assert_array_equal(mesh.elem_real_constant, [2, 3])
    np.testing.assert_array_equal(mesh.section, [4, 4])
    np.testing.assert_array_equal(mesh.element_coord_system(), [0, 11])
    assert mesh.key_option == {1: [[2, 3]]}


def test_load_mesh_defaults_attributes_to_one_and_zero():
    mesh = _ArchiveMapdl().load_mesh(_two_hexes())

    np.testing.assert_array_equal(mesh.material_type, [1, 1])
    np.testing.assert_array_equal(mesh.elem_real_constant, [1, 1])
    np.testing.assert_array_equal(mesh.section, [1, 1])
    np.testing.assert_array_equal(mesh.element_coord_system(), [0, 0])


def test_load_mesh_reuses_grid_attributes_and_element_ids():
    grid = _two_hexes()
    grid.cell_data["ansys_elem_num"] = [20, 10]
    grid.cell_data["ansys_material_type"] = [5, 6]
    grid.cell_data["ansys_secnum"] = [2, 2]

    mesh = _ArchiveMapdl().load_mesh(grid)

    np.testing.assert_array_equal(mesh.enum, [20, 10])
    np.testing.assert_array_equal(mesh.material_type, [5, 6])
    np.testing.assert_array_equal(mesh.section, [2, 2])


@pytest.mark.parametrize(
    "kwargs,match",
    [
        ({"mat": [1, 2, 3]}, "`mat` must be an integer or a sequence of 2"),
        ({"real": 0}, "`real` values must be greater than or equal to 1"),
        ({"esys": -1}, "`esys` values must be greater than or equal to 0"),
        ({"secnum": 1.5}, "`secnum` must be an integer"),
        ({"keyopt": {19: 1}}, "`keyopt` must map KEYOPT numbers"),
        ({"on_conflict": "merge"}, "`on_conflict` must be"),
    ],
)
def test_load_mesh_rejects_invalid_attributes(kwargs, match):
    with pytest.raises(ValueError, match=match):
        _ArchiveMapdl().load_mesh(_two_hexes(), **kwargs)


def test_load_mesh_creates_embedded_and_explicit_mesh_components():
    grid = _two_hexes()
    grid.point_data["fixed"] = grid.points[:, 0] == 0
    grid.cell_data["Core"] = np.array([0, 1], np.uint8)
    grid.cell_data["vtkGhostType"] = np.zeros(2, np.uint8)
    grid.point_data["ansys_flag"] = np.ones(grid.n_points, bool)
    grid.point_data["empty"] = np.zeros(grid.n_points, bool)
    mapdl = _ArchiveMapdl()

    mesh = mapdl.load_mesh(
        grid,
        components={
            "inlet": [1, 2, 3, 5],
            "left": ("ELEMENT", [1]),
            "tip": ("NODES", grid.points[:, 0] == 2),
        },
    )

    nodes = {k: v.tolist() for k, v in mesh.node_components.items()}
    elems = {k: v.tolist() for k, v in mesh.element_components.items()}
    assert nodes == {
        "FIXED": [1, 4, 7, 10],
        "INLET": [1, 2, 3, 5],
        "TIP": [3, 6, 9, 12],
    }
    assert elems == {"CORE": [2], "LEFT": [1]}
    assert "CMBLOCK,INLET,NODE,3\n(8i10)\n         1        -3         5\n" in mapdl.cdb


def test_load_mesh_explicit_components_replace_embedded_ones_and_can_skip_embedded():
    grid = _two_hexes()
    grid.point_data["FIXED"] = np.ones(grid.n_points, bool)
    grid.cell_data["CORE"] = np.ones(2, bool)

    mesh = _ArchiveMapdl().load_mesh(
        grid, components={"fixed": [2]}, include_components=False
    )

    assert {k: v.tolist() for k, v in mesh.node_components.items()} == {"FIXED": [2]}
    assert mesh.element_components == {}


def test_load_mesh_sanitizes_component_names():
    mesh = _ArchiveMapdl().load_mesh(
        _two_hexes(),
        components={"bad-name": [1], "1st": [2], "x" * 40: [3]},
        sanitize_names=True,
    )

    assert sorted(mesh.node_components) == ["BAD_NAME", "C_1ST", "X" * 32]


@pytest.mark.parametrize(
    "components,sanitize,match",
    [
        ({"bad-name": [1]}, False, "Invalid Mesh Component name 'bad-name'"),
        ({"_hidden": [1]}, False, "Invalid Mesh Component name '_hidden'"),
        ({"x" * 33: [1]}, False, "Invalid Mesh Component name"),
        ({"a-b": [1], "a b": [2]}, True, "'a-b' and 'a b' both map to 'A_B'"),
        ({"both": [1], "BOTH": ("ELEM", [1])}, False, "used for both NODE and ELEM"),
        ({"miss": [99]}, False, r"references NODE IDs not in the mesh: \[99\]"),
        ({"kind": ("KP", [1])}, False, "type must be 'NODE' or 'ELEM'"),
    ],
)
def test_load_mesh_rejects_invalid_components(components, sanitize, match):
    mapdl = _ArchiveMapdl()

    with pytest.raises(ValueError, match=match):
        mapdl.load_mesh(_two_hexes(), components=components, sanitize_names=sanitize)
    assert mapdl.calls == []


def test_load_mesh_errors_when_mesh_already_exists():
    mapdl = _ArchiveMapdl(node_max=4)

    with pytest.raises(ValueError, match="on_conflict='replace'"):
        mapdl.load_mesh(_two_hexes())
    assert mapdl.calls == []


def test_load_mesh_replace_deletes_mesh_entities_and_mesh_components():
    mapdl = _ArchiveMapdl(
        node_max=8, elem_max=1, components={"OLDN": "NODE", "OLDE": "ELEM", "KPS": "KP"}
    )

    mesh = mapdl.load_mesh(_two_hexes(), on_conflict="replace")

    deleted = mapdl.calls[: mapdl.calls.index(("CDREAD", "DB"))]
    assert ("CMDELE", "OLDN") in deleted and ("CMDELE", "OLDE") in deleted
    assert ("CMDELE", "KPS") not in deleted
    assert deleted.index(("EDELE", "ALL")) < deleted.index(("NDELE", "ALL"))
    assert mapdl.components == {"KPS": "KP"}
    np.testing.assert_array_equal(mesh.nnum, np.arange(1, 13))


def test_load_mesh_append_offsets_node_element_and_element_type_ids():
    grid = _two_hexes()
    grid.point_data["fixed"] = grid.points[:, 0] == 0
    mapdl = _ArchiveMapdl(node_max=100, elem_max=50, etypes={1: 186})

    mesh = mapdl.load_mesh(
        grid, components={"CORE": ("ELEM", [2])}, on_conflict="append"
    )

    np.testing.assert_array_equal(mesh.nnum, np.arange(101, 113))
    np.testing.assert_array_equal(mesh.enum, [51, 52])
    np.testing.assert_array_equal(mesh.et_id, [2, 2])
    assert _cell_nodes(mesh) == [101, 102, 105, 104, 107, 108, 111, 110]
    assert mesh.node_components["FIXED"].tolist() == [101, 104, 107, 110]
    assert mesh.element_components["CORE"].tolist() == [52]


def test_load_mesh_writes_multi_line_component_blocks():
    grid = pv.ImageData(dimensions=(10, 2, 2)).cast_to_unstructured_grid()
    every_other = list(range(1, grid.n_points + 1, 2))

    mesh = _ArchiveMapdl().load_mesh(grid, components={"ODD": every_other})

    assert mesh.node_components["ODD"].tolist() == every_other
