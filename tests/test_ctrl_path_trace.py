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

"""Offline tests for the STEP 1 liveness-path observer."""

from concurrent.futures import ThreadPoolExecutor
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock
import weakref

import grpc
import pytest

_PLUGIN_PATH = Path(__file__).resolve().parents[1] / ".ci/ctrl_path_trace.py"
_SPEC = importlib.util.spec_from_file_location("ctrl_path_trace", _PLUGIN_PATH)
assert _SPEC is not None
assert _SPEC.loader is not None
trace_plugin = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = trace_plugin
_SPEC.loader.exec_module(trace_plugin)
pytest_plugins = ["pytester"]


def records(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


@pytest.fixture
def recorder(tmp_path):
    observer = trace_plugin._Trace(tmp_path / "trace.jsonl")
    yield observer
    # Direct callback tests do not own the active coverage trace hook.
    observer._active = False
    observer.close()


def frame(function, client=None, module="ansys.mapdl.core.mapdl_grpc", **values):
    return SimpleNamespace(
        f_globals={"__name__": module},
        f_code=SimpleNamespace(co_name=function),
        f_locals={"self": client, **values},
        f_lineno=23,
        f_back=SimpleNamespace(
            f_code=SimpleNamespace(co_name="original_test"), f_lineno=7
        ),
    )


def test_emit_serializes_concurrent_records_and_ignores_closed_file(recorder, tmp_path):
    recorder.nodeid = "tests/test_grpc.py::test_connect_via_channel[ctrl-001]"
    recorder.phase = "call"
    with ThreadPoolExecutor(max_workers=4) as workers:
        list(workers.map(lambda value: recorder.emit("sample", value=value), range(80)))
    recorder.close()
    recorder.close()
    recorder.emit("must_not_be_written")
    observed = records(tmp_path / "trace.jsonl")
    assert [row["sequence"] for row in observed] == list(range(1, 81))
    assert {row["value"] for row in observed} == set(range(80))
    assert all(
        row["nodeid"] == recorder.nodeid and row["phase"] == "call" for row in observed
    )
    assert all(
        isinstance(row["time_ns"], int) and isinstance(row["thread"], int)
        for row in observed
    )


def test_snapshot_reads_only_stored_safe_state(recorder):
    class Client:
        @property
        def is_alive(self):
            pytest.fail("Diagnostics must not call liveness properties")

    client = Client()
    client._channel_state = grpc.ChannelConnectivity.READY
    client._MapdlCore__exited = False
    client._exiting = False
    client._busy = True
    client._stub = object()
    client._channel_str = "private-endpoint:50052"
    assert recorder._snapshot(None) == {}
    snapshot = recorder._snapshot(client)
    assert snapshot == {
        "client": None,
        "channel_state": "READY",
        "exited": False,
        "exiting": False,
        "busy": True,
        "has_stub": True,
    }
    client._channel_state = "not-a-connectivity-enum"
    client._stub = None
    assert recorder._snapshot(client)["channel_state"] is None
    assert recorder._snapshot(client)["has_stub"] is False
    assert "private-endpoint" not in json.dumps(snapshot)


@pytest.mark.parametrize("command", ["VERSION", "EXIT"])
def test_trace_status_and_returns_do_not_publish_payloads(recorder, tmp_path, command):
    class RpcFailure(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.UNIMPLEMENTED

        def details(self):
            pytest.fail("Diagnostics must not read server exception details")

        def __str__(self):
            pytest.fail("Diagnostics must not stringify server exceptions")

    client = SimpleNamespace(_stub=object(), _MapdlCore__exited=False)
    recorder._active = True
    recorder.trace(frame("__init__", client), "call", None)
    ctrl_frame = frame("_ctrl_raw", client, cmd=command)
    recorder.trace(
        ctrl_frame, "exception", (RpcFailure, RpcFailure("private-payload"), None)
    )
    recorder.trace(ctrl_frame, "return", "private-response")
    recorder.trace(frame("_ctrl", client, cmd="private-command"), "return", None)
    recorder.trace(
        frame("_connect", client),
        "exception",
        (ValueError, ValueError("private-value"), None),
    )
    protected_frame = frame("wrapper", module="ansys.mapdl.core.errors")
    protected_frame.f_locals = {"mapdl": client}
    recorder.trace(protected_frame, "call", None)
    observed = records(tmp_path / "trace.jsonl")
    assert observed[0]["client"] == 1
    assert observed[1]["grpc_status"] == "UNIMPLEMENTED"
    assert observed[1]["exception_type"] == "RpcFailure"
    assert observed[1]["ctrl_command"] == command
    assert observed[1]["caller_function"] == "original_test"
    assert observed[2]["nonempty_response"] is True
    assert observed[3]["nonempty_response"] is False
    assert "ctrl_command" not in observed[3]
    assert "grpc_status" not in observed[4]
    assert observed[5]["client"] == 1
    assert "private-" not in json.dumps(observed)


def test_trace_filters_frames_and_records_boolean_branches(recorder, tmp_path):
    assert recorder.trace(frame("is_alive"), "call", None) is None
    recorder._active = True
    assert (
        recorder.trace(frame("is_alive", module="unrelated.module"), "call", None)
        is None
    )
    assert recorder.trace(frame("prep7"), "call", None) is None
    assert recorder.trace(frame("_connect"), "line", None) == recorder.trace
    assert recorder.trace(frame("_ctrl"), "opcode", None) == recorder.trace
    alive_frame = frame("is_alive")
    recorder.trace(alive_frame, "line", None)
    for result in (True, False, None):
        recorder.trace(alive_frame, "return", result)
    error_frame = frame("wrapper", module="ansys.mapdl.core.errors")
    error_frame.f_back = None
    recorder.trace(error_frame, "call", None)
    generic_frame = frame("handle_generic_grpc_error", module="ansys.mapdl.core.errors")
    recorder.trace(generic_frame, "call", None)
    observed = records(tmp_path / "trace.jsonl")
    assert [row["event"] for row in observed] == [
        "line",
        "return",
        "return",
        "return",
        "call",
        "call",
    ]
    assert [row["result"] for row in observed[1:4]] == [True, False, None]
    assert "caller_function" not in observed[4]


def test_trace_handles_nonstatus_rpc_errors(recorder, tmp_path):
    class UnknownRpcFailure(grpc.RpcError):
        def code(self):
            return None

    recorder._active = True
    recorder.trace(
        frame("_ctrl"), "exception", (UnknownRpcFailure, UnknownRpcFailure(), None)
    )
    assert records(tmp_path / "trace.jsonl")[0]["grpc_status"] is None


def test_trace_does_not_retain_clients_or_exception_objects(recorder):
    class Client:
        pass

    class RpcFailure(grpc.RpcError):
        def code(self):
            return grpc.StatusCode.UNAVAILABLE

    client = Client()
    error = RpcFailure()
    client_ref, error_ref = weakref.ref(client), weakref.ref(error)
    recorder._active = True
    recorder.trace(frame("__init__", client), "call", None)
    recorder.trace(frame("_ctrl", client), "exception", (RpcFailure, error, None))
    del client, error
    gc.collect()
    assert client_ref() is None
    assert error_ref() is None


def test_start_and_close_manage_only_tracing_hooks(recorder, monkeypatch):
    main_setter, thread_setter = Mock(), Mock()
    monkeypatch.setattr(trace_plugin.sys, "gettrace", lambda: None)
    monkeypatch.setattr(trace_plugin.threading, "gettrace", lambda: None)
    monkeypatch.setattr(trace_plugin.sys, "settrace", main_setter)
    monkeypatch.setattr(trace_plugin.threading, "settrace", thread_setter)
    recorder.start()
    assert recorder._active
    main_setter.assert_called_once_with(recorder.trace)
    thread_setter.assert_called_once_with(recorder.trace)
    recorder.close()
    assert not recorder._active
    assert main_setter.call_args.args == (None,)
    assert thread_setter.call_args.args == (None,)


@pytest.mark.parametrize(
    "existing_main,existing_thread", [(True, False), (False, True)]
)
def test_start_rejects_existing_trace_hooks(
    recorder, monkeypatch, existing_main, existing_thread
):
    monkeypatch.setattr(
        trace_plugin.sys, "gettrace", lambda: object() if existing_main else None
    )
    monkeypatch.setattr(
        trace_plugin.threading,
        "gettrace",
        lambda: object() if existing_thread else None,
    )
    with pytest.raises(pytest.UsageError, match="coverage tracer or debugger"):
        recorder.start()
    assert not recorder._active


def configuration(tmp_path, repetitions):
    options = {
        "ctrl_path_repetitions": repetitions,
        "ctrl_path_log": str(tmp_path / "trace.jsonl"),
    }
    return SimpleNamespace(
        getoption=lambda key, default=None: options.get(key, default)
    )


def complete_hook(hook, result=None):
    with pytest.raises(StopIteration):
        hook.send(result)


def test_configuration_and_phase_hooks(tmp_path, monkeypatch):
    monkeypatch.delenv("CTRL_SUBJECT_ROOT", raising=False)
    monkeypatch.delenv("CTRL_CONSTRAINTS", raising=False)
    config = configuration(tmp_path, 2)
    parser = Mock()
    trace_plugin.pytest_addoption(parser)
    assert parser.addoption.call_count == 2
    trace_plugin.pytest_configure(config)
    observer = config._ctrl_path_trace
    monkeypatch.setattr(observer, "start", Mock())
    fake_mapdl = ModuleType("ansys.mapdl")
    fake_mapdl.core = SimpleNamespace(__file__=str(tmp_path / "__init__.py"))
    for name in ("mapdl_grpc.py", "errors.py"):
        (tmp_path / name).write_text("# synthetic source\n", encoding="utf-8")
    monkeypatch.setitem(sys.modules, "ansys.mapdl", fake_mapdl)
    monkeypatch.setattr(
        trace_plugin.metadata,
        "distributions",
        lambda: [SimpleNamespace(metadata={"Name": "test-package"}, version="1.0")],
    )
    session = SimpleNamespace(config=config)
    trace_plugin.pytest_sessionstart(session)
    observer.start.assert_called_once_with()
    item = SimpleNamespace(
        config=config, nodeid="test_grpc.py::test_connect_via_channel[ctrl-001]"
    )
    protocol = trace_plugin.pytest_runtest_protocol(item, None)
    next(protocol)
    assert (observer.nodeid, observer.phase) == (item.nodeid, "setup")
    trace_plugin.pytest_runtest_call(item)
    assert observer.phase == "call"
    for when in ("setup", "call", "teardown"):
        hook = trace_plugin.pytest_runtest_makereport(item, None)
        next(hook)
        complete_hook(
            hook,
            SimpleNamespace(
                get_result=lambda: SimpleNamespace(when=when, outcome="passed")
            ),
        )
    trace_plugin.pytest_runtest_teardown(item)
    assert observer.phase == "teardown"
    complete_hook(protocol)
    assert (observer.nodeid, observer.phase) == (None, "between_tests")
    trace_plugin.pytest_sessionfinish(session, 0)
    trace_plugin.pytest_unconfigure(config)
    observed = records(tmp_path / "trace.jsonl")
    assert [row["event"] for row in observed] == [
        "session_start",
        "test_start",
        "test_report",
        "test_report",
        "test_report",
        "test_end",
        "session_finish",
    ]
    assert observed[0]["packages"] == {"test-package": "1.0"}
    assert (
        observed[0]["plugin_sha256"]
        == hashlib.sha256(_PLUGIN_PATH.read_bytes()).hexdigest()
    )
    assert observed[0]["constraints_sha256"] is None
    assert observed[0]["test_source_sha256"] is None
    assert set(observed[0]["library_sha256"]) == {"mapdl_grpc.py", "errors.py"}
    assert observed[-1]["exitstatus"] == 0


def test_disabled_and_invalid_configuration(tmp_path):
    with pytest.raises(pytest.UsageError, match="nonnegative"):
        trace_plugin.pytest_configure(configuration(tmp_path, -1))
    config = configuration(tmp_path, 0)
    trace_plugin.pytest_configure(config)
    assert not hasattr(config, "_ctrl_path_trace")
    session, item = SimpleNamespace(config=config), SimpleNamespace(config=config)
    trace_plugin.pytest_sessionstart(session)
    protocol = trace_plugin.pytest_runtest_protocol(item, None)
    next(protocol)
    complete_hook(protocol)
    trace_plugin.pytest_runtest_call(item)
    trace_plugin.pytest_runtest_teardown(item)
    report = trace_plugin.pytest_runtest_makereport(item, None)
    next(report)
    complete_hook(report)
    trace_plugin.pytest_sessionfinish(session, 0)
    trace_plugin.pytest_unconfigure(config)
    assert not (tmp_path / "trace.jsonl").exists()


@pytest.mark.parametrize(
    "function,repetitions,expected",
    [
        ("test_connect_via_channel", 2, True),
        ("test_generic_grpc_exception", 2, True),
        ("test_other", 2, False),
        ("test_connect_via_channel", 0, False),
    ],
)
def test_generation_selects_original_targets(tmp_path, function, repetitions, expected):
    metafunc = SimpleNamespace(
        config=configuration(tmp_path, repetitions),
        function=SimpleNamespace(__name__=function),
        definition=SimpleNamespace(
            path=tmp_path / "test_grpc.py", nodeid=f"test_grpc.py::{function}"
        ),
        module=SimpleNamespace(__file__=str(tmp_path / "test_grpc.py")),
        parametrize=Mock(),
    )
    trace_plugin.pytest_generate_tests(metafunc)
    assert metafunc.parametrize.called is expected
    if expected:
        args, kwargs = metafunc.parametrize.call_args
        assert args[0] == "_ctrl_iteration"
        assert list(args[1]) == [0, 1]
        assert kwargs["indirect"] is True
        assert kwargs["ids"] == ["ctrl-001", "ctrl-002"]


_SYNTHETIC_CLIENT = """
import grpc
from .errors import protect_grpc

class RpcFailure(grpc.RpcError):
    def code(self):
        return grpc.StatusCode.UNIMPLEMENTED
    def details(self):
        raise AssertionError("observer read exception payload")

class MapdlGrpc:
    def __init__(self, channel=None, fallback=True):
        self._channel_state = grpc.ChannelConnectivity.READY
        self._stub = object()
        self._exited = False
        self._exiting = False
        self._busy = False
        self._fallback = fallback
        self._connect()
    @property
    def _exited(self):
        return self._MapdlCore__exited
    @_exited.setter
    def _exited(self, value):
        self._MapdlCore__exited = value
    def _connect(self):
        return True
    def _ctrl_raw(self, cmd):
        raise RpcFailure("secret-rpc-payload-endpoint")
    @protect_grpc
    def _ctrl(self, cmd):
        return self._ctrl_raw(cmd)
    @property
    def is_alive(self):
        if self._exited:
            return False
        try:
            return bool(self._ctrl("VERSION"))
        except grpc.RpcError:
            if self._fallback:
                return True
            return False
"""

_SYNTHETIC_ERRORS = """
from functools import wraps

def protect_grpc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
"""

_SYNTHETIC_CONFTEST = """
import json
import os
from pathlib import Path
import grpc
import pytest

@pytest.fixture(scope="session")
def mapdl():
    counts = {"session_setup": 1, "session_teardown": 0, "function_setup": 0, "function_teardown": 0}
    yield counts
    counts["session_teardown"] += 1
    Path("fixture-counts.json").write_text(json.dumps(counts))
    assert counts["function_setup"] == counts["function_teardown"] == int(os.environ["EXPECTED_TESTS"])

@pytest.fixture
def grpc_channel(mapdl, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unexpected network RPC/channel")
    monkeypatch.setattr(grpc, "insecure_channel", forbidden)
    mapdl["function_setup"] += 1
    yield object()
    mapdl["function_teardown"] += 1
"""

_SYNTHETIC_TESTS = """
import os
from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

def test_connect_via_channel(grpc_channel):
    mapdl = MapdlGrpc(channel=grpc_channel, fallback=os.environ.get("FAIL_ORIGINAL") != "1")
    assert mapdl.is_alive

def test_generic_grpc_exception(grpc_channel):
    mapdl = MapdlGrpc(channel=grpc_channel, fallback=False)
    assert not mapdl.is_alive
"""


def synthetic_project(pytester, monkeypatch, expected):
    monkeypatch.setenv("PYTHONPATH", str(_PLUGIN_PATH.parent))
    monkeypatch.setenv("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
    for key in (
        "PYTEST_ADDOPTS",
        "COVERAGE_PROCESS_START",
        "ALLOW_FAILURE_RATE",
        "CTRL_SUBJECT_ROOT",
        "CTRL_CONSTRAINTS",
        "FAIL_ORIGINAL",
    ):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("EXPECTED_TESTS", str(expected))
    for directory in ("ansys", "ansys/mapdl", "ansys/mapdl/core"):
        package = pytester.path / directory
        package.mkdir(exist_ok=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
    (pytester.path / "ansys/mapdl/core/mapdl_grpc.py").write_text(
        _SYNTHETIC_CLIENT, encoding="utf-8"
    )
    (pytester.path / "ansys/mapdl/core/errors.py").write_text(
        _SYNTHETIC_ERRORS, encoding="utf-8"
    )
    pytester.makeconftest(_SYNTHETIC_CONFTEST)
    pytester.makepyfile(test_grpc=_SYNTHETIC_TESTS)
    pytester.makeini("[pytest]\naddopts = --reruns=3 --maxfail=4\n")
    return [
        "-p",
        "ctrl_path_trace",
        "-p",
        "pytest_cov.plugin",
        "-p",
        "pytest_rerunfailures",
        "-p",
        "random_order.plugin",
        "-o",
        "addopts=",
        "--no-cov",
        "--reruns=0",
        "--random-order-bucket=none",
        "--maxfail=1",
        "-q",
        "test_grpc.py",
    ]


def test_real_trace_repetitions_preserve_fixtures_and_expected_false(
    pytester, monkeypatch
):
    args = synthetic_project(pytester, monkeypatch, expected=4)
    result = pytester.runpytest_subprocess(*args, "--ctrl-path-repetitions=2")
    result.assert_outcomes(passed=4)
    observed = records(pytester.path / "ctrl-path.jsonl")
    counts = json.loads((pytester.path / "fixture-counts.json").read_text())
    assert counts == {
        "session_setup": 1,
        "session_teardown": 1,
        "function_setup": 4,
        "function_teardown": 4,
    }
    starts = [row for row in observed if row["event"] == "test_start"]
    assert [row["nodeid"] for row in starts] == [
        f"test_grpc.py::{name}[ctrl-{iteration:03d}]"
        for iteration in (1, 2)
        for name in ("test_connect_via_channel", "test_generic_grpc_exception")
    ]
    collection = next(row for row in observed if row["event"] == "collection")
    assert collection["items"] == [row["nodeid"] for row in starts]
    for start in starts:
        events = [row for row in observed if row["nodeid"] == start["nodeid"]]
        raw_error = next(
            row
            for row in events
            if row["event"] == "exception" and row.get("function") == "_ctrl_raw"
        )
        alive_return = next(
            row
            for row in events
            if row["event"] == "return" and row.get("function") == "is_alive"
        )
        assert raw_error["grpc_status"] == "UNIMPLEMENTED"
        assert raw_error["sequence"] < alive_return["sequence"]
        assert alive_return["result"] is ("test_connect_via_channel" in start["nodeid"])
        assert alive_return["exited"] is False
        assert any(
            row["event"] == "line" and row.get("function") == "is_alive"
            for row in events
        )
        assert [row["outcome"] for row in events if row["event"] == "test_report"] == [
            "passed"
        ] * 3
    assert observed[-1]["event"] == "session_finish"
    assert observed[-1]["exitstatus"] == 0
    assert "secret-rpc-payload-endpoint" not in json.dumps(observed)


def test_real_trace_stops_first_failure_without_retry(pytester, monkeypatch):
    args = synthetic_project(pytester, monkeypatch, expected=1)
    monkeypatch.setenv("FAIL_ORIGINAL", "1")
    result = pytester.runpytest_subprocess(*args, "--ctrl-path-repetitions=2")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    observed = records(pytester.path / "ctrl-path.jsonl")
    assert sum(row["event"] == "test_start" for row in observed) == 1
    assert [
        row["outcome"]
        for row in observed
        if row["event"] == "test_report" and row["when"] == "call"
    ] == ["failed"]
    assert observed[-1]["exitstatus"] == 1
    counts = json.loads((pytester.path / "fixture-counts.json").read_text())
    assert counts["session_teardown"] == counts["function_teardown"] == 1


def test_inactive_plugin_keeps_unparametrized_tests(pytester, monkeypatch):
    args = synthetic_project(pytester, monkeypatch, expected=2)
    result = pytester.runpytest_subprocess(*args)
    result.assert_outcomes(passed=2)
    assert not (pytester.path / "ctrl-path.jsonl").exists()


def test_collection_orders_distinct_cases_by_iteration(tmp_path):
    config = configuration(tmp_path, 2)
    trace_plugin.pytest_configure(config)
    items = [
        SimpleNamespace(
            callspec=SimpleNamespace(params={"_ctrl_iteration": iteration}),
            originalname=name,
            path=Path("tests/test_grpc.py"),
            nodeid=f"test_grpc.py::{name}[ctrl-{iteration + 1:03d}]",
        )
        for name in ("test_generic_grpc_exception", "test_connect_via_channel")
        for iteration in (1, 0)
    ]
    trace_plugin.pytest_collection_modifyitems(config, items)
    assert [
        (item.callspec.params["_ctrl_iteration"], item.originalname) for item in items
    ] == [
        (iteration, name)
        for iteration in (0, 1)
        for name in ("test_connect_via_channel", "test_generic_grpc_exception")
    ]
    trace_plugin.pytest_unconfigure(config)
    assert records(tmp_path / "trace.jsonl")[0]["items"] == [
        item.nodeid for item in items
    ]
    trace_plugin.pytest_collection_modifyitems(configuration(tmp_path, 0), [])


def test_generation_does_not_repeat_same_name_in_other_module(tmp_path):
    metafunc = SimpleNamespace(
        config=configuration(tmp_path, 2),
        function=SimpleNamespace(__name__="test_connect_via_channel"),
        definition=SimpleNamespace(path=tmp_path / "test_other.py"),
        parametrize=Mock(),
    )
    trace_plugin.pytest_generate_tests(metafunc)
    metafunc.parametrize.assert_not_called()


@pytest.mark.parametrize("matching", [True, False])
def test_sessionstart_checks_installed_source_hashes(tmp_path, monkeypatch, matching):
    installed = tmp_path / "installed"
    installed.mkdir()
    subject = tmp_path / "subject"
    source = subject / "src/ansys/mapdl/core"
    source.mkdir(parents=True)
    for name in ("mapdl_grpc.py", "errors.py"):
        (installed / name).write_text("# subject source\n", encoding="utf-8")
        (source / name).write_text(
            "# subject source\n" if matching else "# wrong source\n", encoding="utf-8"
        )
    fake_mapdl = ModuleType("ansys.mapdl")
    fake_mapdl.core = SimpleNamespace(__file__=str(installed / "__init__.py"))
    monkeypatch.setitem(sys.modules, "ansys.mapdl", fake_mapdl)
    (subject / "tests").mkdir()
    for name in ("test_grpc.py", "conftest.py"):
        (subject / "tests" / name).write_text(
            "# original subject test source\n", encoding="utf-8"
        )
    constraints = tmp_path / "constraints.txt"
    constraints.write_text("grpcio==1.0\n", encoding="utf-8")
    monkeypatch.setenv("CTRL_SUBJECT_ROOT", str(subject))
    monkeypatch.setenv("CTRL_CONSTRAINTS", str(constraints))
    monkeypatch.setattr(trace_plugin.metadata, "distributions", lambda: [])
    config = configuration(tmp_path, 2)
    trace_plugin.pytest_configure(config)
    observer = config._ctrl_path_trace
    monkeypatch.setattr(observer, "start", Mock())
    try:
        if matching:
            trace_plugin.pytest_sessionstart(SimpleNamespace(config=config))
            observer.start.assert_called_once_with()
            start = records(tmp_path / "trace.jsonl")[0]
            assert start["event"] == "session_start"
            assert (
                start["plugin_sha256"]
                == hashlib.sha256(_PLUGIN_PATH.read_bytes()).hexdigest()
            )
            assert (
                start["constraints_sha256"]
                == hashlib.sha256(constraints.read_bytes()).hexdigest()
            )
            assert start["test_source_sha256"] == {
                name: hashlib.sha256((subject / name).read_bytes()).hexdigest()
                for name in ("tests/test_grpc.py", "tests/conftest.py")
            }
        else:
            with pytest.raises(pytest.UsageError, match="Installed library differs"):
                trace_plugin.pytest_sessionstart(SimpleNamespace(config=config))
            observer.start.assert_not_called()
            assert records(tmp_path / "trace.jsonl") == []
    finally:
        trace_plugin.pytest_unconfigure(config)


def test_collection_preserves_mixed_items_in_original_order(tmp_path):
    config = configuration(tmp_path, 2)
    trace_plugin.pytest_configure(config)
    items = [
        SimpleNamespace(
            originalname="test_connect_via_channel",
            path=Path("tests/test_grpc.py"),
            nodeid="test_grpc.py::test_connect_via_channel[ctrl-002]",
        ),
        SimpleNamespace(
            originalname="test_other",
            path=Path("tests/test_other.py"),
            nodeid="test_other.py::test_other",
        ),
        SimpleNamespace(
            originalname="test_connect_via_channel",
            path=Path("tests/test_grpc.py"),
            nodeid="test_grpc.py::test_connect_via_channel[ctrl-001]",
        ),
    ]
    original_order = list(items)
    trace_plugin.pytest_collection_modifyitems(config, items)
    trace_plugin.pytest_unconfigure(config)
    assert items == original_order
    collection = records(tmp_path / "trace.jsonl")[0]
    assert collection["paired"] is False
    assert collection["items"] == [item.nodeid for item in original_order]


@pytest.mark.parametrize("error_type", [OSError, RecursionError, TypeError, ValueError])
def test_emit_contains_writer_failure(recorder, monkeypatch, error_type):
    original_file = recorder._file
    writer = SimpleNamespace(
        write=Mock(side_effect=error_type("private observer payload")),
        close=original_file.close,
    )
    monkeypatch.setattr(recorder, "_file", writer)
    recorder._active = True
    recorder.emit("sample")
    assert recorder.failure == error_type.__name__
    assert recorder._active is False
    assert recorder.trace(frame("_ctrl"), "call", None) is None


def test_emit_contains_serialization_failure(recorder, tmp_path):
    recorder.emit("sample", unsupported=object())
    assert recorder.failure == "TypeError"
    assert records(tmp_path / "trace.jsonl") == []


@pytest.mark.parametrize(
    "error_type", [AttributeError, OSError, RecursionError, TypeError, ValueError]
)
def test_trace_contains_observer_errors(recorder, monkeypatch, error_type):
    def fail_snapshot(client):
        raise error_type("private observer payload")

    monkeypatch.setattr(recorder, "_snapshot", fail_snapshot)
    recorder._active = True
    assert recorder.trace(frame("_ctrl"), "call", None) is None
    assert recorder.failure == error_type.__name__
    assert recorder._active is False


def test_failure_keeps_only_first_error_type_and_clears_owned_hooks(
    recorder, monkeypatch
):
    class ObserverFailure(ValueError):
        pass

    main_setter, thread_setter = Mock(), Mock()
    monkeypatch.setattr(trace_plugin.sys, "settrace", main_setter)
    monkeypatch.setattr(trace_plugin.threading, "settrace", thread_setter)
    recorder._active = recorder._started = True
    error = ObserverFailure("private observer payload")
    error_ref = weakref.ref(error)
    recorder._fail(error)
    del error
    gc.collect()
    recorder._fail(OSError("another private payload"))
    assert error_ref() is None
    assert recorder.failure == "ObserverFailure"
    assert recorder._active is False
    main_setter.assert_called_with(None)
    thread_setter.assert_called_with(None)
    recorder.close()
    assert recorder._started is False


def test_close_contains_file_failure(recorder, monkeypatch):
    original_file = recorder._file
    writer = SimpleNamespace(close=Mock(side_effect=OSError("private close payload")))
    monkeypatch.setattr(recorder, "_file", writer)
    try:
        recorder.close()
        assert recorder.failure == "OSError"
        recorder.close()
        writer.close.assert_called_once_with()
    finally:
        original_file.close()


@pytest.mark.parametrize(
    "original_status", [pytest.ExitCode.OK, pytest.ExitCode.TESTS_FAILED]
)
def test_incomplete_trace_marks_session_without_hiding_original_failure(
    recorder, tmp_path, capsys, original_status
):
    recorder._fail(ValueError("private observer payload"))
    session = SimpleNamespace(
        config=SimpleNamespace(_ctrl_path_trace=recorder), exitstatus=original_status
    )
    trace_plugin.pytest_sessionfinish(session, original_status)
    assert session.exitstatus == (
        pytest.ExitCode.INTERNAL_ERROR
        if original_status == pytest.ExitCode.OK
        else original_status
    )
    finish = records(tmp_path / "trace.jsonl")[-1]
    assert finish["trace_complete"] is False
    assert finish["exitstatus"] == original_status
    stderr = capsys.readouterr().err
    assert "Ctrl path trace incomplete: ValueError" in stderr
    assert "private observer payload" not in stderr


@pytest.mark.parametrize("original_failure", [False, True])
def test_real_observer_failure_does_not_replace_original_execution(
    pytester, monkeypatch, original_failure
):
    expected = 1 if original_failure else 4
    args = synthetic_project(pytester, monkeypatch, expected=expected)
    if original_failure:
        monkeypatch.setenv("FAIL_ORIGINAL", "1")
    pytester.makeconftest(_SYNTHETIC_CONFTEST + """
def pytest_sessionstart(session):
    def fail_snapshot(client):
        raise ValueError("private observer payload")
    session.config._ctrl_path_trace._snapshot = fail_snapshot
""")
    result = pytester.runpytest_subprocess(*args, "--ctrl-path-repetitions=2")
    if original_failure:
        result.assert_outcomes(failed=1)
        assert result.ret == pytest.ExitCode.TESTS_FAILED
    else:
        result.assert_outcomes(passed=4)
        assert result.ret == pytest.ExitCode.INTERNAL_ERROR
    observed = records(pytester.path / "ctrl-path.jsonl")
    assert sum(row["event"] == "test_start" for row in observed) == expected
    assert observed[-1]["trace_complete"] is False
    assert "private observer payload" not in json.dumps(observed)
    counts = json.loads((pytester.path / "fixture-counts.json").read_text())
    assert counts["session_teardown"] == 1
    assert counts["function_teardown"] == expected


def test_snapshot_reads_real_exited_property_backing(recorder, monkeypatch):
    from ansys.mapdl.core.mapdl_grpc import MapdlGrpc

    def forbidden(*args, **kwargs):
        pytest.fail("The backing-property test must not initialize or connect MAPDL")

    monkeypatch.setattr(MapdlGrpc, "__init__", forbidden)
    monkeypatch.setattr(grpc, "insecure_channel", forbidden)
    # The uninitialized object owns no resources for the destructor to release.
    monkeypatch.setattr(MapdlGrpc, "__del__", lambda self: None)
    client = MapdlGrpc.__new__(MapdlGrpc)
    try:
        for exited in (True, False):
            client._exited = exited
            assert vars(client)["_MapdlCore__exited"] is exited
            assert "_exited" not in vars(client)
            assert recorder._snapshot(client)["exited"] is exited
    finally:
        del client
