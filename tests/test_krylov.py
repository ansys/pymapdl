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

"""Tests comparing results of krylov pymadl function with apdl macro"""

import os

from ansys.tools.common.versioning import server_meets_version
import numpy as np
import pytest

from conftest import has_dependency

if not has_dependency("ansys-math-core"):
    # Needs ansys-math-core
    pytest.skip(
        allow_module_level=True,
        reason="Skipping because 'ansys-math-core' is not installed",
    )

PATH = os.path.dirname(os.path.abspath(__file__))

# Krylov APDL Macro Files
lib_path = os.path.join(PATH, "test_files")

# Results from APDL Macro to compare with PyMAPDL results
# Case 1 : Model with point load

# Expanded sol
Xii_macro_pt_load = [
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    1.25777677e-08 - 4.65192672e-19j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    1.25777677e-08 - 4.65192662e-19j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    1.25777677e-08 - 4.65192681e-19j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
    1.25777677e-08 - 4.65192661e-19j,
    0.00000000e00 + 0.00000000e00j,
    0.00000000e00 + 0.00000000e00j,
]

# Case 2 : Model with Pressure load
Xii_macro_pres_load = [
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    0.00000000e00 + 0.0j,
    1.01806232e-10 + 0.0j,
    -3.84610666e-10 + 0.0j,
    0.00000000e00 + 0.0j,
    -4.86686586e-11 + 0.0j,
    8.03322966e-11 + 0.0j,
    0.00000000e00 + 0.0j,
    -4.86686586e-11 + 0.0j,
    8.03322966e-11 + 0.0j,
    0.00000000e00 + 0.0j,
    1.01806232e-10 + 0.0j,
    -3.84610666e-10 + 0.0j,
    0.00000000e00 + 0.0j,
]


def solu_krylov(mapdl, frq):
    mapdl.allsel()
    mapdl.run("/SOLU")
    mapdl.antype("HARMIC")  # HARMONIC ANALYSIS
    mapdl.hropt("KRYLOV")
    mapdl.eqslv("SPARSE")
    mapdl.harfrq(frq)  # Set beginning and ending frequency
    mapdl.nsubst(1)  # Set the number of frequency increments
    mapdl.wrfull(1)  # GENERATE .FULL FILE AND STOP
    mapdl.solve()
    mapdl.finish()


@pytest.mark.krylov_tests
def test_krylov_with_point_load(mapdl, cleared):
    if not server_meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL 2022 R2 or later.")

    # Case1 : Run Krylov PyMAPDL
    mapdl.jobname = "point_load_py"

    # Parameters set for Krylov
    max_dim_q = 10
    frequency = 100

    mapdl.cdread("db", os.path.join(lib_path, "krylov_point_load"), "cdb")
    solu_krylov(mapdl, frequency)

    dd = mapdl.krylov
    dd.gensubspace(max_dim_q, frequency, check_orthogonality=True)
    dd.solve(frequency, frequency, freq_steps=1, ramped_load=True)
    dd.expand(residual_computation=True, residual_algorithm="l2")
    Xii_py = dd.mm.vec(name="Xii").asarray()

    # setting the absolute and relative tolerance
    rtol = 1e-16
    atol = 1e-16

    # Verify DOF solution
    assert np.allclose(Xii_macro_pt_load, Xii_py, rtol, atol)


@pytest.mark.krylov_tests
@pytest.mark.parametrize(
    "residual_algorithm", ["L-inf", "Linf", "L-1", "L1", "L-2", "L2"]
)
def test_krylov_with_pressure_load(mapdl, cleared, residual_algorithm):
    if not server_meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL 2022 R2 or later.")

    # With ramped loading
    # Case1 : Run Krylov PyMAPDL
    mapdl.jobname = "pressure_py"

    # Parameters set for Krylov
    max_q = 10
    frq = 100

    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")
    # Run Harmonic Analysis
    solu_krylov(mapdl, frq)

    dd = mapdl.krylov
    dd.gensubspace(max_q, frq, check_orthogonality=True)
    dd.solve(frq, frq, freq_steps=1, ramped_load=True)
    dd.expand(residual_computation=True, residual_algorithm=residual_algorithm)
    Xii_py = dd.mm.vec(name="Xii").asarray()

    # setting the absolute and relative tolerance
    rtol = 1e-16
    atol = 1e-16

    # Verify DOF solution
    assert np.allclose(Xii_macro_pres_load, Xii_py, rtol, atol)


