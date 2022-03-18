from typing import Dict, List, Set
from ._nonlinear_models import _BaseModel
from .common import TB_MATERIAL_HEADER_REGEX


class TableDataParser:
    models: Dict[str, _BaseModel]

    def __init__(self, models: Dict[str, _BaseModel]):
        self.models = models

    @staticmethod
    def _get_tb_sections_with_id(data: str, id_: int) -> Dict[str, List[str]]:
        """
        Throws indexerror if material ID doesn't exist in the file
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

    def deserialize_model(self, model_code: str, model_data: List[str]) -> _BaseModel:
        if model_code not in self.models.keys():
            raise NotImplementedError(f"Model with key '{model_code}' is not implemented yet.")
        target_model = self.models[model_code]
        return target_model.deserialize_model(model_code, model_data)