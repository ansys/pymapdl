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

"""Unit tests regarding plotting."""
import os
from unittest.mock import patch

import numpy as np
import pytest

from conftest import has_dependency, requires

if not has_dependency("pyvista"):
    pytest.skip(
        allow_module_level=True, reason="Skipping because 'pyvista' is not installed"
    )


from ansys.mapdl.core.errors import ComponentDoesNotExits, MapdlRuntimeError
from ansys.mapdl.core.plotting import GraphicsBackend
from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

FORCE_LABELS = [["FX", "FY", "FZ"], ["HEAT"], ["CHRG"]]
DISPL_LABELS = [["UX", "UY", "UZ"], ["TEMP"], ["VOLT"]]
ALL_LABELS = FORCE_LABELS.copy()
ALL_LABELS.extend(DISPL_LABELS)


@pytest.fixture
def boundary_conditions_example(mapdl, cleared):
    mapdl.et("", 189)

    mapdl.n(1, 0, 0, 0)
    mapdl.n(2, 1, 0, 0)
    mapdl.n(3, 2, 0, 0)
    mapdl.n(4, 0, 0, 1)
    mapdl.n(5, 1, 0, 1)
    mapdl.n(6, 2, 0, 1)

    mapdl.nsel("s", "node", "", 1)
    mapdl.f("all", "FX", 0)
    mapdl.nsel("s", "node", "", 2)
    mapdl.f("all", "FY", 0)
    mapdl.nsel("s", "node", "", 3)
    mapdl.f("all", "FZ", 0)

    mapdl.nsel("s", "node", "", 4)
    mapdl.d("all", "UX", 0)
    mapdl.nsel("s", "node", "", 5)
    mapdl.d("all", "UY", 0)
    mapdl.nsel("s", "node", "", 6)
    mapdl.d("all", "UZ", 0)

    mapdl.n(7, 0, 1, 0)
    mapdl.n(8, 1, 1, 0)
    mapdl.n(9, 2, 1, 0)
    mapdl.n(10, 0, 2, 0)
    mapdl.n(11, 1, 2, 0)
    mapdl.n(12, 2, 2, 0)

    mapdl.nsel("s", "node", "", 7)
    mapdl.f("all", "FX", 10)
    mapdl.nsel("s", "node", "", 8)
    mapdl.f("all", "FY", 20)
    mapdl.nsel("s", "node", "", 9)
    mapdl.f("all", "FZ", 30)

    mapdl.nsel("s", "node", "", 10)
    mapdl.d("all", "UX", 20)
    mapdl.nsel("s", "node", "", 11)
    mapdl.d("all", "UY", 20)
    mapdl.nsel("s", "node", "", 12)
    mapdl.d("all", "UZ", 20)

    mapdl.nsel("all")


@pytest.fixture
def block_example_coupled(mapdl, cleared):
    mapdl.et(1, 226)
    mapdl.keyopt(1, 1, 1011)  # Thermal-Piezoelectric

    # Disp
    # UX, UY, UZ,
    # TEMP, VOLT

    # Force
    # FX, FY, FZ,
    # HEAT, CHRG
    mapdl.n(1, 0, 0, 0)
    mapdl.n(2, 1, 0, 0)
    mapdl.n(3, 2, 0, 0)


def check_geometry(mapdl, function):
    prev_knum = mapdl.geometry.knum
    prev_lnum = mapdl.geometry.lnum
    prev_anum = mapdl.geometry.anum
    prev_kps = mapdl.geometry.get_keypoints(
        return_as_array=True, return_ids_in_array=True
    )
    prev_lines = mapdl.geometry.get_lines(return_as_list=True)
    prev_areas = mapdl.geometry.get_areas(return_as_list=True)

    out = function()

    new_knum = mapdl.geometry.knum
    new_lnum = mapdl.geometry.lnum
    new_anum = mapdl.geometry.anum
    new_kps = mapdl.geometry.get_keypoints(
        return_as_array=True, return_ids_in_array=True
    )
    new_lines = mapdl.geometry.get_lines(return_as_list=True)
    new_areas = mapdl.geometry.get_areas(return_as_list=True)

    assert np.allclose(prev_knum, new_knum)
    assert np.allclose(prev_lnum, new_lnum)
    assert np.allclose(prev_anum, new_anum)
    assert len(prev_kps) == len(new_kps)
    assert len(prev_lines) == len(new_lines)
    assert len(prev_areas) == len(new_areas)
    assert all([each in new_kps for each in prev_kps])
    assert all([each in new_lines for each in prev_lines])
    assert all([each in new_areas for each in prev_areas])
    assert all([each in prev_kps for each in new_kps])
    assert all([each in prev_lines for each in new_lines])
    assert all([each in prev_areas for each in new_areas])

    return out


def test_plot_empty_mesh(mapdl, cleared):
    with pytest.warns(UserWarning):
        mapdl.nplot()

    with pytest.warns(UserWarning):
        mapdl.eplot()