# Test Exceptions
@pytest.mark.parametrize(
    "maxQ,freq,check_ortho,error_msg",
    [
        (
            10.2,
            100,
            True,
            "The maximum size of the Krylov subspace must be greater than 0.",
        ),
        (
            -2,
            100,
            True,
            "The maximum size of the Krylov subspace must be greater than 0.",
        ),
        (
            10,
            100.3,
            True,
            "The frequency value ('freq_val') for building the Krylov subspace must be",
        ),
        (
            10,
            -100,
            True,
            "The frequency value ('freq_val') for building the Krylov subspace must be",
        ),
        (
            10,
            100,
            3,
            "The 'check_orthogonality' value for building the Krylov subspace must be",
        ),
    ],
)
def test_non_valid_inputs_gensubspace(
    mapdl, cleared, maxQ, freq, check_ortho, error_msg
):
    if not server_meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL 2022 R2 or later.")

    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")
    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd.gensubspace(maxQ, freq, check_ortho)
    assert error_msg in str(e.value)


@pytest.mark.parametrize(
    "freq_start,freq_end,freq_steps,ramped_load,error_msg",
    [
        (
            -2,
            100,
            10,
            True,
            "The beginning frequency value for solving the reduced solution must be",
        ),
        (
            2,
            100,
            -10,
            False,
            "The number of frequencies ('freq_steps') for which to compute the reduced",
        ),
        (
            2,
            100,
            10,
            1,
            "The 'ramped_load' argument for computing the reduced solution must be",
        ),
    ],
)
def test_non_valid_inputs_solve(
    mapdl, cleared, freq_start, freq_end, freq_steps, ramped_load, error_msg
):
    if not server_meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL 2022 R2 or later.")

    mapdl.clear()
    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")

    # Parameters set for Krylov
    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd._check_input_solve(freq_start, freq_end, freq_steps, ramped_load)
    assert error_msg in str(e.value)


@pytest.mark.parametrize(
    "return_solution,residual_computation,residual_algorithm,error_msg",
    [
        (
            2,
            100,
            "l-inf",
            "The 'return_solution' value for expanding the solution must be",
        ),
        (
            True,
            5,
            "l-inf",
            "The 'residual_computation' must be True or False",
        ),
        (
            True,
            -1,
            "l-inf",
            "The 'residual_computation' must be True or False",
        ),
        (
            True,
            True,
            "l-3",
            "The provided 'residual_algorithm' is not allowed. Only allowed are",
        ),
    ],
)
def test_non_valid_inputs_expand(
    mapdl, return_solution, residual_computation, residual_algorithm, error_msg
):
    if not server_meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL 2022 R2 or later.")

    mapdl.clear()
    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")

    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd._check_input_expand(
            return_solution, residual_computation, residual_algorithm
        )
    assert error_msg in str(e.value)


def test_check_full_file_exist(mapdl, cleared):
    # deleting previous full file.
    if mapdl.is_local:
        full_file = mapdl.directory / (mapdl.jobname + ".full")
        if os.path.exists(full_file):
            os.remove(full_file)
    else:
        mapdl.slashdelete(mapdl.jobname + ".full")

    kk = mapdl.krylov
    with pytest.raises(FileNotFoundError):
        kk._check_full_file_exists("mydummy.full")

    with pytest.raises(FileNotFoundError):
        kk._check_full_file_exists()
