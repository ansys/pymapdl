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

# Subspace :
Qz_macro_pt_load = [
    [
        5.00000000e-01 - 1.84926562e-11j,
        -3.87354017e-07 - 5.08906971e-01j,
        3.61333350e-01 - 8.51722938e-07j,
        9.94518787e-07 - 5.13609180e-01j,
        5.88590777e-01 - 2.59109046e-06j,
        -1.44692928e-07 - 3.61497270e-01j,
        -3.26254862e-01 + 1.91185664e-05j,
        -1.99868241e-05 + 6.82308395e-01j,
        5.44556501e-01 - 1.49733761e-05j,
        -4.82116166e-05 + 3.62589620e-01j,
    ],
    [
        5.00000000e-01 - 1.84926562e-11j,
        -1.87795593e-07 - 4.35415764e-01j,
        -6.54646668e-01 + 1.11316086e-06j,
        1.09181165e-06 - 4.78025488e-01j,
        -3.91254740e-01 + 1.71792461e-06j,
        6.81467569e-07 + 6.52535848e-01j,
        -2.12914986e-01 + 1.59580996e-05j,
        -2.18689615e-05 + 5.86977495e-01j,
        -4.27920101e-01 + 7.72290926e-06j,
        8.64786505e-05 - 6.53459262e-01j,
    ],
    [
        5.00000000e-01 - 1.84926562e-11j,
        7.42718986e-08 + 2.46551217e-01j,
        5.67766112e-01 - 1.14216909e-06j,
        9.80871738e-07 - 5.19804410e-01j,
        -5.89080742e-01 + 2.59111184e-06j,
        -6.56503076e-07 - 5.92886936e-01j,
        3.91200576e-01 - 5.33364816e-06j,
        -2.27897814e-05 + 3.57573043e-01j,
        -6.07556012e-01 + 1.20934487e-05j,
        -7.82407631e-05 + 5.91590495e-01j,
    ],
    [
        5.00000000e-01 - 1.84926562e-11j,
        4.91044590e-07 + 7.00456498e-01j,
        -3.44263841e-01 + 6.80623592e-07j,
        1.07141755e-06 - 4.87340351e-01j,
        3.91745460e-01 - 1.71783762e-06j,
        -9.01942120e-08 + 3.03317939e-01j,
        8.33778797e-01 - 2.05535638e-05j,
        -2.11641929e-05 + 2.49106785e-01j,
        3.88867967e-01 - 1.09640138e-05j,
        4.04467633e-05 - 3.02556489e-01j,
    ],
]

