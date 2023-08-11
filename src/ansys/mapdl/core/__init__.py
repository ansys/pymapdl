# Importing logging
import logging
import os
import sys
from warnings import warn

import platformdirs

# Setup data directory
USER_DATA_PATH = platformdirs.user_data_dir(
    appname="ansys_mapdl_core", appauthor="Ansys"
)
if not os.path.exists(USER_DATA_PATH):  # pragma: no cover
    os.makedirs(USER_DATA_PATH)

DEPRECATING_MINIMUM_PYTHON_VERSION = True
MINIMUM_PYTHON_VERSION = (3, 8)

first_time_file = os.path.join(USER_DATA_PATH, ".firstime")
if not os.path.exists(first_time_file):  # pragma: no cover
    py_ver = f"{sys.version_info[0]}.{sys.version_info[1]}"
    py_ver_min = f"{MINIMUM_PYTHON_VERSION[0]}.{MINIMUM_PYTHON_VERSION[1]}"

    if (
        sys.version_info[1] == MINIMUM_PYTHON_VERSION[1]
        and DEPRECATING_MINIMUM_PYTHON_VERSION
    ):
        warn(
            f"Support for Python {py_ver} will be dropped in the next minor " "release."
        )

    if sys.version_info[1] <= MINIMUM_PYTHON_VERSION[1]:
        warn(
            f"Python {py_ver} is not being tested or officially supported. "
            "It is recommended you use a newer version of Python. "
            f"The mininimum supported and tested version is {py_ver_min}.\n\n"
            "**This warning is shown only the first time you run PyMAPDL.**\n"
        )

    with open(first_time_file, "w") as fid:
        fid.write("")

EXAMPLES_PATH = os.path.join(USER_DATA_PATH, "examples")

from ansys.mapdl.core.logging import Logger

LOG = Logger(level=logging.ERROR, to_file=False, to_stdout=True)
LOG.debug("Loaded logging module as LOG")


BUILDING_GALLERY = False
RUNNING_TESTS = False

if RUNNING_TESTS:  # pragma: no cover
    LOG.debug("Running tests on Pytest")

_LOCAL_PORTS = []


# Per contract with Sphinx-Gallery, this method must be available at top level
try:
    import pyvista

    _HAS_PYVISTA = True
except ModuleNotFoundError:  # pragma: no cover
    LOG.debug("The module 'Pyvista' is not installed.")
    _HAS_PYVISTA = False

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))


from ansys.tools.path.path import (
    change_default_ansys_path,
    find_ansys,
    get_ansys_path,
    get_available_ansys_installations,
    save_ansys_path,
)

from ansys.mapdl.core._version import SUPPORTED_ANSYS_VERSIONS
from ansys.mapdl.core.convert import convert_apdl_block, convert_script
from ansys.mapdl.core.launcher import close_all_local_instances

# override default launcher when on pyansys.com
if "ANSJUPHUB_VER" in os.environ:  # pragma: no cover
    from ansys.mapdl.core.jupyter import launch_mapdl_on_cluster as launch_mapdl
else:
    from ansys.mapdl.core.launcher import launch_mapdl

from ansys.mapdl.core.mapdl_grpc import MapdlGrpc as Mapdl
from ansys.mapdl.core.misc import Information, Report, _check_has_ansys
from ansys.mapdl.core.pool import LocalMapdlPool
from ansys.mapdl.core.theme import MapdlTheme, _apply_default_theme

_HAS_ANSYS = _check_has_ansys()

_apply_default_theme()

BUILDING_GALLERY = False
RUNNING_TESTS = False


VERSION_MAP = {
    (0, 0, 0): "2020R2",
    (0, 3, 0): "2021R1",
    (0, 4, 0): "2021R2",
    (0, 4, 1): "2021R2",
    (0, 5, 0): "2022R1",
    (0, 5, 1): "2022R2",  # as of 21 Mar 2022 unreleased
}
"""A dictionary relating PyMAPDL server versions with the unified install ones."""
