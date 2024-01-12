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

"""gRPC service specific tests"""
import os
import re
import shutil

import pytest

from ansys.mapdl.core import examples
from ansys.mapdl.core.common_grpc import DEFAULT_CHUNKSIZE
from ansys.mapdl.core.errors import (
    MapdlCommandIgnoredError,
    MapdlExitedError,
    MapdlRuntimeError,
)
from ansys.mapdl.core.misc import random_string

PATH = os.path.dirname(os.path.abspath(__file__))

from conftest import has_dependency, requires

# skip entire module unless HAS_GRPC installed or connecting to server
pytestmark = requires("grpc")


def write_tmp_in_mapdl_instance(mapdl, filename, ext="txt"):
    """Write a temporary file from MAPDL."""
    with mapdl.non_interactive:
        mapdl.cfopen(filename, ext)
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


def test_connect_via_channel(mapdl):
    """Validate MapdlGrpc can be created directly from a channel."""

    import grpc

    from ansys.mapdl.core.mapdl_grpc import MAX_MESSAGE_LENGTH, MapdlGrpc

    channel = grpc.insecure_channel(
        mapdl._channel_str,
        options=[
            ("grpc.max_receive_message_length", MAX_MESSAGE_LENGTH),
        ],
    )
    mapdl = MapdlGrpc(channel=channel)
    assert mapdl.is_alive


def test_clear_nostart(mapdl):
    resp = mapdl._send_command("FINISH")
    resp = mapdl._send_command("/CLEAR, NOSTART")
    assert re.search("CLEAR (ANSYS|MAPDL) DATABASE AND RESTART", resp)


# NOTE: This command cannot be run repeately, otherwise we end up with
# to many levels of /INPUT.  2021R2 should have a fix for this
def test_clear(mapdl):
    resp = mapdl._send_command("FINISH")
    resp = mapdl._send_command("/CLEAR")
    assert "CLEAR" in resp


def test_clear_multiple(mapdl):
    # simply should not fail.  See:
    # https://github.com/ansys/pymapdl/issues/380
    for i in range(20):
        mapdl.run("/CLEAR")


@pytest.mark.xfail(
    reason="MAPDL bug 867421", raises=(MapdlExitedError, UnicodeDecodeError)
)
def test_invalid_get_bug(mapdl):
    with pytest.raises((MapdlRuntimeError, MapdlCommandIgnoredError)):
        mapdl.get_value("ACTIVE", item1="SET", it1num="invalid")


def test_invalid_get(mapdl):
    with pytest.raises((MapdlRuntimeError, MapdlCommandIgnoredError)):
        mapdl.get_value("ACTIVE")


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
    os.remove(tmpfile)
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
        mapdl.download("__notafile__", target)


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


@pytest.mark.parametrize("file_name", ["full26.dat", "static.dat"])
def test_read_input_file(mapdl, file_name):
    test_file = os.path.join(PATH, "test_files", file_name)
    mapdl.finish()
    mapdl.clear()
    response = mapdl.input(test_file)

    assert (
        re.search("\*\*\*\*\*  (ANSYS|MAPDL) SOLUTION ROUTINE  \*\*\*\*\*", response)
        or "PyMAPDL: Simulation Finished." in response
    )


def test_no_get_value_non_interactive(mapdl):
    with pytest.raises((MapdlRuntimeError, MapdlCommandIgnoredError)):
        with mapdl.non_interactive:
            mapdl.get_value("ACTIVE", item1="CSYS")


def test__download(mapdl, tmpdir):
    # Creating temp file
    write_tmp_in_mapdl_instance(mapdl, "myfile0")

    file_name = "myfile0.txt"
    assert file_name in mapdl.list_files()

    out_file = tmpdir.join("out_" + file_name)
    mapdl._download(file_name, out_file_name=out_file)
    assert out_file.exists()

    out_file = tmpdir.join("out1_" + file_name)
    if has_dependency("tqdm"):
        mapdl._download(file_name, out_file_name=out_file, progress_bar=True)
    else:
        mapdl._download(file_name, out_file_name=out_file)
    assert out_file.exists()

    out_file = tmpdir.join("out2_" + file_name)
    mapdl._download(file_name, out_file_name=out_file, chunk_size=DEFAULT_CHUNKSIZE / 2)
    assert out_file.exists()

    out_file = tmpdir.join("out3_" + file_name)
    mapdl._download(file_name, out_file_name=out_file, chunk_size=DEFAULT_CHUNKSIZE * 2)
    assert out_file.exists()


