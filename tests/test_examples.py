import os
import re

import pytest

from ansys.mapdl.core import EXAMPLES_PATH, examples
from ansys.mapdl.core.examples.downloads import (
    _download_file,
    _download_rotor_tech_demo_plot,
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


def test_bracket(mapdl, cleared):
    # note that this method just returns a file path
    bracket_file = examples.download_bracket()
    assert os.path.isfile(bracket_file)

    # load the bracket and then print out the geometry
    mapdl.aux15()
    out = mapdl.igesin(bracket_file)
    n_ent = re.findall(r"TOTAL NUMBER OF ENTITIES \s*=\s*(\d*)", out)
    assert int(n_ent[0]) > 0


def test_download_example_data_true_download():
    path = download_example_data("LatheCutter.anf", "geometry")
    assert os.path.exists(path)


def test_failed_download():
    filename = "non_existing_file"
    with pytest.raises(RuntimeError):
        _download_file(filename, directory=None)


def test_download_cfx_mapping_example_data(running_test):
    with running_test:
        assert all(download_cfx_mapping_example_data().values())


def test_download_manifold_example_data(running_test):
    with running_test:
        assert all(download_manifold_example_data().values())


def test_download_bracket(running_test):
    with running_test:
        assert download_bracket() is True


def test_download_vtk_rotor(running_test):
    with running_test:
        assert download_vtk_rotor() is True


def test__download_rotor_tech_demo_plot(running_test):
    with running_test:
        assert _download_rotor_tech_demo_plot() is True


def test_download_example_data(running_test):
    with running_test:
        assert download_example_data("LatheCutter.anf", "geometry") is True


def test_download_tech_demo_data(running_test):
    with running_test:
        assert (
            download_tech_demo_data("td-21", "ring_stiffened_cylinder_mesh_file.cdb")
            is True
        )
