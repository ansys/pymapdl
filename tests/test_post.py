# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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

"""Test post-processing module for ansys.mapdl.core"""
import inspect
import re

import numpy as np
import pytest

from conftest import has_dependency, requires

if has_dependency("pyvista"):
    from pyvista import Plotter
    from pyvista.plotting.renderer import CameraPosition
    from ansys.mapdl.core.theme import PyMAPDL_cmap

from ansys.mapdl.core import examples
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.plotting import MapdlPlotter
from ansys.mapdl.core.post import (
    COMPONENT_STRESS_TYPE,
    PRINCIPAL_TYPE,
    STRESS_TYPES,
    PostProcessing,
)


@pytest.fixture(scope="module")
def static_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()

    # cylinder and mesh parameters
    # torque = 100
    radius = 2
    h_tip = 2
    height = 20
    elemsize = 0.5
    # pi = np.arccos(-1)
    force = 100 / radius
    pressure = force / (h_tip * 2 * np.pi * radius)

    mapdl.prep7()
    mapdl.et(1, 186)
    mapdl.et(2, 154)
    mapdl.r(1)
    mapdl.r(2)

    # Aluminum properties (or something)
    mapdl.mp("ex", 1, 10e6)
    mapdl.mp("nuxy", 1, 0.3)
    mapdl.mp("dens", 1, 0.1 / 386.1)
    mapdl.mp("dens", 2, 0)

    # Simple cylinder
    for i in range(4):
        mapdl.cylind(radius, "", "", height, 90 * (i - 1), 90 * i)

    mapdl.nummrg("kp")

    # mesh cylinder
    mapdl.lsel("s", "loc", "x", 0)
    mapdl.lsel("r", "loc", "y", 0)
    mapdl.lsel("r", "loc", "z", 0, height - h_tip)
    mapdl.lesize("all", elemsize * 2)
    mapdl.mshape(0)
    mapdl.mshkey(1)

    mapdl.esize(elemsize)
    mapdl.allsel("all")
    mapdl.vsweep("ALL")
    mapdl.csys(1)
    mapdl.asel("s", "loc", "z", "", height - h_tip + 0.0001)
    mapdl.asel("r", "loc", "x", radius)
    mapdl.local(11, 1)

    mapdl.csys(0)

    # mesh the surface with SURF154
    mapdl.aatt(2, 2, 2, 11)
    mapdl.amesh("all")
    mapdl.prep7()

    # Apply tangential pressure
    mapdl.esel("S", "TYPE", "", 2)
    mapdl.sfe("all", 2, "pres", "", pressure)

    # Constrain bottom of cylinder/rod
    mapdl.asel("s", "loc", "z", 0)
    mapdl.nsla("s", 1)
    mapdl.d("all", "all")
    mapdl.allsel()

    # new solution
    mapdl.run("/SOLU")
    mapdl.antype("static", "new")
    # mapdl.eqslv('pcg', 1e-8)
    mapdl.solve()

    # necessary for any prnsol printouts
    mapdl.header("off", "off", "off", "off", "off", "off")
    nsigfig = 10
    mapdl.format("", "E", nsigfig + 9, nsigfig)
    # mapdl.post1(mute=True)
    # mapdl.set(1, 1)
    mapdl.mute = False


@pytest.fixture(scope="module")
def plastic_solve(mapdl):
    mapdl.mute = True
    mapdl.finish()
    mapdl.clear()
    mapdl.input(examples.verif_files.vmfiles["vm273"])

    mapdl.post1()
    mapdl.set(1, 2)
    mapdl.mute = False


@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_disp(mapdl, static_solve, comp):
    disp_from_grpc = mapdl.post_processing.nodal_displacement(comp)

    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    nnum, disp_from_prns = np.genfromtxt(mapdl.prnsol("U", comp).splitlines()[1:]).T

    assert np.allclose(mapdl.mesh.nnum, nnum)
    assert np.allclose(disp_from_grpc, disp_from_prns)


