import appdirs
import os

# Importing logging
import logging
from ansys.mapdl.core.logging import Logger
LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug('Loaded logging module as LOG')

_LOCAL_PORTS = []

# Per contract with Sphinx-Gallery, this method must be available at top level
from pyvista.utilities.sphinx_gallery import _get_sg_image_scraper

from ansys.mapdl.core._version import __version__
from ansys.mapdl.core.convert import convert_script, convert_apdl_block
from ansys.mapdl.core.launcher import (
    launch_mapdl,
    change_default_ansys_path,
    find_ansys,
    close_all_local_instances,
)
from ansys.mapdl.core.misc import Report, _check_has_ansys
from ansys.mapdl.core.launcher import get_ansys_path
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc as Mapdl
from ansys.mapdl.core.pool import LocalMapdlPool
from ansys.mapdl.core.theme import MapdlTheme

from ansys.mapdl.core import examples

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


# override default launcher when on pyansys.com
if 'ANSJUPHUB_VER' in os.environ:
    from ansys.mapdl.core.jupyter import launch_mapdl_on_cluster as launch_mapdl
