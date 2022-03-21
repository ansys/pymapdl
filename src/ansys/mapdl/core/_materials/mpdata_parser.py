from typing import Dict, List, Optional

from .common import FLOAT_VALUE_REGEX, MP_MATERIAL_HEADER_REGEX, model_type, np
from .property_codes import PropertyCode


class _MaterialDataParser:
    @staticmethod
    def parse_material(data: str, id_: int) -> Dict[PropertyCode, model_type]:
        """
        Parse the response from an `MPLIST` command into a set of material properties and nonlinear material models.

        Parameters
        ----------
        data: str
            String response from the `MPLIST` command.
        id_: int
            Material identity to be parsed
        """
        data_section = _MaterialDataParser._get_mp_section_with_id(data, id_)
        return _MaterialDataParser._process_material(data_section)

    @staticmethod
    def _get_mp_section_with_id(data: str, id_: int) -> List[str]:
        """
        Extract material property information for the specified material identity.

        Parameters
        ----------
        data: str
            String response from the `MPLIST` command
        id_: int
            Material identity to be extracted

        Returns
        -------
        List[str]
            Relevant section of the data input, split on newlines
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
    def _process_material(material_data: List[str]) -> Dict[PropertyCode, model_type]:
        """
        Deserialize a material into a property dictionary

        Parameters
        ----------
        material_data: List[str]
            List of lines containing property data for one material

        Returns
        -------
        Dict[PropertyCode, Union[float, np.ndarray]]
            Dictionary of material properties, indexed by property code
        """
        property_data: Dict[PropertyCode, model_type] = {}
        property_lines: Dict[PropertyCode, List[str]] = {}
        reference_temperature = None
        current_property_code = None
        lines = [line.strip() for line in material_data if line.strip()]
        for line in lines:
            if line.startswith("TEMP"):
                current_property_code = _MaterialDataParser._process_property_header(
                    line
                )
                property_lines[current_property_code] = []
            elif line.startswith("REFT"):
                temp_string = line.split("=")[1]
                temp_val_match = FLOAT_VALUE_REGEX.search(temp_string)
                assert temp_val_match is not None, "Invalid material input"
                reference_temperature = float(temp_val_match.group(0))
            else:
                assert current_property_code is not None, "Invalid material input"
                property_lines[current_property_code].append(line)
        for k, v in property_lines.items():
            property_data[k] = _MaterialDataParser._process_property(v)
        if reference_temperature is not None:
            property_data[PropertyCode.REFT] = reference_temperature
        return property_data

    @staticmethod
    def _process_property_header(header_line: str) -> PropertyCode:
        """
        Deserialize a property header line into the relevant property code

        Parameters
        ----------
        header_line: str
            Material property header line

        Returns
        -------
        PropertyCode
            Corresponding property code object

        Raises
        ------
        KeyError
            If the header line specifies an unknown property code
        IndexError
            If the header line does not match the expected format
        """
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
        Deserialize the property data into a python object. Single values are deserialized into floats, arrays are
        deserialized into NumPy arrays, where the first column contains temperature values and the second contains
        property values at those temperatures.

        Parameters
        ----------
        property_data: List[str]
            Property data section to be deserialized

        Returns
        -------
        Union[float, np.ndarray]
            Deserialized model, either a single float, or a NumPy array if the property is temperature-dependent.
        """

        property_value: Optional[model_type] = None
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
        assert property_value is not None, "Invalid property data input"
        return property_value
