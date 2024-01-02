"""The mapdl database module, allowing the access to the MAPDL database from Python."""

from .database import MINIMUM_MAPDL_VERSION, DBDef, check_mapdl_db_is_alive
from .database import MapdlDb  # noqa: F401
