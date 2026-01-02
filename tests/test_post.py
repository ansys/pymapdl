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

"""Test post-processing module for ansys.mapdl.core"""
import inspect
import re

import numpy as np
import pytest

from conftest import NullContext, TestClass, has_dependency, requires

if has_dependency("ansys-tools-visualization_interface"):
    from pyvista.plotting.renderer import CameraPosition
    from ansys.mapdl.core.plotting.theme import PyMAPDL_cmap
    from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

from ansys.mapdl.core import examples
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.post import (
    COMPONENT_STRESS_TYPE,
    PRINCIPAL_TYPE,
    STRESS_TYPES,
    PostProcessing,
)


def test_repr(mapdl, cleared):
    mapdl.prep7()
    print(mapdl.post_processing)
    repr_ = mapdl.post_processing.__repr__()

    assert "Number of result sets" in repr_
    assert "Current load step" in repr_
    assert "Number of result sets" in repr_
    assert "Enable routine POST1 to see a table of available results" in repr_

    mapdl.post1()
    assert (
        "Enable routine POST1 to see a table of available results"
        not in mapdl.post_processing.__repr__()
    )


class Test_static_solve(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def static_solve(mapdl):
        with mapdl.muted:
            # cylinder and mesh parameters
            # torque = 100
            radius = 2
            h_tip = 2
            height = 20
            elemsize = 0.5
            # pi = np.arccos(-1)
            force = 100 / radius
            pressure = force / (h_tip * 2 * np.pi * radius)

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

        mapdl.save("static_solve", slab="all")

    @pytest.fixture(scope="function")
    def resume(self, mapdl, static_solve):
        self.mapdl = mapdl

        mapdl.prep7()
        mapdl.resume("static_solve")

        # necessary for any prnsol printouts
        mapdl.header("off", "off", "off", "off", "off", "off")
        nsigfig = 10
        mapdl.format("", "E", nsigfig + 9, nsigfig)

        mapdl.post1()
        mapdl.allsel()
        mapdl.set("last")

    @staticmethod
    @pytest.mark.parametrize("comp", ["X", "Y", "z"])  # lowercase intentional
    def test_disp(mapdl, resume, comp):
        disp_from_grpc = mapdl.post_processing.nodal_displacement(comp)

        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        nnum, disp_from_prns = np.genfromtxt(mapdl.prnsol("U", comp).splitlines()[1:]).T

        assert np.allclose(mapdl.mesh.nnum, nnum)
        assert np.allclose(disp_from_grpc, disp_from_prns)

    @staticmethod
    def test_enum_all(mapdl, resume):
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

    @staticmethod
    def test_disp_norm_all(mapdl, resume):
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

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    @pytest.mark.parametrize(
        "comp", ["X", "Y", "z", "norm", "all"]
    )  # lowercase intentional
    def test_disp_plot(mapdl, resume, comp):
        if comp == "all":
            context = pytest.raises(
                ValueError, match='"ALL" not allowed in this context'
            )
        else:
            context = NullContext()

        with context:
            assert (
                mapdl.post_processing.plot_nodal_displacement(
                    comp, smooth_shading=True, cmap=PyMAPDL_cmap
                )
                is None
            )

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_disp_plot_subselection(mapdl, resume):
        mapdl.nsel("S", "NODE", vmin=500, vmax=503, mute=True)
        mapdl.esel("S", "ELEM", vmin=500, vmax=510, mute=True)

        pl = mapdl.post_processing.plot_nodal_displacement(
            "X",
            smooth_shading=True,
            show_node_numbering=True,
            return_plotter=True,
        )

        assert pl.show() is None

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_uncomplete_element_plotting(mapdl, resume):
        enums = mapdl.esel("S", "ELEM", vmin=500, vmax=510)
        mapdl.nsel("s", "node", vmin=50, vmax=60)

        pl = mapdl.post_processing.plot_element_displacement(
            "X",
            smooth_shading=True,
            show_node_numbering=True,
            return_plotter=True,
        )

        mesh = pl.meshes[0]
        elem_ids = np.unique(mesh.cell_data["ansys_elem_num"])

        # assert no state change
        assert mapdl.mesh.n_elem == len(enums)

        assert np.allclose(elem_ids, enums)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_uncomplete_nodal_plotting(mapdl, resume):
        nnums = mapdl.nsel("S", "node", vmin=500, vmax=510)

        pl = mapdl.post_processing.plot_nodal_displacement(
            "X",
            smooth_shading=True,
            show_node_numbering=True,
            return_plotter=True,
        )

        # assert no state change
        assert mapdl.mesh.n_node == len(nnums)
        assert np.allclose(mapdl.mesh.nnum, nnums)

    @staticmethod
    def test_nodal_eqv_stress(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        mapdl.prnsol("S", "PRIN")  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        seqv_ans = data[:, -1]
        seqv = mapdl.post_processing.nodal_eqv_stress()

        seqv_aligned = seqv[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(seqv_ans, seqv_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_eqv_stress(mapdl, resume, verify_image_cache):
        verify_image_cache.skip = True  # skipping image verification

        assert mapdl.post_processing.plot_nodal_eqv_stress(smooth_shading=True) is None

    @staticmethod
    def test_node_selection(mapdl, resume):
        mapdl.nsel("S", "NODE", vmin=1, vmax=2000, mute=True)
        assert mapdl.post_processing.selected_nodes.sum() == 2000

        mapdl.nsel("all", mute=True)
        assert mapdl.post_processing.selected_nodes.sum() == mapdl.mesh.n_node

    @staticmethod
    def test_element_selection(mapdl, resume):
        mx_val = 1000
        mapdl.esel("S", "ELEM", vmin=1, vmax=mx_val, mute=True)
        assert mapdl.post_processing.selected_elements.sum() == mx_val

        mapdl.esel("all", mute=True)
        assert mapdl.post_processing.selected_elements.sum() == mapdl.mesh.n_elem

    # TODO: add valid result
    @staticmethod
    @pytest.mark.parametrize("comp", ["X", "Y", "z", "all"])  # lowercase intentional
    def test_rot(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_rotation(comp)

        # need a result with ROTX DOF
        # mapdl.post1(mute=True)
        # mapdl.set(1, 1, mute=True)
        # nnum, from_prns = np.genfromtxt(mapdl.prnsol('ROT', comp).splitlines()[1:]).T

        # assert np.allclose(mapdl.mesh.nnum, nnum)
        # assert np.allclose(from_grpc, from_prns)
        assert np.allclose(from_grpc, 0)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    @pytest.mark.parametrize("comp", ["X", "Y", "z", "all"])  # lowercase intentional
    def test_plot_rot(mapdl, resume, comp):
        if comp == "all":
            context = pytest.raises(
                ValueError, match='"ALL" not allowed in this context'
            )
        else:
            context = NullContext()

        with context:
            assert mapdl.post_processing.plot_nodal_rotation(comp) is None

    # TODO: add valid result
    @staticmethod
    def test_temperature(mapdl, resume):
        from_grpc = mapdl.post_processing.nodal_temperature()
        assert np.allclose(from_grpc, 0)

    # TODO: add valid result
    @staticmethod
    def test_element_temperature(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        values = mapdl.post_processing.element_temperature()
        assert np.allclose(values, 0)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_element_temperature(mapdl, resume):
        mapdl.set(1, 1, mute=True)
        assert mapdl.post_processing.plot_element_temperature() is None

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_temperature(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_temperature() is None

    # TODO: add valid result
    @staticmethod
    def test_pressure(mapdl, resume):
        from_grpc = mapdl.post_processing.nodal_pressure()
        assert np.allclose(from_grpc, 0)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_pressure(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_pressure() is None

    # TODO: add valid result
    @staticmethod
    def test_voltage(mapdl, resume):
        from_grpc = mapdl.post_processing.nodal_voltage()
        assert np.allclose(from_grpc, 0)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_voltage(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_voltage() is None

    @staticmethod
    @pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
    def test_nodal_component_stress(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_component_stress(comp)
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        index = COMPONENT_STRESS_TYPE.index(comp)
        mapdl.prnsol("S", "COMP")  # flush to ignore warning
        arr = np.genfromtxt(mapdl.prnsol("S", "COMP").splitlines()[1:])
        nnum_ans = arr[:, 0]
        from_prns = arr[:, index + 1]

        # grpc includes all nodes.  ignore the ones not included in prnsol
        from_grpc = from_grpc[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(from_grpc, from_prns)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_component_stress(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_component_stress("X") is None

    @staticmethod
    @pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
    def test_nodal_principal_stress(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_principal_stress(comp)
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        index = PRINCIPAL_TYPE.index(comp)
        mapdl.prnsol("S", "PRIN")  # flush to ignore warning
        arr = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
        nnum_ans = arr[:, 0]
        from_prns = arr[:, index + 1]

        # grpc includes all nodes.  ignore the ones not included in prnsol
        from_grpc = from_grpc[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(from_grpc, from_prns, 1e-5)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_principal_stress(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_principal_stress(1) is None

    @staticmethod
    def test_nodal_stress_intensity(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        mapdl.prnsol("S", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("S", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        sint_ans = data[:, -2]
        sint = mapdl.post_processing.nodal_stress_intensity()

        sint_aligned = sint[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(sint_ans, sint_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_stress_intensity(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_stress_intensity() is None

    @staticmethod
    @pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
    def test_nodal_total_component_strain(mapdl, resume, comp):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        index = COMPONENT_STRESS_TYPE.index(comp)
        mapdl.prnsol("EPTO", "COMP", mute=True)  # run twice to clear out warning

        data = np.genfromtxt(mapdl.prnsol("EPTO", "COMP").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        data_ans = data[:, index + 1]
        data = mapdl.post_processing.nodal_total_component_strain(comp)
        data = data[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(data_ans, data)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_total_component_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_total_component_strain("x") is None

    @staticmethod
    @pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
    def test_nodal_principal_total_strain(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_total_principal_strain(comp)
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        index = PRINCIPAL_TYPE.index(comp)
        mapdl.prnsol("EPTO", "PRIN")  # flush to ignore warning
        arr = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
        nnum_ans = arr[:, 0]
        from_prns = arr[:, index + 1]

        # grpc includes all nodes.  ignore the ones not included in prnsol
        from_grpc = from_grpc[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(from_grpc, from_prns)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_principal_total_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_total_principal_strain(1) is None

    @staticmethod
    def test_nodal_total_strain_intensity(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        mapdl.prnsol("EPTO", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        sint_ans = data[:, -2]
        sint = mapdl.post_processing.nodal_total_strain_intensity()

        sint_aligned = sint[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(sint_ans, sint_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_total_strain_intensity(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_total_strain_intensity() is None

    @staticmethod
    def test_nodal_total_eqv_strain(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        mapdl.prnsol("EPTO", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPTO", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        seqv_ans = data[:, -1]
        seqv = mapdl.post_processing.nodal_total_eqv_strain()

        seqv_aligned = seqv[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(seqv_ans, seqv_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_total_eqv_strain(mapdl, resume):
        assert (
            mapdl.post_processing.plot_nodal_total_eqv_strain(smooth_shading=True)
            is None
        )

    ###############################################################################
    @staticmethod
    @pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
    def test_nodal_elastic_component_strain(mapdl, resume, comp):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        index = COMPONENT_STRESS_TYPE.index(comp)
        mapdl.prnsol("EPEL", "COMP", mute=True)  # run twice to clear out warning

        data = np.genfromtxt(mapdl.prnsol("EPEL", "COMP").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        data_ans = data[:, index + 1]
        data = mapdl.post_processing.nodal_elastic_component_strain(comp)
        data = data[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(data_ans, data)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_elastic_component_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_elastic_component_strain("x") is None

    @staticmethod
    @pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
    def test_nodal_elastic_principal_strain(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_elastic_principal_strain(comp)
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        index = PRINCIPAL_TYPE.index(comp)
        mapdl.prnsol("EPEL", "PRIN")  # flush to ignore warning
        arr = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
        nnum_ans = arr[:, 0]
        from_prns = arr[:, index + 1]

        # grpc includes all nodes.  ignore the ones not included in prnsol
        from_grpc = from_grpc[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(from_grpc, from_prns)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_elastic_principal_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_elastic_principal_strain(1) is None

    @staticmethod
    def test_nodal_elastic_strain_intensity(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        mapdl.prnsol("EPEL", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        sint_ans = data[:, -2]
        sint = mapdl.post_processing.nodal_elastic_strain_intensity()

        sint_aligned = sint[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(sint_ans, sint_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_elastic_strain_intensity(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_elastic_strain_intensity() is None

    @staticmethod
    def test_nodal_elastic_eqv_strain(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        mapdl.prnsol("EPEL", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPEL", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        seqv_ans = data[:, -1]
        seqv = mapdl.post_processing.nodal_elastic_eqv_strain()

        seqv_aligned = seqv[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(seqv_ans, seqv_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_elastic_eqv_strain(mapdl, resume):
        assert (
            mapdl.post_processing.plot_nodal_elastic_eqv_strain(smooth_shading=True)
            is None
        )

    @staticmethod
    @pytest.mark.parametrize("comp", ["X", "Y", "z", "all"])  # lowercase intentional
    def test_elem_disp(mapdl, resume, comp):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        mapdl.allsel()

        disp_from_grpc = mapdl.post_processing.element_displacement(comp)

        # use pretab to get the data
        table_name = "values"
        if comp != "all":
            mapdl.etable(table_name, "U", comp, mute=True)
            arr = np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
        else:
            arr = []
            for direction in ["x", "y", "z"]:
                mapdl.etable(table_name, "U", direction, mute=True)
                arr.append(
                    np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
                )
            arr = np.array(arr).T

        assert np.allclose(arr, disp_from_grpc)

    @staticmethod
    @pytest.mark.parametrize("option", ["min", "max", "avg"])
    def test_elem_disp_all(mapdl, resume, option):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        disp_from_grpc = mapdl.post_processing.element_displacement("ALL", option)

        # use pretab to get the data
        arrays = []
        for comp in ["x", "y", "z"]:
            table_name = "values" + comp
            mapdl.etable(table_name, "U", comp, option=option, mute=True)
            arrays.append(
                np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
            )
        array = np.vstack(arrays).T
        assert np.allclose(array, disp_from_grpc)

    @staticmethod
    def test_elem_disp_norm(mapdl, resume):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        disp = mapdl.post_processing.element_displacement("ALL")
        norm_disp = np.linalg.norm(disp, axis=1)
        disp_from_grpc = mapdl.post_processing.element_displacement("NORM")
        assert np.allclose(norm_disp, disp_from_grpc)

    @staticmethod
    @pytest.mark.parametrize("comp", ["X", "Y", "Z", "NORM", "all"])
    @requires("ansys-tools-visualization_interface")
    def test_elem_disp_plot(mapdl, resume, comp):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)

        if comp == "all":
            context = pytest.raises(
                ValueError, match='"ALL" not allowed in this context'
            )
        else:
            context = NullContext()

        with context:
            assert mapdl.post_processing.plot_element_displacement(comp) is None

    STRESS_TYPES.extend([1, 2, 3])

    @staticmethod
    @pytest.mark.parametrize("component", STRESS_TYPES)
    @pytest.mark.parametrize("option", ["min", "max", "avg"])
    def test_element_stress(mapdl, resume, component, option):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        stress = mapdl.post_processing.element_stress(component, option)

        # use pretab to get the data
        table_name = "values" + str(component)
        mapdl.etable(table_name, "S", component, option=option, mute=True)
        from_pretab = np.genfromtxt(mapdl.pretab(table_name).splitlines()[1:])[:, 1]
        assert np.allclose(stress, from_pretab)

    @staticmethod
    @pytest.mark.parametrize("comp", ["X", "1", "INT", "EQV"])
    @requires("ansys-tools-visualization_interface")
    def test_plot_element_stress(mapdl, resume, comp):
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        assert mapdl.post_processing.plot_element_stress(comp) is None

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_element_values(mapdl, resume, verify_image_cache):
        verify_image_cache.high_variance_test = 600
        mapdl.post1(mute=True)
        mapdl.set(1, 1, mute=True)
        assert mapdl.post_processing.plot_element_values("S", "X") is None

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_general_plotter_returns(mapdl, resume, verify_image_cache):
        verify_image_cache.skip = True  # skipping image verification

        # Returns

        assert (
            mapdl.post_processing.plot_nodal_displacement("X", smooth_shading=True)
            is None
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
        assert isinstance(p, MapdlPlotter)
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


###############################################################################


class Test_plastic_solve(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def plastic_solve(mapdl):
        with mapdl.muted:
            mapdl.input(examples.verif_files.vmfiles["vm273"])

        mapdl.save("plastic_solve", slab="all")

    @staticmethod
    @pytest.fixture(scope="function")
    def resume(mapdl, plastic_solve):
        mapdl.prep7()
        mapdl.resume("plastic_solve")

        mapdl.allsel()
        mapdl.post1()
        mapdl.set(1, 2)

        # necessary for any prnsol printouts
        mapdl.header("off", "off", "off", "off", "off", "off")
        nsigfig = 10
        mapdl.format("", "E", nsigfig + 9, nsigfig)

    @staticmethod
    def test_list_in_repr(mapdl, resume):
        mapdl.finish()
        assert "Enable routine POST1 to see a table of available results" in str(
            mapdl.post_processing
        )

        mapdl.post1()
        assert mapdl.set("LIST") in mapdl.post_processing.__str__()

    @staticmethod
    @pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
    def test_nodal_plastic_component_strain(mapdl, resume, comp):
        index = COMPONENT_STRESS_TYPE.index(comp)
        mapdl.prnsol("EPPL", "COMP", mute=True)  # run twice to clear out warning

        data = np.genfromtxt(mapdl.prnsol("EPPL", "COMP").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        data_ans = data[:, index + 1]
        data = mapdl.post_processing.nodal_plastic_component_strain(comp)
        data = data[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(data_ans, data)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_plastic_component_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_plastic_component_strain("x") is None

    @staticmethod
    @pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
    def test_nodal_plastic_principal_strain(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_plastic_principal_strain(comp)

        index = PRINCIPAL_TYPE.index(comp)
        mapdl.prnsol("EPPL", "PRIN")  # flush to ignore warning
        arr = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
        nnum_ans = arr[:, 0]
        from_prns = arr[:, index + 1]

        # grpc includes all nodes.  ignore the ones not included in prnsol
        from_grpc = from_grpc[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(from_grpc, from_prns)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_plastic_principal_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_plastic_principal_strain(1) is None

    @staticmethod
    def test_nodal_plastic_strain_intensity(mapdl, resume):
        mapdl.prnsol("EPPL", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        sint_ans = data[:, -2]
        sint = mapdl.post_processing.nodal_plastic_strain_intensity()

        sint_aligned = sint[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(sint_ans, sint_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_plastic_strain_intensity(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_plastic_strain_intensity() is None

    @staticmethod
    def test_nodal_plastic_eqv_strain(mapdl, resume):
        mapdl.prnsol("EPPL", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPPL", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        seqv_ans = data[:, -1]
        seqv = mapdl.post_processing.nodal_plastic_eqv_strain()

        seqv_aligned = seqv[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(seqv_ans, seqv_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_plastic_eqv_strain(mapdl, resume):
        assert (
            mapdl.post_processing.plot_nodal_plastic_eqv_strain(smooth_shading=True)
            is None
        )


class Test_contact_solve(TestClass):

    @staticmethod
    @pytest.fixture(scope="class")
    def contact_solve(mapdl):
        # Based on tech demo 28.
        # ***** Problem parameters ********
        l = 76.2e-03 / 3  # Length of each plate,m
        w = 31.75e-03 / 2  # Width of each plate,m
        t = 3.18e-03  # Thickness of each plate,m
        r1 = 7.62e-03  # Shoulder radius of tool,m
        h = 15.24e-03  # Height of tool, m
        l1 = r1  # Starting location of tool on weldline
        l2 = l - l1
        tcc1 = 2e06  # Thermal contact conductance b/w plates,W/m^2'C
        tcc2 = 10  # Thermal contact conductance b/w tool &
        # workpiece,W/m^2'C
        fwgt = 0.95  # weight factor for distribution of heat b/w tool
        # & workpiece
        fplw = 0.8  # Fraction of plastic work converted to heat

        # this is also modified in the dependent fixture
        uz1 = t / 4000  # Depth of penetration,m

        # ==========================================================
        # * Material properties
        # ==========================================================
        # * Material properties for 304l stainless steel Plates
        mapdl.mp("ex", 1, 193e9)  # Elastic modulus (N/m^2)
        mapdl.mp("nuxy", 1, 0.3)  # Poisson's ratio
        mapdl.mp("alpx", 1, 1.875e-5)  # Coefficient of thermal expansion, µm/m'c
        # Fraction of plastic work converted to heat, 80%
        mapdl.mp("qrate", 1, fplw)

        # *BISO material model
        EX = 193e9
        ET = 2.8e9
        EP = EX * ET / (EX - ET)
        mapdl.tb("plas", 1, 1, "", "biso")  # Bilinear isotropic material
        mapdl.tbdata(1, 290e6, EP)  # Yield stress & plastic tangent modulus
        mapdl.mptemp(1, 0, 200, 400, 600, 800, 1000)
        mapdl.mpdata("kxx", 1, 1, 16, 19, 21, 24, 29, 30)  # therm cond.(W/m'C)
        mapdl.mpdata("c", 1, 1, 500, 540, 560, 590, 600, 610)  # spec heat(J/kg'C)
        mapdl.mpdata("dens", 1, 1, 7894, 7744, 7631, 7518, 7406, 7406)  # kg/m^3

        # * Material properties for PCBN tool
        mapdl.mp("ex", 2, 680e9)  # Elastic modulus (N/m^2)
        mapdl.mp("nuxy", 2, 0.22)  # Poisson's ratio
        mapdl.mp("kxx", 2, 100)  # Thermal conductivity(W/m'C)
        mapdl.mp("c", 2, 750)  # Specific heat(J/kg'C)
        mapdl.mp("dens", 2, 4280)  # Density,kg/m^3

        # ==========================================================
        # * Geometry
        # ==========================================================
        # * Node for pilot node
        mapdl.n(1, 0, 0, h)
        # * Workpiece geometry (two rectangular plates)
        mapdl.block(0, w, -l1, l2, 0, -t)
        mapdl.block(0, -w, -l1, l2, 0, -t)
        # * Tool geometry
        mapdl.cyl4(0, 0, r1, 0, r1, 90, h)
        mapdl.cyl4(0, 0, r1, 90, r1, 180, h)
        mapdl.cyl4(0, 0, r1, 180, r1, 270, h)
        mapdl.cyl4(0, 0, r1, 270, r1, 360, h)
        mapdl.vglue(3, 4, 5, 6)

        # ==========================================================
        # * Meshing
        # ==========================================================
        mapdl.et(1, "SOLID226", 11)  # Coupled-field solid element,KEYOPT(1) is
        # set to 11 for a structural-thermal analysis
        mapdl.allsel()
        ndiv1 = 2
        ndiv2 = 5
        ndiv3 = 1

        mapdl.lsel("s", "", "", 4, 5)
        mapdl.lsel("a", "", "", 14, 19, 5)
        mapdl.lesize("all", "", "", ndiv1)
        mapdl.lsel("s", "", "", 16, 17)
        mapdl.lsel("a", "", "", 2, 7, 5)
        mapdl.lesize("all", "", "", ndiv1)
        mapdl.lsel("s", "", "", 1)
        mapdl.lsel("a", "", "", 3)
        mapdl.lsel("a", "", "", 6)
        mapdl.lsel("a", "", "", 8)
        mapdl.lsel("a", "", "", 13)
        mapdl.lsel("a", "", "", 15)
        mapdl.lsel("a", "", "", 18)
        mapdl.lsel("a", "", "", 20)
        mapdl.lesize("all", "", "", ndiv2)
        mapdl.lsel("s", "", "", 9, "")
        mapdl.lsel("a", "", "", 22)
        mapdl.lesize("all", "", "", ndiv3)
        mapdl.allsel("all")
        mapdl.mshmid(2)  # midside nodes dropped
        mapdl.vsweep(1)
        mapdl.vsweep(2)
        mapdl.vsel("u", "volume", "", 1, 2)
        mapdl.mat(2)
        mapdl.esize(0.005)
        mapdl.numstr("NODE", 1000)
        mapdl.vsweep("all")
        mapdl.allsel("all")

        # ==========================================================
        # * Contact Pairs
        # ==========================================================
        # * Define Rigid Surface Constraint on tool top surface
        mapdl.et(2, "TARGE170")
        mapdl.keyopt(2, 2, 1)  # User defined boundary condition on rigid
        # target nodes

        mapdl.et(3, "CONTA174")
        mapdl.keyopt(3, 1, 1)  # To include Temp DOF
        mapdl.keyopt(3, 2, 2)  # To include MPC contact algorithm
        mapdl.keyopt(3, 4, 2)  # For a rigid surface constraint
        mapdl.keyopt(3, 12, 5)  # To set the behavior of contact surface as a
        # bonded (always)

        mapdl.vsel("u", "volume", "", 1, 2)  # Selecting Tool volume
        mapdl.allsel("below", "volume")
        mapdl.nsel("r", "loc", "z", h)  # Selecting nodes on the tool top surface
        mapdl.type(3)
        mapdl.r(3)
        mapdl.real(3)
        mapdl.esln()
        mapdl.esurf()  # Create contact elements
        mapdl.allsel("all")

        # * Define pilot node at the top of the tool
        mapdl.nsel("s", "node", "", 1)
        mapdl.tshap("pilo")
        mapdl.type(2)
        mapdl.real(3)
        mapdl.e(1)  # Create target element on pilot node
        mapdl.allsel()

        # * Define contact pair between two plates
        mapdl.et(6, "TARGE170")
        mapdl.et(7, "CONTA174")
        mapdl.keyopt(7, 1, 1)  # Displacement & Temp dof
        mapdl.keyopt(7, 4, 3)  # To include Surface projection based method
        mapdl.mat(1)
        mapdl.asel("s", "", "", 5)
        mapdl.nsla("", 1)
        mapdl.cm("tn.cnt", "node")  # Creating component on weld side of plate1

        mapdl.asel("s", "", "", 12)
        mapdl.nsla("", 1)
        mapdl.cm("tn.tgt", "node")  # Creating component on weld side of plate2

        mapdl.allsel("all")
        mapdl.type(6)
        mapdl.r(6)
        mapdl.rmodif(6, 14, tcc1)  # A real constant TCC,Thermal contact
        # conductance coeffi. b/w the plates, W/m^2'C
        mapdl.rmodif(6, 35, 1000)  # A real constant TBND,Bonding temperature
        # for welding, 'C
        mapdl.real(6)
        mapdl.cmsel("s", "tn.cnt")
        mapdl.esurf()
        mapdl.type(7)
        mapdl.real(6)
        mapdl.cmsel("s", "tn.tgt")
        mapdl.esurf()
        mapdl.allsel("all")

        # * Define contact pair between tool & workpiece
        mapdl.et(4, "TARGE170")
        mapdl.et(5, "CONTA174")
        mapdl.keyopt(5, 1, 1)  # Displacement & Temp dof
        mapdl.keyopt(5, 5, 3)  # Close gap/reduce penetration with auto cnof
        mapdl.keyopt(5, 9, 1)  # Exclude both initial penetration or gap
        mapdl.keyopt(5, 10, 0)  # Contact stiffness update each iteration
        # based

        # Bottom & lateral(all except top) surfaces of tool for target
        mapdl.vsel("u", "volume", "", 1, 2)
        mapdl.allsel("below", "volume")
        mapdl.nsel("r", "loc", "z", 0, h)
        mapdl.nsel("u", "loc", "z", h)
        mapdl.type(4)
        mapdl.r(5)
        mapdl.tb("fric", 5, 6)  # Definition of friction co efficient at
        # different temp
        mapdl.tbtemp(25)
        mapdl.tbdata(1, 0.4)  # friction co-efficient at temp 25
        mapdl.tbtemp(200)
        mapdl.tbdata(1, 0.4)  # friction co-efficient at temp 200
        mapdl.tbtemp(400)
        mapdl.tbdata(1, 0.4)  # friction co-efficient at temp 400
        mapdl.tbtemp(600)
        mapdl.tbdata(1, 0.3)  # friction co-efficient at temp 600
        mapdl.tbtemp(800)
        mapdl.tbdata(1, 0.3)  # friction co-efficient at temp 800
        mapdl.tbtemp(1000)
        mapdl.tbdata(1, 0.2)  # friction co-efficient at temp 1000
        mapdl.rmodif(5, 9, 500e6)  # Max.friction stress
        mapdl.rmodif(5, 14, tcc2)  # Thermal contact conductance b/w tool and
        # workpiece, 10 W/m^2'C
        mapdl.rmodif(5, 15, 1)  # A real constant FHTG,the fraction of
        # frictional dissipated energy converted
        # into heat
        mapdl.rmodif(5, 18, fwgt)  # A real constant  FWGT, weight factor for
        # the distribution of heat between the
        # contact and target surfaces, 0.95
        mapdl.real(5)
        mapdl.mat(5)
        mapdl.esln()
        mapdl.esurf()
        mapdl.allsel("all")

        # Top surfaces of plates nodes for contact
        mapdl.vsel("s", "volume", "", 1, 2)
        mapdl.allsel("below", "volume")
        mapdl.nsel("r", "loc", "z", 0)
        mapdl.type(5)
        mapdl.real(5)
        mapdl.esln()
        mapdl.esurf()
        mapdl.allsel("all")

        # ==========================================================
        # * Boundary conditions
        # ==========================================================
        mapdl.tref(25)  # Reference temperature 25'C
        mapdl.allsel()
        mapdl.nsel("all")
        mapdl.ic("all", "temp", 25)  # Initial condition at nodes,temp 25'C

        # Mechanical Boundary Conditions
        # 20% ends of the each plate is constraint
        mapdl.nsel("s", "loc", "x", -0.8 * w, -w)
        mapdl.nsel("a", "loc", "x", 0.8 * w, w)
        mapdl.d("all", "uz", 0)  # Displacement constraint in x-direction
        mapdl.d("all", "uy", 0)  # Displacement constraint in y-direction
        mapdl.d("all", "ux", 0)  # Displacement constraint in z-direction
        mapdl.allsel("all")

        # Bottom of workpiece is constraint in z-direction
        mapdl.nsel("s", "loc", "z", -t)
        mapdl.d("all", "uz")  # Displacement constraint in z-direction
        mapdl.allsel("all")

        # Thermal Boundary Conditions
        # Convection heat loss from the workpiece surfaces
        mapdl.vsel("s", "volume", "", 1, 2)  # Selecting the workpiece
        mapdl.allsel("below", "volume")
        mapdl.nsel("r", "loc", "z", 0)
        mapdl.nsel("a", "loc", "x", -w)
        mapdl.nsel("a", "loc", "x", w)
        mapdl.nsel("a", "loc", "y", -l1)
        mapdl.nsel("a", "loc", "y", l2)
        mapdl.sf("all", "conv", 30, 25)

        # Convection (high)heat loss from the workpiece bottom
        mapdl.nsel("s", "loc", "z", -t)
        mapdl.sf("all", "conv", 300, 25)
        mapdl.allsel("all")

        # Convection heat loss from the tool surfaces
        mapdl.vsel("u", "volume", "", 1, 2)  # Selecting the tool
        mapdl.allsel("below", "volume")
        mapdl.csys(1)
        mapdl.nsel("r", "loc", "x", r1)
        mapdl.nsel("a", "loc", "z", h)
        mapdl.sf("all", "conv", 30, 25)
        mapdl.allsel("all")

        # Constraining all DOFs at pilot node except the Temp DOF
        mapdl.d(1, "all")
        mapdl.ddele(1, "temp")
        mapdl.allsel("all")
        # ==========================================================
        # * Solution
        # ==========================================================
        # from precedent fixture
        uz1 = 3.18e-03 / 4000

        mapdl.run("/solu")
        mapdl.antype(4)  # Transient analysis
        mapdl.lnsrch("on")
        mapdl.cutcontrol("plslimit", 0.15)
        mapdl.kbc(0)  # Ramped loading within a load step
        mapdl.nlgeom("on")  # Turn on large deformation effects
        mapdl.timint("off", "struc")  # Structural dynamic effects are turned off.
        mapdl.nropt("unsym")

        # Load Step1
        mapdl.time(1)
        mapdl.nsubst(5, 10, 2)
        mapdl.d(1, "uz", -uz1)  # Tool plunges into the workpiece
        mapdl.outres("all", "all")
        mapdl.allsel()
        mapdl.solve()

        mapdl.save("contact_solve", slab="all")

    @staticmethod
    @pytest.fixture(scope="function")
    def resume(mapdl, contact_solve):
        mapdl.prep7()
        mapdl.resume("contact_solve")
        mapdl.post1()
        mapdl.allsel()
        mapdl.set("last")

        # Format tables.
        mapdl.header("OFF", "OFF", "OFF", "OFF", "OFF", "OFF")
        nsigfig = 10
        mapdl.format("", "E", nsigfig + 9, nsigfig)
        mapdl.page(1e9, "", -1, 240)

    @staticmethod
    def test_time(mapdl, resume):
        assert mapdl.post_processing.time == 1

    @staticmethod
    def test_freq(mapdl, resume):
        # same as post_processing.time
        mapdl.set("last")

        assert mapdl.post_processing.freq == 1
        assert mapdl.post_processing.time == mapdl.post_processing.freq

    @staticmethod
    def test_nodal_contact_friction_stress(mapdl, resume):
        # Format tables.
        prnsol = mapdl.prnsol("CONT")
        array = np.genfromtxt(prnsol.splitlines(), skip_header=1)
        sfric_prn = array[:, 4]
        nodes = array[:, 0]

        index = nodes.astype(int) - 1  # -1 to convert apdl node number to python index.
        sfric_nod = mapdl.post_processing.nodal_contact_friction_stress()[index]

        assert np.allclose(sfric_prn, sfric_nod)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_contact_friction_stress(mapdl, resume):
        assert (
            mapdl.post_processing.plot_nodal_contact_friction_stress(
                smooth_shading=True
            )
            is None
        )

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    @pytest.mark.parametrize(
        "vmin,vmax,vinc",
        [
            [0, 1, 1],
            [0.2, 0.3, 1],
            [0, 1, 2],
            [0.2, 0.5, 5],
        ],
    )
    def test_plot_incomplete_element_selection(mapdl, resume, vmin, vmax, vinc):
        n_elem = mapdl.mesh.n_elem
        mapdl.esel(
            "S",
            "ELEM",
            "",
            vmin=int(n_elem * vmin) + 1,
            vmax=int(n_elem * vmax),
            vinc=vinc,
        )
        assert mapdl.post_processing.plot_element_displacement() is None

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    @pytest.mark.parametrize("vol", [1, 2])
    def test_plot_volume_selection(mapdl, resume, vol):
        mapdl.vsel("s", "", "", vol)
        mapdl.eslv("s")
        assert mapdl.post_processing.plot_element_displacement() is None

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    @pytest.mark.parametrize(
        "vmin,vmax,vinc",
        [
            [0, 1, 1],
            [0.2, 0.3, 1],
            [0, 1, 2],
            [0.2, 0.5, 5],
        ],
    )
    def test_plot_incomplete_node_selection(mapdl, resume, vmin, vmax, vinc):
        n_node = mapdl.mesh.n_node
        mapdl.nsel(
            "S",
            "NODE",
            "",
            vmin=int(n_node * vmin) + 1,
            vmax=int(n_node * vmax),
            vinc=vinc,
        )
        assert mapdl.post_processing.plot_nodal_displacement() is None

    @staticmethod
    def test_time_frequency_values(mapdl, resume):
        assert np.allclose(
            mapdl.post_processing.time_values,
            mapdl.post_processing.frequency_values,
        )

    @staticmethod
    def test_time_values(mapdl, resume):
        assert np.allclose(
            mapdl.post_processing.time_values, np.array([0.2, 0.4, 0.7, 1.0])
        )

    @staticmethod
    @pytest.mark.parametrize("step_", [1, 2, 3, 4])
    def test_set(mapdl, resume, step_):
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
                "If ``graphics_backend=GraphicsBackend.PYVISTA`` (default), this function uses"
                in docstring
            ), f"'graphics_backend=GraphicsBackend.PYVISTA' part not found in {meth.__name__}"
            assert (
                len(
                    re.findall(
                        ":class:`MapdlPlotter<ansys.mapdl.core.plotting.visualizer.MapdlPlotter>`",
                        docstring,
                    )
                )
                >= 2
            ), f"Less than two complete one-liner general plotter link in {meth.__name__}"
            assert (
                len(
                    re.findall(
                        "<ansys.mapdl.core.plotting.visualizer.MapdlPlotter>`",
                        docstring,
                    )
                )
                >= 3
            ), f"Less than three complete one-liner general plotter link in {meth.__name__}"


@requires("ansys-tools-visualization_interface")
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


def test_exited(mapdl, cleared):
    mapdl._exited = True
    with pytest.raises(MapdlRuntimeError):
        mapdl.post_processing.plot_nodal_displacement(
            "NORM", line_width=10, render_lines_as_tubes=True, smooth_shading=True
        )
    mapdl._exited = False


###############################################################################


class Test_thermal_solve:

    @staticmethod
    @pytest.fixture(scope="class")
    def thermal_solve(mapdl):
        with mapdl.muted:
            mapdl.finish()
            mapdl.clear()

            mapdl.prep7()
            mapdl.et(1, "PLANE223", 11, 1)  # COUPLE-FIELD ELEMENT TYPE, WEAK COUPLING
            mapdl.et(2, "CONTA175", 1)  # CONTACT ELEMENT TYPE
            mapdl.et(3, "TARGE169")  # TARGET ELEMENT TYPE
            mapdl.mp("EX", 1, 10e6)  # YOUNG'S MODULUS
            mapdl.mp("KXX", 1, 250)  # CONDUCTIVITY
            mapdl.mp("ALPX", 1, 12e-6)  # THERMAL EXPANSION COEFFICIENT
            mapdl.mp("PRXY", "", 0.3)
            mapdl.r(2, "", "", -1000, -0.005)
            mapdl.rmore("", "", "", "", "", -100)
            mapdl.rmore("", 100)
            mapdl.rmore()
            mapdl.rmore(0.01)

            # SET UP FINITE ELEMENT MODEL
            mapdl.n(1)
            mapdl.n(2, 0.4)
            mapdl.n(3, "(0.4+0.0035)")
            mapdl.n(4, "(0.9+0.0035)")
            mapdl.ngen(2, 4, 1, 4, 1, "", 0.1)
            mapdl.e(1, 2, 6, 5)  # PLANE223 ELEMENTS
            mapdl.e(3, 4, 8, 7)
            mapdl.type(2)  # CONTACT ELEMENTS
            mapdl.real(2)
            mapdl.e(2)
            mapdl.e(6)
            mapdl.type(3)  # TARGET ELEMENTS
            mapdl.real(2)
            mapdl.nsel("S", "NODE", "", 3, 7, 4)
            mapdl.esln()
            mapdl.esurf()
            mapdl.allsel()

            # APPLY INITIAL BOUNDARY CONDITIONS
            mapdl.d(1, "UY", "", "", 4, 1)
            mapdl.d(1, "UX", "", "", 5, 4)
            mapdl.d(4, "UX", "", "", 8, 4)
            mapdl.tref(100)
            mapdl.eresx("YES")
            mapdl.finish()

            mapdl.slashsolu()
            mapdl.nlgeom("ON")  # LARGE DEFLECTION EFFECTS TURNED ON
            mapdl.d(1, "TEMP", 500, "", 5, 4)
            mapdl.d(3, "TEMP", 100, "", 4)
            mapdl.d(7, "TEMP", 100, "", 8)
            mapdl.solve()  # FIRST LOAD STEP

            mapdl.solution()
            mapdl.allsel()
            mapdl.outres("all", "all")
            mapdl.solve()

        mapdl.save("thermal_solve")
        mapdl.finish()

    @staticmethod
    @pytest.fixture()
    def resume(mapdl, thermal_solve):
        mapdl.solution()
        mapdl.resume("thermal_solve")

        mapdl.post1()
        mapdl.allsel()
        mapdl.set("last")

        mapdl.header("OFF", "OFF", "OFF", "OFF", "OFF", "OFF")
        nsigfig = 10
        mapdl.format("", "E", nsigfig + 9, nsigfig)
        mapdl.page(1e9, "", -1, 240)

    @staticmethod
    @pytest.mark.parametrize("comp", COMPONENT_STRESS_TYPE)
    def test_nodal_thermal_component_strain(mapdl, resume, comp):

        index = COMPONENT_STRESS_TYPE.index(comp)
        mapdl.prnsol("EPTH", "COMP", mute=True)  # run twice to clear out warning

        data = np.genfromtxt(mapdl.prnsol("EPTH", "COMP").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        data_ans = data[:, index + 1]
        data = mapdl.post_processing.nodal_thermal_component_strain(comp)
        data = data[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(data_ans, data)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_thermal_component_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_thermal_component_strain("x") is None

    @staticmethod
    @pytest.mark.parametrize("comp", PRINCIPAL_TYPE)
    def test_nodal_thermal_principal_strain(mapdl, resume, comp):
        from_grpc = mapdl.post_processing.nodal_thermal_principal_strain(comp)

        index = PRINCIPAL_TYPE.index(comp)
        mapdl.prnsol("EPTH", "PRIN")  # flush to ignore warning
        arr = np.genfromtxt(mapdl.prnsol("EPTH", "PRIN").splitlines()[1:])
        nnum_ans = arr[:, 0]
        from_prns = arr[:, index + 1]

        # grpc includes all nodes.  ignore the ones not included in prnsol
        from_grpc = from_grpc[np.isin(mapdl.mesh.nnum, nnum_ans)]

        assert np.allclose(from_grpc, from_prns)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_thermal_principal_strain(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_thermal_principal_strain(1) is None

    @staticmethod
    def test_nodal_thermal_strain_intensity(mapdl, resume):
        mapdl.prnsol("EPTH", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPTH", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        sint_ans = data[:, -2]
        sint = mapdl.post_processing.nodal_thermal_strain_intensity()

        sint_aligned = sint[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(sint_ans, sint_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_thermal_strain_intensity(mapdl, resume):
        assert mapdl.post_processing.plot_nodal_thermal_strain_intensity() is None

    @staticmethod
    def test_nodal_thermal_eqv_strain(mapdl, resume):
        mapdl.prnsol("EPTH", "PRIN", mute=True)  # run twice to clear out warning
        data = np.genfromtxt(mapdl.prnsol("EPTH", "PRIN").splitlines()[1:])
        nnum_ans = data[:, 0].astype(np.int32)
        seqv_ans = data[:, -1]
        seqv = mapdl.post_processing.nodal_thermal_eqv_strain()

        seqv_aligned = seqv[np.isin(mapdl.mesh.nnum, nnum_ans)]
        assert np.allclose(seqv_ans, seqv_aligned)

    @staticmethod
    @requires("ansys-tools-visualization_interface")
    def test_plot_nodal_thermal_eqv_strain(mapdl, resume):
        assert (
            mapdl.post_processing.plot_nodal_thermal_eqv_strain(smooth_shading=True)
            is None
        )


###############################################################################
