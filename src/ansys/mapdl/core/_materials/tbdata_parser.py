from typing import Dict, List, Optional

from ._nonlinear_models import _BaseModel
from .common import TB_MATERIAL_HEADER_REGEX


class _TableDataParser:
    """
    Parses responses from the `TBLIST` command into individual non-linear models.
    """

    models: Dict[str, _BaseModel]

    def __init__(self, models: Dict[str, _BaseModel]):
        self.models = models

    @staticmethod
    def _get_tb_sections_with_id(data: str, id_: int) -> Dict[str, List[str]]:
        """
        Extract material property information for the specified material identity.

        Parameters
        ----------
        data: str
            String response from the `TBLIST` command
        id_: int
            Material identity to be extracted

        Returns
        -------
        Dict[str, List[str]]
            Dictionary of relevant non-linear model sections, indexed by model name. Each section is split on newlines.
        """
        tb_chunks: Dict[str, List[str]] = {}
        header_lines = TB_MATERIAL_HEADER_REGEX.findall(data)
        for line in header_lines:
            if len(line) == 2 and int(line[1]) == id_:
                tb_chunks[line[0]] = []

        if len(tb_chunks) == 0:
            raise IndexError(f"Material with ID {id_} not found in data")

        material_code = None
        for line in data.splitlines():
            stripped_line = line.strip()
            match = TB_MATERIAL_HEADER_REGEX.search(stripped_line)
            if match:
                current_material_id = int(match.groups()[1])
                if current_material_id == id_:
                    material_code = match.groups()[0]
                else:
                    material_code = None
            if material_code is not None:
                tb_chunks[material_code].append(line)

        return tb_chunks

    def get_models_by_id(
        self, data: str, material_id: int
    ) -> Optional[Dict[str, _BaseModel]]:
        material_model_data = self._get_tb_sections_with_id(data, material_id)
        model_data_map = {}
        for model_code, model_data in material_model_data.items():
            model_data_map[model_code] = self.deserialize_model(model_code, model_data)
        return model_data_map

    def deserialize_model(self, model_code: str, model_data: List[str]) -> _BaseModel:
        """
        Deserialize a model definition into a model object.

        Parameters
        ----------
        model_code: str
            String model code. See :meth:`ansys.mapdl.core._commands._preproc.materials.tb`
        model_data: List[str]
            List of lines containing model data for one material and one model

        Returns
        -------
        _BaseModel
            A model object

        Raises
        ------
        NotImplementedError
            If a wrapper with the specified model_code does not exist.

        """
        if model_code not in self.models.keys():
            raise NotImplementedError(
                f"Model with key '{model_code}' is not implemented yet."
            )
        target_model = self.models[model_code]
        return target_model.deserialize_model(model_code, model_data)
