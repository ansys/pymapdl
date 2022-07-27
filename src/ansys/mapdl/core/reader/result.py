"""
Replacing Result in PyMAPDL.
"""

import weakref


class DPFResult:
    """Main class"""

    def __init__(self, mapdl):
        """Initialize Result instance"""
        from ansys.mapdl.core.mapdl import _MapdlCore

        if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
            raise TypeError("Must be initialized using Mapdl instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self._set_loaded = False

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of MAPDL"""
        return self._mapdl_weakref()

    @property
    def _log(self):
        """alias for mapdl log"""
        return self._mapdl._log

    def _set_log_level(self, level):
        """alias for mapdl._set_log_level"""
        return self._mapdl._set_log_level(level)
