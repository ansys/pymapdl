"""Functions to download sample datasets from the pymapdl data repository
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
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(pymapdl.EXAMPLES_PATH)
    return zip_ref.close()


def _get_file_url(filename):
    return f'https://github.com/akaszynski/pyansys-data/raw/master/data/{filename}'


def _retrieve_file(url, filename):
    # First check if file has already been downloaded
    local_path = os.path.join(pymapdl.EXAMPLES_PATH, os.path.basename(filename))
    local_path_no_zip = local_path.replace('.zip', '')
    if os.path.isfile(local_path_no_zip) or os.path.isdir(local_path_no_zip):
        return local_path_no_zip, None

    # grab the correct url retriever
    urlretrieve = urllib.request.urlretrieve

    # Perform download
    saved_file, resp = urlretrieve(url)
    shutil.move(saved_file, local_path)
    if get_ext(local_path) in ['.zip']:
        _decompress(local_path)
        local_path = local_path[:-4]
    return local_path, resp


def download_file(filename):
    return _download_file(filename)


def _download_file(filename):
    url = _get_file_url(filename)
    return _retrieve_file(url, filename)


def _download_and_read(filename):
    saved_file, _ = _download_file(filename)
    if saved_file[-3:] == 'cdb':
        return pymapdl.Archive(saved_file)
    else:
        return pymapdl.read_binary(saved_file)


###############################################################################
# def download_verification_result(index):
#     """Download a verification manual result file"""
#     return _download_and_read('vm%d.rst' % index)
