try:
    from ansys.dpf.core import Model

    HAS_DPF_CORE = True
except ModuleNotFoundError:  # pragma: no cover
    HAS_DPF_CORE = False

from .mesh import MapdlMesh
