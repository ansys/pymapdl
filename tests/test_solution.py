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

"""Test ansys.mapdl.solution.Solution"""
import pytest

from ansys.mapdl.core.errors import MapdlRuntimeError


class TestSolution:
    @pytest.fixture(scope="class")
    def setup(self, mapdl):
        from conftest import clear

        clear(mapdl)
        mapdl.prep7()

    @staticmethod
    def test_time_step_size(setup, mapdl):
        assert isinstance(mapdl.solution.time_step_size, float)

    @staticmethod
    def test_n_cmls(setup, mapdl):
        assert isinstance(mapdl.solution.n_cmls, float)

    @staticmethod
    def test_n_cmss(setup, mapdl):
        assert isinstance(mapdl.solution.n_cmss, float)

    @staticmethod
    def test_n_eqit(setup, mapdl):
        assert isinstance(mapdl.solution.n_eqit, float)

    @staticmethod
    def test_n_cmit(setup, mapdl):
        assert isinstance(mapdl.solution.n_cmit, float)

    @staticmethod
    def test_converged(setup, mapdl):
        assert isinstance(mapdl.solution.converged, bool)

    @staticmethod
    def test_mx_dof(setup, mapdl):
        assert isinstance(mapdl.solution.mx_dof, float)

    @staticmethod
    def test_res_frq(setup, mapdl):
        assert isinstance(mapdl.solution.res_frq, float)

    @staticmethod
    def test_res_eig(setup, mapdl):
        assert isinstance(mapdl.solution.res_eig, float)

    @staticmethod
    def test_decent_parm(setup, mapdl):
        assert isinstance(mapdl.solution.decent_parm, float)

    @staticmethod
    def test_force_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.force_cnv, float)

    @staticmethod
    def test_moment_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.moment_cnv, float)

    @staticmethod
    def test_heat_flow_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.heat_flow_cnv, float)

    @staticmethod
    def test_magnetic_flux_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.magnetic_flux_cnv, float)

    @staticmethod
    def test_current_segment_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.current_segment_cnv, float)

    @staticmethod
    def test_current_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.current_cnv, float)

    @staticmethod
    def test_fluid_flow_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.fluid_flow_cnv, float)

    @staticmethod
    def test_displacement_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.displacement_cnv, float)

    @staticmethod
    def test_rotation_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.rotation_cnv, float)

    @staticmethod
    def test_temperature_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.temperature_cnv, float)

    @staticmethod
    def test_vector_cnv(setup, mapdl):
        assert isinstance(mapdl.solution.vector_cnv, float)

    @staticmethod
    def test_smcv(setup, mapdl):
        assert isinstance(mapdl.solution.smcv, float)

    @staticmethod
    def test_voltage_conv(setup, mapdl):
        assert isinstance(mapdl.solution.voltage_conv, float)

    @staticmethod
    def test_pressure_conv(setup, mapdl):
        assert isinstance(mapdl.solution.pressure_conv, float)

    @staticmethod
    def test_velocity_conv(setup, mapdl):
        assert isinstance(mapdl.solution.velocity_conv, float)

    @staticmethod
    def test_mx_creep_rat(setup, mapdl):
        assert isinstance(mapdl.solution.mx_creep_rat, float)

    @staticmethod
    def test_mx_plastic_inc(setup, mapdl):
        assert isinstance(mapdl.solution.mx_plastic_inc, float)

    @staticmethod
    def test_n_cg_iter(setup, mapdl):
        assert isinstance(mapdl.solution.n_cg_iter, float)

    @staticmethod
    def test_solution_call(setup, mapdl):
        mapdl.finish()
        output = mapdl.solution()
        assert "MAPDL SOLUTION ROUTINE" in output or "ANSYS SOLUTION ROUTINE" in output

    @staticmethod
    def test_exited(setup, mapdl):
        mapdl._exited = True
        with pytest.raises(MapdlRuntimeError):
            parm = mapdl.solution.time_step_size
        mapdl._exited = False
