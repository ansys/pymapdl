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


"""The plotting commands MAPDL extended mixin."""

import warnings
from functools import wraps

import numpy as np

from ansys.mapdl.core.errors import ComponentDoesNotExits
from ansys.mapdl.core.mapdl_core import _MapdlCore
from ansys.mapdl.core.misc import check_deprecated_vtk_kwargs, requires_graphics
from ansys.mapdl.core.plotting import GraphicsBackend

from . import _ExtendedMixinBase


class _ExtendedPlottingCommandsMixin(_ExtendedMixinBase):
    """Static responsibility mixin for the extended MAPDL facade."""

    @check_deprecated_vtk_kwargs
    @requires_graphics
    def kplot(
        self,
        np1="",
        np2="",
        ninc="",
        lab="",
        *,
        graphics_backend=None,
        show_keypoint_numbering=True,
        **kwargs,
    ):
        """Display the selected keypoints.

        APDL Command: KPLOT

        .. note::
            PyMAPDL plotting commands with ``graphics_backend=GraphicsBackend.PYVISTA`` ignore any
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

        graphics_backend : GraphicsBackend, optional
            Plot the currently selected lines using ``ansys-tools-visualization_interface``.

        show_keypoint_numbering : bool, optional
            Display keypoint numbers when ``graphics_backend=GraphicsBackend.PYVISTA``.



        Returns
        -------
        object
            Plot display object when using PyVista graphics backend, None otherwise.

        Notes
        -----
        This command is valid in any processor.
        """
        if graphics_backend is None:
            graphics_backend = self._graphics_backend

        if graphics_backend is GraphicsBackend.PYVISTA:
            from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

            pl = kwargs.get("plotter", None)
            pl = MapdlPlotter().switch_scene(pl)

            kwargs.setdefault("title", "MAPDL Keypoint Plot")
            if not self.geometry.n_keypoint:
                warnings.warn(
                    "Either no keypoints have been "
                    "selected or there are no keypoints in "
                    "the database."
                )
                pl.plot([], [], [], **kwargs)
                return pl.show(**kwargs)

            keypoints = self.geometry.get_keypoints(return_as_array=True)
            points = [{"points": keypoints}]

            labels = []
            if show_keypoint_numbering:
                labels.append(
                    {"points": keypoints, "labels": self.geometry.knum.astype(int)}
                )
            pl.plot([], points, labels, **kwargs)
            return pl.show(**kwargs)

        # otherwise, use the legacy plotter
        if graphics_backend is GraphicsBackend.MAPDL:
            with self._enable_interactive_plotting():
                return super().kplot(np1=np1, np2=np2, ninc=ninc, lab=lab, **kwargs)

    @check_deprecated_vtk_kwargs
    @requires_graphics
    def lplot(
        self,
        nl1="",
        nl2="",
        ninc="",
        *,
        graphics_backend=None,
        show_line_numbering=True,
        show_keypoint_numbering=False,
        color_lines=False,
        **kwargs,
    ):
        """Display the selected lines.

        APDL Command: LPLOT

        .. note::
            PyMAPDL plotting commands with ``graphics_backend=GraphicsBackend.PYVISTA`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        nl1, nl2, ninc
            Display lines from NL1 to NL2 (defaults to NL1) in steps
            of NINC (defaults to 1).  If NL1 = ALL (default), NL2 and
            NINC are ignored and display all selected lines [LSEL].

        graphics_backend : GraphicsBackend, optional
            Plot the currently selected lines using ``ansys-tools-visualization_interface``.

        show_line_numbering : bool, optional
            Display line and keypoint numbers when ``graphics_backend=GraphicsBackend.PYVISTA``.

        show_keypoint_numbering : bool, optional
            Number keypoints.  Only valid when ``show_keypoints=True``

        color_lines : bool, optional
            Color each line with a different color.

        **kwargs
            See :class:`ansys.mapdl.core.plotting.visualizer.MapdlPlotter` for
            more keyword arguments applicable when visualizing with
            ``graphics_backend=GraphicsBackend.PYVISTA``.

        Notes
        -----
        Mesh divisions on plotted lines are controlled by the ``ldiv``
        option of the ``psymb`` command when ``graphics_backend=GraphicsBackend.MAPDL``.
        Otherwise, line divisions are controlled automatically.

        This command is valid in any processor.

        Returns
        -------
        object
            Plot display object when using PyVista graphics backend, None otherwise.

        Examples
        --------
        >>> mapdl.lplot(graphics_backend=GraphicsBackend.PYVISTA, cpos='xy', line_width=10)
        """
        if graphics_backend is None:
            graphics_backend = self._graphics_backend

        if graphics_backend:
            from ansys.mapdl.core.plotting.theme import get_ansys_colors
            from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

            kwargs.setdefault("show_scalar_bar", False)
            kwargs.setdefault("title", "MAPDL Line Plot")
            if not self.geometry.n_line:
                warnings.warn(
                    "Either no lines have been selected or there is nothing to plot."
                )
                pl = MapdlPlotter()
                pl.plot([], [], [], **kwargs)
                return pl.show(**kwargs)

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
                            "labels": line["entity_num"].astype(int),
                        }
                    )

            if show_keypoint_numbering:
                labels.append(
                    {
                        "points": self.geometry.get_keypoints(return_as_array=True),
                        "labels": self.geometry.knum.astype(int),
                    }
                )
            pl = MapdlPlotter()
            pl.plot(meshes, [], labels, **kwargs)
            return pl.show(**kwargs)
        else:
            with self._enable_interactive_plotting():
                return super().lplot(nl1=nl1, nl2=nl2, ninc=ninc, **kwargs)

    @check_deprecated_vtk_kwargs
    @requires_graphics
    def aplot(
        self,
        na1="",
        na2="",
        ninc="",
        degen="",
        scale="",
        *,
        graphics_backend=None,
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
            PyMAPDL plotting commands with ``graphics_backend=GraphicsBackend.PYVISTA`` ignore any
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
            Degeneracy marker.  This option is ignored when ``graphics_backend=GraphicsBackend.PYVISTA``.

        scale : float, optional
            Scale factor for the size of the degeneracy-marker star.
            The scale is the size in window space (-1 to 1 in both
            directions) (defaults to 0.075).  This option is ignored
            when ``graphics_backend != GraphicsBackend.MAPDL``.

        graphics_backend : GraphicsBackend, optional
            Plot the currently selected areas using ``ansys-tools-visualization_interface``.
            As this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            Quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best) when ``graphics_backend=GraphicsBackend.PYVISTA``.

        show_area_numbering : bool, optional
            Display area numbers when ``graphics_backend=GraphicsBackend.PYVISTA``.

        show_line_numbering : bool, optional
            Display line numbers when ``graphics_backend=GraphicsBackend.PYVISTA``.

        color_areas : Union[bool, str, np.array], optional
            Only used when ``graphics_backend=GraphicsBackend.PYVISTA``.
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
            See :class:`ansys.mapdl.core.plotting.visualizer.MapdlPlotter` for
            more keyword arguments applicable when visualizing with
            ``graphics_backend=GraphicsBackend.PYVISTA``.

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

        Returns
        -------
        object
            Plot display object when using PyVista graphics backend, None otherwise.
        """
        if graphics_backend is None:
            graphics_backend = self._graphics_backend

        if graphics_backend:
            from matplotlib.colors import to_rgba

            from ansys.mapdl.core.plotting.theme import get_ansys_colors
            from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

            kwargs.setdefault("show_scalar_bar", False)
            kwargs.setdefault("title", "MAPDL Area Plot")
            kwargs.setdefault("scalar_bar_args", {"title": "Scalar Bar Title"})

            if not self.geometry.n_area:
                warnings.warn(
                    "Either no areas have been selected or there is nothing to plot."
                )
                pl = MapdlPlotter()
                pl.plot([], [], [], **kwargs)
                return pl.show(**kwargs)

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
                    if len(anum) != 1:
                        raise RuntimeError(
                            f"The pv.Unstructured from the entity {anum[0]} contains entities"
                            f"from other entities {anum}"  # Sanity check
                        )

                    area = surf.extract_cells(surf["entity_num"] == anum)
                    centers.append(area.center)

                labels.append(
                    {"points": np.array(centers), "labels": anums.astype(int)}
                )

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
                            "labels": lines["entity_num"].astype(int),
                        }
                    )
            pl = MapdlPlotter()
            pl.plot(meshes, [], labels, **kwargs)
            return pl.show(**kwargs)
        if graphics_backend is GraphicsBackend.MAPDL:
            with self._enable_interactive_plotting():
                return super().aplot(
                    na1=na1, na2=na2, ninc=ninc, degen=degen, scale=scale, **kwargs
                )

    @check_deprecated_vtk_kwargs
    @requires_graphics
    def vplot(
        self,
        nv1="",
        nv2="",
        ninc="",
        degen="",
        scale="",
        *,
        graphics_backend=None,
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
            PyMAPDL plotting commands with ``graphics_backend=GraphicsBackend.PYVISTA`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        nv1, nv2, ninc
            Display volumes from NV1 to NV2 (defaults to NV1) in steps
            of NINC (defaults to 1).  If NV1 = ALL (default), NV2 and
            NINC are ignored and all selected volumes [VSEL] are
            displayed.  Ignored when ``graphics_backend=GraphicsBackend.PYVISTA``.

        degen
            Degeneracy marker.  ``"blank"`` No degeneracy marker is
            used (default), or ``"DEGE"``.  A red star is placed on
            keypoints at degeneracies (see the Modeling and Meshing
            Guide).  Not available if /FACET,WIRE is set.  Ignored
            when ``graphics_backend=GraphicsBackend.PYVISTA``.

        scale
            Scale factor for the size of the degeneracy-marker star.  The scale
            is the size in window space (-1 to 1 in both directions) (defaults
            to .075).  Ignored when ``graphics_backend=GraphicsBackend.PYVISTA``.

        graphics_backend : GraphicsBackend, optional
            Plot the currently selected volumes using ``ansys-tools-visualization_interface``.
            As this creates a temporary surface mesh, this may have a
            long execution time for large meshes.

        quality : int, optional
            quality of the mesh to display.  Varies between 1 (worst)
            to 10 (best).  Applicable when ``graphics_backend=GraphicsBackend.PYVISTA``.

        show_numbering : bool, optional
            Display line and keypoint numbers when ``graphics_backend=GraphicsBackend.PYVISTA``.

        **kwargs
            See :class:`ansys.mapdl.core.plotting.visualizer.MapdlPlotter` for
            more keyword arguments applicable when visualizing with
            ``graphics_backend=GraphicsBackend.PYVISTA``.

        Returns
        -------
        object
            Plot display object when using PyVista graphics backend, None otherwise.

        Examples
        --------
        Plot while displaying area numbers.

        >>> mapdl.vplot(show_area_numbering=True)
        """
        if graphics_backend is None:
            graphics_backend = self._graphics_backend

        if graphics_backend is GraphicsBackend.PYVISTA:
            from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

            pl = kwargs.get("plotter", None)
            pl = MapdlPlotter().switch_scene(pl)

            kwargs.setdefault("title", "MAPDL Volume Plot")
            if not self.geometry.n_volu:
                warnings.warn(
                    "Either no volumes have been selected or there is nothing to plot."
                )
                pl = MapdlPlotter()
                pl.plot([], [], [], **kwargs)
                return pl.show(**kwargs)

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

                    pl_aplot = self.aplot(
                        graphics_backend=GraphicsBackend.PYVISTA,
                        color_areas=color_areas,
                        quality=quality,
                        show_area_numbering=show_area_numbering,
                        show_line_numbering=show_line_numbering,
                        show_lines=show_lines,
                        return_plotter=True,
                        **kwargs,
                    )

                    meshes_ = pl_aplot.get_meshes_from_plotter()

                    for each_mesh in meshes_:
                        each_mesh.cell_data["entity_num"] = int(each_volu)

                    meshes.extend(meshes_)

                meshes = [{"mesh": meshes}]

            pl.plot(meshes, points, labels, **kwargs)
            return pl.show(return_plotter=return_plotter, **kwargs)

        elif graphics_backend is GraphicsBackend.MAPDL:
            with self._enable_interactive_plotting():
                return super().vplot(
                    nv1=nv1, nv2=nv2, ninc=ninc, degen=degen, scale=scale, **kwargs
                )
        else:
            raise ValueError(f"Invalid graphics backend: {graphics_backend}. ")

    @check_deprecated_vtk_kwargs
    @requires_graphics
    def nplot(self, nnum="", *, graphics_backend=None, **kwargs):
        """APDL Command: NPLOT

        Displays nodes.

        .. note::
           PyMAPDL plotting commands with ``graphics_backend=GraphicsBackend.PYVISTA`` ignore any
           values set with the ``PNUM`` command.

        Parameters
        ----------
        nnum : bool, int, optional
            Node number key:

            - ``False`` : No node numbers on display (default).
            - ``True`` : Include node numbers on display.

            .. note::
               This parameter is only valid when ``graphics_backend==GraphicsBackend.PYVISTA``

        graphics_backend : GraphicsBackend, optional
            Plot the currently selected nodes using an specific backend.
            Defaults to current ``graphics_backend`` setting as set on the
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
        ...     graphics_backend=GraphicsBackend.PYVISTA,
        ...     background='w',
        ...     color='k',
        ...     show_bounds=True
        ... )

        Plot without using VTK.

        >>> mapdl.prep7()
        >>> mapdl.n(1, 0, 0, 0)
        >>> mapdl.n(11, 10, 0, 0)
        >>> mapdl.fill(1, 11, 9)
        >>> mapdl.nplot(graphics_backend=GraphicsBackend.MAPDL)

        Plot nodal boundary conditions.

        >>> mapdl.nplot(
        ...     plot_bc=True,
        ...     plot_bc_labels=True,
        ...     bc_labels="mechanical",
        ... )

        Returns
        -------
        object
            Plot display object when using PyVista graphics backend, None otherwise.
        """
        if graphics_backend is None:
            graphics_backend = self._graphics_backend

        if "knum" in kwargs:
            raise ValueError("`knum` keyword deprecated.  Please use `nnum` instead.")

        if graphics_backend is GraphicsBackend.PYVISTA:
            import pyvista as pv

            from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

            pl = kwargs.get("plotter", None)
            pl = MapdlPlotter().switch_scene(pl)

            kwargs.setdefault("title", "MAPDL Node Plot")
            if not self.mesh.n_node:
                warnings.warn("There are no nodes to plot.")
                pl.plot([], [], [], **kwargs)
                return pl.show(**kwargs)

            labels = []
            if nnum:
                # must eliminate duplicate points or labeling fails miserably.
                pcloud = pv.PolyData(self.mesh.nodes)
                pcloud["labels"] = self.mesh.nnum
                pcloud.clean(inplace=True)

                labels = [
                    {"points": pcloud.points, "labels": pcloud["labels"].astype(int)}
                ]
            points = [{"points": self.mesh.nodes}]
            pl.plot([], points, labels, mapdl=self, **kwargs)
            return pl.show(**kwargs)

        elif graphics_backend is GraphicsBackend.MAPDL:
            # otherwise, use the built-in nplot
            if isinstance(nnum, bool):
                nnum = int(nnum)

            with self._enable_interactive_plotting():
                return super().nplot(nnum, **kwargs)
        else:
            raise ValueError(f"Invalid graphics backend: {graphics_backend}. ")

    @check_deprecated_vtk_kwargs
    @requires_graphics
    def eplot(self, show_node_numbering=False, *, graphics_backend=None, **kwargs):
        """Plots the currently selected elements.

        APDL Command: EPLOT

        .. note::
            PyMAPDL plotting commands with ``graphics_backend=GraphicsBackend.PYVISTA`` ignore any
            values set with the ``PNUM`` command.

        Parameters
        ----------
        graphics_backend : GraphicsBackend, optional
            Plot the currently selected elements using the picked backend.
            Defaults to current ``graphics_backend`` setting.

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
            See ``help(ansys.mapdl.core.plotting.visualizer.MapdlPlotter)`` for more
            keyword arguments related to visualizing using ``graphics_backend``.

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

        Returns
        -------
        object
            Plot display object when using PyVista graphics backend, None otherwise.
        """
        if graphics_backend is None:
            graphics_backend = self._graphics_backend

        if graphics_backend is GraphicsBackend.PYVISTA:
            from ansys.mapdl.core.plotting.visualizer import MapdlPlotter

            pl = kwargs.get("plotter", None)
            pl = MapdlPlotter().switch_scene(pl)
            pl.mapdl = self

            kwargs.setdefault("title", "MAPDL Element Plot")
            if not self._mesh.n_elem:
                warnings.warn("There are no elements to plot.")
                pl.plot([], [], [], mapdl=self, **kwargs)
                return pl.show(**kwargs)

            # TODO: Consider caching the surface
            esurf = self.mesh._grid.linear_copy().extract_surface().clean()
            kwargs.setdefault("show_edges", True)

            # if show_node_numbering:
            labels = []
            if show_node_numbering:
                labels = [
                    {
                        "points": esurf.points,
                        "labels": esurf["ansys_node_num"].astype(int),
                    }
                ]

            pl.plot(
                [{"mesh": esurf, "style": kwargs.pop("style", "surface")}],
                [],
                labels,
                mapdl=self,
                **kwargs,
            )
            return pl.show(**kwargs)
        elif graphics_backend is GraphicsBackend.MAPDL:
            # otherwise, use MAPDL plotter
            with self._enable_interactive_plotting():
                return self.run("EPLOT", **kwargs)

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
