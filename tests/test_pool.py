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

import os
from pathlib import Path
import socket
import time

import numpy as np
import pytest

from conftest import ON_LOCAL, ON_STUDENT, START_INSTANCE, has_dependency

if has_dependency("ansys-tools-path"):
    from ansys.tools.path import find_ansys

    EXEC_FILE = find_ansys()[0]

else:
    EXEC_FILE = os.environ.get("PYMAPDL_MAPDL_EXEC")

from ansys.mapdl.core import Mapdl, MapdlPool, examples
from ansys.mapdl.core.errors import VersionError
from ansys.mapdl.core.launcher import LOCALHOST, MAPDL_DEFAULT_PORT
from conftest import QUICK_LAUNCH_SWITCHES, NullContext, requires

# skip entire module unless HAS_GRPC
pytestmark = requires("grpc")

# skipping if ON_STUDENT and ON_LOCAL because we cannot spawn that many instances.
if ON_STUDENT and ON_LOCAL:
    pytest.skip(allow_module_level=True)


skip_if_ignore_pool = pytest.mark.skipif(
    os.environ.get("IGNORE_POOL", "").upper() == "TRUE",
    reason="Ignoring Pool tests.",
)


MAPDL194PATH = "/usr/ansys_inc/v194/ansys/bin/mapdl"
skip_requires_194 = pytest.mark.skipif(
    not os.path.isfile(MAPDL194PATH), reason="Requires MAPDL 194"
)

TWAIT = 100
NPROC = 1


@pytest.fixture(scope="module")
def pool(tmpdir_factory):
    run_path = str(tmpdir_factory.mktemp("ansys_pool"))

    port = os.environ.get("PYMAPDL_PORT", 50056)

    if ON_LOCAL:

        mapdl_pool = MapdlPool(
            2,
            license_server_check=False,
            run_location=run_path,
            port=port,
            start_timeout=30,
            exec_file=EXEC_FILE,
            additional_switches=QUICK_LAUNCH_SWITCHES,
            nproc=NPROC,
            wait=True,  # make sure that the pool is ready before testing
        )
    else:
        port2 = os.environ.get("PYMAPDL_PORT2", 50057)

        mapdl_pool = MapdlPool(
            2,
            license_server_check=False,
            start_instance=False,
            port=[port, port2],
            wait=True,
        )

    yield mapdl_pool

    ##########################################################################
    # test exit
    mapdl_pool.exit()

    timeout = time.time() + TWAIT

    while len(mapdl_pool) != 0:
        time.sleep(0.1)
        if time.time() > timeout:
            raise TimeoutError(f"Failed to kill instance in {TWAIT} seconds")

    assert len(mapdl_pool) == 0

    # check it's been cleaned up
    if mapdl_pool[0] is not None:
        pth = mapdl_pool[0].directory
        if mapdl_pool._spawn_kwargs["remove_temp_files"]:
            assert not list(Path(pth).rglob("*.page*"))


