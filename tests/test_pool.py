import os
from pathlib import Path
import time

from ansys.tools.path import find_ansys
import numpy as np
import pytest

from ansys.mapdl.core import LocalMapdlPool, examples
from ansys.mapdl.core.errors import VersionError
from conftest import QUICK_LAUNCH_SWITCHES, skip_if_not_local

# skip entire module unless HAS_GRPC
pytestmark = pytest.mark.skip_grpc


skip_if_ignore_pool = pytest.mark.skipif(
    os.environ.get("IGNORE_POOL", "").upper() == "TRUE",
    reason="Ignoring Pool tests.",
)


MAPDL194PATH = "/usr/ansys_inc/v194/ansys/bin/mapdl"
skip_requires_194 = pytest.mark.skipif(
    not os.path.isfile(MAPDL194PATH), reason="Requires MAPDL 194"
)

TWAIT = 90
NPROC = 1


@pytest.fixture(scope="module")
def pool(tmpdir_factory):
    EXEC_FILE = find_ansys()[0]
    run_path = str(tmpdir_factory.mktemp("ansys_pool"))

    mapdl_pool = LocalMapdlPool(
        4,
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
            raise TimeoutError(f"Failed to restart instance in {TWAIT} seconds")

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
            4,
            nproc=NPROC,
            exec_file="/usr/ansys_inc/v194/ansys/bin/mapdl",
            additional_switches=QUICK_LAUNCH_SWITCHES,
        )


@skip_if_not_local
def test_heal(pool):
    pool_sz = len(pool)
    pool[0].exit()
    pool[1].exit()
    pool[2].exit()

    time.sleep(1)  # wait for shutdown
    timeout = time.time() + TWAIT
    while len(pool) < pool_sz:
        time.sleep(0.1)
        if time.time() > timeout:
            raise TimeoutError(f"Failed to restart instance in {TWAIT} seconds")

    assert len(pool) == pool_sz
    pool._verify_unique_ports()


@skip_if_not_local
@skip_if_ignore_pool
def test_simple_map(pool):
    pool_sz = len(pool)
    _ = pool.map(lambda mapdl: mapdl.prep7())
    assert len(pool) == pool_sz


@skip_if_not_local
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
    output = pool.map(func, times, timeout=timeout)
    assert len(output) == (times < timeout).sum()

    # wait for the pool to heal before continuing
    timeout = time.time() + TWAIT
    while len(pool) < pool_sz:
        time.sleep(0.1)
        if time.time() > timeout:
            raise TimeoutError(f"Failed to restart instance in {TWAIT} seconds")

    assert len(pool) == pool_sz


@skip_if_not_local
@skip_if_ignore_pool
def test_simple(pool):
    pool_sz = len(pool)

    def func(mapdl):
        mapdl.clear()

    outs = pool.map(func)
    assert len(outs) == len(pool)
    assert len(pool) == pool_sz


# fails intermittently
@skip_if_not_local
@skip_if_ignore_pool
def test_batch(pool):
    input_files = [examples.vmfiles["vm%d" % i] for i in range(1, 11)]
    outputs = pool.run_batch(input_files)
    assert len(outputs) == len(input_files)


# fails intermittently
@skip_if_not_local
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
    outputs = pool.map(func, inputs, progress_bar=True, wait=True)

    assert len(outputs) == len(inputs)


@skip_if_not_local
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


@skip_if_not_local
@skip_if_ignore_pool
def test_directory_names_default(pool):
    dirs_path_pool = os.listdir(pool._root_dir)
    assert "Instance_0" in dirs_path_pool
    assert "Instance_1" in dirs_path_pool
    assert "Instance_2" in dirs_path_pool
    assert "Instance_3" in dirs_path_pool


@skip_if_not_local
@skip_if_ignore_pool
def test_directory_names_custom_string(tmpdir):
    pool = LocalMapdlPool(
        2,
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


@skip_if_not_local
@skip_if_ignore_pool
def test_directory_names_function(tmpdir):
    def myfun(i):
        if i == 0:
            return "instance_zero"
        elif i == 1:
            return "instance_one"
        else:
            return "Other_instance"

    pool = LocalMapdlPool(
        3,
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
