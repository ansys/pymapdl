"""
Replacing Result in PyMAPDL.
"""

import tempfile
import weakref

from ansys.mapdl.core.misc import random_string


class DPFResult:
    """Main class"""

    def __init__(self, mapdl):
        """Initialize Result instance"""
        from ansys.mapdl.core.mapdl import _MapdlCore

        if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
            raise TypeError("Must be initialized using Mapdl instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self._set_loaded = False

        # dpf
        self.__rst_directory = None
        self.__tmp_rst_name = None
        self._update_required = False  # if true, it triggers a update on the RST file
        self._cached_dpf_model = None

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

    @property
    def _rst(self):
        return os.path.join(self._rst_directory, self._tmp_rst_name)

    @property
    def local(self):
        return self._mapdl._local

    @property
    def _rst_directory(self):
        if self.__rst_directory is None:
            if self.local:
                _rst_directory = self._mapdl.directory
            else:
                _rst_directory = os.path.join(tempfile.gettempdir(), random_string())
                if not os.path.exists(_rst_directory):
                    os.mkdir(_rst_directory)

            self.__rst_directory = _rst_directory

        return self.__rst_directory

    @property
    def _tmp_rst_name(self):
        if self.__tmp_rst_name is None:
            if self.local:
                self.__tmp_rst_name = self._mapdl.jobname
            else:
                self.__tmp_rst_name = f"model_{random_string()}.rst"
        return self.__tmp_rst_name

    def _update(self, progress_bar=None, chunk_size=None):
        # Saving model
        self._mapdl.save(self._tmp_rst_name[:-4], "rst", "model")

        if not self.local:
            self.logger.debug("Updating the local copy of remote RST file.")
            # download file
            self._mapdl.download(
                self._tmp_rst_name,
                self._rst_directory,
                chunk_size=chunk_size,
                progress_bar=progress_bar,
            )

        # Updating model
        self._build_dpf_object()

        # Resetting flag
        self._update_required = False

    def _build_dpf_object(self):
        self.logger.debug("Building DPF Model object.")
        self._cached_dpf_model = Model(self._rst)
