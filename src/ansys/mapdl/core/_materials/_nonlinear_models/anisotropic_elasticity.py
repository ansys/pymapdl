from enum import Enum
from typing import List, Optional, Tuple, Union

import numpy as np

from ..common import (
    FLOAT_VALUE_REGEX,
    MATRIX_LABEL_REGEX,
    _chunk_lower_triangular_matrix,
    fill_upper_triangular_matrix,
)
from ._base import _BaseModel
from .exceptions import ModelValidationException

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ..material import Material  # noqa: F401
    from ._base import _MapdlCore  # noqa: F401


class ElasticityMode(Enum):
    """
    Determines which kind of coefficients are used in the model
    """

    # Indicates that the model coefficients have units of stiffness, for example GPa
    STIFFNESS = 1

    # Indicates that the model coefficients have units of compliance (inverse stiffness), for example GPa^-1
    COMPLIANCE = 2


class AnisotropicElasticity(_BaseModel):
    """
    Anisotropic elasticity model defines different elastic coefficients for each coordinate axis. This model can be
    used with plane and solid elements. The elastic coefficient matrix (D) is specified as one or up to six NumPy
    arrays, allowing temperature dependence to be modelled.

    The elastic coefficient matrix is defined as a 2 x n_dimensions array:

    .. math::
          \begin{matrix}
            D_{11}\\
            D_{21} & D_{22}\\
            D_{31} & D_{32} & D_{33}\\
            D_{41} & D_{42} & D_{43} & D_44}
          \end{matrix}

    This can either be specified in "stiffness" form, with units of Force/Area, or in "compliance" form with the inverse
    unit.

    Notes
    -----
    This model wraps the APDL "ELAS" and "ANEL" models in both their forms, if one temperature is provided then the
    "ELAS" model will be used, with either the "AELS" or "AELF" TBOPT, Otherwise the "ANEL" model will be written.
    """

    _n_dimensions: int
    _coefficient_type: ElasticityMode
    _coefficients: np.ndarray
    _temperature: np.ndarray

    model_codes = ("ELAS", "ANEL")

    def __init__(
        self,
        n_dimensions: int,
        coefficient_type: ElasticityMode,
        coefficients: Optional[np.ndarray] = None,
        temperature: Union[None, float, np.ndarray] = None,
    ) -> None:
        """
        Create an Anisotropic Elasticity model.

        Parameters
        ----------
        n_dimensions: int
            Number of dimensions for the model. Must be either 2 or 3.
        coefficient_type: ElasticityMode
            Whether the model uses stiffness or compliance coefficients.
        coefficients: np.ndarray
            Model coefficients, either one 2*n_dims x 2*n_dims array of model coefficients, or if the model is
            temperature dependent, up to 6 x 2*n_dims x 2*n_dims array of model coefficients at temperature.
        temperature: Union[float, np.ndarray]
            Either a single temperature at which the model is to be applied, or an array of up to six temperatures if
            the model is temperature-dependent. If multiple temperatures are defined, ensure they cover the range of
            anticipated temperatures at which the model will be applied.
        """
        if n_dimensions not in [2, 3]:
            raise ValueError("n_dimensions must be int 2 or 3")
        self._n_dimensions = n_dimensions
        self._coefficient_type = coefficient_type
        self._temperature = np.array([], dtype=float)
        self._coefficients = np.array([], dtype=float)
        if temperature is not None:
            if isinstance(temperature, (float, int)):
                self._temperature = np.array([temperature], dtype=float)
            else:
                self._temperature = temperature
        if coefficients is not None:
            self._coefficients = coefficients

    def __repr__(self) -> str:
        return f"<AnisotropicElasticity n_dimensions={self._n_dimensions}, temperature_count={len(self._temperature)}, mode={self._coefficient_type.name}>"

    @property
    def coefficients(self) -> np.ndarray:
        """
        Returns the current coefficient array for the model.
        """
        return self._coefficients

    @coefficients.setter
    def coefficients(self, value: np.ndarray):
        self._coefficients = value

    @property
    def temperature(self) -> np.ndarray:
        """
        Returns the temperature defined for the model.
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value: Union[float, np.ndarray]):
        if isinstance(value, (float, int)):
            self._temperature = np.array([value], dtype=float)
        else:
            self._temperature = value

    @classmethod
    def deserialize_model(
        cls, model_code: str, model_data: List[str]
    ) -> "AnisotropicElasticity":
        """
        Converts output from a `TBLIST` command into an `AnisotropicElasticity` object representing that model. The
        input should be a section of output referring to one model from one material.

        Parameters
        ----------
        model_code: str
            String model code, either "ELAS" or "ANEL"
        model_data: List[str]
            Lines from MAPDL output corresponding to this model for one material.

        Returns
        -------
        AnisotropicElasticity
            Wrapper for the underlying MAPDL material model

        Notes
        -----
        Depending on the type of the underlying model, the parameters of the returned `AnisotropicElasticity` model will
        vary, but this class will be returned for either "ELAS" or "ANEL" material models.
        """
        assert (
            model_code in cls.model_codes
        ), f"Invalid model_code ({model_code}) provided."
        header_row_index = 0
        for index, line in enumerate(model_data):
            if line.strip().startswith("Temps"):
                header_row_index = index
                break
        if model_code == "ANEL":
            n_dim, temps, coeffs = cls.deserialize_anel_data(
                model_data[header_row_index : header_row_index + 22]
            )
            mode = ElasticityMode.STIFFNESS
            for line in model_data[header_row_index + 23 :]:
                if line.strip().startswith("Flexibility"):
                    mode = ElasticityMode.COMPLIANCE
                    break
            return cls(n_dim, mode, coeffs, temps)

        else:
            n_dim, temp, coeffs = cls.deserialize_elas_data(
                model_data[header_row_index : header_row_index + 22]
            )
            if "STIFFNESS" in model_data[header_row_index - 2]:
                mode = ElasticityMode.STIFFNESS
            else:
                mode = ElasticityMode.COMPLIANCE
            return cls(n_dim, mode, coeffs, temp)

    @staticmethod
    def deserialize_anel_data(
        model_data: List[str],
    ) -> Tuple[int, np.ndarray, np.ndarray]:
        """
        Deserializes the first section of data returned by calling `TBLIST` with an "ANEL" model. The first row contains
        the temperatures at which the model is applied, and subsequent rows contain each coefficient value at each
        specified temperature

        Parameters
        ----------
        model_data: List[str]
            Lines from MAPDL output corresponding to the model coefficients and measured temperatures.
        """
        temp_values = [
            float(match[0]) for match in FLOAT_VALUE_REGEX.findall(model_data[0])
        ]
        matrix_data = AnisotropicElasticity.read_matrix(model_data[1:])
        coeffs = []
        for temp_index, temp_value in enumerate(temp_values):
            data_at_temp = [row[temp_index + 1] for row in matrix_data]
            if np.allclose(data_at_temp[10:], 0):
                data_at_temp = data_at_temp[0:10]
            coeffs.append(fill_upper_triangular_matrix(data_at_temp))
        if all([matrix.size == 16 for matrix in coeffs]):
            ndim = 2
        else:
            ndim = 3
        coeff_np = np.empty((len(temp_values), 2 * ndim, 2 * ndim))
        for index, matrix in enumerate(coeffs):
            coeff_np[index, 0 : 2 * ndim, 0 : 2 * ndim] = matrix
        return ndim, np.asarray(temp_values, dtype=float), coeff_np

    @staticmethod
    def deserialize_elas_data(model_data: List[str]) -> Tuple[int, float, np.ndarray]:
        """
        Deserializes the first section of data returned by calling `TBLIST` with an "ELAS" model. The first row contains
        the temperature at which the model is applied, and subsequent rows contain each coefficient value.

        Parameters
        ----------
        model_data: List[str]
            Lines from MAPDL output corresponding to the model coefficients and measured temperature.
        """
        temp_values = float(FLOAT_VALUE_REGEX.findall(model_data[0])[0][0])
        matrix_data = AnisotropicElasticity.read_matrix(model_data[1:])
        data_at_temp = [row[1] for row in matrix_data]
        if np.allclose(data_at_temp[10:], 0):
            data_at_temp = data_at_temp[0:10]
            ndim = 2
        else:
            ndim = 3
        coeffs = fill_upper_triangular_matrix(data_at_temp)
        return ndim, temp_values, coeffs

    @staticmethod
    def read_matrix(model_data: List[str]) -> List[Tuple]:
        """
        Helper method to iterate through a provided list of strings and extract, if present, a valid matrix element
        label and any subsequent floating point values.

        Parameters
        ----------
        model_data: List[str]
            Matrix coefficient section from the output of a `TBLIST` command. Any rows that do not begin with a label
            are ignored, otherwise each row is deserialized into a tuple with the string label and any associated float
            values.
        """
        values = []
        for row in model_data:
            label = MATRIX_LABEL_REGEX.search(row)
            if label:
                current_values = FLOAT_VALUE_REGEX.findall(row)
                values.append(
                    (label.groups()[0], *(float(value[0]) for value in current_values))
                )
        return values

    def write_model(self, mapdl: "_MapdlCore", material: "Material") -> None:
        """
        Writes the model to MAPDL. Performs some pre-flight verification, and writes the correct model for the provided
        values of coefficients and temperatures.

        If no temperature value was specified for the model then the current reference temperature for the material will
        be used.

        Parameters
        ----------
        mapdl: _MapdlCore
            Configured instance of PyMapdl.
        material: Material
            Material object with which this model will be associated.
        """
        is_ok, issues = self.validate_model()
        if not is_ok:
            raise ModelValidationException("\n".join(issues))

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
                tbopt = "0"
            else:
                tbopt = "1"

            # Ensure temperatures and coefficients are sorted
            sort_order = np.argsort(self._temperature)
            self._temperature = self._temperature[sort_order]
            self._coefficients = self._coefficients[sort_order, :, :]

        # Write table specification
        mapdl.tb(lab, material.material_id, ntemp, tbopt=tbopt)

        for temp_index, temp_val in enumerate(self._temperature):
            mapdl.tbtemp(temp_val)
            for chunk_index, data_chunk in enumerate(
                _chunk_lower_triangular_matrix(self._coefficients[temp_index])
            ):
                mapdl.tbdata(6 * chunk_index + 1, *data_chunk)

    def validate_model(self) -> Tuple[bool, List[str]]:
        """
        Validate some aspects of the model before attempting to write to MAPDL.

        * Validate that the number of provided temperatures match the size of the first dimension of the coefficient
          array.
        * Validate that the coefficient array is either two or three-dimensional.
        * Validate that no more than six temperature samples are provided.

        Returns
        -------
        Tuple
            First element is boolean, true if validation is successful. If false then the second element will contain a
            list of strings with more information.
        """
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
            validation_errors.append(
                "Invalid dimension of coefficients array, must be 2 or 3."
            )

        # Check that size of temperature matches 3rd dimension of coefficients
        if coef_matrix_count and coef_matrix_count != self._temperature.size:
            is_valid = False
            validation_errors.append(
                f"Inconsistent number of temperature values ({self._temperature.size}) and coefficient values ({coef_matrix_count})."
            )

        if self._temperature.size > 6:
            is_valid = False
            validation_errors.append(
                "This model supports a maximum of 6 temperature values"
            )

        return is_valid, validation_errors
