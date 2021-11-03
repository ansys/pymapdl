"""Functions to download sample datasets from the pyansys data repository.
"""
import shutil
import os
import urllib.request
import zipfile

from ansys.mapdl import core as pymapdl


def get_ext(filename):
    """Extract the extension of the filename"""
    ext = os.path.splitext(filename)[1].lower()
    return ext


def delete_downloads():
    """Delete all downloaded examples to free space or update the files"""
    shutil.rmtree(pymapdl.EXAMPLES_PATH)
    os.makedirs(pymapdl.EXAMPLES_PATH)
    return True


def _decompress(filename):
    zip_ref = zipfile.ZipFile(filename, "r")
    zip_ref.extractall(pymapdl.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(filename, directory=None):
    if directory:
        return (
            f"https://github.com/pyansys/example-data/raw/master/{directory}/{filename}"
        )
    return f"https://github.com/pyansys/example-data/raw/master/{filename}"


def _retrieve_file(url, filename):
    # First check if file has already been downloaded
    local_path = os.path.join(pymapdl.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace(".zip", "")
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip, None

    # grab the correct url retriever
    urlretrieve = urllib.request.urlretrieve

    # Perform download
    saved_file, resp = urlretrieve(url)
    shutil.move(saved_file, local_path)
    if get_ext(local_path) in [".zip"]:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path, resp


def _download_file(filename, directory=None):
    url = _get_file_url(filename, directory)
    return _retrieve_file(url, filename)


def download_bracket():
    """Download an IGS bracket.

    Examples
    --------
    >>> from ansys.mapdl.core import examples
    >>> filename = examples.download_bracket()
    >>> filename
    '/home/user/.local/share/ansys_mapdl_core/examples/bracket.iges'

    """
    return _download_file("bracket.iges", "geometry")[0]


def download_tech_demo_data(example, filename):
    """Download Tech Demos external data."""
    example = 'tech_demos/' + example
    return _download_file(filename=filename, directory=example)[0]


def download_vtk_rotor():
    """Download rotor vtk file."""
    return _download_file("rotor.vtk", "geometry")[0]


def _download_rotor_tech_demo_plot():
    """Download rotor surface vtk file."""
    return _download_file("rotor2.vtk", "geometry")[0]
