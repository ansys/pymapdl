from collections import Iterable
from typing import Callable, List

import pytest
import numpy as np
import numpy.testing

from ansys.mapdl.core._materials.common import _chunk_data, _chunk_lower_triangular_matrix, fill_upper_triangular_matrix
from ansys.mapdl.core._materials.material import Material
from ansys.mapdl.core._materials.property_codes import PropertyCode


class TestCommonFunctions:
    @pytest.mark.parametrize(
        ("iterable_input", "expected_output"),
        [
            ([1.], [[1.]]),
            ([1., 2., 3., 4., 5., 6.], [[1., 2., 3., 4., 5., 6.]]),
            ([1., 2., 3., 4., 5., 6., 7.], [[1., 2., 3., 4., 5., 6.], [7.]])
        ]
    )
    @pytest.mark.parametrize("input_type", (list, tuple))
    def test_chunk_data(self, iterable_input: Iterable[float], expected_output: Iterable[Iterable[float]], input_type: Callable):
        iterable_input = input_type(iterable_input)
        chunked_data = _chunk_data(iterable_input)
        for chunk in zip(chunked_data, expected_output):
            assert chunk[0] == chunk[1]

    @pytest.mark.parametrize(
        ("array_input", "expected_output"),
        [
            ([[1.]], [[1.]]),
            ([[1., 2.], [3., 4.]], [[1., 3., 4.]]),
            ([[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]], [[1., 4., 5., 7., 8., 9.]]),
            ([[1., 2., 3., 4.], [5., 6., 7., 8.], [9., 10., 11., 12.], [13., 14., 15., 16.]], [[1., 5., 6., 9., 10., 11.], [13., 14., 15., 16.]])
        ]
    )
    def test_chunk_lower_triangular_matrix(self, array_input: Iterable[Iterable[float]], expected_output: Iterable[Iterable[float]]):
        np_input = np.asarray(array_input, dtype=float)
        chunked_array = _chunk_lower_triangular_matrix(np_input)
        for chunk in zip(chunked_array, expected_output):
            assert chunk[0] == chunk[1]

    def test_chunk_lower_triangular_throws_with_1_dimension(self):
        input_array = np.array([1.])
        with pytest.raises(ValueError):
            _ = _chunk_lower_triangular_matrix(input_array)

    def test_chunk_lower_triangular_throws_with_3_dimensions(self):
        input_array = np.array([[[1.]]])
        with pytest.raises(ValueError):
            _ = _chunk_lower_triangular_matrix(input_array)

    @pytest.mark.parametrize(
        "array_input",
        [
            [[1., 2.], [3., 4.], [5., 6.]],
            [[1., 2., 3.], [4., 5., 6.]]
        ]
    )
    def test_chunk_lower_triangular_throws_with_non_square_input(self, array_input: Iterable[Iterable[float]]):
        np_input = np.asarray(array_input, dtype=float)
        with pytest.raises(ValueError):
            _ = _chunk_lower_triangular_matrix(np_input)

    @pytest.mark.parametrize(
        ("array_input", "expected_output"),
        [
            ([1.], [[1.]]),
            ([1., 3., 4.], [[1., 3.], [3., 4.]]),
            ([1., 2., 3., 5., 6., 9.], [[1., 2., 3.], [2., 5., 6.], [3., 6., 9.]]),
            ([1., 2., 3., 4., 6., 7., 8., 11., 12., 16.], [[1., 2., 3., 4.], [2., 6., 7., 8.], [3., 7., 11., 12.], [4., 8., 12., 16.]])
        ]
    )
    def test_fill_upper_triangular_matrix(self, array_input: List[float], expected_output: Iterable[Iterable[float]]):
        filled_array = fill_upper_triangular_matrix(array_input)
        expected_output = np.asarray(expected_output, dtype=float)
        numpy.testing.assert_array_equal(expected_output, filled_array)

    def test_invalid_input_length(self):
        input_data = [1., 2., 3., 4.]
        with pytest.raises(ValueError):
            _ = fill_upper_triangular_matrix(input_data)


class TestMaterial:
    def test_create_empty_material(self):
        id_ = 3
        material = Material(material_id=id_)
        assert material.material_id == id_

    def test_create_material_with_simple_properties(self):
        id_ = 3
        properties = {
            PropertyCode.DENS: 3000.,
            PropertyCode.EX: 6_000_000.
        }
        material = Material(material_id=id_, properties=properties)
        assert material.material_id == id_
        for k, v in properties.items():
            assert material.properties[k] == properties[k]

    def test_create_material_with_functional_properties(self):
        id_ = 3
        properties = {
            PropertyCode.DENS: np.asarray([[0.0, 4000.], [100., 3700.], [200., 3400.]], dtype=float),
            PropertyCode.EX: np.asarray([[0.0, 6e6], [100., 5.5e6], [200., 5e6]], dtype=float),
        }
        material = Material(material_id=id_, properties=properties)
        assert material.material_id == id_
        for k, v in properties.items():
            np.testing.assert_array_equal(material.properties[k], properties[k])

    def test_create_material_with_reference_temperature(self):
        id_ = 5
        ref_temperature = 25.
        material = Material(material_id=id_, reference_temperature=ref_temperature)
        assert material.material_id == id_
        assert material.reference_temperature == ref_temperature
        assert material.properties[PropertyCode.REFT] == ref_temperature

    def test_assigning_array_reference_temperature_throws(self):
        material = Material(material_id=10)
        temperature_array = np.asarray([[0.0, 0.0], [100., 100.], [200., 200.]], dtype=float)
        with pytest.raises(AssertionError):
            material.properties[PropertyCode.REFT] = temperature_array

    @pytest.mark.parametrize("invalid_input", ["foo", b"110", 12])
    def test_assigning_invalid_property_type_throws(self, invalid_input):
        material = Material(material_id=10)
        property = PropertyCode.DENS
        with pytest.raises(AssertionError):
            material.properties[property] = invalid_input