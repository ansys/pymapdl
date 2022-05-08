import os
from collections import Iterable
from typing import Callable, List, Tuple

import pytest
import numpy as np
import numpy.testing

from ansys.mapdl.core._materials._nonlinear_models import _BaseModel
from ansys.mapdl.core._materials.common import _chunk_data, _chunk_lower_triangular_matrix, fill_upper_triangular_matrix
from ansys.mapdl.core._materials.material import Material
from ansys.mapdl.core._materials.property_codes import PropertyCode
from ansys.mapdl.core._materials.tbdata_parser import TableDataParser
from ansys.mapdl.core.mapdl import _MapdlCore

HEADER_LINES = [
    "Header",
    "Some kind of header is present, need to actually get some output",
    "-----------------------------",
]

ANEL_LINES = [
    "(ANEL) Table For Material 12",
    "1 DATA ANEL",
    "2 DATA ANEL",
    "3 DATA ANEL",
    "",
]

CHAB_LINES = [
    "(CHAB) Table For Material 12",
    "1 DATA CHAB",
    "2 DATA CHAB",
    "3 DATA CHAB",
    "4 DATA CHAB",
    "",
]

TNM_LINES = [
    "(TNM) Table For Material 11",
    "1 DATA TNM",
    "2 DATA TNM",
    "3 DATA TNM",
]

VALID_TABLE = os.linesep.join([*HEADER_LINES, *ANEL_LINES, *CHAB_LINES, *TNM_LINES])


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


def make_material_with_properties() -> Material:
    id_ = 3
    properties = {
        PropertyCode.DENS: 3000.,
        PropertyCode.EX: 6_000_000.,
        PropertyCode.REFT: 23.0
    }
    return Material(material_id=id_, properties=properties)


class TestMaterial:
    def test_create_empty_material(self):
        id_ = 3
        material = Material(material_id=id_)
        assert material.material_id == id_

    def test_default_reference_temperature(self):
        id_ = 1
        material = Material(material_id=id_)
        assert material.reference_temperature == pytest.approx(0.0)

    def test_setting_material_id_works(self):
        material = Material(material_id=1)
        material.material_id = 2
        assert material.material_id == 2

    def test_create_material_with_simple_properties(self):
        id_ = 3
        properties = {
            PropertyCode.DENS: 3000.,
            PropertyCode.EX: 6_000_000.,
            PropertyCode.REFT: 23.0
        }
        material = Material(material_id=id_, properties=properties)
        assert material.material_id == id_
        assigned_properties = material.get_properties()
        assert len(assigned_properties) == 3
        for k, v in properties.items():
            assert assigned_properties[k] == pytest.approx(properties[k])

    def test_removing_property_removes_property(self):
        material = make_material_with_properties()
        assert len(material.get_properties()) == 3
        material.remove_property(PropertyCode.DENS)
        assert len(material.get_properties()) == 2

    def test_removing_invalid_property_throws(self):
        material = make_material_with_properties()
        with pytest.raises(KeyError):
            material.remove_property("TEST")

    def test_removing_reference_temperature_throws(self):
        material = make_material_with_properties()
        with pytest.raises(KeyError):
            material.remove_property(PropertyCode.REFT)

    def test_create_material_with_functional_properties(self):
        id_ = 3
        properties = {
            PropertyCode.DENS: np.asarray([[0.0, 4000.], [100., 3700.], [200., 3400.]], dtype=float),
            PropertyCode.EX: np.asarray([[0.0, 6e6], [100., 5.5e6], [200., 5e6]], dtype=float),
        }
        material = Material(material_id=id_, properties=properties)
        assert material.material_id == id_
        for k, v in properties.items():
            np.testing.assert_array_equal(material.get_property(k), properties[k])

    def test_create_material_with_reference_temperature(self):
        id_ = 5
        ref_temperature = 25.
        material = Material(material_id=id_, reference_temperature=ref_temperature)
        assert material.material_id == id_
        assert material.reference_temperature == pytest.approx(ref_temperature)
        assert material.get_property(PropertyCode.REFT) == pytest.approx(ref_temperature)

    def test_assigning_array_reference_temperature_throws(self):
        material = Material(material_id=10)
        temperature_array = np.asarray([[0.0, 0.0], [100., 100.], [200., 200.]], dtype=float)
        with pytest.raises(AssertionError):
            material.set_property(PropertyCode.REFT, temperature_array)

    def test_assigning_reference_temperature(self):
        material = Material(material_id=10)
        reference_temperature = 23.0
        material.reference_temperature = reference_temperature
        assert material.get_property(PropertyCode.REFT) == pytest.approx(reference_temperature)

    @pytest.mark.parametrize("invalid_input", ["foo", b"110", 12])
    def test_assigning_invalid_property_type_throws(self, invalid_input):
        material = Material(material_id=10)
        property_code = PropertyCode.DENS
        with pytest.raises(AssertionError):
            material.set_property(property_code, invalid_input)

    def test_create_material_with_nonlinear_model(self):
        material = Material(material_id=1, nonlinear_models={"TEST": TestNonlinearModel()})
        assert "TEST" in material.get_models()
        model = material.get_model("TEST")
        assert isinstance(model, TestNonlinearModel)

    def test_removing_nonlinear_model_removes_model(self):
        material = Material(material_id=1, nonlinear_models={"TEST": TestNonlinearModel()})
        assert len(material.get_models()) == 1
        material.remove_model("TEST")
        assert len(material.get_models()) == 0

    def test_removing_nonexistent_model_throws(self):
        material = Material(material_id=1, nonlinear_models={"TEST": TestNonlinearModel()})
        assert len(material.get_models()) == 1
        with pytest.raises(KeyError):
            material.remove_model("OTHER")


class TestNonlinearModel(_BaseModel):
    def write_model(self, mapdl: "_MapdlCore", material: "Material") -> None:
        return None

    def validate_model(self) -> "Tuple[bool, List[str]]":
        return True, []

    @classmethod
    def deserialize_model(cls, model_code: str, model_data: List[str]) -> "_BaseModel":
        return TestNonlinearModel()


class TestTableDataParser:
    def test_valid_table_with_material_id(self):
        parsed_data = TableDataParser._get_tb_sections_with_id(VALID_TABLE, 12)
        assert len(parsed_data) == 2
        assert "ANEL" in parsed_data
        anel_data = parsed_data["ANEL"]
        assert len(anel_data) == 5
        assert anel_data == ANEL_LINES
        assert "CHAB" in parsed_data
        chab_data = parsed_data["CHAB"]
        assert len(chab_data) == 6
        assert chab_data == CHAB_LINES

    def test_valid_table_with_missing_id(self):
        with pytest.raises(IndexError):
            TableDataParser._get_tb_sections_with_id(VALID_TABLE, 10)