@skip_requires_194
def test_invalid_exec():
    with pytest.raises(VersionError):
        MapdlPool(
            4,
            nproc=NPROC,
            exec_file="/usr/ansys_inc/v194/ansys/bin/mapdl",
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


# @pytest.mark.xfail(strict=False, reason="Flaky test. See #2435")
def test_heal(pool):
    pool_sz = len(pool)
    pool_names = pool._names  # copy pool names

    # Killing one instance
    pool[0].exit()

    time.sleep(1)  # wait for shutdown
    timeout = time.time() + TWAIT
    while len(pool) < pool_sz:
        time.sleep(0.1)
        if time.time() > timeout:
            raise TimeoutError(f"Failed to restart instance in {TWAIT} seconds")

    assert pool._names == pool_names
    assert len(pool) == pool_sz
    pool._verify_unique_ports()


@skip_if_ignore_pool
def test_simple_map(pool):
    pool_sz = len(pool)
    _ = pool.map(lambda mapdl: mapdl.prep7())
    assert len(pool) == pool_sz


@skip_if_ignore_pool
@requires("local")
@pytest.mark.skipif(True, reason="Pool tests are flaky. See #3254")
def test_map_timeout(pool):
    pool_sz = len(pool)

    def func(mapdl, tsleep):
        mapdl.clear()
        mapdl.prep7()
        time.sleep(tsleep)
        mapdl.post1()
        return tsleep

    timeout = 2
    times = np.array([0, 1, 3, 4])
    output = pool.map(func, times, timeout=timeout, wait=True)

    assert len(output) == (times < timeout).sum()

    # the timeout option kills the MAPDL instance when we reach the timeout.
    # Let's wait for the pool to heal before continuing
    timeout = time.time() + TWAIT
    while len(pool) < pool_sz:
        time.sleep(0.1)
        if time.time() > timeout:
            raise TimeoutError(f"Failed to restart instance in {TWAIT} seconds")

    assert len(pool) == pool_sz


@skip_if_ignore_pool
def test_simple(pool):
    pool_sz = len(pool)

    def func(mapdl):
        mapdl.clear()

    outs = pool.map(func)
    assert len(outs) == len(pool)
    assert len(pool) == pool_sz


# fails intermittently
@skip_if_ignore_pool
def test_batch(pool):
    input_files = [examples.vmfiles["vm%d" % i] for i in range(1, len(pool) + 3)]
    outputs = pool.run_batch(input_files)
    assert len(outputs) == len(input_files)


# fails intermittently
@skip_if_ignore_pool
def test_map(pool):
    completed_indices = []

    def func(mapdl, input_file, index):
        # input_file, index = args
        print(len(pool))
        mapdl.clear()
        output = mapdl.input(input_file)
        completed_indices.append(index)
        return mapdl.parameters.routine

    inputs = [(examples.vmfiles["vm%d" % i], i) for i in range(1, len(pool) + 1)]
    outputs = pool.map(func, inputs, wait=True)

    assert len(outputs) == len(inputs)


@skip_if_ignore_pool
@pytest.mark.skipif(
    not START_INSTANCE, reason="This test requires the pool to be local"
)
def test_abort(pool, tmpdir):
    pool_sz = len(pool)  # initial pool size

    old_paths = [mapdl.directory for mapdl in pool]

    tmp_file = str(tmpdir.join("woa.inp"))
    with open(tmp_file, "w") as f:
        f.write("EXIT")

    input_files = [examples.vmfiles["vm%d" % i] for i in range(1, 11)]
    input_files += [tmp_file]

    outputs = pool.run_batch(input_files)
    assert len(outputs) == len(input_files)

    # ensure failed instance restarts
    timeout = time.time() + TWAIT
    while len(pool) < pool_sz:
        time.sleep(0.1)
        if time.time() > timeout:
            raise TimeoutError(f"Failed to restart instance in {TWAIT} seconds")

    assert len(pool) == pool_sz

    # verify the temporary directory has been cleaned up for one of the instances
    for path in old_paths:
        path_deleted = os.path.isdir(path)
        if path_deleted:
            break

    assert path_deleted


@skip_if_ignore_pool
def test_directory_names_default(pool):
    dirs_path_pool = os.listdir(pool._root_dir)
    for i, _ in enumerate(pool._instances):
        assert pool._names(i) in dirs_path_pool
        assert f"Instance_{i}" in dirs_path_pool


@requires("local")
@skip_if_ignore_pool
def test_directory_names_custom_string(tmpdir):
    pool = MapdlPool(
        2,
        exec_file=EXEC_FILE,
        run_location=tmpdir,
        nproc=NPROC,
        names="my_instance",
        port=50056,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )

    dirs_path_pool = os.listdir(pool._root_dir)
    assert "my_instance_0" in dirs_path_pool
    assert "my_instance_1" in dirs_path_pool

    pool.exit(block=True)


@requires("local")
@skip_if_ignore_pool
def test_directory_names_function(tmpdir):
    def myfun(i):
        if i == 0:
            return "instance_zero"
        elif i == 1:
            return "instance_one"
        else:
            return "Other_instance"

    pool = MapdlPool(
        3,
        exec_file=EXEC_FILE,
        nproc=NPROC,
        names=myfun,
        run_location=tmpdir,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )

    dirs_path_pool = os.listdir(pool._root_dir)
    assert "instance_zero" in dirs_path_pool
    assert "instance_one" in dirs_path_pool
    assert "Other_instance" in dirs_path_pool

    pool.exit(block=True)


def test_num_instances():
    with pytest.raises(ValueError, match="least 1 instance"):
        pool = MapdlPool(
            0,
            exec_file=EXEC_FILE,
            nproc=NPROC,
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


@skip_if_ignore_pool
def test_only_one_instance():
    pool = MapdlPool(
        1,
        exec_file=EXEC_FILE,
        nproc=NPROC,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )
    pool_sz = len(pool)
    _ = pool.map(lambda mapdl: mapdl.prep7())
    assert len(pool) == pool_sz
    pool.exit()


def test_ip(monkeypatch):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", raising=False)
    monkeypatch.delenv("PYMAPDL_IP", raising=False)

    ips = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
    ports = [50083, 50100, 50898]
    pool_ = MapdlPool(
        3,
        ip=ips,
        port=ports,
        exec_file=EXEC_FILE,
        nproc=NPROC,
        additional_switches=QUICK_LAUNCH_SWITCHES,
        _debug_no_launch=True,
    )
    args = pool_._debug_no_launch

    assert not args["start_instance"]  # Because of ip
    assert args["ips"] == ips
    assert args["ports"] == ports


def test_next(pool):
    # Check the instances are free
    for each_instance in pool:
        assert not each_instance.locked
        assert not each_instance._busy

    with pool.next() as mapdl:
        assert isinstance(mapdl, Mapdl)
        assert mapdl.locked
        assert mapdl._busy
        mapdl.prep7()

    for each_instance in pool:
        assert not each_instance.locked
        assert not each_instance._busy


def test_next_with_returns_index(pool):
    # Check the instances are free
    for each_instance in pool:
        assert not each_instance.locked
        assert not each_instance._busy

    with pool.next(return_index=True) as (mapdl, index):
        assert isinstance(mapdl, Mapdl)
        assert isinstance(index, int)

        assert mapdl.locked
        assert mapdl._busy
        mapdl.prep7()

        assert mapdl == pool[index]

    for each_instance in pool:
        assert not each_instance.locked
        assert not each_instance._busy


def test_multiple_ips():
    ips = [
        "123.45.67.01",
        "123.45.67.02",
        "123.45.67.03",
        "123.45.67.04",
        "123.45.67.05",
    ]

    conf = MapdlPool(ip=ips, _debug_no_launch=True)._debug_no_launch

    ips = [socket.gethostbyname(each) for each in ips]

    assert conf["ips"] == ips
    assert conf["ports"] == [50052 for i in range(len(ips))]
    assert conf["start_instance"] is False
    assert conf["exec_file"] is None
    assert conf["n_instances"] == len(ips)


@pytest.mark.parametrize(
    "n_instances,ip,port,exp_n_instances,exp_ip,exp_port,context",
    [
        ## n_instances not set
        pytest.param(
            None,
            None,
            None,
            None,
            None,
            None,
            pytest.raises(
                ValueError, match="The number of instances could not be inferred "
            ),
        ),
        pytest.param(
            None,
            [],
            None,
            None,
            None,
            None,
            pytest.raises(
                ValueError, match="The number of instances could not be inferred "
            ),
        ),
        pytest.param(
            None,
            [],
            [],
            None,
            None,
            None,
            pytest.raises(
                ValueError, match="The number of instances could not be inferred "
            ),
        ),
        pytest.param(None, [], 50052, 1, [LOCALHOST], [50052], NullContext()),
        pytest.param(
            None,
            None,
            [50052, 50053],
            2,
            [LOCALHOST, LOCALHOST],
            [50052, 50053],
            NullContext(),
        ),
        pytest.param(
            None,
            None,
            set(),
            None,
            None,
            None,
            pytest.raises(TypeError, match="Argument 'port' does not support"),
        ),
        pytest.param(
            None,
            "123.0.0.1",
            [50052, 50053, 50055],
            3,
            ["123.0.0.1", "123.0.0.1", "123.0.0.1"],
            [50052, 50053, 50055],
            NullContext(),
        ),
        pytest.param(
            None,
            "123.0.0.1",
            [],
            None,
            None,
            None,
            pytest.raises(
                ValueError, match="The number of ports should be higher than"
            ),
        ),
        pytest.param(
            None,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            None,
            3,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            [50052, 50052, 50052],
            NullContext(),
        ),
        pytest.param(
            None,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            50053,
            3,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            [50053, 50053, 50053],
            NullContext(),
        ),
        pytest.param(
            None,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            [50052, 50053],
            None,
            None,
            None,
            pytest.raises(ValueError, match="should be the same as the number of IPs"),
        ),
        pytest.param(
            None,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            [50052, 50053, 50053],
            3,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3"],
            [50052, 50053, 50053],
            NullContext(),
        ),
        pytest.param(
            None,
            set(),
            None,
            None,
            None,
            None,
            pytest.raises(TypeError, match="Argument 'ip' does not support"),
        ),
        ## n_instances set
        # ip is none
        pytest.param(
            {},
            None,
            None,
            None,
            None,
            None,
            pytest.raises(
                TypeError, match="Only integers are allowed for 'n_instances'"
            ),
        ),
        pytest.param(
            0,
            None,
            None,
            None,
            None,
            None,
            pytest.raises(
                ValueError, match="Must request at least 1 instance to create"
            ),
        ),
        pytest.param(
            2,
            None,
            None,
            2,
            [LOCALHOST, LOCALHOST],
            [MAPDL_DEFAULT_PORT, MAPDL_DEFAULT_PORT + 1],
            NullContext(),
        ),
        pytest.param(
            3,
            None,
            None,
            3,
            [LOCALHOST, LOCALHOST, LOCALHOST],
            [MAPDL_DEFAULT_PORT, MAPDL_DEFAULT_PORT + 1, MAPDL_DEFAULT_PORT + 2],
            NullContext(),
        ),
        pytest.param(
            3,
            None,
            50053,
            3,
            [LOCALHOST, LOCALHOST, LOCALHOST],
            [50053, 50053 + 1, 50053 + 2],
            NullContext(),
        ),
        pytest.param(
            3,
            None,
            [50052, 50053],
            None,
            None,
            None,
            pytest.raises(
                ValueError,
                match="If using 'n_instances' and 'port' without multiple 'ip'",
            ),
        ),
        pytest.param(
            3,
            None,
            [50052, 50053, 50054],
            3,
            [LOCALHOST, LOCALHOST, LOCALHOST],
            [50052, 50053, 50054],
            NullContext(),
        ),
        pytest.param(
            3,
            None,
            set(),
            None,
            None,
            None,
            pytest.raises(
                TypeError,
                match="Argument 'port' does not support this type of argument",
            ),
        ),
        # ip is string
        pytest.param(
            3,
            "123.0.0.1",
            None,
            None,
            None,
            None,
            pytest.raises(ValueError, match="If using 'n_instances' and only one 'ip'"),
        ),
        pytest.param(
            3,
            "123.0.0.1",
            50053,
            None,
            None,
            None,
            pytest.raises(ValueError, match="If using 'n_instances' and only one 'ip'"),
        ),
        pytest.param(
            3,
            "123.0.0.1",
            [50053, 50052],
            None,
            None,
            None,
            pytest.raises(ValueError, match="If using 'n_instances' and only one 'ip'"),
        ),
        pytest.param(
            3,
            "123.0.0.1",
            [50053, 50052, 50054],
            3,
            ["123.0.0.1", "123.0.0.1", "123.0.0.1"],
            [50053, 50052, 50054],
            NullContext(),
        ),
        # ip is list
        pytest.param(
            3,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            None,
            None,
            None,
            None,
            pytest.raises(
                ValueError, match="should be the same as the number of instances"
            ),
        ),
        pytest.param(
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            None,
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            [
                MAPDL_DEFAULT_PORT,
                MAPDL_DEFAULT_PORT,
                MAPDL_DEFAULT_PORT,
                MAPDL_DEFAULT_PORT,
            ],
            NullContext(),
        ),
        pytest.param(
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            50053,
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            [50053, 50053, 50053, 50053],
            NullContext(),
        ),
        pytest.param(
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            [50053, 50054],
            None,
            None,
            None,
            pytest.raises(
                ValueError,
                match="you should provide as many ports as number of instances",
            ),
        ),
        pytest.param(
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            [50055] * 4,
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            [50055] * 4,
            NullContext(),
        ),
        pytest.param(
            4,
            ["123.0.0.1", "123.0.0.2", "123.0.0.3", "123.0.0.4"],
            set(),
            None,
            None,
            None,
            pytest.raises(
                TypeError, match="Argument 'port' does not support this type of"
            ),
        ),
        # ip type is not allowed
        pytest.param(
            4,
            set(),
            None,
            None,
            None,
            None,
            pytest.raises(
                TypeError, match="Argument 'ip' does not support this type of"
            ),
        ),
    ],
)
def test_ip_port_n_instance(
    monkeypatch, n_instances, ip, port, exp_n_instances, exp_ip, exp_port, context
):
    monkeypatch.delenv("PYMAPDL_START_INSTANCE", raising=False)
    monkeypatch.delenv("PYMAPDL_IP", raising=False)
    monkeypatch.setenv(
        "PYMAPDL_MAPDL_EXEC", "/ansys_inc/v222/ansys/bin/ansys222"
    )  # to avoid trying to find it.

    with context:
        conf = MapdlPool(
            n_instances=n_instances, ip=ip, port=port, _debug_no_launch=True
        )._debug_no_launch

        if exp_ip:
            exp_ip = [socket.gethostbyname(each) for each in exp_ip]

        assert conf["n_instances"] == exp_n_instances
        assert len(conf["ips"]) == exp_n_instances
        assert len(conf["ports"]) == exp_n_instances
        assert conf["ips"] == exp_ip
        assert conf["ports"] == exp_port
        assert conf["exec_file"] == "/ansys_inc/v222/ansys/bin/ansys222"
