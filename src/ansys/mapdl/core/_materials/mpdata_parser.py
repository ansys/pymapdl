from typing import Dict, List
from .property_codes import PropertyCode
from .common import model_type, MP_MATERIAL_HEADER_REGEX, FLOAT_VALUE_REGEX, np


class _MaterialDataParser:
    @staticmethod
    def parse_material(data: str, id_) -> Dict[PropertyCode, model_type]:
        data_section = _MaterialDataParser._get_mp_section_with_id(data, id_)
        return _MaterialDataParser._process_material(data_section)

    @staticmethod
    def _get_mp_section_with_id(data: str, id_: int) -> List[str]:
        """
        Throws indexerror if material ID doesn't exist in the file
        """

        material_ids = map(int, MP_MATERIAL_HEADER_REGEX.findall(data))
        if id_ not in material_ids:
            raise IndexError(f"Material with ID {id_} not found in data")

        relevant_lines = []
        reading_correct_material = False
        for line in data.splitlines():
            stripped_line = line.strip()
            if stripped_line.startswith("MATERIAL"):
                match = MP_MATERIAL_HEADER_REGEX.match(stripped_line)
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
                current_property_code = _MaterialDataParser._process_property_header(
                    line
                )
                property_data[current_property_code] = []
            elif line.startswith("REFT"):
                temp_string = line.split("=")[1]
                temp_val = FLOAT_VALUE_REGEX.search(temp_string).group(0)
                reference_temperature = float(temp_val)
            else:
                property_data[current_property_code].append(line)
        for k, v in property_data.items():
            property_data[k] = _MaterialDataParser._process_property(v)
        if reference_temperature is not None:
            property_data[PropertyCode.REFT] = reference_temperature
        return property_data

    @staticmethod
    def _process_property_header(header_line: str) -> PropertyCode:
        stripped_header_line = header_line.strip()
        try:
            property_name = stripped_header_line[4:].strip().split(" ")[0]
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
                property_value = np.vstack(
                    [property_value, [float(match[0]) for match in line_values]]
                )
        return property_value
