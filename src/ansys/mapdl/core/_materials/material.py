import pathlib
from dataclasses import dataclass
from typing import Dict, Union, Tuple, List

from .property_codes import PropertyCode
from ..mapdl import _MapdlCore

model_type = Union[float, "PolynomialModel", List[List[float]]]

class Material:
    _mapdl: _MapdlCore
    _properties: Dict[PropertyCode, model_type]
    id: int

    def __init__(self, mapdl: _MapdlCore, material_id: int = None, properties: Dict[PropertyCode, model_type] = None):
        self._mapdl = mapdl
        if material_id is None:
            # Choose a new material ID, build a list with existing IDs and choose the first one that's not in use
            existing_material_ids = set()
            resp = mapdl.run("MPLIST,ALL,,,DENS,")
            lines = resp.split("\n")
            for line in lines:
                if line.startswith("MPDATA"):
                    tokens = line.split(',')
                    existing_material_ids.add(int(tokens[1]))
            self.id = min(existing_material_ids.difference(range(0,max(existing_material_ids)+2)))
        else:
            self.id = material_id
        if properties is not None:
            self.properties = properties


    def save(self, file_name: Union[str, pathlib.Path], extension: str = None, save_nonlinear_properties: bool = False):
        pass

    def refresh(self):
        pass

    @classmethod
    def from_id(cls, mapdl: _MapdlCore, material_id: int) -> 'Material':

        return cls(mapdl, material_id=material_id)

    def plot_property(self, property_name: str, x_lims: Tuple[float, float], y_lims: Tuple[float, float]):
        pass

    @property
    def material_id(self) -> int:
        return self.id

    @material_id.setter
    def material_id(self, value: int):
        self.id = value

    @property
    def properties(self) -> Dict[PropertyCode, model_type]:
        return self._properties

    @properties.setter
    def properties(self, properties: Dict[PropertyCode, model_type]) -> None:
        self._properties = properties

    def _parse_mp_output(self, response: str) -> Dict[PropertyCode, model_type]:
        pass


@dataclass
class PolynomialModel:
    c0: float
    c1: float
    c2: float
    c3: float
    c4: float

    def __str__(self) -> str:
        return f"{self.c0:.3e}{self.render_coefficient(self.c1)}x{self.render_coefficient(self.c2)}x^2{self.render_coefficient(self.c3)}x^3{self.render_coefficient(self.c4)}x^4"

    @staticmethod
    def render_coefficient(coefficient: float) -> str:
        output = ""
        if coefficient > 0:
            output += "+"
        output += f"{coefficient:.3e}"
        return output