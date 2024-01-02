from ansys.mapdl.core.mapdl_extended import _MapdlExtended


class MapdlBase(_MapdlExtended):
    """Base MAPDL class shared across all MAPDL subclasses.

    .. warning:: This class should NOT be imported by itself.
       You should always import a subclass of it
    """

    pass
