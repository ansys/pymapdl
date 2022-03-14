import pathlib
from itertools import islice
from typing import Dict, Union, Tuple, Iterable, List
import numpy as np
import re

from .property_codes import PropertyCode
from ..mapdl import _MapdlCore

model_type = Union[float, np.ndarray]

MATERIAL_HEADER_REGEX = re.compile(r"MATERIAL NUMBER\s+([\d]+)")
FLOAT_VALUE_REGEX = re.compile(r"(-?\d+\.\d*([Ee][+-]\d+)?)")


class Material:
    _mapdl: _MapdlCore
    _properties: Dict[PropertyCode, model_type]
    _is_dirty: Dict[PropertyCode, bool]
    _id: int
    _reference_temperature: float

    def __init__(self, mapdl: _MapdlCore, material_id: int = None, properties: Dict[PropertyCode, model_type] = None):
        self._mapdl = mapdl
        self._properties = {}
        self._is_dirty = {k.name: False for k in PropertyCode}
        if material_id is None:
            # Choose a new material ID, build a list with existing IDs and choose the first one that's not in use
            existing_material_ids = set()
            resp = mapdl.mplist("ALL", lab="DENS")
            ids = MATERIAL_HEADER_REGEX.findall(resp)
            for existing_id in ids:
                existing_material_ids.add(int(existing_id))
            self._id = min(existing_material_ids.difference(range(0, max(existing_material_ids)+2)))
        else:
            self._id = material_id
        if properties is not None:
            self._properties = properties
            for property_code in self._properties:
                self._is_dirty[property_code] = True

    def save(self, file_name: Union[str, pathlib.Path], extension: str = None, save_nonlinear_properties: bool = False):
        pass

    def refresh(self):
        mp_data = self._mapdl.mplist(self._id)
        self.properties = MaterialDataParser.parse_material(mp_data, self._id)

    @classmethod
    def from_id(cls, mapdl: _MapdlCore, material_id: int) -> 'Material':
        mp_data = mapdl.mplist(material_id)
        property_data = MaterialDataParser.parse_material(mp_data, material_id)
        return cls(mapdl, material_id=material_id, properties=property_data)

    def plot_property(self, property_name: str, x_lims: Tuple[float, float], y_lims: Tuple[float, float]):
        pass

    @property
    def material_id(self) -> int:
        return self._id

    @material_id.setter
    def material_id(self, value: int):
        self._id = value

    @property
    def properties(self) -> Dict[PropertyCode, model_type]:
        return self._properties

    @properties.setter
    def properties(self, properties: Dict[PropertyCode, model_type]) -> None:
        self._properties = properties

    @property
    def reference_temperature(self) -> float:
        if self._reference_temperature is None:
            if PropertyCode.REFT in self._properties:
                self._reference_temperature = self._properties[PropertyCode.REFT]
            else:
                self._reference_temperature = self._mapdl.get("out_reft", PropertyCode.REFT.name, self._id)
        return self._reference_temperature

    @reference_temperature.setter
    def reference_temperature(self, value: float) -> None:
        self._mapdl.mp(PropertyCode.REFT.name, self._id, value)
        self._reference_temperature = value

    def _parse_mp_output(self, response: str) -> Dict[PropertyCode, model_type]:
        """Parse the output of an mplist command to update this material. No effect if the material_id is not in the
        returned data. Does not operate on other materials if present.
        """
        pass

    def _write_property(self, property_code: PropertyCode) -> None:
        property_value = self.properties[property_code]
        if isinstance(property_value, float):
            self._mapdl.mp(property_code.name, self._id, property_value)
        elif isinstance(property_value, np.ndarray):
            if property_value.ndim != 2:
                raise ValueError("Invalid dimension for property, must be 2-dimensional")
            if property_value.shape[1] != 2:
                if property_value.shape[0] == 2:
                    property_value = np.transpose(property_value)
                else:
                    raise ValueError("Invalid array shape, must be 2-by-N")
            temp_values = property_value[:][0]
            for index, chunk in enumerate(self._chunk_data(temp_values)):
                self._mapdl.mptemp(6 * index + 1, *chunk)
            property_values = property_value[:][1]
            for index, chunk in enumerate(self._chunk_data(property_values)):
                self._mapdl.mpdata(property_code.name, self._id, 6 * index + 1, *chunk)

    @staticmethod
    def _chunk_data(data: Iterable):
        data_iterator = iter(data)
        piece = list(islice(data_iterator, 6))
        while piece:
            yield piece
            piece = list(islice(data_iterator, 6))


