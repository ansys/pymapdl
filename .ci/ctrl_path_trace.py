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

"""Trace client liveness decisions without changing the library or issuing RPCs."""

import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import sys
import threading
import time

import grpc
import pytest

_TARGETS = {"test_connect_via_channel", "test_generic_grpc_exception"}
_METHODS = {
    "__init__",
    "_connect",
    "_ctrl",
    "_ctrl_raw",
    "is_alive",
    "connectivity_callback",
}


class _Trace:
    def __init__(self, path):
        self._file = Path(path).open("w", encoding="utf-8", buffering=1)
        self._lock = threading.Lock()
        self._sequence = 0
        self._clients = {}
        self._client_count = 0
        self._active = False
        self._started = False
        self._closed = False
        self.failure = None
        self.nodeid = None
        self.phase = "session"

    def _fail(self, error):
        if self.failure is None:
            self.failure = type(error).__name__
        self._active = False
        if self._started:
            sys.settrace(None)
            threading.settrace(None)

    def emit(self, event, **fields):
        try:
            with self._lock:
                if self._closed:
                    return
                self._sequence += 1
                record = {
                    "sequence": self._sequence,
                    "time_ns": time.time_ns(),
                    "thread": threading.get_ident(),
                    "nodeid": self.nodeid,
                    "phase": self.phase,
                    "event": event,
                    **fields,
                }
                self._file.write(json.dumps(record) + "\n")
        except (OSError, RecursionError, TypeError, ValueError) as error:
            self._fail(error)

    def _snapshot(self, client):
        if client is None:
            return {}
        values = vars(client)
        state = values.get("_channel_state")
        return {
            "client": self._clients.get(id(client)),
            "channel_state": (
                state.name if isinstance(state, grpc.ChannelConnectivity) else None
            ),
            "exited": values.get("_MapdlCore__exited"),
            "exiting": values.get("_exiting"),
            "busy": values.get("_busy"),
            "has_stub": values.get("_stub") is not None,
        }

    def trace(self, frame, event, arg):
        if not self._active:
            return None
        try:
            return self._trace(frame, event, arg)
        except (
            AttributeError,
            OSError,
            RecursionError,
            TypeError,
            ValueError,
        ) as error:
            self._fail(error)
            return None

    def _trace(self, frame, event, arg):
        module = frame.f_globals.get("__name__", "")
        function = frame.f_code.co_name
        is_client = module == "ansys.mapdl.core.mapdl_grpc" and function in _METHODS
        is_error = module == "ansys.mapdl.core.errors" and function in {
            "wrapper",
            "handle_generic_grpc_error",
        }
        if not (is_client or is_error):
            return None
        if event == "line" and function != "is_alive":
            return self.trace
        client = frame.f_locals.get("self", frame.f_locals.get("mapdl"))
        if event == "call" and is_client and function == "__init__":
            self._client_count += 1
            self._clients[id(client)] = self._client_count
        fields = {
            "module": module.rsplit(".", 1)[-1],
            "function": function,
            "line": frame.f_lineno,
            **self._snapshot(client),
        }
        if is_error:
            fields["operation"] = getattr(frame.f_locals.get("func"), "__name__", None)
        if function == "__init__" and event == "call":
            fields["supplied_channel"] = frame.f_locals.get("channel") is not None
        timeout = frame.f_locals.get("timeout")
        if timeout is None or isinstance(timeout, (int, float)):
            fields["timeout_s"] = timeout
        caller = frame.f_back
        if caller is not None:
            fields["caller_function"] = caller.f_code.co_name
            fields["caller_line"] = caller.f_lineno
        command = frame.f_locals.get("cmd")
        if command in ("VERSION", "EXIT", "set_verb"):
            fields["ctrl_command"] = command
        if event == "exception":
            error = arg[1]
            fields["exception_type"] = type(error).__name__
            if isinstance(error, grpc.RpcError):
                code = error.code()
                fields["grpc_status"] = (
                    code.name if isinstance(code, grpc.StatusCode) else None
                )
        elif event == "return":
            if function in {"is_alive", "_connect"}:
                fields["result"] = arg if isinstance(arg, bool) else None
            elif function in {"_ctrl", "_ctrl_raw"}:
                fields["nonempty_response"] = bool(arg)
        elif event not in {"call", "line"}:
            return self.trace
        self.emit(event, **fields)
        return self.trace

    def start(self):
        if sys.gettrace() is not None or threading.gettrace() is not None:
            raise pytest.UsageError(
                "Ctrl path tracing requires no coverage tracer or debugger"
            )
        self._active = True
        self._started = True
        threading.settrace(self.trace)
        sys.settrace(self.trace)

    def close(self):
        self._active = False
        if self._started:
            self._started = False
            sys.settrace(None)
            threading.settrace(None)
        try:
            with self._lock:
                if not self._closed:
                    self._closed = True
                    self._file.close()
        except OSError as error:
            self._fail(error)


