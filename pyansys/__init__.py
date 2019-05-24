from pyansys._version import __version__

from pyansys.archive import (Archive, write_cmblock, write_nblock,
                             save_as_archive)

from pyansys.common import read_binary
from pyansys.cellquality import *
from pyansys.convert import convert_script
from pyansys.ansys import ANSYS
from pyansys.ansys import change_default_ansys_path

try:
    from pyansys import ansys
    has_ansys = ansys.check_valid_ansys()
except:
    has_ansys = False
