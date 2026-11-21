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

import os
import signal
from unittest.mock import MagicMock, patch

import grpc
import pytest

from ansys.mapdl.core import errors
from ansys.mapdl.core.errors import (
    MapdlCommandIgnoredError,
    MapdlConnectionError,
    MapdlException,
    MapdlExitedError,
    MapdlgRPCError,
    MapdlInvalidRoutineError,
    MapdlRuntimeError,
    _build_unavailable_suggestion,
    _get_error_file_tail,
    handle_generic_grpc_error,
    protect_from,
    protect_grpc,
)
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc
from conftest import NullContext

error_shape_error_limits = """

*** ERROR ***                           CP =       0.969   TIME= 13:30:36
 Previous testing revealed that 14 of the 38745 selected elements
 violate shape error limits.  Please review error messages on the
 output or error file (or issue the CHECK command), then delete or
 unselect those elements.

 """  # the last empty line is important!

error_highly_distorted = """

*** ERROR *** CP = 2872.649 TIME= 16:29:51
 One or more elements have become highly distorted. Excessive
 distortion of elements is usually a symptom indicating the need for
 corrective action elsewhere. Try incrementing the load more slowly
 (increase the number of substeps or decrease the time step size). You
 may need to improve your mesh to obtain elements with better aspect
 ratios. Also consider the behavior of materials, contact pairs,
 and/or constraint equations. If this message appears in the first
 iteration of first substep, be sure to perform element shape checking.

"""  # the last empty line is important!

error_inside_out = """

*** ERROR ***                           CP =       0.969   TIME= 13:30:36
 Previous testing revealed that 14 of the 38745 selected elements
 is turning inside out
 output or error file (or issue the CHECK command), then delete or
 unselect those elements.

 """  # Made up example. The last empty line is important!

empty_log = """
***** END OF INPUT ENCOUNTERED *****

 PURGE ALL SOLUTION AND POST DATA
 SAVE ALL MODEL DATA

 ALL CURRENT ANSYS DATA WRITTEN TO FILE NAME= file.db
  FOR POSSIBLE RESUME FROM THIS POINT


 NUMBER OF WARNING MESSAGES ENCOUNTERED=          0
 NUMBER OF ERROR   MESSAGES ENCOUNTERED=          0

+--------- D I S T R I B U T E D   A N S Y S   S T A T I S T I C S ------------+
"""


@pytest.mark.parametrize(
    "response,expected_error",
    [
        pytest.param(
            empty_log,
            None,
            id="Normal output without errors or warns.",
        ),
        pytest.param(
            error_highly_distorted,
            None,
            id="Failed because of highly distorted elements.",
        ),
        pytest.param(
            error_shape_error_limits,
            MapdlRuntimeError,
            id="Failed because of shape error limits.",
        ),
    ],
)
def test_raise_output_errors(mapdl, cleared, response, expected_error):
    if expected_error:
        with pytest.raises(expected_error):
            mapdl._raise_output_errors(response)
    else:
        mapdl._raise_output_errors(response)


def get_error_classes():
    from ansys.mapdl.core import errors

    def is_exception_class(obj):
        try:
            return issubclass(obj, MapdlException)
        except TypeError:
            return False

    errors_to_tests = []
    for each in dir(errors):
        obj = getattr(errors, each)
        if not each.startswith("_") and is_exception_class(obj):
            errors_to_tests.append(obj)
    return errors_to_tests


@pytest.mark.parametrize("error_class", get_error_classes())
def test_exception_classes(error_class):
    message = "Exception message"
    with pytest.raises(error_class, match=message):
        raise error_class(message)


def test_error_handler(mapdl, cleared):
    text = "is not a recognized"
    with pytest.raises(MapdlInvalidRoutineError, match="recognized"):
        mapdl._raise_errors(text)

    text = "command is ignored"
    with pytest.raises(MapdlCommandIgnoredError, match="ignored"):
        mapdl._raise_errors(text)

    text = "*** ERROR ***\n This is my own errorrrr"
    with pytest.raises(MapdlRuntimeError, match="errorrrr"):
        mapdl._raise_errors(text)