def test_download_file_with_vkt_false(mapdl, cube_solve, tmpdir):
    # Testing basic behaviour
    with patch.object(mapdl, "_graphics_backend", GraphicsBackend.MAPDL):
        mapdl.eplot(savefig="myfile.png")
        assert os.path.exists("myfile.png")
        ti_m = os.path.getmtime("myfile.png")

        # Testing overwriting
        mapdl.eplot(savefig="myfile.png")
        assert not os.path.exists("myfile_1.png")
        assert os.path.getmtime("myfile.png") != ti_m  # file has been modified.

        os.remove("myfile.png")

        # Testing no extension
        mapdl.eplot(savefig="myfile")
        assert os.path.exists("myfile")
        os.remove("myfile")

        # Testing update name when file exists.
        mapdl.eplot(savefig=True)
        assert os.path.exists("plot.png")

        mapdl.eplot(savefig=True)
        assert os.path.exists("plot_1.png")

        os.remove("plot.png")
        os.remove("plot_1.png")

        # Testing full path for downloading
        plot_ = os.path.join(tmpdir, "myplot.png")
        mapdl.eplot(savefig=plot_)
        assert os.path.exists(plot_)

        plot_ = os.path.join(tmpdir, "myplot")
        mapdl.eplot(savefig=plot_)
        assert os.path.exists(plot_)


@pytest.mark.parametrize(
    "method",
    [
        "kplot",
        "lplot",
        "aplot",
        "vplot",
        "nplot",
        "eplot",
    ],
)
def test_plots_no_vtk(mapdl, cube_solve, method):
    _ = getattr(mapdl, method)(graphics_backend=GraphicsBackend.MAPDL)


