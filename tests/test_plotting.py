"""Unit tests regarding plotting."""
import os

import numpy as np
import pytest
from pyvista.plotting import Plotter

from ansys.mapdl.core.errors import ComponentDoesNotExits
from ansys.mapdl.core.plotting import general_plotter
from conftest import skip_no_xserver


@pytest.fixture
def bc_example(mapdl, make_block):
    mapdl.prep7()

    mapdl.nsel("s", "node", "", 1)
    mapdl.f("all", "FX", 0)
    mapdl.f("all", "FY", 0)
    mapdl.f("all", "FZ", 0)

    mapdl.nsel("s", "node", "", 2)
    mapdl.f("all", "FX", 100)
    mapdl.f("all", "FY", 200)
    mapdl.f("all", "FZ", 100)

    mapdl.nsel("s", "node", "", 3)
    mapdl.d("all", "UX", 0)
    mapdl.d("all", "UY", 0)
    mapdl.d("all", "UZ", 0)

    mapdl.nsel("s", "node", "", 4)
    mapdl.d("all", "UX", 1)
    mapdl.d("all", "UY", 2)
    mapdl.d("all", "UZ", 3)

    mapdl.nsel("all")


@skip_no_xserver
def test_kplot(cleared, mapdl, tmpdir):
    mapdl.k("", 0, 0, 0)
    mapdl.k("", 1, 0, 0)
    mapdl.k("", 1, 1, 0)
    mapdl.k("", 0, 1, 0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl.kplot(savefig=filename)
    assert cpos is None
    assert os.path.isfile(filename)

    mapdl.kplot(vtk=False)  # make sure legacy still works


@skip_no_xserver
def test_lplot(cleared, mapdl, tmpdir):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    mapdl.l(k0, k1)
    mapdl.l(k1, k2)
    mapdl.l(k2, k3)
    mapdl.l(k3, k0)

    filename = str(tmpdir.mkdir("tmpdir").join("tmp.png"))
    cpos = mapdl.lplot(show_keypoint_numbering=True, savefig=filename)
    assert cpos is None
    assert os.path.isfile(filename)

    mapdl.lplot(vtk=False)  # make sure legacy still works


@skip_no_xserver
def test_aplot(cleared, mapdl):
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
    mapdl.aplot(color_areas=True, show_lines=True, show_line_numbering=True)

    mapdl.aplot(quality=100)
    mapdl.aplot(quality=-1)

    # and legacy as well
    mapdl.aplot(vtk=False)


@skip_no_xserver
@pytest.mark.parametrize("vtk", [True, False])
def test_vplot(cleared, mapdl, vtk):
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.vplot(vtk=vtk, color_areas=True)


@skip_no_xserver
def test_nplot(cleared, mapdl):
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=False)


@pytest.mark.parametrize("nnum", [True, False])
@skip_no_xserver
def test_nplot_vtk(cleared, mapdl, nnum):
    mapdl.n(1, 0, 0, 0)
    mapdl.n(11, 10, 0, 0)
    mapdl.fill(1, 11, 9)
    mapdl.nplot(vtk=True, nnum=nnum, background="w", color="k")


@skip_no_xserver
def test_eplot(mapdl, make_block):
    init_elem = mapdl.mesh.n_elem
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    mapdl.eplot(show_node_numbering=True, background="w", color="b")
    mapdl.aplot()  # check aplot and verify it doesn't mess up the element plotting
    assert mapdl.mesh.n_elem == init_elem


@skip_no_xserver
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


@skip_no_xserver
@pytest.mark.parametrize("return_plotter", [True, False])
@pytest.mark.parametrize("plot_bc_legend", [True, False])
@pytest.mark.parametrize("plot_bc_labels", [True, False])
def test_bc_plot_options(
    mapdl, bc_example, return_plotter, plot_bc_legend, plot_bc_labels
):
    p = mapdl.nplot(
        return_plotter=return_plotter,
        plot_bc=True,
        plot_bc_legend=plot_bc_legend,
        plot_bc_labels=plot_bc_labels,
    )

    if return_plotter:
        assert isinstance(p, Plotter)
    else:
        assert p is None


