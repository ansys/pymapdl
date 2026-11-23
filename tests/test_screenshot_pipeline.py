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

"""Offline tests for the Server Plot Screenshot pipeline."""

import logging
import os
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from ansys.mapdl.core.errors import MapdlRuntimeError
from ansys.mapdl.core.mapdl_extended import _MapdlExtended
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from conftest import requires


class ScriptedMapdl(_MapdlExtended):
    """``Mapdl`` double whose ``_run`` mimics MAPDL's PNG display output.

    Plot commands write ``file<NNN>.png`` into ``workdir`` only while the
    ``PNG`` device is active, like Mechanical APDL does.
    """

    def __init__(self, workdir):
        self._log = MagicMock()
        self._log.logger.level = logging.WARNING
        self._apdl_log = None
        self._MapdlCore__exited = False
        self._store_commands = False
        self._stored_commands = []
        self._ignore_errors = False
        self._file_type_for_plots = "PNG"
        self._show_matplotlib_figures = False
        self._pending_plot_output = None
        self.workdir = workdir
        self.sent = []
        self.plot_index = 0
        self.blank_plots = False
        self.plot_verbs = {"EPLOT", "/REPLOT"}

    @property
    def directory(self):
        return self.workdir

    @property
    def jobname(self):
        return "file"

    def _run(self, command, verbose=False, mute=False):
        self.sent.append(command)
        verb = command.split(",")[0].strip().upper()
        plots = verb in self.plot_verbs and not self.blank_plots
        if plots and self._file_type_for_plots == "PNG":
            name = f"file{self.plot_index:03d}.png"
            (self.workdir / name).write_bytes(f"{verb} frame".encode())
            self.plot_index += 1
            return f" PRODUCE {verb} PLOT\n POST1 DISPLAY WRITTEN TO FILE {name}"
        if plots and self._file_type_for_plots == "TIFF":
            # Real MAPDL 26.1 ``/SHOW,TIFF`` output.
            return (
                f" PRODUCE {verb} PLOT\n CUMULATIVE DISPLAY NUMBER   1 "
                "WRITTEN TO FILE file000.tif       - RASTER MODE."
            )
        return f"{verb} executed"

    @property
    def replots(self):
        return [cmd for cmd in self.sent if cmd.upper().startswith("/REP")]


@pytest.fixture
def fake(tmp_path):
    return ScriptedMapdl(tmp_path)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "PRODUCE NODAL PLOT IN DSYS=      0",
        "ALL CURRENT ANSYS DATA WRITTEN TO FILE NAME= file.db",
        "CUMULATIVE DISPLAY NUMBER   1 WRITTEN TO FILE file000.tif  - RASTER MODE.",
        "PUT VPLO DISPLAY ON VRML FILE file00.wrl - RASTER MODE.",
    ],
)
def test_is_png_found_rejects_text_without_a_display_file(fake, text):
    assert fake.is_png_found(text) is False


@pytest.mark.parametrize(
    "text",
    [
        "WRITTEN TO FILE",
        "POST1 DISPLAY WRITTEN TO FILE file002.png",
        "CUMULATIVE DISPLAY NUMBER   1 WRITTEN TO FILE file000.png  - RASTER MODE.",
        "CUMULATIVE DISPLAY NUMBER   1 WRITTEN TO FILE                   - RASTER MODE.",
        "PREP7 DISPLAY WRITTEN TO FILE\n my_job000.png",
    ],
)
def test_is_png_found_detects_display_file_output(fake, text):
    assert fake.is_png_found(text) is True


def test_plot_command_saves_the_png_it_wrote_without_replot(fake, tmp_path):
    out = tmp_path / "out.png"

    assert fake.run("EPLOT", savefig=str(out)) == str(out)

    assert out.read_bytes() == b"EPLOT frame"
    assert fake.replots == []
    assert "DISPLAY WRITTEN TO FILE file000.png" in fake._response
    assert fake._pending_plot_output is None


def test_plot_command_without_a_frame_warns_instead_of_returning_a_stale_png(
    fake, tmp_path
):
    (tmp_path / "file000.png").write_bytes(b"stale frame")
    fake.blank_plots = True

    with pytest.warns(UserWarning, match="EPLOT executed"):
        assert fake.run("EPLOT", savefig=str(tmp_path / "out.png")) is None

    assert not (tmp_path / "out.png").exists()
    assert fake.replots == []


def test_plot_command_on_a_non_png_device_replots_once_as_png(fake, tmp_path):
    fake._file_type_for_plots = "TIFF"
    out = tmp_path / "out.png"

    assert fake.run("EPLOT", savefig=str(out)) == str(out)

    assert out.read_bytes() == b"/REPLOT frame"
    assert len(fake.replots) == 1
    assert fake.file_type_for_plots == "TIFF"


