# Importing logging
import logging
import os

import appdirs

from ansys.mapdl.core.logging import Logger

LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug("Loaded logging module as LOG")

_LOCAL_PORTS = []

# Per contract with Sphinx-Gallery, this method must be available at top level
try:
    from pyvista.utilities.sphinx_gallery import _get_sg_image_scraper

    _HAS_PYVISTA = True
except ModuleNotFoundError:  # pragma: no cover
    LOG.debug("The module 'Pyvista' is not installed.")
    _HAS_PYVISTA = False

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

from ansys.mapdl.core import examples
from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS
from ansys.mapdl.core.convert import convert_apdl_block, convert_script
from ansys.mapdl.core.launcher import (
    change_default_ansys_path,
    close_all_local_instances,
    find_ansys,
    get_ansys_path,
    get_available_ansys_installations,
    save_ansys_path,
)

# override default launcher when on pyansys.com
if "ANSJUPHUB_VER" in os.environ:  # pragma: no cover
    from ansys.mapdl.core.jupyter import launch_mapdl_on_cluster as launch_mapdl
else:
    from ansys.mapdl.core.launcher import launch_mapdl

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc as Mapdl
from ansys.mapdl.core.misc import Information, Report, _check_has_ansys
from ansys.mapdl.core.pool import LocalMapdlPool
from ansys.mapdl.core.theme import MapdlTheme

_HAS_ANSYS = _check_has_ansys()

# Setup data directory
try:
    USER_DATA_PATH = appdirs.user_data_dir("ansys_mapdl_core")
    if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
        os.makedirs(USER_DATA_PATH)

    EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")
    if not os.path.exists(EXAMPLES_PATH):  # pragma: no cover
        os.makedirs(EXAMPLES_PATH)

except:  # pragma: no cover
    pass

BUILDING_GALLERY = False
