# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""Functions to download sample datasets from the pyansys data repository.
"""
from functools import wraps
import os
import shutil
from typing import Callable, Dict, Optional
import zipfile

from ansys.mapdl import core as pymapdl
from ansys.mapdl.core import _HAS_REQUESTS

if _HAS_REQUESTS:
    import requests


def check_directory_exist(directory: str) -> Callable:
    # Wrapping LISTING FUNCTIONS.
    def wrap_function(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # Check if folder exists
            if not os.path.exists(directory):
                os.makedirs(directory)

            return func(*args, **kwargs)

        return inner_wrapper

    return wrap_function


def get_ext(filename: str) -> str:
    """Extract the extension of the filename"""
    ext = os.path.splitext(filename)[1].lower()
    return ext


def delete_downloads() -> bool:
    """Delete all downloaded examples to free space or update the files"""
    if os.path.exists(pymapdl.EXAMPLES_PATH):
        shutil.rmtree(pymapdl.EXAMPLES_PATH)
    return True


@check_directory_exist(pymapdl.EXAMPLES_PATH)
def _decompress(filename: str) -> None:
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(pymapdl.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(filename: str, directory: Optional[str] = None) -> str:
    if directory:
        return (
            f"https://github.com/ansys/example-data/raw/master/{directory}/{filename}"
        )
    return f"https://github.com/ansys/example-data/raw/master/{filename}"


def _check_url_exist(url: str) -> bool:
    response = requests.get(url, timeout=10)  # 10 seconds timeout
    return response.status_code == 200


@check_directory_exist(pymapdl.EXAMPLES_PATH)
def _retrieve_file(url: str, filename: str, _test: bool = False) -> str:
    # escape test
    if pymapdl.RUNNING_TESTS:
        return _check_url_exist(url)

    # First check if file has already been downloaded
    local_path = os.path.join(pymapdl.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip

    # Perform download
    requested_file = requests.get(url, timeout=10)
    requested_file.raise_for_status()

    with open(local_path, "wb") as f:
        f.write(requested_file.content)

    if get_ext(local_path) in [".zip"]:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path


def _download_file(
    filename: str, directory: Optional[str] = None, _test: Optional[bool] = False
) -> str:
    url = _get_file_url(filename, directory)
    try:
        return _retrieve_file(url, filename, _test)
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(
            "Retrieving the file from internet failed.\n"
            "You can download this file from:\n"
            f"{url}\n"
            "\n"
            "The reported error message is:\n"
            f"{str(e)}"
        )


def download_bracket() -> str:
    """Download an IGS bracket.

    Examples
    --------
    >>> from ansys.mapdl.core import examples
    >>> filename = examples.download_bracket()
    >>> filename
    '/home/user/.local/share/ansys_mapdl_core/examples/bracket.iges'

    """
    return _download_file("bracket.iges", "geometry")


def download_tech_demo_data(example: str, filename: str) -> str:
    """Download Tech Demos external data."""
    example = "tech_demos/" + example
    return _download_file(filename=filename, directory=example)


def download_vtk_rotor() -> str:
    """Download rotor vtk file."""
    return _download_file("rotor.vtk", "geometry")


def _download_rotor_tech_demo_vtk() -> str:
    """Download the rotor surface VTK file."""
    return _download_file("rotor2.vtk", "geometry")


def download_example_data(filename: str, directory: Optional[str] = None) -> str:
    return _download_file(filename, directory=directory)


def download_manifold_example_data() -> Dict[str, str]:
    """Download the manifold example data and return the
    download paths into a dictionary domain id->path.
    Examples files are downloaded to a persistent cache to avoid
    re-downloading the same file twice.

    Returns
    -------
    dict[str:str]
        Path to the example files.

    Examples
    --------
    Download the manifold geometry, ans file and return the path of the file
    >>> from ansys.mapdl.core.examples.downloads import download_manifold_example_data
    >>> paths = download_manifold_example_data()
    >>> paths
    {geometry: 'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\examples\\manifold_geometry.anf',
     mapping_data: 'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\examples\\manifold_cht-final_temp.csv'}
    """

    files_dir = "pymapdl/manifold"
    return {
        "geometry": _download_file(
            filename="manifold_geometry.anf", directory=files_dir
        ),
        "mapping_data": _download_file(
            filename="manifold_cht-final_temp.csv", directory=files_dir
        ),
    }


def download_cfx_mapping_example_data() -> Dict[str, str]:
    """Download the CFX mapping data and return the
    download paths into a dictionary domain id->path.
    Examples files are downloaded to a persistent cache to avoid
    re-downloading the same file twice.

    Returns
    -------
    dict[str:str]
        Path to the example files.

    Examples
    --------
    >>> from ansys.mapdl.core.examples.downloads import download_cfx_mapping_example_data
    >>> paths = download_cfx_mapping_example_data()
    >>> paths
    {data: 'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\examples\\11_blades_mode_1_ND_0.csv',
     model: 'C:\\Users\\user\\AppData\\Local\\ansys_mapdl_core\\ansys_mapdl_core\\examples\\ExampleMapping.db'}
    """

    files_dir = "pymapdl/cfx_mapping"
    return {
        "data": _download_file(
            filename="11_blades_mode_1_ND_0.csv", directory=files_dir
        ),
        "model": _download_file(filename="ExampleMapping.db", directory=files_dir),
    }
