import os
import numpy as np

import pyansys
from pyansys.mapdl import _MapdlCore
from pyansys.misc import supress_logging

ROUTINE_MAP = {0: 'Begin level',
               17: 'PREP7',
               21: 'SOLUTION',
               31: 'POST1',
               36: 'POST26',
               52: 'AUX2',
               53: 'AUX3',
               62: 'AUX12',
               65: 'AUX15'}

UNITS_MAP = {-1: 'NONE',
             0: 'USER',
             1: 'SI',
             2: 'CGS',
             3: 'BFT',
             4: 'BIN',
             5: 'MKS',
             6: 'MPA',
             7: 'uMKS'}


class Parameters():
    """Collection of MAPDL parameters obtainable from the \*GET command"""

    def __init__(self, mapdl):
        if not isinstance(mapdl, _MapdlCore):
            raise TypeError('Must be implemented from MAPDL class')
        self._mapdl = mapdl

    def _set_log_level(self, level):
        self._mapdl.set_log_level(level)

    @property
    def _log(self):
        return self._mapdl._log

    @property
    def routine(self):
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
        value = self._mapdl.get_value('ACTIVE', item1='ROUT')
        return ROUTINE_MAP[int(value)]

    @property
    def units(self):
        """Units specified by /UNITS command.

        Returns
        -------
        units : str
            Active Units.  One of:- "USER"
            - "SI"
            - "CGS"
            - "BFT"
            - "BIN"
            - "MKS
            - "MPA"
            - "uMKS
        """
        value = self._mapdl.get_value("ACTIVE", item1="UNITS")
        return UNITS_MAP[int(value)]

    @property
    def revision(self):
        """MAPDL revision version.

        MAPDL revision version as a float.  For example ``20.2``.
        """
        return float(self._mapdl.get_value("ACTIVE", item1="REV"))

    @property
    def platform(self):
        """The current platform.

        Current platform.  For example ``"LIN"`` for Linux.
        """
        return self._mapdl.get_value("ACTIVE", item1="PLATFORM")

    @property
    def csys(self):
        """Active coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="CSYS"))

    @property
    def dsys(self):
        """Active display coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="DSYS"))

    @property
    def rsys(self):
        """Active result coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="RSYS"))

    @property
    def esys(self):
        """Active element coordinate system"""
        return int(self._mapdl.get_value("ACTIVE", item1="ESYS"))

    @property
    def section(self):
        """Active section number"""
        return int(self._mapdl.get_value("ACTIVE", item1="SECT"))

    @property
    def material(self):
        """Active material"""
        return int(self._mapdl.get_value("ACTIVE", item1="MAT"))

    @property
    def real(self):
        """Active real constant set"""
        return int(self._mapdl.get_value("ACTIVE", item1="REAL"))

    @property
    def type(self):
        """Active element type"""
        return int(self._mapdl.get_value("ACTIVE", item1="type"))

    @property
    @supress_logging
    def _parm(self):
        """Current MAPDL parameters"""
        return interp_star_status(self._mapdl.starstatus())

    def __repr__(self):
        """Return the current parameters in a pretty format"""
        lines = ['MAPDL Parameters',
                 '----------------']
        for key, info in self._parm.items():
            if info['type'] == 'ARRAY':
                value_str = 'ARRAY DIM %s' % str(info['shape'])
            elif info['type'] == 'CHARACTER':
                value_str = '"%s"' % info['value']
            else:
                value_str = str(info['value'])
            lines.append('%-32s : %s' % (key, value_str))
        return '\n'.join(lines)

    def __getitem__(self, key):
        """Return a parameter"""
        if not isinstance(key, str):
            raise TypeError('Parameter name must be a string')
        key = key.upper()

        parameters = self._parm
        if key not in parameters:
            raise IndexError('%s not a valid parameter_name' % key)

        parm = parameters[key]
        if parm['type'] == 'ARRAY':
            return self._get_parameter_array(key, parm['shape'])

        return parm['value']

    def __setitem__(self, key, value):
        """Set a parameter"""
        # parameters = self._parm  # check parameter exists
        if isinstance(value, (np.ndarray, list)):
            self._set_parameter_array(key, value)
        else:
            self._set_parameter(key, value)

    @supress_logging
    def _set_parameter(self, name, value):
        """Set a single parameter within MAPDL

        Parameters
        ----------
        name : str
            An alphanumeric name used to identify this parameter.  Par
            may be up to 32 characters, beginning with a letter and
            containing only letters, numbers, and underscores.  Examples:
            ``"ABC" "A3X" "TOP_END"``.

        """
        if not isinstance(value, (str, int, float)):
            raise TypeError('``Parameter`` must be either a float, int, or string')

        if not isinstance(name, str):
            raise TypeError('``name`` must be a string')

        if len(name) > 32:
            raise ValueError('Length of ``name`` must be 32 characters or less')

        # delete the parameter if it exists as an array
        parm = self._parm
        if name in parm:
            if parm[name]['type'] == 'ARRAY':
                self._mapdl.starset(name)

        if isinstance(value, str):
            if ' ' in value:
                raise ValueError('Spaces not allowed in strings in MAPDL')
            self._mapdl.starset(name, "'%s'" % value)
        else:
            self._mapdl.starset(name, value)

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
        format_str = '(1F20.12)'
        with self._mapdl.non_interactive:
            self._mapdl.mwrite(parm_name.upper(), label='kji')  # use C ordering
            self._mapdl.run(format_str)

        st = self._mapdl.last_response.rfind(format_str) + len(format_str) + 1
        arr_flat = np.fromstring(self._mapdl.last_response[st:], sep='\n')
        return arr_flat.reshape(shape).squeeze()

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
            raise TypeError('Only numerical arrays or lists are supported')
        if arr.ndim > 3:
            raise ValueError('MAPDL VREAD only supports a arrays with a'
                             ' maximum of 3 dimensions.')

        if not isinstance(name, str):
            raise TypeError('``name`` must be a string')

        name = name.upper()

        idim, jdim, kdim = arr.shape[0], 0, 0
        if arr.ndim >= 2:
            jdim = arr.shape[1]
        if arr.ndim == 3:
            kdim = arr.shape[2]

        # write array from numpy to disk
        filename = '_tmp.dat'
        self._write_numpy_array(filename, arr)

        self._mapdl.dim(name, imax=idim, jmax=jdim, kmax=kdim)
        with self._mapdl.non_interactive:
            self._mapdl.vread('%s(1, 1),%s,,,IJK, %d, %d, %d' % (name,
                                                                 filename,
                                                                 idim,
                                                                 jdim,
                                                                 kdim))
            self._mapdl.run('(1F20.12)')

    def _write_numpy_array(self, filename, arr):
        """Write a numpy array to disk"""
        filename = os.path.join(self._mapdl.path, filename)
        if arr.dtype != np.double:
            arr = arr.astype(np.double)
        pyansys._reader.write_array(filename.encode(), arr.ravel('F'))


def interp_star_status(status):
    """Interperts \*STATUS command output from MAPDL

    Parameters
    ----------
    status : str
        Output from MAPDL *STATUS

    Returns
    -------
    parameters : dict
        Dictionary of parameters.
    """
    parameters = {}
    st = status.find('NAME                              VALUE')
    for line in status[st+80:].splitlines():
        items = line.split()
        if not items:
            continue

        # line will contain either a character, scalar, or array
        name = items[0]
        if len(items) == 2:
            if items[1][-9:] == 'CHARACTER':
                parameters[name] = {'type': 'CHARACTER',
                                    'value': items[1][:-9]}
            # else:
                # log.warning(
        elif len(items) == 3:
            if items[2] == 'SCALAR':
                value = float(items[1])
            else:
                value = items[1]
            parameters[name] = {'type': items[2],
                                'value': value}
        elif len(items) == 5:
            shape = (int(items[2]), int(items[3]), int(items[4]))
            parameters[name] = {'type': items[1],
                                'shape': shape}
    return parameters
