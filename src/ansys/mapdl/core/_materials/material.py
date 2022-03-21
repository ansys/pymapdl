from typing import Dict, Optional, Union

import numpy as np

from ._nonlinear_models import _BaseModel
from .common import model_type
from .property_codes import PropertyCode


class Material:
    """
    Wrapper class for a MAPDL material. Associates a material_id with one or more properties and nonlinear material
    models.

    If created directly then the material must be written to MAPDL before it can be used. If returned by the
    MaterialManager then this class represents the state of the material at that point.
    """

    _properties: Dict[PropertyCode, model_type]
    _nonlinear_models: Dict[str, _BaseModel]
    _id: Optional[int]
    _reference_temperature: float

    def __init__(
        self,
        material_id: int = None,
        properties: Union[Dict[PropertyCode, model_type], Dict[str, _BaseModel]] = None,
        reference_temperature: float = 0.0,
    ):
        """
        Create a new instance of a Material. Optionally specify a material ID, or other properties.

        Parameters
        ----------
        material_id: int
            The ID to be associated with this material. If it already exists within MAPDL then writing this material
            will overwrite the existing material.
        properties: Union[Dict[PropertyCode, model_type], Dict[str, _BaseModel]]
            Dictionary of material properties. Linear material properties are specified with the `PropertyCode` enum and
            either a float value or an np.ndarray of temperatures and property values. Nonlinear material models are
            specified with their model code (from the TB command), and the model object.
        reference_temperature: float
            Reference temperature for this material, affects thermal expansion and some non-linear models. Default 0.0
        """
        self._properties = {}
        self._id = material_id
        if properties is not None:
            self.properties = properties
        self._properties[PropertyCode.REFT] = reference_temperature
        self._reference_temperature = reference_temperature

    @property
    def material_id(self) -> Optional[int]:
        """
        Return the material ID
        """
        return self._id

    @material_id.setter
    def material_id(self, value: int):
        self._id = value

    @property
    def properties(
        self,
    ) -> Union[Dict[PropertyCode, model_type], Dict[str, _BaseModel]]:
        """
        Return the currently assigned linear properties and nonlinear models.
        """
        return {**self._properties, **self._nonlinear_models}  # type: ignore

    @properties.setter
    def properties(
        self, properties: Union[Dict[PropertyCode, model_type], Dict[str, _BaseModel]]
    ) -> None:
        for k, v in properties.items():
            if isinstance(k, str):
                assert isinstance(
                    v, _BaseModel
                ), "Nonlinear models must inherit from '_BaseModel', linear models should be set with the 'PropertyCode' enum."
                self._nonlinear_models[k] = v
            else:
                assert isinstance(
                    v, (float, np.ndarray)
                ), "Linear material properties must be either floats or numpy arrays."
                self._properties[k] = v

    @property
    def reference_temperature(self) -> float:
        """
        Return the current reference temperature for the model.
        """
        if PropertyCode.REFT in self._properties:
            return float(self._properties[PropertyCode.REFT])
        else:
            self._properties[PropertyCode.REFT] = self._reference_temperature
            return self._reference_temperature

    @reference_temperature.setter
    def reference_temperature(self, value: float) -> None:
        self._properties[PropertyCode.REFT] = value
