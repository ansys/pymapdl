import appdirs
import os
from pyansys._version import __version__

from pyansys.archive import (Archive, write_cmblock, write_nblock,
                             save_as_archive)

from pyansys.common import read_binary
from pyansys.cellquality import *
from pyansys.convert import convert_script
from pyansys.mapdl import ANSYS, Mapdl
from pyansys.mapdl import change_default_ansys_path

# Sphinx-gallery tools
from pyansys.sphinx_gallery import Scraper, _get_sg_image_scraper

try:
    from pyansys import mapdl
    has_ansys = mapdl.check_valid_ansys()
except:
    has_ansys = False


# Set up data directory
try:
    USER_DATA_PATH = appdirs.user_data_dir('pyansys')
    if not os.path.exists(USER_DATA_PATH):
        os.makedirs(USER_DATA_PATH)

    EXAMPLES_PATH = os.path.join(USER_DATA_PATH, 'examples')
    if not os.path.exists(EXAMPLES_PATH):
        os.makedirs(EXAMPLES_PATH)
except:
    pass


from pyansys.examples.downloads import *