@pytest.mark.parametrize(
    "backend", [GraphicsBackend.PYVISTA, GraphicsBackend.MAPDL, None]
)
def test_kplot(cleared, mapdl, tmpdir, backend):
    mapdl.k("", 0, 0, 0)
    mapdl.k("", 1, 0, 0)
    mapdl.k("", 1, 1, 0)
    mapdl.k("", 0, 1, 0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl.kplot(graphics_backend=backend, savefig=filename)
    assert cpos is None
    if backend:
        assert os.path.isfile(filename)


@pytest.mark.parametrize(
    "backend", [GraphicsBackend.PYVISTA, GraphicsBackend.MAPDL, None]
)
def test_lplot(cleared, mapdl, tmpdir, backend):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    mapdl.l(k0, k1)
    mapdl.l(k1, k2)
    mapdl.l(k2, k3)
    mapdl.l(k3, k0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl.lplot(
        graphics_backend=backend, show_keypoint_numbering=True, savefig=filename
    )
    assert cpos is None
    if backend:
        assert os.path.isfile(filename)


@pytest.mark.parametrize(
    "backend", [GraphicsBackend.PYVISTA, GraphicsBackend.MAPDL, None]
)
def test_aplot(cleared, mapdl, backend):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    mapdl.al(l0, l1, l2, l3)
    mapdl.aplot(show_area_numbering=True)
    color_areas_bool = True if backend == GraphicsBackend.PYVISTA else False
    mapdl.aplot(
        backend=backend,
        color_areas=color_areas_bool,
        show_lines=True,
        show_line_numbering=True,
    )

    mapdl.aplot(quality=10)
    mapdl.aplot(quality=1)


@pytest.mark.parametrize(
    "backend", [GraphicsBackend.PYVISTA, GraphicsBackend.MAPDL, None]
)
def test_vplot(cleared, mapdl, backend):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.vplot(graphics_backend=backend, color_areas=True)


@pytest.mark.parametrize("nnum", [True, False])
@pytest.mark.parametrize(
    "backend", [GraphicsBackend.PYVISTA, GraphicsBackend.MAPDL, None]
)
def test_nplot(cleared, mapdl, nnum, backend):
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(graphics_backend=backend, nnum=nnum, background="w", color="k")


@pytest.mark.parametrize(
    "backend", [GraphicsBackend.PYVISTA, GraphicsBackend.MAPDL, None]
)
def test_eplot(mapdl, make_block, backend):
    init_elem = mapdl.mesh.n_elem
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    mapdl.eplot(show_node_numbering=True, background="w", color="b")
    mapdl.eplot(
        graphics_backend=backend, show_node_numbering=True, background="w", color="b"
    )
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    assert mapdl.mesh.n_elem == init_elem


def test_eplot_savefig(mapdl, make_block, tmpdir):
    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    mapdl.eplot(
        background="w",
        show_edges=True,
        smooth_shading=True,
        window_size=[1920, 1080],
        savefig=filename,
    )
    assert os.path.isfile(filename)


@pytest.mark.parametrize(
    "field", ["UX", "UY", "UZ", "FX", "FY", "FZ", "TEMP", "HEAT", "VOLT", "CHRG"]
)
@pytest.mark.parametrize("magnitude", [0, 50, 500])
def test_single_glyph(mapdl, cleared, field, magnitude, verify_image_cache):
    mapdl.et(1, 226)
    mapdl.keyopt(1, 1, 1011)  # Thermal-Piezoelectric
    mapdl.n(1, 0, 0, 0)

    if field in [x for group in DISPL_LABELS for x in group]:
        func = getattr(mapdl, "d")
    else:
        func = getattr(mapdl, "f")

    func(1, field, magnitude)

    if magnitude > 0:
        mapdl.n(2, 1, 0, 0)
        func(2, field, magnitude * 2)

    if magnitude > 50:
        mapdl.n(3, 2, 0, 0)
        func(3, field, magnitude * 10)

    mapdl.allsel()

    p = mapdl.nplot(
        plot_bc=True,
        # point_size=max(magnitude, 10),
        # render_points_as_spheres=True,
        plot_bc_legend=True,
        plot_bc_labels=True,
        title="",
    )


@pytest.mark.parametrize("return_plotter", [True, False])
@pytest.mark.parametrize("plot_bc_legend", [True, False])
@pytest.mark.parametrize("plot_bc_labels", [True, False])
def test_bc_plot_options(
    mapdl,
    boundary_conditions_example,
    verify_image_cache,
    return_plotter,
    plot_bc_legend,
    plot_bc_labels,
    bc_labels_font_size=50,
):

    if plot_bc_legend or plot_bc_labels:
        # The legend and labels generate highly variance than other tests
        verify_image_cache.high_variance_test = True

    p = mapdl.nplot(
        return_plotter=return_plotter,
        plot_bc=True,
        plot_bc_legend=plot_bc_legend,
        plot_bc_labels=plot_bc_labels,
        title="",
    )

    if return_plotter:
        assert isinstance(p, MapdlPlotter)
        p.show()
    else:
        assert p is None


@pytest.mark.parametrize("field", ALL_LABELS)
@pytest.mark.parametrize(
    "loads", [[0, 0, 0], [10, 10, 10], [10, 20, 30], [10, 100, 1000]]
)
def test_bc_plot_options_fields(
    mapdl, block_example_coupled, verify_image_cache, field, loads
):
    mapdl.prep7()
    for i in range(len(field)):
        mapdl.nsel("s", "node", "", i + 1)
        if field[i] in [x for group in FORCE_LABELS for x in group]:
            mapdl.f("all", field[i], loads[i])
        else:
            mapdl.d("all", field[i], loads[i])

    mapdl.nsel("s", "node", "", 1, 3)

    p = mapdl.nplot(
        plot_bc=True,
        plot_bc_legend=True,
        plot_bc_labels=True,
        title="",
    )

    assert p is None


@pytest.mark.parametrize(
    "bc_labels",  # Added second part of the argument to avoid image cache name clashing.
    # See https://github.com/pyvista/pytest-pyvista/issues/93
    [
        ["Mechanical", "Title case"],
        ["mechanical", "lower case"],
        ["meCHANICAL", "Mixed case"],
        ["ux", "Lower case"],
        ["UX", "Upper case"],
        [["UX", "UY"], "List of displacements"],
        ["CSGZ", "Magnetic forces"],
    ],
)
def test_bc_plot_bc_labels(mapdl, boundary_conditions_example, bc_labels):
    p = mapdl.nplot(
        return_plotter=True,
        plot_bc=True,
        plot_bc_labels=True,
        bc_labels=bc_labels[0],
        title="",
    )
    assert isinstance(p, MapdlPlotter), bc_labels[1]
    p.show()  # plotting for catching


@pytest.mark.parametrize(
    "bc_labels",
    [
        "error",
        ["UX", "error"],
    ],
)
def test_bc_plot_bc_labels_error(mapdl, boundary_conditions_example, bc_labels):
    with pytest.raises(ValueError):
        mapdl.nplot(
            return_plotter=True,
            plot_bc=True,
            plot_bc_labels=True,
            bc_labels=bc_labels,
            title="",
        )


@pytest.mark.parametrize(
    "bc_target",
    [
        ["Nodes", "Title case"],
        ["NOdes", "Mixed case"],
    ],
)
def test_bc_plot_bc_target(mapdl, boundary_conditions_example, bc_target):
    p = mapdl.nplot(
        return_plotter=True,
        plot_bc=True,
        plot_bc_labels=True,
        bc_target=bc_target[0],
        title="",
    )
    assert isinstance(p, MapdlPlotter), bc_target[1]
    p.show()  # plotting for catching


@pytest.mark.parametrize(
    "bc_target",
    [
        ["NOsdes"],
        "error",
        ["error"],
        {"error": "Not accepting dicts"},
    ],
)
def test_bc_plot_bc_target_error(mapdl, boundary_conditions_example, bc_target):
    with pytest.raises(ValueError):
        mapdl.nplot(
            return_plotter=True,
            plot_bc=True,
            plot_bc_labels=True,
            bc_target=bc_target,
            title="",
        )


def test_bc_no_mapdl(mapdl, cleared):
    with pytest.raises(ValueError):
        pl = MapdlPlotter()
        pl.plot([], [], [], plot_bc=True)
        pl.show()
        # mapdl should be an argument if plotting BC


def test_bc_only_one_node(mapdl, boundary_conditions_example):
    mapdl.nsel("s", "node", "", 1)
    mapdl.nplot(
        plot_bc=True,
        title="",
    )


def test_bc_glyph(mapdl, boundary_conditions_example):
    mapdl.nplot(plot_bc=True, bc_glyph_size=19)
    with pytest.raises(ValueError):
        mapdl.nplot(
            plot_bc=True,
            bc_glyph_size="big",
            title="",
        )


def test_bc_bc_labels(mapdl, boundary_conditions_example, verify_image_cache):
    """Test values for 'bc_labels' keyword argument."""
    verify_image_cache.skip = True  # skipping image verification

    mapdl.nplot(plot_bc=True, bc_labels="UX")
    mapdl.nplot(plot_bc=True, bc_labels=["Ux", "uy", "VOLT"])

    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_labels=["big"])

    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_labels={"not": "valid"})

    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_labels=["UX", {"not": "valid"}])