@skip_no_xserver
@pytest.mark.parametrize(
    "bc_labels",
    [
        "Mechanical",
        "mechanical",
        "meCHANICAL",
        "ux",
        "UX",
        ["UX", "UY"],
        "CSGZ",
    ],
)
def test_bc_plot_bc_labels(mapdl, bc_example, bc_labels):
    p = mapdl.nplot(
        return_plotter=True,
        plot_bc=True,
        plot_bc_labels=True,
        bc_labels=bc_labels,
    )
    assert isinstance(p, Plotter)


@skip_no_xserver
@pytest.mark.parametrize(
    "bc_labels",
    [
        "error",
        ["UX", "error"],
    ],
)
def test_bc_plot_bc_labels_error(mapdl, bc_example, bc_labels):
    with pytest.raises(ValueError):
        p = mapdl.nplot(
            return_plotter=True,
            plot_bc=True,
            plot_bc_labels=True,
            bc_labels=bc_labels,
        )


@skip_no_xserver
@pytest.mark.parametrize(
    "bc_target",
    [
        "Nodes",
        "NOdes",
    ],
)
def test_bc_plot_bc_target(mapdl, bc_example, bc_target):
    p = mapdl.nplot(
        return_plotter=True,
        plot_bc=True,
        plot_bc_labels=True,
        bc_target=bc_target,
    )
    assert isinstance(p, Plotter)


@skip_no_xserver
@pytest.mark.parametrize(
    "bc_target",
    [
        ["NOdes"],
        "error",
        ["error"],
        {"error": "Not accepting dicts"},
    ],
)
def test_bc_plot_bc_target_error(mapdl, bc_example, bc_target):
    with pytest.raises(ValueError):
        p = mapdl.nplot(
            return_plotter=True,
            plot_bc=True,
            plot_bc_labels=True,
            bc_target=bc_target,
        )


def test_bc_no_mapdl(mapdl):
    with pytest.raises(ValueError):
        general_plotter(
            [], [], [], plot_bc=True
        )  # mapdl should be an argument if plotting BC


def test_bc_only_one_node(mapdl, bc_example):
    mapdl.nsel("s", "node", "", 1)
    mapdl.nplot(plot_bc=True)


def test_bc_glyph(mapdl, bc_example):
    mapdl.nplot(plot_bc=True, bc_glyph_size=19)
    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_glyph_size="big")


def test_bc_bc_labels(mapdl, bc_example):
    """Test values for 'bc_labels' keyword argument."""
    mapdl.nplot(plot_bc=True, bc_labels="UX")
    mapdl.nplot(plot_bc=True, bc_labels=["Ux", "uy", "VOLT"])
    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_labels=["big"])

    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_labels={"not": "valid"})

    with pytest.raises(ValueError):
        mapdl.nplot(plot_bc=True, bc_labels=["UX", {"not": "valid"}])


def test_all_same_values(mapdl, bc_example):
    """Test the BC glyph size when all the BC have same magnitude."""
    mapdl.nsel("all")
    mapdl.f("all", "FX", 0)
    mapdl.nplot(plot_bc=True, bc_labels="FX")


@pytest.mark.parametrize(
    "selection",
    ["S", "R", "A", "U"],
)
def test_pick_nodes(mapdl, make_block, selection):
    # Cleaning the model a bit
    mapdl.modmsh("detach")  # detaching geom and fem
    mapdl.edele("all")
    mapdl.nsel("s", "node", "", 1)
    mapdl.nsel("a", "node", "", 2)
    mapdl.nsel("inver")
    mapdl.ndele("all")

    def debug_orders(pl, point):
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        pl.iren._mouse_left_button_press(int(width * point[0]), int(height * point[1]))
        pl.iren._mouse_left_button_release(width, height)
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
        tolerance=0.2,
    )  # Selects node 2

    assert isinstance(selected, (list, np.ndarray))
    if isinstance(selected, np.ndarray):
        assert selected.all()
    else:
        assert selected
    assert len(selected) > 0

    if selection != "U":
        assert sorted(selected) == sorted(mapdl._get_selected_("node"))

    if selection == "S":
        assert selected == [1]
    elif selection == "R":
        assert selected == [2]
    elif selection == "A":
        assert 1 in selected
        assert len(selected) > 1
    elif selection == "U":
        assert 2 not in selected
        assert 1 in selected


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
        pl.show(auto_close=False)
        pl.windows_size = (100, 100)
        width, height = pl.window_size
        pl.iren._mouse_left_button_press(int(width * point[0]), int(height * point[1]))
        pl.iren._mouse_left_button_release(width, height)
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
    )
    assert selected == []


