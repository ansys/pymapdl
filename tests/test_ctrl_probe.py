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

"""gRPC service specific tests"""

from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock

from ansys.api.mapdl.v0 import mapdl_pb2_grpc
import grpc
import pytest

import conftest

pytest_plugins = ["pytester"]


class ProbeError(grpc.RpcError):
    def __init__(self, status):
        self.status = status

    def code(self):
        return self.status


def mock_probe(monkeypatch, tmp_path, status=None):
    output = tmp_path / "probe.jsonl"
    monkeypatch.setenv("PYMAPDL_CTRL_PROBE_FILE", str(output))
    monkeypatch.setenv("PYMAPDL_IP", "127.0.0.1")
    monkeypatch.setenv("PYMAPDL_PORT", "21000")
    channel = MagicMock()
    channel.__enter__.return_value = channel
    channel_factory = MagicMock(return_value=channel)
    stub = MagicMock()
    if status:
        stub.Ctrl.side_effect = ProbeError(status)
    monkeypatch.setattr(grpc, "insecure_channel", channel_factory)
    monkeypatch.setattr(mapdl_pb2_grpc, "MapdlServiceStub", lambda _: stub)
    return output, channel, channel_factory, stub


@pytest.mark.parametrize(
    "status", [None, grpc.StatusCode.UNIMPLEMENTED, grpc.StatusCode.UNAVAILABLE]
)
def test_probe_closes_fresh_channel(monkeypatch, tmp_path, status):
    output, channel, factory, stub = mock_probe(monkeypatch, tmp_path, status)
    record = conftest._probe_ctrl(SimpleNamespace(), "test_previous", "after_teardown")
    factory.assert_called_once_with(
        "127.0.0.1:21000", options=(("grpc.use_local_subchannel_pool", 1),)
    )
    channel.__exit__.assert_called_once()
    assert stub.Ctrl.call_args.args[0].ctrl == "VERSION"
    assert stub.Ctrl.call_args.kwargs == {"timeout": 2.0}
    assert record["status"] == (status.name if status else "OK")
    assert record["first_unimplemented"] == (status == grpc.StatusCode.UNIMPLEMENTED)
    assert record["nodeid"] == "test_previous"
    assert output.read_text().count("\n") == 1
    assert "127.0.0.1" not in output.read_text()


def test_probe_marks_only_first_unimplemented(monkeypatch, tmp_path):
    mock_probe(monkeypatch, tmp_path, grpc.StatusCode.UNIMPLEMENTED)
    config = SimpleNamespace()
    first = conftest._probe_ctrl(config, None, "session_start")
    second = conftest._probe_ctrl(config, "test_later", "after_teardown", 2)
    assert first["first_unimplemented"]
    assert not second["first_unimplemented"]
    assert (first["sequence"], second["sequence"]) == (1, 2)
    assert second["attempt"] == 2


def test_probe_runs_after_teardown(monkeypatch):
    monkeypatch.setenv("PYMAPDL_CTRL_PROBE", "1")
    probe = MagicMock()
    monkeypatch.setattr(conftest, "_probe_ctrl", probe)
    item = SimpleNamespace(config=SimpleNamespace(), nodeid="test_a", execution_count=2)
    hook = conftest.pytest_runtest_makereport(item, SimpleNamespace(when="teardown"))
    next(hook)
    probe.assert_not_called()
    with pytest.raises(StopIteration):
        next(hook)
    probe.assert_called_once_with(item.config, "test_a", "after_teardown", 2)


def test_probe_disabled_by_default(monkeypatch):
    monkeypatch.delenv("PYMAPDL_CTRL_PROBE", raising=False)
    probe = MagicMock()
    monkeypatch.setattr(conftest, "_probe_ctrl", probe)
    conftest.pytest_sessionstart(SimpleNamespace())
    hook = conftest.pytest_runtest_makereport(
        SimpleNamespace(), SimpleNamespace(when="teardown")
    )
    next(hook)
    with pytest.raises(StopIteration):
        next(hook)
    probe.assert_not_called()


@pytest.mark.parametrize("retry_condition", [True, False])
def test_probe_follows_rerun_plugin_finalizers(monkeypatch, pytester, retry_condition):
    events = pytester.path / "events.txt"
    pytester.makeini("[pytest]\naddopts=")
    pytester.makepyfile(f"""
        from pathlib import Path
        import pytest

        attempts = 0

        @pytest.fixture(scope="module", autouse=True)
        def resource():
            yield
            with Path({str(events)!r}).open("a") as stream:
                stream.write("module_teardown\\n")

        @pytest.mark.flaky(reruns=1, condition={retry_condition})
        def test_retry():
            global attempts
            attempts += 1
            assert attempts > 1
        """)

    def record(*args):
        with events.open("a") as stream:
            stream.write("probe\n")

    monkeypatch.setenv("PYMAPDL_CTRL_PROBE", "1")
    monkeypatch.setattr(conftest, "_probe_ctrl", record)
    plugin = ModuleType("ctrl_probe_integration")
    plugin.pytest_runtest_makereport = conftest.pytest_runtest_makereport
    result = pytester.runpytest_inprocess(
        "--reruns=1", "--reruns-delay=0", "-q", plugins=[plugin]
    )
    if retry_condition:
        result.assert_outcomes(passed=1)
    else:
        result.assert_outcomes(failed=1)
    assert result.parseoutcomes().get("rerun", 0) == int(retry_condition)
    observed = events.read_text().splitlines()
    assert observed.count("probe") == (2 if retry_condition else 1)
    assert observed[-2:] == ["module_teardown", "probe"]
