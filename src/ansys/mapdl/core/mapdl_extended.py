from functools import wraps

from ansys.mapdl.core import _HAS_PYVISTA
from ansys.mapdl.core.errors import ComponentDoesNotExits, IncorrectWorkingDirectory
from ansys.mapdl.core.mapdl_core import _MapdlCore
from ansys.mapdl.core.misc import (
    allow_iterables_vmin,
    allow_pickable_entities,
    load_file,
)
from ansys.mapdl.core.theme import get_ansys_colors

if _HAS_PYVISTA:
    from ansys.mapdl.core.plotting import general_plotter


class _MapdlExtended(_MapdlCore):
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
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
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
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
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
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
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
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
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
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
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
                    f"Using the keyword argument 'vtk' requires having Pyvista installed."
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

    @wraps(Commands.cmplot)
    def cmplot(self, label: str = "", entity: str = "", keyword: str = "", **kwargs):
        """Wraps cmplot"""

        label = label.upper()
        entity = entity.upper()

        if label in ["N", "P"]:
            raise ValueError(f"The label '{label}' is not supported.")

        if (not label or label == "ALL") and not entity:
            raise ValueError(
                f"If not using label or label =='ALL', then you "
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

        kwargs.setdefault("title", f"PyMAPDL CMPLOT")
        output = func(**kwargs)

        # returning to previous selection
        self.cmsel("s", "__tmp_cm__", entity=entity)
        self.components.select(cmps_names)
        return output

    @wraps(Commands.inquire)
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
            "ENVNAME",
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

    @wraps(Commands.parres)
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

    @wraps(Commands.lgwrite)
    def lgwrite(self, fname="", ext="", kedit="", remove_grpc_extra=True, **kwargs):
        """Wraps original /LGWRITE"""

        # always add extension to fname
        if ext:
            fname = fname + f".{ext}"

        # seamlessly deal with remote instances in gRPC mode
        target_dir = None
        is_grpc = "Grpc" in type(self).__name__
        if is_grpc and fname:
            if not self._local and os.path.basename(fname) != fname:
                target_dir, fname = os.path.dirname(fname), os.path.basename(fname)

        # generate the log and download if necessary
        output = super().lgwrite(fname=fname, kedit=kedit, **kwargs)

        if not fname:
            # defaults to <jobname>.lgw
            fname = self.jobname + ".lgw"
        if target_dir is not None:
            self.download(fname, target_dir=target_dir)

        # remove extra grpc /OUT commands
        if remove_grpc_extra and is_grpc and target_dir:
            filename = os.path.join(target_dir, fname)
            with open(filename, "r") as fid:
                lines = [line for line in fid if not line.startswith("/OUT")]
            with open(filename, "w") as fid:
                fid.writelines(lines)

        return output

    @wraps(Commands.vwrite)
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

    @wraps(Commands.nrm)
    def nrm(self, name="", normtype="", parr="", normalize="", **kwargs):
        """Wraps *NRM"""
        if not parr:
            parr = "__temp_par__"
        super().nrm(
            name=name, normtype=normtype, parr=parr, normalize=normalize, **kwargs
        )
        return self.parameters[parr]

    @wraps(Commands.com)
    def com(self, comment="", **kwargs):
        """Wraps /COM"""
        if self.print_com and not self.mute and not kwargs.get("mute", False):
            print("/COM,%s" % (str(comment)))

        return super().com(comment=comment, **kwargs)

    @wraps(Commands.lssolve)
    def lssolve(self, lsmin="", lsmax="", lsinc="", **kwargs):
        """Wraps LSSOLVE"""
        with self.non_interactive:
            super().lssolve(lsmin=lsmin, lsmax=lsmax, lsinc=lsinc, **kwargs)
        return self.last_response
