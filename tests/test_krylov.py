"""Tests comparing results of krylov pymadl function with apdl macro"""
import os

import numpy as np

PATH = os.path.dirname(os.path.abspath(__file__))

# Krylov Apdl Macro Files
ulib_path = os.path.join(PATH, "test_files")
kry_gensub = os.path.join(ulib_path, "KRYGENSUB.mac")
kry_solve = os.path.join(ulib_path, "KRYSOLVE.mac")
kry_expand = os.path.join(ulib_path, "KRYEXPAND.mac")


def model_setup(mapdl, damp=0):
    mapdl.clear()
    mapdl.prep7()
    mapdl.et(1, 185)
    length = 1.5
    width = 0.3
    mapdl.block(0, length, -width / 2, width / 2, -width / 2, width / 2)
    mapdl.vsweep(1)

    # Define a material (nominal steel in SI)
    mapdl.mp("EX", 1, 210e9)  # Elastic moduli in Pa (kg/(m*s**2))
    mapdl.mp("DENS", 1, 7800)  # Density in kg/m3
    mapdl.mp("NUXY", 1, 0.3)  # Poisson's Ratio

    if damp == 1:
        mapdl.mp("ALPD", 1, 0.001)

    # Create BC
    mapdl.nsel("S", "LOC", "X", 0)
    mapdl.d("ALL", "UX")
    mapdl.d("ALL", "UY")
    mapdl.d("ALL", "UZ")

    mapdl.allsel()

    return length, width


def solu_krylov(mapdl, frq_):
    mapdl.allsel()
    mapdl.run("/SOLU")
    mapdl.antype("HARMIC")  # HARMONIC ANALYSIS
    mapdl.hropt("KRYLOV")
    mapdl.eqslv("SPARSE")
    mapdl.harfrq(frq_)  # Set beginning and ending frequency
    mapdl.nsubst(1)  # Set the number of frequency increments
    mapdl.wrfull(1)  # GENERATE .FULL FILE AND STOP
    output = mapdl.solve()
    mapdl.finish()


def test_krylov_with_point_load(mapdl):
    # Case1 : Run Krylov Pymapdl
    length, width = model_setup(mapdl, damp=1)
    mm = mapdl.math
    mapdl.jobname = "point_load_py"

    # Parameters set for Krylov
    maxQ = 10
    frq_ = 100
    Freqval_ = frq_

    # Define Load
    mapdl.prep7()
    mapdl.nsel("S", "LOC", "X", length)
    mapdl.f("ALL", "FX", 1000)
    mapdl.allsel()
    mapdl.d("ALL", "UY")
    mapdl.d("ALL", "UZ")

    solu_krylov(mapdl, frq_)

    dd = mapdl.krylov
    Qz_py = dd.krygensub(maxQ, Freqval_, 1, 1).asarray()
    Yz_py = dd.krysolve(Freqval_, Freqval_, 1, 1, 1).asarray()
    dd.kryexpand(1, 3)
    Xii_py = mm.vec(name="Xii").asarray()

    # Case2 :Run Krylov Macro
    length, width = model_setup(mapdl, damp=1)
    mapdl.jobname = "point_load_mac"

    # Define Load
    mapdl.prep7()
    mapdl.nsel("S", "LOC", "X", length)
    mapdl.f("ALL", "FX", 1000)
    mapdl.allsel()
    mapdl.d("ALL", "UY")
    mapdl.d("ALL", "UZ")

    # Run Harmonic Analysis
    solu_krylov(mapdl, frq_)

    mapdl.use(kry_gensub, maxQ, Freqval_, 1, 1)
    Qz_macro = mm.mat(name="Qz").asarray()
    mapdl.use(kry_solve, Freqval_, Freqval_, 1, 1, 1)
    Yz_macro = mm.mat(name="Yz").asarray()
    mapdl.use(kry_expand, 1, 3)
    Xii_macro = mm.vec(name="Xii").asarray()

    # Compare Case 1 and 2 Results
    # setting the absolute and relative tolerance
    rtol = 1e-10
    atol = 1e-10

    # Verify Subspace
    assert np.allclose(Qz_macro, Qz_py, rtol, atol)
    # Verify Reduced Solution
    assert np.allclose(Yz_macro, Yz_py, rtol, atol)
    # Verify DOF solution
    assert np.allclose(Xii_macro, Xii_py, rtol, atol)


def test_krylov_with_pressure_load(mapdl):
    # With ramped loading
    # Case1 : Run Krylov Pymapdl
    length, width = model_setup(mapdl)
    mm = mapdl.math
    mapdl.jobname = "pressure_py"

    # Parameters set for Krylov
    maxQ = 10
    frq_ = 100
    Freqval_ = frq_

    # Define Load
    mapdl.prep7()
    mapdl.nsel("S", "LOC", "Y", width / 2)
    mapdl.sf("ALL", "PRES", 1000)
    mapdl.allsel()
    mapdl.d("ALL", "UZ")

    # Run Harmonic Analysis
    solu_krylov(mapdl, frq_)

    dd = mapdl.krylov
    Qz_py = dd.krygensub(maxQ, Freqval_, 1, 1).asarray()
    Yz_py = dd.krysolve(Freqval_, Freqval_, 1, 0, 1).asarray()
    dd.kryexpand(1, 3)
    Xii_py = mm.vec(name="Xii").asarray()

    # # Case2 :Run Krylov Macro
    length, width = model_setup(mapdl)
    mapdl.jobname = "pressure_mac"

    mapdl.prep7()
    mapdl.nsel("S", "LOC", "Y", width / 2)
    mapdl.sf("ALL", "PRES", 1000)
    mapdl.allsel()
    mapdl.d("ALL", "UZ")

    # Run Harmonic Analysis
    solu_krylov(mapdl, frq_)

    mapdl.use(kry_gensub, maxQ, Freqval_, 1, 1)
    Qz_macro = mm.mat(name="Qz").asarray()
    mapdl.use(kry_solve, Freqval_, Freqval_, 1, 0, 1)
    Yz_macro = mm.mat(name="Yz").asarray()
    mapdl.use(kry_expand, 1, 3)
    Xii_macro = mm.vec(name="Xii").asarray()

    # Compare Case 1 and 2 Results
    # setting the absolute and relative tolerance
    rtol = 1e-10
    atol = 1e-10

    # Verify Subspace
    assert np.allclose(Qz_macro, Qz_py, rtol, atol)
    # Verify Reduced Solution
    assert np.allclose(Yz_macro, Yz_py, rtol, atol)
    # Verify DOF solution
    assert np.allclose(Xii_macro, Xii_py, rtol, atol)