def test_all_same_values(mapdl, boundary_conditions_example):
    """Test the BC glyph size when all the BC have same magnitude."""
    mapdl.nsel("all")
    mapdl.f("all", "FX", 0)
    mapdl.nplot(
        plot_bc=True,
        bc_labels="FX",
        title="",
    )


@pytest.mark.parametrize(
    "selection",
    ["S", "R", "A", "U"],
)
def test_pick_nodes(mapdl, make_block, selection, verify_image_cache):
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.edele("all")
    mapdl.nsel("s", "node", "", 1)
    mapdl.nsel("a", "node", "", 2)
    mapdl.nsel("inver")
    mapdl.ndele("all")

    def debug_orders(pl, point):
        pl = pl.scene
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        if pl._picking_right_clicking_observer is None:
            pl.iren._mouse_left_button_press(
                int(width * point[0]), int(height * point[1])
            )
            pl.iren._mouse_left_button_release(width, height)
        else:
            pl.iren._mouse_right_button_press(
                int(width * point[0]), int(height * point[1])
            )
            pl.iren._mouse_right_button_release(width, height)
        pl.iren._mouse_move(int(width * point[0]), int(height * point[1]))

    mapdl.nsel("S", "node", "", 1)
    if selection == "R" or selection == "U":
        point = (285 / 1024, 280 / 800)
        mapdl.nsel("a", "node", "", 2)
    elif selection == "A":
        point = (285 / 1024, 280 / 800)
    else:
        point = (0.5, 0.5)

    selected = mapdl.nsel(
        selection,
        "P",
        _debug=lambda x: debug_orders(x, point=point),
        tolerance=1,
    )  # Selects node 2

    assert isinstance(selected, (list, np.ndarray))
    if isinstance(selected, np.ndarray):
        assert selected.all(), "Array is empty"
    else:
        assert selected, "List is empty"
    assert len(selected) > 0, "The result has length zero"

    if selection != "U":
        assert sorted(selected) == sorted(
            mapdl._get_selected_("node")
        ), "Order does not match"

    if selection in ["S", "R"]:
        assert selected == [2], "Second node is not selected, nor the only one"
    elif selection == "A":
        assert 1 in selected, "Node 1 is not selected"
        assert len(selected) > 1, "There should be at least two nodes"
    elif selection == "U":
        assert 2 not in selected, "Node 2 should not be selected."
        assert 1 in selected, "Node 1 should be selected."

    mapdl.nplot()


@pytest.mark.parametrize(
    "selection",
    ["S", "R", "A", "U"],
)
def test_pick_kp(mapdl, make_block, selection):
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.vdele("all")
    mapdl.adele("all")
    mapdl.ldele("all")
    mapdl.ksel("u", "kp", "", 1)
    mapdl.ksel("u", "kp", "", 2)
    mapdl.kdele("all")
    mapdl.ksel("all")

    def debug_orders(pl, point):
        pl = pl.scene
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        if pl._picking_right_clicking_observer is None:
            pl.iren._mouse_left_button_press(
                int(width * point[0]), int(height * point[1])
            )
            pl.iren._mouse_left_button_release(width, height)
        else:
            pl.iren._mouse_right_button_press(
                int(width * point[0]), int(height * point[1])
            )
            pl.iren._mouse_right_button_release(width, height)

        pl.iren._mouse_move(int(width * point[0]), int(height * point[1]))

    mapdl.ksel("S", "KP", "", 1)
    if selection == "R" or selection == "U":
        point = (285 / 1024, 280 / 800)
        mapdl.ksel("a", "kp", "", 2)  # Selects node 2
    elif selection == "A":
        point = (285 / 1024, 280 / 800)
    else:
        point = (0.5, 0.5)

    selected = mapdl.ksel(
        selection,
        "P",
        _debug=lambda x: debug_orders(x, point=point),
        tolerance=0.2,
    )

    assert isinstance(selected, (list, np.ndarray))
    if isinstance(selected, np.ndarray):
        assert selected.all()
    else:
        assert selected
    assert len(selected) > 0
    if selection != "U":
        assert sorted(selected) == sorted(mapdl._get_selected_("kp"))

    if selection == "S":
        assert selected == [1]
    elif selection == "R":
        assert selected == [2]
    elif selection == "A":
        assert 1 in selected
        assert 2 in selected
    elif selection == "U":
        assert 2 not in selected
        assert 1 in selected


def test_pick_node_failure(mapdl, make_block):
    # it should work for the KP too.
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.edele("all")
    mapdl.nsel("s", "node", "", 1)
    mapdl.nsel("a", "node", "", 2)
    mapdl.nsel("inver")
    mapdl.ndele("all")

    with pytest.raises(ValueError):
        mapdl.nsel("X", "P")

    with pytest.raises(ValueError):
        mapdl.nsel("S", "node", "", [1, 2, 3], 1)

    with pytest.raises(ValueError):
        mapdl.nsel("S", "node", "", [1, 2, 3], "", 1)


