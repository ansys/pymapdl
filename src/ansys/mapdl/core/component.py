"""Component related module"""

from typing import TYPE_CHECKING, Any, Literal, Optional, Union, get_args
import warnings
import weakref

import numpy as np
from numpy.typing import NDArray

from ansys.mapdl.core.errors import ComponentDoesNotExits, ComponentIsNotSelected
from ansys.mapdl.core.mapdl import _MapdlCore

if TYPE_CHECKING:  # pragma: no cover
    import logging

ENTITIES_TYP = Literal[
    "NODE", "NODES", "ELEM", "ELEMS", "ELEMENTS", "VOLU", "AREA", "LINE", "KP"
]

VALID_ENTITIES = list(get_args(ENTITIES_TYP))

SELECTOR_FUNCTION = [
    "NSEL",
    "NSEL",
    "ESEL",
    "ESEL",
    "ESEL",
    "VSEL",
    "ASEL",
    "LSEL",
    "KSEL",
]

ENTITIES_MAPPING = {
    entity.upper(): func for entity, func in zip(VALID_ENTITIES, SELECTOR_FUNCTION)
}


ITEMS_VALUES = Optional[Union[str, int, list[int], NDArray[Any]]]
UNDERLYING_DICT = dict[str, ITEMS_VALUES]

warning_entity = (
    "Assuming a {default_entity} selection.\n"
    "It is recommended you use the following notation to avoid this warning:\n"
    ">>> mapdl.components['{key}'] = '{default_entity}' {value}\n"
    "Alternatively, you disable this warning using:\n"
    ">>> mapdl.components.default_entity_warning=False"
)


def _check_valid_pyobj_to_entities(
    items: Union[tuple[int, ...], list[int], NDArray[Any]]
):
    """Check whether the python objects can be converted to entities.
    At the moment, only list and numpy arrays of ints are allowed.
    """

    if not all([isinstance(each, (int, np.integer)) for each in items]):
        raise ValueError("Only integers are allowed for component definition.")


class Component(tuple):
    """Component object

    Object which contain the definition of a component.

    Parameters
    ----------
    type_ : str
        The entity type. For instance "NODES", "KP", "VOLU", etc

    items_ : Optional[Union[str, int, list[int], NDArray[Any]]]
        Item ids contained in the component.

    Examples
    --------
    To create a component object

    >>> mycomp = Component("NODES", [1, 2, 3])
    >>>  mycomp
    Component(type='NODES', items=(1, 2, 3))

    To index the content of the component object:
    >>> mycomp[0]
    1
    >>> mycomp[1]
    2

    To access the type of the entities:
    >>> mycomp.type
    "NODES"

    Convert to list:
    >>> list(mycomp)
    [1, 2, 3]
    """

    def __new__(cls, type_: ENTITIES_TYP, items_: tuple):
        if not isinstance(type_, str) or type_.upper() not in VALID_ENTITIES:
            raise ValueError(
                f"The value '{type_}' is not allowed for 'type' definition."
            )
        obj = super().__new__(cls, items_)
        obj.type = type_

        return obj

    def __str__(self):
        tup_str = super().__str__()
        return f"Component(type='{self.type}', items={tup_str})"

    def __repr__(self) -> str:
        tup_str = super().__repr__()
        return f"Component(type='{self.type}', items={tup_str})"


