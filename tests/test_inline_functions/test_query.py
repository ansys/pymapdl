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

from ansys.mapdl.core.errors import MapdlCommandIgnoredError, MapdlRuntimeError
from conftest import TestClass, requires


class TestParseParameter:
    @pytest.mark.parametrize(
        "values",
        [
            ("PARAMETER test = 4", 4.0),
            ("PARAMETER=4", 4.0),
            ("PARAMETER WARNING = 4", 4.0),
            ("PARAMETER = _=4", 4.0),
            ("WARNING = PARAMETER = 4", 4.0),
            ("PARAMETER = .4", 0.4),
        ],
    )
    def test_parse_float(self, values, query):
        input_, output = values
        if "WARNING" in values[0]:
            with pytest.warns(UserWarning):
                assert query._parse_parameter_float_response(input_) == output
        else:
            assert query._parse_parameter_float_response(input_) == output

    @pytest.mark.parametrize(
        "values",
        [
            ("PARAMETER test = 4", 4),
            ("PARAMETER=4", 4),
            ("PARAMETER WARNING = 4", 4),
            ("PARAMETER = _=4", 4),
            ("WARNING = PARAMETER = 4", 4),
            ("PARAMETER = .4", 0),
        ],
    )
    def test_parse_int(self, values, query):
        input_, output = values
        if "WARNING" in values[0]:
            with pytest.warns(UserWarning):
                assert query._parse_parameter_integer_response(input_) == output
        else:
            assert query._parse_parameter_integer_response(input_) == output

    def test_parse_float_type_warning(self, query):
        input_ = "WARNING PARAMETER = 4"
        with pytest.warns(UserWarning):
            query._parse_parameter_float_response(input_)

    def test_parse_int_type_warning(self, query):
        input_ = "WARNING PARAMETER = 4"
        with pytest.warns(UserWarning):
            query._parse_parameter_integer_response(input_)

    @pytest.mark.parametrize(
        "value", ["parameter test = 4", "PARAMETER 4", "WARNING = 4", ""]
    )
    def test_parse_float_type_error(self, value, query):
        input_ = value
        with pytest.raises(TypeError):
            query._parse_parameter_float_response(input_)

    @pytest.mark.parametrize(
        "value", ["parameter test = 4", "PARAMETER 4", "WARNING = 4", ""]
    )
    def test_parse_int_type_error(self, value, query):
        input_ = value
        with pytest.raises(TypeError):
            query._parse_parameter_integer_response(input_)


class TestRunQuery(TestClass):

    @pytest.fixture(scope="class")
    def line_geometry(self, mapdl):
        k0 = mapdl.k(1, 0, 0, 0)
        k1 = mapdl.k(2, 1, 2, 2)
        l0 = mapdl.l(k0, k1)
        q = mapdl.queries
        return q, [k0, k1], l0

    @pytest.mark.parametrize("command", [("KX(1)", float), ("KP(1,1,1)", int)])
    def test_run_query_returned_type(self, line_geometry, command):
        q, kps, l0 = line_geometry
        cmd, type_ = command
        integer = False if type_ == float else True
        v = q._run_query(cmd, integer=integer)
        assert isinstance(v, type_)

    def test_interactive_mode_error(self, mapdl, line_geometry):
        q, _, _ = line_geometry
        with pytest.raises((MapdlRuntimeError, MapdlCommandIgnoredError)):
            with mapdl.non_interactive:
                q.kx(1)

    @requires("grpc")  # only works in gRPC mode
    def test_nopr_mode(self, mapdl, line_geometry):
        try:
            # enter no printout mode
            mapdl._run("/NOPR", mute=True)
            assert mapdl.prep7() is None

            # verify that queries still work
            q, kps, l0 = line_geometry
            assert q.kx(2) == 1.0
        finally:
            # always return printing
            mapdl._run("/GOPR", mute=True)
