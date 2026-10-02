"""Database component command extensions."""

from functools import wraps

from ansys.mapdl.core.mapdl_core import _MapdlCore

from .. import _ExtendedMixinBase


class _ExtendedComponentMixin(_ExtendedMixinBase):
    """Extended component commands."""
    @wraps(_MapdlCore.cmlist)
    def cmlist(self, *args, **kwargs):
        from ansys.mapdl.core.commands import ComponentListing

        return ComponentListing(super().cmlist(*args, **kwargs))