def test_enum_all(mapdl, static_solve):
    # ensure that element selection status has no effect on the all_enum
    try:
        n_elem = mapdl.mesh.n_elem
        mapdl.esel("S", "ELEM", vmin=10, vmax=19, mute=True)
        mapdl.post_processing._all_enum
        assert len(mapdl.post_processing._all_enum) == n_elem
    finally:
        # static solve is a module fixture, change in state here will affect
        # downstream tests unless reset
        mapdl.allsel(mute=True)


def test_disp_norm_all(mapdl, static_solve):
    # test norm
    disp_norm = mapdl.post_processing.nodal_displacement("NORM")

    x = mapdl.post_processing.nodal_displacement("X")
    y = mapdl.post_processing.nodal_displacement("Y")
    z = mapdl.post_processing.nodal_displacement("Z")
    disp = np.vstack((x, y, z))
    manual_norm = np.linalg.norm(disp, axis=0)
    assert np.allclose(disp_norm, manual_norm)

    # test all
    assert np.allclose(disp.T, mapdl.post_processing.nodal_displacement("ALL"))


@pytest.mark.parametrize("comp", ["X", "Y", "z", "norm"])  # lowercase intentional
@requires("pyvista")
def test_disp_plot(mapdl, static_solve, comp):
    assert (
        mapdl.post_processing.plot_nodal_displacement(
            comp, smooth_shading=True, cmap=PyMAPDL_cmap
        )
        is None
    )


@requires("pyvista")
def test_disp_plot_subselection(mapdl, static_solve, verify_image_cache):
    verify_image_cache.skip = True  # skipping image verification

    mapdl.nsel("S", "NODE", vmin=500, vmax=2000, mute=True)
    mapdl.esel("S", "ELEM", vmin=500, vmax=2000, mute=True)
    assert (
        mapdl.post_processing.plot_nodal_displacement(
            "X", smooth_shading=True, show_node_numbering=True
        )
        is None
    )
    mapdl.allsel()


