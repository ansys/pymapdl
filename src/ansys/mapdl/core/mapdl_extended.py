# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

from functools import wraps
import os
import pathlib
import tempfile
from typing import Union
import warnings

import numpy as np
from numpy.typing import DTypeLike, NDArray

from ansys.mapdl.core import LOG as logger
from ansys.mapdl.core import _HAS_PYVISTA
from ansys.mapdl.core.commands import CommandListingOutput
from ansys.mapdl.core.errors import (
    CommandDeprecated,
    ComponentDoesNotExits,
    IncorrectWorkingDirectory,
    MapdlRuntimeError,
)
from ansys.mapdl.core.mapdl_core import _MapdlCore
from ansys.mapdl.core.mapdl_types import KwargDict, MapdlFloat
from ansys.mapdl.core.misc import (
    allow_iterables_vmin,
    allow_pickable_entities,
    load_file,
    random_string,
    supress_logging,
)
from ansys.mapdl.core.theme import get_ansys_colors

if _HAS_PYVISTA:
    from ansys.mapdl.core.plotting import general_plotter, get_meshes_from_plotter


class _MapdlCommandExtended(_MapdlCore):
    """Class that extended MAPDL capabilities by wrapping or overwriting commands"""

    def file(self, fname: str = "", ext: str = "", **kwargs) -> str:
        """Specifies the data file where results are to be found.

        APDL Command: FILE

        Parameters
        ----------
        fname : str
            File name and directory path (248 characters maximum, including the
            characters needed for the directory path).  An unspecified
            directory path defaults to the working directory; in this case, you
            can use all 248 characters for the file name.

        ext : str, default: "rst"
            Filename extension (eight-character maximum). If ``fname`` has an
            extension this is ignored.

        Notes
        -----
        Specifies the Ansys data file where the results are to be found for
        postprocessing.

        Examples
        --------
        Load a result file that is outside of the current working directory.

        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()
        >>> mapdl.post1()
        >>> mapdl.file('/tmp/file.rst')

        """
        fname = self._get_file_name(fname, ext, "rst")
        fname = self._get_file_path(fname, kwargs.get("progress_bar", False))
        file_, ext_, _ = self._decompose_fname(fname)
        return self._file(file_, ext_, **kwargs)

    def _file(self, filename: str, extension: str, **kwargs) -> str:
        """Run the MAPDL ``file`` command with a proper filename."""
        return self.run(f"FILE,{filename},{extension}", **kwargs)

    @wraps(_MapdlCore.lsread)
    def lsread(self, *args, **kwargs):
        """Wraps the ``LSREAD`` which does not work in interactive mode."""
        self._log.debug("Forcing 'LSREAD' to run in non-interactive mode.")
        with self.non_interactive:
            super().lsread(*args, **kwargs)
        return self._response.strip()

    @wraps(_MapdlCore.use)
    def use(self, *args, **kwargs):
        """Wrap the use command."""
        # Because of `name` can be a macro file or a macro block on a macro library
        # file, we are going to test if the file exists locally first, then remote,
        # and if not, silently assume that it is a macro in a macro library.
        # I do not think there is a way to check if the macro exists before use it.
        if "name" in kwargs:
            name = kwargs.pop("name")
        else:
            if len(args) < 1:
                raise ValueError("Missing `name` argument")
            name = args[0]

        base_name = os.path.basename(name)

        # Check if it is a file local
        if os.path.exists(name):
            self.upload(name)

        elif base_name in self.list_files():
            # the file exists in the MAPDL working directory, so do nothing.
            pass

        else:
            if os.path.dirname(name):
                # It seems you provided a path (or something like that)
                raise FileNotFoundError(
                    f"The name supplied to 'mapdl.use' ('{name}') is not a file in the Python "
                    "working directory, nor in the MAPDL working directory. "
                )
            # Preferring logger.warning over warn (from warnings), since it is less intrusive.
            self._log.warning(
                f"The name supplied to 'mapdl.use' ('{name}') is not a file in the Python "
                "working directory, nor in the MAPDL working directory. "
                "PyMAPDL will assume it is a macro block inside a macro library "
                "file previously defined using 'mapdl.ulib'."
            )
            # If MAPDL cannot find named macro file, it will throw a runtime error.

        # Update arg because the path is no longer needed
        args = (base_name, *args[1:])

        with self.non_interactive:
            super().use(*args, **kwargs)

        return self._response  # returning last response

    @wraps(_MapdlCore.set)
    def set(
        self,
        lstep="",
        sbstep="",
        fact="",
        kimg="",
        time="",
        angle="",
        nset="",
        order="",
        **kwargs,
    ):
        """Wraps SET to return a Command listing"""
        output = super().set(
            lstep, sbstep, fact, kimg, time, angle, nset, order, **kwargs
        )

        if (
            isinstance(lstep, str)
            and lstep.upper() == "LIST"
            and not sbstep
            and not fact
        ):
            return CommandListingOutput(
                output,
                magicwords=["SET", "TIME/FREQ"],
                columns_names=[
                    "SET",
                    "TIME/FREQ",
                    "LOAD STEP",
                    "SUBSTEP",
                    "CUMULATIVE",
                ],
            )
        else:
            return output

    @wraps(_MapdlCore.vsel)
    def vsel(self, *args, **kwargs) -> str:
        """Wraps superclassed VSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().vsel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="volu", plot_function="vplot")
        @allow_iterables_vmin(entity="volume")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.nsel)
    def nsel(self, *args, **kwargs) -> str:
        """Wraps previons NSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().nsel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities()
        @allow_iterables_vmin(entity="node")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.esel)
    def esel(self, *args, **kwargs) -> str:
        """Wraps previons ESEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().esel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="elem", plot_function="eplot")
        @allow_iterables_vmin(entity="elem")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.ksel)
    def ksel(self, *args, **kwargs) -> str:
        """Wraps superclassed KSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().ksel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="kp", plot_function="kplot")
        @allow_iterables_vmin(entity="kp")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.lsel)
    def lsel(self, *args, **kwargs) -> str:
        """Wraps superclassed LSEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().lsel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="line", plot_function="lplot")
        @allow_iterables_vmin(entity="line")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.asel)
    def asel(self, *args, **kwargs) -> str:
        """Wraps superclassed ASEL to allow to use a list/tuple/array for vmin.

        It will raise an error in case vmax or vinc are used too.
        """
        sel_func = (
            super().asel
        )  # using super() inside the wrapped function confuses the references

        @allow_pickable_entities(entity="area", plot_function="aplot")
        @allow_iterables_vmin(entity="area")
        def wrapped(self, *args, **kwargs):
            return sel_func(*args, **kwargs)

        return wrapped(self, *args, **kwargs)

    @wraps(_MapdlCore.dim)
    def dim(
        self,
        par="",
        type_="",
        imax="",
        jmax="",
        kmax="",
        var1="",
        var2="",
        var3="",
        csysid="",
        **kwargs,
    ):
        self._check_parameter_name(par)  # parameter name check
        if "(" in par or ")" in par:
            raise ValueError(
                "Parenthesis are not allowed as parameter name in 'mapdl.dim'."
            )

        return super().dim(
            par, type_, imax, jmax, kmax, var1, var2, var3, csysid, **kwargs
        )

    @wraps(_MapdlCore.mpwrite)
    def mpwrite(
        self,
        fname="",
        ext="",
        lib="",
        mat="",
        download_file=False,
        progress_bar=False,
        **kwargs,
    ):
        fname_ = fname + "." + ext
        if not self._local:
            if os.path.dirname(fname_):
                raise IOError(
                    "Only writing files to the MAPDL working directory is allowed. "
                    f"The supplied path {fname_} is not allowed."
                )

        output = super().mpwrite(fname, ext, lib, mat, **kwargs)
        if download_file:
            self.download(os.path.basename(fname_), progress_bar=progress_bar)

        return output

    @wraps(_MapdlCore.mpread)
    def mpread(self, fname="", ext="", lib="", **kwargs):
        if lib:
            raise NotImplementedError(
                "The option 'lib' is not supported by the MAPDL gRPC server."
            )

        fname_ = fname + "." + ext
        fname = load_file(self, fname_)
        self._log.info("Bypassing 'MPREAD' with 'INPUT'.")
        return self.input(fname)

    @wraps(_MapdlCore.cwd)
    def cwd(self, *args, **kwargs):
        """Wraps cwd."""
        output = super().cwd(*args, mute=False, **kwargs)

        if output is not None:
            if "*** WARNING ***" in output:
                raise IncorrectWorkingDirectory(
                    "\n" + "\n".join(output.splitlines()[1:])
                )

        return output

    @wraps(_MapdlCore.list)
    def list(self, filename, ext=""):
        """Displays the contents of an external, coded file.

        APDL Command: ``/LIST``

        Parameters
        ----------
        fname : str
            File name and directory path. An unspecified directory
            path defaults to the working directory.

        ext : str, optional
            Filename extension
        """
        if hasattr(self, "_local"):  # gRPC
            if not self._local:
                return self._download_as_raw(filename).decode()

        path = pathlib.Path(filename)
        if path.parent != ".":
            path = os.path.join(self.directory, filename)

        path = str(path) + ext
        with open(path) as fid:
            return fid.read()

    def kplot(
        self,
        np1="",
        np2="",
        ninc="",
        lab="",
        vtk=None,
        show_keypoint_numbering=True,
        **kwargs,
    ):
        """Display the selected keypoints.

        APDL Command: KPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        np1, np2, ninc
            Display keypoints from NP1 to NP2 (defaults to NP1) in
            steps of NINC (defaults to 1).  If NP1 = ALL (default),
            NP2 and NINC are ignored and all selected keypoints [KSEL]
            are displayed.

        lab
            Determines what keypoints are plotted (one of the following):

            (blank) - Plots all keypoints.

            HPT - Plots only those keypoints that are hard points.

        vtk : bool, optional
            Plot the currently selected lines using ``pyvista``.

        show_keypoint_numbering : bool, optional
            Display keypoint numbers when ``vtk=True``.



        Notes
        -----
        This command is valid in any processor.
        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    "Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("title", "MAPDL Keypoint Plot")
            if not self.geometry.n_keypoint:
                warnings.warn(
                    "Either no keypoints have been "
                    "selected or there are no keypoints in "
                    "the database."
                )
                return general_plotter([], [], [], **kwargs)

            keypoints = self.geometry.get_keypoints(return_as_array=True)
            points = [{"points": keypoints}]

            labels = []
            if show_keypoint_numbering:
                labels.append({"points": keypoints, "labels": self.geometry.knum})

            return general_plotter([], points, labels, **kwargs)

        # otherwise, use the legacy plotter
        with self._enable_interactive_plotting():
            return super().kplot(np1=np1, np2=np2, ninc=ninc, lab=lab, **kwargs)

    def lplot(
        self,
        nl1="",
        nl2="",
        ninc="",
        vtk=None,
        show_line_numbering=True,
        show_keypoint_numbering=False,
        color_lines=False,
        **kwargs,
    ):
        """Display the selected lines.

        APDL Command: LPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        nl1, nl2, ninc
            Display lines from NL1 to NL2 (defaults to NL1) in steps
            of NINC (defaults to 1).  If NL1 = ALL (default), NL2 and
            NINC are ignored and display all selected lines [LSEL].

        vtk : bool, optional
            Plot the currently selected lines using ``pyvista``.

        show_line_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        show_keypoint_numbering : bool, optional
            Number keypoints.  Only valid when ``show_keypoints=True``

        **kwargs
            See :meth:`ansys.mapdl.core.plotting.general_plotter` for
            more keyword arguments applicable when visualizing with
            ``vtk=True``.

        Notes
        -----
        Mesh divisions on plotted lines are controlled by the ``ldiv``
        option of the ``psymb`` command when ``vtk=False``.
        Otherwise, line divisions are controlled automatically.

        This command is valid in any processor.

        Examples
        --------
        >>> mapdl.lplot(vtk=True, cpos='xy', line_width=10)
        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    "Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("show_scalar_bar", False)
            kwargs.setdefault("title", "MAPDL Line Plot")
            if not self.geometry.n_line:
                warnings.warn(
                    "Either no lines have been selected or there is nothing to plot."
                )
                return general_plotter([], [], [], **kwargs)

            lines = self.geometry.get_lines(return_as_list=True)
            meshes = []

            if color_lines:
                size_ = len(lines)
                # Because this is only going to be used for plotting
                # purposes, we don't need to allocate
                # a huge vector with random numbers (colours).
                # By default `pyvista.DataSetMapper.set_scalars` `n_colors`
                # argument is set to 256, so let do here the same.
                # We will limit the number of randoms values (colours)
                # to 256.
                #
                # Link: https://docs.pyvista.org/api/plotting/_autosummary/pyvista.DataSetMapper.set_scalars.html#pyvista.DataSetMapper.set_scalars
                size_ = min([256, size_])
                # Generating a colour array,
                # Size = number of areas.
                # Values are random between 0 and min(256, number_areas)
                colors = get_ansys_colors(size_)

                # Creating a mapping of colors
                ent_num = []
                for line in lines:
                    ent_num.append(int(np.unique(line["entity_num"])[0]))
                ent_num.sort()

                # expand color array until matching the number of areas.
                # In this case we start to repeat colors in the same order.
                colors = np.resize(colors, (len(ent_num), 4))

                for line, color in zip(lines, colors):
                    meshes.append({"mesh": line, "color": color})

            else:
                for line in lines:
                    meshes.append({"mesh": line, "color": kwargs.get("color", "white")})

            labels = []
            if show_line_numbering:
                for line in lines:
                    labels.append(
                        {
                            "points": line.points[len(line.points) // 2],
                            "labels": line["entity_num"],
                        }
                    )

            if show_keypoint_numbering:
                labels.append(
                    {
                        "points": self.geometry.get_keypoints(return_as_array=True),
                        "labels": self.geometry.knum,
                    }
                )

            return general_plotter(meshes, [], labels, **kwargs)
        else:
            with self._enable_interactive_plotting():
                return super().lplot(nl1=nl1, nl2=nl2, ninc=ninc, **kwargs)

    def aplot(
        self,
        na1="",
        na2="",
        ninc="",
        degen="",
        scale="",
        vtk=None,
        quality=4,
        show_area_numbering=False,
        show_line_numbering=False,
        color_areas=False,
        show_lines=False,
        **kwargs,
    ):
        """Display the selected areas.

        Displays the selected areas from ``na1`` to ``na2`` in steps
        of ``ninc``.

        APDL Command: ``APLOT``

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        na1 : int, optional
            Minimum area to display.

        na2 : int, optional
            Maximum area to display.

        ninc : int, optional
            Increment between minimum and maximum area.

        degen, str, optional
            Degeneracy marker.  This option is ignored when ``vtk=True``.

        scale : float, optional
            Scale factor for the size of the degeneracy-marker star.
            The scale is the size in window space (-1 to 1 in both
            directions) (defaults to 0.075).  This option is ignored
            when ``vtk=True``.

        vtk : bool, optional
            Plot the currently selected areas using ``pyvista``.  As
            this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            Quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best) when ``vtk=True``.

        show_area_numbering : bool, optional
            Display area numbers when ``vtk=True``.

        show_line_numbering : bool, optional
            Display line numbers when ``vtk=True``.

        color_areas : Union[bool, str, np.array], optional
            Only used when ``vtk=True``.
            If ``color_areas`` is a bool, randomly color areas when ``True``.
            If ``color_areas`` is a string, it must be a valid color string
            which will be applied to all areas.
            If ``color_areas`` is an array or list made of color names (str) or
            the RGBa numbers ([R, G, B, transparency]), it colors each area with
            the colors, specified in that array or list.

        show_lines : bool, optional
            Plot lines and areas.  Change the thickness of the lines
            with ``line_width=``

        **kwargs
            See :meth:`ansys.mapdl.core.plotting.general_plotter` for
            more keyword arguments applicable when visualizing with
            ``vtk=True``.

        Examples
        --------
        Plot areas between 1 and 4 in increments of 2.

        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.aplot(1, 4, 2)

        Plot all areas and randomly color the areas.  Label center of
        areas by their number.

        >>> mapdl.aplot(show_area_numbering=True, color_areas=True)

        Return the plotting instance and modify it.

        >>> mapdl.aplot()
        >>> pl = mapdl.aplot(return_plotter=True)
        >>> pl.show_bounds()
        >>> pl.set_background('black')
        >>> pl.add_text('my text')
        >>> pl.show()

        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    "Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            from matplotlib.colors import to_rgba

            kwargs.setdefault("show_scalar_bar", False)
            kwargs.setdefault("title", "MAPDL Area Plot")
            kwargs.setdefault("scalar_bar_args", {"title": "Scalar Bar Title"})

            if not self.geometry.n_area:
                warnings.warn(
                    "Either no areas have been selected or there is nothing to plot."
                )
                return general_plotter([], [], [], **kwargs)

            if quality > 10:
                quality = 10
            if quality < 1:
                quality = 1
            surfs = self.geometry.get_areas(return_as_list=True, quality=quality)
            meshes = []
            labels = []

            # anums = np.unique(surf["entity_num"])
            anums = self.geometry.anum  # This might need double check

            # individual surface isolation is quite slow, so just
            # color individual areas
            if (isinstance(color_areas, np.ndarray) and len(color_areas) > 1) or (
                not isinstance(color_areas, np.ndarray) and color_areas
            ):
                if isinstance(color_areas, bool):
                    size_ = len(anums)
                    # Because this is only going to be used for plotting
                    # purposes, we don't need to allocate
                    # a huge vector with random numbers (colours).
                    # By default `pyvista.DataSetMapper.set_scalars` `n_colors`
                    # argument is set to 256, so let do here the same.
                    # We will limit the number of randoms values (colours)
                    # to 256.
                    #
                    # Link: https://docs.pyvista.org/api/plotting/_autosummary/pyvista.DataSetMapper.set_scalars.html#pyvista.DataSetMapper.set_scalars
                    size_ = min([256, size_])
                    # Generating a colour array,
                    # Size = number of areas.
                    # Values are random between 0 and min(256, number_areas)
                    colors = get_ansys_colors(size_)

                elif isinstance(color_areas, str):
                    # A color is provided as a string
                    colors = np.atleast_2d(to_rgba(color_areas))

                else:
                    if len(anums) != len(color_areas):
                        raise ValueError(
                            "The length of the parameter array 'color_areas' "
                            "should be the same as the number of areas."
                            f"\nanums: {anums}"
                            f"\ncolor_areas: {color_areas}"
                        )

                    if isinstance(color_areas[0], str):
                        colors = [to_rgba(each) for each in color_areas]
                    else:
                        colors = color_areas

                # Creating a mapping of colors
                ent_num = []
                for each_surf in surfs:
                    ent_num.append(int(np.unique(each_surf["entity_num"])[0]))
                ent_num.sort()

                # expand color array until matching the number of areas.
                # In this case we start to repeat colors in the same order.
                colors = np.resize(colors, (len(ent_num), 3))

                for surf, color in zip(surfs, colors):
                    meshes.append({"mesh": surf, "color": color})

            else:
                for surf in surfs:
                    meshes.append({"mesh": surf, "color": kwargs.get("color", "white")})

            if show_area_numbering:
                centers = []

                for surf in surfs:
                    anum = np.unique(surf["entity_num"])
                    assert (
                        len(anum) == 1
                    ), f"The pv.Unstructured from the entity {anum[0]} contains entities from other entities {anum}"  # Sanity check

                    area = surf.extract_cells(surf["entity_num"] == anum)
                    centers.append(area.center)

                labels.append({"points": np.array(centers), "labels": anums})

            if show_lines or show_line_numbering:
                kwargs.setdefault("line_width", 2)
                # subselect lines belonging to the current areas

                with self.save_selection:
                    self.lsla("S", mute=True)
                    lines = self.geometry.get_lines()

                if show_lines:
                    meshes.append(
                        {"mesh": lines, "color": kwargs.get("edge_color", "k")}
                    )
                if show_line_numbering:
                    labels.append(
                        {
                            "points": lines.points[50::101],
                            "labels": lines["entity_num"],
                        }
                    )

            return general_plotter(meshes, [], labels, **kwargs)

        with self._enable_interactive_plotting():
            return super().aplot(
                na1=na1, na2=na2, ninc=ninc, degen=degen, scale=scale, **kwargs
            )

    def vplot(
        self,
        nv1="",
        nv2="",
        ninc="",
        degen="",
        scale="",
        vtk=None,
        quality=4,
        show_volume_numbering=False,
        show_area_numbering=False,
        show_line_numbering=False,
        color_areas=False,
        show_lines=True,
        **kwargs,
    ):
        """Plot the selected volumes.

        APDL Command: VPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        nv1, nv2, ninc
            Display volumes from NV1 to NV2 (defaults to NV1) in steps
            of NINC (defaults to 1).  If NV1 = ALL (default), NV2 and
            NINC are ignored and all selected volumes [VSEL] are
            displayed.  Ignored when ``vtk=True``.

        degen
            Degeneracy marker.  ``"blank"`` No degeneracy marker is
            used (default), or ``"DEGE"``.  A red star is placed on
            keypoints at degeneracies (see the Modeling and Meshing
            Guide).  Not available if /FACET,WIRE is set.  Ignored
            when ``vtk=True``.

        scale
            Scale factor for the size of the degeneracy-marker star.  The scale
            is the size in window space (-1 to 1 in both directions) (defaults
            to .075).  Ignored when ``vtk=True``.

        vtk : bool, optional
            Plot the currently selected volumes using ``pyvista``.  As
            this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).  Applicable when ``vtk=True``.

        show_numbering : bool, optional
            Display line and keypoint numbers when ``vtk=True``.

        **kwargs
            See :meth:`ansys.mapdl.core.plotting.general_plotter` for
            more keyword arguments applicable when visualizing with
            ``vtk=True``.

        Examples
        --------
        Plot while displaying area numbers.

        >>> mapdl.vplot(show_area_numbering=True)

        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    "Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("title", "MAPDL Volume Plot")
            if not self.geometry.n_volu:
                warnings.warn(
                    "Either no volumes have been selected or there is nothing to plot."
                )
                return general_plotter([], [], [], **kwargs)

            # Storing entities selection
            with self.save_selection:
                volumes = self.geometry.vnum
                meshes = []
                points = []
                labels = []

                return_plotter = kwargs.pop("return_plotter", False)
                color_areas = True

                for each_volu in volumes:
                    self.vsel("S", vmin=each_volu)
                    self.aslv("S", mute=True)  # select areas attached to active volumes

                    pl = self.aplot(
                        vtk=True,
                        color_areas=color_areas,
                        quality=quality,
                        show_area_numbering=show_area_numbering,
                        show_line_numbering=show_line_numbering,
                        show_lines=show_lines,
                        return_plotter=True,
                        **kwargs,
                    )

                    meshes_ = get_meshes_from_plotter(pl)

                    for each_mesh in meshes_:
                        each_mesh.cell_data["entity_num"] = int(each_volu)

                    meshes.extend(meshes_)

                meshes = [{"mesh": meshes}]

            return general_plotter(
                meshes, points, labels, return_plotter=return_plotter, **kwargs
            )

        else:
            with self._enable_interactive_plotting():
                return super().vplot(
                    nv1=nv1, nv2=nv2, ninc=ninc, degen=degen, scale=scale, **kwargs
                )

    def nplot(self, nnum="", vtk=None, **kwargs):
        """APDL Command: NPLOT

        Displays nodes.

        .. note::
           PyMAPDL plotting commands with ``vtk=True`` ignore any
           values set with the ``PNUM`` command.

        Parameters
        ----------
        nnum : bool, int, optional
            Node number key:

            - ``False`` : No node numbers on display (default).
            - ``True`` : Include node numbers on display.

            .. note::
               This parameter is only valid when ``vtk==True``

        vtk : bool, optional
            Plot the currently selected nodes using ``pyvista``.
            Defaults to current ``use_vtk`` setting as set on the
            initialization of MAPDL.

        plot_bc : bool, optional
            Activate the plotting of the boundary conditions.
            Defaults to ``False``.

            .. warning:: This is in alpha state.

        plot_bc_legend : bool, optional
            Shows the boundary conditions legend.
            Defaults to ``False``

        plot_bc_labels : bool, optional
            Shows the boundary conditions label per node.
            Defaults to ``False``.

        bc_labels : List[str], Tuple(str), optional
            List or tuple of strings with the boundary conditions
            to plot, i.e. ``["UX", "UZ"]``.
            You can obtain the allowed boundary conditions by
            evaluating ``ansys.mapdl.core.plotting.BCS``.
            You can use also the following shortcuts:

            * **'mechanical'**
              To plot the following mechanical boundary conditions: ``'UX'``,
              ``'UY'``, ``'UZ'``, ``'FX'``, ``'FY'``, and ``'FZ'``.  Rotational
              or momentum boundary conditions are not allowed.

            * ``'thermal'``
              To plot the following boundary conditions: 'TEMP' and
              'HEAT'.

            * ``'electrical'``
              To plot the following electrical boundary conditions:
              ``'VOLT'``, ``'CHRGS'``, and ``'AMPS'``.

            Defaults to all the allowed boundary conditions present
            in the responses of :func:`ansys.mapdl.core.Mapdl.dlist`
            and :func:`ansys.mapdl.core.Mapdl.flist()`.

        bc_target : List[str], Tuple(str), optional
            Specify the boundary conditions target
            to plot, i.e. "Nodes", "Elements".
            You can obtain the allowed boundary conditions target by
            evaluating ``ansys.mapdl.core.plotting.ALLOWED_TARGETS``.
            Defaults to only ``"Nodes"``.

        bc_glyph_size : float, optional
            Specify the size of the glyph used for the boundary
            conditions plotting.
            By default is ratio of the bounding box dimensions.

        bc_labels_font_size : float, optional
            Size of the text on the boundary conditions labels.
            By default it is 16.

        Examples
        --------
        Plot using VTK while showing labels and changing the background.

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(
        ...     nnum=True,
        ...     vtk=True,
        ...     background='w',
        ...     color='k',
        ...     show_bounds=True
        ... )

        Plot without using VTK.

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(vtk=False)

        Plot nodal boundary conditions.

        >>> mapdl.nplot(
        ...     plot_bc=True,
        ...     plot_bc_labels=True,
        ...     bc_labels="mechanical",
        ... )

        """
        if vtk is None:
            vtk = self._use_vtk

        if vtk is True:
            if _HAS_PYVISTA:
                # lazy import here to avoid top level import
                import pyvista as pv
            else:  # pragma: no cover
                raise ModuleNotFoundError(
                    "Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if "knum" in kwargs:
            raise ValueError("`knum` keyword deprecated.  Please use `nnum` instead.")

        if vtk:
            kwargs.setdefault("title", "MAPDL Node Plot")
            if not self.mesh.n_node:
                warnings.warn("There are no nodes to plot.")
                return general_plotter([], [], [], mapdl=self, **kwargs)

            labels = []
            if nnum:
                # must eliminate duplicate points or labeling fails miserably.
                pcloud = pv.PolyData(self.mesh.nodes)
                pcloud["labels"] = self.mesh.nnum
                pcloud.clean(inplace=True)

                labels = [{"points": pcloud.points, "labels": pcloud["labels"]}]
            points = [{"points": self.mesh.nodes}]
            return general_plotter([], points, labels, mapdl=self, **kwargs)

        # otherwise, use the built-in nplot
        if isinstance(nnum, bool):
            nnum = int(nnum)

        with self._enable_interactive_plotting():
            return super().nplot(nnum, **kwargs)

    def eplot(self, show_node_numbering=False, vtk=None, **kwargs):
        """Plots the currently selected elements.

        APDL Command: EPLOT

        .. note::
            PyMAPDL plotting commands with ``vtk=True`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        vtk : bool, optional
            Plot the currently selected elements using ``pyvista``.
            Defaults to current ``use_vtk`` setting.

        show_node_numbering : bool, optional
            Plot the node numbers of surface nodes.

        plot_bc : bool, optional
            Activate the plotting of the boundary conditions.
            Defaults to ``False``.

            .. warning:: This is in alpha state.

        plot_bc_legend : bool, optional
            Shows the boundary conditions legend.
            Defaults to ``False``

        plot_bc_labels : bool, optional
            Shows the boundary conditions label per node.
            Defaults to ``False``.

        bc_labels : List[str], Tuple(str), optional
            List or tuple of strings with the boundary conditions
            to plot, i.e. ``["UX", "UZ"]``.
            You can obtain the allowed boundary conditions by
            evaluating ``ansys.mapdl.core.plotting.BCS``.
            You can use also the following shortcuts:

            * **'mechanical'**
              To plot the following mechanical boundary conditions: ``'UX'``,
              ``'UY'``, ``'UZ'``, ``'FX'``, ``'FY'``, and ``'FZ'``.  Rotational
              or momentum boundary conditions are not allowed.

            * ``'thermal'``
              To plot the following boundary conditions: 'TEMP' and
              'HEAT'.

            * ``'electrical'``
              To plot the following electrical boundary conditions:
              ``'VOLT'``, ``'CHRGS'``, and ``'AMPS'``.

            Defaults to all the allowed boundary conditions present
            in the responses of :func:`ansys.mapdl.core.Mapdl.dlist`
            and :func:`ansys.mapdl.core.Mapdl.flist()`.

        bc_target : List[str], Tuple(str), optional
            Specify the boundary conditions target
            to plot, i.e. "Nodes", "Elements".
            You can obtain the allowed boundary conditions target by
            evaluating ``ansys.mapdl.core.plotting.ALLOWED_TARGETS``.
            Defaults to only ``"Nodes"``.

        bc_glyph_size : float, optional
            Specify the size of the glyph used for the boundary
            conditions plotting.
            By default is ratio of the bounding box dimensions.

        bc_labels_font_size : float, optional
            Size of the text on the boundary conditions labels.
            By default it is 16.

        **kwargs
            See ``help(ansys.mapdl.core.plotter.general_plotter)`` for more
            keyword arguments related to visualizing using ``vtk``.

        Examples
        --------
        >>> mapdl.clear()
        >>> mapdl.prep7()
        >>> mapdl.block(0, 1, 0, 1, 0, 1)
        >>> mapdl.et(1, 186)
        >>> mapdl.esize(0.1)
        >>> mapdl.vmesh('ALL')
        >>> mapdl.vgen(2, 'all')
        >>> mapdl.eplot(show_edges=True, smooth_shading=True,
                        show_node_numbering=True)

        Save a screenshot to disk without showing the plot

        >>> mapdl.eplot(background='w', show_edges=True, smooth_shading=True,
                        window_size=[1920, 1080], savefig='screenshot.png',
                        off_screen=True)

        """
        if vtk is None:
            vtk = self._use_vtk
        elif vtk is True:
            if not _HAS_PYVISTA:  # pragma: no cover
                raise ModuleNotFoundError(
                    "Using the keyword argument 'vtk' requires having Pyvista installed."
                )

        if vtk:
            kwargs.setdefault("title", "MAPDL Element Plot")
            if not self._mesh.n_elem:
                warnings.warn("There are no elements to plot.")
                return general_plotter([], [], [], mapdl=self, **kwargs)

            # TODO: Consider caching the surface
            esurf = self.mesh._grid.linear_copy().extract_surface().clean()
            kwargs.setdefault("show_edges", True)

            # if show_node_numbering:
            labels = []
            if show_node_numbering:
                labels = [{"points": esurf.points, "labels": esurf["ansys_node_num"]}]

            return general_plotter(
                [{"mesh": esurf, "style": kwargs.pop("style", "surface")}],
                [],
                labels,
                mapdl=self,
                **kwargs,
            )

        # otherwise, use MAPDL plotter
        with self._enable_interactive_plotting():
            return self.run("EPLOT", **kwargs)

    def clear(self, *args, **kwargs):
        """Clear the database.

        APDL Command: ``/CLEAR``

        Resets the ANSYS database to the conditions at the beginning
        of the problem.  Sets the import and Boolean options back to
        the ANSYS default. All items are deleted from the database and
        memory values are set to zero for items derived from database
        information.  All files are left intact.  This command is
        useful between multiple analyses in the same run, or between
        passes of a multi-pass analysis (such as between the
        substructure generation, use, and expansion passes).  Should
        not be used in a do-loop since loop counters will be reset.
        on the same line as the ``/CLEAR`` command.

        ``/CLEAR`` resets the jobname to match the currently open
        session .LOG and .ERR files. This will return the jobname to
        its original value, or to the most recent value specified on
        ``/FILNAME`` with KEY = 1.

        This command is valid only at the Begin level.

        Examples
        --------
        >>> mapdl.clear()

        """
        if self.is_grpc:
            self._create_session()
        self.run("/CLE,NOSTART", mute=True)

    @wraps(_MapdlCore.cmplot)
    def cmplot(self, label: str = "", entity: str = "", keyword: str = "", **kwargs):
        """Wraps cmplot"""

        label = label.upper()
        entity = entity.upper()

        if label in ["N", "P"]:
            raise ValueError(f"The label '{label}' is not supported.")

        if (not label or label == "ALL") and not entity:
            raise ValueError(
                "If not using label or label =='ALL', then you "
                "need to provide a valid entity."
            )

        if label != "ALL":
            if label not in self.components:
                raise ComponentDoesNotExits(f"The component '{label}' does not exist.")

            if not entity:
                entity = self.components[label].type
            else:
                entity_ = self.components[label].type
                if entity_.upper() != entity.upper():
                    raise ValueError(
                        f"The component entity supplied '{entity}' "
                        "does not seems to match the component "
                        f"type '{entity_}' with name '{label}' "
                        "in MAPDL."
                    )

        if label and not entity:
            # supposing entity
            entity = self.components[label].type

        if entity[:4] not in ["NODE", "ELEM", "KP", "LINE", "AREA", "VOLU"]:
            raise ValueError(f"The entity '{entity}' is not allowed.")

        cmps_names = self.components.names
        self.cm("__tmp_cm__", entity=entity)
        if label == "ALL":
            self.cmsel("ALL", entity=entity)
        else:
            self.cmsel("S", name=label, entity=entity)

        mapping = {
            "NODE": self.nplot,
            "ELEM": self.eplot,
            "KP": self.kplot,
            "LINE": self.lplot,
            "AREA": self.aplot,
            "VOLU": self.vplot,
        }
        func = mapping[entity]

        kwargs.setdefault("title", "PyMAPDL CMPLOT")
        output = func(**kwargs)

        # returning to previous selection
        self.cmsel("s", "__tmp_cm__", entity=entity)
        self.components.select(cmps_names)
        return output

    @wraps(_MapdlCore.inquire)
    def inquire(self, strarray="", func="", arg1="", arg2=""):
        """Wraps original INQUIRE function"""
        func_options = [
            "LOGIN",
            "DOCU",
            "APDL",
            "PROG",
            "AUTH",
            "USER",
            "DIRECTORY",
            "JOBNAME",
            "RSTDIR",
            "RSTFILE",
            "RSTEXT",
            "OUTPUT",
            "ENV",
            "TITLE",
            "EXIST",
            "DATE",
            "SIZE",
            "WRITE",
            "READ",
            "EXEC",
            "LINES",
        ]

        if strarray.upper() in func_options and func.upper() not in func_options:
            # Likely you are using the old ``_Mapdl.inquire`` implementation.
            raise ValueError(
                "Arguments of this method have changed. `Mapdl.inquire` now includes the optional `strarray` parameter "
                f"as the first argument. Either use `inquire(func={strarray})`, or `inquire("
                ", {strarray})`"
            )

        if func == "":
            func = "DIRECTORY"

        if strarray.upper() not in func_options and func.upper() not in func_options:
            raise ValueError(
                f"The arguments (strarray='{strarray}', func='{func}') are not valid."
            )

        response = self.run(f"/INQUIRE,{strarray},{func},{arg1},{arg2}", mute=False)
        if func.upper() in [
            "ENV",
            "TITLE",
        ]:  # the output is multiline, we just need the last line.
            response = response.splitlines()[-1]

        return response.split("=")[1].strip()

    @wraps(_MapdlCore.parres)
    def parres(self, lab="", fname="", ext="", **kwargs):
        """Wraps the original /PARRES function"""
        if not fname:
            fname = self.jobname

        fname = self._get_file_name(
            fname=fname, ext=ext, default_extension="parm"
        )  # Although documentation says `PARM`

        # Getting the path for local/remote
        filename = self._get_file_path(fname, progress_bar=False)

        return self.input(filename)

    @wraps(_MapdlCore.lgwrite)
    def lgwrite(self, fname="", ext="", kedit="", remove_grpc_extra=True, **kwargs):
        """Wraps original /LGWRITE"""
        if not fname:
            fname = self.jobname

        fname = self._get_file_name(fname=fname, ext=ext, default_extension="lgw")

        if self.is_local:
            fname_ = fname
        else:
            file_, ext_, _ = self._decompose_fname(fname)
            fname_ = self._get_file_name(fname=file_, ext=ext_)

        # generate the log and download if necessary
        output = super().lgwrite(fname=fname_, kedit=kedit, **kwargs)

        # Let's download the file to the location
        self._download(fname_, fname)
        fname_ = fname  # Update path

        # remove extra grpc /OUT commands
        REMOVE_LINES = ("/OUT", "/OUT,anstmp")
        REMOVE_LINES_STARTING = (
            "*SET,__PYMAPDL_SESSION_ID__",
            "! *STATUS,__PYMAPDL_SESSION_ID__",
            "*STATUS,__PYMAPDL_SESSION_ID__",
        )

        if remove_grpc_extra and self.is_grpc:
            with open(fname_, "r") as fid:
                lines = [
                    line.strip() + "\n"
                    for line in fid
                    if (
                        line.strip() not in REMOVE_LINES
                        and not line.startswith(REMOVE_LINES_STARTING)
                    )
                ]

            with open(fname_, "w") as fid:
                fid.writelines(lines)

        return output

    @wraps(_MapdlCore.vwrite)
    def vwrite(
        self,
        par1="",
        par2="",
        par3="",
        par4="",
        par5="",
        par6="",
        par7="",
        par8="",
        par9="",
        par10="",
        par11="",
        par12="",
        par13="",
        par14="",
        par15="",
        par16="",
        par17="",
        par18="",
        par19="",
        **kwargs,
    ):
        """Wrapping *VWRITE"""

        # cannot be run in interactive mode
        if not self._store_commands:
            raise MapdlRuntimeError(
                "VWRTIE cannot run interactively.  \n\nPlease use "
                "``with mapdl.non_interactive:``"
            )

        return super().vwrite(
            par1=par1,
            par2=par2,
            par3=par3,
            par4=par4,
            par5=par5,
            par6=par6,
            par7=par7,
            par8=par8,
            par9=par9,
            par10=par10,
            par11=par11,
            par12=par12,
            par13=par13,
            par14=par14,
            par15=par15,
            par16=par16,
            par17=par17,
            par18=par18,
            par19=par19,
            **kwargs,
        )

    @wraps(_MapdlCore.nrm)
    def nrm(self, name="", normtype="", parr="", normalize="", **kwargs):
        """Wraps *NRM"""
        if not parr:
            parr = "__temp_par__"
        super().nrm(
            name=name, normtype=normtype, parr=parr, normalize=normalize, **kwargs
        )
        return self.parameters[parr]

    @wraps(_MapdlCore.com)
    def com(self, comment="", **kwargs):
        """Wraps /COM"""
        if self.print_com and not self.mute and not kwargs.get("mute", False):
            print("/COM,%s" % (str(comment)))

        return super().com(comment=comment, **kwargs)

    @wraps(_MapdlCore.lssolve)
    def lssolve(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """Wraps LSSOLVE"""
        with self.non_interactive:
            super().lssolve(lsmin=lsmin, lsmax=lsmax, lsinc=lsinc, **kwargs)
        return self.last_response

    @wraps(_MapdlCore.edasmp)
    def edasmp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edasmp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edasmp(*args, **kwargs)

    @wraps(_MapdlCore.edbound)
    def edbound(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edbound()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edbound(*args, **kwargs)

    @wraps(_MapdlCore.edbx)
    def edbx(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edbx()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edbx(*args, **kwargs)

    @wraps(_MapdlCore.edcgen)
    def edcgen(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcgen()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcgen(*args, **kwargs)

    @wraps(_MapdlCore.edclist)
    def edclist(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edclist()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edclist(*args, **kwargs)

    @wraps(_MapdlCore.edcmore)
    def edcmore(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcmore()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcmore(*args, **kwargs)

    @wraps(_MapdlCore.edcnstr)
    def edcnstr(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcnstr()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcnstr(*args, **kwargs)

    @wraps(_MapdlCore.edcontact)
    def edcontact(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcontact()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcontact(*args, **kwargs)

    @wraps(_MapdlCore.edcrb)
    def edcrb(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcrb()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcrb(*args, **kwargs)

    @wraps(_MapdlCore.edcurve)
    def edcurve(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcurve()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcurve(*args, **kwargs)

    @wraps(_MapdlCore.eddbl)
    def eddbl(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddbl()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddbl(*args, **kwargs)

    @wraps(_MapdlCore.eddc)
    def eddc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddc(*args, **kwargs)

    @wraps(_MapdlCore.edipart)
    def edipart(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edipart()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edipart(*args, **kwargs)

    @wraps(_MapdlCore.edlcs)
    def edlcs(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edlcs()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edlcs(*args, **kwargs)

    @wraps(_MapdlCore.edmp)
    def edmp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edmp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edmp(*args, **kwargs)

    @wraps(_MapdlCore.ednb)
    def ednb(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.ednb()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().ednb(*args, **kwargs)

    @wraps(_MapdlCore.edndtsd)
    def edndtsd(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edndtsd()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edndtsd(*args, **kwargs)

    @wraps(_MapdlCore.ednrot)
    def ednrot(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.ednrot()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().ednrot(*args, **kwargs)

    @wraps(_MapdlCore.edpart)
    def edpart(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpart()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpart(*args, **kwargs)

    @wraps(_MapdlCore.edpc)
    def edpc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpc(*args, **kwargs)

    @wraps(_MapdlCore.edsp)
    def edsp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edsp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edsp(*args, **kwargs)

    @wraps(_MapdlCore.edweld)
    def edweld(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edweld()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edweld(*args, **kwargs)

    @wraps(_MapdlCore.edadapt)
    def edadapt(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edadapt()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edadapt(*args, **kwargs)

    @wraps(_MapdlCore.edale)
    def edale(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edale()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edale(*args, **kwargs)

    @wraps(_MapdlCore.edbvis)
    def edbvis(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edbvis()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edbvis(*args, **kwargs)

    @wraps(_MapdlCore.edcadapt)
    def edcadapt(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcadapt()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcadapt(*args, **kwargs)

    @wraps(_MapdlCore.edcpu)
    def edcpu(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcpu()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcpu(*args, **kwargs)

    @wraps(_MapdlCore.edcsc)
    def edcsc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcsc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcsc(*args, **kwargs)

    @wraps(_MapdlCore.edcts)
    def edcts(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edcts()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edcts(*args, **kwargs)

    @wraps(_MapdlCore.eddamp)
    def eddamp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddamp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddamp(*args, **kwargs)

    @wraps(_MapdlCore.eddrelax)
    def eddrelax(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddrelax()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddrelax(*args, **kwargs)

    @wraps(_MapdlCore.eddump)
    def eddump(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.eddump()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().eddump(*args, **kwargs)

    @wraps(_MapdlCore.edenergy)
    def edenergy(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edenergy()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edenergy(*args, **kwargs)

    @wraps(_MapdlCore.edfplot)
    def edfplot(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edfplot()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edfplot(*args, **kwargs)

    @wraps(_MapdlCore.edgcale)
    def edgcale(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edgcale()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edgcale(*args, **kwargs)

    @wraps(_MapdlCore.edhgls)
    def edhgls(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edhgls()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edhgls(*args, **kwargs)

    @wraps(_MapdlCore.edhist)
    def edhist(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edhist()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edhist(*args, **kwargs)

    @wraps(_MapdlCore.edhtime)
    def edhtime(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edhtime()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edhtime(*args, **kwargs)

    @wraps(_MapdlCore.edint)
    def edint(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edint()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edint(*args, **kwargs)

    @wraps(_MapdlCore.edis)
    def edis(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edis()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edis(*args, **kwargs)

    @wraps(_MapdlCore.edload)
    def edload(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edload()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edload(*args, **kwargs)

    @wraps(_MapdlCore.edopt)
    def edopt(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edopt()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edopt(*args, **kwargs)

    @wraps(_MapdlCore.edout)
    def edout(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edout()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edout(*args, **kwargs)

    @wraps(_MapdlCore.edpl)
    def edpl(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpl()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpl(*args, **kwargs)

    @wraps(_MapdlCore.edpvel)
    def edpvel(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edpvel()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edpvel(*args, **kwargs)

    @wraps(_MapdlCore.edrc)
    def edrc(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrc()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrc(*args, **kwargs)

    @wraps(_MapdlCore.edrd)
    def edrd(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrd()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrd(*args, **kwargs)

    @wraps(_MapdlCore.edri)
    def edri(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edri()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edri(*args, **kwargs)

    @wraps(_MapdlCore.edrst)
    def edrst(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrst()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrst(*args, **kwargs)

    @wraps(_MapdlCore.edrun)
    def edrun(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edrun()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edrun(*args, **kwargs)

    @wraps(_MapdlCore.edshell)
    def edshell(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edshell()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edshell(*args, **kwargs)

    @wraps(_MapdlCore.edsolv)
    def edsolv(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edsolv()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edsolv(*args, **kwargs)

    @wraps(_MapdlCore.edstart)
    def edstart(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edstart()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edstart(*args, **kwargs)

    @wraps(_MapdlCore.edterm)
    def edterm(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edterm()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edterm(*args, **kwargs)

    @wraps(_MapdlCore.edtp)
    def edtp(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edtp()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edtp(*args, **kwargs)

    @wraps(_MapdlCore.edvel)
    def edvel(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edvel()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edvel(*args, **kwargs)

    @wraps(_MapdlCore.edwrite)
    def edwrite(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.edwrite()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().edwrite(*args, **kwargs)

    @wraps(_MapdlCore.rexport)
    def rexport(self, *args, **kwargs):
        if self.version >= 19.1:
            raise CommandDeprecated(
                "The command 'Mapdl.rexport()' for explicit analysis was deprecated in Ansys 19.1"
            )
        super().rexport(*args, **kwargs)

    @wraps(_MapdlCore.get)
    def get(
        self,
        par: str = "__floatparameter__",
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        item3: MapdlFloat = "",
        it3num: MapdlFloat = "",
        item4: MapdlFloat = "",
        it4num: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> Union[float, str]:
        self._check_parameter_name(par)

        command = f"*GET,{par},{entity},{entnum},{item1},{it1num},{item2},{it2num},{item3},{it3num},{item4},{it4num}"
        kwargs["mute"] = False

        # Checking printout is not suppressed by checking "wrinqr" flag.
        with self.force_output:
            response = self.run(command, **kwargs)

        if self._store_commands:
            # Return early in non_interactive
            return

        value = response.split("=")[-1].strip()
        if item3:
            if len(value.splitlines()) > 1:
                self._log.info(
                    f"The command '{command}' is showing the next message: '{value.splitlines()[1].strip()}'"
                )
            value = value.splitlines()[0]

        try:  # always either a float or string
            return float(value)
        except ValueError:
            return value

    @wraps(_MapdlCore.cmlist)
    def cmlist(self, *args, **kwargs):
        from ansys.mapdl.core.commands import ComponentListing

        return ComponentListing(super().cmlist(*args, **kwargs))


class _MapdlExtended(_MapdlCommandExtended):
    """Extend Mapdl class with new functions"""

    def load_table(self, name, array, var1="", var2="", var3="", csysid=""):
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
            self.dim(
                name,
                "TABLE",
                imax=array.shape[0],
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

        # weird bug where MAPDL ignores the first row when there are greater than 2 columns
        if array.shape[1] > 2:
            array = np.vstack((array[0], array))

        base_name = random_string() + ".txt"
        filename = os.path.join(tempfile.gettempdir(), base_name)
        np.savetxt(filename, array, header="File generated by PyMAPDL:load_table")

        if not self._local:
            self.upload(filename, progress_bar=False)
            filename = base_name
        # skip the first line its a header we wrote in np.savetxt
        self.tread(name, filename, nskip=1, mute=True)

        if self._local:
            os.remove(filename)
        else:
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
            array,
            delimiter=",",
            header="File generated by PyMAPDL:load_array",
            fmt="%24.18e",
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
            fmt = "(" + ",',',".join(["E24.18" for i in range(jmax)]) + ")"
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
            self.vwrite("%s(1)" % parm_name)
            self.run("(F20.12)")

        array = np.fromstring(self.last_response, sep="\n")

        if delete_after or "__vget_tmp_" in parm_name:
            self.run(f"{parm_name}=")

        if dtype:
            return array.astype(dtype)
        else:
            return array

    def get_nodal_constrains(self, label=None):
        """
        Get the applied nodal constrains:

        Uses ``DLIST``.

        Parameters
        ----------
        label : [str], optional
            If given, the output nodal constrains are filtered to correspondent given label.
            Example of labels are ``UX``, ``UZ``, ``VOLT`` or ``TEMP``. By default None

        Returns
        -------
        List[List[Str]] or numpy.array
            If parameter ``label`` is give, the output is converted to a
            numpy array instead of a list of list of strings.
        """
        constrains = self.dlist().to_list()
        if label:
            constrains = np.array(
                [[each[0], each[2], each[3]] for each in constrains if each[1] == label]
            )
        return constrains

    def get_nodal_loads(self, label=None):
        """
        Get the applied nodal loads.

        Uses ``FLIST``.

        Parameters
        ----------
        label : [str], optional
            If given, the output nodal loads are filtered to correspondent given label.
            Example of labels are ``FX``, ``FZ``, ``CHRGS`` or ``CSGZ``. By default None

        Returns
        -------
        List[List[Str]] or numpy.array
            If parameter ``label`` is give, the output is converted to a
            numpy array instead of a list of list of strings.
        """
        loads = self.flist().to_list()
        if label:
            loads = np.array(
                [[each[0], each[2], each[3]] for each in loads if each[1] == label]
            )
        return loads

    def modal_analysis(
        self,
        method="lanb",
        nmode="",
        freqb="",
        freqe="",
        cpxmod="",
        nrmkey="",
        modtype="",
        memory_option="",
        mxpand="",
        elcalc=False,
    ) -> str:
        """Run a modal with basic settings analysis

        Parameters
        ----------
        method : str
            Mode-extraction method to be used for the modal analysis.
            Defaults to lanb (block lanczos).  Must be one of the following:

            - LANB : Block Lanczos
            - LANPCG : PCG Lanczos
            - SNODE : Supernode modal solver
            - SUBSP : Subspace algorithm
            - UNSYM : Unsymmetric matrix
            - DAMP : Damped system
            - QRDAMP : Damped system using QR algorithm
            - VT : Variational Technology

        nmode : int, optional
            The number of modes to extract. The value can depend on
            the value supplied for Method. NMODE has no default and
            must be specified. If Method = LANB, LANPCG, or SNODE, the
            number of modes that can be extracted can equal the DOFs
            in the model after the application of all boundary
            conditions.

        freqb : float, optional
            The beginning, or lower end, of the frequency range of
            interest.

        freqe : float, optional
            The ending, or upper end, of the frequency range of
            interest (in Hz). The default for Method = SNODE is
            described below. The default for all other methods is to
            calculate all modes, regardless of their maximum
            frequency.

        cpxmod : str, optional
            Complex eigenmode key. Valid only when ``method='QRDAMP'``
            or ``method='unsym'``

            - AUTO : Determine automatically if the eigensolutions are
              real or complex and output them accordingly. This is
              the default for ``method='UNSYM'``.  Not supported for
              Method = QRDAMP.
            - ON or CPLX : Calculate and output complex eigenmode
              shapes.
            - OFF or REAL : Do not calculate complex eigenmode
              shapes. This is required if a mode-
              superposition analysis is intended after the
              modal analysis for Method = QRDAMP. This is the
              default for this method.

        nrmkey : bool, optional
            Mode shape normalization key.  When ``True`` (default),
            normalize the mode shapes to the mass matrix.  When False,
            Normalize the mode shapes to unity instead of to the mass
            matrix.  If a subsequent spectrum or mode-superposition
            analysis is planned, the mode shapes should be normalized
            to the mass matrix.

        modtype : str, optional
            Type of modes calculated by the eigensolver. Only
            applicable to the unsymmetric eigensolver.

            - Blank : Right eigenmodes. This value is the default.
            - BOTH : Right and left eigenmodes. The left eigenmodes are
              written to Jobname.LMODE.  This option must be
              activated if a mode-superposition analysis is intended.

        memory_option : str, optional
            Memory allocation option:

            * ``DEFAULT`` - Default Memory mode
                      Use the default memory allocation strategy for
                      the sparse solver. The default strategy attempts
                      to run in the INCORE memory mode. If there is
                      not enough available physical memory when the
                      solver starts to run in the ``INCORE`` memory
                      mode, the solver will then attempt to run in the
                      ``OUTOFCORE`` memory mode.

            * ``INCORE`` - In-core memory mode
                     Use a memory allocation strategy in the sparse
                     solver that will attempt to obtain enough memory
                     to run with the entire factorized matrix in
                     memory. This option uses the most amount of
                     memory and should avoid doing any I/O. By
                     avoiding I/O, this option achieves optimal solver
                     performance. However, a significant amount of
                     memory is required to run in this mode, and it is
                     only recommended on machines with a large amount
                     of memory. If the allocation for in-core memory
                     fails, the solver will automatically revert to
                     out-of-core memory mode.

            * ``OUTOFCORE`` - Out of core memory mode.
                        Use a memory allocation strategy in the sparse
                        solver that will attempt to allocate only
                        enough work space to factor each individual
                        frontal matrix in memory, but will store the
                        entire factorized matrix on disk. Typically,
                        this memory mode results in poor performance
                        due to the potential bottleneck caused by the
                        I/O to the various files written by the
                        solver.

        mxpand : bool, optional
            Number of modes or array name (enclosed in percent signs)
            to expand and write.  If -1, do not expand and do not
            write modes to the results file during the
            analysis. Default ``""``.
        elcalc : bool, optional
            Calculate element results, reaction forces, energies, and
            the nodal degree of freedom solution.  Default ``False``.

        Returns
        -------
        str
            Output from MAPDL SOLVE command.

        Notes
        -----
        For models that involve a non-symmetric element stiffness
        matrix, as in the case of a contact element with frictional
        contact, the QRDAMP eigensolver (MODOPT, QRDAMP) extracts
        modes in the modal subspace formed by the eigenmodes from the
        symmetrized eigenproblem. The QRDAMP eigensolver symmetrizes
        the element stiffness matrix on the first pass of the
        eigensolution, and in the second pass, eigenmodes are
        extracted in the modal subspace of the first eigensolution
        pass. For such non- symmetric eigenproblems, you should verify
        the eigenvalue and eigenmode results using the non-symmetric
        matrix eigensolver (MODOPT,UNSYM).

        The DAMP and QRDAMP options cannot be followed by a subsequent
        spectrum analysis. The UNSYM method supports spectrum analysis
        when eigensolutions are real.

        Examples
        --------
        Modal analysis using default parameters for the first 6 modes

        >>> mapdl.modal_analysis(nmode=6)

        """
        if nrmkey:
            if nrmkey.upper() != "OFF":
                nrmkey = "ON"
        nrmkey = "OFF"

        self.slashsolu(mute=True)
        self.antype(2, "new", mute=True)
        self.modopt(method, nmode, freqb, freqe, cpxmod, nrmkey, modtype, mute=True)
        self.bcsoption(memory_option, mute=True)

        if mxpand:
            self.mxpand(mute=True)
        if elcalc:
            self.mxpand(elcalc="YES", mute=True)

        out = self.solve()
        self.finish(mute=True)
        return out

    def get_value(
        self,
        entity: str = "",
        entnum: str = "",
        item1: str = "",
        it1num: MapdlFloat = "",
        item2: str = "",
        it2num: MapdlFloat = "",
        item3: MapdlFloat = "",
        it3num: MapdlFloat = "",
        item4: MapdlFloat = "",
        it4num: MapdlFloat = "",
        **kwargs: KwargDict,
    ) -> Union[float, str]:
        """Runs the MAPDL GET command and returns a Python value.

        This method uses :func:`Mapdl.get`.

        See the full MADPL command documentation at `*GET
        <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_GET.html>`_

        .. note::
           This method is not available when within the
           :func:`Mapdl.non_interactive`
           context manager.

        Parameters
        ----------
        entity : str
            Entity keyword. Valid keywords are ``"NODE"``, ``"ELEM"``,
            ``"KP"``, ``"LINE"``, ``"AREA"``, ``"VOLU"``, ``"PDS"``,
            etc.

        entnum : str, int, optional
            The number or label for the entity. In some cases, a zero
            (or blank ``""``) ``entnum`` represents all entities of
            the set.

        item1 : str, optional
            The name of a particular item for the given entity.

        it1num : str, int, optional
            The number (or label) for the specified Item1 (if
            any). Some Item1 labels do not require an IT1NUM value.

        item2 : str, optional
            A second set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it2num : str, int, optional
            The number (or label) for the specified ``item2`` (if
            any). Some ``item2`` labels do not require an ``it2num``
            value.

        item3 : str, optional
            A third set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this
            level of information.

        it3num : str, int, optional
            The number (or label) for the specified ``item3`` (if
            any). Some ``item3`` labels do not require an ``it3num``
            value.

        item4 : str, optional
            A fourth set of item labels and numbers to further qualify the item
            for which data are to be retrieved. Most items do not require this level of information.

        it4num : str, int, optional
            The number (or label) for the specified ``item4`` (if
            any). Some ``item4`` labels do not require an ``it4num``
            value.

        Returns
        -------
        float
            Floating point value of the parameter.

        Examples
        --------
        Retrieve the number of nodes.

        >>> value = ansys.get_value('node', '', 'count')
        >>> value
        3003

        Retrieve the number of nodes using keywords.

        >>> value = ansys.get_value(entity='node', item1='count')
        >>> value
        3003
        """
        return self._get(
            entity=entity,
            entnum=entnum,
            item1=item1,
            it1num=it1num,
            item2=item2,
            it2num=it2num,
            item3=item3,
            it3num=it3num,
            item4=item4,
            it4num=it4num,
            **kwargs,
        )
