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

"""Live Mechanical APDL tests of ``load_mesh``, ``to_pyvista``, and ``export_mesh``."""

import numpy as np
import pytest

from conftest import clear, has_dependency, requires

if has_dependency("pyvista"):
    import pyvista as pv

pytestmark = [requires("grpc"), requires("pyvista")]

from test_mesh_bridge_grid import (
    HEX_CORNERS,
    HEX_EDGES,
    TET_CORNERS,
    TET_EDGES,
    _quadratic_points,
)
from test_mesh_bridge_load import _MeshioMesh

# SOLID186 prism: K = L, O = P, and A = B, with S = K and W = O.
WEDGE_CORNERS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1)]
WEDGE_EDGES = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3), (0, 3), (1, 4), (2, 5)]
WEDGE_SLOTS = [0, 1, 2, 2, 3, 4, 5, 5, 6, 7, 2, 8, 9, 10, 5, 11, 12, 13, 14, 14]


def _element(mapdl, nodes, etype, mat=1, secnum=1, esys=0):
    mapdl.type(etype)
    mapdl.mat(mat)
    mapdl.secnum(secnum)
    mapdl.esys(esys)
    mapdl.e(*nodes[:8])
    for start in range(8, len(nodes), 8):
        mapdl.emore(*nodes[start : start + 8])


def _nodes(mapdl, points, first, skip=()):
    ids = []
    for i, xyz in enumerate(points):
        ids.append(0 if i in skip else first + i)
        if i not in skip:
            mapdl.n(first + i, *xyz)
    return ids


def _define_materials_and_sections(mapdl):
    mapdl.prep7()
    mapdl.mp("EX", 1, 210e9)
    mapdl.mp("PRXY", 1, 0.3)
    mapdl.mp("EX", 2, 70e9)
    mapdl.mp("PRXY", 2, 0.33)
    mapdl.sectype(3, "BEAM", "RECT")
    mapdl.secdata(0.1, 0.2)


def _build_mixed_model(mapdl):
    """SOLID186 hex20 + wedge15 + hex20 without two midsides, SOLID187, BEAM189."""
    _define_materials_and_sections(mapdl)
    mapdl.et(1, "SOLID186")
    mapdl.keyopt(1, 2, 1)
    mapdl.et(2, "SOLID187")
    mapdl.et(3, "BEAM189")
    mapdl.local(11, 0, 0, 0, 0, 30)
    mapdl.csys(0)

    hex20 = _quadratic_points(HEX_CORNERS, HEX_EDGES)
    _element(mapdl, _nodes(mapdl, hex20, 1), 1)
    wedge = _quadratic_points(WEDGE_CORNERS, WEDGE_EDGES, shift=2.0)
    wedge_ids = _nodes(mapdl, wedge, 21)
    _element(mapdl, [wedge_ids[i] for i in WEDGE_SLOTS], 1, mat=2, esys=11)
    hex_ids = _nodes(mapdl, _quadratic_points(HEX_CORNERS, HEX_EDGES, 4.0), 41, (8, 9))
    _element(mapdl, hex_ids, 1)
    tet = _quadratic_points(TET_CORNERS, TET_EDGES, shift=6.0)
    _element(mapdl, _nodes(mapdl, tet, 61), 2, mat=2)
    beam = _nodes(mapdl, [(8, 0, 0), (9, 0, 0), (8.5, 0, 0)], 81)
    _element(mapdl, beam, 3, secnum=3)

    mapdl.nsel("S", "NODE", "", 1, 4)
    mapdl.cm("NBASE", "NODE")
    mapdl.nsel("S", "NODE", "", 81, 83)
    mapdl.cm("NBEAM", "NODE")
    mapdl.esel("S", "ELEM", "", 1, 3)
    mapdl.cm("EBRICK", "ELEM")
    mapdl.esel("S", "ELEM", "", 4, 5)
    mapdl.cm("EOTHER", "ELEM")
    mapdl.allsel()


def _partial_selection(mapdl):
    """Leave only ``NBASE`` selected among the components, and part of the mesh."""
    mapdl.cmsel("S", "NBASE")
    mapdl.allsel()
    mapdl.esel("S", "ELEM", "", 4)
    mapdl.nsle("S")
    return _selection(mapdl)


def _selection(mapdl):
    return (
        mapdl.mesh.nnum.tolist(),
        mapdl.mesh.enum.tolist(),
        sorted(mapdl.components.names),
    )


