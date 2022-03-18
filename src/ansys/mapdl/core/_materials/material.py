from typing import Dict, Union

from .property_codes import PropertyCode
from .common import model_type

TYPE_CHECKING = False
if TYPE_CHECKING:
    from _nonlinear_models import _BaseModel


class Material:
    _properties: Dict[PropertyCode, model_type]
    _nonlinear_models: 'Dict[str, _BaseModel]'
    _id: int
    _reference_temperature: float

    def __init__(self, material_id: int = None, properties: Union[Dict[PropertyCode, model_type], Dict[str, '_BaseModel']] = None, reference_temperature: float = 0.):
        self._properties = {}
        self._id = material_id
        if properties is not None:
            self.properties = properties
        self._properties[PropertyCode.REFT] = reference_temperature
        self._reference_temperature = reference_temperature

    @property
    def material_id(self) -> int:
        return self._id

    @material_id.setter
    def material_id(self, value: int):
        self._id = value

    @property
    def properties(self) -> Union[Dict[PropertyCode, model_type], Dict[str, '_BaseModel']]:
        return {**self._properties, **self._nonlinear_models}

    @properties.setter
    def properties(self, properties: Union[Dict[PropertyCode, model_type], Dict[str, '_BaseModel']]) -> None:
        for k, v in properties.items():
            if isinstance(k, str):
                assert isinstance(v, _BaseModel), "Nonlinear models must inherit from '_BaseModel', linear models should be set with the 'PropertyCode' enum"
                self._nonlinear_models[k] = v
            else:
                self._properties[k] = v

    @property
    def reference_temperature(self) -> float:
        if PropertyCode.REFT in self._properties:
            return self._properties[PropertyCode.REFT]
        else:
            self._properties[PropertyCode.REFT] = self._reference_temperature
            return self._reference_temperature

    @reference_temperature.setter
    def reference_temperature(self, value: float) -> None:
        self._properties[PropertyCode.REFT] = value
