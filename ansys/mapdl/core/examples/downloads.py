"""Functions to download sampe datasets from the VTK data repository
"""
import shutil
import os
import urllib.request
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
    urlretrieve = urllib.request.urlretrieve

    # Perfrom download
    saved_file, resp = urlretrieve(url)
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
    if saved_file[-3:] == 'cdb':
        return pyansys.Archive(saved_file)
    else:
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


def _download_solid239_240():
    """SOLID239 and SOLID240 file for unit testing"""
    return _download_and_read('solid239_240.rth')


def _download_plane238():
    """PLANE result for unit testing"""
    return _download_and_read('plane238.rth')


def _download_shell181():
    """SHELL181 result for unit testing"""
    return _download_and_read('shell181.rst')


def download_corner_pipe():
    """Corner pipe result for unit testing and basic demo"""
    return _download_and_read('cyc_stress.rst')


def download_academic_rotor_result():
    """Cyclic academic rotor result file"""
    return _download_and_read('academic_rotor.rst')


def download_academic_rotor_archive():
    """Cyclic academic rotor archive file"""
    return _download_and_read('academic_rotor.cdb')


def download_academic_rotor_4blade_result():
    """Cyclic academic rotor result file"""
    return _download_and_read('academic_rotor_4_blade.rst')