def _snapshot(mapdl):
    """Whole-model nodes, element records, element types, and Mesh Components."""
    with mapdl.save_selection:
        mapdl.allsel()
        mapdl.cmsel("ALL")
        mesh = mapdl.mesh
        elements = {
            int(rec[8]): (rec[:5].tolist(), np.trim_zeros(rec[10:], "b").tolist())
            for rec in mesh.elem
        }
        snapshot = dict(
            nnum=mesh.nnum.tolist(),
            nodes=np.array(mesh.nodes),
            elements=elements,
            ekey=mesh.ekey.tolist(),
            key_option=mesh.key_option,
            node_components={k: list(v) for k, v in mesh.node_components.items()},
            element_components={k: list(v) for k, v in mesh.element_components.items()},
        )
    return snapshot


def _assert_same_mesh(actual, expected):
    nodes = actual.pop("nodes")
    np.testing.assert_allclose(nodes, expected.pop("nodes"), atol=1e-10)
    assert actual == expected


@pytest.fixture
def mixed_model(mapdl, cleared):
    _build_mixed_model(mapdl)
    return _snapshot(mapdl)


def test_mixed_model_snapshot_is_built_as_expected(mapdl, mixed_model):
    assert mixed_model["ekey"] == [[1, 186], [2, 187], [3, 189]]
    assert mixed_model["key_option"] == {1: [[2, 1]]}
    assert mixed_model["elements"][2][0] == [2, 1, 1, 1, 11]
    assert mixed_model["elements"][3][1][8:10] == [0, 0]
    assert mixed_model["elements"][5] == ([1, 3, 1, 3, 0], [81, 82, 83])
    assert set(mixed_model["node_components"]) == {"NBASE", "NBEAM"}
    assert set(mixed_model["element_components"]) == {"EBRICK", "EOTHER"}


def test_grid_keeps_quadratic_cell_types(mapdl, mixed_model):
    assert set(mapdl.mesh.grid.celltypes) == {
        pv.CellType.QUADRATIC_HEXAHEDRON,
        pv.CellType.QUADRATIC_WEDGE,
        pv.CellType.QUADRATIC_TETRA,
        pv.CellType.QUADRATIC_EDGE,
    }


def test_to_pyvista_captures_unselected_components(mapdl, mixed_model):
    before = _partial_selection(mapdl)

    grid = mapdl.mesh.to_pyvista()

    assert _selection(mapdl) == before
    assert grid.n_cells == 5
    node_num = grid.point_data["ansys_node_num"]
    assert sorted(node_num[grid.point_data["NBEAM"]]) == [81, 82, 83]
    elem_num = grid.cell_data["ansys_elem_num"]
    assert elem_num[grid.cell_data["EOTHER"]].tolist() == [4, 5]


@pytest.mark.parametrize("source", ["cdb", "vtu", "grid"])
def test_mixed_model_round_trips_through_load_mesh(
    mapdl, mixed_model, tmp_path, source
):
    before = _partial_selection(mapdl)
    if source == "grid":
        mesh = mapdl.mesh.to_pyvista()
    elif source == "cdb":
        mesh = mapdl.export_mesh(tmp_path / "model.cdb")
    else:
        mesh = mapdl.mesh.export(tmp_path / "model.vtu")
    assert _selection(mapdl) == before

    clear(mapdl)
    _define_materials_and_sections(mapdl)
    mapdl.load_mesh(mesh)

    _assert_same_mesh(_snapshot(mapdl), mixed_model)
    assert mapdl.get_value("EX", 2, "TEMP", 0) == pytest.approx(70e9)
    assert "Rectangle" in mapdl.slist(3)


def test_export_cdb_selected_only(mapdl, mixed_model, tmp_path):
    _partial_selection(mapdl)

    path = mapdl.export_mesh(tmp_path / "tet.cdb", selected_only=True)

    clear(mapdl)
    mapdl.load_mesh(path)
    snapshot = _snapshot(mapdl)
    assert list(snapshot["elements"]) == [4]
    assert snapshot["nnum"] == list(range(61, 71))
    assert snapshot["node_components"] == {}
    assert snapshot["element_components"] == {}


def _hexes(shift=0.0):
    grid = pv.ImageData(dimensions=(3, 2, 2)).cast_to_unstructured_grid()
    grid.points += [shift, 0, 0]
    grid.point_data["LEFT"] = grid.points[:, 0] == shift
    return grid


