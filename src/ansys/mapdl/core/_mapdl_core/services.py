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


"""The services MAPDL core responsibility mixin."""

from enum import Enum  # noqa: F401
from functools import wraps  # noqa: F401
import glob  # noqa: F401
import logging  # noqa: F401
import os  # noqa: F401
import pathlib  # noqa: F401
import re  # noqa: F401
from shutil import copyfile, rmtree  # noqa: F401

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from subprocess import DEVNULL, call  # nosec B404  # noqa: F401
import tempfile  # noqa: F401
import time  # noqa: F401
from typing import (  # noqa: F401
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    TextIO,
    Tuple,
    TypeAlias,
    Union,
)
from uuid import uuid4  # noqa: F401
from warnings import warn  # noqa: F401
import weakref  # noqa: F401

import numpy as np  # noqa: F401

from ansys.mapdl import core as pymapdl  # noqa: F401
from ansys.mapdl.core import LOG as logger  # noqa: F401
from ansys.mapdl.core import _HAS_DPF, _HAS_VISUALIZER  # noqa: F401
from ansys.mapdl.core.commands import (  # noqa: F401
    CMD_BC_LISTING,
    CMD_LISTING,
    CMD_XSEL,
    XSEL_DOCSTRING_INJECTION,
    BoundaryConditionsListingOutput,
    CommandListingOutput,
    Commands,
    StringWithLiteralRepr,
    inject_docs,
)
from ansys.mapdl.core.errors import (  # noqa: F401
    ComponentNoData,
    MapdlCommandIgnoredError,
    MapdlExitedError,
    MapdlFileNotFoundError,
    MapdlInvalidRoutineError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.information import Information  # noqa: F401
from ansys.mapdl.core.inline_functions import Query  # noqa: F401
from ansys.mapdl.core.mapdl_types import MapdlFloat  # noqa: F401
from ansys.mapdl.core.misc import (  # noqa: F401
    check_deprecated_vtk_kwargs,
    check_valid_routine,
    last_created,
    random_string,
    requires_graphics,
    requires_package,
    run_as,
    supress_logging,
)
from ansys.mapdl.core.plotting import GraphicsBackend  # noqa: F401

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.reader import Archive  # noqa: F401

    from ansys.mapdl.core.component import ComponentManager  # noqa: F401
    from ansys.mapdl.core.mapdl import MapdlBase  # noqa: F401
    from ansys.mapdl.core.mapdl_geometry import Geometry, LegacyGeometry  # noqa: F401
    from ansys.mapdl.core.parameters import Parameters  # noqa: F401
    from ansys.mapdl.core.plugin import ansPlugin  # noqa: F401
    from ansys.mapdl.core.solution import Solution  # noqa: F401
    from ansys.mapdl.core.xpl import ansXpl  # noqa: F401

    if _HAS_DPF:
        from ansys.mapdl.core.reader import DPFResult  # noqa: F401

from ansys.mapdl.core.post import PostProcessing  # noqa: F401

from . import _CoreMixinBase
from .constants import (  # noqa: F401
    _ALLOWED_START_PARM,
    _PERMITTED_ERRORS,
    _TMP_COMP,
    DEBUG_LEVELS,
    ENTITIES_TO_SELECTION_MAPPING,
    GUI_FONT_SIZE,
    INVAL_COMMANDS,
    INVAL_COMMANDS_SILENT,
    LOG_APDL_DEFAULT_FILE_NAME,
    MAX_COMMAND_LENGTH,
    MAX_PARAM_CHARS,
    PLOT_COMMANDS,
    PNG_IS_WRITTEN_TO_FILE,
    SESSION_ID_NAME,
    STATUS,
    VALID_DEVICES,
    VALID_DEVICES_LITERAL,
    VALID_FILE_TYPE_FOR_PLOT,
    VALID_FILE_TYPE_FOR_PLOT_LITERAL,
    VALID_SELECTION_ENTITY_TP,
    VALID_SELECTION_TYPE_TP,
    VWRITE_MWRITE_REPLACEMENT,
)


class _CoreServicesMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

    @property
    def components(self) -> "ComponentManager":
        """MAPDL Component manager.

        Returns
        -------
        :class:`ansys.mapdl.core.component.ComponentManager`

        Examples
        --------
        Check if a solution has converged.

        >>> mapdl.solution.converged
        """
        if self.exited:  # pragma: no cover
            raise MapdlRuntimeError("MAPDL exited.")
        return self._componentmanager

    @property
    def geometry(self) -> "Geometry":
        """Geometry information.

        See :class:`ansys.mapdl.core.mapdl_geometry.Geometry`

        Examples
        --------
        Print the current status of the geometry.

        >>> print(mapdl.geometry)
        MAPDL Selected Geometry
        Keypoints:  8
        Lines:      12
        Areas:      6
        Volumes:    1

        Return the number of lines.

        >>> mapdl.geometry.n_line
        12

        Return the number of areas.

        >>> mapdl.geometry.n_area
        6

        Select a list of keypoints.

        >>> mapdl.geometry.keypoint_select([1, 5, 10])

        Append to an existing selection of lines.

        >>> mapdl.geometry.line_select([1, 2, 3], sel_type='A')

        Reselect from the existing selection of lines.

        >>> mapdl.geometry.line_select([3, 4, 5], sel_type='R')
        """
        if self._geometry is None:  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
            self._geometry = self._create_geometry()
        return self._geometry

    @property
    def info(self):
        """General information"""
        return self._info

    @property
    def mesh(self):
        """Mesh information.

        Returns
        -------
        :class:`Mapdl.Mesh <ansys.mapdl.core.mesh_grpc.Mesh>`

        Examples
        --------
        Return an array of the active nodes

        >>> mapdl.mesh.nodes
        array([[ 1.,  0.,  0.],
               [ 2.,  0.,  0.],
               [ 3.,  0.,  0.],
               [ 4.,  0.,  0.],
               [ 5.,  0.,  0.],
               [ 6.,  0.,  0.],
               [ 7.,  0.,  0.],
               [ 8.,  0.,  0.],
               [ 9.,  0.,  0.],
               [10.,  0.,  0.]])

        Return an array of the node numbers of the active nodes

        >>> mapdl.mesh.nnum
        array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10], dtype=int32)

        Simply query and print the geometry

        >>> print(mapdl.mesh)
          ANSYS Mapdl Mesh
          Number of Nodes:              321
          Number of Elements:           40
          Number of Element Types:      1
          Number of Node Components:    2
          Number of Element Components: 2

        Access the geometry as a VTK object

        >>> mapdl.mesh.grid
        """
        return self._mesh

    @property
    def parameters(self) -> "Parameters":
        """Collection of MAPDL parameters.

        Notes
        -----
        See :ref:`ref_special_named_param` for additional notes regarding parameter naming in MAPDL.

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
        return self._parameters

    def scalar_param(self, parm_name):
        response = self.starstatus(parm_name)
        response = response.splitlines()[-1]

        if parm_name.upper() not in response:
            raise ValueError(f"Parameter {parm_name} not found")
        return float(response.split()[1].strip())

    @property
    def post_processing(self) -> "PostProcessing":
        """Post-process an active MAPDL session.

        Examples
        --------
        Get the nodal displacement in the X direction for the first
        result set.

        >>> mapdl.set(1, 1)
        >>> disp_x = mapdl.post_processing.nodal_displacement('X')
        array([1.07512979e-04, 8.59137773e-05, 5.70690047e-05, ...,
               5.70333124e-05, 8.58600402e-05, 1.07445726e-04])
        """
        if self.exited:
            raise MapdlRuntimeError(
                "MAPDL exited.\n\nCan only postprocess a live " "MAPDL instance."
            )

        if self._post_object is None:  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
            self._post_object = PostProcessing(self)

        return self._post_object

    @property
    def queries(self):
        """Get instance of Query class containing inline functions of APDL.

        Most of the results of these methods are shortcuts for specific
        combinations of arguments supplied to :func:`ansys.mapdl.core.Mapdl.get`.

        Currently implemented functions:

        - ``centrx(e)`` - get the centroid x-coordinate of element `e`
        - ``centry(e)`` - get the centroid y-coordinate of element `e`
        - ``centrz(e)`` - get the centroid z-coordinate of element `e`
        - ``nx(n)`` - get the x-coordinate of node `n`
        - ``ny(n)`` - get the y-coordinate of node `n`
        - ``nz(n)`` - get the z-coordinate of node `n`
        - ``kx(k)`` - get the x-coordinate of keypoint `k`
        - ``ky(k)`` - get the y-coordinate of keypoint `k`
        - ``kz(k)`` - get the z-coordinate of keypoint `k`
        - ``lx(n, lfrac)`` - X-coordinate of line ``n`` at length fraction ``lfrac``
        - ``ly(n, lfrac)`` - Y-coordinate of line ``n`` at length fraction ``lfrac``
        - ``lz(n, lfrac)`` - Z-coordinate of line ``n`` at length fraction ``lfrac``
        - ``lsx(n, lfrac)`` - X-slope of line ``n`` at length fraction ``lfrac``
        - ``lsy(n, lfrac)`` - Y-slope of line ``n`` at length fraction ``lfrac``
        - ``lsz(n, lfrac)`` - Z-slope of line ``n`` at length fraction ``lfrac``
        - ``ux(n)`` - get the structural displacement at node `n` in x
        - ``uy(n)`` - get the structural displacement at node `n` in y
        - ``uz(n)`` - get the structural displacement at node `n` in z
        - ``rotx(n)`` - get the rotational displacement at node `n` in x
        - ``roty(n)`` - get the rotational displacement at node `n` in y
        - ``rotz(n)`` - get the rotational displacement at node `n` in z
        - ``nsel(n)`` - get the selection status of node `n`
        - ``ksel(k)`` - get the selection status of keypoint `k`
        - ``lsel(n)`` - get the selection status of line `n`
        - ``asel(a)`` - get the selection status of area `a`
        - ``esel(n)`` - get the selection status of element `e`
        - ``vsel(v)`` - get the selection status of volume `v`
        - ``ndnext(n)`` - get the next selected node with a number greater than `n`.
        - ``kpnext(k)`` - get the next selected keypoint with a number greater than `k`.
        - ``lsnext(n)`` - get the next selected line with a number greater than `n`.
        - ``arnext(a)`` - get the next selected area with a number greater than `a`.
        - ``elnext(e)`` - get the next selected element with a number greater than `e`.
        - ``vlnext(v)`` - get the next selected volume with a number greater than `v`.
        - ``node(x, y, z)`` - get the node closest to coordinate (x, y, z)
        - ``kp(x, y, z)`` - get the keypoint closest to coordinate (x, y, z)

        Returns
        -------
        :class:`ansys.mapdl.core.inline_functions.Query`
            Instance of the Query class

        Examples
        --------
        In this example we construct a solid box and mesh it. Then we use
        the ``Query`` methods ``nx``, ``ny``, and ``nz`` to find the
        cartesian coordinates of the first node.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.prep7()
        >>> mapdl.et(1, 'SOLID5')
        >>> mapdl.block(0, 10, 0, 20, 0, 30)
        >>> mapdl.esize(2)
        >>> mapdl.vmesh('ALL')
        >>> q = mapdl.queries
        >>> q.nx(1), q.ny(1), q.nz(1)
        0.0 20.0 0.0
        """
        if self._query is None:
            self._query = Query(self)
        return self._query

    @property
    def solution(self) -> "Solution":
        """Solution parameters of MAPDL.

        Returns
        -------
        :class:`ansys.mapdl.core.solution.Solution`
            The solution object contains methods to check the convergence of the
            solution, the number of iterations, and the current time step.

        Examples
        --------
        Check if a solution has converged.

        >>> mapdl.solution.converged
        """
        if self.exited:
            raise MapdlRuntimeError("MAPDL exited.")
        return self._solution

    @property
    def plugins(self) -> "ansPlugin":
        """MAPDL plugin handler

        Plugin Manager for MAPDL

        Examples
        --------

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> plugins = mapdl.plugins
        >>> plugins.load('PluginDPF')
        """
        if self._plugin is None:  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
            from ansys.mapdl.core.plugin import ansPlugin

            self._plugin = ansPlugin(self)
        return self._plugin

    @property
    @requires_package("ansys.mapdl.reader", softerror=True)
    def result(self):
        """Binary interface to the result file using ``ansys-dpf-core`` or
        ``ansys-mapdl-reader``.

        If `ansys-dpf-core` is not installed, then a :class:`ansys.mapdl.reader.rst.Result`
        object is returned.

        Returns
        -------
        :class:`ansys.mapdl.reader.rst.Result`.
            Result reader class.  See `Legacy PyMAPDL Reader <https://readerdocs.pyansys.com/>`.

        Examples
        --------
        >>> mapdl.solve()
        >>> mapdl.finish()
        >>> result = mapdl.result
        >>> print(result)
        PyMAPDL-Reader Result file object
        Units       : User Defined
        Version     : 18.2
        Cyclic      : False
        Result Sets : 1
        Nodes       : 3083
        Elements    : 977
        ...
        Available Results:
        EMS : Miscellaneous summable items (normally includes face pressures)
        ENF : Nodal forces
        ENS : Nodal stresses
        ENG : Element energies and volume
        EEL : Nodal elastic strains
        ETH : Nodal thermal strains (includes swelling strains)
        EUL : Element euler angles
        EMN : Miscellaneous nonsummable items
        EPT : Nodal temperatures
        NSL : Nodal displacements
        RF  : Nodal reaction forces
        """
        if _HAS_DPF and not self._use_reader_backend:
            from ansys.mapdl.core.reader import DPFResult

            if self._dpf_result is None:
                # create a DPFResult object
                self._dpf_result = DPFResult(
                    rst_file=None, mapdl=self, logger=self._log
                )

            return self._dpf_result

        from ansys.mapdl.reader import read_binary
        from ansys.mapdl.reader.rst import Result

        if not self._local:
            # download to temporary directory
            save_path = tempfile.mkdtemp(suffix=f"ansys_tmp_{random_string()}")
            result_path = self.download_result(save_path)
        else:
            if self._distributed_result_file and self._result_file:
                result_path = self._distributed_result_file
                result = Result(result_path, read_mesh=False)
                if result._is_cyclic:
                    result_path = self._result_file
                else:  # pragma: no cover
                    # return the file with the last access time
                    filenames = [
                        self._distributed_result_file,
                        self._result_file,
                    ]
                    result_path = last_created(filenames)
                    if result_path is None:  # if same return result_file
                        result_path = self._result_file

            elif self._distributed_result_file:
                result_path = self._distributed_result_file
                result = Result(result_path, read_mesh=False)
                if result._is_cyclic:
                    if not os.path.isfile(self._result_file):
                        raise MapdlRuntimeError(
                            "Distributed Cyclic result not supported"
                        )
                    result_path = self._result_file
            else:
                result_path = self._result_file

        if result_path is None or not os.path.isfile(result_path):
            raise FileNotFoundError(
                f"No result file(s) at {result_path or self.directory}. "
                "Check that there is at least one RST file in the working directory "
                f"'{self.directory}', or solve an MAPDL model to generate one."
            )

        return read_binary(result_path)

    @property
    def result_file(self):
        """Return the RST file path."""
        return self._result_file

    @property
    def _distributed_result_file(self):
        """Path of the distributed result file"""
        try:
            filename = self.inquire("", "RSTFILE")
            if not filename:
                filename = self.jobname
        except Exception:
            filename = self.jobname

        # ansys decided that a jobname ended in a number needs a bonus "_"
        if filename[-1].isnumeric():
            filename += "_"

        rth_basename = "%s0.%s" % (filename, "rth")
        rst_basename = "%s0.%s" % (filename, "rst")

        rth_file = self.directory / rth_basename
        rst_file = self.directory / rst_basename

        if os.path.isfile(rth_file) and os.path.isfile(rst_file):
            return last_created([rth_file, rst_file])
        elif os.path.isfile(rth_file):
            return rth_file
        elif os.path.isfile(rst_file):
            return rst_file

    @property
    @supress_logging
    def _mesh(self) -> "Archive":
        """Write entire archive to ASCII and read it in as an
        ``ansys.mapdl.core.Archive``
        """
        from ansys.mapdl.reader import Archive

        if self._archive_cache is None:  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
            # write database to an archive file
            arch_filename = self.directory / "_tmp.cdb"
            nblock_filename = self.directory / "nblock.cdb"

            # must have all nodes elements are using selected
            self.cm("__NODE__", "NODE", mute=True)
            self.nsle("S", mute=True)
            self.cdwrite("db", arch_filename, mute=True)
            self.cmsel("S", "__NODE__", "NODE", mute=True)

            self.cm("__ELEM__", "ELEM", mute=True)
            self.esel("NONE", mute=True)
            self.cdwrite("db", nblock_filename, mute=True)
            self.cmsel("S", "__ELEM__", "ELEM", mute=True)

            self._archive_cache = Archive(arch_filename, parse_vtk=False, name="Mesh")
            if self._archive_cache is None:
                raise MapdlRuntimeError("Failed to create the mesh archive.")
            grid = self._archive_cache._parse_vtk(additional_checking=True)
            self._archive_cache._grid = grid

            # rare bug
            if grid is not None:
                if grid.n_node != self._archive_cache.n_node:
                    self._archive_cache = Archive(
                        arch_filename, parse_vtk=True, name="Mesh"
                    )

            # overwrite nodes in archive
            nblock = Archive(nblock_filename, parse_vtk=False)
            self._archive_cache._nodes = nblock._nodes
            self._archive_cache._nnum = nblock._nnum
            self._archive_cache._node_coord = None

        return self._archive_cache

    @property
    def _result_file(self):
        """Path of the non-distributed result file"""
        try:
            with self.run_as_routine("POST1"):
                filename = self.inquire("", "RSTFILE")
        except Exception:  # pragma: no cover
            filename = self.jobname

        try:
            with self.run_as_routine("POST1"):
                ext = self.inquire("", "RSTEXT")
        except Exception:  # pragma: no cover
            ext = "rst"

        if self._local:
            if ext == "":
                # Case where there is RST extension because it is thermal for example
                filename = self.jobname

                rth_file = self.directory / f"{filename}.rth"
                rst_file = self.directory / f"{filename}.rst"

                if self._prioritize_thermal and os.path.isfile(rth_file):
                    return rth_file

                if os.path.isfile(rth_file) and os.path.isfile(rst_file):
                    return last_created([rth_file, rst_file])
                elif os.path.isfile(rth_file):
                    return rth_file
                elif os.path.isfile(rst_file):
                    return rst_file
            else:
                filename = self.directory / f"{filename}.{ext}"
                if os.path.isfile(filename):
                    return filename
        else:
            return f"{filename}.{ext}"

    def _create_geometry(self) -> Union["Geometry", "LegacyGeometry"]:
        """Return geometry cache"""

        if self.legacy_geometry:
            from ansys.mapdl.core.mapdl_geometry import LegacyGeometry

            return LegacyGeometry
        else:
            from ansys.mapdl.core.mapdl_geometry import Geometry

            return Geometry(self)

    def _reset_cache(self):
        """Reset cached items"""
        self._archive_cache = None
