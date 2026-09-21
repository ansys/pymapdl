# Copyright (C) 2016 - 2026 ANSYS, Inc. and/or its affiliates.
# Copyright (C) 2016 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""The arrays MAPDL extended mixin."""

from functools import wraps  # noqa: F401
import os  # noqa: F401
import pathlib  # noqa: F401
import re  # noqa: F401
import shutil  # noqa: F401
import tempfile  # noqa: F401
from typing import Union  # noqa: F401
import warnings  # noqa: F401
import weakref  # noqa: F401

import numpy as np  # noqa: F401
from numpy.typing import DTypeLike, NDArray  # noqa: F401

from ansys.mapdl.core import LOG as logger  # noqa: F401
from ansys.mapdl.core import parse  # noqa: F401
from ansys.mapdl.core.commands import CommandListingOutput, CommandOutput  # noqa: F401
from ansys.mapdl.core.errors import (  # noqa: F401
    CommandDeprecated,
    ComponentDoesNotExits,
    IncorrectWorkingDirectory,
    MapdlCommandIgnoredError,
    MapdlDoLoopLimitError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_core import _MapdlCore  # noqa: F401
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat  # noqa: F401
from ansys.mapdl.core.misc import (  # noqa: F401
    allow_iterables_vmin,
    allow_pickable_entities,
    check_deprecated_vtk_kwargs,
    random_string,
    requires_graphics,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401

from . import _ExtendedMixinBase


class _ExtendedArrayMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    def load_table(
        self, name, array, var1="", var2="", var3="", csysid="", col_header=False
    ):
        """Load a table from Python to into MAPDL.

        Uses :func:`tread <Mapdl.tread>` to transfer the table.

        Parameters
        ----------
        name : str
            An alphanumeric name used to identify this table.  Name
            may be up to 32 characters, beginning with a letter and
            containing only letters, numbers, and underscores.
            Examples: ``"ABC" "A3X" "TOP_END"``.

        array : numpy.ndarray or list
            List as a table or :class:`numpy.ndarray` array.

        var1 : str, optional
            Variable name corresponding to the first dimension (row).
            Default ``"Row"``.

            A primary variable (listed below) or can be an independent
            parameter. If specifying an independent parameter, then you must
            define an additional table for the independent parameter. The
            additional table must have the same name as the independent
            parameter and may be a function of one or more primary variables or
            another independent parameter. All independent parameters must
            relate to a primary variable.

            - ``"TIME"``: Time
            - ``"FREQ"``: Frequency
            - ``"X"``: X-coordinate location
            - ``"Y"``: Y-coordinate location
            - ``"Z"``: Z-coordinate location
            - ``"TEMP"``: Temperature
            - ``"VELOCITY"``: Velocity
            - ``"PRESSURE"``: Pressure
            - ``"GAP"``: Geometric gap/penetration
            - ``"SECTOR"``: Cyclic sector number
            - ``"OMEGS"``: Amplitude of the rotational velocity vector
            - ``"ECCENT"``: Eccentricity
            - ``"THETA"``: Phase shift
            - ``"ELEM"``: Element number
            - ``"NODE"``: Node number
            - ``"CONC"``: Concentration

        var2 : str, optional
            Variable name corresponding to the first dimension (column).
            See ``var1``.  Default column.

        var3 : str, optional
            Variable name corresponding to the first dimension (plane).
            See ``var1``. Default Plane.

        csysid : str, optional
            An integer corresponding to the coordinate system ID number.
            APDL Default = 0 (global Cartesian)

        col_header : bool, optional
            Indicates if the first row of the input array is a header.
            Set to True if the array includes a header row.
            Default is False.

        Examples
        --------
        Transfer a table to MAPDL. The first column is time values and must be
        ascending in order.

        >>> my_conv = np.array([[0, 0.001],
                                [120, 0.001],
                                [130, 0.005],
                                [700, 0.005],
                                [710, 0.002],
                                [1000, 0.002]])
        >>> mapdl.load_table('MY_TABLE', my_conv, 'TIME')
        >>> mapdl.parameters['MY_TABLE']
        array([[0.001],
               [0.001],
               [0.005],
               [0.005],
               [0.002],
               [0.002]])
        """
        if not isinstance(array, np.ndarray):
            raise ValueError("The table should be a Numpy array")
        if array.shape[0] < 2 or array.shape[1] < 2:
            raise ValueError(
                "One or two of the array dimensions are too small to create a table."
            )

        if array.ndim == 2:
            # MAPDL considers the first row to be column header when col num > 2.
            # When col header is not available duplicate the first row
            if array.shape[1] > 2:
                if col_header is False:
                    array = np.vstack((array[0], array))
                imax_val = array.shape[0] - 1
            else:
                imax_val = array.shape[0]

            self.dim(
                name,
                "TABLE",
                imax=imax_val,
                jmax=array.shape[1] - 1,
                kmax="",
                var1=var1,
                var2=var2,
                var3=var3,
                csysid=csysid,
            )
        else:
            raise ValueError(
                f"Expecting only a 2D table, but input contains\n{array.ndim} dimensions"
            )

        if not np.all(array[:-1, 0] <= array[1:, 0]):
            raise ValueError(
                "The underlying ``TREAD`` command requires that the first column is in "
                "ascending order."
            )

        base_name = random_string() + ".txt"
        filename = os.path.join(tempfile.gettempdir(), base_name)
        np.savetxt(filename, array, header="File generated by PyMAPDL:load_table")

        if not self._local:
            self.upload(filename, progress_bar=False)
            filename = base_name

        # skip the first line its a header we wrote in np.savetxt
        self.tread(name, filename, nskip=1, mute=True)

        if not self._local:
            self.slashdelete(filename)

    def load_array(self, name, array):
        """
        Load an array from Python to MAPDL.

        Uses ``VREAD`` to transfer the array.
        The format of the numbers used in the intermediate file is F24.18.

        Parameters
        ----------
        name : str
            An alphanumeric name used to identify this table.  Name
            may be up to 32 characters, beginning with a letter and
            containing only letters, numbers, and underscores.
            Examples: ``"ABC" "A3X" "TOP_END"``.

        array : np.ndarray or list
            List as a table or ``numpy`` array.

        Examples
        --------
        >>> my_conv = np.array([[0, 0.001],
        ...                     [120, 0.001],
        ...                     [130, 0.005],
        ...                     [700, 0.005],
        ...                     [710, 0.002],
        ...                     [1000, 0.002]])
        >>> mapdl.load_array('MY_ARRAY', my_conv)
        >>> mapdl.parameters['MY_ARRAY']
        array([[0.0e+00, 1.0e-03],
                [1.2e+02, 1.0e-03],
                [1.3e+02, 5.0e-03],
                [7.0e+02, 5.0e-03],
                [7.1e+02, 2.0e-03],
                [1.0e+03, 2.0e-03]])
        """
        if not isinstance(array, np.ndarray):
            array = np.asarray(array)

        if array.ndim > 2:
            raise NotImplementedError(
                "Only loading of 1D or 2D arrays is supported at the moment."
            )

        jmax = 1
        kmax = ""

        if array.ndim > 0:
            imax = array.shape[0]

        if array.ndim > 1:
            jmax = array.shape[1]

        self.dim(name, "ARRAY", imax=imax, jmax=jmax, kmax="")

        base_name = random_string() + ".txt"
        filename = os.path.join(tempfile.gettempdir(), base_name)
        self._log.info(f"Generating file for table in {filename}")
        np.savetxt(
            filename,
            array.ravel(),
            delimiter="",
            header="File generated by PyMAPDL:load_array",
            fmt="%+24.18e",  # adding sign.
        )

        if not self._local:
            self.upload(filename, progress_bar=False)
            filename = base_name

        with self.non_interactive:
            label = "jik"
            n1 = jmax
            n2 = imax
            n3 = kmax
            self.vread(name, filename, n1=n1, n2=n2, n3=n3, label=label, nskip=1)
            fmt = f"(1E25.18)"  # Adding one extra space for the sign
            logger.info("Using *VREAD with format %s in %s", fmt, filename)
            self.run(fmt)

        if self._local:
            os.remove(filename)
        else:
            self.slashdelete(filename)

    @supress_logging
    def get_array(
        self,
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        kloop: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> NDArray[np.float64]:
        """Uses the ``*VGET`` command to Return an array from ANSYS as a
        Python array.

        See `VGET
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_VGET_st.html>`
        for more details.

        Parameters
        ----------
        entity
            Entity keyword.  Valid keywords are NODE, ELEM, KP, LINE,
            AREA, VOLU, etc

        entnum
            The number of the entity.

        item1
            The name of a particular item for the given entity.  Valid
            items are as shown in the Item1 columns of the tables
            below.

        it1num
            The number (or label) for the specified Item1 (if any).
            Valid IT1NUM values are as shown in the IT1NUM columns of
            the tables below.  Some Item1 labels do not require an
            IT1NUM value.

        item2, it2num
            A second set of item labels and numbers to further qualify
            the item for which data is to be retrieved.  Most items do
            not require this level of information.

        kloop
            Field to be looped on:

            - 0 or 2 : Loop on the ENTNUM field (default).
            - 3 : Loop on the Item1 field.
            - 4 : Loop on the IT1NUM field. Successive items are as shown with IT1NUM.
            - 5 : Loop on the Item2 field.
            - 6 : Loop on the IT2NUM field. Successive items are as shown with IT2NUM.

        Notes
        -----
        Please reference your Ansys help manual ``*VGET`` command tables
        for all the available ``*VGET`` values.

        Returns
        -------
        numpy.ndarray
            Array from MAPDL.

        Examples
        --------
        List the current selected node numbers

        >>> mapdl.get_array('NODE', item1='NLIST')
        array([  1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,
              ...
              314., 315., 316., 317., 318., 319., 320., 321.])

        List the displacement in the X direction for the first result

        >>> mapdl.post1()
        >>> mapdl.set(1, 1)
        >>> disp_x = mapdl.get_array('NODE', item1='U', it1num='X')
        array([ 0.01605306, -0.01605306,  0.00178402, -0.01605306,
               ...
               -0.00178402, -0.01234851,  0.01234851, -0.01234851])
        """
        if self._store_commands:
            raise MapdlRuntimeError(
                "Cannot use `mapdl.get_array` when in `non_interactive` mode, "
                "since it does not return anything until the `non_interactive` context "
                "manager is finished.\n"
                "Exit `non_interactive` mode before using this method.\n\n"
                "Alternatively you can use `mapdl.vget` to specify the name of the MAPDL parameter where to store the retrieved value."
            )

        arr = self._get_array(
            entity, entnum, item1, it1num, item2, it2num, kloop, **kwargs
        )

        # edge case where corba refuses to return the array
        ntry = 0
        while arr.size == 1 and arr[0] == -1:
            arr = self._get_array(
                entity, entnum, item1, it1num, item2, it2num, kloop, **kwargs
            )
            if ntry > 5:
                raise MapdlRuntimeError("Unable to get array for %s" % entity)
            ntry += 1
        return arr

    def _get_array(
        self,
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        kloop: MapdlFloat = "",
        dtype: DTypeLike = None,
        delete_after: bool = True,
        **kwargs,
    ) -> NDArray[np.float64]:
        """Uses the VGET command to get an array from ANSYS"""
        parm_name = kwargs.pop("parm", None)

        if self._store_commands and not parm_name:
            raise MapdlRuntimeError(
                "Cannot use `mapdl._get_array` when in `non_interactive` mode, "
                "since it does not return anything until the `non_interactive` context "
                "manager is finished.\n"
                "Exit `non_interactive` mode before using this method.\n\n"
                "Alternatively you can use `mapdl.vget` or use the `parm` kwarg in "
                "`mapdl._get_array` to specify the name of the MAPDL parameter where to store the retrieved value. In any case, this function will return `None`"
            )

        if parm_name is None:
            parm_name = "__vget_tmp_%d__" % self._vget_arr_counter
            self._vget_arr_counter += 1

        out = self.starvget(
            parm_name,
            entity,
            entnum,
            item1,
            it1num,
            item2,
            it2num,
            kloop,
            mute=False,
        )

        if self._store_commands:
            # Return early
            return None

        # check if empty array
        if "the dimension number 1 is 0" in out:
            return np.empty(0)

        with self.non_interactive:
            self.vwrite("%s(1)" % parm_name)  # type: ignore[arg-type]
            self.run("(F20.12)")  # type: ignore[arg-type]

        array = np.fromstring(self.last_response, sep="\n")

        if delete_after or "__vget_tmp_" in parm_name:
            self.run(f"{parm_name}=")

        if dtype:
            return array.astype(dtype)
        else:
            return array