def test_load_mesh_conflict_policies(mapdl, cleared):
    mapdl.load_mesh(_hexes())

    with pytest.raises(ValueError, match="already exist"):
        mapdl.load_mesh(_hexes())
    assert mapdl.mesh.n_elem == 2

    tets = pv.ImageData(dimensions=(2, 2, 2)).triangulate()
    mesh = mapdl.load_mesh(tets, on_conflict="replace")
    assert mesh.n_elem == tets.n_cells
    assert mesh.nnum.tolist() == list(range(1, 9))
    assert "LEFT" not in mapdl.components

    mesh = mapdl.load_mesh(_hexes(5.0), on_conflict="append")
    assert mesh.n_elem == tets.n_cells + 2
    assert mesh.nnum.max() == 8 + 12
    np.testing.assert_array_equal(mesh.ekey, [[1, 185], [2, 185], [3, 185]])
    assert mapdl.mesh.node_components["LEFT"] == (9, 12, 15, 18)


LENGTH, WIDTH, SIZE, FORCE = 10.0, 1.0, 0.5, 1000.0
EX, PRXY = 200e9, 0.3


def _gmsh_cantilever():
    """Second-order Gmsh-style mesh: tetra10 volume and triangle6 end patches."""
    box = pv.ImageData(
        dimensions=(int(LENGTH / SIZE) + 1, 3, 3), spacing=(SIZE, SIZE, SIZE)
    ).triangulate()
    points = np.array(box.points)
    tets = box.cells_dict[pv.CellType.TETRA].copy()
    a, b, c, d = (points[tets[:, i]] for i in range(4))
    inverted = np.einsum("ij,ij->i", np.cross(b - a, c - a), d - a) < 0
    tets[inverted, 1:3] = tets[inverted, 2:0:-1]

    edges = np.sort(tets[:, TET_EDGES], axis=2).reshape(-1, 2)
    unique, inverse = np.unique(edges, axis=0, return_inverse=True)
    midside = {tuple(edge): len(points) + i for i, edge in enumerate(unique)}
    points = np.vstack([points, points[unique].mean(axis=1)])
    tet10 = np.hstack([tets, len(box.points) + inverse.reshape(-1, 6)])

    faces = {"FIXED": [], "TIP": []}
    for tet in tets:
        for face in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
            corners = tet[list(face)]
            x = points[corners, 0]
            name = "FIXED" if np.all(x == 0) else "TIP" if np.all(x == LENGTH) else None
            if name:
                mids = [
                    midside[tuple(sorted(e))]
                    for e in zip(corners, np.roll(corners, -1))
                ]
                faces[name].append([*corners, *mids])
    tri6 = np.array(faces["FIXED"] + faces["TIP"])
    tags = np.array([2] * len(faces["FIXED"]) + [3] * len(faces["TIP"]))
    return _MeshioMesh(
        points,
        [("tetra10", tet10), ("triangle6", tri6)],
        cell_data={"gmsh:physical": [np.ones(len(tet10), int), tags]},
        field_data={
            "BEAM": np.array([1, 3]),
            "FIXED": np.array([2, 2]),
            "TIP": np.array([3, 2]),
        },
    )


def _solve_tip_deflection(mapdl):
    mapdl.mp("EX", 1, EX)
    mapdl.mp("PRXY", 1, PRXY)
    mapdl.d("FIXED", "ALL", 0)
    mapdl.cmsel("S", "TIP")
    n_tip = mapdl.mesh.n_node
    mapdl.f("ALL", "FY", -FORCE / n_tip)
    mapdl.allsel()
    mapdl.slashsolu()
    mapdl.antype("STATIC")
    mapdl.solve()
    mapdl.finish()
    mapdl.post1()
    mapdl.set(1)
    mapdl.cmsel("S", "TIP")
    tip = mapdl.post_processing.nodal_displacement("Y").mean()
    mapdl.allsel()
    mapdl.finish()
    return tip


def test_external_cantilever_matches_native_mesh(mapdl, cleared):
    mesh = mapdl.load_mesh(_gmsh_cantilever(), etype="SOLID187")
    assert mesh.ekey.tolist() == [[1, 187]]
    assert mapdl.components["FIXED"].type == "NODE"
    assert mapdl.components["TIP"].type == "NODE"
    assert mapdl.components["BEAM"].type == "ELEM"
    external = _solve_tip_deflection(mapdl)

    clear(mapdl)
    mapdl.et(1, "SOLID187")
    mapdl.block(0, LENGTH, 0, WIDTH, 0, WIDTH)
    mapdl.esize(SIZE)
    mapdl.vmesh("ALL")
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.cm("FIXED", "NODE")
    mapdl.nsel("S", "LOC", "X", LENGTH)
    mapdl.cm("TIP", "NODE")
    mapdl.allsel()
    native = _solve_tip_deflection(mapdl)

    beam_theory = -FORCE * LENGTH**3 / (3 * EX * WIDTH**4 / 12)
    assert external == pytest.approx(native, rel=0.03)
    assert external == pytest.approx(beam_theory, rel=0.05)
