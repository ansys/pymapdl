"""Database setup command extensions."""

from functools import wraps

from ansys.mapdl.core.mapdl_core import _MapdlCore

from .. import _ExtendedMixinBase


class _ExtendedDatabaseSetupMixin(_ExtendedMixinBase):
    """Extended database setup commands."""
    @wraps(_MapdlCore.clear)
    def clear(self, read: str = "NOSTART", **kwargs):
        """Wraps the MAPDL ``CLEAR`` command to use `NOSTART` with mute=True"""
        if self.is_grpc:
            self._create_session()
        kwargs.setdefault("mute", True)
        getattr(super(), "clear")(read=read, **kwargs)