@pytest.mark.parametrize(
    # Tests inputs
    "message,condition,context",
    [
        (None, None, NullContext()),
        ("My custom error", None, NullContext()),
        ("my error", None, pytest.raises(ValueError)),
        (None, None, NullContext()),
        (None, True, NullContext()),
        (None, False, pytest.raises(ValueError)),
        ("my error", False, pytest.raises(ValueError)),
        ("my error", True, pytest.raises(ValueError)),
        ("My custom error", False, pytest.raises(ValueError)),
        ("My custom error", True, NullContext()),
    ],
    # Test ids
    ids=[
        "Match any message. No condition",
        "Match message. No condition",
        "Raises an exception. No condition (raise internal exception)",
        "No message. No condition",
        "No message. True condition",
        "No message. False condition (raise internal exception)",
        "Different error message. False condition (raise internal exception)",
        "Different error message. True condition (raise internal exception)",
        "Same error message. False condition (raise internal exception)",
        "Same error message. True condition",
    ],
)
def test_protect_from(message, condition, context):
    class myclass:
        @protect_from(ValueError, message, condition)
        def raising(self):
            raise ValueError("My custom error")

    with context:
        myobj = myclass()
        myobj.raising()


def test_protect_grpc_translates_closed_channel_value_error():
    """A 'Cannot invoke RPC on closed channel' ValueError becomes a
    'MapdlExitedError' and marks the instance as exited."""
    mock_mapdl = MagicMock(spec=MapdlGrpc)
    mock_mapdl._log = MagicMock()
    mock_mapdl._exited = False
    mock_mapdl.exited = False

    @protect_grpc
    def raising(self):
        raise ValueError("Cannot invoke RPC on closed channel")

    with pytest.raises(MapdlExitedError, match="closed channel"):
        raising(mock_mapdl)

    assert mock_mapdl._exited is True


def test_protect_grpc_reraises_unrelated_value_error():
    """A 'ValueError' unrelated to a closed channel must propagate unchanged."""
    mock_mapdl = MagicMock(spec=MapdlGrpc)
    mock_mapdl._log = MagicMock()
    mock_mapdl._exited = False
    mock_mapdl.exited = False

    @protect_grpc
    def raising(self):
        raise ValueError("some unrelated argument error")

    with pytest.raises(ValueError, match="some unrelated argument error"):
        raising(mock_mapdl)

    assert mock_mapdl._exited is False


class TestBuildUnavailableSuggestion:
    """Tests for _build_unavailable_suggestion."""

    def test_sigkill_points_to_oom(self):
        """A SIGKILL (9) exit signal produces the OOM-specific suggestion."""
        mock_mapdl = MagicMock(spec=MapdlGrpc)
        mock_mapdl._get_process_exit_signal.return_value = 9

        suggestion = _build_unavailable_suggestion(mock_mapdl)

        assert "SIGKILL" in suggestion
        assert "Out-Of-Memory" in suggestion
        assert "dmesg" in suggestion

    def test_other_signal_is_named(self):
        """A non-SIGKILL exit signal is reported by name, without the OOM claim."""
        mock_mapdl = MagicMock(spec=MapdlGrpc)
        mock_mapdl._get_process_exit_signal.return_value = 11  # SIGSEGV

        suggestion = _build_unavailable_suggestion(mock_mapdl)

        assert "signal 11" in suggestion
        assert "SIGSEGV" in suggestion
        assert "Out-Of-Memory" not in suggestion

    def test_unknown_signal_number_falls_back_to_number(self):
        """An out-of-range signal number is shown as-is instead of a name."""
        mock_mapdl = MagicMock(spec=MapdlGrpc)
        mock_mapdl._get_process_exit_signal.return_value = 999

        suggestion = _build_unavailable_suggestion(mock_mapdl)

        assert "signal 999 (999)" in suggestion

    def test_no_exit_signal_falls_back_to_generic_message(self):
        """When the exit signal cannot be determined, use the generic message."""
        mock_mapdl = MagicMock(spec=MapdlGrpc)
        mock_mapdl._get_process_exit_signal.return_value = None

        suggestion = _build_unavailable_suggestion(mock_mapdl)

        assert "might* have died" in suggestion

    @pytest.mark.parametrize("exit_signal", [None, 9, 11])
    def test_suggestion_works_without_signal_sigkill(self, monkeypatch, exit_signal):
        """Without ``signal.SIGKILL``, as on Windows, the suggestion is still built.

        Removing the attribute reproduces the Windows failure on any platform.
        """
        monkeypatch.delattr(signal, "SIGKILL", raising=False)
        mock_mapdl = MagicMock(spec=MapdlGrpc)
        mock_mapdl._get_process_exit_signal.return_value = exit_signal

        suggestion = _build_unavailable_suggestion(mock_mapdl)

        if exit_signal is None:
            assert "might* have died" in suggestion
        else:
            assert f"signal {exit_signal}" in suggestion

    def test_missing_helper_falls_back_to_generic_message(self):
        """MAPDL objects without the helper (e.g. older mocks) still work."""
        mock_mapdl = MagicMock()
        del mock_mapdl._get_process_exit_signal

        suggestion = _build_unavailable_suggestion(mock_mapdl)

        assert "might* have died" in suggestion


