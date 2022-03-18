from typing import Union, List, Tuple, Iterable
from numbers import Number

import numpy as np
from enum import Enum

from ..common import _chunk_lower_triangular_matrix, FLOAT_VALUE_REGEX, MATRIX_LABEL_REGEX, fill_lower_triangular_matrix
from ._base import _BaseModel
from .exceptions import ModelValidationException

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ..material import Material
    from ._base import _MapdlCore


class ElasticityMode(Enum):
    STIFFNESS = 1
    COMPLIANCE = 2


class AnisotropicElasticity(_BaseModel):
    _n_dimensions: int
    _coefficient_type: ElasticityMode
    _coefficients: np.ndarray
    _temperature: np.ndarray

    model_codes = ("ELAS", "ANEL")

    def __init__(self, n_dimensions: int, coefficient_type: ElasticityMode, coefficients: np.ndarray = None,
                 temperature: Union[float, np.ndarray] = None) -> None:
        if n_dimensions not in [2, 3]:
            raise ValueError("n_dimensions must be int 2 or 3")
        self._n_dimensions = n_dimensions
        self._coefficient_type = coefficient_type
        if temperature is not None:
            if isinstance(temperature, Number):
                self._temperature = np.array([temperature], dtype=float)
            else:
                self._temperature = temperature
        if coefficients is not None:
            self._coefficients = coefficients

    def __repr__(self) -> str:
        return f"<AnisotropicElasticity n_dimensions={self._n_dimensions}, temperature_count={len(self._temperature)}, mode={self._coefficient_type.name}>"

    @property
    def coefficients(self) -> np.ndarray:
        return self._coefficients

    @coefficients.setter
    def coefficients(self, value: np.array):
        self._coefficients = value

    @property
    def temperature(self) -> np.ndarray:
        return self._temperature

    @temperature.setter
    def temperature(self, value: Union[float, np.ndarray]):
        if isinstance(value, Number):
            self._temperature = np.array([value], dtype=float)
        else:
            self._temperature = value

    @classmethod
    def deserialize_model(cls, model_code: str, model_data: List[str]) -> "AnisotropicElasticity":
        assert model_code in cls.model_codes, "Invalid model_code provided. How?"
        header_row_index = None
        for index, line in enumerate(model_data):
            if line.strip().startswith("Temps"):
                header_row_index = index
                break
        if model_code == "ANEL":
            n_dim, temps, coeffs = cls.deserialize_anel_data(model_data[header_row_index:header_row_index + 22])
            mode = ElasticityMode.STIFFNESS
            for line in model_data[header_row_index + 23:]:
                if line.strip().startswith("Flexibility"):
                    mode = ElasticityMode.COMPLIANCE
                    break
            return cls(n_dim, mode, coeffs, temps)

        else:
            n_dim, temp, coeffs = cls.deserialize_elas_data(model_data[header_row_index:header_row_index + 22])
            if "STIFFNESS" in model_data[header_row_index - 2]:
                mode = ElasticityMode.STIFFNESS
            else:
                mode = ElasticityMode.COMPLIANCE
            return cls(n_dim, mode, coeffs, temp)

    @staticmethod
    def deserialize_anel_data(model_data: List[str]) -> Tuple[int, np.ndarray, np.ndarray]:
        temp_values = [float(match[0]) for match in FLOAT_VALUE_REGEX.findall(model_data[0])]
        matrix_data = AnisotropicElasticity.read_matrix(model_data[1:])
        coeffs = []
        for temp_index, temp_value in enumerate(temp_values):
            data_at_temp = [row[temp_index + 1] for row in matrix_data]
            if np.allclose(data_at_temp[10:], 0):
                data_at_temp = data_at_temp[0:10]
            coeffs.append(fill_lower_triangular_matrix(data_at_temp))
        if all([matrix.size == 16 for matrix in coeffs]):
            ndim = 2
        else:
            ndim = 3
        coeff_np = np.empty((len(temp_values), 2 * ndim, 2 * ndim))
        for index, matrix in enumerate(coeffs):
            coeff_np[index, 0: 2 * ndim, 0: 2 * ndim] = matrix
        return ndim, np.asarray(temp_values, dtype=float), coeff_np

    @staticmethod
    def deserialize_elas_data(model_data: List[str]) -> Tuple[int, float, np.ndarray]:
        temp_values = float(FLOAT_VALUE_REGEX.findall(model_data[0])[0][0])
        matrix_data = AnisotropicElasticity.read_matrix(model_data[1:])
        data_at_temp = [row[1] for row in matrix_data]
        if np.allclose(data_at_temp[10:], 0):
            data_at_temp = data_at_temp[0:10]
            ndim = 2
        else:
            ndim = 3
        coeffs = fill_lower_triangular_matrix(data_at_temp)
        return ndim, temp_values, coeffs

    @staticmethod
    def read_matrix(model_data: List[str]) -> List[Tuple]:
        values = []
        for row in model_data:
            label = MATRIX_LABEL_REGEX.search(row)
            if label:
                current_values = FLOAT_VALUE_REGEX.findall(row)
                values.append((label.groups()[0], *(float(value[0]) for value in current_values)))
        return values

    def write_model(self, mapdl: '_MapdlCore', material: 'Material') -> None:
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException('\n'.join(issues))

        if self._temperature is None:
            self._temperature = np.array(material.reference_temperature, dtype=float)

        if self._temperature.size == 1:
            # Write ELASTIC model
            ntemp = 1
            lab = "ELASTIC"
            if self._coefficient_type == ElasticityMode.STIFFNESS:
                tbopt = "AELS"
            else:
                tbopt = "AELF"
            self._coefficients = np.expand_dims(self._coefficients, 0)
        else:
            # Write ANEL model
            ntemp = self._temperature.size
            lab = "ANEL"
            if self._coefficient_type == ElasticityMode.STIFFNESS:
                tbopt = 0
            else:
                tbopt = 1

            # Ensure temperatures and coefficients are sorted
            sort_order = np.argsort(self._temperature)
            self._temperature = self._temperature[sort_order]
            self._coefficients = self._coefficients[sort_order, :, :]

        # Write table specification
        mapdl.tb(lab, material.material_id, ntemp, tbopt=tbopt)

        for temp_index, temp_val in enumerate(self._temperature):
            mapdl.tbtemp(temp_val)
            for chunk_index, data_chunk in enumerate(_chunk_lower_triangular_matrix(self._coefficients[temp_index])):
                mapdl.tbdata(6 * chunk_index + 1, *data_chunk)

    def validate_model(self) -> Tuple[bool, List[str]]:
        # Check that matrix is square and of size (2*d, 2*d)
        coefficient_shape = self._coefficients.shape
        coef_matrix_count = None
        validation_errors = []
        is_valid = True

        if len(coefficient_shape) == 2:
            coef_matrix_count = 1
        elif len(coefficient_shape) == 3:
            coef_matrix_count = coefficient_shape[0]
        else:
            is_valid = False
            validation_errors.append("Invalid dimension of coefficients array, must be 2 or 3.")

        # Check that size of temperature matches 3rd dimension of coefficients
        if coef_matrix_count and coef_matrix_count != self._temperature.size:
            is_valid = False
            validation_errors.append(
                f"Inconsistent number of temperature values ({self._temperature.size}) and coefficient values ({coef_matrix_count}).")

        if self._temperature.size > 6:
            is_valid = False
            validation_errors.append("This model supports a maximum of 6 temperature values")

        return is_valid, validation_errors