def test_plot_command_on_tiff_replots_instead_of_returning_a_stale_png(fake, tmp_path):
    (tmp_path / "file000.png").write_bytes(b"stale frame")
    fake.plot_index = 1
    fake._file_type_for_plots = "TIFF"
    out = tmp_path / "out.png"

    assert fake.run("EPLOT", savefig=str(out)) == str(out)

    assert out.read_bytes() == b"/REPLOT frame"
    assert (tmp_path / "file001.png").exists()
    assert len(fake.replots) == 1
    assert fake.file_type_for_plots == "TIFF"


# Command Wrappers newly captured as Server Plot Screenshots, with their verb.
NEWLY_CAPTURED_PLOT_CALLS = [
    ("plcamp", (), "PLCAMP"),
    ("plorb", (), "PLORB"),
    ("plcrack", (), "PLCRACK"),
    ("plcint", (), "PLCINT"),
    ("plcksurf", (), "PLCKSURF"),
    ("plas", (), "PLAS"),
    ("plfar", (), "PLFAR"),
    ("plnear", (), "PLNEAR"),
    ("plf2d", (), "PLF2D"),
    ("mpplot", (), "MPPLOT"),
    ("layplot", (), "LAYPLOT"),
    ("tbfplot", (), "TBFPLOT"),
    ("pltrac", (), "PLTRAC"),
    ("plgeom", (), "PLGEOM"),
    ("plmap", (), "PLMAP"),
    ("plzz", (), "PLZZ"),
    ("plchist", (), "PLCHIST"),
    ("plcfreq", (), "PLCFREQ"),
    ("svplot", (), "SVPLOT"),
    ("mdplot", (), "MDPLOT"),
    ("fsplot", (), "FSPLOT"),
    ("splot", (), "SPLOT"),
    ("gplot", (), "GPLOT"),
    ("replot", (), "/REPLOT"),
    ("plmc", (), "PLMC"),
    ("plpagm", (), "PLPAGM"),
    ("plpath", (), "PLPATH"),
    ("pldisp", (), "PLDISP"),
    ("plvect", (), "PLVECT"),
    ("plls", (), "PLLS"),
    ("pletab", (), "PLETAB"),
    ("plsect", (), "PLSECT"),
    ("starvplot", (), "*VPLOT"),
    ("supl", (), "SUPL"),
    ("run", ("CMPLOT,MYCOMP",), "CMPLOT"),
]


@pytest.mark.parametrize("method,args,verb", NEWLY_CAPTURED_PLOT_CALLS)
def test_plot_command_wrapper_saves_its_png_and_keeps_its_output(
    fake, tmp_path, method, args, verb
):
    fake.plot_verbs.add(verb)
    out = tmp_path / "out.png"

    assert getattr(fake, method)(*args, savefig=str(out)) == str(out)

    assert out.read_bytes() == f"{verb} frame".encode()
    assert f"PRODUCE {verb} PLOT" in fake._response
    # Only ``replot`` itself sends ``/REPLOT``; captured PNGs need no redraw.
    assert len(fake.replots) == (1 if verb == "/REPLOT" else 0)


@pytest.mark.parametrize("method,args,verb", NEWLY_CAPTURED_PLOT_CALLS)
def test_plot_command_wrapper_without_savefig_displays_and_returns_none(
    fake, tmp_path, method, args, verb
):
    fake.plot_verbs.add(verb)

    with patch.object(ScriptedMapdl, "_display_plot") as display:
        assert getattr(fake, method)(*args) is None

    display.assert_called_once_with(os.path.join(tmp_path, "file000.png"))
    assert f"PRODUCE {verb} PLOT" in fake._response
    assert len(fake.replots) == (1 if verb == "/REPLOT" else 0)


def test_replot_on_a_non_png_device_redraws_once_as_png_without_recursing(
    fake, tmp_path
):
    fake._file_type_for_plots = "TIFF"
    out = tmp_path / "out.png"

    assert fake.replot(savefig=str(out)) == str(out)

    assert out.read_bytes() == b"/REPLOT frame"
    # The user's ``/REPLOT`` on TIFF, then one fallback ``/REPLOT`` on PNG.
    assert len(fake.replots) == 2
    assert fake.file_type_for_plots == "TIFF"
    assert "file000.tif" in fake._response


def test_direct_screenshot_replots_as_png_and_restores_the_device(fake, tmp_path):
    fake._file_type_for_plots = "TIFF"
    out = tmp_path / "out.png"

    assert fake.screenshot(savefig=str(out)) == str(out)

    assert out.read_bytes() == b"/REPLOT frame"
    assert len(fake.replots) == 1
    assert fake.file_type_for_plots == "TIFF"


