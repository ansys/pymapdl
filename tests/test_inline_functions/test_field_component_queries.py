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

import pytest

from conftest import TestClass


class TestFieldComponentValueGetter(TestClass):

    # The tests change the mesh so this fixture must be function scoped.
    @pytest.fixture(scope="class")
    def box_with_fields(self, mapdl):
        mapdl.mp("kxx", 1, 45)
        mapdl.mp("ex", 1, 2e10)
        mapdl.mp("perx", 1, 1)
        mapdl.mp("murx", 1, 1)
        if mapdl.version >= 25.1:
            mapdl.tb("pm", 1, "", "", "perm")
            mapdl.tbdata("", 0)

        mapdl.et(1, "SOLID70")
        mapdl.et(2, "CPT215")
        mapdl.keyopt(2, 12, 1)  # Activating PRES DOF
        mapdl.et(3, "SOLID122")
        mapdl.et(4, "SOLID96")
        mapdl.block(0, 1, 0, 1, 0, 1)
        mapdl.esize(0.5)

        mapdl.save("box_with_fields")

    @staticmethod
    @pytest.fixture(scope="function")
    def resume(mapdl, box_with_fields):
        mapdl.prep7()
        mapdl.resume("box_with_fields")
        mapdl.prep7()

    def test_temp(self, mapdl, resume):
        mapdl.type(1)
        mapdl.vmesh(1)
        mapdl.d("all", "temp", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        temp_value = mapdl.queries.temp(1)
        assert temp_value == 5.0

    def test_pressure(self, mapdl, resume):
        mapdl.type(2)
        mapdl.vmesh(1)
        mapdl.d("all", "pres", 5.0)
        mapdl.d("all", "ux", 0.0, lab2="uy", lab3="uz")
        mapdl.slashsolu()
        mapdl.solve()
        pres_value = mapdl.queries.pres(1)
        assert pres_value == 5.0

    def test_volt(self, mapdl, resume):
        mapdl.type(3)
        mapdl.vmesh(1)
        mapdl.d("all", "volt", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        volt_value = mapdl.queries.volt(1)
        assert volt_value == 5.0

    def test_mag(self, mapdl, resume):
        mapdl.type(4)
        mapdl.vmesh(1)
        mapdl.d("all", "mag", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        mag_value = mapdl.queries.mag(1)
        assert mag_value == 5.0
