import pytest


class TestParseParameter:
    @pytest.mark.parametrize('values', [('parameter test = 4', 4.),
                                        ('= 4', 4.),
                                        ('_ = 4', 4.),
                                        ('_=4', 4.),
                                        ('=4', 4.),
                                        ('_ = .4', .4)])
    def test_parse_float(self, values, box_geometry):
        q, kps, areas, nodes = box_geometry
        input_, output = values
        assert q._parse_parameter_float_response(input_) == output

    @pytest.mark.parametrize('values', [('parameter test = 4', 4),
                                        ('= 4', 4),
                                        ('_ = 4', 4),
                                        ('_=4', 4),
                                        ('=4', 4),
                                        ('_ = .4', 0)])
    def test_parse_int(self, values, box_geometry):
        q, kps, areas, nodes = box_geometry
        input_, output = values
        assert q._parse_parameter_integer_response(input_) == output

    @pytest.mark.parametrize('input_', ['parameter test 4',
                                        ''])
    def test_parse_float_failure(self, input_, box_geometry):
        q, kps, areas, nodes = box_geometry
        with pytest.raises(TypeError):
            q._parse_parameter_float_response(input_)

    @pytest.mark.parametrize('input_', ['parameter test 4',
                                        ''])
    def test_parse_int_failure(self, input_, box_geometry):
        q, kps, areas, nodes = box_geometry
        with pytest.raises(TypeError):
            q._parse_parameter_integer_response(input_)
