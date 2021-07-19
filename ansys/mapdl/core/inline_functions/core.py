import warnings
from enum import IntEnum


class SelectionStatus(IntEnum):
    """Enumeration class for selection status information.

    This class is used with methods on the ``Query`` class and has the
    following options.

    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1

    Examples
    --------
    The following example is taken from ``Query.nsel`` and demonstrates
    how `SelectionSatus` appears in PyMAPDL.

    Here we create a single node and interrogate its selection
    status.

    >>> from ansys.mapdl.core import launch_mapdl
    >>> from ansys.mapdl.core.inline_functions import Query
    >>> mapdl = launch_mapdl()
    >>> mapdl.prep7()
    >>> n1 = mapdl.n(1, 0, 0, 0)
    >>> n1
    1

    We can use ``Query.nsel`` to interrogate the selection status
    of the node. The response is an ``enum.IntEnum`` object. If
    you query a node that does not exist, it will return a status
    ``SelectionStatus.UNDEFINED``.

    >>> q = Query(mapdl)
    >>> q.nsel(n1)
    <SelectionStatus.SELECTED: 1>
    >>> mapdl.nsel('NONE')
    >>> q.nsel(n1)
    <SelectionStatus.UNSELECTED: -1>
    >>> q.nsel(0)
    <SelectionStatus.UNDEFINED: 0>
    """
    UNSELECTED = -1
    UNDEFINED = 0
    SELECTED = 1


class _ParameterParsing:
    def _parse_parameter_integer_response(self, response) -> int:
        return int(self._parse_parameter_float_response(response))

    @staticmethod
    def _parse_parameter_float_response(response) -> float:
        if 'PARAMETER' not in response or '=' not in response:
            raise TypeError(f'Parameter response not recognised: '
                            f'"{response}"')
        parts = response.rsplit('=', 1)
        if 'WARNING' in parts[0]:
            warnings.warn(parts[0])

        number = parts[1].strip()
        return float(number)