def test_plotter_input(mapdl, make_block):
    pl = Plotter(off_screen=True)
    # because in CICD we use 'screen_off', this will trigger a warning,
    # since using 'plotter' will overwrite this kwarg.
    with pytest.warns(UserWarning):
        pl2 = mapdl.eplot(return_plotter=True, plotter=pl)
    assert pl == pl2
    assert pl is pl2

    # invalid plotter type
    with pytest.raises(TypeError):
        pl2 = mapdl.eplot(return_plotter=True, plotter=[])


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

    assert pl.bounds
    assert len(pl.bounds) == 6
    assert pl.bounds != default_bounds


def test_background(mapdl, make_block):
    default_color = "#4c4c4cff"
    pl = mapdl.eplot(background="red", return_plotter=True)
    assert pl.background_color != default_color
    assert pl.background_color == "red"


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


def test_vsel_iterable(mapdl, make_block):
    mapdl.run("VGEN, 5, 1, , , 100, , , , , ")
    assert np.allclose(
        mapdl.vsel("S", "volu", "", [1, 2, 4], "", ""), np.array([1, 2, 4])
    )


def test_color_areas(mapdl, make_block):
    mapdl.aplot(vtk=True, color_areas=True, return_plotter=True)


# This is to remind us that the pl.mesh does not return data for all meshes in CICD.
@pytest.mark.xfail
def test_color_areas_fail(mapdl, make_block):
    pl = mapdl.aplot(vtk=True, color_areas=True, return_plotter=True)
    assert len(np.unique(pl.mesh.cell_data["Data"], axis=0)) == mapdl.geometry.n_area


@skip_no_xserver
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
    pl = mapdl.aplot(vtk=True, color_areas=color_areas, return_plotter=True)
    assert len(np.unique(pl.mesh.cell_data["Data"], axis=0)) == len(color_areas)


def test_color_areas_error(mapdl, make_block):
    color_areas = ["red", "green", "blue"]
    with pytest.raises(ValueError):
        mapdl.aplot(vtk=True, color_areas=color_areas)


def test_WithInterativePlotting(mapdl, make_block):
    mapdl.eplot(vtk=False)
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
        last_png = os.path.join(mapdl.directory, last_png)
    else:
        mapdl.download(last_png)

    # the file size will be 3kb if the image is empty.
    assert os.path.getsize(last_png) // 1024 > 4  # kbs

    # cleaning
    os.remove(last_png)


def test_file_type_for_plots(mapdl):
    assert mapdl.file_type_for_plots in ["PNG", "TIFF", "PNG", "VRML", "TERM", "CLOSE"]

    mapdl.file_type_for_plots = "TIFF"
    assert mapdl.file_type_for_plots == "TIFF"

    with pytest.raises(ValueError):
        mapdl.file_type_for_plots = "asdf"

    mapdl.default_plot_file_type = "PNG"
    n_files_ending_png_before = len(
        [each for each in mapdl.list_files() if each.endswith(".png")]
    )

    mapdl.eplot(vtk=False)
    n_files_ending_png_after = len(
        [each for each in mapdl.list_files() if each.endswith(".png")]
    )

    assert n_files_ending_png_before + 1 == n_files_ending_png_after


@pytest.mark.parametrize("entity", ["KP", "LINE", "AREA", "VOLU", "NODE", "ELEM"])
def test_cmplot_individual(mapdl, make_block, entity):
    mapdl.allsel()
    mapdl.cm("tmp_cm", entity=entity)
    pl = mapdl.cmplot("tmp_cm", return_plotter=True)


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

    assert np.allclose(pl.mesh.points, ent[ids - 1])
