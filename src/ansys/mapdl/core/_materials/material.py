from typing import Dict, Optional, Set

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
    _SCALAR_PROPERTIES: Set[PropertyCode] = {PropertyCode.REFT}

    def __init__(
        self,
        material_id: int = None,
        properties: Dict[PropertyCode, model_type] = None,
        nonlinear_models: Dict[str, _BaseModel] = None,
        reference_temperature: float = 0.0,
    ):
        """
        Create a new instance of a Material. Optionally specify a material ID, or other properties.

        Parameters
        ----------
        material_id: int
            The ID to be associated with this material. If it already exists within MAPDL then writing this material
            will overwrite the existing material.
        properties: Union[MaterialPropertyDict, Dict]
            Dictionary of material properties. Linear material properties are specified with the `PropertyCode` enum and
            either a float value or an np.ndarray of temperatures and property values. Nonlinear material models are
            specified with their model code (from the TB command), and the model object.
        reference_temperature: float
            Reference temperature for this material, affects thermal expansion and some non-linear models. Default 0.0
        """
        self._properties = {}
        self._nonlinear_models = {}
        self._id = material_id
        self._properties[PropertyCode.REFT] = reference_temperature
        if properties is not None:
            for k, v in properties.items():
                self.set_property(k, v)
        self._reference_temperature = self._properties[PropertyCode.REFT]
        if nonlinear_models is not None:
            for k, v in nonlinear_models.items():
                self.set_model(k, v)

    @property
    def material_id(self) -> Optional[int]:
        """
        Return the material ID
        """
        return self._id

    @material_id.setter
    def material_id(self, value: int):
        self._id = value

    def get_properties(
        self,
    ) -> "Dict[PropertyCode, model_type]":
        """
        Return the currently assigned linear material properties.
        """
        return self._properties

    def get_property(self, property_code: PropertyCode) -> model_type:
        """
        Return the assigned value of the specified linear material property.
        """
        return self._properties[property_code]

    def remove_property(self, property_code: PropertyCode) -> None:
        """
        Clears a property value.
        """
        if property_code == PropertyCode.REFT:
            raise KeyError("Cannot remove reference temperature property.")
        self._properties.pop(property_code)

    def set_property(self, property_code: PropertyCode, value: model_type) -> None:
        """
        Set a linear material property. Either provide a single float, for properties that are treated as Isothermal,
        or provide an array of floats for properties that are to be treated as temperature dependent. For
        temperature-dependent properties provide a 2*N array where the first column specifies temperatures, and the
        second column provides the property values.
        """
        assert isinstance(
            value, (float, np.ndarray)
        ), "Linear material properties must be either floats or numpy arrays."
        if property_code in self._SCALAR_PROPERTIES:
            assert isinstance(
                value, float
            ), f"Property f{property_code} must be a float."
        self._properties[property_code] = value

    def get_models(self) -> "Dict[str, _BaseModel]":
        """
        Return the currently assigned nonlinear material models.
        """
        return self._nonlinear_models

    def get_model(self, model_code: str) -> "_BaseModel":
        """
        Return the nonlinear material model with the specified model code.
        """
        return self._nonlinear_models[model_code]

    def set_model(self, model_type: str, value: _BaseModel) -> None:
        """
        Set a nonlinear material model.
        """
        assert isinstance(
            value, _BaseModel
        ), "Nonlinear models must inherit from '_BaseModel'"
        self._nonlinear_models[model_type] = value

    def remove_model(self, model_code: str) -> None:
        """
        Clears a nonlinear material model.
        """
        self._nonlinear_models.pop(model_code)

    @property
    def reference_temperature(self) -> float:
        """
        Return the current reference temperature for the model.
        """
        return float(self._properties[PropertyCode.REFT])

    @reference_temperature.setter
    def reference_temperature(self, value: float) -> None:
        self._properties[PropertyCode.REFT] = value
