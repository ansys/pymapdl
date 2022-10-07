"""Tests comparing results of krylov pymadl function with apdl macro"""
import os

import numpy as np
import pytest

PATH = os.path.dirname(os.path.abspath(__file__))

# Krylov Apdl Macro Files
ulib_path = os.path.join(PATH, "test_files")
kry_gensub = os.path.join(ulib_path, "KRYGENSUB.mac")
kry_solve = os.path.join(ulib_path, "KRYSOLVE.mac")
kry_expand = os.path.join(ulib_path, "KRYEXPAND.mac")


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
    if mapdl.info.mapdl_version_build not in ["22.2", "23.1"]:
        pytest.skip("Requires MAPDL v222 and above")

    # Case1 : Run Krylov Pymapdl
    mapdl.clear()
    mm = mapdl.math
    mapdl.jobname = "point_load_py"
    print(mapdl.directory)

    # Parameters set for Krylov
    max_q = 10
    frq = 100

    mapdl.cdread("db", os.path.join(ulib_path, "krylov_point_load"), "cdb")
    solu_krylov(mapdl, frq)

    dd = mapdl.krylov
    Qz_py = dd.krygensub(max_q, frq, True, True).asarray()
    Yz_py = dd.krysolve(frq, frq, 1, 1, True).asarray()
    dd.kryexpand(True, 3)
    Xii_py = mm.vec(name="Xii").asarray()

    mapdl.clear()
    # Case2 :Run Krylov Macro
    mapdl.jobname = "point_load_mac"

    mapdl.cdread("db", os.path.join(ulib_path, "krylov_point_load"), "cdb")
    # Run Harmonic Analysis
    solu_krylov(mapdl, frq)

    mapdl.use(kry_gensub, max_q, frq, 1, 1)
    Qz_macro = mm.mat(name="Qz").asarray()

    mapdl.use(kry_solve, frq, frq, 1, 1, 1)
    Yz_macro = mm.mat(name="Yz").asarray()
    mapdl.use(kry_expand, 1, 3)
    Xii_macro = mm.vec(name="Xii").asarray()

    # Compare Case 1 and 2 Results
    # setting the absolute and relative tolerance
    rtol = 1e-6
    atol = 1e-6

    # Verify Subspace
    assert np.allclose(Qz_macro, Qz_py, rtol, atol)
    # Verify Reduced Solution
    assert np.allclose(Yz_macro, Yz_py, rtol, atol)
    # Verify DOF solution
    assert np.allclose(Xii_macro, Xii_py, rtol, atol)


@pytest.mark.parametrize("res_key", [0, 1, 2, 3])
def test_krylov_with_pressure_load(mapdl, res_key):
    if mapdl.info.mapdl_version_build not in ["22.2", "23.1"]:
        pytest.skip("Requires MAPDL v222 and above")

    # With ramped loading
    # Case1 : Run Krylov Pymapdl
    mapdl.clear()
    mm = mapdl.math
    mapdl.jobname = "pressure_py"

    # Parameters set for Krylov
    max_q = 10
    frq = 100
    freq_val = frq

    mapdl.cdread("db", os.path.join(ulib_path, "krylov_pressure_load"), "cdb")
    # Run Harmonic Analysis
    solu_krylov(mapdl, frq)

    dd = mapdl.krylov
    Qz_py = dd.krygensub(max_q, frq, True, True).asarray()
    Yz_py = dd.krysolve(frq, frq, 1, 0, True).asarray()
    dd.kryexpand(True, res_key)
    Xii_py = mm.vec(name="Xii").asarray()

    mapdl.clear()
    # Case2 :Run Krylov Macro
    mapdl.jobname = "pressure_mac"

    mapdl.cdread("db", os.path.join(ulib_path, "krylov_pressure_load"), "cdb")
    # Run Harmonic Analysis
    solu_krylov(mapdl, frq)

    mapdl.use(kry_gensub, 10, 100, 1, 1)
    Qz_macro = mm.mat(name="Qz").asarray()
    mapdl.use(kry_solve, 100, 100, 1, 0, 1)
    Yz_macro = mm.mat(name="Yz").asarray()
    mapdl.use(kry_expand, 1, res_key)
    Xii_macro = mm.vec(name="Xii").asarray()

    # Compare Case 1 and 2 Results
    # setting the absolute and relative tolerance
    rtol = 1e-6
    atol = 1e-6

    # Verify Subspace
    assert np.allclose(Qz_macro, Qz_py, rtol, atol)
    # Verify Reduced Solution
    assert np.allclose(Yz_macro, Yz_py, rtol, atol)
    # Verify DOF solution
    assert np.allclose(Xii_macro, Xii_py, rtol, atol)


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
    if mapdl.info.mapdl_version_build not in ["22.2", "23.1"]:
        pytest.skip("Requires MAPDL v222 and above")

    mapdl.clear()
    # Parameters set for Krylov
    maxQ = input_kry_gensub[0]
    freq_val = input_kry_gensub[1]

    mapdl.cdread("db", os.path.join(ulib_path, "krylov_pressure_load"), "cdb")
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
    if mapdl.info.mapdl_version_build not in ["22.2", "23.1"]:
        pytest.skip("Requires MAPDL v222 and above")

    mapdl.clear()
    mapdl.cdread("db", os.path.join(ulib_path, "krylov_pressure_load"), "cdb")

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
    if mapdl.info.mapdl_version_build not in ["22.2", "23.1"]:
        pytest.skip("Requires MAPDL v222 and above")

    mapdl.clear()
    mapdl.cdread("db", os.path.join(ulib_path, "krylov_pressure_load"), "cdb")

    solu_krylov(mapdl, 100)
    dd = mapdl.krylov
    with pytest.raises(ValueError) as e:
        dd.kryexpand(input_kryexpand[0], input_kryexpand[1])
    assert str(e.value) == input_kryexpand[2]