# Reduced sol :
Yz_macro_pt_load = [
    [4.53522007e-08 + 4.80605524e-12j],
    [-2.47364308e-12 - 1.83836225e-07j],
    [1.01821190e-07 - 5.05639606e-11j],
    [-4.51797374e-12 + 5.70324250e-08j],
    [6.35561623e-07 - 4.33302566e-11j],
    [-5.66796438e-12 - 1.98070834e-07j],
    [-1.86595149e-07 - 9.06820165e-12j],
    [-5.96288922e-12 + 4.52539460e-08j],
    [-6.36517086e-07 + 3.14287095e-11j],
    [3.32791414e-11 - 8.68995698e-08j],
]

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
Qz_macro_pres_load = [
    [
        0.17609857 + 0.00000000j,
        0.00000000 - 0.33564229j,
        0.56457277 + 0.00000000j,
        0.00000000 - 0.19388433j,
        0.38181719 + 0.00000000j,
        0.00000000 - 0.18047491j,
        0.08586845 + 0.00000000j,
        0.00000000 - 0.15943891j,
        0.54168745 + 0.00000000j,
        0.00000000 + 0.38491684j,
    ],
    [
        -0.66527742 + 0.00000000j,
        0.00000000 - 0.02057382j,
        0.12555705 + 0.00000000j,
        0.00000000 - 0.20302242j,
        -0.27439468 + 0.00000000j,
        0.00000000 - 0.33887137j,
        0.64185249 + 0.00000000j,
        0.00000000 - 0.47840375j,
        -0.08935224 + 0.00000000j,
        0.00000000 - 0.45568367j,
    ],
    [
        -0.08418425 + 0.00000000j,
        0.00000000 + 0.33039543j,
        0.38840947 + 0.00000000j,
        0.00000000 + 0.48258673j,
        -0.07620894 + 0.00000000j,
        0.00000000 + 0.29872773j,
        0.40667459 + 0.00000000j,
        0.00000000 + 0.45175313j,
        0.21012417 + 0.00000000j,
        0.00000000 - 0.36302748j,
    ],
    [
        0.13895419 + 0.00000000j,
        0.00000000 + 0.52702925j,
        0.12095908 + 0.00000000j,
        0.00000000 - 0.43393641j,
        -0.40478408 + 0.00000000j,
        0.00000000 + 0.43272516j,
        -0.34716849 + 0.00000000j,
        0.00000000 - 0.14577362j,
        0.39361108 + 0.00000000j,
        0.00000000 + 0.06100319j,
    ],
    [
        -0.08418425 + 0.00000000j,
        0.00000000 + 0.33039543j,
        0.38840947 + 0.00000000j,
        0.00000000 + 0.48258673j,
        0.13261652 + 0.00000000j,
        0.00000000 - 0.13256738j,
        -0.4684826 + 0.00000000j,
        0.00000000 - 0.45823289j,
        -0.20987796 + 0.00000000j,
        0.00000000 + 0.27553565j,
    ],
    [
        0.13895419 + 0.00000000j,
        0.00000000 + 0.52702925j,
        0.12095908 + 0.00000000j,
        0.00000000 - 0.43393641j,
        0.6377766 + 0.00000000j,
        0.00000000 + 0.25360324j,
        0.09186937 + 0.00000000j,
        0.00000000 + 0.11900884j,
        -0.3925941 + 0.00000000j,
        0.00000000 - 0.31884317j,
    ],
    [
        0.17609857 + 0.00000000j,
        0.00000000 - 0.33564229j,
        0.56457277 + 0.00000000j,
        0.00000000 - 0.19388433j,
        -0.42280844 + 0.00000000j,
        0.00000000 + 0.05972658j,
        -0.04095272 + 0.00000000j,
        0.00000000 + 0.16414774j,
        -0.54186637 + 0.00000000j,
        0.00000000 + 0.52808241j,
    ],
    [
        -0.66527742 + 0.00000000j,
        0.00000000 - 0.02057382j,
        0.12555705 + 0.00000000j,
        0.00000000 - 0.20302242j,
        -0.07843547 + 0.00000000j,
        0.00000000 - 0.70046393j,
        -0.25524253 + 0.00000000j,
        0.00000000 + 0.51893475j,
        0.08781218 + 0.00000000j,
        0.00000000 + 0.22853708j,
    ],
]

Yz_macro_pres_load = [
    [5.85283190e-10 + 0.00000000e00j],
    [-0.00000000e00 + 2.49347644e-11j],
    [1.96179823e-11 + 0.00000000e00j],
    [-0.00000000e00 + 2.92009790e-12j],
    [-3.48429156e-12 + 0.00000000e00j],
    [0.00000000e00 + 3.47795647e-12j],
    [-3.32135986e-11 + 0.00000000e00j],
    [0.00000000e00 - 8.34732010e-13j],
    [-7.00176030e-14 + 0.00000000e00j],
    [-0.00000000e00 + 4.55857038e-11j],
]

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
    Qz_py = dd.krygensub(max_q, frq, True, True).asarray()
    Yz_py = dd.krysolve(frq, frq, 1, 1, True).asarray()
    dd.kryexpand(True, 3)
    Xii_py = mm.vec(name="Xii").asarray()

    # setting the absolute and relative tolerance
    rtol = 1e-4
    atol = 1e-4

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
    Qz_py = dd.krygensub(max_q, frq, True, True).asarray()
    print(Qz_py)
    Yz_py = dd.krysolve(frq, frq, 1, 0, True).asarray()
    print(Yz_py)
    dd.kryexpand(True, res_key)
    Xii_py = mm.vec(name="Xii").asarray()
    print(Xii_py)

    # setting the absolute and relative tolerance
    rtol = 1e-4
    atol = 1e-4

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
        pytest.skip("Requires MAPDL v222 and above")

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
