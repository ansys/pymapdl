from typing import Any
import weakref

from ansys.mapdl.core.mapdl import _MapdlCore


class Component(dict):
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if __key not in ["type", "items"]:
            raise KeyError(f"The key '{__key}' is not allowed in 'Component' class.")

        if __key == "type":
            if not isinstance(__value, str) or __value.upper() not in [
                "NODE",
                "ELEM",
                "VOLU",
                "AREA",
                "LINE",
                "KP",
            ]:
                raise ValueError(
                    f"The value '{__value}' is not allowed for 'type' definition."
                )
        return super().__setitem__(__key, __value)

    @property
    def type(self):
        return super().__getitem__("type")

    @property
    def items(self):
        return super().__getitem__("items")


class ComponentManager(dict):
    def __init__(self, mapdl):
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError("Must be implemented from MAPDL class")
        self._mapdl_weakref = weakref.ref(mapdl)

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _set_log_level(self, level):
        self._mapdl.set_log_level(level)

    @property
    def _log(self):
        return self._mapdl._log
