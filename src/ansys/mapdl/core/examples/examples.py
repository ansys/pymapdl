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

"""pymapdl examples"""
import os

# get location of this folder and the example files
__dir_path: str = os.path.dirname(os.path.realpath(__file__))

# add any files you'd like to import here.  For example:
wing_model: str = os.path.join(__dir_path, "wing.dat")

# Verification files
from ansys.mapdl.core.examples.verif_files import vmfiles

laterally_loaded_tapered_support_structure = vmfiles["vm5"]
pinched_cylinder = vmfiles["vm6"]
transient_thermal_stress_in_a_cylinder = vmfiles["vm33"]
elongation_of_a_solid_bar = vmfiles["vm37"]
natural_frequency_of_a_piezoelectric_transducer = vmfiles["vm175"]
frequency_response_of_electrical_input_admittance = vmfiles["vm176"]
electrothermal_microactuator_analysis = vmfiles["vm223"]
piezoelectric_rectangular_strip_under_pure_bending_load = vmfiles["vm231"]
transient_response_of_a_ball_impacting_a_flexible_surface = vmfiles["vm65"]
threed_nonaxisymmetric_vibration_of_a_stretched_membrane = vmfiles["vm155"]
modal_analysis_of_a_cyclic_symmetric_annular_plate = vmfiles["vm244"]
nonaxisymmetric_vibration_of_a_stretched_circular_membrane = vmfiles["vm153"]


# be sure to add the input file directly in this directory
# This way, files can be loaded with:
# from ansys.mapdl.core import examples
# examples.wing_model