def test_protect_grpc_translates_future_cancelled_error():
    """A 'FutureCancelledError', raised when the connectivity watchdog cancels
    an in-flight call because the channel died, becomes a
    'MapdlConnectionError' instead of propagating unchanged or retrying."""
    mock_mapdl = MagicMock(spec=MapdlGrpc)
    mock_mapdl._log = MagicMock()
    mock_mapdl._exited = False
    mock_mapdl.exited = False
    mock_mapdl.channel_state = "TRANSIENT_FAILURE"

    @protect_grpc
    def raising(self):
        raise grpc.FutureCancelledError()

    with pytest.raises(MapdlConnectionError, match="TRANSIENT_FAILURE"):
        raising(mock_mapdl)


def test_protect_grpc_future_cancelled_error_adds_error_file(tmp_path):
    """When the channel dies during a call, the end of the MAPDL error file is
    added to the 'MapdlConnectionError' message (local instances only)."""
    (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")
    mock_mapdl = _dead_mapdl(tmp_path)
    mock_mapdl._log = MagicMock()
    mock_mapdl._exited = False
    mock_mapdl.exited = False
    mock_mapdl.channel_state = "TRANSIENT_FAILURE"

    @protect_grpc
    def raising(self):
        raise grpc.FutureCancelledError()

    with pytest.raises(MapdlConnectionError) as excinfo:
        raising(mock_mapdl)

    assert "TRANSIENT_FAILURE" in str(excinfo.value)
    assert "supports (128000) has been exceeded." in str(excinfo.value)


class _FakeRpcError(grpc.RpcError):
    """Minimal 'grpc.RpcError' double exposing 'code()'/'details()'."""

    def __init__(self, code, details):
        self._code = code
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details


@pytest.mark.parametrize(
    "details,expected_limit",
    [
        # Message format seen with streaming RPCs (gRPC wraps it with
        # "Stream removed (CLIENT: ...)").
        (
            "Stream removed (CLIENT: Received message larger than max "
            "(262152 vs. 1024))",
            262152,
        ),
        # Message format seen with unary RPCs.
        ("Received message larger than max (512 vs. 100)", 512),
        # No sizes in the details: suggest the 512 MB fallback.
        ("Received message larger than max", 512 * 1024**2),
    ],
)
def test_protect_grpc_translates_resource_exhausted_error(details, expected_limit):
    """A 'RESOURCE_EXHAUSTED' error whose details report a message that is
    too large becomes a 'MapdlgRPCError' on the first attempt, suggesting
    'PYMAPDL_MAX_MESSAGE_LENGTH' set to the received message size (or a 512 MB
    fallback when the size is not reported), regardless of whether gRPC wraps
    the details with a 'Stream removed' prefix."""

    mock_mapdl = MagicMock(spec=MapdlGrpc)
    mock_mapdl._log = MagicMock()
    mock_mapdl._exited = False
    mock_mapdl.exited = False
    mock_mapdl.is_alive = True
    attempts = []

    @protect_grpc
    def raising(self, n_attempts=2):
        attempts.append(None)
        raise _FakeRpcError(grpc.StatusCode.RESOURCE_EXHAUSTED, details)

    with pytest.raises(
        MapdlgRPCError, match="Received message larger than max"
    ) as excinfo:
        raising(mock_mapdl, n_attempts=2)

    assert f"PYMAPDL_MAX_MESSAGE_LENGTH={expected_limit}" in str(excinfo.value)
    assert len(attempts) == 1


# The error that Ansys Student writes to 'file.err' before aborting when a mesh
# exceeds its node limit. PyMAPDL only sees the gRPC connection closing.
NODE_LIMIT_ERROR = (
    " *** FATAL ***                           CP =      43.375   TIME= 23:25:01\n"
    " The maximum number of nodes that this version of Mechanical APDL\n"
    " supports (128000) has been exceeded.\n"
)


def _dead_mapdl(path, local=True, jobname="file"):
    """Mock of a MAPDL instance whose process has died."""
    mapdl = MagicMock(spec=MapdlGrpc)
    mapdl._local = local
    mapdl._path = path
    mapdl._jobname = jobname
    mapdl._start_parm = {}
    mapdl.is_alive = False
    mapdl.ip = "127.0.0.1"
    mapdl.port = 50052
    return mapdl


class TestGetErrorFileTail:
    """Tests for _get_error_file_tail."""

    def test_reads_only_the_end_of_a_large_file(self, tmp_path):
        """Only the last lines of a large error file are returned."""
        content = b" old warning\n" * 50_000 + NODE_LIMIT_ERROR.encode("latin-1")
        (tmp_path / "file.err").write_bytes(content)

        tail = _get_error_file_tail(_dead_mapdl(tmp_path))

        assert "supports (128000) has been exceeded." in tail
        assert "file.err" in tail
        body = tail.splitlines()[1:]
        assert len(body) == errors.ERROR_FILE_TAIL_LINES
        assert body[-1].strip() == "supports (128000) has been exceeded."

    def test_short_file_is_returned_whole(self, tmp_path):
        """A file shorter than the limit is returned without dropping its first line."""
        (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        tail = _get_error_file_tail(_dead_mapdl(tmp_path))

        assert "*** FATAL ***" in tail

    def test_remote_instance_returns_empty_string(self, tmp_path):
        """The file system of a remote instance is not accessible."""
        (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        assert _get_error_file_tail(_dead_mapdl(tmp_path, local=False)) == ""

    def test_missing_file_returns_empty_string(self, tmp_path):
        """No error file, no message."""
        assert _get_error_file_tail(_dead_mapdl(tmp_path)) == ""

    def test_empty_file_returns_empty_string(self, tmp_path):
        """An error file with only blank lines adds nothing."""
        (tmp_path / "file.err").write_text("\n \n", encoding="latin-1")

        assert _get_error_file_tail(_dead_mapdl(tmp_path)) == ""

    def test_most_recent_file_is_used_in_distributed_mode(self, tmp_path):
        """With 'file.err' and 'file0.err', the most recently modified one is read."""
        old = tmp_path / "file.err"
        old.write_text(" old run\n", encoding="latin-1")
        os.utime(old, (1_000_000, 1_000_000))
        (tmp_path / "file0.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        tail = _get_error_file_tail(_dead_mapdl(tmp_path))

        assert "file0.err" in tail
        assert "old run" not in tail

    def test_custom_jobname(self, tmp_path):
        """The cached jobname is used to find the file."""
        (tmp_path / "myjob.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        tail = _get_error_file_tail(_dead_mapdl(tmp_path, jobname="myjob"))

        assert "myjob.err" in tail

    def test_run_location_is_used_when_directory_is_not_cached(self, tmp_path):
        """Without a cached directory, the launch 'run_location' is used."""
        (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")
        mapdl = _dead_mapdl(None)
        mapdl._start_parm = {"run_location": str(tmp_path)}

        assert "128000" in _get_error_file_tail(mapdl)

    def test_no_directory_returns_empty_string(self):
        """Without a cached directory or run location, nothing is read."""
        assert _get_error_file_tail(_dead_mapdl(None)) == ""

    def test_unreadable_file_returns_empty_string(self, tmp_path):
        """An OSError while reading the file does not hide the original error."""
        (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        with patch("builtins.open", side_effect=PermissionError("locked")):
            assert _get_error_file_tail(_dead_mapdl(tmp_path)) == ""

    def test_unreadable_directory_returns_empty_string(self, tmp_path):
        """An OSError while listing the directory does not hide the original error."""
        (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        with patch("pathlib.Path.iterdir", side_effect=PermissionError("denied")):
            assert _get_error_file_tail(_dead_mapdl(tmp_path)) == ""

    def test_worker_file_with_fatal_error_is_shown(self, tmp_path):
        """In distributed mode, a fatal error written only by another process is shown."""
        (tmp_path / "file0.err").write_text(
            " *** WARNING ***\n note\n", encoding="latin-1"
        )
        (tmp_path / "file1.err").write_text(" nothing to report\n", encoding="latin-1")
        (tmp_path / "file2.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        tail = _get_error_file_tail(_dead_mapdl(tmp_path))

        assert "file0.err" in tail
        assert "file2.err" in tail
        assert "supports (128000) has been exceeded." in tail
        assert "file1.err" not in tail
        assert "nothing to report" not in tail
        assert tail.index("file0.err") < tail.index("file2.err")

    def test_worker_file_without_main_file(self, tmp_path):
        """A fatal error in a worker file is shown even without 'JOBNAME0.err'."""
        (tmp_path / "file3.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        tail = _get_error_file_tail(_dead_mapdl(tmp_path))

        assert "file3.err" in tail
        assert "128000" in tail

    def test_number_of_worker_files_is_limited(self, tmp_path):
        """Only the first worker files are shown; the others are listed by name."""
        for rank in (1, 2, 10, 11):
            (tmp_path / f"file{rank}.err").write_text(
                NODE_LIMIT_ERROR, encoding="latin-1"
            )

        tail = _get_error_file_tail(_dead_mapdl(tmp_path), max_worker_files=2)

        assert tail.count("Last lines of the MAPDL error file") == 2
        assert "file1.err':" in tail
        assert "file2.err':" in tail
        assert "Other MAPDL error files with errors: file10.err, file11.err" in tail

    def test_worker_file_with_error_is_shown(self, tmp_path):
        """A worker file with an error, but no fatal error, is shown too."""
        (tmp_path / "file1.err").write_text(
            " *** ERROR ***                           CP =       1.000\n"
            " Element 12 has a negative Jacobian.\n",
            encoding="latin-1",
        )

        tail = _get_error_file_tail(_dead_mapdl(tmp_path))

        assert "file1.err" in tail
        assert "negative Jacobian" in tail

    def test_worker_files_with_fatal_error_are_shown_first(self, tmp_path):
        """When the number of files is limited, those with a fatal error are kept."""
        for rank in (1, 2):
            (tmp_path / f"file{rank}.err").write_text(
                " *** ERROR ***\n The VSWE command is ignored.\n", encoding="latin-1"
            )
        (tmp_path / "file7.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        tail = _get_error_file_tail(_dead_mapdl(tmp_path), max_worker_files=2)

        assert "file7.err':" in tail
        assert "file1.err':" in tail
        assert tail.index("file7.err") < tail.index("file1.err")
        assert "Other MAPDL error files with errors: file2.err" in tail

    def test_other_jobnames_are_ignored(self, tmp_path):
        """Files of other jobs in the same directory are not read."""
        for name in ("file_old.err", "other0.err", "file1.err.bak"):
            (tmp_path / name).write_text(NODE_LIMIT_ERROR, encoding="latin-1")

        assert _get_error_file_tail(_dead_mapdl(tmp_path)) == ""


def _grpc_error():
    error = MagicMock()
    error.details.return_value = "Socket closed"
    return error


def test_handle_generic_grpc_error_adds_error_file_when_mapdl_died(tmp_path):
    """If MAPDL died, the end of its error file is part of the exception message."""
    (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")
    mapdl = _dead_mapdl(tmp_path)

    def run():
        """Function that raised the gRPC error."""

    with pytest.raises(MapdlExitedError) as excinfo:
        handle_generic_grpc_error(_grpc_error(), run, (mapdl, "VSWEEP,3"), {})

    assert "supports (128000) has been exceeded." in str(excinfo.value)
    assert "VSWEEP,3" in str(excinfo.value)
    mapdl.exit.assert_called_once()


def test_handle_generic_grpc_error_without_error_file_keeps_message(tmp_path):
    """Without an error file, the message is the same as before."""
    mapdl = _dead_mapdl(tmp_path)

    def run():
        """Function that raised the gRPC error."""

    with pytest.raises(MapdlExitedError) as excinfo:
        handle_generic_grpc_error(_grpc_error(), run, (mapdl, "VSWEEP,3"), {})

    assert "error file" not in str(excinfo.value)


def test_handle_generic_grpc_error_alive_mapdl_does_not_read_error_file(tmp_path):
    """While MAPDL is alive, the error file is not read."""
    (tmp_path / "file.err").write_text(NODE_LIMIT_ERROR, encoding="latin-1")
    mapdl = _dead_mapdl(tmp_path)
    mapdl.is_alive = True

    def run():
        """Function that raised the gRPC error."""

    with pytest.raises(MapdlRuntimeError) as excinfo:
        handle_generic_grpc_error(_grpc_error(), run, (mapdl, "VSWEEP,3"), {})

    assert "128000" not in str(excinfo.value)
    mapdl.exit.assert_not_called()
