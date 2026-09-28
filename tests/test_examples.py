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
import re
from subprocess import PIPE, STDOUT, Popen
from unittest.mock import patch

import pytest

from ansys.mapdl.core import EXAMPLES_PATH, examples
from ansys.mapdl.core.examples.downloads import (
    _download_file,
    _download_rotor_tech_demo_vtk,
    check_directory_exist,
    delete_downloads,
    download_bracket,
    download_cfx_mapping_example_data,
    download_example_data,
    download_manifold_example_data,
    download_tech_demo_data,
    download_vtk_rotor,
    get_ext,
)
from conftest import requires

DUMMY_PATH = "/dummy/download/path"


def test_check_directory_exist(tmpdir):
    tmp_dir = os.path.join(tmpdir, "mytempdir")

    assert not os.path.exists(tmp_dir)

    @check_directory_exist(tmp_dir)
    def myfunc():
        return "Directory should exist after this"

    assert not os.path.exists(tmp_dir)

    assert myfunc()
    assert os.path.exists(tmp_dir)


@pytest.mark.parametrize(
    "filename,ext",
    (
        ["asdf/adfasdf/asdfaf.tt", ".tt"],
        ["asdfadf/asdfasfdasf", ""],
        ["asdfsadf.qerq", ".qerq"],
    ),
)
def test_get_ext(filename, ext):
    assert get_ext(filename) == ext


def test_delete_downloads():
    if not os.path.exists(EXAMPLES_PATH):
        os.mkdir(EXAMPLES_PATH)

    # Check we can delete the folder with files even.
    file_path = os.path.join(EXAMPLES_PATH, "myfile")
    with open(file_path, "w") as fid:
        fid.write("dummy file")

    delete_downloads()
    assert not os.path.exists(EXAMPLES_PATH)
    assert not os.path.exists(file_path)


def test_load_verif():
    for filename in examples.vmfiles.values():
        assert os.path.isfile(filename)


@requires("requests")
def test_bracket(mapdl, cleared):
    # note that this method just returns a file path
    bracket_file = examples.download_bracket()

    assert os.path.isfile(bracket_file)

    # load the bracket and then print out the geometry
    mapdl.aux15()
    out = mapdl.igesin(bracket_file)
    n_ent = re.findall(r"TOTAL NUMBER OF ENTITIES \s*=\s*(\d*)", out)
    assert int(n_ent[0]) > 0


@requires("requests")
def test_download_example_data_true_download():
    path = download_example_data("LatheCutter.anf", "geometry")
    assert os.path.exists(path)


@requires("requests")
def test_failed_download():
    # ansys.tools.common.example_download.DownloadManager raises RuntimeError
    # (rather than requests.exceptions.HTTPError) on download failures.
    filename = "non_existing_file"
    with pytest.raises(RuntimeError):
        _download_file(filename, directory=None)


@requires("ansys.tools.common")
def test_retrieve_file_skips_download_when_already_cached():
    from ansys.mapdl.core.examples.downloads import _retrieve_file

    filename = "unique_test_cached_file.txt"
    os.makedirs(EXAMPLES_PATH, exist_ok=True)
    local_path = os.path.join(EXAMPLES_PATH, filename)

    try:
        with open(local_path, "w") as fid:
            fid.write("already downloaded")

        with patch(
            "ansys.mapdl.core.examples.downloads.download_manager"
        ) as mock_manager:
            result = _retrieve_file(filename, "some/dir")

        mock_manager.download_file.assert_not_called()
        assert result == local_path
    finally:
        if os.path.isfile(local_path):
            os.remove(local_path)


@requires("ansys.tools.common")
def test_retrieve_file_uses_examples_path_as_destination():
    from ansys.mapdl.core.examples.downloads import _retrieve_file

    filename = "unique_test_destination_file.txt"
    expected_local_path = os.path.join(EXAMPLES_PATH, filename)

    with patch("ansys.mapdl.core.examples.downloads.download_manager") as mock_manager:
        mock_manager.download_file.return_value = expected_local_path

        result = _retrieve_file(filename, "some/dir")

        mock_manager.download_file.assert_called_once_with(
            filename=filename,
            directory="some/dir",
            destination=EXAMPLES_PATH,
        )
        assert result == expected_local_path


