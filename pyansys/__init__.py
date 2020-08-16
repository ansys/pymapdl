import appdirs
import os

# Per contract with Sphinx-Gallery, this method must be available at top level
from pyvista.utilities.sphinx_gallery import _get_sg_image_scraper

from pyansys._version import __version__
from pyansys.archive import (Archive, write_cmblock, write_nblock,
                             save_as_archive)
from pyansys.cell_quality import quality
from pyansys.common import read_binary
from pyansys.convert import convert_script
from pyansys.launcher import launch_mapdl, change_default_ansys_path
from pyansys.misc import Report, _configure_pyvista, _check_has_ansys
from pyansys.examples.downloads import *


_HAS_ANSYS = _check_has_ansys()

# Setup data directory
try:
    USER_DATA_PATH = appdirs.user_data_dir('pyansys')
    if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
        os.makedirs(USER_DATA_PATH)

    EXAMPLES_PATH = os.path.join(USER_DATA_PATH, 'examples')
    if not os.path.exists(EXAMPLES_PATH):  # pragma: no cover
        os.makedirs(EXAMPLES_PATH)

except:  # pragma: no cover
    pass

# set pyvista defaults
_configure_pyvista()
