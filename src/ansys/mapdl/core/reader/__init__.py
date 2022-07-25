try:
    from ansys.dpf.core import Model

    HAS_DPF_CORE = True
except ModuleNotFoundError:
    HAS_DPF_CORE = False

from .mesh import DPFMapdlMesh
