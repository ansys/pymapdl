from abc import ABCMeta, abstractmethod
from typing import Tuple, List

TYPE_CHECKING = False
if TYPE_CHECKING:
    from ..material import Material
    from .exceptions import ModelValidationException
    from ansys.mapdl.core.mapdl import _MapdlCore


class _BaseModel(metaclass=ABCMeta):
    model_codes: Tuple

    @abstractmethod
    def write_model(self, mapdl: '_MapdlCore', material: 'Material') -> None:
        ...

    @abstractmethod
    def validate_model(self) -> 'Tuple[bool, List[ModelValidationException]]':
        ...

    @classmethod
    @abstractmethod
    def deserialize_model(cls, model_code: str, model_data: List[str]) -> "_BaseModel":
        ...
