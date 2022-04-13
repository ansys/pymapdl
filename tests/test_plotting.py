"""Unit tests regarding plotting."""
import os

import pytest
from pyvista.plotting import Plotter, system_supports_plotting

skip_no_xserver = pytest.mark.skipif(
    not system_supports_plotting(), reason="Requires active X Server"
)


@pytest.fixture
def bc_example(mapdl, make_block):

    mapdl.prep7()

    mapdl.nsel("s", "node", "", 1)
    mapdl.f("all", "FX", 100)
    mapdl.f("all", "FY", 100)
    mapdl.f("all", "FZ", 100)

    mapdl.nsel("s", "node", "", 2)
    mapdl.d("all", "UX", 0)
    mapdl.d("all", "UY", 0)
    mapdl.d("all", "UZ", 0)

    mapdl.nsel("a", "node", "", 1)


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
        pytest.param("error", marks=pytest.mark.xfail),
        pytest.param(["UX", "error"], marks=pytest.mark.xfail),
        "CSGZ",
    ],
)
def test_bc_plot_bc_labels(mapdl, bc_example, bc_labels):
    p = mapdl.nplot(
        return_plotter=True, plot_bc=True, plot_bc_labels=True, bc_labels=bc_labels
    )
    assert isinstance(p, Plotter)


@skip_no_xserver
@pytest.mark.parametrize(
    "bc_target",
    [
        "Nodes",
        "NOdes",
        pytest.param(["NOdes"], marks=pytest.mark.xfail),
        pytest.param("error", marks=pytest.mark.xfail),
        pytest.param(["error"], marks=pytest.mark.xfail),
        pytest.param({"error": "Not accepting dicts"}, marks=pytest.mark.xfail),
    ],
)
def test_bc_plot_bc_target(mapdl, bc_example, bc_target):
    p = mapdl.nplot(
        return_plotter=True, plot_bc=True, plot_bc_labels=True, bc_target=bc_target
    )
    assert isinstance(p, Plotter)