def pytest_addoption(parser):
    parser.addoption("--ctrl-path-repetitions", type=int, default=0)
    parser.addoption("--ctrl-path-log", default="ctrl-path.jsonl")


def pytest_configure(config):
    repeats = config.getoption("ctrl_path_repetitions")
    if repeats < 0:
        raise pytest.UsageError("--ctrl-path-repetitions must be nonnegative")
    if repeats:
        config._ctrl_path_trace = _Trace(config.getoption("ctrl_path_log"))


@pytest.fixture(autouse=True)
def _ctrl_iteration():
    yield


def pytest_generate_tests(metafunc):
    repeats = metafunc.config.getoption("ctrl_path_repetitions")
    if (
        repeats
        and metafunc.definition.path.name == "test_grpc.py"
        and metafunc.function.__name__ in _TARGETS
    ):
        metafunc.parametrize(
            "_ctrl_iteration",
            range(repeats),
            indirect=True,
            ids=[f"ctrl-{i + 1:03d}" for i in range(repeats)],
        )


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    recorder = getattr(config, "_ctrl_path_trace", None)
    if recorder is None:
        return
    order = {"test_connect_via_channel": 0, "test_generic_grpc_exception": 1}
    paired = all(
        item.originalname in _TARGETS and item.path.name == "test_grpc.py"
        for item in items
    )
    if paired:
        items.sort(
            key=lambda item: (
                item.callspec.params["_ctrl_iteration"],
                order[item.originalname],
            )
        )
    recorder.emit("collection", items=[item.nodeid for item in items], paired=paired)


def pytest_sessionstart(session):
    recorder = getattr(session.config, "_ctrl_path_trace", None)
    if recorder is None:
        return
    from ansys.mapdl import core

    source = Path(core.__file__).parent
    library_hashes = {
        name: hashlib.sha256((source / name).read_bytes()).hexdigest()
        for name in ("mapdl_grpc.py", "errors.py")
    }
    subject = os.environ.get("CTRL_SUBJECT_ROOT")
    if subject:
        for name, actual in library_hashes.items():
            expected = Path(subject) / "src/ansys/mapdl/core" / name
            if hashlib.sha256(expected.read_bytes()).hexdigest() != actual:
                raise pytest.UsageError(
                    "Installed library differs from the selected client source"
                )
    test_root = os.environ.get("CTRL_TEST_ROOT", subject)
    constraints = os.environ.get("CTRL_CONSTRAINTS")
    recorder.emit(
        "session_start",
        python=sys.version.split()[0],
        plugin_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        constraints_sha256=(
            hashlib.sha256(Path(constraints).read_bytes()).hexdigest()
            if constraints
            else None
        ),
        test_source_sha256=(
            {
                name: hashlib.sha256((Path(test_root) / name).read_bytes()).hexdigest()
                for name in ("tests/test_grpc.py", "tests/conftest.py")
            }
            if test_root
            else None
        ),
        test_ref=os.environ.get("CTRL_TEST_REF"),
        subject_ref=os.environ.get("CTRL_SUBJECT_REF"),
        diagnostic_ref=os.environ.get("GITHUB_SHA"),
        debug_testing=os.environ.get("PYMAPDL_DEBUG_TESTING"),
        packages={d.metadata["Name"]: d.version for d in metadata.distributions()},
        library_sha256=library_hashes,
    )
    recorder.start()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    recorder = getattr(item.config, "_ctrl_path_trace", None)
    if recorder is not None:
        recorder.nodeid = item.nodeid
        recorder.phase = "setup"
        recorder.emit("test_start")
    yield
    if recorder is not None:
        recorder.emit("test_end")
        recorder.nodeid = None
        recorder.phase = "between_tests"


def pytest_runtest_call(item):
    recorder = getattr(item.config, "_ctrl_path_trace", None)
    if recorder is not None:
        recorder.phase = "call"


def pytest_runtest_teardown(item):
    recorder = getattr(item.config, "_ctrl_path_trace", None)
    if recorder is not None:
        recorder.phase = "teardown"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    recorder = getattr(item.config, "_ctrl_path_trace", None)
    if recorder is not None:
        report = outcome.get_result()
        recorder.emit("test_report", when=report.when, outcome=report.outcome)


def pytest_sessionfinish(session, exitstatus):
    recorder = getattr(session.config, "_ctrl_path_trace", None)
    if recorder is not None:
        recorder.emit(
            "session_finish",
            exitstatus=int(exitstatus),
            trace_complete=recorder.failure is None,
        )
        recorder.close()
        if recorder.failure is not None:
            print("Ctrl path trace incomplete: " + recorder.failure, file=sys.stderr)
            if exitstatus == pytest.ExitCode.OK:
                session.exitstatus = pytest.ExitCode.INTERNAL_ERROR


def pytest_unconfigure(config):
    recorder = getattr(config, "_ctrl_path_trace", None)
    if recorder is not None:
        recorder.close()
