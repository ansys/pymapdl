# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Test geometry commands"""
import numpy as np
import pytest

from conftest import has_dependency, requires

if has_dependency("pyvista"):
    import pyvista as pv

from ansys.mapdl.core.mapdl_geometry import Geometry, LegacyGeometry


def test_keypoint_selection(mapdl, cleared):
    def generate_random_kp():
        mapdl.k("", *np.random.random(3))

    # create n random rectangles
    n_item = 10
    for i in range(n_item):
        generate_random_kp()

    # select every other area
    rng = range(1, n_item + 1, 2)
    items = mapdl.geometry.keypoint_select(rng, return_selected=True)
    assert np.allclose(items, rng)

    items = mapdl.geometry.keypoint_select(None, return_selected=True)
    assert items is None

    items = mapdl.geometry.keypoint_select("ALL", return_selected=True)
    assert np.allclose(items, range(1, n_item + 1))


def test_line_selection(mapdl, cleared):
    def generate_random_line():
        k0 = mapdl.k("", *np.random.random(3))
        k1 = mapdl.k("", *np.random.random(3))
        mapdl.l(k0, k1)

    # create n random rectangles
    n_item = 10
    for i in range(n_item):
        generate_random_line()

    # select every other area
    rng = range(1, n_item + 1, 2)
    items = mapdl.geometry.line_select(rng, return_selected=True)
    assert np.allclose(items, rng)

    items = mapdl.geometry.line_select(None, return_selected=True)
    assert items is None

    items = mapdl.geometry.line_select("ALL", return_selected=True)
    assert np.allclose(items, range(1, n_item + 1))


def test_area_selection(mapdl, cleared):
    def generate_random_area():
        start_x, start_y, height, width = np.random.random(4)
        mapdl.blc4(start_x * 10, start_y * 10, height, width)

    # create n random rectangles
    n_item = 10
    for i in range(n_item):
        generate_random_area()

    # select every other area
    rng = range(1, n_item + 1, 2)
    items = mapdl.geometry.area_select(rng, return_selected=True)
    assert np.allclose(items, rng)

    items = mapdl.geometry.area_select(None, return_selected=True)
    assert items is None

    items = mapdl.geometry.area_select("ALL", return_selected=True)
    assert np.allclose(items, range(1, n_item + 1))


def test_volu_selection(mapdl, cleared):
    def generate_random_volu():
        start_x, start_y, height, width, depth = np.random.random(5)
        mapdl.blc4(start_x * 10, start_y * 10, height, width, depth)

    # create n random volumes
    n_item = 20
    for i in range(n_item):
        generate_random_volu()

    # select every other volu
    rng = range(1, n_item + 1, 2)
    items = mapdl.geometry.volume_select(rng, return_selected=True)
    assert np.allclose(items, rng)

    items = mapdl.geometry.volume_select(None, return_selected=True)
    assert items is None

    items = mapdl.geometry.volume_select("ALL", return_selected=True)
    assert np.allclose(items, range(1, n_item + 1))


def test_vdrag(mapdl, cleared):
    # create a square with a hole in it.
    anum0 = mapdl.blc4(0, 0, 1, 1)
    anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
    aout = mapdl.asba(anum0, anum1)

    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    l0 = mapdl.l(k0, k1)
    assert "DRAG AREAS" in mapdl.vdrag(aout, nlp1=l0)


def test_vext(mapdl, cleared):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    k2 = mapdl.k("", 0, 0, 0.5)
    carc0 = mapdl.circle(k0, 1, k1)
    a0 = mapdl.al(*carc0)

    # next, and extrude it
    mapdl.vext(a0, dz=4)


def test_vrotate(mapdl, cleared):
    # first, create an area from a circle
    hoop_radius = 10
    hoop_thickness = 0.5
    k0 = mapdl.k("", hoop_radius, 0, 0)
    k1 = mapdl.k("", hoop_radius, 1, 0)
    k2 = mapdl.k("", hoop_radius, 0, hoop_thickness)
    carc0 = mapdl.circle(k0, 1, k1)
    a0 = mapdl.al(*carc0)

    # define a Z-axis
    k_axis0 = mapdl.k("", 0, 0, 0)
    k_axis1 = mapdl.k("", 0, 0, 1)

    # Rotate about the Z-axis.  By default it will rotate all 360 degrees
    mapdl.vrotat(a0, pax1=k_axis0, pax2=k_axis1)


def test_vsymm(mapdl, cleared):
    vnum = mapdl.blc4(1, 1, 1, 1, depth=1)
    mapdl.vsymm("X", vnum)
    assert mapdl.geometry.vnum.size == 2


