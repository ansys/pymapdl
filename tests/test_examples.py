import os
import re

import pytest

from ansys.mapdl.core import examples
from ansys.mapdl.core.examples.downloads import (
    _download_file,
    _download_rotor_tech_demo_plot,
    download_bracket,
    download_cfx_mapping_example_data,
    download_example_data,
    download_manifold_example_data,
    download_tech_demo_data,
    download_vtk_rotor,
)


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


def test_download_example_data():
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
