import inspect
from pathlib import Path
from typing import Dict, List, Union

import ansys.mapdl.core._materials._nonlinear_models as models

from .common import MP_MATERIAL_HEADER_REGEX, _chunk_data, model_type, np
from .material import Material
from .mpdata_parser import _MaterialDataParser
from .property_codes import PropertyCode

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ansys.mapdl.core.mapdl import _MapdlCore


class MaterialManager:
    """
    Class to manage material creation, assignment and other management tasks. Main entry-point for the pythonic material
    management interface.
    """

    model_type_map: Dict[str, models._BaseModel] = {}
    mapdl: "_MapdlCore"

    def __init__(self, mapdl: "_MapdlCore"):
        """
        Create a new MaterialManager object ready for use.

        Parameters
        ----------
        mapdl: _MapdlCore
            Valid instance of PyMAPDL
        """
        response = inspect.getmembers(models, self.__is_subclass_predicate)
        model_classes: List[models._BaseModel] = [tple[1] for tple in response]
        for class_ in model_classes:
            supported_model_codes = class_.model_codes
            for model_code in supported_model_codes:
                self.model_type_map[model_code] = class_
        self.mapdl = mapdl

    @staticmethod
    def __is_subclass_predicate(obj: object) -> bool:
        """
        Predicate to determine if a given object is a strict subclass of :obj:`models._BaseModel`

        Parameters
        ----------
        obj: object
            Any python object

        Returns
        -------
        bool
            True if object is strictly a subclass of :obj:`models._BaseModel`, otherwise False
        """
        return (
            isinstance(obj, type)
            and issubclass(obj, models._BaseModel)
            and not inspect.isabstract(obj)
        )

    def get_materials(self) -> Dict[int, "Material"]:
        """
        Returns all currently defined materials in the session

        Returns
        -------
        Dict[int, Material]
            Dictionary of all defined materials, indexed by identity.
        """
        materials = []
        data = self.mapdl.mplist()
        material_ids = list(map(int, MP_MATERIAL_HEADER_REGEX.findall(data)))
        for material_id in material_ids:
            material_properties = _MaterialDataParser.parse_material(data, material_id)
            materials.append(Material(material_id, material_properties))
        return {material.material_id: material for material in materials}

    def get_material(self, id_: int) -> "Material":
        """
        Gets a material defined in the session with specified identity

        Parameters
        ----------
        id_: int
            Material identity
        """
        data = self.mapdl.mplist(id_)
        material_properties = _MaterialDataParser.parse_material(data, id_)
        return Material(id_, material_properties)

    def delete_material(self, id_: int, check_assignments=True) -> None:
        """
        Deletes a material from the session with specified identity. Optionally verify if the material has associated
        elements.

        Parameters
        ----------
        id_: int
            Material identity
        check_assignments: bool
            If True the command will not execute if this material is associated with any elements, it will list the
            associated entities. If False then ignore all assignments and delete the material anyway.
        """
        if check_assignments:
            check_level = "CHECK"
        else:
            check_level = "NOCHECK"
        self.mapdl.mpdele("ALL", mat1=id_, lchk=check_level)

    def write_material(self, material: Material) -> Material:
        """
        Write a material to MAPDL. If no material identity is specified in the material, then determine the first
        unoccupied identity.

        Parameters
        ----------
        material: Material
            Material object to be written to MAPDL

        Returns
        -------
        Material
            Material as written to MAPDL, will have populated material_id
        """
        if material.material_id is None:
            ids = self._get_current_ids()
            material.material_id = min(set(range(max(ids) + 2)) - set(ids))
        for property_code, value in material.properties:
            if isinstance(property_code, PropertyCode):
                self._write_property(material.material_id, property_code, value)
            else:
                value.write_model(self.mapdl, self)
        return self.get_material(material.material_id)

    def load_material_card(
        self,
        file_path: Union[str, Path],
        read_nonlinear: bool = False,
        material_id: int = None,
    ) -> Dict[int, Material]:
        """
        Read one or more materials from a saved material card. File path should refer to location on the machine hosting
        the MAPDL process.

        Parameters
        ----------
        file_path: Union[str, Path]
            Path to the file to be read, either a string path or PathLib.Path
        read_nonlinear: bool
            If True, read nonlinear properties. The file must have been written with either `write_nonlinear=True` or
            with the APDL option `lib='LIB'`
        material_id: int
            If read_nonlinear is True then this specifies which material identity should be used when importing the
            data. Ignored if read_nonlinear is False. Defaults to the first unoccupied material identity in MAPDL.

        Returns
        -------
        Dict[int, Material]
            Dictionary of imported materials, indexed by identity

        Notes
        -----
        If read_nonlinear is True, then the MAT pointer in MAPDL will be set to the newly imported material.
        """
        previous_ids = self._get_current_ids()
        if isinstance(file_path, str):
            file_path = Path(file_path)
        extension = file_path.suffix.lstrip(".")
        path = file_path.with_suffix("")
        if read_nonlinear:
            lib = "LIB"
            if material_id is None:
                ids = self._get_current_ids()
                material_id = min(set(range(max(ids) + 2)) - set(ids))
            self.mapdl.mat(material_id)
        else:
            lib = None
        self.mapdl.mpread(path, extension, lib=lib)
        material_dict = self.get_materials()
        return {
            id_: material
            for id_, material in material_dict.items()
            if id_ not in previous_ids
        }

    def save_material(
        self,
        file_name: Union[str, Path],
        material: Material,
        write_nonlinear: bool = False,
    ):
        """
        Write the specified material out to a file on the machine hosting the MAPDL process.

        Parameters
        ----------
        file_name: Union[str, Path]
            Path to the file to be written, either a string path or PathLib.Path
        material: Material
            Material to be written
        write_nonlinear: bool
            If True, write all nonlinear properties to the file, this also allows the material identity to be specified
            at import time. Otherwise, only write linear properties.

        """
        if isinstance(file_name, str):
            file_name = Path(file_name)
        fname = file_name.with_suffix("")
        ext = file_name.suffix.lstrip(".")
        if write_nonlinear:
            lib = "LIB"
        else:
            lib = None
        self.mapdl.mpwrite(fname, ext, lib, material.material_id)

    def _get_current_ids(self) -> List[int]:
        """
        Returns all identities currently assigned within MAPDL

        Returns
        -------
        List[int]
            List of all assigned material identities
        """
        existing_material_ids = set()
        resp = self.mapdl.mplist("ALL", lab="DENS")
        ids = MP_MATERIAL_HEADER_REGEX.findall(resp)
        for existing_id in ids:
            existing_material_ids.add(int(existing_id))
        return sorted(list(existing_material_ids))

    def _write_property(
        self, material_id: int, property_code: PropertyCode, property_value: model_type
    ) -> None:
        """
        Write a linear property to MAPDL

        Parameters
        ----------
        material_id: int
            Integer material identity to which this property refers
        property_code: PropertyCode
            PropertyCode value indicating which property is to be written
        property_value: Union[float, np.ndarray]
            Either a single float value if the property is isothermal, or a numpy array with columns corresponding to
            temperature and property value if the property is temperature-dependent. Up to 100 values may be provided
            for temperature-dependent properties.
        """
        if isinstance(property_value, float):
            self.mapdl.mp(property_code.name, material_id, property_value)
        elif isinstance(property_value, np.ndarray):
            if property_value.ndim != 2:
                raise ValueError(
                    "Invalid dimension for property, must be 2-dimensional"
                )
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
                self.mapdl.mpdata(
                    property_code.name, material_id, 6 * index + 1, *chunk
                )
        else:
            raise TypeError(
                f"Property has invalid type: {type(property_value)}. Must be either float or np.ndarray."
            )