@requires("ansys.tools.common")
def test_retrieve_file_decompresses_zip(tmp_path):
    import shutil
    import zipfile

    from ansys.mapdl.core.examples.downloads import _retrieve_file

    zip_name = "unique_test_archive.zip"
    os.makedirs(EXAMPLES_PATH, exist_ok=True)
    zip_local_path = os.path.join(EXAMPLES_PATH, zip_name)

    # `_decompress` extracts the archive contents directly into
    # `EXAMPLES_PATH`, so the archive must contain a top-level entry
    # matching the zip's own name (minus the ".zip" extension) for the
    # returned path to resolve to an extracted directory.
    inner_file = tmp_path / "inner.txt"
    inner_file.write_text("hello")
    with zipfile.ZipFile(zip_local_path, "w") as zip_ref:
        zip_ref.write(inner_file, arcname="unique_test_archive/inner.txt")

    try:
        with patch(
            "ansys.mapdl.core.examples.downloads.download_manager"
        ) as mock_manager:
            mock_manager.download_file.return_value = zip_local_path

            result = _retrieve_file(zip_name, "some/dir")

        assert result == zip_local_path[:-4]
        assert os.path.isdir(result)
        assert os.path.isfile(os.path.join(result, "inner.txt"))
    finally:
        shutil.rmtree(zip_local_path[:-4], ignore_errors=True)
        if os.path.isfile(zip_local_path):
            os.remove(zip_local_path)


@requires("requests")
def test_download_cfx_mapping_example_data():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        result = download_cfx_mapping_example_data()
        mock_retrieve.assert_called()
        assert all(v == DUMMY_PATH for v in result.values())


@requires("requests")
def test_download_manifold_example_data():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        result = download_manifold_example_data()
        mock_retrieve.assert_called()
        assert all(v == DUMMY_PATH for v in result.values())


@requires("requests")
def test_download_bracket():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        assert download_bracket() == DUMMY_PATH
        mock_retrieve.assert_called()


@requires("requests")
def test_download_vtk_rotor():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        assert download_vtk_rotor() == DUMMY_PATH
        mock_retrieve.assert_called()


@requires("requests")
def test__download_rotor_tech_demo_vtk():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        assert _download_rotor_tech_demo_vtk() == DUMMY_PATH
        mock_retrieve.assert_called()


@requires("requests")
def test_download_example_data():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        assert download_example_data("LatheCutter.anf", "geometry") == DUMMY_PATH
        mock_retrieve.assert_called()


@requires("requests")
def test_download_tech_demo_data():
    with patch(
        "ansys.mapdl.core.examples.downloads._retrieve_file", return_value=DUMMY_PATH
    ) as mock_retrieve:
        assert (
            download_tech_demo_data("td-21", "ring_stiffened_cylinder_mesh_file.cdb")
            == DUMMY_PATH
        )
        mock_retrieve.assert_called()


@requires("requests")
def test_detach_examples_submodule():
    cmd = """
import sys

assert 'ansys.mapdl.core' not in sys.modules, 'PyMAPDL is loaded!'
assert 'requests' not in sys.modules, 'Requests is loaded!'
assert 'ansys.mapdl.core.examples' not in sys.modules, 'Examples is loaded!'

from ansys.mapdl import core as pymapdl

assert 'ansys.mapdl.core' in sys.modules, 'PyMAPDL is not loaded!'
assert 'ansys.mapdl.core.examples' not in sys.modules, 'Examples is loaded!'

from ansys.mapdl.core.examples import vmfiles

assert 'ansys.mapdl.core.examples' in sys.modules, 'examples is not loaded!'
assert 'requests' in sys.modules, 'requests is not loaded!'

print('Everything went well')
""".strip().replace("\n", ";").replace(";;", ";")

    cmd_line = f"""python -c "{cmd}" """

    p = Popen(cmd_line, shell=True, stdout=PIPE, stderr=STDOUT)
    out = p.communicate()[0].decode()

    assert out.strip() == "Everything went well"

    p.kill()
    del p


def test_external_models():
    from ansys.mapdl.core.examples import examples

    for each in dir(examples):
        if each not in ["os", "dir_path"] and not each.startswith("__"):
            obj = getattr(examples, each)
