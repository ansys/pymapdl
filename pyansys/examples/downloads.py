"""Functions to download sampe datasets from the VTK data repository
"""
import shutil
import os
import sys
import zipfile

import pyansys


def get_ext(filename):
    """Extract the extension of the filename"""
    ext = os.path.splitext(filename)[1].lower()
    return ext


def delete_downloads():
    """Delete all downloaded examples to free space or update the files"""
    shutil.rmtree(pyansys.EXAMPLES_PATH)
    os.makedirs(pyansys.EXAMPLES_PATH)
    return True


def _decompress(filename):
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(pyansys.EXAMPLES_PATH)
    return zip_ref.close()


def _get_vtk_file_url(filename):
    return 'https://github.com/akaszynski/pyansys-data/raw/master/data/{}'.format(filename)


def _retrieve_file(url, filename):
    # First check if file has already been downloaded
    local_path = os.path.join(pyansys.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace('.zip', '')
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip, None
    # grab the correct url retriever
    if sys.version_info < (3,):
        import urllib
        urlretrieve = urllib.urlretrieve
    else:
        import urllib.request
        urlretrieve = urllib.request.urlretrieve
    # Perfrom download
    saved_file, resp = urlretrieve(url)
    # new_name = saved_file.replace(os.path.basename(saved_file), os.path.basename(filename))
    shutil.move(saved_file, local_path)
    if get_ext(local_path) in ['.zip']:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path, resp


def download_file(filename):
    return _download_file(filename)

def _download_file(filename):
    url = _get_vtk_file_url(filename)
    return _retrieve_file(url, filename)


def _download_and_read(filename):
    saved_file, _ = _download_file(filename)
    return pyansys.read_binary(saved_file)


###############################################################################
def download_verification_result(index):
    """Download a verification manual result file"""
    return _download_and_read('vm%d.rst' % index)


def download_shaft_modal():
    """Download modal analysis of a rotor shaft"""
    return _download_and_read('shaft_modal.rst')


def download_sector_modal():
    """Download modal analysis of a cyclic turbine sector"""
    return _download_and_read('sector_modal.rst')


def download_pontoon():
    """Download modal analysis of a cyclic turbine sector"""
    return _download_and_read('pontoon.rst')
