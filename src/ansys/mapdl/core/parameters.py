import os
import re
import tempfile
import weakref

try:
    from ansys.mapdl.reader._reader import write_array

    _HAS_READER = True
except ModuleNotFoundError:  # pragma: no cover
    from ansys.mapdl.core.misc import write_array

    _HAS_READER = False

import numpy as np

from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.mapdl import _MapdlCore
from ansys.mapdl.core.misc import supress_logging

ROUTINE_MAP = {
    0: "Begin level",
    17: "PREP7",
    21: "SOLUTION",
    31: "POST1",
    36: "POST26",
    52: "AUX2",
    53: "AUX3",
    62: "AUX12",
    65: "AUX15",
}

UNITS_MAP = {
    -1: "NONE",
    0: "USER",
    1: "SI",
    2: "CGS",
    3: "BFT",
    4: "BIN",
    5: "MKS",
    6: "MPA",
    7: "uMKS",
}


class Parameters:
    """Collection of MAPDL parameters.

    Notes
    -----

    See :ref:`ref_parameters` for additional notes.

    Examples
    --------
    Simply list all parameters except for MAPDL MATH parameters.

    >>> mapdl.parameters
    ARR                              : ARRAY DIM (3, 1, 1)
    PARM_FLOAT                       : 20.0
    PARM_INT                         : 10.0
    PARM_LONG_STR                    : "stringstringstringstringstringst"
    PARM_STR                         : "string"
    PORT                             : 50052.0

    Get a parameter

    >>> mapdl.parameters['PARM_FLOAT']
    20.0

    Get an array parameter

    >>> mapdl.parameters['ARR']
    array([1., 2., 3.])

    """

    def __init__(self, mapdl):
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError("Must be implemented from MAPDL class")
        self._mapdl_weakref = weakref.ref(mapdl)
        self.show_leading_underscore_parameters = False
        self.show_trailing_underscore_parameters = False
        self.full_parameters_output = self._full_parameter_output(self)

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def _set_log_level(self, level):
        self._mapdl.set_log_level(level)

    @property
    def _log(self):
        return self._mapdl._log

    @property
    def numcpu(self) -> int:
        """Number of Distributed MAPDL processes being used.

        Notes
        -----
        This will always return ``1`` when using shared memory parallel.

        Examples
        --------
        >>> mapdl.parameters.numcpu
        2

        """
        return int(self._mapdl.get_value("ACTIVE", item1="NUMCPU"))

    @property
    def routine(self) -> str:
        """Current routine string as a string.  For example ``"/PREP7"``

        MAPDL Command: \*GET, ACTIVE, 0, ROUT

        Returns
        -------
        routine : str
            Routine as a string.  One of:

                - ``"Begin level"``
                - ``"PREP7"``
                - ``"SOLUTION"``
                - ``"POST1"``
                - ``"POST26"``
                - ``"AUX2"``
                - ``"AUX3"``
                - ``"AUX12"``
                - ``"AUX15"``

        Examples
        --------
        >>> mapdl.parameters.routine
        'PREP7'
        """
        value = self._mapdl.get_value("ACTIVE", item1="ROUT")
        return ROUTINE_MAP[int(value)]

    @property
    def units(self) -> str:
        """Units specified by /UNITS command.

        Returns
        -------
        units : str
            Active Units.  One of:
                - ``"None"``
                - ``"USER"``
                - ``"SI"``
                - ``"CGS"``
                - ``"BFT"``
                - ``"BIN"``
                - ``"MKS``
                - ``"MPA"``
                - ``"uMKS"``

        Examples
        --------
        >>> mapdl.parameters.units
        'NONE'
        """
        value = self._mapdl.get_value("ACTIVE", item1="UNITS")
        return UNITS_MAP[int(value)]

    @property
    def revision(self) -> float:
        """MAPDL revision version.

        Examples
        --------
        >>> mapdl.parameters.revision
        20.2
        """
        return float(self._mapdl.get_value("ACTIVE", item1="REV"))

    @property
    def platform(self) -> str:
        """The current platform.

        Examples
        --------
        >>> mapdl.parameters.platform
        'LIN'
        """
        return self._mapdl.get_value("ACTIVE", item1="PLATFORM")

    @property
    def csys(self) -> int:
        """Active coordinate system

        Examples
        --------
        >>> mapdl.parameters.csys
        0
        """
        return int(self._mapdl.get_value("ACTIVE", item1="CSYS"))

    @property
    def dsys(self) -> int:
        """Active display coordinate system

        Examples
        --------
        >>> mapdl.parameters.dsys
        0
        """
        return int(self._mapdl.get_value("ACTIVE", item1="DSYS"))

    @property
    def rsys(self) -> int:
        """Active result coordinate system

        Examples
        --------
        >>> mapdl.parameters.rsys
        0
        """
        return int(self._mapdl.get_value("ACTIVE", item1="RSYS"))

    @property
    def esys(self) -> int:
        """Active element coordinate system

        Examples
        --------
        >>> mapdl.parameters.esys
        0
        """
        return int(self._mapdl.get_value("ACTIVE", item1="ESYS"))

    @property
    def section(self) -> int:
        """Active section number

        Examples
        --------
        >>> mapdl.parameters.section
        1
        """
        return int(self._mapdl.get_value("ACTIVE", item1="SECT"))

    @property
    def material(self) -> int:
        """Active material

        Examples
        --------
        >>> mapdl.parameters.material
        1
        """
        return int(self._mapdl.get_value("ACTIVE", item1="MAT"))

    @property
    def real(self) -> int:
        """Active real constant set

        Examples
        --------
        >>> mapdl.parameters.real
        1
        """
        return int(self._mapdl.get_value("ACTIVE", item1="REAL"))

    @property
    def type(self) -> int:
        """Active element type

        Examples
        --------
        >>> mapdl.parameters.type
        1
        """
        return int(self._mapdl.get_value("ACTIVE", item1="type"))

    @property
    @supress_logging
    def _parm(self):
        """Current MAPDL parameters"""
        params = interp_star_status(self._mapdl.starstatus(avoid_non_interactive=True))

        if self.show_leading_underscore_parameters:
            _params = interp_star_status(self._mapdl.starstatus("_PRM"))
            params.update(_params)

        if self.show_trailing_underscore_parameters:
            params_ = interp_star_status(self._mapdl.starstatus("PRM_"))
            params.update(params_)

        return params

    def __repr__(self):
        """Return the current parameters in a pretty format"""
        lines = ["MAPDL Parameters", "----------------"]
        for key, info in self._parm.items():
            value_str = ""
            if info["type"] == "ARRAY":
                value_str = "ARRAY DIM %s" % str(info["shape"])
            elif info["type"] == "TABLE":
                value_str = "TABLE DIM %s" % str(info["shape"])
            elif info["type"] == "CHARACTER":
                value_str = '"%s"' % info["value"]
            elif "value" in info:
                value_str = str(info["value"])
            else:
                continue
            lines.append("%-32s : %s" % (key, value_str))
        return "\n".join(lines)

    def __getitem__(self, key):
        """Return a parameter"""
        if not isinstance(key, str):
            raise TypeError("Parameter name must be a string")
        key = key.upper()

        with self.full_parameters_output:
            parameters = self._parm

        if key not in parameters:
            try:
                val_ = interp_star_status(self._mapdl.starstatus(key))
                val_ = val_[list(val_.keys())[0]]["value"]
                if len(val_) == 1:
                    return val_[0]
                else:
                    return val_
                return
            except MapdlRuntimeError:
                raise IndexError("%s not a valid parameter_name" % key)

        parm = parameters[key]
        if parm["type"] in ["ARRAY", "TABLE"]:  # Array case
            try:
                return self._get_parameter_array(key, parm["shape"])
            except ValueError:
                # allow a second attempt
                return self._get_parameter_array(key, parm["shape"])
        else:
            if "grpc" in self._mapdl.name.lower() and parm["type"] not in ["CHARACTER"]:
                return self._mapdl.scalar_param(key)  # Only works with numbers
            else:
                return parm["value"]

    def __setitem__(self, key, value):
        """Set a parameter"""
        self._mapdl._check_parameter_name(key)

        # parameters = self._parm  # check parameter exists
        if isinstance(value, (np.ndarray, list)):
            self._set_parameter_array(key, value)
        else:
            self._set_parameter(key, value)

    def __contains__(self, key):
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
        return key.upper() in self._parm.keys()

    def __iter__(self):
        """
        Return an iterator over the keys in the dictionary.

        Returns
        -------
        iterator
            An iterator over the keys in the dictionary.

        """
        yield from self._parm.keys()

    def keys(self):
        """
        Return a view object that contains the keys in the dictionary.

        Returns
        -------
        dict_keys
            A view object that contains the keys in the dictionary.

        """
        return self._parm.keys()

    def values(self):
        """
        Return a view object that contains the values in the dictionary.

        Returns
        -------
        dict_values
            A view object that contains the values in the dictionary.

        """
        return self._parm.values()

    def copy(self):
        """
        Return a shallow copy of the dictionary.

        Returns
        -------
        dict
            A shallow copy of the dictionary.

        """
        return self._parm.copy()

    def items(self):
        """
        Return a view object that contains the key-value pairs in the dictionary.

        Returns
        -------
        dict_items
            A view object that contains the key-value pairs in the dictionary.

        """
        return self._parm.items()

    @supress_logging
    def _set_parameter(self, name, value):
        """Set a single parameter within MAPDL

        Parameters
        ----------
        name : str
            An alphanumeric name used to identify this parameter.  Name
            may be up to 32 characters, beginning with a letter and
            containing only letters, numbers, and underscores.
            Examples: ``"ABC" "A3X" "TOP_END"``.

        """
        if not isinstance(value, (str, int, float)):
            raise TypeError("``Parameter`` must be either a float, int, or string")

        if isinstance(value, str) and len(value) >= 32:
            raise ValueError("Length of ``value`` must be 32 characters or less")

        if not isinstance(name, str):
            raise TypeError("``name`` must be a string")

        if len(name) >= 32:
            raise ValueError("Length of ``name`` must be 32 characters or less")

        # delete the parameter if it exists as an array
        parm = self._parm
        if name in parm:
            if parm[name]["type"] == "ARRAY":
                self._mapdl.starset(name, mute=True)

        if isinstance(value, str):
            if " " in value:
                raise ValueError("Spaces not allowed in strings in MAPDL")
            self._mapdl.starset(name, f"'{value}'", mute=True)
        else:
            self._mapdl.starset(name, value, mute=True)

    @supress_logging
    def _get_parameter_array(self, parm_name, shape):
        """Return an ANSYS array parameter as a numpy.ndarray

        Parameters
        ----------
        parm_name : str
            MAPDL parameter name.

        Returns
        -------
        array : np.ndarray
            Numpy array.
        """
        escaped = False
        for each_format_number in [20, 30, 40, 64, 100]:
            format_str = f"(1F{each_format_number}.12)"
            with self._mapdl.non_interactive:
                # use C ordering
                self._mapdl.mwrite(parm_name.upper(), label="kji")
                self._mapdl.run(format_str)

            st = self._mapdl.last_response.rfind(format_str) + len(format_str) + 1
            output = self._mapdl.last_response[st:]

            if "**" not in output:
                escaped = True
                break

        if not escaped:  # pragma: no cover
            raise MapdlRuntimeError(
                f"The array '{parm_name}' has a number format "
                "that could not be read using '{format_str}'."
            )

        arr_flat = np.fromstring(output, sep="\n").reshape(shape)

        if len(shape) == 3:
            if shape[2] == 1:
                arr_flat = arr_flat.squeeze(axis=2)

        return arr_flat

    @supress_logging
    def _set_parameter_array(self, name, arr):
        """Load a numpy array or python list directly to MAPDL

        Writes the numpy array to disk and then reads it in within
        MAPDL using \*VREAD.

        Parameters
        ----------
        arr : np.ndarray or List
            Array to send to MAPDL.  Maximum of 3 dimensions.

        name : str
            Name of the array to write to within MAPDL.

        Examples
        --------
        Load a 1D numpy array into MAPDL

        >>> arr = np.array([10, 20, 30])
        >>> mapdl.set_parameter_array(arr, 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([10., 20., 30.])

        Load a 2D numpy array into MAPDL

        >>> arr = np.random.random((5, 3))
        >>> mapdl.set_parameter_array(arr, 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([[0.39806635, 0.15060953, 0.3990557 ],
               [0.26837768, 0.02033222, 0.15655861],
               [0.46110226, 0.06381489, 0.20068533],
               [0.20122863, 0.5727896 , 0.85636037],
               [0.68126612, 0.67460878, 0.3678797 ]])

        Load a python list into MAPDL

        >>> mapdl.set_parameter_array([10, -1, 8, 4, 10], 'MYARR')
        >>> parm, mapdl_arrays = mapdl.load_parameters()
        >>> mapdl_arrays['MYARR']
        array([10., -1.,  8.,  4., 10.])

        """
        # type checks
        arr = np.array(arr)
        if not np.issubdtype(arr.dtype, np.number):
            raise TypeError("Only numerical arrays or lists are supported")
        if arr.ndim > 3:
            raise ValueError(
                "MAPDL VREAD only supports a arrays with a" " maximum of 3 dimensions."
            )

        if not isinstance(name, str):
            raise TypeError("``name`` must be a string")

        name = name.upper()

        idim, jdim, kdim = arr.shape[0], 1, 1
        if arr.ndim >= 2:
            jdim = arr.shape[1]
        if arr.ndim == 3:
            kdim = arr.shape[2]

        # 2021R1 and earlier has stability issues.  Directly stream
        # results for improved performance and stability, but up to a
        # size limit.
        if arr.size < 1000:
            return self._set_array_chain(name, arr, idim, jdim, kdim)

        # write array from numpy to disk
        filename = "_tmp.dat"
        self._write_numpy_array(filename, arr)

        cmd = f"{name}(1, 1),{filename},,,IJK,{idim},{jdim},{kdim}"
        with self._mapdl.non_interactive:
            self._mapdl.dim(name, imax=idim, jmax=jdim, kmax=kdim)
            self._mapdl.vread(cmd)
            self._mapdl.run("(1F20.12)")

    def _set_array_chain(self, name, arr, idim, jdim, kdim):
        """Sets an array using chained commands

        Faster and more stable (as of 2021R1) for small arrays.
        """
        if arr.ndim == 1:
            arr = np.expand_dims(arr, [1, 2])
        elif arr.ndim == 2:
            arr = np.expand_dims(arr, 2)

        # backwards compatibility with CORBA
        if hasattr(self._mapdl, "mute"):
            old_mute = self._mapdl.mute
            self._mapdl.mute = True

        with self._mapdl.non_interactive:
            self._mapdl.dim(name, imax=idim, jmax=jdim, kmax=kdim)
            for i in range(idim):
                for j in range(jdim):
                    for k in range(kdim):
                        index = f"{i + 1},{j + 1},{k + 1}"
                        self._mapdl.run(f"{name}({index})={arr[i, j, k]}")

        if hasattr(self._mapdl, "mute"):
            self._mapdl.mute = old_mute

    def _write_numpy_array(self, filename, arr):
        """Write a numpy array to disk"""
        if arr.dtype != np.double:
            arr = arr.astype(np.double)

        if self._mapdl._local:
            filename = os.path.join(self._mapdl.directory, filename)
        else:
            filename = os.path.join(tempfile.gettempdir(), filename)
        write_array(filename.encode(), arr.ravel("F"))

        if not self._mapdl._local:
            self._mapdl.upload(filename, progress_bar=False)

    def __delitem__(self, parameter):
        parameter = parameter.upper()
        if parameter in self:
            self._parm.__delitem__(parameter)
            self._mapdl.run(f"{parameter}=")  # Deleting parameter in MAPDL.
        else:
            raise KeyError(f"The parameter '{parameter}' does not exist.")

    class _full_parameter_output:
        """Change the show_** options to true to allow full parameter output."""

        def __init__(self, parent):
            self._parent = weakref.ref(parent)
            self.show_leading_underscore_parameters = None
            self.show_trailing_underscore_parameters = None

        def __enter__(self):
            """Storing current state."""
            self.show_leading_underscore_parameters = (
                self._parent().show_leading_underscore_parameters
            )
            self.show_trailing_underscore_parameters = (
                self._parent().show_trailing_underscore_parameters
            )

            # Getting full output.
            self._parent().show_leading_underscore_parameters = True
            self._parent().show_trailing_underscore_parameters = True

        def __exit__(self, *args):
            """Coming back to previous state."""
            self._parent().show_leading_underscore_parameters = (
                self.show_leading_underscore_parameters
            )
            self._parent().show_trailing_underscore_parameters = (
                self.show_trailing_underscore_parameters
            )


