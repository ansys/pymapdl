"""Contains the ansXpl class"""
import weakref
import json

import numpy as np
from ansys.grpc.mapdl import ansys_kernel_pb2 as anskernel

from ansys.mapdl.core.errors import MapdlRuntimeError


class ansXpl():
    """ANSYS database explorer class.

    Examples
    --------
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> xpl = mapdl.xpl
    """

    def __init__(self, mapdl):
        from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError('Must be initialized using MapdlGrpc class')

        self._mapdl_weakref = weakref.ref(mapdl)
        self._filename = None
        self._open = False

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl"""
        return self._mapdl_weakref()

    def open(self, filename, option=""):
        """Open an MAPDL file to explore

        Parameters
        ----------
        filename : str
            Name of the file to open.

        Returns
        -------
        mapdl_response : str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.open('file.full')
        """
        self._filename = filename
        out = self._mapdl.run("*XPL,OPEN,%s,,%s" % (filename, option))
        self._open = True
        return out

    def close(self):
        """Close the MAPDL file after opening.

        Returns
        -------
        mapdl_response : str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.close()
        """
        response = self._mapdl.run("*XPL,CLOSE")
        self._check_ignored(response)
        self._open = False
        return response

    def list(self, nlev=1):
        """List the records at the current level.

        Parameters
        ----------
        nlev: int
            Number of levels to recursively explore.

        Returns
        -------
        mapdl_response : str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.list(1)
        """
        response = self._mapdl.run("*XPL,LIST,%d" % nlev)
        self._check_ignored(response)
        return response

    def _check_ignored(self, response):
        """Check for ignored in response"""
        if 'ignored' in response:
            raise MapdlRuntimeError(response)

    def help(self):
        """XPL help message

        Examples
        --------
        >>> print(xpl.help())
        """
        return self._mapdl.run("*XPL,HELP")

    def step(self, where):
        """Go down in the tree of records

        Parameters
        ----------
        where : str
            Path to follow. This path can be composed of several
            levels, for example ``"BRANCH1::SUBBRANCH2::.."``

        Returns
        -------
        mapdl_response : str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.step('MASS')
        >>> print(xpl.where())
         =====      ANSYS File Xplorer : Display Current Location
         Current Location : FULL::MASS
            File Location : 7644
        """
        response = self._mapdl.run("*XPL,STEP,%s" % where)
        if 'Not Found' in response:
            raise RuntimeError(response.strip())
        return response

    def info(self, recname, option=""):
        """Gives details on a specific record, or all records (using
        ``"*"``)

        Parameters
        ----------
        recname : str
            Record of interest

        option : str
            Options string.

        Returns
        -------
        mapdl_response : str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.open('file.full')
        >>> print(xpl.info('NGPH'))
        =====      ANSYS File Xplorer : Information about Block NGPH
        ::NGPH                 Size =      6.289 KB
                 - Record Size   : 81
                 - Data type     : integer values
        """
        return self._mapdl.run("*XPL,INFO," + recname + "," + option)

    def print(self, recname):
        """Print values of a given records, or all records (using
        ``"*"``)

        Parameters
        ----------
        recname : str
            Record of interest

        option : str
            Options string.

        Returns
        -------
        mapdl_response : str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.open('file.full')
        >>> print(xpl.print('DOFSBYNOD'))
        =====      ANSYS File Xplorer : Print Block DOFSBYNOD
        DOFSBYNOD :
        Size : 3
               1         2         3

        """
        return self._mapdl.run("*XPL,PRINT,%s" % recname)

    def json(self):
        """Create a JSON representation of the tree or records.

        Examples
        --------
        >>> xpl.json()
        {'name': 'FULL',
         'children': [{'name': 'DOFSBYNOD', 'size': 24},
         {'name': 'BACK', 'size': 336},
         {'name': 'STIFF', 'size': 120132},
         {'name': 'RHS', 'size': 1956},
         {'name': 'DIAGK', 'size': 1956},
         {'name': 'SCLK', 'size': 36},
         {'name': 'NODEEXT', 'size': 32},
         {'name': 'PCGDOFS', 'size': 984},
         {'name': 'BCDOFS', 'size': 984},
         {'name': 'BCVALUES', 'size': 20},
         {'name': 'MASS', 'size': 52020},
         {'name': 'DIAGM', 'size': 1236},
         {'name': 'NGPH', 'size': 6440}]}
        """
        self._mapdl.run("*XPL,JSON,_mylocal_.json")
        text = self._mapdl._download_as_raw('_mylocal_.json').decode()
        return json.loads(text)

    def where(self):
        """Prints the current location in the MAPDL FIle

        Returns
        -------
        location_string : str
            String containing the current location.

        Examples
        --------
        >>> print(xpl.where())
         =====      ANSYS File Xplorer : Display Current Location
         Current Location : FULL
            File Location : 412
        """
        return self._mapdl.run("*XPL,WHERE")

    def up(self, nlev=1):
        """Go up in the tree.

        nlev : int
            Number of levels to recursively go up, or TOP

        Examples
        --------
        >>> print(xpl.up())
         =====      ANSYS File Xplorer : Go up to 1 level(s)
                     -> Already at the top level. Command is ignored
        """
        if str(nlev).upper().strip() == 'TOP':
            return self._mapdl.run("*XPL,UP,TOP")
        return self._mapdl.run("*XPL,UP,%d" % nlev)

    def goto(self, path):
        """Go directly to a new location in the file.

        Parameters
        ----------
        path : str
            Absolute path to the new location.

        Examples
        --------
        >>> print(xpl.goto('MASS'))
         =====      ANSYS File Xplorer : Go up to top level(s)
         =====      ANSYS File Xplorer : Step into Block MASS
        """
        return self._mapdl.run("*XPL,GOTO,%s" % path)

    def copy(self, newfile, option=''):
        """Copy the current opened as a new file.

        Parameters
        ----------
        newfile : str
            Name of the new file to create

        option: str
            Option.

        Examples
        --------
        >>> xpl.copy('tmpfile.full')
         =====      ANSYS File Xplorer : Copy file.full ANSYS file to file tmpfile.full
            >>      Remove existing output file tmpfile.full
        """
        return self._mapdl.run("*XPL,COPY,%s,%s" % (newfile, option))

    def save(self):
        """Save the current file, ignoring the marked records"""
        response = self._mapdl.run("*XPL,SAVE").strip()
        self._check_ignored(response)
        return response

    def read(self, recordname):
        """Read a given record and fill a Python array.

        Returns
        -------
        arr : ansys.mapdl.AnsMat
            The array of values.

        Examples
        --------
        >>> vec = xpl.read('MASS')
        >>> vec.asarray()
        array([ 4,  7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43,
               46, 49, 52, 55, 58,  1], dtype=int32)
        """
        response = self._mapdl.run("*XPL,READ,%s,TmpXplData" % recordname)
        self._check_ignored(response)
        response = self._mapdl._data_info("TmpXplData")

        if (response.stype == anskernel.INTEGER):
            dtype = np.int32
        elif (response.stype == anskernel.DOUBLE):
            dtype = np.double
        elif (response.stype == anskernel.HYPER):
            dtype = np.int64
        else:
            raise TypeError('Unhandled ANSYS type %s' % response.stype)

        mm = self._mapdl.math
        return mm.vec(dtype=dtype, name="TmpXplData")

    def __repr__(self):
        txt = 'MAPDL File Explorer\n'
        if self._open:
            txt += '\tOpen file:%s' % self._filename
            txt += '\n'.join(self.where().splitlines()[1:])
        else:
            txt += '\tNo open file'
        return txt
