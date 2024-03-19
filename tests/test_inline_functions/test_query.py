import pytest

from ansys.mapdl.core.errors import MapdlCommandIgnoredError, MapdlRuntimeError


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


class TestRunQuery:
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

    @pytest.mark.skip_grpc  # only works in gRPC mode
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