def test_va(mapdl, cleared):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 1, 1, 1)

    # create faces
    a0 = mapdl.a(k0, k1, k2)
    a1 = mapdl.a(k0, k1, k3)
    a2 = mapdl.a(k1, k2, k3)
    a3 = mapdl.a(k0, k2, k3)

    # generate the volume
    vnum = mapdl.va(a0, a1, a2, a3)
    assert vnum == 1


def test_kbetw(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    assert mapdl.kbetw(k0, k1) == 3


def test_kdist(cleared, mapdl):
    kp0 = (0, 10, -3)
    kp1 = (-1e10, 10, 4)

    knum0 = mapdl.k("", *kp0)
    knum1 = mapdl.k("", *kp1)
    kpdist, xdist, ydist, zdist = mapdl.kdist(knum0, knum1)
    assert kpdist == round(
        np.sqrt(
            (kp1[0] - kp0[0]) ** 2 + (kp1[1] - kp0[1]) ** 2 + (kp1[2] - kp0[2]) ** 2
        ),
        7,
    )
    assert xdist == kp1[0] - kp0[0]
    assert ydist == kp1[1] - kp0[1]
    assert zdist == kp1[2] - kp0[2]


# kept here for potential usage
def test_kfill(cleared, mapdl):
    kp0 = (0, 0, 0)
    kp1 = (10, 0, 0)

    knum0 = mapdl.k("", *kp0)
    knum1 = mapdl.k("", *kp1)
    mapdl.kfill(knum0, knum1, 8, ninc=1)


def test_kl(cleared, mapdl):
    kp0 = (0, 0, 0)
    kp1 = (10, 0, 0)
    knum0 = mapdl.k("", *kp0)
    knum1 = mapdl.k("", *kp1)
    lnum = mapdl.l(knum0, knum1)

    assert mapdl.kl(lnum, 0.5) == knum1 + 1


def test_knode(cleared, mapdl):
    nnum = mapdl.n("", 1, 2, 3)
    knum1 = mapdl.knode("", nnum)
    assert knum1 == 1


def test_l2ang(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    k2 = mapdl.k("", 0, 0, 0.5)
    carc0 = mapdl.circle(k0, 1, k1)
    carc1 = mapdl.circle(k2, 1, k1)
    lnum = mapdl.l2ang(carc0[0], carc1[0], 90, 90)
    assert lnum == 11


def test_spline(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0.2, 0.2, 0)
    k2 = mapdl.k("", 0.4, 0.3, 0)
    k3 = mapdl.k("", 0.6, 0.5, 0)
    k4 = mapdl.k("", 0.8, 0.3, 0)
    assert mapdl.spline(k0, k1, k2, k3, k4) == [1, 2, 3, 4]


def test_ltan(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    k2 = mapdl.k("", -1, 1.5, 0)
    carc = mapdl.circle(k0, 1, k1, arc=90)
    assert mapdl.ltan(carc[0], k2) == 2


def test_adrag(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    carc = mapdl.circle(k0, 1, k1, arc=90)
    l0 = mapdl.l(k0, k1)
    assert "2" in mapdl.adrag(carc[0], nlp1=l0)


def test_l2tan(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)

    k2 = mapdl.k("", -1.5, 1.5, 0)
    k3 = mapdl.k("", -1.5, 1.5, 1)

    carc0 = mapdl.circle(k0, 1, k1, arc=90)
    carc1 = mapdl.circle(k2, 1, k3, arc=90)
    lnum = mapdl.l2tan(1, 2)
    assert lnum == 3


def test_lang(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    lnum = mapdl.l(k0, k1)
    k2 = mapdl.k("", 1, 1, 0)

    # output is three as the first line is split
    assert mapdl.lang(lnum, k2, 60) == 3


def test_larc(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 1, 0)
    k2 = mapdl.k("", 0, 1, 0)
    assert mapdl.larc(k0, k1, k2, 2) == 1


def test_kcenter(cleared, mapdl):
    # compute the center of a circle
    x, y, z = 0 + 1j, 1 + 0j, 0 - 1j

    # commented out should we wish to confirm the coordinates
    # w = z-x
    # w /= y-x
    # c = (x-y)*(w-abs(w)**2)/2j/w.imag-x

    k0 = mapdl.k("", x.real, x.imag, 0)
    k1 = mapdl.k("", y.real, y.imag, 0)
    k2 = mapdl.k("", z.real, z.imag, 0)
    k3 = mapdl.kcenter("KP", k0, k1, k2)
    assert k3 == k2 + 1


def test_blc4(cleared, mapdl):
    assert mapdl.blc4(0, 0, 1, 1) == 1


def test_kbetw_blc4(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    assert mapdl.kbetw(k0, k1) == 3


def test_asba(cleared, mapdl):
    anum0 = mapdl.blc4(0, 0, 1, 1)
    anum1 = mapdl.blc4(0.25, 0.25, 0.5, 0.5)
    aout = mapdl.asba(anum0, anum1)
    assert aout == 3


def test_cyl4(cleared, mapdl):
    assert mapdl.cyl4(0, 0, 1, depth=10) == 1


def test_k(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    assert k0 == 1
    k1 = mapdl.k(2, 0, 0, 1)
    assert k1 == 2


def test_l(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    assert l0 == 1


def test_a(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2)
    assert a0 == 1


def test_larea(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert mapdl.larea(k0, k2, a0) == 5


def test_lextnd(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 0, 1)
    carcs = mapdl.circle(k0, 1, k1, arc=90)
    mapdl.lextnd(carcs[0], 3, 1)


def test_lfillt(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 0, 1, 0)
    k2 = mapdl.k("", 1, 0, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k0, k2)
    assert mapdl.lfillt(l0, l1, 0.25) == 3


def test_lstr(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 1, 1)
    assert mapdl.lstr(k0, k1) == 1


def test_lcomb(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 0, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k0, k2)
    assert mapdl.lcomb(l0, l1) == 1


def test_v(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 0, 1, 0)
    k3 = mapdl.k("", 0, 0, 1)
    v0 = mapdl.v(k0, k1, k2, k3)
    assert v0 == 1


def test_n(cleared, mapdl):
    n0 = mapdl.n("", 0, 0, 0)
    assert n0 == 1
    n1 = mapdl.n(2, 0, 0, 1)
    assert n1 == 2


def test_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 2, 1, 0)
    l0 = mapdl.bsplin(k0, k1, k2)
    assert l0 == 1


def test_a_bsplin(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    a0 = mapdl.a(k0, k1, k2, k3)
    assert a0 == 1


def test_al(cleared, mapdl):
    k0 = mapdl.k("", 0, 0, 0)
    k1 = mapdl.k("", 1, 0, 0)
    k2 = mapdl.k("", 1, 1, 0)
    k3 = mapdl.k("", 0, 1, 0)
    l0 = mapdl.l(k0, k1)
    l1 = mapdl.l(k1, k2)
    l2 = mapdl.l(k2, k3)
    l3 = mapdl.l(k3, k0)
    a0 = mapdl.al(l0, l1, l2, l3)
    assert a0 == 1


def test_bcl5(cleared, mapdl):
    # test both the area and volume cases
    assert mapdl.blc5(width=0.5, height=0.5) == 1
    assert mapdl.blc5(width=1, height=4, depth=9) == 1


def test_block(cleared, mapdl):
    assert mapdl.block(0, 1, 0, 2, 1, 4) == 1


def test_con4(cleared, mapdl):
    assert mapdl.con4(rad1=3, rad2=0, depth=10) == 1


def test_cone(cleared, mapdl):
    assert mapdl.cone(rbot=5, rtop=1, z1=0, z2=10, theta1=180, theta2=90) == 1


def test_cyl5(cleared, mapdl):
    # test both the area and volume cases
    assert mapdl.cyl5(xedge1=1, yedge1=1, xedge2=2, yedge2=2) == 1
    assert mapdl.cyl5(xedge1=1, yedge1=1, xedge2=2, yedge2=2, depth=5) == 1


def test_cylind(cleared, mapdl):
    assert mapdl.cylind(0.9, 1, z1=0, z2=5) == 1


def test_pcirc(cleared, mapdl):
    assert mapdl.pcirc(0.95, 1) == 1


def test_rectng(cleared, mapdl):
    assert mapdl.rectng(0.5, 1.5, 0.5, 2.5) == 1


def test_sph4(cleared, mapdl):
    assert mapdl.sph4(0, 0, rad1=0.9, rad2=1.0) == 1


def test_sphere(cleared, mapdl):
    assert mapdl.sphere(rad1=0.95, rad2=1.0, theta1=90, theta2=270) == 1


def test_sph5(cleared, mapdl):
    assert mapdl.sph5(xedge1=1, yedge1=1, xedge2=2, yedge2=2) == 1


def test_ndist(cleared, mapdl):
    node1 = (0, -5, 13)
    node2 = (-10, 70, 1)

    node_num1 = mapdl.n("", *node1)
    node_num2 = mapdl.n("", *node2)
    node_dist, node_xdist, node_ydist, node_zdist = mapdl.ndist(node_num1, node_num2)
    assert node_dist == round(
        np.sqrt(
            (node2[0] - node1[0]) ** 2
            + (node2[1] - node1[1]) ** 2
            + (node2[2] - node1[2]) ** 2
        ),
        7,
    )
    assert node_xdist == node2[0] - node1[0]
    assert node_ydist == node2[1] - node1[1]
    assert node_zdist == node2[2] - node1[2]


def test_empty_model(mapdl, cleared):
    assert mapdl.geometry.knum.size == 0
    assert mapdl.geometry.lnum.size == 0
    assert mapdl.geometry.anum.size == 0
    assert mapdl.geometry.vnum.size == 0


@requires("pyvista")
@pytest.mark.parametrize(
    "entity,number", (["keypoints", 8], ["lines", 12], ["areas", 6], ["volumes", 1])
)
def test_entities_simple_cube(mapdl, cube_solve, entity, number):
    entity = getattr(mapdl.geometry, entity)
    assert len(entity) == number
    assert isinstance(entity, pv.MultiBlock)


@requires("pyvista")
@pytest.mark.parametrize(
    "entity,number", (["keypoints", 26], ["lines", 45], ["areas", 28], ["volumes", 6])
)
def test_entities_multiple_bodies(mapdl, contact_geom_and_mesh, entity, number):
    entity = getattr(mapdl.geometry, entity)
    assert len(entity) == number
    assert isinstance(entity, pv.MultiBlock)


def test_create_geometry(mapdl, cleared):
    assert isinstance(mapdl._create_geometry(), Geometry)


@requires("pyvista")
def test_get_lines(mapdl, contact_geom_and_mesh):
    assert isinstance(mapdl.geometry.get_lines(), pv.PolyData)


@requires("pyvista")
@pytest.mark.parametrize(
    "entity,number", (["keypoints", 26], ["lines", 45], ["areas", 28], ["volumes", 6])
)
def test_geometry_get_apis(mapdl, contact_geom_and_mesh, entity, number):
    func = getattr(mapdl.geometry, f"get_{entity}")

    default = func()
    assert isinstance(default, pv.PolyData)

    if entity in ["areas", "volumes"]:
        type_ = pv.UnstructuredGrid
    else:
        type_ = pv.PolyData

    as_a_list = func(return_as_list=True)
    assert isinstance(as_a_list, list)
    assert all([isinstance(each, type_) for each in as_a_list])
    assert len(as_a_list) == number

    if "entity" == "keypoints":
        as_an_array = func(return_as_array=True)
        assert isinstance(as_an_array, np.ndarray)
        assert len(as_an_array) == number


@requires("pyvista")
@pytest.mark.parametrize(
    "entity,entity_name,number",
    (
        ["keypoints", "kp", 26],
        ["lines", "line", 45],
        ["areas", "area", 28],
        ["volumes", "volume", 6],
    ),
)
def test_geometry_names(mapdl, contact_geom_and_mesh, entity, entity_name, number):
    func = getattr(mapdl.geometry, entity)

    mb_names = list(func.keys())
    assert len(mb_names) == number

    func1 = getattr(mapdl.geometry, f"{entity[0]}num")
    names = [f"{entity_name} {int(each)}" for each in func1]

    # sorting because the Xnum return this sorted, but the underlying IGES doesn't have to.
    mb_names.sort()
    names.sort()

    assert mb_names == names


@requires("pyvista")
def test_geometry_get_item(mapdl, contact_geom_and_mesh):
    assert isinstance(mapdl.geometry["kp 2"], pv.PolyData)
    assert mapdl.geometry["kp 2"].n_points > 0

    assert isinstance(mapdl.geometry["line 1"], pv.PolyData)
    assert mapdl.geometry["line 1"].n_cells > 0

    assert isinstance(mapdl.geometry["area 1"], pv.UnstructuredGrid)
    assert mapdl.geometry["area 1"].n_cells > 0

    assert isinstance(mapdl.geometry["volume 1"], pv.UnstructuredGrid)
    assert mapdl.geometry["volume 1"].n_cells > 0


@requires("pyvista")
def test_geometry_get_item_error(mapdl, contact_geom_and_mesh):
    with pytest.raises(ValueError):
        mapdl.geometry["l 0"]

    with pytest.raises(ValueError):
        mapdl.geometry["kip 0"]


@requires("pyvista")
def test_geometry_get_block_error(mapdl, contact_geom_and_mesh):
    with pytest.raises(KeyError):
        mapdl.geometry["kp 0"]


@requires("pyvista")
def test_build_legacy_geometry(mapdl, contact_geom_and_mesh):
    leg_geo = LegacyGeometry(mapdl)

    assert np.allclose(
        leg_geo.keypoints(), mapdl.geometry.get_keypoints(return_as_array=True)
    )
    assert isinstance(leg_geo.keypoints(), np.ndarray)

    assert leg_geo.lines() == mapdl.geometry.get_lines()
    assert isinstance(leg_geo.lines(), pv.PolyData)

    assert leg_geo.areas() == mapdl.geometry.get_areas(return_as_list=True)
    assert isinstance(leg_geo.areas(), list)

    assert leg_geo.areas(merge=True) == mapdl.geometry.get_areas()
    assert isinstance(leg_geo.areas(merge=True), pv.PolyData)