def test_nsel_ksel_iterable_input(mapdl, make_block):
    # Testing using iterable (list/tuple/array) as vmin
    assert np.allclose(
        mapdl.nsel("S", "node", "", [1, 2, 3], "", ""), np.array([1, 2, 3])
    )

    # Special cases where the iterable is empty
    # empty list
    output = mapdl.nsel("S", "node", "", [])
    assert output is not None  # it should select nothing
    if isinstance(output, np.ndarray):
        assert output.size == 0
    elif isinstance(output, list):
        assert len(output) == 0
    assert len(mapdl._get_selected_("node")) == 0

    # empty tuple
    output = mapdl.nsel("S", "node", "", ())
    assert output is not None  # it should select nothing
    if isinstance(output, np.ndarray):
        assert output.size == 0
    elif isinstance(output, list):
        assert len(output) == 0

    assert len(mapdl._get_selected_("node")) == 0

    # empty array
    output = mapdl.nsel("S", "node", "", np.empty((0)))
    assert output is not None  # it should select nothing
    if isinstance(output, np.ndarray):
        assert output.size == 0
    elif isinstance(output, list):
        assert len(output) == 0
    assert len(mapdl._get_selected_("node")) == 0


def test_pick_node_special_cases(mapdl, make_block):
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.edele("all")
    mapdl.nsel("s", "node", "", 1)
    mapdl.nsel("a", "node", "", 2)
    mapdl.nsel("inver")
    mapdl.ndele("all")

    # we pick nothing
    def debug_orders_0(pl, point):
        pl = pl.scene
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        pl.iren._mouse_move(int(width * point[0]), int(height * point[1]))

    mapdl.nsel("S", "node", "", 1)
    point = (285 / 1024, 280 / 800)
    mapdl.nsel("a", "node", "", 2)
    selected = mapdl.nsel(
        "S", "P", _debug=lambda x: debug_orders_0(x, point=point), tolerance=0.2
    )  # Selects node 2
    assert selected == []
    assert np.allclose(mapdl._get_selected_("node"), [1, 2])

    # we pick something already picked
    # we just make sure the number is not repeated and there is no error.
    def debug_orders_1(pl, point):
        pl = pl.scene
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        # First click
        pl.iren._mouse_left_button_press(int(width * point[0]), int(height * point[1]))
        pl.iren._mouse_left_button_release(width, height)
        # Second click
        pl.iren._mouse_left_button_press(int(width * point[0]), int(height * point[1]))
        pl.iren._mouse_left_button_release(width, height)
        pl.iren._mouse_move(int(width * point[0]), int(height * point[1]))

    mapdl.nsel("S", "node", "", 1)
    point = (285 / 1024, 280 / 800)
    mapdl.nsel("a", "node", "", 2)
    selected = mapdl.nsel(
        "S", "P", _debug=lambda x: debug_orders_1(x, point=point), tolerance=0.1
    )  # Selects node 2
    assert selected is not None


def test_pick_node_select_unselect_with_mouse(mapdl, make_block):
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.edele("all")
    mapdl.nsel("s", "node", "", 1)
    mapdl.nsel("a", "node", "", 2)
    mapdl.nsel("inver")
    mapdl.ndele("all")

    # we pick something already picked
    # we just make sure the number is not repeated and there is no error.
    def debug_orders_1(pl, point):
        pl = pl.scene
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        # First click- selecting
        pl.iren._mouse_left_button_press(int(width * point[0]), int(height * point[1]))
        pl.iren._mouse_left_button_release(width, height)

        pl.iren._simulate_keypress("u")  # changing to unselecting
        pl._inver_mouse_click_selection = True  # making sure

        # Second click- unselecting
        pl.iren._mouse_left_button_press(int(width * point[0]), int(height * point[1]))
        pl.iren._mouse_left_button_release(width, height)
        pl.iren._mouse_move(int(width * point[0]), int(height * point[1]))
        # so we have selected nothing

    mapdl.nsel("S", "node", "", 1)
    point = (285 / 1024, 280 / 800)
    mapdl.nsel("a", "node", "", 2)
    selected = mapdl.nsel(
        "S", "P", _debug=lambda x: debug_orders_1(x, point=point), tolerance=0.1
    )  # Selects node 2
    assert selected == []