class ComponentManager:
    """Collection of MAPDL components.

    Notes
    -----

    **Components need to be selected** using
    :attr:`Mapdl.cmsel() <ansys.mapdl.core.Mapdl.cmsel>` before
    being listed in :attr:`Mapdl.components <ansys.mapdl.core.Mapdl.components>`

    Examples
    --------
    Simply list all the *selected* components:

    >>> mapdl.components
    MAPDL Components
    ----------------
    MYCOMP1                          : NODE
    MYCOMP2                          : ELEM

    Get a component:
    >>> mapdl.components["mycomp1"]
    Component(type='NODE', items=(1, 3, 6))

    Set a component specifying the type and items:
    >>> mapdl.components["mycomp3] = "KP", [1,2,3]

    Set a component without specifying the type, by default it is ``NODE``:
    >>> mapdl.components["mycomp4"] = (1, 2, 3)

    You can change the default type by changing
    :attr:`Mapdl.components.default_entity <ansys.mapdl.core.Mapdl.components.default_entity>`
    >>> mapdl.component.default_entity = "KP"
        /Users/german.ayuso/pymapdl/src/ansys/mapdl/core/component.py:282: UserWarning: Assuming a NODES selection.
        It is recommended you use the following notation to avoid this warning:
        \>\>\> mapdl.components['mycomp3'] = 'NODES' (1, 2, 3)
        Alternatively, you disable this warning using
    >>> mapdl.component["mycomp] = [1, 2, 3]
    >>> mapdl.component["mycomp"].type
    'KP'

    You can also create a component from the already selected entities:
    >>> mapdl.lsel("S",1, 2)
    >>> mapdl.components["mylinecomp"] = "LINE"
    >>> mapdl.components["mylinecomp"]
    (1, 2)

    Selecting a component and retrieving it:
    >>> mapdl.cmsel("s", "mycomp3")
    >>> mapdl.components["mycomp3"]
    Component(type='KP', items=(1, 2, 3))
    """

    def __init__(self, mapdl: _MapdlCore) -> None:
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError("Must be implemented from MAPDL class")

        self._mapdl_weakref: weakref.ReferenceType[_MapdlCore] = weakref.ref(mapdl)
        self.__comp: UNDERLYING_DICT = {}
        self._update_always: bool = True
        self._lose_mode: bool = False  # if True, PyMAPDL will try to select the CM first if it does not appear in the CMLIST output.

        self._default_entity: ENTITIES_TYP = "NODES"
        self._default_entity_warning: bool = True

    @property
    def default_entity(self):
        return self._default_entity

    @default_entity.setter
    def default_entity(self, value: ENTITIES_TYP):
        if not isinstance(value, str) or value.upper() not in VALID_ENTITIES:
            raise ValueError(
                f"Only the following entities are allowed:\n{', '.join(VALID_ENTITIES)}"
            )
        self._default_entity = value.upper()

    @property
    def default_entity_warning(self):
        return self._default_entity_warning

    @default_entity_warning.setter
    def default_entity_warning(self, value: bool):
        self._default_entity_warning = value

    @property
    def _mapdl(self) -> _MapdlCore:
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _log(self) -> "logging.Logger":
        return self._mapdl.logger

    @property
    def logger(self) -> "logging.Logger":
        return self._log()

    @property
    def _comp(self) -> UNDERLYING_DICT:
        if self.__comp is None or self._update_always:
            self.__comp = self._mapdl._parse_cmlist()
        return self.__comp

    @_comp.setter
    def _comp(self, value):
        self.__comp = value

    def __getitem__(self, key: str) -> ITEMS_VALUES:
        self._comp = self._mapdl._parse_cmlist()
        forced_to_select = False

        if key.upper() not in self._comp and self._lose_mode:
            # the component will not appear in "cmlist" if it has not been selected
            # previously using "cmsel". This behaviour is a bit different than with
            # parameters for example. However it is consistent with geometry definition.
            # Then this API might look a bit confusing, because it resemble parameters,
            # but requires to select the CM.
            self._mapdl.cmsel("A", key)
            forced_to_select = True

        try:
            cmtype = self._comp[key.upper()]
        except KeyError:
            # testing if the CM exists or not
            # it seems you can use `*get` with components which are not selected.
            # It will return 0 if it does not exists.
            if self._mapdl.get_value("COMP", key, "type"):
                # the component exits, but it might not be selected
                raise ComponentIsNotSelected(
                    f"The component named '{key}' is not selected. Use 'mapdl.cmsel' to select it."
                )
            else:
                raise ComponentDoesNotExits(
                    f"The component named '{key}' does not exist in the MAPDL instance."
                )

        output = self._mapdl._parse_cmlist_indiv(key, cmtype)
        if forced_to_select:
            # Unselect to keep the state of the things as before calling this method.
            self._mapdl.cmsel("U", key)

        return Component(cmtype, output)

    def __setitem__(self, key: str, value: ITEMS_VALUES) -> None:
        if not isinstance(key, str):
            raise ValueError("Only strings are allowed for component names.")

        if isinstance(value, Component):
            # Allowing to use a component object to be set.
            cmname = key
            cmtype = value.type
            cmitems = value

        elif isinstance(value, tuple):
            if len(value) == 2:
                if not isinstance(value[0], str) or not isinstance(
                    value[1], (list, tuple, np.ndarray)
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

            else:
                # Asumng default entity
                if self.default_entity_warning:
                    warnings.warn(
                        warning_entity.format(
                            default_entity=self.default_entity,
                            key=key,
                            value=value,
                        ),
                        UserWarning,
                    )

                cmname = key
                cmtype = self.default_entity
                cmitems = value

        elif isinstance(value, str):
            # create a component with the already selected elements
            if value.upper() not in VALID_ENTITIES:
                raise ValueError(
                    f"The value '{value}' is not allowed for 'type' definition."
                )

            cmname = key
            cmtype = value

            self._mapdl.cm(cmname, cmtype)

            return  # Early exit

        elif isinstance(value, (list, np.ndarray)):
            # Assuming we are defining a CM with nodes
            if self.default_entity_warning:
                warnings.warn(
                    warning_entity.format(
                        default_entity=self.default_entity,
                        key=key,
                        value=value,
                    ),
                    UserWarning,
                )

            cmname = key
            cmtype = self.default_entity
            cmitems = value

        else:
            raise ValueError("Only strings or tuples are allowed for assignment.")

        _check_valid_pyobj_to_entities(cmitems)

        # Save current selection
        self._mapdl.cm("__temp__", cmtype)

        # Select the cmitems entities
        func = getattr(self._mapdl, ENTITIES_MAPPING[cmtype].lower())
        func(type_="S", vmin=cmitems)

        # create component
        self._mapdl.cm(cmname, cmtype)

        # reselecting previous selection
        self._mapdl.cmsel("S", "__temp__")
        self._mapdl.cmdele("__temp__")

    def __repr__(self) -> str:
        """Return the current components in a pretty format"""
        lines = ["MAPDL Components", "----------------"]
        if self._comp:
            for key, item in self._comp.items():
                lines.append("%-32s : %s" % (key, item))

        return "\n".join(lines)

    def __contains__(self, key: str) -> bool:
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


    def items(self):
        """
        Return a view object that contains the key-value pairs in the dictionary.

        Returns
        -------
        dict_items
            A view object that contains the key-value pairs in the dictionary.

        """
        return self._comp.items()