class MaterialDataParser:
    @staticmethod
    def parse_material(data: str, id_) -> Dict[PropertyCode, model_type]:
        data_section = MaterialDataParser._get_mp_section_with_id(data, id_)
        return MaterialDataParser._process_material(data_section)


    @staticmethod
    def _get_mp_section_with_id(data: str, id_: int) -> List[str]:
        """
        Throws indexerror if material ID doesn't exist in the file
        """

        material_ids = map(int, MATERIAL_HEADER_REGEX.findall(data))
        if id_ not in material_ids:
            raise IndexError(f"Material with ID {id_} not found in data")

        relevant_lines = []
        reading_correct_material = False
        for line in data.splitlines():
            stripped_line = line.strip()
            if stripped_line.startswith("MATERIAL"):
                match = MATERIAL_HEADER_REGEX.match(stripped_line)
                if match:
                    current_id = int(match.groups()[0])
                    if current_id == id_:
                        reading_correct_material = True
                    else:
                        reading_correct_material = False
            elif reading_correct_material:
                relevant_lines.append(line)

        return relevant_lines

    @staticmethod
    def _process_material(material_data: List[str]):
        property_data = {}
        reference_temperature = None
        current_property_code = None
        lines = [line.strip() for line in material_data if line.strip()]
        for line in lines:
            if line.startswith("TEMP"):
                current_property_code = MaterialDataParser._process_property_header(line)
                property_data[current_property_code] = []
            elif line.startswith("REFT"):
                temp_string = line.split("=")[1]
                temp_val = FLOAT_VALUE_REGEX.search(temp_string).group(0)
                reference_temperature = float(temp_val)
            else:
                property_data[current_property_code].append(line)
        for k, v in property_data.items():
            property_data[k] = MaterialDataParser._process_property(v)
        if reference_temperature is not None:
            property_data[PropertyCode.REFT] = reference_temperature
        return property_data

    @staticmethod
    def _process_property_header(header_line: str) -> PropertyCode:
        stripped_header_line = header_line.strip()
        try:
            property_name = stripped_header_line[4:].strip().split(' ')[0]
        except IndexError:
            raise IndexError("Invalid property header line")
        try:
            return PropertyCode[property_name]
        except KeyError:
            raise KeyError(f"Invalid property: '{property_name}'")

    @staticmethod
    def _process_property(property_data: List[str]) -> model_type:
        """
        Data format should be
          TEMP         EX
         231.34       0.23E12
         ...          ...

        OR
          TEMP         DENS
                      0.32E4
        """

        property_value = None
        if len(property_data) == 2:
            match = FLOAT_VALUE_REGEX.search(property_data[1])
            if match:
                property_value = float(match.group(0))
        else:
            property_value = np.ndarray((0, 2), dtype=float)
            for data_line in property_data[1:]:
                line_values = FLOAT_VALUE_REGEX.findall(data_line)
                property_value = np.vstack([property_value, [float(match[0]) for match in line_values]])
        return property_value


def get_materials(mapdl: _MapdlCore):
    """
    Returns all currently defined materials in the session
    """
    materials = []
    data = mapdl.mplist()
    material_ids = list(map(int, MATERIAL_HEADER_REGEX.findall(data)))
    for material_id in material_ids:
        material_properties = MaterialDataParser.parse_material(data, material_id)
        materials.append(Material(mapdl, material_id, material_properties))
    return materials
