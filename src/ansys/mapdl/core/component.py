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

    if not all([isinstance(each, (int, np.integer)) for each in items]):
        raise ValueError("Only integers are allowed for component definition.")


class Component(dict):
    def __setitem__(self, key: Any, value: Any) -> None:
        if key not in ["type", "items"]:
            raise KeyError(f"The key '{key}' is not allowed in 'Component' class.")

        if key == "type":
            if not isinstance(value, str) or value.upper() not in VALID_ENTITIES:
                raise ValueError(
                    f"The value '{value[0]}' is not allowed for 'type' definition."
                )
        return super().__setitem__(key, value)

    @property
    def type(self):
        return super().__getitem__("type")

    @property
    def items(self):
        return super().__getitem__("items")


class ComponentManager(dict):
    def __init__(self, mapdl: _MapdlCore) -> None:
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError("Must be implemented from MAPDL class")

        self._mapdl_weakref = weakref.ref(mapdl)
        self.__comp = None
        self._update_always = True

    @property
    def _mapdl(self) -> _MapdlCore:
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _set_log_level(self, level):
        self._mapdl.set_log_level(level)

    @property
    def _log(self):
        return self._mapdl._log

    @property
    def _comp(self):
        if self.__comp is None or self._update_always:
            self.__comp = self._mapdl._parse_cmlist()
        return self.__comp

    @_comp.setter
    def _comp(self, value):
        self.__comp = value

    def __getitem__(self, key: Any) -> Any:
        self._comp = self._mapdl._parse_cmlist()
        try:
            cmtype = self._comp[key.upper()]
        except KeyError:
            raise KeyError(
                f"The component named '{key}' does not exist in the MAPDL instance."
            )
        return self._mapdl._parse_cmlist_indiv(key, cmtype)

    def __setitem__(self, key: Any, value: Any) -> None:
        if not isinstance(key, str):
            raise ValueError("Only strings are allowed for component names.")

        if isinstance(value, tuple):
            if len(value) != 2:
                raise ValueError(
                    "Only two values are allowed for assignment. The first one a string with the type name and the second a list or numpy array with the selected elements"
                )
            if not isinstance(value[0], str) or not isinstance(
                value[1], (list, np.ndarray)
            ):
                raise ValueError(
                    "Only strings are allowed for the first argument, and a list or numpy array for the second."
                )

            if value[0].upper() not in VALID_ENTITIES:
                raise ValueError(
                    f"The value '{value}' is not allowed for 'type' definition."
                )

            cmname = key
            cmtype = value[0].upper()
            cmitems = value[1]

        elif isinstance(value, str):
            # create a component with the already selected elements
            cmname = key
            cmtype = value

            self._mapdl.cm(cmname, cmtype)

            return  # Early exit

        elif isinstance(value, (list, np.ndarray)):
            # Assuming we are defining a CM with nodes
            warnings.warn(
                "Assuming a NODE selection. It is recommended you use the following notation to avoid this warning:\n>>> mapdl.components['mycomp'] = 'nodes', [1, 2, 3,4]"
            )

            cmname = key
            cmtype = "NODES"
            cmitems = value

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

    def __repr__(self) -> str:
        """Return the current components in a pretty format"""
        lines = ["MAPDL Components", "----------------"]
        if self._comp:
            for key, item in self._comp.items():
                lines.append("%-32s : %s" % (key, item))

        return "\n".join(lines)

    def __contains__(self, key) -> bool:
        """
        Check if a given key is present in the dictionary.

        Parameters
        ----------
        key : hashable
            The key to search for in the dictionary.

        Returns
        -------
        bool
            True if the key is in the dictionary, False otherwise.

        """
        return key.upper() in self._comp.keys()

    def __iter__(self):
        """
        Return an iterator over the keys in the dictionary.

        Returns
        -------
        iterator
            An iterator over the keys in the dictionary.

        """
        yield from self._comp.keys()

    def keys(self):
        """
        Return a view object that contains the keys in the dictionary.

        Returns
        -------
        dict_keys
            A view object that contains the keys in the dictionary.

        """
        return self._comp.keys()

    def values(self):
        """
        Return a view object that contains the values in the dictionary.

        Returns
        -------
        dict_values
            A view object that contains the values in the dictionary.

        """
        return self._comp.values()

    def copy(self):
        """
        Return a shallow copy of the dictionary.

        Returns
        -------
        dict
            A shallow copy of the dictionary.

        """
        return self._comp.copy()

    def items(self):
        """
        Return a view object that contains the key-value pairs in the dictionary.

        Returns
        -------
        dict_items
            A view object that contains the key-value pairs in the dictionary.

        """
        return self._comp.items()
