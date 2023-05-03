from typing import Any
import weakref

import numpy as np

from ansys.mapdl.core.mapdl import _MapdlCore


class Component:
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
        self._comp = None

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _set_log_level(self, level):
        self._mapdl.set_log_level(level)

    @property
    def _log(self):
        return self._mapdl._log

    def __getitem__(self, __key: Any) -> Any:
        self._comp = self._mapdl._parse_cmlist()
        try:
            cmtype = self._comp[__key.upper()]
        except KeyError:
            raise KeyError(
                f"The component named '{__key}' does not exist in the MAPDL instance."
            )
        return self._mapdl._parse_cmlist_indiv(__key, cmtype)

    def __setitem__(self, __key: Any, __value: Any) -> None:
        if isinstance(__value, tuple):
            if len(__value) != 2:
                raise ValueError(
                    "Only two values are allowed for assignment. The first one a string with the type name and the second a list or numpy array with the selected elements"
                )
            if not isinstance(__value[0], str) or not isinstance(
                __value[1], (list, np.array)
            ):
                raise ValueError(
                    "Only strings are allowed for the first argument, and a list or numpy array for the second."
                )

            cmtype = __value[0]
            cmitems = __value[1]

            # Save current selection

            # Select the cmitems entities

            # create component

            # reselecting previous selection
            for i in cmitems:
                self._mapdl.run()

        elif isinstance(__value, str):
            # create a component with the already selected elements
            cmtype = __value

        else:
            raise ValueError("Only strings or tuples are allowed for assignment.")

        # type_ =
        self._mapdl.cm("")

    def __repr__(self):
        """Return the current parameters in a pretty format"""
        lines = ["MAPDL Components", "----------------"]
        if self._comp:
            for key, item in self._comp:
                lines.append("%-32s : %s" % (key, item))

        return "\n".join(lines)