@pytest.mark.parametrize(
    "files_to_download,expected_output",
    [
        ["myfile0.txt", ["myfile0.txt"]],
        [["myfile0.txt", "myfile1.txt"], ["myfile0.txt", "myfile1.txt"]],
        ["myfile*", ["myfile0.txt", "myfile1.txt"]],
    ],
)
def test_download(mapdl, tmpdir, files_to_download, expected_output):
    write_tmp_in_mapdl_instance(mapdl, "myfile0")
    write_tmp_in_mapdl_instance(mapdl, "myfile1")

    list_files = mapdl.download(files_to_download, target_dir=tmpdir)
    assert len(expected_output) == len(list_files)

    for file_to_check in list_files:
        basename = os.path.basename(file_to_check)
        file_ = os.path.join(tmpdir, basename)
        assert basename in expected_output
        assert os.path.exists(file_)
        os.remove(file_)


@pytest.mark.parametrize(
    "files_to_download,expected_output",
    [
        ["myfile0.txt", ["myfile0.txt"]],
        [["myfile0.txt", "myfile1.txt"], ["myfile0.txt", "myfile1.txt"]],
        ["myfile*", ["myfile0.txt", "myfile1.txt"]],
    ],
)
def test_download_without_target_dir(mapdl, files_to_download, expected_output):
    write_tmp_in_mapdl_instance(mapdl, "myfile0")
    write_tmp_in_mapdl_instance(mapdl, "myfile1")

    list_files = mapdl.download(files_to_download)
    assert len(expected_output) == len(list_files)

    for file_to_check in list_files:
        basename = os.path.basename(file_to_check)
        file_ = os.path.join(os.getcwd(), basename)
        assert basename in expected_output
        assert os.path.exists(file_)
        os.remove(file_)


@pytest.mark.parametrize(
    "extension_to_download,files_to_download,expected_output",
    [
        ["txt", "myfile*", ["myfile0.txt", "myfile1.txt"]],
        ["txt", "myfile0", ["myfile0.txt"]],
        [None, "file*.err", None],
        ["err", "*", None],
    ],
)
def test_download_with_extension(
    mapdl, extension_to_download, files_to_download, expected_output
):
    write_tmp_in_mapdl_instance(mapdl, "myfile0")
    write_tmp_in_mapdl_instance(mapdl, "myfile1")

    list_files = mapdl.download(files_to_download, extension=extension_to_download)

    if extension_to_download == "err" or files_to_download.endswith("err"):
        remote_list_files = mapdl.list_files()

        assert all(
            [
                each.endswith("err") and os.path.basename(each) in remote_list_files
                for each in list_files
            ]
        )
    else:
        assert len(expected_output) == len(list_files)

        for file_to_check in list_files:
            basename = os.path.basename(file_to_check)
            assert basename in expected_output
            assert os.path.exists(os.path.join(os.getcwd(), basename))
            assert os.path.exists(file_to_check)

    for file in list_files:
        os.remove(file)


@requires("local")
def test_download_recursive(mapdl):
    if mapdl._local:
        temp_dir = os.path.join(mapdl.directory, "new_folder")
        os.makedirs(temp_dir, exist_ok=True)
        with open(os.path.join(temp_dir, "file0.txt"), "a") as fid:
            fid.write("dummy")
        with open(os.path.join(temp_dir, "file1.txt"), "a") as fid:
            fid.write("dummy")

        mapdl.download(temp_dir, recursive=True)  # This is referenced to os.getcwd
        assert os.path.exists("file0.txt")
        assert os.path.exists("file1.txt")
        os.remove("file0.txt")
        os.remove("file1.txt")

        mapdl.download("**", target_dir="new_dir", recursive=True)
        assert os.path.exists(os.path.join("new_dir", "file0.txt"))
        assert os.path.exists(os.path.join("new_dir", "file1.txt"))
        shutil.rmtree(temp_dir)
        shutil.rmtree("new_dir")


def test_download_project(mapdl, tmpdir):
    target_dir = tmpdir.mkdir("tmp")
    mapdl.download_project(target_dir=target_dir)
    files_extensions = list(
        set([each.split(".")[-1] for each in os.listdir(target_dir)])
    )
    assert "log" in files_extensions


def test_download_project_extensions(mapdl, tmpdir):
    target_dir = tmpdir.mkdir("tmp")
    mapdl.download_project(extensions=["log", "err"], target_dir=target_dir)
    files_extensions = set([each.split(".")[-1] for each in os.listdir(target_dir)])

    expected = {"log", "out", "err", "lock"}
    assert expected.intersection(files_extensions) == {"log", "err"}


