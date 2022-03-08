"""gRPC service specific tests"""
import os
import re

import pytest

from ansys.mapdl.core import examples, launch_mapdl
from ansys.mapdl.core.common_grpc import DEFAULT_CHUNKSIZE
from ansys.mapdl.core.launcher import check_valid_ansys, get_start_instance

PATH = os.path.dirname(os.path.abspath(__file__))

# skip entire module unless HAS_GRPC installed or connecting to server
pytestmark = pytest.mark.skip_grpc

skip_launch_mapdl = pytest.mark.skipif(
    not get_start_instance() and check_valid_ansys(),
    reason="Must be able to launch MAPDL locally",
)


skip_in_cloud = pytest.mark.skipif(
    not get_start_instance(),
    reason="""
Must be able to launch MAPDL locally. Remote execution does not allow for
directory creation.
""",
)


def write_tmp(mapdl, filename, ext="txt"):
    """Write a temporary file from MAPDL."""
    with mapdl.non_interactive:
        mapdl.cfopen(filename, "txt")
        mapdl.vwrite("dummy_file")  # Needs to write something, File cannot be empty.
        mapdl.run("(A10)")
        mapdl.cfclos()


@pytest.fixture(scope="function")
def setup_for_cmatrix(mapdl, cleared):
    mapdl.prep7()
    mapdl.title("Capacitance of two long cylinders above a ground plane")
    mapdl.run("a=100")  # Cylinder inside radius (μm)
    mapdl.run("d=400")  # Outer radius of air region
    mapdl.run("ro=800")  # Outer radius of infinite elements
    mapdl.et(1, 121)  # 8-node 2-D electrostatic element
    mapdl.et(2, 110, 1, 1)  # 8-node 2-D Infinite element
    mapdl.emunit("epzro", 8.854e-6)  # Set free-space permittivity for μMKSV units
    mapdl.mp("perx", 1, 1)
    mapdl.cyl4("d/2", "d/2", "a", 0)  # Create mode in first quadrant
    mapdl.cyl4(0, 0, "ro", 0, "", 90)
    mapdl.cyl4(0, 0, "2*ro", 0, "", 90)
    mapdl.aovlap("all")
    mapdl.numcmp("area")
    mapdl.run("smrtsiz,4")
    mapdl.mshape(1)  # Mesh air region
    mapdl.amesh(3)
    mapdl.lsel("s", "loc", "x", "1.5*ro")
    mapdl.lsel("a", "loc", "y", "1.5*ro")
    mapdl.lesize("all", "", "", 1)
    mapdl.type(2)
    mapdl.mshape(0)
    mapdl.mshkey(1)
    mapdl.amesh(2)  # Mesh infinite region
    mapdl.run("arsymm,x,all")  # Reflect model about y axis
    mapdl.nummrg("node")
    mapdl.nummrg("kpoi")
    mapdl.csys(1)
    mapdl.nsel("s", "loc", "x", "2*ro")
    mapdl.sf("all", "inf")  # Set infinite flag in Infinite elements
    mapdl.local(11, 1, "d/2", "d/2")
    mapdl.nsel("s", "loc", "x", "a")
    mapdl.cm("cond1", "node")  # Assign node component to 1st conductor
    mapdl.local(12, 1, "-d/2", "d/2")
    mapdl.nsel("s", "loc", "x", "a")
    mapdl.cm("cond2", "node")  # Assign node component to 2nd conductor
    mapdl.csys(0)
    mapdl.nsel("s", "loc", "y", 0)
    mapdl.cm("cond3", "node")  # Assign node component to ground conductor
    mapdl.allsel("all")
    mapdl.finish()
    mapdl.run("/solu")


def test_clear_nostart(mapdl):
    resp = mapdl._send_command("FINISH")
    resp = mapdl._send_command("/CLEAR, NOSTART")
    assert "CLEAR ANSYS DATABASE AND RESTART" in resp


# NOTE: This command cannot be run repeately, otherwise we end up with
# to many levels of /INPUT.  2021R2 should have a fix for this
def test_clear(mapdl):
    resp = mapdl._send_command("FINISH")
    resp = mapdl._send_command("/CLEAR")
    assert "CLEAR" in resp


def test_clear_multiple(mapdl):
    # simply should not fail.  See:
    # https://github.com/pyansys/pymapdl/issues/380
    for i in range(20):
        mapdl.run("/CLEAR")


