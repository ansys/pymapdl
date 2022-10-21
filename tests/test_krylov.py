"""Tests comparing results of krylov pymadl function with apdl macro"""
import os

import numpy as np
import pytest

from ansys.mapdl.core.check_version import meets_version

PATH = os.path.dirname(os.path.abspath(__file__))

# Krylov Apdl Macro Files
lib_path = os.path.join(PATH, "test_files")

# Results from APDL Macro to compare with Pymapdl results
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


def test_krylov_with_point_load(mapdl):
    if not meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL v222 and above")

    # Case1 : Run Krylov Pymapdl
    mapdl.clear()
    mm = mapdl.math
    mapdl.jobname = "point_load_py"

    # Parameters set for Krylov
    max_q = 10
    frq = 100

    mapdl.cdread("db", os.path.join(lib_path, "krylov_point_load"), "cdb")
    solu_krylov(mapdl, frq)

    dd = mapdl.krylov
    dd.krygensub(max_q, frq, True, True).asarray()
    dd.krysolve(frq, frq, 1, 1, True).asarray()
    dd.kryexpand(True, 3)
    Xii_py = mm.vec(name="Xii").asarray()

    # setting the absolute and relative tolerance
    rtol = 1e-16
    atol = 1e-16

    # Verify DOF solution
    assert np.allclose(Xii_macro_pt_load, Xii_py, rtol, atol)


@pytest.mark.parametrize("res_key", [0, 1, 2, 3])
def test_krylov_with_pressure_load(mapdl, res_key):
    if not meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL v222 and above")

    # With ramped loading
    # Case1 : Run Krylov Pymapdl
    mapdl.clear()
    mm = mapdl.math
    mapdl.jobname = "pressure_py"

    # Parameters set for Krylov
    max_q = 10
    frq = 100

    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")
    # Run Harmonic Analysis
    solu_krylov(mapdl, frq)

    dd = mapdl.krylov
    dd.krygensub(max_q, frq, True, True).asarray()
    dd.krysolve(frq, frq, 1, 0, True).asarray()
    dd.kryexpand(True, res_key)
    Xii_py = mm.vec(name="Xii").asarray()

    # setting the absolute and relative tolerance
    rtol = 1e-16
    atol = 1e-16

    # Verify DOF solution
    assert np.allclose(Xii_macro_pres_load, Xii_py, rtol, atol)


# Test Exceptions
@pytest.mark.parametrize(
    "input_kry_gensub",
    [
        (
            10.2,
            100,
            True,
            True,
            "The maximum size of Krylov subspace is required to be greater than 0",
        ),
        (
            -2,
            100,
            True,
            True,
            "The maximum size of Krylov subspace is required to be greater than 0",
        ),
        (
            10,
            100.3,
            True,
            True,
            "The frequency value for building the Krylov subspace is required to be greater or equal to 0 Hz",
        ),
        (
            10,
            -100,
            True,
            True,
            "The frequency value for building the Krylov subspace is required to be greater or equal to 0 Hz",
        ),
        (
            10,
            100,
            3,
            False,
            "The chk_ortho_key value for building the Krylov subspace is required to be Boolean True or False",
        ),
        (
            10,
            100,
            True,
            2,
            "The out_key value for building the Krylov subspace is required to be to be Boolean True or False",
        ),
    ],
)
def test_non_valid_inputs_krygensub(mapdl, input_kry_gensub):
    if not meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL v222 and above")

    mapdl.clear()
    # Parameters set for Krylov
    maxQ = input_kry_gensub[0]
    freq_val = input_kry_gensub[1]

    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")
    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd.krygensub(maxQ, freq_val, input_kry_gensub[2], input_kry_gensub[3])
    assert str(e.value) == input_kry_gensub[4]


@pytest.mark.parametrize(
    "input_krysolve",
    [
        (
            -2,
            100,
            10,
            0,
            True,
            "The beginning frequency value for solving the reduced solution is required to be greater than or equal to 0",
        ),
        (
            2,
            100,
            -10,
            1,
            False,
            "The number of frequencies for which to compute the reduced solution is required to be greater than 0",
        ),
        (
            2,
            100,
            10,
            -1,
            True,
            "The Load key value for computing the reduced solution is required to be 0 or 1",
        ),
        (
            2,
            100,
            10,
            0,
            2,
            "The out_key value for computing the reduced solution is required to be Boolean True or False",
        ),
    ],
)
def test_non_valid_inputs_krysolve(mapdl, input_krysolve):
    if not meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL 2022 R2 or later.")

    mapdl.clear()
    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")

    # Parameters set for Krylov
    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd.krysolve(
            input_krysolve[0],
            input_krysolve[1],
            input_krysolve[2],
            input_krysolve[3],
            input_krysolve[4],
        )
    assert str(e.value) == input_krysolve[5]


@pytest.mark.parametrize(
    "input_kryexpand",
    [
        (
            2,
            100,
            "The out_key value for expanding the reduced solution is required to be Boolean True or False",
        ),
        (
            True,
            5,
            "The res_key value for expanding the reduced solution is required to be 0 -> 3",
        ),
        (
            True,
            -1,
            "The res_key value for expanding the reduced solution is required to be 0 -> 3",
        ),
    ],
)
def test_non_valid_inputs_kryexpand(mapdl, input_kryexpand):
    if not meets_version(mapdl._server_version, (0, 5, 0)):
        pytest.skip("Requires MAPDL v222 and above")

    mapdl.clear()
    mapdl.cdread("db", os.path.join(lib_path, "krylov_pressure_load"), "cdb")

    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd.kryexpand(input_kryexpand[0], input_kryexpand[1])
    assert str(e.value) == input_kryexpand[2]
