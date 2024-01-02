# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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


class TestFieldComponentValueGetter:
    def test_temp(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(1)
        mapdl.vmesh(1)
        mapdl.d("all", "temp", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        temp_value = mapdl.queries.temp(1)
        assert temp_value == 5.0

    def test_pressure(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(2)
        mapdl.vmesh(1)
        mapdl.d("all", "pres", 5.0)
        mapdl.d("all", "ux", 0.0, lab2="uy", lab3="uz")
        mapdl.slashsolu()
        mapdl.solve()
        pres_value = mapdl.queries.pres(1)
        assert pres_value == 5.0

    def test_volt(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(3)
        mapdl.vmesh(1)
        mapdl.d("all", "volt", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        volt_value = mapdl.queries.volt(1)
        assert volt_value == 5.0

    def test_mag(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(4)
        mapdl.vmesh(1)
        mapdl.d("all", "mag", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        mag_value = mapdl.queries.mag(1)
        assert mag_value == 5.0
