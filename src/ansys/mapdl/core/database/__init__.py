"""The mapdl database module, allowing the access to the MAPDL database from Python."""

from .database import MapdlDb  # noqa: F401
from .database import VALID_MAPDL_VERSIONS, DBDef, check_mapdl_db_is_alive