def test_download_result(mapdl, cleared, tmpdir):
    if "file.rst" not in mapdl.list_files():
        write_tmp_in_mapdl_instance(mapdl, "file", ext="rst")  # fake rst file
    target_dir = tmpdir.mkdir(f"tmp_{random_string()}")
    mapdl.download_result(target_dir)
    assert os.path.exists(os.path.join(target_dir, "file.rst"))

    assert not os.path.exists("file.rst")
    mapdl.download_result(preference="rst")  # with default argument
    assert os.path.exists("file.rst")

    os.remove("file.rst")

    mapdl.download_result(preference="rth")
    try:
        os.remove("file.rst")
    except Exception:
        pass
    try:
        os.remove("file.rth")
    except Exception:
        pass


def test__channel_str(mapdl):
    assert mapdl._channel_str is not None
    assert ":" in mapdl._channel_str
    assert re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", mapdl._channel_str)
    assert re.search("\d{4,6}", mapdl._channel_str)


def test_mode(mapdl):
    assert mapdl.connection == "grpc"
    assert mapdl.is_grpc
    assert not mapdl.is_corba
    assert not mapdl.is_console


def test_input_output(mapdl):
    file_ = "myinput.inp"
    with open(file_, "w") as fid:
        for i in range(4):
            fid.write(f"/com, line {i}\n")

    output = mapdl.input(file_)
    assert "/INPUT FILE" in output
    assert "line 0" in output
    assert "line 3" in output

    os.remove(file_)


def test_input_ext_argument(mapdl):
    file_ = "myinput.inp"
    with open(file_, "w") as fid:
        for i in range(4):
            fid.write(f"/com, line {i}\n")

    output = mapdl.input("myinput", "inp")
    assert "/INPUT FILE" in output
    assert "line 0" in output
    assert "line 1" in output
    assert "line 2" in output
    assert "line 3" in output

    os.remove(file_)


def test_input_dir_argument(mapdl, tmpdir):
    file_ = "myinput.inp"
    target_dir = str(tmpdir.mkdir(f"tmp_{random_string()}"))
    file_path = os.path.join(target_dir, file_)
    with open(file_path, "w") as fid:
        for i in range(4):
            fid.write(f"/com, line {i}\n")

    output = mapdl.input(file_, "", target_dir)
    assert "/INPUT FILE" in output
    assert "line 0" in output
    assert "line 1" in output
    assert "line 2" in output
    assert "line 3" in output

    os.remove(file_path)


def test_input_line_argument(mapdl):
    file_ = "myinput.inp"
    with open(file_, "w") as fid:
        for i in range(4):
            fid.write(f"/com, line {i}\n")

    output = mapdl.input(file_, line=2)
    assert "/INPUT FILE" in output
    assert "line 0" not in output
    assert "line 1" not in output
    assert "line 2" in output
    assert "line 3" in output

    os.remove(file_)


def test_input_multiple_argument(mapdl, tmpdir):
    file_ = "myinput.inp"
    target_dir = str(tmpdir.mkdir(f"tmp_{random_string()}"))
    file_path = os.path.join(target_dir, file_)
    with open(file_path, "w") as fid:
        for i in range(4):
            fid.write(f"/com, line {i}\n")

    output = mapdl.input("myinput", "inp", target_dir, 2)
    assert "/INPUT FILE" in output
    assert "line 0" not in output
    assert "line 1" not in output
    assert "line 2" in output
    assert "line 3" in output

    os.remove(file_path)


def test_input_log_argument(mapdl):
    with pytest.raises(ValueError, match="'log' argument is not supported"):
        mapdl.input(log="asdf")


def test_input_compatibility_api_change(mapdl):
    """This test is because the API change happened in 0.65 to homogenise the APDL command
    with the gRPC method."""

    with pytest.raises(ValueError, match="Only strings are allowed in 'ext'"):
        mapdl.input(ext=1)

    with pytest.raises(ValueError, match="Only strings are allowed in 'dir_'"):
        mapdl.input(dir_=1)

    with pytest.raises(ValueError, match="A file name must be supplied."):
        mapdl.input()


@requires("grpc")
@requires("local")
def test__check_stds(mapdl):
    """Test that the standard input is checked."""

    mapdl._read_stds()
    assert mapdl._stdout is not None
    assert mapdl._stderr is not None