def find_parameter_listing_line(status):
    for ind, each in enumerate(status.splitlines()):
        if "PARAMETER STATUS-" in each:
            return ind
    raise ValueError("Could not find parameter listing line")


def parameter_header(line):
    return "NAME" in line and "VALUE" in line and "TYPE" in line


def math_header(line):
    return "Name" in line and "Type" in line and "Dims" in line and "Workspace" in line


def array_header(line):
    return "LOCATION" in line and "VALUE" in line


def is_parameter_listing(status):
    return any([parameter_header(each) for each in status.splitlines()])


def is_math_listing(status):
    return any([math_header(each) for each in status.splitlines()])


def is_array_listing(status):
    return any([array_header(each) for each in status.splitlines()])


def interp_star_status(status):
    """Interprets \*STATUS command output from MAPDL

    Parameters
    ----------
    status : str
        Output from MAPDL \*STATUS

    Returns
    -------
    parameters : dict
        Dictionary of parameters.
    """
    # Exiting if there is no parameters
    if "There are no parameters defined." in status:
        return {}

    # If there is a general call to *STATUS (no arguments), the output has some extra
    # parameters that we don't want to include in the analysis.
    ind = find_parameter_listing_line(status)
    status = "\n".join(status.splitlines()[ind:])

    if "PARAMETER STATUS" not in status:
        raise ValueError(
            f"The expected output does not seem a parameter listing. \n--\n{status}"
        )

    parameters = {}
    is_string_array = False
    if is_parameter_listing(status):
        # Works for one parameter or general listing
        header = "NAME                              VALUE"
        incr = 80
    elif is_math_listing(status):
        # listing of math parameters
        header = "  Name                   Type"
        incr = 84
    elif is_array_listing(status):
        # listing of one array parameter
        header = "LOCATION                VALUE"
        incr = 30
        name_ = re.search(r"STATUS-(.*)[^\(]\(", status).group(1).strip()
    else:
        # listing of a string array
        is_string_array = True
        header = ""  # no header. Find will return 0.
        incr = sum([len(each) for each in status.splitlines()[0:2]]) + 1
        name_ = re.search(r"STATUS-(.*)[^\(]\(", status).group(1).strip()

    st = status.find(header)

    if st == -1:
        return {}

    lines = status[st + incr :].splitlines()
    elements = []
    if is_array_listing(status):
        myarray = np.array([each.split() for each in lines]).astype(float)
        idim = int(myarray[:, 0].max())
        jdim = int(myarray[:, 1].max())
        kdim = int(myarray[:, 2].max())
        myarray = np.zeros((idim, jdim, kdim))

    for line in lines:
        items = line.split()
        if not items:
            continue

        # line will contain either a character, scalar, or array
        name = items[0]
        if len(items) == 2 or "CHARACTER" in items[-1].upper():
            name = line[:32].strip()
            value = line.replace(items[-1], "")[33:].strip()
            parameters[name] = {"type": "CHARACTER", "value": value}

        elif len(items) == 3:
            if items[2] == "SCALAR":
                value = float(items[1])
            else:
                value = items[1]
            parameters[name] = {"type": items[2], "value": value}
        elif len(items) == 4:
            # it is an array or string array
            if is_array_listing(status):
                myarray[
                    int(items[0]) - 1, int(items[1]) - 1, int(items[2]) - 1
                ] = float(items[3])
            elif is_string_array:
                elements.append(items[-1])

        elif is_string_array:
            last_element = (
                re.search(r"\s*\d+\s+\d+\s+\d+\s+(.*)$", line).group(1).strip()
            )
            elements.append(last_element)

        elif len(items) == 5:
            if items[1] in ["DMAT", "VEC", "SMAT"]:
                parameters[name] = {
                    "type": items[1],
                    "MemoryMB": float(items[2]),
                    "dimensions": get_apdl_math_dimensions(items[3]),
                    "workspace": int(items[4]),
                }
            elif items[1] in ["LSENGINE"]:
                parameters[name] = {
                    "type": items[1],
                    "workspace": int(items[4]),
                }
            else:
                shape = (int(items[2]), int(items[3]), int(items[4]))
                parameters[name] = {"type": items[1], "shape": shape}

    if is_array_listing(status):
        dims = [ind for ind, each in enumerate([idim, jdim, kdim]) if each == 1]
        if dims:
            try:
                return {name_: {"type": "ARRAY", "value": myarray.squeeze(tuple(dims))}}
            except ValueError:
                return {name_: {"type": "ARRAY", "value": myarray}}
        else:
            return {name_: {"type": "ARRAY", "value": myarray}}
    elif is_string_array:
        return {name_: {"type": "STRING_ARRAY", "value": elements}}
    else:
        return parameters


def get_apdl_math_dimensions(dimensions_str):
    """Convert the dimensions string to a tuple (arrays) or int (vectors)"""
    if ":" in dimensions_str:
        return tuple([int(each) for each in dimensions_str[1:-1].split(":")])
    else:
        return int(dimensions_str)