def test_invalid_get(mapdl):
    with pytest.raises(ValueError):
        mapdl.get_value("ACTIVE", item1="SET", it1num="invalid")


def test_stream(mapdl):
    resp = mapdl._send_command_stream("/PREP7")
    assert "PREP7" in resp


def test_basic_input_output(mapdl, tmpdir):
    mapdl.finish()
    mapdl.clear("NOSTART")
    filename = "tmp2.inp"
    basic_inp = tmpdir.join(filename)
    with open(basic_inp, "w") as f:
        f.write("FINISH\n")
        f.write("/PREP7\n")

    mapdl.upload(basic_inp)
    tmpfile = "tmp.out"
    mapdl._send_command("/OUT, %s" % tmpfile, mute=True)
    mapdl._send_command("/INPUT, %s" % filename, mute=True)
    mapdl._send_command("/OUT, TERM", mute=True)
    mapdl.download(tmpfile)
    assert os.path.isfile(tmpfile)
    # input file won't actually run, but we want to see if the output switches


def test_upload_large(mapdl):
    mapdl.finish()
    mapdl.clear("NOSTART")

    file_name = examples.vmfiles["vm153"]
    test_file = os.path.join(PATH, "test_files", file_name)

    mapdl.upload(test_file)
    assert os.path.basename(file_name) in mapdl.list_files()


def test_upload_fail(mapdl):
    with pytest.raises(FileNotFoundError):
        mapdl.upload("thisisnotafile")


def test_input_empty(mapdl):
    resp = mapdl._send_command("/INPUT")
    assert "INPUT FILE" in resp


def test_input_empty(mapdl):
    resp = mapdl._send_command("/INPUT, not_a_file")
    assert "does not exist" in resp


def test_large_output(mapdl, cleared):
    """Verify we can receive messages over the default 4MB limit."""
    mapdl.block(0, 1, 0, 1, 0, 1)
    mapdl.et(1, 187)
    mapdl.esize(0.05)
    mapdl.vmesh("all")
    msg = mapdl.nlist()
    assert len(msg) > 4 * 1024**2


def test__download_missing_file(mapdl, tmpdir):
    target = tmpdir.join("tmp")
    with pytest.raises(FileNotFoundError):
        mapdl._download("__notafile__", target)


@skip_launch_mapdl  # need to be able to start/stop an instance of MAPDL
def test_grpc_custom_ip():
    ip = "127.0.0.2"
    mapdl = launch_mapdl(ip=ip)
    assert mapdl._ip == ip


def test_cmatrix(mapdl, setup_for_cmatrix):
    cap_name = "aaaaa"
    output = mapdl.cmatrix(1, "cond", 3, 0, cap_name)
    assert "Capacitance matricies are stored in file" in output
    assert cap_name in output

    # also test if it works while we're already in non-interactive:
    # no asserts needed here since we're not concerned about the last response
    cap_name = "bbbbb"
    with mapdl.non_interactive:
        mapdl.cmatrix(1, "cond", 3, 0, cap_name)

    # we have to manually get the response here.  This is ok because
    # user is not expected to do this.
    output = mapdl._download_as_raw("cmatrix.out").decode()
    assert "Capacitance matricies are stored in file" in output
    assert cap_name in output


# these tests take some time to run, and we might consider moving
# these to a functional testing module/directory outside of the tests
# directory.


def test_read_input_file_verbose(mapdl):
    test_file = examples.vmfiles["vm153"]
    mapdl.finish()
    mapdl.clear()
    response = mapdl.input(test_file, verbose=True)
    assert re.search("\*\*\*\*\*  (ANSYS|MAPDL) SOLUTION ROUTINE  \*\*\*\*\*", response)


test_files = ["full26.dat", "static.dat"]


@pytest.mark.parametrize("file_name", test_files)
def test_read_input_file(mapdl, file_name):
    test_file = os.path.join(PATH, "test_files", file_name)
    mapdl.finish()
    mapdl.clear()
    response = mapdl.input(test_file)
    assert re.search("\*\*\*\*\*  (ANSYS|MAPDL) SOLUTION ROUTINE  \*\*\*\*\*", response)


