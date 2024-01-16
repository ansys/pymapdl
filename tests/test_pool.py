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
import time

import numpy as np
import pytest

from conftest import ON_STUDENT, has_dependency

if has_dependency("ansys-tools-path"):
    from ansys.tools.path import find_ansys

    EXEC_FILE = find_ansys()[0]

else:
    EXEC_FILE = os.environ.get("PYMAPDL_MAPDL_EXEC")

if not EXEC_FILE:
    pytest.skip(allow_module_level=True)

from ansys.mapdl.core import LocalMapdlPool, examples
from ansys.mapdl.core.errors import VersionError
from conftest import QUICK_LAUNCH_SWITCHES, requires

# skip entire module unless HAS_GRPC
pytestmark = requires("grpc")


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

if ON_STUDENT:
    MAPDL_INSTANCES = 1
else:
    MAPDL_INSTANCES = 4


@pytest.fixture(scope="module")
def pool(tmpdir_factory):
    run_path = str(tmpdir_factory.mktemp("ansys_pool"))

    mapdl_pool = LocalMapdlPool(
        MAPDL_INSTANCES,
        license_server_check=False,
        run_location=run_path,
        port=50056,
        start_timeout=30,
        exec_file=EXEC_FILE,
        additional_switches=QUICK_LAUNCH_SWITCHES,
        nproc=NPROC,
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
        LocalMapdlPool(
            MAPDL_INSTANCES,
            nproc=NPROC,
            exec_file="/usr/ansys_inc/v194/ansys/bin/mapdl",
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


# @pytest.mark.xfail(strict=False, reason="Flaky test. See #2435")
@requires("local")
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


@requires("local")
@skip_if_ignore_pool
def test_simple_map(pool):
    pool_sz = len(pool)
    _ = pool.map(lambda mapdl: mapdl.prep7())
    assert len(pool) == pool_sz


@requires("local")
@skip_if_ignore_pool
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


@requires("local")
@skip_if_ignore_pool
def test_simple(pool):
    pool_sz = len(pool)

    def func(mapdl):
        mapdl.clear()

    outs = pool.map(func)
    assert len(outs) == len(pool)
    assert len(pool) == pool_sz


# fails intermittently
@requires("local")
@skip_if_ignore_pool
def test_batch(pool):
    input_files = [examples.vmfiles["vm%d" % i] for i in range(1, 11)]
    outputs = pool.run_batch(input_files)
    assert len(outputs) == len(input_files)


# fails intermittently
@requires("local")
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

    inputs = [(examples.vmfiles["vm%d" % i], i) for i in range(1, 11)]
    outputs = pool.map(func, inputs, wait=True)

    assert len(outputs) == len(inputs)


@requires("local")
@skip_if_ignore_pool
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


@requires("local")
@skip_if_ignore_pool
def test_directory_names_default(pool):
    dirs_path_pool = os.listdir(pool._root_dir)
    assert "Instance_0" in dirs_path_pool
    assert "Instance_1" in dirs_path_pool
    assert "Instance_2" in dirs_path_pool
    assert "Instance_3" in dirs_path_pool


@requires("local")
@skip_if_ignore_pool
def test_directory_names_custom_string(tmpdir):
    pool = LocalMapdlPool(
        min([2, MAPDL_INSTANCES]),  # to not spawn more than necessary
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
    instances_names = [
        "instance_zero",
        "instance_one",
        "Other_instance",
        "Other_instance",
        "Other_instance",
    ]

    def myfun(i):
        return instances_names[i]

    mapdl_instances = min([3, MAPDL_INSTANCES])
    pool = LocalMapdlPool(
        mapdl_instances,  # to not spawn more than necessary
        exec_file=EXEC_FILE,
        nproc=NPROC,
        names=myfun,
        run_location=tmpdir,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )

    dirs_path_pool = os.listdir(pool._root_dir)
    for each in zip(range(mapdl_instances), instances_names):
        each in dirs_path_pool

    pool.exit(block=True)


def test_num_instances():
    with pytest.raises(ValueError, match="least 1 instance"):
        pool = LocalMapdlPool(
            0,
            exec_file=EXEC_FILE,
            nproc=NPROC,
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


@requires("local")
@skip_if_ignore_pool
def test_only_one_instance():
    pool = LocalMapdlPool(
        1,
        exec_file=EXEC_FILE,
        nproc=NPROC,
        additional_switches=QUICK_LAUNCH_SWITCHES,
    )
    pool_sz = len(pool)
    _ = pool.map(lambda mapdl: mapdl.prep7())
    assert len(pool) == pool_sz
    pool.exit()
