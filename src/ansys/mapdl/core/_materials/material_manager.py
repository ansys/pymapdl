import inspect
from pathlib import Path
from typing import Dict, List, Union

import ansys.mapdl.core._materials._nonlinear_models as models
from .common import MP_MATERIAL_HEADER_REGEX, _chunk_data, model_type, np
from .property_codes import PropertyCode
from .mpdata_parser import _MaterialDataParser
from .material import Material

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl import _MapdlCore


class MaterialManager:
    model_type_map: Dict[str, models._BaseModel] = {}
    mapdl: '_MapdlCore'

    def __init__(self, mapdl: '_MapdlCore'):
        response = inspect.getmembers(models, self.__is_subclass_predicate)
        model_classes: List[models._BaseModel] = [tple[1] for tple in response]
        for class_ in model_classes:
            supported_model_codes = class_.model_codes
            for model_code in supported_model_codes:
                self.model_type_map[model_code] = class_
        self.mapdl = mapdl

    @staticmethod
    def __is_subclass_predicate(obj):
        return isinstance(obj, type) and issubclass(obj, models._BaseModel) and not inspect.isabstract(obj)

    def get_materials(self) -> Dict[int, 'Material']:
        """
        Returns all currently defined materials in the session
        """
        materials = []
        data = self.mapdl.mplist()
        material_ids = list(map(int, MP_MATERIAL_HEADER_REGEX.findall(data)))
        for material_id in material_ids:
            material_properties = _MaterialDataParser.parse_material(data, material_id)
            materials.append(Material(material_id, material_properties))
        return {material.material_id: material for material in materials}

    def get_material(self, id_: int) -> 'Material':
        data = self.mapdl.mplist(id_)
        material_properties = _MaterialDataParser.parse_material(data, id_)
        return Material(id_, material_properties)

    def delete_material(self, id_: int, check_assignments=True) -> None:
        if check_assignments:
            check_level = "CHECK"
        else:
            check_level = "NOCHECK"
        self.mapdl.mpdele("ALL", mat1=id_, lchk=check_level)

    def write_material(self, material: Material) -> Material:
        if material.material_id is None:
            ids = self._get_current_ids()
            material.material_id = min(set(range(max(ids) + 2)) - set(ids))
        for property_code, value in material.properties:
            self._write_property(material.material_id, property_code, value)
        return self.get_material(material.material_id)

    def load_material_card(self, file_path: Union[str, Path], read_nonlinear: bool = False) -> Dict[int, Material]:
        previous_ids = self._get_current_ids()
        if isinstance(file_path, str):
            file_path = Path(file_path)
        extension = file_path.suffix.lstrip('.')
        path = file_path.with_suffix('')
        if read_nonlinear:
            lib = "LIB"
        else:
            lib = None
        self.mapdl.mpread(path, extension, lib=lib)
        material_dict = self.get_materials()
        return {id_: material for id_, material in material_dict.items() if id_ not in previous_ids}

    def save_material(self, file_name: Union[str, Path], material: Material, write_nonlinear: bool = False):
        if isinstance(file_name, str):
            file_name = Path(file_name)
        fname = file_name.with_suffix('')
        ext = file_name.suffix.lstrip('.')
        if write_nonlinear:
            lib = 'LIB'
        else:
            lib = None
        self.mapdl.mpwrite(fname, ext, lib, material.material_id)

    def _get_current_ids(self) -> List[int]:
        existing_material_ids = set()
        resp = self.mapdl.mplist("ALL", lab="DENS")
        ids = MP_MATERIAL_HEADER_REGEX.findall(resp)
        for existing_id in ids:
            existing_material_ids.add(int(existing_id))
        return sorted(list(existing_material_ids))

    def _write_property(self, material_id: int, property_code: PropertyCode, property_value: model_type) -> None:
        if isinstance(property_value, float):
            self.mapdl.mp(property_code.name, material_id, property_value)
        elif isinstance(property_value, np.ndarray):
            if property_value.ndim != 2:
                raise ValueError("Invalid dimension for property, must be 2-dimensional")
            if property_value.shape[1] != 2:
                if property_value.shape[0] == 2:
                    property_value = np.transpose(property_value)
                else:
                    raise ValueError("Invalid array shape, must be 2-by-N")
            temp_values = property_value[:][0]
            for index, chunk in enumerate(_chunk_data(temp_values)):
                self.mapdl.mptemp(6 * index + 1, *chunk)
            property_values = property_value[:][1]
            for index, chunk in enumerate(_chunk_data(property_values)):
                self.mapdl.mpdata(property_code.name, material_id, 6 * index + 1, *chunk)