@pytest.mark.parametrize(
    "selection",
    ["S", "R", "A", "U"],
)
def test_pick_areas(mapdl, make_block, selection):
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.edele("all")
    mapdl.asel("s", "area", "", 1)
    mapdl.asel("a", "area", "", 2)

    def debug_orders(pl, point):
        pl = pl.scene
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        if pl._picking_right_clicking_observer is None:
            pl.iren._mouse_left_button_press(
                int(width * point[0]), int(height * point[1])
            )
            pl.iren._mouse_left_button_release(width, height)
        else:
            pl.iren._mouse_right_button_press(
                int(width * point[0]), int(height * point[1])
            )
            pl.iren._mouse_right_button_release(width, height)
        pl.iren._mouse_move(int(width * point[0]), int(height * point[1]))

    mapdl.asel("S", "area", "", 1)
    if selection == "R" or selection == "U":
        point_to_pick = (285 / 1024, 280 / 800)
        mapdl.asel("a", "area", "", 2)
    elif selection == "A":
        point_to_pick = (285 / 1024, 280 / 800)
    else:
        point_to_pick = (0.5, 0.5)

    selected = mapdl.asel(
        selection,
        "P",
        "area",
        _debug=lambda x: debug_orders(x, point=point_to_pick),
        tolerance=0.2,
    )  # Selects node 2

    assert isinstance(selected, (list, np.ndarray))
    if isinstance(selected, np.ndarray):
        assert selected.all()
    else:
        assert selected
    assert len(selected) > 0

    if selection != "U":
        assert sorted(selected) == sorted(mapdl._get_selected_("area"))

    if selection == "S":
        assert selected == [2]  # area where the point clicks is area 2.
    elif selection == "R":
        assert selected == [1]  # area where the point clicks is area 282.
    elif selection == "A":
        assert 6 in selected
        assert len(selected) > 1
    elif selection == "U":
        assert 282 not in selected
        assert 2 in selected


@requires("pyvista")
def test_plotter_input(mapdl, make_block):
    import pyvista as pv

    pl = MapdlPlotter()
    pl2 = mapdl.eplot(return_plotter=True, plotter=pl)
    assert pl is pl2
    pl2.show()  # plotting for catching

    # invalid plotter type
    with pytest.raises(TypeError):
        pl2 = mapdl.eplot(return_plotter=True, plotter=[])

    pl_pv = pv.Plotter()
    pl3 = mapdl.eplot(return_plotter=True, plotter=pl_pv)
    assert pl3.scene is pl_pv
    pl3.show()


def test_cpos_input(mapdl, make_block):
    cpos = [
        (0.3914, 0.4542, 0.7670),
        (0.0243, 0.0336, -0.0222),
        (-0.2148, 0.8998, -0.3796),
    ]

    cpos1 = mapdl.eplot(cpos=cpos, return_cpos=True)
    assert np.allclose(np.array(cpos), np.array([each for each in cpos1]), rtol=1e-4)


def test_show_bounds(mapdl, make_block):
    default_bounds = [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0]
    pl = mapdl.eplot(show_bounds=True, return_plotter=True)

    assert pl.scene.bounds
    assert len(pl.scene.bounds) == 6
    assert pl.scene.bounds != default_bounds
    pl.show()  # plotting for catching


def test_background(mapdl, make_block):
    default_color = "#4c4c4cff"
    pl = mapdl.eplot(background="red", return_plotter=True)
    assert pl.scene.background_color != default_color
    assert pl.scene.background_color == "red"
    pl.show()  # plotting for catching


def test_plot_nodal_values(mapdl, make_block):
    assert mapdl.post_processing.plot_nodal_values("U", "X") is None
    assert mapdl.post_processing.plot_nodal_values("U", "Y") is None
    assert mapdl.post_processing.plot_nodal_values("U", "Z") is None


def test_lsel_iterable(mapdl, make_block):
    assert np.allclose(
        mapdl.lsel("S", "line", "", [1, 2, 3], "", ""), np.array([1, 2, 3])
    )


def test_asel_iterable(mapdl, make_block):
    assert np.allclose(
        mapdl.asel("S", "area", "", [1, 2, 3], "", ""), np.array([1, 2, 3])
    )


def test_vsel_iterable_and_kswp(mapdl, make_block):
    mapdl.run("VGEN, 5, 1, , , 100, , , , , ")
    assert np.allclose(
        mapdl.vsel("S", "volu", "", [1, 2, 4], "", ""), np.array([1, 2, 4])
    )
    mapdl.vsel("S", "volu", "", [1], "", "", kswp=1)
    assert np.allclose(mapdl.geometry.vnum, [1]) and np.allclose(
        mapdl.geometry.anum, [1, 2, 3, 4, 5, 6]
    )


def test_color_areas(mapdl, make_block):
    mapdl.aplot(color_areas=True)


@pytest.mark.parametrize(
    "color_areas",
    [
        ["red", "green", "blue", "yellow", "white", "purple"],
        [
            [255, 255, 255],
            [255, 255, 0],
            [255, 0, 0],
            [0, 255, 0],
            [0, 255, 255],
            [0, 0, 0],
        ],
        255
        * np.array([[1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 1, 0], [0, 1, 1], [0, 0, 0]]),
    ],
)
def test_color_areas_individual(mapdl, make_block, color_areas):
    # we do rely on the `pytest-pyvista` extension to deal with the differences
    mapdl.aplot(color_areas=color_areas)


def test_color_areas_error(mapdl, make_block):
    color_areas = ["red", "green", "blue"]
    with pytest.raises(ValueError):
        mapdl.aplot(color_areas=color_areas)


def test_WithInterativePlotting(mapdl, make_block):
    mapdl.eplot(graphics_backend=GraphicsBackend.MAPDL)
    jobname = mapdl.jobname.upper()

    def filtering(file_name):
        file_name = file_name.upper()
        if file_name.startswith(jobname) and file_name.endswith(".PNG"):
            return True
        else:
            return False

    list_files = sorted([each for each in mapdl.list_files() if filtering(each)])
    last_png = list_files[0]

    if mapdl.is_local:
        last_png = mapdl.directory / last_png
    else:
        mapdl.download(last_png)

    # the file size will be 3kb if the image is empty.
    assert os.path.getsize(last_png) // 1024 > 4  # kbs

    # cleaning
    os.remove(last_png)


