from typing import Any
import warnings
import weakref

import numpy as np

from ansys.mapdl.core.mapdl import _MapdlCore

ENTITIES_MAPPING = {
    "NODE": "NSEL",
    "NODES": "NSEL",
    "ELEM": "ESEL",
    "ELEMS": "ESEL",
    "ELEMENTS": "ESEL",
    "VOLU": "VSEL",
    "AREA": "ASEL",
    "LINE": "LSEL",
    "KP": "KSEL",
}

VALID_ENTITIES = list(ENTITIES_MAPPING.keys())


def _check_valid_pyobj_to_entities(items):
    """Check whether the python objects can be converted to entities.
    At the moment, only list and numpy arrays of ints are allowed.
    """
    if not isinstance(items, (list, np.ndarray)):
        raise TypeError(
            "Only list or numpy arrays are allowed for component definitions."
        )

    if not all([isinstance(each, (int, np.int_)) for each in items]):
        raise ValueError("Only integers are allowed for component definition.")


class Component:
    def __setitem__(self, __key: Any, __value: Any) -> None:
        if __key not in ["type", "items"]:
            raise KeyError(f"The key '{__key}' is not allowed in 'Component' class.")

        if __key == "type":
            if not isinstance(__value, str) or __value.upper() not in VALID_ENTITIES:
                raise ValueError(
                    f"The value '{__value[0]}' is not allowed for 'type' definition."
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
        if not isinstance(__key, str):
            raise ValueError("Only strings are allowed for component names.")

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

            if __value[0].upper() not in VALID_ENTITIES:
                raise ValueError(
                    f"The value '{__value}' is not allowed for 'type' definition."
                )

            cmname = __key
            cmtype = __value[0].upper()
            cmitems = __value[1]

        elif isinstance(__value, str):
            # create a component with the already selected elements
            cmname = __key
            cmtype = __value

            self._mapdl.cm(cmname, cmtype)

            return  # Early exit

        elif isinstance(__value, (list, np.ndarray)):
            # Assuming we are defining a CM with  nodes
            warnings.warn(
                "Assuming a NODE selection. It is recommended you use the following notation to avoid this warning:\n>>> mapdl.components['mycomp'] = 'nodes', [1, 2, 3,4]"
            )

            cmname = __key
            cmtype = "NODES"
            cmitems = __value

        else:
            raise ValueError("Only strings or tuples are allowed for assignment.")

        _check_valid_pyobj_to_entities(cmitems)

        # Save current selection
        self._mapdl.cm("__temp_comp__", cmtype)

        # Select the cmitems entities
        func = getattr(self._mapdl, ENTITIES_MAPPING[cmtype].lower())
        func(type_="S", vmin=cmitems)

        # create component
        self._mapdl.cm(cmname, cmtype)

        # reselecting previous selection
        self._mapdl.cmsel("S", "__temp_comp__")
        self._mapdl.cmdele("__temp_comp__")

    def __repr__(self):
        """Return the current parameters in a pretty format"""
        lines = ["MAPDL Components", "----------------"]
        if self._comp:
            for key, item in self._comp:
                lines.append("%-32s : %s" % (key, item))

        return "\n".join(lines)