def test_nodal_eqv_stress(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("S", "PRIN")  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_eqv_stress()

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


@requires("pyvista")
def test_plot_nodal_eqv_stress(mapdl, static_solve, verify_image_cache):
    verify_image_cache.skip = True  # skipping image verification

    assert mapdl.post_processing.plot_nodal_eqv_stress(smooth_shading=True) is None


def test_node_selection(mapdl, static_solve):
    mapdl.nsel("S", "NODE", vmin=1, vmax=2000, mute=True)
    assert mapdl.post_processing.selected_nodes.sum() == 2000

    mapdl.nsel("all", mute=True)
    assert mapdl.post_processing.selected_nodes.sum() == mapdl.mesh.n_node


def test_element_selection(mapdl, static_solve):
    mx_val = 1000
    mapdl.esel("S", "ELEM", vmin=1, vmax=mx_val, mute=True)
    assert mapdl.post_processing.selected_elements.sum() == mx_val

    mapdl.esel("all", mute=True)
    assert mapdl.post_processing.selected_elements.sum() == mapdl.mesh.n_elem


# TODO: add valid result
@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_rot(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_rotation(comp)

    # need a result with ROTX DOF
    # mapdl.post1(mute=True)
    # mapdl.set(1, 1, mute=True)
    # nnum, from_prns = np.genfromtxt(mapdl.prnsol('ROT', comp).splitlines()[1:]).T

    # assert np.allclose(mapdl.mesh.nnum, nnum)
    # assert np.allclose(from_grpc, from_prns)
    assert np.allclose(from_grpc, 0)


@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
@requires("pyvista")
def test_plot_rot(mapdl, static_solve, comp):
    assert mapdl.post_processing.plot_nodal_rotation(comp) is None


# TODO: add valid result
def test_temperature(mapdl, static_solve):
    from_grpc = mapdl.post_processing.nodal_temperature()
    assert np.allclose(from_grpc, 0)


# TODO: add valid result
def test_element_temperature(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    values = mapdl.post_processing.element_temperature()
    assert np.allclose(values, 0)


@requires("pyvista")
def test_plot_element_temperature(mapdl, static_solve):
    mapdl.set(1, 1, mute=True)
    assert mapdl.post_processing.plot_element_temperature() is None


@requires("pyvista")
def test_plot_temperature(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_temperature() is None


# TODO: add valid result
def test_pressure(mapdl, static_solve):
    from_grpc = mapdl.post_processing.nodal_pressure()
    assert np.allclose(from_grpc, 0)


@requires("pyvista")
def test_plot_pressure(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_pressure() is None


# TODO: add valid result
def test_voltage(mapdl, static_solve):
    from_grpc = mapdl.post_processing.nodal_voltage()
    assert np.allclose(from_grpc, 0)


@requires("pyvista")
def test_plot_voltage(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_voltage() is None


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_component_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_component_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("S", "COMP")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "COMP").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


@requires("pyvista")
def test_plot_nodal_component_stress(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_component_stress("X") is None


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_principal_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_principal_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("S", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


@requires("pyvista")
def test_plot_nodal_principal_stress(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_principal_stress(1) is None


def test_nodal_stress_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("S", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_stress_intensity

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


@requires("pyvista")
def test_plot_nodal_stress_intensity(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_stress_intensity() is None


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_total_component_strain(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("EPTO", "COMP", mute=True)  # run twice to clear out warning

    data = np.genfromtxt(mapdl.prnsol("EPTO", "COMP").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    data_ans = data[:, index + 1]
    data = mapdl.post_processing.nodal_total_component_strain(comp)
    data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(data_ans, data)


@requires("pyvista")
def test_plot_nodal_total_component_strain(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_total_component_strain("x") is None


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_principal_total_strain(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_total_principal_strain(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("EPTO", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


@requires("pyvista")
def test_plot_nodal_principal_total_strain(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_total_principal_strain(1) is None


def test_nodal_total_strain_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPTO", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_total_strain_intensity()

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


@requires("pyvista")
def test_plot_nodal_total_strain_intensity(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_total_strain_intensity() is None


def test_nodal_total_eqv_strain(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPTO", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_total_eqv_strain()

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


@requires("pyvista")
def test_plot_nodal_total_eqv_strain(mapdl, static_solve):
    assert (
        mapdl.post_processing.plot_nodal_total_eqv_strain(smooth_shading=True) is None
    )


###############################################################################
@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_component_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_component_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("S", "COMP")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "COMP").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


@requires("pyvista")
def test_plot_nodal_component_stress(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_component_stress("X") is None


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_principal_stress(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_principal_stress(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("S", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(from_grpc, from_prns, atol=1e-5)


@requires("pyvista")
def test_plot_nodal_principal_stress(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_principal_stress(1) is None


def test_nodal_stress_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("S", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_stress_intensity()

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


@requires("pyvista")
def test_plot_nodal_stress_intensity(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_stress_intensity() is None


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_elastic_component_strain(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("EPEL", "COMP", mute=True)  # run twice to clear out warning

    data = np.genfromtxt(mapdl.prnsol("EPEL", "COMP").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    data_ans = data[:, index + 1]
    data = mapdl.post_processing.nodal_elastic_component_strain(comp)
    data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(data_ans, data)


@requires("pyvista")
def test_plot_nodal_elastic_component_strain(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_elastic_component_strain("x") is None


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_elastic_principal_strain(mapdl, static_solve, comp):
    from_grpc = mapdl.post_processing.nodal_elastic_principal_strain(comp)
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("EPEL", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


@requires("pyvista")
def test_plot_nodal_elastic_principal_strain(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_elastic_principal_strain(1) is None


def test_nodal_elastic_strain_intensity(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPEL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_elastic_strain_intensity()

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


@requires("pyvista")
def test_plot_nodal_elastic_strain_intensity(mapdl, static_solve):
    assert mapdl.post_processing.plot_nodal_elastic_strain_intensity() is None


def test_nodal_elastic_eqv_strain(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    mapdl.prnsol("EPEL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_elastic_eqv_strain()

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


@requires("pyvista")
def test_plot_nodal_elastic_eqv_strain(mapdl, static_solve):
    assert (
        mapdl.post_processing.plot_nodal_elastic_eqv_strain(smooth_shading=True) is None
    )


@pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
def test_elem_disp(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    mapdl.allsel()

    disp_from_grpc = mapdl.post_processing.element_displacement(comp)

    # use pretab to get the data
    table_name = "values"
    mapdl.etable(table_name, "U", comp, mute=True)
    arr = np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
    assert np.allclose(arr, disp_from_grpc)


@pytest.mark.parametrize("option", ["min", "max", "avg"])
def test_elem_disp_all(mapdl, static_solve, option):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)

    disp_from_grpc = mapdl.post_processing.element_displacement("ALL", option)

    # use pretab to get the data
    arrays = []
    for comp in ["x", "y", "z"]:
        table_name = "values" + comp
        mapdl.etable(table_name, "U", comp, option=option, mute=True)
        arrays.append(np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1])
    array = np.vstack(arrays).T
    assert np.allclose(array, disp_from_grpc)


def test_elem_disp_norm(mapdl, static_solve):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    disp = mapdl.post_processing.element_displacement("ALL")
    norm_disp = np.linalg.norm(disp, axis=1)
    disp_from_grpc = mapdl.post_processing.element_displacement("NORM")
    assert np.allclose(norm_disp, disp_from_grpc)


@pytest.mark.parametrize("comp", ["X", "Y", "Z", "NORM"])
@requires("pyvista")
def test_elem_disp_plot(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    assert mapdl.post_processing.plot_element_displacement(comp) is None


@pytest.mark.parametrize("component", STRESS_TYPES[::3])
@pytest.mark.parametrize("option", ["min", "max", "avg"])
def test_element_stress(mapdl, static_solve, component, option):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    stress = mapdl.post_processing.element_stress(component, option)

    # use pretab to get the data
    table_name = "values" + component
    mapdl.etable(table_name, "S", component, option=option, mute=True)
    from_pretab = np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
    assert np.allclose(stress, from_pretab)


@pytest.mark.parametrize("comp", ["X", "1", "INT", "EQV"])
@requires("pyvista")
def test_plot_element_stress(mapdl, static_solve, comp):
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    assert mapdl.post_processing.plot_element_stress(comp) is None


@requires("pyvista")
def test_plot_element_values(mapdl, static_solve, verify_image_cache):
    verify_image_cache.high_variance_test = 600
    mapdl.post1(mute=True)
    mapdl.set(1, 1, mute=True)
    assert mapdl.post_processing.plot_element_values("S", "X") is None


###############################################################################


@pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
def test_nodal_plastic_component_strain(mapdl, plastic_solve, comp):
    index = COMPONENT_STRESS_TYPE.index(comp)
    mapdl.prnsol("EPPL", "COMP", mute=True)  # run twice to clear out warning

    data = np.genfromtxt(mapdl.prnsol("EPPL", "COMP").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    data_ans = data[:, index + 1]
    data = mapdl.post_processing.nodal_plastic_component_strain(comp)
    data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(data_ans, data)


@requires("pyvista")
def test_plot_nodal_plastic_component_strain(mapdl, plastic_solve):
    assert mapdl.post_processing.plot_nodal_plastic_component_strain("x") is None


@pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
def test_nodal_plastic_principal_strain(mapdl, plastic_solve, comp):
    from_grpc = mapdl.post_processing.nodal_plastic_principal_strain(comp)

    index = PRINCIPAL_TYPE.index(comp)
    mapdl.prnsol("EPPL", "PRIN")  # flush to ignore warning
    arr = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
    nnum_ans = arr[:, 0]
    from_prns = arr[:, index + 1]

    # grpc includes all nodes.  ignore the ones not included in prnsol
    from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

    assert np.allclose(from_grpc, from_prns)


@requires("pyvista")
def test_plot_nodal_plastic_principal_strain(mapdl, plastic_solve):
    assert mapdl.post_processing.plot_nodal_plastic_principal_strain(1) is None


def test_nodal_plastic_strain_intensity(mapdl, plastic_solve):
    mapdl.prnsol("EPPL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    sint_ans = data[:, -2]
    sint = mapdl.post_processing.nodal_plastic_strain_intensity()

    sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(sint_ans, sint_aligned)


@requires("pyvista")
def test_plot_nodal_plastic_strain_intensity(mapdl, plastic_solve):
    assert mapdl.post_processing.plot_nodal_plastic_strain_intensity() is None


def test_nodal_plastic_eqv_strain(mapdl, plastic_solve):
    mapdl.prnsol("EPPL", "PRIN", mute=True)  # run twice to clear out warning
    data = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
    nnum_ans = data[:, 0].astype(np.int32)
    seqv_ans = data[:, -1]
    seqv = mapdl.post_processing.nodal_plastic_eqv_strain()

    seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
    assert np.allclose(seqv_ans, seqv_aligned)


@requires("pyvista")
def test_plot_nodal_plastic_eqv_strain(mapdl, plastic_solve):
    assert (
        mapdl.post_processing.plot_nodal_plastic_eqv_strain(smooth_shading=True) is None
    )


def test_nodal_contact_friction_stress(mapdl, contact_solve):
    # Format tables.
    mapdl.post1()
    mapdl.header("OFF", "OFF", "OFF", "OFF", "OFF", "OFF")
    nsigfig = 10
    mapdl.format("", "E", nsigfig + 9, nsigfig)
    mapdl.page(1e9, "", -1, 240)

    prnsol = mapdl.prnsol("CONT")
    array = np.genfromtxt(prnsol.splitlines(), skip_header=1)
    sfric_prn = array[:, 4]
    nodes = array[:, 0]

    index = nodes.astype(int) - 1  # -1 to convert apdl node number to python index.
    sfric_nod = mapdl.post_processing.nodal_contact_friction_stress()[index]

    assert np.allclose(sfric_prn, sfric_nod)


@requires("pyvista")
def test_plot_nodal_contact_friction_stress(mapdl, contact_solve):
    assert (
        mapdl.post_processing.plot_nodal_contact_friction_stress(smooth_shading=True)
        is None
    )


@requires("pyvista")
def test_plot_incomplete_element_selection(mapdl, contact_solve):
    mapdl.esel("S", "ELEM", "", 1, mapdl.mesh.n_elem // 2)
    assert mapdl.post_processing.plot_element_displacement() is None

    mapdl.nsel("S", "NODE", "", 1, mapdl.mesh.n_elem // 2, 2)
    assert mapdl.post_processing.plot_element_displacement() is None

    mapdl.nsel("S", "NODE", "", 5, mapdl.mesh.n_elem // 2, 2)
    assert mapdl.post_processing.plot_element_displacement() is None

    mapdl.vsel("s", "", "", 1)
    mapdl.eslv("s")
    assert mapdl.post_processing.plot_element_displacement() is None

    mapdl.vsel("s", "", "", 2)
    mapdl.eslv("s")
    assert mapdl.post_processing.plot_element_displacement() is None


@requires("pyvista")
def test_plot_incomplete_nodal_selection(mapdl, contact_solve, verify_image_cache):
    verify_image_cache.skip = True

    mapdl.nsel("S", "NODE", "", 1, mapdl.mesh.n_node // 2)
    assert mapdl.post_processing.plot_nodal_displacement() is None

    mapdl.nsel("S", "NODE", "", 1, mapdl.mesh.n_node // 2, 2)
    assert mapdl.post_processing.plot_nodal_displacement() is None

    mapdl.nsel("S", "NODE", "", 5, mapdl.mesh.n_node // 2, 2)
    assert mapdl.post_processing.plot_nodal_displacement() is None

    mapdl.vsel("s", "", "", 1)
    mapdl.eslv("S")
    mapdl.nsle("S")
    assert mapdl.post_processing.plot_nodal_displacement() is None

    mapdl.vsel("s", "", "", 2)
    mapdl.eslv("S")
    mapdl.nsle("S")
    assert mapdl.post_processing.plot_nodal_displacement() is None


@requires("pyvista")
def test_general_plotter_returns(mapdl, static_solve, verify_image_cache):
    verify_image_cache.skip = True  # skipping image verification

    # Returns

    assert (
        mapdl.post_processing.plot_nodal_displacement("X", smooth_shading=True) is None
    )
    assert isinstance(
        mapdl.post_processing.plot_nodal_displacement(
            "X", smooth_shading=True, return_cpos=True
        ),
        CameraPosition,
    )

    p = mapdl.post_processing.plot_nodal_displacement(
        "X", smooth_shading=True, return_plotter=True
    )
    assert isinstance(p, Plotter)
    p.show()

    with pytest.raises(ValueError):
        mapdl.post_processing.plot_nodal_displacement(
            "X", smooth_shading=True, return_cpos=True, return_plotter=True
        )

    # Returns + Save figure.
    assert (
        mapdl.post_processing.plot_nodal_displacement(
            "X",
            smooth_shading=True,
            savefig=True,
            return_cpos=False,
            return_plotter=False,
        )
        is None
    )
    assert isinstance(
        mapdl.post_processing.plot_nodal_displacement(
            "X",
            smooth_shading=True,
            savefig=True,
            return_cpos=True,
            return_plotter=False,
        ),
        CameraPosition,
    )

    p = mapdl.post_processing.plot_nodal_displacement(
        "X",
        smooth_shading=True,
        savefig=True,
        return_cpos=False,
        return_plotter=True,
    )
    assert isinstance(p, MapdlPlotter)


def test_time_frequency_values(mapdl, contact_solve):
    assert np.allclose(
        mapdl.post_processing.time_values,
        mapdl.post_processing.frequency_values,
    )


def test_time_values(mapdl, contact_solve):
    assert np.allclose(
        mapdl.post_processing.time_values, np.array([0.2, 0.4, 0.7, 1.0])
    )


@pytest.mark.parametrize("step_", [1, 2, 3, 4])
def test_set(mapdl, contact_solve, step_):
    mapdl.set(nset=step_)
    assert mapdl.post_processing.step == step_


def test_meta_post_plot_docstrings():
    for each in dir(PostProcessing):
        if each.startswith("plot_"):
            meth = getattr(PostProcessing, each)
            docstring = meth.__doc__

            for section in ["Parameters", "Returns", "Notes", "Examples"]:
                assert re.search(
                    f"{section}\n *-*", docstring
                ), f"Section '{section}' not in '{meth.__name__}'"

            signature = inspect.signature(meth)
            for each_ in signature.parameters:
                if each_ != "self":
                    assert (
                        each_ in docstring
                    ), f"The argument '{each_}' in '{meth.__name__}' is not in its docstring."

            assert (
                "If ``vkt=True`` (default), this function uses" in docstring
            ), f"'vtk=True' part not found in {meth.__name__}"
            assert (
                len(
                    re.findall(
                        ":func:`general_plotter <ansys.mapdl.core.plotting.general_plotter>`",
                        docstring,
                    )
                )
                >= 2
            ), f"Less than two complete one-liner general plotter link in {meth.__name__}"
            assert (
                len(
                    re.findall(
                        "<ansys.mapdl.core.plotting.general_plotter>`",
                        docstring,
                    )
                )
                >= 3
            ), f"Less than three complete one-liner general plotter link in {meth.__name__}"


@requires("pyvista")
def test_cuadratic_beam(mapdl, cuadratic_beam_problem):
    # Display elements with their nodes numbers.
    mapdl.eplot(show_node_numbering=True, line_width=5, cpos="xy", font_size=40)

    mapdl.post1()
    mapdl.set(1)
    assert (
        mapdl.post_processing.plot_nodal_displacement(
            "NORM", line_width=10, render_lines_as_tubes=True, smooth_shading=True
        )
        is None
    )


def test_exited(mapdl):
    mapdl._exited = True
    with pytest.raises(MapdlRuntimeError):
        mapdl.post_processing.plot_nodal_displacement(
            "NORM", line_width=10, render_lines_as_tubes=True, smooth_shading=True
        )
    mapdl._exited = False


###############################################################################
# @pytest.mark.parametrize('comp', COMPONENT_STRESS_TYPE)
# def test_nodal_thermal_component_strain(mapdl, thermal_solve, comp):

#     index = COMPONENT_STRESS_TYPE.index(comp)
#     mapdl.prnsol('EPPL', 'COMP', mute=True)  # run twice to clear out warning

#     data = np.genfromtxt(mapdl.prnsol('EPPL', 'COMP').splitlines()[1:])
#     nnum_ans = data[:, 0].astype(np.int32)
#     data_ans = data[:, index + 1]
#     data = mapdl.post_processing.nodal_thermal_component_strain(comp)
#     data = data[np.in1d(mapdl.mesh.nnum, nnum_ans)]

#     assert np.allclose(data_ans, data)


# @requires("pyvista")
# def test_plot_nodal_thermal_component_strain(mapdl, thermal_solve):
#     assert mapdl.post_processing.plot_nodal_thermal_component_strain('x') is None


# @pytest.mark.parametrize('comp', PRINCIPAL_TYPE)
# def test_nodal_thermal_principal_strain(mapdl, thermal_solve, comp):
#     from_grpc = mapdl.post_processing.nodal_thermal_principal_strain(comp)

#     index = PRINCIPAL_TYPE.index(comp)
#     mapdl.prnsol('EPPL', 'PRIN')  # flush to ignore warning
#     arr = np.genfromtxt(mapdl.prnsol('EPPL', 'PRIN').splitlines()[1:])
#     nnum_ans = arr[:, 0]
#     from_prns = arr[:, index + 1]

#     # grpc includes all nodes.  ignore the ones not included in prnsol
#     from_grpc = from_grpc[np.in1d(mapdl.mesh.nnum, nnum_ans)]

#     assert np.allclose(from_grpc, from_prns)


# @requires("pyvista")
# def test_plot_nodal_thermal_principal_strain(mapdl, thermal_solve):
#     assert mapdl.post_processing.plot_nodal_thermal_principal_strain(1) is None


# def test_nodal_thermal_strain_intensity(mapdl, thermal_solve):
#     mapdl.prnsol('EPPL', 'PRIN', mute=True)  # run twice to clear out warning
#     data = np.genfromtxt(mapdl.prnsol('EPPL', 'PRIN').splitlines()[1:])
#     nnum_ans = data[:, 0].astype(np.int32)
#     sint_ans = data[:, -2]
#     sint = mapdl.post_processing.nodal_thermal_strain_intensity()

#     sint_aligned = sint[np.in1d(mapdl.mesh.nnum, nnum_ans)]
#     assert np.allclose(sint_ans, sint_aligned)


# @requires("pyvista")
# def test_plot_nodal_thermal_strain_intensity(mapdl, thermal_solve):
#     assert mapdl.post_processing.plot_nodal_thermal_strain_intensity() is None


# def test_nodal_thermal_eqv_strain(mapdl, thermal_solve):
#     mapdl.prnsol('EPPL', 'PRIN', mute=True)  # run twice to clear out warning
#     data = np.genfromtxt(mapdl.prnsol('EPPL', 'PRIN').splitlines()[1:])
#     nnum_ans = data[:, 0].astype(np.int32)
#     seqv_ans = data[:, -1]
#     seqv = mapdl.post_processing.nodal_thermal_eqv_strain()

#     seqv_aligned = seqv[np.in1d(mapdl.mesh.nnum, nnum_ans)]
#     assert np.allclose(seqv_ans, seqv_aligned)


# @requires("pyvista")
# def test_plot_nodal_thermal_eqv_strain(mapdl, thermal_solve):
#     assert mapdl.post_processing.plot_nodal_thermal_eqv_strain(smooth_shading=True) is None

###############################################################################