def test_file_type_for_plots(mapdl, cleared):
    assert mapdl.file_type_for_plots in ["PNG", "TIFF", "PNG", "VRML", "TERM", "CLOSE"]

    mapdl.file_type_for_plots = "TIFF"
    assert mapdl.file_type_for_plots == "TIFF"

    with pytest.raises(ValueError):
        mapdl.file_type_for_plots = "asdf"

    mapdl.default_plot_file_type = "PNG"
    n_files_ending_png_before = len(
        [each for each in mapdl.list_files() if each.endswith(".png")]
    )

    mapdl.eplot(graphics_backend=GraphicsBackend.MAPDL)
    n_files_ending_png_after = len(
        [each for each in mapdl.list_files() if each.endswith(".png")]
    )

    assert n_files_ending_png_before + 1 == n_files_ending_png_after


@pytest.mark.parametrize("entity", ["KP", "LINE", "AREA", "VOLU", "NODE", "ELEM"])
def test_cmplot_individual(mapdl, make_block, entity):
    mapdl.allsel()
    mapdl.cm("tmp_cm", entity=entity)
    mapdl.cmplot("tmp_cm")


@pytest.mark.parametrize("label", ["N", "P"])
def test_cmplot_label_error(mapdl, make_block, label):
    with pytest.raises(ValueError):
        mapdl.cmplot(label)


def test_cmplot_entity_error(mapdl, make_block):
    with pytest.raises(ValueError):
        mapdl.cmplot("all", "non_valid_entity")


def test_cmplot_incorrect_entity(mapdl, make_block):
    mapdl.allsel()
    mapdl.cm("tmp_cm", entity="NODE")
    with pytest.raises(ValueError):
        mapdl.cmplot("tmp_cm", "KP")


def test_cmplot_component_not_exist(mapdl, make_block):
    with pytest.raises(ComponentDoesNotExits):
        mapdl.cmplot("not_exist")


@pytest.mark.parametrize("entity", ["KP", "NODE"])
def test_cmplot_all(mapdl, make_block, entity):
    mapdl.allsel()
    ids = np.array([1, 2, 3, 4])
    if entity == "KP":
        ent = mapdl.geometry.get_keypoints(return_as_array=True)
        func_sel = mapdl.ksel
    else:
        ent = mapdl.mesh.nodes
        func_sel = mapdl.nsel

    func_sel("S", vmin=ids[:2])
    mapdl.cm("tmp_cm1", entity=entity)

    func_sel("S", vmin=ids[2:])
    mapdl.cm("tmp_cm2", entity=entity)

    pl = mapdl.cmplot("all", entity, return_plotter=True)

    assert np.allclose(pl.meshes[0].points, ent[ids - 1])
    pl.show()


def test_cuadratic_beam(mapdl, cuadratic_beam_problem):
    mapdl.post1()
    mapdl.set(1)
    assert (
        mapdl.post_processing.plot_nodal_displacement(
            "NORM", line_width=10, render_lines_as_tubes=True, smooth_shading=True
        )
        is None
    )


@pytest.mark.parametrize("background", ["white", "black", "green", "red"])
def test_labels_colors_background(mapdl, make_block, background):
    # Test if the labels change color according background
    mapdl.nplot(background=background, nnum=True)


def test_vplot_show_volume_numbering(mapdl, make_block):
    mapdl.vplot(show_volume_numbering=True)


def test_vplot_area_numbering(mapdl, make_block):
    mapdl.vplot(show_area_numbering=True)


def test_vplot_line_numbering(mapdl, make_block):
    mapdl.vplot(show_line_numbering=True)


def test_vplot_multi_numbering(mapdl, make_block):
    mapdl.vplot(
        show_area_numbering=True, show_line_numbering=True, show_volume_numbering=True
    )


def test_vplot_color(mapdl, make_block):
    mapdl.vplot(color="gray")


def test_vplot_cpos(mapdl, make_block):
    mapdl.vplot(cpos="xy")


def test_vplot_multiargs(mapdl, make_block):
    mapdl.vplot(
        color="gray",
        cpos="xy",
        show_volume_numbering=True,
        show_line_numbering=False,
        show_area_numbering=True,
    )


def test_node_numbering_order(mapdl, cleared):
    # create nodes
    for node in range(1, 6):
        mapdl.n(node, (node - 1) * 0.01)  # only need to define the X dimension

    pl = mapdl.nplot(nnum=True, return_plotter=True, font_size=32)
    assert np.allclose(mapdl.mesh.nodes, pl.meshes[0].points)
    # There is no way to retrieve labels from the plotter object. So we cannot
    # test it.
    pl.show()


def test_lplot_line(mapdl, cleared):
    # Create keypoints 3 keypoints
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)
    mapdl.k(3, 1, 1, 0)

    # Create line connecting keypoints 1 and 2
    mapdl.l(1, 2)

    # Plot the geometry
    mapdl.lplot(
        show_line_numbering=False, show_keypoint_numbering=True, color_lines=True
    )


