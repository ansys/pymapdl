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


"""The plotting MAPDL core responsibility mixin."""

import glob
import os
import pathlib
import sys
import tempfile
import weakref
from shutil import copyfile, rmtree

# Subprocess is needed to start the backend. But
# the input is controlled by the library. Excluding bandit check.
from subprocess import DEVNULL, call  # nosec B404
from typing import TYPE_CHECKING, Optional
from warnings import warn

from ansys.mapdl.core import _HAS_DPF
from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.misc import random_string, requires_graphics, supress_logging
from ansys.mapdl.core.plotting import GraphicsBackend

if TYPE_CHECKING:  # pragma: no cover
    from ansys.mapdl.core.mapdl import MapdlBase

    if _HAS_DPF:
        pass


from . import _CoreMixinBase
from .constants import (
    PNG_IS_WRITTEN_TO_FILE,
    VALID_DEVICES,
    VALID_DEVICES_LITERAL,
    VALID_FILE_TYPE_FOR_PLOT,
    VALID_FILE_TYPE_FOR_PLOT_LITERAL,
)


class _CorePlottingMixin(_CoreMixinBase):
    """Static responsibility mixin for the MAPDL core facade."""

    @property
    def default_file_type_for_plots(self):
        """Default file type for plots.

        Use when device is not properly set, for instance when the device is closed.
        """
        return self._default_file_type_for_plots

    @default_file_type_for_plots.setter
    def default_file_type_for_plots(self, value: VALID_FILE_TYPE_FOR_PLOT_LITERAL):
        """Set default file type for plots.

        Used when device is not properly set, for instance when the device is closed.
        """
        if not isinstance(value, str) or value.upper() not in VALID_FILE_TYPE_FOR_PLOT:
            raise ValueError(f"'{value}' is not allowed as file output for plots.")
        self._default_file_type_for_plots = value.upper()  # type: ignore[assignment]

    @property
    def file_type_for_plots(self):
        """Returns the current file type for plotting."""
        if not self._file_type_for_plots:
            self._run("/show, PNG")
            self._file_type_for_plots = "PNG"
        return self._file_type_for_plots

    @file_type_for_plots.setter
    def file_type_for_plots(self, value: VALID_DEVICES_LITERAL):
        """Modify the current file type for plotting."""
        if isinstance(value, str) and value.upper() in VALID_DEVICES:
            self._run(
                f"/show, {value.upper()}"
            )  # To avoid recursion we need to use _run.
            self._file_type_for_plots = value.upper()  # type: ignore[assignment]
        else:
            raise ValueError(f"'{value}' is not allowed as file output for plots.")

    @property
    def graphics_backend(self) -> GraphicsBackend:
        """Returns current graphics backend."""
        return self._graphics_backend

    @graphics_backend.setter
    def graphics_backend(self, value: GraphicsBackend):
        """Set the graphics backend to be used."""
        self._graphics_backend = value

    def open_gui(
        self,
        include_result: bool | None = None,
        inplace: bool | None = None,
        exec_file: str | None = None,
    ):  # pragma: no cover
        """Save the existing database and open it up in the MAPDL GUI.

        Parameters
        ----------
        include_result : bool, optional
            Allow the result file to be post processed in the GUI.  It is
            ignored if ``inplace`` is ``True``.  By default, ``True``.

        inplace : bool, optional
            Open the GUI on the current MAPDL working directory, instead of
            creating a new temporary directory and coping the results files
            over there.  If ``True``, ignores ``include_result`` parameter. By
            default, this ``False``.

        exec_file: str, optional
            Path to the MAPDL executable. If not provided, it will try to obtain
            it using the `ansys.tools.common` package. If this package is not
            available, it will use the same executable as the current MAPDL
            instance.

        Examples
        --------
        >>> from ansys.mapdl.core import launch_mapdl
        >>> mapdl = launch_mapdl()

        Create a square area using keypoints.

        >>> mapdl.prep7()
        >>> mapdl.k(1, 0, 0, 0)
        >>> mapdl.k(2, 1, 0, 0)
        >>> mapdl.k(3, 1, 1, 0)
        >>> mapdl.k(4, 0, 1, 0)
        >>> mapdl.l(1, 2)
        >>> mapdl.l(2, 3)
        >>> mapdl.l(3, 4)
        >>> mapdl.l(4, 1)
        >>> mapdl.al(1, 2, 3, 4)

        Open up the gui.

        >>> mapdl.open_gui()

        Resume where you left off.

        >>> mapdl.et(1, 'MESH200', 6)
        >>> mapdl.amesh('all')
        >>> mapdl.eplot()
        """
        # lazy load here to avoid circular import
        from ansys.mapdl.core import _HAS_ATC

        if not self._local:
            raise MapdlRuntimeError(
                "``open_gui`` can only be called from a local MAPDL instance."
            )

        if inplace and include_result:
            raise ValueError(
                "'inplace' and 'include_result' kwargs are not compatible."
            )

        if inplace and include_result is None:
            include_result = False

        if include_result is None:
            include_result = True

        if not inplace:
            inplace = False

        name = self.jobname

        # specify a path for the temporary database if any.
        if inplace:
            run_dir = self._start_parm.get("run_location") or str(self.directory)

        else:
            temp_dir = tempfile.gettempdir()
            run_dir = os.path.join(temp_dir, f"ansys_{random_string(10)}")

            # Sanity checks
            if os.path.isdir(run_dir):
                rmtree(run_dir)
            os.mkdir(run_dir)

        database_file = os.path.join(run_dir, f"{name}.db")
        if os.path.isfile(database_file) and not inplace:
            os.remove(database_file)

        # cache result file, version, and routine before closing
        resultfile = self._result_file
        version = self.version
        self._cache_routine()

        # finish, save and exit the server
        self.finish(mute=True)
        self.save(database_file, mute=True)

        # Exit and do not remove the temporary directory. This is backwards
        # compatible with CONSOLE and CORBA modes.
        remove_tmp = False
        if hasattr(self, "_remove_tmp"):
            remove_tmp = self._remove_tmp  # type: ignore[has-type]  # Set by _MapdlCore.__init__.
        self._remove_tmp = False
        self.exit()

        # copy result file to temp directory
        if not inplace:
            if include_result and self._result_file is not None:
                if os.path.isfile(resultfile):
                    tmp_resultfile = os.path.join(run_dir, "%s.rst" % name)
                    copyfile(resultfile, tmp_resultfile)

        # write temporary input file
        start_file = os.path.join(run_dir, f"start{version}.ans")
        with open(start_file, "w") as f:
            f.write("RESUME\n")

        # some versions of ANSYS just look for "start.ans" when starting
        other_start_file = os.path.join(run_dir, "start.ans")
        with open(other_start_file, "w") as f:
            f.write("RESUME\n")

        # issue system command to run ansys in GUI mode
        cwd = os.getcwd()
        os.chdir(run_dir)

        if not exec_file:
            if _HAS_ATC:
                from ansys.mapdl.core import get_mapdl_path

                exec_file_ = get_mapdl_path(allow_input=False)
            else:
                exec_file_ = None

            exec_file = self._start_parm.get("exec_file", exec_file_)

        if not exec_file:
            raise MapdlRuntimeError(
                "The path to the MAPDL executable was not found. "
                "Please set it using the 'exec_file' parameter when "
                "launching MAPDL."
            )

        nproc = self._start_parm.get("nproc", 2)
        add_sw = self._start_parm.get("additional_switches", "")

        if inplace:
            warn(
                "MAPDL GUI has been opened using 'inplace' kwarg. "
                f"The changes you make will overwrite the files in {run_dir}."
            )
        add_sw = add_sw.split()

        # Ensure exec_file is a file
        try:
            pathlib.Path(exec_file).is_file()
        except FileNotFoundError:
            raise FileNotFoundError("The executable file for ANSYS was not found. ")

        exec_array = [
            f"{exec_file}",
            "-g",
            "-j",
            f"{name}",
            "-np",
            f"{nproc}",
            *add_sw,
        ]

        # exec_array is controlled by the library. Excluding bandit check.
        call(
            exec_array,
            stdout=DEVNULL,
            cwd=run_dir,
        )  # nosec B603

        # Going back
        os.chdir(cwd)

        # Clearing
        os.remove(start_file)
        os.remove(other_start_file)

        # reattach to a new session and reload database
        self._launch(self._start_parm)
        self.resume(database_file, mute=True)

        # restore remove tmp state
        self._remove_tmp = remove_tmp

    @supress_logging
    def _enable_interactive_plotting(self, pixel_res: int = 1600):
        """Enables interactive plotting.  Requires matplotlib

        Parameters
        ----------
        pixel_res : int
            Pixel resolution.  Valid values are from 256 to 2400.
            Lowering the pixel resolution produces a "fuzzier" image.
            Increasing the resolution produces a "sharper" image but
            takes longer to render.
        """
        return self.WithInterativePlotting(self, pixel_res)

    class WithInterativePlotting:
        """Allows to redirect plots to MAPDL plots."""

        def __init__(self, parent: "MapdlBase", pixel_res: int) -> None:
            self._parent = weakref.ref(parent)
            self._pixel_res = pixel_res

        @requires_graphics
        def __enter__(self) -> None:
            parent = self._parent()
            if parent is None:
                raise MapdlRuntimeError("Parent reference is None")

            parent._log.debug("Entering in 'WithInterativePlotting' mode")

            self._active = not parent._store_commands
            if not self._active:
                return

            self.previous_device = parent.file_type_for_plots
            entered = False
            try:
                if not parent._png_mode:
                    parent.show("PNG", mute=True)
                    parent.gfile(self._pixel_res, mute=True)

                if parent.file_type_for_plots not in [
                    "PNG",
                    "TIFF",
                    "PNG",
                    "VRML",
                ]:
                    parent.show(parent.default_file_type_for_plots)
                entered = True
            finally:
                if not entered:
                    parent._restore_plot_device(
                        self.previous_device,
                        primary_exception=sys.exc_info()[1],
                        use_property=True,
                    )

        @requires_graphics
        def __exit__(self, *args) -> None:
            parent = self._parent()
            if parent is None:
                raise MapdlRuntimeError("Parent reference is None")

            parent._log.debug("Exiting in 'WithInterativePlotting' mode")
            if not self._active:
                return

            try:
                parent.show("close", mute=True)

                if not parent._store_commands:
                    if not parent._png_mode:
                        parent.show("PNG", mute=True)
                        parent.gfile(self._pixel_res, mute=True)
            finally:
                parent._restore_plot_device(
                    self.previous_device,
                    primary_exception=sys.exc_info()[1],
                    use_property=True,
                )

    def is_png_found(self, text: str) -> bool:
        # findall returns None if there is no match
        return PNG_IS_WRITTEN_TO_FILE.findall(text) is not None

    def _restore_plot_device(
        self,
        previous_device: VALID_FILE_TYPE_FOR_PLOT_LITERAL,
        primary_exception: Optional[BaseException],
        *,
        use_property: bool = False,
    ) -> None:
        try:
            if use_property:
                self.file_type_for_plots = previous_device
            else:
                self.show(previous_device)
        except Exception:
            if primary_exception is None:
                raise
            self._log.exception("Unable to restore the previous plotting device.")

    def _get_plot_name(self, text: str) -> str:
        """Obtain the plot filename."""
        self._log.debug(f"Output from terminal used to find plot name: {text}")

        if self.is_png_found(text):
            # flush graphics writer
            previous_device = self.file_type_for_plots
            try:
                self.show("CLOSE", mute=True)
                # self.show("PNG", mute=True)
                filename = self._screenshot_path()
            finally:
                self._restore_plot_device(
                    previous_device,
                    primary_exception=sys.exc_info()[1],
                )
            self._log.debug(f"Screenshot at: {filename}")

            if os.path.isfile(filename):
                return filename
            else:  # pragma: no cover
                raise MapdlRuntimeError(f"Unable to find screenshot at {filename}")
        else:
            raise MapdlRuntimeError(
                "Unable to find plotted file in MAPDL command output. "
                "One possible reason is that the graphics device is not correct. "
                "Please check you are using FULL graphics device. "
                "For example:\n"
                ">>> mapdl.graphics('FULL')"
                f"\nThe text output from MAPDL is:\n{text}"
            )

    def _display_plot(self, filename: str) -> None:
        """Display the last generated plot (*.png) from MAPDL"""
        import matplotlib.image as mpimg
        import matplotlib.pyplot as plt

        def in_ipython():
            # from scooby.in_ipython
            # to avoid dependency here.
            try:
                __IPYTHON__
                return True
            except NameError:  # pragma: no cover
                return False

        self._log.debug("A screenshot file has been found.")
        img = mpimg.imread(filename)
        plt.imshow(img)
        plt.axis("off")

        if self._show_matplotlib_figures:  # pragma: no cover
            self._log.debug("Using Matplotlib to plot")
            plt.show()  # consider in-line plotting

        if in_ipython():
            self._log.debug("Using ipython")
            from IPython.display import display

            display(plt.gcf())

    def _download_plot(
        self, filename: str, plot_name: str, default_name: str = "plot"
    ) -> str:
        """Copy the temporary download plot to the working directory."""
        if isinstance(plot_name, str):
            provided = True
            path_ = pathlib.Path(plot_name)
            if path_.is_dir() or path_.suffix == "":
                plot_name = f"{default_name}.png"
                plot_stem = default_name
                plot_ext = ".png"
                plot_path = str(path_)
            else:
                plot_name = path_.name
                plot_stem = path_.stem
                plot_ext = path_.suffix
                plot_path = str(path_.parent)
                if not plot_path or plot_path == ".":
                    plot_path = os.getcwd()

        elif isinstance(plot_name, bool):
            provided = False
            plot_name = f"{default_name}.png"
            plot_stem = default_name
            plot_ext = ".png"
            plot_path = os.getcwd()
        else:  # pragma: no cover
            raise ValueError("Only booleans and str are allowed.")

        id_ = 0
        plot_path_ = os.path.join(plot_path, plot_name)
        while os.path.exists(plot_path_) and not provided:
            id_ += 1
            plot_path_ = os.path.join(plot_path, f"{plot_stem}_{id_}{plot_ext}")
        else:
            copyfile(filename, plot_path_)

        self._log.debug(
            f"Copy plot file from temp directory to working directory as: {plot_path}"
        )
        if provided:
            return plot_path_
        else:
            return os.path.basename(plot_path_)

    def _screenshot_path(self):
        """Return last filename based on the current jobname"""
        filenames = glob.glob(str(self.directory / f"{self.jobname}*.png"))
        filenames.sort()
        return filenames[-1]

    def screenshot(
        self, savefig: Optional[str] = None, default_name: str = "mapdl_screenshot"
    ) -> str | None:
        """Take an MAPDL screenshot and show it in a popup window.

        Parameters
        ----------
        savefig : Optional[str], optional
            Name of or path to the screenshot file.
            The default is ``None``.

        Returns
        -------
        str | None
            Returns the file name if ``savefig`` is provided. Otherwise, it returns None.

        Raises
        ------
        FileNotFoundError
            If the path given in the ``savefig`` parameter is not found or is not consistent.
        ValueError
            If given a wrong type for the ``savefig`` parameter.
        """
        previous_device = self.file_type_for_plots
        try:
            self.show("PNG")
            out_ = self.replot()
        finally:
            self._restore_plot_device(
                previous_device,
                primary_exception=sys.exc_info()[1],
            )
        file_name = self._get_plot_name(out_)

        if savefig:
            return self._download_plot(file_name, savefig, default_name=default_name)
        elif self._has_matplotlib:
            self._display_plot(file_name)
        else:
            self._log.debug("Since matplolib is not installed, images are not shown.")
