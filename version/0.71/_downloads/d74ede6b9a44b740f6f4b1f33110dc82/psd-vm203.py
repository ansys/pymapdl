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

"""
.. _ref_psd_vm203:

=========================
Dynamic Load Effect on a Supported Thick Plate
=========================

This example demonstrates how to perform a random vibration analysis
using PyMAPDL.


This example is based on the ANSYS Verification Manual, problem 203
(VM203).

Description
===========

A simply-supported thick square plate of length L, thickness t, and mass
per unit area m is subject to random uniform pressure power spectral
density. Determine the peak one-sigma displacement at undamped natural
frequency.

A frequency range of 1.0 Hz to 80 Hz is used as an approximation of the
white noise PSD forcing function frequency.  The PSD curve is a constant
$$(1E6 N/m^2)^2 / Hz$$.

The model is solved using SHELL281 elements and generic materials.

Import modules
==============
"""
import matplotlib.pyplot as plt
from tabulate import tabulate

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()

mapdl.clear()
mapdl.prep7()
mapdl.units("mks")

###############################################################################
# Parameters
# ==========
#
# Loading parameters
LOAD_PRES = -1e6
DAMPING_RATIO = 0.02

###############################################################################
# Set up the FE model
# ===================
#
# Set the element type to SHELL281, which is a 3D structural
# high-order shell element.
thickness = 1

mapdl.et(1, "SHELL281")
mapdl.sectype(1, "SHELL")
mapdl.secdata(1, thickness, 0, 5)

###############################################################################
# Set material properties
# -----------------------
#
# Units are in the international unit system.
#
EX = 200e9
PR = 0.3
DENS = 8000

mapdl.mp("EX", 1, EX)
mapdl.mp("NUXY", 1, PR)
mapdl.mp("DENS", 1, DENS)

###############################################################################
# Create geometry
# ---------------
#
# Create the model geometry.
L1 = 10

mapdl.n(1, 0, 0, 0)
mapdl.n(9, 0, L1, 0)
mapdl.fill()
mapdl.ngen(5, 40, 1, 9, 1, L1 / 4)
mapdl.n(21, L1 / 8, 0, 0)
mapdl.n(29, L1 / 8, 10, 0)
mapdl.fill(21, 29, 3)
mapdl.ngen(4, 40, 21, 29, 2, L1 / 4)
mapdl.en(1, 1, 41, 43, 3, 21, 42, 23, 2)
mapdl.egen(4, 2, 1)
mapdl.egen(4, 40, 1, 4)

###############################################################################
# Loads and boundary conditions
# ------------------------------
#
# Define loads and boundary conditions.
#
# Apply a uniform pressure load of 1,000,000 N/m^2
mapdl.sfe("ALL", "", "PRES", "", LOAD_PRES)

###############################################################################
# Apply constraints UX, UY, ROTZ DOFs all fixed
#
mapdl.d("ALL", "UX", 0, "", "", "", "UY", "ROTZ")

###############################################################################
# Simply supported on the four corners
#
mapdl.d(1, "UZ", 0, 0, 9, 1, "ROTX")
mapdl.d(161, "UZ", 0, 0, 169, 1, "ROTX")
mapdl.d(1, "UZ", 0, 0, 161, 20, "ROTY")
mapdl.d(9, "UZ", 0, 0, 169, 20, "ROTY")


###############################################################################
# Solve the model
# ===============
#
# Solve the modal analysis using the PCG Lanczos solver to find and expand the
# first two modes of the model.
n_modes = 2
mapdl.solution()
mapdl.antype("MODAL")
mapdl.modopt("LANPCG", n_modes)
mapdl.mxpand(n_modes, "", "", "YES")

mapdl.solve()
# Getting frequency of the first mode
f0 = mapdl.get_value("MODE", 1, "FREQ")

mapdl.finish()

###############################################################################
# PSD Spectrum analysis
# =====================
#
# Now let's perform PSD spectrum analysis using the two solved modes:
#
mapdl.slashsolu()
mapdl.antype("SPECTR")
mapdl.spopt("PSD", n_modes, "ON")

###############################################################################
# Define the PSD spectrum
#
mapdl.psdunit(1, "PRES")

###############################################################################
# Applying proportional damping
#
mapdl.dmprat(DAMPING_RATIO)

###############################################################################
# PSD frequency value table 1 to 80 Hz
#
freqA = 1.0
freqB = 80.0

mapdl.psdfrq(1, 1, freq1=freqA, freq2=freqB)
mapdl.psdval(1, 1.0, 1.0)

###############################################################################
# Define the PSD load vector generated at modal analysis
#
mapdl.sfedele("ALL", "", "PRES")
mapdl.lvscale(1)
mapdl.pfact(1, "NODE")

###############################################################################
# Write out the displacement result
#
mapdl.psdres("DISP", "REL")
# set for PSD mode combination method
mapdl.psdcom()
mapdl.solve()

mapdl.finish()

###############################################################################
# Post-processing
# ===============
#
# Now we can plot the results of the one-sigma displacement solution.
# We will plot the Z displacement of the nodes.
mapdl.post1()
# One Sigma Displacement Solution Results
mapdl.set(3, 1)
mapdl.post_processing.plot_nodal_displacement("Z", cmap="jet", cpos="iso")
mapdl.finish()

###############################################################################
# Use post26 to capture then plot the response psd and the max value
#
number_frequencies = 2
mapdl.post26()
mapdl.store("PSD", number_frequencies)

node85_uz = mapdl.nsol(2, 85, "U", "Z")
rpsduz = mapdl.rpsd(3, 2, "", 1, 2)


###############################################################################
# While you can use the `extrem` command to get the maximum and minimum values:
print(mapdl.extrem(2, 3))

###############################################################################
# You can also use Numpy methods to find the max value of the response psd.
print(
    tabulate(
        [
            ["", "Maximum", "Minimum"],
            ["Z-displacement on node 85", node85_uz.max(), node85_uz.min()],
            ["Response power spectral density", rpsduz.max(), rpsduz.min()],
        ],
        headers="firstrow",
        tablefmt="grid",
        floatfmt=".4e",
        numalign="center",
        stralign="right",
    )
)

###############################################################################
# To get the maximum value of the response psd you can use the `get_value`
# ( wrapper of `*GET`) method with the `EXTREM` option:
Pmax = mapdl.get_value("VARI", 3, "EXTREM", "VMAX")

###############################################################################
# However, you can also use the numpy methods here as well:
Pmax = rpsduz.max()

###############################################################################
# plot the response psd
freqs = mapdl.vget("FREQS", 1)

# Remove the last two values as they are zero
plt.plot(freqs[:-2], rpsduz[:-2], label="RPSD UZ")

plt.xlabel("Frequency Hz")
plt.ylabel(r"RPSD $\left( \dfrac{M^2}{Hz}\right)$")
plt.legend()
plt.tight_layout()
plt.show()

###############################################################################
# Compare and print results to manual values
manual = [45.9, 3.4018e-3]

arr = [
    ["", "Manual", "Calculated", "Ratio"],
    ["Frequency (Hz)", manual[0], f0, abs(f0 / manual[0])],
    ["Peak Deflection PSD (m^2/Hz)", manual[1], Pmax, abs(Pmax / manual[1])],
]

print(tabulate(arr, headers="firstrow", tablefmt="grid"))

###############################################################################
# Exit MAPDL
mapdl.exit()