def test_no_get_value_non_interactive(mapdl):
    with pytest.raises(RuntimeError, match="Cannot use gRPC enabled ``GET``"):
        with mapdl.non_interactive:
            mapdl.get_value("ACTIVE", item1="CSYS")


def test__download(mapdl, tmpdir):
    # Creating temp file
    write_tmp(mapdl, "myfile0")

    file_name = "myfile0.txt"
    assert file_name in mapdl.list_files()

    out_file = tmpdir.join("out_" + file_name)
    mapdl._download(file_name, out_file_name=out_file)
    assert out_file.exists()

    out_file = tmpdir.join("out1_" + file_name)
    mapdl._download(file_name, out_file_name=out_file, progress_bar=True)
    assert out_file.exists()

    out_file = tmpdir.join("out2_" + file_name)
    mapdl._download(file_name, out_file_name=out_file, chunk_size=DEFAULT_CHUNKSIZE / 2)
    assert out_file.exists()

    out_file = tmpdir.join("out3_" + file_name)
    mapdl._download(file_name, out_file_name=out_file, chunk_size=DEFAULT_CHUNKSIZE * 2)
    assert out_file.exists()


@pytest.mark.parametrize(
    "option,expected_files",
    [
        ["myfile0.txt", ["myfile0.txt"]],
        [["myfile0.txt", "myfile1.txt"], ["myfile0.txt", "myfile1.txt"]],
        ["myfile*", ["myfile0.txt", "myfile1.txt"]],
    ],
)
def test_download(mapdl, tmpdir, option, expected_files):
    write_tmp(mapdl, "myfile0")
    write_tmp(mapdl, "myfile1")

    mapdl.download(option, target_dir=tmpdir)
    for file_to_check in expected_files:
        assert os.path.exists(tmpdir.join(file_to_check))


def test_download_without_target_dir(mapdl, tmpdir):
    write_tmp(mapdl, "myfile0")
    write_tmp(mapdl, "myfile1")

    old_cwd = os.getcwd()
    try:
        # must use try/finally block as we change the cwd here
        os.chdir(str(tmpdir))

        mapdl.download("myfile0.txt")
        assert os.path.exists("myfile0.txt")

        mapdl.download(["myfile0.txt", "myfile1.txt"])
        assert os.path.exists("myfile0.txt")
        assert os.path.exists("myfile1.txt")

        mapdl.download("myfile*")
        assert os.path.exists("myfile0.txt")
        assert os.path.exists("myfile1.txt")
    finally:
        os.chdir(old_cwd)


@skip_in_cloud  # This is going to run only in local
def test_download_recursive(mapdl, tmpdir):
    if mapdl._local:  # mapdl._local = True
        dir_ = tmpdir.mkdir("temp00")
        file1 = dir_.join("file0.txt")
        file2 = dir_.join("file1.txt")
        with open(file1, "w") as fid:
            fid.write("dummy")
        with open(file2, "w") as fid:
            fid.write("dummy")

        mapdl.download(
            os.path.join(dir_, "*"), recursive=True
        )  # This is referenced to os.getcwd
        assert os.path.exists("file0.txt")
        assert os.path.exists("file1.txt")
        os.remove("file0.txt")
        os.remove("file1.txt")

        mapdl.download(os.path.join(dir_, "*"), target_dir="new_dir", recursive=True)
        assert os.path.exists(os.path.join("new_dir", "file0.txt"))
        assert os.path.exists(os.path.join("new_dir", "file1.txt"))
        os.remove(os.path.join("new_dir", "file0.txt"))
        os.remove(os.path.join("new_dir", "file1.txt"))


def test_download_project(mapdl, tmpdir):
    target_dir = tmpdir.mkdir("tmp")
    mapdl.download_project(target_dir=target_dir)
    files_extensions = [each.split(".")[-1] for each in os.listdir(target_dir)]

    assert "log" in files_extensions
    assert "out" in files_extensions
    assert "err" in files_extensions
    assert "lock" in files_extensions


def test_download_project_extensions(mapdl, tmpdir):
    target_dir = tmpdir.mkdir("tmp")
    mapdl.download_project(extensions=["log", "out"], target_dir=target_dir)
    files_extensions = [each.split(".")[-1] for each in os.listdir(target_dir)]

    assert "log" in files_extensions
    assert "out" in files_extensions
    assert "err" not in files_extensions
    assert "lock" not in files_extensions
