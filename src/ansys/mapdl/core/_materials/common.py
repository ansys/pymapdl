from itertools import islice
from typing import Iterable, Union, List
import re

import numpy as np

MP_MATERIAL_HEADER_REGEX = re.compile(r"MATERIAL NUMBER\s+([\d]+)")
TB_MATERIAL_HEADER_REGEX = re.compile(
    r"\(([A-Z]+)\) Table For Material\s+([\d]+)[^\n]*"
)
FLOAT_VALUE_REGEX = re.compile(r"(-?\d+\.\d*([Ee][+-]\d+)?)")
MATRIX_LABEL_REGEX = re.compile(r"(\w\s?\d{1,2})")

model_type = Union[float, np.ndarray]


def _chunk_data(data: Iterable):
    data_iterator = iter(data)
    piece = list(islice(data_iterator, 6))
    while piece:
        yield piece
        piece = list(islice(data_iterator, 6))


def _chunk_lower_triangular_matrix(matrix: np.ndarray) -> Iterable[Iterable[float]]:
    vals = []
    for row_index in range(0, matrix.shape[0]):
        for col_index in range(0, row_index + 1):
            vals.append(matrix[row_index][col_index])
    return _chunk_data(vals)


def fill_lower_triangular_matrix(vector: List[float]) -> np.ndarray:
    size_x = (np.sqrt(8 * len(vector) + 1) - 1) / 2
    if not np.isclose(int(size_x), size_x):
        raise ValueError(
            f"vector does not appear to be a valid lower-triangular matrix in flat form (size {len(vector)}) is not a triangular number"
        )
    size_x = int(size_x)
    output = np.zeros((size_x, size_x))
    output[np.triu_indices(output.shape[0], k=0)] = vector
    return output + output.T - np.diag(np.diag(output))
