"""Contains the ansXpl class."""
import json
import pathlib
import random
import string
import weakref

from ansys.api.mapdl.v0 import mapdl_pb2
import numpy as np

from .common_grpc import ANSYS_VALUE_TYPE
from .errors import MapdlRuntimeError


def id_generator(size=6, chars=string.ascii_uppercase):
    """Generate a random string using only uppercase letters."""
    return "".join(random.choice(chars) for _ in range(size))


MYCTYPE = {
    np.int32: "I",
    np.int64: "L",
    np.single: "F",
    np.double: "D",
    np.complex64: "C",
    np.complex128: "Z",
}


class ansXpl:
    """
    ANSYS database explorer.

    Examples
    --------
    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()
    >>> xpl = mapdl.xpl

    Open a mode file and extract a vector.

    >>> xpl.open('file.mode')
    >>> vec = xpl.read('MASS')
    >>> vec.asarray()
    array([ 4,  7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43,
            46, 49, 52, 55, 58,  1], dtype=int32)

    """

    def __init__(self, mapdl):
        """Initialize the class."""
        from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

        if not isinstance(mapdl, MapdlGrpc):  # pragma: no cover
            raise TypeError("Must be initialized using MapdlGrpc class")

        self._mapdl_weakref = weakref.ref(mapdl)
        self._filename = None
        self._open = False

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of mapdl."""
        return self._mapdl_weakref()

    def open(self, filename, option=""):
        """
        Open an MAPDL file to explore.

        Parameters
        ----------
        filename : str
            Name of the file to open.

        Returns
        -------
        str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.open('file.mode')
        ===============================================
        =====      ANSYS File Xplorer            ======
        ===============================================

        Opening the file.mode ANSYS File

        """
        self._filename = filename
        out = self._mapdl.run(f"*XPL,OPEN,{filename},,{option}")
        self._open = True
        return out

    def close(self):
        """
        Close the MAPDL file after opening.

        Returns
        -------
        str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.open("file.mode")
        >>> xpl.close()
        =====      ANSYS File Xplorer : Close the file.mode ANSYS File
        """
        response = self._mapdl.run("*XPL,CLOSE")
        self._check_ignored(response)
        self._open = False
        return response

    def list(self, nlev=1):
        """
        List the records at the current level.

        Parameters
        ----------
        nlev: int
            Number of levels to recursively explore.

        Returns
        -------
        str
            Listing of records from the current level.

        Examples
        --------
        Open a full file and list the current records.

        >>> xpl.open("file.full")
        >>> xpl.list()
        =====      ANSYS File Xplorer : List Blocks in File file.full
         ::FULL::HEADER         Size =        652  B     Total  Size =    180.297 KB
         ::FULL::DOFSBYNOD            Size =         24  B
         ::FULL::BACK                 Size =        336  B

         ::FULL::STIFF::HEADER        Size =    117.316 KB
         ::FULL::RHS                  Size =      1.910 KB
         ::FULL::DIAGK                Size =      1.910 KB
         ::FULL::SCLK                 Size =      1.910 KB
         ::FULL::MRK                  Size =        984  B
         ::FULL::NODEEXT              Size =        336  B
         ::FULL::PCGDOFS              Size =        984  B
         ::FULL::BCDOFS               Size =        984  B
         ::FULL::BCVALUES             Size =         12  B

         ::FULL::MASS::HEADER         Size =     50.801 KB
         ::FULL::DIAGM                Size =      1.910 KB
         ::FULL::NGPH                 Size =        336  B

        """
        response = self._mapdl.run(f"*XPL,LIST,{nlev}")
        self._check_ignored(response)
        return response

    def _check_ignored(self, response):
        """Check for ignored in response."""
        if "ignored" in response:
            raise MapdlRuntimeError(response)

    def help(self):
        """
        XPL help message.

        Examples
        --------
        >>> print(xpl.help())
        """
        return self._mapdl.run("*XPL,HELP")

    def step(self, where):
        """
        Go down in the tree of records

        Parameters
        ----------
        where : str
            Path to follow. This path can be composed of several
            levels, for example ``"BRANCH1::SUBBRANCH2::.."``

        Returns
        -------
        str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.step('MASS')
        >>> print(xpl.where())
         =====      ANSYS File Xplorer : Display Current Location
         Current Location : FULL::MASS
            File Location : 7644
        """
        response = self._mapdl.run(f"*XPL,STEP,{where}")
        if "Not Found" in response:
            raise MapdlRuntimeError(response.strip())
        return response

    def info(self, recname, option=""):
        """
        Gives details on a specific record, or all records (using ``"*"``)

        Parameters
        ----------
        recname : str
            Record of interest

        option : str
            Options string.

        Returns
        -------
        str
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
        return self._mapdl.run(f"*XPL,INFO,{recname},{option}")

    def print(self, recname):
        """
        Print values of a given records, or all records (using ``"*"``).

        Parameters
        ----------
        recname : str
            Record of interest

        option : str
            Options string.

        Returns
        -------
        str
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
        return self._mapdl.run(f"*XPL,PRINT,{recname}")

    def json(self):
        """
        Return a JSON representation of the tree or records.

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
        text = self._mapdl._download_as_raw("_mylocal_.json").decode()
        return json.loads(text)

    def where(self):
        """
        Returns the current location in the MAPDL file.

        Returns
        -------
        str
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
        """
        Go up in the tree.

        nlev : int
            Number of levels to recursively go up, or TOP

        Examples
        --------
        >>> print(xpl.up())
         =====      ANSYS File Xplorer : Go up to 1 level(s)
                     -> Already at the top level. Command is ignored
        """
        if str(nlev).upper().strip() == "TOP":
            return self._mapdl.run("*XPL,UP,TOP")
        return self._mapdl.run(f"*XPL,UP,{nlev}")

    def goto(self, path):
        """
        Go directly to a new location in the file.

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
        return self._mapdl.run(f"*XPL,GOTO,{path}")

    def copy(self, newfile, option=""):
        """
        Copy the current opened as a new file.

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
        return self._mapdl.run(f"*XPL,COPY,{newfile},{option}")

    def save(self):
        """Save the current file, ignoring the marked records."""
        response = self._mapdl.run("*XPL,SAVE").strip()
        self._check_ignored(response)
        return response

    def extract(self, recordname, sets="ALL", asarray=False):  # pragma: no cover
        """
        Import a Matrix/Vector from a MAPDL result file.

        At the moment, this only supports reading the displacement vectors from
        a result file.

        Parameters
        ----------
        recordname : str
            Record name. Currently only supports the ``"NSL"`` record,
            displacement vectors.

        sets : str or int
            Number of sets. Can be ``"ALL"`` or the number of sets to load.

        asarray : bool, optional
            Return a :class:`numpy.ndarray` rather than a :class:`AnsMat
            <ansys.mapdl.core.math.AnsMat>`. Default ``False``.

        Returns
        -------
        numpy.ndarray or ansys.mapdl.core.math.AnsMat
            A :class:`numpy.ndarray` or :class:`AnsMat
            <ansys.mapdl.core.math.AnsMat>` of the displacement vectors,
            depending on the value of ``asarray``.

        Notes
        -----
        This only works on the ``"NSL"`` record of MAPDL result files.

        Examples
        --------
        First, open a result file and extract the displacement vectors for all
        sets.

        >>> xpl.open("file.rst")
        >>> mat = xpl.extract("NSL")
        >>> mat
        Dense APDLMath Matrix (243, 10)

        Convert to a dense numpy array

        >>> arr = mat.asarray()
        >>> arr
        array([[-9.30806802e-03, -2.39600770e-02, -5.37856729e-03, ...,
                -5.61188243e-03, -7.17686067e-11,  3.71893252e-03],
               [-1.60960014e-02,  2.00410618e-02,  8.05822565e-03, ...,
                -1.26917511e-02, -5.14133724e-11, -1.38783485e-03],
               [ 2.54040694e-02,  3.91901513e-03, -2.67965796e-03, ...,
                -1.46365178e-02,  8.31735188e-11, -2.33109771e-03],
               ...,
               [-2.80679551e-03, -1.45686692e-02,  8.05466291e-03, ...,
                 5.88196684e-03,  1.72211103e-02,  6.10079082e-03],
               [-7.06675717e-03,  1.30455037e-02, -6.31685295e-03, ...,
                 1.08619340e-02, -1.72211102e-02,  2.52199472e-03],
               [ 2.29726170e-02,  3.54392176e-03, -1.87020162e-03, ...,
                 1.20642736e-02,  2.58299321e-11,  9.14504940e-04]])

        """
        if recordname.upper() != "NSL":
            raise ValueError("Currently, the only supported recordname is 'NSL'")

        rand_name = id_generator()
        self._mapdl._log.info(
            "Calling MAPDL to extract the %s matrix from %s",
            recordname,
            self._filename,
        )
        num_first = 1
        num_last = 1
        if sets == "ALL":
            num_last = -1

        dtype = np.double
        file_extension = pathlib.Path(self._filename).suffix[1:]
        if file_extension.lower() != "rst":
            raise MapdlRuntimeError(
                "This method only supports extracting records from result files"
            )

        self._mapdl.run(
            f"*DMAT,{rand_name},{MYCTYPE[dtype]},IMPORT,{file_extension},{self._filename},"
            f"{num_first},{num_last},{recordname}",
            mute=False,
        )
        return self._mapdl.math.mat(dtype=dtype, name=rand_name)

    def read(self, recordname, asarray=False):
        """
        Read a record and return either an APDL math matrix or an APDL math vector.

        Returns
        -------
        ansys.mapdl.AnsMat or ansys.mapdl.AnsVec
            A handle to the APDLMath object.

        asarray : bool, optional
            Return a :class:`numpy.ndarray` rather than a :class:`AnsMat
            <ansys.mapdl.core.math.AnsMat>`. Default ``False``.

        Examples
        --------
        >>> vec = xpl.read('MASS')
        >>> vec.asarray()
        array([ 4,  7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43,
               46, 49, 52, 55, 58,  1], dtype=int32)
        >>> vec = xpl.read('MASS', asarray=True)
        array([ 4,  7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43,
               46, 49, 52, 55, 58,  1], dtype=int32)
        """
        rand_name = id_generator()
        response = self._mapdl.run(f"*XPL,READ,{recordname},{rand_name}")
        self._check_ignored(response)
        data_info = self._mapdl._data_info(rand_name)

        dtype = ANSYS_VALUE_TYPE[data_info.stype]
        if dtype is None:  # pragma: no cover
            raise ValueError("Unknown MAPDL data type")

        # return either vector or matrix type
        if data_info.objtype == mapdl_pb2.DataType.VEC:
            out = self._mapdl.math.vec(dtype=dtype, name=rand_name)
        elif data_info.objtype in [
            mapdl_pb2.DataType.DMAT,
            mapdl_pb2.DataType.SMAT,
        ]:  # pragma: no cover
            out = self._mapdl.math.mat(dtype=dtype, name=rand_name)
        else:  # pragma: no cover
            raise ValueError(f"Unhandled MAPDL matrix object type {data_info.objtype}")

        if asarray:
            out = out.asarray()
        return out

    def write(self, recordname, vecname):
        """
        Write a given record back to an MAPDL file.

        Use the write function at your own risk, you may corrupt an existing
        file by changing the size of a record in the file.  This method must be
        used only on a non-compressed file.

        Parameters
        ----------
        recordname : str
            Name of the record you want to overwrite. Your position
            in the file must be set accordingly to this record location
            (same as if you want to read it).

        vecname : str
            Name of the APDLMath vector you want to write in the MAPDL
            file. Its size must be consistent with the existing record.

        Returns
        -------
        str
            Response from MAPDL.

        Examples
        --------
        >>> xpl.write('MASS', vecname)
        """
        response = self._mapdl.run(f"*XPL,WRITE,{recordname},{vecname}")
        self._check_ignored(response)
        return response

    def __repr__(self):
        txt = "MAPDL File Explorer\n"
        if self._open:
            txt += "\tOpen file:%s" % self._filename
            txt += "\n".join(self.where().splitlines()[1:])
        else:
            txt += "\tNo open file"
        return txt
