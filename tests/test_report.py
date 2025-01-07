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

"""Test report features"""

from conftest import has_dependency, requires

if has_dependency("pyvista"):
    from pyvista.plotting import system_supports_plotting

from ansys.mapdl import core as pymapdl


@requires("pyvista")
def test_report():
    report = pymapdl.Report(
        additional=["matplotlib", "pyvista", "pyiges", "tqdm"],
        gpu=system_supports_plotting(),
    )
    assert "PyAnsys Software and Environment Report" in str(report)

    # Check that when adding additional (repeated) packages, they appear only once
    assert str(report).count("pyvista") == 1


def test_plain_report():
    from ansys.mapdl.core.report import Plain_Report

    core = ["numpy", "ansys.mapdl.reader"]
    optional = ["pyvista", "tqdm"]
    additional = ["scipy", "ger"]

    report = Plain_Report(core=core, optional=optional, additional=additional, gpu=True)
    rep_str = report.__repr__()

    for each in core + optional + additional:
        assert each in rep_str

    # There should be only one package not found ("ger")
    assert "Package not found" in rep_str
    not_found_packages = 1

    # Plus the not additional packages
    if not has_dependency("pyvista"):
        not_found_packages += 1
    if not has_dependency("tqdm"):
        not_found_packages += 1
    if not has_dependency("ansys.mapdl.reader"):
        not_found_packages += 1
    if not has_dependency("scipy"):
        not_found_packages += 1
    if not has_dependency("pexpect"):
        not_found_packages += 1

    _rep_str = rep_str.replace("Package not found", "", not_found_packages)
    assert "Package not found" not in _rep_str

    assert "\n" in rep_str
    assert len(rep_str.splitlines()) > 3

    assert "Core packages" in rep_str
    assert "Optional packages" in rep_str
    assert "Additional packages" in rep_str

    # Plain report should not represent GPU details evenif asked for
    assert "GPU Details" not in rep_str


def test_plain_report_no_options():
    from ansys.mapdl.core.report import Plain_Report

    core = ["numpy", "ansys.mapdl.reader"]

    report = Plain_Report(core=core)
    rep_str = report.__repr__()

    for each in core:
        assert each in rep_str

    assert "\n" in rep_str
    assert len(rep_str.splitlines()) > 3

    assert "Core packages" in rep_str
    assert "Optional packages" not in rep_str
    assert "Additional packages" not in rep_str