def test_direct_screenshot_without_a_frame_raises(fake, tmp_path):
    (tmp_path / "file000.png").write_bytes(b"stale frame")
    fake.blank_plots = True

    with pytest.raises(MapdlRuntimeError, match="Unable to find plotted file"):
        fake.screenshot(savefig=str(tmp_path / "out.png"))


def test_plot_command_saves_the_exact_png_named_by_mapdl(fake, tmp_path):
    (tmp_path / "file999.png").write_bytes(b"older frame")
    fake.plot_index = 5
    out = tmp_path / "out.png"

    fake.run("EPLOT", savefig=str(out))

    assert out.read_bytes() == b"EPLOT frame"


@pytest.mark.parametrize(
    "files,expected",
    [
        (["file999.png", "file1000.png", "file_custom.png"], "file1000.png"),
        (["file_custom.png", "other000.png"], "file_custom.png"),
    ],
)
def test_local_screenshot_path_sorts_numbered_plots_numerically(
    fake, tmp_path, files, expected
):
    for name in files:
        (tmp_path / name).write_bytes(b"png")

    assert os.path.basename(fake._screenshot_path()) == expected


def test_local_screenshot_path_without_png_raises(fake, tmp_path):
    (tmp_path / "other000.png").write_bytes(b"png")

    with pytest.raises(MapdlRuntimeError, match="file"):
        fake._screenshot_path()


def _remote_mapdl(files, tmp_path):
    """Return a remote ``MapdlGrpc`` whose working directory lists ``files``."""
    mapdl = MapdlGrpc.__new__(MapdlGrpc)
    mapdl._local = False
    mapdl._jobname = "file"
    mapdl.list_files = lambda: files
    mapdl.downloaded = []

    def fake_download(filename, out_file_name):
        mapdl.downloaded.append(filename)
        with open(out_file_name, "wb") as stream:
            stream.write(filename.encode())

    mapdl._download = fake_download
    return mapdl


@pytest.mark.parametrize(
    "target,expected",
    [
        (None, "file1000.png"),
        ("file005.png", "file005.png"),
        ("missing.png", "file1000.png"),
    ],
)
def test_remote_screenshot_path_downloads_exact_or_latest_numbered_png(
    tmp_path, target, expected
):
    files = ["file999.png", "file1000.png", "file005.png", "file_custom.png"]
    mapdl = _remote_mapdl(files, tmp_path)

    with patch(
        "ansys.mapdl.core.mapdl_grpc.tempfile.gettempdir", return_value=str(tmp_path)
    ):
        path = mapdl._screenshot_path(target)

    assert mapdl.downloaded == [expected]
    assert open(path).read() == expected


def test_remote_screenshot_path_without_png_raises(tmp_path):
    mapdl = _remote_mapdl(["file.db", "other000.png"], tmp_path)

    with pytest.raises(MapdlRuntimeError, match="file"):
        mapdl._screenshot_path()


@pytest.fixture
def frame_png(tmp_path):
    import matplotlib.pyplot as plt

    plt.switch_backend("Agg")  # headless: no GUI toolkit needed
    path = tmp_path / "frame.png"
    plt.imsave(path, np.zeros((4, 4, 3)))
    return str(path)


@pytest.fixture
def user_axes():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    yield ax
    plt.close(fig)


@requires("matplotlib")
def test_display_plot_leaves_user_figures_untouched(fake, frame_png, user_axes):
    import matplotlib.pyplot as plt

    fake._display_plot(frame_png)

    assert plt.get_fignums() == [user_axes.figure.number]
    assert plt.gca() is user_axes
    assert len(user_axes.images) == 0


@requires("matplotlib")
def test_display_plot_shows_then_closes_its_figure(fake, frame_png):
    import matplotlib.pyplot as plt

    fake._show_matplotlib_figures = True
    with patch.object(plt, "show") as show:
        fake._display_plot(frame_png)

    show.assert_called_once_with()
    assert plt.get_fignums() == []


@requires("matplotlib")
@requires("IPython")
def test_display_plot_hands_its_figure_to_ipython_without_a_gui(
    fake, frame_png, monkeypatch
):
    import builtins

    import matplotlib.pyplot as plt

    monkeypatch.setattr(builtins, "__IPYTHON__", True, raising=False)
    no_gui = RuntimeError("no GUI display")
    with (
        patch.object(plt, "subplots", side_effect=no_gui),
        patch.object(plt, "figure", side_effect=no_gui),
        patch("IPython.display.display") as display,
    ):
        fake._display_plot(frame_png)

    (fig,), _ = display.call_args
    assert fig.axes[0].images
    assert plt.get_fignums() == []
