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

"""Test ansys.mapdl.solution.Solution"""

import pytest

from ansys.mapdl.core.errors import MapdlRuntimeError


def test_time_step_size(mapdl, cleared):
    assert isinstance(mapdl.solution.time_step_size, float)


def test_n_cmls(mapdl, cleared):
    assert isinstance(mapdl.solution.n_cmls, float)


def test_n_cmss(mapdl, cleared):
    assert isinstance(mapdl.solution.n_cmss, float)


def test_n_eqit(mapdl, cleared):
    assert isinstance(mapdl.solution.n_eqit, float)


def test_n_cmit(mapdl, cleared):
    assert isinstance(mapdl.solution.n_cmit, float)


def test_converged(mapdl, cleared):
    assert isinstance(mapdl.solution.converged, bool)


def test_mx_dof(mapdl, cleared):
    assert isinstance(mapdl.solution.mx_dof, float)


def test_res_frq(mapdl, cleared):
    assert isinstance(mapdl.solution.res_frq, float)


def test_res_eig(mapdl, cleared):
    assert isinstance(mapdl.solution.res_eig, float)


def test_decent_parm(mapdl, cleared):
    assert isinstance(mapdl.solution.decent_parm, float)


def test_force_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.force_cnv, float)


def test_moment_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.moment_cnv, float)


def test_heat_flow_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.heat_flow_cnv, float)


def test_magnetic_flux_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.magnetic_flux_cnv, float)


def test_current_segment_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.current_segment_cnv, float)


def test_current_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.current_cnv, float)


def test_fluid_flow_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.fluid_flow_cnv, float)


def test_displacement_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.displacement_cnv, float)


def test_rotation_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.rotation_cnv, float)


def test_temperature_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.temperature_cnv, float)


def test_vector_cnv(mapdl, cleared):
    assert isinstance(mapdl.solution.vector_cnv, float)


def test_smcv(mapdl, cleared):
    assert isinstance(mapdl.solution.smcv, float)


def test_voltage_conv(mapdl, cleared):
    assert isinstance(mapdl.solution.voltage_conv, float)


def test_pressure_conv(mapdl, cleared):
    assert isinstance(mapdl.solution.pressure_conv, float)


def test_velocity_conv(mapdl, cleared):
    assert isinstance(mapdl.solution.velocity_conv, float)


def test_mx_creep_rat(mapdl, cleared):
    assert isinstance(mapdl.solution.mx_creep_rat, float)


def test_mx_plastic_inc(mapdl, cleared):
    assert isinstance(mapdl.solution.mx_plastic_inc, float)


def test_n_cg_iter(mapdl, cleared):
    assert isinstance(mapdl.solution.n_cg_iter, float)


def test_solution_call(mapdl, cleared):
    mapdl.finish()
    output = mapdl.solution()
    assert "MAPDL SOLUTION ROUTINE" in output or "ANSYS SOLUTION ROUTINE" in output


def test_exited(mapdl, cleared):
    mapdl._exited = True
    with pytest.raises(MapdlRuntimeError):
        parm = mapdl.solution.time_step_size
    mapdl._exited = False