@pytest.mark.parametrize(
    "func,entity",
    [("vplot", "VOLU"), ("aplot", "AREA"), ("lplot", "LINE"), ("kplot", "KP")],
)
@pytest.mark.parametrize("partial", [True, False])
def test_xplot_not_changing_geo_selection(mapdl, cleared, func, entity, partial):
    mapdl.prep7()
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.block(1, 2, 1, 2, 1, 2)
    mapdl.block(2, 3, 2, 3, 2, 3)

    mapdl.geometry._select_items(1, entity, "S")
    mapdl.cm("selection1", entity)
    mapdl.cmsel("u", "selection1")

    mapdl.geometry._select_items(2, entity, "S")
    mapdl.cm("selection2", entity)

    if not partial:
        mapdl.allsel()
        mapdl.cmsel("all")

    fn = getattr(mapdl, func)
    check_geometry(mapdl, fn)


def test_xplot_not_changing_geo_selection2(mapdl, cleared):
    mapdl.rectng(0, 1, 0, 1)
    mapdl.cm("area1", "area")
    mapdl.cmsel("u", "area1")
    mapdl.rectng(2, 4, -1, 1)
    mapdl.cm("area2", "area")
    mapdl.allsel()
    mapdl.cmsel("all")

    check_geometry(mapdl, mapdl.aplot)


@pytest.mark.parametrize(
    "plot_func,entity,gen_func,arg1,arg2",
    [
        ("vplot", "VOLU", "block", (0, 1, 0, 1, 0, 1), (1, 2, 1, 2, 1, 2)),
        # Uncommenting the following lines, raise an exception for channel not
        # alive. See #3421
        # ("aplot", "AREA", "rectng", (0, 1, 0, 1), (1, 2, 1, 2)),
        # ("lplot", "LINE", "l", (1, 1, 1), (1, -1, 1)),
        # ("kplot", "KP", "k", ("", 0, 0, 0), ("", 1, 1, 1)),
    ],
)
def test_xplot_not_changing_geo_selection_components(
    mapdl, cleared, plot_func, entity, gen_func, arg1, arg2
):
    mapdl.prep7()
    gen_func = getattr(mapdl, gen_func)

    if entity == "LINE":
        kp0 = mapdl.k("", 0, 0, 0)
        kp1 = mapdl.k("", 1, 1, 1)
        mapdl.l(kp0, kp1)
    else:
        gen_func(*arg1)

    mapdl.cm("select1", entity)
    mapdl.cmsel("u", "select1")

    if entity == "LINE":
        kp2 = mapdl.k("", 0, 0, 0)
        kp3 = mapdl.k("", *arg2)
        mapdl.l(kp2, kp3)
    else:
        gen_func(*arg2)

    mapdl.cm("select2", entity)

    mapdl.allsel()
    mapdl.cmsel("all")

    plot_func = getattr(mapdl, plot_func)
    check_geometry(mapdl, plot_func)


@pytest.mark.parametrize("quality", [101, -2, 0, "as"])
def test_aplot_quality_fail(mapdl, make_block, quality):
    with pytest.raises(
        ValueError,
        match="The argument 'quality' can only be an integer between 1 and 10",
    ):
        mapdl.aplot(quality=quality)


@patch("ansys.mapdl.core.Mapdl.is_png_found", lambda *args, **kwargs: False)
def test_plot_path(mapdl, tmpdir):
    mapdl.graphics("POWER")

    with pytest.raises(
        MapdlRuntimeError,
        match="One possible reason is that the graphics device is not correct",
    ):
        mapdl.eplot(graphics_backend=GraphicsBackend.MAPDL)


def test_add_mesh():
    """Test the add_mesh method from MapdlPlotter class."""
    import pyvista as pv

    cube1 = pv.Cube()
    pl1 = MapdlPlotter()
    pl1.add_mesh(cube1)

    cube2 = pv.Cube()
    meshes_dict = [
        {
            "mesh": cube2,
            "scalars": np.random.default_rng(seed=1).random((8, 3)),
        }
    ]

    pl2 = MapdlPlotter()
    pl2.add_mesh(meshes_dict)

    cube3 = pv.Cube()
    sphere = pv.Sphere()

    pl3 = MapdlPlotter()
    pl3.add_mesh([cube3, sphere])

    assert pl1.meshes[0] == cube1
    assert pl2.meshes[0] == cube2
    assert pl3.meshes[0] == cube3
    assert pl3.meshes[1] == sphere


def test_plot_path_screenshoot(mapdl, cleared, tmpdir):
    mapdl.graphics("POWER")
    # mapdl.screenshot is not affected by the device.
    # It should not raise exceptions
    scheenshot_path = os.path.join(tmpdir, "screenshot.png")
    mapdl.screenshot(scheenshot_path)

    assert os.path.exists(scheenshot_path)
    assert os.path.getsize(scheenshot_path) > 100  # check if it is not empty

    # Returning to previous state.
    mapdl.graphics("FULL")


def test_deprecated_params(mapdl, make_block):
    with pytest.warns(DeprecationWarning, match="'vtk' and 'use_vtk' are deprecated"):
        mapdl.eplot(vtk=True)
    with pytest.warns(DeprecationWarning, match="'vtk' and 'use_vtk' are deprecated"):
        mapdl.eplot(vtk=False)
